import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_final_derived_surface.py'
spec=importlib.util.spec_from_file_location('fds',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def closed():return {'schema':'oleander.3d.final-derived-surface-receipt.v2','candidate_revision':'V45','source_surface_revision':'V40','derived_surface_method':'SUBD1_BOOLEAN','subdivision_level':1,'topology_mode':'CLOSED_SOLID_BOOLEAN','final_connected_components':1,'expected_aperture_boundary_edge_count':0,'aperture_boundary_loop_count':0,'unexpected_nonmanifold_edge_count':0,'aperture_region_edge_p95_m':.08,'aperture_region_edge_max_m':.58,'aperture_region_sliver_face_count':0,'aperture_region_min_face_area_m2':1e-4,'machine_finish_state':'MACHINE_SURFACED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity']}
def open_shell():
 d=closed();d.update({'topology_mode':'OPEN_SURFACE_APERTURE_SHELL','expected_aperture_boundary_edge_count':24,'aperture_boundary_loop_count':1,'derived_surface_method':'SUBD1_DECLARED_OPENING'});return d
class T(unittest.TestCase):
 def test_valid_closed_long_straight_edge_allowed(self):self.assertEqual(mod.validate(closed())['machine_finish_state'],'MACHINE_SURFACED_VISUAL_HOLD')
 def test_valid_open_shell_single_declared_loop(self):self.assertEqual(mod.validate(open_shell())['topology_mode'],'OPEN_SURFACE_APERTURE_SHELL')
 def test_unexpected_nonmanifold_reject(self):
  d=open_shell();d['unexpected_nonmanifold_edge_count']=2;d['machine_finish_state']='MACHINE_SURFACE_FINISH_REJECT';self.assertEqual(mod.validate(d)['machine_finish_state'],'MACHINE_SURFACE_FINISH_REJECT')
 def test_open_shell_without_loops_fails_hold(self):
  d=open_shell();d['aperture_boundary_loop_count']=0
  with self.assertRaises(ValueError):mod.validate(d)
 def test_closed_with_expected_boundaries_fails(self):
  d=closed();d['expected_aperture_boundary_edge_count']=2
  with self.assertRaises(ValueError):mod.validate(d)
 def test_false_reject(self):
  d=open_shell();d['machine_finish_state']='MACHINE_SURFACE_FINISH_REJECT'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_pass_forbidden(self):
  d=open_shell();d['machine_finish_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
if __name__=='__main__':unittest.main()