import importlib.util,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_surface_fold_diagnostic.py'
spec=importlib.util.spec_from_file_location('sfd',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
def valid():return {'schema':'oleander.3d.surface-fold-diagnostic.v1','candidate_revision':'V40','fold_count':1,'folds':[{'edge_vertices':[1,2],'face_indices':[3,4],'normal_dot':-.3,'center_m':[-1.2,.7,.9]}],'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY'}
class T(unittest.TestCase):
 def test_valid(self):self.assertEqual(mod.validate(valid())['fold_count'],1)
 def test_count_mismatch(self):
  d=valid();d['fold_count']=0
  with self.assertRaises(ValueError):mod.validate(d)
 def test_missing_center(self):
  d=valid();del d['folds'][0]['center_m']
  with self.assertRaises(ValueError):mod.validate(d)
 def test_nonfold_dot(self):
  d=valid();d['folds'][0]['normal_dot']=.2
  with self.assertRaises(ValueError):mod.validate(d)
 def test_zero_folds(self):
  d=valid();d['fold_count']=0;d['folds']=[];self.assertEqual(mod.validate(d)['fold_count'],0)
if __name__=='__main__':unittest.main()