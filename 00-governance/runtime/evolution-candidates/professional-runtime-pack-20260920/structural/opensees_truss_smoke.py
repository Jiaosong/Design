#!/usr/bin/env python3
from __future__ import annotations

import json
import math

import openseespy.opensees as ops

L = 3.0
A = 0.01
E = 200e9
P = 100_000.0

ops.wipe()
ops.model("basic", "-ndm", 2, "-ndf", 2)
ops.node(1, 0.0, 0.0)
ops.node(2, L, 0.0)
ops.fix(1, 1, 1)
ops.fix(2, 0, 1)
ops.uniaxialMaterial("Elastic", 1, E)
ops.element("truss", 1, 1, 2, A, 1)
ops.timeSeries("Linear", 1)
ops.pattern("Plain", 1, 1)
ops.load(2, P, 0.0)
ops.system("BandSPD")
ops.numberer("RCM")
ops.constraints("Plain")
ops.integrator("LoadControl", 1.0)
ops.algorithm("Linear")
ops.analysis("Static")
code = ops.analyze(1)
if code != 0:
    raise SystemExit(f"analysis failed with code {code}")

actual = float(ops.nodeDisp(2, 1))
expected = P * L / (A * E)
if not math.isclose(actual, expected, rel_tol=1e-8, abs_tol=1e-12):
    raise SystemExit(f"displacement mismatch: actual={actual} expected={expected}")

print(json.dumps({
    "runtime": "OpenSeesPy",
    "model": "2D elastic axial truss",
    "L_m": L,
    "A_m2": A,
    "E_Pa": E,
    "P_N": P,
    "actual_displacement_m": actual,
    "closed_form_displacement_m": expected,
    "result": "PASS_RUNTIME_SMOKE",
    "does_not_prove": [
        "project structural model validity",
        "load basis correctness",
        "code compliance",
        "engineering approval",
        "field truth"
    ]
}, indent=2))
