from __future__ import annotations

import json
import py_compile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V013 = ROOT / "90-shared/toolchains/modeling-worker/v0.13"


class ModelingWorkerV013R3Interface(unittest.TestCase):
    def test_r3_contract_is_source_level_and_non_promotional(self):
        source = json.loads((V013 / "G1_PRIMARY_CURVE_SOURCE.json").read_text(encoding="utf-8"))
        contract = json.loads((V013 / "G1_R3_INTERFACE_FAIRNESS_CONTRACT.json").read_text(encoding="utf-8"))
        variants = json.loads((V013 / "G1_R3_INTERFACE_RELATION_VARIANTS.json").read_text(encoding="utf-8"))

        self.assertEqual(contract["schema"], "oleander.modeling-worker.v0.13.g1.r3.interface-fairness-contract.v1")
        self.assertEqual(contract["design_state"], "REVISE")
        self.assertEqual(contract["authority_state"], "WORKING_SOURCE")
        self.assertEqual(contract["candidate_promotion"], "NOT_RUN")
        self.assertEqual(contract["source_policy"]["allowed_source_family"], "INTERFACE_DECK_BOUNDARY")
        self.assertTrue(contract["source_policy"]["mesh_local_patch_forbidden"])
        self.assertTrue(contract["source_policy"]["hidden_sculpt_correction_forbidden"])
        self.assertFalse(contract["source_policy"]["derived_mesh_is_authority"])
        self.assertEqual(contract["source_policy"]["theta_center_semantics_locked"], "TOP_MERIDIAN")
        self.assertEqual(contract["source_policy"]["preserve_r2_depth_m"], 0.012)
        self.assertEqual(contract["gate_role"], "WORKING_DESIGN_DIAGNOSTIC_ONLY_NOT_PROMOTION_EVIDENCE")

        broad = source["machine_thresholds"]
        basis = contract["threshold_basis"]
        self.assertEqual(basis["broad_longitudinal_deg_per_0_01u"], broad["max_longitudinal_normal_delta_deg_per_0_01u"])
        self.assertEqual(basis["broad_circumferential_deg_per_0_05rad"], broad["max_circumferential_normal_delta_deg_per_0_05rad"])
        self.assertEqual(basis["derived_working_limits"]["max_longitudinal_deg_per_0_01u"], 8.0)
        self.assertEqual(basis["derived_working_limits"]["p95_longitudinal_deg_per_0_01u"], 6.0)
        self.assertEqual(basis["derived_working_limits"]["max_circumferential_deg_per_0_05rad"], 12.0)
        self.assertEqual(basis["derived_working_limits"]["p95_circumferential_deg_per_0_05rad"], 10.0)
        self.assertEqual(basis["threshold_status"], "WORKING_R3_DIAGNOSTIC_THRESHOLD_NOT_UNIVERSAL_CLASS_A_CRITERION")

        self.assertEqual(variants["allowed_source_family"], "INTERFACE_DECK_BOUNDARY")
        self.assertFalse(variants["mesh_local_patch_allowed"])
        self.assertEqual(variants["locked_values"]["theta_center"], "TOP_MERIDIAN")
        self.assertEqual(variants["locked_values"]["depth_m"], 0.012)
        self.assertEqual(len(variants["variants"]), 3)
        allowed = {"u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"}
        for row in variants["variants"]:
            self.assertTrue(set(row["source_overrides"]).issubset(allowed))
            self.assertEqual(row["source_overrides"]["depth_m"], 0.012)

    def test_r3_scripts_compile_and_reuse_shared_surface_runtime(self):
        fairness = V013 / "g1_r3_interface_fairness.py"
        visual = V013 / "g1_r3_blender_visual.py"
        py_compile.compile(str(fairness), doraise=True)
        py_compile.compile(str(visual), doraise=True)

        fairness_code = fairness.read_text(encoding="utf-8")
        visual_code = visual.read_text(encoding="utf-8")
        self.assertIn("core < rho < 1.0", fairness_code)
        self.assertIn("qa.normal", fairness_code)
        self.assertIn("WORKING_SOURCE_EXPERIMENT_NOT_PROMOTED", fairness_code)
        self.assertIn("iso.load_surface_runtime(binding)", visual_code)
        self.assertIn("surface_runtime.render_setup", visual_code)
        self.assertIn("surface_runtime.render(", visual_code)
        self.assertIn("rt.extract_native_source(template)", visual_code)
        self.assertIn("set_deck_values(deck, original)", visual_code)
        self.assertNotIn("\ndef material(", visual_code)
        self.assertNotIn("\ndef camera(", visual_code)
        self.assertNotIn("\ndef render_setup(", visual_code)


if __name__ == "__main__":
    unittest.main()
