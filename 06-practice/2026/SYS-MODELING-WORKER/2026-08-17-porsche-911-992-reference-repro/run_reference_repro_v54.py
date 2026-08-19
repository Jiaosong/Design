#!/usr/bin/env python3
"""V54 — claim/carrier congruence repair; geometry unchanged from V51.

The reference FRONT/REAR profile target is a largest-main-vehicle silhouette and explicitly covers
cabin/body taper + shoulder-to-roof relation. V51 measured only its current primary carrier. V54
preserves that body-only diagnostic and compares it against a whole-visible gross carrier assembled
from the same primary body plus current greenhouse visual proxy/frame members.

This is an evidence experiment, not a geometry edit. The proxy can only screen gross silhouette; it
cannot prove final aperture architecture, exact greenhouse surface, or reference fidelity.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V53=HERE/'run_reference_repro_v53.py'
text=V53.read_text();marker='\nrun53()\n'
if marker not in text: raise SystemExit('V53 run marker missing')
ctx={'__file__':str(V53),'__name__':'oleander_v54_carrier_congruence'}
exec(compile(text.split(marker,1)[0],str(V53),'exec'),ctx)

v=ctx['v'];runtime=ctx['runtime'];patch51=ctx['patch51'];emit_fold_diag=ctx['emit_fold_diag']
# PROFILE is nested upstream and not guaranteed to be re-exported by every wrapper; load the authority file directly.
PROFILE=json.loads((HERE/'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json').read_text())
base_projection=runtime['projection30'];EVID='V54_CLAIM_CARRIER_CONGRUENCE'
Z0=.140;ZR=v.HEIGHT-Z0

PROXY_NAMES=[
 'V49_QUARTER_GLASS_L','V49_QUARTER_GLASS_R','V49_DOOR_GLASS_L','V49_DOOR_GLASS_R',
 'REF_B_PILLAR_L','REF_B_PILLAR_R','V49_A_PILLAR_FRAME_L','V49_A_PILLAR_FRAME_R',
 'V49_C_PILLAR_FRAME_L','V49_C_PILLAR_FRAME_R','V49_WINDSHIELD_PROXY','V49_REAR_GLASS_PROXY'
]
BODY='DIAG_FRONT_IDENTITY_FEATURE_GRID_V51'

def object_triangles(name):
    obj=bpy.data.objects.get(name)
    if obj is None:return []
    dg=bpy.context.evaluated_depsgraph_get();eo=obj.evaluated_get(dg);me=eo.to_mesh();mw=eo.matrix_world.copy();tris=[]
    try:
        me.calc_loop_triangles()
        for lt in me.loop_triangles:
            pts=[]
            for vi in lt.vertices:
                p=mw@me.vertices[vi].co;pts.append((float(p.x),float(p.y),float(p.z)))
            tris.append(tuple(pts))
    finally: eo.to_mesh_clear()
    return tris

def z_plane_points(tri,z):
    pts=[]
    for i in range(3):
        x1,y1,z1=tri[i];x2,y2,z2=tri[(i+1)%3]
        if abs(z2-z1)<1e-12:
            if abs(z-z1)<1e-8:pts.extend(((x1,y1),(x2,y2)))
            continue
        if z<min(z1,z2)-1e-9 or z>max(z1,z2)+1e-9:continue
        t=(z-z1)/(z2-z1)
        if -1e-9<=t<=1+1e-9:pts.append((x1+t*(x2-x1),y1+t*(y2-y1)))
    return pts

def profile_from_union(tris,profile,which):
    samples=[];errs=[]
    for frac,target in profile:
        z=Z0+float(frac)*ZR;pts=[]
        for tri in tris:
            if z<min(p[2] for p in tri)-1e-9 or z>max(p[2] for p in tri)+1e-9:continue
            for xx,yy in z_plane_points(tri,z):
                if which=='front' and xx>=-.15:pts.append((xx,yy))
                elif which=='rear' and xx<=.15:pts.append((xx,yy))
        cand=max((abs(yy) for _,yy in pts),default=float('nan'))/(.5*v.WIDTH);err=cand-float(target) if math.isfinite(cand) else float('nan')
        samples.append({'height_fraction':frac,'target_half_width_ratio':target,'candidate_half_width_ratio':cand,'error':err})
        if math.isfinite(err):errs.append(err)
    if len(errs)<max(6,int(.70*len(profile))): raise SystemExit('FAIL_WHOLE_VISIBLE_PROFILE_COVERAGE_'+which.upper())
    return math.sqrt(sum(e*e for e in errs)/len(errs)),samples,len(errs)/len(profile)

def projection54():
    d=base_projection();d['carrier_evidence_revision']=EVID;d['geometry_revision_unchanged']='V51_FRONT_TRANSVERSE_IDENTITY_REPAIR'
    body_tris=object_triangles(BODY);members=[BODY];alltris=list(body_tris);missing=[]
    for name in PROXY_NAMES:
        t=object_triangles(name)
        if t:alltris.extend(t);members.append(name)
        else:missing.append(name)
    fr,fs,fc=profile_from_union(alltris,PROFILE['front']['profile'],'front');rr,rs,rc=profile_from_union(alltris,PROFILE['rear']['profile'],'rear')
    body_metrics={m['id']:dict(m) for m in d['metrics']};old_front=body_metrics['FRONT_HALF_PROJECTED_PROFILE_RMSE'];old_rear=body_metrics['REAR_HALF_PROJECTED_PROFILE_RMSE']
    for m in d['metrics']:
        if m['id']=='FRONT_HALF_PROJECTED_PROFILE_RMSE':m.update({'candidate':fr,'abs_error':fr,'candidate_measurement_source':'V54_WHOLE_VISIBLE_GROSS_SILHOUETTE_PROXY_FRONT_Z_SLICE','measurement_role':'CLAIM_CARRIER_CONGRUENT_GROSS_SCREEN','carrier':'PRIMARY_BODY_PLUS_GREENHOUSE_VISUAL_PROXY'})
        elif m['id']=='REAR_HALF_PROJECTED_PROFILE_RMSE':m.update({'candidate':rr,'abs_error':rr,'candidate_measurement_source':'V54_WHOLE_VISIBLE_GROSS_SILHOUETTE_PROXY_REAR_Z_SLICE','measurement_role':'CLAIM_CARRIER_CONGRUENT_GROSS_SCREEN','carrier':'PRIMARY_BODY_PLUS_GREENHOUSE_VISUAL_PROXY'})
    d['front_profile_samples']=fs;d['rear_profile_samples']=rs;d['front_profile_finite_sample_coverage']=fc;d['rear_profile_finite_sample_coverage']=rc
    d['profile_carrier_congruence']={
      'reference_carrier':'LARGEST_MAIN_VEHICLE_SILHOUETTE_IN_SOURCE_STUDIO_IMAGE',
      'candidate_carrier':'PRIMARY_BODY_PLUS_GREENHOUSE_VISUAL_PROXY',
      'candidate_members':members,'missing_optional_proxy_members':missing,
      'body_only_preserved':{'front_rmse':old_front['candidate'],'front_measurement_source':old_front.get('candidate_measurement_source'),'rear_rmse':old_rear['candidate'],'rear_measurement_source':old_rear.get('candidate_measurement_source')},
      'whole_visible_proxy':{'front_rmse':fr,'rear_rmse':rr},
      'status':'CONGRUENT_FOR_GROSS_SILHOUETTE_SCREEN_ONLY',
      'does_not_prove':['final aperture architecture','exact greenhouse surface','independent reference fidelity']}
    d['status']='PROJECTION_MACHINE_SCREENING_PASS' if all(float(m['candidate'])<=float(m['limit']) for m in d['metrics']) else 'PROJECTION_MACHINE_SCREENING_FAIL'
    return d
runtime['projection30']=projection54

def run54():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try: runtime['run30']()
    except SystemExit as e:
        patch51(out);emit_fold_diag(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:
        patch51(out);emit_fold_diag(out)
run54()
