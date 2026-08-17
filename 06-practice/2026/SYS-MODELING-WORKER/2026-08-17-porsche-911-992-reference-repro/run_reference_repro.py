#!/usr/bin/env python3
"""Blender argv/runtime bridge for the Porsche 911 reference-reproduction benchmark."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import bpy

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

# Focused runtime repair 1: explicit material/side binding for wheel construction.
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

# Focused runtime repair 2: Blender 5.2 exposes EEVEE as BLENDER_EEVEE.
def setup_render_fixed(path, samples, rx, ry):
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x = rx
    sc.render.resolution_y = ry
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    sc.render.image_settings.color_mode = "RGBA"
    sc.render.filepath = str(path)
    sc.render.film_transparent = False
    try:
        sc.view_settings.look = "AgX - Medium High Contrast"
    except Exception:
        pass
    sc["OLEANDER_REQUESTED_SAMPLES"] = samples

mod.build_wheels = build_wheels_fixed
mod.setup_render = setup_render_fixed
mod.main()
