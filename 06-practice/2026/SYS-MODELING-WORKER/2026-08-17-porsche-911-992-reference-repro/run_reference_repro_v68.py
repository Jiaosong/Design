#!/usr/bin/env python3
"""V68 — boundary-aware Derived topology refinement on V59 LKG.

V67 found 56 evaluated host faces straddling the declared rear-glass lateral boundary. This means the
V59 evaluated mesh is sufficiently sampled for primary-form diagnostics but under-resolved for semantic
aperture ownership. V68 does NOT add Source controls and does NOT change the primary shape.

It locally bisects only the Derived display host inside the rear-glass XZ band along the positive/negative
rear-glass lateral boundary planes. The untouched V59 evaluated diagnostic carrier remains the primary-body
evidence carrier. After splitting, V68 re-audits boundary straddles and host/surface preservation.

`SURFACE_SAMPLING_SUFFICIENT != SEMANTIC_BOUNDARY_TOPOLOGY_SUFFICIENT`.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy, bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V59=HERE/'run_reference_repro_v59.py'
text=V59.read_text(encoding='utf-8'); marker='\nrun59()\n'
if marker not in text: raise SystemExit('V59 run marker missing')
ns={'__file__':str(V59),'__name__':'oleander_v68_boundary_refinement'}
exec(compile(text.split(marker,1)[0],str(V59),'exec'),ns)

v=ns['v'];core=ns['core'];runtime=ns['runtime'];base_v59_build=core['build_visual_hull']
folds=ns['folds'];edge_p95=ns['edge_p95']
REV='V68_DERIVED_REAR_GLASS_BOUNDARY_REFINEMENT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_DERIVED_BOUNDARY_REFINEMENT_V68'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE__DERIVED_BOUNDARY_TOPOLOGY_REFINEMENT_ONLY'
v.REFERENCE_CONTRACT['primary_body_source_revision_locked']='V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
v.REFERENCE_CONTRACT['boundary_refinement_reason']='V67_56_CANONICAL_BOUNDARY_STRADDLING_FACES'

REAR_TOP=(-.405,.455,1.220)
REAR_BOTTOM=(-1.145,.535,.970)
BAND=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]
M=(REAR_BOTTOM[1]-REAR_TOP[1])/(REAR_BOTTOM[0]-REAR_TOP[0])

STATS={}


def point_in_poly(p,poly):
    x,z=p;inside=False;j=len(poly)-1
    for i in range(len(poly)):
        xi,zi=poly[i];xj,zj=poly[j]
        if ((zi>z)!=(zj>z)) and (x < (xj-xi)*(z-zi)/((zj-zi) or 1e-12)+xi):inside=not inside
        j=i
    return inside

def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def seg_intersect(a,b,c,d):
    eps=1e-10;o1=orient(a,b,c);o2=orient(a,b,d);o3=orient(c,d,a);o4=orient(c,d,b)
    return ((o1>eps and o2<-eps) or (o1<-eps and o2>eps)) and ((o3>eps and o4<-eps) or (o3<-eps and o4>eps))
def polygons_overlap(a,b):
    if any(point_in_poly(p,b) for p in a):return True
    if any(point_in_poly(p,a) for p in b):return True
    for i in range(len(a)):
        for j in range(len(b)):
            if seg_intersect(a[i],a[(i+1)%len(a)],b[j],b[(j+1)%len(b)]):return True
    return False

def rear_half_width(x):
    x=float(x);x0=REAR_TOP[0];x1=REAR_BOTTOM[0]
    if x>=x0:return REAR_TOP[1]
    if x<=x1:return REAR_BOTTOM[1]
    t=(x-x0)/(x1-x0);return REAR_TOP[1]*(1-t)+REAR_BOTTOM[1]*t

def world_dims(obj):
    pts=[obj.matrix_world@vert.co for vert in obj.data.vertices]
    return [max(float(p[i]) for p in pts)-min(float(p[i]) for p in pts) for i in range(3)]

def selected_geom_for_band(bm):
    faces=[]
    for f in bm.faces:
        xz=[(float(vv.co.x),float(vv.co.z)) for vv in f.verts]
        if polygons_overlap(xz,BAND):faces.append(f)
    edges={e for f in faces for e in f.edges};verts={vv for f in faces for vv in f.verts}
    return faces,list(verts|edges|set(faces))

def straddle_counts_mesh(obj,tol=1e-5):
    counts={'REAR_INTERIOR_ONLY':0,'REAR_LATERAL_BOUNDARY_STRADDLE':0,'OUTSIDE_REAR_LATERAL_BOUNDARY':0}
    mw=obj.matrix_world
    for p in obj.data.polygons:
        pts=[mw@obj.data.vertices[i].co for i in p.vertices];xz=[(float(q.x),float(q.z)) for q in pts]
        if not polygons_overlap(xz,BAND):continue
        c=mw@p.center;limit=rear_half_width(float(c.x));ay=[abs(float(q.y)) for q in pts];amin=min(ay);amax=max(ay)
        if amax<=limit+tol:state='REAR_INTERIOR_ONLY'
        elif amin>=limit-tol:state='OUTSIDE_REAR_LATERAL_BOUNDARY'
        else:state='REAR_LATERAL_BOUNDARY_STRADDLE'
        counts[state]+=1
    return counts

def refine_boundary(obj):
    before_v=len(obj.data.vertices);before_e=len(obj.data.edges);before_f=len(obj.data.polygons);before_dims=world_dims(obj)
    before_straddle=straddle_counts_mesh(obj)
    bm=bmesh.new();bm.from_mesh(obj.data)
    operations=[]
    planes=[
      ('POSITIVE',Vector((REAR_TOP[0],REAR_TOP[1],0.0)),Vector((-M,1.0,0.0))),
      ('NEGATIVE',Vector((REAR_TOP[0],-REAR_TOP[1],0.0)),Vector((M,1.0,0.0)))
    ]
    for label,co,no in planes:
        faces,geom=selected_geom_for_band(bm)
        pre=(len(bm.verts),len(bm.edges),len(bm.faces))
        res=bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-6,plane_co=co,plane_no=no.normalized(),clear_inner=False,clear_outer=False)
        post=(len(bm.verts),len(bm.edges),len(bm.faces))
        operations.append({'plane':label,'selected_faces':len(faces),'before':pre,'after':post,'cut_geom_count':len(res.get('geom_cut',[]))})
    bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(obj.data);bm.free();obj.data.update()
    after_v=len(obj.data.vertices);after_e=len(obj.data.edges);after_f=len(obj.data.polygons);after_dims=world_dims(obj)
    after_straddle=straddle_counts_mesh(obj)
    dim_error=[abs(after_dims[i]-before_dims[i]) for i in range(3)]
    STATS.update({
      'before_vertices':before_v,'before_edges':before_e,'before_faces':before_f,'before_dims':before_dims,
      'after_vertices':after_v,'after_edges':after_e,'after_faces':after_f,'after_dims':after_dims,
      'dimension_abs_error_m':dim_error,'operations':operations,
      'before_boundary_counts':before_straddle,'after_boundary_counts':after_straddle
    })
    obj['OLEANDER_DERIVED_BOUNDARY_REFINEMENT']=REV
    obj['OLEANDER_SOURCE_REVISION_LOCKED']='V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
    obj['OLEANDER_SOURCE_MUTATED']=False
    return obj

def build68(name,bodymat):
    obj=base_v59_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':refine_boundary(obj)
    return obj
core['build_visual_hull']=build68


def receipt(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY')
    if obj is None:raise SystemExit('FAIL_V68_HOST_MISSING')
    fc=folds(obj);p95=edge_p95(obj)
    before_s=STATS['before_boundary_counts']['REAR_LATERAL_BOUNDARY_STRADDLE'];after_s=STATS['after_boundary_counts']['REAR_LATERAL_BOUNDARY_STRADDLE']
    dims_ok=max(STATS['dimension_abs_error_m'])<=1e-6
    topology_refined=STATS['after_faces']>STATS['before_faces'] and STATS['after_vertices']>STATS['before_vertices']
    split_effective=after_s<before_s
    state='PASS_DERIVED_BOUNDARY_REFINEMENT' if dims_ok and topology_refined and split_effective and fc==0 else 'FAIL_DERIVED_BOUNDARY_REFINEMENT'
    d={
      'schema':'oleander.3d.derived-semantic-boundary-refinement-receipt.v1','candidate_revision':REV,
      'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','source_mutated':False,
      'host':'DERIVED_911_9922_BODY','host_state_class':'DERIVED_EXECUTION',
      'edit_scope':'REAR_GLASS_LATERAL_BOUNDARY_LOCAL_DERIVED_TOPOLOGY_ONLY',
      'before':{'vertices':STATS['before_vertices'],'edges':STATS['before_edges'],'faces':STATS['before_faces'],'dimensions_m':STATS['before_dims'],'boundary_counts':STATS['before_boundary_counts']},
      'after':{'vertices':STATS['after_vertices'],'edges':STATS['after_edges'],'faces':STATS['after_faces'],'dimensions_m':STATS['after_dims'],'boundary_counts':STATS['after_boundary_counts']},
      'dimension_abs_error_m':STATS['dimension_abs_error_m'],'bisect_operations':STATS['operations'],
      'adjacent_normal_fold_count':fc,'evaluated_edge_p95_m':p95,
      'shape_preservation_gate':'PASS' if dims_ok and fc==0 else 'FAIL',
      'boundary_straddle_before':before_s,'boundary_straddle_after':after_s,
      'boundary_refinement_result':state,
      'next_route':'RERUN_EXCLUSIVE_OWNER_PREFLIGHT' if state=='PASS_DERIVED_BOUNDARY_REFINEMENT' and after_s==0 else 'REFINE_BOUNDARY_PARTITION_METHOD_BEFORE_DESTRUCTIVE_EDIT',
      'does_not_prove':['Source improvement','reference fidelity','Class-A continuity','aperture closure','production topology','Design KEEP']
    }
    Path(out,'V68_DERIVED_BOUNDARY_REFINEMENT_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(d,indent=2));return d

def run68():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    receipt(out);raise SystemExit(code)

run68()
