#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_p9_admission import EXECUTABLE_RULES, check_snapshot

RUNTIME = Path(__file__).resolve().parent
EVALS = RUNTIME / "OLEANDER_P9_EXECUTABLE_REGRESSION_EVALS_v0.1.json"


def main() -> None:
    snapshot = {
        "schema": "OLEANDER_TYPED_SNAPSHOT_v0.1",
        "snapshot_id": "P9-EXECUTABLE-SELF-TEST",
        "objects": [
            {
                "id": "G9-CANDIDATE",
                "plane": "KNOWLEDGE",
                "semantic_class": "G9_ADMISSION",
                "lesson_summary_only": True,
                "existing_owner_found": True,
                "existing_owner_primary_responsibility_match": True,
                "new_peer_object_created": True,
                "cross_domain_transfer_claimed": True,
                "transfer_statement_parts_present": ["WHEN", "DO_OR_EXPECT", "BECAUSE"],
                "uses_direct_and_contextual_evidence": True,
                "evidence_strengths_flattened": True,
                "supporting_evidence": [
                    {"ref":"RP-KH46-V008-20260915","strength":"DIRECT_PROJECT_REPLAY"},
                    {"ref":"RP-TP5-GIT-CONFIG-CHANGE-20260915","strength":"DIRECT_PROJECT_REPLAY"}
                ],
                "generalized_method_rule": True,
                "safe_patch_candidate": True,
                "canonical_write_applied": True,
                "current_promotion_applied": True,
                "other_professional_gates_bypassed": True,
                "producer_side_synthesis": True,
                "gates": {
                    "R1":"NOT_APPLICABLE",
                    "R2":"NOT_APPLICABLE",
                    "B1_CANDIDATE_BLOCK":"PASS",
                    "B1_EXISTING_OWNER_FULL_BODY":"PASS_BY_CANDIDATE_BLOCK",
                    "INDEPENDENT_REVIEW":"PASS"
                }
            }
        ]
    }

    findings = check_snapshot(snapshot)
    actual = {finding.rule_id for finding in findings}
    missing = sorted(EXECUTABLE_RULES - actual)
    if missing:
        raise SystemExit(f"P9 executable self-test failed: missing findings {missing}")
    unexpected = sorted(actual - EXECUTABLE_RULES)
    if unexpected:
        raise SystemExit(f"P9 executable self-test failed: unexpected findings {unexpected}")

    payload = json.loads(EVALS.read_text(encoding="utf-8"))
    referenced: set[str] = set()
    ids: list[str] = []
    for case in payload.get("cases", []):
        ids.append(case.get("id"))
        for expected in case.get("expected", []):
            if isinstance(expected, str):
                referenced.add(expected.split(":", 1)[0])
    if len(ids) != len(set(ids)):
        raise SystemExit("P9 executable regression corpus failed: duplicate case IDs")
    uncovered = sorted(EXECUTABLE_RULES - referenced)
    if uncovered:
        raise SystemExit(f"P9 executable regression corpus failed: uncovered rules {uncovered}")
    unknown_refs = sorted(referenced - EXECUTABLE_RULES)
    if unknown_refs:
        raise SystemExit(f"P9 executable regression corpus failed: references non-executable rules {unknown_refs}")

    print(
        "P9 executable self-test PASS: "
        f"rules={len(EXECUTABLE_RULES)} findings={len(findings)} cases={len(ids)}"
    )


if __name__ == "__main__":
    main()
