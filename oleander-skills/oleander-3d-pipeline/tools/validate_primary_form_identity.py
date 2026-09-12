#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
SCHEMA='oleander.3d.primary-form-identity-receipt.v1'

def req(c,m):
    if not c: raise ValueError(m)
def finite(x): return isinstance(x,(int,float)) and math.isfinite(float(x))
def validate(d):
    for k in ('schema','candidate_revision','reference_revision','gesture_metric','front_profile_metric','rear_profile_metric','identity_relations','finite_measurement_coverage','pre_aperture_surface_state','regression_decision','visual_review_state','machine_identity_state','does_not_prove'):
        req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA,'bad:schema')
    for k in ('gesture_metric','front_profile_metric','rear_profile_metric'):
        m=d[k]; req(isinstance(m,dict),'bad:'+k); req(finite(m.get('candidate')),'nonfinite:'+k); req(finite(m.get('limit')) and float(m['limit'])>0,'bad_limit:'+k)
    cov=float(d['finite_measurement_coverage']); req(math.isfinite(cov) and .90<=cov<=1.0,'fail:measurement_coverage')
    req(d['pre_aperture_surface_state'] in ('MACHINE_CONSTRUCTED_VISUAL_HOLD','MACHINE_SURFACE_TOPOLOGY_FAIL'),'bad:surface_state')
    req(d['regression_decision'] in ('KEEP_LKG_HOLD_EXPERIMENT','KEEP_LKG_REJECT_EXPERIMENT'),'bad:regression_decision')
    req(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    req(d['machine_identity_state'] in ('MACHINE_SCREENED_VISUAL_HOLD','MACHINE_REJECT'),'bad:machine_identity_state')
    rel=d['identity_relations']; req(isinstance(rel,list) and len(rel)>=2,'fail:identity_relations_missing')
    for r in rel:
        req(isinstance(r,dict) and r.get('id') and r.get('state') in ('SCREENED','FAIL','HOLD'),'bad:identity_relation')
    req(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    if d['machine_identity_state']=='MACHINE_SCREENED_VISUAL_HOLD':
        req(all(float(d[k]['candidate'])<=float(d[k]['limit']) for k in ('gesture_metric','front_profile_metric','rear_profile_metric')),'false_machine_screen')
        req(d['pre_aperture_surface_state']=='MACHINE_CONSTRUCTED_VISUAL_HOLD','false_surface_screen')
        req(all(r['state']=='SCREENED' for r in rel),'false_relation_screen')
    return d

def main():
    if len(sys.argv)!=2: print('usage: validate_primary_form_identity.py RECEIPT.json',file=sys.stderr); return 2
    try: validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e: print(f'PRIMARY FORM IDENTITY RECEIPT FAIL: {e}',file=sys.stderr); return 1
    print('PRIMARY FORM IDENTITY RECEIPT PASS'); return 0
if __name__=='__main__': raise SystemExit(main())
