#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Callable

import bpy

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import g1_geometry_core as base
import g1_r2_core as r2
import g1_r2_qa as qa
import g1_r2_blender_roundtrip as rt
import g1_r2_blender_scene as bs
import g1_r2_topology_isolation as iso


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--execution-contract", required=True)
    p.add_argument("--binding", required=True)
    p.add_argument("--contract", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--resolution", type=int, default=640)
    return p.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(float(v) for v in values)
    rank = (len(ordered) - 1) * q
    lo = int(math.floor(rank))
    hi = int(math.ceil(rank))
    if lo == hi:
        return ordered[lo]
    f = rank - lo
    return ordered[lo] * (1.0 - f) + ordered[hi] * f


def vsub(a, b):
    return tuple(float(a[i]) - float(b[i]) for i in range(3))


def vadd(a, b):
    return tuple(float(a[i]) + float(b[i]) for i in range(3))


def vscale(a, s: float):
    return tuple(float(v) * float(s) for v in a)


def cross(a, b):
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def dot(a, b):
    return sum(float(a[i]) * float(b[i]) for i in range(3))


def unit(a):
    n = math.sqrt(dot(a, a))
    if n <= 1e-14:
        raise RuntimeError("Degenerate diagnostic normal")
    return tuple(float(v) / n for v in a)


def angle(a, b) -> float:
    return math.degrees(math.acos(max(-1.0, min(1.0, dot(a, b)))))


def derivative_vec(fn: Callable[[float], tuple[float, float, float]], u: float, h: float = 1e-5):
    lo = max(0.000001, u - h)
    hi = min(0.999999, u + h)
    return vscale(vsub(fn(hi), fn(lo)), 1.0 / (hi - lo))


def derivative_scalar(fn: Callable[[float], float], u: float, h: float = 1e-5) -> float:
    lo = max(0.000001, u - h)
    hi = min(0.999999, u + h)
    return (float(fn(hi)) - float(fn(lo))) / (hi - lo)


def smootherstep(t: float) -> float:
    x = max(0.0, min(1.0, float(t)))
    return x * x * x * (x * (x * 6.0 - 15.0) + 10.0)


def axis_point(source: dict[str, Any], u: float):
    return tuple(float(v) for v in base.bezier(base.own(source, "GRIP_AXIS")["control_points"], u))


def axis_derivative(source: dict[str, Any], u: float):
    return derivative_vec(lambda x: axis_point(source, x), u)


def envelope(source: dict[str, Any], u: float) -> float:
    exponent = float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))
    if not 0.0 < u < 1.0:
        return 0.0
    return math.sin(math.pi * u) ** exponent


def profile_value(source: dict[str, Any], family: str, u: float) -> float:
    return float(base.bezier(base.own(source, family)["control_values"], u))


def profile_derivative(source: dict[str, Any], family: str, u: float) -> float:
    return derivative_scalar(lambda x: profile_value(source, family, x), u)


def section_state(source: dict[str, Any], u: float, theta: float, symmetric: bool = False):
    top = profile_value(source, "PALM_PROFILE", u)
    thumb = profile_value(source, "THUMB_SIDE_PLAN", u)
    opposite = profile_value(source, "OPPOSITE_SIDE_PLAN", u)
    lower = profile_value(source, "LOWER_RETURN_PROFILE", u)

    dtop = profile_derivative(source, "PALM_PROFILE", u)
    dthumb = profile_derivative(source, "THUMB_SIDE_PLAN", u)
    dopposite = profile_derivative(source, "OPPOSITE_SIDE_PLAN", u)
    dlower = profile_derivative(source, "LOWER_RETURN_PROFILE", u)

    if symmetric:
        lateral = 0.5 * (thumb + opposite)
        dlateral = 0.5 * (dthumb + dopposite)
        vertical = 0.5 * (top + lower)
        dvertical = 0.5 * (dtop + dlower)
        thumb = opposite = lateral
        dthumb = dopposite = dlateral
        top = lower = vertical
        dtop = dlower = dvertical

    sn = math.sin(theta)
    cs = math.cos(theta)

    lat_a = 0.5 * (thumb + opposite)
    lat_b = 0.5 * (thumb - opposite)
    dlat_a = 0.5 * (dthumb + dopposite)
    dlat_b = 0.5 * (dthumb - dopposite)

    ver_a = 0.5 * (top + lower)
    ver_b = 0.5 * (top - lower)
    dver_a = 0.5 * (dtop + dlower)
    dver_b = 0.5 * (dtop - dlower)

    lateral = lat_a + lat_b * sn
    dlateral = dlat_a + dlat_b * sn
    vertical = ver_a + ver_b * cs
    dvertical = dver_a + dver_b * cs

    raw = (0.0, lateral * sn, vertical * cs)
    raw_u = (0.0, dlateral * sn, dvertical * cs)
    raw_theta = (
        0.0,
        lat_a * cs + 2.0 * lat_b * sn * cs,
        -ver_a * sn - 2.0 * ver_b * sn * cs,
    )
    return raw, raw_u, raw_theta


