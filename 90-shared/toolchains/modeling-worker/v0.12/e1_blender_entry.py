#!/usr/bin/env python3
"""Blender execution adapter for Modeling Worker v0.12 E1.

Blender keeps its own CLI arguments in sys.argv. This adapter extracts only the
arguments after `--`, then invokes the benchmark with a clean Python argv. It also
normalizes the Blender 5.2 EEVEE engine enum used by this runtime.

These are execution-plumbing compatibility fixes only; no geometry, design relationship
or Surface Fairness threshold is modified.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import bpy


def main() -> None:
    if "--" not in sys.argv:
        raise SystemExit("E1 requires Blender script arguments after --")
    user_argv = sys.argv[sys.argv.index("--") + 1:]
    target = Path(__file__).with_name("e1_freeform_bicubic.py")
    spec = importlib.util.spec_from_file_location("oleander_e1_freeform", target)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)

    def setup_scene_blender52(res: int = 640):
        sc = bpy.context.scene
        sc.render.engine = "BLENDER_EEVEE"
        sc.render.resolution_x = res
        sc.render.resolution_y = res
        sc.render.resolution_percentage = 100
        sc.render.image_settings.file_format = "PNG"
        sc.render.film_transparent = False
        sc.world.color = (0.025, 0.025, 0.025)
        module.add_area("KEY", (2.5, 3.5, 4.5), 1300, 4.0)
        module.add_area("FILL", (-2.5, -3.0, 2.8), 900, 3.5)
        module.add_area("STRIP", (0.0, 4.8, 1.8), 1100, 1.0)
        return sc

    module.setup_scene = setup_scene_blender52
    sys.argv = [str(target), *user_argv]
    module.main()


if __name__ == "__main__":
    main()
