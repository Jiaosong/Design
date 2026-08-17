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


def theta_center_rad(source: dict[str, Any]) -> float:
    d = base.own(source, "INTERFACE_DECK_BOUNDARY")
    if "theta_center_rad" in d:
        return float(d["theta_center_rad"])
    if d.get("theta_center") == "TOP_MERIDIAN":
        return 0.0
    raise ValueError("INTERFACE_DECK_BOUNDARY requires theta_center_rad or theta_center=TOP_MERIDIAN")


def termination_exponent(source: dict[str, Any]) -> float:
    return float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))


def termination_cap_onset(source: dict[str, Any]) -> float:
    return float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_cap_onset_u", 1.0))


def termination_cap_pole_scale(source: dict[str, Any]) -> float:
    return float(
        base.own(source, "LOWER_RETURN_PROFILE").get(
            "termination_cap_pole_curvature_scale", r2.CAP_POLE_CURVATURE_SCALE_DEFAULT
        )
    )


def extract_native_source(template: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(template)
    base.own(out, "GRIP_AXIS")["control_points"] = [list(p) for p in curve_points(NAMES["GRIP_AXIS"])]
    base.own(out, "PALM_PROFILE")["control_values"] = [float(p[2]) for p in curve_points(NAMES["PALM_PROFILE"])]
    base.own(out, "THUMB_SIDE_PLAN")["control_values"] = [float(p[1]) for p in curve_points(NAMES["THUMB_SIDE_PLAN"])]
    base.own(out, "OPPOSITE_SIDE_PLAN")["control_values"] = [float(-p[1]) for p in curve_points(NAMES["OPPOSITE_SIDE_PLAN"])]
    lower_obj = bpy.data.objects[NAMES["LOWER_RETURN_PROFILE"]]
    lower = base.own(out, "LOWER_RETURN_PROFILE")
    lower["control_values"] = [float(-p[2]) for p in curve_points(NAMES["LOWER_RETURN_PROFILE"])]
    lower["termination_envelope_exponent"] = float(
        lower_obj.get("termination_envelope_exponent", termination_exponent(template))
    )
    lower["termination_envelope"] = f"sin(pi*u)^{lower['termination_envelope_exponent']}"
    lower["termination_envelope_semantics"] = str(
        lower_obj.get("termination_envelope_semantics", "SHARED_CROSS_SECTION_TERMINATION_ENVELOPE")
    )
    if "termination_cap_onset_u" in lower_obj:
        lower["termination_cap_onset_u"] = float(lower_obj["termination_cap_onset_u"])
        lower["termination_cap_pole_curvature_scale"] = float(
            lower_obj.get("termination_cap_pole_curvature_scale", r2.CAP_POLE_CURVATURE_SCALE_DEFAULT)
        )
        lower["termination_cap_law"] = str(lower_obj.get("termination_cap_law", r2.CAP_LAW))
        lower["termination_cap_semantics"] = str(lower_obj.get("termination_cap_semantics", r2.CAP_SEMANTICS))
        lower["termination_cap_endpoint_section"] = str(
            lower_obj.get("termination_cap_endpoint_section", r2.CAP_ENDPOINT_SECTION)
        )
    else:
        for key in (
            "termination_cap_onset_u",
            "termination_cap_pole_curvature_scale",
            "termination_cap_law",
            "termination_cap_semantics",
            "termination_cap_endpoint_section",
        ):
            lower.pop(key, None)

    deck = bpy.data.objects[NAMES["INTERFACE_DECK_BOUNDARY"]]
    d = base.own(out, "INTERFACE_DECK_BOUNDARY")
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "depth_m", "core_fraction"):
        if key in deck:
            d[key] = float(deck[key])
    if d.get("theta_center") != "TOP_MERIDIAN":
        d["theta_center_rad"] = float(deck.get("theta_center_rad", theta_center_rad(template)))
    return out