def differential_normal(
    source: dict[str, Any],
    u: float,
    theta: float,
    mode: str,
    center_u: float,
    contract: dict[str, Any],
):
    symmetric = mode in {"CROSS_SECTION_SYMMETRY_NEUTRAL", "COMBINED_NEUTRAL"}
    raw, raw_u, raw_theta = section_state(source, u, theta, symmetric=symmetric)

    start = float(contract["analytic_probe"]["diagnostic_intervention_start_u"])
    env = envelope(source, u)
    env_u = derivative_scalar(lambda x: envelope(source, x), u)

    if mode in {"SINGLE_POLE_COLLAPSE_NEUTRAL", "COMBINED_NEUTRAL"} and u >= start:
        env = envelope(source, start)
        env_u = 0.0

    radial_u = vadd(vscale(raw, env_u), vscale(raw_u, env))
    radial_theta = vscale(raw_theta, env)

    if mode in {"AXIS_TANGENT_NEUTRAL", "COMBINED_NEUTRAL"}:
        g_u = axis_derivative(source, center_u)
    else:
        g_u = axis_derivative(source, u)

    return unit(cross(vadd(g_u, radial_u), radial_theta))


def turn_row(source: dict[str, Any], u: float, mode: str, contract: dict[str, Any]):
    span = float(contract["analytic_probe"]["normal_turn_span_u"])
    half = 0.5 * span
    um = max(0.00001, u - half)
    up = min(0.9999, u + half)
    theta_samples = int(contract["analytic_probe"]["theta_samples"])
    turns: list[tuple[float, float]] = []
    for j in range(theta_samples):
        theta = 2.0 * math.pi * j / theta_samples
        a = differential_normal(source, um, theta, mode, u, contract)
        b = differential_normal(source, up, theta, mode, u, contract)
        turns.append((angle(a, b), theta))
    hotspot_turn, hotspot_theta = max(turns, key=lambda x: x[0])
    return {
        "u": u,
        "normal_turn_span_u": up - um,
        "max_normal_turn_deg": hotspot_turn,
        "p95_normal_turn_deg": percentile([v for v, _ in turns], 0.95),
        "hotspot_theta_rad": hotspot_theta,
        "hotspot_theta_deg": math.degrees(hotspot_theta),
    }


def direct_turn_row(source: dict[str, Any], u: float, contract: dict[str, Any]):
    span = float(contract["analytic_probe"]["normal_turn_span_u"])
    half = 0.5 * span
    um = max(0.00001, u - half)
    up = min(0.9999, u + half)
    theta_samples = int(contract["analytic_probe"]["theta_samples"])
    turns = []
    for j in range(theta_samples):
        theta = 2.0 * math.pi * j / theta_samples
        turns.append((qa.ang(qa.normal(source, um, theta), qa.normal(source, up, theta)), theta))
    value, theta = max(turns, key=lambda x: x[0])
    return {"u": u, "max_normal_turn_deg": value, "hotspot_theta_rad": theta}


