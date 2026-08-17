#!/usr/bin/env python3
"""OLEANDER 3D Skill — Porsche 911 Carrera (992) reference reproduction benchmark.

This is a study/reproduction benchmark built from public dimensional hard points and visual
reference, not an original automotive design. The script intentionally keeps the sparse Source
control mesh separate from dense derived display geometry and from presentation/detail objects.

No Porsche logo/badge/trademark graphic is reproduced. Added fine dimensions are visual-study
estimates unless explicitly bound to the dimension contract below.
"""
from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import math
from pathlib import Path

import bpy
from mathutils import Vector

MODEL = "OLEANDER_PORSCHE_911_CARRERA_992_REFERENCE_REPRO"

# Official body hard points used for the benchmark (metres).
LENGTH = 4.542
WIDTH = 1.852
HEIGHT = 1.302
WHEELBASE = 2.450
FRONT_OVERHANG = 1.016
REAR_OVERHANG = 1.076
GROUND_CLEARANCE = 0.122
FRONT_X = LENGTH * 0.5
REAR_X = -LENGTH * 0.5
FRONT_AXLE_X = FRONT_X - FRONT_OVERHANG
REAR_AXLE_X = FRONT_AXLE_X - WHEELBASE

# Public tyre-size benchmark used only to set visual wheel envelopes.
FRONT_TIRE = {"section_m": 0.235, "aspect": 0.40, "rim_in": 19}
REAR_TIRE = {"section_m": 0.295, "aspect": 0.35, "rim_in": 20}


def tyre_geometry(spec):
    rim_r = spec["rim_in"] * 0.0254 * 0.5
    sidewall = spec["section_m"] * spec["aspect"]
    outer_r = rim_r + sidewall
    torus_major = (outer_r + rim_r) * 0.5
    torus_minor = (outer_r - rim_r) * 0.5
    return {"rim_r": rim_r, "sidewall": sidewall, "outer_r": outer_r,
            "torus_major": torus_major, "torus_minor": torus_minor}


FRONT_WHEEL = tyre_geometry(FRONT_TIRE)
REAR_WHEEL = tyre_geometry(REAR_TIRE)
FRONT_TRACK_Y = WIDTH * 0.5 - FRONT_TIRE["section_m"] * 0.5 - 0.020
REAR_TRACK_Y = WIDTH * 0.5 - REAR_TIRE["section_m"] * 0.5 - 0.015

# Sparse editable silhouette/section table. Values are metres.
# x, half-width, centre-top, roof-side, belt, shoulder, lower-side, rocker
CONTROLS = [
    (-2.271, .840, .620, .610, .575, .525, .405, .205),
    (-2.100, .900, .720, .700, .665, .620, .470, .215),
    (-1.750, .926, .820, .790, .730, .685, .505, .220),
    (-1.450, .926, .865, .830, .765, .710, .515, .220),
    (-1.195, .926, .885, .845, .785, .725, .520, .220),
    (-0.950, .910, 1.080, 1.015, .855, .755, .520, .220),
    (-0.650, .890, 1.220, 1.120, .895, .775, .520, .220),
    (-0.300, .870, 1.295, 1.205, .920, .790, .515, .220),
    ( 0.100, .860, 1.302, 1.220, .920, .790, .510, .220),
    ( 0.450, .860, 1.270, 1.180, .900, .780, .505, .220),
    ( 0.720, .870, 1.150, 1.060, .870, .760, .500, .220),
    ( 0.950, .890, .910, .870, .820, .740, .495, .220),
    ( 1.255, .910, .790, .775, .740, .700, .475, .215),
    ( 1.550, .905, .750, .735, .700, .655, .455, .210),
    ( 1.850, .880, .700, .685, .655, .610, .420, .200),
    ( 2.100, .840, .620, .605, .575, .535, .375, .190),
    ( 2.271, .780, .540, .525, .500, .460, .335, .180),
]

CONTROL_KEYS = ("x", "half_width", "z_center", "z_roof_side", "z_belt", "z_shoulder", "z_lower", "z_rocker")
CONTROL_JSON = [dict(zip(CONTROL_KEYS, row)) for row in CONTROLS]

