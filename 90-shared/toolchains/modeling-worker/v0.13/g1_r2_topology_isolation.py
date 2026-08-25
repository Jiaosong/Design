#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import bpy

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import g1_r2_core as r2
import g1_r2_qa as qa
import g1_r2_blender_roundtrip as rt
import g1_r2_blender_scene as bs


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--correction", required=True)
    parser.add_argument("--binding", required=True)
    parser.add_argument("--isolation-contract", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--resolution", type=int, default=512)
    return parser.parse_args(sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:])


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_surface_runtime(binding: dict[str, Any]):
    runtime_binding = binding["runtime_binding"]
    module_path = ROOT / runtime_binding["module"]
    spec = importlib.util.spec_from_file_location("oleander_blender_surface_system_f1_runtime", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load shared Blender Surface System runtime: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    identity = module.validate_binding(binding, ROOT / runtime_binding["contract"])
    identity["module"] = runtime_binding["module"]
    identity["contract_path"] = runtime_binding["contract"]
    return module, identity


def source_digest(source: dict[str, Any]) -> str:
    payload = json.dumps(
        rt.source_numeric_snapshot(source),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def make_topology_object(name: str, source: dict[str, Any], topology: dict[str, int], collection):
    execution = copy.deepcopy(source)
    execution["derived_execution"]["u_rings"] = int(topology["u_rings"])
    execution["derived_execution"]["circumferential_samples"] = int(topology["circumferential_samples"])
    verts, faces, _ = r2.mesh(execution, False)
    old = bpy.data.objects.get(name)
    if old is not None:
        mesh = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if mesh and mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    obj = bs.mesh_obj(name, verts, faces, collection, "R2 topology-isolation derived execution geometry")
    obj["OLEANDER_TOPOLOGY_ISOLATION"] = True
    obj["OLEANDER_SOURCE_MODE"] = "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE"
    obj["OLEANDER_U_RINGS"] = int(topology["u_rings"])
    obj["OLEANDER_CIRC_SAMPLES"] = int(topology["circumferential_samples"])
    return obj, len(verts), len(faces)


def set_only_rendered(collection, target) -> None:
    for obj in collection.objects:
        if obj.type == "MESH" and obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY":
            obj.hide_render = obj != target


def require_surface_asset(name: str, kind: str):
    if kind == "material":
        asset = bpy.data.materials.get(name)
    elif kind == "object":
        asset = bpy.data.objects.get(name)
    else:
        raise ValueError(kind)
    if asset is None:
        raise RuntimeError(f"Required Surface System {kind} missing from saved .blend: {name}")
    return asset


def render_ab(surface_runtime, binding, out: Path, base_obj, dense_obj, qa_collection):
    camera = require_surface_asset("HERO_CAM", "object")
    profile = binding["runtime_binding"]["diagnostic_material_profile"]
    reflection = require_surface_asset(profile["reflection"]["name"], "material")
    zebra = require_surface_asset(profile["zebra"]["name"], "material")
    scene = bpy.context.scene
    renders: dict[str, dict[str, str]] = {}
    for rig in ("STRIP", "GRAZING", "ZEBRA"):
        mat = zebra if rig == "ZEBRA" else reflection
        set_only_rendered(base_obj.users_collection[0], base_obj)
        base_name = f"ISO_BASE_{rig}_PERSPECTIVE"
        base_file = surface_runtime.render(scene, out, base_name, camera, base_obj, mat, rig, qa_collection)
        set_only_rendered(dense_obj.users_collection[0], dense_obj)
        dense_name = f"ISO_DENSE_{rig}_PERSPECTIVE"
        dense_file = surface_runtime.render(scene, out, dense_name, camera, dense_obj, mat, rig, qa_collection)
        renders[rig] = {"baseline": base_file, "dense": dense_file}
    return renders


def percentile_from_hist(hist: list[int], q: float) -> float:
    total = sum(hist)
    if total == 0:
        return 0.0
    target = max(1, math.ceil(total * q))
    running = 0
    bins = len(hist) - 1
    for index, count in enumerate(hist):
        running += count
        if running >= target:
            return index / bins
    return 1.0


def image_difference(path_a: Path, path_b: Path) -> dict[str, float | int | str]:
    image_a = bpy.data.images.load(str(path_a), check_existing=False)
    image_b = bpy.data.images.load(str(path_b), check_existing=False)
    try:
        if tuple(image_a.size) != tuple(image_b.size):
            raise RuntimeError(f"Image size mismatch: {path_a.name} vs {path_b.name}")
        pixels_a = image_a.pixels[:]
        pixels_b = image_b.pixels[:]
        if len(pixels_a) != len(pixels_b):
            raise RuntimeError("Image pixel buffer length mismatch")
        hist = [0] * 1001
        total = 0.0
        maximum = 0.0
        count = 0
        for i in range(0, len(pixels_a), 4):
            for channel in range(3):
                delta = abs(float(pixels_a[i + channel]) - float(pixels_b[i + channel]))
                total += delta
                maximum = max(maximum, delta)
                hist[min(1000, int(delta * 1000.0))] += 1
                count += 1
        return {
            "width": int(image_a.size[0]),
            "height": int(image_a.size[1]),
            "channel_samples": count,
            "mean_abs_rgb": total / count if count else 0.0,
            "p95_abs_rgb": percentile_from_hist(hist, 0.95),
            "p99_abs_rgb": percentile_from_hist(hist, 0.99),
            "max_abs_rgb": maximum,
            "pixel_space": "BLENDER_IMAGE_PIXEL_BUFFER",
        }
    finally:
        bpy.data.images.remove(image_a)
        bpy.data.images.remove(image_b)


def analytic_source_hotspots(source: dict[str, Any], spec: dict[str, Any]):
    u_samples = int(spec["u_samples"])
    theta_samples = int(spec["theta_samples"])
    du = float(spec["du"])
    dt = float(spec["dtheta_rad"])
    rho_lo, rho_hi = [float(v) for v in spec["interface_rho_band"]]
    termination = float(spec["termination_u_band"])
    keep = int(spec["top_hotspots_per_zone"])
    zones: dict[str, list[dict[str, float | str]]] = {
        "INTERFACE_TRANSITION": [],
        "TERMINATION": [],
        "BROAD_SURFACE": [],
    }

    for i in range(u_samples):
        u = 0.02 + 0.96 * i / max(1, u_samples - 1)
        um = max(0.0001, u - du)
        up = min(0.9999, u + du)
        for j in range(theta_samples):
            theta = 2.0 * math.pi * j / theta_samples
            n_um = qa.normal(source, um, theta)
            n_up = qa.normal(source, up, theta)
            n_tm = qa.normal(source, u, theta - dt)
            n_tp = qa.normal(source, u, theta + dt)
            long_turn = qa.ang(n_um, n_up)
            circ_turn = qa.ang(n_tm, n_tp)
            score = math.hypot(long_turn, circ_turn)
            rho = r2.rho(source, u, theta)
            if rho_lo <= rho <= rho_hi:
                zone = "INTERFACE_TRANSITION"
            elif u <= termination or u >= 1.0 - termination:
                zone = "TERMINATION"
            else:
                zone = "BROAD_SURFACE"
            zones[zone].append(
                {
                    "zone": zone,
                    "u": u,
                    "theta_rad": theta,
                    "rho_interface": rho,
                    "longitudinal_normal_turn_deg_per_0_01u": long_turn,
                    "circumferential_normal_turn_deg_per_0_05rad": circ_turn,
                    "combined_turn_score": score,
                }
            )

    summary = {}
    all_hotspots = []
    for zone, values in zones.items():
        values.sort(key=lambda item: float(item["combined_turn_score"]), reverse=True)
        top = values[:keep]
        summary[zone] = {
            "sample_count": len(values),
            "max_combined_turn_score": float(top[0]["combined_turn_score"]) if top else 0.0,
            "top_hotspots": top,
        }
        all_hotspots.extend(top)
    all_hotspots.sort(key=lambda item: float(item["combined_turn_score"]), reverse=True)
    return {
        "sampling": {
            "u_samples": u_samples,
            "theta_samples": theta_samples,
            "du": du,
            "dtheta_rad": dt,
            "normal_turn_span_u": 2.0 * du,
            "normal_turn_span_theta_rad": 2.0 * dt,
        },
        "zones": summary,
        "global_top_hotspots": all_hotspots[:keep],
        "topology_independent": True,
    }


def classify(metrics: dict[str, dict[str, float]], contract: dict[str, Any]):
    bands = contract["visual_ab"]["heuristic_bands"]
    invariant = bands["topology_invariant"]
    sensitive = bands["topology_sensitive"]
    all_invariant = all(
        float(metric["mean_abs_rgb"]) <= float(invariant["mean_abs_rgb_max"])
        and float(metric["p99_abs_rgb"]) <= float(invariant["p99_abs_rgb_max"])
        for metric in metrics.values()
    )
    sensitive_count = sum(
        1
        for metric in metrics.values()
        if float(metric["mean_abs_rgb"]) >= float(sensitive["mean_abs_rgb_min"])
        and float(metric["p99_abs_rgb"]) >= float(sensitive["p99_abs_rgb_min"])
    )
    if all_invariant:
        return (
            "TOPOLOGY_INVARIANT_SOURCE_RELATION_SUSPECTED",
            "Re-enter Relation / Surface Source. Preserve both topology results as diagnostic evidence; do not patch the dense mesh locally.",
        )
    if sensitive_count >= int(sensitive["minimum_rigs"]):
        return (
            "TOPOLOGY_SENSITIVE_EXECUTION_GEOMETRY_SUSPECTED",
            "Re-enter Surface Construction / Execution Geometry using the same sparse Source; do not promote or alter Source authority yet.",
        )
    return (
        "INCONCLUSIVE_VISUAL_REVIEW_REQUIRED",
        "Review paired Strip / Grazing / Zebra renders before routing. Keep Working Source and Candidate Promotion blocked.",
    )


def main():
    a = args()
    source_seed = load(a.source)
    correction = load(a.correction)
    binding = load(a.binding)
    contract = load(a.isolation_contract)
    out = Path(a.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    template = r2.apply(source_seed, correction)
    source_before = rt.extract_native_source(template)
    source_digest_before = source_digest(source_before)

    surface_runtime, runtime_identity = load_surface_runtime(binding)
    scene = bpy.context.scene
    if scene.get("OLEANDER_SURFACE_SYSTEM_RUNTIME_API") != binding["runtime_binding"]["api"]:
        raise RuntimeError("Saved .blend is not bound to the expected shared Blender Surface System runtime")

    derived_collection = bpy.data.collections.get(binding["surface_evaluation"]["derived_collection"])
    qa_collection = bpy.data.collections.get(binding["surface_evaluation"]["qa_collection"])
    if derived_collection is None or qa_collection is None:
        raise RuntimeError("Expected derived/QA collections are missing from saved .blend")

    baseline_obj, baseline_vertices, baseline_faces = make_topology_object(
        "OL_ISO_R2_BASE_TOPOLOGY",
        source_before,
        contract["topologies"]["baseline"],
        derived_collection,
    )
    dense_obj, dense_vertices, dense_faces = make_topology_object(
        "OL_ISO_R2_DENSE_TOPOLOGY",
        source_before,
        contract["topologies"]["dense"],
        derived_collection,
    )

    renders = render_ab(surface_runtime, binding, out, baseline_obj, dense_obj, qa_collection)
    image_metrics = {
        rig: image_difference(out / pair["baseline"], out / pair["dense"])
        for rig, pair in renders.items()
    }
    analytic = analytic_source_hotspots(source_before, contract["analytic_source_probe"])

    source_after = rt.extract_native_source(template)
    source_digest_after = source_digest(source_after)
    source_error = rt.source_difference(source_before, source_after)
    classification, next_action = classify(image_metrics, contract)

    expected_renders = set(contract["outputs"]["renders"])
    actual_renders = {name for pair in renders.values() for name in pair.values()}
    checks = {
        "same_native_source_digest_before_after": source_digest_before == source_digest_after,
        "source_not_edited_during_isolation": max(source_error.values()) <= 1e-12,
        "baseline_derived_not_authority": baseline_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "dense_derived_not_authority": dense_obj.get("OLEANDER_AUTHORITY") == "DERIVED_EXECUTION_NOT_AUTHORITY",
        "dense_topology_materially_denser": dense_faces >= baseline_faces * 3.9,
        "shared_surface_system_runtime_verified": runtime_identity["status"] == "PASS" and all(runtime_identity["checks"].values()),
        "all_paired_renders_written": expected_renders == actual_renders and all((out / name).exists() for name in expected_renders),
        "analytic_probe_topology_independent": analytic["topology_independent"] is True,
        "candidate_promotion_still_blocked": contract["candidate_promotion"] == "NOT_RUN",
    }
    status = "TOPOLOGY_SOURCE_ISOLATION_EXECUTED" if all(checks.values()) else "TOPOLOGY_SOURCE_ISOLATION_FAIL_REVISE"

    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r2.topology-source-isolation-report.v1",
        "status": status,
        "classification": classification,
        "classification_role": "DIAGNOSTIC_ROUTING_HEURISTIC_NOT_PROMOTION_EVIDENCE",
        "job_state": "R2_TOPOLOGY_VS_SOURCE_ISOLATION_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "checks": checks,
        "source": {
            "mode": "BLENDER_NATIVE_EDITABLE_WORKING_SOURCE",
            "digest_before": source_digest_before,
            "digest_after": source_digest_after,
            "family_error_m": source_error,
            "unchanged": source_digest_before == source_digest_after and max(source_error.values()) <= 1e-12,
        },
        "topology": {
            "baseline": {
                **contract["topologies"]["baseline"],
                "vertices": baseline_vertices,
                "faces": baseline_faces,
                "object": baseline_obj.name,
                "authority": baseline_obj.get("OLEANDER_AUTHORITY"),
            },
            "dense": {
                **contract["topologies"]["dense"],
                "vertices": dense_vertices,
                "faces": dense_faces,
                "object": dense_obj.name,
                "authority": dense_obj.get("OLEANDER_AUTHORITY"),
            },
            "face_density_ratio": dense_faces / baseline_faces,
        },
        "shared_surface_system_runtime": runtime_identity,
        "visual_ab": {
            "camera": contract["visual_ab"]["camera"],
            "renders": renders,
            "metrics": image_metrics,
            "heuristic_bands": contract["visual_ab"]["heuristic_bands"],
            "threshold_role": contract["visual_ab"]["threshold_role"],
        },
        "analytic_source_probe": analytic,
        "next_legal_action": next_action,
        "boundary": contract["boundary"],
    }
    (out / contract["outputs"]["report"]).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "TOPOLOGY_SOURCE_ISOLATION_EXECUTED" else 7


if __name__ == "__main__":
    raise SystemExit(main())
