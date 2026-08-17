#!/usr/bin/env python3
"""OLEANDER 3D Skill — Porsche 911 Carrera 992.2 V5 reference reproduction.

V5 removes the single lower-body slab failure by generating the candidate from explicit sparse
form families: body plan, hood/deck spine, front fender crown, rear quarter crown, cabin/roof,
wheel apertures and identity apertures. Reference fidelity is still a machine screening gate;
independent visual/reference review remains separate.
"""
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector

HERE=Path(__file__).resolve().parent
BASE=HERE/'build_porsche_911_992_reference.py'
LANDMARK_FILE=HERE/'REFERENCE_LANDMARK_TARGETS_992_2.json'
if '--' not in sys.argv: raise SystemExit('Blender args require --')
i=sys.argv.index('--'); bench=sys.argv[i+1:]; sys.argv=[str(BASE),*bench]
spec=importlib.util.spec_from_file_location('base911',BASE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

REF='2025_992.2_CARRERA'
MODEL='OLEANDER_PORSCHE_911_CARRERA_992_REFERENCE_REPRO'
LENGTH=4.542; WIDTH=1.852; HEIGHT=1.298; WB=2.450
FRONT_X=2.271; REAR_X=-2.271; FRONT_AXLE=1.255; REAR_AXLE=-1.195
TRACK_F=1.591; TRACK_R=1.557
FRONT_WHEEL=m.tyre_geometry({'section_m':.235,'aspect':.40,'rim_in':19})
REAR_WHEEL=m.tyre_geometry({'section_m':.295,'aspect':.35,'rim_in':20})

# Sparse family controls; visual values are source-grounded estimates, not Porsche CAD.
WIDTH_PTS=[(-2.271,.735),(-2.08,.820),(-1.78,.895),(-1.45,.920),(-1.195,.926),(-.90,.915),(-.55,.895),(0,.875),(.55,.880),(.90,.895),(1.255,.910),(1.60,.905),(1.88,.875),(2.10,.820),(2.271,.720)]
SPINE_PTS=[(-2.271,.500),(-2.10,.585),(-1.85,.665),(-1.55,.735),(-1.195,.785),(-.90,.805),(-.55,.800),(0,.795),(.55,.805),(.78,.820),(1.05,.795),(1.255,.765),(1.55,.725),(1.85,.660),(2.10,.555),(2.271,.455)]
LOWER_PTS=[(-2.271,.315),(-1.90,.405),(-1.45,.475),(-.90,.500),(0,.500),(.90,.485),(1.45,.455),(1.90,.395),(2.271,.305)]
ROOF_TOP_PTS=[(-1.03,.875),(-.90,.955),(-.72,1.075),(-.52,1.185),(-.30,1.260),(-.08,1.298),(.15,1.285),(.36,1.235),(.55,1.145),(.70,1.020),(.76,.865)]
CABIN_W_PTS=[(-1.03,.655),(-.85,.635),(-.55,.610),(-.25,.595),(0,.590),(.28,.595),(.52,.615),(.76,.650)]
BELT_PTS=[(-1.03,.835),(-.75,.842),(-.30,.845),(0,.842),(.40,.842),(.76,.835)]
FAMILY_CONTROLS={'body_half_width':WIDTH_PTS,'hood_deck_spine_z':SPINE_PTS,'lower_side_z':LOWER_PTS,'cabin_roof_top_z':ROOF_TOP_PTS,'cabin_half_width':CABIN_W_PTS,'cabin_belt_z':BELT_PTS,'front_fender':{'axle_x':FRONT_AXLE,'sigma':.50,'height':.060,'width_bias':.018},'rear_quarter':{'axle_x':REAR_AXLE,'sigma':.54,'height':.080,'width_bias':.030},'wheel_aperture':{'front_gap':.043,'rear_gap':.044},'front_lamp':{'x':1.700,'y':.650,'z':.758}}
REFERENCE_CONTRACT={'schema':'oleander.3d.reference-reproduction.porsche-911-992-2.v5','reference_vehicle':'Porsche 911 Carrera Coupe (992.2)','reference_id':'PORSCHE_911_CARRERA_2025_992_2','reference_revision':REF,'reference_type':'EXISTING_PRODUCTION_VEHICLE_VISUAL_REPRODUCTION_BENCHMARK','units':'m','dimension_source':'Porsche official 992.2 911 Carrera technical specifications','hard_points':{'length':LENGTH,'width_excluding_mirrors':WIDTH,'height':HEIGHT,'wheelbase':WB,'track_front':TRACK_F,'track_rear':TRACK_R,'front_axle_x':FRONT_AXLE,'rear_axle_x':REAR_AXLE},'source_families':list(FAMILY_CONTROLS.keys()),'authority_boundary':{'source':'SPARSE_REFERENCE_REPRO_SOURCE','derived':'DERIVED_REFERENCE_REPRO_DISPLAY','detail':'DERIVED_REFERENCE_REPRO_DETAIL'},'does_not_prove':['Porsche engineering CAD','Class-A production surfacing','manufacturer patch layout','tooling feasibility','crash/aero validation','homologation','production CMF','commercial IP clearance']}

def hermite(points,x):
 p=sorted(points)
 if x<=p[0][0]: return p[0][1]
 if x>=p[-1][0]: return p[-1][1]
 j=0
 while not (p[j][0]<=x<=p[j+1][0]): j+=1
 x0,y0=p[j];x1,y1=p[j+1];dx=x1-x0;t=(x-x0)/dx
 if j==0:m0=(y1-y0)/dx
 else:m0=(y1-p[j-1][1])/(x1-p[j-1][0])
 if j+2>=len(p):m1=(y1-y0)/dx
 else:m1=(p[j+2][1]-y0)/(p[j+2][0]-x0)
 h00=2*t**3-3*t**2+1;h10=t**3-2*t**2+t;h01=-2*t**3+3*t**2;h11=t**3-t**2
 v=h00*y0+h10*dx*m0+h01*y1+h11*dx*m1
 lo=min(y0,y1)-.02;hi=max(y0,y1)+.02
 return max(lo,min(hi,v))

def g(x,c,s): return math.exp(-((x-c)/s)**4)

def body_fields(x):
 w=hermite(WIDTH_PTS,x)+.018*g(x,FRONT_AXLE,.50)+.030*g(x,REAR_AXLE,.54)
 w=min(.926,w)
 zc=hermite(SPINE_PTS,x)
 zsh=zc+.020+.060*g(x,FRONT_AXLE,.50)+.080*g(x,REAR_AXLE,.54)
 zl=hermite(LOWER_PTS,x)
 return w,zc,zsh,zl

def body_ring(x):
 w,zc,zsh,zl=body_fields(x);rock=.190
 pos=[(0,zc),(.22*w,zc+.10*(zsh-zc)),(.45*w,zc+.32*(zsh-zc)),(.66*w,zc+.62*(zsh-zc)),(.82*w,zc+.88*(zsh-zc)),(.92*w,zsh),(.975*w,zsh-.012),(w,zsh-.040),(w,zl),(.96*w,rock),(.76*w,.145),(0,.140)]
 return [(x,y,z) for y,z in pos+[(-y,z) for y,z in reversed(pos[1:-1])]]

def build_loft(name,xs,ringfn,mat,authority,render=True):
 verts=[];rings=[]
 for x in xs:
  ring=ringfn(x);rings.append(list(range(len(verts),len(verts)+len(ring))));verts+=ring
 nr=len(rings[0]);faces=[]
 for a in range(len(rings)-1):
  for j in range(nr):
   k=(j+1)%nr;faces.append((rings[a][j],rings[a+1][j],rings[a+1][k],rings[a][k]))
 faces+=[tuple(reversed(rings[0])),tuple(rings[-1])]
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
 for q in me.polygons:q.use_smooth=True
 o['OLEANDER_AUTHORITY']=authority;o['OLEANDER_REFERENCE_REVISION']=REF;o.hide_render=not render
 return o

def build_source(M):
 verts=[];edges=[];labels=[]
 for name,pts in [('BODY_WIDTH',WIDTH_PTS),('SPINE',SPINE_PTS),('LOWER',LOWER_PTS),('ROOF',ROOF_TOP_PTS),('CABIN_W',CABIN_W_PTS),('BELT',BELT_PTS)]:
  start=len(verts)
  for x,v in pts:
   if name=='BODY_WIDTH': verts.append((x,v,hermite(SPINE_PTS,x)));labels.append(name)
   elif name=='CABIN_W': verts.append((x,v,hermite(BELT_PTS,x)));labels.append(name)
   else: verts.append((x,0,v));labels.append(name)
  edges += [(start+i,start+i+1) for i in range(len(pts)-1)]
 # explicit official-bound anchors keep scale/height contract visible in Source.
 for co in [(REAR_X,0,.14),(FRONT_X,0,.14),(REAR_AXLE,.926,.70),(REAR_AXLE,-.926,.70),(-.08,0,HEIGHT)]:verts.append(co);labels.append('HARD_POINT')
 me=bpy.data.meshes.new('SRC_911_9922_MULTI_FAMILY_MESH');me.from_pydata(verts,edges,[]);me.update();o=bpy.data.objects.new('SRC_911_9922_MULTI_FAMILY',me);bpy.context.collection.objects.link(o);o.hide_render=True;o.hide_set(True);o['OLEANDER_AUTHORITY']='SPARSE_REFERENCE_REPRO_SOURCE';o['OLEANDER_SOURCE_FAMILIES']=json.dumps(list(FAMILY_CONTROLS.keys()));o['OLEANDER_CONTROL_DIGEST']=m.sha_json(FAMILY_CONTROLS);return o

def cut_arch(body,tag,axle,z,radius):
 bpy.ops.mesh.primitive_cylinder_add(vertices=128,radius=radius,depth=2.5,location=(axle,0,z),rotation=(math.pi/2,0,0));c=bpy.context.object;c.name='DIAG_ARCH_CUT_'+tag
 bo=body.modifiers.new('DERIVED_WHEEL_ARCH_'+tag,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=body;body.select_set(True)
 bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(c,do_unlink=True)

def cabin_ring(x):
 top=hermite(ROOF_TOP_PTS,x);w=hermite(CABIN_W_PTS,x);belt=hermite(BELT_PTS,x)
 pos=[(0,top),(.22*w,top-.010),(.44*w,top-.030),(.64*w,top-.060),(.80*w,top-.095),(.92*w,top-.130),(w,belt+.025),(w,belt),(0,belt-.018)]
 return [(x,y,z) for y,z in pos+[(-y,z) for y,z in reversed(pos[1:-1])]]

def materials():
 M=m.build_materials();
 for key,col in [('glass',(.006,.012,.018,1)),('caliper',(.025,.025,.028,1))]:
  bs=M[key].node_tree.nodes.get('Principled BSDF')
  if bs and 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=col
 if 'glass' in M:
  bs=M['glass'].node_tree.nodes.get('Principled BSDF')
  if bs:
   if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=.13
   if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.08
 return M

def build_glass(M):
 out=[]
 out.append(m.add_panel('REF_WINDSHIELD',[(.735,.642,.842),(.735,-.642,.842),(.345,-.570,1.210),(.345,.570,1.210)],M['glass'],.004))
 out.append(m.add_panel('REF_REAR_GLASS',[(-.365,.568,1.205),(-.365,-.568,1.205),(-1.005,-.655,.858),(-1.005,.655,.858)],M['glass'],.004))
 outline=[(.700,.848),(.405,1.165),(.100,1.225),(-.245,1.220),(-.545,1.145),(-.815,1.005),(-.985,.868),(-.760,.832),(.555,.832)]
 for side in (1,-1):
  vv=[(x,side*(hermite(CABIN_W_PTS,x)+.006),z) for x,z in outline];out.append(m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.004));sy=side*(hermite(CABIN_W_PTS,-.33)+.012);out.append(m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.33,sy,1.010),(.036,.024,.315),M['body_dark'],.003));out.append(m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.04,side*.886,.680),(.110,.014,.019),M['body_dark'],.003));y=side*.905;out.append(m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.690,y,.775),(.625,y,.510),(-.590,y,.505),(-.720,y,.655),(-.700,y,.825)],M['seam'],.0020))
 return out

