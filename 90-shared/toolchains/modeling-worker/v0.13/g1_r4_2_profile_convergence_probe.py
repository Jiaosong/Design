#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import g1_geometry_core as base
import g1_r2_core as r2
import g1_r2_qa as qa


def load(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def apply_confirmed_interface(source: dict[str, Any], confirmed: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(source)
    d = base.own(out, "INTERFACE_DECK_BOUNDARY")
    relation = confirmed["source_overrides"]
    for key in ("u_center", "u_halfspan", "theta_halfspan_rad", "core_fraction", "depth_m"):
        d[key] = float(relation[key])
    d["theta_center"] = str(relation["theta_center"])
    d.pop("theta_center_rad", None)
    d["blend"] = str(relation["blend"])
    return out


def source_digest(source: dict[str, Any]) -> str:
    payload = {
        "GRIP_AXIS": base.own(source, "GRIP_AXIS")["control_points"],
        "PALM_PROFILE": base.own(source, "PALM_PROFILE")["control_values"],
        "THUMB_SIDE_PLAN": base.own(source, "THUMB_SIDE_PLAN")["control_values"],
        "OPPOSITE_SIDE_PLAN": base.own(source, "OPPOSITE_SIDE_PLAN")["control_values"],
        "LOWER_RETURN_PROFILE": {
            "control_values": base.own(source, "LOWER_RETURN_PROFILE")["control_values"],
            "termination_envelope_exponent": float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55)),
        },
        "INTERFACE_DECK_BOUNDARY": base.own(source, "INTERFACE_DECK_BOUNDARY"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def envelope(source: dict[str, Any], u: float) -> float:
    exponent = float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))
    if not 0.0 < u < 1.0:
        return 0.0
    return math.sin(math.pi * u) ** exponent


def profile_amplitude(source: dict[str, Any], family: str, u: float) -> tuple[float, float]:
    raw = float(base.bezier(base.own(source, family)["control_values"], u))
    return raw, raw * envelope(source, u)


def derivative(fn, u: float, h: float = 1e-5) -> float:
    lo = max(0.000001, u - h)
    hi = min(0.999999, u + h)
    return (float(fn(hi)) - float(fn(lo))) / (hi - lo)


def axis_tangent(source: dict[str, Any], u: float) -> tuple[float, float, float]:
    pts = base.own(source, "GRIP_AXIS")["control_points"]
    h = 1e-5
    lo = max(0.0, u - h)
    hi = min(1.0, u + h)
    a = base.bezier(pts, lo)
    b = base.bezier(pts, hi)
    v = tuple(float(b[i]) - float(a[i]) for i in range(3))
    n = math.sqrt(sum(x * x for x in v))
    return tuple(x / n for x in v)


def angle(a, b) -> float:
    dot = sum(float(a[i]) * float(b[i]) for i in range(3))
    return math.degrees(math.acos(max(-1.0, min(1.0, dot))))


