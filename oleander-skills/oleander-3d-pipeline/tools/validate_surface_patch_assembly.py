#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
SCHEMA='oleander.3d.surface-patch-assembly-receipt.v1'
def req(c,m):
    if not c:raise ValueError(m)
def validate(d):
    for k in ('schema','candidate_revision','opaque_patch_count','glass_patch_count','patches','boundary_pairs','max_shared_boundary_gap_m','floating_visible_patch_count','machine_assembly_state','visual_review_state','does_not_prove'):req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA,'bad:schema');req(int(d['opaque_patch_count'])>=3,'fail:opaque_patch_count');req(int(d['glass_patch_count'])>=3,'fail:glass_patch_count')
    req(isinstance(d['patches'],list) and len(d['patches'])>=int(d['opaque_patch_count'])+int(d['glass_patch_count']),'bad:patches')
    for p in d['patches']:req(p.get('id') and p.get('role') and p.get('authority'),'bad:patch')
    req(isinstance(d['boundary_pairs'],list) and len(d['boundary_pairs'])>=4,'fail:boundary_pairs')
    gaps=[]
    for b in d['boundary_pairs']:
        req(b.get('id') and 'max_gap_m' in b,'bad:boundary_pair');g=float(b['max_gap_m']);req(math.isfinite(g) and g>=0,'bad:boundary_gap');gaps.append(g)
    mg=float(d['max_shared_boundary_gap_m']);req(math.isfinite(mg) and mg>=0,'bad:max_gap');req(abs(mg-max(gaps))<=1e-9,'bad:max_gap_recompute')
    quality=(mg<=.010 and int(d['floating_visible_patch_count'])==0)
    req(d['machine_assembly_state'] in ('MACHINE_ASSEMBLED_VISUAL_HOLD','MACHINE_ASSEMBLY_REJECT'),'bad:machine_assembly_state')
    if d['machine_assembly_state']=='MACHINE_ASSEMBLED_VISUAL_HOLD':req(quality,'false:assembly_hold')
    else:req(not quality,'false:assembly_reject')
    req(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    req(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    return d
def main():
    if len(sys.argv)!=2:print('usage: validate_surface_patch_assembly.py RECEIPT.json',file=sys.stderr);return 2
    try:validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e:print(f'SURFACE PATCH ASSEMBLY RECEIPT INVALID: {e}',file=sys.stderr);return 1
    print('SURFACE PATCH ASSEMBLY RECEIPT VALID');return 0
if __name__=='__main__':raise SystemExit(main())