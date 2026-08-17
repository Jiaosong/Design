#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from pathlib import Path
from typing import Any

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

CAP_KEYS = (
    "termination_cap_onset_u",
    "termination_cap_law",
    "termination_cap_semantics",
    "termination_cap_endpoint_section",
    "termination_cap_numeric_dof_count",
)


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


def dist(a, b) -> float:
    return math.dist(tuple(float(v) for v in a), tuple(float(v) for v in b))


def axis_point(source: dict[str, Any], u: float):
    return tuple(float(v) for v in base.bezier(base.own(source, "GRIP_AXIS")["control_points"], u))


def set_confirmed_interface(deck: Any, relation: dict[str, Any]) -> None:
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        deck[key] = float(relation[key])
    deck["theta_center_rad"] = 0.0
    deck["theta_center_semantics"] = str(relation["theta_center"])
    deck["blend"] = str(relation["blend"])


def bind_cap(lower_obj: Any, onset: float) -> None:
    lower_obj["termination_cap_onset_u"] = float(onset)
    lower_obj["termination_cap_law"] = r2.CAP_LAW
    lower_obj["termination_cap_semantics"] = r2.CAP_SEMANTICS
    lower_obj["termination_cap_endpoint_section"] = r2.CAP_ENDPOINT_SECTION
    lower_obj["termination_cap_numeric_dof_count"] = 1


def clear_cap(lower_obj: Any) -> None:
    for key in CAP_KEYS:
        if key in lower_obj:
            del lower_obj[key]


def max_position_regression(reference, candidate, u_samples, theta_samples: int) -> float:
    error = 0.0
    for u in u_samples:
        for j in range(theta_samples):
            t = 2.0 * math.pi * j / theta_samples
            error = max(error, dist(r2.point(reference, u, t, False, True), r2.point(candidate, u, t, False, True)))
    return error


def onset_continuity(reference, candidate, onset: float, epsilon: float, theta_samples: int):
    pos = 0.0
    normal = 0.0
    for j in range(theta_samples):
        t = 2.0 * math.pi * j / theta_samples
        pos = max(pos, dist(r2.point(reference, onset, t, False, True), r2.point(candidate, onset, t, False, True)))
        normal = max(
            normal,
            qa.ang(
                qa.normal(candidate, max(0.00001, onset - epsilon), t),
                qa.normal(candidate, min(0.99999, onset + epsilon), t),
            ),
        )
    return pos, normal


def normal_turn(candidate, u: float, span: float, theta_samples: int):
    half = 0.5 * span
    lo = max(0.00001, u - half)
    hi = min(0.99999, u + half)
    values = []
    for j in range(theta_samples):
        t = 2.0 * math.pi * j / theta_samples
        values.append(qa.ang(qa.normal(candidate, lo, t), qa.normal(candidate, hi, t)))
    ordered = sorted(values)
    p95 = ordered[min(len(ordered) - 1, int(math.floor(0.95 * (len(ordered) - 1))))]
    return max(values), p95


def cap_turn_probe(candidate: dict[str, Any], onset: float, gate: dict[str, Any]):
    span = float(gate["cap_turn_span_u"])
    theta_samples = int(gate["theta_samples"])
    rows = []
    for tau in gate["cap_tau_samples"]:
        u = onset + (1.0 - onset) * float(tau)
        mx, p95 = normal_turn(candidate, u, span, theta_samples)
        rows.append({"tau": float(tau), "u": u, "max_normal_turn_deg": mx, "p95_normal_turn_deg": p95})
    near = []
    for u in gate["near_pole_samples"]:
        mx, p95 = normal_turn(candidate, float(u), span, theta_samples)
        near.append({"u": float(u), "max_normal_turn_deg": mx, "p95_normal_turn_deg": p95})
    return {
        "rows": rows,
        "near_pole_rows": near,
        "cap_region_max_normal_turn_deg": max(row["max_normal_turn_deg"] for row in rows),
        "near_pole_max_normal_turn_deg": max(row["max_normal_turn_deg"] for row in near),
    }


