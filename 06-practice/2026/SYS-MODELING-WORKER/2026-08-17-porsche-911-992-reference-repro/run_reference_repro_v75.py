#!/usr/bin/env python3
"""V75 — residual boundary diagnostic from a reopened standalone V72 .blend.

V74 proved stacked exec composition is not deterministic for this benchmark: standalone V72 and a composed
V72 invocation shared Source identity, bounds and residual count but differed materially in topology/folds.
V75 therefore does not import any prior Vxx script. The workflow first executes V72 standalone, persists its
native .blend, then reopens that exact .blend and runs this diagnostic against the scene state.

The authoritative input for this diagnostic is the reopened Derived scene plus the V72 receipt/hash witness.
The original host is never mutated; tolerance A/B runs only on disposable mesh copies.
"""
from __future__ import annotations
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy,bmesh
from mathutils import Vector

BAND=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]
EDGE_ID=2;A=BAND[EDGE_ID];B=BAND[(EDGE_ID+1)%len(BAND)]

def args():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--parent-receipt',required=True)
    argv=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    return p.parse_args(argv)
def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def orient(p):return (B[0]-A[0])*(p[1]-A[1])-(B[1]-A[1])*(p[0]-A[0])
def bbox_overlap(poly,eps=1e-6):
    xs=[p[0] for p in poly];zs=[p[1] for p in poly]
    return not (max(xs)<min(A[0],B[0])-eps or min(xs)>max(A[0],B[0])+eps or max(zs)<min(A[1],B[1])-eps or min(zs)>max(A[1],B[1])+eps)
def true_straddle(poly,tol=1e-7):
    if not bbox_overlap(poly):return False
    s=[orient(p) for p in poly];return min(s)<-tol and max(s)>tol
def world_dims(obj):
    pts=[obj.matrix_world@v.co for v in obj.data.vertices]
    return [max(float(p[i]) for p in pts)-min(float(p[i]) for p in pts) for i in range(3)]
def folds(obj):
    ef={};n=0
    for p in obj.data.polygons:
        for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
    for fs in ef.values():
        if len(fs)==2 and float(obj.data.polygons[fs[0]].normal.dot(obj.data.polygons[fs[1]].normal))<-.15:n+=1
    return n
def nonmanifold(obj):
    ef={}
    for p in obj.data.polygons:
        for e in p.edge_keys:ef[tuple(sorted(e))]=ef.get(tuple(sorted(e)),0)+1
    return sum(1 for n in ef.values() if n!=2)
def edge2_count(obj):
    mw=obj.matrix_world;n=0
    for p in obj.data.polygons:
        xz=[(float((mw@obj.data.vertices[i].co).x),float((mw@obj.data.vertices[i].co).z)) for i in p.vertices]
        if true_straddle(xz):n+=1
    return n
def snapshot(obj):
    return {'vertices':len(obj.data.vertices),'edges':len(obj.data.edges),'faces':len(obj.data.polygons),'dims':world_dims(obj),'folds':folds(obj),'nonmanifold_edges':nonmanifold(obj),'edge2_straddles':edge2_count(obj)}
def residual_faces(obj):
    mw=obj.matrix_world;out=[]
    for p in obj.data.polygons:
        pts=[mw@obj.data.vertices[i].co for i in p.vertices];xz=[(float(q.x),float(q.z)) for q in pts]
        if not true_straddle(xz):continue
        signed=[orient(q) for q in xz]
        out.append({'polygon_index':int(p.index),'vertex_count':len(p.vertices),'vertices_world':[[float(q.x),float(q.y),float(q.z)] for q in pts],'signed_edge2_orient':signed,'signed_min':min(signed),'signed_max':max(signed),'min_abs_signed':min(abs(x) for x in signed),'max_abs_signed':max(abs(x) for x in signed)})
    return out
def select_residual_geom(bm):
    faces=[]
    for f in bm.faces:
        poly=[(float(v.co.x),float(v.co.z)) for v in f.verts]
        if true_straddle(poly):faces.append(f)
    es={e for f in faces for e in f.edges};vs={v for f in faces for v in f.verts}
    return faces,list(vs|es|set(faces))
