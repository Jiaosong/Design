#!/usr/bin/env python3
"""Blender argv adapter for Modeling Worker v0.12 E1.

Blender keeps its own CLI arguments in sys.argv. This adapter extracts only the
arguments after `--`, then invokes the benchmark with a clean Python argv. It changes
execution plumbing only; no geometry, relationship or fairness threshold is modified.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def main() -> None:
    if "--" not in sys.argv:
        raise SystemExit("E1 requires Blender script arguments after --")
    user_argv = sys.argv[sys.argv.index("--") + 1:]
    target = Path(__file__).with_name("e1_freeform_bicubic.py")
    spec = importlib.util.spec_from_file_location("oleander_e1_freeform", target)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    sys.argv = [str(target), *user_argv]
    module.main()


if __name__ == "__main__":
    main()
