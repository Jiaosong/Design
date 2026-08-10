"""Capture real Rhino viewport and Grasshopper canvas evidence.

Run inside Rhino through rhinocode after Grasshopper is open and a document is active.
The output is real GUI/runtime evidence; it does not by itself prove the design result is correct.
"""

import json
import os
import traceback
from datetime import datetime, timezone

import Rhino
import Grasshopper
from System.Drawing import Size
from System.Drawing.Imaging import ImageFormat


def utc_now():
    return datetime.now(timezone.utc).isoformat()


out_dir = os.environ.get("OLEANDER_RHINO_OUT")
if not out_dir:
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.path.abspath(os.path.join(here, "..", "runtime-state"))
os.makedirs(out_dir, exist_ok=True)

receipt = {
    "timestamp": utc_now(),
    "status": "CAPTURE STARTED",
    "outputs": {},
    "errors": [],
    "evidence_boundary": [
        "Captured images prove that the corresponding Rhino/Grasshopper UI state was rendered.",
        "They do not automatically prove geometry, engineering performance, or project approval."
    ]
}

try:
    doc = Rhino.RhinoDoc.ActiveDoc
    if doc is None or doc.Views.ActiveView is None:
        raise RuntimeError("No active Rhino document/view available")

    view = doc.Views.ActiveView
    viewport_path = os.path.join(out_dir, "rhino_viewport.png")
    viewport_bitmap = view.CaptureToBitmap(Size(1600, 1000), True, True, True)
    if viewport_bitmap is None:
        raise RuntimeError("Rhino viewport CaptureToBitmap returned None")
    viewport_bitmap.Save(viewport_path, ImageFormat.Png)
    viewport_bitmap.Dispose()
    receipt["outputs"]["rhino_viewport_png"] = viewport_path

except Exception as exc:
    receipt["errors"].append({
        "stage": "rhino_viewport",
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc()
    })

try:
    canvas = Grasshopper.Instances.ActiveCanvas
    if canvas is None:
        raise RuntimeError("No active Grasshopper canvas available")

    canvas_path = os.path.join(out_dir, "grasshopper_canvas.png")
    canvas_bitmap = canvas.CreatePreview(Size(1800, 1200))
    if canvas_bitmap is None:
        raise RuntimeError("Grasshopper canvas CreatePreview returned None")
    canvas_bitmap.Save(canvas_path, ImageFormat.Png)
    canvas_bitmap.Dispose()
    receipt["outputs"]["grasshopper_canvas_png"] = canvas_path

except Exception as exc:
    receipt["errors"].append({
        "stage": "grasshopper_canvas",
        "type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc()
    })

if len(receipt["outputs"]) == 2 and not receipt["errors"]:
    receipt["status"] = "CANVAS CAPTURED / VIEWPORT CAPTURED"
elif receipt["outputs"]:
    receipt["status"] = "PARTIAL CAPTURE / HOLD"
else:
    receipt["status"] = "CAPTURE FAIL"

receipt_path = os.path.join(out_dir, "capture_receipt.json")
with open(receipt_path, "w", encoding="utf-8") as f:
    json.dump(receipt, f, ensure_ascii=False, indent=2)

print("OLEANDER_CAPTURE_RECEIPT=" + receipt_path)
print("OLEANDER_CAPTURE_STATUS=" + receipt["status"])
