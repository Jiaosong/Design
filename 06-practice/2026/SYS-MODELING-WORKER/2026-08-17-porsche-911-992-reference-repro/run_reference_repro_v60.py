#!/usr/bin/env python3
"""V60 — owned greenhouse aperture architecture on the locked V59 primary body.

Primary-body Source delta: NONE relative to V59.
Authorized edit family: GREENHOUSE_APERTURE_ARCHITECTURE_ONLY.

The V59 sparse hood/fender relation, V49 sparse Source density, rear primary form, official hard points,
axles and wheel/tyre package are frozen. V60 changes only Derived display/aperture execution:

  HOST_SURFACE -> OPENING_BOUNDARY -> INTERFACE_SURFACE -> INFILL -> BACKING_OR_VOID

Unlike V49/V59 proxy glazing, the rendered Derived body receives actual window/windshield/backlight
openings. The uncut V59 evaluated diagnostic carrier is preserved for primary-body surface evidence.

This is still a reference-reproduction benchmark. It does not prove Porsche CAD, manufacturer aperture
construction, Class-A surfacing, sealing/tooling, manufacturing feasibility, physical CMF, Design KEEP
or MAIN KEEP.
"""
from __future__ import annotations
import json
from pathlib import Path
import bpy

HERE = Path(__file__).resolve().parent
V59 = HERE / 'run_reference_repro_v59.py'
text = V59.read_text(encoding='utf-8')
marker = '\nrun59()\n'
if marker not in text:
    raise SystemExit('V59 run marker missing')
ctx = {'__file__': str(V59), '__name__': 'oleander_v60_aperture_ownership'}
exec(compile(text.split(marker, 1)[0], str(V59), 'exec'), ctx)

v = ctx['v']
core = ctx['core']
runtime = ctx['runtime']
G = ctx['ns']['G']
base_build = core['build_visual_hull']
REV = 'V60_GREENHOUSE_APERTURE_OWNERSHIP'
PRIMARY_BODY_REV = 'V59_SPARSE_FRONT_HOOD_FENDER_RELATION'

v.REF = '2025_992.2_CARRERA_APERTURE_OWNERSHIP_V60'
v.REFERENCE_CONTRACT['reference_revision'] = v.REF
v.REFERENCE_CONTRACT['candidate_revision'] = REV
v.REFERENCE_CONTRACT['primary_body_revision_locked'] = PRIMARY_BODY_REV
v.REFERENCE_CONTRACT['source_edit_scope'] = 'NONE_PRIMARY_BODY__DERIVED_GREENHOUSE_APERTURE_ONLY'
v.REFERENCE_CONTRACT['aperture_architecture_state'] = 'OWNED_OPENING_INTERFACE_INFILL_BACKING_EXPERIMENT'
v.REFERENCE_CONTRACT['aperture_protocols'] = [
    'reference-reproduction/APERTURE_BACKING_BOUNDARY_OWNERSHIP_PROTOCOL_v1.md',
    'reference-reproduction/APERTURE_INTERFACE_SURFACE_PROTOCOL_v1.md'
]
v.FAMILY_CONTROLS['GREENHOUSE_APERTURE_ARCHITECTURE_V60'] = {
    'tier': 'DERIVED_IDENTITY_CRITICAL_APERTURE',
    'reference': 'REFERENCE_GREENHOUSE_TARGETS_992_2.json',
    'host_surface': 'DERIVED_911_9922_BODY',
    'opening_boundary_owners': [
        'BOUNDARY_SIDE_GLASS_L', 'BOUNDARY_SIDE_GLASS_R',
        'BOUNDARY_WINDSHIELD', 'BOUNDARY_REAR_GLASS'
    ],
    'interface_surfaces': [
        'A_PILLAR', 'ROOF_RAIL', 'B_PILLAR', 'C_PILLAR_SAIL',
        'WINDOW_BELT', 'COWL', 'REAR_DECK'
    ],
    'backing': ['CABIN_OCCLUSION', 'DASH', 'REAR_BULKHEAD'],
    'protected': [
        PRIMARY_BODY_REV, 'V49_SOURCE_DENSITY', 'REAR_PRIMARY_BODY',
        'OFFICIAL_HARD_POINTS', 'AXLES', 'WHEEL_TYRE_PACKAGE'
    ],
    'forbidden': [
        'CAGE_DENSIFICATION', 'PRIMARY_BODY_REWRITE', 'REAR_PRIMARY_FORM_EDIT',
        'CAMERA_TUNING_TO_HIDE_APERTURE_DEFECTS', 'OPAQUE_GLASS_AS_BACKING_SUBSTITUTE'
    ]
}
v.REFERENCE_CONTRACT['source_families'] = list(v.FAMILY_CONTROLS.keys())

