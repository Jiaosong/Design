import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "oleander-skills" / "oleander-3d-pipeline"
VALIDATOR_PATH = SKILL / "tools" / "validate_modeling_route.py"
CONTRACT_PATH = SKILL / "contracts" / "3D_MODELING_ROUTE_CONTRACT_v1.json"
ROUTER_PATH = SKILL / "K3_MODELING_SPECIALIST_ROUTER_v2.md"

spec = importlib.util.spec_from_file_location("validate_modeling_route", VALIDATOR_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class Oleander3DV2ModelingRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def test_specialist_protocol_files_exist_without_second_current_router(self):
        paths = [
            ROUTER_PATH,
            SKILL / "REPRESENTATION_ROUTER_PROTOCOL_v1.md",
            SKILL / "structure-to-form" / "STRUCTURE_TO_FORM_PROTOCOL_v1.md",
            SKILL / "reference-reproduction" / "FEATURE_ALIGNED_CURVE_NETWORK_PROTOCOL_v1.md",
            SKILL / "domain-packs" / "automotive" / "AUTOMOTIVE_SURFACE_PACK_v1.md",
        ]
        for path in paths:
            self.assertTrue(path.exists(), path)
        self.assertFalse((SKILL / "00_CURRENT_V2_ROUTER.md").exists())

    def test_architecture_binding_preserves_oleander_system(self):
        b = self.contract["oleander_architecture_binding"]
        self.assertTrue(b["current_authority_unchanged"])
        self.assertEqual("v0.3", b["canonical_project_flow"])
        self.assertEqual("v0.3", b["project_control_plane"])
        self.assertEqual("K3_EXECUTION_ROUTER", b["kernel"])
        self.assertTrue(b["project_axis_unchanged"])
        self.assertFalse(b["system_gates_added"])
        self.assertFalse(b["system_breakers_added"])
        self.assertFalse(b["project_control_card_replaced"])
        self.assertEqual("INTERNAL_EXECUTION_STAGES_NOT_PROJECT_GATES", b["specialist_stage_ids_are"])
        self.assertEqual("CB-01_ROOT_CAUSE_RECLASSIFICATION", b["repeated_revise_breaker"])

    def test_structure_to_form_receipt_passes(self):
        receipt = {
            "schema": "oleander.3d.modeling-route-receipt.v1",
            "task_id": "TEST_ORIGINAL_PRODUCT",
            "modeling_intent": "ORIGINAL_PRODUCT",
            "route": "STRUCTURE_TO_FORM",
            "representation_family": "HYBRID",
            "source_authority_owner": "TEST_SOURCE",
            "hard_constraints": [],
            "functional_constraints": ["must operate"],
            "design_decisions": [],
            "assumptions": ["component dimensions provisional"],
            "required_stage_graph": [
                "S0_PRODUCT_INTENT",
                "S1_FUNCTIONAL_DECOMPOSITION",
                "S2_COMPONENT_GRAPH",
                "S3_INTERFACE_MOTION_GRAPH",
                "S4_PACKAGE_CLEARANCE",
                "S5_STRUCTURAL_TOPOLOGY",
                "S6_FORM_ENVELOPE",
                "S7_PRIMARY_SURFACE",
            ],
            "required_diagnostics": ["BROAD"],
            "does_not_prove": ["engineering release"],
        }
        self.assertEqual([], validator.validate_receipt(receipt, self.contract))

    def test_reference_receipt_requires_identity_curves_before_surface(self):
        receipt = {
            "schema": "oleander.3d.modeling-route-receipt.v1",
            "task_id": "TEST_REFERENCE",
            "modeling_intent": "REPRODUCE",
            "route": "REFERENCE_RECONSTRUCTION",
            "representation_family": "FEATURE_CURVE_STRUCTURED_SUBD",
            "source_authority_owner": "TEST_SOURCE",
            "hard_constraints": [],
            "functional_constraints": [],
            "design_decisions": [],
            "assumptions": [],
            "required_stage_graph": [
                "R0_REFERENCE_LOCK",
                "R1_CALIBRATION",
                "R2_HARD_POINTS_LANDMARKS",
                "R5_PRIMARY_SURFACE",
            ],
            "required_diagnostics": ["BROAD"],
            "does_not_prove": ["reference fidelity"],
        }
        errors = validator.validate_receipt(receipt, self.contract)
        self.assertTrue(any(e.startswith("STAGE_PREFIX_MISMATCH") for e in errors))
        self.assertIn("REFERENCE_STAGE_MISSING:R3_IDENTITY_FEATURE_CURVES", errors)
        self.assertIn("REFERENCE_STAGE_MISSING:R4_SECTION_NETWORK", errors)

    def test_repeated_revise_uses_existing_cb01_not_new_gate(self):
        rr = self.contract["representation_reopening"]
        self.assertEqual("CB-01_REPEATED_REVISE_BREAKER", rr["control_plane_owner"])
        self.assertEqual(2, rr["trigger_after_consecutive_visual_or_project_revise"])
        self.assertEqual("ROOT_CAUSE_RECLASSIFICATION", rr["required_first_action"])
        self.assertEqual("REOPEN_REPRESENTATION_MODEL", rr["specialist_action_when_representation_is_causal"])
        text = ROUTER_PATH.read_text(encoding="utf-8")
        self.assertIn("Do **not** create a new Representation Escalation Gate", text)
        self.assertIn("K3 Execution Router", text)
        self.assertIn("STRUCTURE_TO_FORM", text)
        self.assertIn("REFERENCE_RECONSTRUCTION", text)

    def test_structure_protocol_forbids_styling_before_package(self):
        text = (SKILL / "structure-to-form" / "STRUCTURE_TO_FORM_PROTOCOL_v1.md").read_text(encoding="utf-8")
        self.assertLess(text.index("S4 Package & Clearance"), text.index("S7 Primary Surface"))
        self.assertIn("shrinking unknown internals", text)
        self.assertIn("not OLEANDER P0–P4 project levels", text)

    def test_feature_curve_protocol_has_held_out_validation(self):
        text = (SKILL / "reference-reproduction" / "FEATURE_ALIGNED_CURVE_NETWORK_PROTOCOL_v1.md").read_text(encoding="utf-8")
        self.assertIn("Fit vs held-out validation", text)
        self.assertIn("structured patch cage", text)
        self.assertIn("Aperture rule", text)
        self.assertIn("CB-01", text)
        self.assertNotIn("STOP_PARAMETER_TUNING_REOPEN_REPRESENTATION", text)


if __name__ == "__main__":
    unittest.main()
