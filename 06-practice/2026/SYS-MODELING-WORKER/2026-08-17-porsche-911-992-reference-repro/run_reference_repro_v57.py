#!/usr/bin/env python3
"""V57 — Source-cage vs evaluated-surface density audit; geometry unchanged from V49.

Question: did V49 actually lack evaluated surface density, or did the surface receipt incorrectly use
Source ring control count as a Derived/evaluated-density gate?

No geometry edit. Build V49 unchanged, then persist separate topology statistics for:
- Source/cage metadata (semantic rail + ring control count);
- production body mesh after V49's normal build path;
- final evaluated diagnostic surface used by projection.

This diagnostic exists to repair the Skill contract, not to promote V49 reference fidelity.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V49=HERE/'run_reference_repro_v49.py'
text=V49.read_text(); marker='\nrun49()\n'
if marker not in text: raise SystemExit('V49 run marker missing')
ns={'__file__':str(V49),'__name__':'oleander_v57_density_audit'}
exec(compile(text.split(marker,1)[0],str(V49),'exec'),ns)

v=ns['v']; RAILS=ns['RAILS']
REV='V57_V49_SOURCE_VS_EVALUATED_DENSITY_AUDIT'

def mesh_stats(obj):
    if obj is None: return None
    me=obj.data
    me.calc_loop_triangles()
    edge_lengths=[]
    mw=obj.matrix_world
    for e in me.edges:
        a=mw@me.vertices[e.vertices[0]].co; b=mw@me.vertices[e.vertices[1]].co
        edge_lengths.append(float((a-b).length))
    edge_lengths.sort()
    p95=edge_lengths[min(len(edge_lengths)-1,max(0,int(math.ceil(.95*len(edge_lengths))-1)))] if edge_lengths else None
    ef={}
    for p in me.polygons:
        for e in p.edge_keys: ef.setdefault(tuple(sorted(e)),[]).append(p.index)
    flips=0
    for fs in ef.values():
        if len(fs)==2 and float(me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal))<-.15: flips+=1
    return {
      'object':obj.name,
      'vertices':len(me.vertices),'edges':len(me.edges),'faces':len(me.polygons),
      'triangles':len(me.loop_triangles),'edge_p95_m':p95,'adjacent_face_normal_flip_count':flips,
      'oleander_ring_vertices_property':int(obj.get('OLEANDER_RING_VERTICES',0)),
      'oleander_longitudinal_stations_property':int(obj.get('OLEANDER_LONGITUDINAL_STATIONS',0))
    }

def emit(out):
    body=bpy.data.objects.get('DERIVED_911_9922_BODY')
    diag=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V49')
    bs=mesh_stats(body); ds=mesh_stats(diag)
    d={
      'schema':'oleander.3d.source-vs-evaluated-density-audit.v1',
      'candidate_geometry_revision':'V49_FEATURE_ALIGNED_CURVE_NETWORK',
      'evidence_revision':REV,
      'geometry_revision_unchanged':'V49_FEATURE_ALIGNED_CURVE_NETWORK',
      'source_semantic_rail_count':len(RAILS),
      'source_ring_control_count':20,
      'production_body_mesh':bs,
      'final_evaluated_diagnostic_mesh':ds,
      'legacy_surface_gate':{'required_body_ring_vertices_min':30,'observed_source_ring_control_count':20,'state':'LEGACY_GATE_MIXES_SOURCE_CONTROL_DENSITY_WITH_EVALUATED_DENSITY'},
      'density_interpretation':'EVALUATED_DENSITY_MUST_BE_MEASURED_ON_EVALUATED_CARRIER_NOT_SOURCE_RING_CONTROL_COUNT',
      'does_not_prove':['reference fidelity','reflection fairness','Class-A continuity','design quality','manufacturing feasibility']
    }
    Path(out,'SOURCE_VS_EVALUATED_DENSITY_AUDIT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2))

def run57():
    a=v.m.parse_args(); out=Path(a.out).resolve()
    try:
        v.main()
    except SystemExit as e:
        emit(out)
        if isinstance(e.code,int) and e.code not in (0,None): raise
    else:
        emit(out)
run57()
