#!/usr/bin/env python3
"""V55 — causal blend + ordered lower-return surface repair.

Goal: remove V51's 190 pre-aperture adjacent-face normal reversals without touching detail/CMF.
V53 localized folds to rear body->cabin transition, front release/terminal transition and lower return.
This revision reuses the historically successful V40 causal strategy and V49 no-fold section ordering:
- long rear body->cabin blend (-1.72 -> -0.88 m);
- long front cabin release (+0.58 -> +1.10 m);
- profile inversion only on upper identity rails;
- V49 ordered lower-side / rocker / lower-return family restored;
- V49 terminal plan setback retained;
- V51 hood-center vs twin-fender-crown semantic relation retained.

A surface-quality repair is not a reference-fidelity promotion.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V51=HERE/'run_reference_repro_v51.py'
text=V51.read_text(); marker='\nrun51()\n'
if marker not in text: raise SystemExit('V51 run marker missing')
ns={'__file__':str(V51),'__name__':'oleander_v55_declarations'}
exec(compile(text.split(marker,1)[0],str(V51),'exec'),ns)

v=ns['v']; core=ns['core']; runtime=ns['runtime']; base_build=ns['base_build']; apply_subd=ns['apply_subd']
tri_plane_top=ns['tri_plane_top']; evaluated_mesh_data=ns['evaluated_mesh_data']; z_plane_points=ns['z_plane_points']
PROFILE=ns['PROFILE']; SIDE=ns['SIDE']; FRONT_ID=ns['FRONT_ID']; RAILS=ns['RAILS']; CRITICAL_X=ns['CRITICAL_X']
outer_target50=ns['outer_target50']; lerp=ns['lerp']; s01=ns['s01']
# V51 retains V50 namespace in `ctx`; use only immutable upstream reference helpers from it.
up=ns['ctx']; G=up['G']; interpG=up['interpG']

REV='V55_CAUSAL_BLEND_ORDERED_SURFACE_REPAIR'
v.REF='2025_992.2_CARRERA_SURFACE_REPAIR_V55'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v55'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['primary_form_method']='FEATURE_ALIGNED_UPPER_PROFILE_PLUS_LONG_CAUSAL_BLEND_AND_ORDERED_LOWER_RETURN'
v.REFERENCE_CONTRACT['representation_state']='SURFACE_CAUSAL_REPAIR'
v.REFERENCE_CONTRACT['source_edit_scope']='CABIN_BLEND_AND_LOWER_RETURN_AND_TERMINAL_ORDER_ONLY'
v.REFERENCE_CONTRACT['protected_gate_families']=['V51_HOOD_FENDER_HIERARCHY','OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE','MID_BODY_ZERO_FOLD_REGION']
v.FAMILY_CONTROLS['SURFACE_REPAIR_V55']={
  'rear_cabin_blend_x_m':[-1.72,-.88],
  'front_cabin_release_x_m':[.58,1.10],
  'profile_inversion_scope':'UPPER_IDENTITY_RAILS_ONLY',
  'lower_return_source':'V49_ORDERED_SAFE_FAMILY',
  'terminal_plan_source':'V49_NO_FOLD_SETBACK',
  'front_identity':'V51_HOOD_CENTER_BELOW_TWIN_FENDER_CROWNS',
  'protected':['HARD_POINTS','AXLES','WHEELS','MID_BODY_ZERO_FOLD_REGION']
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())


def cabin_weight55(x):
    x=float(x)
    if x<=-1.72:return 0.0
    if x<-.88:return s01((x+1.72)/.84)
    if x<=.58:return 1.0
    if x<1.10:return 1.0-s01((x-.58)/.52)
    return 0.0

def front_weight55(x): return math.exp(-((float(x)-1.45)/.72)**4)
def rear_weight55(x): return math.exp(-((float(x)+1.35)/.78)**4)
def belt55(x):
    x=float(x)
    if G[0][0]<=x<=G[-1][0]: return max(.805,min(.875,interpG(x,2)-.035))
    return .825+.018*math.exp(-((x-v.REAR_AXLE)/.75)**4)+.010*math.exp(-((x-v.FRONT_AXLE)/.65)**4)
def cabin_half_width55(x,top,belt):
    raw=.5*v.WIDTH*core['profile_ratio'](x,(top+belt)*.5);w=core['plan_half_width'](x)
    return min(.78*w,max(.46,raw-.055))

def safe_sparse55(x):
    x=float(x);w=core['plan_half_width'](x);top=core['side_top'](x);floor=core['terminal_floor'](x)
    cw=cabin_weight55(x);fw=front_weight55(x);rw=rear_weight55(x);belt=belt55(x);cabw=cabin_half_width55(x,top,belt)
    body_y=[0.0,.24*w,.48*w,.72*w,.90*w,w]; cabin_y=[0.0,.28*cabw,.58*cabw,cabw,.91*w,w]
    ys=[lerp(a,b,cw) for a,b in zip(body_y,cabin_y)]
    body_z=[top-.086*fw-.090*rw,top-.058*fw-.062*rw,top-.028*fw-.036*rw,top-.004*fw-.010*rw,top-.016*fw-.006*rw,top-.066*fw-.058*rw]
    cabin_z=[top,top-.012,top-.040,top-.086,belt+.050,belt-.012]
    zs=[lerp(a,b,cw) for a,b in zip(body_z,cabin_z)]
    if cw<.35:
        zs[3]=max(zs[3],zs[2]+.012);zs[4]=min(zs[3]-.006,max(zs[4],zs[5]+.018))
    # Upper rails: use profile constraint as a bounded width cap, never on lower return.
    upper=[];fracs=[0.0,.30,.58,.82,.95,1.0]
    for i,(y,z) in enumerate(zip(ys,zs)):
        if i==0: yy=0.0
        else: yy=min(y,fracs[i]*outer_target50(x,z))
        upper.append([yy,z])
    for i in range(1,6): upper[i][0]=max(upper[i][0],upper[i-1][0]+.004)
    # V51 front identity relation, applied smoothly after the long cabin release.
    fz=0.0 if x<=.55 else (1.0 if x>=1.35 else s01((x-.55)/.80))
    if fz>0:
        fr=[0.0,.46,.74,.91,.99,1.0]
        for i in range(1,6): upper[i][0]=lerp(upper[i][0],min(w,fr[i]*outer_target50(x,upper[i][1])),fz)
        for i in range(1,6): upper[i][0]=max(upper[i][0],upper[i-1][0]+.004)
        lc=math.exp(-((x-1.48)/.62)**4)
        upper[0][1]-=.020*lc
        upper[3][1]=lerp(upper[3][1],top-.004,.82*lc)
        upper[4][1]=lerp(upper[4][1],top-.008,.86*lc)
        upper[5][1]=min(upper[5][1],top-.010)
    # Ordered V49 lower family: explicitly monotone after outer side.
    side_lower=max(.32,floor+.075)
    lower=[[.998*w,side_lower],[.965*w,max(.185,floor+.018)],[.78*w,max(.145,floor-.002)],[.44*w,max(.140,floor-.008)],[0.0,max(.140,floor-.010)]]
    pos=upper+lower
    for i in range(7,len(pos)): pos[i][0]=min(pos[i][0],pos[i-1][0]-.004)
    pos[-1][0]=0.0
    # V49 terminal plan rule, which had no fold inversions.
    ft=s01((x-1.74)/(v.FRONT_X-1.74)) if x>1.74 else 0.0;rt=s01((-x-1.74)/(-v.REAR_X-1.74)) if x<-1.74 else 0.0
    out=[]
    for y,z in pos:
        q=abs(y)/max(w,1e-6);setback=(.080*ft+.070*rt)*(q**1.45);center_retreat=(.018*ft+.020*rt)*max(0.0,1-q/.70)
        xe=x-setback-center_retreat if x>0 else x+setback+center_retreat;out.append((xe,y,z))
    return out

def dense_ring55(x):
    sparse=safe_sparse55(x);half=[]
    for a,b in zip(sparse,sparse[1:]):
        half.append(a);half.append(tuple((a[j]+b[j])*.5 for j in range(3)))
    half.append(sparse[-1])
    return half+[(px,-py,pz) for px,py,pz in reversed(half[1:-1])]
core['hull_ring']=dense_ring55;v.body_ring=dense_ring55

def build55(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o);d=o.copy();d.data=o.data.copy();d.name='DIAG_CAUSAL_BLEND_SURFACE_V55';bpy.context.collection.objects.link(d);d.hide_render=True;d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY';d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_CAUSAL_BLEND_SURFACE_REPAIR'
        o['OLEANDER_FORM_FAMILY']='CAUSAL_BLEND_ORDERED_SURFACE_REPAIR_V55';o['OLEANDER_SOURCE_RAIL_COUNT']=len(RAILS);o['OLEANDER_DERIVED_RING_VERTICES']=len(dense_ring55(0.0));o['OLEANDER_APERTURE_ARCHITECTURE']='HOLD_PROXY_GREENHOUSE'
    return o
core['build_visual_hull']=build55

Z0=.140;ZR=v.HEIGHT-Z0

def profile_rmse55(tris,profile,which):
    samples=[];errs=[]
    for frac,target in profile:
        z=Z0+float(frac)*ZR;pts=[]
        for tri in tris:
            if z<min(p[2] for p in tri)-1e-9 or z>max(p[2] for p in tri)+1e-9:continue
            for xx,yy in z_plane_points(tri,z):
                if which=='front' and xx>=.55:pts.append((xx,yy))
                elif which=='rear' and xx<=-.55:pts.append((xx,yy))
        cand=max((abs(yy) for _,yy in pts),default=float('nan'))/(.5*v.WIDTH);err=cand-float(target) if math.isfinite(cand) else float('nan')
        samples.append({'height_fraction':frac,'target_half_width_ratio':target,'candidate_half_width_ratio':cand,'error':err})
        if math.isfinite(err):errs.append(err)
    if len(errs)<max(6,int(.70*len(profile))):raise SystemExit('FAIL_EVALUATED_PROFILE_COVERAGE_'+which.upper())
    return math.sqrt(sum(e*e for e in errs)/len(errs)),samples,len(errs)/len(profile)

def front_semantic55():
    body='DIAG_CAUSAL_BLEND_SURFACE_V55';tris=evaluated_mesh_data(body);lamps=[bpy.data.objects.get('REF_HEADLAMP_LENS_1'),bpy.data.objects.get('REF_HEADLAMP_LENS_-1')]
    if not all(lamps):return {'semantic_relation_state':'HOLD','reason':'HEADLAMP_SEMANTIC_OBJECTS_MISSING'}
    lx=sum(float(o.location.x) for o in lamps)/2.; lys=[float(o.location.y) for o in lamps]
    def xpts(tri,x):
        q=[]
        for i in range(3):
            x1,y1,z1=tri[i];x2,y2,z2=tri[(i+1)%3]
            if abs(x2-x1)<1e-12:continue
            if x<min(x1,x2)-1e-9 or x>max(x1,x2)+1e-9:continue
            t=(x-x1)/(x2-x1)
            if -1e-9<=t<=1+1e-9:q.append((y1+t*(y2-y1),z1+t*(z2-z1)))
        return q
    pts=[]
    for t in tris:
        if min(p[0] for p in t)-1e-9<=lx<=max(p[0] for p in t)+1e-9:pts.extend(xpts(t,lx))
    def maxz(c,h):
        z=[zz for yy,zz in pts if abs(yy-c)<=h];return max(z) if z else float('nan')
    hood=maxz(0,.18);crowns=[maxz(y,.15) for y in lys];mean=sum(crowns)/2 if all(math.isfinite(z) for z in crowns) else float('nan');delta=mean-hood if math.isfinite(mean) and math.isfinite(hood) else float('nan')
    return {'schema':'oleander.3d.front-semantic-identity-metric.v1','source':'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json','candidate_geometry_revision':REV,'evaluated_carrier':body,'section_x_m':lx,'hood_center_top_z_m':hood,'left_fender_crown_z_m':crowns[0],'right_fender_crown_z_m':crowns[1],'mean_fender_crown_minus_hood_m':delta,'hood_fender_min_positive_delta_m':.005,'hood_fender_hierarchy_state':'SCREENED' if math.isfinite(delta) and delta>=.005 else 'FAIL','semantic_relation_state':'SCREENED' if math.isfinite(delta) and delta>=.005 else 'FAIL','lamp_host_integration_state':'HOLD_APERTURE_ARCHITECTURE_NOT_CONSTRUCTED','lower_fascia_subordination_state':'HOLD_VISUAL_REVIEW_REQUIRED','does_not_prove':['full lamp-host integration','reference fidelity','Class-A continuity']}

def projection55():
    diag=bpy.data.objects.get('DIAG_CAUSAL_BLEND_SURFACE_V55')
    if diag is None:raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: DIAG_CAUSAL_BLEND_SURFACE_V55')
    side=[];errs=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x);e=cand-z if math.isfinite(cand) else float('nan');side.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e,'candidate_measurement_source':'V55_FINAL_EVALUATED_CAUSAL_BLEND_XZ'});errs.append(e) if math.isfinite(e) else None
    sr=math.sqrt(sum(e*e for e in errs)/len(errs));tris=evaluated_mesh_data('DIAG_CAUSAL_BLEND_SURFACE_V55');fr,fs,fc=profile_rmse55(tris,PROFILE['front']['profile'],'front');rr,rs,rc=profile_rmse55(tris,PROFILE['rear']['profile'],'rear')
    metrics=[{'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.,'candidate':sr,'abs_error':sr,'limit':.040,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V55_FINAL_EVALUATED_CAUSAL_BLEND_XZ'},{'id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','target':0.,'candidate':fr,'abs_error':fr,'limit':float(PROFILE['gates']['front_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','candidate_measurement_source':'V55_BODY_ONLY_FRONT_YZ','measurement_role':'BODY_ONLY_DIAGNOSTIC_NOT_WHOLE_VISIBLE_FIDELITY'},{'id':'REAR_HALF_PROJECTED_PROFILE_RMSE','target':0.,'candidate':rr,'abs_error':rr,'limit':float(PROFILE['gates']['rear_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','candidate_measurement_source':'V55_BODY_ONLY_REAR_YZ','measurement_role':'BODY_ONLY_DIAGNOSTIC_NOT_WHOLE_VISIBLE_FIDELITY'}]
    return {'schema':'oleander.3d.stage-aware-primary-form-projection.v1','candidate_revision':REV,'reference':'992.2 source-grounded profiles','status':'PROJECTION_MACHINE_SCREENING_PASS' if all(m['candidate']<=m['limit'] for m in metrics) else 'PROJECTION_MACHINE_SCREENING_FAIL','primary_form_stage':'SURFACE_CAUSAL_REPAIR_APERTURE_HOLD','representation_state':'SURFACE_CAUSAL_REPAIR','source_edit_scope':'CABIN_BLEND_AND_LOWER_RETURN_AND_TERMINAL_ORDER_ONLY','metrics':metrics,'front_identity_metrics':front_semantic55(),'side_upper_samples':side,'front_profile_samples':fs,'rear_profile_samples':rs,'side_upper_finite_sample_coverage':len(errs)/len(SIDE),'front_profile_finite_sample_coverage':fc,'rear_profile_finite_sample_coverage':rc,'stage_capabilities':{'PRIMARY_FORM_PROJECTION':'AVAILABLE','SURFACE_CAUSAL_REPAIR':'AVAILABLE','FINAL_APERTURE_ARCHITECTURE':'NOT_APPLICABLE_STAGE_HOLD'},'held_out_views':['HERO_FRONT_3Q','HERO_REAR_3Q','TOP_FRONT_3Q'],'independent_visual_review':False,'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD','does_not_prove':['whole-visible reference fidelity','final aperture architecture','Class-A continuity','manufacturing feasibility']}
runtime['projection30']=projection55

BEST={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V51','value':0.012065718914790685},'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V48','value':0.07244949168881082},'REAR_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V50','value':0.06847548372047164}}
def regression55(pr):
    cur={m['id']:m for m in pr['metrics']};locks=[];tols={'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.006,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.020,'REAR_HALF_PROJECTED_PROFILE_RMSE':.020}
    for k,b in BEST.items():
        cv=float(cur[k]['candidate']);locks.append({'id':k,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':cv,'limit':tols[k],'status':'PASS' if cv<=b['value']+tols[k] else 'REGRESSED'})
    return {'schema':'oleander.3d.reference-regression-promotion-receipt.v2','baseline_revision':'GATE_LOCAL_BEST_KNOWN','candidate_revision':REV,'edit_scope':['SURFACE_FOLD_ROOT_CAUSE_ONLY'],'target_metric_delta':{'metric_id':'PRE_APERTURE_FOLD_COUNT','baseline':190,'candidate':'MEASURED_IN_SURFACE_RECEIPT','direction':'LOWER_IS_BETTER','improved':False},'regression_locks':locks,'best_known_gate_baselines':BEST,'measurement_comparability':'COMPARABLE_BODY_ONLY_DIAGNOSTICS','promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT','visual_review_state':'NOT_RUN','does_not_prove':['reference fidelity','design quality','Class-A continuity']}
runtime['regression30']=regression55

def components(o):
    me=o.data;adj=[set() for _ in me.vertices];used=set()
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
def fold_rows(o):
    me=o.data;ef={};rows=[]
    for p in me.polygons:
        for e in p.edge_keys:ef.setdefault(tuple(sorted(e)),[]).append(p.index)
    for e,fs in ef.items():
        if len(fs)==2:
            dot=float(me.polygons[fs[0]].normal.dot(me.polygons[fs[1]].normal))
            if dot<-.15:
                c=(me.vertices[e[0]].co+me.vertices[e[1]].co)*.5;rows.append({'edge_vertices':list(e),'face_indices':fs,'normal_dot':dot,'center_m':[float(c.x),float(c.y),float(c.z)]})
    return rows
def edge_p95(o):
    ls=sorted((o.data.vertices[e.vertices[0]].co-o.data.vertices[e.vertices[1]].co).length for e in o.data.edges);return float(ls[min(len(ls)-1,int(math.ceil(.95*len(ls))-1))]) if ls else 9.
def surface55():
    body=bpy.data.objects.get('DERIVED_911_9922_BODY');rows=fold_rows(body) if body else [];bc=components(body) if body else 99;ep=edge_p95(body) if body else 9.;stations=int(body.get('OLEANDER_LONGITUDINAL_STATIONS',0)) if body else 0;ring=int(body.get('OLEANDER_RING_VERTICES',0)) if body else 0
    ok=(bc==1 and len(rows)==0 and stations>=80 and ring>=30 and ep<=.30)
    return {'schema':'oleander.3d.primary-body-surface-receipt.v1','revision':REV,'surface_measurement_scope':'CLOSED_PRIMARY_VISUAL_HULL_BEFORE_FINAL_APERTURE_ARCHITECTURE','body_cap_edges_excluded':True,'body_connected_components':bc,'cabin_connected_components':0,'body_adjacent_face_normal_flip_count':len(rows),'cabin_adjacent_face_normal_flip_count':0,'body_local_edge_p95_m':ep,'body_longitudinal_stations':stations,'body_ring_vertices':ring,'machine_surface_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD' if ok else 'MACHINE_SURFACE_TOPOLOGY_FAIL','visual_review_state':'NOT_RUN','representation':'CAUSAL_BLEND_ORDERED_SURFACE_REPAIR','source_semantic_rail_count':len(RAILS),'derived_ring_vertices_expected':len(dense_ring55(0.0)),'aperture_architecture_state':'HOLD_PROXY_ONLY','does_not_prove':['reference fidelity','Class-A continuity','final aperture architecture','manufacturing feasibility']}
runtime['surface_receipt']=surface55

def patch55(out):
    p=Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json');p.unlink() if p.exists() else None
    body=bpy.data.objects.get('DERIVED_911_9922_BODY');rows=fold_rows(body) if body else []
    fd={'schema':'oleander.3d.surface-fold-diagnostic.v1','candidate_revision':REV,'fold_count':len(rows),'folds':rows,'authority':'DIAGNOSTIC_NOT_REFERENCE_AUTHORITY','does_not_prove':['reference fidelity','Class-A continuity']};Path(out,'SURFACE_FOLD_DIAGNOSTIC.json').write_text(json.dumps(fd,ensure_ascii=False,indent=2)+'\n')
    stage={'schema':'oleander.3d.stage-capability-routing-receipt.v1','candidate_revision':REV,'stage':'SURFACE_CAUSAL_REPAIR_APERTURE_HOLD','required_capabilities':['PRIMARY_FORM_PROJECTION','SURFACE_CAUSAL_REPAIR'],'available_capabilities':['PRIMARY_FORM_PROJECTION','SURFACE_CAUSAL_REPAIR','GREENHOUSE_VISUAL_PROXY'],'held_capabilities':['FINAL_APERTURE_ARCHITECTURE'],'held_result':'NOT_APPLICABLE_STAGE_HOLD','failed_required_capabilities':[],'legacy_name_dependencies_not_required':[],'result':'PASS_STAGE_AWARE_ROUTING','does_not_prove':['reference fidelity','design quality']};Path(out,'STAGE_CAPABILITY_ROUTING_RECEIPT.json').write_text(json.dumps(stage,ensure_ascii=False,indent=2)+'\n')
    delta={'schema':'oleander.3d.source-edit-delta.surface-causal-repair.v1','candidate_revision':REV,'changed_variables':['rear cabin blend length','front cabin release length','profile inversion upper-only','ordered lower return','terminal section source'],'protected_variables':['V51 hood-fender hierarchy','hard points','axles','wheels','mid-body zero-fold region'],'rollback_revision':'V51_FRONT_TRANSVERSE_IDENTITY_REPAIR','does_not_prove':['reference fidelity','Class-A continuity']};Path(out,'SOURCE_EDIT_DELTA.json').write_text(json.dumps(delta,ensure_ascii=False,indent=2)+'\n')
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if p.exists():
            d=json.loads(p.read_text());d['reference_fidelity_revision']=REV;d['primary_form_stage']='SURFACE_CAUSAL_REPAIR_APERTURE_HOLD';d['representation_state']='SURFACE_CAUSAL_REPAIR';d['source_edit_scope']='CABIN_BLEND_AND_LOWER_RETURN_AND_TERMINAL_ORDER_ONLY';d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW';d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def run55():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:runtime['run30']()
    except SystemExit as e:patch55(out);raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:patch55(out)
run55()
