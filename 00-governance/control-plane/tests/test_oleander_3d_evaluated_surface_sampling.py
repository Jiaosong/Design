from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_evaluated_surface_sampling.py'
s=importlib.util.spec_from_file_location('ess',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
C=json.loads((ROOT/'oleander-skills/oleander-3d-pipeline/contracts/EVALUATED_SURFACE_SAMPLING_CONTRACT_v1.json').read_text())
def r(): return {'schema':'oleander.3d.evaluated-surface-sampling-receipt.v1','source_id':'V49_SOURCE','source_state_class':'SOURCE_CONTROL_CAGE','source_control_count':20,'source_control_count_role':'INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE','source_mutated_for_sampling':False,'evaluated_carrier':'V49_FINAL_EVALUATED','evaluated_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY','evaluation_method':'CATMULL_CLARK_SUBD_EVALUATION','evaluated_sampling_gate':{'basis':'EVALUATED_EDGE_P95_AT_CURRENT_REVIEW_SCALE','threshold_or_rule':'edge_p95<=0.30m','observed':0.205,'status':'PASS','context':'bounded primary-form review'},'result':'PASS_EVALUATED_SAMPLING','does_not_prove':['surface fairness','reference fidelity','Design KEEP']}
class T(unittest.TestCase):
 def test_sparse_source_dense_eval_pass(self):self.assertTrue(m.validate(r(),C))
 def test_source_count_cannot_be_sampling_basis(self):
  d=r();d['evaluated_sampling_gate']['basis']='SOURCE_RING_CONTROL_COUNT'
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_unproven_source_mutation_cannot_sampling_pass(self):
  d=r();d['source_mutated_for_sampling']=True
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_proven_equivalent_source_edit_may_pass(self):
  d=r();d['source_mutated_for_sampling']=True;d['source_equivalence_proven_after_sampling_edit']=True
  self.assertTrue(m.validate(d,C))
 def test_hold_basis(self):
  d=r();d['evaluated_sampling_gate']['status']='HOLD';d['result']='HOLD_EVALUATED_SAMPLING_BASIS_UNRESOLVED'
  self.assertTrue(m.validate(d,C))
if __name__=='__main__':unittest.main()
