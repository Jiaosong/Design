import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_primary_body_surface.py'
spec=importlib.util.spec_from_file_location('pb',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def valid():
 return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':'V31','surface_measurement_scope':'PRE_APERTURE_PRIMARY_SKIN','body_cap_edges_excluded':True,'body_connected_components':1,'cabin_connected_components':1,'body_adjacent_face_normal_flip_count':0,'cabin_adjacent_face_normal_flip_count':0,'body_local_edge_p95_m':.18,'body_longitudinal_stations':91,'body_ring_vertices':30,'machine_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity']}
class T(unittest.TestCase):
 def test_valid(self):self.assertEqual(mod.validate(valid())['surface_measurement_scope'],'PRE_APERTURE_PRIMARY_SKIN')
 def test_wrong_scope(self):
  d=valid();d['surface_measurement_scope']='POST_BOOLEAN_BODY'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_cap_edges_not_excluded(self):
  d=valid();d['body_cap_edges_excluded']=False
  with self.assertRaises(ValueError):mod.validate(d)
 def test_body_disconnect(self):
  d=valid();d['body_connected_components']=2
  with self.assertRaises(ValueError):mod.validate(d)
 def test_cabin_disconnect(self):
  d=valid();d['cabin_connected_components']=2
  with self.assertRaises(ValueError):mod.validate(d)
 def test_fold(self):
  d=valid();d['body_adjacent_face_normal_flip_count']=1
  with self.assertRaises(ValueError):mod.validate(d)
 def test_stretch(self):
  d=valid();d['body_local_edge_p95_m']=.8
  with self.assertRaises(ValueError):mod.validate(d)
 def test_sparse_longitudinal(self):
  d=valid();d['body_longitudinal_stations']=40
  with self.assertRaises(ValueError):mod.validate(d)
 def test_sparse_ring(self):
  d=valid();d['body_ring_vertices']=20
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_pass_forbidden(self):
  d=valid();d['machine_surface_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
if __name__=='__main__':unittest.main()