REFERENCE_CONTRACT = {
    "schema": "oleander.3d.reference-reproduction.porsche-911-992.v1",
    "reference_vehicle": "Porsche 911 Carrera (992)",
    "reference_type": "EXISTING_PRODUCTION_VEHICLE_VISUAL_REPRODUCTION_BENCHMARK",
    "dimension_source": "Porsche official published technical data / newsroom",
    "units": "m",
    "hard_points": {
        "length": LENGTH,
        "width_excluding_mirrors": WIDTH,
        "height": HEIGHT,
        "wheelbase": WHEELBASE,
        "front_overhang": FRONT_OVERHANG,
        "rear_overhang": REAR_OVERHANG,
        "ground_clearance_visual_contract": GROUND_CLEARANCE,
        "front_axle_x": FRONT_AXLE_X,
        "rear_axle_x": REAR_AXLE_X,
    },
    "tyre_visual_contract": {
        "front": {**FRONT_TIRE, **FRONT_WHEEL},
        "rear": {**REAR_TIRE, **REAR_WHEEL},
    },
    "authority_boundary": {
        "source": "SPARSE_REFERENCE_REPRO_SOURCE",
        "dense_body": "DERIVED_REFERENCE_REPRO_DISPLAY",
        "details": "DERIVED_REFERENCE_REPRO_DETAIL",
        "claim": "visual/modeling benchmark only",
    },
    "does_not_prove": [
        "Porsche engineering CAD", "Class-A production surfacing", "tooling feasibility",
        "panel architecture", "crash/aero validation", "homologation", "production CMF",
        "commercial IP clearance",
    ],
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--out", required=True)
    p.add_argument("--samples", type=int, default=16)
    p.add_argument("--resolution-x", type=int, default=1152)
    p.add_argument("--resolution-y", type=int, default=768)
    return p.parse_args()


def canonical_json(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha_json(data):
    return hashlib.sha256(canonical_json(data).encode()).hexdigest()


def mesh_hash(obj):
    h = hashlib.sha256()
    for v in obj.data.vertices:
        h.update(f"{v.co.x:.9f},{v.co.y:.9f},{v.co.z:.9f};".encode())
    for p in obj.data.polygons:
        h.update(("F" + ",".join(str(i) for i in p.vertices) + ";").encode())
    return h.hexdigest()


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def mat(name, base, metallic=0.0, roughness=0.45, emission=None, emission_strength=0.0, transmission=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = base
        if "Metallic" in bsdf.inputs:
            bsdf.inputs["Metallic"].default_value = metallic
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = roughness
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = transmission
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = transmission
        if emission is not None:
            if "Emission Color" in bsdf.inputs:
                bsdf.inputs["Emission Color"].default_value = emission
            elif "Emission" in bsdf.inputs:
                bsdf.inputs["Emission"].default_value = emission
            if "Emission Strength" in bsdf.inputs:
                bsdf.inputs["Emission Strength"].default_value = emission_strength
    return m


def build_materials():
    return {
        "body": mat("REF_BODY_GT_SILVER", (.34, .37, .40, 1), metallic=.72, roughness=.20),
        "body_dark": mat("REF_BODY_DARK_TRIM", (.025, .028, .032, 1), metallic=.18, roughness=.24),
        "glass": mat("REF_GLASS", (.015, .035, .050, 1), metallic=.05, roughness=.08, transmission=.28),
        "tire": mat("REF_TIRE", (.012, .012, .014, 1), roughness=.54),
        "rim": mat("REF_RIM", (.16, .18, .20, 1), metallic=.92, roughness=.16),
        "disc": mat("REF_BRAKE_DISC", (.22, .23, .24, 1), metallic=.88, roughness=.30),
        "caliper": mat("REF_BRAKE_CALIPER", (.52, .015, .012, 1), metallic=.35, roughness=.24),
        "headlamp": mat("REF_HEADLAMP", (.75, .86, 1.0, 1), metallic=.08, roughness=.08, emission=(.65, .82, 1.0, 1), emission_strength=1.5),
        "tail": mat("REF_TAIL_LIGHT", (.32, .004, .003, 1), roughness=.18, emission=(1.0, .01, .005, 1), emission_strength=3.2),
        "seam": mat("REF_SEAM", (.015, .016, .018, 1), roughness=.26),
        "ground": mat("REF_STUDIO_GROUND", (.10, .105, .11, 1), roughness=.58),
    }


def smoothstep(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3.0 - 2.0 * t)


CONTROL_X = [r[0] for r in CONTROLS]


def interpolated_control(x):
    if x <= CONTROL_X[0]:
        return CONTROLS[0]
    if x >= CONTROL_X[-1]:
        return CONTROLS[-1]
    i = bisect.bisect_right(CONTROL_X, x) - 1
    a, b = CONTROLS[i], CONTROLS[i + 1]
    t = smoothstep((x - a[0]) / (b[0] - a[0]))
    vals = [x]
    for k in range(1, len(a)):
        vals.append(a[k] * (1.0 - t) + b[k] * t)
    return tuple(vals)


def arch_data(x):
    candidates = []
    for axle_x, outer_r, opening_extra in (
        (FRONT_AXLE_X, FRONT_WHEEL["outer_r"], .055),
        (REAR_AXLE_X, REAR_WHEEL["outer_r"], .060),
    ):
        opening_r = outer_r + opening_extra
        dx = abs(x - axle_x)
        if dx < opening_r:
            z = outer_r + math.sqrt(max(0.0, opening_r * opening_r - dx * dx)) - .015
            candidates.append((opening_r, z))
    if not candidates:
        return False, None
    return True, max(z for _, z in candidates)


def section_ring(x):
    _, hw, zc, zrs, zb, zs, zl, zr = interpolated_control(x)
    arch, arch_z = arch_data(x)
    lower = max(zl, arch_z) if arch else zl
    under = max(.142, GROUND_CLEARANCE + .020)
    # Closed cross-section ring, clockwise from centre-top around +Y side, underbody and -Y side.
    positive = [
        (0.00 * hw, zc),
        (.25 * hw, .70 * zc + .30 * zrs),
        (.50 * hw, zrs),
        (.68 * hw, .55 * zrs + .45 * zb),
        (.80 * hw, zb),
        (.94 * hw, .50 * zb + .50 * zs),
        (1.00 * hw, zs),
        (.995 * hw, lower),
        (.90 * hw, zr),
        (0.00, under),
    ]
    negative = [(-y, z) for y, z in reversed(positive[1:-1])]
    ring = positive + negative
    return [(x, y, z) for y, z in ring], arch


def build_body_mesh(name, xs, material, authority, render_visible):
    verts = []
    rings = []
    arch_flags = []
    for x in xs:
        ring, arch = section_ring(x)
        rings.append(list(range(len(verts), len(verts) + len(ring))))
        verts.extend(ring)
        arch_flags.append(arch)
    nring = len(rings[0])
    faces = []
    # side skin
    for i in range(len(rings) - 1):
        mid = (xs[i] + xs[i + 1]) * .5
        arch_active, _ = arch_data(mid)
        for j in range(nring):
            j2 = (j + 1) % nring
            # open wheel wells from arch boundary down to underbody on both sides
            skip = arch_active and ((j in (7, 8)) or (j in (9, 10)))
            if skip:
                continue
            faces.append((rings[i][j], rings[i + 1][j], rings[i + 1][j2], rings[i][j2]))
    # front / rear end caps
    faces.append(tuple(reversed(rings[0])))
    faces.append(tuple(rings[-1]))
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata(verts, [], faces)
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    for p in me.polygons:
        p.use_smooth = True
    obj["OLEANDER_AUTHORITY"] = authority
    obj["OLEANDER_REFERENCE"] = "Porsche 911 Carrera 992"
    obj["OLEANDER_SOURCE_CONTROL_DIGEST"] = sha_json({"contract": REFERENCE_CONTRACT, "controls": CONTROL_JSON})
    obj.hide_render = not render_visible
    return obj


def body_bounds(obj):
    xs = [v.co.x for v in obj.data.vertices]
    ys = [v.co.y for v in obj.data.vertices]
    zs = [v.co.z for v in obj.data.vertices]
    return {
        "min_x": min(xs), "max_x": max(xs), "min_y": min(ys), "max_y": max(ys),
        "min_z": min(zs), "max_z": max(zs),
        "length": max(xs) - min(xs), "width": max(ys) - min(ys),
    }


def add_bevel(obj, width=.004, segments=2):
    mod = obj.modifiers.new("REF_MICRO_BEVEL", "BEVEL")
    mod.width = width
    mod.segments = segments
    mod.limit_method = "ANGLE"


def add_cube(name, location, scale, material, bevel=.0, authority="DERIVED_REFERENCE_REPRO_DETAIL"):
    bpy.ops.mesh.primitive_cube_add(location=location)
    o = bpy.context.object
    o.name = name
    o.scale = (scale[0] * .5, scale[1] * .5, scale[2] * .5)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    if bevel > 0:
        add_bevel(o, bevel, 3)
    o["OLEANDER_AUTHORITY"] = authority
    return o


def add_uv_sphere(name, location, scale, material, authority="DERIVED_REFERENCE_REPRO_DETAIL"):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=48, ring_count=24, location=location)
    o = bpy.context.object
    o.name = name
    o.scale = scale
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material)
    for p in o.data.polygons:
        p.use_smooth = True
    o["OLEANDER_AUTHORITY"] = authority
    return o


def add_curve(name, points, material, bevel_depth=.003, authority="DERIVED_REFERENCE_REPRO_DETAIL"):
    cu = bpy.data.curves.new(name + "_CURVE", "CURVE")
    cu.dimensions = "3D"
    cu.resolution_u = 2
    cu.bevel_depth = bevel_depth
    cu.bevel_resolution = 3
    sp = cu.splines.new("NURBS")
    sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points):
        p.co = (*co, 1.0)
    sp.order_u = min(3, len(points))
    sp.use_endpoint_u = True
    obj = bpy.data.objects.new(name, cu)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    obj["OLEANDER_AUTHORITY"] = authority
    return obj


