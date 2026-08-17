#!/usr/bin/env python3
"""Blender argv/runtime bridge for the Porsche 911 reference-reproduction benchmark."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "build_porsche_911_992_reference.py"

if "--" not in sys.argv:
    raise SystemExit("Blender argv bridge requires '--' before benchmark arguments")

idx = sys.argv.index("--")
benchmark_args = sys.argv[idx + 1 :]
sys.argv = [str(TARGET), *benchmark_args]

spec = importlib.util.spec_from_file_location("porsche_911_992_reference", TARGET)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

# Focused runtime repair: the original build_wheels helper unpacked `side` into the
# material-table position. Keep the geometry contract untouched and bind arguments explicitly.
def build_wheels_fixed(M):
    all_objs = []
    specs = [
        ("FL", mod.FRONT_AXLE_X, mod.FRONT_TRACK_Y, mod.FRONT_TIRE, mod.FRONT_WHEEL, 1),
        ("FR", mod.FRONT_AXLE_X, -mod.FRONT_TRACK_Y, mod.FRONT_TIRE, mod.FRONT_WHEEL, -1),
        ("RL", mod.REAR_AXLE_X, mod.REAR_TRACK_Y, mod.REAR_TIRE, mod.REAR_WHEEL, 1),
        ("RR", mod.REAR_AXLE_X, -mod.REAR_TRACK_Y, mod.REAR_TIRE, mod.REAR_WHEEL, -1),
    ]
    for code, x, y, tyre_spec, geom, side in specs:
        all_objs.extend(mod.build_wheel(code, x, y, tyre_spec, geom, M, side))
    return all_objs

mod.build_wheels = build_wheels_fixed
mod.main()
