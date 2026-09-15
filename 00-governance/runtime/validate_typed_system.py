#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
REGISTRY = RUNTIME / "OLEANDER_TYPED_SYSTEM_VALIDATOR_RULE_REGISTRY_v0.1.json"
EVALS = RUNTIME / "OLEANDER_TYPED_SYSTEM_REGRESSION_EVALS_v0.1.json"

ALLOWED_PLANES = {"KNOWLEDGE", "PROJECT", "RUNTIME_CONTROL"}
ALLOWED_OUTCOMES = {"PASS", "FAIL", "HOLD", "REVIEW_SIGNAL", "NOT_APPLICABLE", "NOT_EVALUATED"}
PRIORITY_ORDER = ["P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9", "P10", "P11", "INT"]
CLOSED_DIMENSION_RESULTS = {"PASS", "ACCEPTED", "OUTSIDE_CLAIM", "NOT_APPLICABLE"}
HIGH_PROMOTION_BADGES = {"PASS", "VERIFIED", "CURRENT_VERIFIED", "PROFESSIONAL_PASS", "KEEP_MAIN"}


@dataclass
class Finding:
    rule_id: str
    outcome: str
    severity: str
    object_id: str | None
    message: str
    basis: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.outcome not in ALLOWED_OUTCOMES:
            raise ValueError(f"invalid outcome {self.outcome}")


def fail(msg: str) -> None:
    raise SystemExit(f"typed-system validation failed: {msg}")


def load_json(path: Path) -> Any:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def priority_key(rule_id: str) -> tuple[int, str]:
    prefix = rule_id.split("/", 1)[0]
    try:
        idx = PRIORITY_ORDER.index(prefix)
    except ValueError:
        idx = len(PRIORITY_ORDER)
    return idx, rule_id


def validate_registry() -> list[Finding]:
    data = load_json(REGISTRY)
    findings: list[Finding] = []

    if data.get("evaluation_order") != PRIORITY_ORDER:
        findings.append(Finding(
            "INT/REGISTRY-001", "FAIL", "S3_MAJOR", None,
            "validator registry evaluation_order must remain P0→P11→INT",
            {"actual": data.get("evaluation_order"), "expected": PRIORITY_ORDER},
        ))

    seen: set[str] = set()
    duplicates: set[str] = set()
    for namespace, rules in data.get("rules", {}).items():
        if namespace not in PRIORITY_ORDER:
            findings.append(Finding(
                "INT/REGISTRY-002", "FAIL", "S2_MATERIAL", None,
                f"unknown rule namespace {namespace}"
            ))
        for rule_id in rules:
            if rule_id in seen:
                duplicates.add(rule_id)
            seen.add(rule_id)
            if "/" not in rule_id:
                findings.append(Finding(
                    "INT/REGISTRY-003", "FAIL", "S2_MATERIAL", None,
                    f"rule id is not namespaced: {rule_id}"
                ))
    if duplicates:
        findings.append(Finding(
            "INT/REGISTRY-004", "FAIL", "S3_MAJOR", None,
            "duplicate rule ids in registry",
            {"duplicates": sorted(duplicates)},
        ))

    derived = data.get("replay_derived_rules", {})
    missing = sorted(set(derived) - seen)
    if missing:
        findings.append(Finding(
            "INT/REGISTRY-005", "FAIL", "S2_MATERIAL", None,
            "replay-derived rules must also appear in the namespace rule lists",
            {"missing": missing},
        ))

    if not findings:
        findings.append(Finding(
            "INT/REGISTRY-000", "PASS", "S0_INFO", None,
            f"registry structurally valid with {len(seen)} unique rules"
        ))
    return findings


def validate_eval_corpus() -> list[Finding]:
    data = load_json(EVALS)
    cases = data.get("cases", [])
    findings: list[Finding] = []
    ids = [case.get("id") for case in cases]
    dup = sorted({x for x in ids if x and ids.count(x) > 1})
    if dup:
        findings.append(Finding(
            "INT/EVAL-001", "FAIL", "S2_MATERIAL", None,
            "duplicate regression case IDs", {"duplicates": dup}
        ))
    for case in cases:
        cid = case.get("id")
        if not cid or not case.get("priority") or not case.get("input") or not case.get("expected"):
            findings.append(Finding(
                "INT/EVAL-002", "FAIL", "S2_MATERIAL", cid,
                "regression case missing id/priority/input/expected"
            ))
    if not findings:
        findings.append(Finding(
            "INT/EVAL-000", "PASS", "S0_INFO", None,
            f"regression corpus structurally valid with {len(cases)} cases"
        ))
    return findings


