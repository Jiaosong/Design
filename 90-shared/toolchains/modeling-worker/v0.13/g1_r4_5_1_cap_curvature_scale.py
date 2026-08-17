#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
import g1_r2_topology_isolation as iso
import g1_r4_5_termination_cap_relation as r45


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--execution-contract", required=True)
    p.add_argument("--binding", required=True)
    p.add_argument("--contract", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--resolution", type=int, default=512)
    return p.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def bind_relation(lower_obj: Any, onset: float, scale: float | None) -> None:
    lower_obj["termination_cap_onset_u"] = float(onset)
    if scale is None:
        if "termination_cap_pole_curvature_scale" in lower_obj:
            del lower_obj["termination_cap_pole_curvature_scale"]
        lower_obj["termination_cap_numeric_dof_count"] = 1
    else:
        lower_obj["termination_cap_pole_curvature_scale"] = float(scale)
        lower_obj["termination_cap_numeric_dof_count"] = 2
    lower_obj["termination_cap_law"] = r2.CAP_LAW
    lower_obj["termination_cap_semantics"] = r2.CAP_SEMANTICS
    lower_obj["termination_cap_endpoint_section"] = r2.CAP_ENDPOINT_SECTION


def clear_relation(lower_obj: Any) -> None:
    for key in (
        "termination_cap_onset_u",
        "termination_cap_pole_curvature_scale",
        "termination_cap_numeric_dof_count",
        "termination_cap_law",
        "termination_cap_semantics",
        "termination_cap_endpoint_section",
    ):
        if key in lower_obj:
            del lower_obj[key]


def evaluate(reference: dict[str, Any], candidate: dict[str, Any], contract: dict[str, Any], r2_fix: dict[str, Any]):
    policy = contract["policy"]
    gate = contract["machine_gate"]
    onset = float(contract["relation_vocabulary"]["locked_onset_value"])
    candidate["machine_thresholds"]["max_sparse_authority_scalar_count"] = int(policy["max_sparse_authority_scalar_count"])
    machine, _ = qa.evaluate(candidate, r2_fix, False)
    legacy_required = {k: v for k, v in machine["checks"].items() if k not in {"broad_long", "broad_circ"}}
    pos, normal = r45.onset_continuity(reference, candidate, onset, float(gate["onset_probe_epsilon_u"]), int(gate["theta_samples"]))
    interface_regression = r45.max_position_regression(
        reference,
        candidate,
        [float(v) for v in gate["interface_regression_u_samples"]],
        int(gate["interface_regression_theta_samples"]),
    )
    turns = r45.cap_turn_probe(candidate, onset, gate)
    radial = r45.radial_monotonicity(
        candidate,
        onset,
        int(gate["radial_monotonic_samples"]),
        int(gate["theta_samples"]),
        float(gate["radial_monotonic_tolerance_m"]),
    )
    close_error = r45.closure_error(candidate, int(gate["theta_samples"]))
    extra_rings = len(r2._u_values(candidate)) - int(candidate["derived_execution"]["u_rings"])
    lower = base.own(candidate, "LOWER_RETURN_PROFILE")
    scale = float(lower["termination_cap_pole_curvature_scale"])
    near = max(float(turns["near_pole_max_normal_turn_deg"]), 1e-9)
    ratio = float(turns["cap_region_max_normal_turn_deg"]) / near
    checks = {
        "legacy_machine_contract_outside_cap_passes": all(legacy_required.values()),
        "sparse_authority_count_is_50_or_less": machine["sparse_scalar_count"] <= int(policy["max_sparse_authority_scalar_count"]),
        "relation_has_exactly_two_numeric_dofs": int(contract["relation_vocabulary"]["numeric_dof_count"]) == 2,
        "cap_owner_is_existing_lower_return_family": contract["source_owner_family"] == "LOWER_RETURN_PROFILE",
        "onset_locked_exactly": abs(float(lower["termination_cap_onset_u"]) - onset) <= 1e-12,
        "pole_scale_explicit": "termination_cap_pole_curvature_scale" in lower,
        "cap_semantics_exact": lower.get("termination_cap_semantics") == r2.CAP_SEMANTICS,
        "cap_law_exact": lower.get("termination_cap_law") == r2.CAP_LAW,
        "cap_endpoint_section_exact": lower.get("termination_cap_endpoint_section") == r2.CAP_ENDPOINT_SECTION,
        "onset_position_continuity": pos <= float(gate["onset_position_continuity_max_m"]),
        "onset_normal_continuity": normal <= float(gate["onset_normal_continuity_max_deg"]),
        "confirmed_interface_zero_regression": interface_regression <= float(gate["interface_regression_max_displacement_m"]),
        "cap_region_normal_turn": turns["cap_region_max_normal_turn_deg"] <= float(gate["cap_region_max_normal_turn_deg"]),
        "near_pole_normal_turn": turns["near_pole_max_normal_turn_deg"] <= float(gate["near_pole_max_normal_turn_deg"]),
        "reflection_flow_concentration_ratio": ratio <= float(gate["reflection_flow_concentration_ratio_max"]),
        "radial_mean_monotonic": radial["mean_radius_increase_count"] == 0,
        "radial_max_monotonic": radial["max_radius_increase_count"] == 0,
        "single_pole_closure_exact": close_error <= float(gate["closure_position_tolerance_m"]),
        "cap_aware_execution_sampling_present": extra_rings >= int(gate["minimum_cap_aware_extra_u_rings"]),
        "candidate_promotion_not_run": policy["candidate_promotion"] == "NOT_RUN",
    }
    return {
        "machine_pass": all(checks.values()),
        "termination_cap_pole_curvature_scale": scale,
        "checks": checks,
        "legacy_machine_report": machine,
        "onset_position_continuity_error_m": pos,
        "onset_normal_continuity_deg": normal,
        "interface_regression_max_displacement_m": interface_regression,
        "cap_turn_probe": turns,
        "reflection_flow_concentration_ratio": ratio,
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
    obj = bpy.data.objects.new(name, bpy.data.meshes.new(name + "_MESH"))
    collection.objects.link(obj)
    obj.data.from_pydata(verts, [], faces)
    obj.data.update()
    for polygon in obj.data.polygons:
        polygon.use_smooth = True
    obj["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"
    obj["OLEANDER_ROLE"] = "R4.5.1 cap-scale derived execution geometry"
    obj["OLEANDER_SOURCE_DIGEST"] = iso.source_digest(source)
    return obj, len(verts), len(faces)


def render_set(surface_runtime: Any, binding: dict[str, Any], out: Path, qa_collection: Any, obj: Any, camera: Any, prefix: str):
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    clay = iso.require_surface_asset(profile["clay"]["name"], "material")
    reflection = iso.require_surface_asset(profile["reflection"]["name"], "material")
    zebra = iso.require_surface_asset(profile["zebra"]["name"], "material")
    result = {}
    for rig, mat in (("BROAD", clay), ("STRIP", reflection), ("GRAZING", reflection), ("ZEBRA", zebra)):
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

    authorization = (HERE / contract["authorization_receipt"]).read_text(encoding="utf-8")
    if "ONE_DOF_ONSET_ONLY_INSUFFICIENT_FOR_PROFESSIONAL_REFLECTION_FLOW" not in authorization:
        raise RuntimeError("R4.5.1 requires the R4.5 visual-revise authorization receipt")

    template = r2.apply(seed, r2_fix)
    native_before = rt.extract_native_source(template)
    native_digest_before = iso.source_digest(native_before)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    lower_obj = bpy.data.objects.get(rt.NAMES["LOWER_RETURN_PROFILE"])
    if deck is None or lower_obj is None:
        raise RuntimeError("Expected Blender-native Source objects missing")

    original_deck = {key: deck[key] for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m", "theta_center_rad", "theta_center_semantics", "blend")}
    original_lower_extra = {key: lower_obj[key] for key in lower_obj.keys() if key.startswith("termination_cap_")}
    r45.set_confirmed_interface(deck, confirmed["source_overrides"])
    clear_relation(lower_obj)
    confirmed_reference = rt.extract_native_source(template)

    onset = float(contract["relation_vocabulary"]["locked_onset_value"])
    bind_relation(lower_obj, onset, None)
    scale_one_reference = rt.extract_native_source(template)
    variants = {}
    for variant_id, spec in contract["variants"].items():
        scale = float(spec["termination_cap_pole_curvature_scale"])
        bind_relation(lower_obj, onset, scale)
        source = rt.extract_native_source(template)
        result, source = evaluate(confirmed_reference, source, contract, r2_fix)
        result["source_digest"] = iso.source_digest(source)
        variants[variant_id] = {"result": result, "source": source}

    machine_pass_ids = [key for key, row in variants.items() if row["result"]["machine_pass"]]
    if machine_pass_ids:
        selected_for_roundtrip = min(machine_pass_ids, key=lambda key: variants[key]["result"]["cap_turn_probe"]["cap_region_max_normal_turn_deg"])
        bind_relation(lower_obj, onset, variants[selected_for_roundtrip]["result"]["termination_cap_pole_curvature_scale"])
        roundtrip = rt.controlled_native_cap_pole_scale_edit_test(template, delta_scale=0.01)
    else:
        selected_for_roundtrip = None
        roundtrip = {"pass": False, "checks": {"machine_pass_variant_required": False}}

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections missing")

    baseline_obj, bv, bf = replace_object("OL_DERIVED_G1_R4_5_1_SCALE_1_REFERENCE", scale_one_reference, derived_collection)
    local = contract["local_view"]
    target = r45.axis_point(scale_one_reference, float(local["target_u"]))
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old_cam = bpy.data.objects.get(local["name"])
    if old_cam is not None:
        bpy.data.objects.remove(old_cam, do_unlink=True)
    camera = surface_runtime.camera(local["name"], float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_5_1_ROLE"] = "CAP_SCALE_VISUAL_CAMERA"

    iso.set_only_rendered(derived_collection, baseline_obj)
    renders = {"SCALE_1_00_REFERENCE": render_set(surface_runtime, binding, out, qa_collection, baseline_obj, camera, "R4_5_1_SCALE_1_00_REFERENCE")}
    geometry = {"SCALE_1_00_REFERENCE": {"vertices": bv, "faces": bf, "authority": baseline_obj.get("OLEANDER_AUTHORITY"), "source_digest": iso.source_digest(scale_one_reference)}}
    for variant_id in machine_pass_ids:
        obj, vc, fc = replace_object(f"OL_DERIVED_G1_R4_5_1_{variant_id}", variants[variant_id]["source"], derived_collection)
        iso.set_only_rendered(derived_collection, obj)
        renders[variant_id] = render_set(surface_runtime, binding, out, qa_collection, obj, camera, f"R4_5_1_{variant_id}")
        geometry[variant_id] = {"vertices": vc, "faces": fc, "authority": obj.get("OLEANDER_AUTHORITY"), "source_digest": obj.get("OLEANDER_SOURCE_DIGEST")}

    image_diffs = {
        variant_id: {
            rig: iso.image_difference(out / renders["SCALE_1_00_REFERENCE"][rig], out / renders[variant_id][rig])
            for rig in ("BROAD", "STRIP", "GRAZING", "ZEBRA")
        }
        for variant_id in machine_pass_ids
    }

    machine_ranked = sorted(
        machine_pass_ids,
        key=lambda key: (
            variants[key]["result"]["cap_turn_probe"]["cap_region_max_normal_turn_deg"],
            variants[key]["result"]["reflection_flow_concentration_ratio"],
            abs(variants[key]["result"]["termination_cap_pole_curvature_scale"] - 1.0),
        ),
    )

    for key, value in original_deck.items():
        deck[key] = value
    clear_relation(lower_obj)
    for key, value in original_lower_extra.items():
        lower_obj[key] = value
    restored = rt.extract_native_source(template)
    restored_error = rt.source_difference(native_before, restored)
    restored_digest = iso.source_digest(restored)

    global_checks = {
        "r4_5_visual_revise_authorization_present": True,
        "relation_has_two_numeric_dofs": int(contract["relation_vocabulary"]["numeric_dof_count"]) == 2,
        "onset_locked_at_0_88": abs(onset - 0.88) <= 1e-12,
        "owner_is_existing_source_family": contract["source_owner_family"] == "LOWER_RETURN_PROFILE",
        "native_scale_roundtrip_pass": bool(roundtrip.get("pass")),
        "shared_surface_runtime_pass": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "at_least_one_machine_pass_variant": len(machine_pass_ids) > 0,
        "all_rendered_variants_are_machine_pass": set(renders) - {"SCALE_1_00_REFERENCE"} == set(machine_pass_ids),
        "all_rendered_geometry_is_derived_not_authority": all(row["authority"] == "DERIVED_EXECUTION_NOT_AUTHORITY" for row in geometry.values()),
        "native_source_restored_exactly": native_digest_before == restored_digest and max(restored_error.values()) <= 1e-12,
        "candidate_promotion_not_run": contract["policy"]["candidate_promotion"] == "NOT_RUN",
    }
    status = "R4_5_1_CAP_SCALE_MACHINE_PASS_VISUAL_REVIEW_REQUIRED" if all(global_checks.values()) else "R4_5_1_CAP_SCALE_MACHINE_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.5.1.cap-curvature-scale-report.v1",
        "status": status,
        "job_state": "R4_5_1_CAP_SCALE_BATCH_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "relation_vocabulary": contract["relation_vocabulary"],
        "global_checks": global_checks,
        "roundtrip": roundtrip,
        "variants": {key: row["result"] for key, row in variants.items()},
        "machine_pass_variants": machine_pass_ids,
        "machine_ranked_variants": machine_ranked,
        "roundtrip_probe_variant": selected_for_roundtrip,
        "geometry": geometry,
        "renders": renders,
        "image_difference_metrics_vs_scale_1": image_diffs,
        "surface_system_runtime": runtime_identity,
        "visual_gate": contract["visual_gate"],
        "next_legal_action": "Review only Machine-PASS Broad/Strip/Grazing/Zebra variants against the rejected scale=1.0 reference. Confirm a scale only if the discrete terminal cap island/hook is materially reduced without onset kink, interface regression or closure degradation.",
        "boundary": contract["boundary"],
    }
    (out / "G1_R4_5_1_CAP_CURVATURE_SCALE_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("REQUIRED") else 13


if __name__ == "__main__":
    raise SystemExit(main())
