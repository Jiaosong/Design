from __future__ import annotations
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "00-governance" / "runtime" / "evolution-candidates" / "technical-drawing-successor-20260920"
class TechnicalDrawingReviewPacketTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((DIR / name).read_text(encoding="utf-8"))
    def test_packet_keeps_real_native_roundtrip_open(self):
        packet = self.load("REVIEW_DECISION_PACKET_v0.3.json")
        blockers = {row["id"]: row["state"] for row in packet["validation_blockers"]}
        self.assertEqual("OPEN", blockers["TD-BLOCK-REAL-NATIVE-ROUNDTRIP"])
        self.assertEqual("OPEN", blockers["TD-BLOCK-INDEPENDENT-REVIEW"])
        self.assertEqual("READY_FOR_INDEPENDENT_REVIEW_WITH_REAL_NATIVE_ROUNDTRIP_BLOCKER", packet["machine_readiness"])
    def test_review_template_cannot_self_validate(self):
        outcome = self.load("INDEPENDENT_REVIEW_OUTCOME_TEMPLATE_v0.3.json")
        self.assertIsNone(outcome["reviewer_id"])
        self.assertIsNone(outcome["producer_distinct"])
        self.assertEqual("PENDING", outcome["decision"])
        self.assertFalse(outcome["installation_transition_allowed"])
        self.assertEqual("PENDING_INDEPENDENT_REVIEW", outcome["state"])
    def test_gate_stays_pending(self):
        gate = self.load("LIFECYCLE_REVIEW_GATE_v0.3.json")
        self.assertEqual("PENDING", gate["independent_review"]["review_state"])
        self.assertEqual("PENDING", gate["gates"]["validated_transition_decision"])
        self.assertEqual("NOT_ELIGIBLE_UNTIL_VALIDATED", gate["gates"]["installed_owner_transition"])
if __name__ == "__main__":
    unittest.main()
