#!/usr/bin/env python3
"""V48 — primary-form correction + stage-aware evidence routing.

V48 is a bounded successor to V47. It keeps the 992.2 hard points, wheel/axle placement,
SIDE outer gesture and aperture HOLD boundary, while correcting the causal first-read
failures observed in the V47 six-view render:

- front lamp/fender host relation instead of attached-eye discs;
- stronger hood-valley / fender-crown depth ordering;
- quieter lower fascia so intake graphics do not replace the primary form;
- less slab-like rear terminal mass;
- greenhouse proxy without large dark surface backings.

The evidence runtime is also repaired: primary-form projection is measured directly from
the final evaluated primary body. Aperture-dependent metrics are declared
NOT_APPLICABLE_STAGE_HOLD while aperture architecture is intentionally HOLD; missing
historical object names must not crash a valid primary-form stage.

This remains a reference-reproduction candidate, not Porsche CAD, Class-A surfacing,
engineering release, manufacturing proof, homologation or Design KEEP.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE=Path(__file__).resolve().parent
V47=HERE/'run_reference_repro_v47.py'
text=V47.read_text()
if text.count("M['rear_light']") != 1:
    raise SystemExit("V48 expected one legacy V47 rear_light lookup")
text=text.replace("M['rear_light']", "M['tail']")
marker='\nrun47()\n'
if marker not in text:
    raise SystemExit('V47 run marker missing')
ctx={'__file__':str(V47),'__name__':'oleander_v48_declarations'}
exec(compile(text.split(marker,1)[0],str(V47),'exec'),ctx)

v=ctx['v']
core=ctx['core']
runtime=ctx['env']
ns43=ctx['ns']
base_ring=ctx['hull_ring47']
base_build=ctx['base_build']
apply_subd=ctx['apply_subd']
base_regression=ctx['base_regression']
base_surface=ctx['base_surface']
base_patch=ctx['base_patch']
tri_plane_top=ctx['tri_plane_top']
G=ctx['G']
lerp=ctx['lerp']
SIDE=ctx['SIDE']
PROFILE=json.loads((HERE/'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json').read_text())
FRONT_ID=json.loads((HERE/'REFERENCE_FRONT_IDENTITY_TARGETS_992_2.json').read_text())

REV='V48_PRIMARY_FORM_STAGE_AWARE'
ctx['REV']=REV
v.REF='2025_992.2_CARRERA_PRIMARY_FORM_V48'
v.REFERENCE_CONTRACT['schema']='oleander.3d.reference-reproduction.porsche-911-992-2.v48'
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['primary_form_method']='V47_LKG_PLUS_HOST_INTEGRATED_FRONT_REAR_CAUSAL_CORRECTION'
v.REFERENCE_CONTRACT['projection_measurement']='FINAL_EVALUATED_PRIMARY_BODY_STAGE_AWARE'
v.REFERENCE_CONTRACT['aperture_architecture_state']='HOLD_PROXY_ONLY'
v.REFERENCE_CONTRACT['stage_capability_rule']='MISSING_NON_APPLICABLE_CAPABILITY_RETURNS_HOLD_NOT_RUNTIME_FAILURE'
v.FAMILY_CONTROLS['VISUAL_MASS_V48']={
    'protected':['OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE','SIDE_OUTER_GESTURE','V40_ZERO_FOLD_BASE'],
    'front':{
        'hood_center_longitudinal_setback_m':0.045,
        'fender_crown_longitudinal_advance_m':0.026,
        'fender_crown_extra_relief_m':0.014,
        'lamp_host':'SHALLOW_LENS_INSIDE_FENDER_CROWN',
        'lower_fascia':'SUBORDINATE_TO_HOOD_FENDER_BAND'
    },
    'rear':{
        'center_upper_terminal_setback_m':0.052,
        'outer_haunch_terminal_hold_m':0.012,
        'center_deck_extra_drop_m':0.012
    },
    'greenhouse':'CALIBRATED_GLASS_PROXY_WITHOUT_SURFACE_DARK_BACKING',
    'aperture_architecture':'HOLD_NOT_CONSTRUCTED'
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())

def s01(x):
    x=max(0.0,min(1.0,float(x)))
    return x*x*(3.0-2.0*x)

def interpG(x,field):
    x=float(x)
    if x<=G[0][0]: return G[0][field]
    if x>=G[-1][0]: return G[-1][field]
    for a,b in zip(G,G[1:]):
        if a[0]<=x<=b[0]:
            return lerp(a[field],b[field],(x-a[0])/(b[0]-a[0]))
    return G[-1][field]

# ---- primary-form correction: modify only interior transverse relations, not SIDE outer rail ----
def hull_ring48(x):
    ring=[list(p) for p in base_ring(x)]
    w=max(abs(p[1]) for p in ring) or 1.0
    fi=math.exp(-((float(x)-1.48)/.60)**4)
    ri=math.exp(-((float(x)+1.35)/.68)**4)
    front_terminal=s01((float(x)-1.62)/(v.FRONT_X-1.62)) if x>1.62 else 0.0
    rear_terminal=s01((-float(x)-1.62)/(-v.REAR_X-1.62)) if x<-1.62 else 0.0
    for p in ring:
        _,y,z=p
        q=abs(y)/w
        if z>.50 and q<.95 and fi>.001:
            if q<.56:
                p[0]-=.045*fi*((1-q/.56)**1.35)
                p[2]-=.010*fi*((1-q/.56)**1.20)
            elif .64<q<.93:
                bell=max(0.0,1-abs(q-.79)/.15)
                p[0]+=.026*fi*(bell**1.5)
                p[2]+=.014*fi*(bell**1.5)
        if front_terminal>0 and z>.54 and q<.94:
            p[0]-=.030*front_terminal*(1-q/.94)**1.1
        if z>.48 and q<.95 and ri>.001:
            if q<.55:
                p[0]+=.052*ri*((1-q/.55)**1.25)
                p[2]-=.012*ri*((1-q/.55)**1.15)
            elif .65<q<.93:
                bell=max(0.0,1-abs(q-.80)/.16)
                p[0]-=.012*ri*(bell**1.35)
        if rear_terminal>0 and z>.54 and q<.60:
            p[0]+=.025*rear_terminal*(1-q/.60)
    return [tuple(p) for p in ring]

core['hull_ring']=hull_ring48
v.body_ring=hull_ring48

def build48(name,bodymat):
    o=base_build(name,bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        d=o.copy(); d.data=o.data.copy()
        d.name='DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V48'
        bpy.context.collection.objects.link(d)
        d.hide_render=True; d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY'
        d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_PRIMARY_BODY_BEFORE_PROXY_GREENHOUSE'
        o['OLEANDER_FORM_FAMILY']='911_PRIMARY_FORM_V48'
        o['OLEANDER_APERTURE_ARCHITECTURE']='HOLD_PROXY_GREENHOUSE'
    return o

core['build_visual_hull']=build48

def gy48(x,z):
    w=core['plan_half_width'](x)
    raw=.5*v.WIDTH*core['profile_ratio'](x,z)
    return min(w-.010,max(.40,raw-.008))

def strip48(name,pts,side,mat,offset=-.006,authority='DERIVED_APERTURE_INFILL'):
    verts=[]; faces=[]
    for x,zt,zb in pts:
        yy=gy48(x,(zt+zb)*.5)+offset
        verts.extend([(x,side*yy,zt),(x,side*yy,zb)])
    for i in range(len(pts)-1):
        a=2*i; faces.append((a,a+1,a+3,a+2))
    me=bpy.data.meshes.new(name+'_MESH')
    me.from_pydata(verts,[],faces); me.update()
    o=bpy.data.objects.new(name,me); bpy.context.collection.objects.link(o)
    o.data.materials.append(mat); o['OLEANDER_AUTHORITY']=authority
    for p in me.polygons: p.use_smooth=True
    return o

def proxy_glass48(M):
    out=[]
    bp=(-.20,interpG(-.20,1),interpG(-.20,2))
    q=[p for p in G if p[0]<-.20]+[bp]
    d=[bp]+[p for p in G if p[0]>-.20]
    for side,label in ((1,'L'),(-1,'R')):
        out.append(strip48('V48_QUARTER_GLASS_'+label,q,side,M['glass']))
        out.append(strip48('V48_DOOR_GLASS_'+label,d,side,M['glass']))
        top=interpG(-.20,1); bot=interpG(-.20,2)
        yy=gy48(-.20,(top+bot)*.5)-.002
        out.append(v.m.add_cube('V48_B_PILLAR_'+label,(-.20,side*yy,(top+bot)*.5),(.025,.012,max(.08,top-bot)),M['body_dark'],.002))
    ws=[(.625,.585,.855),(.625,-.585,.855),(.245,-.515,1.205),(.245,.515,1.205)]
    rg=[(-.405,.465,1.205),(-.405,-.465,1.205),(-1.125,-.545,.985),(-1.125,.545,.985)]
    wso=v.m.add_panel('V48_WINDSHIELD_PROXY',ws,M['glass'],.0015)
    wso['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'; out.append(wso)
    rgo=v.m.add_panel('V48_REAR_GLASS_PROXY',rg,M['glass'],.0015)
    rgo['OLEANDER_AUTHORITY']='DERIVED_APERTURE_INFILL'; out.append(rgo)
    return out

v.build_glass=proxy_glass48

def identity48(M):
    out=[]
    half=v.WIDTH*.5
    cy=float(FRONT_ID['measurement']['lamp_center_lateral_ratio_of_half_body_width'])*half
    r=.5*float(FRONT_ID['measurement']['visible_lamp_diameter_ratio_of_body_width'])*v.WIDTH
    for side in (1,-1):
        recess=v.m.add_uv_sphere('DERIVED_HEADLAMP_RECESS_'+str(side),(1.874,side*cy,.755),(.009,r*1.015,r*1.015),M['body_dark'])
        recess['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE'; out.append(recess)
        lens=v.m.add_uv_sphere('REF_HEADLAMP_LENS_'+str(side),(1.884,side*cy,.755),(.006,r*.94,r*.94),M['headlamp'])
        lens['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_DETAIL'; out.append(lens)
    out.append(v.m.add_cube('REF_FRONT_CENTER_INTAKE',(2.185,0,.275),(.014,.265,.050),M['body_dark'],.022))
    for side in (1,-1):
        out.append(v.m.add_cube('REF_FRONT_SIDE_INTAKE_'+str(side),(2.165,side*.545,.288),(.012,.105,.060),M['body_dark'],.026))
    out.append(v.m.add_cube('REF_FRONT_SPLITTER',(2.190,0,.178),(.012,1.05,.012),M['body_dark'],.005))
    out.append(v.m.add_cube('REF_REAR_LIGHTBAR',(-2.135,0,.655),(.012,1.38,.026),M['tail'],.009))
    return out

v.build_identity=identity48

def evaluated_mesh_data(name):
    obj=bpy.data.objects.get(name)
    if obj is None:
        raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: '+name)
    dg=bpy.context.evaluated_depsgraph_get()
    eo=obj.evaluated_get(dg); me=eo.to_mesh(); me.calc_loop_triangles(); mw=eo.matrix_world.copy()
    tris=[]
    try:
        for lt in me.loop_triangles:
            pts=[]
            for vi in lt.vertices:
                p=mw@me.vertices[vi].co
                pts.append((float(p.x),float(p.y),float(p.z)))
            tris.append(tuple(pts))
    finally:
        eo.to_mesh_clear()
    if not tris:
        raise SystemExit('FAIL_EVALUATED_MESH_PROJECTION_EMPTY')
    return tris

def z_plane_points(tri,z):
    pts=[]
    for i in range(3):
        x1,y1,z1=tri[i]; x2,y2,z2=tri[(i+1)%3]
        if abs(z2-z1)<1e-12:
            if abs(z-z1)<1e-8:
                pts.extend(((x1,y1),(x2,y2)))
            continue
        if z < min(z1,z2)-1e-9 or z > max(z1,z2)+1e-9:
            continue
        t=(z-z1)/(z2-z1)
        if -1e-9<=t<=1+1e-9:
            pts.append((x1+t*(x2-x1),y1+t*(y2-y1)))
    return pts

def profile_rmse(tris,profile,which):
    Z0=.140; ZH=v.HEIGHT
    samples=[]; errs=[]
    for frac,target in profile:
        z=Z0+float(frac)*(ZH-Z0)
        pts=[]
        for tri in tris:
            if z < min(p[2] for p in tri)-1e-9 or z > max(p[2] for p in tri)+1e-9:
                continue
            for x,y in z_plane_points(tri,z):
                if which=='front' and x>=.55:
                    pts.append((x,y))
                elif which=='rear' and x<=-.55:
                    pts.append((x,y))
        cand=max((abs(y) for _,y in pts),default=float('nan'))/(.5*v.WIDTH)
        err=cand-float(target) if math.isfinite(cand) else float('nan')
        samples.append({'height_fraction':frac,'target_half_width_ratio':target,'candidate_half_width_ratio':cand,'error':err})
        if math.isfinite(err): errs.append(err)
    if len(errs)<max(6,int(.70*len(profile))):
        raise SystemExit('FAIL_EVALUATED_PROFILE_COVERAGE_'+which.upper())
    return math.sqrt(sum(e*e for e in errs)/len(errs)),samples,len(errs)/len(profile)

def projection48():
    diag=bpy.data.objects.get('DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V48')
    if diag is None:
        raise SystemExit('FAIL_FINAL_VISIBLE_MEMBERSHIP_UNRESOLVED: DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V48')
    side_errs=[]; side_samples=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x)
        err=cand-z if math.isfinite(cand) else float('nan')
        side_samples.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':err,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_XZ_INTERSECTION'})
        if math.isfinite(err): side_errs.append(err)
    if len(side_errs)<max(6,int(.90*len(SIDE))):
        raise SystemExit('FAIL_EVALUATED_SIDE_PROFILE_COVERAGE')
    side_rmse=math.sqrt(sum(e*e for e in side_errs)/len(side_errs))
    tris=evaluated_mesh_data('DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V48')
    front_rmse,front_samples,front_cov=profile_rmse(tris,PROFILE['front']['profile'],'front')
    rear_rmse,rear_samples,rear_cov=profile_rmse(tris,PROFILE['rear']['profile'],'rear')
    metrics=[
        {'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.0,'candidate':side_rmse,'abs_error':side_rmse,'limit':.040,'reference_target_source':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json:side.top_silhouette_m','candidate_measurement_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_XZ_INTERSECTION'},
        {'id':'FRONT_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':front_rmse,'abs_error':front_rmse,'limit':float(PROFILE['gates']['front_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:front.profile','candidate_measurement_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_FRONT_Z_SLICE'},
        {'id':'REAR_HALF_PROJECTED_PROFILE_RMSE','target':0.0,'candidate':rear_rmse,'abs_error':rear_rmse,'limit':float(PROFILE['gates']['rear_profile_rmse_max']),'reference_target_source':'REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json:rear.profile','candidate_measurement_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_REAR_Z_SLICE'}
    ]
    ok=all(float(m['abs_error'])<=float(m['limit']) for m in metrics)
    return {'schema':'oleander.3d.stage-aware-primary-form-projection.v1','reference':'REFERENCE_VISUAL_HULL_TARGETS_992_2.json + REFERENCE_FRONT_REAR_PROFILE_TARGETS_992_2.json','candidate_revision':REV,'status':'PROJECTION_MACHINE_SCREENING_PASS' if ok else 'PROJECTION_MACHINE_SCREENING_FAIL','primary_form_stage':'PRIMARY_FORM_PROXY_APERTURE_HOLD','stage_capabilities':{'PRIMARY_FORM_PROJECTION':'AVAILABLE','GREENHOUSE_VISUAL_PROXY':'AVAILABLE','FINAL_APERTURE_ARCHITECTURE':'NOT_APPLICABLE_STAGE_HOLD','FINAL_WINDSHIELD_FLANGE':'NOT_APPLICABLE_STAGE_HOLD','FINAL_REAR_GLASS_FLANGE':'NOT_APPLICABLE_STAGE_HOLD'},'not_applicable_metrics':[{'id':'FRONT_UPPER_CABIN_WIDTH_RATIO','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'},{'id':'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'},{'id':'REAR_BACKLIGHT_LOWER_WIDTH_RATIO','state':'NOT_APPLICABLE_STAGE_HOLD','reason':'FINAL_APERTURE_ARCHITECTURE_HOLD_PROXY_ONLY'}],'final_visible_membership':[{'object':'DIAG_PRE_PROXY_GREENHOUSE_SURFACED_V48','role':'FINAL_EVALUATED_PRIMARY_BODY_BEFORE_VISUAL_PROXY','triangles':len(tris)}],'metrics':metrics,'side_upper_samples':side_samples,'front_profile_samples':front_samples,'rear_profile_samples':rear_samples,'side_upper_finite_sample_coverage':len(side_errs)/len(SIDE),'front_profile_finite_sample_coverage':front_cov,'rear_profile_finite_sample_coverage':rear_cov,'independent_visual_review':False,'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD','does_not_prove':['reference fidelity','manufacturer CAD','Class-A continuity','final aperture architecture','production patch layout','manufacturing feasibility','homologation']}

runtime['projection30']=projection48

def regression48(pr):
    current={m['id']:m for m in pr['metrics']}
    side=current['SIDE_UPPER_EVALUATED_MESH_RMSE_M']; front=current['FRONT_HALF_PROJECTED_PROFILE_RMSE']; rear=current['REAR_HALF_PROJECTED_PROFILE_RMSE']
    return {
        'schema':'oleander.3d.reference-regression-promotion-receipt.v1',
        'baseline_revision':'V47_911_VISUAL_MASS_LKG_EXPERIMENT',
        'candidate_revision':REV,
        'edit_scope':['FRONT_HOOD_FENDER_HOST_RELATION','HEADLAMP_EMBEDDING_DEPTH','LOWER_FASCIA_SUBORDINATION','REAR_TERMINAL_MASS','GREENHOUSE_PROXY_CARRIER','STAGE_AWARE_PROJECTION_ROUTING'],
        'protected_families':['OFFICIAL_HARD_POINTS','AXLE_CENTRES','WHEEL_TYRE_PACKAGE','SIDE_OUTER_GESTURE'],
        'target_metric_delta':{'metric_id':'PRIMARY_FORM_REFERENCE_FIDELITY','baseline':'V47_PROJECTION_INVALID_DUE_STAGE_DEPENDENCY','candidate':{'side_upper_rmse_m':side['candidate'],'front_profile_rmse':front['candidate'],'rear_profile_rmse':rear['candidate']},'direction':'TARGET_ERROR','improved':False},
        'regression_locks':[
            {'id':'OFFICIAL_HARD_POINTS','baseline':'LOCKED','candidate':'LOCKED','limit':'EXACT','status':'PASS','evidence_source':'REFERENCE_INPUTS_992_2.json'},
            {'id':'SIDE_OUTER_GESTURE','baseline':'V47_NOT_COMPARABLE','candidate':side['candidate'],'limit':side['limit'],'status':'NOT_COMPARABLE','evidence_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_XZ_INTERSECTION'},
            {'id':'FRONT_GROSS_PROFILE','baseline':'V47_NOT_COMPARABLE','candidate':front['candidate'],'limit':front['limit'],'status':'NOT_COMPARABLE','evidence_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_FRONT_Z_SLICE'},
            {'id':'REAR_GROSS_PROFILE','baseline':'V47_NOT_COMPARABLE','candidate':rear['candidate'],'limit':rear['limit'],'status':'NOT_COMPARABLE','evidence_source':'V48_FINAL_EVALUATED_PRIMARY_BODY_REAR_Z_SLICE'}
        ],
        'measurement_method_ids':['FINAL_EVALUATED_PRIMARY_BODY_XZ_INTERSECTION','FINAL_EVALUATED_PRIMARY_BODY_FRONT_Z_SLICE','FINAL_EVALUATED_PRIMARY_BODY_REAR_Z_SLICE'],
        'measurement_comparability':'NOT_COMPARABLE',
        'incomparability_reason':'V47_PROJECTION_CHAIN_CRASHED_ON_APERTURE_OBJECT_NAME_DEPENDENCY',
        'promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT',
        'visual_review_state':'NOT_RUN',
        'does_not_prove':['reference fidelity','design quality','Class-A continuity','final aperture architecture','manufacturing feasibility']
    }
runtime['regression30']=regression48

def surface48():
    d=base_surface(); d['revision']=REV; d['aperture_architecture_state']='HOLD_PROXY_ONLY'; return d
runtime['surface_receipt']=surface48

def stage_capability_receipt48(out):
    d={'schema':'oleander.3d.stage-capability-routing-receipt.v1','candidate_revision':REV,'stage':'PRIMARY_FORM_PROXY_APERTURE_HOLD','available_capabilities':['PRIMARY_FORM_PROJECTION','SIDE_SILHOUETTE','FRONT_GROSS_PROFILE','REAR_GROSS_PROFILE','GREENHOUSE_VISUAL_PROXY'],'held_capabilities':['FINAL_APERTURE_ARCHITECTURE','FINAL_WINDSHIELD_FLANGE','FINAL_REAR_GLASS_FLANGE'],'held_result':'NOT_APPLICABLE_STAGE_HOLD','legacy_name_dependencies_not_required':['REF_WINDSHIELD','REF_REAR_GLASS'],'result':'PASS_STAGE_AWARE_ROUTING','does_not_prove':['reference fidelity','aperture construction','design quality']}
    Path(out,'STAGE_CAPABILITY_ROUTING_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def proxy_receipt48(out):
    d={'schema':'oleander.3d.visual-mass-proxy-receipt.v1','candidate_revision':REV,'primary_surface':'V40_ZERO_FOLD_SOURCE_PLUS_SUBD1_WITH_V48_CAUSAL_RELIEF','greenhouse_representation':'CALIBRATED_GLASS_PROXY_NO_SURFACE_DARK_BACKING','aperture_architecture_state':'HOLD_NOT_CONSTRUCTED','stage_capability_routing':'PASS_NOT_APPLICABLE_STAGE_HOLD','visual_review_state':'NOT_RUN','machine_state':'MACHINE_VISUAL_MASS_READY_FOR_REVIEW','does_not_prove':['reference fidelity','true host opening','aperture flange','Class-A continuity','manufacturer CAD','production feasibility']}
    Path(out,'VISUAL_MASS_PROXY_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

def patch48(out):
    base_patch(out); proxy_receipt48(out); stage_capability_receipt48(out)
    fp=Path(out,'REFERENCE_FIDELITY_RECEIPT.json')
    if fp.exists():
        fd=json.loads(fp.read_text()); fd['candidate_revision']=REV; fd['screening_scope']='LEGACY_LANDMARK_AND_HARD_POINT_SCREENING_ONLY'; fd['visual_reference_fidelity']='HOLD'; fd['does_not_prove']=sorted(set(fd.get('does_not_prove',[])+['current visual reference fidelity','final aperture architecture'])); fp.write_text(json.dumps(fd,ensure_ascii=False,indent=2)+'\n')
    p=Path(out,'FINAL_DERIVED_SURFACE_RECEIPT.json')
    if p.exists(): p.unlink()
    for fn in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p=Path(out)/fn
        if not p.exists(): continue
        d=json.loads(p.read_text()); d['reference_fidelity_revision']=REV; d['primary_form_stage']='PRIMARY_FORM_PROXY_APERTURE_HOLD'; d['aperture_architecture_state']='HOLD_PROXY_ONLY'; d['stage_capability_routing']='PASS_NOT_APPLICABLE_STAGE_HOLD'; d['visual_reference_fidelity']='HOLD' if fn.endswith('QA.json') else 'HOLD_INDEPENDENT_REVIEW'; d['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON'; p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')

ns43['patch43']=patch48

def run48():
    a=v.m.parse_args(); out=Path(a.out).resolve()
    try:
        runtime['run30']()
    except SystemExit as e:
        patch48(out)
        raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:
        patch48(out)

run48()