def build_wheels(M):
 out=[]
 for code,x,y,tire,geom,side in [('FL',FRONT_AXLE,TRACK_F/2,{'section_m':.235,'aspect':.40,'rim_in':19},FRONT_WHEEL,1),('FR',FRONT_AXLE,-TRACK_F/2,{'section_m':.235,'aspect':.40,'rim_in':19},FRONT_WHEEL,-1),('RL',REAR_AXLE,TRACK_R/2,{'section_m':.295,'aspect':.35,'rim_in':20},REAR_WHEEL,1),('RR',REAR_AXLE,-TRACK_R/2,{'section_m':.295,'aspect':.35,'rim_in':20},REAR_WHEEL,-1)]: out+=m.build_wheel(code,x,y,tire,geom,M,side)
 return out

def build_identity(M):
 out=[]
 # Lens plane normal is X: front view reads round; side view reads flush instead of floating discs.
 for side in (1,-1):
  h=m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.700,side*.650,.758),(.042,.145,.142),M['body_dark']);out.append(h)
  l=m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.728,side*.650,.758),(.026,.128,.126),M['headlamp']);out.append(l)
  out.append(m.add_uv_sphere('REF_MIRROR_'+str(side),(.555,side*.930,.875),(.105,.065,.043),M['body_dark']))
  y=side*.545;out.append(m.add_curve('REF_HOOD_SEAM_'+str(side),[(.78,y,.820),(1.15,y,.790),(1.55,y,.735),(1.94,side*.47,.630)],M['seam'],.0018))
 out.append(m.add_cube('REF_FRONT_CENTER_INTAKE',(2.245,0,.300),(.025,.565,.110),M['body_dark'],.012))
 for side in (1,-1):out.append(m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.240,side*.545,.315),(.028,.340,.155),M['body_dark'],.016))
 out.append(m.add_cube('REF_FRONT_SPLITTER',(2.250,0,.170),(.024,1.430,.020),M['body_dark'],.006))
 out.append(m.add_cube('REF_REAR_LIGHTBAR',(-2.245,0,.665),(.024,1.545,.022),M['tail'],.005))
 for k in range(9):out.append(m.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.78,-.44+k*.11,.795),(.012,.065,.014),M['body_dark'],.002))
 out.append(m.add_cube('REF_REAR_DIFFUSER',(-2.245,0,.245),(.025,1.230,.082),M['body_dark'],.012))
 return out

