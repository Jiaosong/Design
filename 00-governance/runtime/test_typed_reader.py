#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from render_typed_reader import render

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / "00-governance" / "runtime" / "OLEANDER_TYPED_READER_FIXTURES_v0.1.json"


def load() -> dict:
    return json.loads(FIXTURES.read_text(encoding="utf-8"))


def main() -> None:
    data = load()
    fixtures = {f["fixture_id"]: f for f in data["fixtures"]}

    fx1 = fixtures["READER-FX-001-CURRENT-UNPROVEN"]
    p1 = render(fx1["snapshot"], fx1["query"])
    assert p1["identity"]["is_current"] is True
    assert p1["states"]["retrieval_space"] == "CURRENT"
    assert p1["states"]["professional_state"] == "NOT_PROVEN_PROFESSIONAL_PASS"
    assert p1["states"]["bilingual_state"] == "REVISE"
    assert p1["states"]["independent_review_state"] == "HOLD"
    assert p1["single_aggregate_pass_badge"] is False
    assert "CURRENT_RETRIEVAL_DOES_NOT_IMPLY_PROFESSIONAL_PASS" in p1["warnings"]

    fx2 = fixtures["READER-FX-002-SUPPORT-PASS-PARENT-REVISE"]
    p2 = render(fx2["snapshot"], fx2["query"])
    assert p2["states"]["authority_state"] == "WORKING_DESIGN_CANDIDATE_NO_PROMOTION"
    assert p2["states"]["design_review_state"] == "REVISE"
    assert p2["target_results"] == {"G1":"REVISE","G2":"REVISE","G3":"REVISE","G4":"PASS","G5":"PASS","G6":"REVISE"}
    assert len(p2["related_support"]) == 1
    assert p2["related_support"][0]["assurance_result"] == "PASS_SUPPORT_ONLY_PROGRAM_OVERLAY"
    assert "DESIGN_QUALITY_KEEP" in p2["related_support"][0]["does_not_establish"]
    assert p2["single_aggregate_pass_badge"] is False
    assert "BOUNDED_SUPPORT_RESULT_COEXISTS_WITH_UNRESOLVED_PARENT_DESIGN_STATE" in p2["warnings"]
    assert "MIXED_TARGET_RESULTS_PRESERVED" in p2["warnings"]

    print("typed reader self-test PASS: independent state axes and scoped support results preserved")


if __name__ == "__main__":
    main()
