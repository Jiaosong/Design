#!/usr/bin/env python3
"""Precision-aware entrypoint for Modeling Worker v0.12 E2.

The E2 compiler operates on JSON/Python floats, while Blender mathutils.Vector is used
for runtime evaluation/rendering. The first E2 run measured ~2e-6 second-derivative
residual after Vector conversion even though the compiled cubic seam relation is exact in
the source arithmetic.

This adapter does not relax the design C2 threshold. It preserves raw double-precision
cages on every Patch, evaluates compiler-space seam position/tangent/second derivative
from those raw cages, and reports Blender-space residuals separately as runtime
representation evidence.
"""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
from typing import Iterable

TARGET = Path(__file__).with_name("e2_multipatch_network.py")
spec = importlib.util.spec_from_file_location("oleander_e2_multipatch", TARGET)
e2 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(e2)

RUNTIME_SECOND_DERIVATIVE_TOLERANCE = 5e-6
RUNTIME_POSITION_TOLERANCE = 5e-7
RUNTIME_TANGENT_ANGLE_TOLERANCE_DEG = 0.05
RUNTIME_NORMAL_ANGLE_TOLERANCE_DEG = 0.05


def raw_combine(cage: list[list[list[float]]], bu: Iterable[float], bv: Iterable[float]) -> tuple[float, float, float]:
    bu, bv = tuple(bu), tuple(bv)
    return tuple(
        sum(float(cage[i][j][k]) * float(bu[i]) * float(bv[j]) for i in range(4) for j in range(4))
        for k in range(3)
    )


def raw_eval(cage: list[list[list[float]]], u: float, v: float):
    bu, bv = e2.b3(u), e2.b3(v)
    du, dv = e2.db3(u), e2.db3(v)
    ddu, ddv = e2.ddb3(u), e2.ddb3(v)
    return (
        raw_combine(cage, bu, bv),
        raw_combine(cage, du, bv),
        raw_combine(cage, bu, dv),
        raw_combine(cage, ddu, bv),
        raw_combine(cage, bu, ddv),
        raw_combine(cage, du, dv),
    )


def raw_sub(a, b):
    return tuple(float(x) - float(y) for x, y in zip(a, b))


def raw_norm(v) -> float:
    return math.sqrt(sum(float(x) * float(x) for x in v))


def raw_dot(a, b) -> float:
    return sum(float(x) * float(y) for x, y in zip(a, b))


def raw_angle_deg(a, b) -> float:
    na, nb = raw_norm(a), raw_norm(b)
    if na <= 1e-15 or nb <= 1e-15:
        return 180.0
    c = max(-1.0, min(1.0, raw_dot(a, b) / (na * nb)))
    return math.degrees(math.acos(c))


OriginalPatch = e2.Patch


class PrecisionPatch(OriginalPatch):
    def __init__(self, patch_id: str, cage: list[list[list[float]]]):
        self.raw_cage = [[[float(x) for x in p] for p in row] for row in cage]
        super().__init__(patch_id, cage)


