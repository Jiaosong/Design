#!/usr/bin/env python3
"""OLEANDER Automotive Primary Surface v0.8 — R05 tension + flush glazing.
R04 overlays are rejected. Rebuild final shell from R03 control cage with controlled
SubD crease weights; glazing is assigned to final shell faces, not floating panels.
"""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
import bpy,bmesh

ap=argparse.ArgumentParser();ap.add_argument('--base-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
src=Path(a.base_source).read_text();defs=src.split('if __name__=="__main__":')[0];exec(compile(defs,a.base_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Primary_Surface_v0.8';REV='R05'

# Remove R04 rejected overlays and previous final/wire variants; keep R03 source control cage + section guides.
for o in list(bpy.data.objects):
    if o.name.startswith(('R04_GLASS_','R04_PILLAR_')) or o.name in {'BODY_PRIMARY','BODY_CONTROL_WIRE','BODY_TENSION_CAGE'}:
        bpy.data.objects.remove(o,do_unlink=True)
source=bpy.data.objects['BODY_PRIMARY_CAGE']
body_mat=bpy.data.materials['MAT_PRIMARY_CLAY'];glass=bpy.data.materials['MAT_GUIDE_GLASS']
# Diagnostic glass: dark opaque visual zoning only.
bs=next((n for n in glass.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None) if glass.use_nodes else None
if bs:
    set_input(bs,'Base Color',(0.004,0.010,0.014,1));set_input(bs,'Roughness',.20);set_input(bs,['Transmission Weight','Transmission'],0.0)

# Build a tension cage from the R03 semantic section cage.
tension=source.copy();tension.data=source.data.copy();tension.name='BODY_TENSION_CAGE';bpy.context.collection.objects.link(tension);tension.hide_render=True;tension.hide_viewport=True
for p in tension.data.polygons:p.material_index=0
attr=tension.data.attributes.get('crease_edge') or tension.data.attributes.new(name='crease_edge',type='FLOAT',domain='EDGE')
ring_n=16;section_n=18
weights={1:.26,15:.26,3:.18,13:.18,4:.32,12:.32,6:.14,10:.14}
target={}
for j,w in weights.items():
    for i in range(section_n-1):target[tuple(sorted((i*ring_n+j,(i+1)*ring_n+j)))]=w
crease_count=0
for ei,e in enumerate(tension.data.edges):
    w=target.get(tuple(sorted(e.vertices[:])))
    if w is not None:attr.data[ei].value=w;crease_count+=1

final=tension.copy();final.data=tension.data.copy();final.name='BODY_PRIMARY';bpy.context.collection.objects.link(final);final.hide_render=False;final.hide_viewport=False
md=final.modifiers.new('PRIMARY_SUBD','SUBSURF');md.levels=2;md.render_levels=2;bpy.context.view_layer.objects.active=final;bpy.ops.object.modifier_apply(modifier=md.name)
arch_cut(final,FX);arch_cut(final,RX)
# Ensure canonical material slots exist after rebuild.
final.data.materials.clear();final.data.materials.append(body_mat);final.data.materials.append(glass)
final.data.update()

def assign_flush_glazing(o):
    count=0;side=front=rear=0
    for p in o.data.polygons:
        c=p.center;n=p.normal;mi=0
        # Side glass zone; keep a narrow B-pillar body band at x≈-0.16.
        if -1.36 < c.x < .82 and abs(c.y) > .48 and c.z > .875 and abs(n.y) > .22 and not (-.23 < c.x < -.09):
            mi=1;side+=1
        # Front windshield transition.
        if .44 < c.x < 1.02 and c.z > .89 and n.x > .18:
            mi=1;front+=1
        # Rear glazing / fastback transition.
        if -1.52 < c.x < -.92 and c.z > .86 and n.x < -.18:
            mi=1;rear+=1
        p.material_index=mi
        if mi==1:count+=1
    return {'total':count,'side':side,'front':front,'rear':rear}
zone_counts=assign_flush_glazing(final)

wire=make_wire_overlay(tension,'BODY_CONTROL_WIRE',bpy.data.materials['MAT_CONTROL_CAGE']);wire.hide_render=True
section_objs=[o for o in bpy.data.objects if o.name.startswith('SEC_SHELL_') or o.name.startswith('GUIDE_')]
wire_objs=[wire]
for o in section_objs:o.hide_render=True
mats={'BODY':body_mat,'GLASS':glass,'TIRE':bpy.data.materials['MAT_TIRE_GUIDE'],'RIM':bpy.data.materials['MAT_RIM_GUIDE'],'GROUND':bpy.data.materials['MAT_GROUND'],'SECTION':bpy.data.materials['MAT_SECTION'],'GUIDE':bpy.data.materials['MAT_GUIDE'],'CAGE':bpy.data.materials['MAT_CONTROL_CAGE'],'BLACK':bpy.data.materials.get('MAT_SILHOUETTE') or make_mat('MAT_SILHOUETTE',(0.002,0.002,0.002,1),.55,0)}
lights={'BROAD':[bpy.data.objects['BROAD_KEY'],bpy.data.objects['BROAD_FILL']],'STRIP':[bpy.data.objects['STRIP_KEY'],bpy.data.objects['STRIP_FILL']],'GRAZING':[bpy.data.objects['GRAZING_KEY'],bpy.data.objects['GRAZING_FILL']]}

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);build_contract(out);cp=out/'MODELING_CONTRACT.json';c=json.loads(cp.read_text());c['job_id']='SYS-MODELING-WORKER-VAL-03-AUTO-PRIMARY-v0.8-R05';c['decision_question']='Can controlled primary-surface tension and flush glazing zones make the integrated shell read as a coherent automobile without floating component patches or secondary detail?';c['design_state']='REVISE';c['modeling_stage']='M6';c['locks']=[{'target':'R03 integrated section network','state':'DEPENDENCY_LOCKED','reason':'R05 changes surface tension, not hard-point station topology','unlock_trigger':'M5 highlight review shows section-network failure'},{'target':'wheelbase / track / wheel centers / wheel OD','state':'LOCKED','reason':'stance hard points','unlock_trigger':None},{'target':'secondary details','state':'LOCKED','reason':'M7/M8 blocked until M5/M6 pass','unlock_trigger':None}];c['semantic_components']=[{'id':'ASY-VEHICLE','role':'automotive benchmark assembly','parent':None,'source_type':'EDITABLE_SOURCE','source_ref':MODEL,'parameters':{},'instance_rule':None,'authority_state':'WORKING_SOURCE'},{'id':'COMP-INTEGRATED-SHELL','role':'R03 integrated section shell with R05 tension weights','parent':'ASY-VEHICLE','source_type':'EDITABLE_SOURCE','source_ref':'BODY_TENSION_CAGE','parameters':{'crease_lines':['roof_edge','belt','shoulder','rocker']},'instance_rule':'bilateral','authority_state':'WORKING_SOURCE'},{'id':'COMP-FLUSH-GLAZING','role':'flush material-zoned glazing on primary shell','parent':'COMP-INTEGRATED-SHELL','source_type':'DERIVED_MODEL','source_ref':'BODY_PRIMARY material zones','parameters':zone_counts,'instance_rule':'bilateral side zones','authority_state':'NONE'}];c['dependencies']=[{'from':'COMP-INTEGRATED-SHELL','to':'COMP-FLUSH-GLAZING','type':'GEOMETRY'}];c['material_bindings']=[{'target_component':'COMP-INTEGRATED-SHELL','material_or_preset':'MAT_PRIMARY_CLAY','binding_scope':'REFERENCE_ONLY','coordinate_dependency':'R03 control cage','directionality':None,'scale_semantics':'surface diagnostic','status':'BOUND'},{'target_component':'COMP-FLUSH-GLAZING','material_or_preset':'MAT_GUIDE_GLASS','binding_scope':'REFERENCE_ONLY','coordinate_dependency':'final shell polygon zones','directionality':None,'scale_semantics':'component diagnostic','status':'BOUND'}];cp.write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n')
scene=bpy.context.scene;scene['OLEANDER_REVISION']=REV;scene['OLEANDER_REVISION_SCOPE']='R03 control cage retained; controlled crease tension + flush glazing zones; R04 overlays rejected';blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));renders=render_matrix(out,a.samples,a.resolution,mats,lights,section_objs,wire_objs)
mn,mx=bbox([final]);premature=[o.name for o in bpy.data.objects if any(k in o.name for k in ['HANDLE','HEADLAMP','TAILLAMP','SEAT_','SCREEN','CALIPER','MIRROR'])];stats=face_stats(tension);checks={'primary_shell_manifold':nonmanifold(final)==0,'control_ngon_zero':stats['ngon']==0,'crease_edges_present':crease_count>=100,'flush_glazing_faces':zone_counts['total']>=10 and zone_counts['side']>0 and zone_counts['front']>0 and zone_counts['rear']>0,'floating_glazing_absent':len([o for o in bpy.data.objects if o.name.startswith('R04_GLASS_')])==0,'wheel_guides':len([o for o in bpy.data.objects if o.name.endswith('_TIRE')])==4,'premature_detail_absent':len(premature)==0,'render_matrix':len(renders)==8,'height_corridor':1.38<=mx.z<=1.46}
q={'schema':'oleander.automotive-primary-surface.qa.v0.8-r05','model':MODEL,'revision':REV,'status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','crease_edge_count':crease_count,'glazing_zone_counts':zone_counts,'control_face_stats':stats,'checks':checks,'renders':renders,'revision_scope':'Controlled SubD tension lines + flush glazing face zones; no floating R04 panels.','evidence_boundary':'Machine/Construction gate only; M5/M6 visual review required.'};(out/'AUTOMOTIVE_PRIMARY_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');rec={'schema':'oleander.automotive-primary-surface.receipt.v0.8-r05','model':MODEL,'revision':REV,'blender_version':bpy.app.version_string,'status':'EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if q['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL','blend':str(blend),'contract':str(cp),'qa':str(out/'AUTOMOTIVE_PRIMARY_QA.json'),'renders':renders};(out/'AUTOMOTIVE_PRIMARY_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if q['status'].startswith('MACHINE_PASS') else 5)
