from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL_ROOT = ROOT / "oleander-skills/oleander-3d-pipeline"
VALIDATOR = SKILL_ROOT / "tools/validate_receipt.py"
SCHEMA = SKILL_ROOT / "contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json"
TEMPLATES = SKILL_ROOT / "contracts/BLENDER_3D_RECEIPT_TEMPLATES_v1.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("oleander_3d_receipt_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot import OLEANDER 3D receipt validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Oleander3DPipelineReceiptValidator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.templates = json.loads(TEMPLATES.read_text(encoding="utf-8"))["templates"]

    def test_all_15_canonical_templates_validate(self):
        self.assertEqual(len(self.templates), 15)
        self.assertEqual(set(self.templates), set(self.schema["sections"]))
        for section_key, payload in self.templates.items():
            result = self.validator.validate_receipt(section_key, payload, self.schema)
            self.assertEqual(result["status"], "PASS", section_key)
            self.assertEqual(result["section"], section_key)
            self.assertEqual(result["receipt"], self.schema["sections"][section_key]["receipt"])

    def test_missing_common_field_fails_closed(self):
        payload = copy.deepcopy(self.templates["01_authority"])
        payload.pop("does_not_prove")
        with self.assertRaises(self.validator.ReceiptValidationError):
            self.validator.validate_receipt("01_authority", payload, self.schema)

    def test_source_digest_mismatch_cannot_pass(self):
        payload = copy.deepcopy(self.templates["03_blender_source_authority"])
        payload["source_after_sha256"] = "b" * 64
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "identical before/after Source digest",
        ):
            self.validator.validate_receipt("03_blender_source_authority", payload, self.schema)

    def test_authoritative_diagnostic_proxy_cannot_pass(self):
        payload = copy.deepcopy(self.templates["03_blender_source_authority"])
        payload["diagnostic_proxy_authority"] = "SOURCE_OR_WORKING_SOURCE"
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "diagnostic proxy may not be authoritative",
        ):
            self.validator.validate_receipt("03_blender_source_authority", payload, self.schema)

    def test_diagnostic_matrix_requires_exact_four_views_and_one_source_digest(self):
        payload = copy.deepcopy(self.templates["05_surface_diagnostics"])
        payload["rows"] = payload["rows"][:-1]
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "exactly one BROAD/STRIP/GRAZING/ZEBRA",
        ):
            self.validator.validate_receipt("05_surface_diagnostics", payload, self.schema)

        payload = copy.deepcopy(self.templates["05_surface_diagnostics"])
        payload["rows"][2]["source_sha256"] = "c" * 64
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "same Source digest",
        ):
            self.validator.validate_receipt("05_surface_diagnostics", payload, self.schema)

    def test_main_promotion_without_independent_review_must_hold(self):
        payload = copy.deepcopy(self.templates["13_review_gates"])
        payload["main_promotion_requested"] = True
        payload["independent_review_present"] = False
        payload["design_quality_gate"] = "KEEP"
        payload["final_promotion_state"] = "MAIN_KEEP"
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "must remain Design HOLD",
        ):
            self.validator.validate_receipt("13_review_gates", payload, self.schema)

        payload["design_quality_gate"] = "HOLD"
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "cannot be promoted without independent review",
        ):
            self.validator.validate_receipt("13_review_gates", payload, self.schema)

    def test_completion_cannot_hide_residual_blockers(self):
        payload = copy.deepcopy(self.templates["15_completion"])
        payload["residual_blockers"] = ["BLENDER_NATIVE_REOPEN_NOT_RUN"]
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "cannot retain residual blockers",
        ):
            self.validator.validate_receipt("15_completion", payload, self.schema)

        payload = copy.deepcopy(self.templates["15_completion"])
        payload["authority_boundaries_intact"] = False
        with self.assertRaisesRegex(
            self.validator.ReceiptValidationError,
            "requires intact authority boundaries",
        ):
            self.validator.validate_receipt("15_completion", payload, self.schema)


if __name__ == "__main__":
    unittest.main()
