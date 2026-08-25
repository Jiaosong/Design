from __future__ import annotations
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
P = ROOT / 'oleander-skills' / 'oleander-3d-pipeline' / 'tools' / 'validate_measurement_coverage_sufficiency.py'
C = ROOT / 'oleander-skills' / 'oleander-3d-pipeline' / 'contracts' / 'MEASUREMENT_COVERAGE_SUFFICIENCY_CONTRACT_v1.json'
spec = importlib.util.spec_from_file_location('measurement_coverage', P)
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
CONTRACT = json.loads(C.read_text(encoding='utf-8'))


def receipt():
    return {
        'schema':'oleander.3d.measurement-coverage-receipt.v1',
        'claim_id':'WHOLE_FORM_REFERENCE_SCREEN',
        'claim_scope':'WHOLE_VISIBLE_GROSS',
        'required_dimensions':['SIDE_XZ','FRONT_YZ','REAR_YZ'],
        'measured_dimensions':['SIDE_XZ','FRONT_YZ','REAR_YZ'],
        'required_feature_families':['GREENHOUSE','HOOD_FENDER','FRONT_PROFILE','REAR_PROFILE'],
        'measured_feature_families':['GREENHOUSE','HOOD_FENDER','FRONT_PROFILE','REAR_PROFILE'],
        'fit_views':['SIDE'],
        'held_out_views_required':['HERO_FRONT_3Q','HERO_REAR_3Q'],
        'held_out_views_reviewed':['HERO_FRONT_3Q','HERO_REAR_3Q'],
        'unmeasured_critical_items':[],
        'coverage_relation':'SUFFICIENT_FOR_DECLARED_CLAIM',
        'metric_results':[
            {'id':'SIDE_TOP','critical':True,'status':'PASS'},
            {'id':'FRONT_PROFILE','critical':True,'status':'PASS'},
            {'id':'REAR_PROFILE','critical':True,'status':'PASS'}
        ],
        'result':'PASS_COVERAGE_FOR_DECLARED_CLAIM',
        'does_not_prove':['reference fidelity','Design KEEP']
    }


class MeasurementCoverageTests(unittest.TestCase):
    def test_complete_claim_coverage_passes(self):
        self.assertTrue(mod.validate(receipt(), CONTRACT))

    def test_one_side_curve_cannot_prove_whole_form(self):
        d=receipt(); d['measured_dimensions']=['SIDE_XZ']; d['measured_feature_families']=['GREENHOUSE']; d['held_out_views_reviewed']=[]
        with self.assertRaises(SystemExit):
            mod.validate(d, CONTRACT)

    def test_missing_held_out_view_blocks_claim_pass(self):
        d=receipt(); d['held_out_views_reviewed']=['HERO_FRONT_3Q']
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('FAIL_CLAIM_PASS_MISSING_HELD_OUT_VIEWS', str(e.exception))

    def test_failed_critical_metric_cannot_be_averaged_away(self):
        d=receipt(); d['metric_results'][1]['status']='FAIL'
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('FAIL_CLAIM_PASS_WITH_FAILED_CRITICAL_METRIC', str(e.exception))

    def test_partial_diagnostic_is_valid_hold(self):
        d=receipt(); d['measured_dimensions']=['SIDE_XZ']; d['measured_feature_families']=['GREENHOUSE']; d['held_out_views_reviewed']=[]; d['coverage_relation']='PARTIAL_DIAGNOSTIC_ONLY'; d['result']='HOLD_PARTIAL_COVERAGE'; d['unmeasured_critical_items']=['FRONT_YZ','REAR_YZ','HELD_OUT_3Q']
        self.assertTrue(mod.validate(d, CONTRACT))

    def test_insufficient_relation_must_fail(self):
        d=receipt(); d['coverage_relation']='INSUFFICIENT_CRITICAL_DIMENSION_MISSING'; d['result']='HOLD_PARTIAL_COVERAGE'
        with self.assertRaises(SystemExit) as e:
            mod.validate(d, CONTRACT)
        self.assertIn('FAIL_INSUFFICIENT_RELATION_NOT_FAILED', str(e.exception))

    def test_screen_pass_keeps_narrow_scope(self):
        d=receipt(); d['claim_id']='SIDE_TOP_SCREEN'; d['claim_scope']='PRIMARY_FORM_OR_SHELL'; d['required_dimensions']=['SIDE_XZ']; d['measured_dimensions']=['SIDE_XZ']; d['required_feature_families']=['SIDE_TOP_ENVELOPE']; d['measured_feature_families']=['SIDE_TOP_ENVELOPE']; d['held_out_views_required']=[]; d['held_out_views_reviewed']=[]; d['coverage_relation']='SUFFICIENT_FOR_DECLARED_SCREEN'; d['result']='PASS_COVERAGE_FOR_DECLARED_SCREEN'; d['metric_results']=[{'id':'SIDE_TOP','critical':True,'status':'PASS'}]
        self.assertTrue(mod.validate(d, CONTRACT))


if __name__ == '__main__':
    unittest.main()