def probe_row(source: dict[str, Any], contract: dict[str, Any], u: float) -> dict[str, Any]:
    span = float(contract["normal_turn_span_u"])
    half = span / 2.0
    um = max(0.00001, u - half)
    up = min(0.9999, u + half)
    families = list(contract["profile_families"])

    profile_metrics: dict[str, Any] = {}
    palm_post = profile_amplitude(source, "PALM_PROFILE", u)[1]
    for family in families:
        raw, post = profile_amplitude(source, family, u)
        post_derivative = derivative(lambda x, f=family: profile_amplitude(source, f, x)[1], u)
        if family == "PALM_PROFILE":
            ratio = 1.0
            ratio_derivative = 0.0
        else:
            ratio = post / palm_post if palm_post else 0.0
            ratio_derivative = derivative(
                lambda x, f=family: profile_amplitude(source, f, x)[1] / profile_amplitude(source, "PALM_PROFILE", x)[1],
                u,
                h=1e-4,
            )
        profile_metrics[family] = {
            "raw_amplitude_m": raw,
            "post_envelope_amplitude_m": post,
            "post_envelope_longitudinal_derivative_m_per_u": post_derivative,
            "relative_amplitude_to_palm": ratio,
            "relative_ratio_longitudinal_derivative_per_u": ratio_derivative,
        }

    sectors = {
        name: qa.ang(qa.normal(source, um, float(theta)), qa.normal(source, up, float(theta)))
        for name, theta in contract["sectors"].items()
    }
    angular = []
    theta_samples = int(contract["theta_samples"])
    for j in range(theta_samples):
        theta = 2.0 * math.pi * j / theta_samples
        turn = qa.ang(qa.normal(source, um, theta), qa.normal(source, up, theta))
        angular.append((turn, theta))
    hotspot_turn, hotspot_theta = max(angular, key=lambda item: item[0])
    axis_turn = angle(axis_tangent(source, um), axis_tangent(source, up))
    relative_derivatives = {
        family: profile_metrics[family]["relative_ratio_longitudinal_derivative_per_u"]
        for family in families if family != "PALM_PROFILE"
    }
    return {
        "u": u,
        "normal_turn_span_u": up - um,
        "termination_envelope": envelope(source, u),
        "profiles": profile_metrics,
        "sector_normal_turn_deg": sectors,
        "hotspot": {
            "theta_rad": hotspot_theta,
            "theta_deg": math.degrees(hotspot_theta),
            "normal_turn_deg": hotspot_turn,
        },
        "grip_axis_tangent_turn_deg": axis_turn,
        "largest_relative_convergence_family": max(relative_derivatives, key=relative_derivatives.get),
        "relative_convergence_derivative_per_u": relative_derivatives,
    }


