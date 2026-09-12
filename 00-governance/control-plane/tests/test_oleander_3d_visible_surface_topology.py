import importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_visible_surface_topology.py'
spec=importlib.util.spec_from_file_location('topoval',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def valid():
 return {
  'schema':'oleander.3d.visible-surface-topology-receipt.v1','revision':'V29',
  'opaque_cabin_object':'DERIVED_911_9922_CABIN','opaque_cabin_exists':True,
  'opaque_cabin_architecture':'PROFILE_INVERTED_CONNECTED_CABIN_V29',
  'opaque_cabin_connected_components':1,'shared_vertex_boundary_count':8,
  'aperture_boundary_gap_max_m':0.0004,'adjacent_face_normal_flip_count':0,'open_patch_rim_walls':False,
  'forbidden_floating_interface_objects':[],'forbidden_floating_interface_count':0,
  'real_glazing_objects':['REF_WINDSHIELD','REF_DOOR_GLASS_L','REF_DOOR_GLASS_R','REF_QUARTER_GLASS_L','REF_QUARTER_GLASS_R','REF_REAR_GLASS'],
  'no_opaque_surface_behind_glazing_declared':True,
  'machine_topology_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN',
  'does_not_prove':['Class-A continuity','reference fidelity']}

class T(unittest.TestCase):
 def test_valid(self):self.assertEqual(mod.validate(valid())['opaque_cabin_connected_components'],1)
 def test_disconnected_islands_fail(self):
  d=valid();d['opaque_cabin_connected_components']=4
  with self.assertRaises(ValueError):mod.validate(d)
 def test_shared_vertex_count_fails(self):
  d=valid();d['shared_vertex_boundary_count']=2
  with self.assertRaises(ValueError):mod.validate(d)
 def test_boundary_gap_fails(self):
  d=valid();d['aperture_boundary_gap_max_m']=.006
  with self.assertRaises(ValueError):mod.validate(d)
 def test_normal_flip_fails(self):
  d=valid();d['adjacent_face_normal_flip_count']=3
  with self.assertRaises(ValueError):mod.validate(d)
 def test_open_patch_rim_wall_fails(self):
  d=valid();d['open_patch_rim_walls']=True
  with self.assertRaises(ValueError):mod.validate(d)
 def test_floating_patch_fails(self):
  d=valid();d['forbidden_floating_interface_objects']=['REF_C_PILLAR_SAIL_L'];d['forbidden_floating_interface_count']=1
  with self.assertRaises(ValueError):mod.validate(d)
 def test_missing_glass_fails(self):
  d=valid();d['real_glazing_objects'].remove('REF_REAR_GLASS')
  with self.assertRaises(ValueError):mod.validate(d)
 def test_opaque_behind_glass_unresolved_fails(self):
  d=valid();d['no_opaque_surface_behind_glazing_declared']=False
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_machine_pass_semantic_fails(self):
  d=valid();d['machine_topology_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_count_mismatch_fails(self):
  d=valid();d['forbidden_floating_interface_count']=1
  with self.assertRaises(ValueError):mod.validate(d)

if __name__=='__main__':unittest.main()
