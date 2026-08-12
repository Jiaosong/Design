#!/usr/bin/env python3
"""OLEANDER Automotive Detail v0.10 — M8 detail/instance validation.

Derived from promoted v0.9 M7 secondary-geometry benchmark.
Adds only: wheel-face/brake detail, mirrors, flush handles and minimal wipers.
Does not modify v0.9 primary/secondary model objects.
"""
from __future__ import annotations
import argparse, hashlib, json, math, sys
from pathlib import Path
import bpy
from mathutils import Vector

MODEL='OLEANDER_Automotive_Detail_v0.10'
REV='M8-R01'

ap=argparse.ArgumentParser();ap.add_argument('--base-source',required=True);ap.add_argument('--out',required=True);ap.add_argument('--samples',type=int,default=8);ap.add_argument('--resolution',type=int,default=640)
av=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];a=ap.parse_args(av)
src=Path(a.base_source).read_text(encoding='utf-8');defs=src.split('if __name__=="__main__":')[0];exec(compile(defs,a.base_source,'exec'),globals(),globals());MODEL='OLEANDER_Automotive_Detail_v0.10'
body=bpy.data.objects['BODY_PRIMARY']

# ---------- immutable-source hash ----------
def is_model_source(o):
    if o.name.startswith('M8_'):return False
    if o.name=='GROUND' or o.name.startswith(('SEC_SHELL_','GUIDE_')) or o.name=='BODY_CONTROL_WIRE':return False
    if o.type in {'LIGHT','CAMERA'}:return False
    return o.type in {'MESH','CURVE'}

def scene_model_hash():
    h=hashlib.sha256()
    for o in sorted([x for x in bpy.data.objects if is_model_source(x)],key=lambda x:x.name):
        h.update((o.name+'|'+o.type+'|').encode())
        for row in o.matrix_world:
            h.update(','.join(f'{v:.9f}' for v in row).encode())
        h.update(b'|mats:')
        for m in o.data.materials:h.update(((m.name if m else 'NONE')+';').encode())
        if o.type=='MESH':
            for v in o.data.vertices:h.update(f'v{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};'.encode())
            for p in o.data.polygons:h.update(('p'+','.join(map(str,p.vertices[:]))+f':{p.material_index};').encode())
        elif o.type=='CURVE':
            for sp in o.data.splines:
                h.update(sp.type.encode())
                for bp in sp.bezier_points:h.update(f'b{bp.co.x:.9f},{bp.co.y:.9f},{bp.co.z:.9f};'.encode())
                for pt in sp.points:h.update(f'q{pt.co.x:.9f},{pt.co.y:.9f},{pt.co.z:.9f},{pt.co.w:.9f};'.encode())
    return h.hexdigest()

source_hash_before=scene_model_hash()
source_names_before=sorted(o.name for o in bpy.data.objects if is_model_source(o))

# ---------- materials ----------
def detail_mat(name,color,rough=.35,metal=0.0,em=None):
    m=bpy.data.materials.get(name) or bpy.data.materials.new(name);m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();outn=nt.nodes.new('ShaderNodeOutputMaterial');bs=nt.nodes.new('ShaderNodeBsdfPrincipled');set_input(bs,'Base Color',color);set_input(bs,'Roughness',rough);set_input(bs,'Metallic',metal)
    if em:set_input(bs,['Emission Color','Emission'],em[0]);set_input(bs,'Emission Strength',em[1])
    nt.links.new(bs.outputs['BSDF'],outn.inputs['Surface']);return m
mat_rim=detail_mat('MAT_M8_RIM',(.26,.28,.29,1),.28,1)
mat_disc=detail_mat('MAT_M8_DISC',(.12,.13,.13,1),.38,1)
mat_cal=detail_mat('MAT_M8_CALIPER',(.28,.035,.012,1),.36,0)
mat_mirror=detail_mat('MAT_M8_MIRROR_BODY',(.035,.042,.041,1),.28,0)
mat_glass=detail_mat('MAT_M8_MIRROR_GLASS',(.025,.035,.038,1),.12,0)
mat_handle=detail_mat('MAT_M8_HANDLE',(.12,.13,.13,1),.30,1)
mat_wiper=detail_mat('MAT_M8_WIPER',(.012,.014,.014,1),.62,0)

# ---------- helpers ----------
def add_cube(name,loc,dims,mat,rot=(0,0,0),bev=.005):
    bpy.ops.mesh.primitive_cube_add(location=loc,rotation=rot);o=bpy.context.object;o.name=name;o.dimensions=dims;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    if bev:md=o.modifiers.new('EDGE','BEVEL');md.width=bev;md.segments=3
    return o

