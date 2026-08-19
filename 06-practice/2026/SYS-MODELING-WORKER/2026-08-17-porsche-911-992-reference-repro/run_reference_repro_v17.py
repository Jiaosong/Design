#!/usr/bin/env python3
"""V17 — evidence stabilization for the V16 patch-network candidate.
No macro geometry change. Enlarges diagnostic frames and verifies mask semantics before metrics are allowed to drive V18 geometry edits.
"""
from __future__ import annotations
import json,math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V16=HERE/'run_reference_repro_v16.py'
text=V16.read_text(); marker='\ntry:\n v.main()'
if marker not in text: raise SystemExit('V16 declaration marker missing')
ns={'__file__':str(V16),'__name__':'oleander_v16_declarations'}
exec(compile(text.split(marker,1)[0],str(V16),'exec'),ns)
v=ns['v'];PROJ=ns['PROJ'];CONTOUR=ns['CONTOUR'];SIDE_TOP=ns['SIDE_TOP'];SIDE_LOW=ns['SIDE_LOW']
v.REF='2025_992.2_CARRERA_PATCH_NETWORK_MASK_STABLE_V17'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v17'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['projection_measurement']='EMISSION_MASK_FINAL_VISIBLE_PATCH_NETWORK_STABLE_FRAME'

base_mask=ns['mask_render']

def mask17(objects,out,label,loc,target,scale,w,hpx):
 rec=base_mask(objects,out,label,loc,target,scale,w,hpx)
 # V17 validity: mask must contain foreground/background, plausible coverage and >=2 px bbox margin.
 if rec['bbox']:
  x0,y0,x1,y1=rec['bbox'];margin=min(x0,y0,rec['width_px']-1-x1,rec['height_px']-1-y1)
 else: margin=-1
 rec['frame_margin_px']=margin
 rec['valid']=rec['bbox'] is not None and .01<=rec['coverage']<=.75 and margin>=2
 return rec
ns['mask_render']=mask17

