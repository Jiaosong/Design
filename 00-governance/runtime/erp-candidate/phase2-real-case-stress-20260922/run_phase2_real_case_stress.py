from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


HERE = Path(__file__).resolve().parent
ERP_ROOT = HERE.parent
REPO_ROOT = HERE.parents[3]
EV3_ROOT = ERP_ROOT / "ev3-real-case-stress-20260922"
OUT = HERE / "output"
BASELINE_MAIN = "69f73a1a0e105d6797affccc0d8c09110febb345"
STAMP = "2026-09-22T17:45:00+08:00"

sys.path[:0] = [str(EV3_ROOT), str(ERP_ROOT)]

import case_c01  # noqa: E402
import case_c04  # noqa: E402
import case_fallingwater  # noqa: E402
from build_enterprise_kernel_v0_2 import build_kernel_v0_2  # noqa: E402
from reconcile_enterprise_kernel_v0_2 import reconcile_v0_2  # noqa: E402
from validate_erp_candidate import validate_projection  # noqa: E402


KERNEL_SCHEMA = json.loads((ERP_ROOT / "OLEANDER_ENTERPRISE_KERNEL_v0.2.schema.json").read_text(encoding="utf-8"))
RECON_SCHEMA = json.loads((ERP_ROOT / "OLEANDER_ENTERPRISE_RECONCILIATION_DECISION_v0.2.schema.json").read_text(encoding="utf-8"))


def canonical_text_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def build_source_rows(specs: list[tuple[str, Path, str, str]]) -> list[dict]:
    rows = []
    for ref, path, availability, semantics in specs:
        if not path.is_file():
            raise FileNotFoundError(path)
        if semantics == "GIT_CANONICAL_BLOB_SHA256":
            rel = path.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
            payload = subprocess.check_output(["git", "show", f"{BASELINE_MAIN}:{rel}"], cwd=REPO_ROOT)
            display_path = f"git:{BASELINE_MAIN}:{rel}"
        elif semantics == "RAW_BYTES_V1":
            payload = path.read_bytes()
            display_path = str(path)
        else:
            payload = canonical_text_bytes(path)
            display_path = str(path)
        rows.append({
            "ref": ref,
            "path": display_path,
            "availability": availability,
            "hash_semantics": semantics,
            "sha256": hashlib.sha256(payload).hexdigest().upper(),
            "bytes": len(payload),
        })
    return rows


