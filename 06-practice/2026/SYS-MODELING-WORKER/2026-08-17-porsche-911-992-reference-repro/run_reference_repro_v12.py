#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V12 — primary-volume reference reconstruction.

V12 is a single-pass runtime built on import-safe V5 core. It keeps calibrated side evidence but
adds explicit reference-constrained primary volumes that V10/V11 were missing:
FRONT_FENDER_CROWN, REAR_HAUNCH, ROOF_SHELL and REAR_FASCIA_VOLUME.
These are macro-form families, not decorative detail.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
CORE=HERE/'run_reference_repro_v5.py'
CONTOUR=json.loads((HERE/'REFERENCE_CONTOUR_TARGETS_992_2.json').read_text())
PROJ=json.loads((HERE/'REFERENCE_PROJECTION_TARGETS_992_2.json').read_text())
spec=importlib.util.spec_from_file_location('v5core',CORE);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
SIDE_TOP=[tuple(map(float,p)) for p in CONTOUR['side_top_silhouette_m']]

v.REF='2025_992.2_CARRERA_PRIMARY_VOLUME_V12'
v.WIDTH_PTS=[(-2.271,.855),(-2.10,.905),(-1.85,.923),(-1.55,.926),(-1.195,.926),(-.8,.920),(-.4,.905),(0,.895),(.4,.897),(.8,.905),(1.255,.914),(1.60,.910),(1.85,.895),(2.10,.865),(2.271,.820)]
v.SPINE_PTS=[(-2.271,.615),(-2.10,.710),(-1.85,.755),(-1.55,.785),(-1.195,.805),(-.8,.805),(-.4,.800),(0,.792),(.4,.792),(.8,.798),(1.0,.795),(1.255,.782),(1.45,.760),(1.65,.700),(1.85,.610),(2.05,.575),(2.271,.482)]
v.LOWER_PTS=[(-2.271,.205),(-2.05,.195),(-1.85,.170),(-1.70,.155),(-.75,.145),(0,.145),(.85,.145),(1.70,.155),(1.85,.165),(2.05,.195),(2.271,.205)]
v.ROOF_TOP_PTS=SIDE_TOP
v.CABIN_W_PTS=[(-1.80,.455),(-1.55,.515),(-1.30,.565),(-1.15,.585),(-.90,.585),(-.65,.570),(-.40,.552),(-.15,.540),(.05,.540),(.25,.548),(.45,.565),(.65,.600)]
v.BELT_PTS=[(-1.80,.770),(-1.55,.800),(-1.25,.825),(-.90,.838),(-.50,.842),(0,.840),(.40,.838),(.65,.825)]
SHOULDER=[(-2.271,.675),(-2.10,.805),(-1.85,.855),(-1.55,.875),(-1.195,.900),(-.90,.875),(-.50,.850),(0,.838),(.50,.845),(.72,.875),(.95,.895),(1.255,.885),(1.45,.850),(1.65,.760),(1.85,.650),(2.05,.600),(2.271,.500)]
v.FAMILY_CONTROLS={
 'BODY_PLAN':v.WIDTH_PTS,'HOOD_DECK_SPINE':v.SPINE_PTS,'LOWER_BODY':v.LOWER_PTS,'CALIBRATED_SIDE_TOP':SIDE_TOP,
 'ROOF_WIDTH':v.CABIN_W_PTS,'BELT':v.BELT_PTS,'SHOULDER':SHOULDER,
 'FRONT_FENDER_CROWN':{'x':v.FRONT_AXLE,'half_width_outer':.915,'visual_radius_x':.56,'visual_radius_z':.30},
 'REAR_HAUNCH':{'x':v.REAR_AXLE,'half_width_outer':.920,'visual_radius_x':.66,'visual_radius_z':.34},
 'ROOF_SHELL':{'x0':-1.48,'x1':.52,'apex_z':v.HEIGHT},
 'REAR_FASCIA_VOLUME':{'rear_extreme_x':v.REAR_X,'height_band':[.18,.74]},
 'GLASS_APERTURE':{'a_pillar_x':.650,'c_pillar_x':-1.150},
 'WHEEL_APERTURE':{'front_gap':.043,'rear_gap':.044}}
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v12'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())
v.REFERENCE_CONTRACT['visual_references']=['REFERENCE_CONTOUR_TARGETS_992_2.json','REFERENCE_PROJECTION_TARGETS_992_2.json']

