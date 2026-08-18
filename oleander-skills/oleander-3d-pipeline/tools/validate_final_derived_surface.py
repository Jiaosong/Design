#!/usr/bin/env python3
from __future__ import annotations
import json,math,sys
from pathlib import Path
SCHEMA='oleander.3d.final-derived-surface-receipt.v2'
def req(c,m):
    if not c:raise ValueError(m)
def validate(d):
    keys=('schema','candidate_revision','source_surface_revision','derived_surface_method','subdivision_level','topology_mode','final_connected_components','expected_aperture_boundary_edge_count','aperture_boundary_loop_count','unexpected_nonmanifold_edge_count','aperture_region_edge_p95_m','aperture_region_edge_max_m','aperture_region_sliver_face_count','aperture_region_min_face_area_m2','machine_finish_state','visual_review_state','does_not_prove')
    for k in keys:req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA,'bad:schema');req(d['topology_mode'] in ('CLOSED_SOLID_BOOLEAN','OPEN_SURFACE_APERTURE_SHELL'),'bad:topology_mode');req(int(d['subdivision_level'])>=0,'bad:subdivision_level')
    vals=[float(d['aperture_region_edge_p95_m']),float(d['aperture_region_edge_max_m']),float(d['aperture_region_min_face_area_m2'])];req(all(math.isfinite(v) and v>=0 for v in vals),'bad:surface_metrics')
    base=(int(d['final_connected_components'])==1 and int(d['unexpected_nonmanifold_edge_count'])==0 and float(d['aperture_region_edge_p95_m'])<=.12 and int(d['aperture_region_sliver_face_count'])==0)
    if d['topology_mode']=='CLOSED_SOLID_BOOLEAN':topo=(int(d['expected_aperture_boundary_edge_count'])==0 and int(d['aperture_boundary_loop_count'])==0)
    else:topo=(int(d['expected_aperture_boundary_edge_count'])>0 and int(d['aperture_boundary_loop_count'])>=4)
    quality=base and topo
    req(d['machine_finish_state'] in ('MACHINE_SURFACED_VISUAL_HOLD','MACHINE_SURFACE_FINISH_REJECT'),'bad:machine_finish_state')
    if d['machine_finish_state']=='MACHINE_SURFACED_VISUAL_HOLD':req(quality,'false:surface_finish_hold')
    else:req(not quality,'false:surface_finish_reject')
    req(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    req(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    return d
def main():
    if len(sys.argv)!=2:print('usage: validate_final_derived_surface.py RECEIPT.json',file=sys.stderr);return 2
    try:validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e:print(f'FINAL DERIVED SURFACE RECEIPT INVALID: {e}',file=sys.stderr);return 1
    print('FINAL DERIVED SURFACE RECEIPT VALID');return 0
if __name__=='__main__':raise SystemExit(main())