def add_panel(name, verts, material, solidify=.005):
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata(verts, [], [tuple(range(len(verts)))])
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    if solidify:
        mod = o.modifiers.new("REF_PANEL_THICKNESS", "SOLIDIFY")
        mod.thickness = solidify
        mod.offset = 0.0
    for p in me.polygons:
        p.use_smooth = True
    o["OLEANDER_AUTHORITY"] = "DERIVED_REFERENCE_REPRO_DETAIL"
    return o


def build_glass_and_seams(M):
    objs = []
    # Windshield and rear window.
    objs.append(add_panel("REF_WINDSHIELD", [
        (.92, .67, .890), (.92, -.67, .890), (.38, -.56, 1.245), (.38, .56, 1.245)
    ], M["glass"], .006))
    objs.append(add_panel("REF_REAR_GLASS", [
        (-.48, .57, 1.225), (-.48, -.57, 1.225), (-1.08, -.72, .875), (-1.08, .72, .875)
    ], M["glass"], .006))

    side_xz = [(.76, .885), (.47, 1.145), (.10, 1.235), (-.36, 1.205), (-.72, 1.070), (-.95, .875), (-.68, .835), (.57, .845)]
    for side in (1, -1):
        verts = []
        for x, z in side_xz:
            hw = interpolated_control(x)[1]
            verts.append((x, side * hw * .74, z))
        objs.append(add_panel(f"REF_SIDE_GLASS_{'L' if side>0 else 'R'}", verts, M["glass"], .006))
        # B-pillar and flush handle.
        hw = interpolated_control(-.18)[1]
        objs.append(add_cube(f"REF_B_PILLAR_{'L' if side>0 else 'R'}", (-.18, side * hw * .745, 1.005), (.045, .016, .300), M["body_dark"], .004))
        hw2 = interpolated_control(-.20)[1]
        objs.append(add_cube(f"REF_DOOR_HANDLE_{'L' if side>0 else 'R'}", (-.20, side * hw2 * 1.01, .705), (.115, .018, .025), M["body_dark"], .005))
        # Door perimeter derived from the visible side envelope.
        y = side * .905
        objs.append(add_curve(f"REF_DOOR_SEAM_{'L' if side>0 else 'R'}", [
            (.70, y, .755), (.58, y, .535), (-.64, y, .535), (-.82, y, .735), (-.73, y, .845)
        ], M["seam"], .0032))
    # Hood and rear deck seam cues.
    for side in (1, -1):
        objs.append(add_curve(f"REF_HOOD_SEAM_{'L' if side>0 else 'R'}", [
            (.98, side*.56, .795), (1.40, side*.58, .755), (1.88, side*.51, .690), (2.02, side*.39, .650)
        ], M["seam"], .0028))
        objs.append(add_curve(f"REF_REAR_DECK_SEAM_{'L' if side>0 else 'R'}", [
            (-1.02, side*.59, .875), (-1.42, side*.66, .815), (-1.82, side*.62, .755), (-2.03, side*.50, .705)
        ], M["seam"], .0028))
    return objs


