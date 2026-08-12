#!/usr/bin/env python3
"""Deterministic technical wrapper for R29.
Inject Blender's bpy module into revise_v011_r29.py, which omitted the import.
No R29 design variable, topology, source coordinate, QA criterion, or wheel package changes.
"""
import importlib.util
import bpy

BASE='/tmp/revise_v011_r29.py'
spec=importlib.util.spec_from_file_location('r29',BASE)
r29=importlib.util.module_from_spec(spec)
spec.loader.exec_module(r29)
r29.bpy=bpy

if __name__=='__main__':
    r29.main()
