#!/usr/bin/env python3
"""Deterministic M8 gate fix: restore wheel radius from canonical 0.700 m HP OD.

No Source, M7 secondary, prototype or instance design parameter changes.
"""
from __future__ import annotations
import importlib.util

spec=importlib.util.spec_from_file_location('m8','/tmp/revise_v011_r29a_m8.py')
m8=importlib.util.module_from_spec(spec);spec.loader.exec_module(m8)
m8.WHEEL_RADIUS=m8.TARGET_OD*.5

if __name__=='__main__':
    m8.main()
