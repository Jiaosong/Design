#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
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
import g1_r2_topology_isolation as iso
import g1_r4_termination_isolation as r4
import g1_r4_2_profile_convergence_probe as r42


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--execution-contract", required=True)
    p.add_argument("--binding", required=True)
    p.add_argument("--r4-contract", required=True)
    p.add_argument("--r4-2-contract", required=True)
    p.add_argument("--variants", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--resolution", type=int, default=640)
    return p.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def set_interface(deck: Any, relation: dict[str, Any]) -> None:
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        deck[key] = float(relation[key])
    deck["theta_center_rad"] = 0.0
    deck["theta_center_semantics"] = str(relation["theta_center"])
    deck["blend"] = str(relation["blend"])


def set_profile_control(obj: Any, axis: str, index: int, value: float) -> None:
    point = obj.data.splines[0].points[index]
    if axis == "Y-":
        point.co[1] = -float(value)
    elif axis == "Z-":
        point.co[2] = -float(value)
    else:
        raise ValueError(f"Unsupported R4.3 profile axis: {axis}")


def read_profile_control(obj: Any, axis: str, index: int) -> float:
    point = obj.data.splines[0].points[index]
    if axis == "Y-":
        return float(-point.co[1])
    if axis == "Z-":
        return float(-point.co[2])
    raise ValueError(axis)


def machine_summary(source: dict[str, Any], r2_fix: dict[str, Any]) -> dict[str, Any]:
    result, _ = qa.evaluate(source, r2_fix, False)
    return {
        "pass": all(result["checks"].values()),
        "checks": result["checks"],
        "dimensions_m": result["dimensions_m"],
        "interface_depth_m": result["interface_depth_m"],
        "broad_fairness": result["broad_fairness"],
        "outer_continuity_deg": result["outer_continuity_deg"],
        "core_continuity_deg": result["core_continuity_deg"],
    }


def ownership_probe(source: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    rows = [r42.probe_row(source, contract, float(u)) for u in contract["sample_u"]]
    classification, evidence = r42.classify(rows, contract)
    return {
        "classification": classification,
        "classification_evidence": evidence,
        "pre_cap_max_surface_turn_deg": max(row["hotspot"]["normal_turn_deg"] for row in rows if row["u"] <= 0.98),
        "near_pole_max_surface_turn_deg": max(row["hotspot"]["normal_turn_deg"] for row in rows if row["u"] >= 0.995),
        "near_pole_rows": [row for row in rows if row["u"] >= 0.995],
    }


def render_set(surface_runtime: Any, binding: dict[str, Any], out: Path, qa_collection: Any, obj: Any, camera: Any, prefix: str):
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    reflection = iso.require_surface_asset(profile["reflection"]["name"], "material")
    zebra = iso.require_surface_asset(profile["zebra"]["name"], "material")
    result = {}
    for rig in ("STRIP", "GRAZING", "ZEBRA"):
        material = zebra if rig == "ZEBRA" else reflection
        stem = f"{prefix}_{rig}"
        result[rig] = surface_runtime.render(bpy.context.scene, out, stem, camera, obj, material, rig, qa_collection)
    return result


def main() -> int:
    a = args()
    seed = load(a.source)
    r2_fix = load(a.r2_correction)
    confirmed = load(a.confirmed_interface)
    execution = load(a.execution_contract)
    binding = load(a.binding)
    r4_contract = load(a.r4_contract)
    r42_contract = load(a.r4_2_contract)
    variants_contract = load(a.variants)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    template = r2.apply(seed, r2_fix)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    opposite_obj = bpy.data.objects.get(rt.NAMES["OPPOSITE_SIDE_PLAN"])
    lower_obj = bpy.data.objects.get(rt.NAMES["LOWER_RETURN_PROFILE"])
    if deck is None or opposite_obj is None or lower_obj is None:
        raise RuntimeError("Required native Source objects are missing")

    deck_original = {key: deck[key] for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m", "theta_center_rad", "theta_center_semantics", "blend")}
    index = int(variants_contract["active_control_index"])
    opposite_original = read_profile_control(opposite_obj, "Y-", index)
    lower_original = read_profile_control(lower_obj, "Z-", index)
    exponent_original = float(lower_obj["termination_envelope_exponent"])

    set_interface(deck, confirmed["source_overrides"])
    lower_obj["termination_envelope_exponent"] = 0.34
    set_profile_control(opposite_obj, "Y-", index, float(variants_contract["baseline"]["OPPOSITE_SIDE_PLAN"]))
    set_profile_control(lower_obj, "Z-", index, float(variants_contract["baseline"]["LOWER_RETURN_PROFILE"]))
    baseline_source = rt.extract_native_source(template)
    baseline_digest = iso.source_digest(baseline_source)
    baseline_machine = machine_summary(baseline_source, r2_fix)
    baseline_probe = ownership_probe(baseline_source, r42_contract)

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections are missing")

    baseline_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R4_3_BASELINE", baseline_source, derived_collection, False)
    baseline_obj["OLEANDER_R4_3_ROLE"] = "BASELINE_CONFIRMED_INTERFACE_TERMINATION"
    baseline_obj["OLEANDER_SOURCE_DIGEST"] = baseline_digest

    local = r4_contract["local_view"]
    target_u = float(local["target_u"])
    target_axis = base.bezier(base.own(baseline_source, "GRIP_AXIS")["control_points"], target_u)
    target = tuple(float(v) for v in target_axis)
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old_cam = bpy.data.objects.get("R4_3_TERMINATION_PROFILE_CAM")
    if old_cam is not None:
        bpy.data.objects.remove(old_cam, do_unlink=True)
    camera = surface_runtime.camera("R4_3_TERMINATION_PROFILE_CAM", float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_3_ROLE"] = "TERMINATION_PROFILE_VARIANT_LOCAL_CAMERA"

    iso.set_only_rendered(derived_collection, baseline_obj)
    baseline_renders = render_set(surface_runtime, binding, out, qa_collection, baseline_obj, camera, "R4_3_BASELINE")

    rows = []
    for variant in variants_contract["variants"]:
        controls = variant["controls"]
        set_profile_control(opposite_obj, "Y-", index, float(controls["OPPOSITE_SIDE_PLAN"]))
        set_profile_control(lower_obj, "Z-", index, float(controls["LOWER_RETURN_PROFILE"]))
        candidate = rt.extract_native_source(template)
        diffs = rt.source_difference(baseline_source, candidate)
        changed = [name for name, value in diffs.items() if value > 1e-8]
        expected = ["OPPOSITE_SIDE_PLAN"] if abs(float(controls["LOWER_RETURN_PROFILE"]) - float(variants_contract["baseline"]["LOWER_RETURN_PROFILE"])) <= 1e-12 else ["OPPOSITE_SIDE_PLAN", "LOWER_RETURN_PROFILE"]
        machine = machine_summary(candidate, r2_fix)
        probe = ownership_probe(candidate, r42_contract)
        obj, _, _, _ = rt.replace_derived(f"OL_DERIVED_{variant['variant_id']}", candidate, derived_collection, False)
        obj["OLEANDER_R4_3_ROLE"] = "NATIVE_TERMINAL_PROFILE_VARIANT"
        obj["OLEANDER_VARIANT_ID"] = variant["variant_id"]
        iso.set_only_rendered(derived_collection, obj)
        renders = render_set(surface_runtime, binding, out, qa_collection, obj, camera, variant["variant_id"])
        image_diffs = {
            rig: iso.image_difference(out / baseline_renders[rig], out / renders[rig])
            for rig in ("STRIP", "GRAZING", "ZEBRA")
        }
        candidate_opp = float(base.own(candidate, "OPPOSITE_SIDE_PLAN")["control_values"][index])
        candidate_low = float(base.own(candidate, "LOWER_RETURN_PROFILE")["control_values"][index])
        checks = {
            "only_ownership_profile_families_changed": changed == expected,
            "opposite_native_readback_matches": abs(candidate_opp - float(controls["OPPOSITE_SIDE_PLAN"])) <= 1e-8,
            "lower_native_readback_matches": abs(candidate_low - float(controls["LOWER_RETURN_PROFILE"])) <= 1e-8,
            "termination_exponent_locked_0_34": abs(float(base.own(candidate, "LOWER_RETURN_PROFILE")["termination_envelope_exponent"]) - 0.34) <= 1e-12,
            "profile_endpoint_controls_remain_0_003": abs(float(base.own(candidate, "OPPOSITE_SIDE_PLAN")["control_values"][5]) - 0.003) <= 1e-8 and abs(float(base.own(candidate, "LOWER_RETURN_PROFILE")["control_values"][5]) - 0.003) <= 1e-8,
            "confirmed_interface_relation_preserved": all(
                abs(float(base.own(candidate, "INTERFACE_DECK_BOUNDARY")[key]) - float(confirmed["source_overrides"][key])) <= 1e-12
                for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m")
            ) and base.own(candidate, "INTERFACE_DECK_BOUNDARY").get("theta_center") == "TOP_MERIDIAN",
            "existing_machine_qa_pass": machine["pass"],
            "derived_mesh_not_authority": obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
            "all_fixed_rig_renders_written": all((out / name).exists() for name in renders.values()),
        }
        rows.append({
            "variant_id": variant["variant_id"],
            "design_question": variant["design_question"],
            "controls": controls,
            "source_family_differences_from_baseline": diffs,
            "machine": machine,
            "profile_convergence_probe": probe,
            "checks": checks,
            "visual_qa_eligible": all(checks.values()),
            "renders": renders,
            "image_difference_metrics_vs_baseline": image_diffs,
        })

    # Restore the saved R2 native source exactly.
    set_profile_control(opposite_obj, "Y-", index, opposite_original)
    set_profile_control(lower_obj, "Z-", index, lower_original)
    lower_obj["termination_envelope_exponent"] = exponent_original
    for key, value in deck_original.items():
        deck[key] = value
    restored = rt.extract_native_source(template)
    r2_native = r2.apply(seed, r2_fix)
    restore_error = rt.source_difference(r2_native, restored)

    visual_candidates = [row["variant_id"] for row in rows if row["visual_qa_eligible"]]
    checks = {
        "baseline_existing_machine_qa_pass": baseline_machine["pass"],
        "all_three_professional_variants_executed": len(rows) == 3,
        "all_variants_machine_authority_and_render_pass": len(visual_candidates) == 3,
        "saved_r2_native_source_restored": max(restore_error.values()) <= 1e-8,
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "candidate_promotion_not_run": True,
    }
    status = "R4_3_TERMINAL_PROFILE_VARIANTS_RENDERED_VISUAL_DECISION_REQUIRED" if all(checks.values()) else "R4_3_TERMINAL_PROFILE_VARIANTS_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.3.termination-profile-report.v1",
        "status": status,
        "job_state": "R4_3_NATIVE_OPPOSITE_LOWER_PROFILE_BATCH_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "interface_relation_state": "CONFIRMED_LOCKED",
        "termination_exponent_state": "0.34_NATIVE_LOCKED",
        "termination_state": "PROFILE_RELATION_VARIANTS_UNDER_VISUAL_REVIEW",
        "checks": checks,
        "surface_system_runtime": runtime_identity,
        "baseline": {
            "source_digest": baseline_digest,
            "machine": baseline_machine,
            "profile_convergence_probe": baseline_probe,
            "renders": baseline_renders,
        },
        "variants": rows,
        "visual_candidates": visual_candidates,
        "visual_decision": "NOT_RUN_REQUIRES_TERMINATION_STRIP_GRAZING_ZEBRA_REVIEW",
        "next_legal_action": "Compare every passing professional terminal-profile variant. Select only if local convergence improves without overfilling the cap; then perform global/interface regression confirmation.",
        "boundary": variants_contract["boundary"],
    }
    (out / "G1_R4_3_TERMINATION_PROFILE_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("DECISION_REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