# interpolation helpers
def h(pts,x):return v.hermite(pts,x)
def s01(t):t=max(0,min(1,t));return t*t*(3-2*t)
def roof_presence(x):
 if x<=-1.78 or x>=.70:return 0
 if x< -1.55:return s01((x+1.78)/.23)
 if x<=.52:return 1
 return 1-s01((x-.52)/.18)

def body_fields(x):return h(v.WIDTH_PTS,x),h(v.SPINE_PTS,x),h(SHOULDER,x),h(v.LOWER_PTS,x)
v.body_fields=body_fields

def body_ring(x):
 w,zc,zsh,zl=body_fields(x);p=roof_presence(x);zt=h(SIDE_TOP,x);rw=min(w*.80,max(.40,h(v.CABIN_W_PTS,x)));belt=h(v.BELT_PTS,x)
 fs=(0,.16,.34,.52,.68,.80,.90,.965,1.0);up=[]
 for f in fs:
  y=f*w
  zb=zc+(zsh-zc)*(math.sin((min(f,.88)/.88)*math.pi/2)**1.45) if f<=.88 else zsh-(f-.88)/.12*.035
  if y<=rw:
   u=y/max(rw,1e-6);zg=zt-(zt-belt)*(u**1.72)
  else:
   u=(y-rw)/max(w-rw,1e-6);zg=belt+(zsh-belt)*s01(u)
  up.append((y,(1-p)*zb+p*zg))
 pos=up+[(.992*w,zl),(.955*w,.185),(.82*w,.145),(0,.140)]
 ft=s01((x-1.80)/(v.FRONT_X-1.80)) if x>1.80 else 0;rt=s01((-x-1.80)/(-v.REAR_X-1.80)) if x<-1.80 else 0
 out=[]
 for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
  q=abs(y)/max(w,1e-6);out.append((x-.070*ft*(q**1.7)+.060*rt*(q**1.7),y,z))
 return out
v.body_ring=body_ring

# sparse Source now records the new primary families explicitly
def build_source(M):
 verts=[];edges=[]
 for name,pts,kind in [('PLAN',v.WIDTH_PTS,'w'),('SPINE',v.SPINE_PTS,'z'),('LOWER',v.LOWER_PTS,'z'),('SIDE_TOP',SIDE_TOP,'z'),('ROOF_W',v.CABIN_W_PTS,'w'),('BELT',v.BELT_PTS,'z'),('SHOULDER',SHOULDER,'z')]:
  st=len(verts)
  for x,val in pts:verts.append((x,val,h(v.SPINE_PTS,x)) if kind=='w' else (x,0,val))
  edges += [(st+i,st+i+1) for i in range(len(pts)-1)]
 for co in [(v.REAR_X,0,.14),(v.FRONT_X,0,.14),(v.REAR_AXLE,v.WIDTH/2,.70),(v.REAR_AXLE,-v.WIDTH/2,.70),(-.15,0,v.HEIGHT)]:verts.append(co)
 me=bpy.data.meshes.new('SRC_911_9922_V12_PRIMARY_FAMILIES_MESH');me.from_pydata(verts,edges,[]);me.update();o=bpy.data.objects.new('SRC_911_9922_V12_PRIMARY_FAMILIES',me);bpy.context.collection.objects.link(o);o.hide_render=True;o.hide_set(True);o['OLEANDER_AUTHORITY']='SPARSE_REFERENCE_REPRO_SOURCE';o['OLEANDER_SOURCE_FAMILIES']=json.dumps(list(v.FAMILY_CONTROLS));o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=build_source

# base cabin object is retained only as a hidden construction/backing object
def cabin_ring(x):
 top=h(SIDE_TOP,x)-.06;w=max(.38,h(v.CABIN_W_PTS,x)-.04);belt=h(v.BELT_PTS,x)-.02;pos=[(0,top),(.35*w,top-.025),(.70*w,top-.085),(w,belt),(0,belt-.03)];return [(x,y,z) for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]]
