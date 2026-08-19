#!/usr/bin/env python3
"""V56 — causal A/B: V49 geometry + circumferential densification only.

Question: did V50's deterministic densification reveal/create folds, or did the later transverse
profile remap create them?

Geometry source: V49 feature-aligned rail network unchanged.
Only delta: insert one derived midpoint between adjacent positive-half section controls, mirror, and
regenerate the visual hull. No profile inversion, no V51 front identity edit, no cabin-blend edit.

This is a diagnostic experiment, not a design candidate or fidelity promotion.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V49=HERE/'run_reference_repro_v49.py'
text=V49.read_text();marker='\nrun49()\n'
if marker not in text:raise SystemExit('V49 run marker missing')
ns={'__file__':str(V49),'__name__':'oleander_v56_densification_ab'}
exec(compile(text.split(marker,1)[0],str(V49),'exec'),ns)

v=ns['v'];core=ns['core'];base_build=ns['base_build'];apply_subd=ns['apply_subd'];base_ring=ns['feature_ring49'];RAILS=ns['RAILS']
REV='V56_V49_DENSIFICATION_ONLY_AB'
v.REF='2025_992.2_CARRERA_V56_DENSIFICATION_AB'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['experiment']='V49_SOURCE_PLUS_DERIVED_CIRCUMFERENTIAL_DENSIFICATION_ONLY'
v.REFERENCE_CONTRACT['does_not_prove']=['reference fidelity','design quality','Class-A continuity']

def dense56(x):
    full=base_ring(x);half=full[:11];dense=[]
    for a,b in zip(half,half[1:]):
        dense.append(a);dense.append(tuple((a[j]+b[j])*.5 for j in range(3)))
    dense.append(half[-1])
    return dense+[(px,-py,pz) for px,py,pz in reversed(dense[1:-1])]
core['hull_ring']=dense56;v.body_ring=dense56

def build56(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        o['OLEANDER_EXPERIMENT']=REV;o['OLEANDER_SOURCE']='V49_FEATURE_ALIGNED_CURVE_NETWORK';o['OLEANDER_ONLY_DELTA']='DERIVED_CIRCUMFERENTIAL_DENSIFICATION'
    return o
core['build_visual_hull']=build56

def fold_rows(o):
    me=o.data;ef={};rows=[]
    for p in me.polygons:
        for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
    for e,fs in ef.items():
        if len(fs)==2:
            dot=float(me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal))
            if dot<-.15:
                c=(me.vertices[e[0]].co+me.vertices[e[1]].co)*.5;rows.append({'edge_vertices':list(e),'face_indices':fs,'normal_dot':dot,'center_m':[float(c.x),float(c.y),float(c.z)]})
    return rows

def run56():
    a=v.m.parse_args();out=Path(a.out).resolve();v.main();body=bpy.data.objects.get('DERIVED_911_9922_BODY');rows=fold_rows(body) if body else []
    d={'schema':'oleander.3d.densification-causal-ab.v1','candidate_revision':REV,'baseline_revision':'V49_FEATURE_ALIGNED_CURVE_NETWORK','source_geometry_equivalence':'V49_SOURCE_RELATIONS_UNCHANGED','only_delta':'ONE_DERIVED_MIDPOINT_PER_ADJACENT_POSITIVE_HALF_SECTION_CONTROL','source_semantic_rail_count':len(RAILS),'derived_ring_vertices':len(dense56(0.0)),'fold_count':len(rows),'folds':rows,'causal_interpretation':'DENSIFICATION_ALONE_CAUSES_OR_REVEALS_FOLDS' if rows else 'DENSIFICATION_ALONE_NOT_CAUSAL_FOR_FOLDS','design_state':'DIAGNOSTIC_ONLY','does_not_prove':['reference fidelity','design quality','Class-A continuity']}
    Path(out,'DENSIFICATION_CAUSAL_AB.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'OLEANDER_PORSCHE_911_CARRERA_992_REFERENCE_REPRO.blend'))
    print(json.dumps({'fold_count':len(rows),'interpretation':d['causal_interpretation'],'derived_ring_vertices':d['derived_ring_vertices']},indent=2))
run56()