def trial(source,dist):
    me=source.data.copy();tmp=bpy.data.objects.new('DIAG_V75_'+str(dist).replace('.','_'),me);bpy.context.collection.objects.link(tmp);tmp.hide_render=True
    before=snapshot(tmp);bm=bmesh.new();bm.from_mesh(tmp.data);faces,geom=select_residual_geom(bm);dx=B[0]-A[0];dz=B[1]-A[1];pre=(len(bm.verts),len(bm.edges),len(bm.faces))
    res=bmesh.ops.bisect_plane(bm,geom=geom,dist=dist,plane_co=Vector((A[0],0.0,A[1])),plane_no=Vector((dz,0.0,-dx)).normalized(),clear_inner=False,clear_outer=False)
    post=(len(bm.verts),len(bm.edges),len(bm.faces));bm.normal_update();bm.to_mesh(tmp.data);bm.free();tmp.data.update();after=snapshot(tmp)
    rec={'dist':dist,'selected_faces':len(faces),'pre_bmesh':pre,'post_bmesh':post,'geom_cut_count':len(res.get('geom_cut',[])),'before':before,'after':after,'material_reduction':after['edge2_straddles']<before['edge2_straddles'],'protected_invariants':'PASS' if (max(abs(after['dims'][i]-before['dims'][i]) for i in range(3))<=1e-9 and after['folds']==before['folds'] and after['nonmanifold_edges']==before['nonmanifold_edges']) else 'FAIL'}
    bpy.data.objects.remove(tmp,do_unlink=True);bpy.data.meshes.remove(me);return rec

def main():
    a=args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);parent=Path(a.parent_receipt).resolve();pd=json.loads(parent.read_text())
    host=bpy.data.objects.get('DERIVED_911_9922_BODY')
    if host is None:raise SystemExit('FAIL_V75_HOST_MISSING')
    before=snapshot(host);expected=pd['global_after']
    witness_checks={
      'vertices':before['vertices']==expected['vertices'],'edges':before['edges']==expected['edges'],'faces':before['faces']==expected['faces'],
      'folds':before['folds']==expected['folds'],'nonmanifold':before['nonmanifold_edges']==expected['nonmanifold_edges'],
      'edge2_straddles':before['edge2_straddles']==expected['xz_edge_straddles']['EDGE_2'],
      'dims':max(abs(before['dims'][i]-expected['dims'][i]) for i in range(3))<=1e-9
    }
    if not all(witness_checks.values()):
        d={'schema':'oleander.3d.reopened-scene-diagnostic.v1','revision':'V75_REOPENED_V72_RESIDUAL_DIAGNOSTIC','scene_witness':'FAIL','witness_checks':witness_checks,'actual':before,'expected':expected,'does_not_prove':['operator conclusion','Design KEEP']}
        (out/'V75_REOPENED_V72_RESIDUAL_DIAGNOSTIC.json').write_text(json.dumps(d,indent=2)+'\n');raise SystemExit(9)
    residual=residual_faces(host);trials=[trial(host,d) for d in (1e-7,5e-8,1e-8,1e-9,0.0)];after=snapshot(host)
    successful=[t for t in trials if t['material_reduction'] and t['protected_invariants']=='PASS']
    result='TOLERANCE_SENSITIVE_OPERATOR_CAN_PROGRESS' if successful else 'OPERATOR_STAGNATION_CONFIRMED_ON_REOPENED_STANDALONE_SCENE'
    route='APPLY_SMALLEST_EVIDENCED_TOLERANCE_ON_DERIVED_HOST_ONLY' if successful else 'RECLASSIFY_RESIDUAL_TOPOLOGY_OR_BOUNDARY_OPERATOR__DO_NOT_DELETE'
    d={'schema':'oleander.3d.reopened-scene-diagnostic.v1','revision':'V75_REOPENED_V72_RESIDUAL_DIAGNOSTIC','input_blend':bpy.data.filepath,'input_blend_sha256':sha256(bpy.data.filepath),'parent_receipt':str(parent),'parent_receipt_sha256':sha256(parent),'scene_witness':'PASS_MATCHES_V72_RECEIPT','witness_checks':witness_checks,'source_revision_locked':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','host_before':before,'host_after':after,'host_unchanged_by_diagnostic':before==after,'residual_faces':residual,'tolerance_trials':trials,'diagnostic_result':result,'next_route':route,'does_not_prove':['production tolerance','aperture deletion success','aperture closure','reference fidelity','Class-A continuity','Design KEEP']}
    (out/'V75_REOPENED_V72_RESIDUAL_DIAGNOSTIC.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print(json.dumps(d,indent=2))
    raise SystemExit(0)
if __name__=='__main__':main()
