#!/usr/bin/env python3
"""OLEANDER Automotive Primary Surface v0.8 — R06 diagnostic integrity patch.

R05 visual review exposed a diagnostic bug: the legacy SIDE_SILHOUETTE renderer cleared
material slots to create a black silhouette. Blender then collapsed polygon material indices,
so later Broad/Strip/Grazing renders could no longer display the flush glazing zones even
though Machine QA counted them correctly.

R06 does NOT change design geometry. It preserves the R05 source shell and material indices,
uses view-layer material override for silhouette, and adds explicit glazing-mask renders plus
pixel visibility gates. This separates render-test failure from design-geometry failure.
"""
from __future__ import annotations
import argparse,json,sys,math
from pathlib import Path
import bpy
from mathutils import Vector

ap=argparse.ArgumentParser();ap.add_argument('--base-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
src=Path(a.base_source).read_text();defs=src.split('if __name__=="__main__":')[0];exec(compile(defs,a.base_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Primary_Surface_v0.8';REV='R06'
body=bpy.data.objects['BODY_PRIMARY'];body_mat=bpy.data.materials['MAT_PRIMARY_CLAY'];glass=bpy.data.materials['MAT_GUIDE_GLASS']
black=bpy.data.materials.get('MAT_SILHOUETTE') or make_mat('MAT_SILHOUETTE',(0.002,0.002,0.002,1),.55,0)
section_objs=[o for o in bpy.data.objects if o.name.startswith('SEC_SHELL_') or o.name.startswith('GUIDE_')]
wire_objs=[o for o in bpy.data.objects if o.name=='BODY_CONTROL_WIRE']
for o in section_objs+wire_objs:o.hide_render=True
lights={'BROAD':[bpy.data.objects['BROAD_KEY'],bpy.data.objects['BROAD_FILL']],'STRIP':[bpy.data.objects['STRIP_KEY'],bpy.data.objects['STRIP_FILL']],'GRAZING':[bpy.data.objects['GRAZING_KEY'],bpy.data.objects['GRAZING_FILL']]}

def mat_index_counts(o):
    d={}
    for p in o.data.polygons:d[p.material_index]=d.get(p.material_index,0)+1
    return d
before=mat_index_counts(body)

def render_view(out,label,loc,target,lens,ortho,scale,rig,mode='normal'):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);set_rig(lights,rig);toggle_overlay(section_objs,wire_objs,mode=='section',mode=='wire')
    scene=bpy.context.scene;layer=bpy.context.view_layer
    old_override=layer.material_override
    if mode=='silhouette':
        set_world((1,1,1),.80);layer.material_override=black
    else:
        set_world((.012,.012,.012),.16);layer.material_override=None
    cam=camera('CAM_'+label,loc,target,lens,ortho,scale);scene.camera=cam;p=rd/f'{MODEL}__{label}.png';setup_render(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);layer.material_override=old_override;bpy.data.objects.remove(cam,do_unlink=True);return {'view':label,'file':str(p),'rig':rig,'mode':mode}

def emission_mat(name,color):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();o=nt.nodes.new('ShaderNodeOutputMaterial');e=nt.nodes.new('ShaderNodeEmission');e.inputs['Color'].default_value=color;e.inputs['Strength'].default_value=1.0;nt.links.new(e.outputs['Emission'],o.inputs['Surface']);return m

def glazing_mask(out,label,loc,target,ortho=False,scale=5,lens=75):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
    dup=body.copy();dup.data=body.data.copy();dup.name='GLAZING_MASK_BODY';bpy.context.collection.objects.link(dup)
    white=emission_mat('MAT_MASK_BODY',(1,1,1,1));red=emission_mat('MAT_MASK_GLASS',(1,0,0,1));dup.data.materials.clear();dup.data.materials.append(white);dup.data.materials.append(red)
    # Hide every scene object except mask body and camera.
    hidden={o.name:o.hide_render for o in bpy.context.scene.objects};
    for o in bpy.context.scene.objects:o.hide_render=(o!=dup)
    set_world((0,0,0),0.0);cam=camera('CAM_'+label,loc,target,lens,ortho,scale);cam.hide_render=False;bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{label}.png';setup_render(p,1,a.resolution);bpy.context.scene.render.film_transparent=False;bpy.ops.render.render(write_still=True)
    # Actual image visibility proof: count strongly-red pixels in rendered PNG through Blender image loader.
    im=bpy.data.images.load(str(p),check_existing=False);px=list(im.pixels);redpix=0;bodypix=0
    for i in range(0,len(px),4):
        r,g,b,al=px[i:i+4]
        if r>.75 and g<.20 and b<.20:redpix+=1
        if r>.60 and g>.60 and b>.60:bodypix+=1
    bpy.data.images.remove(im)
    bpy.data.objects.remove(cam,do_unlink=True);bpy.data.objects.remove(dup,do_unlink=True)
    for o in bpy.context.scene.objects:
        if o.name in hidden:o.hide_render=hidden[o.name]
    return {'view':label,'file':str(p),'red_pixels':redpix,'white_pixels':bodypix,'red_fraction_of_frame':redpix/(a.resolution*a.resolution)}

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);records=[]
records.append(render_view(out,'SIDE_SILHOUETTE',(0,-8.5,1.15),(0,0,.62),85,True,5.1,'BROAD','silhouette'))
records.append(render_view(out,'FRONT_ORTHO',(7.0,0,1.10),(0,0,.65),85,True,2.55,'BROAD'))
records.append(render_view(out,'TOP_ORTHO',(0,0,8.0),(0,0,.55),85,True,5.2,'BROAD'))
records.append(render_view(out,'CLAY_BROAD',(5.8,-6.7,2.8),(.05,0,.65),75,False,5,'BROAD'))
records.append(render_view(out,'CLAY_STRIP',(5.8,-6.7,2.8),(.05,0,.65),75,False,5,'STRIP'))
records.append(render_view(out,'CLAY_GRAZING',(5.8,-6.7,2.8),(.05,0,.65),75,False,5,'GRAZING'))
records.append(render_view(out,'SECTION_OVERLAY',(5.6,-6.4,3.0),(0,0,.70),78,False,5,'BROAD','section'))
records.append(render_view(out,'CONTROL_CAGE',(5.8,-6.7,2.8),(.05,0,.65),75,False,5,'BROAD','wire'))
mask_side=glazing_mask(out,'GLAZING_MASK_SIDE',(0,-8.5,1.15),(0,0,.62),True,5.1,85);records.append(mask_side)
mask_front=glazing_mask(out,'GLAZING_MASK_FRONT',(7.0,0,1.10),(0,0,.65),True,2.55,85);records.append(mask_front)
after=mat_index_counts(body)

# The primary geometry must remain byte-semantically unchanged at polygon/material-index level during diagnostics.
checks={'material_indices_preserved':before==after,'glass_face_index_present':after.get(1,0)>0,'glazing_mask_side_visible':mask_side['red_pixels']>500,'glazing_mask_front_visible':mask_front['red_pixels']>200,'primary_shell_manifold':nonmanifold(body)==0,'wheel_guides':len([o for o in bpy.data.objects if o.name.endswith('_TIRE')])==4,'premature_detail_absent':len([o for o in bpy.data.objects if any(k in o.name for k in ['HANDLE','HEADLAMP','TAILLAMP','SEAT_','SCREEN','CALIPER','MIRROR'])])==0,'render_matrix':len(records)==10}
q={'schema':'oleander.automotive-primary-surface.qa.v0.8-r06','model':MODEL,'revision':REV,'status':'DIAGNOSTIC_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'DIAGNOSTIC_FAIL','material_index_counts_before':before,'material_index_counts_after':after,'glazing_masks':{'side':mask_side,'front':mask_front},'checks':checks,'renders':records,'revision_scope':'No design geometry change. Diagnostic renderer corrected to preserve polygon material indices; explicit glazing-mask proof added.','evidence_boundary':'Diagnostic integrity PASS does not equal modeling-quality PASS.'};(out/'AUTOMOTIVE_PRIMARY_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
# Copy source blend unchanged as the inspected working source.
bpy.context.scene['OLEANDER_REVISION']=REV;bpy.context.scene['OLEANDER_REVISION_SCOPE']='diagnostic-only; R05 geometry unchanged';blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));rec={'schema':'oleander.automotive-primary-surface.receipt.v0.8-r06','model':MODEL,'revision':REV,'blender_version':bpy.app.version_string,'status':'EXECUTED_DIAGNOSTIC_PASS_VISUAL_REVIEW_REQUIRED' if q['status'].startswith('DIAGNOSTIC_PASS') else 'EXECUTED_DIAGNOSTIC_FAIL','blend':str(blend),'qa':str(out/'AUTOMOTIVE_PRIMARY_QA.json'),'renders':records};(out/'AUTOMOTIVE_PRIMARY_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status'].startswith('DIAGNOSTIC_PASS') else 5)
