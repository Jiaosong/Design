#!/usr/bin/env python3
"""V32 — rear Y/Z envelope error routing on V31 dense-body / pre-aperture-skin baseline.

V31 improved FRONT projected profile to the current machine best but REAR remained severely over-wide.
V32 changes only the rear high/mid Y/Z envelope. Front geometry, wheelbase, wheel apertures, rocker/lower
return and calibrated lower glazing anchors remain protected.

Runtime composition is explicit: `outer` is V31 declarations, `core` is the V30 callable namespace that
actually owns build_loft/run30/projection hooks. This avoids hidden multi-exec namespace mutation.
"""
from __future__ import annotations
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
V31=HERE/'run_reference_repro_v31.py'
text=V31.read_text();marker="\nns['run30']()\n"
if marker not in text:raise SystemExit('V31 run marker missing')
outer={'__file__':str(V31),'__name__':'oleander_v32_v31_declarations'}
exec(compile(text.split(marker,1)[0],str(V31),'exec'),outer)
core=outer['ns']
v=outer['v'];PROFILE=outer['PROFILE'];metric=outer['metric'];old_body_ring=v.body_ring
old_cabin=core['simple_cabin30'];base_projection=outer['projection31'];surface31=outer['surface31'];s01=outer['s01']

v.REF='2025_992.2_CARRERA_REAR_YZ_ENVELOPE_V32'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v32'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['failure_routing']='REAR_YZ_ENVELOPE_ONLY'
v.REFERENCE_CONTRACT['runtime_composition']='EXPLICIT_OUTER_V31_CORE_V30_NAMESPACE'
v.REFERENCE_CONTRACT['protected_front_machine_baseline']='V31_FRONT_HALF_PROJECTED_PROFILE_RMSE_0.07230088060916158'
v.FAMILY_CONTROLS['REAR_YZ_ENVELOPE_V32']={
 'reference':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile',
 'body_activation_x_m':[-1.55,-.45],'body_activation_z_m':[.78,1.18],
 'cabin_activation_x_m':[-1.20,-.35],
 'protected':['FRONT_HALF','SIDE_LOWER','WHEELBASE','AXLE_CENTRES','WHEEL_APERTURE','LOWER_TERMINAL_RETURN','WINDSHIELD_LOWER','REAR_GLASS_LOWER']}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

REAR=sorted([(float(f),float(r)) for f,r in PROFILE['rear']['profile']],reverse=True)
ZMIN=.140;ZMAX=1.298;ZR=ZMAX-ZMIN

def lerp(a,b,t):return a*(1-t)+b*t

def rear_ratio(frac):
    frac=float(frac)
    if frac>=REAR[0][0]:
        f0,r0=REAR[0];return max(.08,r0*(1-frac)/max(1e-6,1-f0)) if frac<=1 else .08
    if frac<=REAR[-1][0]:return REAR[-1][1]
    for (f0,r0),(f1,r1) in zip(REAR,REAR[1:]):
        if f0>=frac>=f1:
            t=(f0-frac)/(f0-f1);return lerp(r0,r1,t)
    return REAR[-1][1]

def rear_half_target(z,margin=.025):
    frac=max(.10,min(.98,(float(z)-ZMIN)/ZR));return .5*v.WIDTH*rear_ratio(frac)+margin

def rear_x_weight(x):
    if x>=-.35:return 0.0
    if x<=-1.65:return max(0.0,1.0-s01((-x-1.65)/.45))
    return s01((-x-.35)/.65)

def rear_z_weight(z):return s01((float(z)-.76)/.34)

# V31/V30 dense body builder resolves body_ring30 in `core`.
def body_ring32(x):
    ring=old_body_ring(x);xw=rear_x_weight(x)
    if xw<=0:return ring
    out=[]
    for xe,y,z in ring:
        zw=rear_z_weight(z)
        if zw<=0 or abs(y)<1e-8:out.append((xe,y,z));continue
        cap=rear_half_target(z,.040);ay=abs(y);desired=min(ay,cap);strength=xw*zw*.82
        out.append((xe,math.copysign(lerp(ay,desired,strength),y),z))
    return out
