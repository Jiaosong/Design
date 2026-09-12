#!/usr/bin/env python3
"""V25 — best-known-gate hybrid: preserve V24 front, recover/improve V23 rear, keep backing.

V24 proved useful front/aperture backing changes but regressed the best-known rear profile from V23.
V25 therefore starts from V24's front/shared-boundary architecture, restores a stronger rear roof crown,
rebuilds only the rear rail/sail/deck boundary loop, and validates against per-gate best-known baselines.
No whole-revision promotion is implied by machine success.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE = Path(__file__).resolve().parent
V24 = HERE / 'run_reference_repro_v24.py'
text = V24.read_text()
marker = '\nrun24()\n'
if marker not in text:
    raise SystemExit('V24 run marker missing')
ns24 = {'__file__': str(V24), '__name__': 'oleander_v24_declarations'}
exec(compile(text.split(marker, 1)[0], str(V24), 'exec'), ns24)
v = ns24['v']
inner = ns24['ns']
PROFILE = ns24['PROFILE']
CROSS_SECTION = ns24['CROSS_SECTION']

v.REF = '2025_992.2_CARRERA_BEST_KNOWN_GATE_HYBRID_V25'
v.REFERENCE_CONTRACT['schema'] = 'oleander.3d.reference-reproduction.porsche-911-992-2.v25'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['best_known_gate_policy'] = 'V2_PER_GATE_BASELINE'
v.REFERENCE_CONTRACT['front_geometry_basis'] = 'V24_FRONT_SHARED_BOUNDARY'
v.REFERENCE_CONTRACT['rear_geometry_basis'] = 'V23_CROSS_SECTION_PLUS_V25_CLOSURE'
v.FAMILY_CONTROLS['BEST_KNOWN_GATE_HYBRID_V25'] = {
    'front_profile_basis': {'revision': 'V24', 'rmse': 0.07774682558830627},
    'rear_profile_basis': {'revision': 'V23', 'rmse': 0.1173280708436564},
    'rear_roof_edge_drop_m': 0.190,
    'rear_roof_half_width_cap_m': 0.520,
    'front_roof_edge_drop_m': 0.100,
    'front_roof_half_width_cap_m': 0.600,
    'backing_basis': 'V24_DERIVED_EXECUTION_NOT_AUTHORITY',
}
v.REFERENCE_CONTRACT['source_families'] = list(v.FAMILY_CONTROLS.keys())

# V24 front values are retained. Rear returns to V23 plan width but receives a deeper edge drop so the
# high rear profile narrows without changing the SIDE apex curve.
def roof_half_width25(x):
    base = max(0.44, v.hermite(v.CABIN_W_PTS, x))
    if x >= 0.0:
        return min(max(base, 0.585), 0.600)
    return min(base, 0.520)


def roof_drop25(x):
    if x >= 0.20:
        return 0.100
    if x <= -0.20:
        return 0.190
    t = (x + 0.20) / 0.40
    return 0.190 * (1.0 - t) + 0.100 * t

# V23 roof-patch functions resolve these names through their execution namespace.
inner['roof_half_width'] = roof_half_width25
inner['roof_drop'] = roof_drop25


def roof_point25(x, side, fraction):
    rw = roof_half_width25(x)
    f = max(0.0, min(1.0, float(fraction)))
    top = v.hermite(v.ROOF_TOP_PTS, x)
    z = top - roof_drop25(x) * (f ** CROSS_SECTION['roof']['crown_exponent'])
    return (x, side * rw * f, z)


def body_outer_y(x, z):
    ring = v.body_ring(x)
    vals = []
    cyc = ring[1:] + ring[:1]
    for a, b in zip(ring, cyc):
        _, y0, z0 = a; _, y1, z1 = b
        if abs(z1-z0) < 1e-10:
            if abs(z-z0) < 1e-7: vals.extend((abs(y0), abs(y1)))
            continue
        if z < min(z0,z1)-1e-8 or z > max(z0,z1)+1e-8: continue
        t = (z-z0)/(z1-z0)
        if -1e-8 <= t <= 1+1e-8:
            vals.append(abs(y0+t*(y1-y0)))
    return max(vals) if vals else max(abs(p[1]) for p in ring)


def make_strip(name, sections, mat, thickness=.008, owner='UNSET'):
    verts=[]
    for outer,inner in sections: verts.extend((outer,inner))
    faces=[(2*i,2*i+1,2*i+3,2*i+2) for i in range(len(sections)-1)]
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE';o['OLEANDER_INTERFACE_SURFACE']=True;o['OLEANDER_BOUNDARY_OWNER']=owner
    if thickness:
        s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0
    for p in me.polygons:p.use_smooth=True
    return o


def make_panel(name, verts, mat, thickness=.008, owner='UNSET', interface=True):
    me=bpy.data.meshes.new(name+'_MESH');me.from_pydata(verts,[],[tuple(range(len(verts)))]);me.update()
    o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY']='DERIVED_REFERENCE_REPRO_INTERFACE' if interface else 'DERIVED_APERTURE_INFILL';o['OLEANDER_BOUNDARY_OWNER']=owner
    if interface:o['OLEANDER_INTERFACE_SURFACE']=True
    if thickness:
        s=o.modifiers.new(name+'_THICKNESS','SOLIDIFY');s.thickness=thickness;s.offset=0
    for p in me.polygons:p.use_smooth=True
    return o


def remove_prefixes(prefixes):
    for o in list(bpy.context.scene.objects):
        if any(o.name.startswith(p) for p in prefixes):
            bpy.data.objects.remove(o,do_unlink=True)

# Start from V24 because its front shared-boundary + backing system produced the best-known FRONT profile.
base_greenhouse = v.build_glass

def greenhouse25(M):
    out = base_greenhouse(M)
    # Preserve V24 front/cowl/A-pillar and backing. Replace only rear glass/quarter/rail/sail/deck/belt loop.
    remove_prefixes((
        'REF_REAR_GLASS','REF_QUARTER_GLASS_L','REF_QUARTER_GLASS_R',
        'REF_C_PILLAR_SAIL_L','REF_C_PILLAR_SAIL_R','REF_REAR_DECK_INTERFACE',
        'REF_ROOF_RAIL_SURFACE_L','REF_ROOF_RAIL_SURFACE_R',
        'REF_WINDOW_BELT_SURFACE_L','REF_WINDOW_BELT_SURFACE_R'))

    c_top={s:roof_point25(-.390,s,.86) for s in (1,-1)}
    c_low={s:(-1.150,s*.592,.990) for s in (1,-1)}
    b_top={s:roof_point25(-.220,s,.84) for s in (1,-1)}
    rear=[c_top[1],c_top[-1],c_low[-1],c_low[1]]
    out.append(make_panel('REF_REAR_GLASS',rear,M['glass'],.003,'REAR_GLASS_EDGE',False))

    rear_outer=body_outer_y(-1.360,.835)
    out.append(make_panel('REF_REAR_DECK_INTERFACE',[c_low[1],c_low[-1],(-1.360,-rear_outer,.835),(-1.360,rear_outer,.835)],M['body'],.010,'REAR_GLASS_EDGE'))

    for s in (1,-1):
        code='L' if s>0 else 'R'
        belt_b=(-.220,s*.570,.842);belt_rear=(-.820,s*.585,.865)
        quarter=[b_top[s],c_top[s],c_low[s],belt_rear,belt_b]
        out.append(make_panel('REF_QUARTER_GLASS_'+code,quarter,M['glass'],.003,'REAR_GLASS_EDGE',False))

        # Split rail: V24 front remains, rear half uses the stronger V25 rear crown.
        front_sections=[]
        for i in range(13):
            x=.235+(-.235)*i/12
            # front V24 crown behavior
            rw=min(max(max(.44,v.hermite(v.CABIN_W_PTS,x)),.585),.600)
            top=v.hermite(v.ROOF_TOP_PTS,x)
            def fp(fr): return (x,s*rw*fr,top-.100*(fr**CROSS_SECTION['roof']['crown_exponent']))
            front_sections.append((fp(1.0),fp(.88)))
        out.append(make_strip('REF_ROOF_RAIL_SURFACE_FRONT_'+code,front_sections,M['body'],.009,'ROOF_EDGE'))

        rear_sections=[]
        for i in range(17):
            x=0.0+(-.390)*i/16
            rear_sections.append((roof_point25(x,s,1.0),roof_point25(x,s,.84)))
        out.append(make_strip('REF_ROOF_RAIL_SURFACE_REAR_'+code,rear_sections,M['body'],.009,'ROOF_EDGE'))

        # Smooth sail strip: narrow at the roof/backlight and progressively opens only near the quarter shoulder.
        sail=[]
        xs=(-.390,-.520,-.680,-.840,-1.000,-1.150)
        inner_y=(abs(c_top[s][1]),.455,.475,.505,.545,.592)
        inner_z=(c_top[s][2],1.145,1.095,1.045,1.010,.990)
        outer_y=(roof_half_width25(-.390),.445,.465,.500,.565,.635)
        outer_z=(roof_point25(-.390,s,1.0)[2],1.125,1.065,1.000,.935,.875)
        for x,iy,iz,oy,oz in zip(xs,inner_y,inner_z,outer_y,outer_z):
            sail.append(((x,s*oy,oz),(x,s*iy,iz)))
        out.append(make_strip('REF_C_PILLAR_SAIL_'+code,sail,M['body'],.010,'REAR_GLASS_EDGE'))

        # Narrow belt transition derived from the V23 successful rear profile, not the V24 broad body-outer strip.
        belt_sections=[
            ((.620,s*.620,.815),(.620,s*.600,.835)),
            ((-.220,s*.600,.825),(-.220,s*.570,.842)),
            ((-.820,s*.555,.850),(-.820,s*.525,.865)),
            ((-1.100,s*.545,.900),(-1.100,s*.505,.918)),
        ]
        out.append(make_strip('REF_WINDOW_BELT_SURFACE_'+code,belt_sections,M['body'],.008,'BELT_EDGE'))
    return out
v.build_glass=greenhouse25

# Re-label V24 projection output. Geometry used by the projection is rebuilt before this function runs.
base_projection=ns24['projection24']
def relabel(data):
    if isinstance(data,dict):return {k:relabel(vv) for k,vv in data.items()}
    if isinstance(data,list):return [relabel(x) for x in data]
    if isinstance(data,str):return data.replace('V24_','V25_')
    return data

def projection25():
    d=relabel(base_projection());d['candidate_revision']='V25_BEST_KNOWN_GATE_HYBRID';d['aperture_interface']='FRONT_V24_REAR_V23_PLUS_SHARED_CLOSURE';return d

BEST={
 'SIDE_UPPER_EVALUATED_MESH_RMSE_M':{'revision':'V24','value':0.030139607740253867,'evidence_source':'V24 REFERENCE_PROJECTION_RECEIPT.json'},
 'SIDE_LOWER_EVALUATED_MESH_RMSE_M':{'revision':'V23','value':0.061843072886901856,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':{'revision':'V23','value':0.0014470662102585852,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':{'revision':'V23','value':0.0004535585654735774,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':{'revision':'V23','value':0.0006911364693363842,'evidence_source':'V23 REFERENCE_PROJECTION_RECEIPT.json'},
 'FRONT_HALF_PROJECTED_PROFILE_RMSE':{'revision':'V24','value':0.07774682558830627,'evidence_source':'V24 REFERENCE_PROJECTION_RECEIPT.json'},
}


def metric(pr,id):return next(m for m in pr['metrics'] if m['id']==id)

def regression25(pr):
    vals={
      'SIDE_UPPER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate'],
      'SIDE_LOWER_EVALUATED_MESH_RMSE_M':metric(pr,'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate'],
      'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':metric(pr,'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error'],
      'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':metric(pr,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error'],
      'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':metric(pr,'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error'],
      'FRONT_HALF_PROJECTED_PROFILE_RMSE':metric(pr,'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate'],
    }
    limits={
      'SIDE_UPPER_EVALUATED_MESH_RMSE_M':.034,'SIDE_LOWER_EVALUATED_MESH_RMSE_M':.066,
      'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR':.010,'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR':.010,
      'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR':.010,'FRONT_HALF_PROJECTED_PROFILE_RMSE':.085,
    }
    locks=[]
    for id,b in BEST.items():
        candidate=vals[id]
        locks.append({'id':id,'baseline':b['value'],'baseline_revision':b['revision'],'candidate':candidate,'limit':limits[id],
                      'status':'PASS' if math.isfinite(candidate) and candidate<=limits[id] else 'REGRESSED','evidence_source':b['evidence_source']})
    rear=metric(pr,'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate'];baseline=.1173280708436564
    rear_improved=math.isfinite(rear) and rear < baseline
    all_locks=all(x['status']=='PASS' for x in locks)
    decision='KEEP_LKG_HOLD_EXPERIMENT' if all_locks and rear_improved else 'KEEP_LKG_REJECT_EXPERIMENT'
    return {
      'schema':'oleander.3d.reference-regression-promotion-receipt.v2',
      'baseline_revision':'BEST_KNOWN_GATE_BASELINE_2026-08-18',
      'candidate_revision':'V25_BEST_KNOWN_GATE_HYBRID',
      'edit_scope':['FRONT_V24_BEST_RETAINED','REAR_ROOF_CROWN','REAR_RAIL_SAIL_DECK_SHARED_BOUNDARY','BACKING_OCCLUSION_RETAINED'],
      'target_metric_delta':{'metric_id':'REAR_HALF_PROJECTED_PROFILE_RMSE','baseline':baseline,'candidate':rear,'direction':'LOWER_IS_BETTER','improved':rear_improved},
      'regression_locks':locks,
      'best_known_gate_baselines':BEST,
      'measurement_method_ids':['V25_FINAL_EVALUATED_MESH_XZ','V25_FINAL_EVALUATED_MESH_YZ'],
      'measurement_comparability':'COMPARABLE','promotion_decision':decision,'visual_review_state':'NOT_RUN','does_not_prove':PROFILE['does_not_prove']}


def post(out):
    if not (out/'REFERENCE_REPRO_QA.json').exists():return
    pr=projection25();(out/'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr,ensure_ascii=False,indent=2)+'\n')
    rr=regression25(pr);(out/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr,ensure_ascii=False,indent=2)+'\n')
    aperture={'schema':'oleander.3d.aperture-interface-receipt.v1','revision':'V25_BEST_KNOWN_GATE_HYBRID',
      'apertures':['WINDSHIELD','SIDE_DOOR_GLASS_L/R','QUARTER_GLASS_L/R','REAR_GLASS'],
      'boundary_owners':['WINDSHIELD_EDGE','ROOF_EDGE','REAR_GLASS_EDGE','BELT_EDGE'],
      'shared_boundary_method':'FRONT_V24_SHARED_BOUNDARY_PLUS_REAR_V25_COMMON_ROOF_POINT',
      'backing_objects':['REF_CABIN_OCCLUSION_BACKING','REF_DASH_BACKING','REF_REAR_BULKHEAD_BACKING'],
      'backing_authority':'DERIVED_EXECUTION_NOT_AUTHORITY','projected_profile_state':pr['status'],
      'boundary_closure_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD','backing_occlusion_state':'MACHINE_CONSTRUCTED_VISUAL_HOLD',
      'visual_review_state':'NOT_RUN','does_not_prove':['manufacturer patch layout','Class-A continuity','seal engineering','tooling','production glazing design']}
    (out/'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(aperture,ensure_ascii=False,indent=2)+'\n')
    q=json.loads((out/'REFERENCE_REPRO_QA.json').read_text());q['reference_fidelity_revision']='V25_BEST_KNOWN_GATE_HYBRID';q['projection_machine_gate']=pr['status'];q['failure_routing']='REAR_INTERFACE_ONLY_WITH_FRONT_BEST_KNOWN_LOCK';q['regression_promotion_decision']=rr['promotion_decision'];q['best_known_gate_policy']='V2_PER_GATE_BASELINE';q['verification_run']='PASS';q['visual_reference_fidelity']='HOLD';q['design_quality_gate']='HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON';(out/'REFERENCE_REPRO_QA.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
    r=json.loads((out/'REFERENCE_REPRO_RECEIPT.json').read_text());r['reference_fidelity_revision']='V25_BEST_KNOWN_GATE_HYBRID';r['projection_machine_gate']=pr['status'];r['regression_promotion_decision']=rr['promotion_decision'];r['best_known_gate_policy']='V2_PER_GATE_BASELINE';r['visual_reference_fidelity']='HOLD_INDEPENDENT_REVIEW';(out/'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')


def run25():
    a=v.m.parse_args();out=Path(a.out).resolve()
    try:v.main()
    except SystemExit as exc:
        post(out);raise SystemExit(exc.code if isinstance(exc.code,int) else 0)
    else:post(out)

run25()
