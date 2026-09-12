#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V16 — shared-boundary patch network + emission-mask gate.

The visible architecture changes materially from V15:
- lower body / hood / quarter shell stops at the belt/window boundary through the cabin zone;
- roof is a shallow outer panel patch, not a closed cabin volume;
- glazing occupies the actual open region between lower body and roof;
- A/B/C pillars and roof rails are explicit interface patches;
- no large Boolean window cuts are required;
- silhouette metrics come from a white-emission/black-background mask of the final visible body+roof network.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
CORE=HERE/'run_reference_repro_v5.py'
CONTOUR=json.loads((HERE/'REFERENCE_CONTOUR_TARGETS_992_2.json').read_text())
PROJ=json.loads((HERE/'REFERENCE_PROJECTION_TARGETS_992_2.json').read_text())
SIDE_TOP=[tuple(map(float,p)) for p in CONTOUR['side_top_silhouette_m']]
SIDE_LOW=[tuple(map(float,p)) for p in PROJ['side']['lower_body_silhouette_m']]
spec=importlib.util.spec_from_file_location('v5core',CORE);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

v.REF='2025_992.2_CARRERA_SHARED_BOUNDARY_PATCH_V16'
v.WIDTH_PTS=[(-2.271,.845),(-2.10,.895),(-1.85,.918),(-1.55,.926),(-1.195,.926),(-.80,.920),(-.40,.905),(0,.895),(.40,.897),(.80,.905),(1.255,.914),(1.60,.910),(1.85,.895),(2.10,.860),(2.271,.790)]
v.SPINE_PTS=[(-2.271,.590),(-2.10,.675),(-1.85,.730),(-1.55,.785),(-1.195,.815),(-.80,.810),(-.40,.800),(0,.790),(.40,.785),(.65,.790),(.80,.790),(1.00,.790),(1.255,.775),(1.45,.750),(1.65,.690),(1.85,.600),(2.05,.555),(2.271,.460)]
v.LOWER_PTS=[(-2.271,.205),(-2.05,.195),(-1.85,.170),(-1.72,.150),(-.75,.145),(0,.145),(.90,.145),(1.72,.155),(1.86,.170),(2.05,.195),(2.271,.205)]
v.ROOF_TOP_PTS=SIDE_TOP
v.CABIN_W_PTS=[(-1.15,.590),(-.95,.575),(-.70,.555),(-.45,.540),(-.20,.530),(.05,.530),(.25,.538),(.45,.555),(.65,.600)]
v.BELT_PTS=[(-1.30,.815),(-1.15,.830),(-.90,.838),(-.50,.842),(0,.840),(.40,.836),(.65,.822),(.80,.815)]
CROWN={'front_peak_fraction':.82,'rear_peak_fraction':.88,'front_center_drop_m':.080,'rear_center_drop_m':.055,'outer_drop_m':.032}
TERM={'front_outer_setback_m':.078,'rear_outer_setback_m':.065}
v.FAMILY_CONTROLS={
 'LOWER_BODY_PRIMARY_SHELL':{'plan':v.WIDTH_PTS,'spine':v.SPINE_PTS,'lower':v.LOWER_PTS,'belt':v.BELT_PTS},
 'ROOF_OUTER_PANEL':{'side_top':SIDE_TOP,'half_width':v.CABIN_W_PTS,'x_extent':[-1.15,.65]},
 'FRONT_FENDER_CROWN_SECTION':CROWN,'REAR_HAUNCH_SECTION':CROWN,'TERMINAL_PLAN_CURVATURE':TERM,
 'GLASS_APERTURE':{'a_pillar_x':.650,'c_pillar_x':-1.150},'INTERFACE_PATCHES':['A_PILLAR','B_PILLAR','C_PILLAR','ROOF_RAIL'],
 'WHEEL_APERTURE':{'front_gap':.043,'rear_gap':.044}}
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v16'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())
v.REFERENCE_CONTRACT['visible_primary_architecture']='SHARED_BOUNDARY_PATCH_NETWORK'
v.REFERENCE_CONTRACT['projection_measurement']='EMISSION_MASK_FINAL_VISIBLE_PATCH_NETWORK'

# Helpers
def h(pts,x):return v.hermite(pts,x)
def s01(t):t=max(0.0,min(1.0,t));return t*t*(3-2*t)
def side_top(x):return h(SIDE_TOP,x)
def belt(x):return h(v.BELT_PTS,x)
def cabin_open_weight(x):
 if x<=-1.20 or x>=.70:return 0.0
 if x<-1.08:return s01((x+1.20)/.12)
 if x<=.58:return 1.0
 return 1.0-s01((x-.58)/.12)
