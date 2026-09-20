#!/usr/bin/env python3
"""Compile bounded professional candidate receipts and read back project closure objects.

This is a non-authority projection.  It may derive a candidate receipt from an
existing DOMAIN_PROCESS_INSTANCE, verify source bytes and report PASS readiness,
but it never emits an overall professional PASS.  An authorized downstream
professional/review transition remains separate.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "00-governance" / "schemas"
COMPILER_REF = "00-governance/runtime/compile_project_receipts.py"
COMPILER_SCHEMA = SCHEMA_DIR / "project-receipt-compiler.v1.schema.json"
TEXT_HASH_SEMANTICS = "UTF8_TEXT_LF_CANONICAL_V1"
BINARY_HASH_SEMANTICS = "RAW_BYTES_V1"
TEXT_EXTENSIONS = {
    ".json", ".md", ".py", ".txt", ".yaml", ".yml", ".csv", ".tsv",
    ".svg", ".html", ".htm", ".css", ".js", ".mjs", ".cjs", ".ts",
    ".tsx", ".jsx", ".xml", ".toml", ".ini", ".cfg", ".gitattributes",
    ".gitignore",
}


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise RuntimeError(f"cannot load module {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


PROCESS_VALIDATOR = _load_module(
    "oleander_professional_process_validator",
    SCHEMA_DIR / "validate_professional_domain_process.py",
)
CLOSURE_VALIDATOR = _load_module(
    "oleander_project_closure_validator",
    SCHEMA_DIR / "validate_project_closure_objects.py",
)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical_hash_bytes(path: Path, data: bytes | None = None) -> tuple[bytes, str]:
    """Return checkout-stable bytes plus an explicit digest semantic.

    Git text checkouts can differ only by CRLF/LF depending on platform and
    core.autocrlf.  For known UTF-8 text formats, hash a single canonical LF
    representation.  Binary/unknown formats retain exact raw-byte identity.
    """
    raw = path.read_bytes() if data is None else data
    suffix = path.suffix.lower()
    text_named = suffix in TEXT_EXTENSIONS or path.name.lower() in {
        "readme", "license", ".gitattributes", ".gitignore"
    }
    if text_named:
        try:
            text = raw.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError(f"declared text file is not UTF-8: {path}") from exc
        normalized = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
        return normalized, TEXT_HASH_SEMANTICS
    return raw, BINARY_HASH_SEMANTICS


def hash_file(path: Path, data: bytes | None = None) -> dict[str, Any]:
    canonical, semantics = canonical_hash_bytes(path, data)
    return {
        "sha256": sha256_bytes(canonical),
        "bytes": len(canonical),
        "hash_semantics": semantics,
    }


def sha256_file(path: Path) -> str:
    return str(hash_file(path)["sha256"])


def display_path(path: Path) -> str:
    """Persist repository paths portably; preserve real external source paths."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def _validate_contract(payload: dict[str, Any]) -> list[str]:
    try:
        import jsonschema  # type: ignore
    except ImportError:
        required = {
            "PROFESSIONAL_RECEIPT_COMPILATION_REQUEST": {
                "object_type", "schema_version", "compilation_id", "project_id",
                "target_receipt_type", "process_instance_ref", "process_instance_sha256",
                "process_instance_hash_semantics",
                "source_revision", "claim_ceiling", "requested_result", "output_ref", "readback_ref",
            },
            "PROJECT_CLOSURE_READBACK_REQUEST": {
                "object_type", "schema_version", "compilation_id", "project_id", "object_refs", "readback_ref",
            },
        }.get(payload.get("object_type"), set())
        return [f"missing required field: {k}" for k in sorted(required - set(payload))]
    schema = load_json(COMPILER_SCHEMA)
    validator = jsonschema.Draft202012Validator(schema)
    return [
        f"{'.'.join(str(x) for x in err.path) or '$'}: {err.message}"
        for err in sorted(validator.iter_errors(payload), key=lambda e: list(e.path))
    ]


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Write canonical UTF-8/LF bytes directly.  Text-mode writes on Windows can
    # translate LF to CRLF and make generated artifacts appear dirty after a
    # clean checkout even though canonical digest identity is unchanged.
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    # Do not rewrite an identical generated artifact.  On Git for Windows,
    # changing only mtime/stat metadata can leave a false dirty signal even
    # when raw and filtered blob identity are exactly unchanged.
    if path.is_file():
        existing = path.read_bytes()
        canonical_existing, semantics = canonical_hash_bytes(path, existing)
        if semantics == TEXT_HASH_SEMANTICS and canonical_existing == data:
            return
        if semantics == BINARY_HASH_SEMANTICS and existing == data:
            return
    path.write_bytes(data)


