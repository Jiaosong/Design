#!/usr/bin/env python3
"""Blender argv bridge for the Porsche 911 reference-reproduction benchmark."""
from __future__ import annotations

import runpy
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "build_porsche_911_992_reference.py"

if "--" not in sys.argv:
    raise SystemExit("Blender argv bridge requires '--' before benchmark arguments")

idx = sys.argv.index("--")
benchmark_args = sys.argv[idx + 1 :]
sys.argv = [str(TARGET), *benchmark_args]
runpy.run_path(str(TARGET), run_name="__main__")
