"""OLEANDER Rhino + Grasshopper runtime probe.

Run INSIDE a live Rhino 8.11+ instance through:
    rhinocode script <full-path-to-this-file>

This script writes a runtime manifest. It does not claim a Grasshopper
training definition has been solved.
"""

import json
import os
import traceback
from datetime import datetime, timezone

import Rhino


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def safe_get(obj, name, default=None):
    try:
        return getattr(obj, name)
    except Exception:
        return default


out_dir = os.environ.get("OLEANDER_RHINO_OUT")
if not out_dir:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(here, "..", "runtime-state"))
os.makedirs(out_dir, exist_ok=True)

manifest = {
    "timestamp": utc_now(),
    "status": "PROBE STARTED",
    "rhino": {},
    "grasshopper": {},
    "required_components": {},
    "errors": [],
    "evidence_boundary": [
        "A runtime probe is not a Grasshopper definition test.",
        "CP2 and CP4 remain OPEN until a real definition is solved and real evidence is captured."
    ]
}

try:
    doc = Rhino.RhinoDoc.ActiveDoc
    manifest["rhino"] = {
        "exe_version": safe_get(Rhino.RhinoApp, "ExeVersion"),
        "version": str(safe_get(Rhino.RhinoApp, "Version", "UNKNOWN")),
        "active_document": safe_get(doc, "Name", None) if doc else None,
        "active_view": safe_get(safe_get(doc, "Views", None), "ActiveView", None).ActiveViewport.Name if doc and doc.Views.ActiveView else None,
        "script_context": "rhinocode / live Rhino"
    }

    # Load/show Grasshopper through the real Rhino command system.
    Rhino.RhinoApp.RunScript("_Grasshopper", False)

    import Grasshopper

    server = Grasshopper.Instances.ComponentServer
    proxies = list(server.ObjectProxies)

    names = []
    for p in proxies:
        try:
            n = p.Desc.Name
            if n:
                names.append(str(n))
        except Exception:
            pass

    required_terms = [
        "Param Viewer",
        "Path Mapper",
        "Graft",
        "Flatten"
    ]
    for term in required_terms:
        hits = sorted({n for n in names if term.lower() in n.lower()})
        manifest["required_components"][term] = hits[:20]

    canvas = Grasshopper.Instances.ActiveCanvas
    active_doc = Grasshopper.Instances.ActiveDocument

    manifest["grasshopper"] = {
        "sdk_loaded": True,
        "component_proxy_count": len(proxies),
        "active_canvas_available": canvas is not None,
        "active_document_available": active_doc is not None,
        "running_headless": bool(Grasshopper.Instances.RunningHeadless),
    }
    manifest["status"] = "RHINO RUNTIME PASS / GRASSHOPPER SDK PASS"

except Exception as exc:
    manifest["status"] = "PROBE FAIL"
    manifest["errors"].append({
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc()
    })

manifest_path = os.path.join(out_dir, "runtime_probe_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2, default=str)

print("OLEANDER_RUNTIME_MANIFEST=" + manifest_path)
print("OLEANDER_RUNTIME_STATUS=" + manifest["status"])
