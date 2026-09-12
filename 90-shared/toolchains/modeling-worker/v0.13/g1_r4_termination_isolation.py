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
import g1_r2_blender_scene as bs
import g1_r2_blender_roundtrip as rt
import g1_r2_topology_isolation as iso


def args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--execution-contract", required=True)
    p.add_argument("--binding", required=True)
    p.add_argument("--isolation-contract", required=True)
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
    return ordered[lo] * (1 - f) + ordered[hi] * f


def set_interface(deck: Any, relation: dict[str, Any]) -> None:
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        deck[key] = float(relation[key])
    deck["theta_center_rad"] = 0.0
    deck["theta_center_semantics"] = str(relation["theta_center"])
    deck["blend"] = str(relation["blend"])


def custom_mesh(source: dict[str, Any], u_values: list[float], nv: int):
    verts = [r2.point(source, 0.0, 0.0)]
    faces = []
    for u in u_values:
        for j in range(nv):
            verts.append(r2.point(source, float(u), 2 * math.pi * j / nv))
    back = len(verts)
    verts.append(r2.point(source, 1.0, 0.0))
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
    return verts, faces


def replace_custom(name: str, source: dict[str, Any], collection: Any, u_values: list[float], nv: int, role: str):
    old = bpy.data.objects.get(name)
    if old is not None:
        mesh = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    verts, faces = custom_mesh(source, u_values, nv)
    obj = bs.mesh_obj(name, verts, faces, collection, role)
    obj["OLEANDER_R4_TOPOLOGY_ROLE"] = role
    obj["OLEANDER_SOURCE_DIGEST"] = iso.source_digest(source)
    return obj, verts, faces


def ring_radius_metrics(source: dict[str, Any], u: float, theta_samples: int) -> dict[str, float]:
    axis = base.bezier(base.own(source, "GRIP_AXIS")["control_points"], u)
    radii = []
    for j in range(theta_samples):
        p = r2.point(source, u, 2 * math.pi * j / theta_samples)
        radii.append(math.hypot(float(p[1]) - float(axis[1]), float(p[2]) - float(axis[2])))
    return {
        "min_m": min(radii),
        "mean_m": sum(radii) / len(radii),
        "max_m": max(radii),
    }


