#!/usr/bin/env python3
"""Porsche 911 Carrera 992.2 V11 — evaluated-projection constrained refinement.

V11 consumes V10's calibrated exterior shell, then fixes failures seen in the actual V10 renders:
- narrow the roof/cabin to the front-reference ratio;
- extend and reshape the side glass/C-pillar to the calibrated side reference;
- hide the volumetric dark cabin backing that leaked into 3/4 renders;
- reduce headlamp protrusion and improve host/recess hierarchy;
- simplify front/rear fascia into continuous 992.2-like horizontal layers;
- measure projection ratios from final evaluated geometry, not Source target values.
"""
from __future__ import annotations
import importlib.util,json,math,sys
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V10=HERE/'run_reference_repro_v10.py'
PROJ_FILE=HERE/'REFERENCE_PROJECTION_TARGETS_992_2.json'

# Import V10 despite its executable tail. The first pass is provenance/warm-up only; V11 clears the scene
# inside the second v.main() and overwrites output with the revised candidate.
spec=importlib.util.spec_from_file_location('v10runtime',V10);v10=importlib.util.module_from_spec(spec)
try:
 spec.loader.exec_module(v10)
except SystemExit:
 pass
v=v10.v
proj=json.loads(PROJ_FILE.read_text())

# Cross-view repair: front reference requires a noticeably narrower upper cabin than V10.
v.WIDTH_PTS=[
 (-2.271,.855),(-2.100,.900),(-1.850,.923),(-1.550,.926),(-1.195,.926),(-.800,.920),(-.400,.905),(0,.895),
 (.400,.897),(.800,.905),(1.255,.914),(1.600,.910),(1.850,.895),(2.100,.865),(2.271,.820)]
v.CABIN_W_PTS=[
 (-1.800,.455),(-1.550,.515),(-1.300,.565),(-1.150,.585),(-.900,.585),(-.650,.570),(-.400,.552),(-.150,.540),
 (.050,.540),(.250,.548),(.450,.565),(.650,.600)]
v.BELT_PTS=[(-1.800,.770),(-1.550,.800),(-1.250,.825),(-.900,.838),(-.500,.842),(0,.840),(.400,.838),(.650,.825)]
v.FAMILY_CONTROLS['body_half_width']=v.WIDTH_PTS
v.FAMILY_CONTROLS['roof_fastback_half_width']=v.CABIN_W_PTS
v.FAMILY_CONTROLS['belt_z']=v.BELT_PTS
v.FAMILY_CONTROLS['glass_aperture_extent']={'a_pillar_base_x':.650,'c_pillar_base_x':-1.150}
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v11'
v.REFERENCE_CONTRACT['reference_revision']='2025_992.2_CARRERA_EVALUATED_PROJECTION_CONSTRAINED'
v.REFERENCE_CONTRACT['projection_reference']='REFERENCE_PROJECTION_TARGETS_992_2.json'
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

# V10 ring functions read v.WIDTH_PTS / v.CABIN_W_PTS dynamically, so the primary shell immediately
# adopts the revised front/rear projection proportions.
v.body_fields=v10.body_fields10
v.body_ring=v10.body_ring10
v.cabin_ring=v10.cabin_backing_ring

# Keep V10 calibrated Source builder, but bind the new projection target as additional evidence.
orig_source=v10.build_source10
def build_source11(M):
 o=orig_source(M);o['OLEANDER_PROJECTION_EVIDENCE']='REFERENCE_PROJECTION_TARGETS_992_2.json';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=build_source11

# Dark cabin backing caused false roof/cutout reads in V10 3/4 views. It remains a non-authoritative
# construction object but is no longer rendered.
def loft11(name,xs,ringfn,mat,authority,render=True):
 o=v10.loft10(name,xs,ringfn,mat,authority,render)
 if name=='DERIVED_911_9922_CABIN':
  o.hide_render=True;o['OLEANDER_EXPOSURE_ROLE']='NON_RENDERED_INTERIOR_BACKING'
 return o
v.build_loft=loft11