def analytic_probe(source: dict[str, Any], contract: dict[str, Any]):
    modes = list(contract["counterfactuals"])
    sample_u = [float(v) for v in contract["analytic_probe"]["sample_u"]]
    near_min = float(contract["analytic_probe"]["near_pole_u_min"])
    pre_max = float(contract["analytic_probe"]["pre_cap_u_max"])

    rows = {mode: [turn_row(source, u, mode, contract) for u in sample_u] for mode in modes}
    direct = [direct_turn_row(source, u, contract) for u in sample_u]

    summary = {}
    for mode, data in rows.items():
        summary[mode] = {
            "pre_cap_max_normal_turn_deg": max(r["max_normal_turn_deg"] for r in data if r["u"] <= pre_max),
            "near_pole_max_normal_turn_deg": max(r["max_normal_turn_deg"] for r in data if r["u"] >= near_min),
            "near_pole_p95_max_normal_turn_deg": max(r["p95_normal_turn_deg"] for r in data if r["u"] >= near_min),
        }

    baseline = float(summary["BASELINE"]["near_pole_max_normal_turn_deg"])
    reductions = {}
    for mode in modes:
        current = float(summary[mode]["near_pole_max_normal_turn_deg"])
        reductions[mode] = 0.0 if mode == "BASELINE" else (baseline - current) / baseline

    direct_near = max(r["max_normal_turn_deg"] for r in direct if r["u"] >= near_min)
    full_near = summary["BASELINE"]["near_pole_max_normal_turn_deg"]
    direct_error = abs(direct_near - full_near)

    h = contract["routing_heuristics"]
    axis_r = reductions["AXIS_TANGENT_NEUTRAL"]
    sym_r = reductions["CROSS_SECTION_SYMMETRY_NEUTRAL"]
    pole_r = reductions["SINGLE_POLE_COLLAPSE_NEUTRAL"]
    combined_r = reductions["COMBINED_NEUTRAL"]

    if (
        pole_r >= float(h["single_pole_dominant_min_reduction_fraction"])
        and axis_r <= float(h["axis_or_symmetry_max_reduction_for_single_pole_dominant"])
        and sym_r <= float(h["axis_or_symmetry_max_reduction_for_single_pole_dominant"])
        and combined_r >= float(h["combined_min_reduction_fraction"])
    ):
        classification = "SINGLE_POLE_COLLAPSE_CONSTRUCTION_DOMINANT_EXISTING_RELATION_SET_INSUFFICIENT"
    elif axis_r >= max(sym_r, pole_r) + float(h["dominant_margin_fraction"]):
        classification = "GRIP_AXIS_ENDPOINT_TANGENT_DOMINANT"
    elif sym_r >= max(axis_r, pole_r) + float(h["dominant_margin_fraction"]):
        classification = "CROSS_SECTION_ASYMMETRY_DOMINANT"
    elif combined_r >= 0.50:
        classification = "MIXED_TERMINATION_CONSTRUCTION_INTERACTION"
    else:
        classification = "INCONCLUSIVE_REVISE"

    return {
        "method": "LOCAL_DIFFERENTIAL_CONSTRUCTION_COUNTERFACTUAL",
        "rows": rows,
        "direct_r2_control_rows": direct,
        "summary": summary,
        "near_pole_reduction_fraction_vs_baseline": reductions,
        "direct_vs_differential_near_pole_error_deg": direct_error,
        "classification": classification,
    }


def set_confirmed_interface(deck: Any, relation: dict[str, Any]) -> None:
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        deck[key] = float(relation[key])
    deck["theta_center_rad"] = 0.0
    deck["theta_center_semantics"] = str(relation["theta_center"])
    deck["blend"] = str(relation["blend"])


def visual_weight(u: float, contract: dict[str, Any]) -> float:
    start = float(contract["visual_geometry"]["blend_start_u"])
    full = float(contract["visual_geometry"]["blend_full_u"])
    if u <= start:
        return 0.0
    if u >= full:
        return 1.0
    return smootherstep((u - start) / (full - start))


def visual_axis(source: dict[str, Any], u: float, mode: str, contract: dict[str, Any]):
    current = axis_point(source, u)
    if mode not in {"AXIS_TANGENT_NEUTRAL", "COMBINED_NEUTRAL"}:
        return current
    start = float(contract["visual_geometry"]["blend_start_u"])
    if u <= start:
        return current
    g0 = axis_point(source, start)
    dg0 = axis_derivative(source, start)
    return vadd(g0, vscale(dg0, u - start))


