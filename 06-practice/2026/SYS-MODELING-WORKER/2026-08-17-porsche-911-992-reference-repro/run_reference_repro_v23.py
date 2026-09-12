#!/usr/bin/env python3
"""V23 — error-routed front/rear cross-section correction with regression locks.

V22 proved SIDE X/Z envelopes and basic aperture ratios while FRONT/REAR projected width profiles failed.
V23 therefore edits Y-distribution only: roof crown, front body section taper, rear haunch/sail taper and
interface-to-host boundary placement. Wheelbase, wheel apertures, lower terminal returns and SIDE target
curves remain locked. This is a working-source experiment, not a fidelity/design promotion.
"""
from __future__ import annotations
import json, math
from pathlib import Path
import bpy

HERE = Path(__file__).resolve().parent
V22 = HERE / 'run_reference_repro_v22.py'
text = V22.read_text()
marker = '\ntry:\n v.main()'
if marker not in text:
    raise SystemExit('V22 declaration marker missing')
ns = {'__file__': str(V22), '__name__': 'oleander_v22_declarations'}
exec(compile(text.split(marker, 1)[0], str(V22), 'exec'), ns)
v = ns['v']
PROFILE = ns['PROFILE']
CONTOUR = ns['CONTOUR']

V22_FRONT_RMSE = 0.11187706409643428
V22_REAR_RMSE = 0.27203900272925413
V22_LOCKS = {
    'SIDE_UPPER_EVALUATED_MESH_RMSE_M': 0.03031218750190201,
    'SIDE_LOWER_EVALUATED_MESH_RMSE_M': 0.06184307296925532,
    'FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR': 0.0014470662102585852,
    'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR': 0.0004535585654735774,
    'REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR': 0.0006911364693363842,
}

v.REF = '2025_992.2_CARRERA_CROSS_SECTION_ERROR_ROUTED_V23'
v.REFERENCE_CONTRACT['schema'] = 'oleander.3d.reference-reproduction.porsche-911-992-2.v23'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['cross_section_revision'] = 'V22_FRONT_REAR_PROFILE_ERROR_ROUTED'
v.REFERENCE_CONTRACT['regression_baseline'] = 'V22_FULL_FASTBACK_INTERFACE'
v.REFERENCE_CONTRACT['regression_protocol'] = 'REGRESSION_BASELINE_PROMOTION_PROTOCOL_v1'

CROSS_SECTION = {
    'roof': {
        'front_edge_drop_m': 0.105,
        'neutral_edge_drop_m': 0.118,
        'rear_edge_drop_m': 0.132,
        'crown_exponent': 1.15,
        'front_half_width_cap_m': 0.560,
        'rear_half_width_cap_m': 0.520,
    },
    'front_body_y_scale_by_z': [
        [0.14, 0.94], [0.30, 0.90], [0.50, 0.91], [0.70, 0.93],
        [0.82, 0.94], [0.90, 0.93], [1.00, 0.90],
    ],
    'rear_body_y_scale_by_z': [
        [0.14, 0.92], [0.30, 0.90], [0.50, 0.90], [0.65, 0.91],
        [0.75, 0.88], [0.85, 0.80], [0.95, 0.66], [1.05, 0.54],
        [1.15, 0.46], [1.30, 0.38],
    ],
    'rear_interface_y_scale_by_z': [
        [0.82, 0.96], [0.90, 0.84], [1.00, 0.70], [1.10, 0.62],
        [1.20, 0.58], [1.30, 0.54],
    ],
    'a_pillar_y_scale_by_z': [[0.80, 1.00], [1.00, 0.94], [1.22, 0.84]],
    'protected_xz_families': [
        'SIDE_TOP_SILHOUETTE', 'SIDE_LOWER_ENVELOPE', 'WHEEL_APERTURE',
        'LOWER_TERMINAL_RETURN', 'WHEELBASE', 'AXLE_CENTRES'
    ],
}
v.FAMILY_CONTROLS['FRONT_REAR_CROSS_SECTION_V23'] = CROSS_SECTION
v.REFERENCE_CONTRACT['source_families'] = list(v.FAMILY_CONTROLS.keys())


def interp_table(table, z):
    pts = [(float(a), float(b)) for a, b in table]
    if z <= pts[0][0]:
        return pts[0][1]
    if z >= pts[-1][0]:
        return pts[-1][1]
    for (z0, s0), (z1, s1) in zip(pts, pts[1:]):
        if z0 <= z <= z1:
            t = (z - z0) / (z1 - z0)
            t = t * t * (3.0 - 2.0 * t)
            return s0 * (1.0 - t) + s1 * t
    return pts[-1][1]