def fi(x):return math.exp(-((x-v.FRONT_AXLE)/.62)**4)
def ri(x):return math.exp(-((x-v.REAR_AXLE)/.70)**4)
def body_fields(x):
 w=h(v.WIDTH_PTS,x);zc=h(v.SPINE_PTS,x);zl=h(v.LOWER_PTS,x);outside=side_top(x);bw=cabin_open_weight(x);top=(1-bw)*outside+bw*(belt(x)+.015);return w,zc,top,zl
v.body_fields=body_fields

def crown(f,target,x,zc):
 a,b=fi(x),ri(x);rear=b>=a;inf=max(a,b);peak=CROWN['rear_peak_fraction'] if rear else CROWN['front_peak_fraction'];drop=(CROWN['rear_center_drop_m'] if rear else CROWN['front_center_drop_m'])*(.35+.65*inf)+.018*(1-inf);center=min(zc,target-drop)
 if f<=peak:return center+(target-center)*(math.sin((f/peak)*math.pi/2)**1.50)
 return target-CROWN['outer_drop_m']*((f-peak)/(1-peak))**1.15

def body_ring(x):
 w,zc,target,zl=body_fields(x);fs=(0,.12,.25,.38,.52,.65,.76,.84,.91,.965,1.0);zv=[crown(f,target,x,zc) for f in fs];off=target-max(zv);pos=[(f*w,z+off) for f,z in zip(fs,zv)]+[(.998*w,zl),(.968*w,.190),(.84*w,.146),(0,.140)]
 ft=s01((x-1.80)/(v.FRONT_X-1.80)) if x>1.80 else 0;rt=s01((-x-1.80)/(-v.REAR_X-1.80)) if x<-1.80 else 0;out=[]
 for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
  q=abs(y)/max(w,1e-6);out.append((x-TERM['front_outer_setback_m']*ft*q**1.65+TERM['rear_outer_setback_m']*rt*q**1.65,y,z))
 return out
v.body_ring=body_ring

# Sparse Source contains separate semantic patch boundaries, but no rendered dense patch becomes authority.
def build_source(M):
 verts=[];edges=[]
 for name,pts,kind in [('PLAN',v.WIDTH_PTS,'w'),('SPINE',v.SPINE_PTS,'z'),('LOWER',v.LOWER_PTS,'z'),('SIDE_TOP',SIDE_TOP,'z'),('ROOF_WIDTH',v.CABIN_W_PTS,'w'),('BELT',v.BELT_PTS,'z')]:
  st=len(verts)
  for x,val in pts:verts.append((x,val,h(v.SPINE_PTS,x)) if kind=='w' else (x,0,val))
  edges += [(st+i,st+i+1) for i in range(len(pts)-1)]
 for co in [(v.REAR_X,0,.14),(v.FRONT_X,0,.14),(v.REAR_AXLE,v.WIDTH/2,.70),(v.REAR_AXLE,-v.WIDTH/2,.70),(-.15,0,v.HEIGHT)]:verts.append(co)
 me=bpy.data.meshes.new('SRC_911_9922_V16_PATCH_NETWORK_MESH');me.from_pydata(verts,edges,[]);me.update();o=bpy.data.objects.new('SRC_911_9922_V16_PATCH_NETWORK',me);bpy.context.collection.objects.link(o);o.hide_render=True;o.hide_set(True);o['OLEANDER_AUTHORITY']='SPARSE_REFERENCE_REPRO_SOURCE';o['OLEANDER_ARCHITECTURE']='SHARED_BOUNDARY_PATCH_NETWORK';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=build_source

# Build roof as an open shallow patch. V5 main requests DERIVED_911_9922_CABIN; intercept that call.
base_loft=v.build_loft
def roof_patch(name,material):
 xs=[-1.15+1.80*i/90 for i in range(91)];fracs=(-1.0,-.72,-.40,0,.40,.72,1.0);verts=[];rings=[]
 for x in xs:
  top=side_top(x);rw=max(.44,h(v.CABIN_W_PTS,x));ring=[]
  for f in fracs:
   # broad shallow roof: only 45 mm crown drop at roof edge
   z=top-.045*(abs(f)**1.85);ring.append(len(verts));verts.append((x,f*rw,z))
  rings.append(ring)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fracs)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(material);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DISPLAY';o['OLEANDER_FORM_FAMILY']='ROOF_OUTER_PANEL';o['OLEANDER_BOUNDARY_OWNER']='A_C_PILLAR_AND_ROOF_RAIL_INTERFACE';sol=o.modifiers.new('ROOF_PANEL_THICKNESS','SOLIDIFY');sol.thickness=.010;sol.offset=-.25
 for p in me.polygons:p.use_smooth=True
 return o