def diagnostic_point(source: dict[str, Any], u: float, theta: float, mode: str, contract: dict[str, Any]):
    if mode == "BASELINE" or u <= float(contract["visual_geometry"]["blend_start_u"]):
        return r2.point(source, u, theta, False, True)

    g = visual_axis(source, u, mode, contract)
    w = visual_weight(u, contract)

    top = profile_value(source, "PALM_PROFILE", u)
    thumb = profile_value(source, "THUMB_SIDE_PLAN", u)
    opposite = profile_value(source, "OPPOSITE_SIDE_PLAN", u)
    lower = profile_value(source, "LOWER_RETURN_PROFILE", u)

    if mode in {"CROSS_SECTION_SYMMETRY_NEUTRAL", "COMBINED_NEUTRAL"}:
        lateral = 0.5 * (thumb + opposite)
        vertical = 0.5 * (top + lower)
        thumb = (1.0 - w) * thumb + w * lateral
        opposite = (1.0 - w) * opposite + w * lateral
        top = (1.0 - w) * top + w * vertical
        lower = (1.0 - w) * lower + w * vertical

    env = envelope(source, u)
    if mode in {"SINGLE_POLE_COLLAPSE_NEUTRAL", "COMBINED_NEUTRAL"}:
        start = float(contract["visual_geometry"]["blend_start_u"])
        frozen = envelope(source, start)
        env = (1.0 - w) * env + w * frozen

    top *= env
    thumb *= env
    opposite *= env
    lower *= env

    sn = math.sin(theta)
    cs = math.cos(theta)
    lateral = 0.5 * (thumb + opposite) + 0.5 * (thumb - opposite) * sn
    vertical = 0.5 * (top + lower) + 0.5 * (top - lower) * cs
    return (
        float(g[0]),
        float(g[1]) + lateral * sn,
        float(g[2]) + vertical * cs,
    )


def custom_mesh(source: dict[str, Any], mode: str, contract: dict[str, Any]):
    spec = contract["visual_geometry"]
    nu = int(spec["base_u_rings"])
    nv = int(spec["circumferential_samples"])
    u_values = [i / (nu + 1) for i in range(1, nu + 1)]
    u_values.extend(float(v) for v in spec["extra_u_rings"])
    u_values = sorted(set(v for v in u_values if v < 1.0))

    verts = [diagnostic_point(source, 0.0, 0.0, mode, contract)]
    faces = []
    for u in u_values:
        for j in range(nv):
            verts.append(diagnostic_point(source, u, 2.0 * math.pi * j / nv, mode, contract))

    if mode in {"AXIS_TANGENT_NEUTRAL", "COMBINED_NEUTRAL"}:
        pole = visual_axis(source, 1.0, mode, contract)
    else:
        pole = axis_point(source, 1.0)
    back = len(verts)
    verts.append(tuple(float(v) for v in pole))

    for j in range(nv):
        faces.append((0, 1 + j, 1 + (j + 1) % nv))
    for i in range(len(u_values) - 1):
        a = 1 + i * nv
        b = a + nv
        for j in range(nv):
            n = (j + 1) % nv
            faces.append((a + j, b + j, b + n, a + n))
    last = 1 + (len(u_values) - 1) * nv
    for j in range(nv):
        faces.append((last + j, back, last + (j + 1) % nv))
    return verts, faces, u_values


