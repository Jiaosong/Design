#!/usr/bin/env python3
"""Blender runtime/refinement bridge for the Porsche 911 (992) reference reproduction.

The base file holds the benchmark contract. This bridge applies focused v2 reference-fidelity
repairs without changing the official hard points:
- Blender argv routing;
- explicit wheel argument binding;
- headless Cycles CPU rendering;
- corrected wheel-arch topology (arched opening instead of rectangular cutout);
- revised 911 roof/hood/rear-haunch sparse controls;
- darker continuous greenhouse and flush elliptical lamps;
- float32-aware dimensional readback.
"""
from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
TARGET = HERE / "build_porsche_911_992_reference.py"

if "--" not in sys.argv:
    raise SystemExit("Blender argv bridge requires '--' before benchmark arguments")
idx = sys.argv.index("--")
benchmark_args = sys.argv[idx + 1 :]
sys.argv = [str(TARGET), *benchmark_args]

spec = importlib.util.spec_from_file_location("porsche_911_992_reference", TARGET)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Reference-fidelity v2 sparse station table. Official outer dimensions / axle hard points remain locked.
V2_CONTROLS = [
    (-2.271, .820, .650, .625, .600, .575, .420, .205),
    (-2.100, .875, .710, .690, .655, .625, .465, .210),
    (-1.820, .915, .775, .750, .705, .680, .500, .215),
    (-1.500, .926, .825, .800, .750, .715, .515, .218),
    (-1.195, .926, .865, .835, .785, .742, .525, .220),
    (-1.000, .920, .925, .885, .815, .755, .525, .220),
    (-.780,  .905, 1.045, .990, .850, .765, .522, .220),
    (-.560,  .885, 1.170, 1.095, .875, .772, .518, .220),
    (-.300,  .865, 1.265, 1.175, .895, .780, .513, .220),
    (-.050,  .852, 1.302, 1.210, .905, .782, .508, .220),
    (.220,   .850, 1.288, 1.198, .902, .780, .505, .220),
    (.460,   .855, 1.235, 1.155, .888, .772, .502, .220),
    (.680,   .865, 1.125, 1.055, .858, .758, .498, .220),
    (.850,   .878, .965, .925, .828, .745, .493, .220),
    (1.020,  .895, .825, .805, .780, .725, .485, .218),
    (1.255,  .912, .785, .770, .742, .705, .474, .215),
    (1.520,  .910, .758, .742, .712, .670, .452, .210),
    (1.800,  .895, .710, .695, .660, .620, .420, .202),
    (2.060,  .860, .635, .620, .590, .555, .380, .192),
    (2.271,  .800, .555, .540, .515, .485, .340, .180),
]
mod.CONTROLS = V2_CONTROLS
mod.CONTROL_X = [r[0] for r in V2_CONTROLS]
mod.CONTROL_JSON = [dict(zip(mod.CONTROL_KEYS, row)) for row in V2_CONTROLS]


def build_wheels_fixed(M):
    all_objs = []
    specs = [
        ("FL", mod.FRONT_AXLE_X, mod.FRONT_TRACK_Y, mod.FRONT_TIRE, mod.FRONT_WHEEL, 1),
        ("FR", mod.FRONT_AXLE_X, -mod.FRONT_TRACK_Y, mod.FRONT_TIRE, mod.FRONT_WHEEL, -1),
        ("RL", mod.REAR_AXLE_X, mod.REAR_TRACK_Y, mod.REAR_TIRE, mod.REAR_WHEEL, 1),
        ("RR", mod.REAR_AXLE_X, -mod.REAR_TRACK_Y, mod.REAR_TIRE, mod.REAR_WHEEL, -1),
    ]
    for code, x, y, tyre_spec, geom, side in specs:
        all_objs.extend(mod.build_wheel(code, x, y, tyre_spec, geom, M, side))
    return all_objs


