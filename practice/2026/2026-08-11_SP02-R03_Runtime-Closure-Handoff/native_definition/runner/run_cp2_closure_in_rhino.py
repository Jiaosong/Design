# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import traceback

DLL = os.environ.get("SP02_RUNTIME_DLL")
EVIDENCE = os.environ.get("SP02_EVIDENCE_DIR")
PROVIDER = os.environ.get("SP02_PROVIDER_ID", "P01_GUI_WINDOWS_DESKTOP")
EXIT_AFTER = os.environ.get("SP02_EXIT_AFTER_CP2", "1") == "1"

if not DLL or not os.path.isfile(DLL):
    raise RuntimeError("SP02_RUNTIME_DLL must point to compiled Sp02NativeDefinitionBuilder.dll")
if not EVIDENCE:
    raise RuntimeError("SP02_EVIDENCE_DIR is required")

try:
    loaded = False
    try:
        from System.Reflection import Assembly
        Assembly.LoadFrom(os.path.abspath(DLL))
        loaded = True
    except Exception:
        pass

    if not loaded:
        try:
            import clr
            clr.AddReferenceToFileAndPath(os.path.abspath(DLL))
            loaded = True
        except Exception:
            pass

    if not loaded:
        raise RuntimeError("Could not load SP02 runtime closure assembly inside Rhino")

    from Oleander.Sp02 import Sp02RuntimeClosure
    summary = Sp02RuntimeClosure.Run(os.path.abspath(EVIDENCE), PROVIDER)
    print("SP02 CP2 one-run summary: " + str(summary))

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