def add_sphere(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=40,ring_count=20,location=loc);o=bpy.context.object;o.name=name;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    return o

def add_curve(name,pts,mat,depth=.003):
    cu=bpy.data.curves.new(name+'_CURVE','CURVE');cu.dimensions='3D';cu.bevel_depth=depth;cu.bevel_resolution=3;sp=cu.splines.new('BEZIER');sp.bezier_points.add(len(pts)-1)
    for bp,co in zip(sp.bezier_points,pts):bp.co=co;bp.handle_left_type='AUTO';bp.handle_right_type='AUTO'
    o=bpy.data.objects.new(name,cu);bpy.context.collection.objects.link(o);o.data.materials.append(mat);return o

def flush_handle(name,x,side):
    y=side*.944
    # small detail panel shrinkwrapped to source shell
    verts=[(x-.085,y,.735),(x+.085,y,.735),(x+.075,y,.765),(x-.075,y,.765)]
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],[(0,1,2,3)]);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat_handle)
    sw=o.modifiers.new('CONFORM','SHRINKWRAP');sw.target=body;sw.wrap_method='NEAREST_SURFACEPOINT';sw.offset=.004;bpy.context.view_layer.objects.active=o
    try:bpy.ops.object.modifier_apply(modifier=sw.name)
    except:pass
    so=o.modifiers.new('THICKNESS','SOLIDIFY');so.thickness=.004;bv=o.modifiers.new('EDGE','BEVEL');bv.width=.005;bv.segments=2
    return o

# ---------- wheel detail as one definition repeated at four hard-point locations ----------
FX,RX=1.36,-1.36;WY=.79;WZ=.345
wheel_instances=[]
for x,ax in ((FX,'F'),(RX,'R')):
    for side,sy in ((1,'L'),(-1,'R')):
        y=side*WY;outboard=side*.055
        # brake disc
        bpy.ops.mesh.primitive_cylinder_add(vertices=56,radius=.155,depth=.018,location=(x,y+outboard,WZ),rotation=(math.radians(90),0,0));disc=bpy.context.object;disc.name=f'M8_DISC_{ax}{sy}';disc.data.materials.append(mat_disc)
        # rim outer ring
        bpy.ops.mesh.primitive_torus_add(major_radius=.190,minor_radius=.018,major_segments=56,minor_segments=12,location=(x,y+side*.076,WZ),rotation=(math.radians(90),0,0));ring=bpy.context.object;ring.name=f'M8_RIM_RING_{ax}{sy}';ring.data.materials.append(mat_rim)
        # hub
        bpy.ops.mesh.primitive_cylinder_add(vertices=40,radius=.047,depth=.035,location=(x,y+side*.085,WZ),rotation=(math.radians(90),0,0));hub=bpy.context.object;hub.name=f'M8_HUB_{ax}{sy}';hub.data.materials.append(mat_rim)
        # five split spokes — restrained, not decorative dense pattern
        for i in range(5):
            a0=2*math.pi*i/5
            for branch in (-.055,.055):
                aa=a0+branch;rr=.115;px=x+rr*math.cos(aa);pz=WZ+rr*math.sin(aa)
                sp=add_cube(f'M8_SPOKE_{ax}{sy}_{i}_{"A" if branch<0 else "B"}',(px,y+side*.090,pz),(.145,.020,.014),mat_rim,(0,-aa,0),.004)
        # caliper at rear side of disc
        cal=add_cube(f'M8_CALIPER_{ax}{sy}',(x-.105,y+side*.068,WZ),(.055,.022,.105),mat_cal,(0,0,0),.009)
        wheel_instances.append(f'{ax}{sy}')

# ---------- mirrors ----------
for side,sy in ((1,'L'),(-1,'R')):
    y=side*.995
    housing=add_sphere(f'M8_MIRROR_{sy}',(.66,y,.995),(.125,.052,.050),mat_mirror)
    stem=add_cube(f'M8_MIRROR_STEM_{sy}',(.63,side*.958,.958),(.085,.026,.036),mat_mirror,(0,0,0),.010)
    glass_y=y+side*.048
    glass_obj=add_cube(f'M8_MIRROR_GLASS_{sy}',(.648,glass_y,.997),(.090,.006,.046),mat_glass,(0,0,0),.008)

# ---------- flush handles ----------
for side,sy in ((1,'L'),(-1,'R')):
    flush_handle(f'M8_HANDLE_FRONT_{sy}',.36,side)
    flush_handle(f'M8_HANDLE_REAR_{sy}',-.63,side)

