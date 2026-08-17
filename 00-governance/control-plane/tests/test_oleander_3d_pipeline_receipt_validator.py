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

    def validate(self, section_key, payload):
        return self.validator.validate_receipt(section_key, payload, self.schema)

    def assert_invalid(self, section_key, payload, pattern=None):
        context = (
            self.assertRaisesRegex(self.validator.ReceiptValidationError, pattern)
            if pattern
            else self.assertRaises(self.validator.ReceiptValidationError)
        )
        with context:
            self.validate(section_key, payload)

    def test_all_15_canonical_templates_validate_with_section_specific_rules(self):
        self.assertEqual(len(self.templates), 15)
        self.assertEqual(set(self.templates), set(self.schema["sections"]))
        self.assertEqual(
            set(self.schema["sections"]),
            set(self.validator.SECTION_KEYS_WITH_SPECIFIC_RULES),
        )
        for section_key, payload in self.templates.items():
            with self.subTest(section=section_key):
                result = self.validate(section_key, payload)
                self.assertEqual(result["status"], "PASS")
                self.assertEqual(result["section"], section_key)
                self.assertEqual(
                    result["receipt"],
                    self.schema["sections"][section_key]["receipt"],
                )
                self.assertTrue(result["section_specific_rule"])

    def test_missing_common_field_fails_closed(self):
        payload = copy.deepcopy(self.templates["01_authority"])
        payload.pop("does_not_prove")
        self.assert_invalid("01_authority", payload)

    def test_every_section_has_a_real_false_pass_rejection(self):
        cases = []

        p = copy.deepcopy(self.templates["01_authority"])
        p["scale"] = 0
        cases.append(("01_authority", p))

        p = copy.deepcopy(self.templates["02_state_classification"])
        p["rows"].append(copy.deepcopy(p["rows"][0]))
        cases.append(("02_state_classification", p))

        p = copy.deepcopy(self.templates["03_blender_source_authority"])
        p["source_after_sha256"] = "b" * 64
        cases.append(("03_blender_source_authority", p))

        p = copy.deepcopy(self.templates["04_sparse_edit"])
        p["new_value"] = 1.0
        cases.append(("04_sparse_edit", p))

        p = copy.deepcopy(self.templates["05_surface_diagnostics"])
        p["rows"] = p["rows"][:-1]
        cases.append(("05_surface_diagnostics", p))

        p = copy.deepcopy(self.templates["06_geometry_topology"])
        p["source_form_quality_not_inferred"] = False
        cases.append(("06_geometry_topology", p))

        p = copy.deepcopy(self.templates["07_spatial_models"])
        p["rows"][0]["field_status"] = "FIELD_VERIFIED"
        cases.append(("07_spatial_models", p))

        p = copy.deepcopy(self.templates["08_materials_cmf"])
        p["rows"][0]["claim_level"] = "PRODUCTION_CMF_DECISION"
        cases.append(("08_materials_cmf", p))

        p = copy.deepcopy(self.templates["09_camera_render"])
        p["drift_detected"] = True
        cases.append(("09_camera_render", p))

        p = copy.deepcopy(self.templates["10_technical_outputs"])
        p["vector_text_confirmed"] = False
        cases.append(("10_technical_outputs", p))

        p = copy.deepcopy(self.templates["11_exchange_roundtrip"])
        p["source_authority_unchanged"] = False
        cases.append(("11_exchange_roundtrip", p))

        p = copy.deepcopy(self.templates["12_production_artifacts"])
        p["rows"][0]["bytes"] = 0
        cases.append(("12_production_artifacts", p))

        p = copy.deepcopy(self.templates["13_review_gates"])
        p["design_quality_gate"] = "KEEP"
        p["independent_review_present"] = False
        cases.append(("13_review_gates", p))

        p = copy.deepcopy(self.templates["14_failure_routing"])
        p["changed_variable"] = p["controlled_variables"][0]
        cases.append(("14_failure_routing", p))

        p = copy.deepcopy(self.templates["15_completion"])
        p["machine_gate"] = "FAIL"
        cases.append(("15_completion", p))

        self.assertEqual(len(cases), 15)
        for section_key, payload in cases:
            with self.subTest(section=section_key):
                self.assert_invalid(section_key, payload)

    def test_source_authority_specific_guards(self):
        payload = copy.deepcopy(self.templates["03_blender_source_authority"])
        payload["diagnostic_proxy_authority"] = "SOURCE_OR_WORKING_SOURCE"
        self.assert_invalid(
            "03_blender_source_authority",
            payload,
            "diagnostic proxy may not be authoritative",
        )

        payload = copy.deepcopy(self.templates["03_blender_source_authority"])
        payload["material_slots_preserved"] = False
        self.assert_invalid(
            "03_blender_source_authority",
            payload,
            "material_slots_preserved=true",
        )

    def test_sparse_edit_requires_bounded_causal_delta_and_rollback(self):
        payload = copy.deepcopy(self.templates["04_sparse_edit"])
        payload["rollback_value"] = payload["previous_value"] + 0.01
        self.assert_invalid("04_sparse_edit", payload, "rollback_value")

        payload = copy.deepcopy(self.templates["04_sparse_edit"])
        payload["new_value"] = payload["previous_value"]
        self.assert_invalid("04_sparse_edit", payload, "no-op")

    def test_diagnostic_matrix_requires_exact_four_views_and_one_source_digest(self):
        payload = copy.deepcopy(self.templates["05_surface_diagnostics"])
        payload["rows"] = payload["rows"][:-1]
        self.assert_invalid(
            "05_surface_diagnostics",
            payload,
            "exactly one BROAD/STRIP/GRAZING/ZEBRA",
        )

        payload = copy.deepcopy(self.templates["05_surface_diagnostics"])
        payload["rows"][2]["source_sha256"] = "c" * 64
        self.assert_invalid(
            "05_surface_diagnostics",
            payload,
            "same Source digest",
        )

    def test_spatial_evidence_cannot_promote_assumption_to_field_measurement(self):
        payload = copy.deepcopy(self.templates["07_spatial_models"])
        payload["rows"][0]["field_status"] = "FIELD_MEASURED"
        self.assert_invalid("07_spatial_models", payload, "non-measured evidence")

    def test_cmf_physical_claim_requires_physical_evidence(self):
        payload = copy.deepcopy(self.templates["08_materials_cmf"])
        payload["rows"][0]["claim_level"] = "MEASURED_PHYSICAL_FINISH"
        self.assert_invalid("08_materials_cmf", payload, "requires physical evidence")

    def test_review_gate_cannot_self_promote(self):
        payload = copy.deepcopy(self.templates["13_review_gates"])
        payload["main_promotion_requested"] = True
        payload["independent_review_present"] = False
        payload["design_quality_gate"] = "KEEP"
        payload["final_promotion_state"] = "MAIN_KEEP"
        self.assert_invalid(
            "13_review_gates",
            payload,
            "Design KEEP requires independent review|must remain Design HOLD",
        )

        payload = copy.deepcopy(self.templates["13_review_gates"])
        payload["main_promotion_requested"] = True
        payload["independent_review_present"] = True
        payload["design_quality_gate"] = "KEEP"
        payload["design_review_system_or_reviewer"] = payload["producer"]
        payload["final_promotion_state"] = "MAIN_KEEP"
        self.assert_invalid("13_review_gates", payload, "producer cannot be recorded")

    def test_completion_cannot_hide_blockers_or_incomplete_requested_deliverables(self):
        payload = copy.deepcopy(self.templates["15_completion"])
        payload["residual_blockers"] = ["BLENDER_NATIVE_REOPEN_NOT_RUN"]
        self.assert_invalid("15_completion", payload, "cannot retain residual blockers")

        payload = copy.deepcopy(self.templates["15_completion"])
        payload["authority_boundaries_intact"] = False
        self.assert_invalid("15_completion", payload, "requires intact authority boundaries")

        payload = copy.deepcopy(self.templates["15_completion"])
        requested = payload["requested_deliverables"][0]
        payload["deliverable_statuses"][requested] = "MISSING"
        self.assert_invalid("15_completion", payload, "is not complete")


if __name__ == "__main__":
    unittest.main()
