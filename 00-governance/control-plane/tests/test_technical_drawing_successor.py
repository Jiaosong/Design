from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "00-governance" / "runtime" / "evolution-candidates" / "technical-drawing-successor-20260920" / "tools" / "validate_roundtrip.py"
SPEC = importlib.util.spec_from_file_location("td_roundtrip", VALIDATOR)
assert SPEC and SPEC.loader
td = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(td)

FIX = ROOT / "00-governance" / "runtime" / "evolution-candidates" / "technical-drawing-successor-20260920" / "fixtures" / "successor"


class TechnicalDrawingSuccessorTests(unittest.TestCase):
    def load(self, name: str):
        return json.loads((FIX / name).read_text(encoding="utf-8"))

    def test_controlled_fixture_roundtrip(self):
        self.assertEqual([], td.validate_receipt(self.load("TD-RT-01_RECEIPT.json"), ROOT))

    def test_c04_range_envelope_roundtrip(self):
        self.assertEqual([], td.validate_receipt(self.load("C04_F01_RANGE_ENVELOPE_RECEIPT_v0.3.json"), ROOT))

    def test_c04_range_is_not_collapsed(self):
        payload = self.load("C04_F01_RANGE_ENVELOPE_RECEIPT_v0.3.json")
        source = payload["source_authority"]["values"]
        expected = {row["id"]: (row["width"], row["height"]) for row in payload["expected_geometry"]}
        self.assertEqual((800.0, 120.0), expected["F01_MIN_PLAN"])
        self.assertEqual((1400.0, 180.0), expected["F01_MAX_PLAN"])
        self.assertEqual(source["width_mm"], [800, 1400])
        self.assertEqual(source["support_depth_mm"], [120, 180])
        self.assertEqual(source["top_height_mm"], [900, 1050])

    def test_self_promotion_forbidden(self):
        payload = self.load("TD-RT-01_RECEIPT.json")
        payload["result"] = "PASS_CURRENTIZATION"
        self.assertTrue(td.validate_receipt(payload, ROOT))

    def test_c01_correct_hold_preserves_no_invention(self):
        payload = self.load("C01_INTERIOR_NATIVE_DRAWING_HOLD_v0.3.json")
        self.assertEqual("CAPABILITY_HOLD", payload["execution_decision"])
        self.assertIn("Do not invent room dimensions", payload["forbidden_shortcut"])

    def test_kh_binding_does_not_claim_fresh_roundtrip(self):
        payload = self.load("KH-LY46_ADD07_EXTERNAL_NATIVE_BINDING_v0.3.json")
        self.assertEqual("EXTERNAL_PROJECT_NATIVE / NO_COPY / NO_REAUTHOR", payload["binding_mode"])
        self.assertEqual("PARTIAL", payload["currentization_evidence_state"])
        self.assertIn("fresh binary roundtrip in this branch", payload["does_not_prove"])


if __name__ == "__main__":
    unittest.main()
