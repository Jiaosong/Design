#!/usr/bin/env python3
import argparse,hashlib,json,sys
from pathlib import Path
import bpy
from mathutils import Vector

A='TRIANGULATION_A';B='TRIANGULATION_B';IMG='TRI_TBN_NORMAL';MAT='TRI_TBN_MAT'
UV=[(0,0),(1,0),(1,1),(0,1)]
VERTS=[(-.82,-.62,-.18),(.82,-.62,.12),(.82,.62,.48),(-.82,.62,-.28)]
FACES_A=[(0,1,2),(0,2,3)];FACES_B=[(0,1,3),(1,2,3)]

def cli():
 a=sys.argv;a=a[a.index('--')+1:] if '--' in a else [];p=argparse.ArgumentParser();p.add_argument('--out',required=True);return p.parse_args(a)
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for c in iter(lambda:f.read(1<<20),b''):h.update(c)
 return h.hexdigest()
def arr(v):return [float(x) for x in v]
def norm(v):q=Vector(v);q.normalize();return q
def mapv(v):return Vector((v.x,v.z,-v.y))
def avg(vs):
 q=Vector((0,0,0))
 for v in vs:q+=Vector(v)
 q/=len(vs);q.normalize();return q

def make(name,faces,x):
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(VERTS,[],faces);me.update()
 for p in me.polygons:p.use_smooth=True
 uv=me.uv_layers.new(name='UVMap')
 for poly in me.polygons:
  for li in poly.loop_indices:uv.data[li].uv=UV[me.loops[li].vertex_index]
 o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.location=(x,0,0);return o

def normal_image(out,q):
 rgb=[.5*(q[i]+1) for i in range(3)];im=bpy.data.images.new('GEN',width=8,height=8,alpha=False,float_buffer=False);im.colorspace_settings.name='Non-Color';px=[]
 for _ in range(64):px.extend((*rgb,1.0))
 im.pixels=px;p=out/'TRI_TBN_NORMAL.png';im.filepath_raw=str(p);im.file_format='PNG';im.save();ext=bpy.data.images.load(str(p),check_existing=False);ext.name=IMG;ext.colorspace_settings.name='Non-Color';return ext,p,rgb

def material(img):
 m=bpy.data.materials.new(MAT);m.use_nodes=True;nt=m.node_tree;bs=nt.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.48,.48,.48,1);bs.inputs['Roughness'].default_value=.4;tx=nt.nodes.new('ShaderNodeTexImage');tx.image=img;nm=nt.nodes.new('ShaderNodeNormalMap');nm.space='TANGENT';nt.links.new(tx.outputs['Color'],nm.inputs['Color']);nt.links.new(nm.outputs['Normal'],bs.inputs['Normal']);return m

def contract(o,q):
 me=o.data;me.calc_tangents(uvmap='UVMap');loops=[];ps=[]
 for l in me.loops:
  t=norm(l.tangent);n=norm(l.normal);w=-1 if l.bitangent_sign<0 else 1;b=norm(n.cross(t))*w;p=norm(t*q.x+b*q.y+n*q.z);loops.append({'vertex':l.vertex_index,'tangent':arr(t),'normal':arr(n),'w':w,'perturbed':arr(p)});ps.append(p)
 ap=avg(ps);return {'loop_count':len(me.loops),'polygon_count':len(me.polygons),'loops':loops,'average_perturbed_source':arr(ap),'expected_target_average_perturbed':arr(norm(mapv(ap)))}

def angle(a,b):
 a=norm(a);b=norm(b);return float(a.angle(b)*180/3.141592653589793)
def main():
 a=cli();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);q=norm((.36,.48,.80));img,png,rgb=normal_image(out,q);mat=material(img);oa=make(A,FACES_A,-1.25);ob=make(B,FACES_B,1.25);oa.data.materials.append(mat);ob.data.materials.append(mat);bpy.context.view_layer.update();ca=contract(oa,q);cb=contract(ob,q);sep=angle(ca['average_perturbed_source'],cb['average_perturbed_source'])
 if sep<.1:raise RuntimeError(f'witness not discriminative: {sep}')
 blend=out/'TRIANGULATION_TBN_WITNESS.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));bpy.ops.object.select_all(action='DESELECT');oa.select_set(True);ob.select_set(True);bpy.context.view_layer.objects.active=oa;glb=out/'TRIANGULATION_TBN_WITNESS.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_materials='EXPORT',export_tangents=True)
 rec={'schema':'oleander.3d.gltf-triangulation-tbn-source.v1','blender_version':bpy.app.version_string,'same_vertex_positions':VERTS,'same_vertex_uv':UV,'faces':{A:FACES_A,B:FACES_B},'tangent_space_sample':arr(q),'encoded_normal_rgb':rgb,'normal_texture':png.name,'normal_texture_sha256':sha(png),'asset':glb.name,'asset_bytes':glb.stat().st_size,'asset_sha256':sha(glb),'native_master':blend.name,'objects':{A:ca,B:cb},'source_average_perturbed_separation_deg':sep,'claim':'triangulation is a shading/bake dependency when a surface is not perfectly planar or when tangent frames depend on topology; it must not be changed silently after tangent-space baking','evidence_class':'NATIVE_TRIANGULATION_TBN_SENSITIVITY_PENDING_TARGET_RUNTIME','holds':['Three target reconstruction','pixel shader output parity','production retopo mesh','MikkTSpace cross-DCC parity','Design KEEP']};(out/'SOURCE_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
