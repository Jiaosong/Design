#!/usr/bin/env python3
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector

POS='TBN_POS_SCALE'; NEG='TBN_NEG_SCALE'; IMG='NEG_SCALE_TBN_NORMAL'; MAT='NEG_SCALE_TBN_MAT'

def cli():
    a=sys.argv;a=a[a.index('--')+1:] if '--' in a else []
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);return p.parse_args(a)
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda:f.read(1<<20),b''):h.update(c)
    return h.hexdigest()
def arr(v):return [float(x) for x in v]
def norm(v):
    q=Vector(v);q.normalize();return q
def mapv(v):return Vector((v.x,v.z,-v.y))
def avg(vs):
    q=Vector((0,0,0))
    for v in vs:q+=Vector(v)
    q/=len(vs);q.normalize();return q

def basis():
    t=norm((0.73,0.31,0.608));n0=Vector((-0.27,0.88,0.39));n=norm(n0-t*t.dot(n0));b=norm(n.cross(t))
    if t.cross(b).dot(n)<0:b=-b
    return t,b,n

def quad(name,t,b):
    ht,hb=.72,.52;vs=[-t*ht-b*hb,t*ht-b*hb,t*ht+b*hb,-t*ht+b*hb]
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata([arr(v) for v in vs],[],[(0,1,2,3)]);me.update()
    for p in me.polygons:p.use_smooth=True
    uv=me.uv_layers.new(name='UVMap');coords=[(0,0),(1,0),(1,1),(0,1)]
    for li,co in zip(me.polygons[0].loop_indices,coords):uv.data[li].uv=co
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);return o

def normal_image(out,q):
    rgb=[.5*(q[i]+1) for i in range(3)];im=bpy.data.images.new('GEN',width=8,height=8,alpha=False,float_buffer=False);im.colorspace_settings.name='Non-Color';px=[]
    for _ in range(64):px.extend((*rgb,1.0))
    im.pixels=px;p=out/'NEG_SCALE_TBN_NORMAL.png';im.filepath_raw=str(p);im.file_format='PNG';im.save();ext=bpy.data.images.load(str(p),check_existing=False);ext.name=IMG;ext.colorspace_settings.name='Non-Color';return ext,p,rgb

def material(img):
    m=bpy.data.materials.new(MAT);m.use_nodes=True;nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.48,.48,.48,1);bs.inputs['Roughness'].default_value=.4
    tx=nt.nodes.new('ShaderNodeTexImage');tx.image=img;nm=nt.nodes.new('ShaderNodeNormalMap');nm.space='TANGENT';nt.links.new(tx.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs['Normal'],bs.inputs['Normal']);return m

def contract(o,q):
    me=o.data;me.calc_tangents(uvmap='UVMap');ts=[Vector(l.tangent) for l in me.loops];ns=[Vector(l.normal) for l in me.loops];signs=[-1 if l.bitangent_sign<0 else 1 for l in me.loops]
    if len(set(signs))!=1:raise RuntimeError((o.name,signs))
    t=avg(ts);n=avg(ns);w=signs[0];b=norm(n.cross(t))*w;p=norm(t*q.x+b*q.y+n*q.z)
    A=o.matrix_world.to_3x3();Nmat=A.inverted().transposed();wt=norm(A@t);wn=norm(Nmat@n);wb=norm(A@b);wp=norm(A@p)
    # Blender -> glTF/Three axis map has determinant +1, so it preserves handedness of the already-transformed world basis.
    return {'local':{'tangent':arr(t),'normal':arr(n),'bitangent':arr(b),'sign':w,'perturbed':arr(p)},'source_world':{'linear_determinant':float(A.determinant()),'tangent':arr(wt),'normal':arr(wn),'bitangent':arr(wb),'perturbed':arr(wp)},'expected_target_world':{'tangent':arr(norm(mapv(wt))),'normal':arr(norm(mapv(wn))),'bitangent':arr(norm(mapv(wb))),'perturbed':arr(norm(mapv(wp)))}}

def main():
    a=cli();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);t,b,n=basis();q=norm((.36,.48,.80));img,png,rgb=normal_image(out,q);mat=material(img)
    pos=quad(POS,t,b);neg=quad(NEG,t,b);pos.location=(-1.15,0,0);neg.location=(1.15,0,0);neg.scale=(-1,1,1);bpy.context.view_layer.update();pos.data.materials.append(mat);neg.data.materials.append(mat)
    cp=contract(pos,q);cn=contract(neg,q)
    if cp['source_world']['linear_determinant']<=0 or cn['source_world']['linear_determinant']>=0:raise RuntimeError('controlled determinant witness not established')
    blend=out/'NEGATIVE_SCALE_TBN_WITNESS.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));bpy.ops.object.select_all(action='DESELECT');pos.select_set(True);neg.select_set(True);bpy.context.view_layer.objects.active=pos
    glb=out/'NEGATIVE_SCALE_TBN_WITNESS.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_materials='EXPORT',export_tangents=True)
    rec={'schema':'oleander.3d.gltf-negative-scale-tbn-source.v1','blender_version':bpy.app.version_string,'tangent_space_sample':arr(q),'encoded_normal_rgb':rgb,'normal_texture':png.name,'normal_texture_sha256':sha(png),'asset':glb.name,'asset_bytes':glb.stat().st_size,'asset_sha256':sha(glb),'native_master':blend.name,'objects':{POS:cp,NEG:cn},'claim':'negative-scale transforms are not assumed tangent-safe; source world B/P are transformed independently and target runtime must reconstruct the same directions from exported tangent/normal/w semantics','evidence_class':'NATIVE_NEGATIVE_SCALE_TBN_PENDING_TARGET_RUNTIME','holds':['Three negative-scale TBN reconstruction','non-uniform negative scale','skinning','triangulation change','pixel shader parity','Design KEEP']}
    (out/'SOURCE_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
