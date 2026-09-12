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
import g1_r3_interface_fairness as fairness


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--r2-correction", required=True)
    parser.add_argument("--execution-contract", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--fairness-contract", required=True)
    parser.add_argument("--confirmation-contract", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--resolution", type=int, default=768)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def set_relation(deck: Any, relation: dict[str, Any]) -> None:
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        deck[key] = float(relation[key])
    deck["theta_center_rad"] = 0.0
    deck["theta_center_semantics"] = str(relation["theta_center"])
    deck["blend"] = str(relation["blend"])


def render_pair(surface_runtime, binding, out: Path, qa_collection: Any, obj: Any, cam: Any, prefix: str) -> dict[str, str]:
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    reflection = iso.require_surface_asset(profile["reflection"]["name"], "material")
    zebra = iso.require_surface_asset(profile["zebra"]["name"], "material")
    result = {}
    for rig in ("STRIP", "GRAZING", "ZEBRA"):
        mat = zebra if rig == "ZEBRA" else reflection
        stem = f"{prefix}_{rig}"
        result[rig] = surface_runtime.render(bpy.context.scene, out, stem, cam, obj, mat, rig, qa_collection)
    return result


def machine_summary(source: dict[str, Any], r2_fix: dict[str, Any]) -> dict[str, Any]:
    result, _ = qa.evaluate(source, r2_fix, False)
    return {
        "pass": all(result["checks"].values()),
        "checks": result["checks"],
        "dimensions_m": result["dimensions_m"],
        "interface_depth_m": result["interface_depth_m"],
        "outer_continuity_deg": result["outer_continuity_deg"],
        "core_continuity_deg": result["core_continuity_deg"],
    }


def main() -> int:
    a = args()
    source_seed = load(a.source)
    r2_fix = load(a.r2_correction)
    execution_contract = load(a.execution_contract)
    binding = load(a.binding)
    fairness_contract = load(a.fairness_contract)
    confirmation = load(a.confirmation_contract)
    relation = confirmation["source_relation"]
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    template = r2.apply(source_seed, r2_fix)
    baseline_source = rt.extract_native_source(template)
    digest_before = iso.source_digest(baseline_source)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    if deck is None:
        raise RuntimeError("Blender-native INTERFACE_DECK_BOUNDARY source object is missing")
    original = {key: deck[key] for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m", "theta_center_rad", "theta_center_semantics", "blend")}

    if confirmation["policy"]["parameter_tuning_in_confirmation_forbidden"] is not True:
        raise RuntimeError("R3.3 must be an exact selected-direction confirmation")
    set_relation(deck, relation)
    candidate_source = rt.extract_native_source(template)
    source_diffs = rt.source_difference(baseline_source, candidate_source)
    changed_families = [name for name, value in source_diffs.items() if value > 1e-8]
    machine = machine_summary(candidate_source, r2_fix)
    interior = fairness.interior_fairness(candidate_source, fairness_contract)

    # Restore native Working Source before visual execution; derived geometry remains diagnostic only.
    for key, value in original.items():
        deck[key] = value
    restored_source = rt.extract_native_source(template)
    restored_error = rt.source_difference(baseline_source, restored_source)
    digest_after = iso.source_digest(restored_source)

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution_contract["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections are missing")

    baseline_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R3_3_R2_REFERENCE", baseline_source, derived_collection, False)
    candidate_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R3_3_B_CONFIRMATION", candidate_source, derived_collection, False)
    baseline_obj["OLEANDER_R3_3_ROLE"] = "R2_REFERENCE"
    candidate_obj["OLEANDER_R3_3_ROLE"] = "R3_2_B_EXACT_CONFIRMATION"
    candidate_obj["OLEANDER_VARIANT_ID"] = confirmation["selected_direction"]

    hero = iso.require_surface_asset(confirmation["policy"]["hero_camera_required"], "object")
    target = tuple(float(v) for v in r2.point(candidate_source, float(relation["u_center"]), 0.0, False, False))
    local_spec = confirmation["local_view"]
    offset = tuple(float(v) for v in local_spec["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old_close = bpy.data.objects.get(local_spec["name"])
    if old_close is not None:
        bpy.data.objects.remove(old_close, do_unlink=True)
    close_cam = surface_runtime.camera(local_spec["name"], float(local_spec["lens_mm"]), location, target, qa_collection)
    close_cam["OLEANDER_R3_3_ROLE"] = "LOCAL_INTERFACE_CONFIRMATION_CAMERA"

    iso.set_only_rendered(derived_collection, baseline_obj)
    baseline_hero = render_pair(surface_runtime, binding, out, qa_collection, baseline_obj, hero, "R3_3_R2_HERO")
    baseline_close = render_pair(surface_runtime, binding, out, qa_collection, baseline_obj, close_cam, "R3_3_R2_INTERFACE_CLOSE")
    iso.set_only_rendered(derived_collection, candidate_obj)
    candidate_hero = render_pair(surface_runtime, binding, out, qa_collection, candidate_obj, hero, "R3_3_B_HERO")
    candidate_close = render_pair(surface_runtime, binding, out, qa_collection, candidate_obj, close_cam, "R3_3_B_INTERFACE_CLOSE")

    hero_diffs = {rig: iso.image_difference(out / baseline_hero[rig], out / candidate_hero[rig]) for rig in ("STRIP", "GRAZING", "ZEBRA")}
    close_diffs = {rig: iso.image_difference(out / baseline_close[rig], out / candidate_close[rig]) for rig in ("STRIP", "GRAZING", "ZEBRA")}

    all_outputs = list(baseline_hero.values()) + list(baseline_close.values()) + list(candidate_hero.values()) + list(candidate_close.values())
    checks = {
        "exact_selected_direction_used": all(abs(float(base.own(candidate_source, "INTERFACE_DECK_BOUNDARY")[key]) - float(relation[key])) <= 1e-12 for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m")),
        "top_meridian_preserved": base.own(candidate_source, "INTERFACE_DECK_BOUNDARY").get("theta_center") == "TOP_MERIDIAN",
        "only_interface_boundary_changed": changed_families == ["INTERFACE_DECK_BOUNDARY"],
        "machine_pass": machine["pass"],
        "interior_fairness_pass": interior["pass"],
        "shared_surface_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "local_camera_created_via_shared_runtime": close_cam.get("OLEANDER_ROLE") == "F1_DIAGNOSTIC_CAMERA",
        "baseline_derived_not_authority": baseline_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "candidate_derived_not_authority": candidate_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "source_restored": max(restored_error.values()) <= 1e-12 and digest_before == digest_after,
        "all_hero_and_local_renders_written": all((out / name).exists() for name in all_outputs),
        "candidate_promotion_still_blocked": confirmation["policy"]["candidate_promotion"] == "NOT_RUN",
    }
    status = "R3_3_EXACT_B_CONFIRMATION_RENDERED_VISUAL_DECISION_REQUIRED" if all(checks.values()) else "R3_3_CONFIRMATION_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r3.3.interface-confirmation-report.v1",
        "status": status,
        "job_state": "R3_3_EXACT_SELECTED_DIRECTION_CONFIRMATION_EXECUTED",
        "design_state": "REVISE / INTERFACE DIRECTION SELECTED",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "selected_direction": confirmation["selected_direction"],
        "source_relation": relation,
        "source_family_differences_from_r2": source_diffs,
        "machine": machine,
        "interior_fairness": interior,
        "checks": checks,
        "surface_system_runtime": runtime_identity,
        "local_camera": {"name": close_cam.name, "lens_mm": close_cam.data.lens, "location": list(close_cam.location), "target": list(target)},
        "renders": {
            "r2_hero": baseline_hero,
            "r2_interface_close": baseline_close,
            "b_hero": candidate_hero,
            "b_interface_close": candidate_close
        },
        "image_difference_metrics": {"hero": hero_diffs, "interface_close": close_diffs},
        "visual_decision": "NOT_RUN_REQUIRES_GLOBAL_AND_LOCAL_REVIEW",
        "termination_state": confirmation["termination_state"],
        "boundary": confirmation["boundary"]
    }
    (out / "G1_R3_3_INTERFACE_CONFIRMATION_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("DECISION_REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
