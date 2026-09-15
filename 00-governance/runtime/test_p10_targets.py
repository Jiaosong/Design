#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_p10_targets import EXECUTABLE_RULES, check_snapshot

RUNTIME = Path(__file__).resolve().parent
EVALS = RUNTIME / "OLEANDER_P10_EXECUTABLE_REGRESSION_EVALS_v0.1.json"


def main() -> None:
    snapshot = {
        "schema": "OLEANDER_TYPED_SNAPSHOT_v0.1",
        "snapshot_id": "P10-EXECUTABLE-SELF-TEST",
        "objects": [
            {
                "id": "REL",
                "plane": "PROJECT",
                "semantic_class": "PRESENTATION_RELEASE",
                "source_revision": "rev-new",
                "reusable_or_carry_forward_claimed": True,
                "medium_pass_reused_without_target_condition": True,
                "medium_readback_vector": {"DESKTOP":"PASS"},
                "browser_target_pass": True,
                "design_keep_closed_from_browser": True,
                "simulated_or_derived_user_facing_state": True,
                "targets_exposing_simulation": ["DESKTOP", "MOBILE"],
                "truth_boundary_readable_targets": ["DESKTOP"],
                "deployment_status": "PASS",
                "external_content_readback": "NOT_EVALUATED",
                "external_content_pass_inferred_from_deployment": True,
                "section_or_page_count_change_used_as_content_loss_proof": True,
                "source_mutation_inferred_from_count_change": True,
                "reduced_motion_state_present": True,
                "reduced_motion_separate_style_identity": True,
                "information_architecture_or_semantic_role_changed": False
            },
            {
                "id": "ASSET",
                "plane": "PROJECT",
                "semantic_class": "PRESENTATION_ASSET",
                "semantic_source_id": "SRC-01",
                "runtime_instances": ["chunk-a", "chunk-b"],
                "declared_independent_source_count": 2,
                "manifest_revision": "rev-old",
                "current_source_revision": "rev-new",
                "manifest_claimed_complete_current_coverage": True,
                "runtime_slot_role": "MAIN",
                "visual_semantic_role": "PRIMARY_MAIN",
                "design_review_state_promoted_from_runtime_role": True
            }
        ]
    }

    findings = check_snapshot(snapshot)
    actual = {finding.rule_id for finding in findings}
    missing = sorted(EXECUTABLE_RULES - actual)
    if missing:
        raise SystemExit(f"P10 executable self-test failed: missing findings {missing}")
    unexpected = sorted(actual - EXECUTABLE_RULES)
    if unexpected:
        raise SystemExit(f"P10 executable self-test failed: unexpected findings {unexpected}")

    payload = json.loads(EVALS.read_text(encoding="utf-8"))
    referenced: set[str] = set()
    ids: list[str] = []
    for case in payload.get("cases", []):
        ids.append(case.get("id"))
        for expected in case.get("expected", []):
            if isinstance(expected, str):
                referenced.add(expected.split(":", 1)[0])
    if len(ids) != len(set(ids)):
        raise SystemExit("P10 executable regression corpus failed: duplicate case IDs")
    uncovered = sorted(EXECUTABLE_RULES - referenced)
    if uncovered:
        raise SystemExit(f"P10 executable regression corpus failed: uncovered rules {uncovered}")
    unknown_refs = sorted(referenced - EXECUTABLE_RULES)
    if unknown_refs:
        raise SystemExit(f"P10 executable regression corpus failed: references non-executable rules {unknown_refs}")

    print(
        "P10 executable self-test PASS: "
        f"rules={len(EXECUTABLE_RULES)} findings={len(findings)} cases={len(ids)}"
    )


if __name__ == "__main__":
    main()
