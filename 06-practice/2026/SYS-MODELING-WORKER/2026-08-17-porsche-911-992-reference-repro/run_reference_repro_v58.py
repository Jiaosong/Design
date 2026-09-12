#!/usr/bin/env python3
"""V58 — v2 primary-surface receipt on unchanged V49 geometry.

Geometry delta: NONE.
Source/representation: V49_FEATURE_ALIGNED_CURVE_NETWORK unchanged.
Purpose: validate the repaired OLEANDER primary-surface machine gate using the final evaluated carrier
instead of Source ring-control count.

A machine surface HOLD/PASS does not change V49 Reference Fidelity or Design Quality, which remain
REJECT/REVISE pending held-out visual/reference review and later aperture/identity work.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V49=HERE/'run_reference_repro_v49.py'
text=V49.read_text(); marker='\nrun49()\n'
if marker not in text: raise SystemExit('V49 run marker missing')
ns={'__file__':str(V49),'__name__':'oleander_v58_surface_receipt_v2'}
exec(compile(text.split(marker,1)[0],str(V49),'exec'),ns)

v=ns['v']; RAILS=ns['RAILS']
REV='V58_V49_SURFACE_RECEIPT_V2'
SOURCE_GEOM='V49_FEATURE_ALIGNED_CURVE_NETWORK'
EVAL='DIAG_FEATURE_ALIGNED_SURFACED_V49'

def components(obj):
    me=obj.data;adj=[set() for _ in me.vertices];used=set()
    for p in me.polygons:
        vs=list(p.vertices);used.update(vs)
        for a,b in zip(vs,vs[1:]+vs[:1]):adj[a].add(b);adj[b].add(a)
    seen=set();n=0
    for s in used:
        if s in seen:continue
        n+=1;stack=[s];seen.add(s)
        while stack:
            q=stack.pop()
            for z in adj[q]:
                if z not in seen:seen.add(z);stack.append(z)
    return n

def fold_count(obj):
    me=obj.data;ef={};n=0
    for p in me.polygons:
        for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
    for fs in ef.values():
        if len(fs)==2 and float(me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal))<-.15:n+=1
    return n

def edge_p95(obj):
    mw=obj.matrix_world;ls=[]
    for e in obj.data.edges:
        a=mw@obj.data.vertices[e.vertices[0]].co;b=mw@obj.data.vertices[e.vertices[1]].co;ls.append(float((a-b).length))
    ls.sort();return ls[min(len(ls)-1,max(0,int(math.ceil(.95*len(ls))-1)))] if ls else float('inf')

def emit(out):
    body=bpy.data.objects.get('DERIVED_911_9922_BODY');ev=bpy.data.objects.get(EVAL)
    if body is None or ev is None: raise SystemExit('FAIL_V58_EVALUATED_CARRIER_MISSING')
    me=ev.data;me.calc_loop_triangles();p95=edge_p95(ev);folds=fold_count(ev);comps=components(ev)
    sampling_status='PASS' if math.isfinite(p95) and p95<=.30 else 'HOLD'
    machine='MACHINE_CONSTRUCTED_VISUAL_HOLD' if comps==1 and folds==0 and sampling_status=='PASS' else ('MACHINE_SURFACE_TOPOLOGY_FAIL' if comps!=1 or folds!=0 else 'MACHINE_SURFACE_SAMPLING_HOLD')
    d={
      'schema':'oleander.3d.primary-body-surface-receipt.v2',
      'revision':REV,
      'geometry_revision_unchanged':SOURCE_GEOM,
      'surface_measurement_scope':'CLOSED_PRIMARY_VISUAL_HULL_BEFORE_FINAL_APERTURE_ARCHITECTURE',
      'source_state_class':'SOURCE_CONTROL_CAGE',
      'source_semantic_rail_count':len(RAILS),
      'source_ring_control_count':int(body.get('OLEANDER_RING_VERTICES',20) or 20),
      'source_density_role':'INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE',
      'evaluated_carrier':EVAL,
      'evaluated_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY',
      'evaluated_vertices':len(me.vertices),
      'evaluated_edges':len(me.edges),
      'evaluated_faces':len(me.polygons),
      'evaluated_triangles':len(me.loop_triangles),
      'evaluated_connected_components':comps,
      'evaluated_adjacent_face_normal_flip_count':folds,
      'evaluated_edge_p95_m':p95,
      'evaluated_sampling_gate':{
        'basis':'EVALUATED_EDGE_P95_AT_CURRENT_REVIEW_SCALE',
        'status':sampling_status,
        'threshold_or_rule':'evaluated_edge_p95_m <= 0.30',
        'observed':p95,
        'review_scope':'current 992.2 primary-form diagnostic / 960-1152px review renders; not a universal production tolerance'
      },
      'machine_surface_state':machine,
      'visual_review_state':'REJECT',
      'reference_fidelity_state':'REJECT',
      'design_quality_state':'REVISE',
      'legacy_v49_surface_failure_reclassified':'OLD_V1_SOURCE_RING_DENSITY_GATE_INVALID_FOR_EVALUATED_SURFACE_QUALITY',
      'does_not_prove':['reference fidelity','Class-A continuity','reflection fairness','final aperture architecture','manufacturing feasibility','Design KEEP','MAIN KEEP']
    }
    Path(out,'PRIMARY_BODY_SURFACE_RECEIPT_V2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    Path(out,'PRIMARY_BODY_SURFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2))

def run58():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:
        v.main()
    except SystemExit as e:
        emit(out)
        if isinstance(e.code,int) and e.code not in (0,None): raise
    else: emit(out)
run58()