def validate_schema(schema: dict, value: dict, label: str) -> None:
    errors = sorted(Draft202012Validator(schema).iter_errors(value), key=lambda e: list(e.absolute_path))
    if errors:
        first = errors[0]
        raise RuntimeError(f"{label} schema error at {'/'.join(map(str, first.absolute_path))}: {first.message}")


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def run_case(name: str, module) -> dict:
    rows = build_source_rows(module.SOURCE_SPECS)
    projection = module.build_projection(rows, ERP_ROOT / "example_enterprise_projection_v0.3.1.json")
    validate_projection(projection)
    projection_path = OUT / f"{name.lower()}_phase2_projection_v0.3.1.json"
    write_json(projection_path, projection)
    projection_payload = projection_path.read_bytes()

    kernel = build_kernel_v0_2(
        projection,
        projection_path.relative_to(REPO_ROOT).as_posix(),
        hashlib.sha256(projection_payload).hexdigest().upper(),
        STAMP,
    )
    validate_schema(KERNEL_SCHEMA, kernel, f"{name} kernel")
    kernel_path = OUT / f"{name.lower()}_phase2_kernel_v0.2.json"
    write_json(kernel_path, kernel)
    kernel_payload = kernel_path.read_bytes()

    decision = reconcile_v0_2(
        kernel,
        kernel_path.relative_to(REPO_ROOT).as_posix(),
        hashlib.sha256(kernel_payload).hexdigest().upper(),
        STAMP,
    )
    validate_schema(RECON_SCHEMA, decision, f"{name} reconciliation")
    decision_path = OUT / f"{name.lower()}_phase2_reconciliation_v0.2.json"
    write_json(decision_path, decision)

    module_bindings = {row["module"]: row for row in kernel["module_bindings"]}
    assert set(module_bindings) == {"ERP", "PLM", "MES", "BPM", "QMS", "MBSE", "KNOWLEDGE_GRAPH", "AGENT_RUNTIME"}
    assert kernel["kernel_metrics"]["unresolved_identity_ref_count"] == 0
    assert kernel["kernel_metrics"]["authority_gain_count"] == 0
    assert kernel["kernel_metrics"]["enterprise_module_binding_count"] == 8
    assert decision["advance_decision"] == "HOLD"
    assert not decision["contradictions"]
    kg_relations = [row for row in kernel["relations"] if row["relation_type"].startswith("PROVENANCE_")]
    assert all(row["authority_effect"] == "NONE" for row in kg_relations)

    blockers = {row["blocker_class"] for row in decision["blocking_conditions"]}
    if name == "C01":
        assert "MBSE_VALIDATION_INCOMPLETE" in blockers
        assert "MES_READBACK_MISSING" not in blockers
        assert module_bindings["MES"]["kernel_object_refs"]
        assert module_bindings["MBSE"]["kernel_object_refs"]
        assert module_bindings["KNOWLEDGE_GRAPH"]["kernel_object_refs"]
    elif name == "C04":
        assert "MBSE_VERIFICATION_INCOMPLETE" in blockers
        assert "MBSE_VALIDATION_INCOMPLETE" in blockers
        assert not module_bindings["MES"]["kernel_object_refs"]
        assert module_bindings["MBSE"]["kernel_object_refs"]
    elif name == "FALLINGWATER":
        assert "SOURCE_STALE" in blockers
        assert "MBSE_VALIDATION_INCOMPLETE" in blockers
        assert projection["reconciliation"]["projection_freshness_state"] == "SOURCE_READBACK_STALE"
        assert projection["reconciliation"]["drift_state"] == "DIVERGED"
        assert not projection["project_axis_refs"]

    return {
        "projection_freshness_state": projection["reconciliation"]["projection_freshness_state"],
        "drift_state": projection["reconciliation"]["drift_state"],
        "enterprise_readiness_state": projection["reconciliation"]["enterprise_readiness_state"],
        "decision": decision["advance_decision"],
        "blocker_classes": sorted(blockers),
        "blocker_count": len(decision["blocking_conditions"]),
        "action_count": len(decision["action_requests"]),
        "contradiction_count": len(decision["contradictions"]),
        "unresolved_authority_requirement_count": len(decision["unresolved_authority_requirements"]),
        "phase2_module_object_counts": {
            module_name: len(module_bindings[module_name]["kernel_object_refs"])
            for module_name in ["MES", "MBSE", "KNOWLEDGE_GRAPH", "AGENT_RUNTIME"]
        },
        "source_rows": rows,
    }


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    results = {
        "stress_test_id": "OLEANDER_ENTERPRISE_PHASE2_REAL_CASE_STRESS_20260922",
        "baseline_main_commit": BASELINE_MAIN,
        "generated_at": STAMP,
        "kernel_revision": "0.2-candidate",
        "reconciliation_revision": "0.2-candidate",
        "cases": {},
        "overall_state": "HOLD",
        "promotion_eligible": False,
        "independent_review": "NOT_RUN",
        "authority_gain_count": 0,
        "does_not_prove": [
            "CURRENT_ADOPTION", "DESIGN_KEEP", "PROFESSIONAL_PASS", "PROJECT_PROMOTION",
            "PHYSICAL_EXECUTION_ACCEPTANCE", "SYSTEMS_ENGINEERING_CURRENT", "KNOWLEDGE_CURRENT", "AGENT_MUTATION_AUTHORITY",
        ],
    }
    for name, module in [("C01", case_c01), ("C04", case_c04), ("FALLINGWATER", case_fallingwater)]:
        results["cases"][name] = run_case(name, module)
    write_json(HERE / "PHASE2_REAL_CASE_STRESS_SUMMARY_20260922.json", results)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
