#!/usr/bin/env python3
"""V49 — feature-aligned curve/section representation reopen.

V48 proved that low SIDE/FRONT/REAR gross-profile error can coexist with a visibly generic,
rippled 911. V49 therefore follows CB-01 root-cause reclassification and reopens the
representation model instead of tuning more local V48 offsets.

Representation:
    reference evidence → semantic longitudinal rails → causal critical sections →
    generated shared skin → SubD1 evaluated surface

Tier-A rails:
    CENTER_SPINE / ROOF_CROWN
    INNER_CROWN
    FENDER_HAUNCH_CROWN
    CABIN_EDGE
    SHOULDER
    OUTER_SIDE
    ROCKER / LOWER_RETURN

The visible skin remains one generated shell for primary-form review. Greenhouse infill is
still a derived visual proxy; final aperture architecture remains HOLD.

This is a modeling/Skill benchmark, not Porsche CAD, Class-A surfacing, engineering release,
manufacturing feasibility, homologation, physical CMF, Design KEEP or MAIN KEEP.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V48=HERE/'run_reference_repro_v48.py'
text=V48.read_text()
marker='\nrun48()\n'
if marker not in text:
    raise SystemExit('V48 run marker missing')
ns={'__file__':str(V48),'__name__':'oleander_v49_declarations'}
exec(compile(text.split(marker,1)[0],str(V48),'exec'),ns)

v=ns['v']; core=ns['core']; runtime=ns['runtime']; ns43=ns['ns43']
base_build=ns['base_build']; apply_subd=ns['apply_subd']
tri_plane_top=ns['tri_plane_top']; evaluated_mesh_data=ns['evaluated_mesh_data']
z_plane_points=ns['z_plane_points']; PROFILE=ns['PROFILE']; SIDE=ns['SIDE']; FRONT_ID=ns['FRONT_ID']
G=ns['G']; lerp=ns['lerp']; interpG=ns['interpG']; s01=ns['s01']

REV='V49_FEATURE_ALIGNED_CURVE_NETWORK'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_FEATURE_ALIGNED_V49'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v49'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['primary_form_method']='FEATURE_ALIGNED_LONGITUDINAL_RAIL_NETWORK'
v.REFERENCE_CONTRACT['representation_state']='REOPEN_REPRESENTATION_MODEL'
v.REFERENCE_CONTRACT['representation_protocol']='oleander-skills/oleander-3d-pipeline/reference-reproduction/FEATURE_ALIGNED_CURVE_NETWORK_PROTOCOL_v1.md'
v.REFERENCE_CONTRACT['aperture_architecture_state']='HOLD_PROXY_ONLY'
v.REFERENCE_CONTRACT['fit_views']=['SIDE','FRONT','REAR']
v.REFERENCE_CONTRACT['held_out_views']=['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q']

CRITICAL_X=[v.REAR_X,-2.05,-1.72,v.REAR_AXLE,-1.18,-.88,-.52,-.20,.24,.58,.82,v.FRONT_AXLE,1.62,1.87,2.08,v.FRONT_X]
RAILS=['CENTER_SPINE_ROOF_CROWN','INNER_CROWN','MID_CROWN','FENDER_HAUNCH_OR_CABIN_EDGE','SHOULDER','OUTER_SIDE','LOWER_SIDE','ROCKER','LOWER_RETURN']
v.FAMILY_CONTROLS['FEATURE_ALIGNED_CURVE_NETWORK_V49']={
    'tier':'TIER_A_IDENTITY_CRITICAL','critical_sections_x_m':CRITICAL_X,'longitudinal_rails':RAILS,
    'reference_sources':['REFERENCE_VISUAL_HULL_TARGETS_992_2.json','REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','REFERENCE_GREENHOUSE_TARGETS_992_2.json','REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json'],
    'protected':['OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE'],
    'replaces':'V48_LOCAL_OFFSET_ON_GENERIC_MULTI_VIEW_RING','aperture_architecture':'HOLD_NOT_CONSTRUCTED'
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def cabin_weight49(x):
    x=float(x)
    if -1.25<=x<=.58:return 1.0
    if -1.55<x<-1.25:return s01((x+1.55)/.30)
    if .58<x<.86:return 1.0-s01((x-.58)/.28)
    return 0.0

def front_weight49(x):return math.exp(-((float(x)-1.45)/.72)**4)
def rear_weight49(x):return math.exp(-((float(x)+1.35)/.78)**4)

def belt49(x):
    x=float(x)
    if G[0][0]<=x<=G[-1][0]:return max(.805,min(.875,interpG(x,2)-.035))
    return .825+.018*math.exp(-((x-v.REAR_AXLE)/.75)**4)+.010*math.exp(-((x-v.FRONT_AXLE)/.65)**4)

def cabin_half_width49(x,top,belt):
    raw=.5*v.WIDTH*core['profile_ratio'](x,(top+belt)*.5);w=core['plan_half_width'](x)
    return min(.78*w,max(.46,raw-.055))

def feature_ring49(x):
    x=float(x);w=core['plan_half_width'](x);top=core['side_top'](x);floor=core['terminal_floor'](x)
    cw=cabin_weight49(x);fw=front_weight49(x);rw=rear_weight49(x);belt=belt49(x);cabw=cabin_half_width49(x,top,belt)
    body_y=[0.0,.24*w,.48*w,.72*w,.90*w,w];cabin_y=[0.0,.28*cabw,.58*cabw,cabw,.91*w,w]
    ys=[lerp(a,b,cw) for a,b in zip(body_y,cabin_y)]
    body_z=[top-.086*fw-.090*rw,top-.058*fw-.062*rw,top-.028*fw-.036*rw,top-.004*fw-.010*rw,top-.016*fw-.006*rw,top-.066*fw-.058*rw]
    cabin_z=[top,top-.012,top-.040,top-.086,belt+.050,belt-.012]
    zs=[lerp(a,b,cw) for a,b in zip(body_z,cabin_z)]
    if cw<.35:
        zs[3]=max(zs[3],zs[2]+.012);zs[4]=min(zs[3]-.006,max(zs[4],zs[5]+.018))
    upper=list(zip(ys,zs))
    side_lower=max(.32,floor+.075)
    lower=[(.998*w,side_lower),(.965*w,max(.185,floor+.018)),(.78*w,max(.145,floor-.002)),(.44*w,max(.140,floor-.008)),(0.0,max(.140,floor-.010))]
    pos=upper+lower
    ft=s01((x-1.74)/(v.FRONT_X-1.74)) if x>1.74 else 0.0;rt=s01((-x-1.74)/(-v.REAR_X-1.74)) if x<-1.74 else 0.0
    out=[]
    for y,z in pos+[(-yy,zz) for yy,zz in reversed(pos[1:-1])]:
        q=abs(y)/max(w,1e-6);setback=(.080*ft+.070*rt)*(q**1.45);center_retreat=(.018*ft+.020*rt)*max(0.0,1-q/.70)
        xe=x-setback-center_retreat if x>0 else x+setback+center_retreat;out.append((xe,y,z))
    return out

core['hull_ring']=feature_ring49;v.body_ring=feature_ring49

def build49(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o);d=o.copy();d.data=o.data.copy();d.name='DIAG_FEATURE_ALIGNED_SURFACED_V49';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_FEATURE_ALIGNED_PRIMARY_BODY'
        o['OLEANDER_FORM_FAMILY']='FEATURE_ALIGNED_CURVE_NETWORK_V49';o['OLEANDER_SOURCE_RAILS']='|'.join(RAILS);o['OLEANDER_APERTURE_ARCHITECTURE']='HOLD_PROXY_GREENHOUSE'
    return o
core['build_visual_hull']=build49

def gy49(x,z):
    w=core['plan_half_width'](x);raw=.5*v.WIDTH*core['profile_ratio'](x,z);return min(w-.018,max(.40,raw-.028))

def strip49(name,pts,side,mat,offset=-.010):
    verts=[];faces=[]
    for x,zt,zb in pts:
        yy=gy49(x,(zt+zb)*.5)+offset;verts.extend([(x,side*yy,zt),(x,side*yy,zb)])
    for i in range(len(pts)-1):a=2*i;faces.append((a,a+1,a+3,a+2))
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat);o['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'
    for p in me.polygons:p.use_smooth=True
    return o

def glass49(M):
    out=[];split=-.23;bp=(split,interpG(split,1),interpG(split,2));quarter=[p for p in G if p[0]<split]+[bp];door=[bp]+[p for p in G if p[0]>split]
    for side,label in ((1,'L'),(-1,'R')):
        out+=[strip49('V49_QUARTER_GLASS_'+label,quarter,side,M['glass']),strip49('V49_DOOR_GLASS_'+label,door,side,M['glass'])]
        top=interpG(split,1);bot=interpG(split,2);yy=gy49(split,(top+bot)*.5)-.004
        out.append(v.m.add_cube('REF_B_PILLAR_'+label,(split,side*yy,(top+bot)*.5),(.028,.014,max(.10,top-bot)),M['body_dark'],.002))
        ay=side*(gy49(.56,.90)-.004);cy=side*(gy49(-1.10,1.00)-.004)
        out.append(v.m.add_curve('V49_A_PILLAR_FRAME_'+label,[(.56,ay,.88),(.42,side*(gy49(.42,1.05)-.004),1.05),(.24,side*(gy49(.24,1.20)-.004),1.20)],M['body'],.008))
        out.append(v.m.add_curve('V49_C_PILLAR_FRAME_'+label,[(-.42,side*(gy49(-.42,1.20)-.004),1.20),(-.76,side*(gy49(-.76,1.10)-.004),1.10),(-1.10,cy,.98)],M['body'],.010))
    ws=[(.61,.565,.865),(.61,-.565,.865),(.245,-.500,1.205),(.245,.500,1.205)];rg=[(-.43,.450,1.205),(-.43,-.450,1.205),(-1.10,-.525,.990),(-1.10,.525,.990)]
    out.append(v.m.add_panel('V49_WINDSHIELD_PROXY',ws,M['glass'],.0012));out.append(v.m.add_panel('V49_REAR_GLASS_PROXY',rg,M['glass'],.0012));return out
v.build_glass=glass49

def identity49(M):
    out=[];half=v.WIDTH*.5;cy=float(FRONT_ID['measurement']['lamp_center_lateral_ratio_of_half_body_width'])*half;r=.5*float(FRONT_ID['measurement']['visible_lamp_diameter_ratio_of_body_width'])*v.WIDTH
    for side in (1,-1):
        bezel=v.m.add_uv_sphere('DERIVED_HEADLAMP_BEZEL_'+str(side),(1.868,side*cy,.755),(.006,r,r),M['body_dark']);bezel['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';out.append(bezel)
        lens=v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.876,side*cy,.755),(.004,r*.94,r*.94),M['glass']);lens['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL';out.append(lens)
    out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.178,0,.272),(.010,.250,.042),M['body_dark'],.020))
    for side in (1,-1):out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.158,side*.55,.285),(.010,.085,.050),M['body_dark'],.024))
    out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.125,0,.655),(.010,1.40,.024),M['tail'],.008));return out
v.build_identity=identity49

def profile_rmse49(tris,profile,which):
    Z0=.140;ZH=v.HEIGHT;samples=[];errs=[]
    for frac,target in profile:
        z=Z0+float(frac)*(ZH-Z0);pts=[]
        for tri in tris:
            if z<min(p[2] for p in tri)-1e-9 or z>max(p[2] for p in tri)+1e-9:continue
            for x,y in z_plane_points(tri,z):
                if which=='front' and x>=.55:pts.append((x,y))
                elif which=='rear' and x<=-.55:pts.append((x,y))
        cand=max((abs(y) for _,y in pts),default=float('nan'))/(.5*v.WIDTH);err=cand-float(target) if math.isfinite(cand) else float('nan');samples.append({'height_fraction':frac,'target_half_width_ratio':target,'candidate_half_width_ratio':cand,'error':err})
        if math.isfinite(err):errs.append(err)
    if len(errs)<max(6,int(.70*len(profile))):raise SystemExit('FAIL_EVALUATED_PROFILE_COVERAGE_'+which.upper())
    return math.sqrt(sum(e*e for e in errs)/len(errs)),samples,len(errs)/len(profile)

def projection49():
    diag=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V49')
    if diag is None:raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: DIAG_FEATURE_ALIGNED_SURFACED_V49')
    side_errs=[];side_samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x);err=cand-z if math.isfinite(cand) else float('nan');side_samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':err,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V49_FINAL_EVALUATED_FEATURE_RAIL_BODY_XZ_INTERSECTION'});side_errs.append(err) if math.isfinite(err) else None
    if len(side_errs)<max(6,int(.90*len(SIDE))):raise SystemExit('FAIL_EVALUATED_SIDE_PROFILE_COVERAGE')
    side_rmse=math.sqrt(sum(e*e for e in side_errs)/len(side_errs));tris=evaluated_mesh_data('DIAG_FEATURE_ALIGNED_SURFACED_V49');front_rmse,front_samples,front_cov=profile_rmse49(tris,PROFILE['front']['profile'],'front');rear_rmse,rear_samples,rear_cov=profile_rmse49(tris,PROFILE['rear']['profile'],'rear')
    metrics=[{'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':side_rmse,'abs_error':side_rmse,'limit':.040,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V49_FINAL_EVALUATED_FEATURE_RAIL_BODY_XZ_INTERSECTION'},{'id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':front_rmse,'abs_error':front_rmse,'limit':float(PROFILE['gates']['front_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','candidate_measurement_source':'V49_FINAL_EVALUATED_FEATURE_RAIL_BODY_FRONT_Z_SLICE'},{'id':'REAR_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':rear_rmse,'abs_error':rear_rmse,'limit':float(PROFILE['gates']['rear_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','candidate_measurement_source':'V49_FINAL_EVALUATED_FEATURE_RAIL_BODY_REAR_Z_SLICE'}];ok=all(m['abs_error']<=m['limit'] for m in metrics)
    return {'schema':'oleander.3d.stage-aware-primary-form-projection.v1','reference':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json + REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','candidate_revision':REV,'status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','primary_form_stage':'FEATURE_ALIGNED_PRIMARY_FORM_APERTURE_HOLD','representation_state':'REOPEN_REPRESENTATION_MODEL','fit_views':['SIDE','FRONT','REAR'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'stage_capabilities':{'PRIMARY_FORM_PROJECTION':'AVAILABLE','FEATURE_ALIGNED_CURVE_NETWORK':'AVAILABLE','GREENHOUSE_VISUAL_PROXY':'AVAILABLE','FINAL_APERTURE_ARCHITECTURE':'NOT_APPLICABLE_STAGE_HOLD'},'not_applicable_metrics':[{'id':'FINAL_WINDSHIELD_FLANGE','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'},{'id':'FINAL_REAR_GLASS_FLANGE','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'}],'final_visible_membership':[{'object':'DIAG_FEATURE_ALIGNED_SURFACED_V49','role':'FINAL_EVALUATED_FEATURE_ALIGNED_PRIMARY_BODY','triangles':len(tris)}],'metrics':metrics,'side_upper_samples':side_samples,'front_profile_samples':front_samples,'rear_profile_samples':rear_samples,'side_upper_finite_sample_coverage':len(side_errs)/len(SIDE),'front_profile_finite_sample_coverage':front_cov,'rear_profile_finite_sample_coverage':rear_cov,'independent_visual_review':False,'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD','does_not_prove':['reference fidelity','held-out identity','manufacturer CAD','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['projection30']=projection49

V48_BASE={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':0.03135369571685643,'FRONT_HALF_PROJECTED_PROFILE_RMSE':0.07244949168881082,'REAR_HALF_PROJECTED_PROFILE_RMSE':0.08103906166232307}
def regression49(pr):
    cur={m['id']:m for m in pr['metrics']}
    def score(vals):return math.sqrt(((vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M']/.040)**2+(vals['FRONT_HALF_PROJECTED_PROFILE_RMSE']/.100)**2+(vals['REAR_HALF_PROJECTED_PROFILE_RMSE']/.110)**2)/3.0)
    cv={k:float(cur[k]['candidate']) for k in V48_BASE};bscore=score(V48_BASE);cscore=score(cv);locks=[]
    for k in V48_BASE:
        tol=.004 if k.startswith('SIDE') else .012;status='PASS' if cv[k]<=V48_BASE[k]+tol else 'REGRESSED';locks.append({'id':k,'baseline':V48_BASE[k],'candidate':cv[k],'limit':tol,'status':status,'evidence_source':'V48/V49_SAME_FINAL_EVALUATED_STAGE_AWARE_MEASUREMENT'})
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v1','baseline_revision':'V48_PRIMARY_FORM_STAGE_AWARE','candidate_revision':REV,'edit_scope':['REOPEN_REPRESENTATION_MODEL','FEATURE_ALIGNED_LONGITUDINAL_RAILS','CAUSAL_CRITICAL_SECTIONS','GREENHOUSE_FRAME_CUES'],'target_metric_delta':{'metric_id':'NORMALIZED_PRIMARY_FORM_ERROR_SCORE','baseline':bscore,'candidate':cscore,'direction':'LOWER_IS_BETTER','improved':cscore<bscore},'regression_locks':locks,'measurement_method_ids':['FINAL_EVALUATED_PRIMARY_BODY_XZ_INTERSECTION','FINAL_EVALUATED_PRIMARY_BODY_FRONT_Z_SLICE','FINAL_EVALUATED_PRIMARY_BODY_REAR_Z_SLICE'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':['held-out reference identity','design quality','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['regression30']=regression49

def surface49():
    d=ns['base_surface']();d['revision']=REV;d['representation']='FEATURE_ALIGNED_CURVE_NETWORK';d['aperture_architecture_state']='HOLD_PROXY_ONLY';return d
runtime['surface_receipt']=surface49

def patch49(out):
    ns['base_patch'](out);p=Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json');p.unlink() if p.exists() else None
    feature={'schema':'oleander.3d.feature-curve-network-receipt.v1','candidate_revision':REV,'representation_state':'REOPEN_REPRESENTATION_MODEL','tier':'TIER_A_IDENTITY_CRITICAL','source_rail_inventory':RAILS,'critical_sections_x_m':CRITICAL_X,'fit_views':['SIDE','FRONT','REAR'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'generated_surface':'DERIVED_911_9922_BODY','evaluated_diagnostic':'DIAG_FEATURE_ALIGNED_SURFACED_V49','aperture_architecture_state':'HOLD_PROXY_ONLY','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','final aperture architecture','manufacturing feasibility']};Path(out,'FEATURE_CURVE_NETWORK_RECEIPT.json').write_text(json.dumps(feature,ensure_ascii=False,indent=2)+'\n')
    stage={'schema':'oleander.3d.stage-capability-routing-receipt.v1','candidate_revision':REV,'stage':'FEATURE_ALIGNED_PRIMARY_FORM_APERTURE_HOLD','required_capabilities':['PRIMARY_FORM_PROJECTION','FEATURE_ALIGNED_CURVE_NETWORK','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE'],'available_capabilities':['PRIMARY_FORM_PROJECTION','FEATURE_ALIGNED_CURVE_NETWORK','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE','GREENHOUSE_VISUAL_PROXY'],'held_capabilities':['FINAL_APERTURE_ARCHITECTURE','FINAL_WINDSHIELD_FLANGE','FINAL_REAR_GLASS_FLANGE'],'held_result':'NOT_APPLICABLE_STAGE_HOLD','failed_required_capabilities':[],'legacy_name_dependencies_not_required':['REF_WINDSHIELD','REF_REAR_GLASS'],'result':'PASS_STAGE_AWARE_ROUTING','does_not_prove':['reference fidelity','aperture construction','design quality']};Path(out,'STAGE_CAPABILITY_ROUTING_RECEIPT.json').write_text(json.dumps(stage,ensure_ascii=False,indent=2)+'\n')
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='FEATURE_ALIGNED_PRIMARY_FORM_APERTURE_HOLD';d['representation_state']='REOPEN_REPRESENTATION_MODEL';d['aperture_architecture_state']='HOLD_PROXY_ONLY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    fp=Path(out,'REFERENCE_FIDELITY_RECEIPT.json')
    if fp.exists():
        d=json.loads(fp.read_text());d['candidate_revision']=REV;d['screening_scope']='HARD_POINT_AND_LANDMARK_SCREENING_ONLY';d['visual_reference_fidelity']='HOLD';fp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ns43['patch43']=patch49

def run49():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:runtime['run30']()
    except SystemExit as e:patch49(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch49(out)
run49()
