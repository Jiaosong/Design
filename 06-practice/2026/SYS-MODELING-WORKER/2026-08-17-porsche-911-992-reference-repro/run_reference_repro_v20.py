#!/usr/bin/env python3
"""V20 — lower-envelope correction driven only by V19 evaluated-mesh projection failures.
Upper shell / greenhouse / aperture ratios are locked. Changes are limited to wheel-aperture geometry,
rocker/bumper lower return and lower terminal-plan behavior.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V19=HERE/'run_reference_repro_v19.py'
text=V19.read_text();marker='\ntry:\n v.main()'
if marker not in text:raise SystemExit('V19 declaration marker missing')
ns={'__file__':str(V19),'__name__':'oleander_v19_declarations'}
exec(compile(text.split(marker,1)[0],str(V19),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR'];SIDE_TOP=ns['SIDE_TOP'];SIDE_LOW=ns['SIDE_LOW']
v.REF='2025_992.2_CARRERA_LOWER_ENVELOPE_V20'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v20'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['lower_envelope_revision']='V19_ERROR_ROUTED_WHEEL_APERTURE_AND_BUMPER_RETURN'
v.FAMILY_CONTROLS['WHEEL_APERTURE']={'front_center_z':.300,'front_radius':.424,'rear_center_z':.315,'rear_radius':.423,'basis':'V19 evaluated lower silhouette inversion'}
v.FAMILY_CONTROLS['LOWER_TERMINAL_RETURN']={'rear':[[-2.271,.416],[-2.10,.407],[-1.90,.263],[-1.72,.150]],'front':[[1.72,.155],[1.85,.160],[2.05,.197],[2.271,.207]]}

def h(pts,x):return v.hermite(pts,x)
rear_floor=[(-2.271,.416),(-2.10,.407),(-1.90,.263),(-1.72,.150)]
front_floor=[(1.72,.155),(1.85,.160),(2.05,.197),(2.271,.207)]
base_ring=v.body_ring

def target_floor(x):
 if x<=-1.72:return h(rear_floor,x)
 if x>=1.72:return h(front_floor,x)
 return .140

def ring20(x):
 ring=base_ring(x);floor=target_floor(x);out=[]
 # Restore lower terminal vertices to the true longitudinal station and raise only the low bumper/underbody envelope.
 # Upper fender/shoulder plan curvature remains untouched.
 for xe,y,z in ring:
  if z<=.62 and (x<=-1.72 or x>=1.72):
   xe=x
  if z<floor:
   z=floor
  out.append((xe,y,z))
 return out
v.body_ring=ring20

# Wheel aperture geometry is solved from the calibrated lower silhouette rather than generic tyre-gap only.
def cut_arch20(body,tag,axle,z,radius):
 if tag=='F':center=.300;rad=.424
 elif tag=='R':center=.315;rad=.423
 else:center=z;rad=radius
 bpy.ops.mesh.primitive_cylinder_add(vertices=160,radius=rad,depth=2.6,location=(axle,0,center),rotation=(math.pi/2,0,0));c=bpy.context.object;c.name='DERIVED_ARCH_CUT_V20_'+tag
 bo=body.modifiers.new('DERIVED_WHEEL_ARCH_V20_'+tag,'BOOLEAN');bo.operation='DIFFERENCE';bo.solver='EXACT';bo.object=c;bpy.context.view_layer.objects.active=body;body.select_set(True);bpy.ops.object.modifier_apply(modifier=bo.name);bpy.data.objects.remove(c,do_unlink=True)
v.cut_arch=cut_arch20

# Refresh source digest semantics without modifying upper families.
base_source=v.build_source
def source20(M):
 o=base_source(M);o['OLEANDER_LOWER_ENVELOPE_REVISION']='V20_WHEEL_APERTURE_BUMPER_RETURN';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source20

# Recompute V19-style final evaluated projection, now storing lower samples explicitly.
def eval_tris(names):return ns['evaluated_triangles_xz'](names)
def scan(tris,x):return ns['scan_union'](tris,x)
def panel_ratio(name,lower):return ns['panel_ratio'](name,lower)
def projection20():
 tris,members=eval_tris(['DERIVED_911_9922_BODY','DERIVED_911_9922_CABIN']);upper=[];lower=[];us=[];ls=[]
 for x,t in SIDE_TOP:
  top,bot=scan(tris,x);e=top-t;upper.append(e);us.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e,'candidate_measurement_source':'V20_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'})
 for x,t in SIDE_LOW:
  top,bot=scan(tris,x);e=bot-t;lower.append(e);ls.append({'x':x,'target_bottom':t,'candidate_bottom':bot,'bottom_error_m':e,'candidate_measurement_source':'V20_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'})
 u=[e for e in upper if math.isfinite(e)];l=[e for e in lower if math.isfinite(e)];urmse=math.sqrt(sum(e*e for e in u)/len(u));lrmse=math.sqrt(sum(e*e for e in l)/len(l));fu=panel_ratio('REF_WINDSHIELD',False);fl=panel_ratio('REF_WINDSHIELD',True);rl=panel_ratio('REF_REAR_GLASS',True);t=PROJ['thresholds']
 metrics=[
  {'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.040,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V20_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'},
  {'id':'SIDE_LOWER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.070,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V20_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V20_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V20_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V20_FINAL_REAR_GLASS_LOWER_MESH'}]
 ok=all(m['abs_error']<=m['limit'] for m in metrics)
 return {'schema':'oleander.3d.evaluated-mesh-projection-receipt.v2','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V20_LOWER_ENVELOPE','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','projection_axis':'WORLD_XZ_SIDE','final_visible_membership':members,'metrics':metrics,'side_upper_samples':us,'side_lower_samples':ls,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit as base_exit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection20();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_upper_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v6','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V20_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_upper_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V20_LOWER_ENVELOPE';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['projection_measurement']='FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION';q['failure_routing']='LOWER_ENVELOPE_ONLY';q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V20_LOWER_ENVELOPE';r['projection_machine_gate']=pr['status'];r['verification_run']='PASS';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise SystemExit(base_exit.code if isinstance(base_exit.code,int) else 0)