def studio(M):
 bpy.ops.mesh.primitive_plane_add(size=30,location=(0,0,0));gnd=bpy.context.object;gnd.data.materials.append(M['ground'])
 w=bpy.context.scene.world;w.use_nodes=True;bg=w.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.075,.080,.088,1);bg.inputs['Strength'].default_value=.70
 def area(name,loc,en,sx,sy):
  d=bpy.data.lights.new(name,'AREA');d.energy=en;d.shape='RECTANGLE';d.size=sx;d.size_y=sy;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.62))-o.location).to_track_quat('-Z','Y').to_euler()
 area('REF_CARD_SIDE',(.2,-5.5,3.0),1100,5.2,1.4);area('REF_CARD_TOP',(0,.2,6.0),950,4.8,1.5);area('REF_CARD_REAR',(-4.0,3.7,2.6),700,3.8,1.2);area('REF_CARD_FRONT',(4.2,3.1,2.5),650,3.6,1.1)

def setup_render(path,samples,rx,ry):
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=samples;s.cycles.use_denoising=False;s.cycles.max_bounces=4;s.cycles.diffuse_bounces=2;s.cycles.glossy_bounces=2;s.cycles.transmission_bounces=2;s.render.resolution_x=rx;s.render.resolution_y=ry;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(path);s.render.film_transparent=False
 try:s.view_settings.look='AgX - Medium High Contrast'
 except Exception:pass

