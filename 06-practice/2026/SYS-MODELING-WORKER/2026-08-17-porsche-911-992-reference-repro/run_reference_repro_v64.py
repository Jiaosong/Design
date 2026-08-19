#!/usr/bin/env python3
"""V64 — sparse rear upper-taper experiment from the V59 no-fold LKG.

This is a parallel primary-form experiment, not a continuation of V60-V63 aperture execution.
It starts from V59 so the screened hood/fender relation is retained, then edits only one new Source relation:

    REAR_UPPER_TAPER_RELATION

Observed V59 evidence: rear body-only width-by-height RMSE ≈ 0.1724 against a 0.11 screening limit;
errors are concentrated through the upper/mid rear where the candidate stays too close to full body width.
The edit narrows only the upper rear transverse rails while preserving lower haunch/rocker, XZ side silhouette,
front relation, hard points, axles, wheels, Source density and rear terminal X/Z.

No cage densification, no profile inversion, no aperture edit, no camera tuning.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE = Path(__file__).resolve().parent
V59 = HERE / 'run_reference_repro_v59.py'
text = V59.read_text(encoding='utf-8')
marker = '\nrun59()\n'
if marker not in text:
    raise SystemExit('V59 run marker missing')
ns = {'__file__': str(V59), '__name__': 'oleander_v64_rear_upper_taper'}
exec(compile(text.split(marker,1)[0], str(V59), 'exec'), ns)

v=ns['v']; core=ns['core']; runtime=ns['runtime']
base_ring=ns['ring59']; base_build=ns['base_build']; apply_subd=ns['apply_subd']
SIDE=ns['SIDE']; PROFILE=ns['PROFILE']; tri_plane_top=ns['tri_plane_top']; evaluated_mesh_data=ns['evaluated_mesh_data']
profile_rmse=ns['profile_rmse']; semantic_front_base=ns['semantic_front59']; components=ns['components']; folds=ns['folds']; edge_p95=ns['edge_p95']; RAILS=ns['RAILS']
REV='V64_SPARSE_REAR_UPPER_TAPER_RELATION'
ns['REV']=REV
v.REF='2025_992.2_CARRERA_SPARSE_REAR_TAPER_V64'
v.REFERENCE_CONTRACT['candidate_revision']=REV
v.REFERENCE_CONTRACT['reference_revision']=v.REF
v.REFERENCE_CONTRACT['representation_state']='V59_LKG_PLUS_ONE_SPARSE_REAR_TRANSVERSE_RELATION'
v.REFERENCE_CONTRACT['source_edit_scope']='REAR_UPPER_TAPER_RELATION_ONLY'
v.REFERENCE_CONTRACT['forbidden_deltas']=['PROFILE_INVERSION','CAGE_DENSIFICATION','APERTURE_EDIT','FRONT_EDIT','LOWER_HAUNCH_EDIT','CAMERA_TUNING']
v.FAMILY_CONTROLS['REAR_UPPER_TAPER_RELATION_V64']={
    'owner':'TIER_A_REAR_PRIMARY_IDENTITY',
    'x_center_m':-1.15,
    'x_falloff_m':0.75,
    'upper_rail_y_scale_reduction':[0.0,0.10,0.18,0.28,0.32,0.22],
    'protected':['V59_FRONT_HOOD_FENDER_RELATION','V49_SOURCE_DENSITY','LOWER_HAUNCH','ROCKER','TERMINAL_XZ','HARD_POINTS','AXLES','WHEELS','SIDE_XZ'],
    'rollback':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
}
v.REFERENCE_CONTRACT['source_families']=list(v.FAMILY_CONTROLS.keys())


def ring64(x):
    full=base_ring(x)
    half=[list(p) for p in full[:11]]
    rw=math.exp(-((float(x)+1.15)/.75)**4)
    reductions=(0.0,.10,.18,.28,.32,.22)
    if rw>.0001:
        for i,red in enumerate(reductions):
            if i==0 or red<=0: continue
            half[i][1] *= (1.0-red*rw)
    return [tuple(p) for p in half] + [(px,-py,pz) for px,py,pz in reversed(half[1:-1])]

core['hull_ring']=ring64
v.body_ring=ring64


def build64(name, bodymat):
    o=base_build(name, bodymat)
    if name=='DERIVED_911_9922_BODY':
        apply_subd(o)
        d=o.copy(); d.data=o.data.copy(); d.name='DIAG_FEATURE_ALIGNED_SURFACED_V64'
        bpy.context.collection.objects.link(d); d.hide_render=True; d.hide_set(True)
        d['OLEANDER_AUTHORITY']='DERIVED_DIAGNOSTIC_NOT_AUTHORITY'
        d['OLEANDER_DIAGNOSTIC_ROLE']='FINAL_EVALUATED_V64_REAR_UPPER_TAPER'
        o['OLEANDER_FORM_FAMILY']='V59_LKG_PLUS_REAR_UPPER_TAPER_RELATION'
        o['OLEANDER_SOURCE_RING_CONTROLS']=len(ring64(0.0))
        o['OLEANDER_SOURCE_EDIT_SCOPE']='REAR_UPPER_TAPER_RELATION_ONLY'
    return o

core['build_visual_hull']=build64


def semantic_front64(tris):
    d=semantic_front_base(tris)
    if isinstance(d,dict):
        d['candidate_geometry_revision']=REV
        d['evaluated_carrier']='DIAG_FEATURE_ALIGNED_SURFACED_V64'
    return d


def projection64():
    diag=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V64')
    tris=evaluated_mesh_data('DIAG_FEATURE_ALIGNED_SURFACED_V64')
    side=[]; errs=[]
    for x,z in SIDE:
        cand=tri_plane_top(diag,x); e=cand-z if math.isfinite(cand) else float('nan')
        side.append({'x':x,'target_top':z,'candidate_top':cand,'top_error_m':e})
        if math.isfinite(e): errs.append(e)
    sr=math.sqrt(sum(e*e for e in errs)/len(errs))
    fr,fs,fc=profile_rmse(tris,PROFILE['front']['profile'],'front')
    rr,rs,rc=profile_rmse(tris,PROFILE['rear']['profile'],'rear')
    metrics=[
        {'id':'SIDE_UPPER_EVALUATED_MESH_RMSE_M','target':0.,'candidate':sr,'abs_error':sr,'limit':.040,'candidate_measurement_source':'V64_FINAL_EVALUATED_XZ'},
        {'id':'FRONT_BODY_ONLY_PROFILE_RMSE','target':0.,'candidate':fr,'abs_error':fr,'limit':.100,'candidate_measurement_source':'V64_BODY_ONLY_YZ','measurement_role':'BODY_ONLY_DIAGNOSTIC_NOT_WHOLE_VISIBLE_FIDELITY'},
        {'id':'REAR_BODY_ONLY_PROFILE_RMSE','target':0.,'candidate':rr,'abs_error':rr,'limit':.110,'candidate_measurement_source':'V64_BODY_ONLY_YZ','measurement_role':'BODY_ONLY_DIAGNOSTIC_NOT_WHOLE_VISIBLE_FIDELITY'}
    ]
    return {
        'schema':'oleander.3d.v64-sparse-rear-taper-projection.v1',
        'candidate_revision':REV,'reference_revision':v.REF,
        'status':'MACHINE_SCREENING_RECORDED_NOT_REFERENCE_PASS',
        'source_edit_scope':'REAR_UPPER_TAPER_RELATION_ONLY',
        'metrics':metrics,'front_identity_metrics':semantic_front64(tris),
        'side_upper_samples':side,'front_profile_samples':fs,'rear_profile_samples':rs,
        'fit_views':['REAR_BODY_ONLY'],
        'regression_views':['SIDE','FRONT_BODY_ONLY'],
        'held_out_views':['HERO_REAR_3Q','TOP_FRONT_3Q','HERO_FRONT_3Q'],
        'reference_fidelity_review':'HOLD','design_quality_gate':'HOLD',
        'does_not_prove':['whole-visible reference fidelity','final aperture architecture','Class-A continuity','manufacturing feasibility']
    }

runtime['projection30']=projection64


def regression64(pr):
    m={x['id']:x for x in pr['metrics']}
    rear=float(m['REAR_BODY_ONLY_PROFILE_RMSE']['candidate'])
    side=float(m['SIDE_UPPER_EVALUATED_MESH_RMSE_M']['candidate'])
    front=float(m['FRONT_BODY_ONLY_PROFILE_RMSE']['candidate'])
    rear_base=0.17242950469411836
    target_improved=math.isfinite(rear) and rear <= rear_base-.010
    locks=[
        {'id':'SIDE_UPPER','baseline':0.013857890932342255,'candidate':side,'allowed_max':0.019857890932342255,'status':'PASS' if side<=0.019857890932342255 else 'REGRESSED'},
        {'id':'FRONT_BODY_ONLY','baseline':0.15027779710716418,'candidate':front,'allowed_max':0.16027779710716418,'status':'PASS' if front<=0.16027779710716418 else 'REGRESSED'},
        {'id':'SOURCE_RING_CONTROL_COUNT','baseline':20,'candidate':len(ring64(0.0)),'allowed_max':20,'status':'PASS' if len(ring64(0.0))==20 else 'REGRESSED'}
    ]
    locks_pass=all(x['status']=='PASS' for x in locks)
    return {
        'schema':'oleander.3d.reference-regression-promotion-receipt.v2',
        'baseline_revision':'V59_SPARSE_FRONT_HOOD_FENDER_RELATION','candidate_revision':REV,
        'edit_scope':['REAR_UPPER_TAPER_RELATION_ONLY'],
        'target_metric_delta':{'metric_id':'REAR_BODY_ONLY_PROFILE_RMSE','baseline':rear_base,'candidate':rear,'direction':'LOWER_IS_BETTER','minimum_improvement_required':.010,'improved':target_improved},
        'regression_locks':locks,
        'measurement_comparability':'COMPARABLE_BODY_ONLY_PROFILE_AND_SIDE_XZ',
        'promotion_decision':'KEEP_LKG_HOLD_EXPERIMENT' if target_improved and locks_pass else 'KEEP_V59_LKG_REJECT_EXPERIMENT',
        'visual_review_state':'NOT_RUN',
        'does_not_prove':['reference fidelity','design quality','Class-A continuity']
    }

runtime['regression30']=regression64


def emit_surface_v64(out):
    ev=bpy.data.objects.get('DIAG_FEATURE_ALIGNED_SURFACED_V64')
    if ev is None:
        raise SystemExit('FAIL_V64_EVALUATED_CARRIER_MISSING')
    me=ev.data; me.calc_loop_triangles(); p95=edge_p95(ev); fc=folds(ev); cc=components(ev)
    sampling='PASS' if p95<=.30 else 'HOLD'
    machine='MACHINE_CONSTRUCTED_VISUAL_HOLD' if cc==1 and fc==0 and sampling=='PASS' else ('MACHINE_SURFACE_TOPOLOGY_FAIL' if cc!=1 or fc!=0 else 'MACHINE_SURFACE_SAMPLING_HOLD')
    d={
        'schema':'oleander.3d.primary-body-surface-receipt.v2','revision':REV,
        'surface_measurement_scope':'CLOSED_PRIMARY_VISUAL_HULL_BEFORE_FINAL_APERTURE_ARCHITECTURE',
        'source_state_class':'SOURCE_CONTROL_CAGE','source_semantic_rail_count':len(RAILS),
        'source_ring_control_count':len(ring64(0.0)),
        'source_density_role':'INFORMATIONAL_CAUSAL_CONTROL_COMPLEXITY_NOT_EVALUATED_QUALITY_GATE',
        'evaluated_carrier':'DIAG_FEATURE_ALIGNED_SURFACED_V64','evaluated_state_class':'DERIVED_DIAGNOSTIC_NOT_AUTHORITY',
        'evaluated_vertices':len(me.vertices),'evaluated_edges':len(me.edges),'evaluated_faces':len(me.polygons),'evaluated_triangles':len(me.loop_triangles),
        'evaluated_connected_components':cc,'evaluated_adjacent_face_normal_flip_count':fc,'evaluated_edge_p95_m':p95,
        'evaluated_sampling_gate':{'basis':'EVALUATED_EDGE_P95_AT_CURRENT_REVIEW_SCALE','status':sampling,'threshold_or_rule':'evaluated_edge_p95_m <= 0.30','observed':p95,'review_scope':'992.2 primary-form review; not universal production tolerance'},
        'machine_surface_state':machine,'visual_review_state':'NOT_RUN',
        'does_not_prove':['reference fidelity','Class-A continuity','final aperture architecture','Design KEEP']
    }
    Path(out,'PRIMARY_BODY_SURFACE_RECEIPT_V2.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    Path(out,'PRIMARY_BODY_SURFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')


def run64():
    a=v.m.parse_args(); out=Path(a.out).resolve()
    try:
        runtime['run30']()
    except SystemExit as e:
        emit_surface_v64(out)
        raise SystemExit(e.code if isinstance(e.code,int) else 0)
    else:
        emit_surface_v64(out)

run64()
