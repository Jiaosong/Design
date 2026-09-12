import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_primary_body_surface.py'
spec=importlib.util.spec_from_file_location('pb',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def legacy_v1():
 return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':'V35','surface_measurement_scope':'PRE_APERTURE_PRIMARY_SKIN','body_cap_edges_excluded':True,'body_connected_components':1,'cabin_connected_components':1,'body_adjacent_face_normal_flip_count':0,'cabin_adjacent_face_normal_flip_count':0,'body_local_edge_p95_m':.18,'body_longitudinal_stations':91,'body_ring_vertices':30,'machine_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity']}

def v2():
 return {
  'schema':'oleander.3d.primary-body-surface-receipt.v2','revision':'V57','surface_measurement_scope':'CLOSED_PRIMARY_VISUAL_HULL_BEFORE_FINAL_APERTURE_ARCHITECTURE',
  'source_state_class':'SOURCE_CONTROL_CAGE','source_semantic_rail_count':9,'source_ring_control_count':20,
  'source_density_role':'INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE',
  'evaluated_carrier':'DIAG_FEATURE_ALIGNED_SURFACED_V49','evaluated_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY',
  'evaluated_vertices':4382,'evaluated_edges':13140,'evaluated_faces':8760,'evaluated_triangles':17520,
  'evaluated_connected_components':1,'evaluated_adjacent_face_normal_flip_count':0,'evaluated_edge_p95_m':.2052,
  'evaluated_sampling_gate':{'basis':'EVALUATED_EDGE_P95_AT_CURRENT_REVIEW_SCALE','status':'PASS','threshold_or_rule':'edge_p95_m <= 0.30','observed':.2052},
  'machine_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity']}

class T(unittest.TestCase):
 def test_legacy_v1_still_valid(self):self.assertEqual(mod.validate(legacy_v1())['machine_surface_state'],'MACHINE_CONSTRUCTED_VISUAL_HOLD')
 def test_v2_sparse_source_dense_evaluated_can_pass(self):
  d=v2();self.assertEqual(d['source_ring_control_count'],20);self.assertEqual(mod.validate(d)['machine_surface_state'],'MACHINE_CONSTRUCTED_VISUAL_HOLD')
 def test_v2_source_ring_count_not_quality_gate(self):
  d=v2();d['source_ring_control_count']=8
  self.assertEqual(mod.validate(d)['machine_surface_state'],'MACHINE_CONSTRUCTED_VISUAL_HOLD')
 def test_v2_rejects_source_ring_as_sampling_basis(self):
  d=v2();d['evaluated_sampling_gate']['basis']='SOURCE_RING_CONTROL_COUNT'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_v2_fold_blocks_constructed(self):
  d=v2();d['evaluated_adjacent_face_normal_flip_count']=1
  with self.assertRaises(ValueError):mod.validate(d)
 def test_v2_topology_failure_legal(self):
  d=v2();d['evaluated_adjacent_face_normal_flip_count']=1;d['machine_surface_state']='MACHINE_SURFACE_TOPOLOGY_FAIL'
  self.assertEqual(mod.validate(d)['machine_surface_state'],'MACHINE_SURFACE_TOPOLOGY_FAIL')
 def test_v2_sampling_hold_legal(self):
  d=v2();d['evaluated_sampling_gate']['status']='HOLD';d['machine_surface_state']='MACHINE_SURFACE_SAMPLING_HOLD'
  self.assertEqual(mod.validate(d)['machine_surface_state'],'MACHINE_SURFACE_SAMPLING_HOLD')
 def test_v2_false_sampling_hold_when_pass(self):
  d=v2();d['machine_surface_state']='MACHINE_SURFACE_SAMPLING_HOLD'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_v2_false_topology_fail_when_clean(self):
  d=v2();d['machine_surface_state']='MACHINE_SURFACE_TOPOLOGY_FAIL'
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_pass_forbidden(self):
  d=v2();d['machine_surface_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
if __name__=='__main__':unittest.main()
