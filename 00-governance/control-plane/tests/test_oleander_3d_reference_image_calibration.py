import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
VP=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_reference_image_calibration.py'
spec=importlib.util.spec_from_file_location('calval',VP);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
CONTRACT=json.loads((ROOT/'oleander-skills/oleander-3d-pipeline/contracts/REFERENCE_IMAGE_CALIBRATION_CONTRACT_v1.json').read_text())

def valid():
 return {
  'reference_id':'R','target_revision':'2025_992.2_CARRERA_BODY_SHELL',
  'source_scope':{'side':{'source':'external image','allowed_transfer':'body shell'}},
  'official_hard_points_m':{'length':4.542,'width_excluding_mirrors':1.852,'height':1.298,'wheelbase':2.45,'front_axle_x':1.255,'rear_axle_x':-1.195},
  'side_calibration':{'pixel_anchors':{'rear_extreme_x':10,'rear_wheel_center_x':20,'front_wheel_center_x':80,'front_extreme_x':90,'roof_apex_y':20,'front_wheel_center_y':60}},
  'side_top_silhouette_m':[[-2.271+i*(4.542/19),.7] for i in range(20)],
  'gates':{'visual_reference_gate':'INDEPENDENT_REVIEW_REQUIRED'},
  'does_not_prove':['CAD']}
class T(unittest.TestCase):
 def test_valid(self): self.assertTrue(mod.validate(valid(),CONTRACT))
 def test_missing_scope_fails(self):
  d=valid();d['source_scope']['side'].pop('allowed_transfer')
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_non_monotonic_anchors_fail(self):
  d=valid();d['side_calibration']['pixel_anchors']['front_wheel_center_x']=15
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_short_contour_fails(self):
  d=valid();d['side_top_silhouette_m']=d['side_top_silhouette_m'][:4]
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
 def test_self_promotion_fails(self):
  d=valid();d['gates']['visual_reference_gate']='PASS'
  with self.assertRaises(SystemExit):mod.validate(d,CONTRACT)
if __name__=='__main__':unittest.main()
