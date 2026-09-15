#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_p8_handoffs import EXECUTABLE_RULES, check_snapshot

RUNTIME = Path(__file__).resolve().parent
EVALS = RUNTIME / "OLEANDER_P8_EXECUTABLE_REGRESSION_EVALS_v0.1.json"


def main() -> None:
    snapshot = {
        "schema": "OLEANDER_TYPED_SNAPSHOT_v0.1",
        "snapshot_id": "P8-EXECUTABLE-SELF-TEST",
        "objects": [
            {
                "id": "PKG",
                "plane": "PROJECT",
                "semantic_class": "SUPPORT_PACKAGE",
                "artifacts": [{"id":"a"},{"id":"b"},{"id":"c"}],
                "semantic_object_count": 1,
                "one_file_one_semantic_object": True,
            },
            {
                "id": "H-MAIN",
                "plane": "PROJECT",
                "semantic_class": "HANDOFF",
                "handoff_role": "SOURCE_MASTER",
                "material_cross_software_handoff": True,
                "disposition": "ACCEPT",
                "loss_severity": "AUTHORITY_BREAKING",
                "same_loss_used_for_multiple_roles": True,
                "loss_acceptability_role_scoped": False,
                "consumer_import_or_edit_capable": True,
                "source_change_authority_transferred": True,
                "exchange_reopen_status": "PASS",
                "native_authoring_state_promoted_from_exchange": True,
                "runtime_delivery_format_pass": True,
                "native_parametric_authoring_preserved_claim": True,
                "roundtrip_tested": True,
                "roundtrip_acceptance_basis": "BYTE_HASH_ONLY",
                "byte_identity_controlled_property": False,
                "downstream_package_or_deployment_incomplete": True,
                "unchanged_upstream_source_invalidated": True,
                "per_role_results": {"GEOMETRY_REFERENCE":"PASS","PARAMETRIC_EDITING":"FAIL"},
                "global_handoff_status": "PASS",
                "file_open_or_import_success": True,
                "consumer_task_readback_complete": False,
                "declared_required_dimensions_readback_complete": False,
                "layer_results": {
                    "L2_SCHEMA_NORMATIVE_CONFORMANCE": "PASS",
                    "L4_PROJECT_INFORMATION_REQUIREMENT_CONFORMANCE": "AUTO_GRANTED_FROM_SCHEMA",
                    "L5_CONSUMER_TASK_READBACK": "AUTO_GRANTED_FROM_LOWER_LAYER"
                },
                "exchange_derivative_replaces_source_master": True,
                "per_object_or_information_class_results": {"OBJ-1":"PASS","OBJ-2":"FAIL"},
                "declared_exchange_requirement_exists": True,
                "fidelity_judged_against_total_native_equivalence": True,
                "producer_export_validation_complete": True,
                "consumer_behavior_material": True,
            },
            {
                "id": "H-REF",
                "plane": "PROJECT",
                "semantic_class": "HANDOFF",
                "handoff_role": "REFERENCE_ONLY",
                "disposition": "REJECT",
                "roundtrip_required": False,
                "rejection_reason": "NATIVE_ROUNDTRIP_NOT_PRESERVED",
                "failed_only_due_roundtrip": True,
            },
            {
                "id": "H-UNKNOWN-REQUIRED",
                "plane": "PROJECT",
                "semantic_class": "HANDOFF",
                "disposition": "ACCEPT",
                "required_information_classes": ["FIRE_RATING"],
                "unknown_dimensions": ["FIRE_RATING"],
            },
            {
                "id": "H-UNKNOWN-OUTSIDE",
                "plane": "PROJECT",
                "semantic_class": "HANDOFF",
                "disposition": "HOLD",
                "required_information_classes": ["GEOMETRY"],
                "unknown_dimensions": ["NATIVE_FEATURE_TREE"],
                "global_hold_due_unknown_outside_claim": True,
            },
            {
                "id": "H-EDITABLE",
                "plane": "PROJECT",
                "semantic_class": "HANDOFF",
                "handoff_role": "EDITABLE_MASTER",
                "disposition": "ACCEPT",
                "roundtrip_required": True,
                "roundtrip_status": "OPEN",
                "loss_observation_state": "UNKNOWN_NOT_TESTED",
                "loss_severity": "NONE",
            },
        ],
    }

    findings = check_snapshot(snapshot)
    actual = {finding.rule_id for finding in findings}
    missing = sorted(EXECUTABLE_RULES - actual)
    if missing:
        raise SystemExit(f"P8 executable self-test failed: missing findings {missing}")
    unexpected = sorted(actual - EXECUTABLE_RULES)
    if unexpected:
        raise SystemExit(f"P8 executable self-test failed: unexpected findings {unexpected}")

    payload = json.loads(EVALS.read_text(encoding="utf-8"))
    referenced: set[str] = set()
    ids: list[str] = []
    for case in payload.get("cases", []):
        ids.append(case.get("id"))
        for expected in case.get("expected", []):
            if isinstance(expected, str):
                referenced.add(expected.split(":", 1)[0])
    if len(ids) != len(set(ids)):
        raise SystemExit("P8 executable regression corpus failed: duplicate case IDs")
    uncovered = sorted(EXECUTABLE_RULES - referenced)
    if uncovered:
        raise SystemExit(f"P8 executable regression corpus failed: uncovered rules {uncovered}")
    unknown_refs = sorted(referenced - EXECUTABLE_RULES)
    if unknown_refs:
        raise SystemExit(f"P8 executable regression corpus failed: references non-executable rules {unknown_refs}")

    print(
        "P8 executable self-test PASS: "
        f"rules={len(EXECUTABLE_RULES)} findings={len(findings)} cases={len(ids)}"
    )


if __name__ == "__main__":
    main()