def source_numeric_snapshot(source: dict[str, Any]) -> dict[str, list[float]]:
    d = base.own(source, "INTERFACE_DECK_BOUNDARY")
    lower = base.own(source, "LOWER_RETURN_PROFILE")
    return {
        "GRIP_AXIS": [float(v) for p in base.own(source, "GRIP_AXIS")["control_points"] for v in p],
        "PALM_PROFILE": [float(v) for v in base.own(source, "PALM_PROFILE")["control_values"]],
        "THUMB_SIDE_PLAN": [float(v) for v in base.own(source, "THUMB_SIDE_PLAN")["control_values"]],
        "OPPOSITE_SIDE_PLAN": [float(v) for v in base.own(source, "OPPOSITE_SIDE_PLAN")["control_values"]],
        "LOWER_RETURN_PROFILE": [float(v) for v in lower["control_values"]]
        + [
            float(lower.get("termination_envelope_exponent", 0.55)),
            float(lower.get("termination_cap_onset_u", 1.0)),
            float(lower.get("termination_cap_pole_curvature_scale", r2.CAP_POLE_CURVATURE_SCALE_DEFAULT)),
        ],
        "INTERFACE_DECK_BOUNDARY": [
            float(d["u_center"]),
            float(d["u_halfspan"]),
            theta_center_rad(source),
            float(d["theta_halfspan_rad"]),
            float(d["depth_m"]),
            float(d["core_fraction"]),
        ],
    }


def source_difference(a: dict[str, Any], b: dict[str, Any]) -> dict[str, float]:
    aa = source_numeric_snapshot(a)
    bb = source_numeric_snapshot(b)
    return {k: max(abs(x - y) for x, y in zip(aa[k], bb[k])) if aa[k] else 0.0 for k in aa}


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
    if len(a) != len(b):
        return math.inf
    return max(math.dist(tuple(x), tuple(y)) for x, y in zip(a, b))


def controlled_native_edit_test(template: dict[str, Any], delta_m: float = 0.003, edit_tolerance: float = 1e-8, restore_tolerance: float = 1e-12):
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
    changed = [k for k, v in diffs.items() if v > edit_tolerance]
    checks = {
        "only_thumb_source_family_changed": changed == ["THUMB_SIDE_PLAN"],
        "native_curve_edit_read_back": abs(diffs["THUMB_SIDE_PLAN"] - delta_m) <= edit_tolerance,
        "derived_surface_changed_after_native_edit": displacement >= 0.001,
        "native_source_restored_exactly": max(restored_error.values()) <= restore_tolerance,
    }
    return {
        "edit": {"object": NAMES["THUMB_SIDE_PLAN"], "control_index": 3, "delta_m": delta_m},
        "representation_tolerance_m": edit_tolerance,
        "source_family_differences_m": diffs,
        "changed_families": changed,
        "derived_surface_max_displacement_m": displacement,
        "restored_source_error_m": restored_error,
        "checks": checks,
        "pass": all(checks.values()),
    }


def controlled_native_termination_relation_edit_test(
    template: dict[str, Any],
    delta_exponent: float = 0.02,
    edit_tolerance: float = 1e-8,
    restore_tolerance: float = 1e-12,
):
    baseline = extract_native_source(template)
    bv, _, _ = r2.mesh(baseline, False)
    lower = bpy.data.objects[NAMES["LOWER_RETURN_PROFILE"]]
    original = float(lower["termination_envelope_exponent"])
    lower["termination_envelope_exponent"] = original + float(delta_exponent)
    edited = extract_native_source(template)
    ev, _, _ = r2.mesh(edited, False)
    diffs = source_difference(baseline, edited)
    displacement = max_displacement(bv, ev)
    lower["termination_envelope_exponent"] = original
    restored = extract_native_source(template)
    restored_error = source_difference(baseline, restored)
    changed = [k for k, v in diffs.items() if v > edit_tolerance]
    checks = {
        "only_lower_return_source_family_relation_changed": changed == ["LOWER_RETURN_PROFILE"],
        "native_relation_edit_read_back": abs(diffs["LOWER_RETURN_PROFILE"] - abs(float(delta_exponent))) <= edit_tolerance,
        "derived_surface_changed_after_native_relation_edit": displacement > 1e-6,
        "native_source_restored_exactly": max(restored_error.values()) <= restore_tolerance,
    }
    return {
        "edit": {
            "object": NAMES["LOWER_RETURN_PROFILE"],
            "property": "termination_envelope_exponent",
            "delta": float(delta_exponent),
            "semantics": "SHARED_CROSS_SECTION_TERMINATION_ENVELOPE",
        },
        "source_family_differences": diffs,
        "changed_families": changed,
        "derived_surface_max_displacement_m": displacement,
        "restored_source_error": restored_error,
        "checks": checks,
        "pass": all(checks.values()),
    }


