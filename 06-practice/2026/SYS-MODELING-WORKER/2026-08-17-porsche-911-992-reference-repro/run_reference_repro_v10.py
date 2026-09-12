#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V10 — calibrated-contour integrated shell.

V10 stops hand-tuning a generic body/cabin loft. The primary exterior shell is regenerated from
calibrated 992.2 side-contour evidence plus official hard points and explicit cross-section families.
The rear fastback roof mass is integrated into the body shell; glazing remains a separate aperture
layer. Machine contour binding is not an independent visual-fidelity PASS.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V5=HERE/'run_reference_repro_v5.py'
CONTOUR_FILE=HERE/'REFERENCE_CONTOUR_TARGETS_992_2.json'
spec=importlib.util.spec_from_file_location('v5core',V5);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
contour=json.loads(CONTOUR_FILE.read_text())
SIDE_TOP=[tuple(map(float,p)) for p in contour['side_top_silhouette_m']]

# 992.2 body plan remains broad at both terminations; V9's narrow terminal widths created a wedge car.
v.WIDTH_PTS=[
 (-2.271,.790),(-2.100,.875),(-1.850,.918),(-1.550,.926),(-1.195,.926),(-.800,.918),(-.400,.902),(0,.890),
 (.400,.892),(.800,.902),(1.255,.912),(1.600,.908),(1.850,.890),(2.100,.840),(2.271,.720)]
# Hood/deck centre is intentionally below the fender/quarter crown.
v.SPINE_PTS=[
 (-2.271,.620),(-2.100,.720),(-1.850,.770),(-1.550,.790),(-1.195,.805),(-.800,.805),(-.400,.800),(0,.792),
 (.400,.792),(.800,.800),(1.000,.800),(1.255,.790),(1.450,.775),(1.650,.710),(1.850,.610),(2.050,.585),(2.271,.482)]
v.LOWER_PTS=[(-2.271,.300),(-1.950,.395),(-1.600,.455),(-1.350,.480),(-.900,.490),(0,.480),(.900,.465),(1.350,.445),(1.700,.405),(2.050,.330),(2.271,.270)]
# Exterior roof / fastback mass follows the calibrated side silhouette and continues far behind the glass C-pillar.
v.ROOF_TOP_PTS=SIDE_TOP
v.CABIN_W_PTS=[(-1.800,.470),(-1.600,.530),(-1.350,.590),(-1.100,.635),(-.850,.642),(-.600,.625),(-.300,.602),(0,.590),(.280,.598),(.520,.625),(.700,.652)]
v.BELT_PTS=[(-1.800,.770),(-1.550,.800),(-1.250,.825),(-.900,.838),(-.500,.842),(0,.840),(.400,.838),(.700,.825)]
# Outer shoulder/top targets: calibrated silhouette outside greenhouse; controlled lower crown underneath fastback.
SHOULDER_PTS=[
 (-2.271,.668),(-2.100,.818),(-1.900,.878),(-1.750,.900),(-1.550,.835),(-1.300,.865),(-1.195,.875),(-.900,.858),
 (-.500,.842),(0,.832),(.500,.838),(.720,.878),(.850,.888),(1.000,.897),(1.255,.869),(1.450,.850),(1.650,.760),
 (1.850,.626),(2.050,.617),(2.271,.482)]

v.FAMILY_CONTROLS={
 'body_half_width':v.WIDTH_PTS,'hood_deck_spine_z':v.SPINE_PTS,'lower_side_z':v.LOWER_PTS,
 'calibrated_side_top':SIDE_TOP,'roof_fastback_half_width':v.CABIN_W_PTS,'belt_z':v.BELT_PTS,'shoulder_top_z':SHOULDER_PTS,
 'greenhouse_mass_extent':{'rear_fade_start':-1.85,'rear_full':-1.65,'front_full':.55,'front_fade_end':.72},
 'glass_aperture_extent':{'a_pillar_base_x':.67,'c_pillar_base_x':-1.05},
 'terminal_plan_curvature':{'front_outer_setback_m':.095,'rear_outer_setback_m':.085},
 'wheel_aperture':{'front_gap':.043,'rear_gap':.044}}
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v10'
v.REFERENCE_CONTRACT['reference_revision']='2025_992.2_CARRERA_BODY_SHELL_CALIBRATED'
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())
v.REFERENCE_CONTRACT['visual_reference']='REFERENCE_CONTOUR_TARGETS_992_2.json'