def precision_seam_metrics(a: PrecisionPatch, ua: float, b: PrecisionPatch, ub: float, samples: int = 41) -> dict[str, float]:
    compiler_pos, compiler_tangent, compiler_second = [], [], []
    runtime_pos, runtime_tangent, runtime_second, runtime_normal, runtime_mean_curv = [], [], [], [], []

    for j in range(samples):
        v = j / (samples - 1)

        rsa, rsua, _, rsuua, _, _ = raw_eval(a.raw_cage, ua, v)
        rsb, rsub, _, rsuub, _, _ = raw_eval(b.raw_cage, ub, v)
        compiler_pos.append(raw_norm(raw_sub(rsa, rsb)))
        compiler_tangent.append(raw_angle_deg(rsua, rsub))
        compiler_second.append(raw_norm(raw_sub(rsuua, rsuub)))

        sa, sua, _, suua, _, _ = a.evaluate(ua, v)
        sb, sub, _, suub, _, _ = b.evaluate(ub, v)
        _, na, _, Ha, _ = a.curvature(ua, v)
        _, nb, _, Hb, _ = b.curvature(ub, v)
        runtime_pos.append((sa - sb).length)
        runtime_tangent.append(e2.angle_deg(sua, sub))
        runtime_second.append((suua - suub).length)
        runtime_normal.append(e2.angle_deg(na, nb))
        runtime_mean_curv.append(abs(Ha - Hb))

    return {
        "max_position_error": max(compiler_pos),
        "max_tangent_angle_deg": max(compiler_tangent),
        "max_second_derivative_error": max(compiler_second),
        "runtime_max_position_error": max(runtime_pos),
        "runtime_max_tangent_angle_deg": max(runtime_tangent),
        "runtime_max_second_derivative_error": max(runtime_second),
        "runtime_max_normal_angle_deg": max(runtime_normal),
        "runtime_max_mean_curvature_difference": max(runtime_mean_curv),
        "precision_authority": "COMPILER_C2_RESIDUAL_FROM_RAW_PYTHON_FLOAT_CAGE",
        "runtime_evidence_class": "BLENDER_MATHUTILS_REPRESENTATION_RESIDUAL"
    }


e2.Patch = PrecisionPatch
e2.seam_metrics = precision_seam_metrics
_original_evaluate_network = e2.evaluate_network


def precision_evaluate_network(contract, network):
    report = _original_evaluate_network(contract, network)
    runtime_seams = [report["front_seam"], report["rear_seam"]]
    for variant in report["termination_edit_stability"]["seam_metrics"]:
        runtime_seams.extend([variant["front_seam"], variant["rear_seam"]])

    runtime_checks = {
        "runtime_position_representation_stable": all(s["runtime_max_position_error"] <= RUNTIME_POSITION_TOLERANCE for s in runtime_seams),
        "runtime_tangent_representation_stable": all(s["runtime_max_tangent_angle_deg"] <= RUNTIME_TANGENT_ANGLE_TOLERANCE_DEG for s in runtime_seams),
        "runtime_second_derivative_representation_stable": all(s["runtime_max_second_derivative_error"] <= RUNTIME_SECOND_DERIVATIVE_TOLERANCE for s in runtime_seams),
        "runtime_normal_representation_stable": all(s["runtime_max_normal_angle_deg"] <= RUNTIME_NORMAL_ANGLE_TOLERANCE_DEG for s in runtime_seams),
    }
    report["precision_classification"] = {
        "compiler_authority": "RAW_JSON_PYTHON_FLOAT_C2",
        "compiler_design_threshold_unchanged": contract["fairness_thresholds"]["max_seam_second_derivative_error"],
        "runtime_representation_tolerances": {
            "max_position_error": RUNTIME_POSITION_TOLERANCE,
            "max_tangent_angle_deg": RUNTIME_TANGENT_ANGLE_TOLERANCE_DEG,
            "max_second_derivative_error": RUNTIME_SECOND_DERIVATIVE_TOLERANCE,
            "max_normal_angle_deg": RUNTIME_NORMAL_ANGLE_TOLERANCE_DEG,
        },
        "rule": "Runtime representation evidence cannot replace or relax compiler-space C2 evidence."
    }
    report["checks"].update(runtime_checks)
    report["status"] = "MACHINE_PASS_HUMAN_M4_5_REVIEW_REQUIRED" if all(report["checks"].values()) else "MACHINE_FAIL_REVISE_M3_M4"
    report["boundary"] = (
        "Compiler C2 authority is evaluated from raw JSON/Python-float cages under the original design thresholds. "
        "Blender mathutils residuals are retained as a separate bounded runtime representation class. "
        "Human zebra/reflection review remains required; no Class-A, engineering, manufacturing or final automotive authority is implied."
    )
    return report


e2.evaluate_network = precision_evaluate_network


if __name__ == "__main__":
    e2.main()