def replace_diagnostic(name: str, source: dict[str, Any], mode: str, contract: dict[str, Any], collection: Any):
    old = bpy.data.objects.get(name)
    if old is not None:
        mesh = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    verts, faces, u_values = custom_mesh(source, mode, contract)
    obj = bs.mesh_obj(name, verts, faces, collection, f"R4.4 {mode} diagnostic counterfactual")
    obj["OLEANDER_R4_4_MODE"] = mode
    obj["OLEANDER_DIAGNOSTIC_ONLY"] = True
    obj["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"
    return obj, verts, faces, u_values


def render_set(surface_runtime: Any, binding: dict[str, Any], out: Path, qa_collection: Any, obj: Any, camera: Any, prefix: str):
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    reflection = iso.require_surface_asset(profile["reflection"]["name"], "material")
    zebra = iso.require_surface_asset(profile["zebra"]["name"], "material")
    result = {}
    for rig in ("STRIP", "GRAZING", "ZEBRA"):
        mat = zebra if rig == "ZEBRA" else reflection
        stem = f"{prefix}_{rig}"
        result[rig] = surface_runtime.render(bpy.context.scene, out, stem, camera, obj, mat, rig, qa_collection)
    return result


def main() -> int:
    a = args()
    seed = load(a.source)
    r2_fix = load(a.r2_correction)
    confirmed = load(a.confirmed_interface)
    execution = load(a.execution_contract)
    binding = load(a.binding)
    contract = load(a.contract)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if contract["policy"]["authoritative_source_edit_forbidden"] is not True:
        raise RuntimeError("R4.4 must remain diagnostic-only")

    template = r2.apply(seed, r2_fix)
    r2_native = rt.extract_native_source(template)
    native_digest_before = iso.source_digest(r2_native)

    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    if deck is None:
        raise RuntimeError("Blender-native INTERFACE_DECK_BOUNDARY source object missing")
    original_deck = {
        key: deck[key]
        for key in (
            "u_center",
            "u_halfspan",
            "theta_halfspan_rad",
            "core_fraction",
            "depth_m",
            "theta_center_rad",
            "theta_center_semantics",
            "blend",
        )
    }
    set_confirmed_interface(deck, confirmed["source_overrides"])
    working_source = rt.extract_native_source(template)
    working_digest = iso.source_digest(working_source)
    interface_diff = rt.source_difference(r2_native, working_source)

    for key, value in original_deck.items():
        deck[key] = value
    restored = rt.extract_native_source(template)
    restore_error = rt.source_difference(r2_native, restored)
    native_digest_after = iso.source_digest(restored)

    exponent = float(base.own(working_source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))
    machine, _ = qa.evaluate(working_source, r2_fix, False)
    analytic = analytic_probe(working_source, contract)

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20

    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections missing")

    objects = {}
    geometry = {}
    for mode in contract["counterfactuals"]:
        name = f"OL_DERIVED_G1_R4_4_{mode}"
        obj, verts, faces, u_values = replace_diagnostic(name, working_source, mode, contract, derived_collection)
        obj["OLEANDER_SOURCE_DIGEST"] = working_digest
        objects[mode] = obj
        geometry[mode] = {
            "vertices": len(verts),
            "faces": len(faces),
            "last_ring_u": max(u_values),
            "authority": obj.get("OLEANDER_AUTHORITY"),
            "diagnostic_only": bool(obj.get("OLEANDER_DIAGNOSTIC_ONLY")),
            "source_digest": obj.get("OLEANDER_SOURCE_DIGEST"),
        }

    local = contract["local_view"]
    target_u = float(local["target_u"])
    target = axis_point(working_source, target_u)
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(float(target[i]) + offset[i] for i in range(3))
    old = bpy.data.objects.get(local["name"])
    if old is not None:
        bpy.data.objects.remove(old, do_unlink=True)
    camera = surface_runtime.camera(local["name"], float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_4_ROLE"] = "TERMINATION_CONSTRUCTION_SUFFICIENCY_CAMERA"

    renders = {}
    for mode, obj in objects.items():
        iso.set_only_rendered(derived_collection, obj)
        renders[mode] = render_set(
            surface_runtime,
            binding,
            out,
            qa_collection,
            obj,
            camera,
            f"R4_4_{mode}",
        )

    image_diffs = {}
    for mode in contract["counterfactuals"]:
        if mode == "BASELINE":
            continue
        image_diffs[mode] = {
            rig: iso.image_difference(out / renders["BASELINE"][rig], out / renders[mode][rig])
            for rig in ("STRIP", "GRAZING", "ZEBRA")
        }

    direct_tolerance = float(contract["analytic_probe"]["direct_vs_differential_control_max_error_deg"])
    reductions = analytic["near_pole_reduction_fraction_vs_baseline"]
    h = contract["routing_heuristics"]

    checks = {
        "source_digest_restored_exactly": native_digest_before == native_digest_after
        and max(restore_error.values()) <= 1e-12,
        "confirmed_interface_is_only_temporary_native_difference": [
            k for k, v in interface_diff.items() if v > 1e-8
        ] == ["INTERFACE_DECK_BOUNDARY"],
        "confirmed_interface_locked_in_working_source": base.own(working_source, "INTERFACE_DECK_BOUNDARY")["theta_center"] == "TOP_MERIDIAN"
        and abs(float(base.own(working_source, "INTERFACE_DECK_BOUNDARY")["u_halfspan"]) - 0.26) <= 1e-12
        and abs(float(base.own(working_source, "INTERFACE_DECK_BOUNDARY")["theta_halfspan_rad"]) - 1.06) <= 1e-12
        and abs(float(base.own(working_source, "INTERFACE_DECK_BOUNDARY")["core_fraction"]) - 0.29) <= 1e-12,
        "termination_exponent_locked_at_0_34": abs(exponent - float(contract["policy"]["termination_envelope_exponent_locked"])) <= 1e-12,
        "existing_machine_qa_passes": all(machine["checks"].values()),
        "direct_vs_differential_baseline_control_within_tolerance": analytic["direct_vs_differential_near_pole_error_deg"] <= direct_tolerance,
        "single_pole_counterfactual_has_material_effect": reductions["SINGLE_POLE_COLLAPSE_NEUTRAL"] >= float(h["single_pole_dominant_min_reduction_fraction"]),
        "axis_counterfactual_is_not_individually_dominant": reductions["AXIS_TANGENT_NEUTRAL"] <= float(h["axis_or_symmetry_max_reduction_for_single_pole_dominant"]),
        "symmetry_counterfactual_is_not_individually_dominant": reductions["CROSS_SECTION_SYMMETRY_NEUTRAL"] <= float(h["axis_or_symmetry_max_reduction_for_single_pole_dominant"]),
        "combined_counterfactual_reduces_near_pole_turn": reductions["COMBINED_NEUTRAL"] >= float(h["combined_min_reduction_fraction"]),
        "analytic_classification_not_inconclusive": analytic["classification"] != "INCONCLUSIVE_REVISE",
        "all_counterfactuals_same_sampling": len({(row["vertices"], row["faces"], row["last_ring_u"]) for row in geometry.values()}) == 1,
        "all_counterfactuals_derived_not_authority": all(row["authority"] == "DERIVED_EXECUTION_NOT_AUTHORITY" for row in geometry.values()),
        "all_counterfactuals_diagnostic_only": all(row["diagnostic_only"] for row in geometry.values()),
        "same_confirmed_source_digest_tagged_on_all_counterfactuals": len({row["source_digest"] for row in geometry.values()}) == 1
        and next(iter({row["source_digest"] for row in geometry.values()})) == working_digest,
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "camera_created_via_shared_runtime": camera.get("OLEANDER_ROLE") == "F1_DIAGNOSTIC_CAMERA",
        "all_fixed_rig_renders_written": all((out / name).exists() for group in renders.values() for name in group.values()),
        "candidate_promotion_not_run": contract["policy"]["candidate_promotion"] == "NOT_RUN",
    }

    status = (
        "R4_4_CONSTRUCTION_SUFFICIENCY_ISOLATION_EXECUTED_VISUAL_REVIEW_REQUIRED"
        if all(checks.values())
        else "R4_4_CONSTRUCTION_SUFFICIENCY_ISOLATION_FAIL_REVISE"
    )

    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.4.termination-construction-sufficiency-report.v1",
        "status": status,
        "job_state": "R4_4_DIAGNOSTIC_ONLY_TERMINATION_CONSTRUCTION_SUFFICIENCY_ISOLATION_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "interface_relation_state": "CONFIRMED_LOCKED_FOR_R4_4",
        "termination_state": "REVISE_CONSTRUCTION_SUFFICIENCY_UNDER_REVIEW",
        "source_digest": working_digest,
        "termination_envelope_exponent": exponent,
        "checks": checks,
        "analytic_probe": analytic,
        "analytic_classification": analytic["classification"],
        "visual_classification": "NOT_RUN_REQUIRES_FIXED_STRIP_GRAZING_ZEBRA_REVIEW",
        "counterfactual_geometry": geometry,
        "renders": renders,
        "image_difference_metrics_vs_baseline": image_diffs,
        "surface_system_runtime": runtime_identity,
        "next_legal_action": (
            "Review the fixed-rig counterfactuals. If visual evidence agrees that forced single-pole collapse is dominant, "
            "R4.5 may define one explicit sparse Source-level termination-cap relation. Do not edit existing Source in R4.4."
        ),
        "boundary": contract["boundary"],
    }
    (out / "G1_R4_4_TERMINATION_CONSTRUCTION_SUFFICIENCY_REPORT.json").write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
