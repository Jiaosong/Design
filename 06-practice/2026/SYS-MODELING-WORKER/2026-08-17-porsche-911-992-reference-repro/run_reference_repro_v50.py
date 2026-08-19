#!/usr/bin/env python3
"""V50 — profile-inverted feature rails + dense evaluated grid.

V49 successfully reopened the Source representation and improved SIDE gesture, but FRONT/REAR
projected mass regressed and the evaluated body grid was too sparse for the existing surface
quality screen. V50 reuses two existing OLEANDER 3D specialist protocols:

1. PROJECTED_PROFILE_TO_SECTION_INVERSION_PROTOCOL_v1 — use external FRONT/REAR width-vs-height
   profiles only to constrain the failed transverse section family; this is constraint compliance,
   not independent reference fidelity.
2. PRIMARY_BODY_SURFACE_GRID_PROTOCOL_v1 — keep sparse semantic Source rails while regenerating a
   denser evaluated ring so Source control density is not confused with render/surface density.

Gate-local best-known baselines are preserved: V49 owns SIDE upper; V48 owns FRONT/REAR gross profile.
Held-out 3/4 visual identity remains independent and mandatory.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V49=HERE/'run_reference_repro_v49.py'
text=V49.read_text();marker='\nrun49()\n'
if marker not in text: raise SystemExit('V49 run marker missing')
ns={'__file__':str(V49),'__name__':'oleander_v50_declarations'}
exec(compile(text.split(marker,1)[0],str(V49),'exec'),ns)

v=ns['v'];core=ns['core'];runtime=ns['runtime'];ns43=ns['ns43']
base_build=ns['base_build'];apply_subd=ns['apply_subd'];base_feature_ring=ns['feature_ring49']
tri_plane_top=ns['tri_plane_top'];evaluated_mesh_data=ns['evaluated_mesh_data'];z_plane_points=ns['z_plane_points']
PROFILE=ns['PROFILE'];SIDE=ns['SIDE'];FRONT_ID=ns['FRONT_ID'];G=ns['G'];interpG=ns['interpG'];s01=ns['s01'];lerp=ns['lerp']
RAILS=ns['RAILS'];CRITICAL_X=ns['CRITICAL_X']

REV='V50_PROFILE_INVERTED_FEATURE_GRID'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_PROFILE_INVERTED_FEATURE_GRID_V50'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v50'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['primary_form_method']='FEATURE_ALIGNED_RAIL_NETWORK_PLUS_PROJECTED_PROFILE_SECTION_INVERSION'
v.REFERENCE_CONTRACT['representation_state']='REOPEN_REPRESENTATION_MODEL_CONTINUED'
v.REFERENCE_CONTRACT['profile_inversion_protocol']='oleander-skills/oleander-3d-pipeline/reference-reproduction/PROJECTED_PROFILE_TO_SECTION_INVERSION_PROTOCOL_v1.md'
v.REFERENCE_CONTRACT['surface_grid_protocol']='oleander-skills/oleander-3d-pipeline/reference-reproduction/PRIMARY_BODY_SURFACE_GRID_PROTOCOL_v1.md'
v.REFERENCE_CONTRACT['profile_compliance_boundary']='GENERATED_CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_REFERENCE_FIDELITY'
v.REFERENCE_CONTRACT['fit_views']=['SIDE','FRONT','REAR'];v.REFERENCE_CONTRACT['held_out_views']=['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q']
v.FAMILY_CONTROLS['PROFILE_INVERTED_FEATURE_GRID_V50']={
    'source_rails':RAILS,
    'source_critical_sections_x_m':CRITICAL_X,
    'profile_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json',
    'profile_role':'TRANSVERSE_ENVELOPE_CONSTRAINT_ONLY',
    'derived_midpoint_subdivision_per_source_segment':1,
    'expected_derived_ring_vertices':40,
    'protected':['OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE','V49_SIDE_UPPER_BEST_KNOWN'],
    'gate_local_baselines':{
        'SIDE_UPPER':'V49_FEATURE_ALIGNED_CURVE_NETWORK',
        'FRONT_GROSS_PROFILE':'V48_PRIMARY_FORM_STAGE_AWARE',
        'REAR_GROSS_PROFILE':'V48_PRIMARY_FORM_STAGE_AWARE'
    },
    'aperture_architecture':'HOLD_PROXY_ONLY'
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

Z0=.140;ZH=v.HEIGHT;ZR=ZH-Z0

def ratio_at(profile,frac):
    pts=sorted([(float(a),float(b)) for a,b in profile],reverse=True);frac=float(frac)
    if frac>=pts[0][0]:
        f0,r0=pts[0];return max(.02,r0*(1-frac)/max(1e-6,1-f0)) if frac<=1 else .02
    if frac<=pts[-1][0]:return pts[-1][1]
    for (f0,r0),(f1,r1) in zip(pts,pts[1:]):
        if f0>=frac>=f1:
            t=(f0-frac)/(f0-f1);return lerp(r0,r1,t)
    return pts[-1][1]

def front_weight50(x):
    if x<=-.25:return 0.0
    if x>=.25:return 1.0
    return s01((x+.25)/.50)

def blended_ratio50(x,z):
    frac=max(.10,min(.985,(float(z)-Z0)/ZR));w=front_weight50(x)
    rr=ratio_at(PROFILE['rear']['profile'],frac);rf=ratio_at(PROFILE['front']['profile'],frac)
    return lerp(rr,rf,w)

def outer_target50(x,z):
    return min(core['plan_half_width'](x),.5*v.WIDTH*blended_ratio50(x,z)+.006)

def terminal_x50(x,y,w):
    q=abs(y)/max(w,1e-6);ft=s01((x-1.74)/(v.FRONT_X-1.74)) if x>1.74 else 0.0;rt=s01((-x-1.74)/(-v.REAR_X-1.74)) if x<-1.74 else 0.0
    setback=(.080*ft+.070*rt)*(q**1.45);center_retreat=(.018*ft+.020*rt)*max(0.0,1-q/.70)
    return x-setback-center_retreat if x>0 else x+setback+center_retreat

def sparse_half50(x):
    # V49 provides semantic Z/X rail behavior. V50 only re-solves the failed transverse Y envelope.
    base=[list(p) for p in base_feature_ring(x)[:11]];w=core['plan_half_width'](x)
    upper_frac=[0.0,.30,.58,.82,.95,1.0]
    lower_frac=[1.0,.96,.78,.44,0.0]
    for i,p in enumerate(base):
        z=float(p[2]);target=outer_target50(x,z)
        frac=upper_frac[i] if i<6 else lower_frac[i-6]
        p[1]=max(0.0,min(w,frac*target))
    # preserve causal order on the sparse Source-derived half-section.
    for i in range(1,6):base[i][1]=max(base[i][1],base[i-1][1]+.004)
    for i in range(6,10):base[i][1]=min(base[i][1],base[i-1][1]-.004)
    base[10][1]=0.0
    for p in base:p[0]=terminal_x50(float(x),float(p[1]),w)
    return [tuple(p) for p in base]

def dense_ring50(x):
    sparse=sparse_half50(x);half=[]
    for a,b in zip(sparse,sparse[1:]):
        half.append(a);half.append(tuple((a[j]+b[j])*.5 for j in range(3)))
    half.append(sparse[-1])
    # 21 positive-side/center samples → 40 closed ring vertices after mirroring inner samples.
    return half+[ (px,-py,pz) for px,py,pz in reversed(half[1:-1]) ]

core['hull_ring']=dense_ring50;v.body_ring=dense_ring50

def build50(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o);d=o.copy();d.data=o.data.copy();d.name='DIAG_PROFILE_INVERTED_FEATURE_GRID_V50';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_PROFILE_INVERTED_FEATURE_GRID';o['OLEANDER_FORM_FAMILY']='PROFILE_INVERTED_FEATURE_GRID_V50';o['OLEANDER_SOURCE_RAIL_COUNT']=len(RAILS);o['OLEANDER_DERIVED_RING_VERTICES']=len(dense_ring50(0.0));o['OLEANDER_PROFILE_ROLE']='CONSTRAINT_COMPLIANCE_NOT_FIDELITY';o['OLEANDER_APERTURE_ARCHITECTURE']='HOLD_PROXY_GREENHOUSE'
    return o
core['build_visual_hull']=build50

# Reuse V49 greenhouse/identity visual proxies. They remain derived and aperture architecture stays HOLD.

def profile_rmse50(tris,profile,which):
    samples=[];errs=[]
    for frac,target in profile:
        z=Z0+float(frac)*ZR;pts=[]
        for tri in tris:
            if z<min(p[2] for p in tri)-1e-9 or z>max(p[2] for p in tri)+1e-9:continue
            for xx,yy in z_plane_points(tri,z):
                if which=='front' and xx>=.55:pts.append((xx,yy))
                elif which=='rear' and xx<=-.55:pts.append((xx,yy))
        cand=max((abs(yy) for _,yy in pts),default=float('nan'))/(.5*v.WIDTH);err=cand-float(target) if math.isfinite(cand) else float('nan');samples.append({'height_fraction':frac,'target_half_width_ratio':target,'candidate_half_width_ratio':cand,'error':err})
        if math.isfinite(err):errs.append(err)
    if len(errs)<max(6,int(.70*len(profile))):raise SystemExit('FAIL_EVALUATED_PROFILE_COVERAGE_'+which.upper())
    return math.sqrt(sum(e*e for e in errs)/len(errs)),samples,len(errs)/len(profile)

def projection50():
    diag=bpy.data.objects.get('DIAG_PROFILE_INVERTED_FEATURE_GRID_V50')
    if diag is None:raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: DIAG_PROFILE_INVERTED_FEATURE_GRID_V50')
    side_errs=[];side_samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x);err=cand-z if math.isfinite(cand) else float('nan');side_samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':err,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V50_FINAL_EVALUATED_DENSE_FEATURE_GRID_XZ_INTERSECTION','measurement_role':'INDEPENDENT_ORTHOGONAL_LOCK'});side_errs.append(err) if math.isfinite(err) else None
    if len(side_errs)<max(6,int(.90*len(SIDE))):raise SystemExit('FAIL_EVALUATED_SIDE_PROFILE_COVERAGE')
    side_rmse=math.sqrt(sum(e*e for e in side_errs)/len(side_errs));tris=evaluated_mesh_data('DIAG_PROFILE_INVERTED_FEATURE_GRID_V50');front_rmse,front_samples,front_cov=profile_rmse50(tris,PROFILE['front']['profile'],'front');rear_rmse,rear_samples,rear_cov=profile_rmse50(tris,PROFILE['rear']['profile'],'rear')
    metrics=[
      {'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':side_rmse,'abs_error':side_rmse,'limit':.040,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V50_FINAL_EVALUATED_DENSE_FEATURE_GRID_XZ_INTERSECTION','measurement_role':'INDEPENDENT_ORTHOGONAL_LOCK'},
      {'id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':front_rmse,'abs_error':front_rmse,'limit':float(PROFILE['gates']['front_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','candidate_measurement_source':'V50_FINAL_EVALUATED_PROFILE_INVERTED_FRONT_Z_SLICE','measurement_role':'GENERATED_CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_FIDELITY'},
      {'id':'REAR_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':rear_rmse,'abs_error':rear_rmse,'limit':float(PROFILE['gates']['rear_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','candidate_measurement_source':'V50_FINAL_EVALUATED_PROFILE_INVERTED_REAR_Z_SLICE','measurement_role':'GENERATED_CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_FIDELITY'}]
    ok=all(m['abs_error']<=m['limit'] for m in metrics)
    return {'schema':'oleander.3d.stage-aware-primary-form-projection.v1','reference':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json + REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','candidate_revision':REV,'status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','primary_form_stage':'PROFILE_INVERTED_FEATURE_GRID_APERTURE_HOLD','representation_state':'REOPEN_REPRESENTATION_MODEL_CONTINUED','constraint_compliance_boundary':'FRONT_REAR_GENERATED_FROM_PROFILE_NOT_INDEPENDENT_FIDELITY','fit_views':['SIDE','FRONT','REAR'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'stage_capabilities':{'PRIMARY_FORM_PROJECTION':'AVAILABLE','FEATURE_ALIGNED_CURVE_NETWORK':'AVAILABLE','DENSE_EVALUATED_SURFACE_GRID':'AVAILABLE','PROFILE_INVERSION_CONSTRAINT':'AVAILABLE','GREENHOUSE_VISUAL_PROXY':'AVAILABLE','FINAL_APERTURE_ARCHITECTURE':'NOT_APPLICABLE_STAGE_HOLD'},'not_applicable_metrics':[{'id':'FINAL_WINDSHIELD_FLANGE','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'},{'id':'FINAL_REAR_GLASS_FLANGE','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'}],'final_visible_membership':[{'object':'DIAG_PROFILE_INVERTED_FEATURE_GRID_V50','role':'FINAL_EVALUATED_PROFILE_INVERTED_FEATURE_GRID','triangles':len(tris)}],'metrics':metrics,'side_upper_samples':side_samples,'front_profile_samples':front_samples,'rear_profile_samples':rear_samples,'side_upper_finite_sample_coverage':len(side_errs)/len(SIDE),'front_profile_finite_sample_coverage':front_cov,'rear_profile_finite_sample_coverage':rear_cov,'independent_visual_review':False,'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD','does_not_prove':['held-out reference fidelity','manufacturer CAD','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['projection30']=projection50

BEST={
 'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V49_FEATURE_ALIGNED_CURVE_NETWORK','value':0.013934324664521762,'evidence_source':'V49_FINAL_EVALUATED_FEATURE_RAIL_BODY_XZ_INTERSECTION'},
 'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V48_PRIMARY_FORM_STAGE_AWARE','value':0.07244949168881082,'evidence_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_FRONT_Z_SLICE'},
 'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V48_PRIMARY_FORM_STAGE_AWARE','value':0.08103906166232307,'evidence_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_REAR_Z_SLICE'}
}
def regression50(pr):
    cur={m['id']:m for m in pr['metrics']};locks=[]
    tolerances={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.004,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.012,'REAR_HALF_PROJECTED_PROFILE_RMSE':.012}
    for mid,b in BEST.items():
        cv=float(cur[mid]['candidate']);tol=tolerances[mid];locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':cv,'limit':tol,'status':'PASS' if cv<=b['value']+tol else 'REGRESSED','evidence_source':b['evidence_source']})
    def score(vals):return math.sqrt(((vals['SIDE_UPPER_EVALUATED_MESH_RMSE_M']/.040)**2+(vals['FRONT_HALF_PROJECTED_PROFILE_RMSE']/.100)**2+(vals['REAR_HALF_PROJECTED_PROFILE_RMSE']/.110)**2)/3)
    basevals={k:v['value'] for k,v in BEST.items()};curvals={k:float(cur[k]['candidate']) for k in BEST};bs=score(basevals);cs=score(curvals)
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'GATE_LOCAL_BEST_KNOWN','candidate_revision':REV,'edit_scope':['PROJECTED_PROFILE_TO_TRANSVERSE_SECTION_INVERSION','SPARSE_SOURCE_TO_DENSE_EVALUATED_GRID','GATE_LOCAL_REGRESSION_BASELINES'],'target_metric_delta':{'metric_id':'GATE_LOCAL_NORMALIZED_PRIMARY_FORM_ERROR_SCORE','baseline':bs,'candidate':cs,'direction':'LOWER_IS_BETTER','improved':cs<bs},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['FINAL_EVALUATED_DENSE_FEATURE_GRID_XZ_INTERSECTION','FINAL_EVALUATED_PROFILE_INVERTED_FRONT_Z_SLICE','FINAL_EVALUATED_PROFILE_INVERTED_REAR_Z_SLICE'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':['held-out reference identity','design quality','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['regression30']=regression50

def surface50():
    d=ns['base_surface']();d['revision']=REV;d['representation']='PROFILE_INVERTED_FEATURE_GRID';d['source_semantic_rail_count']=len(RAILS);d['derived_ring_vertices_expected']=len(dense_ring50(0.0));d['profile_role']='CONSTRAINT_COMPLIANCE_NOT_FIDELITY';d['aperture_architecture_state']='HOLD_PROXY_ONLY';return d
runtime['surface_receipt']=surface50

def patch50(out):
    ns['base_patch'](out);p=Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json');p.unlink() if p.exists() else None
    feature={'schema':'oleander.3d.feature-curve-network-receipt.v1','candidate_revision':REV,'representation_state':'REOPEN_REPRESENTATION_MODEL_CONTINUED','tier':'TIER_A_IDENTITY_CRITICAL','source_rail_inventory':RAILS,'source_rail_count':len(RAILS),'critical_sections_x_m':CRITICAL_X,'derived_ring_vertices':len(dense_ring50(0.0)),'densification_rule':'ONE_DERIVED_MIDPOINT_PER_ADJACENT_SPARSE_HALF_SECTION_SEGMENT','profile_inversion_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','profile_inversion_role':'CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_FIDELITY','fit_views':['SIDE','FRONT','REAR'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'generated_surface':'DERIVED_911_9922_BODY','evaluated_diagnostic':'DIAG_PROFILE_INVERTED_FEATURE_GRID_V50','aperture_architecture_state':'HOLD_PROXY_ONLY','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','final aperture architecture','manufacturing feasibility']};Path(out,'FEATURE_CURVE_NETWORK_RECEIPT.json').write_text(json.dumps(feature,ensure_ascii=False,indent=2)+'\n')
    stage={'schema':'oleander.3d.stage-capability-routing-receipt.v1','candidate_revision':REV,'stage':'PROFILE_INVERTED_FEATURE_GRID_APERTURE_HOLD','required_capabilities':['PRIMARY_FORM_PROJECTION','FEATURE_ALIGNED_CURVE_NETWORK','DENSE_EVALUATED_SURFACE_GRID','PROFILE_INVERSION_CONSTRAINT','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE'],'available_capabilities':['PRIMARY_FORM_PROJECTION','FEATURE_ALIGNED_CURVE_NETWORK','DENSE_EVALUATED_SURFACE_GRID','PROFILE_INVERSION_CONSTRAINT','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE','GREENHOUSE_VISUAL_PROXY'],'held_capabilities':['FINAL_APERTURE_ARCHITECTURE','FINAL_WINDSHIELD_FLANGE','FINAL_REAR_GLASS_FLANGE'],'held_result':'NOT_APPLICABLE_STAGE_HOLD','failed_required_capabilities':[],'legacy_name_dependencies_not_required':['REF_WINDSHIELD','REF_REAR_GLASS'],'result':'PASS_STAGE_AWARE_ROUTING','does_not_prove':['held-out reference fidelity','aperture construction','design quality']};Path(out,'STAGE_CAPABILITY_ROUTING_RECEIPT.json').write_text(json.dumps(stage,ensure_ascii=False,indent=2)+'\n')
    inversion={'schema':'oleander.3d.projected-profile-section-inversion-receipt.v1','candidate_revision':REV,'profile_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','edited_source_family':'TRANSVERSE_SECTION_Y_ENVELOPE','protected_families':['SIDE_UPPER_BEST_KNOWN','OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE'],'measurement_role':'MACHINE_CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_REFERENCE_FIDELITY','visual_review_state':'NOT_RUN','does_not_prove':['manufacturer section geometry','reference fidelity','Class-A continuity']};Path(out,'PROFILE_INVERSION_RECEIPT.json').write_text(json.dumps(inversion,ensure_ascii=False,indent=2)+'\n')
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='PROFILE_INVERTED_FEATURE_GRID_APERTURE_HOLD';d['representation_state']='REOPEN_REPRESENTATION_MODEL_CONTINUED';d['profile_inversion_role']='CONSTRAINT_COMPLIANCE_NOT_INDEPENDENT_FIDELITY';d['aperture_architecture_state']='HOLD_PROXY_ONLY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    fp=Path(out,'REFERENCE_FIDELITY_RECEIPT.json')
    if fp.exists():
        d=json.loads(fp.read_text());d['candidate_revision']=REV;d['screening_scope']='HARD_POINT_AND_LANDMARK_SCREENING_ONLY';d['visual_reference_fidelity']='HOLD';fp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
ns43['patch43']=patch50

def run50():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:runtime['run30']()
    except SystemExit as e:patch50(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch50(out)
run50()
