#!/usr/bin/env python3
"""V69 — piecewise canonical Derived boundary split + signed per-vertex audit.

V68 proved a local Derived bisect can change topology without Source mutation, but its single infinite sloped
plane did not match the declared rear-glass boundary outside the glass X range, and its post-audit compared
all face vertices to a width evaluated only at the face centre. It also recalculated normals unnecessarily.

V69 repairs only the boundary operator/evidence semantics:
- piecewise lateral boundary: top constant width / linear glass span / bottom constant width;
- local band selection per boundary segment;
- no global face-normal recalc; preserve existing orientation and only update normals;
- straddle test uses each vertex's signed distance to the same piecewise boundary relation.

Primary Source remains V59 and is not densified.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V59=HERE/'run_reference_repro_v59.py'
text=V59.read_text(encoding='utf-8');marker='\nrun59()\n'
if marker not in text:raise SystemExit('V59 run marker missing')
ns={'__file__':str(V59),'__name__':'oleander_v69_piecewise_boundary_split'}
exec(compile(text.split(marker,1)[0],str(V59),'exec'),ns)

v=ns['v'];core=ns['core'];runtime=ns['runtime'];base_v59_build=core['build_visual_hull']
folds=ns['folds'];edge_p95=ns['edge_p95']
REV='V69_DERIVED_REAR_GLASS_PIECEWISE_BOUNDARY_SPLIT'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_PIECEWISE_BOUNDARY_SPLIT_V69'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE__DERIVED_BOUNDARY_TOPOLOGY_REFINEMENT_ONLY'
v.REFERENCE_CONTRACT['primary_body_source_revision_locked']='V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
v.REFERENCE_CONTRACT['supersedes_experiment']='V68_SINGLE_INFINITE_PLANE_FALSE_BOUNDARY_MODEL'

X_TOP=-.405;Y_TOP=.455;X_BOTTOM=-1.145;Y_BOTTOM=.535
BAND=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]
SLOPE=(Y_BOTTOM-Y_TOP)/(X_BOTTOM-X_TOP)
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
    x=float(x)
    if x>=X_TOP:return Y_TOP
    if x<=X_BOTTOM:return Y_BOTTOM
    t=(x-X_TOP)/(X_BOTTOM-X_TOP);return Y_TOP*(1-t)+Y_BOTTOM*t

def signed_owner_distance(x,y):return abs(float(y))-rear_half_width(float(x))
def world_dims(obj):
    pts=[obj.matrix_world@vv.co for vv in obj.data.vertices]
    return [max(float(p[i]) for p in pts)-min(float(p[i]) for p in pts) for i in range(3)]
def nonmanifold_count(obj):
    counts={}
    for p in obj.data.polygons:
        for e in p.edge_keys:counts[tuple(sorted(e))]=counts.get(tuple(sorted(e)),0)+1
    return sum(1 for n in counts.values() if n!=2)

def boundary_counts(obj,tol=1e-5):
    counts={'REAR_INTERIOR_ONLY':0,'REAR_LATERAL_BOUNDARY_STRADDLE':0,'OUTSIDE_REAR_LATERAL_BOUNDARY':0,'BOUNDARY_ONLY':0}
    mw=obj.matrix_world
    for p in obj.data.polygons:
        pts=[mw@obj.data.vertices[i].co for i in p.vertices];xz=[(float(q.x),float(q.z)) for q in pts]
        if not polygons_overlap(xz,BAND):continue
        signed=[signed_owner_distance(q.x,q.y) for q in pts];lo=min(signed);hi=max(signed)
        if abs(lo)<=tol and abs(hi)<=tol:state='BOUNDARY_ONLY'
        elif hi<=tol:state='REAR_INTERIOR_ONLY'
        elif lo>=-tol:state='OUTSIDE_REAR_LATERAL_BOUNDARY'
        else:state='REAR_LATERAL_BOUNDARY_STRADDLE'
        counts[state]+=1
    return counts

def select_segment_geom(bm,segment):
    faces=[]
    for f in bm.faces:
        xz=[(float(vv.co.x),float(vv.co.z)) for vv in f.verts]
        if not polygons_overlap(xz,BAND):continue
        xs=[float(vv.co.x) for vv in f.verts];xmin=min(xs);xmax=max(xs)
        if segment=='TOP' and xmax < X_TOP-1e-6:continue
        if segment=='MID' and (xmax < X_BOTTOM-1e-6 or xmin > X_TOP+1e-6):continue
        if segment=='BOTTOM' and xmin > X_BOTTOM+1e-6:continue
        faces.append(f)
    edges={e for f in faces for e in f.edges};verts={vv for f in faces for vv in f.verts}
    return faces,list(verts|edges|set(faces))

def split_host(obj):
    STATS['before']={'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold_count(obj),'boundary_counts':boundary_counts(obj)}
    bm=bmesh.new();bm.from_mesh(obj.data);operations=[]
    configs=[
      ('POS_TOP','TOP',Vector((X_TOP,Y_TOP,0)),Vector((0,1,0))),
      ('POS_MID','MID',Vector((X_TOP,Y_TOP,0)),Vector((-SLOPE,1,0))),
      ('POS_BOTTOM','BOTTOM',Vector((X_BOTTOM,Y_BOTTOM,0)),Vector((0,1,0))),
      ('NEG_TOP','TOP',Vector((X_TOP,-Y_TOP,0)),Vector((0,1,0))),
      ('NEG_MID','MID',Vector((X_TOP,-Y_TOP,0)),Vector((SLOPE,1,0))),
      ('NEG_BOTTOM','BOTTOM',Vector((X_BOTTOM,-Y_BOTTOM,0)),Vector((0,1,0)))
    ]
    for label,segment,co,no in configs:
        faces,geom=select_segment_geom(bm,segment);pre=(len(bm.verts),len(bm.edges),len(bm.faces))
        res=bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-7,plane_co=co,plane_no=no.normalized(),clear_inner=False,clear_outer=False)
        post=(len(bm.verts),len(bm.edges),len(bm.faces));operations.append({'id':label,'segment':segment,'selected_faces':len(faces),'before':pre,'after':post,'cut_geom_count':len(res.get('geom_cut',[]))})
    bm.normal_update();bm.to_mesh(obj.data);bm.free();obj.data.update()
    STATS['operations']=operations
    STATS['after']={'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold_count(obj),'boundary_counts':boundary_counts(obj)}
    obj['OLEANDER_DERIVED_BOUNDARY_REFINEMENT']=REV;obj['OLEANDER_SOURCE_MUTATED']=False
    return obj

def build69(name,bodymat):
    obj=base_v59_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':split_host(obj)
    return obj
core['build_visual_hull']=build69


def emit(out):
    b=STATS['before'];a=STATS['after'];dimerr=[abs(a['dims'][i]-b['dims'][i]) for i in range(3)]
    sb=b['boundary_counts']['REAR_LATERAL_BOUNDARY_STRADDLE'];sa=a['boundary_counts']['REAR_LATERAL_BOUNDARY_STRADDLE']
    topology_refined=a['vertices']>b['vertices'] and a['faces']>b['faces'];shape_ok=max(dimerr)<=1e-6 and a['folds']==b['folds'] and a['nonmanifold_edges']==b['nonmanifold_edges']
    effective=sa<sb
    result='PASS_DERIVED_BOUNDARY_REFINEMENT' if topology_refined and shape_ok and effective else 'FAIL_DERIVED_BOUNDARY_REFINEMENT'
    d={'schema':'oleander.3d.derived-semantic-boundary-refinement-receipt.v2','candidate_revision':REV,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','source_mutated':False,
       'boundary_model':'PIECEWISE_TOP_CONSTANT__MID_LINEAR__BOTTOM_CONSTANT','audit_method':'PER_VERTEX_SIGNED_DISTANCE_TO_SAME_BOUNDARY_RELATION',
       'before':b,'after':a,'dimension_abs_error_m':dimerr,'operations':STATS['operations'],'boundary_straddle_before':sb,'boundary_straddle_after':sa,
       'shape_preservation_gate':'PASS' if shape_ok else 'FAIL','boundary_refinement_result':result,
       'next_route':'RERUN_DESTRUCTIVE_PREFLIGHT_WITH_EXCLUSIVE_OWNER_PARTITION' if result=='PASS_DERIVED_BOUNDARY_REFINEMENT' and sa==0 else 'BOUNDARY_OPERATOR_STILL_INSUFFICIENT__DO_NOT_DELETE',
       'does_not_prove':['Source improvement','reference fidelity','Class-A continuity','aperture closure','production topology','Design KEEP']}
    Path(out,'V69_DERIVED_BOUNDARY_REFINEMENT_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,indent=2));return d

def run69():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    emit(out);raise SystemExit(code)
run69()
