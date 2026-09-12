#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path

def metric(d,mid): return next(m for m in d['metrics'] if m['id']==mid)
def main():
    if len(sys.argv)!=2: raise SystemExit('usage: emit_primary_form_identity_receipt.py OUT_DIR')
    out=Path(sys.argv[1]);p=json.loads((out/'REFERENCE_PROJECTION_RECEIPT.json').read_text());g=json.loads((out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').read_text());s=json.loads((out/'PRIMARY_BODY_SURFACE_RECEIPT.json').read_text());c=json.loads((out/'REFERENCE_CONTRACT.json').read_text())
    side=metric(p,'SIDE_UPPER_EVALUATED_MESH_RMSE_M');front=metric(p,'FRONT_HALF_PROJECTED_PROFILE_RMSE');rear=metric(p,'REAR_HALF_PROJECTED_PROFILE_RMSE')
    cov=float(p.get('side_upper_finite_sample_coverage',1.0))
    front_sem=p.get('front_identity_metrics')
    if isinstance(front_sem,dict):
        sem_state='SCREENED' if front_sem.get('semantic_relation_state')=='SCREENED' else ('FAIL' if front_sem.get('semantic_relation_state')=='FAIL' else 'HOLD')
    else:
        sem_state='HOLD'
    rel=[
      {'id':'FASTBACK_GESTURE','state':'SCREENED' if math.isfinite(float(side['candidate'])) and float(side['candidate'])<=float(side['limit']) else 'FAIL'},
      {'id':'REAR_HIGH_MASS_TAPER','state':'SCREENED' if math.isfinite(float(rear['candidate'])) and float(rear['candidate'])<=float(rear['limit']) else 'FAIL'},
      {'id':'FRONT_GROSS_PROFILE','state':'SCREENED' if math.isfinite(float(front['candidate'])) and float(front['candidate'])<=float(front['limit']) else 'FAIL'},
      {'id':'FRONT_HOOD_FENDER_HIERARCHY','state':sem_state,'evidence':'front_identity_metrics' if front_sem else 'MISSING_SEMANTIC_RELATION_METRIC'},
    ]
    machine_ok=(cov>=.90 and all(r['state']=='SCREENED' for r in rel) and s.get('machine_surface_state')=='MACHINE_CONSTRUCTED_VISUAL_HOLD')
    d={'schema':'oleander.3d.primary-form-identity-receipt.v1','candidate_revision':p.get('candidate_revision'),'reference_revision':c.get('reference_revision'),'gesture_metric':{'candidate':side['candidate'],'limit':side['limit']},'front_profile_metric':{'candidate':front['candidate'],'limit':front['limit']},'rear_profile_metric':{'candidate':rear['candidate'],'limit':rear['limit']},'front_semantic_identity_metric':front_sem if front_sem else {'state':'HOLD','reason':'MISSING_SEMANTIC_RELATION_METRIC'},'identity_relations':rel,'finite_measurement_coverage':cov,'pre_aperture_surface_state':s.get('machine_surface_state'),'regression_decision':g.get('promotion_decision'),'visual_review_state':'NOT_RUN','machine_identity_state':'MACHINE_SCREENED_VISUAL_HOLD' if machine_ok else 'MACHINE_REJECT','does_not_prove':['reference fidelity','manufacturer CAD','Class-A continuity','production patch layout','manufacturing feasibility','homologation']}
    (out/'PRIMARY_FORM_IDENTITY_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2))
if __name__=='__main__': main()