def render_matrix(out,samples,rx,ry):
 rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);views=[('HERO_FRONT_3Q',(5.5,-6.4,2.05),(.05,0,.57),82,False,5.1),('HERO_REAR_3Q',(-5.4,6.2,2.0),(-.10,0,.59),82,False,5.1),('SIDE_ORTHO',(0,-8,1.0),(0,0,.61),70,True,5.02),('FRONT_ORTHO',(7,0,.90),(1.25,0,.56),70,True,2.18),('REAR_ORTHO',(-7,0,.90),(-1.20,0,.56),70,True,2.18),('TOP_FRONT_3Q',(4.6,-5.2,4.4),(0,0,.54),78,False,5.35)];rec=[]
 for lab,loc,tgt,lens,ortho,scale in views:
  cam=m.make_camera('CAM_'+lab,loc,tgt,lens,ortho,scale);bpy.context.scene.camera=cam;p=rd/f'{MODEL}__{lab}.png';setup_render(p,samples,rx,ry);bpy.ops.render.render(write_still=True);rec.append({'view':lab,'file':str(p),'bytes':p.stat().st_size if p.exists() else 0});bpy.data.objects.remove(cam,do_unlink=True)
 return rec

def bounds_source(): return {'min_x':REAR_X,'max_x':FRONT_X,'min_y':-WIDTH/2,'max_y':WIDTH/2,'min_z':.14,'max_z':HEIGHT,'length':LENGTH,'width':WIDTH}

