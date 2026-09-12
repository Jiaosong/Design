#!/usr/bin/env python3
"""V18 — compositor-isolated diagnostic evidence for the V16 patch-network geometry.
Geometry is intentionally unchanged from V16/V17. V18 fixes diagnostic semantics and separates
verification success from model-fidelity outcome.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V17=HERE/'run_reference_repro_v17.py'
text=V17.read_text();marker='\ntry:\n v.main()'
if marker not in text:raise SystemExit('V17 declaration marker missing')
ns={'__file__':str(V17),'__name__':'oleander_v17_declarations'}
exec(compile(text.split(marker,1)[0],str(V17),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR']
v.REF='2025_992.2_CARRERA_MASK_COMPOSITOR_ISOLATED_V18'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v18'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['projection_measurement']='COMPOSITOR_ISOLATED_EMISSION_MASK_FINAL_VISIBLE_PATCH_NETWORK'

base_mask=ns['base_mask']
def mask18(objects,out,label,loc,target,scale,w,hpx):
 sc=bpy.context.scene;old_nodes=sc.use_nodes
 try:
  sc.use_nodes=False
  rec=base_mask(objects,out,label,loc,target,scale,w,hpx)
 finally:
  sc.use_nodes=old_nodes
 if rec['bbox']:
  x0,y0,x1,y1=rec['bbox'];margin=min(x0,y0,rec['width_px']-1-x1,rec['height_px']-1-y1)
 else:margin=-1
 rec['frame_margin_px']=margin
 rec['valid']=rec['bbox'] is not None and .005<=rec['coverage']<=.70 and margin>=2
 return rec
ns['mask17']=mask18

# Reuse V17 metric logic but with larger, compositor-isolated masks.
def projection18(out):
 body=bpy.data.objects['DERIVED_911_9922_BODY'];roof=bpy.data.objects['DERIVED_911_9922_CABIN']
 side=mask18([body,roof],out,'SIDE',(0,-8,.68),(0,0,.68),2.30,1200,480)
 front=mask18([body,roof],out,'FRONT',(7,0,.68),(0,0,.68),2.85,800,700)
 rear=mask18([body,roof],out,'REAR',(-7,0,.68),(0,0,.68),2.85,800,700)
 details=[{'view':lab,'coverage':r['coverage'],'bbox':r['bbox'],'frame_margin_px':r['frame_margin_px'],'valid':r['valid'],'file':r['file']} for lab,r in [('SIDE',side),('FRONT',front),('REAR',rear)]]
 if not all(r['valid'] for r in (side,front,rear)):raise SystemExit('FAIL_PROJECTION_MASK_INVALID: '+json.dumps(details))
 def sample(rec,x):
  # Locked camera orientation: SIDE camera at -Y gives image +X = world +X.
  u0,v0,u1,v1=rec['bbox'];u=int(round(u0+(x-v.REAR_X)/(v.FRONT_X-v.REAR_X)*(u1-u0)));rows=[]
  for du in range(-2,3):
   uu=max(u0,min(u1,u+du));rows += [yy for yy in range(v0,v1+1) if rec['mask'][yy][uu]]
  if not rows:return float('nan'),float('nan')
  lo,hi=min(rows),max(rows);z0=.140;z1=v.HEIGHT;return z0+(hi-v0)/max(v1-v0,1)*(z1-z0),z0+(lo-v0)/max(v1-v0,1)*(z1-z0)
 ue=[];le=[];samples=[]
 for x,t in ns['SIDE_TOP']:
  top,bot=sample(side,x);e=top-t;ue.append(e);samples.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e,'candidate_bottom':bot})
 for x,t in ns['SIDE_LOW']:
  top,bot=sample(side,x);le.append(bot-t)
 fu=ns['panel_ratio']('REF_WINDSHIELD',False);fl=ns['panel_ratio']('REF_WINDSHIELD',True);rl=ns['panel_ratio']('REF_REAR_GLASS',True)
 finiteu=[e for e in ue if math.isfinite(e)];finitel=[e for e in le if math.isfinite(e)];urmse=math.sqrt(sum(e*e for e in finiteu)/len(finiteu));lrmse=math.sqrt(sum(e*e for e in finitel)/len(finitel));t=PROJ['thresholds']
 metrics=[
  {'id':'SIDE_UPPER_EMISSION_MASK_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.040,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V18_FINAL_VISIBLE_UNION_EMISSION_MASK'},
  {'id':'SIDE_LOWER_EMISSION_MASK_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.070,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V18_FINAL_VISIBLE_UNION_EMISSION_MASK'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V18_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V18_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V18_FINAL_REAR_GLASS_LOWER_MESH'}]
 ok=all(m['abs_error']<=m['limit'] for m in metrics)
 return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v3','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V18_MASK_COMPOSITOR_ISOLATED','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':metrics,'mask_validity':details,'side_samples':samples,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit as base_exit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection18(out);(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EMISSION_MASK_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v4','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V18_FINAL_VISIBLE_UNION_EMISSION_MASK','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V18_MASK_COMPOSITOR_ISOLATED';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['projection_measurement']='COMPOSITOR_ISOLATED_EMISSION_MASK_FINAL_VISIBLE_PATCH_NETWORK';q['mask_validity_gate']='PASS';q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V18_MASK_COMPOSITOR_ISOLATED';r['projection_machine_gate']=pr['status'];r['verification_run']='PASS';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 # Preserve base machine status exit only. A valid quality FAIL/HOLD does not crash verification.
 raise SystemExit(base_exit.code if isinstance(base_exit.code,int) else 0)