def build_body_mesh_fixed(name, xs, material, authority, render_visible):
    verts, rings = [], []
    for x in xs:
        ring, _ = mod.section_ring(x)
        rings.append(list(range(len(verts), len(verts) + len(ring))))
        verts.extend(ring)
    nring = len(rings[0])
    faces = []
    for i in range(len(rings) - 1):
        mid = (xs[i] + xs[i + 1]) * .5
        arch_active, _ = mod.arch_data(mid)
        for j in range(nring):
            j2 = (j + 1) % nring
            # Only remove the actual lower-side ↔ rocker band on L/R sides.
            # Previous benchmark also removed adjacent underbody bands, producing square wheel holes.
            if arch_active and j in (7, 10):
                continue
            faces.append((rings[i][j], rings[i + 1][j], rings[i + 1][j2], rings[i][j2]))
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
    obj["OLEANDER_SOURCE_CONTROL_DIGEST"] = mod.sha_json({"contract": mod.REFERENCE_CONTRACT, "controls": mod.CONTROL_JSON})
    obj.hide_render = not render_visible
    if authority == "DERIVED_REFERENCE_REPRO_DISPLAY":
        # Derived-only smoothing: Source stays sparse and untouched.
        sub = obj.modifiers.new("REF_DERIVED_SURFACE_SMOOTH", "SUBSURF")
        sub.subdivision_type = "CATMULL_CLARK"
        sub.levels = 1
        sub.render_levels = 1
        bev = obj.modifiers.new("REF_DERIVED_EDGE_SOFTEN", "BEVEL")
        bev.width = .006
        bev.segments = 2
        bev.limit_method = "ANGLE"
    return obj


def body_bounds_fixed(obj):
    xs = [v.co.x for v in obj.data.vertices]
    ys = [v.co.y for v in obj.data.vertices]
    zs = [v.co.z for v in obj.data.vertices]
    # Blender mesh coordinates are float32. Report micrometre-rounded values before exact-contract assertions.
    r = lambda v: round(float(v), 6)
    return {
        "min_x": r(min(xs)), "max_x": r(max(xs)), "min_y": r(min(ys)), "max_y": r(max(ys)),
        "min_z": r(min(zs)), "max_z": r(max(zs)),
        "length": r(max(xs) - min(xs)), "width": r(max(ys) - min(ys)),
    }


def build_materials_fixed():
    M = mod.build_materials_original() if hasattr(mod, "build_materials_original") else mod.build_materials()
    glass = M["glass"]
    bsdf = glass.node_tree.nodes.get("Principled BSDF") if glass.use_nodes else None
    if bsdf:
        if "Base Color" in bsdf.inputs:
            bsdf.inputs["Base Color"].default_value = (.006, .010, .015, 1)
        if "Roughness" in bsdf.inputs:
            bsdf.inputs["Roughness"].default_value = .16
        if "Transmission Weight" in bsdf.inputs:
            bsdf.inputs["Transmission Weight"].default_value = .06
        elif "Transmission" in bsdf.inputs:
            bsdf.inputs["Transmission"].default_value = .06
    return M


# Preserve original material builder before patching it.
mod.build_materials_original = mod.build_materials


def build_glass_and_seams_fixed(M):
    objs = []
    objs.append(mod.add_panel("REF_WINDSHIELD", [
        (.875, .655, .865), (.875, -.655, .865), (.430, -.555, 1.190), (.430, .555, 1.190)
    ], M["glass"], .005))
    objs.append(mod.add_panel("REF_REAR_GLASS", [
        (-.430, .545, 1.185), (-.430, -.545, 1.185), (-1.020, -.690, .900), (-1.020, .690, .900)
    ], M["glass"], .005))
    side_xz = [
        (.790, .870), (.500, 1.145), (.165, 1.220), (-.260, 1.205),
        (-.620, 1.095), (-.900, .915), (-.700, .845), (.585, .842)
    ]
    for side in (1, -1):
        verts=[]
        for x,z in side_xz:
            hw=mod.interpolated_control(x)[1]
            verts.append((x, side*hw*.765, z))
        objs.append(mod.add_panel(f"REF_SIDE_GLASS_{'L' if side>0 else 'R'}", verts, M["glass"], .005))
        hw=mod.interpolated_control(-.365)[1]
        objs.append(mod.add_cube(f"REF_B_PILLAR_{'L' if side>0 else 'R'}", (-.365, side*hw*.772, 1.005), (.040,.018,.310), M["body_dark"], .004))
        hw2=mod.interpolated_control(-.120)[1]
        objs.append(mod.add_cube(f"REF_DOOR_HANDLE_{'L' if side>0 else 'R'}", (-.120, side*hw2*1.006, .704), (.118,.016,.022), M["body_dark"], .004))
        y=side*.902
        objs.append(mod.add_curve(f"REF_DOOR_SEAM_{'L' if side>0 else 'R'}", [
            (.735,y,.760),(.650,y,.555),(-.610,y,.548),(-.730,y,.670),(-.710,y,.835)
        ], M["seam"], .0026))
    for side in (1,-1):
        objs.append(mod.add_curve(f"REF_HOOD_SEAM_{'L' if side>0 else 'R'}", [
            (.965,side*.555,.790),(1.330,side*.575,.760),(1.720,side*.545,.715),(2.015,side*.440,.650)
        ], M["seam"], .0025))
        objs.append(mod.add_curve(f"REF_REAR_DECK_SEAM_{'L' if side>0 else 'R'}", [
            (-1.020,side*.585,.895),(-1.390,side*.655,.835),(-1.760,side*.625,.775),(-2.025,side*.515,.715)
        ], M["seam"], .0025))
    return objs


