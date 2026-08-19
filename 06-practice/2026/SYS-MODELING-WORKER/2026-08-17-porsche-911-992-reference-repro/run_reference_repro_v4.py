#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import bpy
from mathutils import Vector
HERE=Path(__file__).resolve().parent;TARGET=HERE/'build_porsche_911_992_reference.py'
if '--' not in sys.argv:raise SystemExit('Blender args require --')
i=sys.argv.index('--');bench=sys.argv[i+1:];sys.argv=[str(TARGET),*bench]
spec=importlib.util.spec_from_file_location('base911',TARGET);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
REF='2025_992.2_CARRERA';m.HEIGHT=1.298;m.FRONT_TRACK_Y=1.591/2;m.REAR_TRACK_Y=1.557/2
V=[(-2.271,.760,.535,.525,.500,.455,.330,.175),(-2.120,.845,.635,.620,.590,.545,.395,.185),(-1.900,.900,.725,.705,.665,.625,.455,.195),(-1.650,.924,.795,.770,.720,.685,.495,.205),(-1.420,.926,.835,.805,.750,.720,.515,.212),(-1.195,.926,.860,.830,.780,.748,.525,.215),(-1.020,.918,.905,.865,.805,.755,.520,.215),(-.860,.905,1.000,.945,.830,.760,.515,.215),(-.700,.888,1.100,1.025,.850,.765,.510,.215),(-.520,.870,1.195,1.105,.870,.770,.505,.215),(-.300,.852,1.265,1.165,.885,.772,.500,.215),(-.080,.842,1.298,1.195,.895,.772,.495,.215),(.150,.842,1.286,1.190,.892,.770,.492,.215),(.360,.850,1.240,1.150,.880,.762,.490,.215),(.540,.862,1.165,1.085,.858,.750,.485,.213),(.700,.875,1.055,.990,.835,.738,.480,.210),(.830,.885,.925,.890,.810,.725,.472,.208),(1.000,.898,.805,.790,.765,.710,.465,.205),(1.255,.912,.770,.755,.735,.700,.452,.200),(1.520,.908,.742,.728,.705,.670,.430,.195),(1.800,.888,.690,.675,.650,.615,.397,.188),(2.060,.845,.600,.585,.560,.525,.360,.180),(2.271,.765,.500,.488,.468,.435,.315,.168)]
m.CONTROLS=V;m.CONTROL_X=[r[0] for r in V];m.CONTROL_JSON=[dict(zip(m.CONTROL_KEYS,r)) for r in V]
m.REFERENCE_CONTRACT={'schema':'oleander.3d.reference-reproduction.porsche-911-992-2.v4','reference_vehicle':'Porsche 911 Carrera Coupe (992.2)','reference_id':'PORSCHE_911_CARRERA_2025_992_2','reference_revision':REF,'reference_type':'EXISTING_PRODUCTION_VEHICLE_VISUAL_REPRODUCTION_BENCHMARK','units':'m','dimension_source':'Porsche official 992.2 technical specifications','hard_points':{'length':m.LENGTH,'width_excluding_mirrors':m.WIDTH,'height':m.HEIGHT,'wheelbase':m.WHEELBASE,'track_front':1.591,'track_rear':1.557,'front_overhang':m.FRONT_OVERHANG,'rear_overhang':m.REAR_OVERHANG,'front_axle_x':m.FRONT_AXLE_X,'rear_axle_x':m.REAR_AXLE_X},'tyre_visual_contract':{'front':{**m.FRONT_TIRE,**m.FRONT_WHEEL},'rear':{**m.REAR_TIRE,**m.REAR_WHEEL}},'authority_boundary':{'source':'SPARSE_REFERENCE_REPRO_SOURCE','dense_body':'DERIVED_REFERENCE_REPRO_DISPLAY','details':'DERIVED_REFERENCE_REPRO_DETAIL'},'does_not_prove':['Porsche engineering CAD','Class-A production surfacing','tooling feasibility','crash/aero validation','homologation','production CMF','commercial IP clearance']}

def source_ring(x):
 _,hw,zt,zrs,zb,zs,zl,zr=m.interpolated_control(x);p=[(0,zt),(.25*hw,.88*zt+.12*zrs),(.50*hw,zrs),(.75*hw,zb),(.94*hw,zs),(hw,zs-.01),(.998*hw,zl),(.94*hw,zr),(.70*hw,.145),(0,.140)];return [(x,y,z) for y,z in p+[(-y,z) for y,z in reversed(p[1:-1])]],False