def classify(rows: list[dict[str, Any]], contract: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    near = [row for row in rows if row["u"] >= float(contract["routing_heuristics"]["near_pole_u_min"])]
    theta_min = float(contract["routing_heuristics"]["opposite_lower_quadrant_theta_min"])
    theta_max = float(contract["routing_heuristics"]["opposite_lower_quadrant_theta_max"])
    hotspot_in_opposite_lower = all(theta_min <= row["hotspot"]["theta_rad"] <= theta_max for row in near)
    opposite_is_fastest_relative_convergence = all(
        row["largest_relative_convergence_family"] == "OPPOSITE_SIDE_PLAN" for row in near
    )
    opposite_lower_sector_dominates = all(
        max(row["sector_normal_turn_deg"]["OPPOSITE"], row["sector_normal_turn_deg"]["LOWER"])
        > max(row["sector_normal_turn_deg"]["TOP"], row["sector_normal_turn_deg"]["THUMB"])
        for row in near
    )
    surface_turn_dominates_axis = all(
        row["hotspot"]["normal_turn_deg"] > row["grip_axis_tangent_turn_deg"] for row in near
    )
    evidence = {
        "near_pole_hotspots_in_opposite_lower_quadrant": hotspot_in_opposite_lower,
        "opposite_side_has_fastest_relative_convergence_to_palm": opposite_is_fastest_relative_convergence,
        "opposite_or_lower_sector_turn_dominates_top_thumb": opposite_lower_sector_dominates,
        "surface_hotspot_turn_exceeds_grip_axis_tangent_turn": surface_turn_dominates_axis,
    }
    if all(evidence.values()):
        return "OPPOSITE_LOWER_PROFILE_CONVERGENCE_RELATION_SUSPECTED", evidence
    if hotspot_in_opposite_lower and surface_turn_dominates_axis:
        return "GLOBAL_PROFILE_CONVERGENCE_RELATION_SUSPECTED", evidence
    if not surface_turn_dominates_axis:
        return "GRIP_AXIS_TERMINATION_TANGENT_SUSPECTED", evidence
    return "INCONCLUSIVE_REVISE", evidence


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", required=True)
    p.add_argument("--r2-correction", required=True)
    p.add_argument("--confirmed-interface", required=True)
    p.add_argument("--contract", required=True)
    p.add_argument("--out", required=True)
    a = p.parse_args()

    seed = load(a.source)
    r2_fix = load(a.r2_correction)
    confirmed = load(a.confirmed_interface)
    contract = load(a.contract)
    base_source = r2.apply(seed, r2_fix)
    source = apply_confirmed_interface(base_source, confirmed)
    before_digest = source_digest(source)

    if contract["policy"]["source_edit_forbidden"] is not True:
        raise RuntimeError("R4.2 must remain diagnostic-only")
    exponent = float(base.own(source, "LOWER_RETURN_PROFILE").get("termination_envelope_exponent", 0.55))
    if abs(exponent - 0.34) > 1e-12:
        raise RuntimeError(f"R4.2 requires baseline termination exponent 0.34, got {exponent}")

    rows = [probe_row(source, contract, float(u)) for u in contract["sample_u"]]
    classification, evidence = classify(rows, contract)
    after_digest = source_digest(source)

    pre_cap = max(row["hotspot"]["normal_turn_deg"] for row in rows if row["u"] <= 0.98)
    near_pole = max(row["hotspot"]["normal_turn_deg"] for row in rows if row["u"] >= 0.995)
    max_axis = max(row["grip_axis_tangent_turn_deg"] for row in rows if row["u"] >= 0.995)
    max_opposite_relative_derivative = max(
        row["relative_convergence_derivative_per_u"]["OPPOSITE_SIDE_PLAN"] for row in rows if row["u"] >= 0.995
    )
    checks = {
        "source_digest_unchanged": before_digest == after_digest,
        "termination_exponent_unchanged_at_0_34": abs(exponent - 0.34) <= 1e-12,
        "confirmed_interface_locked": base.own(source, "INTERFACE_DECK_BOUNDARY")["theta_center"] == "TOP_MERIDIAN"
        and abs(float(base.own(source, "INTERFACE_DECK_BOUNDARY")["u_halfspan"]) - 0.26) <= 1e-12
        and abs(float(base.own(source, "INTERFACE_DECK_BOUNDARY")["theta_halfspan_rad"]) - 1.06) <= 1e-12
        and abs(float(base.own(source, "INTERFACE_DECK_BOUNDARY")["core_fraction"]) - 0.29) <= 1e-12,
        "near_pole_turn_exceeds_pre_cap": near_pole > pre_cap,
        "probe_is_topology_independent": contract["policy"]["mesh_generation_not_required"] is True,
        "candidate_promotion_not_run": contract["policy"]["candidate_promotion"] == "NOT_RUN",
    }
    status = "R4_2_PROFILE_CONVERGENCE_OWNERSHIP_CLASSIFIED" if all(checks.values()) and classification != "INCONCLUSIVE_REVISE" else "R4_2_PROFILE_CONVERGENCE_REVISE"
    report = {
        "schema": "oleander.modeling-worker.v0.13.g1.r4.2.termination-profile-convergence-report.v1",
        "status": status,
        "job_state": "R4_2_TOPOLOGY_INDEPENDENT_PROFILE_CONVERGENCE_PROBE_EXECUTED",
        "design_state": "REVISE",
        "authority_state": "WORKING_SOURCE",
        "candidate_review": "REOPENED",
        "candidate_promotion": "NOT_RUN",
        "source_digest": before_digest,
        "termination_envelope_exponent": exponent,
        "checks": checks,
        "classification": classification,
        "classification_evidence": evidence,
        "summary_metrics": {
            "pre_cap_max_surface_normal_turn_deg_u_le_0_98": pre_cap,
            "near_pole_max_surface_normal_turn_deg_u_ge_0_995": near_pole,
            "near_pole_max_grip_axis_tangent_turn_deg": max_axis,
            "near_pole_max_opposite_relative_convergence_derivative_per_u": max_opposite_relative_derivative,
        },
        "rows": rows,
        "next_legal_action": "Use the classified profile-convergence ownership to define a bounded Source-level relation experiment. Do not alter unrelated Source families or the confirmed interface relation.",
        "boundary": contract["boundary"],
    }
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "G1_R4_2_TERMINATION_PROFILE_CONVERGENCE_REPORT.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if status.endswith("CLASSIFIED") else 5


if __name__ == "__main__":
    raise SystemExit(main())
