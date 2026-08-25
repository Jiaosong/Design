from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
P=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_blender_runtime.py'
s=importlib.util.spec_from_file_location('br',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
C=json.loads((ROOT/'oleander-skills/oleander-3d-pipeline/contracts/BLENDER_RUNTIME_CONTRACT_v1.json').read_text())

def receipt():
 return {
  'schema':'oleander.3d.blender-runtime-receipt.v1',
  'task_id':'TRAIN-BLENDER-5.2-001',
  'claim':'controlled product CMF comparison render',
  'source_state_class':'VISUALIZATION_OR_RENDER_SCENE',
  'runtime':{'application':'Blender','version':'5.2.0 LTS','build_hash_or_status':'UNKNOWN_NOT_CAPTURED','platform':'linux-x64','device_backend':'CPU','runtime_support_state':'VERIFIED_AVAILABLE'},
  'units_axes':{'unit_system':'METRIC','scale_length':1.0,'up_axis':'Z'},
  'dependencies':{'all_required_dependencies_recoverable':True,'network_only_required_dependency':False,'remote_asset_library_used':False,'materialized_remote_asset_ids':[],'external_dependency_manifest':['textures/','scene.blend']},
  'procedural':{'geometry_nodes_used':False,'simulation_used':False,'deterministic_seed_or_na':'NA','simulation_cache_or_state_or_na':'NA','evaluated_carrier_readback':True,'physical_truth_claim':False},
  'color_management':{'working_space':'scene-linear','display_device':'sRGB','view_transform':'AgX','look':'Medium High Contrast','exposure':0.0,'output_color_space':'Linear Rec.709 EXR','hdr_or_sdr':'SDR','ocio_config_identity':'Blender default 5.2'},
  'render':{'engine':'CYCLES','device_backend':'CPU','samples_or_realtime_policy':'64 samples adaptive','denoise_or_postprocess_policy':'denoise OFF for diagnostic','comparison_lock_id_or_na':'RIG-CMF-001'},
  'io':{'requested_formats':['EXR'],'verified_operators_or_bridges':['EXR'],'representative_roundtrip_required':False,'roundtrip_status':'HOLD_NOT_REQUIRED'},
  'output':{'retained_files':['scene.blend','cmf.exr'],'readback_status':'PASS'},
  'machine_verdict':'PASS','evidence_verdict':'PASS_BOUNDED_RENDER_EVIDENCE','design_review_status':'PENDING',
  'does_not_prove':['field truth','engineering approval','physical material properties','manufacturing readiness','Design KEEP']
 }

class T(unittest.TestCase):
 def test_valid_runtime_receipt(self): self.assertTrue(m.validate(receipt(),C))
 def test_network_only_dependency_fails(self):
  d=receipt();d['dependencies']['network_only_required_dependency']=True
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_remote_asset_must_be_materialized(self):
  d=receipt();d['dependencies']['remote_asset_library_used']=True
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_simulation_cannot_claim_physical_truth(self):
  d=receipt();d['procedural']['simulation_used']=True;d['procedural']['simulation_cache_or_state_or_na']='CACHE-001';d['procedural']['physical_truth_claim']=True
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_requested_io_route_must_be_verified(self):
  d=receipt();d['io']['requested_formats']=['STEP'];d['io']['verified_operators_or_bridges']=[]
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_unknown_runtime_cannot_machine_pass(self):
  d=receipt();d['runtime']['runtime_support_state']='UNKNOWN'
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_color_pipeline_is_required(self):
  d=receipt();d['color_management']['view_transform']=''
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_output_requires_readback(self):
  d=receipt();d['output']['readback_status']='HOLD'
  with self.assertRaises(SystemExit):m.validate(d,C)

if __name__=='__main__':unittest.main()