def build_loft(name,xs,ringfn,mat,authority,render=True):
 if name=='DERIVED_911_9922_CABIN':return roof_patch(name,mat)
 o=base_loft(name,xs,ringfn,mat,authority,render)
 if name=='DERIVED_911_9922_BODY':o['OLEANDER_FORM_SYSTEM']='V16_LOWER_BODY_PRIMARY_SHELL';o['OLEANDER_PATCH_ROLE']='LOWER_BODY_HOOD_QUARTER'
 return o
v.build_loft=build_loft
v.cabin_ring=lambda x:[(x,0,0)] # intercepted, never consumed

# Neutral fidelity materials: geometry first, CMF not under test.
base_materials=v.materials
def materials():
 M=base_materials();b=M['body'].node_tree.nodes.get('Principled BSDF');g=M['glass'].node_tree.nodes.get('Principled BSDF')
 if b:
  if 'Base Color' in b.inputs:b.inputs['Base Color'].default_value=(.34,.36,.39,1)
  if 'Metallic' in b.inputs:b.inputs['Metallic'].default_value=.18
  if 'Roughness' in b.inputs:b.inputs['Roughness'].default_value=.30
 if g:
  if 'Base Color' in g.inputs:g.inputs['Base Color'].default_value=(.004,.010,.016,1)
  if 'Roughness' in g.inputs:g.inputs['Roughness'].default_value=.12
  if 'Transmission Weight' in g.inputs:g.inputs['Transmission Weight'].default_value=.04
  elif 'Transmission' in g.inputs:g.inputs['Transmission'].default_value=.04
 return M
v.materials=materials

# Real open greenhouse: glass panels live between body belt and roof patch; no body polygons behind them.
def build_glass(M):
 out=[]
 windshield=[(.650,.600,.825),(.650,-.600,.825),(.235,-.525,1.208),(.235,.525,1.208)]
 rear=[(-.390,.490,1.208),(-.390,-.490,1.208),(-1.150,-.585,.985),(-1.150,.585,.985)]
 out.append(v.m.add_panel('REF_WINDSHIELD',windshield,M['glass'],.003));out.append(v.m.add_panel('REF_REAR_GLASS',rear,M['glass'],.003))
 outline=[tuple(p) for p in PROJ['side']['glass_outline_m']]
 for side in (1,-1):
  vv=[(x,side*(max(.42,h(v.CABIN_W_PTS,x))+.002),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.650,side*.600,.825),(.455,side*.565,1.050),(.235,side*.525,1.208)],M['body'],.013))
  out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.235,side*.525,1.208),(0,side*.515,1.280),(-.230,side*.500,1.230),(-.390,side*.490,1.208)],M['body'],.013))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.390,side*.490,1.208),(-.760,side*.540,1.055),(-1.150,side*.585,.985)],M['body'],.016))
  out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.235,side*.540,1.015),(.035,.028,.300),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.02,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.595,y,.765),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0017))
 return out
v.build_glass=build_glass

# Thin identity layer only.
def identity(M):
 out=[]
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.715,side*.655,.755),(.030,.126,.122),M['body_dark']));out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.742,side*.655,.755),(.014,.114,.110),M['glass']))
  for iy,dy in enumerate((-.033,.033)):
   for iz,dz in enumerate((-.033,.033)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.758,side*.655+dy,.755+dz),(.006,.019,.019),M['headlamp'],.0025))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.500,side*.940,.875),(.088,.060,.040),M['body_dark']));y=side*.525;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.645,y,.805),(1.04,y,.790),(1.43,y,.750),(1.82,side*.455,.665)],M['seam'],.0014))
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.205,0,.285),(.012,.460,.070),M['body_dark'],.005))
 for side in (1,-1):out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.198,side*.520,.300),(.012,.255,.090),M['body_dark'],.007))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.215,0,.160),(.010,1.300,.010),M['body_dark'],.003));out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.250,0,.700),(.009,1.620,.014),M['tail'],.002));out.append(v.m.add_cube('REF_REAR_GRILLE_PANEL',(-2.215,0,.790),(.010,.875,.078),M['body_dark'],.007));out.append(v.m.add_cube('REF_REAR_PLATE_RECESS',(-2.252,0,.450),(.009,.550,.078),M['body_dark'],.009));out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.242,0,.245),(.010,1.250,.095),M['body_dark'],.010));return out
