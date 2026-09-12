#!/usr/bin/env python3
"""V73 — diagnostic-only audit of the two residual V72 EDGE_2 straddling faces.

V72 bounded refinement reduced complete rear-aperture XZ straddles 118 -> 34 -> 4 -> 2, then correctly
stopped when the fourth cycle selected the remaining two faces but produced no material reduction. V73 does
not delete aperture faces and does not modify Source. It records exact signed distances of the residual faces
to EDGE_2 and runs tolerance A/B tests only on disposable Derived diagnostic mesh copies.

Goal: distinguish numerical/operator tolerance stagnation from a representation/topology failure.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

HERE=Path(__file__).resolve().parent
V72=HERE/'run_reference_repro_v72.py'
text=V72.read_text(encoding='utf-8');marker='\nrun72()\n'
if marker not in text:raise SystemExit('V72 run marker missing')
ns={'__file__':str(V72),'__name__':'oleander_v73_residual_boundary_diagnostic'}
exec(compile(text.split(marker,1)[0],str(V72),'exec'),ns)

v=ns['v'];runtime=ns['runtime'];BAND=ns['BAND'];select_edge_geom=ns['select_edge_geom'];edge_straddle_counts=ns['edge_straddle_counts']
world_dims=ns['world_dims'];folds=ns['folds'];nonmanifold_count=ns['nonmanifold_count']
REV='V73_RESIDUAL_EDGE2_SPLIT_STAGNATION_DIAGNOSTIC'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_RESIDUAL_BOUNDARY_DIAGNOSTIC_V73'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_edit_scope']='NONE_DIAGNOSTIC_ONLY_ON_V72_DERIVED_RESULT'

EDGE_ID=2;A=BAND[EDGE_ID];B=BAND[(EDGE_ID+1)%len(BAND)]

def orient(p):return (B[0]-A[0])*(p[1]-A[1])-(B[1]-A[1])*(p[0]-A[0])
def bbox_overlap(poly,eps=1e-6):
    xs=[p[0] for p in poly];zs=[p[1] for p in poly]
    return not (max(xs)<min(A[0],B[0])-eps or min(xs)>max(A[0],B[0])+eps or max(zs)<min(A[1],B[1])-eps or min(zs)>max(A[1],B[1])+eps)
def true_straddle(poly,tol=1e-7):
    if not bbox_overlap(poly):return False
    s=[orient(p) for p in poly]
    return min(s)<-tol and max(s)>tol

def snapshot(obj):
    ec,u,_=edge_straddle_counts(obj)
    return {'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold_count(obj),'edge_straddles':ec,'unique_straddles':u}

def residual_faces(obj):
    mw=obj.matrix_world;out=[]
    for p in obj.data.polygons:
        pts=[mw@obj.data.vertices[i].co for i in p.vertices];xz=[(float(q.x),float(q.z)) for q in pts]
        if not true_straddle(xz):continue
        signed=[orient(q) for q in xz]
        out.append({
          'polygon_index':int(p.index),'vertex_count':len(p.vertices),
          'vertices_world':[[float(q.x),float(q.y),float(q.z)] for q in pts],
          'signed_edge2_orient':signed,'signed_min':min(signed),'signed_max':max(signed),
          'min_abs_signed':min(abs(x) for x in signed),'max_abs_signed':max(abs(x) for x in signed)
        })
    return out

def tolerance_trial(source_obj,dist):
    me=source_obj.data.copy();tmp=bpy.data.objects.new('DIAG_V73_TOL_'+str(dist).replace('.','_'),me);bpy.context.collection.objects.link(tmp)
    tmp.hide_render=True;tmp['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY'
    before=snapshot(tmp)
    bm=bmesh.new();bm.from_mesh(tmp.data);faces,geom=select_edge_geom(bm,A,B);dx=B[0]-A[0];dz=B[1]-A[1]
    pre=(len(bm.verts),len(bm.edges),len(bm.faces));res=bmesh.ops.bisect_plane(
        bm,geom=geom,dist=dist,plane_co=Vector((A[0],0.0,A[1])),plane_no=Vector((dz,0.0,-dx)).normalized(),
        clear_inner=False,clear_outer=False)
    post=(len(bm.verts),len(bm.edges),len(bm.faces));bm.normal_update();bm.to_mesh(tmp.data);bm.free();tmp.data.update()
    after=snapshot(tmp);record={
      'dist':dist,'selected_faces':len(faces),'pre_bmesh':pre,'post_bmesh':post,'geom_cut_count':len(res.get('geom_cut',[])),
      'before':before,'after':after,'material_reduction':after['edge_straddles'].get('EDGE_2',0)<before['edge_straddles'].get('EDGE_2',0),
      'protected_invariants':'PASS' if (max(abs(after['dims'][i]-before['dims'][i]) for i in range(3))<=1e-6 and after['folds']==before['folds'] and after['nonmanifold_edges']==before['nonmanifold_edges']) else 'FAIL'
    }
    bpy.data.objects.remove(tmp,do_unlink=True);bpy.data.meshes.remove(me)
    return record

def diagnostic(out):
    obj=bpy.data.objects.get('DERIVED_911_9922_BODY')
    if obj is None:raise SystemExit('FAIL_V73_HOST_MISSING')
    host_before=snapshot(obj);faces=residual_faces(obj)
    trials=[tolerance_trial(obj,d) for d in (1e-7,5e-8,1e-8,1e-9,0.0)]
    host_after=snapshot(obj)
    successful=[t for t in trials if t['material_reduction'] and t['protected_invariants']=='PASS']
    if successful:
        best=min(successful,key=lambda t:(t['after']['edge_straddles'].get('EDGE_2',999),t['dist']))
        result='TOLERANCE_SENSITIVE_OPERATOR_CAN_PROGRESS_ON_DIAGNOSTIC_COPY'
        route='V74_APPLY_SMALLEST_EVIDENCED_TOLERANCE_TO_RESIDUAL_DERIVED_FACES_ONLY'
    else:
        best=None;result='OPERATOR_STAGNATION_NOT_RESOLVED_BY_TOLERANCE_AB';route='RECLASSIFY_RESIDUAL_TOPOLOGY_OR_BOUNDARY_REPRESENTATION__DO_NOT_DELETE'
    d={
      'schema':'oleander.3d.residual-boundary-stagnation-diagnostic.v1','candidate_revision':REV,
      'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','source_mutated':False,
      'host':'DERIVED_911_9922_BODY','host_before_diagnostic':host_before,'host_after_diagnostic':host_after,
      'host_unchanged_by_diagnostic':host_before==host_after,'edge_id':EDGE_ID,'edge':{'a':A,'b':B},
      'residual_face_count':len(faces),'residual_faces':faces,'diagnostic_copy_tolerance_trials':trials,
      'diagnostic_result':result,'best_trial':best,'next_route':route,
      'does_not_prove':['production tolerance','aperture deletion success','aperture closure','reference fidelity','Class-A continuity','Design KEEP']
    }
    Path(out,'V73_RESIDUAL_BOUNDARY_STAGNATION_DIAGNOSTIC.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,indent=2));return d

def run73():
    a=v.m.parse_args();out=Path(a.out).resolve();code=0
    try:runtime['run30']()
    except SystemExit as e:code=e.code if isinstance(e.code,int) else 0
    diagnostic(out);raise SystemExit(code)
run73()
