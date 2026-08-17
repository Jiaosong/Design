#!/usr/bin/env python3
"""Blender argv/runtime bridge for the Porsche 911 reference-reproduction benchmark."""
from __future__ import annotations

import importlib.util
import json
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

# Focused runtime repair 2: use the already-proven headless Cycles CPU path.
def setup_render_fixed(path, samples, rx, ry):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = False
    sc.cycles.max_bounces = 4
    sc.cycles.diffuse_bounces = 2
    sc.cycles.glossy_bounces = 2
    sc.cycles.transmission_bounces = 3
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

# Preserve the build script's fail-closed exit while correcting runtime provenance in the emitted QA.
out_dir = None
if "--out" in benchmark_args:
    out_dir = Path(benchmark_args[benchmark_args.index("--out") + 1])

try:
    mod.main()
except SystemExit as exc:
    if exc.code == 0 and out_dir is not None:
        qa_path = out_dir / "REFERENCE_REPRO_QA.json"
        if qa_path.exists():
            qa = json.loads(qa_path.read_text())
            qa["render_engine"] = "CYCLES_CPU"
            qa["runtime_bridge_fixes"] = ["ARGV_ROUTING", "WHEEL_ARGUMENT_BINDING", "HEADLESS_CYCLES_CPU"]
            qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n")
    raise
