#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_p7_conversions import EXECUTABLE_RULES, check_snapshot

RUNTIME = Path(__file__).resolve().parent
EVALS = RUNTIME / "OLEANDER_P7_EXECUTABLE_REGRESSION_EVALS_v0.1.json"


def main() -> None:
    snapshot = {
        "schema": "OLEANDER_TYPED_SNAPSHOT_v0.1",
        "snapshot_id": "P7-EXECUTABLE-SELF-TEST",
        "objects": [
            {
                "id": "ISSUE-REVIEW",
                "plane": "PROJECT",
                "semantic_class": "ISSUE",
                "prior_producer_pass": True,
                "material_review_finding": True,
                "prior_pass_still_current_closure_proof": True,
                "root_cause_state": "SUPPORTED",
                "repair_state": "IMPLEMENTED",
                "repair_refs": [],
                "retest_required": True,
                "retest_refs": [],
                "invalidated_prior_receipts_material": True,
                "supersedes_or_invalidates_receipts": [],
                "closure_state": "CLOSED",
                "higher_review_required": True,
                "review_after_repair": "PENDING",
                "parent_state_auto_closed": True,
                "related_risk_set_to_zero_on_closure": True,
            },
            {
                "id": "ISSUE-CLOUDFLARE",
                "plane": "PROJECT",
                "semantic_class": "ISSUE",
                "introduced_or_effective_at": "2025-06-06T17:38Z",
                "impact_started_at": "2025-07-14T21:48Z",
                "detected_at": "2025-07-14T22:01Z",
                "declared_at": "2025-07-14T22:01Z",
                "detection_time_used_as_issue_origin": True,
                "established_existing_defect": True,
                "retroclassified_as_risk_due_no_prior_impact": True,
                "causal_confidence_promoted_from_temporal_or_contextual_coincidence": True,
                "material_incident": True,
                "single_generic_root_cause_used": True,
                "causal_role_records": [],
                "repair_implemented_at": "2025-07-14T22:20Z",
                "retest_completed_at": "2025-07-14T22:30Z",
                "impact_ended_at": "2025-07-14T22:54Z",
                "resolved_at": "2025-07-14T22:55Z",
                "collapsed_done_timestamp": True,
                "containment_or_recovery_started": True,
                "root_cause_state": "HYPOTHESIZED",
                "action_urgency_promoted_root_cause_confidence": True,
                "postmortem_required": True,
                "failure_cause_recorded": True,
                "detection_gap_material": True,
            },
            {
                "id": "RISK-REALIZED",
                "plane": "PROJECT",
                "semantic_class": "RISK",
                "risk_realization_disposition": "REALIZED_AS_ISSUE",
                "mutated_in_place_to_issue": True,
                "created_post_hoc_from_issue": True,
            },
            {
                "id": "UNKNOWN-TBR",
                "plane": "PROJECT",
                "semantic_class": "UNKNOWN",
                "unknown_resolution_mode": "TBR_PROVISIONAL_VALUE",
                "provisional_value": "3.0 m",
                "converted_to_assumption": True,
                "treated_as_fact_or_accepted_assumption": True,
                "assumption_admission_gates_satisfied": ["NECESSARY_TO_PROCEED", "PROPOSITION_EXPLICIT"],
            },
            {
                "id": "ASSUMPTION-REFUTED",
                "plane": "PROJECT",
                "semantic_class": "ASSUMPTION",
                "assumption_state": "REFUTED",
                "affected_dependency_types": ["DECISION", "REQUIREMENT", "INTERFACE", "ASSURANCE"],
                "reopened_dependency_types": ["DECISION"],
            },
        ],
    }

    findings = check_snapshot(snapshot)
    actual = {finding.rule_id for finding in findings}
    missing = sorted(EXECUTABLE_RULES - actual)
    if missing:
        raise SystemExit(f"P7 executable self-test failed: missing findings {missing}")
    unexpected = sorted(actual - EXECUTABLE_RULES)
    if unexpected:
        raise SystemExit(f"P7 executable self-test failed: unexpected findings {unexpected}")

    payload = json.loads(EVALS.read_text(encoding="utf-8"))
    referenced: set[str] = set()
    ids: list[str] = []
    for case in payload.get("cases", []):
        ids.append(case.get("id"))
        for expected in case.get("expected", []):
            if isinstance(expected, str):
                referenced.add(expected.split(":", 1)[0])
    if len(ids) != len(set(ids)):
        raise SystemExit("P7 executable regression corpus failed: duplicate case IDs")
    uncovered = sorted(EXECUTABLE_RULES - referenced)
    if uncovered:
        raise SystemExit(f"P7 executable regression corpus failed: uncovered rules {uncovered}")
    unknown_refs = sorted(referenced - EXECUTABLE_RULES)
    if unknown_refs:
        raise SystemExit(f"P7 executable regression corpus failed: references non-executable rules {unknown_refs}")

    print(
        "P7 executable self-test PASS: "
        f"rules={len(EXECUTABLE_RULES)} findings={len(findings)} cases={len(ids)}"
    )


if __name__ == "__main__":
    main()