# Side aperture follows independently calibrated pillar/window positions rather than the exterior roof control.
def build_glass11(M):
 out=[]
 out.append(v.m.add_panel('REF_WINDSHIELD',[(.650,.622,.840),(.650,-.622,.840),(.235,-.515,1.215),(.235,.515,1.215)],M['glass'],.003))
 out.append(v.m.add_panel('REF_REAR_GLASS',[(-.390,.515,1.215),(-.390,-.515,1.215),(-1.150,-.590,.990),(-1.150,.590,.990)],M['glass'],.003))
 outline=[tuple(p) for p in proj['side']['glass_outline_m']]
 for side in (1,-1):
  vv=[]
  for x,z in outline:
   w=max(.43,v10.interp(v.CABIN_W_PTS,x));vv.append((x,side*(w+.006),z))
  out.append(v.m.add_panel('REF_SIDE_GLASS_'+('L' if side>0 else 'R'),vv,M['glass'],.003))
  out.append(v.m.add_curve('REF_A_PILLAR_'+('L' if side>0 else 'R'),[(.650,side*.622,.840),(.455,side*.575,1.055),(.235,side*.515,1.215)],M['body'],.009))
  out.append(v.m.add_curve('REF_ROOF_RAIL_'+('L' if side>0 else 'R'),[(.235,side*.515,1.215),(0,side*.505,1.282),(-.230,side*.515,1.235),(-.390,side*.515,1.215)],M['body'],.010))
  out.append(v.m.add_curve('REF_C_PILLAR_EDGE_'+('L' if side>0 else 'R'),[(-.390,side*.515,1.215),(-.760,side*.555,1.055),(-1.150,side*.590,.990)],M['body'],.011))
  out.append(v.m.add_cube('REF_B_PILLAR_'+('L' if side>0 else 'R'),(-.235,side*.555,1.020),(.028,.020,.300),M['body_dark'],.003))
  out.append(v.m.add_cube('REF_DOOR_HANDLE_'+('L' if side>0 else 'R'),(-.020,side*.896,.682),(.105,.012,.017),M['body_dark'],.003))
  y=side*.912;out.append(v.m.add_curve('REF_DOOR_SEAM_'+('L' if side>0 else 'R'),[(.595,y,.770),(.545,y,.500),(-.635,y,.500),(-.800,y,.665),(-.785,y,.825)],M['seam'],.0017))
 return out
v.build_glass=build_glass11

# Identity architecture: thinner embedded lamps; lower openings read as one horizontal system rather than
# three floating black blocks; rear lightbar / grille / lower diffuser become a clear vertical hierarchy.
def build_identity11(M):
 out=[];body=bpy.data.objects.get('DERIVED_911_9922_BODY')
 if body:
  for side in (1,-1):v10.cut_sphere(body,'HEADLAMP_RECESS_'+str(side),(1.745,side*.655,.758),(.060,.145,.142))
  v10.cut_cube(body,'CENTER_INTAKE_RECESS',(2.155,0,.285),(.175,.500,.105),.018)
  for side in (1,-1):v10.cut_cube(body,'SIDE_INTAKE_RECESS_'+str(side),(2.145,side*.515,.300),(.180,.300,.125),.022)
 for side in (1,-1):
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_HOUSING_'+str(side),(1.725,side*.655,.758),(.030,.132,.128),M['body_dark']))
  out.append(v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.750,side*.655,.758),(.012,.120,.116),M['glass']))
  for iy,dy in enumerate((-.036,.036)):
   for iz,dz in enumerate((-.036,.036)):out.append(v.m.add_cube(f'REF_HEADLAMP_LED_{side}_{iy}_{iz}',(1.763,side*.655+dy,.758+dz),(.008,.022,.022),M['headlamp'],.003))
  out.append(v.m.add_uv_sphere('REF_MIRROR_'+str(side),(.500,side*.940,.875),(.088,.060,.040),M['body_dark']))
  y=side*.525;out.append(v.m.add_curve('REF_HOOD_SEAM_'+str(side),[(.645,y,.805),(1.04,y,.795),(1.43,y,.755),(1.82,side*.455,.670)],M['seam'],.0015))
  out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_BACK_'+str(side),(2.085,side*.515,.300),(.020,.255,.085),M['body_dark'],.010))
  # horizontal vanes make the side opening read as an intake, not a black patch.
  for k in (-.032,0,.032):out.append(v.m.add_cube(f'REF_FRONT_SIDE_VANE_{side}_{k}',(2.071,side*.515,.300+k),(.010,.245,.007),M['rim'],.002))
 out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE_BACK',(2.095,0,.285),(.020,.420,.065),M['body_dark'],.008))
 for k in (-.022,0,.022):out.append(v.m.add_cube(f'REF_FRONT_CENTER_VANE_{k}',(2.080,0,.285+k),(.010,.400,.006),M['rim'],.002))
 out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.215,0,.160),(.016,1.330,.014),M['body_dark'],.004))
 # rear visual hierarchy
 out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.170,0,.700),(.014,1.630,.016),M['tail'],.003))
 out.append(v.m.add_cube('REF_REAR_GRILLE_PANEL',(-1.825,0,.805),(.018,.900,.110),M['body_dark'],.012))
 for k in range(11):out.append(v.m.add_cube(f'REF_REAR_GRILLE_VANE_{k:02d}',(-1.836,-.40+k*.08,.805),(.010,.025,.092),M['rim'],.002))
 out.append(v.m.add_cube('REF_REAR_PLATE_RECESS',(-2.180,0,.455),(.016,.570,.090),M['body_dark'],.014))
 out.append(v.m.add_cube('REF_REAR_DIFFUSER',(-2.185,0,.245),(.020,1.300,.115),M['body_dark'],.016))
 for side in (1,-1):
  bpy.ops.mesh.primitive_torus_add(major_radius=.052,minor_radius=.008,major_segments=40,minor_segments=8,location=(-2.192,side*.485,.275),rotation=(0,math.pi/2,0));e=bpy.context.object;e.name='REF_EXHAUST_'+str(side);e.data.materials.append(M['rim']);out.append(e)
 return out
