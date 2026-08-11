# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import traceback

DLL = os.environ.get("SP02_BUILDER_DLL")
OUT = os.environ.get("SP02_GHX_OUT")
EXIT_AFTER = os.environ.get("SP02_EXIT_AFTER_BUILD", "1") == "1"

if not DLL or not os.path.isfile(DLL):
    raise RuntimeError("SP02_BUILDER_DLL must point to compiled Sp02NativeDefinitionBuilder.dll")
if not OUT or not OUT.lower().endswith(".ghx"):
    raise RuntimeError("SP02_GHX_OUT must point to target .ghx path")

try:
    loaded = False
    # Rhino 8 CPython/pythonnet path.
    try:
        from System.Reflection import Assembly
        Assembly.LoadFrom(os.path.abspath(DLL))
        loaded = True
    except Exception:
        pass

    # IronPython-compatible fallback where available.
    if not loaded:
        try:
            import clr
            clr.AddReferenceToFileAndPath(os.path.abspath(DLL))
            loaded = True
        except Exception:
            pass

    if not loaded:
        raise RuntimeError("Could not load builder assembly inside Rhino process")

    from Oleander.Sp02 import Sp02NativeDefinitionBuilder
    receipt = Sp02NativeDefinitionBuilder.Build(os.path.abspath(OUT))
    print("SP02 SG01 definition receipt: " + str(receipt))

except Exception:
    traceback.print_exc()
    raise

finally:
    if EXIT_AFTER:
        try:
            import Rhino
            Rhino.RhinoApp.Exit(False)
        except Exception:
            pass
