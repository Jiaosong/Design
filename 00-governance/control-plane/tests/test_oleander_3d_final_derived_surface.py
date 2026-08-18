import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_final_derived_surface.py'
spec=importlib.util.spec_from_file_location('fds',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def valid():return {'schema':'oleander.3d.final-derived-surface-receipt.v1','candidate_revision':'V43','source_surface_revision':'V40','derived_surface_method':'SUBD1_THEN_BOOLEAN','subdivision_level':1,'final_connected_components':1,'final_nonmanifold_edge_count':0,'aperture_region_edge_p95_m':.08,'aperture_region_edge_max_m':.18,'aperture_region_sliver_face_count':0,'aperture_region_min_face_area_m2':1e-4,'machine_finish_state':'MACHINE_SURFACED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity']}
class T(unittest.TestCase):
 def test_valid(self):self.assertEqual(mod.validate(valid())['machine_finish_state'],'MACHINE_SURFACED_VISUAL_HOLD')
 def test_valid_reject(self):
  d=valid();d['aperture_region_edge_max_m']=.4;d['machine_finish_state']='MACHINE_SURFACE_FINISH_REJECT';self.assertEqual(mod.validate(d)['machine_finish_state'],'MACHINE_SURFACE_FINISH_REJECT')
 def test_false_hold(self):
  d=valid();d['final_nonmanifold_edge_count']=2
  with self.assertRaises(ValueError):mod.validate(d)
 def test_false_reject(self):
  d=valid();d['machine_finish_state']='MACHINE_SURFACE_FINISH_REJECT'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_pass_forbidden(self):
  d=valid();d['machine_finish_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
if __name__=='__main__':unittest.main()