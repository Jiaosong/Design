#!/usr/bin/env python3
"""Validate OLEANDER project-closure receipts and project requirement baselines.

The semantic checks in this file are intentionally stdlib-only.  jsonschema is
used when present, but its absence must not weaken the fail-closed PASS rules.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent

SCHEMAS = {
    "CROSS_DISCIPLINARY_INTEGRATION_RECEIPT": ROOT / "cross-disciplinary-integration-receipt.v1.schema.json",
    "STRUCTURAL_ENGINEERING_DESIGN_PROCESS_RECEIPT": ROOT / "structural-engineering-design-process-receipt.v1.schema.json",
    "BUILDING_SERVICES_MEP_DESIGN_PROCESS_RECEIPT": ROOT / "building-services-mep-design-process-receipt.v1.schema.json",
    "PROJECT_REQUIREMENT_ACCEPTANCE_BASELINE": ROOT / "project-requirement-acceptance-baseline.v1.schema.json",
    "PROJECT_CONFIGURATION_CHANGE_REGISTER": ROOT / "project-configuration-change-register.v1.schema.json",
    "PROJECT_RISK_HAZARD_REGISTER": ROOT / "project-risk-hazard-register.v1.schema.json",
    "PROJECT_OPERATIONAL_ACCEPTANCE_COMPILATION": ROOT / "project-operational-acceptance-compilation.v1.schema.json",
}

STRUCTURAL_PROCESS = ROOT / "structural-engineering-design-process.v1.json"
MEP_PROCESS = ROOT / "building-services-mep-design-process.v1.json"

MATURITY_RANK = {
    "UNRESOLVED": -1,
    "IDENTIFIED": 0,
    "DEFINED": 1,
    "COORDINATED": 2,
    "EXERCISED": 3,
    "VERIFIED": 4,
}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def object_kind(payload: dict[str, Any]) -> str | None:
    return payload.get("receipt_type") or payload.get("object_type")


def schema_errors(payload: dict[str, Any], kind: str) -> list[str]:
    schema = load_json(SCHEMAS[kind])
    errors: list[str] = []
    for key in schema.get("required", []):
        if key not in payload:
            errors.append(f"missing required field: {key}")
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return errors
    validator = jsonschema.Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(payload), key=lambda e: list(e.path)):
        where = ".".join(str(x) for x in error.path) or "$"
        errors.append(f"schema {where}: {error.message}")
    return errors


def duplicate_values(rows: list[dict[str, Any]], key: str) -> list[str]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for row in rows:
        value = row.get(key)
        if isinstance(value, str):
            if value in seen:
                duplicates.append(value)
            seen.add(value)
    return duplicates


def allowed_stage_ids(process_path: Path) -> set[str]:
    return {row["stage_id"] for row in load_json(process_path).get("stages", [])}


def validate_integration(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    interfaces = payload.get("critical_interfaces") or []
    duplicates = duplicate_values(interfaces, "interface_id")
    if duplicates:
        errors.append(f"duplicate interface_id: {sorted(set(duplicates))}")

    interface_ids = {row.get("interface_id") for row in interfaces if isinstance(row, dict)}
    for field in ("unresolved_major_critical_interfaces", "blocked_interfaces"):
        for interface_id in payload.get(field) or []:
            if interface_id not in interface_ids:
                errors.append(f"{field} references unknown interface_id {interface_id!r}")

    if payload.get("integration_verdict") != "PASS":
        return errors

    if payload.get("stale"):
        errors.append("PASS integration receipt cannot be stale")
    for field in ("unresolved_major_critical_interfaces", "blocked_interfaces", "unresolved_authority_conflicts"):
        if payload.get(field):
            errors.append(f"PASS integration receipt requires empty {field}")
    if not payload.get("integrated_readback_refs"):
        errors.append("PASS integration receipt requires integrated_readback_refs")

    for row in interfaces:
        if not row.get("in_claim"):
            continue
        if row.get("criticality") in {"MAJOR", "CRITICAL"}:
            if row.get("disposition") != "CLOSED":
                errors.append(f"PASS requires in-claim {row.get('criticality')} interface {row.get('interface_id')} CLOSED")
            required = MATURITY_RANK.get(row.get("required_maturity"), -99)
            actual = MATURITY_RANK.get(row.get("actual_maturity"), -99)
            if actual < required:
                errors.append(f"PASS interface {row.get('interface_id')} maturity below requirement")
            if row.get("authority_state") not in {"RESOLVED", "NOT_APPLICABLE"}:
                errors.append(f"PASS interface {row.get('interface_id')} has unresolved authority")
            if not row.get("readback_refs"):
                errors.append(f"PASS interface {row.get('interface_id')} requires readback_refs")

    for row in payload.get("shared_variable_authority_summary") or []:
        if row.get("authority_state") not in {"RESOLVED", "NOT_APPLICABLE"}:
            errors.append(f"PASS shared variable {row.get('variable_id')} authority unresolved")
    for row in payload.get("acceptance_contract_results") or []:
        if row.get("required") and row.get("status") != "PASS":
            errors.append(f"PASS integration receipt requires acceptance {row.get('acceptance_id')} PASS")
        if row.get("required") and not row.get("evidence_refs"):
            errors.append(f"required acceptance {row.get('acceptance_id')} lacks evidence_refs")
    for row in payload.get("material_changes") or []:
        if row.get("reconciliation_state") not in {"NOT_REQUIRED", "RECONCILED"}:
            errors.append(f"PASS integration receipt has unreconciled change {row.get('change_id')}")
    for row in payload.get("reopened_reviews") or []:
        if row.get("required") and row.get("status") != "PASS":
            errors.append(f"PASS integration receipt requires reopened review {row.get('review_ref')} PASS")
    if payload.get("reviewer_independence_state") not in {"PASS", "NOT_REQUIRED"}:
        errors.append("PASS integration receipt requires reviewer independence PASS or NOT_REQUIRED")
    return errors


def validate_stage_receipt(payload: dict[str, Any], process_path: Path, review_field: str) -> list[str]:
    errors: list[str] = []
    stages = payload.get("stage_records") or []
    allowed = allowed_stage_ids(process_path)
    duplicates = duplicate_values(stages, "stage_id")
    if duplicates:
        errors.append(f"duplicate stage_id: {sorted(set(duplicates))}")
    for row in stages:
        stage_id = row.get("stage_id")
        if stage_id not in allowed:
            errors.append(f"unknown stage_id {stage_id!r} for {process_path.name}")
        if not row.get("triggered") and row.get("status") != "NOT_TRIGGERED":
            errors.append(f"untriggered stage {stage_id} must be NOT_TRIGGERED")
        if row.get("triggered") and row.get("status") == "NOT_TRIGGERED":
            errors.append(f"triggered stage {stage_id} cannot be NOT_TRIGGERED")

    if payload.get("result") != "PASS":
        return errors
    if payload.get("stale"):
        errors.append("PASS professional receipt cannot be stale")
    if payload.get("blocking_open_items"):
        errors.append("PASS professional receipt requires empty blocking_open_items")
    for row in stages:
        if row.get("triggered"):
            if row.get("status") != "PASS":
                errors.append(f"PASS professional receipt requires triggered stage {row.get('stage_id')} PASS")
            if not row.get("native_output_refs"):
                errors.append(f"PASS stage {row.get('stage_id')} requires native_output_refs")
            if not row.get("actual_readback_refs"):
                errors.append(f"PASS stage {row.get('stage_id')} requires actual_readback_refs")
    for row in payload.get("interface_summary") or []:
        if row.get("required") and row.get("state") != "PASS":
            errors.append(f"PASS professional receipt requires interface {row.get('interface_id')} PASS")
        if row.get("required") and not row.get("evidence_refs"):
            errors.append(f"required interface {row.get('interface_id')} lacks evidence_refs")
    review = payload.get(review_field) or {}
    if review.get("required"):
        if review.get("state") != "PASS":
            errors.append(f"PASS professional receipt requires {review_field} PASS")
        if not review.get("reviewer_ref"):
            errors.append(f"PASS professional receipt requires {review_field}.reviewer_ref")
        if not review.get("review_input_refs"):
            errors.append(f"PASS professional receipt requires {review_field}.review_input_refs")
    return errors


def validate_structural(payload: dict[str, Any]) -> list[str]:
    errors = validate_stage_receipt(payload, STRUCTURAL_PROCESS, "independent_check")
    if payload.get("result") == "PASS":
        for row in payload.get("stage_records") or []:
            if not row.get("triggered"):
                continue
            if row.get("checking_state") not in {"PASS", "NOT_REQUIRED"}:
                errors.append(f"PASS structural stage {row.get('stage_id')} checking_state not closed")
            if row.get("interface_state") in {"OPEN", "FAIL", "HOLD"}:
                errors.append(f"PASS structural stage {row.get('stage_id')} interface_state not closed")
    return errors


def validate_mep(payload: dict[str, Any]) -> list[str]:
    errors = validate_stage_receipt(payload, MEP_PROCESS, "professional_review")
    tracks = payload.get("system_tracks") or []
    duplicates = duplicate_values(tracks, "system_id")
    if duplicates:
        errors.append(f"duplicate system_id: {sorted(set(duplicates))}")
    if payload.get("result") != "PASS":
        return errors
    for row in tracks:
        system_id = row.get("system_id")
        if row.get("status") != "PASS":
            errors.append(f"PASS MEP receipt requires system track {system_id} PASS")
        if not row.get("design_refs"):
            errors.append(f"PASS MEP system track {system_id} requires design_refs")
        if row.get("commissioning_required") and row.get("commissioning_state") not in {"PASS", "DEFERRED_OUTSIDE_CLAIM"}:
            errors.append(f"PASS MEP system track {system_id} commissioning not closed")
        if row.get("integrated_system_test_required") and row.get("integrated_system_test_state") not in {"PASS", "DEFERRED_OUTSIDE_CLAIM"}:
            errors.append(f"PASS MEP system track {system_id} integrated system test not closed")
        if (
            row.get("commissioning_state") == "DEFERRED_OUTSIDE_CLAIM"
            or row.get("integrated_system_test_state") == "DEFERRED_OUTSIDE_CLAIM"
        ) and not row.get("seasonal_or_deferred_test_open"):
            errors.append(f"MEP system track {system_id} deferred test state requires seasonal_or_deferred_test_open=true")
        if not row.get("evidence_refs"):
            errors.append(f"PASS MEP system track {system_id} requires evidence_refs")
    return errors


def validate_requirement_baseline(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rows = payload.get("requirements") or []
    duplicates = duplicate_values(rows, "requirement_id")
    if duplicates:
        errors.append(f"duplicate requirement_id: {sorted(set(duplicates))}")
    known_ids = {row.get("requirement_id") for row in rows if isinstance(row, dict)}
    for requirement_id in payload.get("blocking_requirement_ids") or []:
        if requirement_id not in known_ids:
            errors.append(f"blocking_requirement_ids references unknown requirement_id {requirement_id!r}")
    for row in rows:
        requirement_id = row.get("requirement_id")
        if row.get("applicability") == "NOT_APPLICABLE_WITH_REASON" and not row.get("applicability_reason"):
            errors.append(f"requirement {requirement_id} NOT_APPLICABLE_WITH_REASON requires applicability_reason")
        if row.get("in_claim") and row.get("applicability") == "NOT_APPLICABLE_WITH_REASON":
            errors.append(f"in-claim requirement {requirement_id} cannot be NOT_APPLICABLE_WITH_REASON")
        if row.get("validation_required") and row.get("validation_state") == "NOT_REQUIRED":
            errors.append(f"requirement {requirement_id} validation_required cannot use NOT_REQUIRED state")

    if payload.get("baseline_verdict") != "PASS":
        return errors
    if payload.get("status") != "CURRENT":
        errors.append("PASS requirement baseline must have status CURRENT")
    if payload.get("stale"):
        errors.append("PASS requirement baseline cannot be stale")
    if payload.get("blocking_requirement_ids"):
        errors.append("PASS requirement baseline requires empty blocking_requirement_ids")
    for row in rows:
        if not row.get("in_claim"):
            continue
        requirement_id = row.get("requirement_id")
        if row.get("stale"):
            errors.append(f"PASS requirement {requirement_id} cannot be stale")
        if row.get("applicability") != "APPLICABLE":
            errors.append(f"PASS in-claim requirement {requirement_id} must be APPLICABLE")
        if row.get("verification_state") != "PASS":
            errors.append(f"PASS requirement {requirement_id} verification_state must be PASS")
        if not row.get("evidence_refs"):
            errors.append(f"PASS requirement {requirement_id} requires evidence_refs")
        if row.get("validation_required") and row.get("validation_state") != "PASS":
            errors.append(f"PASS requirement {requirement_id} requires validation PASS")
    return errors


def validate_configuration_register(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    baselines = payload.get("baselines") or []
    changes = payload.get("changes") or []
    duplicates = duplicate_values(baselines, "object_id")
    if duplicates:
        errors.append(f"duplicate baseline object_id: {sorted(set(duplicates))}")
    duplicates = duplicate_values(changes, "change_id")
    if duplicates:
        errors.append(f"duplicate change_id: {sorted(set(duplicates))}")
    if payload.get("register_verdict") != "PASS":
        return errors
    if payload.get("status") != "CURRENT":
        errors.append("PASS configuration register must have status CURRENT")
    if payload.get("stale"):
        errors.append("PASS configuration register cannot be stale")
    if payload.get("open_issue_ids"):
        errors.append("PASS configuration register requires empty open_issue_ids")
    if not any(row.get("state") == "CURRENT" for row in baselines):
        errors.append("PASS configuration register requires at least one CURRENT baseline")
    for row in changes:
        if not row.get("in_claim"):
            continue
        cid = row.get("change_id")
        if row.get("approval_state") not in {"APPROVED", "REJECTED"}:
            errors.append(f"PASS in-claim change {cid} has unresolved approval_state")
        if row.get("approval_state") == "APPROVED" and row.get("propagation_state") != "PASS":
            errors.append(f"PASS approved change {cid} requires propagation PASS")
        if row.get("reacceptance_required") and row.get("reacceptance_state") != "PASS":
            errors.append(f"PASS change {cid} requires reacceptance PASS")
    return errors


def validate_risk_register(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    risks = payload.get("risks") or []
    duplicates = duplicate_values(risks, "risk_id")
    if duplicates:
        errors.append(f"duplicate risk_id: {sorted(set(duplicates))}")
    known_ids = {row.get("risk_id") for row in risks if isinstance(row, dict)}
    for rid in payload.get("blocking_risk_ids") or []:
        if rid not in known_ids:
            errors.append(f"blocking_risk_ids references unknown risk_id {rid!r}")
    if payload.get("register_verdict") != "PASS":
        return errors
    if payload.get("status") != "CURRENT":
        errors.append("PASS risk register must have status CURRENT")
    if payload.get("stale"):
        errors.append("PASS risk register cannot be stale")
    if payload.get("blocking_risk_ids"):
        errors.append("PASS risk register requires empty blocking_risk_ids")
    for row in risks:
        if not row.get("in_claim"):
            continue
        rid = row.get("risk_id")
        if row.get("state") not in {"MITIGATED", "CLOSED"}:
            errors.append(f"PASS in-claim risk {rid} must be MITIGATED or CLOSED")
        if not row.get("mitigation_refs"):
            errors.append(f"PASS in-claim risk {rid} requires mitigation_refs")
        if not row.get("evidence_refs"):
            errors.append(f"PASS in-claim risk {rid} requires evidence_refs")
    return errors


def validate_operational_acceptance(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    defects = payload.get("defects") or []
    tests = payload.get("deferred_tests") or []
    if duplicate_values(defects, "defect_id"):
        errors.append("duplicate defect_id")
    if duplicate_values(tests, "test_id"):
        errors.append("duplicate deferred test_id")
    if payload.get("operational_verdict") != "PASS":
        return errors
    if payload.get("status") != "CURRENT":
        errors.append("PASS operational compilation must have status CURRENT")
    if payload.get("stale"):
        errors.append("PASS operational compilation cannot be stale")
    for field in ("handover_refs", "commissioning_refs", "training_refs", "om_asset_data_refs", "operational_readback_refs"):
        if not payload.get(field):
            errors.append(f"PASS operational compilation requires {field}")
    for row in defects:
        if row.get("blocking") and row.get("status") != "RESOLVED":
            errors.append(f"PASS operational compilation has unresolved blocking defect {row.get('defect_id')}")
    for row in tests:
        if not row.get("required"):
            continue
        if row.get("status") == "PASS":
            continue
        if row.get("status") == "DEFERRED" and row.get("outside_current_claim"):
            continue
        errors.append(f"PASS operational compilation has required test {row.get('test_id')} not closed or validly deferred")
    return errors


def validate_payload(payload: dict[str, Any]) -> list[str]:
    kind = object_kind(payload)
    if kind not in SCHEMAS:
        return [f"unsupported receipt/object type: {kind!r}"]
    errors = schema_errors(payload, kind)
    if kind == "CROSS_DISCIPLINARY_INTEGRATION_RECEIPT":
        errors.extend(validate_integration(payload))
    elif kind == "STRUCTURAL_ENGINEERING_DESIGN_PROCESS_RECEIPT":
        errors.extend(validate_structural(payload))
    elif kind == "BUILDING_SERVICES_MEP_DESIGN_PROCESS_RECEIPT":
        errors.extend(validate_mep(payload))
    elif kind == "PROJECT_REQUIREMENT_ACCEPTANCE_BASELINE":
        errors.extend(validate_requirement_baseline(payload))
    elif kind == "PROJECT_CONFIGURATION_CHANGE_REGISTER":
        errors.extend(validate_configuration_register(payload))
    elif kind == "PROJECT_RISK_HAZARD_REGISTER":
        errors.extend(validate_risk_register(payload))
    elif kind == "PROJECT_OPERATIONAL_ACCEPTANCE_COMPILATION":
        errors.extend(validate_operational_acceptance(payload))
    return errors


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: validate_project_closure_objects.py <json> [<json> ...]", file=sys.stderr)
        return 2
    failed = False
    for raw in argv:
        path = Path(raw)
        payload = load_json(path)
        errors = validate_payload(payload)
        if errors:
            failed = True
            print(f"FAIL {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