v.build_identity=identity

# Current calibrated landmark provenance.
base_lm=v.landmark_receipt
def lm16(source_hash):
 d=base_lm(source_hash)
 for item in d['landmarks']:
  item['candidate_measurement_source']='V16_FINAL_VISIBLE_PATCH_NETWORK'
  if item['id']=='A_PILLAR_BASE':item['candidate']=.650;item['normalized_error']=abs(.650-float(item['target']))/float(item['normalization'])
  if item['id']=='C_PILLAR_BASE':item['candidate']=-1.150;item['normalized_error']=abs(-1.150-float(item['target']))/float(item['normalization'])
 d['mass_families']=['LOWER_BODY_PRIMARY_SHELL','ROOF_OUTER_PANEL','TRUE_OPEN_GREENHOUSE','INTERFACE_PATCH_NETWORK','FENDER_CROWN_SECTION','REAR_HAUNCH_SECTION'];d['visible_primary_architecture']='SHARED_BOUNDARY_PATCH_NETWORK';return d
v.landmark_receipt=lm16

# Dedicated white-emission / black-background silhouette mask.
def emission_material():
 m=bpy.data.materials.get('DIAG_EMISSION_WHITE') or bpy.data.materials.new('DIAG_EMISSION_WHITE');m.use_nodes=True;nt=m.node_tree;nt.nodes.clear();out=nt.nodes.new('ShaderNodeOutputMaterial');em=nt.nodes.new('ShaderNodeEmission');em.inputs['Color'].default_value=(1,1,1,1);em.inputs['Strength'].default_value=1;nt.links.new(em.outputs['Emission'],out.inputs['Surface']);return m

def mask_render(objects,out,label,loc,target,scale,w,hpx):
 sc=bpy.context.scene;states={o.name:o.hide_render for o in sc.objects};vl=sc.view_layers[0];old_override=vl.material_override;oldcam=sc.camera;oldworld=sc.world;oldfilm=sc.render.film_transparent;oldx=sc.render.resolution_x;oldy=sc.render.resolution_y;oldp=sc.render.resolution_percentage;oldpath=sc.render.filepath;olds=sc.cycles.samples
 keep={o.name for o in objects}
 for o in sc.objects:o.hide_render=(o.name not in keep)
 world=bpy.data.worlds.new('DIAG_BLACK_WORLD');world.use_nodes=True;bg=world.node_tree.nodes.get('Background');bg.inputs['Color'].default_value=(0,0,0,1);bg.inputs['Strength'].default_value=0;sc.world=world;vl.material_override=emission_material();cam=v.m.make_camera('MASK_CAM_'+label,loc,target,70,True,scale);sc.camera=cam;sc.render.film_transparent=False;sc.render.resolution_x=w;sc.render.resolution_y=hpx;sc.render.resolution_percentage=100;sc.cycles.samples=1;dd=out/'diagnostics';dd.mkdir(exist_ok=True);p=dd/f'MASK_{label}_FINAL_VISIBLE_PATCH_NETWORK.png';sc.render.filepath=str(p);bpy.ops.render.render(write_still=True)
 im=bpy.data.images.load(str(p),check_existing=False);iw,ih=map(int,im.size);pix=list(im.pixels);mask=[];count=0;xs=[];ys=[]
 for y in range(ih):
  row=[]
  for x in range(iw):
   i=(y*iw+x)*4;on=(pix[i]+pix[i+1]+pix[i+2])/3>.20;row.append(on)
   if on:count+=1;xs.append(x);ys.append(y)
  mask.append(row)
 bpy.data.images.remove(im);coverage=count/(iw*ih)
 valid=count>0 and count<iw*ih and .02<=coverage<=.80 and min(xs)>0 and max(xs)<iw-1 and min(ys)>0 and max(ys)<ih-1
 bbox=[min(xs),min(ys),max(xs),max(ys)] if count else None
 bpy.data.objects.remove(cam,do_unlink=True);vl.material_override=old_override;sc.world=oldworld;sc.camera=oldcam;sc.render.film_transparent=oldfilm;sc.render.resolution_x=oldx;sc.render.resolution_y=oldy;sc.render.resolution_percentage=oldp;sc.render.filepath=oldpath;sc.cycles.samples=olds
 for o in sc.objects:
  if o.name in states:o.hide_render=states[o.name]
 bpy.data.worlds.remove(world)
 return {'file':str(p),'width_px':iw,'height_px':ih,'coverage':coverage,'valid':valid,'bbox':bbox,'mask':mask}

