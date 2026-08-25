from __future__ import annotations

import json
import py_compile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V013 = ROOT / "90-shared/toolchains/modeling-worker/v0.13"
SURFACE_V120 = ROOT / "90-shared/toolchains/blender-surface-system/v1.20.0"
SURFACE_RUNTIME = SURFACE_V120 / "f1_design_validation_runtime.py"
SURFACE_CONTRACT = SURFACE_V120 / "CMF_PRESET_CONTRACT_v1.20.0.json"


class ModelingWorkerV013BlenderBridge(unittest.TestCase):
    def test_blender_bridge_contract_and_scripts_compile(self):
        contract = json.loads((V013 / "G1_R2_BLENDER_EXECUTION_CONTRACT.json").read_text(encoding="utf-8"))
        binding = json.loads((V013 / "G1_R2_BLENDER_SURFACE_BINDING.json").read_text(encoding="utf-8"))
        isolation = json.loads((V013 / "G1_R2_TOPOLOGY_ISOLATION_CONTRACT.json").read_text(encoding="utf-8"))
        surface_contract = json.loads(SURFACE_CONTRACT.read_text(encoding="utf-8"))

        self.assertEqual(contract["schema"], "oleander.modeling-worker.v0.13.g1.r2.blender-execution-contract.v3")
        self.assertEqual(contract["benchmark_id"], "MW-V013-G1-ERGONOMIC-HANDHELD-SHELL")
        self.assertEqual(contract["runtime"]["blender"], "5.2.0 LTS")
        self.assertEqual(contract["runtime"]["engine"], "CYCLES")
        self.assertEqual(contract["design_state"], "REVISE")
        self.assertEqual(contract["authority_state"], "WORKING_SOURCE")
        self.assertEqual(contract["candidate_review"], "REOPENED")
        self.assertEqual(contract["candidate_promotion"], "NOT_RUN")
        self.assertTrue(contract["debug_contract"]["derived_mesh_is_not_source_authority"])
        self.assertTrue(contract["debug_contract"]["blender_native_source_is_editable"])
        self.assertTrue(contract["debug_contract"]["native_source_readback_required"])
        self.assertTrue(contract["debug_contract"]["native_edit_to_derived_rebuild_required"])
        self.assertTrue(contract["debug_contract"]["self_contained_rebuild_text_required"])
        self.assertTrue(contract["debug_contract"]["saved_blend_reopen_rebuild_required"])
        self.assertTrue(contract["debug_contract"]["bootstrap_seed_overwrite_forbidden"])
        self.assertTrue(contract["debug_contract"]["same_source_across_topology_ab_required"])
        self.assertTrue(contract["debug_contract"]["alternate_topology_not_authority"])
        self.assertTrue(contract["debug_contract"]["analytic_source_space_probe_required"])
        self.assertTrue(contract["debug_contract"]["surface_system_runtime_shared_for_topology_ab"])
        self.assertTrue(contract["debug_contract"]["topology_isolation_cannot_promote_candidate"])
        self.assertTrue(contract["roundtrip"]["saved_blend_reopen_rebuild_required"])
        self.assertEqual(contract["roundtrip"]["saved_blend_reopen_report"], "G1_R2_BLENDER_REOPEN_REBUILD_REPORT.json")
        self.assertEqual(contract["roundtrip"]["bootstrap_readback_tolerance_m"], 1e-8)

        topology = contract["topology_source_isolation"]
        self.assertTrue(topology["required"])
        self.assertTrue(topology["same_native_source_required"])
        self.assertTrue(topology["source_edit_forbidden"])
        self.assertTrue(topology["shared_surface_system_runtime_required"])
        self.assertTrue(topology["analytic_source_probe_required"])
        self.assertTrue(topology["promotion_from_isolation_forbidden"])
        self.assertEqual(topology["baseline_topology"], {"u_rings": 56, "circumferential_samples": 72})
        self.assertEqual(topology["dense_topology"], {"u_rings": 112, "circumferential_samples": 144})
        self.assertEqual(set(topology["paired_visual_rigs"]), {"STRIP", "GRAZING", "ZEBRA"})
        self.assertEqual(len(contract["required_isolation_diagnostics"]), 6)

        self.assertEqual(isolation["authority_state"], "WORKING_SOURCE")
        self.assertEqual(isolation["design_state"], "REVISE")
        self.assertEqual(isolation["candidate_promotion"], "NOT_RUN")
        self.assertTrue(isolation["source_policy"]["same_blender_native_working_source_required"])
        self.assertTrue(isolation["source_policy"]["source_edit_forbidden_during_isolation"])
        self.assertTrue(isolation["source_policy"]["mesh_local_patch_forbidden"])
        self.assertFalse(isolation["source_policy"]["derived_topology_is_authority"])
        self.assertEqual(isolation["topologies"]["baseline"], topology["baseline_topology"])
        self.assertEqual(isolation["topologies"]["dense"], topology["dense_topology"])
        self.assertEqual(len(isolation["outputs"]["renders"]), 6)
        self.assertTrue(isolation["classification"]["promotion_forbidden"])

        self.assertEqual(binding["schema"], "oleander.modeling-worker.v0.13.blender-surface-binding.v3")
        self.assertEqual(binding["blender_surface_system"]["version"], "v1.20.0")
        self.assertEqual(binding["blender_surface_system"]["version"], surface_contract["version"])
        self.assertEqual(binding["blender_surface_system"]["fidelity"], surface_contract["fidelity"])
        self.assertEqual(binding["runtime_binding"]["mode"], "EXECUTABLE_SHARED_RUNTIME")
        self.assertEqual(binding["runtime_binding"]["api"], "oleander.blender-surface-system.f1-runtime.v1")
        self.assertEqual(
            binding["runtime_binding"]["module"],
            "90-shared/toolchains/blender-surface-system/v1.20.0/f1_design_validation_runtime.py",
        )
        self.assertEqual(
            binding["runtime_binding"]["contract"],
            "90-shared/toolchains/blender-surface-system/v1.20.0/CMF_PRESET_CONTRACT_v1.20.0.json",
        )
        self.assertTrue(binding["runtime_binding"]["local_parallel_runtime_forbidden"])
        self.assertTrue(
            set(binding["blender_surface_system"]["required_lighting_rigs"]).issubset(
                set(surface_contract["lighting_rigs"])
            )
        )
        self.assertEqual(
            binding["source_authority"]["live_representation_after_bootstrap"],
            "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE",
        )
        self.assertEqual(
            binding["source_authority"]["locked_semantics"]["INTERFACE_DECK_BOUNDARY.theta_center"],
            "TOP_MERIDIAN",
        )
        self.assertTrue(binding["source_authority"]["native_readback_required"])
        self.assertTrue(binding["source_authority"]["native_edit_to_derived_rebuild_required"])
        self.assertEqual(binding["roundtrip_gate"]["bootstrap_readback_tolerance_m"], 1e-8)
        self.assertEqual(len(contract["native_source_objects"]), 6)
        self.assertEqual(len(contract["required_diagnostics"]), 8)

        for filename in (
            "g1_r2_blender_scene.py",
            "g1_r2_blender_roundtrip.py",
            "g1_r2_blender_rebuild.py",
            "g1_r2_blender_reopen_verify.py",
            "g1_r2_blender_entry.py",
            "g1_r2_topology_isolation.py",
        ):
            py_compile.compile(str(V013 / filename), doraise=True)
        py_compile.compile(str(SURFACE_RUNTIME), doraise=True)

    def test_surface_system_runtime_is_not_duplicated_inside_modeling_worker(self):
        entry = (V013 / "g1_r2_blender_entry.py").read_text(encoding="utf-8")
        isolation = (V013 / "g1_r2_topology_isolation.py").read_text(encoding="utf-8")
        scene = (V013 / "g1_r2_blender_scene.py").read_text(encoding="utf-8")
        runtime = SURFACE_RUNTIME.read_text(encoding="utf-8")

        self.assertIn("load_surface_system_runtime(binding)", entry)
        self.assertIn('binding["runtime_binding"]["project_rig_profile"]', entry)
        self.assertIn("surface_runtime.render_setup", entry)
        self.assertIn("surface_runtime.build_project_rigs", entry)
        self.assertIn("surface_runtime.render(", entry)
        self.assertIn("load_surface_runtime(binding)", isolation)
        self.assertIn("surface_runtime.render(", isolation)
        self.assertNotIn("\ndef material(", scene)
        self.assertNotIn("\ndef rigs(", scene)
        self.assertNotIn("\ndef render_setup(", scene)
        self.assertNotIn("\ndef material(", isolation)
        self.assertNotIn("\ndef camera(", isolation)
        self.assertNotIn("\ndef render_setup(", isolation)
        self.assertIn('RUNTIME_API = "oleander.blender-surface-system.f1-runtime.v1"', runtime)
        self.assertIn("def validate_binding(", runtime)
        self.assertIn("def build_project_rigs(", runtime)
        self.assertIn("def render_setup(", runtime)

    def test_topology_isolation_preserves_source_authority_boundary(self):
        isolation_code = (V013 / "g1_r2_topology_isolation.py").read_text(encoding="utf-8")
        isolation_contract = json.loads((V013 / "G1_R2_TOPOLOGY_ISOLATION_CONTRACT.json").read_text(encoding="utf-8"))
        self.assertIn("rt.extract_native_source(template)", isolation_code)
        self.assertIn("rt.source_difference(source_before, source_after)", isolation_code)
        self.assertIn('"DERIVED_EXECUTION_NOT_AUTHORITY"', isolation_code)
        self.assertIn("analytic_source_hotspots", isolation_code)
        self.assertIn("image_difference", isolation_code)
        self.assertIn("TOPOLOGY_INVARIANT_SOURCE_RELATION_SUSPECTED", isolation_code)
        self.assertIn("TOPOLOGY_SENSITIVE_EXECUTION_GEOMETRY_SUSPECTED", isolation_code)
        self.assertEqual(isolation_contract["visual_ab"]["threshold_role"], "DIAGNOSTIC_HEURISTIC_ONLY_NOT_PROMOTION_EVIDENCE")
        self.assertTrue(isolation_contract["classification"]["promotion_forbidden"])

    def test_blender_bridge_binds_existing_r2_authority_as_immutable_bootstrap(self):
        source = json.loads((V013 / "G1_PRIMARY_CURVE_SOURCE.json").read_text(encoding="utf-8"))
        fix = json.loads((V013 / "G1_R2_RELATION_CORRECTION.json").read_text(encoding="utf-8"))
        contract = json.loads((V013 / "G1_R2_BLENDER_EXECUTION_CONTRACT.json").read_text(encoding="utf-8"))
        binding = json.loads((V013 / "G1_R2_BLENDER_SURFACE_BINDING.json").read_text(encoding="utf-8"))
        self.assertEqual(source["authority"], "WORKING_SURFACE_SOURCE")
        self.assertFalse(source["derived_execution"]["editable_authority"])
        self.assertFalse(fix["mesh_local_patch_allowed"])
        self.assertEqual(contract["source_binding"]["bootstrap_primary_curve_source"], "G1_PRIMARY_CURVE_SOURCE.json")
        self.assertEqual(contract["source_binding"]["bootstrap_r2_relation_correction"], "G1_R2_RELATION_CORRECTION.json")
        self.assertEqual(contract["source_binding"]["bootstrap_role"], "IMMUTABLE_SEED_AND_PROVENANCE")
        self.assertEqual(contract["source_binding"]["live_role_after_bootstrap"], "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE")
        self.assertTrue(contract["roundtrip"]["overwrite_bootstrap_seed_forbidden"])
        self.assertEqual(contract["roundtrip"]["controlled_native_edit"]["only_family"], "THUMB_SIDE_PLAN")
        self.assertTrue(contract["topology_source_isolation"]["same_native_source_required"])
        self.assertTrue(contract["topology_source_isolation"]["source_edit_forbidden"])
        self.assertTrue(contract["topology_source_isolation"]["promotion_from_isolation_forbidden"])
        self.assertEqual(
            binding["roundtrip_gate"]["writeback_policy"],
            "WRITE_NEW_ROUNDTRIP_SNAPSHOT; DO NOT_OVERWRITE_BOOTSTRAP_SEED",
        )


if __name__ == "__main__":
    unittest.main()