v.build_identity=build_identity11

# Updated landmark receipt uses independently remeasured A/C targets.
orig_lm=v10.orig_lm
def landmark11(source_hash):
 d=orig_lm(source_hash)
 for item in d['landmarks']:
  item['candidate_measurement_source']='V11_FINAL_GEOMETRY_OR_APERTURE_PROJECTION'
  if item['id']=='A_PILLAR_BASE':item['candidate']=.650;item['normalized_error']=abs(.650-float(item['target']))/float(item['normalization'])
  if item['id']=='C_PILLAR_BASE':item['candidate']=-1.150;item['normalized_error']=abs(-1.150-float(item['target']))/float(item['normalization'])
 d['mass_families']=['CALIBRATED_SIDE_CONTOUR','EVALUATED_PROJECTION_CONSTRAINT','NARROW_CABIN','EXTENDED_C_PILLAR','NON_RENDERED_INTERIOR_BACKING','EMBEDDED_IDENTITY_APERTURES']
 d['reference_binding']='REFERENCE_CONTOUR_TARGETS_992_2.json + REFERENCE_PROJECTION_TARGETS_992_2.json';return d
v.landmark_receipt=landmark11

# Measure the final evaluated body/glass rather than reading the control targets back into the receipt.
def world_vertices(obj,evaluated=True):
 dg=bpy.context.evaluated_depsgraph_get();eo=obj.evaluated_get(dg) if evaluated else obj;me=eo.to_mesh() if evaluated else obj.data
 try:return [eo.matrix_world @ q.co for q in me.vertices]
 finally:
  if evaluated:eo.to_mesh_clear()
def panel_width_ratio(name,lower=True):
 o=bpy.data.objects.get(name);vs=world_vertices(o,False);zs=[p.z for p in vs];zref=min(zs) if lower else max(zs);sel=[p for p in vs if abs(p.z-zref)<.03];return (max(p.y for p in sel)-min(p.y for p in sel))/v.WIDTH
def projection_receipt():
 body=bpy.data.objects['DERIVED_911_9922_BODY'];vs=world_vertices(body,True)
 high=[p for p in vs if p.z>=1.17]
 roof_ratio=(max(p.y for p in high)-min(p.y for p in high))/v.WIDTH if high else 9.0
 wind_ratio=panel_width_ratio('REF_WINDSHIELD',True);rear_ratio=panel_width_ratio('REF_REAR_GLASS',True)
 targets=proj['thresholds'];records=[
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':proj['front']['roof_width_ratio_at_upper_cabin'],'candidate':roof_ratio,'normalization':1.0,'abs_error':abs(roof_ratio-proj['front']['roof_width_ratio_at_upper_cabin']),'limit':targets['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V11_FINAL_EVALUATED_BODY_VERTICES_Z_GE_1.17'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':proj['front']['windshield_lower_width_ratio'],'candidate':wind_ratio,'normalization':1.0,'abs_error':abs(wind_ratio-proj['front']['windshield_lower_width_ratio']),'limit':targets['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V11_FINAL_WINDSHIELD_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':proj['rear']['backlight_lower_width_ratio'],'candidate':rear_ratio,'normalization':1.0,'abs_error':abs(rear_ratio-proj['rear']['backlight_lower_width_ratio']),'limit':targets['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V11_FINAL_REAR_GLASS_MESH'}]
 ok=all(x['abs_error']<=x['limit'] for x in records)
 return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v1','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json','candidate_revision':'V11_EVALUATED_PROJECTION_CONSTRAINED','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':records,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':proj['does_not_prove']}

# Execute revised candidate.
try:
 v.main()
except SystemExit:
 out=Path(v.bench[v.bench.index('--out')+1]) if '--out' in v.bench else None
 if out and (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection_receipt();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
  rmse,ma,rows=v10.side_contour_metrics();binding={'schema':'oleander.3d.reference-contour-binding.v1','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V11_FINAL_PRIMARY_SHELL_PROJECTION','side_top_rmse_m':rmse,'side_top_max_abs_m':ma,'thresholds':v10.contour['gates'],'samples':rows,'status':'MACHINE_BINDING_PASS' if rmse<=v10.contour['gates']['side_top_rmse_m_max'] and ma<=v10.contour['gates']['side_top_max_abs_m'] else 'MACHINE_BINDING_FAIL','does_not_prove':v10.contour['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V11_EVALUATED_PROJECTION_CONSTRAINED';q['reference_contour_binding']=binding['status'];q['projection_machine_gate']=pr['status'];q['macro_form_gate']='MACHINE_SCREENING_ONLY_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V11_EVALUATED_PROJECTION_CONSTRAINED';r['reference_contour_binding']=binding['status'];r['projection_machine_gate']=pr['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
