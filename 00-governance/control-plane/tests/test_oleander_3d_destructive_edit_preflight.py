from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'tools'/'validate_destructive_edit_preflight.py'
C=ROOT/'oleander-skills'/'oleander-3d-pipeline'/'contracts'/'DESTRUCTIVE_EDIT_PREFLIGHT_CONTRACT_v1.json'
s=importlib.util.spec_from_file_location('preflight',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
CONTRACT=json.loads(C.read_text(encoding='utf-8'))


def r():
    return {
      'schema':'oleander.3d.destructive-edit-preflight-receipt.v1',
      'host_id':'DERIVED_BODY','host_state_class':'DERIVED_EXECUTION','operation':'FACE_DELETE',
      'edit_scope':'APERTURE_ONLY','source_mutation_allowed':False,'source_mutation_planned':False,
      'classifier_identity':'APERTURE_OWNER_CLASSIFIER_V1',
      'classifier_dependencies':['REFERENCE_GREENHOUSE_TABLE','EVALUATED_FACE_XZ_Y'],
      'required_owner_ids':['SIDE_L','SIDE_R','REAR'],
      'owner_coverage':{
        'SIDE_L':{'state':'COVERED_EXCLUSIVE','count':120},
        'SIDE_R':{'state':'COVERED_EXCLUSIVE','count':120},
        'REAR':{'state':'COVERED_EXCLUSIVE','count':32}
      },
      'multi_owner_conflicts':{'count':0,'unresolved_count':0,'resolution_method':'NONE_REQUIRED'},
      'predicted_preservation_checks':[{'id':'FACE_RETENTION','hard':True,'status':'PASS','observed':.94}],
      'preflight_result':'PASS_DESTRUCTIVE_EDIT_ALLOWED','destructive_edit_allowed':True,
      'does_not_prove':['host preservation after execution','Design KEEP']
    }


class DestructivePreflightTests(unittest.TestCase):
    def test_valid_exclusive_preflight(self): self.assertTrue(m.validate(r(),CONTRACT))
    def test_missing_required_owner_blocks_pass(self):
        d=r();d['owner_coverage']['REAR']={'state':'MISSING_TARGET_COVERAGE','count':0}
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_PASS_WITH_UNCOVERED_OWNER',str(e.exception))
    def test_multi_owner_conflict_blocks_pass(self):
        d=r();d['multi_owner_conflicts']={'count':6,'unresolved_count':6,'resolution_method':'UNRESOLVED'}
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_PASS_WITH_UNRESOLVED_MULTI_OWNER_CONFLICT',str(e.exception))
    def test_first_match_code_order_forbidden(self):
        d=r();d['multi_owner_conflicts']={'count':6,'unresolved_count':0,'resolution_method':'FIRST_MATCH_CODE_ORDER'}
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_FIRST_MATCH_CODE_ORDER_AS_OWNERSHIP',str(e.exception))
    def test_explicit_shared_boundary_may_pass(self):
        d=r();d['owner_coverage']['REAR']={'state':'COVERED_SHARED_BOUNDARY_EXPLICIT','count':32};d['multi_owner_conflicts']={'count':6,'unresolved_count':0,'resolution_method':'CANONICAL_SHARED_BOUNDARY_PARTITION'}
        self.assertTrue(m.validate(d,CONTRACT))
    def test_predicted_host_loss_blocks_pass(self):
        d=r();d['predicted_preservation_checks'][0]['status']='FAIL'
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_PASS_WITH_PREDICTED_HOST_LOSS',str(e.exception))
    def test_blocked_preflight_cannot_allow_edit(self):
        d=r();d['preflight_result']='FAIL_DESTRUCTIVE_EDIT_BLOCKED_AMBIGUOUS_OWNER';d['destructive_edit_allowed']=True
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_BLOCKED_PREFLIGHT_ALLOWS_EDIT',str(e.exception))
    def test_historical_nested_namespace_dependency_forbidden(self):
        d=r();d['classifier_dependencies']=['HISTORICAL_NESTED_NAMESPACE:ctx.ns.interpG']
        with self.assertRaises(SystemExit) as e:m.validate(d,CONTRACT)
        self.assertIn('FAIL_HISTORICAL_NESTED_NAMESPACE_DEPENDENCY',str(e.exception))


if __name__=='__main__':unittest.main()