def _path_from_ref(ref: str) -> str:
    return ref.split("#", 1)[0].strip()


def _root_paths(request: dict[str, Any], request_path: Path) -> list[Path]:
    roots = [ROOT, request_path.parent]
    for item in request.get("source_roots") or []:
        raw = str(item.get("path") or "")
        if not raw:
            continue
        p = Path(raw)
        if not p.is_absolute():
            p = ROOT / p
        roots.append(p)
    unique: list[Path] = []
    seen: set[str] = set()
    for root in roots:
        key = str(root)
        if key not in seen:
            seen.add(key)
            unique.append(root)
    return unique


def resolve_ref(ref: str, roots: list[Path]) -> tuple[str, Path | None]:
    raw = _path_from_ref(ref)
    if not raw:
        return "UNRESOLVED", None
    direct = Path(raw)
    if direct.is_absolute() and direct.is_file():
        return "RESOLVED", direct
    candidates: list[Path] = []
    for root in roots:
        p = root / raw
        if p.is_file():
            candidates.append(p)
    if not candidates and "/" not in raw and "\\" not in raw:
        for root in roots:
            if not root.is_dir():
                continue
            try:
                matches = list(root.rglob(raw))
            except (OSError, PermissionError):
                matches = []
            candidates.extend(p for p in matches if p.is_file())
    unique = list(dict.fromkeys(str(p.resolve()) for p in candidates))
    if len(unique) == 1:
        return "RESOLVED", Path(unique[0])
    if len(unique) > 1:
        return "AMBIGUOUS", None
    return "UNRESOLVED", None


def source_readback(ref: str, roots: list[Path]) -> dict[str, Any]:
    state, path = resolve_ref(ref, roots)
    if path is None:
        return {
            "ref": ref,
            "resolution_state": state,
            "resolved_path": None,
            "observed_sha256": None,
            "bytes": None,
            "hash_semantics": None,
        }
    observed = hash_file(path)
    return {
        "ref": ref,
        "resolution_state": state,
        "resolved_path": display_path(path),
        "observed_sha256": observed["sha256"],
        "bytes": observed["bytes"],
        "hash_semantics": observed["hash_semantics"],
    }


def _collect_stage_source_refs(instance: dict[str, Any], request: dict[str, Any]) -> list[str]:
    refs = [str(request["process_instance_ref"])]
    for stage in instance.get("stage_instances") or []:
        for field in ("evidence_refs", "review_refs", "actual_readback_refs"):
            refs.extend(str(x) for x in stage.get(field) or [])
        for binding in stage.get("output_execution_bindings") or []:
            refs.extend(str(x) for x in binding.get("artifact_refs") or [])
            refs.extend(str(x) for x in binding.get("readback_refs") or [])
    for row in request.get("interface_records") or []:
        refs.extend(str(x) for x in row.get("evidence_refs") or [])
    for row in request.get("mep_system_tracks") or []:
        refs.extend(str(x) for x in row.get("design_refs") or [])
        refs.extend(str(x) for x in row.get("evidence_refs") or [])
    basis = request.get("basis_of_structural_design_ref")
    if basis:
        refs.append(str(basis))
    return list(dict.fromkeys(x for x in refs if x))


def _stage_status(stage: dict[str, Any]) -> str:
    state = str(stage.get("execution_state") or "")
    verdict = str(stage.get("review_verdict") or "NOT_RUN")
    exit_state = str(stage.get("exit_condition_state") or "NOT_EVALUATED")
    if state == "STALE" or stage.get("stale_scope"):
        return "STALE"
    if verdict == "REJECT":
        return "REJECT"
    if verdict == "REVISE":
        return "REVISE"
    if state == "BLOCKED" or verdict == "HOLD" or exit_state == "BLOCKED":
        return "HOLD"
    if state in {"CLOSED", "CURRENT"} and verdict == "PASS" and exit_state == "SATISFIED":
        return "PASS"
    if state in {"NOT_STARTED", "READY"}:
        return "PENDING"
    return "IN_PROGRESS"