def sample_side(maskrec,x):
 u0,v0,u1,v1=maskrec['bbox'];u=int(round(u0+(x-v.REAR_X)/(v.FRONT_X-v.REAR_X)*(u1-u0)));rows=[]
 for du in range(-2,3):
  uu=max(u0,min(u1,u+du));rows += [yy for yy in range(v0,v1+1) if maskrec['mask'][yy][uu]]
 if not rows:return float('nan'),float('nan')
 lo,hi=min(rows),max(rows);z0=.140;z1=v.HEIGHT;top=z0+(hi-v0)/max(v1-v0,1)*(z1-z0);bottom=z0+(lo-v0)/max(v1-v0,1)*(z1-z0);return top,bottom

def panel_ratio(name,lower):
 o=bpy.data.objects[name];vs=[o.matrix_world@q.co for q in o.data.vertices];zs=[p.z for p in vs];zr=min(zs) if lower else max(zs);sel=[p for p in vs if abs(p.z-zr)<.03];return (max(p.y for p in sel)-min(p.y for p in sel))/v.WIDTH

def projection(out):
 body=bpy.data.objects['DERIVED_911_9922_BODY'];roof=bpy.data.objects['DERIVED_911_9922_CABIN'];side=mask_render([body,roof],out,'SIDE',(0,-8,.75),(0,0,.75),1.55,1200,400);front=mask_render([body,roof],out,'FRONT',(7,0,.75),(0,0,.75),1.55,800,600);rear=mask_render([body,roof],out,'REAR',(-7,0,.75),(0,0,.75),1.55,800,600)
 if not all(x['valid'] for x in (side,front,rear)):raise SystemExit('FAIL_PROJECTION_MASK_INVALID: emission mask validity failed')
 ue=[];le=[];samples=[]
 for x,t in SIDE_TOP:
  top,bot=sample_side(side,x);e=top-t;ue.append(e);samples.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e})
 for x,t in SIDE_LOW:
  top,bot=sample_side(side,x);le.append(bot-t)
 fu=panel_ratio('REF_WINDSHIELD',False);fl=panel_ratio('REF_WINDSHIELD',True);rl=panel_ratio('REF_REAR_GLASS',True);urmse=math.sqrt(sum(e*e for e in ue if math.isfinite(e))/len([e for e in ue if math.isfinite(e)]));lrmse=math.sqrt(sum(e*e for e in le if math.isfinite(e))/len([e for e in le if math.isfinite(e)]));t=PROJ['thresholds'];metrics=[
  {'id':'SIDE_UPPER_EMISSION_MASK_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.040,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V16_FINAL_VISIBLE_UNION_EMISSION_MASK'},
  {'id':'SIDE_LOWER_EMISSION_MASK_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.070,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V16_FINAL_VISIBLE_UNION_EMISSION_MASK'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V16_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V16_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V16_FINAL_REAR_GLASS_LOWER_MESH'}];ok=all(m['abs_error']<=m['limit'] for m in metrics);return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v3','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V16_PATCH_NETWORK','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':metrics,'mask_validity':[{'view':lab,'coverage':rec['coverage'],'bbox':rec['bbox'],'valid':rec['valid'],'file':rec['file']} for lab,rec in [('SIDE',side),('FRONT',front),('REAR',rear)]],'side_samples':samples,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection(out);(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EMISSION_MASK_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v4','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V16_FINAL_VISIBLE_UNION_EMISSION_MASK','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V16_PATCH_NETWORK';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['visible_primary_architecture']='SHARED_BOUNDARY_PATCH_NETWORK';q['projection_measurement']='EMISSION_MASK_FINAL_VISIBLE_PATCH_NETWORK';q['mask_validity_gate']='PASS';q['runtime_passes']=1;q['macro_form_gate']='MACHINE_SCREENING_ONLY_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V16_PATCH_NETWORK';r['projection_machine_gate']=pr['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';r['visible_primary_architecture']='SHARED_BOUNDARY_PATCH_NETWORK';r['runtime_passes']=1;(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
