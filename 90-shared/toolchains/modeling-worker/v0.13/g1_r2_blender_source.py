#!/usr/bin/env python3
from __future__ import annotations
import copy
import math

import bpy

import blender_surface_adapter as bsa
import g1_geometry_core as base
import g1_r2_core as r2

SOURCE_OBJECTS = {
    "GRIP_AXIS": "SRC-GRIP_AXIS",
    "PALM_PROFILE": "SRC-PALM_PROFILE",
    "THUMB_SIDE_PLAN": "SRC-THUMB_SIDE_PLAN",
    "OPPOSITE_SIDE_PLAN": "SRC-OPPOSITE_SIDE_PLAN",
    "LOWER_RETURN_PROFILE": "SRC-LOWER_RETURN_PROFILE",
    "INTERFACE_DECK_BOUNDARY": "SRC-INTERFACE_DECK_BOUNDARY",
}


def compile_r2(base_source: dict, correction: dict) -> dict:
    return r2.apply(base_source, correction)


def _curve_points(obj):
    return [tuple(float(v) for v in p.co[:3]) for p in obj.data.splines[0].points]


def _profile_points(grip, values, mode: str):
    pts = []
    for g, value in zip(grip, values):
        x, y, z = (float(v) for v in g)
        v = float(value)
        if mode == "PALM": pts.append((x, y, z + v))
        elif mode == "THUMB": pts.append((x, y + v, z))
        elif mode == "OPPOSITE": pts.append((x, y - v, z))
        elif mode == "LOWER": pts.append((x, y, z - v))
        else: raise ValueError(mode)
    return pts


def interface_boundary_points(source: dict, count: int = 64):
    d = base.own(source, "INTERFACE_DECK_BOUNDARY")
    uc = float(d["u_center"]); uh = float(d["u_halfspan"])
    tc = float(d.get("theta_center_rad", 0.0)); th = float(d["theta_halfspan_rad"])
    pts = []
    for i in range(count):
        a = 2.0 * math.pi * i / count
        u = uc + uh * math.cos(a)
        t = tc + th * math.sin(a)
        pts.append(r2.point(source, u, t, False, True))
    return pts


def build_native_source(source: dict, collection):
    grip = [tuple(p) for p in base.own(source, "GRIP_AXIS")["control_points"]]
    objects = {}
    objects["GRIP_AXIS"] = bsa.source_curve(SOURCE_OBJECTS["GRIP_AXIS"], grip, "GRIP_AXIS", collection)
    objects["PALM_PROFILE"] = bsa.source_curve(SOURCE_OBJECTS["PALM_PROFILE"], _profile_points(grip, base.own(source,"PALM_PROFILE")["control_values"], "PALM"), "PALM_PROFILE", collection)
    objects["THUMB_SIDE_PLAN"] = bsa.source_curve(SOURCE_OBJECTS["THUMB_SIDE_PLAN"], _profile_points(grip, base.own(source,"THUMB_SIDE_PLAN")["control_values"], "THUMB"), "THUMB_SIDE_PLAN", collection)
    objects["OPPOSITE_SIDE_PLAN"] = bsa.source_curve(SOURCE_OBJECTS["OPPOSITE_SIDE_PLAN"], _profile_points(grip, base.own(source,"OPPOSITE_SIDE_PLAN")["control_values"], "OPPOSITE"), "OPPOSITE_SIDE_PLAN", collection)
    objects["LOWER_RETURN_PROFILE"] = bsa.source_curve(SOURCE_OBJECTS["LOWER_RETURN_PROFILE"], _profile_points(grip, base.own(source,"LOWER_RETURN_PROFILE")["control_values"], "LOWER"), "LOWER_RETURN_PROFILE", collection)
    d = base.own(source, "INTERFACE_DECK_BOUNDARY")
    props = {
        "u_center": float(d["u_center"]),
        "u_halfspan": float(d["u_halfspan"]),
        "theta_center_rad": float(d.get("theta_center_rad", 0.0)),
        "theta_halfspan_rad": float(d["theta_halfspan_rad"]),
        "depth_m": float(d["depth_m"]),
        "core_fraction": float(d["core_fraction"]),
        "OLEANDER_EDIT_MODE": "EDIT CUSTOM PROPERTIES; boundary curve is regenerated from those parameters"
    }
    objects["INTERFACE_DECK_BOUNDARY"] = bsa.source_boundary(SOURCE_OBJECTS["INTERFACE_DECK_BOUNDARY"], interface_boundary_points(source), "INTERFACE_DECK_BOUNDARY", props, collection)
    return objects


def extract_source_from_blend(template: dict) -> dict:
    out = copy.deepcopy(template)
    grip = _curve_points(bpy.data.objects[SOURCE_OBJECTS["GRIP_AXIS"]])
    base.own(out, "GRIP_AXIS")["control_points"] = [list(p) for p in grip]

    palm = _curve_points(bpy.data.objects[SOURCE_OBJECTS["PALM_PROFILE"]])
    thumb = _curve_points(bpy.data.objects[SOURCE_OBJECTS["THUMB_SIDE_PLAN"]])
    opposite = _curve_points(bpy.data.objects[SOURCE_OBJECTS["OPPOSITE_SIDE_PLAN"]])
    lower = _curve_points(bpy.data.objects[SOURCE_OBJECTS["LOWER_RETURN_PROFILE"]])
    base.own(out,"PALM_PROFILE")["control_values"] = [float(p[2]-g[2]) for p,g in zip(palm,grip)]
    base.own(out,"THUMB_SIDE_PLAN")["control_values"] = [float(p[1]-g[1]) for p,g in zip(thumb,grip)]
    base.own(out,"OPPOSITE_SIDE_PLAN")["control_values"] = [float(g[1]-p[1]) for p,g in zip(opposite,grip)]
    base.own(out,"LOWER_RETURN_PROFILE")["control_values"] = [float(g[2]-p[2]) for p,g in zip(lower,grip)]

    deck = bpy.data.objects[SOURCE_OBJECTS["INTERFACE_DECK_BOUNDARY"]]
    d = base.own(out, "INTERFACE_DECK_BOUNDARY")
    for key in ("u_center","u_halfspan","theta_center_rad","theta_halfspan_rad","depth_m","core_fraction"):
        d[key] = float(deck[key])
    return out


def replace_derived_surface(source: dict, collection, name: str = "DRV-G1-R2-EVALUATED-SURFACE", revision: bool = False):
    old = bpy.data.objects.get(name)
    if old is not None:
        data = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if data is not None:
            bpy.data.meshes.remove(data)
    verts, faces, labels = r2.mesh(source, revision)
    obj = bsa.mesh_object(name, verts, faces, collection)
    obj["OLEANDER_SOURCE_BINDING"] = "00_SOURCE_AUTHORITY"
    obj["OLEANDER_RELATION_REVISION"] = bool(revision)
    obj["OLEANDER_SEMANTIC_DECK_FACE_COUNT"] = int(labels.count("DECK"))
    return obj, verts, faces, labels


def source_authority_checks() -> dict[str, bool]:
    checks = {}
    for family, name in SOURCE_OBJECTS.items():
        obj = bpy.data.objects.get(name)
        checks[family] = bool(obj and obj.get("OLEANDER_AUTHORITY") == "WORKING_SURFACE_SOURCE" and obj.get("OLEANDER_EDITABLE") is True)
    derived = bpy.data.objects.get("DRV-G1-R2-EVALUATED-SURFACE")
    checks["derived_mesh_not_source_authority"] = bool(derived and derived.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_GEOMETRY" and derived.get("OLEANDER_EDITABLE_AUTHORITY") is False)
    return checks
