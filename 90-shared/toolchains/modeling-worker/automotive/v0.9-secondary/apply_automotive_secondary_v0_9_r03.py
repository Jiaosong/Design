#!/usr/bin/env python3
"""OLEANDER Automotive Secondary v0.9 — M7-R03 conforming architecture.

R02 Machine PASS / Visual REVISE. R03 preserves the promoted v0.8 BODY_PRIMARY mesh,
removes all R02 secondary overlays, then derives M7 panel/reveal/lamp architecture by
shrinkwrapping it to the locked source shell.

No M8 handle/mirror/interior/wheel-spoke detail.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy, bmesh
from mathutils import Vector

MODEL='OLEANDER_Automotive_Secondary_v0.9'
REV='M7-R03'

ap=argparse.ArgumentParser()
ap.add_argument('--base-source',required=True)
ap.add_argument('--out',required=True)
ap.add_argument('--samples',type=int,default=8)
ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
a=ap.parse_args(av)

# Import only shared helper definitions from primary builder.
src=Path(a.base_source).read_text(encoding='utf-8')
defs=src.split('if __name__=="__main__":')[0]
exec(compile(defs,a.base_source,'exec'),globals(),globals())
MODEL='OLEANDER_Automotive_Secondary_v0.9'

body=bpy.data.objects['BODY_PRIMARY']

def mesh_hash(o):
    h=hashlib.sha256()
    for v in o.data.vertices:
        h.update(f'{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};'.encode())
    for p in o.data.polygons:
        h.update(('p'+','.join(map(str,p.vertices[:]))+f':m{p.material_index};').encode())
    return h.hexdigest()

source_hash_before=mesh_hash(body)

# Keep only the promoted v0.8 primary-source infrastructure before rebuilding M7.
def is_v08_source_object(name):
    exact={
        'BODY_PRIMARY','BODY_PRIMARY_CAGE','BODY_TENSION_CAGE','BODY_CONTROL_WIRE','GROUND',
        'BROAD_KEY','BROAD_FILL','STRIP_KEY','STRIP_FILL','GRAZING_KEY','GRAZING_FILL'
    }
    return name in exact or name.startswith(('WHEEL_','SEC_SHELL_','GUIDE_'))

removed=[]
for o in list(bpy.data.objects):
    if not is_v08_source_object(o.name):
        removed.append(o.name)
        bpy.data.objects.remove(o,do_unlink=True)

# Diagnostic M7 materials.
def m7_mat(name,color,rough=.42,metallic=0.0,emission=None):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes=True
    nt=m.node_tree;nt.nodes.clear()
    out=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled')
    set_input(bs,'Base Color',color);set_input(bs,'Roughness',rough);set_input(bs,'Metallic',metallic)
    if emission:
        set_input(bs,['Emission Color','Emission'],emission[0]);set_input(bs,'Emission Strength',emission[1])
    nt.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
    return m

mat_gap=m7_mat('MAT_M7_PANEL_REVEAL',(.006,.007,.007,1),.66)
mat_fascia=m7_mat('MAT_M7_FASCIA',(.012,.016,.017,1),.58)
mat_housing=m7_mat('MAT_M7_LAMP_HOUSING',(.018,.022,.023,1),.40)
mat_head=m7_mat('MAT_M7_HEAD_LENS',(.48,.55,.53,1),.22,0,((.90,1.0,.92,1),2.2))
mat_tail=m7_mat('MAT_M7_TAIL_LENS',(.30,.008,.006,1),.24,0,((1.0,.012,.006,1),2.1))
mat_rocker=m7_mat('MAT_M7_ROCKER',(.018,.021,.022,1),.54)

# Helpers: derive curves/panels from source shell without editing source.
def shrink_curve(name,points,mat,depth=.0045,offset=.003):
    cu=bpy.data.curves.new(name+'_CURVE','CURVE');cu.dimensions='3D';cu.bevel_depth=depth;cu.bevel_resolution=3
    sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for bp,co in zip(sp.bezier_points,points):
        bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    sw=o.modifiers.new('CONFORM_TO_PRIMARY','SHRINKWRAP');sw.target=body;sw.wrap_method='NEAREST_SURFACEPOINT';sw.offset=offset
    return o

def shrink_panel(name,verts,mat,offset=.004,solid=.006,bevel=.008):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],[tuple(range(len(verts)))]);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    sw=o.modifiers.new('CONFORM_TO_PRIMARY','SHRINKWRAP');sw.target=body;sw.wrap_method='NEAREST_SURFACEPOINT';sw.offset=offset
    bpy.context.view_layer.objects.active=o
    try:bpy.ops.object.modifier_apply(modifier=sw.name)
    except:pass
    so=o.modifiers.new('PANEL_THICKNESS','SOLIDIFY');so.thickness=solid
    if bevel:
        bv=o.modifiers.new('PANEL_EDGE','BEVEL');bv.width=bevel;bv.segments=3
    return o

# 1) Fender/wheel-arch reveal: a narrow conforming seam, not an applique arch strip.
FX,RX=1.36,-1.36;WY=.79;WZ=.345
for x,ax in ((FX,'F'),(RX,'R')):
    for side,sy in ((1,'L'),(-1,'R')):
        pts=[]
        for deg in range(22,159,17):
            t=math.radians(deg)
            pts.append((x+.405*math.cos(t),side*.928,WZ+.405*math.sin(t)))
        shrink_curve(f'M7R03_FENDER_REVEAL_{ax}{sy}',pts,mat_gap,.0038,.0025)

# 2) Rocker: conforming shallow panel zone, kept subordinate to body mass.
for side,sy in ((1,'L'),(-1,'R')):
    y=side*.925
    verts=[(-1.28,y,.205),(1.18,y,.205),(1.18,y,.310),(-1.28,y,.310)]
    shrink_panel(f'M7R03_ROCKER_{sy}',verts,mat_rocker,.003,.004,.006)

# 3) Front fascia: one central conforming panel + two side air-curtain zones.
shrink_panel('M7R03_FRONT_FASCIA',[(2.18,-.54,.34),(2.18,.54,.34),(2.17,.49,.53),(2.17,-.49,.53)],mat_fascia,.004,.006,.014)
for side,sy in ((1,'L'),(-1,'R')):
    yc=side*.68
    shrink_panel(f'M7R03_FRONT_AIR_{sy}',[(2.15,yc-.09,.38),(2.15,yc+.09,.38),(2.14,yc+.08,.55),(2.14,yc-.08,.55)],mat_fascia,.005,.005,.010)

# 4) Headlamp architecture: housing conforms to nose, smaller luminous lens sits inside.
for side,sy in ((1,'L'),(-1,'R')):
    yc=side*.48
    housing=[(2.16,yc-.22,.615),(2.16,yc+.22,.615),(2.15,yc+.20,.735),(2.15,yc-.20,.735)]
    lens=[(2.17,yc-.17,.642),(2.17,yc+.17,.642),(2.16,yc+.15,.698),(2.16,yc-.15,.698)]
    shrink_panel(f'M7R03_HEAD_HOUSING_{sy}',housing,mat_housing,.006,.008,.012)
    shrink_panel(f'M7R03_HEAD_LENS_{sy}',lens,mat_head,.010,.006,.008)

# 5) Rear fascia / lamp architecture using same conforming rule.
shrink_panel('M7R03_REAR_FASCIA',[(-2.18,-.52,.33),(-2.18,-.47,.53),(-2.18,.47,.53),(-2.18,.52,.33)],mat_fascia,.004,.006,.014)
for side,sy in ((1,'L'),(-1,'R')):
    yc=side*.48
    housing=[(-2.16,yc-.22,.625),(-2.16,yc-.20,.735),(-2.16,yc+.20,.735),(-2.16,yc+.22,.625)]
    lens=[(-2.17,yc-.17,.648),(-2.17,yc-.15,.700),(-2.17,yc+.15,.700),(-2.17,yc+.17,.648)]
    shrink_panel(f'M7R03_TAIL_HOUSING_{sy}',housing,mat_housing,.006,.008,.012)
    shrink_panel(f'M7R03_TAIL_LENS_{sy}',lens,mat_tail,.010,.006,.008)

# 6) Panel architecture: thin conforming reveals only.
for side,sy in ((1,'L'),(-1,'R')):
    y=side*.930
    shrink_curve(f'M7R03_DOOR_A_{sy}',[(.38,y,.38),(.37,y,.62),(.34,y,.86)],mat_gap,.0028,.002)
    shrink_curve(f'M7R03_DOOR_B_{sy}',[(-.66,y,.38),(-.65,y,.62),(-.62,y,.86)],mat_gap,.0028,.002)
    shrink_curve(f'M7R03_BELT_{sy}',[(.88,y,.875),(.36,y,.895),(-.30,y,.900),(-1.28,y,.865)],mat_gap,.0028,.002)
# hood/hatch division, derived from shell rather than floating ornament.
for side in (1,-1):
    y=side*.49
    shrink_curve(f'M7R03_HOOD_{side:+}',[(1.86,y,.74),(1.46,y,.83),(1.06,y,.89)],mat_gap,.0027,.002)
    shrink_curve(f'M7R03_HATCH_{side:+}',[(-1.05,y,.885),(-1.48,y,.82),(-1.86,y,.73)],mat_gap,.0027,.002)

source_hash_after=mesh_hash(body)
secondary=[o for o in bpy.data.objects if o.name.startswith('M7R03_')]

# Render infrastructure inherited from v0.8, with no source mutation.
lights={'BROAD':[bpy.data.objects['BROAD_KEY'],bpy.data.objects['BROAD_FILL']],
        'STRIP':[bpy.data.objects['STRIP_KEY'],bpy.data.objects['STRIP_FILL']],
        'GRAZING':[bpy.data.objects['GRAZING_KEY'],bpy.data.objects['GRAZING_FILL']]}
for o in bpy.data.objects:
    if o.name.startswith(('SEC_SHELL_','GUIDE_')) or o.name=='BODY_CONTROL_WIRE':o.hide_render=True

def render_view(out,label,loc,target,lens=75,ortho=False,scale=5,rig='BROAD',override=None):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);set_rig(lights,rig);layer=bpy.context.view_layer;old=layer.material_override
    layer.material_override=override
    set_world((.012,.012,.012),.16)
    cam=camera('CAM_'+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam
    p=rd/f'{MODEL}__{label}.png';setup_render(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True)
    layer.material_override=old;bpy.data.objects.remove(cam,do_unlink=True)
    return {'view':label,'file':str(p),'rig':rig,'override':override.name if override else None}

out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
clay=bpy.data.materials['MAT_PRIMARY_CLAY']
renders=[
 render_view(out,'HERO_FRONT_3Q',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'BROAD'),
 render_view(out,'HERO_REAR_3Q',(-5.6,6.3,2.55),(-.08,0,.62),75,False,5,'BROAD'),
 render_view(out,'SIDE_PROFILE',(0,-8.4,1.20),(0,0,.62),85,True,5.15,'BROAD'),
 render_view(out,'FRONT_ORTHO',(7.0,0,1.05),(0,0,.62),85,True,2.55,'BROAD'),
 render_view(out,'REAR_ORTHO',(-7.0,0,1.05),(0,0,.62),85,True,2.55,'BROAD'),
 render_view(out,'WHEEL_ARCH_DETAIL',(2.05,-3.0,.92),(FX,-WY,.42),95,False,2.5,'BROAD'),
 render_view(out,'CLAY_STRIP',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'STRIP',clay),
 render_view(out,'CLAY_GRAZING',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'GRAZING',clay),
]

# Contract + QA.
contract={
 'contract_version':'v0.2','spec_patch':'v0.2.1','job_id':'SYS-MODELING-WORKER-VAL-04-AUTO-M7-v0.9-R03','domain':'AUTOMOTIVE',
 'decision_question':'Can M7 secondary architecture improve fender/fascia/lamp/panel readability while remaining conforming to and non-mutating of the promoted v0.8 primary shell?',
 'loop':'CANONICAL_PRODUCTION','fidelity':'F2_PROMOTION','design_state':'REVISE','modeling_stage':'M7',
 'source_authority':{'state':'CANDIDATE_AUTHORITY','editable_source':'OLEANDER_Automotive_Primary_Surface_v0.8','artifact_hash':source_hash_before,'derived_models':[MODEL],'exports':[]},
 'hard_points':{'applicable':True,'not_applicable_reason':None,'items':[{'id':'HP-WHEELBASE','role':'locked axle relation','value':2.72,'unit':'m','status':'LOCKED'},{'id':'HP-TRACK','role':'locked stance','value':1.58,'unit':'m','status':'LOCKED'}]},
 'envelopes':{'applicable':True,'not_applicable_reason':None,'items':[{'id':'ENV-PRIMARY','role':'promoted v0.8 primary shell','geometry_type':'locked source mesh','source':'BODY_PRIMARY','status':'LOCKED'}]},
 'sections':{'applicable':True,'not_applicable_reason':None,'items':[{'id':'SEC-M7-SOURCE','role':'v0.8 section-network authority','station':'inherited','plane':'multi','continuity_target':'no M7 mutation','depends_on':['HP-WHEELBASE','HP-TRACK'],'status':'LOCKED'}]},
 'primary_geometry':[{'id':'PG-v0.8','role':'locked promoted primary shell','representation':'SubD source mesh','source_sections':['SEC-M7-SOURCE'],'status':'LOCKED'}],
 'semantic_components':[{'id':'ASY-VEHICLE','role':'M7 derived vehicle','parent':None,'source_type':'EDITABLE_SOURCE','source_ref':MODEL,'parameters':{},'instance_rule':None,'authority_state':'WORKING_SOURCE'},{'id':'COMP-CONFORMING-M7','role':'conforming secondary architecture','parent':'ASY-VEHICLE','source_type':'GENERATOR','source_ref':'BODY_PRIMARY shrinkwrap dependencies','parameters':{'component_count':len(secondary)},'instance_rule':'bilateral where applicable','authority_state':'WORKING_SOURCE'}],
 'dependencies':[{'from':'PG-v0.8','to':'COMP-CONFORMING-M7','type':'GEOMETRY'}],
 'locks':[{'target':'BODY_PRIMARY','state':'FROZEN','reason':'v0.8 F1 primary benchmark is source authority for M7','unlock_trigger':None},{'target':'M8 detail','state':'LOCKED','reason':'M7 must pass first','unlock_trigger':None}],
 'revision':{'revision_id':'M7-R03','semantic_targets':['COMP-CONFORMING-M7'],'parameters':{'strategy':'shrinkwrap conforming panels/reveals'},'expected_affected_components':['M7 secondary only'],'affected_view_policy':'HYBRID'},
 'qa':{'integrity':['source hash unchanged','source manifold','8 renders'],'construction':['all M7 architecture separate from source','fender reveal conforming','lamp housing/lens two-layer','fascia conforming','no M8 detail'],'design_geometry':['front/rear hierarchy','wheel arch integration','rocker subordination','panel-line coherence'],'project':['M7 improves reading without hiding M5 failure'],'diagnostic_views':['HERO_FRONT_3Q','HERO_REAR_3Q','SIDE_PROFILE','FRONT_ORTHO','REAR_ORTHO','WHEEL_ARCH_DETAIL','CLAY_STRIP','CLAY_GRAZING']},
 'resource_budget':{'max_variants':3,'max_iterations':3,'max_runtime_minutes':20,'max_render_views':8,'max_geometry_density':None,'parallelism':1},
 'cache':{'enabled':True,'scope':'PROJECT_LOCAL','key_inputs':['v0.8 source hash','M7-R03 contract','worker source','Blender version']},
 'exit_condition':'Secondary architecture is visually integrated, source primary remains byte-semantically unchanged, and M8 detail is not required to make the component hierarchy read.',
 'promotion':{'eligible_authority_states':['WORKING_SOURCE','CANDIDATE_AUTHORITY'],'worker_may_mutate_source_authority':False,'decision':'PENDING'},
 'persistence':{'policy':'PROMOTION_ONLY','artifact_registry':True,'sync_targets':['NOTION','GITHUB','GOOGLE_DRIVE']},
 'material_bindings':[]
}
(out/'MODELING_CONTRACT.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

prohibited=[o.name for o in bpy.data.objects if any(k in o.name for k in ['HANDLE','MIRROR','SEAT_','SCREEN','CALIPER','SPOKE'])]
checks={
 'source_primary_hash_unchanged':source_hash_before==source_hash_after,
 'source_primary_manifold':nonmanifold(body)==0,
 'conforming_component_count':len(secondary)>=24,
 'fender_reveal_count':len([o for o in secondary if 'FENDER_REVEAL' in o.name])==4,
 'rocker_count':len([o for o in secondary if 'ROCKER' in o.name])==2,
 'headlamp_two_layer':len([o for o in secondary if 'HEAD_HOUSING' in o.name])==2 and len([o for o in secondary if 'HEAD_LENS' in o.name])==2,
 'taillamp_two_layer':len([o for o in secondary if 'TAIL_HOUSING' in o.name])==2 and len([o for o in secondary if 'TAIL_LENS' in o.name])==2,
 'front_fascia':bpy.data.objects.get('M7R03_FRONT_FASCIA') is not None,
 'rear_fascia':bpy.data.objects.get('M7R03_REAR_FASCIA') is not None,
 'door_panel_lines':len([o for o in secondary if 'DOOR_' in o.name])==4,
 'premature_m8_detail_absent':len(prohibited)==0,
 'render_matrix':len(renders)==8,
}
q={'schema':'oleander.automotive-secondary.qa.v0.9-r03','model':MODEL,'revision':REV,'source_authority':'OLEANDER_Automotive_Primary_Surface_v0.8','status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_body_hash_before':source_hash_before,'source_body_hash_after':source_hash_after,'removed_r02_objects':removed,'secondary_component_count':len(secondary),'prohibited_objects':prohibited,'checks':checks,'renders':renders,'boundary':'M7 conforming derived working source only; v0.8 primary authority remains immutable. Visual review required.'}
(out/'AUTOMOTIVE_M7_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

bpy.context.scene['OLEANDER_MODEL']=MODEL;bpy.context.scene['OLEANDER_STAGE']='M7';bpy.context.scene['OLEANDER_SOURCE_AUTHORITY']='OLEANDER_Automotive_Primary_Surface_v0.8';bpy.context.scene['OLEANDER_REVISION']=REV
blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
rec={'schema':'oleander.automotive-secondary.receipt.v0.9-r03','model':MODEL,'revision':REV,'source_authority':'OLEANDER_Automotive_Primary_Surface_v0.8','blender_version':bpy.app.version_string,'status':'EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if q['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL','blend':str(blend),'qa':str(out/'AUTOMOTIVE_M7_QA.json'),'contract':str(out/'MODELING_CONTRACT.json'),'renders':renders}
(out/'AUTOMOTIVE_M7_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(rec,ensure_ascii=False,indent=2))
raise SystemExit(0 if q['status'].startswith('MACHINE_PASS') else 5)
