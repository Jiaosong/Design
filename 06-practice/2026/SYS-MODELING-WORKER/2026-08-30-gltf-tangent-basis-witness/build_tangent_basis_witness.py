#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy

STD_NAME='UV_STANDARD'
MIRROR_NAME='UV_MIRRORED'
MAT_NAME='TANGENT_WITNESS_MAT'
IMG_NAME='TANGENT_WITNESS_NORMAL'


def cli():
    argv=sys.argv
    argv=argv[argv.index('--')+1:] if '--' in argv else []
    p=argparse.ArgumentParser(); p.add_argument('--out',required=True); return p.parse_args(argv)


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()


def create_quad(name,x0,x1,mirror_uv=False):
    y0,y1=-0.55,0.55
    verts=[(x0,y0,0.0),(x1,y0,0.0),(x1,y1,0.0),(x0,y1,0.0)]
    mesh=bpy.data.meshes.new(name+'_MESH')
    mesh.from_pydata(verts,[],[(0,1,2,3)]); mesh.update()
    uv=mesh.uv_layers.new(name='UVMap')
    coords=[(0,0),(1,0),(1,1),(0,1)] if not mirror_uv else [(1,0),(0,0),(0,1),(1,1)]
    poly=mesh.polygons[0]
    for li,co in zip(poly.loop_indices,coords): uv.data[li].uv=co
    obj=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(obj)
    return obj


def external_normal(out):
    target=bpy.data.images.new('TANGENT_WITNESS_GEN',width=8,height=8,alpha=False,float_buffer=False)
    # Constant non-flat tangent-space normal biased toward +T: normalized-ish
    # vector approximately (+0.60, 0.0, +0.80) -> RGB (0.80, 0.50, 0.90).
    px=[]
    for _ in range(64): px.extend((0.80,0.50,0.90,1.0))
    target.pixels=px; target.colorspace_settings.name='Non-Color'
    p=out/'TANGENT_WITNESS_NORMAL.png'; target.filepath_raw=str(p); target.file_format='PNG'; target.save()
    img=bpy.data.images.load(str(p),check_existing=False); img.name=IMG_NAME; img.colorspace_settings.name='Non-Color'
    return img,p


def material(img):
    m=bpy.data.materials.new(MAT_NAME); m.use_nodes=True
    nt=m.node_tree; bsdf=nt.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=(0.48,0.48,0.48,1); bsdf.inputs['Roughness'].default_value=0.44
    tex=nt.nodes.new('ShaderNodeTexImage'); tex.name='NORMAL_TEX'; tex.image=img
    nm=nt.nodes.new('ShaderNodeNormalMap'); nm.name='NORMAL_MAP'; nm.space='TANGENT'; nm.inputs['Strength'].default_value=1.0
    nt.links.new(tex.outputs['Color'],nm.inputs['Color']); nt.links.new(nm.outputs['Normal'],bsdf.inputs['Normal'])
    return m


def tangent_contract(obj):
    mesh=obj.data
    mesh.calc_tangents(uvmap='UVMap')
    signs=[]; tangents=[]
    for loop in mesh.loops:
        signs.append(-1 if loop.bitangent_sign < 0 else 1)
        tangents.append([float(v) for v in loop.tangent])
    uniq=sorted(set(signs))
    return {'loop_count':len(mesh.loops),'signs':signs,'unique_signs':uniq,'tangents':tangents}


def main():
    a=cli(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    std=create_quad(STD_NAME,-1.25,-0.15,False)
    mir=create_quad(MIRROR_NAME,0.15,1.25,True)
    img,img_path=external_normal(out); mat=material(img)
    std.data.materials.append(mat); mir.data.materials.append(mat)
    std_c=tangent_contract(std); mir_c=tangent_contract(mir)
    if len(std_c['unique_signs'])!=1 or len(mir_c['unique_signs'])!=1 or std_c['unique_signs'][0]==mir_c['unique_signs'][0]:
        raise RuntimeError(f'mirrored UV did not produce opposite tangent handedness: {std_c} / {mir_c}')
    blend=out/'TANGENT_BASIS_WITNESS.blend'; bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    bpy.ops.object.select_all(action='DESELECT'); std.select_set(True); mir.select_set(True); bpy.context.view_layer.objects.active=std
    glb=out/'TANGENT_BASIS_WITNESS.glb'
    bpy.ops.export_scene.gltf(filepath=str(glb),export_format='GLB',use_selection=True,export_yup=True,export_materials='EXPORT',export_tangents=True)
    receipt={
      'schema':'oleander.3d.gltf-tangent-basis-source.v1',
      'blender_version':bpy.app.version_string,
      'native_master':blend.name,
      'asset':glb.name,'asset_bytes':glb.stat().st_size,'asset_sha256':sha256(glb),
      'normal_texture':img_path.name,'normal_texture_bytes':img_path.stat().st_size,'normal_texture_sha256':sha256(img_path),
      'normal_texture_semantics':{'colorspace':'Non-Color','tangent_normal_rgb':[0.80,0.50,0.90],'approx_tangent_vector':[0.60,0.0,0.80]},
      'objects':{
        STD_NAME:{'uv_orientation':'standard','blender_tangent':std_c},
        MIRROR_NAME:{'uv_orientation':'mirrored-u','blender_tangent':mir_c}
      },
      'mirrored_uv_flips_bitangent_sign':True,
      'export_contract':{'format':'GLB','export_yup':True,'export_tangents':True,'material_normal_map':True},
      'evidence_class':'NATIVE_TANGENT_BASIS_SOURCE_PENDING_TARGET_RUNTIME',
      'holds':['Three.js TANGENT.w readback','normalTexture material readback','pixel shading parity','negative-scale tangent parity','Design KEEP']
    }
    (out/'SOURCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
