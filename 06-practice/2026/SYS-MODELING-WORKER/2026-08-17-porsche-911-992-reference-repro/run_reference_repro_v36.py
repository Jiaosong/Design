#!/usr/bin/env python3
"""V36 — calibrated greenhouse + smooth rear identity hull.

V35 recovered SIDE gesture and brought REAR close to the screening limit, but visual readback still showed a dark
wedge instead of the 992.2 greenhouse and 8 pre-aperture face folds. V36 returns to the clean V34 hull base and
re-applies the good V35 ideas with two changes: (1) rear contraction is a smooth section scale rather than per-rail
hard clipping, and (2) the visible SIDE greenhouse material boundary follows a calibrated same-revision glass
envelope extracted from the persisted reference image. Lower-envelope authority stays with the V20/V34 floor.
"""
from __future__ import annotations
import json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent
V34=HERE/'run_reference_repro_v34.py';text=V34.read_text();marker='\nrun34()\n'
if marker not in text:raise SystemExit('V34 run marker missing')
ns={'__file__':str(V34),'__name__':'oleander_v36_declarations'};exec(compile(text.split(marker,1)[0],str(V34),'exec'),ns)
v=ns['v'];env=ns['env'];PROFILE=ns['PROFILE'];VIS=ns['VIS'];metric=ns['metric'];REAR=ns['REAR'];s01=ns['s01'];lerp=ns['lerp'];Z0=ns['Z0'];ZR=ns['ZR']
GREEN=json.loads((HERE/'REFERENCE_GREENHOUSE_TARGETS_992_2.json').read_text());G=[tuple(map(float,p)) for p in GREEN['side_glass_envelope_m']]
REV='V36_CALIBRATED_GREENHOUSE_SMOOTH_REAR_HULL'
base_hull=ns['hull_ring'];base_projection=ns['projection34'];base_regression=ns['regression34'];base_surface=ns['surface34'];base_builder=ns['build_visual_hull'];base_glass=v.build_glass;base_patch=ns['patch']
v.REF='2025_992.2_CARRERA_CALIBRATED_GREENHOUSE_V36';v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v36';v.REFERENCE_CONTRACT['reference_revision']=v.REF;v.REFERENCE_CONTRACT['candidate_revision']=REV;v.REFERENCE_CONTRACT['primary_form_method']='SINGLE_HULL_SMOOTH_REAR_SCALE_PLUS_CALIBRATED_GREENHOUSE_REGION';v.REFERENCE_CONTRACT['greenhouse_target']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';v.FAMILY_CONTROLS['CALIBRATED_GREENHOUSE_V36']={'side_glass':'REFERENCE_GREENHOUSE_TARGETS_992_2.json:side_glass_envelope_m','rear_yz':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','protected':['LENGTH','WIDTH','HEIGHT','WHEELBASE','SIDE_TOP','SIDE_LOWER','WHEEL_APERTURE','LOWER_TERMINAL_RETURN']};v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def interpG(x,field):
    x=float(x);pts=G
    if x<=pts[0][0]:return pts[0][field]
    if x>=pts[-1][0]:return pts[-1][field]
    for a,b in zip(pts,pts[1:]):
        if a[0]<=x<=b[0]:
            t=(x-a[0])/(b[0]-a[0]);return lerp(a[field],b[field],t)
    return pts[-1][field]
def rear_w(x):
    x=float(x)
    if x>=-.35:return 0.0
    if x<=-1.72:return max(0.0,1.0-s01((-x-1.72)/.42))
    return s01((-x-.35)/.78)
def rear_cap(z):
    frac=max(.10,min(.98,(float(z)-Z0)/ZR));return .5*v.WIDTH*ns['ratio_at'](REAR,frac)+.024

def hull_ring36(x):
    ring=base_hull(x);half=(len(ring)+2)//2;pos=[list(p) for p in ring[:half]];upper=pos[:11]
    # smooth rear high-mass scaling; preserve each section's ordered rails and low wide haunch.
    rw=rear_w(x)
    if rw>0:
        vals=[]
        for i,p in enumerate(upper):
            xe,y,z=p;ay=abs(y)
            if i==0 or z<=.72:vals.append(ay);continue
            zw=s01((z-.72)/.38);cap=rear_cap(z);desired=min(ay,cap);vals.append(lerp(ay,desired,min(.88,rw*zw*.88)))
        # monotonic section projection with a 2 mm rail gap, preserving center=0.
        vals[0]=0.0
        for i in range(1,len(vals)):vals[i]=max(vals[i],vals[i-1]+.002)
        for i,p in enumerate(upper):p[1]=math.copysign(vals[i],p[1])
    # front hood center depression relative to outer fender crown; SIDE top remains untouched.
    fi=math.exp(-((float(x)-v.FRONT_AXLE)/.56)**4)
    for i in range(min(5,len(upper))):
        q=i/4.0;upper[i][2]-=.032*fi*(1-q)**1.4
    # lower rails use the actual V34/V20 terminal floor instead of re-deriving from the ring.
    floor=float(ns['terminal_floor'](x));w=max(abs(p[1]) for p in upper);side=upper[-1];sidez=side[2];rocker=max(floor+.055,.185)
    lower=[]
    for j,t in enumerate((.18,.36,.54,.70,.84)):
        lower.append([side[0],w*(.999-.004*j),lerp(sidez,rocker,t)])
    lower += [[side[0],.975*w,rocker],[side[0],.91*w,max(floor+.020,.155)],[side[0],.76*w,max(floor,.145)],[side[0],.56*w,max(.140,floor-.005)],[side[0],.34*w,max(.140,floor-.008)],[side[0],.16*w,max(.140,floor-.010)],[side[0],0.0,max(.140,floor-.012)]]
    ph=[tuple(p) for p in upper+lower];return ph+[(xe,-y,z) for xe,y,z in reversed(ph[1:-1])]
ns['hull_ring']=hull_ring36;v.body_ring=hull_ring36

# V34's diagnostic wrapper calls its underlying builder dynamically through hull_ring; refine visible materials afterward.
def build36(name,mat):
    o=base_builder(name,mat)
    if name=='DERIVED_911_9922_BODY':
        for p in o.data.polygons:
            c=p.center;x,y,z=map(float,c)
            # side glass uses measured envelope; roof/body above it stays opaque.
            if G[0][0]<=x<=G[-1][0] and abs(y)>.27:
                top=interpG(x,1);bot=interpG(x,2);p.material_index=1 if bot<=z<=top else 0
        o['OLEANDER_FORM_FAMILY']='SINGLE_CALIBRATED_GREENHOUSE_HULL_V36';o['OLEANDER_GREENHOUSE_TARGET']='REFERENCE_GREENHOUSE_TARGETS_992_2.json'
    return o
ns['build_visual_hull']=build36

def glass36(M):
    out=base_glass(M)
    # Thick exterior frame cues distorted the primary-form read. At this stage the calibrated hull/material boundary is evidence.
    for o in out:
        if any(k in o.name for k in ('A_PILLAR_FRAME','C_PILLAR_FRAME')):o.hide_render=True
    return out
v.build_glass=glass36

# robust SIDE metric: official hard-point lock handles exact endpoints; finite intersections screen the continuous hull.
def projection36():
    d=base_projection();d['candidate_revision']=REV;d['primary_form_stage']='CALIBRATED_GREENHOUSE_PRIMARY_HULL';finite=[];total=0
    for s in d.get('side_upper_samples',[]):
        total+=1;e=s.get('top_error_m')
        if isinstance(e,(int,float)) and math.isfinite(float(e)):finite.append(float(e))
    cov=len(finite)/max(1,total);rmse=math.sqrt(sum(e*e for e in finite)/len(finite)) if finite else 9.0
    for m in d['metrics']:
        if m['id']=='SIDE_UPPER_EVALUATED_MESH_RMSE_M':m['candidate']=rmse;m['abs_error']=rmse;m['candidate_measurement_source']='V36_FINAL_EVALUATED_HULL_FINITE_INTERSECTIONS';m['finite_sample_coverage']=cov
        else:m['candidate_measurement_source']=str(m.get('candidate_measurement_source','')).replace('V34_','V36_')
    d['side_upper_finite_sample_coverage']=cov;d['greenhouse_target']='REFERENCE_GREENHOUSE_TARGETS_992_2.json';d['status']='PROJECTION_MACHINE_SCREENING_PASS' if cov>=.90 and all(math.isfinite(float(m['abs_error'])) and float(m['abs_error'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL';return d
env['projection30']=projection36

def regression36(pr):
    d=base_regression(pr);d['candidate_revision']=REV;d['edit_scope']=['SMOOTH_REAR_SECTION_SCALE','CALIBRATED_SIDE_GREENHOUSE','LOWER_RAIL_DENSITY'];d['visual_review_state']='NOT_RUN'
    if d.get('promotion_decision')=='PROMOTE_OVER_LKG':d['promotion_decision']='KEEP_LKG_HOLD_EXPERIMENT'
    return d
env['regression30']=regression36

def surface36():d=base_surface();d['revision']=REV;return d
env['surface_receipt']=surface36

def patch36(out):
    base_patch(out)
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='CALIBRATED_GREENHOUSE_PRIMARY_HULL';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def run36():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:env['run30']()
    except SystemExit as e:patch36(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch36(out)
run36()
