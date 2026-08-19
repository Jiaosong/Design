#!/usr/bin/env python3
"""Validate primary-body surface receipts without collapsing Source cage density into evaluated-surface quality.

v1 is retained as legacy compatibility. v2 is the current candidate semantics:
- Source/cage control counts are informational authority metadata only.
- Machine surface quality is screened on the declared final evaluated carrier.
- Evaluation/tessellation may be dense while Source controls remain causally sparse.
"""
from __future__ import annotations
import json, math, sys
from pathlib import Path
SCHEMA_V1='oleander.3d.primary-body-surface-receipt.v1'
SCHEMA_V2='oleander.3d.primary-body-surface-receipt.v2'

def req(c,m):
    if not c: raise ValueError(m)

def finite_nonneg(v,name):
    req(isinstance(v,(int,float)) and math.isfinite(float(v)) and float(v)>=0,f'bad:{name}')
    return float(v)

def validate_v1(d):
    """Legacy semantics only. Do not use v1 to justify new Source densification."""
    for k in ('schema','revision','surface_measurement_scope','body_cap_edges_excluded','body_connected_components','cabin_connected_components','body_adjacent_face_normal_flip_count','cabin_adjacent_face_normal_flip_count','body_local_edge_p95_m','body_longitudinal_stations','body_ring_vertices','machine_surface_state','visual_review_state','does_not_prove'):
        req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA_V1,'bad:schema')
    req(d['surface_measurement_scope']=='PRE_APERTURE_PRIMARY_SKIN','bad:surface_measurement_scope')
    req(d['body_cap_edges_excluded'] is True,'bad:body_cap_edges_excluded')
    edge=finite_nonneg(d['body_local_edge_p95_m'],'body_local_edge_stretch')
    comps_ok=(d['body_connected_components']==1 and d['cabin_connected_components']==1)
    folds_ok=(d['body_adjacent_face_normal_flip_count']==0 and d['cabin_adjacent_face_normal_flip_count']==0)
    density_ok=(int(d['body_longitudinal_stations'])>=80 and int(d['body_ring_vertices'])>=30)
    stretch_ok=edge<=.30
    quality_ok=comps_ok and folds_ok and density_ok and stretch_ok
    req(d['machine_surface_state'] in ('MACHINE_CONSTRUCTED_VISUAL_HOLD','MACHINE_SURFACE_TOPOLOGY_FAIL'),'bad:machine_surface_state')
    if d['machine_surface_state']=='MACHINE_CONSTRUCTED_VISUAL_HOLD': req(quality_ok,'false:constructed_state')
    else: req(not quality_ok,'false:failure_state')
    req(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    req(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    d.setdefault('legacy_semantics','SOURCE_RING_COUNT_INCLUDED_IN_QUALITY_GATE_DO_NOT_USE_FOR_NEW_DENSIFICATION_DECISIONS')
    return d

def validate_v2(d):
    for k in (
        'schema','revision','surface_measurement_scope','source_state_class','source_semantic_rail_count',
        'source_ring_control_count','evaluated_carrier','evaluated_state_class','evaluated_vertices','evaluated_edges',
        'evaluated_faces','evaluated_triangles','evaluated_connected_components','evaluated_adjacent_face_normal_flip_count',
        'evaluated_edge_p95_m','evaluated_sampling_gate','machine_surface_state','visual_review_state','does_not_prove'
    ):
        req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA_V2,'bad:schema')
    req(d['surface_measurement_scope'] in ('PRE_APERTURE_PRIMARY_SKIN','CLOSED_PRIMARY_VISUAL_HULL_BEFORE_FINAL_APERTURE_ARCHITECTURE'),'bad:surface_measurement_scope')
    req(d['source_state_class'] in ('SOURCE_OR_WORKING_SOURCE','SOURCE_CONTROL_CAGE'),'bad:source_state_class')
    req(d['evaluated_state_class'] in ('DERIVED_EXECUTION','DERIVED_DIAGNOSTIC_NOT_AUTHORITY'),'bad:evaluated_state_class')
    req(isinstance(d['evaluated_carrier'],str) and d['evaluated_carrier'],'bad:evaluated_carrier')
    source_rails=int(d['source_semantic_rail_count']); source_ring=int(d['source_ring_control_count'])
    req(source_rails>0 and source_ring>0,'bad:source_control_counts')
    # Source counts are intentionally NOT used in quality_ok.
    ev_vertices=int(d['evaluated_vertices']); ev_edges=int(d['evaluated_edges']); ev_faces=int(d['evaluated_faces']); ev_tris=int(d['evaluated_triangles'])
    req(ev_vertices>0 and ev_edges>0 and ev_faces>0 and ev_tris>0,'bad:evaluated_topology_counts')
    edge=finite_nonneg(d['evaluated_edge_p95_m'],'evaluated_edge_p95_m')
    comps_ok=int(d['evaluated_connected_components'])==1
    folds_ok=int(d['evaluated_adjacent_face_normal_flip_count'])==0
    sampling=d['evaluated_sampling_gate']; req(isinstance(sampling,dict),'bad:evaluated_sampling_gate')
    for k in ('basis','status','threshold_or_rule','observed'):
        req(k in sampling,f'missing:evaluated_sampling_gate.{k}')
    req(sampling['status'] in ('PASS','FAIL','HOLD'),'bad:evaluated_sampling_gate.status')
    req(sampling['basis']!='SOURCE_RING_CONTROL_COUNT','fail:source_density_used_as_evaluated_sampling_gate')
    sampling_ok=sampling['status']=='PASS'
    quality_ok=comps_ok and folds_ok and sampling_ok
    req(d['machine_surface_state'] in ('MACHINE_CONSTRUCTED_VISUAL_HOLD','MACHINE_SURFACE_TOPOLOGY_FAIL','MACHINE_SURFACE_SAMPLING_HOLD'),'bad:machine_surface_state')
    if d['machine_surface_state']=='MACHINE_CONSTRUCTED_VISUAL_HOLD': req(quality_ok,'false:constructed_state')
    elif d['machine_surface_state']=='MACHINE_SURFACE_TOPOLOGY_FAIL': req(not comps_ok or not folds_ok,'false:topology_failure_state')
    else: req(comps_ok and folds_ok and not sampling_ok,'false:sampling_hold_state')
    req(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    req(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    if 'source_density_role' in d:
        req(d['source_density_role']=='INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE','bad:source_density_role')
    return d

def validate(d):
    schema=d.get('schema')
    if schema==SCHEMA_V1:return validate_v1(d)
    if schema==SCHEMA_V2:return validate_v2(d)
    raise ValueError('bad:schema')

def main():
    if len(sys.argv)!=2: print('usage: validate_primary_body_surface.py RECEIPT.json',file=sys.stderr);return 2
    try:validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e: print(f'PRIMARY BODY SURFACE RECEIPT INVALID: {e}',file=sys.stderr);return 1
    print('PRIMARY BODY SURFACE RECEIPT VALID');return 0
if __name__=='__main__':raise SystemExit(main())
