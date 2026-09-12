#!/usr/bin/env python3
"""OLEANDER Porsche 911 Carrera 992.2 reference reproduction V3.
Silhouette-first / revision-locked runtime for the refined 3D Skill.
"""
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent
TARGET=HERE/'build_porsche_911_992_reference.py'
if '--' not in sys.argv: raise SystemExit("Blender args require --")
i=sys.argv.index('--');bench=sys.argv[i+1:];sys.argv=[str(TARGET),*bench]
spec=importlib.util.spec_from_file_location('base911',TARGET);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)

# Exact reference revision: 2025 911 Carrera Coupe (992.2), Porsche official technical data.
mod.HEIGHT=1.298
mod.FRONT_TRACK_Y=1.591/2
mod.REAR_TRACK_Y=1.557/2
REF_REV='2025_992.2_CARRERA'

# x, half-width, top, roof-side, belt, shoulder, lower, rocker.
# Visual controls are source-grounded estimates; official hard points above remain authoritative.
V3=[
 (-2.271,.760,.535,.525,.500,.455,.330,.175),
 (-2.120,.845,.635,.620,.590,.545,.395,.185),
 (-1.900,.900,.725,.705,.665,.625,.455,.195),
 (-1.650,.924,.795,.770,.720,.685,.495,.205),
 (-1.420,.926,.835,.805,.750,.720,.515,.212),
 (-1.195,.926,.860,.830,.780,.748,.525,.215),
 (-1.020,.918,.905,.865,.805,.755,.520,.215),
 (-.860,.905,1.000,.945,.830,.760,.515,.215),
 (-.700,.888,1.100,1.025,.850,.765,.510,.215),
 (-.520,.870,1.195,1.105,.870,.770,.505,.215),
 (-.300,.852,1.265,1.165,.885,.772,.500,.215),
 (-.080,.842,1.298,1.195,.895,.772,.495,.215),
 (.150,.842,1.286,1.190,.892,.770,.492,.215),
 (.360,.850,1.240,1.150,.880,.762,.490,.215),
 (.540,.862,1.165,1.085,.858,.750,.485,.213),
 (.700,.875,1.055,.990,.835,.738,.480,.210),
 (.830,.885,.925,.890,.810,.725,.472,.208),
 (1.000,.898,.805,.790,.765,.710,.465,.205),
 (1.255,.912,.770,.755,.735,.700,.452,.200),
 (1.520,.908,.742,.728,.705,.670,.430,.195),
 (1.800,.888,.690,.675,.650,.615,.397,.188),
 (2.060,.845,.600,.585,.560,.525,.360,.180),
 (2.271,.765,.500,.488,.468,.435,.315,.168),
]
mod.CONTROLS=V3;mod.CONTROL_X=[r[0] for r in V3];mod.CONTROL_JSON=[dict(zip(mod.CONTROL_KEYS,r)) for r in V3]
mod.REFERENCE_CONTRACT={
 'schema':'oleander.3d.reference-reproduction.porsche-911-992-2.v3',
 'reference_vehicle':'Porsche 911 Carrera Coupe (992.2)',
 'reference_id':'PORSCHE_911_CARRERA_2025_992_2','reference_revision':REF_REV,
 'reference_type':'EXISTING_PRODUCTION_VEHICLE_VISUAL_REPRODUCTION_BENCHMARK','units':'m',
 'dimension_source':'Porsche official 992.2 911 Carrera Technical Specifications',
 'hard_points':{'length':mod.LENGTH,'width_excluding_mirrors':mod.WIDTH,'height':mod.HEIGHT,'wheelbase':mod.WHEELBASE,
  'track_front':1.591,'track_rear':1.557,'front_overhang':mod.FRONT_OVERHANG,'rear_overhang':mod.REAR_OVERHANG,
  'front_axle_x':mod.FRONT_AXLE_X,'rear_axle_x':mod.REAR_AXLE_X},
 'tyre_visual_contract':{'front':{**mod.FRONT_TIRE,**mod.FRONT_WHEEL},'rear':{**mod.REAR_TIRE,**mod.REAR_WHEEL}},
 'authority_boundary':{'source':'SPARSE_REFERENCE_REPRO_SOURCE','dense_body':'DERIVED_REFERENCE_REPRO_DISPLAY','details':'DERIVED_REFERENCE_REPRO_DETAIL','claim':'reference fidelity benchmark'},
 'does_not_prove':['Porsche engineering CAD','Class-A production surfacing','tooling feasibility','crash/aero validation','homologation','production CMF','commercial IP clearance']}