core['body_ring30']=body_ring32
v.body_ring=body_ring32

# V31 cabin builder is owned by `core`; contract only failed rear high/mid Y/Z vertices.
def cabin32(name,material):
    o=old_cabin(name,material)
    for vert in o.data.vertices:
        x,y,z=map(float,vert.co);xw=rear_x_weight(x);zw=s01((z-.86)/.28)
        if xw<=0 or zw<=0 or abs(y)<1e-8:continue
        cap=rear_half_target(z,.018);ay=abs(y);desired=min(ay,cap);strength=min(1.0,xw*zw*.96)
        vert.co.y=math.copysign(lerp(ay,desired,strength),y)
    o.data.update();o['OLEANDER_REAR_YZ_ENVELOPE']='V32_REFERENCE_PROFILE_SOFT_CONSTRAINT';return o
core['simple_cabin30']=cabin32
v.build_loft=core['build_loft30']

base_source=v.build_source
def source32(M):
    o=base_source(M);o['OLEANDER_FAILURE_ROUTING']='REAR_YZ_ENVELOPE_ONLY';o['OLEANDER_FRONT_PROFILE_BASELINE']='V31_0.07230088060916158';o['OLEANDER_CONTROL_DIGEST']=v.m.sha_json(v.FAMILY_CONTROLS);return o
v.build_source=source32


def relabel(data):
    if isinstance(data,dict):return {k:relabel(x) for k,x in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V31_','V32_')
    return data

def projection32():
    d=relabel(base_projection());d['candidate_revision']='V32_REAR_YZ_ENVELOPE';d['failure_routing']='REAR_YZ_ENVELOPE_ONLY';d['rear_profile_semantics']='TARGET_DERIVED_CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_FIDELITY';return d
core['projection30']=projection32

BEST32={
 'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.030139600203300147,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'SIDE_LOWER_EVALUATED_MESH_RMSE_M':{'revision':'V25','value':0.061843072886901856,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':{'revision':'V23','value':0.0014470662102585852,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':{'revision':'V25','value':0.0004535585654735774,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':{'revision':'V25','value':0.0006911364693363842,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V31','value':0.07230088060916158,'evidence_source':'V31 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V25','value':0.1165857932746437,'evidence_source':'V25 REFERENCE_PROJECTION_RECEIPT.json'}}

def regression32(pr):
    vals={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],'REAR_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']}
    limits={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.078,'REAR_HALF_PROJECTED_PROFILE_RMSE':.130}
    locks=[]
    for mid,b in BEST32.items():
        c=vals[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':c,'limit':limits[mid],'status':'PASS' if math.isfinite(c) and c<=limits[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
    rear=vals['REAR_HALF_PROJECTED_PROFILE_RMSE'];all_locks=all(x['status']=='PASS' for x in locks)
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'MIXED_PER_GATE_BEST_KNOWN_V25_V23_V31','candidate_revision':'V32_REAR_YZ_ENVELOPE','edit_scope':['REAR_BODY_HIGH_YZ','REAR_CABIN_HIGH_YZ','FRONT_LOCKED','LOWER_GEOMETRY_LOCKED'],'target_metric_delta':{'metric_id':'REAR_HALF_PROJECTED_PROFILE_RMSE','baseline':0.2646265637402603,'candidate':rear,'direction':'LOWER_IS_BETTER','improved':rear<0.2646265637402603},'regression_locks':locks,'best_known_gate_baselines':BEST32,'measurement_method_ids':['V32_FINAL_EVALUATED_MESH_XZ','V32_FINAL_EVALUATED_MESH_YZ','V32_PRE_APERTURE_SKIN'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if all_locks else 'KEEP_LKG_REJECT_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}
core['regression30']=regression32

def surface32():
    d=surface31();d['revision']='V32_REAR_YZ_ENVELOPE';return d
core['surface_receipt']=surface32

core['run30']()
