from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'tools'/'validate_coordinate_frame_congruence.py'
C=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'contracts'/'COORDINATE_FRAME_CONGRUENCE_CONTRACT_v1.json'
s=importlib.util.spec_from_file_location('frame',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
CONTRACT=json.loads(C.read_text(encoding='utf-8'))

def r():
    return {
      'schema':'oleander.3d.coordinate-frame-congruence-receipt.v1','operation_id':'V76_EDGE2_BISECT','geometry_id':'V72_REOPENED_BODY','geometry_state_class':'DERIVED_EXECUTION',
      'canonical_target_frame':'WORLD_METRES','predicate_frame':'WORLD_METRES','operator_frame':'WORLD_METRES','transforms':[],
      'metric_or_tolerance_frame':'WORLD_METRES','audit_target_count':2,'operator_selected_count':2,'selection_equivalence_required':True,
      'frame_checks':{'quantity_semantics_bound':True,'canonical_target_bound':True,'transform_verified':True},
      'frame_result':'PASS_FRAME_CONGRUENCE','downstream_evidence_state':'VALID_FOR_DECLARED_SCOPE','does_not_prove':['operator success','Design KEEP']
    }

class CoordinateFrameTests(unittest.TestCase):
    def test_same_frame_equal_selection_passes(self):self.assertTrue(m.validate(r(),CONTRACT))
    def test_world_audit_local_operator_without_transform_cannot_pass(self):
        d=r();d['operator_frame']='OBJECT_LOCAL';d['operator_selected_count']=0
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_FRAME_PASS_WITHOUT_VERIFIED_TRANSFORM',str(e.exception))
    def test_mismatch_is_valid_quarantined_failure(self):
        d=r();d['operator_frame']='OBJECT_LOCAL';d['operator_selected_count']=0;d['frame_result']='FAIL_FRAME_MISMATCH';d['downstream_evidence_state']='NON_PROMOTABLE_DIAGNOSTIC_PROVENANCE';d['frame_checks']['transform_verified']=False
        self.assertTrue(m.validate(d,CONTRACT))
    def test_diagnostic_copy_normalized_frame_passes_with_transform(self):
        d=r();d['predicate_frame']='WORLD_METRES';d['operator_frame']='WORLD_BAKED_DIAGNOSTIC_COPY';d['transforms']=[{'from':'OBJECT_LOCAL','to':'WORLD_BAKED_DIAGNOSTIC_COPY','method':'BAKE_MATRIX_WORLD_INTO_COPY_GEOMETRY','verified':True,'quantity_semantics':['POINT','DIRECTION','PLANE']}];d['frame_result']='PASS_DIAGNOSTIC_COPY_NORMALIZED_FRAME'
        self.assertTrue(m.validate(d,CONTRACT))
    def test_pass_rejects_selection_count_mismatch(self):
        d=r();d['operator_selected_count']=0
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_FRAME_PASS_SELECTION_COUNT_MISMATCH',str(e.exception))
    def test_frame_fail_must_quarantine_downstream(self):
        d=r();d['frame_result']='FAIL_FRAME_MISMATCH';d['downstream_evidence_state']='VALID_FOR_DECLARED_SCOPE';d['operator_selected_count']=0
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_FRAME_MISMATCH_NOT_QUARANTINED',str(e.exception))
    def test_hold_transform_unverified(self):
        d=r();d['predicate_frame']='WORLD_METRES';d['operator_frame']='OBJECT_LOCAL';d['transforms']=[{'from':'OBJECT_LOCAL','to':'WORLD_METRES','verified':False}];d['frame_result']='HOLD_TRANSFORM_UNVERIFIED';d['downstream_evidence_state']='HOLD_NOT_COMPARABLE';d['operator_selected_count']=0
        self.assertTrue(m.validate(d,CONTRACT))
    def test_tolerance_frame_required(self):
        d=r();d['metric_or_tolerance_frame']=''
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_TOLERANCE_FRAME_MISSING',str(e.exception))

if __name__=='__main__':unittest.main()