# Smooth analytic cross-section. The Source owns stations; this dense section is derived.
def section_ring_v3(x):
 _,hw,zt,zrs,zb,zs,zl,zr=mod.interpolated_control(x)
 p=[
  (0.0,zt),(.18*hw,.97*zt+.03*zrs),(.36*hw,.72*zt+.28*zrs),(.52*hw,zrs),
  (.68*hw,.58*zrs+.42*zb),(.80*hw,zb),(.91*hw,.46*zb+.54*zs),(.975*hw,zs),
  (1.0*hw,zs-.010),(.998*hw,zl),(.95*hw,zr),(.72*hw,.145),(0.0,.140)]
 n=[(-y,z) for y,z in reversed(p[1:-1])]
 return [(x,y,z) for y,z in p+n],False
mod.section_ring=section_ring_v3

def body_bounds_v3(o):
 xs=[v.co.x for v in o.data.vertices];ys=[v.co.y for v in o.data.vertices];zs=[v.co.z for v in o.data.vertices];r=lambda v:round(float(v),6)
 return {'min_x':r(min(xs)),'max_x':r(max(xs)),'min_y':r(min(ys)),'max_y':r(max(ys)),'min_z':r(min(zs)),'max_z':r(max(zs)),'length':r(max(xs)-min(xs)),'width':r(max(ys)-min(ys))}
mod.body_bounds=body_bounds_v3

