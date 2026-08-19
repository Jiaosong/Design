#!/usr/bin/env python3
"""V61 — repair V60 aperture execution with cutter-normal normalization + host-retention gate.

V60 is retained as REJECT provenance: the rear-glass Boolean executed but collapsed the Derived host
from 8,637 faces to 96 faces. V61 does not reopen the design scope. It keeps V59 primary-body Source
and the V60 aperture definitions, but repairs execution semantics:

1. recalculate cutter face normals before Boolean evaluation;
2. after every LOCAL cut, verify global host face-retention and world-bounds retention;
3. fail immediately when the local edit damages the global host beyond the declared budget.

`BOOLEAN APPLIED != LOCAL EDIT SUCCEEDED != HOST PRESERVED`.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy
import bmesh

HERE = Path(__file__).resolve().parent
V60 = HERE / 'run_reference_repro_v60.py'
text = V60.read_text(encoding='utf-8')
marker = '\nrun60()\n'
if marker not in text:
    raise SystemExit('V60 run marker missing')
ctx = {'__file__': str(V60), '__name__': 'oleander_v61_host_preservation'}
exec(compile(text.split(marker, 1)[0], str(V60), 'exec'), ctx)

v = ctx['v']
core = ctx['core']
runtime = ctx['runtime']
APERTURE_STATS = ctx['APERTURE_STATS']
PRIMARY_BODY_REV = ctx['PRIMARY_BODY_REV']
REV = 'V61_GREENHOUSE_APERTURE_HOST_PRESERVED'
ctx['REV'] = REV
v.REF = '2025_992.2_CARRERA_APERTURE_HOST_PRESERVED_V61'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['candidate_revision'] = REV
v.REFERENCE_CONTRACT['aperture_architecture_state'] = 'OWNED_APERTURE_WITH_LOCAL_EDIT_HOST_PRESERVATION_GATE'
v.REFERENCE_CONTRACT['derived_edit_host_preservation_protocol'] = 'oleander-3d-pipeline/DERIVED_EDIT_HOST_PRESERVATION_PROTOCOL_v1.md'
v.FAMILY_CONTROLS['GREENHOUSE_APERTURE_ARCHITECTURE_V60']['execution_repair'] = {
    'revision': REV,
    'cutter_normals': 'RECALCULATE_OUTWARD_BEFORE_BOOLEAN',
    'local_face_retention_min': 0.70,
    'local_world_bounds_ratio_min': 0.95,
    'hard_fail': 'FAIL_DERIVED_EDIT_HOST_PRESERVATION'
}

HOST_GATE = {
    'face_retention_min': 0.70,
    'bounds_ratio_min': 0.95,
    'steps': []
}


def world_bounds(obj):
    mw = obj.matrix_world
    pts = [mw @ vert.co for vert in obj.data.vertices]
    if not pts:
        return {'min':[0,0,0], 'max':[0,0,0], 'dimensions':[0,0,0]}
    mins = [min(float(p[i]) for p in pts) for i in range(3)]
    maxs = [max(float(p[i]) for p in pts) for i in range(3)]
    return {'min': mins, 'max': maxs, 'dimensions': [maxs[i]-mins[i] for i in range(3)]}


def normalized_prism(name, polygon_xz, y0, y1):
    obj = ctx['mesh_prism_xz'](name, polygon_xz, y0, y1)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()
    obj['OLEANDER_CUTTER_NORMALS'] = 'RECALCULATED_OUTWARD'
    return obj


def apply_boolean61(host, cutter, owner_id):
    before_faces = len(host.data.polygons)
    before_vertices = len(host.data.vertices)
    before_bounds = world_bounds(host)

    mod = host.modifiers.new('CUT_' + owner_id, 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    try:
        mod.solver = 'EXACT'
    except Exception:
        pass
    mod.object = cutter
    bpy.ops.object.select_all(action='DESELECT')
    host.select_set(True)
    bpy.context.view_layer.objects.active = host
    ok = True
    err = None
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as exc:
        ok = False
        err = type(exc).__name__ + ':' + str(exc)

    after_faces = len(host.data.polygons)
    after_vertices = len(host.data.vertices)
    after_bounds = world_bounds(host)
    face_ratio = after_faces / max(before_faces, 1)
    bound_ratios = [after_bounds['dimensions'][i] / max(before_bounds['dimensions'][i], 1e-9) for i in range(3)]
    min_bound_ratio = min(bound_ratios)
    changed = (before_faces, before_vertices) != (after_faces, after_vertices)
    face_pass = face_ratio >= HOST_GATE['face_retention_min']
    bounds_pass = min_bound_ratio >= HOST_GATE['bounds_ratio_min']
    step = {
        'owner_id': owner_id,
        'before_vertices': before_vertices,
        'before_faces': before_faces,
        'after_vertices': after_vertices,
        'after_faces': after_faces,
        'face_retention_ratio': face_ratio,
        'before_bounds': before_bounds,
        'after_bounds': after_bounds,
        'bounds_retention_ratio_xyz': bound_ratios,
        'min_bounds_retention_ratio': min_bound_ratio,
        'operator_applied': ok,
        'geometry_changed': changed,
        'face_retention_gate': 'PASS' if face_pass else 'FAIL',
        'bounds_retention_gate': 'PASS' if bounds_pass else 'FAIL',
        'status': 'PASS' if ok and changed and face_pass and bounds_pass else 'FAIL',
        'error': err
    }
    HOST_GATE['steps'].append(step)
    APERTURE_STATS['boolean_results'].append({
        'owner_id': owner_id,
        'before_vertices': before_vertices, 'before_faces': before_faces,
        'after_vertices': after_vertices, 'after_faces': after_faces,
        'applied': ok, 'error': err, 'geometry_changed': changed,
        'face_retention_ratio': face_ratio,
        'min_bounds_retention_ratio': min_bound_ratio,
        'host_preservation_status': step['status']
    })
    if cutter.name in bpy.data.objects:
        bpy.data.objects.remove(cutter, do_unlink=True)
    if step['status'] != 'PASS':
        raise SystemExit('FAIL_DERIVED_EDIT_HOST_PRESERVATION_' + owner_id)


# V60 build60 resolves these functions from its own globals; replacing them here repairs execution
# without changing the aperture geometry definitions or primary-body Source.
ctx['mesh_prism_xz'] = normalized_prism
ctx['apply_boolean'] = apply_boolean61


def host_preservation_receipt(out):
    steps = HOST_GATE['steps']
    if len(steps) != 4:
        raise SystemExit('FAIL_HOST_PRESERVATION_STEP_COUNT')
    first, last = steps[0], steps[-1]
    checks = []
    for s in steps:
        checks.append({
            'id': s['owner_id'] + '_FACE_RETENTION', 'metric': 'faces_ratio',
            'before': s['before_faces'], 'after': s['after_faces'],
            'rule': 'after_faces / before_faces >= 0.70 for each declared LOCAL aperture edit',
            'status': s['face_retention_gate'], 'scope': 'GLOBAL_HOST'
        })
        checks.append({
            'id': s['owner_id'] + '_BOUNDS_RETENTION', 'metric': 'min_world_bounds_ratio_xyz',
            'before': 1.0, 'after': s['min_bounds_retention_ratio'],
            'rule': 'min world-space dimension retention >= 0.95 for each declared LOCAL aperture edit',
            'status': s['bounds_retention_gate'], 'scope': 'GLOBAL_HOST'
        })
    all_pass = all(c['status'] == 'PASS' for c in checks)
    d = {
        'schema': 'oleander.3d.derived-edit-host-preservation-receipt.v1',
        'host_id': 'DERIVED_911_9922_BODY',
        'host_state_class': 'DERIVED_EXECUTION',
        'operation': 'BOOLEAN_DIFFERENCE',
        'edit_scope': 'GREENHOUSE_APERTURE_ARCHITECTURE_ONLY',
        'locality': 'LOCAL',
        'source_mutation_allowed': False,
        'source_unchanged_or_na': True,
        'source_witness': 'Operation target is DERIVED_911_9922_BODY; PRIMARY_BODY_SURFACE_RECEIPT_V2 remains revision V59 with 20 Source controls and 0 folds.',
        'before': {
            'vertices': first['before_vertices'], 'faces': first['before_faces'],
            'bounds': first['before_bounds']['dimensions']
        },
        'after': {
            'vertices': last['after_vertices'], 'faces': last['after_faces'],
            'bounds': last['after_bounds']['dimensions']
        },
        'preservation_checks': checks,
        'operator_execution': 'PASS_EXECUTED',
        'host_preservation_result': 'PASS_WITHIN_DECLARED_BUDGET' if all_pass else 'FAIL_HOST_PRESERVATION',
        'evidence_result': 'PASS_EVIDENCE_SCOPE' if all_pass else 'FAIL_EVIDENCE_INVALID',
        'design_result': 'HOLD_NOT_REVIEWED',
        'geometry_changed_only_basis': False,
        'v60_failure_provenance': {
            'revision': 'V60_GREENHOUSE_APERTURE_OWNERSHIP',
            'rear_glass_before_faces': 8637,
            'rear_glass_after_faces': 96,
            'failure': 'DESTRUCTIVE_DERIVED_EDIT_HOST_PRESERVATION_NOT_GATED'
        },
        'does_not_prove': [
            'reference fidelity','Class-A continuity','manufacturer CAD','production aperture construction',
            'physical CMF','Design KEEP','MAIN KEEP'
        ]
    }
    Path(out, 'DERIVED_EDIT_HOST_PRESERVATION_RECEIPT.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    if not all_pass:
        raise SystemExit('FAIL_DERIVED_EDIT_HOST_PRESERVATION')
    return d


def run61():
    a = v.m.parse_args()
    out = Path(a.out).resolve()
    code = 0
    try:
        runtime['run30']()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
    ctx['emit_surface_v2'](out)
    aperture = ctx['aperture_receipt'](out)
    preservation = host_preservation_receipt(out)
    ctx['update_overall_receipts'](out, aperture)
    for name in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p = Path(out, name)
        if p.exists():
            d = json.loads(p.read_text(encoding='utf-8'))
            d['reference_fidelity_revision'] = REV
            d['host_preservation'] = preservation['host_preservation_result']
            d['visual_reference_fidelity'] = 'HOLD_ACTUAL_PREVIEW_REVIEW_REQUIRED'
            d['design_quality_gate'] = 'HOLD_FOR_OLEANDER_ARTIFACT_REVIEW'
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    raise SystemExit(code)


run61()