def _stage_artifacts(stage: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    for binding in stage.get("output_execution_bindings") or []:
        if binding.get("resolution_state") in {"EXECUTED", "READBACK_COMPLETE"}:
            refs.extend(str(x) for x in binding.get("artifact_refs") or [])
    return list(dict.fromkeys(refs))


def _stage_readbacks(stage: dict[str, Any]) -> list[str]:
    refs = [str(x) for x in stage.get("actual_readback_refs") or []]
    for binding in stage.get("output_execution_bindings") or []:
        if binding.get("resolution_state") == "READBACK_COMPLETE":
            refs.extend(str(x) for x in binding.get("readback_refs") or [])
    return list(dict.fromkeys(refs))


def _review_state(instance: dict[str, Any]) -> str:
    stages = instance.get("stage_instances") or []
    if not stages:
        return "NOT_RUN"
    verdicts = {str(stage.get("review_verdict") or "NOT_RUN") for stage in stages}
    if "REJECT" in verdicts:
        return "FAIL"
    if "HOLD" in verdicts:
        return "HOLD"
    if "REVISE" in verdicts:
        return "HOLD"
    if verdicts == {"PASS"} and all(stage.get("review_refs") for stage in stages):
        return "PASS"
    return "NOT_RUN"


def _compile_stage_rows(instance: dict[str, Any], structural: bool) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stage in instance.get("stage_instances") or []:
        row = {
            "stage_id": stage["stage_id"],
            "triggered": True,
            "status": _stage_status(stage),
            "knowledge_mount_refs": [str(x) for x in stage.get("knowledge_mount_refs") or []],
            "native_output_refs": _stage_artifacts(stage),
            "actual_readback_refs": _stage_readbacks(stage),
            "open_items": [str(x) for x in stage.get("open_items") or []],
        }
        if structural:
            review_state = _review_state({"stage_instances": [stage]})
            row["checking_state"] = review_state if review_state in {"NOT_RUN", "PASS", "FAIL", "HOLD"} else "HOLD"
            row["interface_state"] = "NOT_REQUIRED" if not stage.get("interface_refs") else "HOLD"
        rows.append(row)
    return rows


def _candidate_blockers(instance: dict[str, Any], source_integrity: str) -> list[str]:
    blockers = [str(x) for x in instance.get("open_items") or []]
    if instance.get("execution_state") == "STALE" or instance.get("stale_scope"):
        blockers.append("PROCESS_INSTANCE_STALE")
    if source_integrity != "PASS":
        blockers.append("SOURCE_INTEGRITY_READBACK_HOLD")
    return list(dict.fromkeys(blockers))


def _build_professional_receipt(request: dict[str, Any], instance: dict[str, Any], source_integrity: str) -> dict[str, Any]:
    target = request["target_receipt_type"]
    requested = request["requested_result"]
    stage_rows = _compile_stage_rows(instance, target == "STRUCTURAL_ENGINEERING_DESIGN_PROCESS_RECEIPT")
    interface_records = [dict(x) for x in request.get("interface_records") or []]
    blockers = _candidate_blockers(instance, source_integrity)
    if any(row.get("status") != "PASS" for row in stage_rows):
        blockers.append("ONE_OR_MORE_TRIGGERED_STAGES_NOT_PASS")
    if any(row.get("required") and row.get("state") != "PASS" for row in interface_records):
        blockers.append("REQUIRED_INTERFACE_NOT_PASS")

    review_binding = request.get("review_binding") or {}
    review_state = _review_state(instance)
    reviewer_ref = review_binding.get("reviewer_ref")
    review_refs = list(dict.fromkeys(
        str(x)
        for stage in instance.get("stage_instances") or []
        for x in stage.get("review_refs") or []
    ))
    if review_binding.get("required") and (review_state != "PASS" or not reviewer_ref):
        blockers.append("REQUIRED_PROFESSIONAL_REVIEW_NOT_CLOSED")

    common = {
        "schema_version": "1.0",
        "project_id": request["project_id"],
        "workstream_id": request.get("workstream_id"),
        "source_revision": request["source_revision"],
        "claim_ceiling": request["claim_ceiling"],
        "stage_records": stage_rows,
        "interface_summary": interface_records,
        "blocking_open_items": list(dict.fromkeys(blockers)),
        "open_items": [str(x) for x in instance.get("open_items") or []],
        "reopened_items": [str(x) for x in instance.get("reopen_events") or []],
        "stale": bool(instance.get("execution_state") == "STALE" or instance.get("stale_scope")),
        "result": requested if requested != "PASS" else "HOLD",
        "does_not_prove": list(dict.fromkeys([
            *[str(x) for x in request.get("does_not_prove") or []],
            "compiler-granted professional PASS",
            "professional/statutory approval beyond explicit source evidence",
        ])),
    }
    if requested == "PASS":
        common["blocking_open_items"] = list(dict.fromkeys([
            *common["blocking_open_items"],
            "COMPILER_CANNOT_GRANT_PROFESSIONAL_PASS; AUTHORIZED REVIEW/ADOPTION REQUIRED",
        ]))

    if target == "STRUCTURAL_ENGINEERING_DESIGN_PROCESS_RECEIPT":
        return {
            "receipt_type": target,
            **common,
            "process_ref": "00-governance/schemas/structural-engineering-design-process.v1.json",
            "basis_of_structural_design_ref": request.get("basis_of_structural_design_ref") or "NOT_ESTABLISHED_FROM_CURRENT_PROCESS_INSTANCE",
            "analysis_model_refs": [],
            "calculation_drawing_trace_refs": [],
            "field_shop_change_refs": [],
            "independent_check": {
                "required": bool(review_binding.get("required")),
                "state": review_state if review_binding.get("required") else "NOT_REQUIRED",
                "reviewer_ref": reviewer_ref,
                "review_input_refs": review_refs,
            },
        }
    return {
        "receipt_type": target,
        **common,
        "process_ref": "00-governance/schemas/building-services-mep-design-process.v1.json",
        "system_tracks": [dict(x) for x in request.get("mep_system_tracks") or []],
        "professional_review": {
            "required": bool(review_binding.get("required")),
            "state": review_state if review_binding.get("required") else "NOT_REQUIRED",
            "reviewer_ref": reviewer_ref,
            "review_input_refs": review_refs,
        },
    }


def _pass_candidate(receipt: dict[str, Any], request: dict[str, Any], source_integrity: str) -> tuple[str, list[str]]:
    if request.get("requested_result") != "PASS":
        return "NOT_REQUESTED", []
    if source_integrity != "PASS":
        return "HOLD", ["SOURCE_INTEGRITY_READBACK_HOLD"]
    candidate = json.loads(json.dumps(receipt))
    candidate["result"] = "PASS"
    candidate["blocking_open_items"] = [
        x for x in candidate.get("blocking_open_items") or []
        if not x.startswith("COMPILER_CANNOT_GRANT_PROFESSIONAL_PASS")
    ]
    candidate["blocking_open_items"] = [
        x for x in candidate["blocking_open_items"]
        if x not in {"ONE_OR_MORE_TRIGGERED_STAGES_NOT_PASS", "REQUIRED_INTERFACE_NOT_PASS", "REQUIRED_PROFESSIONAL_REVIEW_NOT_CLOSED"}
    ]
    errors = CLOSURE_VALIDATOR.validate_payload(candidate)
    if errors:
        return "HOLD", [f"PASS_CANDIDATE:{x}" for x in errors]
    return "READY_FOR_AUTHORIZED_REVIEW", []


def _resolve_request_path(ref: str, request_path: Path) -> Path:
    p = Path(ref)
    if p.is_absolute():
        return p
    repo_candidate = ROOT / p
    if repo_candidate.exists() or str(ref).startswith("00-") or str(ref).startswith("05-"):
        return repo_candidate
    return request_path.parent / p


def compile_professional(request_path: Path) -> tuple[Path, Path, dict[str, Any]]:
    request = load_json(request_path)
    errors = _validate_contract(request)
    if errors:
        raise ValueError("invalid compilation request: " + "; ".join(errors))
    instance_path = _resolve_request_path(str(request["process_instance_ref"]), request_path)
    if not instance_path.is_file():
        raise FileNotFoundError(instance_path)
    instance_bytes = instance_path.read_bytes()
    observed_instance = hash_file(instance_path, instance_bytes)
    observed_instance_sha = observed_instance["sha256"]
    instance = json.loads(instance_bytes.decode("utf-8"))
    process_errors = PROCESS_VALIDATOR.validate_payload(instance)

    roots = _root_paths(request, request_path)
    source_objects = [source_readback(ref, roots) for ref in _collect_stage_source_refs(instance, request)]
    hold_reasons: list[str] = []
    if observed_instance_sha.upper() != str(request["process_instance_sha256"]).upper():
        hold_reasons.append("PROCESS_INSTANCE_SHA256_MISMATCH")
    if request.get("process_instance_hash_semantics") != observed_instance["hash_semantics"]:
        hold_reasons.append("PROCESS_INSTANCE_HASH_SEMANTICS_MISMATCH")
    if process_errors:
        hold_reasons.extend(f"PROCESS_INSTANCE:{x}" for x in process_errors)
    unresolved = [x for x in source_objects if x["resolution_state"] != "RESOLVED"]
    required_root_missing = []
    for item in request.get("source_roots") or []:
        p = Path(str(item.get("path") or ""))
        if not p.is_absolute():
            p = ROOT / p
        if item.get("required_for_pass") and not p.exists():
            required_root_missing.append(str(p))
    if unresolved:
        hold_reasons.append("ONE_OR_MORE_SOURCE_REFS_UNRESOLVED_OR_AMBIGUOUS")
    if required_root_missing:
        hold_reasons.append("REQUIRED_SOURCE_ROOT_UNAVAILABLE")
    source_integrity = "PASS" if not hold_reasons else "HOLD"

    receipt = _build_professional_receipt(request, instance, source_integrity)
    receipt_errors = CLOSURE_VALIDATOR.validate_payload(receipt)
    schema_validation_state = "PASS" if not receipt_errors else "HOLD"
    if receipt_errors:
        hold_reasons.extend(f"EMITTED_RECEIPT:{x}" for x in receipt_errors)
        receipt["result"] = "HOLD"
        receipt["blocking_open_items"] = list(dict.fromkeys([
            *receipt.get("blocking_open_items", []),
            "EMITTED_RECEIPT_VALIDATION_HOLD",
        ]))

    pass_readiness, readiness_reasons = _pass_candidate(receipt, request, source_integrity)
    hold_reasons.extend(readiness_reasons)

    output_path = _resolve_request_path(str(request["output_ref"]), request_path)
    readback_path = _resolve_request_path(str(request["readback_ref"]), request_path)
    _write_json(output_path, receipt)
    request_hash = hash_file(request_path)
    output_hash = hash_file(output_path)
    compiler_hash = hash_file(Path(__file__))
    readback = {
        "object_type": "PROJECT_RECEIPT_COMPILATION_READBACK",
        "schema_version": "1.1",
        "compilation_id": request["compilation_id"],
        "project_id": request["project_id"],
        "mode": "PROFESSIONAL_COMPILE",
        "compiler_ref": COMPILER_REF,
        "compiler_sha256": compiler_hash["sha256"],
        "compiler_hash_semantics": compiler_hash["hash_semantics"],
        "request_ref": display_path(request_path),
        "request_sha256": request_hash["sha256"],
        "request_hash_semantics": request_hash["hash_semantics"],
        "target_receipt_type": request["target_receipt_type"],
        "source_objects": source_objects,
        "source_integrity_state": source_integrity,
        "schema_validation_state": schema_validation_state,
        "requested_result": request["requested_result"],
        "emitted_result": receipt["result"],
        "pass_readiness": pass_readiness,
        "hold_reasons": list(dict.fromkeys(hold_reasons)),
        "output_ref": display_path(output_path),
        "output_sha256": output_hash["sha256"],
        "output_hash_semantics": output_hash["hash_semantics"],
        "compiler_boundary": "DERIVED_NON_AUTHORITY_PROJECTION_NEVER_AUTO_GRANTS_PROFESSIONAL_PASS",
        "does_not_prove": list(dict.fromkeys([
            *[str(x) for x in request.get("does_not_prove") or []],
            "professional PASS",
            "authorized professional adoption",
            "field/statutory truth beyond resolved sources",
        ])),
    }
    rb_errors = _validate_contract(readback)
    if rb_errors:
        raise ValueError("compiler produced invalid readback: " + "; ".join(rb_errors))
    _write_json(readback_path, readback)
    return output_path, readback_path, readback


def _closure_ref_readback(item: dict[str, Any], request_path: Path, roots: list[Path]) -> tuple[dict[str, Any], list[str]]:
    ref = str(item["ref"])
    _, resolved_path = resolve_ref(ref, roots)
    rb = source_readback(ref, roots)
    errors: list[str] = []
    if rb["resolution_state"] != "RESOLVED" or resolved_path is None:
        errors.append(f"CLOSURE_OBJECT_UNRESOLVED:{ref}")
        return rb, errors
    path = resolved_path
    expected = item.get("expected_sha256")
    if expected and str(expected).upper() != str(rb["observed_sha256"]).upper():
        errors.append(f"CLOSURE_OBJECT_SHA256_MISMATCH:{ref}")
    if item.get("expected_hash_semantics") != rb.get("hash_semantics"):
        errors.append(f"CLOSURE_OBJECT_HASH_SEMANTICS_MISMATCH:{ref}")
    try:
        payload = load_json(path)
    except Exception as exc:  # pragma: no cover - defensive boundary
        errors.append(f"CLOSURE_OBJECT_JSON_READ_FAILED:{ref}:{exc}")
        return rb, errors
    validation_errors = CLOSURE_VALIDATOR.validate_payload(payload)
    errors.extend(f"CLOSURE_OBJECT:{ref}:{x}" for x in validation_errors)
    return rb, errors


def readback_closure_pack(request_path: Path) -> tuple[Path, dict[str, Any]]:
    request = load_json(request_path)
    errors = _validate_contract(request)
    if errors:
        raise ValueError("invalid closure readback request: " + "; ".join(errors))
    roots = _root_paths(request, request_path)
    source_objects: list[dict[str, Any]] = []
    hold_reasons: list[str] = []
    for item in request.get("object_refs") or []:
        rb, item_errors = _closure_ref_readback(item, request_path, roots)
        source_objects.append(rb)
        hold_reasons.extend(item_errors)
    state = "PASS" if not hold_reasons else "HOLD"
    compiler_hash = hash_file(Path(__file__))
    request_hash = hash_file(request_path)
    readback = {
        "object_type": "PROJECT_RECEIPT_COMPILATION_READBACK",
        "schema_version": "1.1",
        "compilation_id": request["compilation_id"],
        "project_id": request["project_id"],
        "mode": "EXISTING_CLOSURE_READBACK",
        "compiler_ref": COMPILER_REF,
        "compiler_sha256": compiler_hash["sha256"],
        "compiler_hash_semantics": compiler_hash["hash_semantics"],
        "request_ref": display_path(request_path),
        "request_sha256": request_hash["sha256"],
        "request_hash_semantics": request_hash["hash_semantics"],
        "target_receipt_type": None,
        "source_objects": source_objects,
        "source_integrity_state": state,
        "schema_validation_state": state,
        "requested_result": None,
        "emitted_result": None,
        "pass_readiness": "NOT_REQUESTED",
        "hold_reasons": list(dict.fromkeys(hold_reasons)),
        "output_ref": None,
        "output_sha256": None,
        "output_hash_semantics": None,
        "compiler_boundary": "DERIVED_NON_AUTHORITY_PROJECTION_NEVER_AUTO_GRANTS_PROFESSIONAL_PASS",
        "does_not_prove": list(dict.fromkeys([
            *[str(x) for x in request.get("does_not_prove") or []],
            "professional PASS",
            "Design KEEP",
            "field/statutory truth beyond resolved sources",
        ])),
    }
    rb_errors = _validate_contract(readback)
    if rb_errors:
        raise ValueError("compiler produced invalid readback: " + "; ".join(rb_errors))
    readback_path = _resolve_request_path(str(request["readback_ref"]), request_path)
    _write_json(readback_path, readback)
    return readback_path, readback


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    compile_cmd = sub.add_parser("compile-professional")
    compile_cmd.add_argument("request")
    readback_cmd = sub.add_parser("readback-closure")
    readback_cmd.add_argument("request")
    args = parser.parse_args(list(argv) if argv is not None else None)
    request_path = Path(args.request).resolve()
    try:
        if args.command == "compile-professional":
            output, readback, result = compile_professional(request_path)
            print(f"OUTPUT {output}")
            print(f"READBACK {readback}")
            print(f"EMITTED_RESULT={result['emitted_result']}")
            print(f"PASS_READINESS={result['pass_readiness']}")
            print(f"SOURCE_INTEGRITY={result['source_integrity_state']}")
        else:
            readback, result = readback_closure_pack(request_path)
            print(f"READBACK {readback}")
            print(f"SOURCE_INTEGRITY={result['source_integrity_state']}")
            print(f"SCHEMA_VALIDATION={result['schema_validation_state']}")
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
