#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import g1_geometry_core as base
import g1_r2_core as r2
import g1_r2_blender_roundtrip as rt
import g1_r2_topology_isolation as iso
import g1_r3_blender_visual as vis


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--r2-correction", required=True)
    parser.add_argument("--execution-contract", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--variants", required=True)
    parser.add_argument("--machine-report", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--resolution", type=int, default=512)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> int:
    a = args()
    source_seed = load(a.source)
    r2_fix = load(a.r2_correction)
    execution_contract = load(a.execution_contract)
    binding = load(a.binding)
    variants_contract = load(a.variants)
    machine_report = load(a.machine_report)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    candidates = list(machine_report.get("visual_candidates", []))
    if not candidates:
        raise RuntimeError("R3.1 has no Machine+Fairness PASS visual candidates")
    by_id = {row["variant_id"]: row for row in variants_contract["variants"]}
    missing = [variant_id for variant_id in candidates if variant_id not in by_id]
    if missing:
        raise RuntimeError(f"R3.1 machine report references missing variants: {missing}")

    template = r2.apply(source_seed, r2_fix)
    baseline_source = rt.extract_native_source(template)
    digest_before = iso.source_digest(baseline_source)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    if deck is None:
        raise RuntimeError("Blender-native INTERFACE_DECK_BOUNDARY source object is missing")
    original = {key: float(deck[key]) for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "depth_m", "core_fraction")}

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution_contract["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections are missing from saved .blend")

    baseline_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R3_1_R2_BASELINE", baseline_source, derived_collection, False)
    baseline_obj["OLEANDER_R3_1_VISUAL_ROLE"] = "R2_REFERENCE"
    iso.set_only_rendered(derived_collection, baseline_obj)
    baseline_renders = vis.render_set(surface_runtime, binding, out, qa_collection, baseline_obj, "R3_1_R2_BASELINE")

    variant_results = []
    all_renders = list(baseline_renders.values())
    for variant_id in candidates:
        variant = by_id[variant_id]
        vis.set_deck_values(deck, variant["source_overrides"])
        candidate_source = rt.extract_native_source(template)
        source_diffs = rt.source_difference(baseline_source, candidate_source)
        changed = [name for name, value in source_diffs.items() if value > 1e-8]
        candidate_obj, _, _, _ = rt.replace_derived(f"OL_DERIVED_{variant_id}", candidate_source, derived_collection, False)
        candidate_obj["OLEANDER_R3_1_VISUAL_ROLE"] = "MACHINE_FAIRNESS_PASS_PROFESSIONAL_VARIANT"
        candidate_obj["OLEANDER_VARIANT_ID"] = variant_id
        iso.set_only_rendered(derived_collection, candidate_obj)
        renders = vis.render_set(surface_runtime, binding, out, qa_collection, candidate_obj, variant_id)
        all_renders.extend(renders.values())
        metrics = {
            rig: iso.image_difference(out / baseline_renders[rig], out / renders[rig])
            for rig in ("STRIP", "GRAZING", "ZEBRA")
        }
        checks = {
            "only_interface_boundary_source_family_changed": changed == ["INTERFACE_DECK_BOUNDARY"],
            "depth_preserved": abs(float(base.own(candidate_source, "INTERFACE_DECK_BOUNDARY")["depth_m"]) - 0.012) <= 1e-12,
            "top_meridian_semantic_preserved": base.own(candidate_source, "INTERFACE_DECK_BOUNDARY").get("theta_center") == "TOP_MERIDIAN",
            "derived_not_authority": candidate_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
            "renders_written": all((out / name).exists() for name in renders.values()),
        }
        variant_results.append({
            "variant_id": variant_id,
            "source_family_differences_from_r2": source_diffs,
            "checks": checks,
            "renders": renders,
            "image_difference_metrics": metrics,
        })
        vis.set_deck_values(deck, original)

    restored_source = rt.extract_native_source(template)
    restored_error = rt.source_difference(baseline_source, restored_source)
    digest_after = iso.source_digest(restored_source)
    checks = {
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "every_machine_fairness_pass_variant_rendered": {row["variant_id"] for row in variant_results} == set(candidates),
        "all_variant_checks_pass": all(all(row["checks"].values()) for row in variant_results),
        "source_restored_after_batch": max(restored_error.values()) <= 1e-12 and digest_before == digest_after,
        "baseline_derived_not_authority": baseline_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "candidate_promotion_still_blocked": machine_report.get("candidate_promotion") == "NOT_RUN",
        "all_batch_renders_written": all((out / name).exists() for name in all_renders),
    }
    status = "R3_1_PROFESSIONAL_BATCH_RENDERED_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "R3_1_BATCH_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r3.1.visual-batch-report.v1",
        "status": status,
        "job_state": "R3_1_MINIMUM_CHANGE_PROFESSIONAL_BATCH_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "machine_selection_policy": machine_report.get("selection_policy"),
        "machine_recommended_minimum_change_variant": machine_report.get("selected_for_fixed_rig_visual_diagnostics"),
        "visual_candidates": candidates,
        "checks": checks,
        "surface_system_runtime": runtime_identity,
        "baseline_renders": baseline_renders,
        "variants": variant_results,
        "source_restored_error": restored_error,
        "visual_decision": "NOT_RUN_BATCH_REVIEW_REQUIRED",
        "termination_state": "OPEN_UNCHANGED_NOT_SOLVED_BY_R3_1_INTERFACE_BATCH",
        "next_legal_action": "Compare every Machine+Fairness PASS professional variant under fixed Strip/Grazing/Zebra. Select the smallest relation change that preserves interface-basin readability and removes the R2 compression; otherwise remain REVISE.",
        "boundary": "R3.1 batch output is diagnostic design evidence only. No Candidate or Canonical Promotion is authorized.",
    }
    (out / "G1_R3_1_VISUAL_BATCH_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("REVIEW_REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
