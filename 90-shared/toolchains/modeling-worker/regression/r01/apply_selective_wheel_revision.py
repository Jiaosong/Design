#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,struct,sys
from pathlib import Path
import bpy
from mathutils import Vector

WORKER_VERSION='oleander-modeling-selective-r01'

def args():
    av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument('--contract',required=True);p.add_argument('--out',required=True);return p.parse_args(av)

def mesh_hash(o):
    h=hashlib.sha256();h.update(o.name.encode())
    for row in o.matrix_world:
        for v in row:h.update(struct.pack('<d',float(v)))
    me=o.data
    for v in me.vertices:
        h.update(struct.pack('<ddd',float(v.co.x),float(v.co.y),float(v.co.z)))
    for p in me.polygons:
        h.update(struct.pack('<I',len(p.vertices)))
        for i in p.vertices:h.update(struct.pack('<I',int(i)))
    return h.hexdigest()

def camera(name,loc,target,lens):
    d=bpy.data.cameras.new(name);d.lens=lens;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o

def render(path,loc,target,lens,samples,res):
    c=camera('REGRESSION_CAMERA',loc,target,lens);bpy.context.scene.camera=c
    s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=samples;s.render.resolution_x=res;s.render.resolution_y=res;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(path)
    try:s.cycles.use_adaptive_sampling=True;s.render.use_persistent_data=True;bpy.context.view_layer.cycles.use_denoising=True;s.view_settings.view_transform='Khronos PBR Neutral'
    except Exception:pass
    bpy.ops.render.render(write_still=True);bpy.data.objects.remove(c,do_unlink=True)

def main():
    a=args();contract=json.loads(Path(a.contract).read_text());out=Path(a.out).resolve();(out/'renders').mkdir(parents=True,exist_ok=True)
    selector='_SPOKE_';targets=sorted([o for o in bpy.data.objects if o.type=='MESH' and selector in o.name],key=lambda x:x.name)
    expected=contract['expected_target_count'];scale=float(contract['parameters']['spoke_chord_scale'])
    before={o.name:mesh_hash(o) for o in bpy.data.objects if o.type=='MESH'}
    if len(targets)!=expected:raise RuntimeError(f'target count {len(targets)} != {expected}')
    for o in targets:
        for v in o.data.vertices:v.co.x*=scale
        o.data.update()
    after={o.name:mesh_hash(o) for o in bpy.data.objects if o.type=='MESH'}
    changed=sorted([n for n in before if before[n]!=after[n]])
    locked_changed=sorted([n for n in changed if selector not in n])
    if locked_changed:raise RuntimeError('locked geometry changed: '+','.join(locked_changed))
    if len(changed)!=expected:raise RuntimeError(f'changed object count {len(changed)} != {expected}')
    budget=contract['resource_budget'];samples=int(budget['samples']);res=int(budget['resolution'])
    render(out/'renders'/'WHEEL_DETAIL.png',(2.0,-3.0,.90),(1.36,-.79,.34),98,samples,res)
    render(out/'renders'/'HERO_FRONT_3Q.png',(6.2,-7.2,2.65),(.05,0,.62),76,samples,res)
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'AUTOMOTIVE_R01_VARIANT.blend'))
    report={'schema':'oleander.selective-modeling-geometry-report.v1','worker_version':WORKER_VERSION,'operation':contract['operation'],'target_count':len(targets),'changed_objects':changed,'locked_changed_objects':locked_changed,'locked_geometry_pass':not locked_changed,'before_target_hash':hashlib.sha256(''.join(before[o.name] for o in targets).encode()).hexdigest(),'after_target_hash':hashlib.sha256(''.join(after[o.name] for o in targets).encode()).hexdigest(),'render_count':2,'source_authority_mutated':False}
    (out/'GEOMETRY_REVISION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    receipt={'schema':'oleander.modeling-worker-receipt.v1','status':'EXECUTED_SELECTIVE_PASS','job_id':contract['job_id'],'worker_version':WORKER_VERSION,'blender_version':bpy.app.version_string,'geometry_report':'GEOMETRY_REVISION_REPORT.json','renders':['WHEEL_DETAIL.png','HERO_FRONT_3Q.png']}
    (out/'MODELING_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