def radial_monotonicity(candidate: dict[str, Any], onset: float, samples: int, theta_samples: int, tolerance: float):
    means = []
    maxima = []
    for i in range(samples):
        u = onset + (0.999 - onset) * i / (samples - 1)
        g = axis_point(candidate, u)
        radii = []
        for j in range(theta_samples):
            t = 2.0 * math.pi * j / theta_samples
            radii.append(dist(r2.point(candidate, u, t, False, False), g))
        means.append({"u": u, "mean_radius_m": sum(radii) / len(radii), "max_radius_m": max(radii)})
    mean_violations = sum(1 for a, b in zip(means, means[1:]) if b["mean_radius_m"] > a["mean_radius_m"] + tolerance)
    max_violations = sum(1 for a, b in zip(means, means[1:]) if b["max_radius_m"] > a["max_radius_m"] + tolerance)
    return {"rows": means, "mean_radius_increase_count": mean_violations, "max_radius_increase_count": max_violations}


def closure_error(candidate: dict[str, Any], theta_samples: int) -> float:
    pole = axis_point(candidate, 1.0)
    return max(dist(r2.point(candidate, 1.0, 2.0 * math.pi * j / theta_samples, False, False), pole) for j in range(theta_samples))


def evaluate_variant(reference: dict[str, Any], candidate: dict[str, Any], onset: float, contract: dict[str, Any], r2_fix: dict[str, Any]):
    policy = contract["policy"]
    gate = contract["machine_gate"]
    candidate = copy.deepcopy(candidate)
    candidate["machine_thresholds"]["max_sparse_authority_scalar_count"] = int(
        policy["max_sparse_authority_scalar_count_with_cap_relation"]
    )
    machine, _ = qa.evaluate(candidate, r2_fix, False)
    legacy_required = {k: v for k, v in machine["checks"].items() if k not in {"broad_long", "broad_circ"}}
    position_continuity, normal_continuity = onset_continuity(
        reference,
        candidate,
        onset,
        float(gate["onset_probe_epsilon_u"]),
        int(gate["theta_samples"]),
    )
    interface_regression = max_position_regression(
        reference,
        candidate,
        [float(v) for v in gate["interface_regression_u_samples"]],
        int(gate["interface_regression_theta_samples"]),
    )
    turns = cap_turn_probe(candidate, onset, gate)
    radial = radial_monotonicity(
        candidate,
        onset,
        int(gate["radial_monotonic_samples"]),
        int(gate["theta_samples"]),
        float(gate["radial_monotonic_tolerance_m"]),
    )
    close_error = closure_error(candidate, int(gate["theta_samples"]))
    extra_rings = len(r2._u_values(candidate)) - int(candidate["derived_execution"]["u_rings"])
    lower = base.own(candidate, "LOWER_RETURN_PROFILE")
    checks = {
        "legacy_machine_contract_outside_cap_passes": all(legacy_required.values()),
        "sparse_authority_count_is_49_or_less": machine["sparse_scalar_count"] <= int(policy["max_sparse_authority_scalar_count_with_cap_relation"]),
        "only_one_new_numeric_cap_dof": int(contract["relation_vocabulary"]["numeric_dof_count"]) == 1,
        "cap_relation_owner_is_existing_lower_return_family": contract["source_owner_family"] == "LOWER_RETURN_PROFILE",
        "cap_semantics_exact": lower.get("termination_cap_semantics") == r2.CAP_SEMANTICS,
        "cap_law_exact": lower.get("termination_cap_law") == r2.CAP_LAW,
        "cap_endpoint_section_exact": lower.get("termination_cap_endpoint_section") == r2.CAP_ENDPOINT_SECTION,
        "onset_does_not_precede_confirmed_interface_outer_u": onset >= float(policy["confirmed_interface_outer_u_max"]),
        "onset_position_continuity": position_continuity <= float(gate["onset_position_continuity_max_m"]),
        "onset_normal_continuity": normal_continuity <= float(gate["onset_normal_continuity_max_deg"]),
        "confirmed_interface_zero_regression": interface_regression <= float(gate["interface_regression_max_displacement_m"]),
        "cap_region_normal_turn": turns["cap_region_max_normal_turn_deg"] <= float(gate["cap_region_max_normal_turn_deg"]),
        "near_pole_normal_turn": turns["near_pole_max_normal_turn_deg"] <= float(gate["near_pole_max_normal_turn_deg"]),
        "radial_mean_monotonic": radial["mean_radius_increase_count"] == 0,
        "radial_max_monotonic": radial["max_radius_increase_count"] == 0,
        "single_pole_closure_exact": close_error <= float(gate["closure_position_tolerance_m"]),
        "cap_aware_execution_sampling_present": extra_rings >= int(gate["minimum_cap_aware_extra_u_rings"]),
        "candidate_promotion_not_run": policy["candidate_promotion"] == "NOT_RUN",
    }
    return {
        "machine_pass": all(checks.values()),
        "checks": checks,
        "legacy_machine_report": machine,
        "legacy_checks_excluding_replaced_cap_fairness": legacy_required,
        "onset_position_continuity_error_m": position_continuity,
        "onset_normal_continuity_deg": normal_continuity,
        "interface_regression_max_displacement_m": interface_regression,
        "cap_turn_probe": turns,
        "radial_monotonicity": radial,
        "closure_position_error_m": close_error,
        "derived_cap_extra_u_rings": extra_rings,
    }, candidate


