#!/usr/bin/env python3
"""OLEANDER Automotive v0.11 — R29A M8.1 Detail Density Upgrade.

Purpose:
- preserve the R29A Primary Source byte-for-byte at the geometric hash level;
- preserve M6 semantic routing and M7 secondary geometry;
- replace coarse wheel-detail presentation with higher-density linked detail families;
- derive body/glazing seam visualization from M6 region boundaries rather than inventing freehand panel lines.

All added dimensions are DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION. This is not automotive
engineering CAD, Class-A surfacing, tooling data, homologation evidence or production CMF.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import math
from collections import defaultdict
from pathlib import Path

import bpy


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


m8 = load('/tmp/revise_v011_r29a_m8.py', 'm8_for_m81')
m8.WHEEL_RADIUS = m8.TARGET_OD * .5
m7 = m8.m7
m6 = m8.m6
r29a = m8.r29a
r20 = m8.r20
r16 = m8.r16
r14 = m8.r14
b = m8.b
hp = m8.hp

MODEL = 'OLEANDER_Automotive_Proportion_Section_Rebuild_v0.11_R29A_M8_1_DETAIL_DENSITY'
CANONICAL_SOURCE_HASH = 'd19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb'
TARGET_OD = .700
WHEEL_RADIUS = TARGET_OD * .5
DETAIL_FACE_OFFSET = .079
SPOKES_PER_WHEEL = 10
LUGS_PER_WHEEL = 5
RIM_MAJOR = .245
RIM_MINOR = .008
DISC_RADIUS = .145
DISC_DEPTH = .012
HUB_RADIUS = .047
HUB_DEPTH = .018
LUG_ORBIT = .031
LUG_RADIUS = .006
LUG_DEPTH = .012
SEAM_DEPTH = .0025

for mod in (m8, m7, m6, r29a, m8.m7.m6.r25, m6.r24, r20, m6.r18, r16, r16.r15,
            r14, r14.r12, r14.r11, r14.r10, r14.r09, r14.r08, r14.r08.r, b):
    mod.MODEL = MODEL
hp.install(b, TARGET_OD)


def mesh_signature(o):
    h = hashlib.sha256()
    for v in o.data.vertices:
        h.update(f'{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};'.encode())
    for p in o.data.polygons:
        h.update(('F' + ','.join(map(str, p.vertices)) + ';').encode())
    return h.hexdigest()


def source_topology(o):
    tri = quad = ngon = 0
    for p in o.data.polygons:
        n = len(p.vertices)
        if n == 3:
            tri += 1
        elif n == 4:
            quad += 1
        else:
            ngon += 1
    return {
        'vertices': len(o.data.vertices),
        'edges': len(o.data.edges),
        'faces': len(o.data.polygons),
        'tri': tri,
        'quad': quad,
        'ngon': ngon,
    }


def bevel_apply(o, width, segments=3):
    bpy.context.view_layer.objects.active = o
    o.select_set(True)
    mod = o.modifiers.new('M8_1_DETAIL_BEVEL', 'BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    bpy.ops.object.modifier_apply(modifier=mod.name)
    o.select_set(False)


def make_tapered_spoke(material):
    r0, r1 = .112, .276
    y0, y1 = -.010, .010
    w0, w1 = .020, .012
    verts = [
        (r0, y0, -w0), (r1, y0, -w1), (r1, y0, w1), (r0, y0, w0),
        (r0, y1, -w0), (r1, y1, -w1), (r1, y1, w1), (r0, y1, w0),
    ]
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    me = bpy.data.meshes.new('PROTO_M8_1_TAPERED_SPOKE_MESH')
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new('PROTO-M8_1-TAPERED-SPOKE', me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    bevel_apply(o, .004, 3)
    o.hide_render = True
    o['OLEANDER_AUTHORITY'] = 'DETAIL_PROTOTYPE_LIBRARY'
    o['OLEANDER_STAGE'] = 'M8.1'
    o['OLEANDER_PARAMETER_STATUS'] = 'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o


def make_torus_proto(name, major, minor, material, major_segments=96, minor_segments=12):
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=major_segments,
        minor_segments=minor_segments,
        location=(0,0,0),
        rotation=(math.pi/2,0,0),
    )
    o = bpy.context.object
    o.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    o.data.name = name.replace('-', '_') + '_MESH'
    o.data.materials.append(material)
    o.hide_render = True
    o['OLEANDER_AUTHORITY'] = 'DETAIL_PROTOTYPE_LIBRARY'
    o['OLEANDER_STAGE'] = 'M8.1'
    o['OLEANDER_PARAMETER_STATUS'] = 'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o


def make_cylinder_proto(name, radius, depth, material, vertices=64, bevel=.0015):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=(0,0,0), rotation=(math.pi/2,0,0))
    o = bpy.context.object
    o.name = name
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    o.data.name = name.replace('-', '_') + '_MESH'
    o.data.materials.append(material)
    if bevel:
        bevel_apply(o, bevel, 2)
    o.hide_render = True
    o['OLEANDER_AUTHORITY'] = 'DETAIL_PROTOTYPE_LIBRARY'
    o['OLEANDER_STAGE'] = 'M8.1'
    o['OLEANDER_PARAMETER_STATUS'] = 'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o


def make_caliper_proto(material):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
    o = bpy.context.object
    o.name = 'PROTO-M8_1-BRAKE-CALIPER'
    o.scale = (.030, .017, .075)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.name = 'PROTO_M8_1_BRAKE_CALIPER_MESH'
    o.data.materials.append(material)
    bevel_apply(o, .007, 4)
    o.hide_render = True
    o['OLEANDER_AUTHORITY'] = 'DETAIL_PROTOTYPE_LIBRARY'
    o['OLEANDER_STAGE'] = 'M8.1'
    o['OLEANDER_PARAMETER_STATUS'] = 'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o


def instance_linked(name, proto, location, rotation=(0,0,0), props=None):
    o = bpy.data.objects.new(name, proto.data)
    bpy.context.collection.objects.link(o)
    o.location = location
    o.rotation_euler = rotation
    o['OLEANDER_AUTHORITY'] = 'DETAIL_INSTANCE'
    o['OLEANDER_STAGE'] = 'M8.1'
    o['OLEANDER_PROTOTYPE'] = proto.name
    if props:
        for k, v in props.items():
            o[k] = v
    return o


def build_semantic_seams(source, assignments, material):
    edge_regions = defaultdict(set)
    for p, region in zip(source.data.polygons, assignments):
        verts = list(p.vertices)
        for i, a in enumerate(verts):
            bvi = verts[(i+1) % len(verts)]
            edge_regions[tuple(sorted((a, bvi)))].add(region)

    allowed = {
        frozenset(('REG-GLASSHOUSE','REG-FRONT-FENDER-L')),
        frozenset(('REG-GLASSHOUSE','REG-FRONT-FENDER-R')),
        frozenset(('REG-GLASSHOUSE','REG-REAR-QUARTER-L')),
        frozenset(('REG-GLASSHOUSE','REG-REAR-QUARTER-R')),
        frozenset(('REG-GLASSHOUSE','REG-BODY-MAIN-L')),
        frozenset(('REG-GLASSHOUSE','REG-BODY-MAIN-R')),
        frozenset(('REG-FRONT-FENDER-L','REG-BODY-MAIN-L')),
        frozenset(('REG-FRONT-FENDER-R','REG-BODY-MAIN-R')),
        frozenset(('REG-REAR-QUARTER-L','REG-BODY-MAIN-L')),
        frozenset(('REG-REAR-QUARTER-R','REG-BODY-MAIN-R')),
        frozenset(('REG-FRONT-TERMINATION','REG-FRONT-FENDER-L')),
        frozenset(('REG-FRONT-TERMINATION','REG-FRONT-FENDER-R')),
        frozenset(('REG-REAR-TERMINATION','REG-REAR-QUARTER-L')),
        frozenset(('REG-REAR-TERMINATION','REG-REAR-QUARTER-R')),
    }

    cu = bpy.data.curves.new('M8_1_SEMANTIC_SEAM_CURVES', 'CURVE')
    cu.dimensions = '3D'
    cu.resolution_u = 1
    cu.bevel_depth = SEAM_DEPTH
    cu.bevel_resolution = 2
    selected = []
    for edge, regions in sorted(edge_regions.items()):
        if len(regions) != 2 or frozenset(regions) not in allowed:
            continue
        a, bvi = edge
        spline = cu.splines.new('POLY')
        spline.points.add(1)
        va = source.data.vertices[a].co
        vb = source.data.vertices[bvi].co
        spline.points[0].co = (va.x, va.y, va.z, 1)
        spline.points[1].co = (vb.x, vb.y, vb.z, 1)
        selected.append({'edge':[a,bvi],'regions':sorted(regions)})
    o = bpy.data.objects.new('DET-M8_1-SEMANTIC-REGION-SEAMS', cu)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    o['OLEANDER_AUTHORITY'] = 'DERIVED_DETAIL_NOT_SOURCE'
    o['OLEANDER_STAGE'] = 'M8.1'
    o['OLEANDER_DERIVATION'] = 'M6_REGION_BOUNDARY_EDGES'
    o['OLEANDER_PARAMETER_STATUS'] = 'DESIGNER_ESTIMATE_FOR_MODELING_VALIDATION'
    return o, selected


def build_detail_families(wheel_records, materials, source, assignments):
    spoke_proto = make_tapered_spoke(materials['metal'])
    rim_proto = make_torus_proto('PROTO-M8_1-HIRES-RIM', RIM_MAJOR, RIM_MINOR, materials['metal'])
    disc_proto = make_cylinder_proto('PROTO-M8_1-BRAKE-DISC', DISC_RADIUS, DISC_DEPTH, materials['disc'], 96, .001)
    hub_proto = make_cylinder_proto('PROTO-M8_1-CENTER-HUB', HUB_RADIUS, HUB_DEPTH, materials['metal'], 64, .002)
    lug_proto = make_cylinder_proto('PROTO-M8_1-LUG', LUG_RADIUS, LUG_DEPTH, materials['dark'], 24, .0008)
    caliper_proto = make_caliper_proto(materials['caliper'])
    prototypes = [spoke_proto, rim_proto, disc_proto, hub_proto, lug_proto, caliper_proto]

    instances = []
    manifest = []
    by_code = {r['wheel_code']: r for r in wheel_records}
    for code in ('FL','FR','RL','RR'):
        rec = by_code[code]
        cx, cy, cz = rec['target_center']
        side = 1 if code.endswith('L') else -1
        face_y = cy + side * DETAIL_FACE_OFFSET
        inner_y = cy + side * (DETAIL_FACE_OFFSET - .016)
        props = {'OLEANDER_PACKAGE_DEPENDENCY': m8.PACKAGE_IDS[code], 'OLEANDER_CONTRACT_DEPENDENCY':'CONTRACT-WHEEL-HP'}

        for i in range(SPOKES_PER_WHEEL):
            angle = 2 * math.pi * i / SPOKES_PER_WHEEL
            o = instance_linked(f'DET-M8_1-SPOKE-{code}-{i:02d}', spoke_proto, (cx,face_y,cz), (0,angle,0), props)
            instances.append(o)
            manifest.append({'id':o.name,'family':'M8_1_TAPERED_SPOKES','wheel':code,'prototype':spoke_proto.name})

        for fam, proto, y in (
            ('M8_1_HIRES_RIM', rim_proto, face_y),
            ('M8_1_BRAKE_DISC', disc_proto, inner_y),
            ('M8_1_CENTER_HUB', hub_proto, face_y + side*.004),
        ):
            o = instance_linked(f'DET-{fam}-{code}', proto, (cx,y,cz), (0,0,0), props)
            instances.append(o)
            manifest.append({'id':o.name,'family':fam,'wheel':code,'prototype':proto.name})

        for i in range(LUGS_PER_WHEEL):
            a = 2 * math.pi * i / LUGS_PER_WHEEL
            x = cx + LUG_ORBIT * math.cos(a)
            z = cz + LUG_ORBIT * math.sin(a)
            o = instance_linked(f'DET-M8_1-LUG-{code}-{i:02d}', lug_proto, (x,face_y + side*.009,z), (0,0,0), props)
            instances.append(o)
            manifest.append({'id':o.name,'family':'M8_1_LUGS','wheel':code,'prototype':lug_proto.name})

        # Caliper is a generic benchmark detail. Place consistently near the rearward-upper quadrant.
        cal_x = cx - .105
        cal_z = cz + .075
        o = instance_linked(f'DET-M8_1-CALIPER-{code}', caliper_proto, (cal_x,inner_y - side*.004,cal_z), (0,0,0), props)
        instances.append(o)
        manifest.append({'id':o.name,'family':'M8_1_BRAKE_CALIPER','wheel':code,'prototype':caliper_proto.name})

    seam_obj, seam_edges = build_semantic_seams(source, assignments, materials['seam'])
    return prototypes, instances, manifest, seam_obj, seam_edges


def render_views(out, samples, res, M, source, body_context, wheelhouses, glazing, instances, seam_obj):
    b.ground(M)
    L = b.rigs()
    b.world((.010,.010,.010), .17)
    source.hide_render = True
    rd = out / 'renders'
    rd.mkdir(parents=True, exist_ok=True)
    wheels = [o for o in bpy.context.scene.objects if o.type == 'MESH' and o.name.startswith('WHEEL_')]
    views = [
        ('M8_1_HERO_FRONT_DETAIL',(6.2,-7.0,2.70),(.05,0,.66),82,False,5.0,'BROAD','ALL'),
        ('M8_1_HERO_REAR_DETAIL',(-6.0,6.8,2.60),(-.10,0,.66),82,False,5.0,'BROAD','ALL'),
        ('M8_1_FRONT_WHEEL_MACRO',(2.40,-3.0,.82),(b.FX,-b.WY,.48),110,False,4.4,'STRIP','FR'),
        ('M8_1_REAR_WHEEL_MACRO',(-2.35,-3.0,.82),(b.RX,-b.WY,.48),110,False,4.4,'STRIP','RR'),
        ('M8_1_SIDE_DETAIL',(0,-8.8,1.14),(0,0,.64),90,True,5.25,'BROAD','ALL'),
        ('M8_1_SEAM_GRAZING',(5.8,-6.8,2.35),(.0,0,.78),88,False,5.0,'GRAZING','ALL'),
    ]
    records = []
    for label, loc, target, lens, ortho, scale, rig, scope in views:
        b.setrig(L, rig)
        for w in wheels:
            w.hide_render = (scope != 'ALL' and scope not in w.name)
        for wh in wheelhouses:
            wh.hide_render = (scope != 'ALL' and not wh.name.endswith(scope))
        for o in instances:
            o.hide_render = (scope != 'ALL' and f'-{scope}-' not in o.name and not o.name.endswith('-'+scope))
        glazing.hide_render = False
        body_context.hide_render = False
        seam_obj.hide_render = False
        cam = b.camera('CAM_'+label, loc, target, lens, ortho, scale)
        bpy.context.scene.camera = cam
        p = rd / f'{MODEL}__{label}.png'
        b.setup(p, samples, res)
        bpy.ops.render.render(write_still=True)
        records.append({'view':label,'file':str(p),'scope':scope,'authority':'DIAGNOSTIC_OR_PRESENTATION_ONLY'})
        bpy.data.objects.remove(cam, do_unlink=True)
    source.hide_render = False
    for o in instances:
        o.hide_render = False
    for wh in wheelhouses:
        wh.hide_render = False
    for w in wheels:
        w.hide_render = False
    return records


def main():
    a = b.parse()
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    b.clear()
    M = b.materials()
    glass = r14.diagnostic_glass()
    rows = b.controls_resampled()

    source, xs, cols, arch_meta, reuse = r29a.build_source_r29a(rows, M, glass)
    source.name = 'PRIMARY_R29A_M8_1_LOCKED_SOURCE'
    source_hash_before = r20.shape_hash(source)
    source_topology_before = source_topology(source)

    assignments, region_counts = m6.classify_regions(source)
    m6.add_region_attribute(source, assignments)
    source.data.update()
    bpy.context.view_layer.update()

    b.wheels(M)
    wheel_records = getattr(b, '_OLEANDER_WHEEL_HP_RECORDS', [])
    wheel_exact = bool(getattr(b, '_OLEANDER_WHEEL_HP_EXACT', False)) and hp.package_exact(wheel_records, TARGET_OD)
    by_code = {r['wheel_code']: r for r in wheel_records}

    mat_wh = b.mat('M8_1_WHEELHOUSE',(.10,.18,.23,1),.48)
    mat_glass = b.mat('M8_1_GLAZING',(.025,.10,.15,1),.16)
    mat_body = b.mat('M8_1_BODY',(.28,.29,.31,1),.46)
    materials = {
        'metal': b.mat('M8_1_WHEEL_METAL',(.24,.25,.27,1),.20),
        'disc': b.mat('M8_1_BRAKE_DISC',(.14,.15,.16,1),.30),
        'dark': b.mat('M8_1_DARK_HARDWARE',(.025,.028,.032,1),.26),
        'caliper': b.mat('M8_1_CALIPER',(.40,.12,.055,1),.24),
        'seam': b.mat('M8_1_SEAM',(.012,.014,.016,1),.30),
    }

    wheelhouses = []
    for code, side in (('FL',1),('FR',-1),('RL',1),('RR',-1)):
        o, _ = m7.make_wheelhouse('SEC-WHEELHOUSE-'+code, by_code[code]['target_center'], side, mat_wh)
        wheelhouses.append(o)
    glazing, _ = m7.extract_glazing_shell(source, assignments, mat_glass)
    secondary = wheelhouses + [glazing]
    secondary_before = {o.name: mesh_signature(o) for o in secondary}
    body_context = m7.make_context_body(source, mat_body)

    prototypes, instances, instance_manifest, seam_obj, seam_edges = build_detail_families(wheel_records, materials, source, assignments)

    source_hash_after_details = r20.shape_hash(source)
    source_topology_after_details = source_topology(source)
    secondary_after_details = {o.name: mesh_signature(o) for o in secondary}

    render_samples = max(8, min(a.samples, 16))
    render_res = max(768, min(a.resolution, 1080))
    renders = render_views(out, render_samples, render_res, M, source, body_context, wheelhouses, glazing, instances, seam_obj)

    source_hash_after_render = r20.shape_hash(source)
    secondary_after_render = {o.name: mesh_signature(o) for o in secondary}

    linked_family_checks = {
        'spokes_single_mesh': len({o.data.name for o in instances if 'SPOKE-' in o.name}) == 1,
        'lug_single_mesh': len({o.data.name for o in instances if 'LUG-' in o.name}) == 1,
        'rim_single_mesh': len({o.data.name for o in instances if 'HIRES_RIM-' in o.name}) == 1,
        'disc_single_mesh': len({o.data.name for o in instances if 'BRAKE_DISC-' in o.name}) == 1,
        'hub_single_mesh': len({o.data.name for o in instances if 'CENTER_HUB-' in o.name}) == 1,
        'caliper_single_mesh': len({o.data.name for o in instances if 'CALIPER-' in o.name}) == 1,
    }

    expected_instances = 4 * (SPOKES_PER_WHEEL + LUGS_PER_WHEEL + 4)
    checks = {
        'canonical_source_hash_before': source_hash_before == CANONICAL_SOURCE_HASH,
        'source_hash_stable_after_details': source_hash_after_details == source_hash_before,
        'source_hash_stable_after_render': source_hash_after_render == source_hash_before,
        'source_topology_stable': source_topology_before == source_topology_after_details,
        'source_ngon_zero': source_topology_after_details['ngon'] == 0,
        'm6_region_assignments_retained': region_counts == m7.EXPECTED_REGION_COUNTS,
        'm7_secondary_signatures_stable': secondary_before == secondary_after_details == secondary_after_render,
        'wheel_hp_package_exact': wheel_exact and len(wheel_records) == 4,
        'detail_prototype_count_six': len(prototypes) == 6,
        'detail_instance_count_expected': len(instances) == expected_instances,
        'semantic_seams_derived_not_empty': len(seam_edges) > 0,
        'semantic_seam_role_non_source': seam_obj.get('OLEANDER_AUTHORITY') == 'DERIVED_DETAIL_NOT_SOURCE',
        'all_detail_instances_non_source': all(o.get('OLEANDER_AUTHORITY') == 'DETAIL_INSTANCE' for o in instances),
        'linked_detail_families': all(linked_family_checks.values()),
        'render_matrix_six': len(renders) == 6,
        'render_resolution_high': render_res >= 768,
        'render_samples_high': render_samples >= 8,
    }
    status = 'MACHINE_PASS_HUMAN_DETAIL_REVIEW_REQUIRED' if all(checks.values()) else 'MACHINE_FAIL'

    qa = {
        'schema':'oleander.auto.v0.11.r29a.m8.1.detail-density.qa.v1',
        'model':MODEL,
        'stage':'M8.1',
        'status':status,
        'source_hash_before':source_hash_before,
        'source_hash_after_details':source_hash_after_details,
        'source_hash_after_render':source_hash_after_render,
        'source_topology':source_topology_before,
        'm6_region_counts':region_counts,
        'm7_secondary_signatures':secondary_before,
        'wheel_hp_package':wheel_records,
        'detail_prototypes':[o.name for o in prototypes],
        'detail_instance_count':len(instances),
        'detail_instance_manifest':instance_manifest,
        'semantic_seam_edge_count':len(seam_edges),
        'semantic_seam_edges':seam_edges,
        'linked_family_checks':linked_family_checks,
        'render_samples':render_samples,
        'render_resolution':[render_res,render_res],
        'renders':renders,
        'checks':checks,
        'boundary':'M8.1 adds derived detail density only. R29A Primary Source, wheel hard points, M6 routing and M7 secondary geometry remain locked. Added wheel hardware and seam widths are designer estimates for modeling validation, not engineering or production specifications.'
    }
    (out/'M8_1_DETAIL_DENSITY_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')

    receipt = {
        'schema':'oleander.auto.v0.11.r29a.m8.1.detail-density.receipt.v1',
        'model':MODEL,
        'blender_version':bpy.app.version_string,
        'renderer':'Cycles CPU',
        'status':'EXECUTED_'+status,
        'source_hash':source_hash_before,
        'source_authority_mutated':False,
        'secondary_geometry_mutated':False,
        'detail_family_count':6,
        'detail_instance_count':len(instances),
        'semantic_seam_edge_count':len(seam_edges),
        'renders':len(renders),
        'does_not_prove':'Detail-density Machine PASS does not prove professional automotive design quality, Class-A, engineering CAD, tooling, manufacturing, homologation or final CMF.'
    }
    (out/'M8_1_DETAIL_DENSITY_RECEIPT.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')

    blend = out / f'{MODEL}.blend'
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    raise SystemExit(0 if status == 'MACHINE_PASS_HUMAN_DETAIL_REVIEW_REQUIRED' else 5)


if __name__ == '__main__':
    main()
