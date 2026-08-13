#!/usr/bin/env python3
"""Technical execution wrapper for R24.
Keeps R24 design geometry unchanged; flips only the 28 appended termination faces to retain R20 winding orientation.
"""
from __future__ import annotations
import importlib.util,bpy

BASE='/tmp/revise_v011_r24.py'
spec=importlib.util.spec_from_file_location('r24',BASE)
r24=importlib.util.module_from_spec(spec);spec.loader.exec_module(r24)

_orig=r24.build_source

def _fixed_build_source(rows,M,glass):
    source,xs,cols,arch_meta,reuse=_orig(rows,M,glass)
    verts=[tuple(v.co) for v in source.data.vertices]
    faces=[tuple(p.vertices) for p in source.data.polygons]
    mats=[p.material_index for p in source.data.polygons]
    assert len(faces)>=28
    for i in range(len(faces)-28,len(faces)):
        faces[i]=tuple(reversed(faces[i]))
    me=bpy.data.meshes.new('PRIMARY_LOCAL_ARCH_SOURCE_MESH_R20_WINDING')
    me.from_pydata(verts,[],faces);me.update()
    o=bpy.data.objects.new('PRIMARY_LOCAL_ARCH_SOURCE',me);bpy.context.collection.objects.link(o)
    o.data.materials.append(M['CLAY']);o.data.materials.append(glass)
    for p,mi in zip(o.data.polygons,mats):
        p.use_smooth=True;p.material_index=mi
    o['OLEANDER_AUTHORITY']='WORKING_SOURCE';o['OLEANDER_TOPOLOGY']='R24_SHARED_ENDPOINT_LOCAL_ARCH_R20_WINDING'
    bpy.data.objects.remove(source,do_unlink=True)
    return o,xs,cols,arch_meta,reuse

r24.build_source=_fixed_build_source
r24.main()