def replace_object(name: str, source: dict[str, Any], collection: Any):
    old = bpy.data.objects.get(name)
    if old is not None:
        mesh = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    verts, faces, _ = r2.mesh(source, False)
    obj = bs.mesh_obj(name, verts, faces, collection, "R4.5 cap-relation derived execution geometry")
    obj["OLEANDER_R4_5"] = True
    obj["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"
    obj["OLEANDER_SOURCE_DIGEST"] = iso.source_digest(source)
    return obj, len(verts), len(faces)


def render_set(surface_runtime: Any, binding: dict[str, Any], out: Path, qa_collection: Any, obj: Any, camera: Any, prefix: str):
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    reflection = iso.require_surface_asset(profile["reflection"]["name"], "material")
    zebra = iso.require_surface_asset(profile["zebra"]["name"], "material")
    result = {}
    for rig in ("STRIP", "GRAZING", "ZEBRA"):
        mat = zebra if rig == "ZEBRA" else reflection
        result[rig] = surface_runtime.render(bpy.context.scene, out, f"{prefix}_{rig}", camera, obj, mat, rig, qa_collection)
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

    prior = (HERE / "G1_R4_4_TERMINATION_CONSTRUCTION_SUFFICIENCY_DECISION_2026-08-14.md").read_text(encoding="utf-8")
    if "SINGLE_POLE_COLLAPSE_CONSTRUCTION_DOMINANT_EXISTING_RELATION_SET_INSUFFICIENT" not in prior:
        raise RuntimeError("R4.5 requires the closed R4.4 structural-insufficiency decision")

    template = r2.apply(seed, r2_fix)
    native_before = rt.extract_native_source(template)
    native_digest_before = iso.source_digest(native_before)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    lower_obj = bpy.data.objects.get(rt.NAMES["LOWER_RETURN_PROFILE"])
    if deck is None or lower_obj is None:
        raise RuntimeError("Expected Blender-native Source objects missing")

    original_deck = {key: deck[key] for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m", "theta_center_rad", "theta_center_semantics", "blend")}
    original_cap = {key: lower_obj[key] for key in CAP_KEYS if key in lower_obj}

    set_confirmed_interface(deck, confirmed["source_overrides"])
    clear_cap(lower_obj)
    reference = rt.extract_native_source(template)
    reference_digest = iso.source_digest(reference)

    variants = {}
    for variant_id, spec in contract["variants"].items():
        onset = float(spec["termination_cap_onset_u"])
        bind_cap(lower_obj, onset)
        extracted = rt.extract_native_source(template)
        result, evaluated = evaluate_variant(reference, extracted, onset, contract, r2_fix)
        result["termination_cap_onset_u"] = onset
        result["source_digest"] = iso.source_digest(evaluated)
        variants[variant_id] = {"result": result, "source": evaluated}

    machine_pass_ids = [key for key, row in variants.items() if row["result"]["machine_pass"]]
    if machine_pass_ids:
        first = machine_pass_ids[0]
        bind_cap(lower_obj, float(variants[first]["result"]["termination_cap_onset_u"]))
        roundtrip = rt.controlled_native_cap_relation_edit_test(template, delta_onset_u=0.005)
    else:
        roundtrip = {"pass": False, "checks": {"machine_pass_variant_required": False}}

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections missing")

    clear_cap(lower_obj)
    baseline_obj, baseline_v, baseline_f = replace_object("OL_DERIVED_G1_R4_5_BASELINE", reference, derived_collection)
    local = contract["local_view"]
    target = axis_point(reference, float(local["target_u"]))
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old_cam = bpy.data.objects.get(local["name"])
    if old_cam is not None:
        bpy.data.objects.remove(old_cam, do_unlink=True)
    camera = surface_runtime.camera(local["name"], float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_5_ROLE"] = "TERMINATION_CAP_RELATION_CAMERA"

    iso.set_only_rendered(derived_collection, baseline_obj)
    renders = {"BASELINE": render_set(surface_runtime, binding, out, qa_collection, baseline_obj, camera, "R4_5_BASELINE")}
    geometry = {
        "BASELINE": {"vertices": baseline_v, "faces": baseline_f, "authority": baseline_obj.get("OLEANDER_AUTHORITY"), "source_digest": reference_digest}
    }
    for variant_id in machine_pass_ids:
        source = variants[variant_id]["source"]
        obj, vc, fc = replace_object(f"OL_DERIVED_G1_R4_5_{variant_id}", source, derived_collection)
        iso.set_only_rendered(derived_collection, obj)
        renders[variant_id] = render_set(surface_runtime, binding, out, qa_collection, obj, camera, f"R4_5_{variant_id}")
        geometry[variant_id] = {"vertices": vc, "faces": fc, "authority": obj.get("OLEANDER_AUTHORITY"), "source_digest": obj.get("OLEANDER_SOURCE_DIGEST")}

    image_diffs = {}
    for variant_id in machine_pass_ids:
        image_diffs[variant_id] = {
            rig: iso.image_difference(out / renders["BASELINE"][rig], out / renders[variant_id][rig])
            for rig in ("STRIP", "GRAZING", "ZEBRA")
        }

    ranked = sorted(
        machine_pass_ids,
        key=lambda key: (
            variants[key]["result"]["cap_turn_probe"]["cap_region_max_normal_turn_deg"],
            variants[key]["result"]["cap_turn_probe"]["near_pole_max_normal_turn_deg"],
            variants[key]["result"]["termination_cap_onset_u"],
        ),
    )
    machine_preferred = ranked[0] if ranked else None

    for key, value in original_deck.items():
        deck[key] = value
    clear_cap(lower_obj)
    for key, value in original_cap.items():
        lower_obj[key] = value
    restored = rt.extract_native_source(template)
    restored_digest = iso.source_digest(restored)
    restore_error = rt.source_difference(native_before, restored)

    global_checks = {
        "r4_4_authorization_present": True,
        "relation_has_one_numeric_dof": int(contract["relation_vocabulary"]["numeric_dof_count"]) == 1,
        "owner_is_existing_source_family": contract["source_owner_family"] == "LOWER_RETURN_PROFILE",
        "blender_native_roundtrip_pass": bool(roundtrip.get("pass")),
        "shared_surface_runtime_pass": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "at_least_one_machine_pass_variant": len(machine_pass_ids) > 0,
        "all_rendered_variants_are_machine_pass": set(renders) - {"BASELINE"} == set(machine_pass_ids),
        "all_rendered_geometry_is_derived_not_authority": all(row["authority"] == "DERIVED_EXECUTION_NOT_AUTHORITY" for row in geometry.values()),
        "native_source_restored_exactly": native_digest_before == restored_digest and max(restore_error.values()) <= 1e-12,
        "candidate_promotion_not_run": contract["policy"]["candidate_promotion"] == "NOT_RUN",
    }
    status = "R4_5_CAP_RELATION_MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(global_checks.values()) else "R4_5_CAP_RELATION_MACHINE_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.5.termination-cap-relation-report.v1",
        "status": status,
        "job_state": "R4_5_SPARSE_CAP_RELATION_BATCH_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "relation_id": contract["relation_id"],
        "relation_vocabulary": contract["relation_vocabulary"],
        "reference_source_digest": reference_digest,
        "global_checks": global_checks,
        "roundtrip": roundtrip,
        "variants": {key: row["result"] for key, row in variants.items()},
        "machine_pass_variants": machine_pass_ids,
        "machine_preferred_variant": machine_preferred,
        "geometry": geometry,
        "renders": renders,
        "image_difference_metrics_vs_baseline": image_diffs,
        "surface_system_runtime": runtime_identity,
        "next_legal_action": "Review only Machine-PASS Strip/Grazing/Zebra variants. If one removes the R4.4 retained convergence without introducing a new cap kink/bulge, persist a separate confirmed Working Source cap relation receipt; otherwise revise R4.5 relation construction. Candidate Promotion remains blocked.",
        "boundary": contract["boundary"],
    }
    (out / "G1_R4_5_TERMINATION_CAP_RELATION_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("REQUIRED") else 9


if __name__ == "__main__":
    raise SystemExit(main())