APERTURE_STATS = {
    'host_pre_vertices': None,
    'host_pre_faces': None,
    'host_post_vertices': None,
    'host_post_faces': None,
    'boolean_results': [],
}


def mesh_prism_xz(name, polygon_xz, y0, y1):
    n = len(polygon_xz)
    verts = [(float(x), float(y0), float(z)) for x, z in polygon_xz]
    verts += [(float(x), float(y1), float(z)) for x, z in polygon_xz]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
    for i in range(n):
        j = (i + 1) % n
        faces.append((i, j, n+j, n+i))
    me = bpy.data.meshes.new(name + '_MESH')
    me.from_pydata(verts, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    obj.hide_render = True
    obj['OLEANDER_AUTHORITY'] = 'DERIVED_BOOLEAN_TOOL_NOT_AUTHORITY'
    return obj


def apply_boolean(host, cutter, owner_id):
    before = (len(host.data.vertices), len(host.data.polygons))
    mod = host.modifiers.new('CUT_' + owner_id, 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    try:
        mod.solver = 'EXACT'
    except Exception:
        pass
    mod.object = cutter
    bpy.context.view_layer.objects.active = host
    host.select_set(True)
    cutter.select_set(False)
    ok = True
    err = None
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as exc:
        ok = False
        err = type(exc).__name__ + ':' + str(exc)
    after = (len(host.data.vertices), len(host.data.polygons))
    APERTURE_STATS['boolean_results'].append({
        'owner_id': owner_id,
        'before_vertices': before[0], 'before_faces': before[1],
        'after_vertices': after[0], 'after_faces': after[1],
        'applied': ok, 'error': err,
        'geometry_changed': before != after
    })
    if cutter.name in bpy.data.objects:
        bpy.data.objects.remove(cutter, do_unlink=True)
    if not ok or before == after:
        raise SystemExit('FAIL_APERTURE_BOOLEAN_' + owner_id)


def side_opening_polygon():
    top = [(float(x), float(zt)) for x, zt, _ in G]
    bottom = [(float(x), float(zb)) for x, _, zb in reversed(G)]
    return top + bottom


def build60(name, bodymat):
    obj = base_build(name, bodymat)
    if name != 'DERIVED_911_9922_BODY':
        return obj

    APERTURE_STATS['host_pre_vertices'] = len(obj.data.vertices)
    APERTURE_STATS['host_pre_faces'] = len(obj.data.polygons)

    # Canonical side-glass opening boundary comes directly from same-revision greenhouse targets.
    poly = side_opening_polygon()
    apply_boolean(obj, mesh_prism_xz('CUTTER_SIDE_L', poly, .30, 1.18), 'BOUNDARY_SIDE_GLASS_L')
    apply_boolean(obj, mesh_prism_xz('CUTTER_SIDE_R', poly, -1.18, -.30), 'BOUNDARY_SIDE_GLASS_R')

    # Windshield/backlight boundaries are explicit canonical XZ definitions. Interface surfaces and
    # glass below consume the same coordinates rather than independently guessed endpoints.
    ws_xz = [(.625, .845), (.245, 1.220), (.185, 1.255), (.710, .775)]
    rg_xz = [(-.405, 1.220), (-1.145, .970), (-1.255, .900), (-.330, 1.255)]
    apply_boolean(obj, mesh_prism_xz('CUTTER_WINDSHIELD', ws_xz, -.66, .66), 'BOUNDARY_WINDSHIELD')
    apply_boolean(obj, mesh_prism_xz('CUTTER_REAR_GLASS', rg_xz, -.65, .65), 'BOUNDARY_REAR_GLASS')

    APERTURE_STATS['host_post_vertices'] = len(obj.data.vertices)
    APERTURE_STATS['host_post_faces'] = len(obj.data.polygons)
    obj['OLEANDER_APERTURE_ARCHITECTURE'] = REV
    obj['OLEANDER_PRIMARY_BODY_SOURCE_REVISION'] = PRIMARY_BODY_REV
    obj['OLEANDER_APERTURE_CUTS_APPLIED'] = 4
    obj['OLEANDER_PRIMARY_BODY_SOURCE_MUTATED'] = False
    return obj


core['build_visual_hull'] = build60


def gy60(x, z):
    w = core['plan_half_width'](x)
    raw = .5 * v.WIDTH * core['profile_ratio'](x, z)
    return min(w - .020, max(.40, raw - .030))


def add_panel(name, verts, mat, thickness=.006, authority='DERIVED_REFERENCE_REPRO_INTERFACE'):
    me = bpy.data.meshes.new(name + '_MESH')
    me.from_pydata([tuple(map(float, p)) for p in verts], [], [tuple(range(len(verts)))])
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY'] = authority
    o['OLEANDER_APERTURE_REVISION'] = REV
    if thickness:
        s = o.modifiers.new(name + '_THICKNESS', 'SOLIDIFY')
        s.thickness = thickness
        s.offset = 0
    for p in me.polygons:
        p.use_smooth = True
    return o


def add_strip(name, sections, mat, thickness=.006, authority='DERIVED_REFERENCE_REPRO_INTERFACE'):
    verts = []
    for outer, inner in sections:
        verts.extend((outer, inner))
    faces = [(2*i, 2*i+1, 2*i+3, 2*i+2) for i in range(len(sections)-1)]
    me = bpy.data.meshes.new(name + '_MESH')
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY'] = authority
    o['OLEANDER_APERTURE_REVISION'] = REV
    if thickness:
        s = o.modifiers.new(name + '_THICKNESS', 'SOLIDIFY')
        s.thickness = thickness
        s.offset = 0
    for p in me.polygons:
        p.use_smooth = True
    return o


def side_glass_strip(name, side, mat):
    verts = []
    for x, zt, zb in G:
        y = side * (gy60(x, (zt + zb) * .5) - .008)
        verts.extend([(x, y, zt), (x, y, zb)])
    faces = [(2*i, 2*i+1, 2*i+3, 2*i+2) for i in range(len(G)-1)]
    me = bpy.data.meshes.new(name + '_MESH')
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(mat)
    o['OLEANDER_AUTHORITY'] = 'DERIVED_APERTURE_INFILL'
    o['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_SIDE_GLASS_' + ('L' if side > 0 else 'R')
    o['OLEANDER_APERTURE_REVISION'] = REV
    for p in me.polygons:
        p.use_smooth = True
    return o


def greenhouse60(M):
    out = []
    # Actual side glazing sits inside the cut host opening.
    out.append(side_glass_strip('V60_SIDE_GLASS_L', 1, M['glass']))
    out.append(side_glass_strip('V60_SIDE_GLASS_R', -1, M['glass']))

    ws = [(.625, .565, .845), (.625, -.565, .845), (.245, -.500, 1.220), (.245, .500, 1.220)]
    rg = [(-.405, .455, 1.220), (-.405, -.455, 1.220), (-1.145, -.535, .970), (-1.145, .535, .970)]
    wso = add_panel('V60_WINDSHIELD', ws, M['glass'], .002, 'DERIVED_APERTURE_INFILL')
    wso['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_WINDSHIELD'; out.append(wso)
    rgo = add_panel('V60_REAR_GLASS', rg, M['glass'], .002, 'DERIVED_APERTURE_INFILL')
    rgo['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_REAR_GLASS'; out.append(rgo)

    # Surface-width interface system. All strips consume the same G envelope or windshield/backlight endpoints.
    for side, label in ((1, 'L'), (-1, 'R')):
        roof_sections = []
        belt_sections = []
        for x, zt, zb in G:
            yi = side * (gy60(x, (zt + zb) * .5) - .002)
            yo = side * (abs(yi) + .055)
            roof_sections.append(((x, yo, zt + .025), (x, yi, zt)))
            belt_sections.append(((x, yo, zb - .018), (x, yi, zb)))
        rr = add_strip('V60_ROOF_RAIL_SURFACE_' + label, roof_sections, M['body'], .008)
        rr['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_SIDE_GLASS_' + label; out.append(rr)
        belt = add_strip('V60_WINDOW_BELT_SURFACE_' + label, belt_sections, M['body'], .008)
        belt['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_SIDE_GLASS_' + label; out.append(belt)

        # B-pillar interrupts the continuous opening as a real surface, not a curve/tube.
        bx = -.225
        btop = ctx['ns']['interpG'](bx, 1)
        bbot = ctx['ns']['interpG'](bx, 2)
        by = side * (gy60(bx, (btop + bbot) * .5) - .004)
        bp = add_panel('V60_B_PILLAR_SURFACE_' + label, [
            (bx-.032, by, bbot-.012), (bx+.032, by, bbot-.012),
            (bx+.032, by, btop+.012), (bx-.032, by, btop+.012)
        ], M['body_dark'], .010)
        bp['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_SIDE_GLASS_' + label; out.append(bp)

        # A-pillar and C-pillar/sail bridge the side opening to windshield/backlight headers.
        sx, szt, szb = G[-1]
        sy = side * (gy60(sx, szt) - .002)
        ap = add_panel('V60_A_PILLAR_SURFACE_' + label, [
            (sx, sy + side*.050, szb-.012), (sx, sy, szb),
            (.245, side*.500, 1.220), (.205, side*.555, 1.245)
        ], M['body'], .010)
        ap['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_WINDSHIELD|BOUNDARY_SIDE_GLASS_' + label; out.append(ap)

        rx, rzt, rzb = G[0]
        ry = side * (gy60(rx, (rzt+rzb)*.5) - .002)
        cp = add_panel('V60_C_PILLAR_SAIL_' + label, [
            (rx, ry, rzt), (rx, ry + side*.070, rzb-.018),
            (-1.245, side*.680, .900), (-1.145, side*.535, .970),
            (-.405, side*.455, 1.220), (-.350, side*.520, 1.245)
        ], M['body'], .012)
        cp['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_REAR_GLASS|BOUNDARY_SIDE_GLASS_' + label; out.append(cp)

    cowl = add_panel('V60_COWL_INTERFACE', [
        (.710,.650,.775),(.710,-.650,.775),(.625,-.565,.845),(.625,.565,.845)
    ], M['body'], .010)
    cowl['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_WINDSHIELD'; out.append(cowl)
    deck = add_panel('V60_REAR_DECK_INTERFACE', [
        (-1.145,.535,.970),(-1.145,-.535,.970),(-1.255,-.700,.900),(-1.255,.700,.900)
    ], M['body'], .012)
    deck['OLEANDER_BOUNDARY_OWNER'] = 'BOUNDARY_REAR_GLASS'; out.append(deck)

    # Spatially plausible dark backing: geometry, not opaque glass/compositor masking.
    for name, loc, scale in [
        ('V60_CABIN_OCCLUSION_BACKING', (-.18,0,.72), (1.20,.72,.20)),
        ('V60_DASH_BACKING', (.43,0,.70), (.28,.70,.12)),
        ('V60_REAR_BULKHEAD_BACKING', (-.88,0,.68), (.18,.68,.16)),
    ]:
        o = v.m.add_cube(name, loc, scale, M['body_dark'], .008)
        o['OLEANDER_AUTHORITY'] = 'DERIVED_EXECUTION_NOT_AUTHORITY'
        o['OLEANDER_APERTURE_ROLE'] = 'BACKING_OR_VOID'
        o['OLEANDER_APERTURE_REVISION'] = REV
        out.append(o)
    return out


v.build_glass = greenhouse60


def aperture_receipt(out):
    interface_names = sorted(o.name for o in bpy.context.scene.objects if o.get('OLEANDER_APERTURE_REVISION') == REV)
    cut_results = APERTURE_STATS['boolean_results']
    cuts_ok = len(cut_results) == 4 and all(x['applied'] and x['geometry_changed'] for x in cut_results)
    required_prefixes = [
        'V60_WINDSHIELD','V60_REAR_GLASS','V60_SIDE_GLASS_L','V60_SIDE_GLASS_R',
        'V60_A_PILLAR_SURFACE_L','V60_A_PILLAR_SURFACE_R',
        'V60_C_PILLAR_SAIL_L','V60_C_PILLAR_SAIL_R',
        'V60_ROOF_RAIL_SURFACE_L','V60_ROOF_RAIL_SURFACE_R',
        'V60_WINDOW_BELT_SURFACE_L','V60_WINDOW_BELT_SURFACE_R',
        'V60_CABIN_OCCLUSION_BACKING','V60_DASH_BACKING','V60_REAR_BULKHEAD_BACKING'
    ]
    missing = [n for n in required_prefixes if bpy.data.objects.get(n) is None]
    d = {
        'schema': 'oleander.3d.aperture-interface-receipt.v1',
        'revision': REV,
        'primary_body_revision_locked': PRIMARY_BODY_REV,
        'primary_body_source_delta': 'NONE',
        'aperture_ids': ['SIDE_L','SIDE_R','WINDSHIELD','REAR_GLASS'],
        'boundary_owner_ids': [
            'BOUNDARY_SIDE_GLASS_L','BOUNDARY_SIDE_GLASS_R','BOUNDARY_WINDSHIELD','BOUNDARY_REAR_GLASS'
        ],
        'host_surface': 'DERIVED_911_9922_BODY',
        'host_cut_method': 'DERIVED_DISPLAY_BOOLEAN_DIFFERENCE__SOURCE_UNCHANGED',
        'host_pre_vertices': APERTURE_STATS['host_pre_vertices'],
        'host_pre_faces': APERTURE_STATS['host_pre_faces'],
        'host_post_vertices': APERTURE_STATS['host_post_vertices'],
        'host_post_faces': APERTURE_STATS['host_post_faces'],
        'boolean_results': cut_results,
        'interface_infill_backing_objects': interface_names,
        'missing_required_objects': missing,
        'source_greenhouse_reference': 'REFERENCE_GREENHOUSE_TARGETS_992_2.json',
        'shared_boundary_method': 'CANONICAL_G_ENVELOPE_PLUS_DECLARED_WINDSHIELD_BACKLIGHT_BOUNDARY_COORDINATES',
        'projected_profile_state': 'PRIMARY_BODY_V59_LOCKS_RETAINED_SEPARATE',
        'boundary_closure_state': 'MACHINE_CONSTRUCTED_VISUAL_REVIEW_REQUIRED' if cuts_ok and not missing else 'FAIL',
        'backing_occlusion_state': 'SCREENED_GEOMETRY_PRESENT_VISUAL_REVIEW_REQUIRED' if not missing else 'FAIL',
        'visual_review_state': 'NOT_RUN',
        'design_quality_gate': 'HOLD_FOR_ACTUAL_PREVIEW_ARTIFACT_REVIEW',
        'does_not_prove': [
            'manufacturer aperture patch layout','Class-A continuity','seal engineering','tooling',
            'production glazing design','reference fidelity','Design KEEP','MAIN KEEP'
        ]
    }
    Path(out, 'APERTURE_INTERFACE_RECEIPT.json').write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')
    if d['boundary_closure_state'] == 'FAIL' or d['backing_occlusion_state'] == 'FAIL':
        raise SystemExit('FAIL_V60_APERTURE_ARCHITECTURE')
    return d


def update_overall_receipts(out, aperture):
    for name in ('REFERENCE_REPRO_QA.json', 'REFERENCE_REPRO_RECEIPT.json'):
        p = Path(out, name)
        if not p.exists():
            continue
        d = json.loads(p.read_text(encoding='utf-8'))
        d['reference_fidelity_revision'] = REV
        d['primary_body_revision_locked'] = PRIMARY_BODY_REV
        d['source_edit_scope'] = 'NONE_PRIMARY_BODY__DERIVED_GREENHOUSE_APERTURE_ONLY'
        d['aperture_architecture'] = aperture['boundary_closure_state']
        d['aperture_backing'] = aperture['backing_occlusion_state']
        d['visual_reference_fidelity'] = 'HOLD_ACTUAL_PREVIEW_REVIEW_REQUIRED'
        d['design_quality_gate'] = 'HOLD_FOR_OLEANDER_ARTIFACT_REVIEW'
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + '\n')


def run60():
    a = v.m.parse_args()
    out = Path(a.out).resolve()
    code = 0
    try:
        runtime['run30']()
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else 0
    # Preserve V59 primary-body v2 evidence; this is intentionally not reclassified as V60 Source geometry.
    ctx['emit_surface_v2'](out)
    aperture = aperture_receipt(out)
    update_overall_receipts(out, aperture)
    raise SystemExit(code)


run60()