def obj_id(obj: dict[str, Any]) -> str | None:
    value = obj.get("id") or obj.get("object_id")
    return str(value) if value is not None else None


def rule_p0_plane(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        plane = obj.get("plane")
        if plane not in ALLOWED_PLANES:
            out.append(Finding(
                "P0/PLANE-001", "FAIL", "S3_MAJOR", obj_id(obj),
                "canonical semantic object must resolve exactly one supported primary plane",
                {"plane": plane},
            ))
    return out


def rule_p0_identity_collision(snapshot: dict[str, Any]) -> list[Finding]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for obj in snapshot.get("objects", []):
        if not obj.get("is_current"):
            continue
        key = obj.get("semantic_key")
        scope = obj.get("scope_key", "GLOBAL")
        if not key:
            continue
        groups.setdefault((str(key), str(scope)), []).append(obj)

    out: list[Finding] = []
    for (key, scope), objs in groups.items():
        if len(objs) > 1:
            out.append(Finding(
                "P0/ID-002", "FAIL", "S4_CRITICAL", None,
                "multiple Current owners for same semantic responsibility/scope",
                {"semantic_key": key, "scope_key": scope, "object_ids": [obj_id(o) for o in objs]},
            ))
    return out


def rule_p1_support_ceiling(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    forbidden_axes = {"design_quality", "professional", "field_operational", "source_authority"}
    for obj in snapshot.get("objects", []):
        if obj.get("semantic_class") != "ASSURANCE_DECISION":
            continue
        if obj.get("scope_kind") != "SUPPORT_ONLY":
            continue
        grants = obj.get("granted_ceilings", {})
        bad = {
            k: v for k, v in grants.items()
            if k in forbidden_axes and v not in (None, "UNASSESSED", "OPEN", "NOT_FIELD", "UNCHANGED")
        }
        if bad:
            out.append(Finding(
                "P1/CLAIM-RP01", "FAIL", "S3_MAJOR", obj_id(obj),
                "support-only PASS cannot raise design/professional/field/source-authority ceilings",
                {"forbidden_grants": bad},
            ))
    return out


def rule_p2_parent_decision(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    by_id = {obj_id(o): o for o in snapshot.get("objects", []) if obj_id(o)}
    for obj in snapshot.get("objects", []):
        if obj.get("semantic_class") != "DECISION_OBJECT":
            continue
        parent = obj.get("parent_decision_ref")
        if not parent or obj.get("status") != "CLOSED":
            continue
        pobj = by_id.get(str(parent))
        if pobj and pobj.get("decision_domain") == "DESIGN_QUALITY" and pobj.get("status") == "CLOSED":
            unresolved = pobj.get("target_results", {})
            if any(v in {"REVISE", "OPEN", "FAIL", "HOLD", "INCONCLUSIVE"} for v in unresolved.values()):
                out.append(Finding(
                    "P2/DECQ-RP01", "FAIL", "S3_MAJOR", obj_id(obj),
                    "support decision closure cannot close parent design-quality decision with unresolved targets",
                    {"parent": parent, "target_results": unresolved},
                ))
    return out


def rule_p3_migration(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        if obj.get("migration_state") not in {"INCOMPLETE", "LEGACY_UNMIGRATED"}:
            continue
        if obj.get("project_failure_reason") == "MISSING_NEW_TYPED_FIELDS_ONLY":
            out.append(Finding(
                "P3/MIG-RP01", "FAIL", "S2_MATERIAL", obj_id(obj),
                "missing typed migration alone cannot be rewritten as project/domain failure"
            ))
    return out


def rule_p4_interface_dimensions(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        if obj.get("semantic_class") != "INTERFACE":
            continue
        if obj.get("disposition") != "CLOSED":
            continue
        dims = obj.get("acceptance_dimensions", {})
        unresolved = {k: v for k, v in dims.items() if v not in CLOSED_DIMENSION_RESULTS}
        if unresolved:
            out.append(Finding(
                "P4/IFC-RP01", "FAIL", "S3_MAJOR", obj_id(obj),
                "interface cannot close while material acceptance dimensions remain unresolved",
                {"unresolved_dimensions": unresolved},
            ))
    return out


def rule_p5_support_change(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        if obj.get("semantic_class") != "CHANGE":
            continue
        if obj.get("change_scope") != "SUPPORT_DERIVATIVE_ONLY":
            continue
        if obj.get("upstream_source_changed") is False:
            stale = set(obj.get("stale_effects", []))
            if "UPSTREAM_SOURCE_CONFIGURATION" in stale:
                out.append(Finding(
                    "P5/CHG-RP01", "FAIL", "S3_MAJOR", obj_id(obj),
                    "support/derivative-only change cannot stale unchanged upstream source configuration"
                ))
    return out


def rule_p6_mixed_results(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        if obj.get("semantic_class") not in {"ASSURANCE_ACTIVITY", "ASSURANCE_DECISION"}:
            continue
        results = obj.get("target_results", {})
        if not isinstance(results, dict) or len(set(results.values())) <= 1:
            continue
        summary = obj.get("summary_result")
        policy = obj.get("aggregation_policy")
        if summary in {"PASS", "FAIL"} and not policy:
            out.append(Finding(
                "P6/ASR-RP02", "FAIL", "S3_MAJOR", obj_id(obj),
                "mixed assurance results need explicit aggregation policy and preserved per-target results",
                {"target_results": results, "summary_result": summary},
            ))
    return out


def rule_p7_unclassified_open(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    forced_classes = {"RISK", "ISSUE", "ASSUMPTION", "UNKNOWN"}
    for obj in snapshot.get("objects", []):
        if obj.get("migration_origin_state") != "OPEN_UNCLASSIFIED":
            continue
        if obj.get("semantic_class") in forced_classes and not obj.get("classification_basis"):
            out.append(Finding(
                "P7/OPEN-RP01", "FAIL", "S2_MATERIAL", obj_id(obj),
                "legacy OPEN state cannot be force-classified without semantic basis"
            ))
    return out


def rule_p8_file_count(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for package in snapshot.get("support_packages", []):
        files = package.get("artifacts", [])
        semantic_count = package.get("semantic_object_count")
        if (
            package.get("shared_semantic_responsibility")
            and isinstance(semantic_count, int)
            and semantic_count >= len(files)
            and len(files) > 1
        ):
            out.append(Finding(
                "P8/ART-RP01", "REVIEW_SIGNAL", "S1_REVIEW", package.get("id"),
                "file count appears to drive semantic object count for one shared support responsibility",
                {"artifact_count": len(files), "semantic_object_count": semantic_count},
            ))
    return out


def rule_p9_census(snapshot: dict[str, Any]) -> list[Finding]:
    census = snapshot.get("corpus_census")
    if census is None:
        return []
    missing = [k for k in ("as_of", "scope", "enumeration_basis", "counts") if not census.get(k)]
    if missing:
        return [Finding(
            "P9/CORPUS-RP01", "FAIL", "S2_MATERIAL", None,
            "corpus census must carry as_of, scope, enumeration basis and counts",
            {"missing": missing},
        )]
    if census.get("hard_ceiling") is True:
        return [Finding(
            "P9/CORPUS-RP01", "FAIL", "S2_MATERIAL", None,
            "corpus count cannot be encoded as a permanent hard ceiling"
        )]
    return []


def rule_p9_review_states(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        review_class = obj.get("review_evidence_class")
        if review_class in {"GRAPH_ONLY", "LINEAGE_ONLY"} and obj.get("content_state") == "PASS":
            out.append(Finding(
                "P9/TERM-RP01", "FAIL", "S2_MATERIAL", obj_id(obj),
                "graph/lineage-only review evidence cannot grant content terminal PASS"
            ))
        if obj.get("full_body_integrity") == "PASS":
            if any(
                obj.get(k) == "PASS_BY_READBACK_ONLY"
                for k in ("content_state", "bilingual_state", "independent_review_state")
            ):
                out.append(Finding(
                    "P9/BODY-RP01", "FAIL", "S2_MATERIAL", obj_id(obj),
                    "full-body integrity/readback cannot self-grant content/bilingual/IR PASS"
                ))
    return out


def rule_p10_asset_identity(snapshot: dict[str, Any]) -> list[Finding]:
    assets = snapshot.get("presentation_assets", [])
    out: list[Finding] = []
    source_ids = [a.get("semantic_source_id") for a in assets if a.get("semantic_source_id")]
    declared = snapshot.get("presentation_metrics", {}).get("independent_source_count")
    if declared is not None and declared > len(set(source_ids)):
        out.append(Finding(
            "P10/ASSET-RP01", "FAIL", "S2_MATERIAL", None,
            "derivative instances cannot inflate independent semantic visual source count",
            {"declared": declared, "unique_semantic_sources": len(set(source_ids))},
        ))
    for asset in assets:
        if asset.get("is_derivative") and not asset.get("semantic_source_id"):
            out.append(Finding(
                "P10/ASSET-RP01", "FAIL", "S2_MATERIAL", asset.get("presentation_asset_id"),
                "presentation derivative must retain semantic_source_id"
            ))
    return out


def rule_p10_role(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for asset in snapshot.get("presentation_assets", []):
        if (
            asset.get("source_role") in {"SUPPORT", "PROCESS_SUPPORT", "REFERENCE_ONLY"}
            and asset.get("semantic_role") == "PRIMARY_MAIN"
            and not asset.get("authorized_role_change")
        ):
            out.append(Finding(
                "P10/ROLE-RP02", "FAIL", "S3_MAJOR", asset.get("presentation_asset_id"),
                "display treatment cannot promote support/reference source into PRIMARY_MAIN without authority"
            ))
        if asset.get("truth_risk") == "E3" and asset.get("semantic_role") in {
            "PRIMARY_EVIDENCE", "FIELD_EVIDENCE", "SOURCE_TRUTH"
        }:
            out.append(Finding(
                "P10/TRUTH-RP03", "FAIL", "S4_CRITICAL", asset.get("presentation_asset_id"),
                "E3 synthetic/reference image cannot occupy evidentiary source role"
            ))
    return out


def rule_p10_medium_readback(snapshot: dict[str, Any]) -> list[Finding]:
    release = snapshot.get("presentation_release")
    if not release:
        return []
    vector = release.get("medium_readback", {})
    if release.get("global_status") == "PASS":
        unresolved = {k: v for k, v in vector.items() if v not in {"PASS", "NOT_APPLICABLE"}}
        if unresolved:
            return [Finding(
                "P10/MED-RP01", "FAIL", "S2_MATERIAL", release.get("id"),
                "global presentation PASS cannot hide unresolved medium-specific readback",
                {"unresolved_media": unresolved},
            )]
    return []


def rule_p11_badges(snapshot: dict[str, Any]) -> list[Finding]:
    out: list[Finding] = []
    for obj in snapshot.get("objects", []):
        if obj.get("retrieval_space") != "CURRENT":
            continue
        professional = obj.get("professional_state")
        badge = obj.get("summary_badge")
        if professional in {"NOT_PROVEN_PROFESSIONAL_PASS", "OPEN", "REVISE", "HOLD"} and badge in HIGH_PROMOTION_BADGES:
            out.append(Finding(
                "P11/BADGE-RP02", "FAIL", "S2_MATERIAL", obj_id(obj),
                "CURRENT retrieval state cannot be presented as professional/content completion",
                {"professional_state": professional, "summary_badge": badge},
            ))
    return out


SNAPSHOT_RULES: list[Callable[[dict[str, Any]], list[Finding]]] = [
    rule_p0_plane,
    rule_p0_identity_collision,
    rule_p1_support_ceiling,
    rule_p2_parent_decision,
    rule_p3_migration,
    rule_p4_interface_dimensions,
    rule_p5_support_change,
    rule_p6_mixed_results,
    rule_p7_unclassified_open,
    rule_p8_file_count,
    rule_p9_census,
    rule_p9_review_states,
    rule_p10_asset_identity,
    rule_p10_role,
    rule_p10_medium_readback,
    rule_p11_badges,
]


def validate_snapshot(snapshot: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    if snapshot.get("schema") != "OLEANDER_TYPED_SNAPSHOT_v0.1":
        findings.append(Finding(
            "P0/SNAPSHOT-001", "FAIL", "S3_MAJOR", None,
            "snapshot schema must be OLEANDER_TYPED_SNAPSHOT_v0.1",
            {"actual": snapshot.get("schema")},
        ))
        return findings

    for rule in SNAPSHOT_RULES:
        findings.extend(rule(snapshot))

    if not findings:
        findings.append(Finding(
            "INT/SNAPSHOT-000", "PASS", "S0_INFO", None,
            "no implemented typed-system invariant violations detected"
        ))
    return sorted(findings, key=lambda f: priority_key(f.rule_id))


def self_test() -> list[Finding]:
    test_snapshot = {
        "schema": "OLEANDER_TYPED_SNAPSHOT_v0.1",
        "snapshot_id": "SELFTEST",
        "objects": [
            {
                "id": "SUP-ASR-1",
                "plane": "PROJECT",
                "semantic_class": "ASSURANCE_DECISION",
                "scope_kind": "SUPPORT_ONLY",
                "granted_ceilings": {"design_quality": "KEEP_MAIN"},
            },
            {
                "id": "IF-1",
                "plane": "PROJECT",
                "semantic_class": "INTERFACE",
                "disposition": "CLOSED",
                "acceptance_dimensions": {"GEOMETRY": "PASS", "OPERATIONAL": "OPEN"},
            },
            {
                "id": "CHG-1",
                "plane": "PROJECT",
                "semantic_class": "CHANGE",
                "change_scope": "SUPPORT_DERIVATIVE_ONLY",
                "upstream_source_changed": false,
                "stale_effects": ["UPSTREAM_SOURCE_CONFIGURATION"],
            },
            {
                "id": "ASR-2",
                "plane": "PROJECT",
                "semantic_class": "ASSURANCE_DECISION",
                "target_results": {"G1": "REVISE", "G4": "PASS"},
                "summary_result": "PASS"
            },
            {
                "id": "KN-1",
                "plane": "KNOWLEDGE",
                "semantic_class": "METHOD",
                "retrieval_space": "CURRENT",
                "professional_state": "NOT_PROVEN_PROFESSIONAL_PASS",
                "summary_badge": "CURRENT_VERIFIED"
            }
        ],
        "corpus_census": {"counts": {"TOTAL": 1215}, "hard_ceiling": true},
        "presentation_assets": [
            {"presentation_asset_id": "IMG-D1", "is_derivative": true},
            {
                "presentation_asset_id": "AI-1",
                "semantic_source_id": "SRC-AI",
                "truth_risk": "E3",
                "source_role": "REFERENCE_ONLY",
                "semantic_role": "FIELD_EVIDENCE"
            }
        ],
        "presentation_metrics": {"independent_source_count": 3},
        "presentation_release": {
            "id": "REL-1",
            "global_status": "PASS",
            "medium_readback": {"PDF_PRINT": "PASS", "DESKTOP_BROWSER": "WAIT"}
        }
    }
    findings = validate_snapshot(test_snapshot)
    expected = {
        "P1/CLAIM-RP01",
        "P4/IFC-RP01",
        "P5/CHG-RP01",
        "P6/ASR-RP02",
        "P9/CORPUS-RP01",
        "P10/ASSET-RP01",
        "P10/TRUTH-RP03",
        "P10/MED-RP01",
        "P11/BADGE-RP02"
    }
    actual = {f.rule_id for f in findings}
    missing = sorted(expected - actual)
    if missing:
        raise SystemExit(f"typed-system self-test failed; missing expected findings: {missing}")
    return findings


def emit_receipt(findings: list[Finding], source: str, as_json: bool) -> None:
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.outcome] = counts.get(finding.outcome, 0) + 1

    receipt = {
        "schema": "OLEANDER_TYPED_VALIDATION_RECEIPT_v0.1",
        "source": source,
        "evaluation_order": PRIORITY_ORDER,
        "counts": counts,
        "findings": [asdict(f) for f in findings],
    }

    if as_json:
        print(json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True))
        return

    print(f"typed-system validator: {source}")
    print(" ".join(f"{k}={v}" for k, v in sorted(counts.items())))
    for finding in findings:
        oid = f" [{finding.object_id}]" if finding.object_id else ""
        print(f"- {finding.outcome:<15} {finding.rule_id}{oid}: {finding.message}")


def main() -> None:
    parser = argparse.ArgumentParser(description="OLEANDER typed-system validator v0.1")
    parser.add_argument("--snapshot", type=Path, help="validate normalized OLEANDER_TYPED_SNAPSHOT_v0.1 JSON")
    parser.add_argument("--self-test", action="store_true", help="run deterministic engine self-test")
    parser.add_argument("--contracts-only", action="store_true", help="validate rule registry + regression corpus only")
    parser.add_argument("--json", action="store_true", help="emit machine-readable receipt")
    args = parser.parse_args()

    findings: list[Finding] = []
    source_parts: list[str] = []

    if args.self_test:
        findings.extend(self_test())
        source_parts.append("self-test")

    if args.contracts_only or (not args.snapshot and not args.self_test):
        findings.extend(validate_registry())
        findings.extend(validate_eval_corpus())
        source_parts.append("contracts")

    if args.snapshot:
        snapshot = load_json(args.snapshot)
        findings.extend(validate_snapshot(snapshot))
        source_parts.append(str(args.snapshot))

    findings = sorted(findings, key=lambda f: priority_key(f.rule_id))
    emit_receipt(findings, "+".join(source_parts) or "none", args.json)

    if any(f.outcome == "FAIL" for f in findings):
        sys.exit(1)


if __name__ == "__main__":
    main()