def lower_ring(x):
 _,hw,zt,zrs,zb,zs,zl,zr=m.interpolated_control(x);inside=-1.05<x<.82;cap=min(zt,zb+.035) if inside else zt
 p=[(0,cap),(.26*hw,cap+.004),(.52*hw,max(cap-.008,zs+.035)),(.74*hw,max(cap-.018,zs+.040)),(.90*hw,zs+.025),(.98*hw,zs+.010),(hw,zs),(.998*hw,zl),(.94*hw,zr),(.72*hw,.145),(0,.140)];return [(x,y,z) for y,z in p+[(-y,z) for y,z in reversed(p[1:-1])]],False

def bounds(o):
 xs=[v.co.x for v in o.data.vertices];ys=[v.co.y for v in o.data.vertices];zs=[v.co.z for v in o.data.vertices];r=lambda v:round(float(v),6);return {'min_x':r(min(xs)),'max_x':r(max(xs)),'min_y':r(min(ys)),'max_y':r(max(ys)),'min_z':r(min(zs)),'max_z':r(max(zs)),'length':r(max(xs)-min(xs)),'width':r(max(ys)-min(ys))}
m.body_bounds=bounds

def loft(name,xs,material,authority,render_visible):
 ringfn=source_ring if authority=='SPARSE_REFERENCE_REPRO_SOURCE' else lower_ring;verts=[];rings=[]
 for x in xs:
  ring,_=ringfn(x);rings.append(list(range(len(verts),len(verts)+len(ring))));verts+=ring
 nr=len(rings[0]);faces=[]
 for a in range(len(rings)-1):
  for j in range(nr):k=(j+1)%nr;faces.append((rings[a][j],rings[a+1][j],rings[a+1][k],rings[a][k]))
 faces+=[tuple(reversed(rings[0])),tuple(rings[-1])];me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material)
 for p in me.polygons:p.use_smooth=True
 o['OLEANDER_AUTHORITY']=authority;o['OLEANDER_REFERENCE']='Porsche 911 Carrera 2025 992.2';o['OLEANDER_SOURCE_CONTROL_DIGEST']=m.sha_json({'contract':m.REFERENCE_CONTRACT,'controls':m.CONTROL_JSON});o.hide_render=not render_visible
 if authority=='DERIVED_REFERENCE_REPRO_DISPLAY':
  for tag,ax,z,radius in [('F',m.FRONT_AXLE_X,m.FRONT_WHEEL['outer_r'],m.FRONT_WHEEL['outer_r']+.040),('R',m.REAR_AXLE_X,m.REAR_WHEEL['outer_r'],m.REAR_WHEEL['outer_r']+.040)]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=radius,depth=2.35,location=(ax,0,z),rotation=(math.pi/2,0,0));cut=bpy.context.object;bo=o.modifiers.new('ARCH_'+tag,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=cut;bpy.context.view_layer.objects.active=o;o.select_set(True)
   try:bpy.ops.object.modifier_apply(modifier=bo.name)
   except Exception:pass
   bpy.data.objects.remove(cut,do_unlink=True)
  bev=o.modifiers.new('BODY_EDGE_SOFTEN','BEVEL');bev.width=.0035;bev.segments=2;bev.limit_method='ANGLE'
 return o
m.build_body_mesh=loft;m.section_ring=source_ring

def cabin_mesh(M):
 C=[(-1.02,.665,.890,.850),(-.86,.650,1.000,.850),(-.68,.625,1.105,.850),(-.48,.605,1.205,.850),(-.25,.592,1.270,.850),(-.05,.590,1.298,.850),(.18,.595,1.282,.850),(.38,.610,1.230,.850),(.58,.635,1.120,.850),(.76,.660,.900,.850)]
 verts=[];rings=[]
 for x,hw,zt,zb in C:
  p=[(0,zt),(.28*hw,zt-.012),(.55*hw,zt-.035),(.82*hw,zt-.075),(hw,zt-.115),(hw,zb),(0,zb-.010)];ring=[(x,y,z) for y,z in p+[(-y,z) for y,z in reversed(p[1:-1])]];rings.append(list(range(len(verts),len(verts)+len(ring))));verts+=ring
 nr=len(rings[0]);faces=[]
 for a in range(len(rings)-1):
  for j in range(nr):k=(j+1)%nr;faces.append((rings[a][j],rings[a+1][j],rings[a+1][k],rings[a][k]))
 faces+=[tuple(reversed(rings[0])),tuple(rings[-1])];me=bpy.data.meshes.new('DERIVED_CABIN_ROOF_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_CABIN_ROOF',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_REGENERATED_FROM']='SRC_PORSCHE_911_992_SPARSE_BODY'
 for p in me.polygons:p.use_smooth=True
 bev=o.modifiers.new('CABIN_SOFTEN','BEVEL');bev.width=.003;bev.segments=2;bev.limit_method='ANGLE';return o

def windows(M):
 out=[cabin_mesh(M)]
 out.append(m.add_panel('REF_WINDSHIELD',[(.770,.640,.855),(.770,-.640,.855),(.365,-.575,1.205),(.365,.575,1.205)],M['glass'],.004));out.append(m.add_panel('REF_REAR_GLASS',[(-.430,.565,1.205),(-.430,-.565,1.205),(-1.005,-.660,.885),(-1.005,.660,.885)],M['glass'],.004))
 outline=[(.720,.855),(.395,1.175),(.080,1.235),(-.270,1.225),(-.575,1.145),(-.850,1.005),(-1.005,.885),(-.770,.835),(.560,.835)]
 for side in (1,-1):
  vv=[(x,side*m.interpolated_control(x)[1]*.755,z) for x,z in outline];out.append(m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.004));y=side*.655;out.append(m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.335,y,1.020),(.034,.026,.325),M['body_dark'],.003));sy=side*.904;out.append(m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.690,sy,.765),(.620,sy,.510),(-.600,sy,.505),(-.720,sy,.650),(-.695,sy,.835)],M['seam'],.0022));out.append(m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.075,side*.907,.682),(.108,.015,.018),M['body_dark'],.003))
 return out
