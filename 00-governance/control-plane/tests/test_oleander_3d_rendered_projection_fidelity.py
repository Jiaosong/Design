import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];VP=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_rendered_projection_fidelity.py'
spec=importlib.util.spec_from_file_location('pv',VP);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
C=json.loads((ROOT/'oleander-skills/oleander-3d-pipeline/contracts/RENDERED_PROJECTION_FIDELITY_CONTRACT_v1.json').read_text())
def metric():return {'id':'ROOF','target':.59,'candidate':.60,'abs_error':.01,'limit':.05,'reference_target_source':'EXTERNAL_REFERENCE','candidate_measurement_source':'FINAL_VISIBLE_UNION_PROJECTION'}
def valid():return {'reference':'R','candidate_revision':'V','status':'PROJECTION_MACHINE_SCREENING_PASS','metrics':[metric()],'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':['CAD']}
class T(unittest.TestCase):
 def test_valid(self):self.assertTrue(mod.validate(valid(),C))
 def test_self_reference_fails(self):
  d=valid();d['metrics'][0]['candidate_measurement_source']='EXTERNAL_REFERENCE'
  with self.assertRaises(SystemExit):mod.validate(d,C)
 def test_intermediate_shell_fails(self):
  d=valid();d['metrics'][0]['candidate_measurement_source']='V12_BASE_SHELL_RING'
  with self.assertRaises(SystemExit):mod.validate(d,C)
 def test_fake_error_fails(self):
  d=valid();d['metrics'][0]['candidate']=.70;d['metrics'][0]['abs_error']=0
  with self.assertRaises(SystemExit):mod.validate(d,C)
 def test_declared_pass_over_limit_fails(self):
  d=valid();d['metrics'][0]['candidate']=.70;d['metrics'][0]['abs_error']=.11
  with self.assertRaises(SystemExit):mod.validate(d,C)
 def test_self_promotion_fails(self):
  d=valid();d['reference_fidelity_review']='KEEP'
  with self.assertRaises(SystemExit):mod.validate(d,C)
if __name__=='__main__':unittest.main()
