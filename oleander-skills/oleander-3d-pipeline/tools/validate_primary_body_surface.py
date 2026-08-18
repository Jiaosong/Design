#!/usr/bin/env python3
"""Fail-closed machine validator for dense primary-body surface experiments."""
from __future__ import annotations
import json, math, sys
from pathlib import Path

SCHEMA='oleander.3d.primary-body-surface-receipt.v1'

def req(c,m):
    if not c:raise ValueError(m)

def validate(d):
    for k in ('schema','revision','surface_measurement_scope','body_cap_edges_excluded',
              'body_connected_components','cabin_connected_components',
              'body_adjacent_face_normal_flip_count','cabin_adjacent_face_normal_flip_count',
              'body_local_edge_p95_m','body_longitudinal_stations','body_ring_vertices',
              'machine_surface_state','visual_review_state','does_not_prove'):
        req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA,'bad:schema')
    req(d['surface_measurement_scope']=='PRE_APERTURE_PRIMARY_SKIN','bad:surface_measurement_scope')
    req(d['body_cap_edges_excluded'] is True,'bad:body_cap_edges_excluded')
    req(d['body_connected_components']==1,'fail:body_disconnected')
    req(d['cabin_connected_components']==1,'fail:cabin_disconnected')
    req(d['body_adjacent_face_normal_flip_count']==0,'fail:body_face_fold')
    req(d['cabin_adjacent_face_normal_flip_count']==0,'fail:cabin_face_fold')
    edge=float(d['body_local_edge_p95_m']);req(math.isfinite(edge) and edge<=.30,'fail:body_local_edge_stretch')
    req(int(d['body_longitudinal_stations'])>=80,'fail:body_station_density')
    req(int(d['body_ring_vertices'])>=30,'fail:body_section_rail_density')
    req(d['machine_surface_state']=='MACHINE_CONSTRUCTED_VISUAL_HOLD','bad:machine_surface_state')
    req(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    req(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    return d

def main():
    if len(sys.argv)!=2:
        print('usage: validate_primary_body_surface.py RECEIPT.json',file=sys.stderr);return 2
    try:validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e:
        print(f'PRIMARY BODY SURFACE RECEIPT FAIL: {e}',file=sys.stderr);return 1
    print('PRIMARY BODY SURFACE RECEIPT PASS');return 0

if __name__=='__main__':raise SystemExit(main())