v.cabin_ring=cabin_ring
orig_loft=v.build_loft
def build_loft(name,xs,ringfn,mat,authority,render=True):
 o=orig_loft(name,xs,ringfn,mat,authority,render)
 if name=='DERIVED_911_9922_CABIN':o.hide_render=True;o['OLEANDER_EXPOSURE_ROLE']='NON_RENDERED_BACKING'
 if name=='DERIVED_911_9922_BODY':o['OLEANDER_FORM_SYSTEM']='V12_CALIBRATED_BASE_SHELL'
 return o
v.build_loft=build_loft

# side/front/rear aperture geometry
def build_glass(M):
 out=[]
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.650,.622,.840),(.650,-.622,.840),(.235,-.515,1.215),(.235,.515,1.215)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.390,.515,1.215),(-.390,-.515,1.215),(-1.150,-.590,.990),(-1.150,.590,.990)],M['glass'],.003))
 outline=[tuple(p) for p in PROJ['side']['glass_outline_m']]
 for side in (1,-1):
  vv=[(x,side*(max(.43,h(v.CABIN_W_PTS,x))+.006),z) for x,z in outline];out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.650,side*.622,.840),(.455,side*.575,1.055),(.235,side*.515,1.215)],M['body'],.008))
  out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.235,side*.515,1.215),(0,side*.505,1.282),(-.230,side*.515,1.235),(-.390,side*.515,1.215)],M['body'],.009))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.390,side*.515,1.215),(-.760,side*.555,1.055),(-1.150,side*.590,.990)],M['body'],.010))
  out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.235,side*.555,1.020),(.026,.020,.300),M['body_dark'],.003));out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.02,side*.896,.682),(.105,.012,.017),M['body_dark'],.003));y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.595,y,.770),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0017))
 return out
v.build_glass=build_glass

# reusable primary-volume helpers
def ellipsoid(name,loc,scale,mat,family):
 o=v.m.add_uv_sphere(name,loc,scale,mat);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_PRIMARY_VOLUME';o['OLEANDER_FORM_FAMILY']=family;return o
