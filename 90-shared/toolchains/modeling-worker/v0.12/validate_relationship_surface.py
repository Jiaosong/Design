#!/usr/bin/env python3
"""OLEANDER Modeling Worker v0.12 contract + sampled-curve fairness validator.

Stdlib-only by design. This is a fail-closed orchestration primitive, not a Class-A
surface evaluator. It verifies that design relationships exist before topology and that
sampled geometric evidence is quantitatively checked instead of being inferred from
smooth shading.
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

SCHEMA = "oleander.modeling-worker.v0.12.relationship-surface-contract"
RELATIONS = {"ALIGN", "TANGENCY", "CURVATURE", "OFFSET", "PROPORTION", "TENSION", "FLOW", "BOUNDARY", "DEPENDENCY"}
CONTINUITY = {"G0", "G1", "G2", "G3", "N/A"}
METRICS = {"G0", "G1", "G2", "TANGENT_JUMP", "CURVATURE_COMB", "CURVATURE_RATE", "INFLECTION_COUNT", "SPACING_REGULARITY", "ZEBRA", "REFLECTION_FLOW", "SILHOUETTE_DERIVATIVE", "TERMINATION_INFLUENCE"}


def _norm(v: tuple[float, float, float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def _sub(a: Iterable[float], b: Iterable[float]) -> tuple[float, float, float]:
    aa, bb = tuple(a), tuple(b)
    return (aa[0] - bb[0], aa[1] - bb[1], aa[2] - bb[2])


def _dot(a: Iterable[float], b: Iterable[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def _cross(a: Iterable[float], b: Iterable[float]) -> tuple[float, float, float]:
    ax, ay, az = a; bx, by, bz = b
    return (ay * bz - az * by, az * bx - ax * bz, ax * by - ay * bx)


def _angle_deg(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    na, nb = _norm(a), _norm(b)
    if na <= 1e-12 or nb <= 1e-12:
        return 180.0
    c = max(-1.0, min(1.0, _dot(a, b) / (na * nb)))
    return math.degrees(math.acos(c))


def curve_metrics(points: list[list[float]]) -> dict[str, float | int]:
    """Compute conservative polyline proxies for fairness diagnostics.

    These values do not prove G2/Class-A quality. They are intended to catch obvious
    tangent jumps, irregular sampling and curvature-rate spikes before human review.
    """
    if len(points) < 5 or any(len(p) != 3 for p in points):
        raise ValueError("curve sample evidence requires >=5 three-dimensional points")
    seg = [_sub(points[i + 1], points[i]) for i in range(len(points) - 1)]
    lengths = [_norm(v) for v in seg]
    mean_len = sum(lengths) / len(lengths)
    if mean_len <= 1e-12:
        raise ValueError("degenerate sampled curve")
    variance = sum((x - mean_len) ** 2 for x in lengths) / len(lengths)
    spacing_cv = math.sqrt(variance) / mean_len
    tangent_jumps = [_angle_deg(seg[i], seg[i + 1]) for i in range(len(seg) - 1)]

    # Discrete curvature proxy: turning angle divided by mean adjacent arc length.
    curvature: list[float] = []
    signed_turn: list[float] = []
    reference_normal: tuple[float, float, float] | None = None
    for i in range(len(seg) - 1):
        denom = max(1e-12, 0.5 * (lengths[i] + lengths[i + 1]))
        angle_rad = math.radians(tangent_jumps[i])
        curvature.append(angle_rad / denom)
        cr = _cross(seg[i], seg[i + 1])
        if _norm(cr) > 1e-10 and reference_normal is None:
            reference_normal = cr
        signed_turn.append(_dot(cr, reference_normal) if reference_normal is not None else 0.0)

    curvature_rate = []
    for i in range(len(curvature) - 1):
        ds = max(1e-12, 0.5 * (lengths[i + 1] + lengths[i + 2]))
        curvature_rate.append(abs(curvature[i + 1] - curvature[i]) / ds)

    signs = [1 if x > 1e-12 else -1 if x < -1e-12 else 0 for x in signed_turn]
    nz = [s for s in signs if s]
    inflections = sum(1 for a, b in zip(nz, nz[1:]) if a != b)
    return {
        "sample_count": len(points),
        "max_tangent_jump_deg": max(tangent_jumps, default=0.0),
        "mean_tangent_jump_deg": sum(tangent_jumps) / max(1, len(tangent_jumps)),
        "spacing_cv": spacing_cv,
        "max_curvature_rate": max(curvature_rate, default=0.0),
        "inflection_count": inflections,
    }


def validate_contract(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = ["schema", "job_id", "decision_question", "authority", "hard_points", "volume_skeleton", "relationship_graph", "primary_curves", "control_cage", "surface_fairness", "execution_geometry", "gate_state"]
    for key in required:
        if key not in data:
            errors.append(f"missing required field: {key}")
    if errors:
        return errors
    if data["schema"] != SCHEMA:
        errors.append(f"schema must be {SCHEMA}")
    if len(str(data["decision_question"]).strip()) < 12:
        errors.append("decision_question is too short")

    graph = data["relationship_graph"]
    node_ids = [x.get("id") for x in graph.get("nodes", [])]
    if len(node_ids) < 2 or len(set(node_ids)) != len(node_ids):
        errors.append("relationship_graph requires >=2 unique node ids")
    for edge in graph.get("edges", []):
        if edge.get("relation") not in RELATIONS:
            errors.append(f"invalid relation: {edge.get('relation')}")
        if edge.get("source") not in node_ids or edge.get("target") not in node_ids:
            errors.append(f"edge {edge.get('id')} references unknown node")
        if not str(edge.get("intended_effect", "")).strip():
            errors.append(f"edge {edge.get('id')} lacks intended_effect")

    curves = data["primary_curves"]
    curve_ids = [x.get("id") for x in curves]
    if len(curve_ids) < 2 or len(set(curve_ids)) != len(curve_ids):
        errors.append("primary_curves requires >=2 unique curve ids")
    for c in curves:
        if c.get("continuity_target") not in CONTINUITY:
            errors.append(f"curve {c.get('id')} has invalid continuity target")
        if not c.get("depends_on"):
            errors.append(f"curve {c.get('id')} must declare dependencies")

    cage = data["control_cage"]
    if cage.get("frequency") != "LOW":
        errors.append("control_cage frequency must be LOW")
    if cage.get("topology_independent") is not True:
        errors.append("control_cage must be topology_independent=true")
    if int(cage.get("max_control_points", 0)) < 4:
        errors.append("control_cage max_control_points must be >=4")

    fairness = data["surface_fairness"]
    required_metrics = fairness.get("required_metrics", [])
    if len(set(required_metrics)) < 3:
        errors.append("surface_fairness requires at least 3 distinct metrics")
    invalid_metrics = set(required_metrics) - METRICS
    if invalid_metrics:
        errors.append(f"invalid fairness metrics: {sorted(invalid_metrics)}")
    if not ({"G1", "G2", "TANGENT_JUMP", "CURVATURE_COMB"} & set(required_metrics)):
        errors.append("surface_fairness must include a continuity/tangent metric")
    if not ({"ZEBRA", "REFLECTION_FLOW", "SILHOUETTE_DERIVATIVE"} & set(required_metrics)):
        errors.append("surface_fairness must include at least one visual-flow metric")

    execution = data["execution_geometry"]
    if execution.get("derived_from_surface_source") is not True:
        errors.append("execution geometry must be derived from surface source")
    if execution.get("smooth_shading_is_evidence") is not False:
        errors.append("smooth shading may not be treated as fairness evidence")

    gates = data["gate_state"]
    if gates.get("M4_5") != "PASS" and gates.get("M5") == "PASS":
        errors.append("M5 cannot PASS while M4.5 Surface Fairness is not PASS")
    if gates.get("M5") != "PASS" and gates.get("M6_plus_blocked") is not True:
        errors.append("M6+ must remain blocked until M5 PASS")

    # If a fairness PASS is claimed, actual evidence must be present and thresholds checked.
    if fairness.get("status") == "PASS" and not fairness.get("evidence"):
        errors.append("surface_fairness PASS requires evidence")
    return errors


def evaluate_fairness(data: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    fairness = data.get("surface_fairness", {})
    thresholds = fairness.get("thresholds", {})
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    sample_evidence = [e for e in fairness.get("evidence", []) if e.get("kind") == "CURVE_SAMPLES"]
    for ev in sample_evidence:
        try:
            metrics = curve_metrics(ev.get("points", []))
        except Exception as exc:
            errors.append(f"evidence {ev.get('id', '<unnamed>')}: {exc}")
            continue
        row = {"id": ev.get("id"), **metrics, "pass": True, "failures": []}
        checks = {
            "max_tangent_jump_deg": lambda v, t: v <= t,
            "spacing_cv": lambda v, t: v <= t,
            "max_curvature_rate": lambda v, t: v <= t,
            "inflection_count": lambda v, t: v <= t,
        }
        for key, fn in checks.items():
            if key in thresholds and not fn(float(metrics[key]), float(thresholds[key])):
                row["pass"] = False
                row["failures"].append(f"{key}={metrics[key]:.6g} exceeds {thresholds[key]}")
        results.append(row)
    if not sample_evidence:
        errors.append("no CURVE_SAMPLES evidence supplied; quantitative fairness remains OPEN")
    return results, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("contract", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()
    data = json.loads(args.contract.read_text(encoding="utf-8"))
    contract_errors = validate_contract(data)
    fairness_results, fairness_errors = evaluate_fairness(data)
    report = {
        "schema": "oleander.modeling-worker.v0.12.validation-report",
        "contract": str(args.contract),
        "contract_valid": not contract_errors,
        "fairness_quantitative_pass": bool(fairness_results) and not fairness_errors and all(r["pass"] for r in fairness_results),
        "contract_errors": contract_errors,
        "fairness_errors": fairness_errors,
        "fairness_results": fairness_results,
        "boundary": "Machine checks are fail-closed proxies. They do not establish Class-A, G2/G3 production surfacing, engineering validity or human design approval."
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        args.report.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if report["contract_valid"] and report["fairness_quantitative_pass"] else 5


if __name__ == "__main__":
    raise SystemExit(main())
