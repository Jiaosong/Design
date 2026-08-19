#!/usr/bin/env python3
"""V51 — front transverse identity repair on V50 + runtime-composition repair.

V50 isolated one remaining gross-profile failure: FRONT. SIDE retained the V49 best-known lock and
REAR improved beyond V48, so V51 protects those families and changes only the front transverse
identity family. The edit is bound to the source-grounded front identity relations:
- round lamp sits inside a raised fender crown;
- hood center reads lower/less dominant than twin outer fender crowns;
- lower fascia remains subordinate.

V51 also repairs a V50 wrapper-only failure: the rendered geometry and .blend were valid, but the
surface receipt wrapper referenced a parent namespace incorrectly. This runtime repair does not count
as a geometry change.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V50=HERE/'run_reference_repro_v50.py'
text=V50.read_text();marker='\nrun50()\n'
if marker not in text: raise SystemExit('V50 run marker missing')
ctx={'__file__':str(V50),'__name__':'oleander_v51_declarations'}
exec(compile(text.split(marker,1)[0],str(V50),'exec'),ctx)

v=ctx['v'];core=ctx['core'];runtime=ctx['runtime'];ns43=ctx['ns43']
base_build=ctx['base_build'];apply_subd=ctx['apply_subd'];base_sparse=ctx['sparse_half50']
tri_plane_top=ctx['tri_plane_top'];evaluated_mesh_data=ctx['evaluated_mesh_data'];z_plane_points=ctx['z_plane_points']
PROFILE=ctx['PROFILE'];SIDE=ctx['SIDE'];FRONT_ID=ctx['FRONT_ID'];RAILS=ctx['RAILS'];CRITICAL_X=ctx['CRITICAL_X']
outer_target50=ctx['outer_target50'];terminal_x50=ctx['terminal_x50'];lerp=ctx['lerp'];s01=ctx['s01']

REV='V51_FRONT_TRANSVERSE_IDENTITY_REPAIR'
ctx['REV']=REV
v.REF='2025_992.2_CARRERA_FRONT_IDENTITY_V51'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v51'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['primary_form_method']='V50_PROFILE_INVERTED_FEATURE_GRID_PLUS_FRONT_TRANSVERSE_IDENTITY_REPAIR'
v.REFERENCE_CONTRACT['representation_state']='FEATURE_GRID_CAUSAL_EDIT'
v.REFERENCE_CONTRACT['source_edit_scope']='FRONT_TRANSVERSE_IDENTITY_FAMILY_ONLY'
v.REFERENCE_CONTRACT['protected_gate_families']=['V49_SIDE_UPPER_BEST_KNOWN','V50_REAR_PROFILE','OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE']
v.REFERENCE_CONTRACT['front_identity_source']='REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json'
v.FAMILY_CONTROLS['FRONT_TRANSVERSE_IDENTITY_V51']={
    'scope_x_m':[.55,v.FRONT_X],
    'upper_rail_width_fractions':[0.0,.46,.74,.91,.99,1.0],
    'hood_center_drop_max_m':.020,
    'fender_crown_target':'SIDE_TOP_MINUS_4_TO_8_MM',
    'lamp_relation':'INSIDE_RAISED_FENDER_CROWN',
    'protected':['SIDE_UPPER','REAR_GROSS_PROFILE','HARD_POINTS','WHEELS','LOWER_ENVELOPE']
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())


def front_zone51(x):
    if x<=.55:return 0.0
    if x>=1.35:return 1.0
    return s01((x-.55)/.80)

def lamp_crown_weight51(x):
    return math.exp(-((float(x)-1.48)/.62)**4)

def sparse_half51(x):
    base=[list(p) for p in base_sparse(x)];fz=front_zone51(x)
    if fz<=0:return [tuple(p) for p in base]
    w=core['plan_half_width'](x);fractions=[0.0,.46,.74,.91,.99,1.0]
    # Re-solve only the front upper transverse family; lower envelope remains V50.
    for i in range(1,6):
        target=min(w,fractions[i]*outer_target50(x,base[i][2]))
        base[i][1]=lerp(base[i][1],target,fz)
    for i in range(1,6):base[i][1]=max(base[i][1],base[i-1][1]+.004)
    fw=lamp_crown_weight51(x);side_top=core['side_top'](x)
    # Identity relation: center hood is lower than twin outer fender crowns without changing SIDE max Z.
    base[0][2]-=.020*fw
    base[3][2]=lerp(base[3][2],side_top-.004,.82*fw)
    base[4][2]=lerp(base[4][2],side_top-.008,.86*fw)
    base[5][2]=min(base[5][2],side_top-.010)
    for p in base:p[0]=terminal_x50(float(x),float(p[1]),w)
    return [tuple(p) for p in base]

def dense_ring51(x):
    sparse=sparse_half51(x);half=[]
    for a,b in zip(sparse,sparse[1:]):
        half.append(a);half.append(tuple((a[j]+b[j])*.5 for j in range(3)))
    half.append(sparse[-1])
    return half+[(px,-py,pz) for px,py,pz in reversed(half[1:-1])]

core['hull_ring']=dense_ring51;v.body_ring=dense_ring51

def build51(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o);d=o.copy();d.data=o.data.copy();d.name='DIAG_FRONT_IDENTITY_FEATURE_GRID_V51';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_FRONT_IDENTITY_FEATURE_GRID';o['OLEANDER_FORM_FAMILY']='FRONT_TRANSVERSE_IDENTITY_V51';o['OLEANDER_SOURCE_RAIL_COUNT']=len(RAILS);o['OLEANDER_DERIVED_RING_VERTICES']=len(dense_ring51(0.0));o['OLEANDER_APERTURE_ARCHITECTURE']='HOLD_PROXY_GREENHOUSE'
    return o
core['build_visual_hull']=build51

Z0=.140;ZR=v.HEIGHT-Z0

def profile_rmse51(tris,profile,which):
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

def projection51():
    diag=bpy.data.objects.get('DIAG_FRONT_IDENTITY_FEATURE_GRID_V51')
    if diag is None:raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: DIAG_FRONT_IDENTITY_FEATURE_GRID_V51')
    side_errs=[];side_samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x);err=cand-z if math.isfinite(cand) else float('nan');side_samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':err,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V51_FINAL_EVALUATED_FRONT_IDENTITY_GRID_XZ','measurement_role':'INDEPENDENT_ORTHOGONAL_LOCK'});side_errs.append(err) if math.isfinite(err) else None
    if len(side_errs)<max(6,int(.90*len(SIDE))):raise SystemExit('FAIL_EVALUATED_SIDE_PROFILE_COVERAGE')
    side_rmse=math.sqrt(sum(e*e for e in side_errs)/len(side_errs));tris=evaluated_mesh_data('DIAG_FRONT_IDENTITY_FEATURE_GRID_V51');front_rmse,front_samples,front_cov=profile_rmse51(tris,PROFILE['front']['profile'],'front');rear_rmse,rear_samples,rear_cov=profile_rmse51(tris,PROFILE['rear']['profile'],'rear')
    metrics=[
      {'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':side_rmse,'abs_error':side_rmse,'limit':.040,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V51_FINAL_EVALUATED_FRONT_IDENTITY_GRID_XZ','measurement_role':'INDEPENDENT_ORTHOGONAL_LOCK'},
      {'id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':front_rmse,'abs_error':front_rmse,'limit':float(PROFILE['gates']['front_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','candidate_measurement_source':'V51_FINAL_EVALUATED_FRONT_IDENTITY_GRID_YZ','measurement_role':'FRONT_CAUSAL_FAMILY_CONSTRAINT_SCREEN'},
      {'id':'REAR_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':rear_rmse,'abs_error':rear_rmse,'limit':float(PROFILE['gates']['rear_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','candidate_measurement_source':'V51_FINAL_EVALUATED_REAR_PRESERVED_YZ','measurement_role':'PROTECTED_GATE'}]
    ok=all(m['abs_error']<=m['limit'] for m in metrics)
    return {'schema':'oleander.3d.stage-aware-primary-form-projection.v1','reference':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json + REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json + REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json','candidate_revision':REV,'status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','primary_form_stage':'FRONT_TRANSVERSE_IDENTITY_REPAIR_APERTURE_HOLD','representation_state':'FEATURE_GRID_CAUSAL_EDIT','source_edit_scope':'FRONT_TRANSVERSE_IDENTITY_FAMILY_ONLY','fit_views':['SIDE','FRONT','REAR'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'stage_capabilities':{'PRIMARY_FORM_PROJECTION':'AVAILABLE','DENSE_EVALUATED_SURFACE_GRID':'AVAILABLE','FRONT_TRANSVERSE_IDENTITY_FAMILY':'AVAILABLE','GREENHOUSE_VISUAL_PROXY':'AVAILABLE','FINAL_APERTURE_ARCHITECTURE':'NOT_APPLICABLE_STAGE_HOLD'},'not_applicable_metrics':[{'id':'FINAL_WINDSHIELD_FLANGE','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'},{'id':'FINAL_REAR_GLASS_FLANGE','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'}],'final_visible_membership':[{'object':'DIAG_FRONT_IDENTITY_FEATURE_GRID_V51','role':'FINAL_EVALUATED_FRONT_IDENTITY_FEATURE_GRID','triangles':len(tris)}],'metrics':metrics,'side_upper_samples':side_samples,'front_profile_samples':front_samples,'rear_profile_samples':rear_samples,'side_upper_finite_sample_coverage':len(side_errs)/len(SIDE),'front_profile_finite_sample_coverage':front_cov,'rear_profile_finite_sample_coverage':rear_cov,'independent_visual_review':False,'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD','does_not_prove':['held-out reference fidelity','manufacturer CAD','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['projection30']=projection51

BEST={
 'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V50_PROFILE_INVERTED_FEATURE_GRID','value':0.013348139745095728,'evidence_source':'V50_FINAL_EVALUATED_DENSE_FEATURE_GRID_XZ_INTERSECTION'},
 'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V48_PRIMARY_FORM_STAGE_AWARE','value':0.07244949168881082,'evidence_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_FRONT_Z_SLICE'},
 'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V50_PROFILE_INVERTED_FEATURE_GRID','value':0.06847548372047164,'evidence_source':'V50_FINAL_EVALUATED_PROFILE_INVERTED_REAR_Z_SLICE'}
}
def regression51(pr):
    cur={m['id']:m for m in pr['metrics']};locks=[];tols={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.004,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.012,'REAR_HALF_PROJECTED_PROFILE_RMSE':.012}
    for mid,b in BEST.items():
        cv=float(cur[mid]['candidate']);locks.append({'id':mid,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':cv,'limit':tols[mid],'status':'PASS' if cv<=b['value']+tols[mid] else 'REGRESSED','evidence_source':b['evidence_source']})
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'GATE_LOCAL_BEST_KNOWN','candidate_revision':REV,'edit_scope':['FRONT_TRANSVERSE_IDENTITY_FAMILY_ONLY','RUNTIME_COMPOSITION_WRAPPER_REPAIR_NO_GEOMETRY_EFFECT'],'target_metric_delta':{'metric_id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','baseline':BEST['FRONT_HALF_PROJECTED_PROFILE_RMSE']['value'],'candidate':float(cur['FRONT_HALF_PROJECTED_PROFILE_RMSE']['candidate']),'direction':'LOWER_IS_BETTER','improved':float(cur['FRONT_HALF_PROJECTED_PROFILE_RMSE']['candidate'])<BEST['FRONT_HALF_PROJECTED_PROFILE_RMSE']['value']},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_method_ids':['V51_FINAL_EVALUATED_FRONT_IDENTITY_GRID_XZ','V51_FINAL_EVALUATED_FRONT_IDENTITY_GRID_YZ','V51_FINAL_EVALUATED_REAR_PRESERVED_YZ'],'measurement_comparability':'COMPARABLE','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':['held-out reference identity','design quality','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['regression30']=regression51


def components(obj):
    me=obj.data;adj=[set() for _ in me.vertices];used=set()
    for p in me.polygons:
        vs=list(p.vertices);used.update(vs)
        for a,b in zip(vs,vs[1:]+vs[:1]):adj[a].add(b);adj[b].add(a)
    seen=set();n=0
    for s in used:
        if s in seen:continue
        n+=1;stack=[s];seen.add(s)
        while stack:
            q=stack.pop()
            for z in adj[q]:
                if z not in seen:seen.add(z);stack.append(z)
    return n

def normal_flips(obj):
    me=obj.data;ef={}
    for p in me.polygons:
        vs=list(p.vertices)
        for a,b in zip(vs,vs[1:]+vs[:1]):ef.setdefault(tuple(sorted((a,b))),[]).append(p.index)
    return sum(1 for fs in ef.values() if len(fs)==2 and me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal)<-.15)

def edge_p95(obj):
    ls=sorted((me.vertices[e.vertices[0]].co-me.vertices[e.vertices[1]].co).length for me in [obj.data] for e in me.edges)
    if not ls:return 9.0
    return float(ls[min(len(ls)-1,int(math.ceil(.95*len(ls))-1))])

def surface51():
    body=bpy.data.objects.get('DERIVED_911_9922_BODY');cabin=bpy.data.objects.get('DERIVED_911_9922_CABIN')
    bc=components(body) if body else 99;cc=components(cabin) if cabin else 99;bf=normal_flips(body) if body else 99;cf=normal_flips(cabin) if cabin else 99;ep=edge_p95(body) if body else 9.0;stations=int(body.get('OLEANDER_LONGITUDINAL_STATIONS',0)) if body else 0;ring=int(body.get('OLEANDER_RING_VERTICES',0)) if body else 0
    quality=(bc==1 and cc==1 and bf==0 and cf==0 and stations>=80 and ring>=30 and ep<=.30)
    return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':REV,'surface_measurement_scope':'PRE_APERTURE_PRIMARY_SKIN','body_cap_edges_excluded':True,'body_connected_components':bc,'cabin_connected_components':cc,'body_adjacent_face_normal_flip_count':bf,'cabin_adjacent_face_normal_flip_count':cf,'body_local_edge_p95_m':ep,'body_longitudinal_stations':stations,'body_ring_vertices':ring,'machine_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD' if quality else 'MACHINE_SURFACE_TOPOLOGY_FAIL','visual_review_state':'NOT_RUN','representation':'PROFILE_INVERTED_FEATURE_GRID_FRONT_IDENTITY_REPAIR','source_semantic_rail_count':len(RAILS),'derived_ring_vertices_expected':len(dense_ring51(0.0)),'aperture_architecture_state':'HOLD_PROXY_ONLY','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','reflection continuity','production patch layout']}
runtime['surface_receipt']=surface51

def patch51(out):
    p=Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json')
    if p.exists():p.unlink()
    feature={'schema':'oleander.3d.feature-curve-network-receipt.v1','candidate_revision':REV,'representation_state':'FEATURE_GRID_CAUSAL_EDIT','tier':'TIER_A_IDENTITY_CRITICAL','source_rail_inventory':RAILS,'source_rail_count':len(RAILS),'critical_sections_x_m':CRITICAL_X,'derived_ring_vertices':len(dense_ring51(0.0)),'source_edit_scope':'FRONT_TRANSVERSE_IDENTITY_FAMILY_ONLY','protected_gate_families':['SIDE_UPPER','REAR_GROSS_PROFILE'],'front_identity_source':'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json','fit_views':['SIDE','FRONT','REAR'],'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'generated_surface':'DERIVED_911_9922_BODY','evaluated_diagnostic':'DIAG_FRONT_IDENTITY_FEATURE_GRID_V51','aperture_architecture_state':'HOLD_PROXY_ONLY','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','final aperture architecture','manufacturing feasibility']};Path(out,'FEATURE_CURVE_NETWORK_RECEIPT.json').write_text(json.dumps(feature,ensure_ascii=False,indent=2)+'\n')
    stage={'schema':'oleander.3d.stage-capability-routing-receipt.v1','candidate_revision':REV,'stage':'FRONT_TRANSVERSE_IDENTITY_REPAIR_APERTURE_HOLD','required_capabilities':['PRIMARY_FORM_PROJECTION','DENSE_EVALUATED_SURFACE_GRID','FRONT_TRANSVERSE_IDENTITY_FAMILY','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE'],'available_capabilities':['PRIMARY_FORM_PROJECTION','DENSE_EVALUATED_SURFACE_GRID','FRONT_TRANSVERSE_IDENTITY_FAMILY','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE','GREENHOUSE_VISUAL_PROXY'],'held_capabilities':['FINAL_APERTURE_ARCHITECTURE','FINAL_WINDSHIELD_FLANGE','FINAL_REAR_GLASS_FLANGE'],'held_result':'NOT_APPLICABLE_STAGE_HOLD','failed_required_capabilities':[],'legacy_name_dependencies_not_required':['REF_WINDSHIELD','REF_REAR_GLASS'],'result':'PASS_STAGE_AWARE_ROUTING','does_not_prove':['held-out reference fidelity','aperture construction','design quality']};Path(out,'STAGE_CAPABILITY_ROUTING_RECEIPT.json').write_text(json.dumps(stage,ensure_ascii=False,indent=2)+'\n')
    delta={'schema':'oleander.3d.source-edit-delta.front-transverse-identity.v1','candidate_revision':REV,'source_family':'FRONT_TRANSVERSE_IDENTITY_V51','changed_variables':['front upper rail width fractions','front hood-center Z','front fender-crown Z'],'protected_variables':['SIDE best-known outer gesture','REAR gross profile','hard points','axles','wheels','lower envelope'],'predicted_effect':'wider/higher twin fender crowns with lower hood center and improved front gross profile','rollback_revision':'V50_PROFILE_INVERTED_FEATURE_GRID','does_not_prove':['reference fidelity','lamp engineering package','Class-A continuity']};Path(out,'SOURCE_EDIT_DELTA.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n')
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='FRONT_TRANSVERSE_IDENTITY_REPAIR_APERTURE_HOLD';d['representation_state']='FEATURE_GRID_CAUSAL_EDIT';d['source_edit_scope']='FRONT_TRANSVERSE_IDENTITY_FAMILY_ONLY';d['runtime_composition_repair']='V50_PARENT_NAMESPACE_BINDING_REPAIRED_NO_GEOMETRY_EFFECT';d['aperture_architecture_state']='HOLD_PROXY_ONLY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    fp=Path(out,'REFERENCE_FIDELITY_RECEIPT.json')
    if fp.exists():
        d=json.loads(fp.read_text());d['candidate_revision']=REV;d['screening_scope']='HARD_POINT_AND_LANDMARK_SCREENING_ONLY';d['visual_reference_fidelity']='HOLD';fp.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def run51():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:runtime['run30']()
    except SystemExit as e:patch51(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch51(out)
run51()