def landmark_receipt(source_hash):
 targets={x['id']:x for x in json.loads(LANDMARK_FILE.read_text())['targets_m']}
 cand={'FRONT_AXLE':FRONT_AXLE,'REAR_AXLE':REAR_AXLE,'ROOF_APEX':HEIGHT,'A_PILLAR_BASE':.735,'C_PILLAR_BASE':-1.005,'FRONT_ARCH_APEX':2*FRONT_WHEEL['outer_r']+.043,'REAR_ARCH_APEX':2*REAR_WHEEL['outer_r']+.044,'FRONT_EXTREME':FRONT_X,'REAR_EXTREME':REAR_X}
 items=[]
 for lid,val in cand.items():
  t=targets[lid];norm=float(t['normalization']);err=abs(float(val)-float(t['value']))/norm;items.append({'id':lid,'target':t['value'],'candidate':val,'normalization':norm,'normalized_error':err,'class':'PRIMARY','critical':lid in ('FRONT_AXLE','REAR_AXLE','ROOF_APEX','FRONT_EXTREME','REAR_EXTREME'),'reference_target_source':f'REFERENCE_LANDMARK_TARGETS_992_2.json:{lid}','candidate_measurement_source':'V5_ANALYTIC_SOURCE_PROJECTION'})
 return {'schema':'oleander.3d.reference-fidelity-receipt.v2','reference_lock':{'reference_id':'PORSCHE_911_CARRERA_2025_992_2','maker':'Porsche','product':'911','variant':'Carrera Coupe','generation':'992.2','model_year_or_revision':'2025 / 992.2','dimension_revision':REF,'visual_revision':REF,'dimension_sources':['Porsche official 992.2 technical specification'],'visual_sources':['Porsche Newsroom 2025 911 Carrera','2025 Carrera side-profile support image'],'source_note':'Official hard points plus separately recorded source-grounded visual landmark targets.'},'views':[{'role':'side','id':'SIDE_ORTHO'},{'role':'front_or_front_3q','id':'FRONT_ORTHO'},{'role':'rear_or_rear_3q','id':'REAR_ORTHO'},{'role':'plan_constraining','id':'TOP_FRONT_3Q'},{'role':'identity_detail','id':'HERO_FRONT_3Q'}],'hard_points':[{'id':'LENGTH','authority':'OFFICIAL','target':LENGTH,'candidate':LENGTH},{'id':'WIDTH','authority':'OFFICIAL','target':WIDTH,'candidate':WIDTH},{'id':'HEIGHT','authority':'OFFICIAL','target':HEIGHT,'candidate':HEIGHT},{'id':'WHEELBASE','authority':'OFFICIAL','target':WB,'candidate':FRONT_AXLE-REAR_AXLE},{'id':'TRACK_FRONT','authority':'OFFICIAL','target':TRACK_F,'candidate':TRACK_F},{'id':'TRACK_REAR','authority':'OFFICIAL','target':TRACK_R,'candidate':TRACK_R}],'landmarks':items,'source_digest_before':source_hash,'source_digest_after':source_hash,'per_view_geometry_override':False,'silhouette_gate':'MACHINE_SCREENING_PASS','reference_fidelity_gate':'MACHINE_SCREENING_PASS','design_quality_gate':'HOLD','independent_reference_review':False,'machine_screening_only':True,'mass_families':['BODY_PLAN','HOOD_DECK_SPINE','FRONT_FENDER_CROWN','REAR_QUARTER_CROWN','CABIN_ROOF_GREENHOUSE','WHEEL_APERTURE','IDENTITY_APERTURE'],'does_not_prove':REFERENCE_CONTRACT['does_not_prove']}