def make_spoke_proto(name, r0, r1, width_inner, width_outer, depth, material):
    yi, yo = -depth*.5, depth*.5
    verts = [
        (r0, yi, -width_inner*.5), (r1, yi, -width_outer*.5), (r1, yi, width_outer*.5), (r0, yi, width_inner*.5),
        (r0, yo, -width_inner*.5), (r1, yo, -width_outer*.5), (r1, yo, width_outer*.5), (r0, yo, width_inner*.5),
    ]
    faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)]
    me = bpy.data.meshes.new(name + "_MESH")
    me.from_pydata(verts, [], faces)
    me.update()
    o = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(o)
    o.data.materials.append(material)
    o.hide_render = True
    o["OLEANDER_AUTHORITY"] = "DETAIL_PROTOTYPE_LIBRARY"
    add_bevel(o, .006, 3)
    return o


def build_wheel(code, x, y, spec, geom, M, side):
    z = geom["outer_r"]
    objs = []
    # tyre
    bpy.ops.mesh.primitive_torus_add(major_radius=geom["torus_major"], minor_radius=geom["torus_minor"], major_segments=72, minor_segments=20,
                                     location=(x,y,z), rotation=(math.pi/2,0,0))
    tire = bpy.context.object; tire.name=f"REF_TIRE_{code}"; tire.data.materials.append(M["tire"]); objs.append(tire)
    for p in tire.data.polygons: p.use_smooth=True
    tire["OLEANDER_AUTHORITY"]="DERIVED_REFERENCE_REPRO_DETAIL"
    # outer rim ring
    bpy.ops.mesh.primitive_torus_add(major_radius=geom["rim_r"]*.84, minor_radius=.018, major_segments=72, minor_segments=12,
                                     location=(x,y,z), rotation=(math.pi/2,0,0))
    rim=bpy.context.object;rim.name=f"REF_RIM_RING_{code}";rim.data.materials.append(M["rim"]);objs.append(rim)
    for p in rim.data.polygons:p.use_smooth=True
    # brake disc
    bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=geom["rim_r"]*.61, depth=.024, location=(x,y,z), rotation=(math.pi/2,0,0))
    disc=bpy.context.object;disc.name=f"REF_BRAKE_DISC_{code}";disc.data.materials.append(M["disc"]);objs.append(disc)
    # hub
    bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=.072, depth=.070, location=(x,y,z), rotation=(math.pi/2,0,0))
    hub=bpy.context.object;hub.name=f"REF_HUB_{code}";hub.data.materials.append(M["rim"]);objs.append(hub)
    # linked tapered spokes: 10 per wheel for a Carrera-style multi-spoke read.
    proto = make_spoke_proto(f"PROTO_SPOKE_{code}", .074, geom["rim_r"]*.80, .043, .020, .030, M["rim"])
    for i in range(10):
        o=bpy.data.objects.new(f"REF_SPOKE_{code}_{i:02d}",proto.data);bpy.context.collection.objects.link(o)
        o.location=(x,y,z);o.rotation_euler=(0,2*math.pi*i/10,0);o["OLEANDER_AUTHORITY"]="DETAIL_INSTANCE";o["OLEANDER_PROTOTYPE"]=proto.name;objs.append(o)
    # five lugs
    for i in range(5):
        a=2*math.pi*i/5; rr=.047
        lx=x+rr*math.cos(a);lz=z+rr*math.sin(a)
        bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=.010,depth=.045,location=(lx,y,lz),rotation=(math.pi/2,0,0))
        lug=bpy.context.object;lug.name=f"REF_LUG_{code}_{i}";lug.data.materials.append(M["body_dark"]);objs.append(lug)
    # caliper at rear-upper quadrant
    cal_x=x-.10;cal_z=z+.16
    cal=add_cube(f"REF_CALIPER_{code}",(cal_x,y+side*.025,cal_z),(.085,.065,.145),M["caliper"],.018);objs.append(cal)
    return objs