def smoothstep01(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


def x_influence(x, front):
    if front:
        if x <= 0.0: return 0.0
        if x >= 0.28: return 1.0
        return smoothstep01(x / 0.28)
    if x >= 0.0: return 0.0
    if x <= -0.28: return 1.0
    return smoothstep01(-x / 0.28)


base_ring = v.body_ring

def body_ring23(x):
    ring = base_ring(x)
    out = []
    fi = x_influence(x, True)
    ri = x_influence(x, False)
    for xe, y, z in ring:
        sf = interp_table(CROSS_SECTION['front_body_y_scale_by_z'], z)
        sr = interp_table(CROSS_SECTION['rear_body_y_scale_by_z'], z)
        scale = 1.0 + fi * (sf - 1.0) + ri * (sr - 1.0)
        out.append((xe, y * scale, z))
    return out
v.body_ring = body_ring23


base_loft = v.build_loft

def roof_drop(x):
    if x >= 0.20:
        return CROSS_SECTION['roof']['front_edge_drop_m']
    if x <= -0.20:
        return CROSS_SECTION['roof']['rear_edge_drop_m']
    t = (x + 0.20) / 0.40
    a = CROSS_SECTION['roof']['rear_edge_drop_m']
    b = CROSS_SECTION['roof']['front_edge_drop_m']
    return a * (1.0 - t) + b * t


def roof_half_width(x):
    rw = max(0.44, v.hermite(v.CABIN_W_PTS, x))
    cap = CROSS_SECTION['roof']['front_half_width_cap_m'] if x >= 0 else CROSS_SECTION['roof']['rear_half_width_cap_m']
    return min(rw, cap)


def roof_patch23(name, material):
    xs = [-1.15 + 1.80 * i / 120 for i in range(121)]
    fracs = (-1.0, -.84, -.68, -.52, -.38, -.26, -.16, -.08, 0.0, .08, .16, .26, .38, .52, .68, .84, 1.0)
    verts, rings = [], []
    exponent = CROSS_SECTION['roof']['crown_exponent']
    for x in xs:
        top = v.hermite(v.ROOF_TOP_PTS, x)
        rw = roof_half_width(x)
        drop = roof_drop(x)
        ring = []
        for f in fracs:
            z = top - drop * (abs(f) ** exponent)
            ring.append(len(verts)); verts.append((x, f * rw, z))
        rings.append(ring)
    faces = []
    for i in range(len(rings) - 1):
        for j in range(len(fracs) - 1):
            faces.append((rings[i][j], rings[i+1][j], rings[i+1][j+1], rings[i][j+1]))
    me = bpy.data.meshes.new(name + '_MESH')
    me.from_pydata(verts, [], faces); me.update()
    o = bpy.data.objects.new(name, me); bpy.context.collection.objects.link(o); o.data.materials.append(material)
    o['OLEANDER_AUTHORITY'] = 'DERIVED_REFERENCE_REPRO_DISPLAY'
    o['OLEANDER_FORM_FAMILY'] = 'ROOF_OUTER_PANEL_V23_CROWN'
    o['OLEANDER_REGENERATED_FROM'] = 'FRONT_REAR_CROSS_SECTION_V23'
    s = o.modifiers.new('ROOF_PANEL_THICKNESS', 'SOLIDIFY'); s.thickness = .010; s.offset = -.25
    for p in me.polygons: p.use_smooth = True
    return o


def build_loft23(name, xs, ringfn, mat, authority, render=True):
    if name == 'DERIVED_911_9922_CABIN':
        return roof_patch23(name, mat)
    return base_loft(name, xs, ringfn, mat, authority, render)
v.build_loft = build_loft23


base_greenhouse = v.build_glass

def transform_mesh_yz(obj, y_scale_fn=None, roof_align=False):
    if obj is None or obj.type != 'MESH': return
    for vert in obj.data.vertices:
        x, y, z = float(vert.co.x), float(vert.co.y), float(vert.co.z)
        if y_scale_fn is not None:
            y *= float(y_scale_fn(z))
        if roof_align:
            top = v.hermite(v.ROOF_TOP_PTS, x)
            rw = max(roof_half_width(x), 1e-6)
            f = min(1.0, abs(y) / rw)
            z = min(z, top - roof_drop(x) * (f ** CROSS_SECTION['roof']['crown_exponent']))
        vert.co.y = y; vert.co.z = z
    obj.data.update()


def greenhouse23(M):
    out = base_greenhouse(M)
    for side in ('L', 'R'):
        transform_mesh_yz(bpy.data.objects.get('REF_ROOF_RAIL_SURFACE_' + side), roof_align=True)
        transform_mesh_yz(
            bpy.data.objects.get('REF_C_PILLAR_SAIL_' + side),
            lambda z: interp_table(CROSS_SECTION['rear_interface_y_scale_by_z'], z)
        )
        transform_mesh_yz(
            bpy.data.objects.get('REF_A_PILLAR_SURFACE_' + side),
            lambda z: interp_table(CROSS_SECTION['a_pillar_y_scale_by_z'], z)
        )
        transform_mesh_yz(
            bpy.data.objects.get('REF_WINDOW_BELT_SURFACE_' + side),
            lambda z: 0.96 if z > .88 else 0.99
        )
    transform_mesh_yz(
        bpy.data.objects.get('REF_REAR_DECK_INTERFACE'),
        lambda z: interp_table(CROSS_SECTION['rear_interface_y_scale_by_z'], z)
    )
    return out
v.build_glass = greenhouse23


base_source = v.build_source

def source23(M):
    o = base_source(M)
    o['OLEANDER_CROSS_SECTION_REVISION'] = 'V23_FRONT_REAR_ERROR_ROUTED'
    o['OLEANDER_EDIT_SCOPE'] = 'Y_DISTRIBUTION_ONLY'
    o['OLEANDER_PROTECTED_XZ'] = json.dumps(CROSS_SECTION['protected_xz_families'])
    o['OLEANDER_CONTROL_DIGEST'] = v.m.sha_json(v.FAMILY_CONTROLS)
    return o
v.build_source = source23


base_projection = ns['projection22']

def replace_measurement_labels(data):
    if isinstance(data, dict):
        return {k: replace_measurement_labels(vv) for k, vv in data.items()}
    if isinstance(data, list):
        return [replace_measurement_labels(x) for x in data]
    if isinstance(data, str):
        return data.replace('V22_', 'V23_')
    return data


def projection23():
    d = replace_measurement_labels(base_projection())
    d['candidate_revision'] = 'V23_FRONT_REAR_CROSS_SECTION_ERROR_ROUTED'
    d['cross_section_revision'] = 'Y_ONLY_FRONT_REAR_PROFILE_CORRECTION'
    return d


def metric_by_id(pr, metric_id):
    return next(m for m in pr['metrics'] if m['id'] == metric_id)


def regression_receipt(pr):
    upper = metric_by_id(pr, 'SIDE_UPPER_EVALUATED_MESH_RMSE_M')['candidate']
    lower = metric_by_id(pr, 'SIDE_LOWER_EVALUATED_MESH_RMSE_M')['candidate']
    fuc = metric_by_id(pr, 'FRONT_UPPER_CABIN_WIDTH_RATIO')['abs_error']
    fwl = metric_by_id(pr, 'FRONT_WINDSHIELD_LOWER_WIDTH_RATIO')['abs_error']
    rbl = metric_by_id(pr, 'REAR_BACKLIGHT_LOWER_WIDTH_RATIO')['abs_error']
    front = metric_by_id(pr, 'FRONT_HALF_PROJECTED_PROFILE_RMSE')['candidate']
    rear = metric_by_id(pr, 'REAR_HALF_PROJECTED_PROFILE_RMSE')['candidate']
    locks_spec = [
        ('SIDE_UPPER_EVALUATED_MESH_RMSE_M', V22_LOCKS['SIDE_UPPER_EVALUATED_MESH_RMSE_M'], upper, .034),
        ('SIDE_LOWER_EVALUATED_MESH_RMSE_M', V22_LOCKS['SIDE_LOWER_EVALUATED_MESH_RMSE_M'], lower, .066),
        ('FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR', V22_LOCKS['FRONT_UPPER_CABIN_WIDTH_RATIO_ERROR'], fuc, .010),
        ('FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR', V22_LOCKS['FRONT_WINDSHIELD_LOWER_WIDTH_RATIO_ERROR'], fwl, .010),
        ('REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR', V22_LOCKS['REAR_BACKLIGHT_LOWER_WIDTH_RATIO_ERROR'], rbl, .010),
    ]
    locks = [{
        'id': lid, 'baseline': baseline, 'candidate': candidate, 'limit': limit,
        'status': 'PASS' if math.isfinite(candidate) and candidate <= limit else 'REGRESSED',
        'evidence_source': 'REFERENCE_PROJECTION_RECEIPT.json'
    } for lid, baseline, candidate, limit in locks_spec]
    rear_improved = math.isfinite(rear) and rear < V22_REAR_RMSE - .005
    front_not_worse = math.isfinite(front) and front <= V22_FRONT_RMSE + .005
    all_locks = all(x['status'] == 'PASS' for x in locks)
    decision = 'KEEP_LKG_HOLD_EXPERIMENT' if all_locks and rear_improved and front_not_worse else 'KEEP_LKG_REJECT_EXPERIMENT'
    return {
        'schema': 'oleander.3d.reference-regression-promotion-receipt.v1',
        'baseline_revision': 'V22_FULL_FASTBACK_INTERFACE',
        'candidate_revision': 'V23_FRONT_REAR_CROSS_SECTION_ERROR_ROUTED',
        'edit_scope': ['ROOF_CROSS_SECTION', 'FRONT_BODY_Y_SECTION', 'REAR_HAUNCH_Y_SECTION', 'GREENHOUSE_INTERFACE_Y_SECTION'],
        'target_metric_delta': {
            'metric_id': 'REAR_HALF_PROJECTED_PROFILE_RMSE',
            'baseline': V22_REAR_RMSE,
            'candidate': rear,
            'direction': 'LOWER_IS_BETTER',
            'improved': rear_improved,
        },
        'secondary_target_metrics': [{
            'metric_id': 'FRONT_HALF_PROJECTED_PROFILE_RMSE',
            'baseline': V22_FRONT_RMSE,
            'candidate': front,
            'direction': 'LOWER_IS_BETTER',
            'improved': math.isfinite(front) and front < V22_FRONT_RMSE,
        }],
        'regression_locks': locks,
        'measurement_method_ids': ['V23_FINAL_EVALUATED_MESH_XZ', 'V23_FINAL_EVALUATED_MESH_YZ'],
        'measurement_comparability': 'COMPARABLE',
        'promotion_decision': decision,
        'visual_review_state': 'NOT_RUN',
        'does_not_prove': PROFILE['does_not_prove'],
    }


def postprocess(out):
    if not (out / 'REFERENCE_REPRO_QA.json').exists():
        return
    pr = projection23()
    (out / 'REFERENCE_PROJECTION_RECEIPT.json').write_text(json.dumps(pr, ensure_ascii=False, indent=2) + '\n')
    rr = regression_receipt(pr)
    (out / 'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').write_text(json.dumps(rr, ensure_ascii=False, indent=2) + '\n')
    source_delta = {
        'schema': 'oleander.3d.source-edit-delta.v1',
        'revision': 'V23_FRONT_REAR_CROSS_SECTION_ERROR_ROUTED',
        'authorization': 'WORKING_SOURCE_REFERENCE_REPRODUCTION_EDIT',
        'edit_scope': rr['edit_scope'],
        'protected_families': CROSS_SECTION['protected_xz_families'],
        'change_axis': 'Y_ONLY_FOR_BODY_AND_INTERFACE_SECTION; ROOF_Z_CHANGES_ONLY_WITHIN_FIXED_SIDE_TOP_ENVELOPE',
        'rollback_revision': 'V22_FULL_FASTBACK_INTERFACE',
        'does_not_prove': PROFILE['does_not_prove'],
    }
    (out / 'SOURCE_EDIT_DELTA_V23.json').write_text(json.dumps(source_delta, ensure_ascii=False, indent=2) + '\n')

    q = json.loads((out / 'REFERENCE_REPRO_QA.json').read_text())
    q['reference_fidelity_revision'] = 'V23_FRONT_REAR_CROSS_SECTION_ERROR_ROUTED'
    q['projection_machine_gate'] = pr['status']
    q['front_profile_rmse'] = pr['front_profile']['rmse']
    q['rear_profile_rmse'] = pr['rear_profile']['rmse']
    q['failure_routing'] = 'FRONT_REAR_CROSS_SECTION_ONLY'
    q['regression_promotion_decision'] = rr['promotion_decision']
    q['regression_locks'] = rr['regression_locks']
    q['verification_run'] = 'PASS'
    q['visual_reference_fidelity'] = 'HOLD'
    q['design_quality_gate'] = 'HOLD_FOR_INDEPENDENT_REFERENCE_COMPARISON'
    (out / 'REFERENCE_REPRO_QA.json').write_text(json.dumps(q, ensure_ascii=False, indent=2) + '\n')

    r = json.loads((out / 'REFERENCE_REPRO_RECEIPT.json').read_text())
    r['reference_fidelity_revision'] = 'V23_FRONT_REAR_CROSS_SECTION_ERROR_ROUTED'
    r['projection_machine_gate'] = pr['status']
    r['regression_promotion_decision'] = rr['promotion_decision']
    r['verification_run'] = 'PASS'
    r['visual_reference_fidelity'] = 'HOLD_INDEPENDENT_REVIEW'
    (out / 'REFERENCE_REPRO_RECEIPT.json').write_text(json.dumps(r, ensure_ascii=False, indent=2) + '\n')


def run():
    a = v.m.parse_args()
    out = Path(a.out).resolve()
    try:
        v.main()
    except SystemExit as exc:
        postprocess(out)
        raise SystemExit(exc.code if isinstance(exc.code, int) else 0)
    else:
        postprocess(out)


run()