# ---------- minimal wiper pair, still external detail ----------
add_curve('M8_WIPER_L',[(.72,-.16,.935),(.50,-.30,1.02)],mat_wiper,.004)
add_curve('M8_WIPER_R',[(.72,.12,.935),(.53,.26,1.01)],mat_wiper,.004)

source_hash_after=scene_model_hash()
source_names_after=sorted(o.name for o in bpy.data.objects if is_model_source(o))
m8=[o for o in bpy.data.objects if o.name.startswith('M8_')]

# ---------- render ----------
lights={'BROAD':[bpy.data.objects['BROAD_KEY'],bpy.data.objects['BROAD_FILL']],'STRIP':[bpy.data.objects['STRIP_KEY'],bpy.data.objects['STRIP_FILL']],'GRAZING':[bpy.data.objects['GRAZING_KEY'],bpy.data.objects['GRAZING_FILL']]}
for o in bpy.data.objects:
    if o.name.startswith(('SEC_SHELL_','GUIDE_')) or o.name=='BODY_CONTROL_WIRE':o.hide_render=True

def render_view(out,label,loc,target,lens=75,ortho=False,scale=5,rig='BROAD',override=None):
    rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);set_rig(lights,rig);layer=bpy.context.view_layer;old=layer.material_override;layer.material_override=override;set_world((.012,.012,.012),.16);cam=camera('CAM_'+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{label}.png';setup_render(p,a.samples,a.resolution);bpy.ops.render.render(write_still=True);layer.material_override=old;bpy.data.objects.remove(cam,do_unlink=True);return {'view':label,'file':str(p),'rig':rig,'override':override.name if override else None}
out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);clay=bpy.data.materials['MAT_PRIMARY_CLAY']
renders=[
 render_view(out,'HERO_FRONT_3Q',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'BROAD'),
 render_view(out,'HERO_REAR_3Q',(-5.6,6.3,2.55),(-.08,0,.62),75,False,5,'BROAD'),
 render_view(out,'SIDE_PROFILE',(0,-8.4,1.20),(0,0,.62),85,True,5.15,'BROAD'),
 render_view(out,'WHEEL_DETAIL',(2.05,-3.0,.92),(FX,-WY,.35),100,False,2.25,'BROAD'),
 render_view(out,'MIRROR_HANDLE_DETAIL',(2.1,-3.0,1.45),(.45,-.86,.88),95,False,2.3,'BROAD'),
 render_view(out,'TOP_3Q',(4.6,-5.2,5.0),(0,0,.58),78,False,5,'BROAD'),
 render_view(out,'CLAY_STRIP',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'STRIP',clay),
 render_view(out,'CLAY_GRAZING',(5.8,-6.6,2.65),(.05,0,.63),75,False,5,'GRAZING',clay),
]

