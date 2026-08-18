#!/usr/bin/env python3
"""Validate machine evidence for visible-surface topology without self-promoting design quality."""
from __future__ import annotations
import json, math, sys
from pathlib import Path

SCHEMA='oleander.3d.visible-surface-topology-receipt.v1'
REQUIRED_GLAZING={
 'REF_WINDSHIELD','REF_DOOR_GLASS_L','REF_DOOR_GLASS_R',
 'REF_QUARTER_GLASS_L','REF_QUARTER_GLASS_R','REF_REAR_GLASS'
}

def require(c,m):
    if not c: raise ValueError(m)

def validate(d):
    for k in ('schema','revision','opaque_cabin_object','opaque_cabin_exists','opaque_cabin_architecture',
              'opaque_cabin_connected_components','shared_vertex_boundary_count','aperture_boundary_gap_max_m',
              'adjacent_face_normal_flip_count','open_patch_rim_walls','forbidden_floating_interface_objects',
              'forbidden_floating_interface_count','real_glazing_objects','no_opaque_surface_behind_glazing_declared',
              'machine_topology_state','visual_review_state','does_not_prove'):
        require(k in d,f'missing:{k}')
    require(d['schema']==SCHEMA,'bad:schema')
    require(d['opaque_cabin_object']=='DERIVED_911_9922_CABIN','bad:opaque_cabin_object')
    require(d['opaque_cabin_exists'] is True,'fail:opaque_cabin_missing')
    require(isinstance(d['opaque_cabin_architecture'],str) and d['opaque_cabin_architecture'],'bad:opaque_cabin_architecture')
    require(d['opaque_cabin_connected_components']==1,'fail:opaque_cabin_disconnected_islands')
    require(isinstance(d['shared_vertex_boundary_count'],int) and d['shared_vertex_boundary_count']>=4,'fail:shared_vertex_boundaries_insufficient')
    gap=float(d['aperture_boundary_gap_max_m']); require(math.isfinite(gap) and gap<=0.002,'fail:aperture_boundary_gap')
    require(isinstance(d['adjacent_face_normal_flip_count'],int) and d['adjacent_face_normal_flip_count']==0,'fail:adjacent_face_normal_flip')
    require(d['open_patch_rim_walls'] is False,'fail:open_patch_solidify_rim_walls')
    forbidden=d['forbidden_floating_interface_objects']
    require(isinstance(forbidden,list),'bad:forbidden_floating_interface_objects')
    require(d['forbidden_floating_interface_count']==len(forbidden),'bad:forbidden_count_mismatch')
    require(len(forbidden)==0,'fail:floating_visible_interface_objects')
    glazing=set(d['real_glazing_objects'])
    require(REQUIRED_GLAZING.issubset(glazing),'fail:required_glazing_missing')
    require(d['no_opaque_surface_behind_glazing_declared'] is True,'fail:opaque_surface_behind_glazing_not_resolved')
    require(d['machine_topology_state']=='MACHINE_CONSTRUCTED_VISUAL_HOLD','bad:machine_topology_state')
    require(d['visual_review_state'] in ('NOT_RUN','HOLD','REVISE','REJECT','KEEP'),'bad:visual_review_state')
    require(isinstance(d['does_not_prove'],list) and 'reference fidelity' in d['does_not_prove'],'bad:does_not_prove')
    return d

def main():
    if len(sys.argv)!=2:
        print('usage: validate_visible_surface_topology.py RECEIPT.json',file=sys.stderr);return 2
    try: validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e:
        print(f'VISIBLE SURFACE TOPOLOGY RECEIPT FAIL: {e}',file=sys.stderr);return 1
    print('VISIBLE SURFACE TOPOLOGY RECEIPT PASS');return 0

if __name__=='__main__': raise SystemExit(main())
