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
import g1_r2_blender_roundtrip as rt
import g1_r2_blender_scene as bs
import g1_r2_topology_isolation as iso


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--r2-correction", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--variants", required=True)
    parser.add_argument("--machine-report", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--resolution", type=int, default=512)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def render_set(surface_runtime, binding, out: Path, qa_collection, target, stem_prefix: str):
    camera = iso.require_surface_asset("HERO_CAM", "object")
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    reflection = iso.require_surface_asset(profile["reflection"]["name"], "material")
    zebra = iso.require_surface_asset(profile["zebra"]["name"], "material")
    renders = {}
    for rig in ("STRIP", "GRAZING", "ZEBRA"):
        mat = zebra if rig == "ZEBRA" else reflection
        stem = f"{stem_prefix}_{rig}_PERSPECTIVE"
        renders[rig] = surface_runtime.render(bpy.context.scene, out, stem, camera, target, mat, rig, qa_collection)
    return renders


def set_deck_values(deck, values: dict[str, float]) -> None:
    for key in ("u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        if key in values:
            deck[key] = float(values[key])


def main() -> int:
    a = args()
    source_seed = load(a.source)
    r2_fix = load(a.r2_correction)
    binding = load(a.binding)
    variants_contract = load(a.variants)
    machine_report = load(a.machine_report)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    selected = machine_report.get("selected_for_fixed_rig_visual_diagnostics")
    if not selected:
        raise RuntimeError("No R3 Machine+Fairness PASS variant selected for visual diagnostics")
    variant = next((row for row in variants_contract["variants"] if row["variant_id"] == selected), None)
    if variant is None:
        raise RuntimeError(f"Selected R3 variant missing from contract: {selected}")

    template = r2.apply(source_seed, r2_fix)
    baseline_source = rt.extract_native_source(template)
    digest_before = iso.source_digest(baseline_source)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    if deck is None:
        raise RuntimeError("Blender-native INTERFACE_DECK_BOUNDARY source object is missing")
    original = {key: float(deck[key]) for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "depth_m", "core_fraction")}

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, {"cycles_samples": 96, "denoise": True, "adaptive_sampling": True}, a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections are missing from saved .blend")

    baseline_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R3_R2_BASELINE", baseline_source, derived_collection, False)
    baseline_obj["OLEANDER_R3_VISUAL_ROLE"] = "R2_REFERENCE"

    set_deck_values(deck, variant["source_overrides"])
    candidate_source = rt.extract_native_source(template)
    candidate_diffs = rt.source_difference(baseline_source, candidate_source)
    changed_families = [name for name, value in candidate_diffs.items() if value > 1e-8]
    candidate_obj, _, _, _ = rt.replace_derived(f"OL_DERIVED_{selected}", candidate_source, derived_collection, False)
    candidate_obj["OLEANDER_R3_VISUAL_ROLE"] = "R3_MACHINE_FAIRNESS_PASS_CANDIDATE"
    candidate_obj["OLEANDER_VARIANT_ID"] = selected

    set_deck_values(deck, original)
    restored_source = rt.extract_native_source(template)
    restored_error = rt.source_difference(baseline_source, restored_source)
    digest_after = iso.source_digest(restored_source)

    iso.set_only_rendered(derived_collection, baseline_obj)
    base_renders = render_set(surface_runtime, binding, out, qa_collection, baseline_obj, "R3_R2_BASELINE")
    iso.set_only_rendered(derived_collection, candidate_obj)
    candidate_renders = render_set(surface_runtime, binding, out, qa_collection, candidate_obj, selected)
    image_metrics = {
        rig: iso.image_difference(out / base_renders[rig], out / candidate_renders[rig])
        for rig in ("STRIP", "GRAZING", "ZEBRA")
    }

    checks = {
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "selected_variant_was_machine_visual_candidate": selected in machine_report.get("visual_candidates", []),
        "only_interface_boundary_source_family_changed": changed_families == ["INTERFACE_DECK_BOUNDARY"],
        "r3_depth_preserved": abs(float(base.own(candidate_source, "INTERFACE_DECK_BOUNDARY")["depth_m"]) - 0.012) <= 1e-12,
        "top_meridian_semantic_preserved": base.own(candidate_source, "INTERFACE_DECK_BOUNDARY").get("theta_center") == "TOP_MERIDIAN",
        "source_restored_after_visual_experiment": max(restored_error.values()) <= 1e-12 and digest_before == digest_after,
        "baseline_derived_not_authority": baseline_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "candidate_derived_not_authority": candidate_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "candidate_promotion_still_blocked": machine_report.get("candidate_promotion") == "NOT_RUN",
        "all_fixed_rig_renders_written": all((out / name).exists() for name in list(base_renders.values()) + list(candidate_renders.values())),
    }
    status = "R3_FIXED_RIG_VISUAL_DIAGNOSTICS_RENDERED_REVIEW_REQUIRED" if all(checks.values()) else "R3_FIXED_RIG_VISUAL_DIAGNOSTICS_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r3.visual-diagnostic-report.v1",
        "status": status,
        "job_state": "R3_FIXED_RIG_VISUAL_DIAGNOSTICS_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "selected_variant": selected,
        "source_family_differences_from_r2": candidate_diffs,
        "source_restored_error": restored_error,
        "checks": checks,
        "surface_system_runtime": runtime_identity,
        "renders": {"baseline": base_renders, "candidate": candidate_renders},
        "image_difference_metrics": image_metrics,
        "visual_decision": "NOT_RUN_REQUIRES_REFLECTION_REVIEW",
        "termination_state": "OPEN_UNCHANGED_NOT_SOLVED_BY_R3_INTERFACE_BATCH",
        "next_legal_action": "Review fixed Strip/Grazing/Zebra pair. If basin hierarchy and reflection field are acceptable, record a separate visual decision before any Candidate review closure.",
        "boundary": "Rendering a Machine+Fairness PASS variant does not authorize Candidate Promotion, Canonical Promotion, Class-A, engineering, manufacturing or Release.",
    }
    (out / "G1_R3_VISUAL_DIAGNOSTIC_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("REVIEW_REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