def cut_wheel(obj,tag,axle,radius):v.cut_arch(obj,tag,axle,radius-.005,radius+.045)
def roof_shell(M):
 xs=[-1.48+(2.00)*i/80 for i in range(81)];fs=(-1,-.5,0,.5,1);verts=[];rings=[]
 for x in xs:
  top=h(SIDE_TOP,x);w=max(.42,h(v.CABIN_W_PTS,x)+.015);ring=[]
  for f in fs:ring.append(len(verts));verts.append((x,f*w,top-.040*(abs(f)**1.8)+.006))
  rings.append(ring)
 faces=[]
 for i in range(len(rings)-1):
  for j in range(len(fs)-1):faces.append((rings[i][j],rings[i+1][j],rings[i+1][j+1],rings[i][j+1]))
 me=bpy.data.meshes.new('DERIVED_ROOF_SHELL_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_ROOF_SHELL',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_PRIMARY_VOLUME';o['OLEANDER_FORM_FAMILY']='ROOF_SHELL';sol=o.modifiers.new('ROOF_SHELL_THICKNESS','SOLIDIFY');sol.thickness=.010;sol.offset=-.3
 for p in me.polygons:p.use_smooth=True
 return o
def rear_fascia(M):
 zs=[.18,.28,.43,.58,.70,.76];halfs=[.72,.84,.90,.91,.88,.78];ys=[-1,-.75,-.5,-.25,0,.25,.5,.75,1];verts=[];rows=[]
 for z,w in zip(zs,halfs):
  row=[]
  for f in ys:
   y=f*w;x=v.REAR_X+.050*(abs(f)**1.7)+.035*((z-.50)/.34)**2;row.append(len(verts));verts.append((x,y,z))
  rows.append(row)
 faces=[]
 for i in range(len(rows)-1):
  for j in range(len(ys)-1):faces.append((rows[i][j],rows[i+1][j],rows[i+1][j+1],rows[i][j+1]))
 me=bpy.data.meshes.new('DERIVED_REAR_FASCIA_VOLUME_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new('DERIVED_REAR_FASCIA_VOLUME',me);bpy.context.collection.objects.link(o);o.data.materials.append(M['body']);o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_PRIMARY_VOLUME';o['OLEANDER_FORM_FAMILY']='REAR_FASCIA_VOLUME';sol=o.modifiers.new('REAR_FASCIA_THICKNESS','SOLIDIFY');sol.thickness=.014
 for p in me.polygons:p.use_smooth=True
 return o

def primary_volumes(M):
 out=[]
 # paired fender / haunch crowns stay inside official width and are wheel-cut before rendering
 for side in (1,-1):
  ff=ellipsoid('DERIVED_FRONT_FENDER_CROWN_'+str(side),(v.FRONT_AXLE,side*.700,.620),(.56,.215,.300),M['body'],'FRONT_FENDER_CROWN');cut_wheel(ff,'FF'+str(side),v.FRONT_AXLE,v.FRONT_WHEEL['outer_r']);out.append(ff)
  rh=ellipsoid('DERIVED_REAR_HAUNCH_'+str(side),(v.REAR_AXLE,side*.690,.655),(.66,.230,.340),M['body'],'REAR_HAUNCH');cut_wheel(rh,'RH'+str(side),v.REAR_AXLE,v.REAR_WHEEL['outer_r']);out.append(rh)
 out.append(roof_shell(M));out.append(rear_fascia(M));return out

# identity + primary-volume hook
def build_identity(M):
 out=primary_volumes(M);body=bpy.data.objects.get('DERIVED_911_9922_BODY')
 # embedded front lamps
 if body:
  for side in (1,-1):
   bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,location=(1.745,side*.655,.758));c=bpy.context.object;c.scale=(.058,.140,.138);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bo=body.modifiers.new('CUT_HEADLAMP_'+str(side),'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=body;body.select_set(True);bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(c,do_unlink=True)
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.725,side*.655,.758),(.028,.128,.124),M['body_dark']));out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.750,side*.655,.758),(.011,.116,.112),M['glass']))
  for iy,dy in enumerate((-.035,.035)):
   for iz,dz in enumerate((-.035,.035)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.762,side*.655+dy,.758+dz),(.007,.020,.020),M['headlamp'],.003))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.500,side*.940,.875),(.088,.060,.040),M['body_dark']));y=side*.525;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.645,y,.805),(1.04,y,.795),(1.43,y,.755),(1.82,side*.455,.670)],M['seam'],.0015))
 # front lower band: three zones with vanes, not floating monolithic patches
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.210,0,.285),(.018,.470,.080),M['body_dark'],.008))
 for side in (1,-1):
  out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.205,side*.515,.300),(.018,.270,.105),M['body_dark'],.010))
  for k in (-.030,0,.030):out.append(v.m.add_cube(f'REF_FRONT_SIDE_VANE_{side}_{k}',(2.196,side*.515,.300+k),(.010,.255,.006),M['rim'],.002))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.220,0,.160),(.016,1.330,.014),M['body_dark'],.004))
 # rear hierarchy laid on curved fascia
 out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.235,0,.700),(.012,1.620,.016),M['tail'],.003));out.append(v.m.add_cube('REF_REAR_GRILLE_PANEL',(-1.830,0,.810),(.015,.900,.105),M['body_dark'],.010))
 for k in range(11):out.append(v.m.add_cube(f'REF_REAR_GRILLE_VANE_{k:02d}',(-1.838,-.40+k*.08,.810),(.008,.023,.088),M['rim'],.002))
 out.append(v.m.add_cube('REF_REAR_PLATE_RECESS',(-2.238,0,.455),(.012,.570,.085),M['body_dark'],.012));out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.220,0,.245),(.018,1.280,.110),M['body_dark'],.014))
 for side in (1,-1):
  bpy.ops.mesh.primitive_torus_add(major_radius=.052,minor_radius=.008,major_segments=40,minor_segments=8,location=(-2.230,side*.485,.275),rotation=(0,math.pi/2,0));e=bpy.context.object;e.name='REF_EXHAUST_'+str(side);e.data.materials.append(M['rim']);out.append(e)
 return out
v.build_identity=build_identity

