#!/usr/bin/env python3
import argparse,hashlib,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector

POS='TBN_POS_SCALE'; NEG='TBN_NEG_SCALE'; NUN='TBN_NEG_NONUNIFORM'; IMG='NEG_SCALE_TBN_NORMAL'; MAT='NEG_SCALE_TBN_MAT'

def cli():
    a=sys.argv;a[a.index('--')+1:] if '--' in a else []
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
def angle_deg(a,b):
    a=norm(a);b=norm(b);return math.degrees(math.acos(max(-1.0,min(1.0,float(a.dot(b))))))

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
    A=o.matrix_world.to_3x3();Nmat=A.inverted().transposed();det=float(A.determinant());det_sign=-1 if det<0 else 1
    wt=norm(A@t);wn=norm(Nmat@n);wb_direct=norm(A@b);wb_ortho=norm(wn.cross(wt))*w*det_sign
    wp_shader=norm(wt*q.x+wb_ortho*q.y+wn*q.z);wp_normal_matrix=norm(Nmat@p)
    return {
      'local':{'tangent':arr(t),'normal':arr(n),'bitangent':arr(b),'sign':w,'perturbed':arr(p)},
      'source_world':{
        'linear_determinant':det,'determinant_sign':det_sign,
        'tangent':arr(wt),'normal':arr(wn),
        'direct_transformed_bitangent':arr(wb_direct),
        'orthonormal_bitangent':arr(wb_ortho),
        'shader_perturbed':arr(wp_shader),
        'normal_matrix_transformed_local_perturbed':arr(wp_normal_matrix),
        'direct_vs_orthonormal_bitangent_angle_deg':angle_deg(wb_direct,wb_ortho),
        'shader_vs_normal_matrix_perturbed_angle_deg':angle_deg(wp_shader,wp_normal_matrix)
      },
      'expected_target_world':{
        'tangent':arr(norm(mapv(wt))),'normal':arr(norm(mapv(wn))),
        'bitangent':arr(norm(mapv(wb_ortho))),'perturbed':arr(norm(mapv(wp_shader)))
      }
    }

def main():
    a=cli();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);bpy.ops.wm.read_factory_settings(use_empty=True);t,b,n=basis();q=norm((.36,.48,.80));img,png,rgb=normal_image(out,q);mat=material(img)
    pos=quad(POS,t,b);neg=quad(NEG,t,b);nun=quad(NUN,t,b)
    pos.location=(-2.3,0,0);neg.location=(0,0,0);nun.location=(2.3,0,0)
    neg.scale=(-1,1,1);nun.scale=(-1.8,.55,1.35)
    for o in (pos,neg,nun):o.data.materials.append(mat)
    bpy.context.view_layer.update()
    cp=contract(pos,q);cn=contract(neg,q);cu=contract(nun,q)
    if cp['source_world']['linear_determinant']<=0 or cn['source_world']['linear_determinant']>=0 or cu['source_world']['linear_determinant']>=0:raise RuntimeError('controlled determinant witness not established')
    if cu['source_world']['direct_vs_orthonormal_bitangent_angle_deg']<=1.0:raise RuntimeError('non-uniform attack is not discriminative enough for this controlled fixture')
    blend=out/'NEGATIVE_SCALE_TBN_WITNESS.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));bpy.ops.object.select_all(action='DESELECT')
    for o in (pos,neg,nun):o.select_set(True)
    bpy.context.view_layer.objects.active=pos
    glb=out/'NEGATIVE_SCALE_TBN_WITNESS.glb';bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_materials='EXPORT',export_tangents=True)
    rec={
      'schema':'oleander.3d.gltf-negative-scale-tbn-source.v2','blender_version':bpy.app.version_string,
      'tangent_space_sample':arr(q),'encoded_normal_rgb':rgb,'normal_texture':png.name,'normal_texture_sha256':sha(png),
      'asset':glb.name,'asset_bytes':glb.stat().st_size,'asset_sha256':sha(glb),'native_master':blend.name,
      'objects':{POS:cp,NEG:cn,NUN:cu},
      'attack':{'nonuniform_negative_scale':[-1.8,.55,1.35],'fixture_discriminator_deg':1.0,'fixture_discriminator_authority':'TEST_LOCAL_NUMERICAL_FIXTURE_ONLY — not a production, engine, geometry, shading, or manufacturing tolerance'},
      'claim':'odd-reflection handedness and non-uniform transform effects must be validated at the final orthonormal world TBN / framebuffer carrier; direct A*B is retained only as an adverse comparison under non-uniform scale',
      'evidence_class':'NATIVE_NEGATIVE_NONUNIFORM_TBN_PENDING_TARGET_RUNTIME',
      'holds':['nested negative transforms','skinning','triangulation change','Three MeshStandardMaterial full PBR parity','hardware GPU/driver parity','other engines/importers','Design KEEP']
    }
    (out/'SOURCE_RECEIPT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