def controlled_native_cap_relation_edit_test(
    template: dict[str, Any],
    delta_onset_u: float = 0.01,
    edit_tolerance: float = 1e-8,
    restore_tolerance: float = 1e-12,
):
    lower_obj = bpy.data.objects[NAMES["LOWER_RETURN_PROFILE"]]
    if "termination_cap_onset_u" not in lower_obj:
        raise RuntimeError("termination_cap_onset_u must be bound before cap roundtrip edit test")
    baseline = extract_native_source(template)
    original = float(lower_obj["termination_cap_onset_u"])
    lower_obj["termination_cap_onset_u"] = original + float(delta_onset_u)
    edited = extract_native_source(template)
    diffs = source_difference(baseline, edited)
    lower_obj["termination_cap_onset_u"] = original
    restored = extract_native_source(template)
    restored_error = source_difference(baseline, restored)
    changed = [k for k, v in diffs.items() if v > edit_tolerance]
    checks = {
        "only_lower_return_source_family_cap_relation_changed": changed == ["LOWER_RETURN_PROFILE"],
        "native_cap_relation_edit_read_back": abs(diffs["LOWER_RETURN_PROFILE"] - abs(float(delta_onset_u))) <= edit_tolerance,
        "native_source_restored_exactly": max(restored_error.values()) <= restore_tolerance,
        "cap_relation_semantics_preserved": base.own(edited, "LOWER_RETURN_PROFILE").get("termination_cap_semantics") == r2.CAP_SEMANTICS,
        "cap_relation_law_preserved": base.own(edited, "LOWER_RETURN_PROFILE").get("termination_cap_law") == r2.CAP_LAW,
    }
    return {
        "edit": {
            "object": NAMES["LOWER_RETURN_PROFILE"],
            "property": "termination_cap_onset_u",
            "delta": float(delta_onset_u),
            "semantics": r2.CAP_SEMANTICS,
        },
        "source_family_differences": diffs,
        "changed_families": changed,
        "restored_source_error": restored_error,
        "checks": checks,
        "pass": all(checks.values()),
    }