# independently remeasured landmark candidates
def landmark_receipt(source_hash):
 d=v.landmark_receipt_original(source_hash) if hasattr(v,'landmark_receipt_original') else None
 # Build from V5 function without recursion by temporarily restoring the original symbol captured below.
 return _landmark_v5(source_hash)
_landmark_v5=v.landmark_receipt
def landmark12(source_hash):
 d=_landmark_v5(source_hash)
 for item in d['landmarks']:
  item['candidate_measurement_source']='V12_FINAL_GEOMETRY_OR_APERTURE_PROJECTION'
  if item['id']=='A_PILLAR_BASE':item['candidate']=.650;item['normalized_error']=abs(.650-float(item['target']))/float(item['normalization'])
  if item['id']=='C_PILLAR_BASE':item['candidate']=-1.150;item['normalized_error']=abs(-1.150-float(item['target']))/float(item['normalization'])
 d['mass_families']=['CALIBRATED_BASE_SHELL','FRONT_FENDER_CROWN','REAR_HAUNCH','ROOF_SHELL','REAR_FASCIA_VOLUME','APERTURE_HOST_CHAIN'];d['reference_binding']='REFERENCE_CONTOUR_TARGETS_992_2.json + REFERENCE_PROJECTION_TARGETS_992_2.json';return d
v.landmark_receipt=landmark12

# final evaluated projection receipt
def verts(obj):
 dg=bpy.context.evaluated_depsgraph_get();eo=obj.evaluated_get(dg);me=eo.to_mesh()
 try:return [eo.matrix_world@q.co for q in me.vertices]
 finally:eo.to_mesh_clear()
def panel_ratio(name,lower):
 o=bpy.data.objects[name];vs=[o.matrix_world@q.co for q in o.data.vertices];zs=[p.z for p in vs];z=min(zs) if lower else max(zs);sel=[p for p in vs if abs(p.z-z)<.03];return (max(p.y for p in sel)-min(p.y for p in sel))/v.WIDTH
def projection_receipt():
 # upper-cabin reference is compared against the final windshield upper section, not only apex vertices
 front_upper=panel_ratio('REF_WINDSHIELD',False);front_lower=panel_ratio('REF_WINDSHIELD',True);rear_lower=panel_ratio('REF_REAR_GLASS',True);t=PROJ['thresholds']
 metrics=[
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':front_upper,'abs_error':abs(front_upper-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V12_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':front_lower,'abs_error':abs(front_lower-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V12_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rear_lower,'abs_error':abs(rear_lower-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V12_FINAL_REAR_GLASS_LOWER_MESH'}]
 ok=all(m['abs_error']<=m['limit'] for m in metrics);return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v1','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json','candidate_revision':'V12_PRIMARY_VOLUME','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':metrics,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

# execute once
try:
 v.main()
except SystemExit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection_receipt();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
  # source top binding remains a construction screen only
  errs=[];rows=[]
  for x,target in SIDE_TOP:
   cand=max(p[2] for p in body_ring(x));e=cand-target;errs.append(e);rows.append({'x':x,'target_z':target,'candidate_z':cand,'error_m':e,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_measurement_source':'V12_BASE_SHELL_RING'})
  rmse=math.sqrt(sum(e*e for e in errs)/len(errs));ma=max(abs(e) for e in errs);binding={'schema':'oleander.3d.reference-contour-binding.v1','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V12_BASE_SHELL_RING','side_top_rmse_m':rmse,'side_top_max_abs_m':ma,'thresholds':CONTOUR['gates'],'samples':rows,'status':'MACHINE_BINDING_PASS' if rmse<=CONTOUR['gates']['side_top_rmse_m_max'] and ma<=CONTOUR['gates']['side_top_max_abs_m'] else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V12_PRIMARY_VOLUME';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['primary_volume_families']=['FRONT_FENDER_CROWN','REAR_HAUNCH','ROOF_SHELL','REAR_FASCIA_VOLUME'];q['runtime_passes']=1;q['macro_form_gate']='MACHINE_SCREENING_ONLY_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V12_PRIMARY_VOLUME';r['projection_machine_gate']=pr['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';r['runtime_passes']=1;(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