checks={
 'source_model_hash_unchanged':source_hash_before==source_hash_after,
 'source_model_object_set_unchanged':source_names_before==source_names_after,
 'primary_manifold':nonmanifold(body)==0,
 'wheel_disc_count':len([o for o in m8 if o.name.startswith('M8_DISC_')])==4,
 'wheel_ring_count':len([o for o in m8 if o.name.startswith('M8_RIM_RING_')])==4,
 'wheel_spoke_count':len([o for o in m8 if o.name.startswith('M8_SPOKE_')])==40,
 'caliper_count':len([o for o in m8 if o.name.startswith('M8_CALIPER_')])==4,
 'mirror_housing_count':len([o for o in m8 if o.name.startswith('M8_MIRROR_') and not ('STEM' in o.name or 'GLASS' in o.name)])==2,
 'mirror_glass_count':len([o for o in m8 if o.name.startswith('M8_MIRROR_GLASS_')])==2,
 'handle_count':len([o for o in m8 if o.name.startswith('M8_HANDLE_')])==4,
 'wiper_count':len([o for o in m8 if o.name.startswith('M8_WIPER_')])==2,
 'render_matrix':len(renders)==8,
}
qa={'schema':'oleander.automotive-detail.qa.v0.10','model':MODEL,'revision':REV,'source_authority':'OLEANDER_Automotive_Secondary_v0.9','status':'MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL','source_scene_hash_before':source_hash_before,'source_scene_hash_after':source_hash_after,'source_object_count':len(source_names_before),'m8_component_count':len(m8),'wheel_instances':wheel_instances,'checks':checks,'renders':renders,'boundary':'M8 visual-detail benchmark only. Interior package and CMF remain later scopes; source v0.9 authority must remain immutable.'}
(out/'AUTOMOTIVE_M8_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
contract={'contract_version':'v0.2','spec_patch':'v0.2.1','job_id':'SYS-MODELING-WORKER-VAL-05-AUTO-M8-v0.10-R01','domain':'AUTOMOTIVE','decision_question':'Can repeated wheel detail, mirrors, flush handles and minimal exterior detail complete benchmark readability without mutating the promoted v0.9 M7 source?','loop':'CANONICAL_PRODUCTION','fidelity':'F2_PROMOTION','design_state':'REVISE','source_authority':{'state':'CANDIDATE_AUTHORITY','editable_source':'OLEANDER_Automotive_Secondary_v0.9','artifact_hash':source_hash_before,'derived_models':[MODEL],'exports':[]},'modeling_stage':'M8','hard_points':{'applicable':True,'not_applicable_reason':None,'items':[{'id':'HP-WHEEL-INSTANCES','role':'4 wheel hard-point instances','value':wheel_instances,'unit':'instance','status':'LOCKED'}]},'envelopes':{'applicable':True,'not_applicable_reason':None,'items':[{'id':'ENV-v0.9','role':'locked M7 model envelope','geometry_type':'source assembly','source':'v0.9','status':'FROZEN'}]},'sections':{'applicable':False,'not_applicable_reason':'M8 adds detail/instances only; section network remains inherited and frozen from v0.8/v0.9.','items':[]},'primary_geometry':[{'id':'PG-v0.8','role':'inherited primary authority','representation':'source mesh','source_sections':[],'status':'FROZEN'}],'semantic_components':[{'id':'ASY-DETAIL','role':'M8 detail derived assembly','parent':None,'source_type':'EDITABLE_SOURCE','source_ref':MODEL,'parameters':{'m8_component_count':len(m8)},'instance_rule':None,'authority_state':'WORKING_SOURCE'}],'dependencies':[],'locks':[{'target':'all v0.9 model objects','state':'FROZEN','reason':'M8 must be additive/derived','unlock_trigger':None},{'target':'interior package / CMF','state':'LOCKED','reason':'not needed to prove M8 exterior detail','unlock_trigger':None}],'revision':{'revision_id':REV,'semantic_targets':['ASY-DETAIL'],'parameters':{'detail_scope':['wheel','mirror','handle','wiper']},'expected_affected_components':['M8-prefixed objects only'],'affected_view_policy':'HYBRID'},'qa':{'integrity':['source scene hash unchanged','source object set unchanged','8 renders'],'construction':['4 repeated wheel assemblies','2 mirror assemblies','4 flush handles','2 wipers'],'design_geometry':['wheel-face readability','mirror scale','handle subordination','detail density'],'project':['M8 does not alter M5/M7 authority'] ,'diagnostic_views':[r['view'] for r in renders]},'resource_budget':{'max_variants':2,'max_iterations':2,'max_runtime_minutes':20,'max_render_views':8,'max_geometry_density':None,'parallelism':1},'cache':{'enabled':True,'scope':'PROJECT_LOCAL','key_inputs':['v0.9 source hash','M8 contract','worker source','Blender version']},'exit_condition':'Detail improves multi-scale completeness while remaining subordinate and source v0.9 is unchanged.','promotion':{'eligible_authority_states':['WORKING_SOURCE','CANDIDATE_AUTHORITY'],'worker_may_mutate_source_authority':False,'decision':'PENDING'},'persistence':{'policy':'PROMOTION_ONLY','artifact_registry':True,'sync_targets':['NOTION','GITHUB','GOOGLE_DRIVE']},'material_bindings':[]}
(out/'MODELING_CONTRACT.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
bpy.context.scene['OLEANDER_MODEL']=MODEL;bpy.context.scene['OLEANDER_STAGE']='M8';bpy.context.scene['OLEANDER_SOURCE_AUTHORITY']='OLEANDER_Automotive_Secondary_v0.9';blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend))
rec={'schema':'oleander.automotive-detail.receipt.v0.10','model':MODEL,'revision':REV,'blender_version':bpy.app.version_string,'status':'EXECUTED_MACHINE_PASS_VISUAL_REVIEW_REQUIRED' if qa['status'].startswith('MACHINE_PASS') else 'EXECUTED_MACHINE_FAIL','blend':str(blend),'qa':str(out/'AUTOMOTIVE_M8_QA.json'),'contract':str(out/'MODELING_CONTRACT.json'),'renders':renders}
(out/'AUTOMOTIVE_M8_RECEIPT.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(rec,ensure_ascii=False,indent=2));raise SystemExit(0 if qa['status'].startswith('MACHINE_PASS') else 5)
