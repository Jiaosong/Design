from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "00-governance" / "schemas" / "validate_professional_execution_capability_plan.py"
PLAN = ROOT / "00-governance" / "runtime" / "evolution-candidates" / "hcd-browser-execution-binding-20260920" / "C04_HCD_DP4_EXECUTION_CAPABILITY_PLAN_v0.1.json"

SPEC = importlib.util.spec_from_file_location("capplan", VALIDATOR)
assert SPEC and SPEC.loader
capplan = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capplan)


class HCDBrowserExecutionBindingTests(unittest.TestCase):
    def load(self):
        return json.loads(PLAN.read_text(encoding="utf-8"))

    def test_partial_plan_is_schema_semantically_valid(self):
        self.assertEqual([], capplan.validate_payload(self.load()))

    def test_browser_surface_available_but_hcd_still_blocked(self):
        payload = self.load()
        rows = {row["capability_id"]: row for row in payload["capabilities"]}
        self.assertEqual("AVAILABLE", rows["HCD-CAP-BROWSER-SURFACE"]["availability_state"])
        self.assertEqual("CANDIDATE_ONLY", rows["HCD-CAP-INTERACTION-OWNER"]["execution_mode"])
        self.assertIn("HCD-CAP-USABILITY-RESEARCH", payload["blocking_capability_ids"])
        self.assertIn("HCD-CAP-ACCESSIBILITY-EVALUATION", payload["blocking_capability_ids"])
        self.assertEqual("PARTIAL", payload["plan_verdict"])

    def test_browser_pass_cannot_be_relabelled_executable_hcd_plan(self):
        payload = self.load()
        payload["plan_verdict"] = "EXECUTABLE"
        payload["blocking_capability_ids"] = []
        self.assertTrue(capplan.validate_payload(payload))


if __name__ == "__main__":
    unittest.main()