# Rebuild projection function with larger diagnostic frames; world→image orientation is fixed by the camera convention.
def projection17(out):
 body=bpy.data.objects['DERIVED_911_9922_BODY'];roof=bpy.data.objects['DERIVED_911_9922_CABIN']
 side=mask17([body,roof],out,'SIDE',(0,-8,.68),(0,0,.68),1.90,1200,480)
 front=mask17([body,roof],out,'FRONT',(7,0,.68),(0,0,.68),2.55,800,700)
 rear=mask17([body,roof],out,'REAR',(-7,0,.68),(0,0,.68),2.55,800,700)
 if not all(x['valid'] for x in (side,front,rear)):
  details=[{'view':lab,'coverage':r['coverage'],'bbox':r['bbox'],'margin':r.get('frame_margin_px')} for lab,r in [('SIDE',side),('FRONT',front),('REAR',rear)]]
  raise SystemExit('FAIL_PROJECTION_MASK_INVALID: '+json.dumps(details))
 # Side sample maps official rear/front extremes to the detected final-visible bbox.
 def sample(rec,x):
  u0,v0,u1,v1=rec['bbox'];u=int(round(u0+(x-v.REAR_X)/(v.FRONT_X-v.REAR_X)*(u1-u0)));rows=[]
  for du in range(-2,3):
   uu=max(u0,min(u1,u+du));rows += [yy for yy in range(v0,v1+1) if rec['mask'][yy][uu]]
  if not rows:return float('nan'),float('nan')
  lo,hi=min(rows),max(rows);z0=.140;z1=v.HEIGHT;top=z0+(hi-v0)/max(v1-v0,1)*(z1-z0);bottom=z0+(lo-v0)/max(v1-v0,1)*(z1-z0);return top,bottom
 ue=[];le=[];samples=[]
 for x,t in SIDE_TOP:
  top,bot=sample(side,x);e=top-t;ue.append(e);samples.append({'x':x,'target_top':t,'candidate_top':top,'top_error_m':e,'candidate_bottom':bot})
 for x,t in SIDE_LOW:
  top,bot=sample(side,x);le.append(bot-t)
 finiteu=[e for e in ue if math.isfinite(e)];finitel=[e for e in le if math.isfinite(e)];urmse=math.sqrt(sum(e*e for e in finiteu)/len(finiteu));lrmse=math.sqrt(sum(e*e for e in finitel)/len(finitel))
 panel_ratio=ns['panel_ratio'];fu=panel_ratio('REF_WINDSHIELD',False);fl=panel_ratio('REF_WINDSHIELD',True);rl=panel_ratio('REF_REAR_GLASS',True);t=PROJ['thresholds']
 metrics=[
  {'id':'SIDE_UPPER_EMISSION_MASK_RMSE_M','target':0.0,'candidate':urmse,'abs_error':urmse,'limit':.040,'reference_target_source':'REFERENCE_CONTOUR_TARGETS_992_2.json:side_top_silhouette_m','candidate_measurement_source':'V17_FINAL_VISIBLE_UNION_EMISSION_MASK'},
  {'id':'SIDE_LOWER_EMISSION_MASK_RMSE_M','target':0.0,'candidate':lrmse,'abs_error':lrmse,'limit':.070,'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:side.lower_body_silhouette_m','candidate_measurement_source':'V17_FINAL_VISIBLE_UNION_EMISSION_MASK'},
  {'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','target':PROJ['front']['roof_width_ratio_at_upper_cabin'],'candidate':fu,'abs_error':abs(fu-PROJ['front']['roof_width_ratio_at_upper_cabin']),'limit':t['front_roof_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.roof_width_ratio_at_upper_cabin','candidate_measurement_source':'V17_FINAL_WINDSHIELD_UPPER_MESH'},
  {'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','target':PROJ['front']['windshield_lower_width_ratio'],'candidate':fl,'abs_error':abs(fl-PROJ['front']['windshield_lower_width_ratio']),'limit':t['front_windshield_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:front.windshield_lower_width_ratio','candidate_measurement_source':'V17_FINAL_WINDSHIELD_LOWER_MESH'},
  {'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','target':PROJ['rear']['backlight_lower_width_ratio'],'candidate':rl,'abs_error':abs(rl-PROJ['rear']['backlight_lower_width_ratio']),'limit':t['rear_backlight_lower_width_ratio_abs_error_max'],'reference_target_source':'REFERENCE_PROJECTION_TARGETS_992_2.json:rear.backlight_lower_width_ratio','candidate_measurement_source':'V17_FINAL_REAR_GLASS_LOWER_MESH'}]
 ok=all(m['abs_error']<=m['limit'] for m in metrics)
 return {'schema':'oleander.3d.rendered-projection-fidelity-receipt.v3','reference':'REFERENCE_PROJECTION_TARGETS_992_2.json + REFERENCE_CONTOUR_TARGETS_992_2.json','candidate_revision':'V17_PATCH_NETWORK_MASK_STABLE','status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','metrics':metrics,'mask_validity':[{'view':lab,'coverage':r['coverage'],'bbox':r['bbox'],'frame_margin_px':r['frame_margin_px'],'valid':r['valid'],'file':r['file']} for lab,r in [('SIDE',side),('FRONT',front),('REAR',rear)]],'side_samples':samples,'independent_visual_review':False,'reference_fidelity_review':'HOLD','does_not_prove':PROJ['does_not_prove']}

try:
 v.main()
except SystemExit:
 a=v.m.parse_args();out=Path(a.out).resolve()
 if (out/'REFERENCE_REPRO_QA.json').exists():
  pr=projection17(out);(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n');urmse=next(m['candidate'] for m in pr['metrics'] if m['id']=='SIDE_UPPER_EMISSION_MASK_RMSE_M');maxabs=max(abs(s['top_error_m']) for s in pr['side_samples'] if math.isfinite(s['top_error_m']));binding={'schema':'oleander.3d.reference-contour-binding.v4','reference':'REFERENCE_CONTOUR_TARGETS_992_2.json','candidate':'V17_FINAL_VISIBLE_UNION_EMISSION_MASK','side_top_rmse_m':urmse,'side_top_max_abs_m':maxabs,'thresholds':CONTOUR['gates'],'samples':pr['side_samples'],'status':'MACHINE_BINDING_PASS' if urmse<=.040 and maxabs<=.080 else 'MACHINE_BINDING_FAIL','does_not_prove':CONTOUR['does_not_prove']};(out/'REFERENCE_CONTOUR_BINDING_RECEIPT.json').write_text(json.dumps(binding,ensure_ascii=False,indent=2)+'\n')
  q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V17_PATCH_NETWORK_MASK_STABLE';q['projection_machine_gate']=pr['status'];q['reference_contour_binding']=binding['status'];q['visible_primary_architecture']='SHARED_BOUNDARY_PATCH_NETWORK';q['projection_measurement']='EMISSION_MASK_FINAL_VISIBLE_PATCH_NETWORK_STABLE_FRAME';q['mask_validity_gate']='PASS';q['runtime_passes']=1;q['macro_form_gate']='MACHINE_SCREENING_ONLY_VISUAL_REVIEW_REQUIRED';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
  r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V17_PATCH_NETWORK_MASK_STABLE';r['projection_machine_gate']=pr['status'];r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';r['runtime_passes']=1;(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
 raise
