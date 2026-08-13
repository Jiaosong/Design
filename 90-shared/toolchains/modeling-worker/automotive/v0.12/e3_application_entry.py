#!/usr/bin/env python3
"""Automotive v0.12 E3 — application benchmark consuming the generic v0.12 compiler.

This file is application code, not a new generic Modeling Worker method. It imports the
existing E2 precision-aware C2 compiler, supplies an Automotive low-frequency Surface
Source, applies declared semantic source edits, and verifies that those edits stay bounded
at source level while derived patch changes continue to satisfy the generic fairness gates.

Machine PASS here only opens Human Project/Visual review. It does not establish Automotive
design authority, Class-A, engineering, manufacturing, PAP or system Promotion.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
GENERIC_PRECISION_ENTRY = HERE.parents[1] / "v0.12" / "e2_precision_entry.py"
_spec = importlib.util.spec_from_file_location("oleander_v012_precision", GENERIC_PRECISION_ENTRY)
precision = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(precision)
e2 = precision.e2

MODEL = "OLEANDER_ModelingWorker_v0.12_E3_AutomotiveApplication"


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def changed_indices(base: list[list[list[float]]], variant: list[list[list[float]]], tol: float = 1e-12) -> set[tuple[int, int]]:
    changed: set[tuple[int, int]] = set()
    for i in range(4):
        for j in range(4):
            if any(abs(float(a) - float(b)) > tol for a, b in zip(base[i][j], variant[i][j])):
                changed.add((i, j))
    return changed


def apply_semantic_control(base: list[list[list[float]]], control: dict[str, Any]) -> tuple[list[list[list[float]]], set[tuple[int, int]]]:
    cage = copy.deepcopy(base)
    declared: set[tuple[int, int]] = set()
    for edit in control["edits"]:
        i, j = (int(edit["index"][0]), int(edit["index"][1]))
        delta = [float(x) for x in edit["delta"]]
        declared.add((i, j))
        cage[i][j] = [float(cage[i][j][k]) + delta[k] for k in range(3)]
    return cage, declared


def evaluate_variant(contract: dict[str, Any], center_cage: list[list[list[float]]]) -> tuple[dict[str, Any], dict[str, Any]]:
    local = copy.deepcopy(contract)
    local["center_patch_cage"] = center_cage
    network = e2.compile_c2_chain(center_cage, local["termination_boundaries"]["front"], local["termination_boundaries"]["rear"])
    report = e2.evaluate_network(local, network)
    return network, report


def make_scene(contract: dict[str, Any], center_cage: list[list[list[float]]], out: Path, resolution: int, tag: str, full_views: bool) -> tuple[dict[str, Any], Any]:
    network = e2.compile_c2_chain(center_cage, contract["termination_boundaries"]["front"], contract["termination_boundaries"]["rear"])
    e2.clear_scene()
    clay = e2.material(f"MAT-{tag}-CLAY", (0.36, 0.38, 0.41), 0.30)
    cage_mat = e2.material(f"MAT-{tag}-CAGE", (0.025, 0.025, 0.03), 0.42)
    seam_mat = e2.material(f"MAT-{tag}-SEAM", (0.72, 0.74, 0.78), 0.22, 0.15)
    zebra = e2.zebra_material()
    ordered = [
        e2.Patch("PATCH-FRONT-TERMINATION", network["PATCH-FRONT-TERMINATION"]),
        e2.Patch("PATCH-CENTER-VOLUME", network["PATCH-CENTER-VOLUME"]),
        e2.Patch("PATCH-REAR-TERMINATION", network["PATCH-REAR-TERMINATION"]),
    ]
    surface, _, _ = e2.build_execution_mesh(ordered)
    surface.name = f"{tag}_DERIVED_EXECUTION_SURFACE"
    surface.data.name = f"{tag}_DERIVED_EXECUTION_MESH"
    diagnostics = e2.cage_diagnostics(network, cage_mat, seam_mat)
    scene = e2.scene_setup(resolution)
    target = (0.0, 0.0, 0.68)

    if full_views:
        cams = {
            "E3_HERO_APPLICATION": e2.camera("CAM-E3-HERO", (4.2, 4.4, 2.7), target, 5.7),
            "E3_SIDE_APPLICATION": e2.camera("CAM-E3-SIDE", (0.0, 6.2, 1.0), target, 5.6),
            "E3_TOP_APPLICATION": e2.camera("CAM-E3-TOP", (0.0, 0.2, 6.4), (0.0, 0.0, 0.55), 5.7),
            "E3_ZEBRA_APPLICATION": e2.camera("CAM-E3-ZEBRA", (4.3, 4.1, 2.4), target, 5.6),
        }
        e2.render(scene, out, cams["E3_HERO_APPLICATION"], "E3_HERO_APPLICATION", surface, clay)
        e2.render(scene, out, cams["E3_SIDE_APPLICATION"], "E3_SIDE_APPLICATION", surface, clay)
        e2.render(scene, out, cams["E3_TOP_APPLICATION"], "E3_TOP_APPLICATION", surface, clay)
        for obj in diagnostics:
            obj.hide_render = True
        e2.render(scene, out, cams["E3_ZEBRA_APPLICATION"], "E3_ZEBRA_APPLICATION", surface, zebra)
        for obj in diagnostics:
            obj.hide_render = False
    else:
        cam = e2.camera(f"CAM-{tag}-SIDE", (0.0, 6.2, 1.0), target, 5.6)
        e2.render(scene, out, cam, f"E3_VARIANT_{tag}_SIDE", surface, clay)

    return network, scene


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--resolution", type=int, default=512)
    args = ap.parse_args(user_args())

    contract = load_json(args.contract)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    base_cage = contract["center_patch_cage"]
    base_network, base_report = evaluate_variant(contract, base_cage)

    variant_rows: dict[str, Any] = {}
    all_source_edits_exact = True
    all_variants_machine_pass = True
    for control_id, control in contract["application_controls"].items():
        variant_cage, declared = apply_semantic_control(base_cage, control)
        actual = changed_indices(base_cage, variant_cage)
        network, report = evaluate_variant(contract, variant_cage)
        exact = actual == declared
        machine_pass = report["status"] == "MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED" and all(report["checks"].values())
        all_source_edits_exact = all_source_edits_exact and exact
        all_variants_machine_pass = all_variants_machine_pass and machine_pass
        variant_rows[control_id] = {
            "declared_source_indices": sorted([list(x) for x in declared]),
            "actual_changed_source_indices": sorted([list(x) for x in actual]),
            "source_edit_exact": exact,
            "machine_status": report["status"],
            "checks": report["checks"],
            "front_seam": report["front_seam"],
            "rear_seam": report["rear_seam"],
            "patch_fairness": report["patch_fairness"],
            "derived_network_changed": network != base_network,
        }

    checks = {
        "generic_precision_compiler_consumed": True,
        "base_machine_fairness_pass": base_report["status"] == "MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED" and all(base_report["checks"].values()),
        "semantic_source_edits_exact": all_source_edits_exact,
        "all_declared_volume_variants_machine_pass": all_variants_machine_pass,
        "surface_source_separate_from_execution_geometry": contract["authority"]["surface_source"] == "WORKING_SOURCE" and contract["authority"]["execution_geometry"] == "DERIVED",
        "termination_is_surface_patch_not_mesh_closure": contract["compiler_policy"]["mesh_closure_for_termination_forbidden"] is True,
        "execution_topology_after_surface_compile": contract["compiler_policy"]["execution_topology_generated_after_surface_compile"] is True,
    }
    status = "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_E3_SOURCE"

    report = {
        "schema": "oleander.modeling-worker.v0.12.e3.application-machine-report",
        "model": MODEL,
        "status": status,
        "decision_question": contract["decision_question"],
        "checks": checks,
        "base_surface_fairness": base_report,
        "semantic_control_variants": variant_rows,
        "boundary": "Machine PASS proves only that declared application source edits are bounded and remain compatible with the existing generic C2/fairness compiler. Human Project/Visual QA, PAP and system Promotion remain open."
    }

    # Render the base application source and four semantic-edit diagnostics.
    _, base_scene = make_scene(contract, base_cage, out, args.resolution, "BASE", True)
    base_scene["OLEANDER_MODEL"] = MODEL
    base_scene["OLEANDER_STAGE"] = "E3_APPLICATION_MACHINE"
    base_scene["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    base_scene["OLEANDER_DECISION_QUESTION"] = contract["decision_question"]
    base_scene["OLEANDER_EXECUTION_SPEC"] = json.dumps(contract, ensure_ascii=False)
    blend_path = out / f"{MODEL}.blend"
    e2.bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    for control_id, control in contract["application_controls"].items():
        variant_cage, _ = apply_semantic_control(base_cage, control)
        make_scene(contract, variant_cage, out, args.resolution, control_id.replace("VOL-", ""), False)

    (out / "E3_APPLICATION_MACHINE_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "E3_COMPILED_SURFACE_SOURCE.json").write_text(json.dumps({
        "schema": "oleander.modeling-worker.v0.12.e3.compiled-surface-source",
        "authority": "WORKING_SURFACE_SOURCE",
        "object_id": "SYS-MODELING-WORKER-v0.12-E3-AUTO",
        "source": "E3_SURFACE_EXECUTION_SPEC.json",
        "center_patch_cage": base_cage,
        "termination_boundaries": contract["termination_boundaries"],
        "compiled_network": base_network,
        "execution_geometry": {"derived": True, "editable_authority": False}
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" else 5


if __name__ == "__main__":
    raise SystemExit(main())
