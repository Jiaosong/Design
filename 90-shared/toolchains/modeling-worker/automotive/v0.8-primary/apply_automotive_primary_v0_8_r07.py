#!/usr/bin/env python3
"""OLEANDER Automotive Primary Surface v0.8 — R07 selective glazing-mask closure.
No design geometry change. Fixes only the R06 mask duplicate material-slot replacement bug.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import bpy

ap=argparse.ArgumentParser();ap.add_argument('--base-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
src=Path(a.base_source).read_text();defs=src.split('if __name__=="__main__":')[0];exec(compile(defs,a.base_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Primary_Surface_v0.8';REV='R07';body=bpy.data.objects['BODY_PRIMARY']

def emission_mat(name,color):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();o=nt.nodes.new('ShaderNodeOutputMaterial');e=nt.nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=color;e.inputs['Strength'].default_value=1.0;nt.links.new(e.outputs['Emission'],o.inputs['Surface']);return m

def mask(out,label,loc,target,ortho,scale,lens):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);dup=body.copy();dup.data=body.data.copy();dup.name='GLAZING_MASK_BODY';bpy.context.collection.objects.link(dup)
    before={};
    for p in dup.data.polygons:before[p.material_index]=before.get(p.material_index,0)+1
    white=emission_mat('MAT_MASK_BODY',(1,1,1,1));red=emission_mat('MAT_MASK_GLASS',(1,0,0,1))
    assert len(dup.data.materials)>=2
    # Critical R07 fix: replace slots in place. Never clear the material list, because Blender
    # clamps polygon material_index to 0 when the slots are cleared.
    dup.data.materials[0]=white;dup.data.materials[1]=red
    after={};
    for p in dup.data.polygons:after[p.material_index]=after.get(p.material_index,0)+1
    hidden={o.name:o.hide_render for o in bpy.context.scene.objects}
    for o in bpy.context.scene.objects:o.hide_render=(o!=dup)
    set_world((0,0,0),0.0);cam=camera('CAM_'+label,loc,target,lens,ortho,scale);cam.hide_render=False;bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{label}.png';setup_render(p,1,a.resolution);bpy.ops.render.render(write_still=True)
    im=bpy.data.images.load(str(p),check_existing=False);px=list(im.pixels);rp=wp=0
    for i in range(0,len(px),4):
        r,g,b,al=px[i:i+4]
        if r>.75 and g<.20 and b<.20:rp+=1
        if r>.60 and g>.60 and b>.60:wp+=1
    bpy.data.images.remove(im);bpy.data.objects.remove(cam,do_unlink=True);bpy.data.objects.remove(dup,do_unlink=True)
    for o in bpy.context.scene.objects:
        if o.name in hidden:o.hide_render=hidden[o.name]
    return {'view':label,'file':str(p),'material_indices_before':before,'material_indices_after':after,'red_pixels':rp,'white_pixels':wp,'red_fraction_of_frame':rp/(a.resolution*a.resolution)}

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
side=mask(out,'GLAZING_MASK_SIDE',(0,-8.5,1.15),(0,0,.62),True,5.1,85);front=mask(out,'GLAZING_MASK_FRONT',(7.0,0,1.10),(0,0,.65),True,2.55,85)
checks={'side_indices_preserved':side['material_indices_before']==side['material_indices_after'],'front_indices_preserved':front['material_indices_before']==front['material_indices_after'],'side_mask_visible':side['red_pixels']>500,'front_mask_visible':front['red_pixels']>200,'source_glass_faces':side['material_indices_before'].get('1',side['material_indices_before'].get(1,0))>0,'primary_shell_manifold':nonmanifold(body)==0}
q={'schema':'oleander.automotive-primary-surface.qa.v0.8-r07','model':MODEL,'revision':REV,'status':'DIAGNOSTIC_PASS' if all(checks.values()) else 'DIAGNOSTIC_FAIL','checks':checks,'side':side,'front':front,'revision_scope':'Selective mask validation only. R05 geometry and R06 normal diagnostic renders remain the visual evidence.','evidence_boundary':'Diagnostic closure only; modeling-quality decision requires R06 visual review.'};(out/'AUTOMOTIVE_PRIMARY_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');rec={'schema':'oleander.automotive-primary-surface.receipt.v0.8-r07','model':MODEL,'revision':REV,'blender_version':bpy.app.version_string,'status':'EXECUTED_DIAGNOSTIC_PASS' if q['status']=='DIAGNOSTIC_PASS' else 'EXECUTED_DIAGNOSTIC_FAIL','qa':str(out/'AUTOMOTIVE_PRIMARY_QA.json'),'renders':[side,front]};(out/'AUTOMOTIVE_PRIMARY_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status']=='DIAGNOSTIC_PASS' else 5)
