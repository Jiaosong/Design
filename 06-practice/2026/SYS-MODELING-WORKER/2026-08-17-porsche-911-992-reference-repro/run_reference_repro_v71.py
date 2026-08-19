#!/usr/bin/env python3
"""V71 — complete rear-aperture XZ boundary refinement on top of V69.

V69 resolved the lateral rear-glass boundary with Derived-only topology refinement. V70 then showed that
118 host faces still touched/crossed the four XZ edges of the declared V60 rear cutter band. V71 refines only
faces that truly straddle each XZ edge line (signed vertices on both sides), using local BMesh plane bisection.

No Source controls are added; V59 remains Source/LKG. No aperture faces are deleted in V71.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V69=HERE/'run_reference_repro_v69.py'
text=V69.read_text(encoding='utf-8');marker='\nrun69()\n'
if marker not in text:raise SystemExit('V69 run marker missing')
ns={'__file__':str(V69),'__name__':'oleander_v71_full_xz_boundary_split'}
exec(compile(text.split(marker,1)[0],str(V69),'exec'),ns)

v=ns['v'];core=ns['core'];runtime=ns['runtime'];base_v69_build=core['build_visual_hull']
BAND=ns['BAND'];boundary_counts=ns['boundary_counts'];folds=ns['folds']
REV='V71_DERIVED_REAR_APERTURE_FULL_XZ_BOUNDARY_SPLIT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_FULL_XZ_BOUNDARY_SPLIT_V71'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE__DERIVED_XZ_BOUNDARY_REFINEMENT_ONLY'
v.REFERENCE_CONTRACT['primary_body_source_revision_locked']='V59_SPARSE_FRONT_HOOD_FENDER_RELATION'

STATS={}

def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def bbox_overlap_segment(poly,a,b,eps=1e-6):
    xs=[p[0] for p in poly];zs=[p[1] for p in poly]
    return not (max(xs)<min(a[0],b[0])-eps or min(xs)>max(a[0],b[0])+eps or max(zs)<min(a[1],b[1])-eps or min(zs)>max(a[1],b[1])+eps)
def true_straddle(poly,a,b,tol=1e-7):
    if not bbox_overlap_segment(poly,a,b):return False
    s=[orient(a,b,p) for p in poly]
    return min(s)<-tol and max(s)>tol

def edge_straddle_counts(obj):
    edges=[(BAND[i],BAND[(i+1)%len(BAND)]) for i in range(len(BAND))]
    counts={f'EDGE_{i}':0 for i in range(4)};unique=set();samples=[];mw=obj.matrix_world
    for p in obj.data.polygons:
        xz=[(float((mw@obj.data.vertices[i].co).x),float((mw@obj.data.vertices[i].co).z)) for i in p.vertices]
        hits=[]
        for idx,(a,b) in enumerate(edges):
            if true_straddle(xz,a,b):counts[f'EDGE_{idx}']+=1;hits.append(idx)
        if hits:
            unique.add(int(p.index))
            if len(samples)<100:samples.append({'polygon_index':int(p.index),'edge_hits':hits,'vertices_xz':xz})
    return counts,len(unique),samples

def world_dims(obj):
    pts=[obj.matrix_world@vv.co for vv in obj.data.vertices]
    return [max(float(p[i]) for p in pts)-min(float(p[i]) for p in pts) for i in range(3)]
def nonmanifold_count(obj):
    counts={}
    for p in obj.data.polygons:
        for e in p.edge_keys:counts[tuple(sorted(e))]=counts.get(tuple(sorted(e)),0)+1
    return sum(1 for n in counts.values() if n!=2)
def select_edge_geom(bm,a,b):
    faces=[]
    for f in bm.faces:
        xz=[(float(vv.co.x),float(vv.co.z)) for vv in f.verts]
        if true_straddle(xz,a,b):faces.append(f)
    es={e for f in faces for e in f.edges};vs={vv for f in faces for vv in f.verts}
    return faces,list(vs|es|set(faces))
def split_xz_edges(obj):
    before_edge,before_unique,before_samples=edge_straddle_counts(obj)
    STATS['before']={'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold_count(obj),'lateral_boundary_counts':boundary_counts(obj),'xz_edge_straddles':before_edge,'xz_unique_straddling_faces':before_unique}
    bm=bmesh.new();bm.from_mesh(obj.data);ops=[]
    for idx in range(4):
        a=BAND[idx];b=BAND[(idx+1)%4];faces,geom=select_edge_geom(bm,a,b);dx=b[0]-a[0];dz=b[1]-a[1]
        pre=(len(bm.verts),len(bm.edges),len(bm.faces))
        if faces:
            bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-7,plane_co=Vector((a[0],0.0,a[1])),plane_no=Vector((dz,0.0,-dx)).normalized(),clear_inner=False,clear_outer=False)
        post=(len(bm.verts),len(bm.edges),len(bm.faces));ops.append({'edge':idx,'selected_true_straddling_faces':len(faces),'before':pre,'after':post})
    bm.normal_update();bm.to_mesh(obj.data);bm.free();obj.data.update()
    after_edge,after_unique,after_samples=edge_straddle_counts(obj)
    STATS['after']={'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold_count(obj),'lateral_boundary_counts':boundary_counts(obj),'xz_edge_straddles':after_edge,'xz_unique_straddling_faces':after_unique}
    STATS['operations']=ops;STATS['before_samples']=before_samples;STATS['after_samples']=after_samples
    obj['OLEANDER_DERIVED_FULL_XZ_BOUNDARY_REFINEMENT']=REV;obj['OLEANDER_SOURCE_MUTATED']=False
    return obj

def build71(name,bodymat):
    obj=base_v69_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':split_xz_edges(obj)
    return obj
core['build_visual_hull']=build71

def emit(out):
    b=STATS['before'];a=STATS['after'];dimerr=[abs(a['dims'][i]-b['dims'][i]) for i in range(3)]
    shape_ok=max(dimerr)<=1e-6 and a['folds']==b['folds'] and a['nonmanifold_edges']==b['nonmanifold_edges']
    lateral_ok=a['lateral_boundary_counts']['REAR_LATERAL_BOUNDARY_STRADDLE']==0
    xz_ok=a['xz_unique_straddling_faces']==0
    refined=a['faces']>=b['faces'] and a['vertices']>=b['vertices']
    result='PASS_COMPLETE_REAR_BOUNDARY_REFINEMENT' if shape_ok and lateral_ok and xz_ok and refined else 'FAIL_COMPLETE_REAR_BOUNDARY_REFINEMENT'
    d={'schema':'oleander.3d.full-semantic-boundary-refinement-receipt.v1','candidate_revision':REV,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','source_mutated':False,
       'host':'DERIVED_911_9922_BODY','edit_scope':'REAR_APERTURE_XZ_BOUNDARY_LOCAL_DERIVED_TOPOLOGY_ONLY','before':b,'after':a,'dimension_abs_error_m':dimerr,
       'operations':STATS['operations'],'shape_preservation_gate':'PASS' if shape_ok else 'FAIL','lateral_boundary_ready':lateral_ok,'xz_boundary_ready':xz_ok,
       'boundary_refinement_result':result,'next_route':'DESTRUCTIVE_PREFLIGHT_CAN_NOW_EVALUATE_COMPLETE_REAR_OPENING_LOOP' if result=='PASS_COMPLETE_REAR_BOUNDARY_REFINEMENT' else 'DO_NOT_DELETE__RECLASSIFY_REMAINING_BOUNDARY_FAILURE',
       'does_not_prove':['aperture size correctness','manufacturer boundary','aperture deletion success','reference fidelity','Class-A continuity','Design KEEP']}
    Path(out,'V71_FULL_REAR_BOUNDARY_REFINEMENT_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,indent=2));return d

def run71():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    ns['emit'](out);emit(out);raise SystemExit(code)
run71()