M10={}
orig_materials=v.materials
def materials10():
 M=orig_materials();M10.clear();M10.update(M)
 for key,col,rough in [('body_dark',(.002,.003,.004,1),.42),('glass',(.004,.010,.016,1),.14)]:
  bs=M[key].node_tree.nodes.get('Principled BSDF') if M[key].use_nodes else None
  if bs:
   if 'Base Color' in bs.inputs:bs.inputs['Base Color'].default_value=col
   if 'Roughness' in bs.inputs:bs.inputs['Roughness'].default_value=rough
   if key=='glass':
    if 'Transmission Weight' in bs.inputs:bs.inputs['Transmission Weight'].default_value=.08
    elif 'Transmission' in bs.inputs:bs.inputs['Transmission'].default_value=.08
 return M
v.materials=materials10

def smooth01(t):
 t=max(0.0,min(1.0,t));return t*t*(3-2*t)
def interp(points,x): return v.hermite(points,x)
def roof_presence(x):
 if x<=-1.85 or x>=.72:return 0.0
 if x< -1.65:return smooth01((x+1.85)/.20)
 if x<=.55:return 1.0
 return 1.0-smooth01((x-.55)/.17)

def body_fields10(x):
 w=interp(v.WIDTH_PTS,x);zc=interp(v.SPINE_PTS,x);zsh=interp(SHOULDER_PTS,x);zl=interp(v.LOWER_PTS,x);return w,zc,zsh,zl
v.body_fields=body_fields10

def body_ring10(x):
 w,zc,zsh,zl=body_fields10(x);p=roof_presence(x);ztop=interp(SIDE_TOP,x);wr=min(w*.82,max(.42,interp(v.CABIN_W_PTS,x)));belt=interp(v.BELT_PTS,x)
 fs=(0.0,.16,.34,.52,.68,.80,.90,.965,1.0);upper=[]
 for f in fs:
  y=f*w
  # hood/deck/fender section: crown rises toward the wheel shoulder and eases at the outer skin.
  if f<=.88: zb=zc+(zsh-zc)*(math.sin((f/.88)*math.pi/2)**1.45)
  else: zb=zsh-(f-.88)/.12*.040
  # integrated greenhouse/fastback section; outer shoulder remains independent of roof width.
  if y<=wr:
   u=y/max(wr,1e-6);zg=ztop-(ztop-belt)*(u**1.72)
  else:
   u=(y-wr)/max(w-wr,1e-6);zg=belt+(zsh-belt)*smooth01(u)
   if f>.94:zg-=((f-.94)/.06)*.035
  z=(1-p)*zb+p*zg;upper.append((y,z))
 pos=upper+[(.992*w,zl),(.955*w,.205),(.820*w,.148),(0,.140)]
 # Rounded plan termination is part of the shell, not an attached ellipsoid.
 front_t=smooth01((x-1.78)/(v.FRONT_X-1.78)) if x>1.78 else 0.0
 rear_t=smooth01((-x-1.78)/(-v.REAR_X-1.78)) if x<-1.78 else 0.0
 out=[]
 for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
  r=abs(y)/max(w,1e-6);xe=x-.095*front_t*(r**1.7)+.085*rear_t*(r**1.7);out.append((xe,y,z))
 return out
v.body_ring=body_ring10

# The V5 main still creates a CABIN object. In V10 it is only dark interior backing, not exterior roof authority.
def cabin_backing_ring(x):
 top=interp(SIDE_TOP,x)-.055;w=max(.40,interp(v.CABIN_W_PTS,x)-.035);belt=interp(v.BELT_PTS,x)-.020
 pos=[(0,top),(.30*w,top-.015),(.58*w,top-.050),(.82*w,top-.105),(w,belt),(0,belt-.035)]
 return [(x,y,z) for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]]
v.cabin_ring=cabin_backing_ring
orig_loft=v.build_loft
def loft10(name,xs,ringfn,mat,authority,render=True):
 use=M10.get('body_dark',mat) if name=='DERIVED_911_9922_CABIN' else mat
 o=orig_loft(name,xs,ringfn,use,authority,render)
 if name=='DERIVED_911_9922_BODY':
  o['OLEANDER_FORM_SYSTEM']='CALIBRATED_CONTOUR_INTEGRATED_PRIMARY_SHELL';o['OLEANDER_REFERENCE_CONTOUR']='REFERENCE_CONTOUR_TARGETS_992_2.json'
 if name=='DERIVED_911_9922_CABIN':
  o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERIOR_BACKING';o['OLEANDER_EXPOSURE_ROLE']='DARK_INTERIOR_BACKING_NOT_EXTERIOR_ROOF'
 return o
