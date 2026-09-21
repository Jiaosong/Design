from __future__ import annotations
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
DIR = ROOT / "00-governance" / "runtime" / "evolution-candidates" / "professional-runtime-pack-20260920"
class ProfessionalRuntimeAdapterReviewPacketTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((DIR / name).read_text(encoding="utf-8"))
    def test_review_packet_covers_exact_contract_runtimes(self):
        contract = self.load("RUNTIME_CONTRACT_v0.1.json")
        packet = self.load("ADAPTER_REVIEW_PACKET_v0.2.json")
        self.assertEqual({r["capability_id"] for r in contract["capabilities"]}, {r["id"] for r in packet["runtimes"]})
        self.assertEqual("READY_FOR_INDEPENDENT_ADAPTER_REVIEW", packet["machine_readiness"])
        self.assertTrue(all(r["current_registration"] is False for r in packet["runtimes"]))
    def test_every_runtime_has_regression_and_reverify_contract(self):
        for row in self.load("ADAPTER_REVIEW_PACKET_v0.2.json")["runtimes"]:
            self.assertTrue(row["version_binding"])
            self.assertTrue(row["regression_baseline"])
            self.assertTrue(row["reverify_if"])
            self.assertTrue(row["candidate_consumers"])
            self.assertTrue(row["authority_ceiling"])
    def test_fresh_readback_matches_review_packet_runtime_set(self):
        packet = self.load("ADAPTER_REVIEW_PACKET_v0.2.json")
        receipt = self.load("FRESH_RUNTIME_READBACK_v0.2.json")
        self.assertEqual("PASS", receipt["workflow_result"])
        self.assertEqual({r["id"] for r in packet["runtimes"]}, {r["id"] for r in receipt["runtimes"]})
        self.assertTrue(all(r["result"] == "PASS_RUNTIME_SMOKE" for r in receipt["runtimes"]))
        self.assertEqual("FRESH_RUNTIME_READBACK_v0.2.json", packet["fresh_runtime_readback_ref"])

    def test_outcome_template_starts_pending(self):
        outcome = self.load("INDEPENDENT_REVIEW_OUTCOME_TEMPLATE_v0.2.json")
        self.assertIsNone(outcome["reviewer_id"])
        self.assertIsNone(outcome["producer_distinct"])
        self.assertEqual("PENDING_INDEPENDENT_REVIEW", outcome["state"])
        self.assertTrue(all(r["decision"] == "PENDING" for r in outcome["runtime_decisions"]))
    def test_gate_does_not_claim_current_registration(self):
        gate = self.load("LIFECYCLE_REVIEW_GATE_v0.1.json")
        self.assertEqual("REVIEW_REQUIRED", gate["verdict"])
        self.assertTrue(all(r["current_owner"] is False for r in gate["runtimes"]))
if __name__ == "__main__":
    unittest.main()
