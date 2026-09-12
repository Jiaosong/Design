import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_primary_form_identity.py'
spec=importlib.util.spec_from_file_location('pfi',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def valid():
 return {'schema':'oleander.3d.primary-form-identity-receipt.v1','candidate_revision':'V35','reference_revision':'992.2','gesture_metric':{'candidate':.02,'limit':.035},'front_profile_metric':{'candidate':.08,'limit':.10},'rear_profile_metric':{'candidate':.10,'limit':.11},'identity_relations':[{'id':'FASTBACK_GESTURE','state':'SCREENED'},{'id':'HOOD_FENDER_HIERARCHY','state':'SCREENED'}],'finite_measurement_coverage':.95,'pre_aperture_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','regression_decision':'KEEP_LKG_HOLD_EXPERIMENT','visual_review_state':'NOT_RUN','machine_identity_state':'MACHINE_SCREENED_VISUAL_HOLD','does_not_prove':['reference fidelity','Class-A continuity']}
class T(unittest.TestCase):
 def test_valid(self): self.assertEqual(mod.validate(valid())['machine_identity_state'],'MACHINE_SCREENED_VISUAL_HOLD')
 def test_low_coverage(self):
  d=valid();d['finite_measurement_coverage']=.89
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_pass_forbidden(self):
  d=valid();d['machine_identity_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_false_screen(self):
  d=valid();d['rear_profile_metric']['candidate']=.20
  with self.assertRaises(ValueError):mod.validate(d)
 def test_surface_failure_cannot_screen(self):
  d=valid();d['pre_aperture_surface_state']='MACHINE_SURFACE_TOPOLOGY_FAIL'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_relations_required(self):
  d=valid();d['identity_relations']=[]
  with self.assertRaises(ValueError):mod.validate(d)
 def test_semantic_relation_hold_cannot_screen(self):
  d=valid();d['identity_relations'][1]['state']='HOLD'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_semantic_relation_fail_cannot_screen(self):
  d=valid();d['identity_relations'][1]['state']='FAIL'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_machine_reject_may_preserve_relation_hold(self):
  d=valid();d['machine_identity_state']='MACHINE_REJECT';d['identity_relations'][1]['state']='HOLD'
  self.assertEqual(mod.validate(d)['machine_identity_state'],'MACHINE_REJECT')
if __name__=='__main__':unittest.main()