def controlled_native_cap_pole_scale_edit_test(
    template: dict[str, Any],
    delta_scale: float = 0.02,
    edit_tolerance: float = 1e-8,
    restore_tolerance: float = 1e-12,
):
    lower_obj = bpy.data.objects[NAMES["LOWER_RETURN_PROFILE"]]
    if "termination_cap_onset_u" not in lower_obj or "termination_cap_pole_curvature_scale" not in lower_obj:
        raise RuntimeError("cap onset and pole curvature scale must be bound before scale roundtrip edit test")
    baseline = extract_native_source(template)
    original = float(lower_obj["termination_cap_pole_curvature_scale"])
    lower_obj["termination_cap_pole_curvature_scale"] = original + float(delta_scale)
    edited = extract_native_source(template)
    diffs = source_difference(baseline, edited)
    lower_obj["termination_cap_pole_curvature_scale"] = original
    restored = extract_native_source(template)
    restored_error = source_difference(baseline, restored)
    changed = [k for k, v in diffs.items() if v > edit_tolerance]
    checks = {
        "only_lower_return_source_family_cap_scale_changed": changed == ["LOWER_RETURN_PROFILE"],
        "native_cap_scale_edit_read_back": abs(diffs["LOWER_RETURN_PROFILE"] - abs(float(delta_scale))) <= edit_tolerance,
        "native_source_restored_exactly": max(restored_error.values()) <= restore_tolerance,
        "cap_relation_semantics_preserved": base.own(edited, "LOWER_RETURN_PROFILE").get("termination_cap_semantics") == r2.CAP_SEMANTICS,
        "cap_relation_law_preserved": base.own(edited, "LOWER_RETURN_PROFILE").get("termination_cap_law") == r2.CAP_LAW,
    }
    return {
        "edit": {
            "object": NAMES["LOWER_RETURN_PROFILE"],
            "property": "termination_cap_pole_curvature_scale",
            "delta": float(delta_scale),
            "semantics": r2.CAP_SEMANTICS,
        },
        "source_family_differences": diffs,
        "changed_families": changed,
        "restored_source_error": restored_error,
        "checks": checks,
        "pass": all(checks.values()),
    }


def authority_checks(template: dict[str, Any], readback_tolerance: float = 1e-8, locked_semantic_tolerance: float = 1e-8):
    extracted = extract_native_source(template)
    diffs = source_difference(template, extracted)
    objects = [bpy.data.objects.get(name) for name in NAMES.values()]
    present = len(objects) == 6 and all(o is not None for o in objects)
    deck = bpy.data.objects.get(NAMES["INTERFACE_DECK_BOUNDARY"])
    lower_obj = bpy.data.objects.get(NAMES["LOWER_RETURN_PROFILE"])
    lower_template = base.own(template, "LOWER_RETURN_PROFILE")
    locked_theta_ok = bool(deck is not None and abs(float(deck.get("theta_center_rad", 0.0))) <= locked_semantic_tolerance)
    termination_relation_present = bool(lower_obj is not None and "termination_envelope_exponent" in lower_obj)
    termination_relation_semantics_ok = bool(
        lower_obj is not None
        and lower_obj.get("termination_envelope_semantics") == "SHARED_CROSS_SECTION_TERMINATION_ENVELOPE"
    )
    cap_expected = "termination_cap_onset_u" in lower_template
    cap_relation_present = bool(lower_obj is not None and "termination_cap_onset_u" in lower_obj)
    cap_scale_expected = "termination_cap_pole_curvature_scale" in lower_template
    cap_scale_present = bool(lower_obj is not None and "termination_cap_pole_curvature_scale" in lower_obj)
    cap_relation_semantics_ok = bool(
        lower_obj is not None
        and lower_obj.get("termination_cap_semantics") == r2.CAP_SEMANTICS
        and lower_obj.get("termination_cap_law") == r2.CAP_LAW
        and lower_obj.get("termination_cap_endpoint_section") == r2.CAP_ENDPOINT_SECTION
    )
    checks = {
        "six_native_source_objects_present": present,
        "all_native_source_objects_editable": present and all(bool(o.get("OLEANDER_EDITABLE", False)) for o in objects),
        "all_native_source_objects_working_source": present and all(o.get("OLEANDER_AUTHORITY") == "WORKING_SURFACE_SOURCE" for o in objects),
        "bootstrap_roundtrip_within_blender_representation_tolerance": max(diffs.values()) <= readback_tolerance,
        "locked_top_meridian_semantic_preserved": locked_theta_ok,
        "native_shared_termination_relation_present": termination_relation_present,
        "native_shared_termination_relation_semantics_preserved": termination_relation_semantics_ok,
        "native_cap_relation_present_when_expected": (not cap_expected) or cap_relation_present,
        "native_cap_relation_semantics_preserved_when_expected": (not cap_expected) or cap_relation_semantics_ok,
        "native_cap_pole_scale_present_when_expected": (not cap_scale_expected) or cap_scale_present,
    }
    return extracted, diffs, checks
