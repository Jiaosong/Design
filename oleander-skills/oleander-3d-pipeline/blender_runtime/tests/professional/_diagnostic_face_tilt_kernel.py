"""Temporary diagnostic: exercise the authoritative face-tilt probe module step by step."""
from __future__ import annotations

import importlib.util
import json
import traceback
from pathlib import Path

import FreeCAD as App
import Part

HERE = Path(__file__).resolve().parent
TARGET = HERE / "probe_freecad_planar_face_tilt.py"
ROOT = Path("/tmp/oleander-face-tilt-mainmodule-diagnostic")
ROOT.mkdir(parents=True, exist_ok=True)


def trace(label, **data):
    print("OLE_TILT_DIAG=" + label + (" " + repr(data) if data else ""), flush=True)


def load_target():
    spec = importlib.util.spec_from_file_location("oleander_face_tilt_target", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load target probe")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    mod = load_target()
    trace("target_imported", path=str(TARGET))

    cases = []
    for width in (80.0, 100.0):
        for angle in (5.0, -5.0):
            trace("before_target_tilt", width=width, angle=angle)
            solid, meta = mod.tilt_top_face(Part.makeBox(width, 50.0, 10.0), angle)
            trace(
                "after_target_tilt",
                width=width,
                angle=angle,
                valid=solid.isValid(),
                solids=len(solid.Solids),
                bbox=[solid.BoundBox.XLength, solid.BoundBox.YLength, solid.BoundBox.ZLength],
                volume=solid.Volume,
                actual_angle=meta["actual_angle_deg"],
            )
            cases.append((width, angle, solid, meta))

    trace("before_failure_gate")
    try:
        mod.tilt_top_face(Part.makeBox(100.0, 50.0, 10.0), 30.0)
        raise AssertionError("30 degree tilt unexpectedly accepted")
    except ValueError as exc:
        trace("failure_gate", error=str(exc))

    doc = App.newDocument("OLE_TILT_TARGET_DIAG")
    pos = mod.add_feature(doc, "OLE_POS_R002", "OLE_DIRECT_FACE_TILT::POS_R002", cases[2][2], 5.0)
    neg = mod.add_feature(doc, "OLE_NEG_R002", "OLE_DIRECT_FACE_TILT::NEG_R002", cases[3][2], -5.0)
    trace("features_added", pos=float(pos.OLE_AngleDeg), neg=float(neg.OLE_AngleDeg))
    doc.recompute()
    fcstd = ROOT / "target_diag.FCStd"
    pos_step = ROOT / "target_pos.step"
    neg_step = ROOT / "target_neg.step"
    trace("before_save")
    doc.saveAs(str(fcstd))
    trace("after_save", exists=fcstd.exists(), size=fcstd.stat().st_size)
    trace("before_pos_step")
    pos.Shape.exportStep(str(pos_step))
    trace("after_pos_step", size=pos_step.stat().st_size)
    trace("before_neg_step")
    neg.Shape.exportStep(str(neg_step))
    trace("after_neg_step", size=neg_step.stat().st_size)
    App.closeDocument(doc.Name)

    trace("before_reopen")
    reopened = App.openDocument(str(fcstd))
    for name, angle in (("OLE_POS_R002", 5.0), ("OLE_NEG_R002", -5.0)):
        obj = reopened.getObject(name)
        trace("reopened_obj", name=name, angle=float(obj.OLE_AngleDeg), valid=obj.Shape.isValid(), solids=len(obj.Shape.Solids))
        assert abs(float(obj.OLE_AngleDeg) - angle) < 1e-6
        assert obj.Shape.isValid() and len(obj.Shape.Solids) == 1
    App.closeDocument(reopened.Name)

    trace("before_tessellate")
    verts, facets = cases[2][2].tessellate(0.25)
    trace("after_tessellate", verts=len(verts), facets=len(facets))
    payload = {
        "bbox": mod.metrics(cases[2][2])["bbox_mm"],
        "volume": cases[2][2].Volume,
        "actual_angle": cases[2][3]["actual_angle_deg"],
        "verts": [[v.x, v.y, v.z] for v in verts],
        "facets": [list(f) for f in facets],
    }
    text = json.dumps(payload, sort_keys=True)
    trace("json_serialized", chars=len(text))
    trace("done")


try:
    main()
except Exception as exc:
    trace("python_exception", error=repr(exc))
    traceback.print_exc()
    raise
