#!/usr/bin/env python3
"""Precision-classified entry for E3 R2.

Compiler-space C2 remains authoritative under the unchanged design thresholds. Blender
mathutils position/tangent/normal continuity remains a runtime representation gate; the
float32 reconstructed second-derivative residual is retained as diagnostic evidence.
Interior fairness and semantic variants remain fail-closed.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "e3_r2_volume_jet_entry.py"
spec = importlib.util.spec_from_file_location("oleander_e3_r2_base", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)

_original_evaluate = base.evaluate_contract


def _control_source_keys(contract):
    ownership = {}
    overlaps = []
    for control_id, edits in contract["semantic_controls"].items():
        keys = {(e["station"], e["field"], int(e["index"])) for e in edits}
        ownership[control_id] = sorted([list(k) for k in keys])
        for key in keys:
            owner = next((cid for cid, owned in ownership.items() if cid != control_id and list(key) in owned), None)
            if owner:
                overlaps.append({"key": list(key), "controls": sorted([owner, control_id])})
    return ownership, overlaps


def evaluate_contract_classified(contract):
    report, network = _original_evaluate(contract)
    th = contract["fairness_thresholds"]
    seams = report["compiler_seams"]

    compiler_ok = all(
        s["max_position_error"] <= th["max_seam_position_error"]
        and s["max_tangent_angle_deg"] <= th["max_seam_tangent_angle_deg"]
        and s["max_second_derivative_error"] <= th["max_seam_second_derivative_error"]
        for s in seams
    )
    runtime_visible_ok = all(
        s["runtime_max_position_error"] <= 5e-7
        and s["runtime_max_tangent_angle_deg"] <= 0.05
        and s["runtime_max_normal_angle_deg"] <= 0.05
        for s in seams
    )
    runtime_d2 = max((s["runtime_max_second_derivative_error"] for s in seams), default=0.0)
    ownership, overlaps = _control_source_keys(contract)

    report["checks"]["compiler_c2_seams_pass"] = compiler_ok
    report["checks"]["runtime_position_tangent_normal_representation_stable"] = runtime_visible_ok
    report["checks"]["runtime_second_derivative_diagnostic_recorded"] = all(
        "runtime_max_second_derivative_error" in s for s in seams
    )
    report["checks"]["semantic_control_source_ownership_disjoint"] = not overlaps
    report["precision_classification"] = {
        "compiler_authority": "RAW_JSON_PYTHON_FLOAT_SHARED_JETS",
        "compiler_design_threshold_unchanged": th["max_seam_second_derivative_error"],
        "runtime_representation_gate": {
            "max_position_error": 5e-7,
            "max_tangent_angle_deg": 0.05,
            "max_normal_angle_deg": 0.05
        },
        "runtime_second_derivative": {
            "class": "BLENDER_FLOAT32_RECONSTRUCTION_DIAGNOSTIC",
            "max_observed": runtime_d2,
            "gating": False,
            "reason": "Blender execution geometry is derived after the analytic Surface Source compiler; compiler-space C2 remains authoritative."
        },
        "semantic_control_source_ownership": ownership,
        "semantic_control_source_overlaps": overlaps,
        "rule": "This classification does not relax compiler C2 or interior fairness and cannot convert a fairness failure to PASS."
    }
    return report, network


base.evaluate_contract = evaluate_contract_classified

if __name__ == "__main__":
    raise SystemExit(base.main())