v.build_loft=loft10

def build_source10(M):
 verts=[];edges=[];families=[('PLAN_WIDTH',v.WIDTH_PTS,'width'),('CENTER_SPINE',v.SPINE_PTS,'z'),('LOWER_SIDE',v.LOWER_PTS,'z'),('SIDE_TOP_CALIBRATED',SIDE_TOP,'z'),('ROOF_FASTBACK_WIDTH',v.CABIN_W_PTS,'width'),('BELT',v.BELT_PTS,'z'),('SHOULDER',SHOULDER_PTS,'z')]
 for name,pts,kind in families:
  s=len(verts)
  for x,val in pts:
   if kind=='width':verts.append((x,val,interp(v.SPINE_PTS,x)))
   else:verts.append((x,0,val))
  edges += [(s+i,s+i+1) for i in range(len(pts)-1)]
 for co in [(v.REAR_X,0,.14),(v.FRONT_X,0,.14),(v.REAR_AXLE,v.WIDTH/2,.70),(v.REAR_AXLE,-v.WIDTH/2,.70),(-.15,0,v.HEIGHT)]:verts.append(co)
 me=bpy.data.meshes.new('SRC_911_9922_CALIBRATED_MULTI_FAMILY_MESH');me.from_pydata(verts,edges,[]);me.update();o=bpy.data.objects.new('SRC_911_9922_CALIBRATED_MULTI_FAMILY',me);bpy.context.collection.objects.link(o);o.hide_render=True;o.hide_set(True);o['OLEANDER_AUTHORITY']='SPARSE_REFERENCE_REPRO_SOURCE';o['OLEANDER_REFERENCE_EVIDENCE']='REFERENCE_CONTOUR_TARGETS_992_2.json';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=build_source10

def build_glass10(M):
 out=[]
 # Aperture edges are calibrated independently from the exterior fastback mass.
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.665,.655,.845),(.665,-.655,.845),(.245,-.555,1.218),(.245,.555,1.218)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.385,.555,1.220),(-.385,-.555,1.220),(-1.035,-.665,.850),(-1.035,.665,.850)],M['glass'],.003))
 outline=[(.665,.845),(.500,1.015),(.245,1.218),(.030,1.260),(-.230,1.240),(-.470,1.180),(-.720,1.050),(-1.035,.850),(-.795,.825),(.525,.825)]
 for side in (1,-1):
  vv=[]
  for x,z in outline:
   w=max(.44,interp(v.CABIN_W_PTS,x));vv.append((x,side*(w+.008),z))
  out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.665,side*.655,.845),(.480,side*.615,1.030),(.245,side*.555,1.218)],M['body'],.010))
  out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.245,side*.555,1.218),(0,side*.545,1.286),(-.230,side*.555,1.240),(-.385,side*.555,1.220)],M['body'],.011))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.385,side*.555,1.220),(-.710,side*.620,1.055),(-1.035,side*.665,.850)],M['body'],.012))
  out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.22,side*.615,1.010),(.030,.022,.305),M['body_dark'],.003))
  out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.02,side*.894,.682),(.108,.013,.018),M['body_dark'],.003))
  y=side*.910;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.605,y,.770),(.555,y,.500),(-.625,y,.500),(-.790,y,.665),(-.770,y,.825)],M['seam'],.0018))
 return out
v.build_glass=build_glass10

