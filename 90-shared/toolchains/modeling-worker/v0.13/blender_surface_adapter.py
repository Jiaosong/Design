#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
from typing import Iterable

import bpy
from mathutils import Vector

SYSTEM = "OLEANDER Blender Surface System"
SYSTEM_VERSION = "v1.20.0"


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)


def collection(name: str):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(c)
    return c


def source_curve(name: str, points: Iterable[Iterable[float]], family: str, coll, bevel: float = 0.0007):
    data = bpy.data.curves.new(name + "-DATA", "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 12
    data.bevel_depth = bevel
    data.bevel_resolution = 2
    spline = data.splines.new("POLY")
    pts = [tuple(float(v) for v in p) for p in points]
    spline.points.add(len(pts) - 1)
    for bp, p in zip(spline.points, pts):
        bp.co = (*p, 1.0)
    obj = bpy.data.objects.new(name, data)
    coll.objects.link(obj)
    obj["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    obj["OLEANDER_SOURCE_FAMILY"] = family
    obj["OLEANDER_EDITABLE"] = True
    obj["OLEANDER_SURFACE_SYSTEM"] = SYSTEM_VERSION
    obj.show_in_front = True
    return obj


def source_boundary(name: str, points, family: str, props: dict[str, float | str], coll):
    obj = source_curve(name, points, family, coll, 0.00055)
    obj.data.splines[0].use_cyclic_u = True
    for k, v in props.items():
        obj[k] = v
    return obj


def mesh_object(name: str, verts, faces, coll, authority: str = "DERIVED_EXECUTION_GEOMETRY"):
    me = bpy.data.meshes.new(name + "-DATA")
    me.from_pydata([tuple(p) for p in verts], [], [tuple(f) for f in faces])
    me.update()
    obj = bpy.data.objects.new(name, me)
    coll.objects.link(obj)
    for poly in me.polygons:
        poly.use_smooth = True
    obj["OLEANDER_AUTHORITY"] = authority
    obj["OLEANDER_EDITABLE_AUTHORITY"] = False
    obj["OLEANDER_SURFACE_SYSTEM"] = SYSTEM_VERSION
    return obj


def principled(name: str, color, roughness: float, metallic: float = 0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    return m


def zebra_material():
    m = bpy.data.materials.new("OL_MAT_ZebraNormalField_v1")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    geo = nt.nodes.new("ShaderNodeNewGeometry")
    dot = nt.nodes.new("ShaderNodeVectorMath")
    dot.operation = "DOT_PRODUCT"
    dot.inputs[1].default_value = (0.72, 0.42, 0.55)
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"; mul.inputs[1].default_value = 30.0
    sine = nt.nodes.new("ShaderNodeMath"); sine.operation = "SINE"
    scale = nt.nodes.new("ShaderNodeMath"); scale.operation = "MULTIPLY"; scale.inputs[1].default_value = 0.5
    add = nt.nodes.new("ShaderNodeMath"); add.operation = "ADD"; add.inputs[1].default_value = 0.5
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.interpolation = "CONSTANT"
    ramp.color_ramp.elements[0].position = 0.48
    ramp.color_ramp.elements[0].color = (0.005, 0.005, 0.005, 1)
    ramp.color_ramp.elements[1].position = 0.52
    ramp.color_ramp.elements[1].color = (0.96, 0.96, 0.96, 1)
    bsdf.inputs["Roughness"].default_value = 0.16
    nt.links.new(geo.outputs["Normal"], dot.inputs[0])
    nt.links.new(dot.outputs["Value"], mul.inputs[0])
    nt.links.new(mul.outputs[0], sine.inputs[0])
    nt.links.new(sine.outputs[0], scale.inputs[0])
    nt.links.new(scale.outputs[0], add.inputs[0])
    nt.links.new(add.outputs[0], ramp.inputs[0])
    nt.links.new(ramp.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(bsdf.outputs[0], out.inputs[0])
    return m


def look_at(obj, target):
    obj.rotation_euler = (Vector(target) - obj.location).to_track_quat("-Z", "Y").to_euler()


def camera(name: str, loc, target, ortho: float, coll):
    d = bpy.data.cameras.new(name + "-DATA")
    d.type = "ORTHO"
    d.ortho_scale = ortho
    o = bpy.data.objects.new(name, d)
    coll.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def area(name: str, loc, target, energy: float, size: float, size_y: float, coll):
    d = bpy.data.lights.new(name + "-DATA", "AREA")
    d.energy = energy
    d.shape = "RECTANGLE"
    d.size = size
    d.size_y = size_y
    o = bpy.data.objects.new(name, d)
    coll.objects.link(o)
    o.location = loc
    look_at(o, target)
    return o


def setup_scene(resolution: int, samples: int = 8, engine: str = "CYCLES"):
    sc = bpy.context.scene
    sc.render.engine = engine
    sc.render.resolution_x = resolution
    sc.render.resolution_y = resolution
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.film_transparent = False
    sc.world.color = (0.018, 0.018, 0.018)
    sc.render.use_persistent_data = True
    if engine == "CYCLES":
        sc.cycles.samples = samples
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.adaptive_threshold = 0.08
    sc["OLEANDER_SURFACE_SYSTEM"] = SYSTEM
    sc["OLEANDER_SURFACE_SYSTEM_VERSION"] = SYSTEM_VERSION
    sc["OLEANDER_FIDELITY"] = "F1_DESIGN_VALIDATION"
    sc["OLEANDER_RENDER_ENGINE"] = engine
    sc["OLEANDER_TARGET_SAMPLES"] = samples
    return sc


def build_lighting(target, coll):
    rigs = {
        "BROAD": [area("LGT-BROAD-KEY", (0.22, -0.34, 0.58), target, 950, 0.42, 0.34, coll),
                  area("LGT-BROAD-FILL", (-0.18, 0.28, 0.34), target, 500, 0.30, 0.24, coll)],
        "STRIP": [area("LGT-STRIP-A", (0.08, -0.34, 0.31), target, 1150, 0.018, 0.42, coll),
                  area("LGT-STRIP-B", (-0.08, 0.30, 0.28), target, 850, 0.014, 0.36, coll)],
        "GRAZING": [area("LGT-GRAZE-A", (0.02, -0.42, 0.12), target, 1350, 0.012, 0.50, coll)]
    }
    for items in rigs.values():
        for o in items:
            o.hide_render = True
    return rigs


def set_rig(rigs, active: str | None):
    for key, items in rigs.items():
        for o in items:
            o.hide_render = key != active


def assign(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def render(sc, out: Path, camera_obj, name: str):
    sc.camera = camera_obj
    sc.render.filepath = str(out / f"{name}.png")
    bpy.ops.render.render(write_still=True)


def set_collection_render(coll, visible: bool):
    coll.hide_render = not visible
