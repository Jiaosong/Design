#!/usr/bin/env python3
from __future__ import annotations
import copy
import math
from typing import Any

import bpy

import g1_geometry_core as base
import g1_r2_core as r2
import g1_r2_blender_scene as bs

NAMES = {
    "GRIP_AXIS": "OL_SRC_GRIP_AXIS",
    "PALM_PROFILE": "OL_SRC_PALM_PROFILE",
    "THUMB_SIDE_PLAN": "OL_SRC_THUMB_SIDE_PLAN",
    "OPPOSITE_SIDE_PLAN": "OL_SRC_OPPOSITE_SIDE_PLAN",
    "LOWER_RETURN_PROFILE": "OL_SRC_LOWER_RETURN_PROFILE",
    "INTERFACE_DECK_BOUNDARY": "OL_SRC_INTERFACE_DECK_BOUNDARY",
}


def curve_points(name: str):
    obj = bpy.data.objects[name]
    return [tuple(float(v) for v in p.co[:3]) for p in obj.data.splines[0].points]


def extract_native_source(template: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(template)
    base.own(out, "GRIP_AXIS")["control_points"] = [list(p) for p in curve_points(NAMES["GRIP_AXIS"])]
    base.own(out, "PALM_PROFILE")["control_values"] = [float(p[2]) for p in curve_points(NAMES["PALM_PROFILE"])]
    base.own(out, "THUMB_SIDE_PLAN")["control_values"] = [float(p[1]) for p in curve_points(NAMES["THUMB_SIDE_PLAN"])]
    base.own(out, "OPPOSITE_SIDE_PLAN")["control_values"] = [float(-p[1]) for p in curve_points(NAMES["OPPOSITE_SIDE_PLAN"])]
    base.own(out, "LOWER_RETURN_PROFILE")["control_values"] = [float(-p[2]) for p in curve_points(NAMES["LOWER_RETURN_PROFILE"])]
    deck = bpy.data.objects[NAMES["INTERFACE_DECK_BOUNDARY"]]
    d = base.own(out, "INTERFACE_DECK_BOUNDARY")
    for key in ("u_center", "u_halfspan", "theta_center_rad", "theta_halfspan_rad", "depth_m", "core_fraction"):
        if key in deck:
            d[key] = float(deck[key])
    return out


def source_numeric_snapshot(source: dict[str, Any]) -> dict[str, list[float]]:
    return {
        "GRIP_AXIS": [float(v) for p in base.own(source,"GRIP_AXIS")["control_points"] for v in p],
        "PALM_PROFILE": [float(v) for v in base.own(source,"PALM_PROFILE")["control_values"]],
        "THUMB_SIDE_PLAN": [float(v) for v in base.own(source,"THUMB_SIDE_PLAN")["control_values"]],
        "OPPOSITE_SIDE_PLAN": [float(v) for v in base.own(source,"OPPOSITE_SIDE_PLAN")["control_values"]],
        "LOWER_RETURN_PROFILE": [float(v) for v in base.own(source,"LOWER_RETURN_PROFILE")["control_values"]],
        "INTERFACE_DECK_BOUNDARY": [float(base.own(source,"INTERFACE_DECK_BOUNDARY")[k]) for k in ("u_center","u_halfspan","theta_center_rad","theta_halfspan_rad","depth_m","core_fraction")],
    }


def source_difference(a: dict[str, Any], b: dict[str, Any]) -> dict[str, float]:
    aa = source_numeric_snapshot(a); bb = source_numeric_snapshot(b)
    return {k: max(abs(x-y) for x,y in zip(aa[k],bb[k])) if aa[k] else 0.0 for k in aa}


def replace_derived(name: str, source: dict[str, Any], collection, revision: bool = False):
    old = bpy.data.objects.get(name)
    if old is not None:
        mesh = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    verts, faces, labels = r2.mesh(source, revision)
    obj = bs.mesh_obj(name, verts, faces, collection, "Blender-native Source Authority derived execution mesh")
    obj["OLEANDER_NATIVE_SOURCE_ROUNDTRIP"] = True
    return obj, verts, faces, labels


def max_displacement(a, b):
    return max(math.dist(tuple(x), tuple(y)) for x, y in zip(a, b))


def controlled_native_edit_test(template: dict[str, Any], delta_m: float = 0.003):
    baseline = extract_native_source(template)
    bv, _, _ = r2.mesh(baseline, False)
    thumb = bpy.data.objects[NAMES["THUMB_SIDE_PLAN"]]
    point = thumb.data.splines[0].points[3]
    original = tuple(point.co)
    point.co[1] += delta_m
    edited = extract_native_source(template)
    ev, _, _ = r2.mesh(edited, False)
    diffs = source_difference(baseline, edited)
    displacement = max_displacement(bv, ev)
    point.co = original
    restored = extract_native_source(template)
    restored_error = source_difference(baseline, restored)
    changed = [k for k,v in diffs.items() if v > 1e-12]
    checks = {
        "only_thumb_source_family_changed": changed == ["THUMB_SIDE_PLAN"],
        "native_curve_edit_read_back": abs(diffs["THUMB_SIDE_PLAN"] - delta_m) <= 1e-9,
        "derived_surface_changed_after_native_edit": displacement >= 0.001,
        "native_source_restored_exactly": max(restored_error.values()) <= 1e-12,
    }
    return {
        "edit": {"object": NAMES["THUMB_SIDE_PLAN"], "control_index": 3, "delta_m": delta_m},
        "source_family_differences_m": diffs,
        "changed_families": changed,
        "derived_surface_max_displacement_m": displacement,
        "restored_source_error_m": restored_error,
        "checks": checks,
        "pass": all(checks.values()),
    }


def authority_checks(template: dict[str, Any]):
    extracted = extract_native_source(template)
    diffs = source_difference(template, extracted)
    objects = [bpy.data.objects.get(name) for name in NAMES.values()]
    present = len(objects) == 6 and all(o is not None for o in objects)
    checks = {
        "six_native_source_objects_present": present,
        "all_native_source_objects_editable": present and all(bool(o.get("OLEANDER_EDITABLE", False)) for o in objects),
        "all_native_source_objects_working_source": present and all(o.get("OLEANDER_AUTHORITY") == "WORKING_SURFACE_SOURCE" for o in objects),
        "bootstrap_roundtrip_exact": max(diffs.values()) <= 1e-12,
    }
    return extracted, diffs, checks