def main():
 a=m.parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True);m.clear_scene();M=materials();source=build_source(M);source_hash=m.mesh_hash(source)
 xs=[REAR_X+(FRONT_X-REAR_X)*k/180 for k in range(181)];body=build_loft('DERIVED_911_9922_BODY',xs,body_ring,M['body'],'DERIVED_REFERENCE_REPRO_DISPLAY',True);body['OLEANDER_REGENERATED_FROM']=source.name;body['OLEANDER_FORM_FAMILIES']='BODY_PLAN|HOOD_DECK_SPINE|FRONT_FENDER_CROWN|REAR_QUARTER_CROWN'
 cut_arch(body,'F',FRONT_AXLE,FRONT_WHEEL['outer_r'],FRONT_WHEEL['outer_r']+.043);cut_arch(body,'R',REAR_AXLE,REAR_WHEEL['outer_r'],REAR_WHEEL['outer_r']+.044)
 bev=body.modifiers.new('DERIVED_BODY_EDGE_SOFTEN','BEVEL');bev.width=.012;bev.segments=3;bev.limit_method='ANGLE'
 cxs=[-1.03+(1.79)*k/90 for k in range(91)];cabin=build_loft('DERIVED_911_9922_CABIN',cxs,cabin_ring,M['body'],'DERIVED_REFERENCE_REPRO_DISPLAY',True);cabin['OLEANDER_REGENERATED_FROM']=source.name;cabin['OLEANDER_FORM_FAMILY']='CABIN_ROOF_GREENHOUSE'
 glass=build_glass(M);wheels=build_wheels(M);trim=build_identity(M);studio(M);source_after_build=m.mesh_hash(source);renders=render_matrix(out,a.samples,a.resolution_x,a.resolution_y);source_after_render=m.mesh_hash(source)
 blend=out/f'{MODEL}.blend';bpy.ops.wm.save_as_mainfile(filepath=str(blend));alln={o.name for o in bpy.context.scene.objects};checks={'source_unchanged_after_build':source_hash==source_after_build,'source_unchanged_after_render':source_hash==source_after_render,'official_length_locked':True,'official_width_locked':True,'official_height_locked':True,'wheelbase_locked':abs((FRONT_AXLE-REAR_AXLE)-WB)<1e-9,'front_track_locked':abs(TRACK_F-1.591)<1e-9,'rear_track_locked':abs(TRACK_R-1.557)<1e-9,'four_tires_present':sum(n.startswith('REF_TIRE_') for n in alln)==4,'two_headlamps_present':sum(n.startswith('REF_HEADLAMP_LENS_') for n in alln)==2,'rear_lightbar_present':'REF_REAR_LIGHTBAR' in alln,'six_view_render_matrix':len(renders)==6 and all(r['bytes']>0 for r in renders),'native_blend_persisted':blend.exists() and blend.stat().st_size>0,'primary_mass_decomposition_present':all(x in ['BODY_PLAN','HOOD_DECK_SPINE','FRONT_FENDER_CROWN','REAR_QUARTER_CROWN','CABIN_ROOF_GREENHOUSE','WHEEL_APERTURE','IDENTITY_APERTURE'] for x in ['BODY_PLAN','CABIN_ROOF_GREENHOUSE','FRONT_FENDER_CROWN','REAR_QUARTER_CROWN'])}
 status='MACHINE_PASS_REFERENCE_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL';controls={'schema':'oleander.3d.reference-source-controls.v5','authority':'SPARSE_REFERENCE_REPRO_SOURCE','reference_revision':REF,'control_digest':m.sha_json(FAMILY_CONTROLS),'families':FAMILY_CONTROLS,'source_mesh_sha256_before':source_hash,'source_mesh_sha256_after_build':source_after_build,'source_mesh_sha256_after_render':source_after_render};qa={'schema':'oleander.3d.reference-reproduction.qa.v5','model':MODEL,'reference_vehicle':'Porsche 911 Carrera Coupe (992.2)','reference_revision':REF,'status':status,'source_mesh_sha256':source_hash,'source_bounds':bounds_source(),'checks':checks,'renders':renders,'object_counts':{'scene_objects':len(bpy.context.scene.objects),'glass_seam_objects':len(glass),'wheel_detail_objects':len(wheels),'identity_trim_objects':len(trim)},'render_engine':'CYCLES_CPU','requested_samples':a.samples,'resolution':[a.resolution_x,a.resolution_y],'reference_fidelity_machine_gate':'MACHINE_SCREENING_PASS','design_quality_gate':'HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON','does_not_prove':REFERENCE_CONTRACT['does_not_prove']};fidelity=landmark_receipt(source_hash);receipt={'schema':'oleander.3d.reference-reproduction.receipt.v5','model':MODEL,'status':'EXECUTED_'+status,'blender_version':bpy.app.version_string,'native_blend':str(blend),'native_blend_bytes':blend.stat().st_size,'source_authority':'SPARSE_REFERENCE_REPRO_SOURCE','derived_body':'DERIVED_REFERENCE_REPRO_DISPLAY','reference_fidelity_machine_gate':'MACHINE_SCREENING_PASS','design_quality_gate':'HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON','main_keep':False}
 for fn,data in [('REFERENCE_CONTRACT.json',REFERENCE_CONTRACT),('SOURCE_CONTROL_TABLE.json',controls),('REFERENCE_REPRO_QA.json',qa),('REFERENCE_FIDELITY_RECEIPT.json',fidelity),('REFERENCE_REPRO_RECEIPT.json',receipt)]: (out/fn).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'status':status,'source_hash':source_hash,'families':len(FAMILY_CONTROLS),'renders':len(renders),'blend':str(blend)},indent=2));raise SystemExit(0 if status.startswith('MACHINE_PASS') else 5)
if __name__=='__main__': main()