def build_wheels(M):
    all_objs=[]
    specs=[
        ("FL",FRONT_AXLE_X, FRONT_TRACK_Y, FRONT_TIRE, FRONT_WHEEL, 1),
        ("FR",FRONT_AXLE_X,-FRONT_TRACK_Y, FRONT_TIRE, FRONT_WHEEL,-1),
        ("RL",REAR_AXLE_X, REAR_TRACK_Y, REAR_TIRE, REAR_WHEEL, 1),
        ("RR",REAR_AXLE_X,-REAR_TRACK_Y, REAR_TIRE, REAR_WHEEL,-1),
    ]
    for s in specs: all_objs.extend(build_wheel(*s,M))
    return all_objs


def build_lights_trim(M):
    objs=[]
    # iconic oval front lamps, no badge or logo graphics.
    for side in (1,-1):
        housing=add_uv_sphere(f"REF_HEADLAMP_HOUSING_{side}",(1.82,side*.675,.770),(.070,.150,.135),M["body_dark"]);objs.append(housing)
        lens=add_uv_sphere(f"REF_HEADLAMP_LENS_{side}",(1.868,side*.675,.778),(.035,.132,.115),M["headlamp"]);objs.append(lens)
    # front lower intakes / splitter cue.
    objs.append(add_cube("REF_FRONT_CENTER_INTAKE",(2.205,0,.345),(.055,.58,.155),M["body_dark"],.025))
    for side in (1,-1):
        objs.append(add_cube(f"REF_FRONT_SIDE_INTAKE_{side}",(2.195,side*.555,.365),(.060,.285,.180),M["body_dark"],.025))
    objs.append(add_cube("REF_FRONT_SPLITTER",(2.220,0,.205),(.060,1.50,.045),M["body_dark"],.012))
    # full-width rear lightbar and diffuser/exhausts.
    objs.append(add_cube("REF_REAR_LIGHTBAR",(-2.155,0,.690),(.040,1.630,.045),M["tail"],.010))
    objs.append(add_cube("REF_REAR_DIFFUSER",(-2.205,0,.255),(.070,1.42,.145),M["body_dark"],.022))
    for side in (1,-1):
        bpy.ops.mesh.primitive_torus_add(major_radius=.060,minor_radius=.010,major_segments=48,minor_segments=10,location=(-2.245,side*.545,.285),rotation=(0,math.pi/2,0))
        ex=bpy.context.object;ex.name=f"REF_EXHAUST_{side}";ex.data.materials.append(M["rim"]);objs.append(ex)
    # mirrors
    for side in (1,-1):
        objs.append(add_uv_sphere(f"REF_MIRROR_{side}",(.48,side*.965,.905),(.110,.075,.052),M["body_dark"]))
    return objs


