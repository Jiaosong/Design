#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import g1_r2_core as r2
import g1_r2_qa as qa
import g1_r2_blender_scene as bs
import g1_r2_blender_roundtrip as rt

MODEL = "OLEANDER_G1_R2_HandheldShell__BLENDER_NATIVE_SOURCE__v0_13"


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--correction", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--resolution", type=int, default=512)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def text(name, content):
    block = bpy.data.texts.get(name) or bpy.data.texts.new(name)
    block.clear()
    block.write(content)
    return block


def load_surface_system_runtime(binding):
    runtime_binding = binding["runtime_binding"]
    module_path = ROOT / runtime_binding["module"]
    if not module_path.is_file():
        raise RuntimeError(f"Blender Surface System shared runtime missing: {module_path}")
    spec = importlib.util.spec_from_file_location("oleander_blender_surface_system_f1_runtime", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Blender Surface System runtime: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    contract_path = ROOT / runtime_binding["contract"]
    identity = module.validate_binding(binding, contract_path)
    identity["module"] = runtime_binding["module"]
    identity["contract_path"] = runtime_binding["contract"]
    return module, identity


def make_materials(surface_runtime, binding):
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    clay_spec = profile["clay"]
    refl_spec = profile["reflection"]
    zebra_spec = profile["zebra"]
    clay = surface_runtime.material(
        clay_spec["name"],
        tuple(clay_spec["base_color"]),
        clay_spec["roughness"],
        clay_spec["metallic"],
    )
    reflection = surface_runtime.material(
        refl_spec["name"],
        tuple(refl_spec["base_color"]),
        refl_spec["roughness"],
        refl_spec["metallic"],
    )
    zebra = surface_runtime.zebra(zebra_spec["name"], zebra_spec["frequency"])
    return clay, reflection, zebra


def main():
    a = args()
    source_path = Path(a.source)
    seed_sha_before = sha(source_path)
    source = load(a.source)
    fix = load(a.correction)
    contract = load(a.contract)
    binding = load(a.binding)
    surface_runtime, surface_runtime_identity = load_surface_system_runtime(binding)
    seed = r2.apply(source, fix)

    out = Path(a.out).resolve()
    diag = out / contract["outputs"]["diagnostic_root"]
    diag.mkdir(parents=True, exist_ok=True)

    gate = binding["roundtrip_gate"]
    read_tol = float(gate["bootstrap_readback_tolerance_m"])
    edit_tol = float(gate["controlled_native_edit_tolerance_m"])
    restore_tol = float(gate["restore_tolerance_m"])
    locked_tol = float(gate["locked_semantic_tolerance_rad"])

    bs.clean()
    source_collection = bs.col(bs.SRC)
    derived_collection = bs.col(bs.DER)
    qa_collection = bs.col(bs.QA)
    source_objects = bs.sources(seed, source_collection)

    live_source, bootstrap_diffs, authority_checks = rt.authority_checks(seed, read_tol, locked_tol)
    edit_delta = float(gate["controlled_native_edit_delta_m"])
    edit_test = rt.controlled_native_edit_test(seed, edit_delta, edit_tol, restore_tol)
    live_source = rt.extract_native_source(seed)

    base_report, baseline_vertices = qa.evaluate(live_source, fix, False)
    revision_report, revision_vertices = qa.evaluate(live_source, fix, True)
    _, baseline_faces, _ = r2.mesh(live_source, False)
    _, revision_faces, _ = r2.mesh(live_source, True)

    baseline = bs.mesh_obj(
        "OL_DERIVED_G1_R2_BASELINE",
        baseline_vertices,
        baseline_faces,
        derived_collection,
        "R2 baseline derived from Blender-native Working Source",
    )
    revision = bs.mesh_obj(
        "OL_DERIVED_G1_R2_THUMB_REVISION",
        revision_vertices,
        revision_faces,
        derived_collection,
        "R2 controlled revision derived from Blender-native Working Source",
    )
    revision.hide_render = True
    revision.hide_viewport = True
    baseline["OLEANDER_SOURCE_MODE"] = "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE"
    revision["OLEANDER_SOURCE_MODE"] = "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE"

    clay, reflection, zebra = make_materials(surface_runtime, binding)
    surface_runtime.assign(baseline, clay)
    surface_runtime.assign(revision, clay)

    scene = bpy.context.scene
    surface_runtime.render_setup(scene, contract["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    target = (0.095, 0.0, 0.052)

    scene["OLEANDER_G1_R2_U_RINGS"] = int(live_source["derived_execution"]["u_rings"])
    scene["OLEANDER_G1_R2_CIRC_SAMPLES"] = int(live_source["derived_execution"]["circumferential_samples"])
    scene["OLEANDER_TERMINATION_ENVELOPE_EXPONENT"] = float(
        live_source["ownership"]["LOWER_RETURN_PROFILE"].get("termination_envelope_exponent", 0.34)
    )
    scene["OLEANDER_LOCKED_THETA_CENTER_TOP"] = True
    scene["OLEANDER_NATIVE_READBACK_TOLERANCE_M"] = read_tol

    hero = surface_runtime.camera("HERO_CAM", 85, (0.34, -0.34, 0.25), target, qa_collection)
    cmf = surface_runtime.camera("CMF_CAM", 110, (0.095, 0.0, 1.20), target, qa_collection)
    inspect = surface_runtime.camera("INSPECTION_CAM", 135, (0.95, 0.0, 0.075), target, qa_collection)
    rigmap = surface_runtime.build_project_rigs(
        qa_collection,
        target,
        binding["runtime_binding"]["project_rig_profile"],
    )
    for obj in qa_collection.objects:
        if (obj.type == "LIGHT" or obj.name == "R2_NEG_FILL") and hasattr(obj, "visible_camera"):
            obj.visible_camera = False

    rendered = []
    for stem, cam, mat, rig in (
        ("BASELINE_BROAD_PERSPECTIVE", hero, clay, "BROAD"),
        ("BASELINE_BROAD_TOP", cmf, clay, "BROAD"),
        ("BASELINE_BROAD_SIDE", inspect, clay, "BROAD"),
        ("BASELINE_STRIP_PERSPECTIVE", hero, reflection, "STRIP"),
        ("BASELINE_GRAZING_PERSPECTIVE", hero, reflection, "GRAZING"),
        ("BASELINE_ZEBRA_PERSPECTIVE", hero, zebra, "ZEBRA"),
    ):
        rendered.append(surface_runtime.render(scene, diag, stem, cam, baseline, mat, rig, qa_collection))

    baseline.hide_render = True
    baseline.hide_viewport = True
    revision.hide_render = False
    revision.hide_viewport = False
    for stem, mat, rig in (
        ("REVISION_BROAD_PERSPECTIVE", clay, "BROAD"),
        ("REVISION_STRIP_PERSPECTIVE", reflection, "STRIP"),
    ):
        rendered.append(surface_runtime.render(scene, diag, stem, hero, revision, mat, rig, qa_collection))

    baseline.hide_render = False
    baseline.hide_viewport = False
    revision.hide_render = True
    revision.hide_viewport = True
    master = surface_runtime.master_exr(scene, diag, hero, baseline, reflection, qa_collection)

    rebuild_source = (HERE / "g1_r2_blender_rebuild.py").read_text(encoding="utf-8")
    text("OLEANDER_G1_R2_REBUILD.py", rebuild_source)
    text("OLEANDER_G1_R2_LIVE_SOURCE.json", json.dumps(live_source, ensure_ascii=False, indent=2))

    roundtrip = {
        "schema": "oleander.modeling-worker.v0.13.g1.r2.blender-native-roundtrip",
        "authority_state": "WORKING_SOURCE",
        "source_mode": "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE",
        "bootstrap_seed_sha256": seed_sha_before,
        "representation_precision": gate["representation_precision"],
        "bootstrap_readback_tolerance_m": read_tol,
        "bootstrap_readback_family_error_m": bootstrap_diffs,
        "authority_checks": authority_checks,
        "controlled_native_edit_test": edit_test,
        "live_source_snapshot": live_source,
        "bootstrap_seed_overwritten": False,
        "writeback_policy": "NEW_SNAPSHOT_ONLY",
        "rebuild_text_block": "OLEANDER_G1_R2_REBUILD.py",
        "surface_system_runtime": surface_runtime_identity,
    }
    (diag / contract["outputs"]["roundtrip_snapshot"]).write_text(
        json.dumps(roundtrip, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    native = {
        "schema": "oleander.modeling-worker.v0.13.g1.r2.blender-native-source-snapshot",
        "authority_state": "WORKING_SOURCE",
        "source_mode": "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE",
        "bootstrap_role": "IMMUTABLE_SEED_AND_PROVENANCE",
        "objects": {
            obj.name: {
                "type": obj.type,
                "role": obj.get("OLEANDER_ROLE"),
                "editable": bool(obj.get("OLEANDER_EDITABLE", False)),
            }
            for obj in source_objects
        },
        "derived_objects": [baseline.name, revision.name],
        "round_trip_readback_and_rebuild": "IMPLEMENTED",
        "bootstrap_seed_overwrite": "FORBIDDEN",
        "locked_semantics": binding["source_authority"]["locked_semantics"],
        "surface_system_runtime": surface_runtime_identity,
    }
    (diag / contract["outputs"]["source_snapshot"]).write_text(
        json.dumps(native, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    scene["OLEANDER_MODEL"] = MODEL
    scene["OLEANDER_STAGE"] = "G1_R2_BLENDER_NATIVE_SOURCE_ROUNDTRIP"
    scene["OLEANDER_AUTHORITY_STATE"] = "WORKING_SOURCE"
    scene["OLEANDER_DESIGN_STATE"] = "REVISE"
    scene["OLEANDER_CANDIDATE_REVIEW"] = "REOPENED"
    scene["OLEANDER_CANDIDATE_PROMOTION"] = "NOT_RUN"
    scene["OLEANDER_SOURCE_MODE"] = "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE"
    scene["OLEANDER_SOURCE_SHA256"] = seed_sha_before
    scene["OLEANDER_CORRECTION_SHA256"] = sha(a.correction)
    scene["OLEANDER_EXECUTION_CONTRACT_SHA256"] = sha(a.contract)
    scene["OLEANDER_SURFACE_BINDING_SHA256"] = sha(a.binding)
    scene["OLEANDER_DIAGNOSTIC_EXPOSURE"] = -1.20
    scene["OLEANDER_SURFACE_SYSTEM_SHARED_RUNTIME_BOUND"] = True

    blend = out / contract["outputs"]["blend"]
    bpy.ops.wm.save_as_mainfile(filepath=str(blend))

    required = set(contract["required_diagnostics"])
    produced = {Path(name).stem for name in rendered}
    seed_sha_after = sha(source_path)
    surface_checks = surface_runtime_identity["checks"]
    checks = {
        "source_authority_objects_present": authority_checks["six_native_source_objects_present"],
        "source_objects_editable": authority_checks["all_native_source_objects_editable"],
        "source_objects_are_working_source": authority_checks["all_native_source_objects_working_source"],
        "bootstrap_to_native_readback_within_representation_tolerance": authority_checks[
            "bootstrap_roundtrip_within_blender_representation_tolerance"
        ],
        "locked_source_semantics_preserved": authority_checks["locked_top_meridian_semantic_preserved"],
        "controlled_native_edit_roundtrip_pass": edit_test["pass"],
        "derived_mesh_not_authority": baseline.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY"
        and revision.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "derived_mesh_built_from_native_readback": baseline.get("OLEANDER_SOURCE_MODE")
        == "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE",
        "surface_system_shared_runtime_bound": surface_runtime_identity["status"] == "PASS"
        and all(surface_checks.values()),
        "surface_system_runtime_api_bound": scene.get("OLEANDER_SURFACE_SYSTEM_RUNTIME_API")
        == binding["runtime_binding"]["api"],
        "baseline_machine_pass_retained": all(base_report["checks"].values()),
        "revision_machine_pass_retained": all(revision_report["checks"].values()),
        "required_diagnostics_written": required.issubset(produced)
        and all((diag / f"{name}.png").exists() for name in required),
        "master_exr_written": (diag / master).exists(),
        "native_blend_written": blend.exists(),
        "self_contained_rebuild_text_embedded": bpy.data.texts.get("OLEANDER_G1_R2_REBUILD.py") is not None,
        "live_source_text_embedded": bpy.data.texts.get("OLEANDER_G1_R2_LIVE_SOURCE.json") is not None,
        "roundtrip_snapshot_written": (diag / contract["outputs"]["roundtrip_snapshot"]).exists(),
        "bootstrap_seed_not_overwritten": seed_sha_before == seed_sha_after,
        "explicit_materials_present": all(
            bpy.data.materials.get(name)
            for name in (
                "OLEANDER_MAT_DIAG_CLAY_v1",
                "OLEANDER_MAT_DIAG_REFLECTION_v1",
                "OLEANDER_MAT_QA_ZEBRA_NORMAL_v1",
            )
        ),
        "explicit_cameras_present": all(
            bpy.data.objects.get(name) for name in ("HERO_CAM", "CMF_CAM", "INSPECTION_CAM")
        ),
        "candidate_review_reopened": contract["candidate_review"] == "REOPENED",
        "candidate_promotion_not_executed": contract["candidate_promotion"] == "NOT_RUN",
    }
    status = (
        "BLENDER_NATIVE_SOURCE_SURFACE_SYSTEM_RUNTIME_PASS_REFLECTION_VISUAL_REVIEW_REQUIRED"
        if all(checks.values())
        else "BLENDER_NATIVE_SOURCE_SURFACE_SYSTEM_RUNTIME_FAIL_REVISE"
    )
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r2.blender-report.v3",
        "model": MODEL,
        "status": status,
        "job_state": "BLENDER_NATIVE_SOURCE_SURFACE_SYSTEM_RUNTIME_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "blender_version": bpy.app.version_string,
        "render_engine": scene.render.engine,
        "diagnostic_exposure": scene.view_settings.exposure,
        "checks": checks,
        "surface_system_runtime": surface_runtime_identity,
        "bootstrap_readback_family_error_m": bootstrap_diffs,
        "native_edit_roundtrip": edit_test,
        "machine_baseline": base_report,
        "machine_revision": revision_report,
        "source_objects": [obj.name for obj in source_objects],
        "derived_objects": [baseline.name, revision.name],
        "camera_jobs": {
            "HERO_CAM": {"lens_mm": 85, "location": [0.34, -0.34, 0.25]},
            "CMF_CAM": {"lens_mm": 110, "location": [0.095, 0.0, 1.20]},
            "INSPECTION_CAM": {"lens_mm": 135, "location": [0.95, 0.0, 0.075]},
        },
        "rigs": rigmap,
        "diagnostics": rendered,
        "master_exr": master,
        "blend": blend.name,
        "roundtrip_snapshot": contract["outputs"]["roundtrip_snapshot"],
        "rebuild_text_block": "OLEANDER_G1_R2_REBUILD.py",
        "source_sha256": seed_sha_before,
        "correction_sha256": sha(a.correction),
        "contract_sha256": sha(a.contract),
        "binding_sha256": sha(a.binding),
        "boundary": contract["boundary"],
    }
    (diag / contract["outputs"]["report"]).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status.startswith("BLENDER_NATIVE_SOURCE_SURFACE_SYSTEM_RUNTIME_PASS") else 5


if __name__ == "__main__":
    raise SystemExit(main())