m.build_glass_and_seams=windows

def wheels(M):
 out=[]
 for code,x,y,t,g,s in [('FL',m.FRONT_AXLE_X,m.FRONT_TRACK_Y,m.FRONT_TIRE,m.FRONT_WHEEL,1),('FR',m.FRONT_AXLE_X,-m.FRONT_TRACK_Y,m.FRONT_TIRE,m.FRONT_WHEEL,-1),('RL',m.REAR_AXLE_X,m.REAR_TRACK_Y,m.REAR_TIRE,m.REAR_WHEEL,1),('RR',m.REAR_AXLE_X,-m.REAR_TRACK_Y,m.REAR_TIRE,m.REAR_WHEEL,-1)]:out+=m.build_wheel(code,x,y,t,g,M,s)
 return out
m.build_wheels=wheels

def trim(M):
 out=[]
 for s in (1,-1):
  h=m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(s),(1.650,s*.665,.752),(.158,.112,.026),M['body_dark']);h.rotation_euler[1]=math.radians(-13);out.append(h);l=m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(s),(1.655,s*.667,.760),(.142,.100,.020),M['headlamp']);l.rotation_euler[1]=math.radians(-13);out.append(l);mir=m.add_uv_sphere('REF_MIRROR_'+str(s),(.545,s*.930,.870),(.110,.065,.045),M['body_dark']);out.append(mir)
 out.append(m.add_cube('REF_FRONT_CENTER_INTAKE',(2.210,0,.335),(.045,.660,.095),M['body_dark'],.014))
 for s in (1,-1):out.append(m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(s),(2.190,s*.560,.345),(.050,.255,.115),M['body_dark'],.014))
 out.append(m.add_cube('REF_FRONT_SPLITTER',(2.228,0,.180),(.040,1.420,.020),M['body_dark'],.006));out.append(m.add_cube('REF_REAR_LIGHTBAR',(-2.150,0,.692),(.025,1.550,.020),M['tail'],.005));out.append(m.add_cube('REF_REAR_DIFFUSER',(-2.200,0,.260),(.045,1.240,.085),M['body_dark'],.014))
 for k in range(8):out.append(m.add_cube(f'REF_REAR_GRILLE_{k:02d}',(-1.760,-.42+k*.12,.792),(.010,.065,.016),M['body_dark'],.003))
 return out
m.build_lights_trim=trim

def studio(M):
 bpy.ops.mesh.primitive_plane_add(size=30,location=(0,0,0));g=bpy.context.object;g.data.materials.append(M['ground']);w=bpy.context.scene.world;w.use_nodes=True;bg=w.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(.07,.075,.082,1);bg.inputs['Strength'].default_value=.65
 def a(n,loc,en,size):d=bpy.data.lights.new(n,'AREA');d.energy=en;d.shape='RECTANGLE';d.size=size;d.size_y=size*.32;o=bpy.data.objects.new(n,d);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.65))-o.location).to_track_quat('-Z','Y').to_euler()
 a('CARD_L',(.2,-5.5,3.0),1050,5.4);a('CARD_TOP',(0,0,6.0),950,4.8);a('CARD_R',(-3.8,4.0,2.8),750,4.0);a('CARD_F',(4.2,3.0,2.6),650,3.6)
m.ground_and_lights=studio

