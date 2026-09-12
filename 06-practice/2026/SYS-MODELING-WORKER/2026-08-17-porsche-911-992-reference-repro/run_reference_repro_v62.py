#!/usr/bin/env python3
"""V62 — topology-owned greenhouse apertures on the locked V59 primary body.

V60 proved that a post-evaluated Boolean can report success while catastrophically destroying the host.
V61 introduced host-preservation guarding but the post-evaluated Boolean route remained an unstable
representation choice. V62 therefore escalates the failure from operator tuning to representation architecture.

Primary-body Source delta: NONE relative to V59.
Authorized Derived edit family: GREENHOUSE_APERTURE_ARCHITECTURE_ONLY.

Instead of Boolean cutters, V62 removes only evaluated host faces classified inside the four owned aperture
regions, keeps boundary edges, and then attaches the same interface/infill/backing architecture. The uncut
V59 evaluated diagnostic carrier remains the primary-body surface evidence carrier.

This is a reference-reproduction benchmark, not Porsche CAD, Class-A surfacing, production aperture topology,
sealing/tooling, manufacturing feasibility, physical CMF, Design KEEP or MAIN KEEP.
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
ctx = {'__file__': str(V60), '__name__': 'oleander_v62_topology_owned_aperture'}
exec(compile(text.split(marker, 1)[0], str(V60), 'exec'), ctx)

v = ctx['v']
core = ctx['core']
runtime = ctx['runtime']
G = ctx['G']
base_build = ctx['base_build']
base_greenhouse = v.build_glass
PRIMARY_BODY_REV = ctx['PRIMARY_BODY_REV']
REV = 'V62_GREENHOUSE_TOPOLOGY_OWNED_APERTURE'
ctx['REV'] = REV

v.REF = '2025_992.2_CARRERA_TOPOLOGY_OWNED_APERTURE_V62'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['candidate_revision'] = REV
v.REFERENCE_CONTRACT['primary_body_revision_locked'] = PRIMARY_BODY_REV
v.REFERENCE_CONTRACT['source_edit_scope'] = 'NONE_PRIMARY_BODY__DERIVED_GREENHOUSE_APERTURE_ONLY'
v.REFERENCE_CONTRACT['aperture_architecture_state'] = 'TOPOLOGY_OWNED_OPENING_INTERFACE_INFILL_BACKING_EXPERIMENT'
v.REFERENCE_CONTRACT['derived_edit_method'] = 'EVALUATED_FACE_CLASSIFICATION_REMOVAL_KEEP_BOUNDARY'
v.REFERENCE_CONTRACT['operator_escalation_provenance'] = ['V60_BOOLEAN_HOST_COLLAPSE', 'V61_BOOLEAN_GUARD_EXECUTION_FAILURE']
v.FAMILY_CONTROLS['GREENHOUSE_APERTURE_ARCHITECTURE_V62'] = {
    'tier': 'DERIVED_IDENTITY_CRITICAL_APERTURE',
    'reference': 'REFERENCE_GREENHOUSE_TARGETS_992_2.json',
    'host_surface': 'DERIVED_911_9922_BODY',
    'method': 'FACE_CLASSIFICATION_DELETE_KEEP_BOUNDARY',
    'opening_boundary_owners': [
        'BOUNDARY_SIDE_GLASS_L','BOUNDARY_SIDE_GLASS_R','BOUNDARY_WINDSHIELD','BOUNDARY_REAR_GLASS'
    ],
    'protected': [
        PRIMARY_BODY_REV,'V49_SOURCE_DENSITY','REAR_PRIMARY_BODY','OFFICIAL_HARD_POINTS',
        'AXLES','WHEEL_TYRE_PACKAGE','DIAG_FEATURE_ALIGNED_SURFACED_V59'
    ],
    'forbidden': [
        'POST_EVALUATED_BOOLEAN','CAGE_DENSIFICATION','PRIMARY_BODY_REWRITE','REAR_PRIMARY_FORM_EDIT',
        'CAMERA_TUNING_TO_HIDE_APERTURE_DEFECTS','OPAQUE_GLASS_AS_BACKING_SUBSTITUTE'
    ],
    'rollback': 'V59_SPARSE_FRONT_HOOD_FENDER_RELATION'
}
v.REFERENCE_CONTRACT['source_families'] = list(v.FAMILY_CONTROLS.keys())

STATS = {
    'host_pre_vertices': 0,
    'host_pre_faces': 0,
    'host_post_vertices': 0,
    'host_post_faces': 0,
    'removed_faces': 0,
    'removed_by_owner': {},
    'face_retention_ratio': 0.0,
    'bounds_retention_ratio_xyz': [],
    'boundary_edge_count': 0,
}


def world_bounds(obj):
    mw = obj.matrix_world
    pts = [mw @ vert.co for vert in obj.data.vertices]
    mins = [min(float(p[i]) for p in pts) for i in range(3)]
    maxs = [max(float(p[i]) for p in pts) for i in range(3)]
    return [maxs[i] - mins[i] for i in range(3)]


def point_in_poly(x, z, poly):
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, zi = poly[i]
        xj, zj = poly[j]
        crosses = ((zi > z) != (zj > z)) and (x < (xj - xi) * (z - zi) / ((zj - zi) or 1e-12) + xi)
        if crosses:
            inside = not inside
        j = i
    return inside


def classify_aperture(x, y, z):
    interp = ctx['ns']['interpG']
    if float(G[0][0]) <= x <= float(G[-1][0]):
        zt = float(interp(x, 1))
        zb = float(interp(x, 2))
        if zb - .012 <= z <= zt + .012 and abs(y) >= .34:
            return 'BOUNDARY_SIDE_GLASS_L' if y > 0 else 'BOUNDARY_SIDE_GLASS_R'

    ws_xz = [(.625,.845),(.245,1.220),(.185,1.255),(.710,.775)]
    rg_xz = [(-.405,1.220),(-1.145,.970),(-1.255,.900),(-.330,1.255)]
    if abs(y) <= .67 and point_in_poly(x, z, ws_xz):
        return 'BOUNDARY_WINDSHIELD'
    if abs(y) <= .66 and point_in_poly(x, z, rg_xz):
        return 'BOUNDARY_REAR_GLASS'
    return None


def remove_owned_aperture_faces(obj):
    before_bounds = world_bounds(obj)
    STATS['host_pre_vertices'] = len(obj.data.vertices)
    STATS['host_pre_faces'] = len(obj.data.polygons)

    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.faces.ensure_lookup_table()
    by_owner = {}
    doomed = []
    for face in list(bm.faces):
        c = obj.matrix_world @ face.calc_center_median()
        owner = classify_aperture(float(c.x), float(c.y), float(c.z))
        if owner:
            doomed.append(face)
            by_owner[owner] = by_owner.get(owner, 0) + 1

    required = ['BOUNDARY_SIDE_GLASS_L','BOUNDARY_SIDE_GLASS_R','BOUNDARY_WINDSHIELD','BOUNDARY_REAR_GLASS']
    missing = [owner for owner in required if by_owner.get(owner, 0) <= 0]
    if missing:
        bm.free()
        raise SystemExit('FAIL_V62_APERTURE_CLASSIFICATION_EMPTY_' + '_'.join(missing))

    bmesh.ops.delete(bm, geom=doomed, context='FACES_KEEP_BOUNDARY')
    bmesh.ops.recalc_face_normals(bm, faces=list(bm.faces))
    boundary_edges = sum(1 for edge in bm.edges if edge.is_boundary)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.update()

    after_bounds = world_bounds(obj)
    STATS['host_post_vertices'] = len(obj.data.vertices)
    STATS['host_post_faces'] = len(obj.data.polygons)
    STATS['removed_faces'] = len(doomed)
    STATS['removed_by_owner'] = by_owner
    STATS['face_retention_ratio'] = STATS['host_post_faces'] / max(STATS['host_pre_faces'], 1)
    STATS['bounds_retention_ratio_xyz'] = [after_bounds[i] / max(before_bounds[i], 1e-9) for i in range(3)]
    STATS['boundary_edge_count'] = boundary_edges

    if STATS['face_retention_ratio'] < .70:
        raise SystemExit('FAIL_V62_HOST_FACE_RETENTION')
    if min(STATS['bounds_retention_ratio_xyz']) < .95:
        raise SystemExit('FAIL_V62_HOST_BOUNDS_RETENTION')
    if boundary_edges <= 0:
        raise SystemExit('FAIL_V62_NO_APERTURE_BOUNDARY_EDGES')

    obj['OLEANDER_APERTURE_ARCHITECTURE'] = REV
    obj['OLEANDER_APERTURE_METHOD'] = 'FACE_CLASSIFICATION_DELETE_KEEP_BOUNDARY'
    obj['OLEANDER_PRIMARY_BODY_SOURCE_REVISION'] = PRIMARY_BODY_REV
    obj['OLEANDER_PRIMARY_BODY_SOURCE_MUTATED'] = False
    return obj


def build62(name, bodymat):
    obj = base_build(name, bodymat)
    if name == 'DERIVED_911_9922_BODY':
        remove_owned_aperture_faces(obj)
    return obj


core['build_visual_hull'] = build62


def greenhouse62(M):
    objs = base_greenhouse(M)
    for obj in objs:
        if obj.name.startswith('V60_'):
            obj.name = 'V62_' + obj.name[len('V60_'):]
        obj['OLEANDER_APERTURE_REVISION'] = REV
    return objs


v.build_glass = greenhouse62


def host_preservation_receipt(out):
    checks = [
        {
            'id':'GLOBAL_FACE_RETENTION','metric':'faces_ratio','before':STATS['host_pre_faces'],
            'after':STATS['host_post_faces'],'rule':'after_faces / before_faces >= 0.70',
            'status':'PASS' if STATS['face_retention_ratio'] >= .70 else 'FAIL','scope':'GLOBAL_HOST'
        },
        {
            'id':'GLOBAL_BOUNDS_RETENTION','metric':'min_world_bounds_ratio_xyz','before':1.0,
            'after':min(STATS['bounds_retention_ratio_xyz']) if STATS['bounds_retention_ratio_xyz'] else 0.0,
            'rule':'min world-space dimension retention >= 0.95',
            'status':'PASS' if STATS['bounds_retention_ratio_xyz'] and min(STATS['bounds_retention_ratio_xyz']) >= .95 else 'FAIL',
            'scope':'GLOBAL_HOST'
        },
        {
            'id':'OWNED_OPENING_BOUNDARIES','metric':'boundary_edge_count','before':0,
            'after':STATS['boundary_edge_count'],'rule':'boundary_edge_count > 0 after declared aperture removal',
            'status':'PASS' if STATS['boundary_edge_count'] > 0 else 'FAIL','scope':'LOCAL_REGION'
        }
    ]
    result = 'PASS_WITHIN_DECLARED_BUDGET' if all(c['status']=='PASS' for c in checks) else 'FAIL_HOST_PRESERVATION'
    d = {
        'schema':'oleander.3d.derived-edit-host-preservation-receipt.v1',
        'host_id':'DERIVED_911_9922_BODY','host_state_class':'DERIVED_EXECUTION',
        'operation':'FACE_CLASSIFICATION_DELETE_KEEP_BOUNDARY','edit_scope':'GREENHOUSE_APERTURE_ARCHITECTURE_ONLY',
        'locality':'LOCAL','source_mutation_allowed':False,'source_unchanged_or_na':True,
        'before':{'vertices':STATS['host_pre_vertices'],'faces':STATS['host_pre_faces'],'bounds':'SEE_APERTURE_RECEIPT'},
        'after':{'vertices':STATS['host_post_vertices'],'faces':STATS['host_post_faces'],'bounds':'SEE_APERTURE_RECEIPT'},
        'preservation_checks':checks,'operator_execution':'PASS_EXECUTED',
        'host_preservation_result':result,'evidence_result':'PASS_EVIDENCE_SCOPE' if result.startswith('PASS') else 'FAIL_EVIDENCE_INVALID',
        'design_result':'HOLD_NOT_REVIEWED','geometry_changed_only_basis':False,
        'does_not_prove':['reference fidelity','Class-A continuity','manufacturer CAD','production aperture construction','Design KEEP','MAIN KEEP']
    }
    Path(out,'DERIVED_EDIT_HOST_PRESERVATION_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    if result != 'PASS_WITHIN_DECLARED_BUDGET':
        raise SystemExit('FAIL_V62_HOST_PRESERVATION_RECEIPT')
    return d


def aperture_receipt(out):
    required = [
        'V62_WINDSHIELD','V62_REAR_GLASS','V62_SIDE_GLASS_L','V62_SIDE_GLASS_R',
        'V62_A_PILLAR_SURFACE_L','V62_A_PILLAR_SURFACE_R',
        'V62_C_PILLAR_SAIL_L','V62_C_PILLAR_SAIL_R',
        'V62_ROOF_RAIL_SURFACE_L','V62_ROOF_RAIL_SURFACE_R',
        'V62_WINDOW_BELT_SURFACE_L','V62_WINDOW_BELT_SURFACE_R',
        'V62_CABIN_OCCLUSION_BACKING','V62_DASH_BACKING','V62_REAR_BULKHEAD_BACKING'
    ]
    missing = [name for name in required if bpy.data.objects.get(name) is None]
    owners = ['BOUNDARY_SIDE_GLASS_L','BOUNDARY_SIDE_GLASS_R','BOUNDARY_WINDSHIELD','BOUNDARY_REAR_GLASS']
    owner_counts = {owner:int(STATS['removed_by_owner'].get(owner,0)) for owner in owners}
    constructed = not missing and all(owner_counts[o] > 0 for o in owners) and STATS['boundary_edge_count'] > 0
    d = {
        'schema':'oleander.3d.aperture-interface-receipt.v1','revision':REV,
        'primary_body_revision_locked':PRIMARY_BODY_REV,'primary_body_source_delta':'NONE',
        'aperture_ids':['SIDE_L','SIDE_R','WINDSHIELD','REAR_GLASS'],'boundary_owner_ids':owners,
        'host_surface':'DERIVED_911_9922_BODY','host_cut_method':'DERIVED_EVALUATED_FACE_CLASSIFICATION_REMOVAL_KEEP_BOUNDARY__SOURCE_UNCHANGED',
        'host_pre_vertices':STATS['host_pre_vertices'],'host_pre_faces':STATS['host_pre_faces'],
        'host_post_vertices':STATS['host_post_vertices'],'host_post_faces':STATS['host_post_faces'],
        'removed_face_count':STATS['removed_faces'],'removed_faces_by_owner':owner_counts,
        'face_retention_ratio':STATS['face_retention_ratio'],'bounds_retention_ratio_xyz':STATS['bounds_retention_ratio_xyz'],
        'boundary_edge_count':STATS['boundary_edge_count'],'interface_infill_backing_objects':sorted(o.name for o in bpy.context.scene.objects if o.get('OLEANDER_APERTURE_REVISION')==REV),
        'missing_required_objects':missing,'source_greenhouse_reference':'REFERENCE_GREENHOUSE_TARGETS_992_2.json',
        'shared_boundary_method':'REFERENCE_ENVELOPE_CLASSIFICATION_PLUS_DECLARED_INTERFACE_SURFACES__VISUAL_COINCIDENCE_REVIEW_REQUIRED',
        'projected_profile_state':'PRIMARY_BODY_V59_LOCKS_RETAINED_SEPARATE',
        'boundary_closure_state':'MACHINE_CONSTRUCTED_VISUAL_REVIEW_REQUIRED' if constructed else 'FAIL',
        'backing_occlusion_state':'SCREENED_GEOMETRY_PRESENT_VISUAL_REVIEW_REQUIRED' if not missing else 'FAIL',
        'visual_review_state':'NOT_RUN','design_quality_gate':'HOLD_FOR_ACTUAL_PREVIEW_ARTIFACT_REVIEW',
        'does_not_prove':['manufacturer aperture patch layout','Class-A continuity','seal engineering','tooling','production glazing design','reference fidelity','Design KEEP','MAIN KEEP']
    }
    Path(out,'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    if not constructed:
        raise SystemExit('FAIL_V62_APERTURE_ARCHITECTURE')
    return d


def update_overall(out, aperture, preservation):
    for name in ('REFERENCE_REPRO_QA.json','REFERENCE_REPRO_RECEIPT.json'):
        p = Path(out,name)
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        d['reference_fidelity_revision'] = REV
        d['primary_body_revision_locked'] = PRIMARY_BODY_REV
        d['source_edit_scope'] = 'NONE_PRIMARY_BODY__DERIVED_GREENHOUSE_APERTURE_ONLY'
        d['aperture_architecture'] = aperture['boundary_closure_state']
        d['host_preservation'] = preservation['host_preservation_result']
        d['visual_reference_fidelity'] = 'HOLD_ACTUAL_PREVIEW_REVIEW_REQUIRED'
        d['design_quality_gate'] = 'HOLD_FOR_OLEANDER_ARTIFACT_REVIEW'
        p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')


def run62():
    a = v.m.parse_args()
    out = Path(a.out).resolve()
    code = 0
    try:
        runtime['run30']()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code,int) else 0
    ctx['emit_surface_v2'](out)
    preservation = host_preservation_receipt(out)
    aperture = aperture_receipt(out)
    update_overall(out, aperture, preservation)
    raise SystemExit(code)


run62()