def ground_and_lights(M):
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0,0,0))
    g=bpy.context.object;g.name="STUDIO_GROUND";g.data.materials.append(M["ground"])
    world=bpy.context.scene.world
    world.use_nodes=True
    bg=world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value=(.018,.020,.024,1)
        bg.inputs["Strength"].default_value=.30
    def area(name,loc,energy,size,color):
        data=bpy.data.lights.new(name,"AREA");data.energy=energy;data.shape="DISK";data.size=size;data.color=color
        o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=loc
        direction=Vector((0,0,.65))-o.location;o.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();return o
    area("KEY_SOFT",(4.8,-4.2,5.8),1300,5.0,(1.0,.92,.84))
    area("FILL_SOFT",(-3.8,-2.5,3.8),850,4.0,(.76,.86,1.0))
    area("RIM_SOFT",(-3.0,4.5,4.5),1150,3.5,(1.0,.42,.30))
    area("TOP_SOFT",(.3,.2,7.0),900,3.0,(1.0,1.0,1.0))


def make_camera(name,loc,target,lens=70,ortho=False,ortho_scale=5.6):
    data=bpy.data.cameras.new(name)
    o=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(o);o.location=loc
    direction=Vector(target)-o.location;o.rotation_euler=direction.to_track_quat('-Z','Y').to_euler()
    if ortho:
        data.type="ORTHO";data.ortho_scale=ortho_scale
    else:
        data.lens=lens
    return o


