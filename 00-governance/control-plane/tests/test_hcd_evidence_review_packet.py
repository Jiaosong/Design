from __future__ import annotations
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "00-governance" / "runtime" / "evolution-candidates" / "hcd-browser-execution-binding-20260920"
class HCDEvidenceReviewPacketTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((DIR / name).read_text(encoding="utf-8"))
    def test_packet_keeps_human_validation_blocked(self):
        packet = self.load("EVIDENCE_REVIEW_PACKET_v0.2.json")
        joined = " | ".join(packet["blocking_findings"]).lower()
        self.assertIn("representative-user", joined)
        self.assertIn("accessibility", joined)
        self.assertEqual("READY_FOR_INDEPENDENT_BOUNDARY_REVIEW", packet["machine_readiness"])
    def test_allowed_transition_is_bounded_evidence_only(self):
        packet = self.load("EVIDENCE_REVIEW_PACKET_v0.2.json")
        self.assertEqual("CANDIDATE_EVIDENCE_BINDING -> MERGEABLE_BOUNDED_PROJECT_EVIDENCE", packet["allowed_transition"])
        self.assertIn("HCD_PROCESS_CURRENT", packet["forbidden_transitions"])
        self.assertIn("ACCESSIBILITY_CONFORMANCE", packet["forbidden_transitions"])
    def test_tested_artifact_evidence_is_not_widened_to_whole_pr_head(self):
        packet = self.load("EVIDENCE_REVIEW_PACKET_v0.2.json")
        rb = packet["source_project_evidence"]["applicability_readback"]
        self.assertTrue(rb["tested_head_is_ancestor_of_current_pr_head"])
        self.assertFalse(rb["app_implementation_changed_after_tested_head"])
        self.assertIn("tested app artifact/configuration", rb["evidence_ceiling"])
        self.assertTrue(rb["stale_if"])

    def test_outcome_template_cannot_promote_hcd(self):
        outcome = self.load("INDEPENDENT_REVIEW_OUTCOME_TEMPLATE_v0.2.json")
        self.assertEqual("PENDING", outcome["decision"])
        self.assertIsNone(outcome["reviewer_id"])
        self.assertIsNone(outcome["accepted_transition"])
        self.assertIn("HCD_PROCESS_CURRENT", outcome["forbidden_transitions"])
    def test_capability_plan_remains_partial(self):
        plan = self.load("C04_HCD_DP4_EXECUTION_CAPABILITY_PLAN_v0.1.json")
        self.assertEqual("PARTIAL", plan["plan_verdict"])
        self.assertTrue(plan["blocking_capability_ids"])
if __name__ == "__main__":
    unittest.main()
