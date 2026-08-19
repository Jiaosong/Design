from __future__ import annotations
import importlib.util,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];P=ROOT/'oleander-skills/oleander-3d-pipeline/tools/validate_evidence_carrier_congruence.py'
s=importlib.util.spec_from_file_location('ecc',P);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
C=json.loads((ROOT/'oleander-skills/oleander-3d-pipeline/contracts/EVIDENCE_CARRIER_CONGRUENCE_CONTRACT_v1.json').read_text())
def r(): return {'schema':'oleander.3d.evidence-carrier-receipt.v1','claim_id':'WHOLE_VISIBLE_GROSS_PROFILE','claim_scope':'WHOLE_VISIBLE_GROSS','reference_carrier':'REF_STUDIO_SILHOUETTE','reference_carrier_scope':'WHOLE_VISIBLE_GROSS','candidate_carrier':'BODY_PLUS_GREENHOUSE_PROXY','candidate_carrier_scope':'WHOLE_VISIBLE_GROSS','candidate_state_class':'VISUAL_PROXY','coverage_relation':'SUFFICIENT_PROXY_FOR_DECLARED_SCOPE','measurement_method':'LOCKED_PROJECTED_PROFILE','normalization_frame':'VEHICLE_BOTTOM_TO_TOP_BODY_WIDTH','regression_comparability':'NOT_APPLICABLE','result':'PASS_SUFFICIENT_PROXY_FOR_DECLARED_SCOPE','proxy_claim_boundary':'GROSS_SILHOUETTE_ONLY','does_not_prove':['final aperture architecture','reference fidelity']}
class T(unittest.TestCase):
 def test_valid_proxy(self): self.assertTrue(m.validate(r(),C))
 def test_mismatch_cannot_pass(self):
  d=r();d['coverage_relation']='MISMATCH';d['result']='PASS_CARRIER_CONGRUENCE'
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_proxy_needs_boundary(self):
  d=r();d.pop('proxy_claim_boundary')
  with self.assertRaises(SystemExit):m.validate(d,C)
 def test_congruent_pass(self):
  d=r();d['candidate_state_class']='DERIVED_DIAGNOSTIC';d['coverage_relation']='CONGRUENT';d['result']='PASS_CARRIER_CONGRUENCE';d.pop('proxy_claim_boundary')
  self.assertTrue(m.validate(d,C))
if __name__=='__main__': unittest.main()