def build_lights_trim_fixed(M):
    objs=[]
    for side in (1,-1):
        housing=mod.add_uv_sphere(f"REF_HEADLAMP_HOUSING_{side}",(1.735,side*.665,.780),(.142,.135,.036),M["body_dark"])
        housing.rotation_euler[1]=math.radians(-12)
        lens=mod.add_uv_sphere(f"REF_HEADLAMP_LENS_{side}",(1.744,side*.665,.788),(.127,.120,.027),M["headlamp"])
        lens.rotation_euler[1]=math.radians(-12)
        objs.extend((housing,lens))
    objs.append(mod.add_cube("REF_FRONT_CENTER_INTAKE",(2.185,0,.340),(.045,.500,.120),M["body_dark"],.020))
    for side in (1,-1):
        objs.append(mod.add_cube(f"REF_FRONT_SIDE_INTAKE_{side}",(2.175,side*.555,.350),(.048,.245,.145),M["body_dark"],.020))
    objs.append(mod.add_cube("REF_FRONT_SPLITTER",(2.205,0,.205),(.050,1.42,.030),M["body_dark"],.010))
    objs.append(mod.add_cube("REF_REAR_LIGHTBAR",(-2.145,0,.705),(.030,1.570,.032),M["tail"],.008))
    objs.append(mod.add_cube("REF_REAR_DIFFUSER",(-2.190,0,.270),(.055,1.34,.105),M["body_dark"],.018))
    for side in (1,-1):
        bpy.ops.mesh.primitive_torus_add(major_radius=.052,minor_radius=.008,major_segments=40,minor_segments=8,
            location=(-2.225,side*.540,.290),rotation=(0,math.pi/2,0))
        ex=bpy.context.object;ex.name=f"REF_EXHAUST_{side}";ex.data.materials.append(M["rim"]);objs.append(ex)
        mirror=mod.add_uv_sphere(f"REF_MIRROR_{side}",(.575,side*.948,.895),(.100,.070,.045),M["body_dark"])
        mirror.rotation_euler[2]=math.radians(side*8)
        objs.append(mirror)
    return objs


def setup_render_fixed(path, samples, rx, ry):
    sc=bpy.context.scene
    sc.render.engine="CYCLES";sc.cycles.device="CPU";sc.cycles.samples=samples
    sc.cycles.use_denoising=False;sc.cycles.max_bounces=4;sc.cycles.diffuse_bounces=2
    sc.cycles.glossy_bounces=2;sc.cycles.transmission_bounces=3
    sc.render.resolution_x=rx;sc.render.resolution_y=ry;sc.render.resolution_percentage=100
    sc.render.image_settings.file_format="PNG";sc.render.image_settings.color_mode="RGBA"
    sc.render.filepath=str(path);sc.render.film_transparent=False
    try: sc.view_settings.look="AgX - Medium High Contrast"
    except Exception: pass
    sc["OLEANDER_REQUESTED_SAMPLES"]=samples

mod.build_wheels=build_wheels_fixed
mod.build_body_mesh=build_body_mesh_fixed
mod.body_bounds=body_bounds_fixed
mod.build_materials=build_materials_fixed
mod.build_glass_and_seams=build_glass_and_seams_fixed
mod.build_lights_trim=build_lights_trim_fixed
mod.setup_render=setup_render_fixed

out_dir=None
if "--out" in benchmark_args:
    out_dir=Path(benchmark_args[benchmark_args.index("--out")+1])

try:
    mod.main()
except SystemExit as exc:
    if out_dir is not None:
        qa_path=out_dir/"REFERENCE_REPRO_QA.json"
        if qa_path.exists():
            qa=json.loads(qa_path.read_text())
            qa["render_engine"]="CYCLES_CPU"
            qa["reference_fidelity_revision"]="V2_ARCH_ROOF_GREENHOUSE_LAMPS"
            qa["runtime_bridge_fixes"]=[
                "ARGV_ROUTING","WHEEL_ARGUMENT_BINDING","HEADLESS_CYCLES_CPU",
                "FLOAT32_DIMENSION_READBACK","WHEEL_ARCH_TOPOLOGY","911_SPARSE_CONTROL_V2",
                "GREENHOUSE_V2","FLUSH_HEADLAMPS_V2"
            ]
            qa_path.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n")
    raise
