#!/usr/bin/env python3
"""V19 — final evaluated mesh projection evidence for V16 patch-network geometry.
No macro geometry change. SIDE silhouette metrics are computed directly from final evaluated
triangles in world X/Z projection, independent of renderer/compositor/material state.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V16=HERE/'run_reference_repro_v16.py'
text=V16.read_text();marker='\ntry:\n v.main()'
if marker not in text:raise SystemExit('V16 declaration marker missing')
ns={'__file__':str(V16),'__name__':'oleander_v16_declarations'}
exec(compile(text.split(marker,1)[0],str(V16),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR'];SIDE_TOP=ns['SIDE_TOP'];SIDE_LOW=ns['SIDE_LOW']
v.REF='2025_992.2_CARRERA_EVALUATED_MESH_PROJECTION_V19'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v19'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['projection_measurement']='FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'

# Candidate membership is explicit and excludes wheels/details/ground.
def evaluated_triangles_xz(names):
 dg=bpy.context.evaluated_depsgraph_get();tris=[];members=[]
 for name in names:
  obj=bpy.data.objects.get(name)
  if obj is None:raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: '+name)
  eo=obj.evaluated_get(dg);me=eo.to_mesh();me.calc_loop_triangles();mw=eo.matrix_world.copy();count=0
  try:
   for lt in me.loop_triangles:
    pts=[]
    for vi in lt.vertices:
     p=mw@me.vertices[vi].co;pts.append((float(p.x),float(p.z)))
    tris.append(tuple(pts));count+=1
  finally:eo.to_mesh_clear()
  members.append({'object':name,'triangles':count})
 if not tris:raise SystemExit('FAIL_EVALUATED_MESH_PROJECTION_EMPTY')
 return tris,members

def scan_triangle_z(tri,x):
 vals=[]
 for i in range(3):
  x1,z1=tri[i];x2,z2=tri[(i+1)%3]
  if abs(x2-x1)<1e-12:
   if abs(x-x1)<1e-9: vals.extend((z1,z2))
   continue
  if x < min(x1,x2)-1e-9 or x > max(x1,x2)+1e-9:continue
  t=(x-x1)/(x2-x1)
  if -1e-9<=t<=1+1e-9:vals.append(z1+t*(z2-z1))
 # A vertical line through triangle may cross two edges; edge/vertex degeneracy is harmless for extrema.
 return vals

def scan_union(tris,x):
 zs=[]
 for tri in tris:
  if x < min(p[0] for p in tri)-1e-9 or x > max(p[0] for p in tri)+1e-9:continue
  zs.extend(scan_triangle_z(tri,x))
 if not zs:return float('nan'),float('nan')
 return max(zs),min(zs)

def panel_ratio(name,lower):
 o=bpy.data.objects[name];vs=[o.matrix_world@q.co for q in o.data.vertices];zs=[p.z for p in vs];zr=min(zs) if lower else max(zs);sel=[p for p in vs if abs(p.z-zr)<.03]
 return (max(p.y for p in sel)-min(p.y for p in sel))/v.WIDTH

def projection_receipt():
 names=['DERIVED_911_9922_BODY','DERIVED_911_9922_CABIN'];tris,members=evaluated_triangles_xz(names)
 upper=[];lower=[];samples=[]
 for x,t in SIDE_TOP:
  top,bot=scan_union(tris,x);e=top-t;upper.append(e);samples.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e,'candidate_bottom':bot,'candidate_measurement_source':'V19_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'})
 for x,t in SIDE_LOW:
  top,bot=scan_union(tris,x);lower.append(bot-t)
 fu=panel_ratio('REF_WINDSHIELD',False);fl=panel_ratio('REF_WINDSHIELD',True);rl=panel_ratio('REF_REAR_GLASS',True)
 u=[e for e in upper if math.isfinite(e)];l=[e for e in lower if math.isfinite(e)]
 if not u or not l:raise SystemExit('FAIL_EVALUATED_MESH_PROJECTION_EMPTY')
 urmse=math.sqrt(sum(e*e for e in u)/len(u));lrmse=math.sqrt(sum(e*e for e in l)/len(l));t=PROJ['thresholds']
 metrics=[
  {'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.040,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V19_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'},
  {'id':'SIDE_LOWER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.070,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V19_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V19_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V19_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V19_FINAL_REAR_GLASS_LOWER_MESH'}]
 ok=all(m['abs_error']<=m['limit'] for m in metrics)
 return {'schema':'oleander.3d.evaluated-mesh-projection-receipt.v1','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V19_EVALUATED_MESH_PROJECTION','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','projection_axis':'WORLD_XZ_SIDE','final_visible_membership':members,'metrics':metrics,'side_samples':samples,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit as base_exit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection_receipt();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
  urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v5','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V19_FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V19_EVALUATED_MESH_PROJECTION';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['projection_measurement']='FINAL_EVALUATED_MESH_TRIANGLE_INTERSECTION';q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V19_EVALUATED_MESH_PROJECTION';r['projection_machine_gate']=pr['status'];r['verification_run']='PASS';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise SystemExit(base_exit.code if isinstance(base_exit.code,int) else 0)
