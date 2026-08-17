import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
VP=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_reference_fidelity.py'
spec=importlib.util.spec_from_file_location('refval',VP);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CONTRACT=json.loads((ROOT/'oleander-skills/oleander-3d-pipeline/contracts/REFERENCE_REPRODUCTION_FIDELITY_CONTRACT_v1.json').read_text())
def lm(x):
 return {'id':x,'target':1.0,'candidate':1.0,'normalization':4.0,'normalized_error':0.0,'class':'PRIMARY','reference_target_source':'external_reference_measurement','candidate_measurement_source':'candidate_projection'}
def valid():
 return {
  'reference_lock':{'reference_id':'P1','maker':'Porsche','product':'911','variant':'Carrera Coupe','generation':'992.2','model_year_or_revision':'2025','dimension_revision':'2025_992.2_CARRERA','visual_revision':'2025_992.2_CARRERA','dimension_sources':['official'],'visual_sources':['official','support'],'source_note':'reference study'},
  'views':[{'role':r} for r in ('side','front_or_front_3q','rear_or_rear_3q','plan_constraining','identity_detail')],
  'hard_points':[{'id':'LENGTH','authority':'OFFICIAL','target':4.542,'candidate':4.542}],
  'landmarks':[lm(x) for x in CONTRACT['required_landmarks']],
  'source_digest_before':'abc','source_digest_after':'abc','per_view_geometry_override':False,
  'silhouette_gate':'PASS','reference_fidelity_gate':'PASS','design_quality_gate':'HOLD','independent_reference_review':False}
class T(unittest.TestCase):
 def test_valid(self): mod.validate(valid(),CONTRACT)
 def test_mixed_revision_fails(self):
  d=valid();d['reference_lock']['visual_revision']='992.1'
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_missing_view_fails(self):
  d=valid();d['views']=d['views'][:-1]
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_landmark_error_fails(self):
  d=valid();d['landmarks'][0]['candidate']=1.3;d['landmarks'][0]['normalized_error']=.075
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_fake_declared_error_fails(self):
  d=valid();d['landmarks'][0]['candidate']=1.3;d['landmarks'][0]['normalized_error']=0.0
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_self_reference_fails(self):
  d=valid();d['landmarks'][0]['candidate_measurement_source']='external_reference_measurement'
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_missing_provenance_fails(self):
  d=valid();d['landmarks'][0].pop('reference_target_source')
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_source_drift_fails(self):
  d=valid();d['source_digest_after']='def'
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_owner_design_pass_fails(self):
  d=valid();d['design_quality_gate']='PASS'
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
if __name__=='__main__':unittest.main()
