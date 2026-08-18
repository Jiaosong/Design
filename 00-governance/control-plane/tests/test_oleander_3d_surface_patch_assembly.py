import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_surface_patch_assembly.py'
spec=importlib.util.spec_from_file_location('spa',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def valid():
 patches=[{'id':'BODY','role':'OPAQUE_PRIMARY','authority':'DERIVED_EXECUTION'},{'id':'ROOF','role':'OPAQUE_PATCH','authority':'DERIVED_EXECUTION'},{'id':'A','role':'OPAQUE_INTERFACE','authority':'DERIVED_EXECUTION'},{'id':'G1','role':'GLASS','authority':'DERIVED_INFILL'},{'id':'G2','role':'GLASS','authority':'DERIVED_INFILL'},{'id':'G3','role':'GLASS','authority':'DERIVED_INFILL'}]
 bp=[{'id':'ROOF_A','max_gap_m':.002},{'id':'A_GLASS','max_gap_m':.003},{'id':'ROOF_G','max_gap_m':.001},{'id':'BODY_A','max_gap_m':.004}]
 return {'schema':'oleander.3d.surface-patch-assembly-receipt.v1','candidate_revision':'V46','opaque_patch_count':3,'glass_patch_count':3,'patches':patches,'boundary_pairs':bp,'max_shared_boundary_gap_m':.004,'floating_visible_patch_count':0,'machine_assembly_state':'MACHINE_ASSEMBLED_VISUAL_HOLD','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity']}
class T(unittest.TestCase):
 def test_valid(self):self.assertEqual(mod.validate(valid())['machine_assembly_state'],'MACHINE_ASSEMBLED_VISUAL_HOLD')
 def test_gap_reject(self):
  d=valid();d['boundary_pairs'][0]['max_gap_m']=.02;d['max_shared_boundary_gap_m']=.02;d['machine_assembly_state']='MACHINE_ASSEMBLY_REJECT';self.assertEqual(mod.validate(d)['machine_assembly_state'],'MACHINE_ASSEMBLY_REJECT')
 def test_false_hold(self):
  d=valid();d['floating_visible_patch_count']=1
  with self.assertRaises(ValueError):mod.validate(d)
 def test_bad_recomputed_max(self):
  d=valid();d['max_shared_boundary_gap_m']=.009
  with self.assertRaises(ValueError):mod.validate(d)
 def test_plain_pass_forbidden(self):
  d=valid();d['machine_assembly_state']='PASS'
  with self.assertRaises(ValueError):mod.validate(d)
if __name__=='__main__':unittest.main()