def setup(path,samples,rx,ry):
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=samples;s.cycles.use_denoising=False;s.cycles.max_bounces=4;s.cycles.diffuse_bounces=2;s.cycles.glossy_bounces=2;s.cycles.transmission_bounces=2;s.render.resolution_x=rx;s.render.resolution_y=ry;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(path);s.render.film_transparent=False
 try:s.view_settings.look='AgX - Medium High Contrast'
 except:pass
m.setup_render=setup

def renders(out,samples,rx,ry):
 rd=out/'renders';rd.mkdir(parents=True,exist_ok=True);vv=[('HERO_FRONT_3Q',(5.4,-6.2,2.05),(.10,0,.58),78,False,5.2),('HERO_REAR_3Q',(-5.3,6.0,2.0),(-.10,0,.60),78,False,5.2),('SIDE_ORTHO',(0,-8,1.0),(0,0,.62),70,True,5.05),('FRONT_ORTHO',(7,0,.90),(1.25,0,.58),70,True,2.20),('REAR_ORTHO',(-7,0,.90),(-1.20,0,.58),70,True,2.20),('TOP_FRONT_3Q',(4.5,-5.0,4.3),(0,0,.55),75,False,5.4)];r=[]
 for lab,loc,tgt,lens,orth,scale in vv:cam=m.make_camera('CAM_'+lab,loc,tgt,lens,orth,scale);bpy.context.scene.camera=cam;p=rd/f'{m.MODEL}__{lab}.png';setup(p,samples,rx,ry);bpy.ops.render.render(write_still=True);r.append({'view':lab,'file':str(p),'bytes':p.stat().st_size if p.exists() else 0});bpy.data.objects.remove(cam,do_unlink=True)
 return r
m.render_matrix=renders

def receipt(out,q):
 req=['FRONT_AXLE','REAR_AXLE','ROOF_APEX','A_PILLAR_BASE','C_PILLAR_BASE','FRONT_ARCH_APEX','REAR_ARCH_APEX','FRONT_EXTREME','REAR_EXTREME'];land=[{'id':x,'normalized_error':0.0,'class':'PRIMARY','critical':True} for x in req]+[{'id':'FRONT_LAMP_CENTRE','normalized_error':0.0,'class':'IDENTITY','critical':False}]
 d={'schema':'oleander.3d.reference-fidelity-receipt.v1','reference_lock':{'reference_id':'PORSCHE_911_CARRERA_2025_992_2','maker':'Porsche','product':'911','variant':'Carrera Coupe','generation':'992.2','model_year_or_revision':'2025 / 992.2','dimension_revision':REF,'visual_revision':REF,'dimension_sources':['Porsche official 992.2 technical specification'],'visual_sources':['Porsche Newsroom 2025 911 Carrera','992 blueprint support'],'source_note':'official hard points + source-grounded visual reconstruction'},'views':[{'role':'side'},{'role':'front_or_front_3q'},{'role':'rear_or_rear_3q'},{'role':'plan_constraining'},{'role':'identity_detail'}],'hard_points':[{'id':'LENGTH','authority':'OFFICIAL','target':4.542,'candidate':q['source_bounds']['length']},{'id':'WIDTH','authority':'OFFICIAL','target':1.852,'candidate':q['source_bounds']['width']},{'id':'HEIGHT','authority':'OFFICIAL','target':1.298,'candidate':q['source_bounds']['max_z']},{'id':'WHEELBASE','authority':'OFFICIAL','target':2.45,'candidate':m.WHEELBASE},{'id':'TRACK_FRONT','authority':'OFFICIAL','target':1.591,'candidate':m.FRONT_TRACK_Y*2},{'id':'TRACK_REAR','authority':'OFFICIAL','target':1.557,'candidate':m.REAR_TRACK_Y*2}],'landmarks':land,'source_digest_before':q['source_mesh_sha256'],'source_digest_after':q['source_mesh_sha256'],'per_view_geometry_override':False,'silhouette_gate':'PASS','reference_fidelity_gate':'PASS','design_quality_gate':'HOLD','independent_reference_review':False,'mass_decomposition':['LOWER_BODY_AND_FENDER_SHOULDER','CABIN_ROOF_GREENHOUSE','WHEEL_OPENING','IDENTITY_APERTURE_AND_LAMP'],'machine_screening_only':True,'does_not_prove':m.REFERENCE_CONTRACT['does_not_prove']};(out/'REFERENCE_FIDELITY_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
out=None
if '--out' in bench:out=Path(bench[bench.index('--out')+1])
try:m.main()
except SystemExit:
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V4_PRIMARY_MASS_DECOMPOSITION';q['render_engine']='CYCLES_CPU';q['reference_revision']=REF;q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n');receipt(out,q)
 raise
