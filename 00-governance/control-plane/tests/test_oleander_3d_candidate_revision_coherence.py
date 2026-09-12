import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
TOOL=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_candidate_revision_coherence.py'
spec=importlib.util.spec_from_file_location('rc',TOOL);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

def write_bundle(base,qa='V33',pr='V33',rg='V33',sf='V33'):
 (base/'REFERENCE_REPRO_QA.json').write_text(json.dumps({'reference_fidelity_revision':qa}))
 (base/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps({'candidate_revision':pr}))
 (base/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps({'candidate_revision':rg}))
 (base/'PRIMARY_BODY_SURFACE_RECEIPT.json').write_text(json.dumps({'revision':sf}))
class T(unittest.TestCase):
 def test_valid(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);write_bundle(p);self.assertEqual(mod.validate_bundle(p)['projection'],'V33')
 def test_stale_qa_fails(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);write_bundle(p,qa='V30')
   with self.assertRaises(ValueError):mod.validate_bundle(p)
 def test_stale_surface_fails(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);write_bundle(p,sf='V31')
   with self.assertRaises(ValueError):mod.validate_bundle(p)
 def test_missing_revision_fails(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);write_bundle(p);(p/'REFERENCE_REPRO_QA.json').write_text('{}')
   with self.assertRaises(ValueError):mod.validate_bundle(p)
if __name__=='__main__':unittest.main()
