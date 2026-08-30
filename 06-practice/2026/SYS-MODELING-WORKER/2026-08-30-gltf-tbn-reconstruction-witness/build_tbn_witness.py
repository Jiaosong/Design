#!/usr/bin/env python3
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

STD='TBN_STANDARD'; MIR='TBN_MIRRORED'; MAT='TBN_WITNESS_MAT'; IMG='TBN_WITNESS_NORMAL'
M=((1.0,0.0,0.0),(0.0,0.0,1.0),(0.0,-1.0,0.0))


def cli():
    a=sys.argv; a=a[a.index('--')+1:] if '--' in a else []
    p=argparse.ArgumentParser(); p.add_argument('--out',required=True); return p.parse_args(a)

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''): h.update(c)
    return h.hexdigest()

def arr(v): return [float(x) for x in v]
def mapv(v): return Vector((v.x,v.z,-v.y))
def norm(v):
    q=Vector(v); q.normalize(); return q

def avg_vec(vs):
    q=Vector((0,0,0))
    for v in vs: q+=Vector(v)
    q/=len(vs); q.normalize(); return q

def make_basis():
    t=norm((0.73,0.31,0.608))
    n0=Vector((-0.27,0.88,0.39))
    n=norm(n0-t*t.dot(n0))
    b=norm(n.cross(t))
    # T x B must point along N for face winding below.
    if t.cross(b).dot(n)<0: b=-b
    return t,b,n

def create_quad(name,center,t,b,mirror=False):
    ht=0.72; hb=0.52; c=Vector(center)
    vs=[c-t*ht-b*hb,c+t*ht-b*hb,c+t*ht+b*hb,c-t*ht+b*hb]
    mesh=bpy.data.meshes.new(name+'_MESH'); mesh.from_pydata([arr(v) for v in vs],[],[(0,1,2,3)]); mesh.update()
    for p in mesh.polygons: p.use_smooth=True
    uv=mesh.uv_layers.new(name='UVMap')
    coords=[(0,0),(1,0),(1,1),(0,1)] if not mirror else [(1,0),(0,0),(0,1),(1,1)]
    for li,co in zip(mesh.polygons[0].loop_indices,coords): uv.data[li].uv=co
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o); return o

def make_normal_image(out,q):
    # q is normalized tangent-space vector with non-zero T/B/N components.
    rgb=[0.5*(q[i]+1.0) for i in range(3)]
    im=bpy.data.images.new('TBN_GEN',width=8,height=8,alpha=False,float_buffer=False); im.colorspace_settings.name='Non-Color'
    px=[]
    for _ in range(64): px.extend((rgb[0],rgb[1],rgb[2],1.0))
    im.pixels=px
    p=out/'TBN_NORMAL.png'; im.filepath_raw=str(p); im.file_format='PNG'; im.save()
    ext=bpy.data.images.load(str(p),check_existing=False); ext.name=IMG; ext.colorspace_settings.name='Non-Color'
    return ext,p,rgb

def make_mat(img):
    m=bpy.data.materials.new(MAT); m.use_nodes=True; nt=m.node_tree; bs=nt.nodes.get('Principled BSDF')
    bs.inputs['Base Color'].default_value=(0.48,0.48,0.48,1); bs.inputs['Roughness'].default_value=0.4
    tx=nt.nodes.new('ShaderNodeTexImage'); tx.name='NORMAL_TEX'; tx.image=img
    nm=nt.nodes.new('ShaderNodeNormalMap'); nm.name='NORMAL_MAP'; nm.space='TANGENT'
    nt.links.new(tx.outputs['Color'],nm.inputs['Color']); nt.links.new(nm.outputs['Normal'],bs.inputs['Normal']); return m

def loop_contract(o,q):
    me=o.data; me.calc_tangents(uvmap='UVMap')
    ts=[Vector(me.loops[i].tangent) for i in range(len(me.loops))]
    ns=[Vector(me.loops[i].normal) for i in range(len(me.loops))]
    signs=[-1 if me.loops[i].bitangent_sign<0 else 1 for i in range(len(me.loops))]
    if len(set(signs))!=1: raise RuntimeError(f'mixed sign in controlled witness {o.name}: {signs}')
    t=avg_vec(ts); n=avg_vec(ns); w=signs[0]; b=norm(n.cross(t))*w
    p=norm(t*q.x+b*q.y+n*q.z)
    mt=norm(mapv(t)); mn=norm(mapv(n)); mp=norm(mapv(p)); mb=norm(mn.cross(mt))*w
    mp_from_mapped_tbn=norm(mt*q.x+mb*q.y+mn*q.z)
    return {
      'loop_count':len(me.loops),'sign':w,'tangent':arr(t),'normal':arr(n),'bitangent':arr(b),
      'perturbed_normal_source':arr(p),
      'expected_target':{'tangent':arr(mt),'normal':arr(mn),'sign':w,'bitangent':arr(mb),'perturbed_normal_mapped_source':arr(mp),'perturbed_normal_from_mapped_tbn':arr(mp_from_mapped_tbn)}
    }

def main():
    a=cli(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True); bpy.ops.wm.read_factory_settings(use_empty=True)
    t,b,n=make_basis(); std=create_quad(STD,(-0.95,0,0),t,b,False); mir=create_quad(MIR,(0.95,0,0),t,b,True)
    q=norm((0.36,0.48,0.80)); img,png,rgb=make_normal_image(out,q); mat=make_mat(img); std.data.materials.append(mat); mir.data.materials.append(mat)
    cs=loop_contract(std,q); cm=loop_contract(mir,q)
    if cs['sign']==cm['sign']: raise RuntimeError('mirrored UV did not flip handedness')
    blend=out/'TBN_RECONSTRUCTION_WITNESS.blend'; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.object.select_all(action='DESELECT'); std.select_set(True); mir.select_set(True); bpy.context.view_layer.objects.active=std
    glb=out/'TBN_RECONSTRUCTION_WITNESS.glb'; bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_materials='EXPORT',export_tangents=True)
    rec={
      'schema':'oleander.3d.gltf-tbn-reconstruction-source.v1','blender_version':bpy.app.version_string,
      'basis_seed':{'geometric_T':arr(t),'geometric_B':arr(b),'geometric_N':arr(n)},
      'coordinate_transform':'(x,y,z)->(x,z,-y)','transform_matrix_rows':[list(r) for r in M],'transform_determinant':1,
      'tangent_space_sample':arr(q),'encoded_normal_rgb':rgb,
      'normal_texture':png.name,'normal_texture_sha256':sha(png),
      'native_master':blend.name,'asset':glb.name,'asset_bytes':glb.stat().st_size,'asset_sha256':sha(glb),
      'objects':{STD:cs,MIR:cm},
      'evidence_class':'NATIVE_TBN_RECONSTRUCTION_PENDING_TARGET_RUNTIME',
      'holds':['Three numeric TBN reconstruction','embedded texture pixel readback','pixel shader parity','negative scale','triangulation change','Design KEEP']
    }
    (out/'SOURCE_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n'); print(json.dumps(rec,indent=2))
if __name__=='__main__': main()
