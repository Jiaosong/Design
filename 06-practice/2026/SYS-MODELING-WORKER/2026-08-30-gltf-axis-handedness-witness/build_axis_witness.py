#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from pathlib import Path

import bpy


def cli():
    argv=sys.argv
    argv=argv[argv.index('--')+1:] if '--' in argv else []
    p=argparse.ArgumentParser()
    p.add_argument('--out',required=True)
    return p.parse_args(argv)


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''):
            h.update(c)
    return h.hexdigest()


def mat(name,color):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    b=m.node_tree.nodes.get('Principled BSDF')
    b.inputs['Base Color'].default_value=(*color,1.0)
    b.inputs['Roughness'].default_value=0.42
    return m


def add_box(name,center,size,color):
    bpy.ops.mesh.primitive_cube_add(size=1.0,location=center)
    o=bpy.context.object
    o.name=name
    o.dimensions=size
    bpy.context.view_layer.objects.active=o
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat(name+'_MAT',color))
    return o


def center_and_size(o):
    return {
        'center':[float(v) for v in o.location],
        'size':[float(v) for v in o.dimensions]
    }


def map_center_xyz_to_gltf(c):
    x,y,z=c
    return [x,z,-y]


def map_size_xyz_to_gltf(s):
    x,y,z=s
    return [x,z,y]


def main():
    a=cli(); out=Path(a.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    specs=[
      ('WITNESS_POS_X',(1.60,0.20,0.35),(0.42,0.62,0.78),(0.82,0.20,0.15)),
      ('WITNESS_POS_Y',(-0.45,1.90,0.60),(0.54,0.74,0.30),(0.16,0.72,0.24)),
      ('WITNESS_POS_Z',(0.75,-0.90,2.25),(0.32,0.44,0.92),(0.18,0.34,0.84)),
      ('WITNESS_NEG_Y',(-1.10,-1.40,0.25),(0.66,0.28,0.50),(0.84,0.66,0.12)),
    ]
    objs=[]
    for name,c,s,col in specs:
        objs.append(add_box(name,c,s,col))
    bpy.ops.object.select_all(action='SELECT')
    glb=out/'AXIS_HANDEDNESS_WITNESS.glb'
    bpy.ops.export_scene.gltf(
        filepath=str(glb),
        export_format='GLB',
        use_selection=True,
        export_yup=True,
        export_materials='EXPORT',
    )
    source={o.name:center_and_size(o) for o in objs}
    expected={
      name:{
        'center':map_center_xyz_to_gltf(v['center']),
        'size':map_size_xyz_to_gltf(v['size'])
      } for name,v in source.items()
    }
    receipt={
      'schema':'oleander.3d.gltf-axis-handedness-source.v1',
      'blender_version':bpy.app.version_string,
      'asset':glb.name,
      'asset_bytes':glb.stat().st_size,
      'asset_sha256':sha256(glb),
      'source_coordinate_system':'Blender right-handed Z-up',
      'target_coordinate_system':'glTF/Three.js right-handed Y-up',
      'declared_transform':'(x,y,z) -> (x,z,-y)',
      'transform_matrix_rows':[[1,0,0],[0,0,1],[0,-1,0]],
      'transform_determinant':1,
      'source_objects':source,
      'expected_target_objects':expected,
      'evidence_class':'NATIVE_EXCHANGE_WITNESS_PENDING_TARGET_RUNTIME',
      'holds':['real browser signed-transform readback','normal/tangent orientation','production asset parity','Design KEEP']
    }
    (out/'SOURCE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__': main()
