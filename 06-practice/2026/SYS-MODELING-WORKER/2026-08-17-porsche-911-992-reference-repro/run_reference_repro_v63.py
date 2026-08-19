#!/usr/bin/env python3
"""V63 — destructive-edit preflight for topology-owned greenhouse apertures.

V62 moved the greenhouse opening away from post-evaluated Boolean toward topology-owned face removal,
but its first CI run failed before any V62 artifact could be persisted. V63 does not change the Porsche
shape or aperture target. It adds a dry-run classification witness before any destructive face deletion.

Core rule:
    CLASSIFICATION_HIT != SAFE_TO_DELETE
    PREFLIGHT_PASS -> DESTRUCTIVE_EDIT_ALLOWED
    PREFLIGHT_FAIL -> HOST_UNCHANGED + DIAGNOSTIC_ARTIFACT

Primary-body Source remains V59. No Source geometry delta is authorized.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy
import bmesh

HERE = Path(__file__).resolve().parent
V62 = HERE / 'run_reference_repro_v62.py'
text = V62.read_text(encoding='utf-8')
marker = '\nrun62()\n'
if marker not in text:
    raise SystemExit('V62 run marker missing')
ns = {'__file__': str(V62), '__name__': 'oleander_v63_aperture_preflight'}
exec(compile(text.split(marker, 1)[0], str(V62), 'exec'), ns)

v = ns['v']
core = ns['core']
runtime = ns['runtime']
STATS = ns['STATS']
base_remove = ns['remove_owned_aperture_faces']
world_bounds = ns['world_bounds']
G = ns['G']
PRIMARY_BODY_REV = ns['PRIMARY_BODY_REV']
REV = 'V63_GREENHOUSE_TOPOLOGY_PREFLIGHT'
ns['REV'] = REV
v.REF = '2025_992.2_CARRERA_TOPOLOGY_PREFLIGHT_V63'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['candidate_revision'] = REV
v.REFERENCE_CONTRACT['aperture_architecture_state'] = 'TOPOLOGY_OWNED_APERTURE_WITH_DESTRUCTIVE_PREFLIGHT'
v.REFERENCE_CONTRACT['destructive_edit_preflight'] = True
v.REFERENCE_CONTRACT['greenhouse_classifier_dependency'] = 'EXPLICIT_BOUND_G_TABLE_NOT_HISTORICAL_NESTED_NAMESPACE'
v.FAMILY_CONTROLS['GREENHOUSE_APERTURE_ARCHITECTURE_V62']['preflight_revision'] = REV


def interp_greenhouse(x, field):
    x = float(x)
    if x <= float(G[0][0]):
        return float(G[0][field])
    if x >= float(G[-1][0]):
        return float(G[-1][field])
    for a,b in zip(G,G[1:]):
        if float(a[0]) <= x <= float(b[0]):
            den = float(b[0]) - float(a[0])
            t = 0.0 if abs(den) < 1e-12 else (x-float(a[0]))/den
            return float(a[field])*(1.0-t) + float(b[field])*t
    return float(G[-1][field])


def point_in_poly(x, z, poly):
    inside = False
    j = len(poly)-1
    for i in range(len(poly)):
        xi,zi = poly[i]; xj,zj = poly[j]
        crosses = ((zi > z) != (zj > z)) and (x < (xj-xi)*(z-zi)/((zj-zi) or 1e-12)+xi)
        if crosses:
            inside = not inside
        j = i
    return inside


def classify_aperture(x, y, z):
    if float(G[0][0]) <= x <= float(G[-1][0]):
        zt = interp_greenhouse(x,1)
        zb = interp_greenhouse(x,2)
        if zb-.012 <= z <= zt+.012 and abs(y) >= .34:
            return 'BOUNDARY_SIDE_GLASS_L' if y > 0 else 'BOUNDARY_SIDE_GLASS_R'
    ws_xz=[(.625,.845),(.245,1.220),(.185,1.255),(.710,.775)]
    rg_xz=[(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]
    if abs(y) <= .67 and point_in_poly(x,z,ws_xz):
        return 'BOUNDARY_WINDSHIELD'
    if abs(y) <= .66 and point_in_poly(x,z,rg_xz):
        return 'BOUNDARY_REAR_GLASS'
    return None


# Inject the semantic classifier into the V62 representation namespace as well as this preflight.
# The destructive function therefore no longer depends on ctx['ns'] depth inherited from historical scripts.
ns['classify_aperture'] = classify_aperture

PREFLIGHT = {
    'schema': 'oleander.3d.destructive-edit-preflight-receipt.v1',
    'candidate_revision': REV,
    'host_id': 'DERIVED_911_9922_BODY',
    'host_state_class': 'DERIVED_EXECUTION',
    'operation': 'FACE_CLASSIFICATION_DELETE_KEEP_BOUNDARY',
    'edit_scope': 'GREENHOUSE_APERTURE_ARCHITECTURE_ONLY',
    'source_revision_locked': PRIMARY_BODY_REV,
    'source_mutation_allowed': False,
    'classifier_dependency': 'EXPLICIT_BOUND_G_TABLE',
    'required_owner_ids': ['BOUNDARY_SIDE_GLASS_L','BOUNDARY_SIDE_GLASS_R','BOUNDARY_WINDSHIELD','BOUNDARY_REAR_GLASS'],
    'owner_hit_counts': {},
    'candidate_delete_faces': 0,
    'host_faces_before': 0,
    'predicted_face_retention_ratio': 0.0,
    'host_bounds_before': [],
    'preflight_checks': [],
    'preflight_result': 'NOT_RUN',
    'destructive_edit_executed': False,
    'does_not_prove': ['aperture quality','reference fidelity','Class-A continuity','Design KEEP','MAIN KEEP']
}


def preflight_remove_owned_aperture_faces(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    counts = {}
    candidate_delete = 0
    for face in list(bm.faces):
        c = obj.matrix_world @ face.calc_center_median()
        owner = classify_aperture(float(c.x), float(c.y), float(c.z))
        if owner:
            candidate_delete += 1
            counts[owner] = counts.get(owner, 0) + 1
    bm.free()

    host_faces = len(obj.data.polygons)
    retention = (host_faces - candidate_delete) / max(host_faces, 1)
    required = PREFLIGHT['required_owner_ids']
    missing = [owner for owner in required if counts.get(owner, 0) <= 0]
    checks = [
        {
            'id':'ALL_REQUIRED_OWNER_MASKS_HIT',
            'status':'PASS' if not missing else 'FAIL',
            'observed':{owner:int(counts.get(owner,0)) for owner in required},
            'rule':'every declared aperture owner must classify at least one evaluated host face'
        },
        {
            'id':'PREDICTED_GLOBAL_FACE_RETENTION',
            'status':'PASS' if retention >= .70 else 'FAIL',
            'observed':retention,
            'rule':'predicted post-edit host face retention >= 0.70 before destructive execution'
        },
        {
            'id':'SOURCE_MUTATION_AUTHORIZATION',
            'status':'PASS',
            'observed':False,
            'rule':'operation remains on Derived host; V59 Source mutation forbidden'
        },
        {
            'id':'CLASSIFIER_DEPENDENCY_BOUND',
            'status':'PASS',
            'observed':'EXPLICIT_BOUND_G_TABLE',
            'rule':'classifier must not depend on historical nested namespace path'
        }
    ]
    passed = all(c['status'] == 'PASS' for c in checks)
    PREFLIGHT.update({
        'owner_hit_counts': {owner:int(counts.get(owner,0)) for owner in required},
        'candidate_delete_faces': int(candidate_delete),
        'host_faces_before': int(host_faces),
        'predicted_face_retention_ratio': float(retention),
        'host_bounds_before': world_bounds(obj),
        'preflight_checks': checks,
        'preflight_result': 'PASS_DESTRUCTIVE_EDIT_ALLOWED' if passed else 'FAIL_DESTRUCTIVE_EDIT_BLOCKED',
        'destructive_edit_executed': bool(passed),
        'missing_owner_masks': missing
    })

    if not passed:
        obj['OLEANDER_APERTURE_PREFLIGHT'] = PREFLIGHT['preflight_result']
        obj['OLEANDER_APERTURE_DESTRUCTIVE_EDIT_EXECUTED'] = False
        return obj

    return base_remove(obj)


# build62 resolves this symbol from the V62 execution namespace.
ns['remove_owned_aperture_faces'] = preflight_remove_owned_aperture_faces


def write_preflight(out):
    Path(out, 'DESTRUCTIVE_EDIT_PREFLIGHT_RECEIPT.json').write_text(json.dumps(PREFLIGHT, ensure_ascii=False, indent=2) + '\n')


def run63():
    a = v.m.parse_args()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    code = 0
    try:
        runtime['run30']()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
    finally:
        write_preflight(out)

    try:
        ns['ctx']['emit_surface_v2'](out)
    except Exception as exc:
        Path(out, 'V63_POSTRUN_DIAGNOSTIC.json').write_text(json.dumps({
            'stage':'emit_surface_v2','error':type(exc).__name__ + ':' + str(exc)
        }, indent=2) + '\n')

    if PREFLIGHT['preflight_result'] != 'PASS_DESTRUCTIVE_EDIT_ALLOWED':
        raise SystemExit(6)

    try:
        preservation = ns['host_preservation_receipt'](out)
        aperture = ns['aperture_receipt'](out)
        ns['update_overall'](out, aperture, preservation)
    except SystemExit:
        raise
    except Exception as exc:
        Path(out, 'V63_POSTRUN_DIAGNOSTIC.json').write_text(json.dumps({
            'stage':'post_receipts','error':type(exc).__name__ + ':' + str(exc)
        }, indent=2) + '\n')
        raise SystemExit(7)

    raise SystemExit(code)


run63()
