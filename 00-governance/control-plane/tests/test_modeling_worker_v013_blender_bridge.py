from __future__ import annotations

import json
import py_compile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
V013 = ROOT / '90-shared/toolchains/modeling-worker/v0.13'


class ModelingWorkerV013BlenderBridge(unittest.TestCase):
    def test_blender_bridge_contract_and_scripts_compile(self):
        contract = json.loads((V013 / 'G1_R2_BLENDER_EXECUTION_CONTRACT.json').read_text(encoding='utf-8'))
        binding = json.loads((V013 / 'G1_R2_BLENDER_SURFACE_BINDING.json').read_text(encoding='utf-8'))
        self.assertEqual(contract['benchmark_id'], 'MW-V013-G1-ERGONOMIC-HANDHELD-SHELL')
        self.assertEqual(contract['runtime']['blender'], '5.2.0 LTS')
        self.assertEqual(contract['runtime']['engine'], 'CYCLES')
        self.assertEqual(contract['design_state'], 'REVISE')
        self.assertEqual(contract['authority_state'], 'WORKING_SOURCE')
        self.assertEqual(contract['candidate_review'], 'REOPENED')
        self.assertEqual(contract['candidate_promotion'], 'NOT_RUN')
        self.assertTrue(contract['debug_contract']['derived_mesh_is_not_source_authority'])
        self.assertTrue(contract['debug_contract']['blender_native_source_is_editable'])
        self.assertTrue(contract['debug_contract']['native_source_readback_required'])
        self.assertTrue(contract['debug_contract']['native_edit_to_derived_rebuild_required'])
        self.assertTrue(contract['debug_contract']['self_contained_rebuild_text_required'])
        self.assertTrue(contract['debug_contract']['saved_blend_reopen_rebuild_required'])
        self.assertTrue(contract['debug_contract']['bootstrap_seed_overwrite_forbidden'])
        self.assertTrue(contract['roundtrip']['saved_blend_reopen_rebuild_required'])
        self.assertEqual(contract['roundtrip']['saved_blend_reopen_report'], 'G1_R2_BLENDER_REOPEN_REBUILD_REPORT.json')
        self.assertEqual(contract['roundtrip']['bootstrap_readback_tolerance_m'], 1e-8)
        self.assertEqual(binding['schema'], 'oleander.modeling-worker.v0.13.blender-surface-binding.v2')
        self.assertEqual(binding['blender_surface_system']['version'], 'v1.20.0')
        self.assertEqual(binding['source_authority']['live_representation_after_bootstrap'], 'BLENDER_NATIVE_EDITABLE_WORKING_SOURCE')
        self.assertEqual(binding['source_authority']['locked_semantics']['INTERFACE_DECK_BOUNDARY.theta_center'], 'TOP_MERIDIAN')
        self.assertTrue(binding['source_authority']['native_readback_required'])
        self.assertTrue(binding['source_authority']['native_edit_to_derived_rebuild_required'])
        self.assertEqual(binding['roundtrip_gate']['bootstrap_readback_tolerance_m'], 1e-8)
        self.assertEqual(len(contract['native_source_objects']), 6)
        self.assertEqual(len(contract['required_diagnostics']), 8)
        for filename in (
            'g1_r2_blender_scene.py',
            'g1_r2_blender_roundtrip.py',
            'g1_r2_blender_rebuild.py',
            'g1_r2_blender_reopen_verify.py',
            'g1_r2_blender_entry.py',
        ):
            py_compile.compile(str(V013 / filename), doraise=True)

    def test_blender_bridge_binds_existing_r2_authority_as_immutable_bootstrap(self):
        source = json.loads((V013 / 'G1_PRIMARY_CURVE_SOURCE.json').read_text(encoding='utf-8'))
        fix = json.loads((V013 / 'G1_R2_RELATION_CORRECTION.json').read_text(encoding='utf-8'))
        contract = json.loads((V013 / 'G1_R2_BLENDER_EXECUTION_CONTRACT.json').read_text(encoding='utf-8'))
        binding = json.loads((V013 / 'G1_R2_BLENDER_SURFACE_BINDING.json').read_text(encoding='utf-8'))
        self.assertEqual(source['authority'], 'WORKING_SURFACE_SOURCE')
        self.assertFalse(source['derived_execution']['editable_authority'])
        self.assertFalse(fix['mesh_local_patch_allowed'])
        self.assertEqual(contract['source_binding']['bootstrap_primary_curve_source'], 'G1_PRIMARY_CURVE_SOURCE.json')
        self.assertEqual(contract['source_binding']['bootstrap_r2_relation_correction'], 'G1_R2_RELATION_CORRECTION.json')
        self.assertEqual(contract['source_binding']['bootstrap_role'], 'IMMUTABLE_SEED_AND_PROVENANCE')
        self.assertEqual(contract['source_binding']['live_role_after_bootstrap'], 'BLENDER_NATIVE_EDITABLE_WORKING_SOURCE')
        self.assertTrue(contract['roundtrip']['overwrite_bootstrap_seed_forbidden'])
        self.assertEqual(contract['roundtrip']['controlled_native_edit']['only_family'], 'THUMB_SIDE_PLAN')
        self.assertEqual(binding['roundtrip_gate']['writeback_policy'], 'WRITE_NEW_ROUNDTRIP_SNAPSHOT; DO_NOT_OVERWRITE_BOOTSTRAP_SEED')


if __name__ == '__main__':
    unittest.main()
