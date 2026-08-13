#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 E3 R3.3 Primary-Curve relation revision.

R3.3 does not change the retained R3 Surface Source architecture. It composes the validated
R3.2 termination correction, then revises only Profile / Plan Primary Curves and
working-fidelity semantic edit amplitudes. Existing Machine thresholds remain unchanged.
Machine PASS opens Human Project/Visual QA only; PAP and Promotion remain blocked.
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
R32_PATH = HERE / "e3_r32_coupled_surface_entry.py"
spec = importlib.util.spec_from_file_location("oleander_e3_r32", R32_PATH)
r32 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(r32)
base = r32.base
bpy = r32.bpy

MODEL = "OLEANDER_ModelingWorker_v0.12_E3_R3_3_PrimaryCurveRelationRevision"


def user_args() -> list[str]:
    return sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]


def apply_r33(base_contract: dict[str, Any], r32_fix: dict[str, Any], r33_fix: dict[str, Any]) -> dict[str, Any]:
    contract = r32.apply_correction(base_contract, r32_fix)
    for key, expected in r33_fix["locked_architecture"].items():
        actual = contract["architecture"].get(key)
        if actual != expected:
            raise ValueError(f"R3.3 architecture drift: {key}={actual!r}, expected {expected!r}")

    for curve, values in r33_fix["profile_primary_curve_overrides"].items():
        if len(values) != len(contract["profile_primary_curves"][curve]):
            raise ValueError(f"R3.3 profile control count changed: {curve}")
        contract["profile_primary_curves"][curve] = [float(v) for v in values]
    for curve, values in r33_fix["plan_primary_curve_overrides"].items():
        if len(values) != len(contract["plan_primary_curves"][curve]):
            raise ValueError(f"R3.3 plan control count changed: {curve}")
        contract["plan_primary_curves"][curve] = [float(v) for v in values]

    for cid, deltas in r33_fix["semantic_delta_overrides"].items():
        edits = contract["semantic_controls"][cid]
        if len(edits) != len(deltas):
            raise ValueError(f"R3.3 semantic edit count changed: {cid}")
        for edit, delta in zip(edits, deltas):
            edit["delta"] = float(delta)

    contract["revision"] = r33_fix["revision"]
    contract["job_id"] = "SYS-MODELING-WORKER-v0.12-AUTO-E3-R3.3"
    contract["decision_question"] = r33_fix["decision_question"]
    contract["boundary"] = r33_fix["boundary"]
    return contract


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-contract", required=True)
    ap.add_argument("--r32-correction", required=True)
    ap.add_argument("--r33-correction", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--resolution", type=int, default=512)
    args = ap.parse_args(user_args())

    base_contract = json.loads(Path(args.base_contract).read_text(encoding="utf-8"))
    r32_fix = json.loads(Path(args.r32_correction).read_text(encoding="utf-8"))
    r33_fix = json.loads(Path(args.r33_correction).read_text(encoding="utf-8"))
    contract = apply_r33(base_contract, r32_fix, r33_fix)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    base_report, base_net = r32.evaluate_core(contract, r32_fix)
    th = contract["machine_thresholds"]
    variants: dict[str, Any] = {}
    all_exact = True
    all_machine = True
    all_effect = True

    for cid in contract["semantic_controls"]:
        vc, declared = base.apply_control(contract, cid)
        actual = base.changed_keys(contract, vc)
        vr, vnet = r32.evaluate_core(vc, r32_fix)
        displacement = base.max_displacement(base_net, vnet)
        exact = actual == declared
        authority_effect = r32.r31.direct_authority_effect(contract, vc, declared)
        machine = all(vr["checks"].values())
        legible = float(th["min_semantic_surface_displacement"]) <= displacement <= float(th["max_semantic_surface_displacement"])
        variants[cid] = {
            "declared_source_keys": [list(k) for k in sorted(declared, key=str)],
            "actual_changed_source_keys": [list(k) for k in sorted(actual, key=str)],
            "source_edit_exact": exact,
            "direct_declared_authority_effect": authority_effect,
            "max_surface_displacement": displacement,
            "working_fidelity_legible": legible,
            "machine_surface_pass": machine,
            "zoned_fairness": vr["zoned_fairness"],
            "profile_metrics": vr["profile_metrics"],
            "plan_metrics": vr["plan_metrics"],
        }
        all_exact = all_exact and exact
        all_machine = all_machine and machine and legible
        all_effect = all_effect and authority_effect["pass"]

    checks = {
        **base_report["checks"],
        "r3_architecture_locked": True,
        "r32_termination_correction_retained": True,
        "primary_curve_control_count_unchanged": all(len(v) == 9 for v in contract["profile_primary_curves"].values()) and all(len(v) == 9 for v in contract["plan_primary_curves"].values()),
        "semantic_source_edits_exact": all_exact,
        "all_semantic_variants_surface_pass": all_machine,
        "semantic_authority_domain_effects_present": all_effect,
        "machine_pass_only_opens_human_review": True,
    }
    status = "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" if all(checks.values()) else "MACHINE_FAIL_REVISE_E3_R3_3_PRIMARY_CURVE_RELATION"
    report = {
        "schema": "oleander.modeling-worker.v0.12.e3.r3.3.machine-report",
        "model": MODEL,
        "status": status,
        "decision_question": contract["decision_question"],
        "checks": checks,
        "base": base_report,
        "semantic_variants": variants,
        "r33_correction": r33_fix,
        "boundary": "R3.3 changes only Profile / Plan Primary Curve relationships and working-fidelity semantic edit amplitudes. R3 architecture, R3.2 termination correction, Machine thresholds, PAP boundary and human-owned Promotion are unchanged. Machine PASS opens Human Project/Visual QA only."
    }

    scene, row_count = base.render_set(base_net, out, args.resolution, "R3_3_BASE", True)
    scene["OLEANDER_MODEL"] = MODEL
    scene["OLEANDER_STAGE"] = "E3_R3_3_APPLICATION_MACHINE"
    scene["OLEANDER_AUTHORITY"] = "WORKING_SURFACE_SOURCE"
    scene["OLEANDER_R33_CORRECTION"] = json.dumps(r33_fix, ensure_ascii=False)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / f"{MODEL}.blend"))

    for cid in contract["semantic_controls"]:
        vc, _ = base.apply_control(contract, cid)
        _, vnet = r32.evaluate_core(vc, r32_fix)
        base.render_set(vnet, out, args.resolution, cid.replace("-", "_"), False)

    (out / "E3_R33_MACHINE_REPORT.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "E3_R33_COMPILED_SURFACE_SOURCE.json").write_text(json.dumps({
        "schema": "oleander.modeling-worker.v0.12.e3.r3.3.compiled-surface-source",
        "authority": "WORKING_SURFACE_SOURCE",
        "revision": "R3.3",
        "profile_primary_curves": contract["profile_primary_curves"],
        "plan_primary_curves": contract["plan_primary_curves"],
        "surface_sources": contract["surface_sources"],
        "relationship_graph": contract["relationship_graph"],
        "semantic_controls": contract["semantic_controls"],
        "qa_semantics": "SOURCE_RELATION / RUNTIME_DIAGNOSTIC / BROAD_INTERIOR / CHARACTER_BAND / INTENTIONAL_BOUNDARY",
        "execution_geometry": {"derived": True, "editable_authority": False, "sample_rows": row_count}
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "MACHINE_PASS_HUMAN_PROJECT_VISUAL_REVIEW_REQUIRED" else 5


if __name__ == "__main__":
    raise SystemExit(main())