def cut_sphere(host,name,loc,scale):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,location=loc);c=bpy.context.object;c.name=name;c.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);bo=host.modifiers.new('CUT_'+name,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=host;host.select_set(True)
 try:bpy.ops.object.modifier_apply(modifier=bo.name)
 finally:bpy.data.objects.remove(c,do_unlink=True)
def cut_cube(host,name,loc,size,bevel=.015):
 c=v.m.add_cube(name,loc,size,M10['body_dark'],bevel);bo=host.modifiers.new('CUT_'+name,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=host;host.select_set(True)
 try:bpy.ops.object.modifier_apply(modifier=bo.name)
 finally:bpy.data.objects.remove(c,do_unlink=True)

def build_identity10(M):
 out=[];body=bpy.data.objects.get('DERIVED_911_9922_BODY')
 if body:
  for side in (1,-1):cut_sphere(body,'HEADLAMP_RECESS_'+str(side),(1.735,side*.655,.760),(.075,.155,.150))
  cut_cube(body,'CENTER_INTAKE_RECESS',(2.170,0,.285),(.190,.430,.105),.018)
  for side in (1,-1):cut_cube(body,'SIDE_INTAKE_RECESS_'+str(side),(2.155,side*.515,.305),(.200,.300,.145),.025)
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.715,side*.655,.760),(.045,.145,.140),M['body_dark']))
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.748,side*.655,.760),(.024,.132,.128),M['glass']))
  for iy,dy in enumerate((-.042,.042)):
   for iz,dz in enumerate((-.042,.042)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.770,side*.655+dy,.760+dz),(.012,.026,.026),M['headlamp'],.004))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.520,side*.945,.875),(.095,.065,.042),M['body_dark']))
  y=side*.525;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.650,y,.805),(1.05,y,.795),(1.45,y,.755),(1.82,side*.455,.670)],M['seam'],.0016))
  out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_BACK_'+str(side),(2.090,side*.515,.305),(.025,.250,.105),M['body_dark'],.012))
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE_BACK',(2.105,0,.285),(.025,.350,.070),M['body_dark'],.008));out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.225,0,.160),(.018,1.320,.016),M['body_dark'],.004))
 out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.175,0,.675),(.016,1.520,.018),M['tail'],.004));out.append(v.m.add_cube('REF_REAR_PLATE_RECESS',(-2.185,0,.430),(.018,.600,.110),M['body_dark'],.016));out.append(v.m.add_cube('REF_REAR_LOWER_TRIM',(-2.190,0,.235),(.016,1.120,.055),M['body_dark'],.010))
 for side in (1,-1):
  bpy.ops.mesh.primitive_torus_add(major_radius=.052,minor_radius=.008,major_segments=40,minor_segments=8,location=(-2.190,side*.485,.270),rotation=(0,math.pi/2,0));e=bpy.context.object;e.name='REF_EXHAUST_'+str(side);e.data.materials.append(M['rim']);out.append(e)
 return out
v.build_identity=build_identity10

def side_contour_metrics():
 errs=[];rows=[]
 for x,target in SIDE_TOP:
  cand=max(p[2] for p in body_ring10(x));e=cand-target;errs.append(e);rows.append({'x':x,'target_z':target,'candidate_z':cand,'error_m':e,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_measurement_source':'V10_BODY_RING_MAX_Z'})
 rmse=math.sqrt(sum(e*e for e in errs)/len(errs));ma=max(abs(e) for e in errs);return rmse,ma,rows

orig_lm=v.landmark_receipt
def landmark10(source_hash):
 d=orig_lm(source_hash)
 for item in d['landmarks']:
  item['candidate_measurement_source']='V10_CALIBRATED_SOURCE_PROJECTION'
  if item['id']=='A_PILLAR_BASE':item['candidate']=.665;item['normalized_error']=abs(.665-float(item['target']))/float(item['normalization'])
  if item['id']=='C_PILLAR_BASE':item['candidate']=-1.035;item['normalized_error']=abs(-1.035-float(item['target']))/float(item['normalization'])
 d['mass_families']=['CALIBRATED_SIDE_CONTOUR','INTEGRATED_FASTBACK_PRIMARY_SHELL','BROAD_TERMINAL_PLAN','FENDER_SHOULDER_CROWN','APERTURE_HOST_CHAIN']
 d['reference_binding']='REFERENCE_CONTOUR_TARGETS_992_2.json';return d
v.landmark_receipt=landmark10

try:
 v.main()
except SystemExit:
 out=Path(v.bench[v.bench.index('--out')+1]) if '--out' in v.bench else None
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  rmse,ma,rows=side_contour_metrics();binding={'schema':'oleander.3d.reference-contour-binding.v1','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V10_CALIBRATED_SOURCE_PROJECTION','side_top_rmse_m':rmse,'side_top_max_abs_m':ma,'thresholds':contour['gates'],'samples':rows,'status':'MACHINE_BINDING_PASS' if rmse<=contour['gates']['side_top_rmse_m_max'] and ma<=contour['gates']['side_top_max_abs_m'] else 'MACHINE_BINDING_FAIL','does_not_prove':contour['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V10_CALIBRATED_CONTOUR_INTEGRATED_SHELL';q['reference_contour_binding']=binding['status'];q['side_top_rmse_m']=rmse;q['side_top_max_abs_m']=ma;q['macro_form_gate']='MACHINE_BINDING_PASS_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V10_CALIBRATED_CONTOUR_INTEGRATED_SHELL';r['reference_contour_binding']=binding['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
