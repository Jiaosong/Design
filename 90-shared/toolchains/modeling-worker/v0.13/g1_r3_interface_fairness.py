#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
import math
from pathlib import Path
from typing import Any

import g1_geometry_core as base
import g1_r2_core as r2
import g1_r2_qa as qa


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
    return ordered[lo] * (1.0 - f) + ordered[hi] * f


def interior_fairness(source: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    spec = contract["sampling"]
    d = base.own(source, "INTERFACE_DECK_BOUNDARY")
    core = float(d["core_fraction"])
    u_samples = int(spec["u_samples"])
    theta_samples = int(spec["theta_samples"])
    du = float(spec["du"])
    dt = float(spec["dtheta_rad"])
    long_turns: list[float] = []
    circ_turns: list[float] = []
    combined: list[float] = []
    hotspot: dict[str, float] | None = None

    for i in range(u_samples):
        u = 0.02 + 0.96 * i / max(1, u_samples - 1)
        um = max(0.0001, u - du)
        up = min(0.9999, u + du)
        for j in range(theta_samples):
            theta = 2.0 * math.pi * j / theta_samples
            rho = r2.rho(source, u, theta)
            if not (core < rho < 1.0):
                continue
            longitudinal = qa.ang(qa.normal(source, um, theta), qa.normal(source, up, theta))
            circumferential = qa.ang(qa.normal(source, u, theta - dt), qa.normal(source, u, theta + dt))
            score = math.hypot(longitudinal, circumferential)
            long_turns.append(longitudinal)
            circ_turns.append(circumferential)
            combined.append(score)
            if hotspot is None or score > hotspot["combined_turn_score"]:
                hotspot = {
                    "u": u,
                    "theta_rad": theta,
                    "rho_interface": rho,
                    "longitudinal_normal_turn_deg_per_0_01u": longitudinal,
                    "circumferential_normal_turn_deg_per_0_05rad": circumferential,
                    "combined_turn_score": score,
                }

    limits = contract["threshold_basis"]["derived_working_limits"]
    metrics = {
        "sample_count": len(combined),
        "max_longitudinal_deg_per_0_01u": max(long_turns) if long_turns else 0.0,
        "p95_longitudinal_deg_per_0_01u": percentile(long_turns, 0.95),
        "max_circumferential_deg_per_0_05rad": max(circ_turns) if circ_turns else 0.0,
        "p95_circumferential_deg_per_0_05rad": percentile(circ_turns, 0.95),
        "max_combined_turn_score": max(combined) if combined else 0.0,
        "p95_combined_turn_score": percentile(combined, 0.95),
        "hotspot": hotspot,
    }
    checks = {
        "samples_present": metrics["sample_count"] > 0,
        "max_longitudinal": metrics["max_longitudinal_deg_per_0_01u"] <= float(limits["max_longitudinal_deg_per_0_01u"]),
        "p95_longitudinal": metrics["p95_longitudinal_deg_per_0_01u"] <= float(limits["p95_longitudinal_deg_per_0_01u"]),
        "max_circumferential": metrics["max_circumferential_deg_per_0_05rad"] <= float(limits["max_circumferential_deg_per_0_05rad"]),
        "p95_circumferential": metrics["p95_circumferential_deg_per_0_05rad"] <= float(limits["p95_circumferential_deg_per_0_05rad"]),
        "max_combined": metrics["max_combined_turn_score"] <= float(limits["max_combined_turn_score"]),
    }
    return {
        "metrics": metrics,
        "checks": checks,
        "pass": all(checks.values()),
        "threshold_role": contract["threshold_basis"]["threshold_status"],
    }


def apply_variant(base_source: dict[str, Any], variant: dict[str, Any], variants_contract: dict[str, Any], fairness_contract: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(base_source)
    d = base.own(out, "INTERFACE_DECK_BOUNDARY")
    locked = variants_contract["locked_values"]
    if d.get("theta_center") != fairness_contract["source_policy"]["theta_center_semantics_locked"]:
        raise RuntimeError("R3 cannot change the locked TOP_MERIDIAN semantic")
    for key, expected in locked.items():
        if key == "blend":
            if str(d.get(key)) != str(expected):
                raise RuntimeError(f"Locked value mismatch for {key}")
        elif key == "theta_center":
            if str(d.get(key)) != str(expected):
                raise RuntimeError(f"Locked value mismatch for {key}")
    overrides = variant["source_overrides"]
    allowed = {"u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"}
    if set(overrides) - allowed:
        raise RuntimeError(f"Illegal R3 source parameter(s): {sorted(set(overrides)-allowed)}")
    for key, value in overrides.items():
        d[key] = float(value)
    if abs(float(d["depth_m"]) - float(fairness_contract["source_policy"]["preserve_r2_depth_m"])) > 1e-12:
        raise RuntimeError("R3 batch must preserve R2 interface depth")
    return out


def changed_parameters(base_source: dict[str, Any], candidate: dict[str, Any]) -> dict[str, dict[str, float]]:
    a = base.own(base_source, "INTERFACE_DECK_BOUNDARY")
    b = base.own(candidate, "INTERFACE_DECK_BOUNDARY")
    out: dict[str, dict[str, float]] = {}
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "depth_m", "core_fraction"):
        av = float(a[key])
        bv = float(b[key])
        if abs(av - bv) > 1e-12:
            out[key] = {"from": av, "to": bv, "delta": bv - av}
    return out


def machine_result(source: dict[str, Any], r2_fix: dict[str, Any]) -> dict[str, Any]:
    result, _ = qa.evaluate(source, r2_fix, False)
    return {
        "checks": result["checks"],
        "pass": all(result["checks"].values()),
        "dimensions_m": result["dimensions_m"],
        "interface_depth_m": result["interface_depth_m"],
        "broad_fairness": result["broad_fairness"],
        "outer_continuity_deg": result["outer_continuity_deg"],
        "core_continuity_deg": result["core_continuity_deg"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--r2-correction", required=True)
    parser.add_argument("--contract", required=True)
    parser.add_argument("--variants", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    source_seed = json.loads(Path(args.source).read_text(encoding="utf-8"))
    r2_fix = json.loads(Path(args.r2_correction).read_text(encoding="utf-8"))
    contract = json.loads(Path(args.contract).read_text(encoding="utf-8"))
    variants_contract = json.loads(Path(args.variants).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    r2_source = r2.apply(source_seed, r2_fix)
    baseline_machine = machine_result(r2_source, r2_fix)
    baseline_fairness = interior_fairness(r2_source, contract)

    results = []
    visual_candidates = []
    for variant in variants_contract["variants"]:
        candidate = apply_variant(r2_source, variant, variants_contract, contract)
        machine = machine_result(candidate, r2_fix)
        fairness = interior_fairness(candidate, contract)
        eligible = machine["pass"] and fairness["pass"]
        snapshot_name = f"{variant['variant_id']}_WORKING_SOURCE_EXPERIMENT.json"
        snapshot = {
            "schema": "oleander.modeling-worker.v0.13.g1.r3.working-source-experiment.v1",
            "variant_id": variant["variant_id"],
            "authority": "WORKING_SOURCE_EXPERIMENT_NOT_PROMOTED",
            "source": candidate,
            "boundary": "Diagnostic Source-relation experiment only; not Candidate or Canonical authority.",
        }
        (out / snapshot_name).write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
        row = {
            "variant_id": variant["variant_id"],
            "design_question": variant["design_question"],
            "changed_parameters": changed_parameters(r2_source, candidate),
            "machine": machine,
            "interior_fairness": fairness,
            "visual_qa_eligible": eligible,
            "source_snapshot": snapshot_name,
        }
        results.append(row)
        if eligible:
            visual_candidates.append(variant["variant_id"])

    ranked = sorted(
        results,
        key=lambda row: (
            not row["visual_qa_eligible"],
            float(row["interior_fairness"]["metrics"]["max_combined_turn_score"]),
            len(row["changed_parameters"]),
        ),
    )
    selected = ranked[0]["variant_id"] if ranked and ranked[0]["visual_qa_eligible"] else None
    checks = {
        "r2_baseline_machine_still_passes": baseline_machine["pass"],
        "r2_baseline_exposes_interior_fairness_failure": not baseline_fairness["pass"],
        "mesh_local_patch_forbidden": variants_contract["mesh_local_patch_allowed"] is False,
        "only_interface_boundary_family_varied": variants_contract["allowed_source_family"] == "INTERFACE_DECK_BOUNDARY",
        "r2_depth_preserved_by_all_variants": all(abs(float(row["machine"]["interface_depth_m"]) - 0.012) <= 1e-9 for row in results),
        "at_least_one_variant_opens_visual_qa": bool(visual_candidates),
        "candidate_promotion_still_blocked": contract["candidate_promotion"] == "NOT_RUN",
    }
    status = "R3_INTERFACE_FAIRNESS_VARIANT_READY_FOR_VISUAL_QA" if all(checks.values()) else "R3_INTERFACE_FAIRNESS_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r3.interface-fairness-report.v1",
        "status": status,
        "job_state": "R3_INTERIOR_TRANSITION_FAIRNESS_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "checks": checks,
        "threshold_basis": contract["threshold_basis"],
        "baseline": {
            "variant_id": variants_contract["baseline"]["variant_id"],
            "machine": baseline_machine,
            "interior_fairness": baseline_fairness,
        },
        "variants": results,
        "visual_candidates": visual_candidates,
        "selected_for_fixed_rig_visual_diagnostics": selected,
        "termination_state": contract["known_open_defects"]["right_front_termination"],
        "next_legal_action": "Render Machine+Fairness PASS R3 variant(s) through fixed shared Surface System Strip/Grazing/Zebra; keep visual decision separate from machine gate.",
        "boundary": contract["boundary"],
    }
    (out / "G1_R3_INTERFACE_FAIRNESS_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("READY_FOR_VISUAL_QA") else 5


if __name__ == "__main__":
    raise SystemExit(main())