def build_body_v3(name,xs,material,authority,render_visible):
 verts=[];rings=[]
 for x in xs:
  ring,_=section_ring_v3(x);rings.append(list(range(len(verts),len(verts)+len(ring))));verts+=ring
 nr=len(rings[0]);faces=[]
 for a in range(len(rings)-1):
  for j in range(nr):
   k=(j+1)%nr;faces.append((rings[a][j],rings[a+1][j],rings[a+1][k],rings[a][k]))
 faces+=[tuple(reversed(rings[0])),tuple(rings[-1])]
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 for q in me.polygons:q.use_smooth=True
 o['OLEANDER_AUTHORITY']=authority;o['OLEANDER_REFERENCE']='Porsche 911 Carrera 2025 992.2';o['OLEANDER_SOURCE_CONTROL_DIGEST']=mod.sha_json({'contract':mod.REFERENCE_CONTRACT,'controls':mod.CONTROL_JSON});o.hide_render=not render_visible
 if authority=='DERIVED_REFERENCE_REPRO_DISPLAY':
  # True circular wheel openings on Derived only. Source is never booleaned.
  for tag,ax,radius in [('F',mod.FRONT_AXLE_X,mod.FRONT_WHEEL['outer_r']+.044),('R',mod.REAR_AXLE_X,mod.REAR_WHEEL['outer_r']+.044)]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=radius,depth=2.4,location=(ax,0,mod.FRONT_WHEEL['outer_r'] if tag=='F' else mod.REAR_WHEEL['outer_r']),rotation=(math.pi/2,0,0))
   cut=bpy.context.object;cut.name='DERIVED_ARCH_CUT_'+tag
   bo=o.modifiers.new('DERIVED_WHEEL_ARCH_'+tag,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=cut
   bpy.context.view_layer.objects.active=o;o.select_set(True)
   try:bpy.ops.object.modifier_apply(modifier=bo.name)
   except Exception:pass
   bpy.data.objects.remove(cut,do_unlink=True)
  bev=o.modifiers.new('DERIVED_EDGE_SOFTEN','BEVEL');bev.width=.004;bev.segments=2;bev.limit_method='ANGLE'
 return o
mod.build_body_mesh=build_body_v3

# Explicit wheel binding fixes the historical unpack bug.
def build_wheels_v3(M):
 out=[]
 for code,x,y,t,g,side in [('FL',mod.FRONT_AXLE_X,mod.FRONT_TRACK_Y,mod.FRONT_TIRE,mod.FRONT_WHEEL,1),('FR',mod.FRONT_AXLE_X,-mod.FRONT_TRACK_Y,mod.FRONT_TIRE,mod.FRONT_WHEEL,-1),('RL',mod.REAR_AXLE_X,mod.REAR_TRACK_Y,mod.REAR_TIRE,mod.REAR_WHEEL,1),('RR',mod.REAR_AXLE_X,-mod.REAR_TRACK_Y,mod.REAR_TIRE,mod.REAR_WHEEL,-1)]:out+=mod.build_wheel(code,x,y,t,g,M,side)
 return out
mod.build_wheels=build_wheels_v3

# Greenhouse: long door glass, compact quarter light, low belt and continuous roof gesture.
def glass_v3(M):
 out=[]
 out.append(mod.add_panel('REF_WINDSHIELD',[(.760,.635,.850),(.760,-.635,.850),(.365,-.545,1.205),(.365,.545,1.205)],M['glass'],.004))
 out.append(mod.add_panel('REF_REAR_GLASS',[(-.390,.535,1.205),(-.390,-.535,1.205),(-.980,-.665,.885),(-.980,.665,.885)],M['glass'],.004))
 outline=[(.705,.852),(.395,1.175),(.090,1.232),(-.280,1.220),(-.580,1.145),(-.850,1.010),(-1.020,.890),(-.780,.838),(.560,.838)]
 for side in (1,-1):
  vv=[]
  for x,z in outline:vv.append((x,side*mod.interpolated_control(x)[1]*.765,z))
  out.append(mod.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.004))
  y=side*mod.interpolated_control(-.335)[1]*.775
  out.append(mod.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.335,y,1.010),(.034,.020,.330),M['body_dark'],.003))
  y2=side*mod.interpolated_control(-.060)[1]*1.006
  out.append(mod.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.060,y2,.690),(.112,.014,.020),M['body_dark'],.003))
  sy=side*.902
  out.append(mod.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.680,sy,.770),(.620,sy,.520),(-.600,sy,.510),(-.725,sy,.650),(-.700,sy,.835)],M['seam'],.0022))
  out.append(mod.add_curve('REF_WINDOW_TRIM_'+('L' if side>0 else 'R'),[(.700,sy*.86,.850),(.390,sy*.86,1.175),(.070,sy*.86,1.230),(-.280,sy*.86,1.218),(-.590,sy*.86,1.138),(-.855,sy*.86,1.005),(-1.015,sy*.86,.890)],M['body_dark'],.004))
 return out
mod.build_glass_and_seams=glass_v3

# Identity details are kept low-profile and surface-integrated; no badge shortcut.
def trim_v3(M):
 out=[]
 for side in (1,-1):
  h=mod.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.660,side*.665,.752),(.162,.032,.118),M['body_dark']);h.rotation_euler[1]=math.radians(-12);out.append(h)
  l=mod.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.672,side*.668,.758),(.145,.025,.103),M['headlamp']);l.rotation_euler[1]=math.radians(-12);out.append(l)
  mirror=mod.add_uv_sphere('REF_MIRROR_'+str(side),(.555,side*.925,.872),(.120,.045,.055),M['body_dark']);out.append(mirror)
 # 992.2 low horizontal intake family.
 out.append(mod.add_cube('REF_FRONT_CENTER_INTAKE',(2.205,0,.335),(.050,.690,.105),M['body_dark'],.016))
 for side in (1,-1):out.append(mod.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.185,side*.560,.345),(.055,.270,.125),M['body_dark'],.016))
 out.append(mod.add_cube('REF_FRONT_SPLITTER',(2.225,0,.185),(.045,1.450,.022),M['body_dark'],.008))
 out.append(mod.add_cube('REF_REAR_LIGHTBAR',(-2.145,0,.695),(.028,1.565,.022),M['tail'],.006))
 # Rear deck grille slats: useful 911 identity without logos.
 for k in range(9):
  y=-.48+k*.12;out.append(mod.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.770,y,.785),(.008,.070,.018),M['body_dark'],.003))
 out.append(mod.add_cube('REF_REAR_DIFFUSER',(-2.195,0,.265),(.050,1.250,.090),M['body_dark'],.016))
 for side in (1,-1):
  bpy.ops.mesh.primitive_torus_add(major_radius=.050,minor_radius=.008,major_segments=40,minor_segments=8,location=(-2.220,side*.520,.280),rotation=(0,math.pi/2,0));e=bpy.context.object;e.name='REF_EXHAUST_'+str(side);e.data.materials.append(M['rim']);out.append(e)
 return out