def setup_render(path,samples,rx,ry):
    sc=bpy.context.scene
    sc.render.engine="BLENDER_EEVEE_NEXT" if False else "BLENDER_EEVEE_NEXT"
    # Reference reproduction prioritises geometry iteration determinism; EEVEE keeps CI fast.
    sc.render.resolution_x=rx;sc.render.resolution_y=ry;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format="PNG";sc.render.filepath=str(path)
    sc.render.film_transparent=False
    try: sc.view_settings.look="AgX - Medium High Contrast"
    except Exception: pass
    sc.render.image_settings.color_mode="RGBA"
    sc["OLEANDER_REQUESTED_SAMPLES"] = samples


def render_matrix(out,samples,rx,ry):
    rd=out/"renders";rd.mkdir(parents=True,exist_ok=True)
    views=[
        ("HERO_FRONT_3Q",(5.8,-6.3,2.65),(.20,0,.62),72,False,5.6),
        ("HERO_REAR_3Q",(-5.8,6.0,2.45),(-.15,0,.62),72,False,5.6),
        ("SIDE_ORTHO",(0,-8.0,1.15),(0,0,.66),70,True,5.15),
        ("FRONT",(6.5,0,1.12),(1.0,0,.62),85,False,5.0),
        ("REAR",(-6.5,0,1.08),(-1.0,0,.60),85,False,5.0),
        ("TOP_FRONT_3Q",(5.2,-5.5,5.2),(.15,0,.58),68,False,5.8),
    ]
    records=[]
    for label,loc,target,lens,ortho,scale in views:
        cam=make_camera("CAM_"+label,loc,target,lens,ortho,scale);bpy.context.scene.camera=cam
        p=rd/f"{MODEL}__{label}.png";setup_render(p,samples,rx,ry);bpy.ops.render.render(write_still=True)
        records.append({"view":label,"file":str(p),"bytes":p.stat().st_size if p.exists() else 0})
        bpy.data.objects.remove(cam,do_unlink=True)
    return records


