#!/usr/bin/env python3
"""V70 — diagnostic-only full rear-aperture boundary audit after V69 lateral split.

V69 successfully reduced lateral rear-glass boundary straddles 56 -> 0 on a Derived-only refinement while
preserving bounds, folds and manifoldness. That does NOT prove the complete aperture loop is topology-ready.
V70 reuses V69 and audits whether host faces still cross any of the four XZ edges of the declared V60 rear
cutter band. Geometry is not further mutated by this audit.

`ONE_BOUNDARY_AXIS_RESOLVED != COMPLETE_SEMANTIC_BOUNDARY_RESOLVED`.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V69=HERE/'run_reference_repro_v69.py'
text=V69.read_text(encoding='utf-8');marker='\nrun69()\n'
if marker not in text:raise SystemExit('V69 run marker missing')
ns={'__file__':str(V69),'__name__':'oleander_v70_full_boundary_audit'}
exec(compile(text.split(marker,1)[0],str(V69),'exec'),ns)

v=ns['v'];runtime=ns['runtime'];BAND=ns['BAND'];polygons_overlap=ns['polygons_overlap'];boundary_counts=ns['boundary_counts']
REV='V70_REAR_APERTURE_FULL_BOUNDARY_AUDIT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_FULL_REAR_BOUNDARY_AUDIT_V70'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE_DIAGNOSTIC_ONLY_ON_V69_DERIVED_REFINEMENT'


def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def on_segment(a,b,p,eps=1e-9):
    return min(a[0],b[0])-eps<=p[0]<=max(a[0],b[0])+eps and min(a[1],b[1])-eps<=p[1]<=max(a[1],b[1])+eps

def segment_cross(a,b,c,d,eps=1e-9):
    o1=orient(a,b,c);o2=orient(a,b,d);o3=orient(c,d,a);o4=orient(c,d,b)
    if ((o1>eps and o2<-eps) or (o1<-eps and o2>eps)) and ((o3>eps and o4<-eps) or (o3<-eps and o4>eps)):return True
    if abs(o1)<=eps and on_segment(a,b,c,eps):return True
    if abs(o2)<=eps and on_segment(a,b,d,eps):return True
    if abs(o3)<=eps and on_segment(c,d,a,eps):return True
    if abs(o4)<=eps and on_segment(c,d,b,eps):return True
    return False

def face_crosses_edge(polyxz,a,b):
    for i in range(len(polyxz)):
        if segment_cross(polyxz[i],polyxz[(i+1)%len(polyxz)],a,b):return True
    return False

def audit(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY')
    if obj is None:raise SystemExit('FAIL_V70_REFINED_HOST_MISSING')
    mw=obj.matrix_world;edges=[(BAND[i],BAND[(i+1)%len(BAND)]) for i in range(len(BAND))]
    per_edge={f'EDGE_{i}':0 for i in range(len(edges))};cross_faces=set();samples=[]
    for p in obj.data.polygons:
        pts=[mw@obj.data.vertices[i].co for i in p.vertices];xz=[(float(q.x),float(q.z)) for q in pts]
        if not polygons_overlap(xz,BAND):continue
        hits=[]
        for idx,(a,b) in enumerate(edges):
            if face_crosses_edge(xz,a,b):
                per_edge[f'EDGE_{idx}']+=1;hits.append(idx)
        if hits:
            cross_faces.add(int(p.index))
            if len(samples)<100:samples.append({'polygon_index':int(p.index),'edge_hits':hits,'vertices_xz':xz})
    lateral=boundary_counts(obj)['REAR_LATERAL_BOUNDARY_STRADDLE']
    xz_cross=len(cross_faces)
    if lateral==0 and xz_cross==0:
        result='PASS_COMPLETE_REAR_APERTURE_BOUNDARY_TOPOLOGY_READY_FOR_PREFLIGHT'
        route='RERUN_EXCLUSIVE_OWNER_PREFLIGHT'
    elif lateral==0:
        result='HOLD_XZ_BOUNDARY_SPLIT_REQUIRED'
        route='SPLIT_DERIVED_TOPOLOGY_ON_REAR_APERTURE_XZ_BOUNDARY_EDGES_THEN_RERUN_FULL_LOOP_AUDIT'
    else:
        result='HOLD_LATERAL_AND_XZ_BOUNDARY_SPLIT_REQUIRED'
        route='RETURN_TO_BOUNDARY_REFINEMENT'
    d={'schema':'oleander.3d.full-semantic-boundary-audit.v1','candidate_revision':REV,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION',
       'host':'DERIVED_911_9922_BODY','host_representation':'V69_DERIVED_PIECEWISE_LATERAL_SPLIT','geometry_mutated_by_audit':False,
       'declared_rear_xz_boundary':BAND,'lateral_boundary_straddle_count':lateral,'xz_boundary_crossing_face_count':xz_cross,'xz_boundary_crossings_by_edge':per_edge,
       'complete_boundary_topology_ready':lateral==0 and xz_cross==0,'audit_result':result,'next_route':route,'sample_crossing_faces':samples,
       'does_not_prove':['correct aperture size','manufacturer boundary','aperture closure after deletion','reference fidelity','Class-A continuity','Design KEEP']}
    Path(out,'V70_FULL_REAR_APERTURE_BOUNDARY_AUDIT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,indent=2));return d

def run70():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    ns['emit'](out);audit(out);raise SystemExit(code)
run70()
