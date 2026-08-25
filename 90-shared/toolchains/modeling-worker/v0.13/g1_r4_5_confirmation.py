#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
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
import g1_r2_topology_isolation as iso
import g1_r4_5_termination_cap_relation as cap


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--r45-contract", required=True)
    p.add_argument("--confirmation", required=True)
    p.add_argument("--execution-contract", required=True)
    p.add_argument("--binding", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--resolution", type=int, default=768)
    return p.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text(name: str, content: str):
    block = bpy.data.texts.get(name) or bpy.data.texts.new(name)
    block.clear()
    block.write(content)
    return block


def render(surface_runtime, binding, out: Path, qa_collection: Any, obj: Any, camera: Any, prefix: str):
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
    seed_path = Path(a.source)
    seed_sha_before = sha256(seed_path)
    seed = load(a.source)
    r2_fix = load(a.r2_correction)
    confirmed_interface = load(a.confirmed_interface)
    r45_contract = load(a.r45_contract)
    confirmation = load(a.confirmation)
    execution = load(a.execution_contract)
    binding = load(a.binding)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if confirmation["policy"]["parameter_tuning_in_confirmation_forbidden"] is not True:
        raise RuntimeError("R4.5 confirmation must replay the exact selected relation")
    relation = confirmation["source_relation"]
    if confirmation["selected_variant"] != "CAP_A_0_88" or abs(float(relation["termination_cap_onset_u"]) - 0.88) > 1e-12:
        raise RuntimeError("R4.5 exact confirmation relation changed")

    template = r2.apply(seed, r2_fix)
    baseline_native = rt.extract_native_source(template)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    lower_obj = bpy.data.objects.get(rt.NAMES["LOWER_RETURN_PROFILE"])
    if deck is None or lower_obj is None:
        raise RuntimeError("Blender-native Source objects missing")

    cap.set_confirmed_interface(deck, confirmed_interface["source_overrides"])
    cap.clear_cap(lower_obj)
    confirmed_reference = rt.extract_native_source(template)
    cap.bind_cap(lower_obj, float(relation["termination_cap_onset_u"]))
    candidate_source = rt.extract_native_source(template)
    candidate_source["machine_thresholds"]["max_sparse_authority_scalar_count"] = int(
        r45_contract["policy"]["max_sparse_authority_scalar_count_with_cap_relation"]
    )

    machine, candidate_source = cap.evaluate_variant(
        confirmed_reference,
        candidate_source,
        float(relation["termination_cap_onset_u"]),
        r45_contract,
        r2_fix,
    )
    roundtrip = rt.controlled_native_cap_relation_edit_test(template, delta_onset_u=0.005)
    extracted_after_edit_restore, native_diffs, authority = rt.authority_checks(candidate_source)
    candidate_digest = iso.source_digest(candidate_source)
    extracted_digest = iso.source_digest(extracted_after_edit_restore)

    interface = base.own(candidate_source, "INTERFACE_DECK_BOUNDARY")
    lower = base.own(candidate_source, "LOWER_RETURN_PROFILE")
    source_checks = {
        "selected_onset_exact": abs(float(lower["termination_cap_onset_u"]) - 0.88) <= 1e-12,
        "cap_law_exact": lower.get("termination_cap_law") == r2.CAP_LAW,
        "cap_semantics_exact": lower.get("termination_cap_semantics") == r2.CAP_SEMANTICS,
        "cap_endpoint_section_exact": lower.get("termination_cap_endpoint_section") == r2.CAP_ENDPOINT_SECTION,
        "one_numeric_cap_dof": int(relation["numeric_dof_count"]) == 1,
        "confirmed_interface_exact": abs(float(interface["u_center"]) - 0.62) <= 1e-12
        and abs(float(interface["u_halfspan"]) - 0.26) <= 1e-12
        and interface.get("theta_center") == "TOP_MERIDIAN"
        and abs(float(interface["theta_halfspan_rad"]) - 1.06) <= 1e-12
        and abs(float(interface["core_fraction"]) - 0.29) <= 1e-12
        and abs(float(interface["depth_m"]) - 0.012) <= 1e-12,
        "termination_envelope_locked": abs(float(lower["termination_envelope_exponent"]) - 0.34) <= 1e-12,
        "machine_gate_pass": bool(machine["machine_pass"]) and all(machine["checks"].values()),
        "native_roundtrip_pass": bool(roundtrip["pass"]),
        "native_authority_checks_pass": all(authority.values()),
        "native_readback_digest_exact": candidate_digest == extracted_digest and max(native_diffs.values()) <= 1e-8,
        "candidate_promotion_not_run": confirmation["policy"]["candidate_promotion"] == "NOT_RUN",
    }

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections missing")

    baseline_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R4_5_CONFIRM_BASELINE", confirmed_reference, derived_collection, False)
    candidate_obj, _, _, _ = rt.replace_derived("OL_DERIVED_G1_R4_5_CAP_A_CONFIRMED", candidate_source, derived_collection, False)
    baseline_obj["OLEANDER_R4_5_ROLE"] = "CONFIRMED_INTERFACE_NO_CAP_REFERENCE"
    candidate_obj["OLEANDER_R4_5_ROLE"] = "CAP_A_EXACT_CONFIRMATION"
    candidate_obj["OLEANDER_SOURCE_DIGEST"] = candidate_digest

    local = confirmation["local_view"]
    target = cap.axis_point(candidate_source, float(local["target_u"]))
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old = bpy.data.objects.get(local["name"])
    if old is not None:
        bpy.data.objects.remove(old, do_unlink=True)
    camera = surface_runtime.camera(local["name"], float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_5_ROLE"] = "CAP_A_CONFIRMATION_CAMERA"

    iso.set_only_rendered(derived_collection, baseline_obj)
    baseline_renders = render(surface_runtime, binding, out, qa_collection, baseline_obj, camera, "R4_5_CONFIRM_BASELINE")
    iso.set_only_rendered(derived_collection, candidate_obj)
    candidate_renders = render(surface_runtime, binding, out, qa_collection, candidate_obj, camera, "R4_5_CONFIRM_CAP_A")
    image_diffs = {
        rig: iso.image_difference(out / baseline_renders[rig], out / candidate_renders[rig])
        for rig in ("BROAD", "STRIP", "GRAZING", "ZEBRA")
    }

    text("OLEANDER_G1_R2_REBUILD.py", (HERE / "g1_r2_blender_rebuild.py").read_text(encoding="utf-8"))
    text("OLEANDER_G1_R2_LIVE_SOURCE.json", json.dumps(candidate_source, ensure_ascii=False, indent=2))
    text("OLEANDER_G1_R4_5_CONFIRMED_RELATION.json", json.dumps(confirmation, ensure_ascii=False, indent=2))

    scene["OLEANDER_MODEL"] = "OLEANDER_G1_R4_5_CAP_A_WORKING_SOURCE__v0_13"
    scene["OLEANDER_STAGE"] = "R4_5_EXACT_CAP_A_CONFIRMATION"
    scene["OLEANDER_AUTHORITY_STATE"] = "WORKING_SOURCE"
    scene["OLEANDER_DESIGN_STATE"] = "REVISE / TERMINATION_RELATION_CONFIRMED_PENDING_CANDIDATE_REVIEW"
    scene["OLEANDER_CANDIDATE_REVIEW"] = "REOPENED"
    scene["OLEANDER_CANDIDATE_PROMOTION"] = "NOT_RUN"
    scene["OLEANDER_TERMINATION_CAP_ONSET_U"] = 0.88
    scene["OLEANDER_TERMINATION_CAP_LAW"] = r2.CAP_LAW
    scene["OLEANDER_TERMINATION_CAP_SEMANTICS"] = r2.CAP_SEMANTICS
    scene["OLEANDER_LIVE_SOURCE_DIGEST"] = candidate_digest
    scene["OLEANDER_SURFACE_SYSTEM_SHARED_RUNTIME_BOUND"] = True

    blend = out / confirmation["outputs"]["blend"]
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))
    snapshot = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.5.confirmed-native-source-snapshot.v1",
        "authority_state": "WORKING_SOURCE",
        "relation_state": "R4_5_CAP_A_EXACT_CONFIRMATION",
        "live_source_digest": candidate_digest,
        "live_source": candidate_source,
        "blender_source_objects": list(rt.NAMES.values()),
        "derived_object": candidate_obj.name,
        "derived_is_authority": False,
        "embedded_live_source_text": "OLEANDER_G1_R2_LIVE_SOURCE.json",
        "embedded_relation_text": "OLEANDER_G1_R4_5_CONFIRMED_RELATION.json",
    }
    (out / confirmation["outputs"]["native_source_snapshot"]).write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    seed_sha_after = sha256(seed_path)
    all_renders = list(baseline_renders.values()) + list(candidate_renders.values())
    checks = {
        **source_checks,
        "shared_surface_runtime_pass": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "candidate_derived_not_authority": candidate_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "saved_blend_keeps_native_cap_relation_active": abs(float(lower_obj["termination_cap_onset_u"]) - 0.88) <= 1e-12,
        "live_source_text_embedded": bpy.data.texts.get("OLEANDER_G1_R2_LIVE_SOURCE.json") is not None,
        "confirmed_relation_text_embedded": bpy.data.texts.get("OLEANDER_G1_R4_5_CONFIRMED_RELATION.json") is not None,
        "all_required_renders_written": all((out / name).exists() for name in all_renders),
        "native_blend_written": blend.exists(),
        "snapshot_written": (out / confirmation["outputs"]["native_source_snapshot"]).exists(),
        "bootstrap_seed_not_overwritten": seed_sha_before == seed_sha_after,
    }
    status = "R4_5_CAP_A_EXACT_CONFIRMATION_PASS_VISUAL_DECISION_REQUIRED" if all(checks.values()) else "R4_5_CAP_A_EXACT_CONFIRMATION_FAIL_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.5.termination-cap-confirmation-report.v1",
        "status": status,
        "job_state": "R4_5_EXACT_CAP_A_CONFIRMATION_EXECUTED",
        "design_state": "REVISE / TERMINATION_RELATION_SELECTED",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "selected_variant": confirmation["selected_variant"],
        "source_relation": relation,
        "source_digest": candidate_digest,
        "machine": machine,
        "roundtrip": roundtrip,
        "checks": checks,
        "surface_system_runtime": runtime_identity,
        "renders": {"baseline": baseline_renders, "candidate": candidate_renders},
        "image_difference_metrics": image_diffs,
        "blend": blend.name,
        "native_source_snapshot": confirmation["outputs"]["native_source_snapshot"],
        "visual_decision": "NOT_RUN_REQUIRES_EXACT_CONFIRMATION_REVIEW",
        "boundary": confirmation["boundary"],
    }
    (out / confirmation["outputs"]["report"]).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("REQUIRED") else 11


if __name__ == "__main__":
    raise SystemExit(main())