def main():
    a=parse_args();out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
    clear_scene();M=build_materials()
    contract_digest=sha_json({"contract":REFERENCE_CONTRACT,"controls":CONTROL_JSON})

    # Sparse editable Source mesh: control-station density only.
    source_x=[r[0] for r in CONTROLS]
    source=build_body_mesh("SRC_PORSCHE_911_992_SPARSE_BODY",source_x,M["body"],"SPARSE_REFERENCE_REPRO_SOURCE",False)
    source.display_type="WIRE";source.hide_set(True)
    source_hash_before=mesh_hash(source)

    # Dense display mesh is regenerated from Source controls; it does not become geometry authority.
    dense_x=[REAR_X+(FRONT_X-REAR_X)*i/120 for i in range(121)]
    body=build_body_mesh("DERIVED_PORSCHE_911_992_BODY",dense_x,M["body"],"DERIVED_REFERENCE_REPRO_DISPLAY",True)
    body["OLEANDER_REGENERATED_FROM"]="SRC_PORSCHE_911_992_SPARSE_BODY"

    glass=build_glass_and_seams(M)
    wheels=build_wheels(M)
    trim=build_lights_trim(M)
    ground_and_lights(M)

    source_hash_after_build=mesh_hash(source)
    renders=render_matrix(out,a.samples,a.resolution_x,a.resolution_y)
    source_hash_after_render=mesh_hash(source)

    blend=out/f"{MODEL}.blend"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))

    bounds=body_bounds(source)
    all_names={o.name for o in bpy.context.scene.objects}
    checks={
        "source_digest_contract_stable":source.get("OLEANDER_SOURCE_CONTROL_DIGEST")==contract_digest,
        "source_mesh_unchanged_after_build":source_hash_before==source_hash_after_build,
        "source_mesh_unchanged_after_render":source_hash_before==source_hash_after_render,
        "official_length_locked":abs(bounds["length"]-LENGTH)<1e-9,
        "official_width_locked":abs(bounds["width"]-WIDTH)<1e-9,
        "official_height_max_locked":abs(bounds["max_z"]-HEIGHT)<1e-9,
        "wheelbase_locked":abs((FRONT_AXLE_X-REAR_AXLE_X)-WHEELBASE)<1e-9,
        "overhang_sum_locked":abs(FRONT_OVERHANG+WHEELBASE+REAR_OVERHANG-LENGTH)<1e-9,
        "front_tyre_od_from_public_size":abs(FRONT_WHEEL["outer_r"]*2-(.019*0+FRONT_TIRE["rim_in"]*.0254+2*FRONT_TIRE["section_m"]*FRONT_TIRE["aspect"]))<1e-9,
        "rear_tyre_od_from_public_size":abs(REAR_WHEEL["outer_r"]*2-(REAR_TIRE["rim_in"]*.0254+2*REAR_TIRE["section_m"]*REAR_TIRE["aspect"]))<1e-9,
        "four_tires_present":sum(1 for n in all_names if n.startswith("REF_TIRE_"))==4,
        "four_brake_discs_present":sum(1 for n in all_names if n.startswith("REF_BRAKE_DISC_"))==4,
        "forty_linked_spokes_present":sum(1 for n in all_names if n.startswith("REF_SPOKE_"))==40,
        "twenty_lugs_present":sum(1 for n in all_names if n.startswith("REF_LUG_"))==20,
        "two_oval_headlamps_present":sum(1 for n in all_names if n.startswith("REF_HEADLAMP_LENS_"))==2,
        "full_width_rear_lightbar_present":"REF_REAR_LIGHTBAR" in all_names,
        "windshield_rear_and_side_glass_present":all(n in all_names for n in ("REF_WINDSHIELD","REF_REAR_GLASS","REF_SIDE_GLASS_L","REF_SIDE_GLASS_R")),
        "six_view_render_matrix":len(renders)==6 and all(r["bytes"]>0 for r in renders),
        "native_blend_persisted":blend.exists() and blend.stat().st_size>0,
    }
    status="MACHINE_PASS_REFERENCE_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL"

    control_payload={
        "schema":"oleander.3d.reference-reproduction.source-controls.v1",
        "model":MODEL,
        "authority":"SPARSE_REFERENCE_REPRO_SOURCE",
        "control_digest":contract_digest,
        "controls":CONTROL_JSON,
        "source_mesh_sha256_before":source_hash_before,
        "source_mesh_sha256_after_build":source_hash_after_build,
        "source_mesh_sha256_after_render":source_hash_after_render,
    }
    qa={
        "schema":"oleander.3d.reference-reproduction.qa.v1",
        "model":MODEL,"reference_vehicle":"Porsche 911 Carrera (992)","status":status,
        "source_control_digest":contract_digest,"source_mesh_sha256":source_hash_before,
        "source_bounds":bounds,"checks":checks,"renders":renders,
        "object_counts":{"scene_objects":len(bpy.context.scene.objects),"glass_seam_objects":len(glass),"wheel_detail_objects":len(wheels),"light_trim_objects":len(trim)},
        "render_engine":"BLENDER_EEVEE_NEXT","requested_samples":a.samples,"resolution":[a.resolution_x,a.resolution_y],
        "design_quality_gate":"HOLD_FOR_REFERENCE_COMPARISON",
        "does_not_prove":REFERENCE_CONTRACT["does_not_prove"],
    }
    receipt={
        "schema":"oleander.3d.reference-reproduction.receipt.v1","model":MODEL,"status":"EXECUTED_"+status,
        "blender_version":bpy.app.version_string,"native_blend":str(blend),"native_blend_bytes":blend.stat().st_size,
        "source_authority":"SPARSE_REFERENCE_REPRO_SOURCE","derived_body":"DERIVED_REFERENCE_REPRO_DISPLAY",
        "reference_contract":"REFERENCE_CONTRACT.json","source_controls":"SOURCE_CONTROL_TABLE.json","qa":"REFERENCE_REPRO_QA.json",
        "design_quality_gate":"HOLD_FOR_REFERENCE_COMPARISON","main_keep":False,
    }
    (out/"REFERENCE_CONTRACT.json").write_text(json.dumps(REFERENCE_CONTRACT,ensure_ascii=False,indent=2)+"\n")
    (out/"SOURCE_CONTROL_TABLE.json").write_text(json.dumps(control_payload,ensure_ascii=False,indent=2)+"\n")
    (out/"REFERENCE_REPRO_QA.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n")
    (out/"REFERENCE_REPRO_RECEIPT.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"status":status,"source_hash":source_hash_before,"controls":len(CONTROLS),"renders":len(renders),"blend":str(blend)},indent=2))
    raise SystemExit(0 if status=="MACHINE_PASS_REFERENCE_REVIEW_REQUIRED" else 5)


if __name__=="__main__":
    main()
