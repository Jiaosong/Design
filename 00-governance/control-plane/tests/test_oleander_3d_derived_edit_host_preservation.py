from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / 'oleander-skills' / 'oleander-3d-pipeline' / 'tools' / 'validate_derived_edit_host_preservation.py'
CONTRACT_PATH = ROOT / 'oleander-skills' / 'oleander-3d-pipeline' / 'contracts' / 'DERIVED_EDIT_HOST_PRESERVATION_CONTRACT_v1.json'
spec = importlib.util.spec_from_file_location('host_preservation_validator', VALIDATOR)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
CONTRACT = json.loads(CONTRACT_PATH.read_text(encoding='utf-8'))


def receipt():
    return {
        'schema': 'oleander.3d.derived-edit-host-preservation-receipt.v1',
        'host_id': 'DERIVED_BODY',
        'host_state_class': 'DERIVED_EXECUTION',
        'operation': 'BOOLEAN_DIFFERENCE',
        'edit_scope': 'LOCAL_APERTURE',
        'locality': 'LOCAL',
        'source_mutation_allowed': False,
        'source_unchanged_or_na': True,
        'before': {'vertices': 8762, 'faces': 8760, 'bounds': [4.54, 1.85, 1.30]},
        'after': {'vertices': 9100, 'faces': 8400, 'bounds': [4.54, 1.85, 1.30]},
        'preservation_checks': [
            {'id':'FACE_RETENTION','metric':'faces_ratio','before':8760,'after':8400,'rule':'>=0.70','status':'PASS','scope':'GLOBAL_HOST'},
            {'id':'BOUNDS_RETENTION','metric':'bounds_ratio_min','before':1.0,'after':0.998,'rule':'>=0.95','status':'PASS','scope':'GLOBAL_HOST'}
        ],
        'operator_execution': 'PASS_EXECUTED',
        'host_preservation_result': 'PASS_WITHIN_DECLARED_BUDGET',
        'evidence_result': 'PASS_EVIDENCE_SCOPE',
        'design_result': 'HOLD_NOT_REVIEWED',
        'does_not_prove': ['Design KEEP']
    }


class HostPreservationTests(unittest.TestCase):
    def test_valid_local_edit(self):
        self.assertTrue(mod.validate(receipt(), CONTRACT))

    def test_local_edit_requires_global_host_check(self):
        d=receipt(); d['preservation_checks'][0]['scope']='LOCAL_REGION'; d['preservation_checks'][1]['scope']='LOCAL_REGION'
        with self.assertRaises(SystemExit) as e: mod.validate(d, CONTRACT)
        self.assertIn('FAIL_LOCAL_EDIT_WITHOUT_GLOBAL_HOST_CHECK', str(e.exception))

    def test_catastrophic_face_loss_cannot_pass(self):
        d=receipt(); d['after']['faces']=96; d['preservation_checks'][0]['after']=96; d['preservation_checks'][0]['status']='FAIL'
        with self.assertRaises(SystemExit) as e: mod.validate(d, CONTRACT)
        self.assertIn('FAIL_HOST_PASS_WITH_FAILED_OR_HELD_CHECK', str(e.exception))

    def test_geometry_changed_only_cannot_pass(self):
        d=receipt(); d['geometry_changed_only_basis']=True
        with self.assertRaises(SystemExit) as e: mod.validate(d, CONTRACT)
        self.assertIn('FAIL_GEOMETRY_CHANGED_ONLY_FALSE_POSITIVE', str(e.exception))

    def test_source_protection_requires_unchanged_witness(self):
        d=receipt(); d['source_unchanged_or_na']=False
        with self.assertRaises(SystemExit) as e: mod.validate(d, CONTRACT)
        self.assertIn('FAIL_PROTECTED_SOURCE_NOT_PROVEN_UNCHANGED', str(e.exception))

    def test_negative_host_result_is_valid_evidence_state(self):
        d=receipt(); d['after']['faces']=96; d['preservation_checks'][0]['after']=96; d['preservation_checks'][0]['status']='FAIL'; d['host_preservation_result']='FAIL_HOST_PRESERVATION'; d['evidence_result']='PASS_EVIDENCE_SCOPE'; d['design_result']='REJECT'
        self.assertTrue(mod.validate(d, CONTRACT))

    def test_machine_gate_cannot_self_promote_design(self):
        d=receipt(); d['design_result']='PASS_INDEPENDENT_DESIGN_REVIEW'
        with self.assertRaises(SystemExit) as e: mod.validate(d, CONTRACT)
        self.assertIn('FAIL_MACHINE_HOST_GATE_SELF_PROMOTED_TO_DESIGN_PASS', str(e.exception))

    def test_independent_design_receipt_keeps_gate_separate(self):
        d=receipt(); d['design_result']='PASS_INDEPENDENT_DESIGN_REVIEW'; d['independent_design_review_receipt']='AR-3D-001'
        self.assertTrue(mod.validate(d, CONTRACT))


if __name__ == '__main__':
    unittest.main()
