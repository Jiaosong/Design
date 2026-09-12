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


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--execution-contract", required=True)
    p.add_argument("--binding", required=True)
    p.add_argument("--r4-isolation-contract", required=True)
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
    r4_contract = load(a.r4_isolation_contract)
    variants_contract = load(a.variants)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    template = r2.apply(seed, r2_fix)

    # First prove that the relation is now genuinely Blender-native editable/readable/restorable.
    relation_roundtrip = rt.controlled_native_termination_relation_edit_test(
        template,
        delta_exponent=0.02,
        edit_tolerance=float(binding["roundtrip_gate"]["controlled_native_edit_tolerance_m"]),
        restore_tolerance=float(binding["roundtrip_gate"]["restore_tolerance_m"]),
    )
    if not relation_roundtrip["pass"]:
        raise RuntimeError(f"Native termination relation roundtrip failed: {relation_roundtrip}")

    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    lower = bpy.data.objects.get(rt.NAMES["LOWER_RETURN_PROFILE"])
    if deck is None or lower is None:
        raise RuntimeError("Required Blender-native Source objects are missing")
    deck_original = {key: deck[key] for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m", "theta_center_rad", "theta_center_semantics", "blend")}
    exponent_original = float(lower["termination_envelope_exponent"])

    # Lock the confirmed interface relation for the entire termination batch.
    set_interface(deck, confirmed["source_overrides"])
    lower["termination_envelope_exponent"] = float(variants_contract["baseline"]["termination_envelope_exponent"])
    baseline_source = rt.extract_native_source(template)
    baseline_digest = iso.source_digest(baseline_source)
    baseline_machine = machine_summary(baseline_source, r2_fix)
    baseline_probe = r4.source_pole_probe(baseline_source, r4_contract)

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections missing")

    base_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R4_1_BASELINE_E034", baseline_source, derived_collection, False)
    base_obj["OLEANDER_R4_1_ROLE"] = "BASELINE_CONFIRMED_INTERFACE_TERMINATION_E034"
    base_obj["OLEANDER_SOURCE_DIGEST"] = baseline_digest

    local = r4_contract["local_view"]
    target_u = float(local["target_u"])
    axis_target = base.bezier(base.own(baseline_source, "GRIP_AXIS")["control_points"], target_u)
    target = tuple(float(v) for v in axis_target)
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old_cam = bpy.data.objects.get("R4_1_TERMINATION_VARIANT_CAM")
    if old_cam is not None:
        bpy.data.objects.remove(old_cam, do_unlink=True)
    camera = surface_runtime.camera("R4_1_TERMINATION_VARIANT_CAM", float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_1_ROLE"] = "TERMINATION_VARIANT_LOCAL_CAMERA"

    iso.set_only_rendered(derived_collection, base_obj)
    baseline_renders = render_set(surface_runtime, binding, out, qa_collection, base_obj, camera, "R4_1_BASELINE_E034")

    rows = []
    for variant in variants_contract["variants"]:
        exponent = float(variant["termination_envelope_exponent"])
        lower["termination_envelope_exponent"] = exponent
        candidate = rt.extract_native_source(template)
        diffs = rt.source_difference(baseline_source, candidate)
        changed = [name for name, value in diffs.items() if value > 1e-8]
        machine = machine_summary(candidate, r2_fix)
        probe = r4.source_pole_probe(candidate, r4_contract)
        obj, _, _, _ = rt.replace_derived(f"OL_DERIVED_{variant['variant_id']}", candidate, derived_collection, False)
        obj["OLEANDER_R4_1_ROLE"] = "NATIVE_TERMINATION_RELATION_VARIANT"
        obj["OLEANDER_VARIANT_ID"] = variant["variant_id"]
        obj["OLEANDER_TERMINATION_ENVELOPE_EXPONENT"] = exponent
        iso.set_only_rendered(derived_collection, obj)
        renders = render_set(surface_runtime, binding, out, qa_collection, obj, camera, variant["variant_id"])
        image_diffs = {
            rig: iso.image_difference(out / baseline_renders[rig], out / renders[rig])
            for rig in ("STRIP", "GRAZING", "ZEBRA")
        }
        checks = {
            "only_native_lower_return_relation_family_changed": changed == ["LOWER_RETURN_PROFILE"],
            "native_exponent_readback_matches_requested": abs(float(base.own(candidate, "LOWER_RETURN_PROFILE")["termination_envelope_exponent"]) - exponent) <= 1e-12,
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
            "termination_envelope_exponent": exponent,
            "source_family_differences_from_e034": diffs,
            "machine": machine,
            "source_space_pole_probe": probe,
            "checks": checks,
            "visual_qa_eligible": all(checks.values()),
            "renders": renders,
            "image_difference_metrics_vs_e034": image_diffs,
        })

    # Restore the saved R2 native Source exactly after extracting all derived diagnostic candidates.
    lower["termination_envelope_exponent"] = exponent_original
    for key, value in deck_original.items():
        deck[key] = value
    restored = rt.extract_native_source(template)
    r2_native = r2.apply(seed, r2_fix)
    restore_error = rt.source_difference(r2_native, restored)

    visual_candidates = [row["variant_id"] for row in rows if row["visual_qa_eligible"]]
    checks = {
        "native_termination_relation_roundtrip_pass": relation_roundtrip["pass"],
        "baseline_existing_machine_qa_pass": baseline_machine["pass"],
        "all_variants_machine_and_authority_pass": all(row["visual_qa_eligible"] for row in rows),
        "all_variants_rendered_independently": len(rows) == len(variants_contract["variants"]) and len(rows) == 3,
        "saved_r2_native_source_restored": max(restore_error.values()) <= 1e-8,
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "candidate_promotion_not_run": True,
    }
    status = "R4_1_NATIVE_TERMINATION_VARIANTS_RENDERED_VISUAL_DECISION_REQUIRED" if all(checks.values()) else "R4_1_NATIVE_TERMINATION_VARIANTS_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.1.termination-envelope-report.v1",
        "status": status,
        "job_state": "R4_1_NATIVE_TERMINATION_RELATION_BATCH_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "interface_relation_state": "CONFIRMED_LOCKED",
        "termination_state": "SOURCE_RELATION_VARIANTS_UNDER_VISUAL_REVIEW",
        "native_relation_roundtrip": relation_roundtrip,
        "checks": checks,
        "surface_system_runtime": runtime_identity,
        "baseline": {
            "variant_id": variants_contract["baseline"]["variant_id"],
            "source_digest": baseline_digest,
            "machine": baseline_machine,
            "source_space_pole_probe": baseline_probe,
            "renders": baseline_renders,
        },
        "variants": rows,
        "visual_candidates": visual_candidates,
        "visual_decision": "NOT_RUN_REQUIRES_TERMINATION_STRIP_GRAZING_ZEBRA_REVIEW",
        "next_legal_action": "Compare every native Source relation variant under fixed local diagnostics. Select only if the right/front convergence improves without creating an uncontrolled fuller cap; then run global/interface regression confirmation.",
        "boundary": variants_contract["boundary"],
    }
    (out / "G1_R4_1_TERMINATION_ENVELOPE_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("DECISION_REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