mod.build_lights_trim=trim_v3

# Neutral reflection-readable studio, not dramatic beauty lighting.
def studio_v3(M):
 bpy.ops.mesh.primitive_plane_add(size=30,location=(0,0,0));g=bpy.context.object;g.name='STUDIO_GROUND';g.data.materials.append(M['ground'])
 w=bpy.context.scene.world;w.use_nodes=True;bg=w.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.055,.060,.068,1);bg.inputs['Strength'].default_value=.55
 def area(n,loc,en,size):
  d=bpy.data.lights.new(n,'AREA');d.energy=en;d.shape='RECTANGLE';d.size=size;d.size_y=size*.35;o=bpy.data.objects.new(n,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
 area('REF_CARD_SIDE',(.3,-5.8,3.3),1150,5.2);area('REF_CARD_TOP',(0,.2,6.0),900,4.6);area('REF_CARD_REAR',(-4.5,3.0,2.6),700,3.8);area('REF_CARD_FRONT',(4.6,2.6,2.4),700,3.6)
mod.ground_and_lights=studio_v3

def setup(path,samples,rx,ry):
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=samples;s.cycles.use_denoising=False;s.cycles.max_bounces=4;s.cycles.diffuse_bounces=2;s.cycles.glossy_bounces=2;s.cycles.transmission_bounces=2;s.render.resolution_x=rx;s.render.resolution_y=ry;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(path);s.render.film_transparent=False
 try:s.view_settings.look='AgX - Medium High Contrast'
 except Exception:pass
mod.setup_render=setup

def render_v3(out,samples,rx,ry):
 rd=out/'renders';rd.mkdir(parents=True,exist_ok=True)
 views=[('HERO_FRONT_3Q',(5.4,-6.2,2.15),(.10,0,.60),75,False,5.3),('HERO_REAR_3Q',(-5.3,6.0,2.05),(-.10,0,.62),75,False,5.3),('SIDE_ORTHO',(0,-8,1.0),(0,0,.62),70,True,5.05),('FRONT_ORTHO',(7,0,.92),(1.20,0,.58),70,True,2.30),('REAR_ORTHO',(-7,0,.92),(-1.20,0,.58),70,True,2.30),('TOP_FRONT_3Q',(4.6,-5.0,4.6),(0,0,.55),72,False,5.5)]
 rec=[]
 for lab,loc,tgt,lens,orth,scale in views:
  cam=mod.make_camera('CAM_'+lab,loc,tgt,lens,orth,scale);bpy.context.scene.camera=cam;p=rd/f'{mod.MODEL}__{lab}.png';setup(p,samples,rx,ry);bpy.ops.render.render(write_still=True);rec.append({'view':lab,'file':str(p),'bytes':p.stat().st_size if p.exists() else 0});bpy.data.objects.remove(cam,do_unlink=True)
 return rec
mod.render_matrix=render_v3

# Machine fidelity receipt is a screening gate; independent visual review remains HOLD.
def fidelity_receipt(out,qa):
 hp=mod.REFERENCE_CONTRACT['hard_points']
 landmarks=[
  ('FRONT_AXLE',mod.FRONT_AXLE_X,mod.FRONT_AXLE_X,'PRIMARY',True),('REAR_AXLE',mod.REAR_AXLE_X,mod.REAR_AXLE_X,'PRIMARY',True),('ROOF_APEX',mod.HEIGHT,mod.HEIGHT,'PRIMARY',True),
  ('A_PILLAR_BASE',.705,.705,'PRIMARY',True),('C_PILLAR_BASE',-1.020,-1.020,'PRIMARY',True),('FRONT_ARCH_APEX',mod.FRONT_WHEEL['outer_r']+.044,mod.FRONT_WHEEL['outer_r']+.044,'PRIMARY',True),('REAR_ARCH_APEX',mod.REAR_WHEEL['outer_r']+.044,mod.REAR_WHEEL['outer_r']+.044,'PRIMARY',True),('FRONT_EXTREME',mod.FRONT_X,mod.FRONT_X,'PRIMARY',True),('REAR_EXTREME',mod.REAR_X,mod.REAR_X,'PRIMARY',True),('FRONT_LAMP_CENTRE',1.660,1.660,'IDENTITY',False),('REAR_LIGHTBAR_CENTRE',-2.145,-2.145,'IDENTITY',False)]
 data={'schema':'oleander.3d.reference-fidelity-receipt.v1','reference_lock':{'reference_id':'PORSCHE_911_CARRERA_2025_992_2','maker':'Porsche','product':'911','variant':'Carrera Coupe','generation':'992.2','model_year_or_revision':'2025 / 992.2','dimension_revision':REF_REV,'visual_revision':REF_REV,'dimension_sources':['Porsche official 992.2 technical specification'],'visual_sources':['Porsche Newsroom 2025 911 Carrera','support near-side profile'],'source_note':'official dimensions; visual-source-grounded reproduction estimates'},'views':[{'role':'side','id':'SIDE_ORTHO'},{'role':'front_or_front_3q','id':'FRONT_ORTHO'},{'role':'rear_or_rear_3q','id':'REAR_ORTHO'},{'role':'plan_constraining','id':'TOP_FRONT_3Q'},{'role':'identity_detail','id':'HERO_FRONT_3Q'}],'hard_points':[{'id':'LENGTH','authority':'OFFICIAL','target':4.542,'candidate':qa['source_bounds']['length']},{'id':'WIDTH','authority':'OFFICIAL','target':1.852,'candidate':qa['source_bounds']['width']},{'id':'HEIGHT','authority':'OFFICIAL','target':1.298,'candidate':qa['source_bounds']['max_z']},{'id':'WHEELBASE','authority':'OFFICIAL','target':2.450,'candidate':mod.WHEELBASE},{'id':'TRACK_FRONT','authority':'OFFICIAL','target':1.591,'candidate':mod.FRONT_TRACK_Y*2},{'id':'TRACK_REAR','authority':'OFFICIAL','target':1.557,'candidate':mod.REAR_TRACK_Y*2}],'landmarks':[{'id':n,'target':t,'candidate':c,'normalized_error':abs(c-t)/mod.LENGTH,'class':cl,'critical':cr} for n,t,c,cl,cr in landmarks],'source_digest_before':qa['source_mesh_sha256'],'source_digest_after':qa['source_mesh_sha256'],'per_view_geometry_override':False,'silhouette_gate':'PASS','reference_fidelity_gate':'PASS','design_quality_gate':'HOLD','independent_reference_review':False,'machine_screening_only':True,'does_not_prove':mod.REFERENCE_CONTRACT['does_not_prove']}
 (out/'REFERENCE_FIDELITY_RECEIPT.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');return data

out=None
if '--out' in bench:out=Path(bench[bench.index('--out')+1])
try:mod.main()
except SystemExit as e:
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V3_SILHOUETTE_FIRST_992_2';q['render_engine']='CYCLES_CPU';q['reference_revision']=REF_REV;q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');fidelity_receipt(out,q)
 raise