def source_pole_probe(source: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    spec = contract["source_space_probe"]
    theta_samples = int(spec["theta_samples"])
    span = float(spec["normal_turn_span_u"])
    half = span / 2
    exp = float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))
    rows = []
    for u_raw in spec["sample_u"]:
        u = float(u_raw)
        turns = []
        um = max(0.00001, u - half)
        up = min(0.9999, u + half)
        for j in range(theta_samples):
            t = 2 * math.pi * j / theta_samples
            turns.append(qa.ang(qa.normal(source, um, t), qa.normal(source, up, t)))
        envelope = math.sin(math.pi * u) ** exp if 0 < u < 1 else 0.0
        rows.append({
            "u": u,
            "termination_envelope": envelope,
            "ring_radius": ring_radius_metrics(source, u, theta_samples),
            "normal_turn_span_u": up - um,
            "max_normal_turn_deg": max(turns),
            "p95_normal_turn_deg": percentile(turns, 0.95),
        })
    return {
        "termination_envelope_exponent": exp,
        "rows": rows,
        "max_normal_turn_deg": max(row["max_normal_turn_deg"] for row in rows),
        "pre_cap_max_normal_turn_deg_u_le_0_98": max(row["max_normal_turn_deg"] for row in rows if row["u"] <= 0.98),
        "near_pole_max_normal_turn_deg_u_ge_0_995": max(row["max_normal_turn_deg"] for row in rows if row["u"] >= 0.995),
        "interpretation": "Topology-independent source-space probe. Increasing turn near u→1 is evidence about the analytic termination field, not proof that the rendered pinch is Source-primary."
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
    contract = load(a.isolation_contract)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    template = r2.apply(seed, r2_fix)
    r2_native = rt.extract_native_source(template)
    deck = bpy.data.objects.get(rt.NAMES["INTERFACE_DECK_BOUNDARY"])
    if deck is None:
        raise RuntimeError("Blender-native INTERFACE_DECK_BOUNDARY source object missing")
    original = {key: deck[key] for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m", "theta_center_rad", "theta_center_semantics", "blend")}
    set_interface(deck, confirmed["source_overrides"])
    working_source = rt.extract_native_source(template)
    working_digest = iso.source_digest(working_source)
    interface_diff = rt.source_difference(r2_native, working_source)
    for key, value in original.items():
        deck[key] = value
    restored = rt.extract_native_source(template)
    restore_error = rt.source_difference(r2_native, restored)

    machine, _ = qa.evaluate(working_source, r2_fix, False)
    pole_probe = source_pole_probe(working_source, contract)

    surface_runtime, runtime_identity = iso.load_surface_runtime(binding)
    scene = bpy.context.scene
    surface_runtime.render_setup(scene, execution["runtime"], a.resolution)
    scene.view_settings.exposure = -1.20
    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections missing")

    baseline, baseline_verts, baseline_faces, _ = rt.replace_derived("OL_DERIVED_G1_R4_TERMINATION_BASELINE", working_source, derived_collection, False)
    baseline["OLEANDER_R4_TOPOLOGY_ROLE"] = "BASELINE_UNIFORM_POLE_FAN"
    baseline["OLEANDER_SOURCE_DIGEST"] = working_digest

    dense_source = copy.deepcopy(working_source)
    dense_source["derived_execution"]["u_rings"] = int(contract["topology_variants"]["dense"]["u_rings"])
    dense_source["derived_execution"]["circumferential_samples"] = int(contract["topology_variants"]["dense"]["circumferential_samples"])
    dense, dense_verts, dense_faces, _ = rt.replace_derived("OL_DERIVED_G1_R4_TERMINATION_DENSE", dense_source, derived_collection, False)
    dense["OLEANDER_R4_TOPOLOGY_ROLE"] = "DENSE_UNIFORM_POLE_FAN"
    dense["OLEANDER_SOURCE_DIGEST"] = working_digest

    base_nu = int(contract["topology_variants"]["pole_refined"]["base_u_rings"])
    nv = int(contract["topology_variants"]["pole_refined"]["circumferential_samples"])
    u_values = [i / (base_nu + 1) for i in range(1, base_nu + 1)]
    u_values.extend(float(v) for v in contract["topology_variants"]["pole_refined"]["extra_u_rings"])
    u_values = sorted(set(u_values))
    refined, refined_verts, refined_faces = replace_custom(
        "OL_DERIVED_G1_R4_TERMINATION_POLE_REFINED",
        working_source,
        derived_collection,
        u_values,
        nv,
        "POLE_REFINED_ANALYTIC_SAMPLING",
    )

    local = contract["local_view"]
    target_u = float(local["target_u"])
    axis_target = base.bezier(base.own(working_source, "GRIP_AXIS")["control_points"], target_u)
    target = tuple(float(v) for v in axis_target)
    offset = tuple(float(v) for v in local["offset_from_target_m"])
    location = tuple(target[i] + offset[i] for i in range(3))
    old = bpy.data.objects.get(local["name"])
    if old is not None:
        bpy.data.objects.remove(old, do_unlink=True)
    camera = surface_runtime.camera(local["name"], float(local["lens_mm"]), location, target, qa_collection)
    camera["OLEANDER_R4_ROLE"] = "TERMINATION_LOCAL_ISOLATION_CAMERA"

    renders = {}
    for key, obj in (("baseline", baseline), ("dense", dense), ("pole_refined", refined)):
        iso.set_only_rendered(derived_collection, obj)
        renders[key] = render_set(surface_runtime, binding, out, qa_collection, obj, camera, f"R4_TERMINATION_{key.upper()}")

    image_diffs = {}
    for key in ("dense", "pole_refined"):
        image_diffs[key] = {
            rig: iso.image_difference(out / renders["baseline"][rig], out / renders[key][rig])
            for rig in ("STRIP", "GRAZING", "ZEBRA")
        }

    variant_geometry = {
        "baseline": {
            "vertices": len(baseline_verts),
            "faces": len(baseline_faces),
            "last_uniform_ring_u": 56 / 57,
            "authority": baseline.get("OLEANDER_AUTHORITY"),
            "source_digest": baseline.get("OLEANDER_SOURCE_DIGEST"),
        },
        "dense": {
            "vertices": len(dense_verts),
            "faces": len(dense_faces),
            "last_uniform_ring_u": 112 / 113,
            "authority": dense.get("OLEANDER_AUTHORITY"),
            "source_digest": dense.get("OLEANDER_SOURCE_DIGEST"),
        },
        "pole_refined": {
            "vertices": len(refined_verts),
            "faces": len(refined_faces),
            "extra_u_rings": contract["topology_variants"]["pole_refined"]["extra_u_rings"],
            "last_ring_u": max(u_values),
            "authority": refined.get("OLEANDER_AUTHORITY"),
            "source_digest": refined.get("OLEANDER_SOURCE_DIGEST"),
        },
    }

    all_render_names = [name for group in renders.values() for name in group.values()]
    checks = {
        "confirmed_interface_is_only_difference_from_r2_native_input": [k for k, v in interface_diff.items() if v > 1e-8] == ["INTERFACE_DECK_BOUNDARY"],
        "saved_blender_source_restored_after_confirmed_interface_readback": max(restore_error.values()) <= 1e-12,
        "existing_machine_qa_passes_on_confirmed_working_source": all(machine["checks"].values()),
        "same_source_digest_across_all_topology_variants": len({row["source_digest"] for row in variant_geometry.values()}) == 1,
        "all_topology_variants_derived_not_authority": all(row["authority"] == "DERIVED_EXECUTION_NOT_AUTHORITY" for row in variant_geometry.values()),
        "dense_is_materially_denser": variant_geometry["dense"]["faces"] > 3 * variant_geometry["baseline"]["faces"],
        "pole_refined_samples_closer_to_endpoint": variant_geometry["pole_refined"]["last_ring_u"] > variant_geometry["dense"]["last_uniform_ring_u"],
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "local_camera_created_via_shared_runtime": camera.get("OLEANDER_ROLE") == "F1_DIAGNOSTIC_CAMERA",
        "all_fixed_rig_renders_written": all((out / name).exists() for name in all_render_names),
        "source_edit_during_isolation_forbidden": contract["policy"]["source_edit_during_isolation_forbidden"] is True,
        "candidate_promotion_still_blocked": contract["policy"]["candidate_promotion"] == "NOT_RUN",
    }
    status = "R4_TERMINATION_ISOLATION_EXECUTED_VISUAL_CLASSIFICATION_REQUIRED" if all(checks.values()) else "R4_TERMINATION_ISOLATION_EXECUTION_FAIL"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.termination-isolation-report.v1",
        "status": status,
        "job_state": "R4_TERMINATION_SOURCE_VS_POLE_TOPOLOGY_ISOLATION_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "interface_relation_state": "CONFIRMED_LOCKED_FOR_R4",
        "termination_state": "OPEN_UNDER_ISOLATION",
        "working_source_digest": working_digest,
        "source_family_difference_r2_to_confirmed_working_source": interface_diff,
        "checks": checks,
        "machine_qa": machine,
        "source_space_pole_probe": pole_probe,
        "variant_geometry": variant_geometry,
        "local_camera": {"name": camera.name, "lens_mm": camera.data.lens, "location": list(camera.location), "target": list(target)},
        "renders": renders,
        "image_difference_metrics_vs_baseline": image_diffs,
        "classification": "NOT_RUN_REQUIRES_LOCAL_STRIP_GRAZING_ZEBRA_REVIEW",
        "classification_options": contract["classification_options"],
        "next_legal_action": "Review local topology A/B/C together with source-space pole probe; route the defect before any termination Source relation edit.",
        "boundary": contract["boundary"],
    }
    (out / "G1_R4_TERMINATION_ISOLATION_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("CLASSIFICATION_REQUIRED") else 7


if __name__ == "__main__":
    raise SystemExit(main())
