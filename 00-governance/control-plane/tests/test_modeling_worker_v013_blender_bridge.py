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
        self.assertEqual(contract['benchmark_id'], 'MW-V013-G1-ERGONOMIC-HANDHELD-SHELL')
        self.assertEqual(contract['runtime']['blender'], '5.2.0 LTS')
        self.assertEqual(contract['runtime']['engine'], 'CYCLES')
        self.assertEqual(contract['design_state'], 'EXPLORE')
        self.assertEqual(contract['authority_state'], 'WORKING_SOURCE')
        self.assertEqual(contract['candidate_promotion'], 'NOT_RUN')
        self.assertFalse(contract['debug_contract']['derived_mesh_is_not_source_authority'] is False)
        self.assertEqual(contract['debug_contract']['round_trip_writeback_to_json'], 'NOT_IMPLEMENTED_IN_THIS_GATE')
        self.assertEqual(len(contract['native_source_objects']), 6)
        self.assertEqual(len(contract['required_diagnostics']), 8)
        py_compile.compile(str(V013 / 'g1_r2_blender_scene.py'), doraise=True)
        py_compile.compile(str(V013 / 'g1_r2_blender_entry.py'), doraise=True)

    def test_blender_bridge_binds_existing_r2_authority(self):
        source = json.loads((V013 / 'G1_PRIMARY_CURVE_SOURCE.json').read_text(encoding='utf-8'))
        fix = json.loads((V013 / 'G1_R2_RELATION_CORRECTION.json').read_text(encoding='utf-8'))
        contract = json.loads((V013 / 'G1_R2_BLENDER_EXECUTION_CONTRACT.json').read_text(encoding='utf-8'))
        self.assertEqual(source['authority'], 'WORKING_SURFACE_SOURCE')
        self.assertFalse(source['derived_execution']['editable_authority'])
        self.assertFalse(fix['mesh_local_patch_allowed'])
        self.assertEqual(contract['source_binding']['primary_curve_source'], 'G1_PRIMARY_CURVE_SOURCE.json')
        self.assertEqual(contract['source_binding']['r2_relation_correction'], 'G1_R2_RELATION_CORRECTION.json')


if __name__ == '__main__':
    unittest.main()
