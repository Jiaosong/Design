#!/usr/bin/env python3
import hashlib
import json
import math
import os
from pathlib import Path

import FreeCAD as App
import Part
import PartDesign  # registers PartDesign feature types

DOC_NAME = "OLEANDER_FREECAD_PARAMETRIC_BENCH"
PARAM_NAME = "Parameters"
BODY_NAME = "Body"
BASE_NAME = "Base"
HOLE_NAME = "Hole"


def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def qmm(v):
    try:
        return float(v.getValueAs("mm"))
    except Exception:
        return float(v.Value)


def bbox(shape):
    b = shape.BoundBox
    return {
        "min": [float(b.XMin), float(b.YMin), float(b.ZMin)],
        "max": [float(b.XMax), float(b.YMax), float(b.ZMax)],
        "size": [float(b.XLength), float(b.YLength), float(b.ZLength)],
    }


def expressions(obj):
    out = {}
    for prop, expr in list(getattr(obj, "ExpressionEngine", [])):
        out[str(prop)] = str(expr)
    return out


def shape_stats(obj):
    s = obj.Shape
    return {
        "is_null": s.isNull(),
        "is_valid": bool(s.isValid()),
        "solids": len(s.Solids),
        "faces": len(s.Faces),
        "edges": len(s.Edges),
        "vertices": len(s.Vertexes),
        "volume_mm3": float(s.Volume),
        "bbox_mm": bbox(s),
    }


def add_length_param(params, name, value):
    params.addProperty("App::PropertyLength", name, "OLEANDER Parameters")
    setattr(params, name, App.Units.Quantity(f"{value} mm"))


def create_model():
    doc = App.newDocument(DOC_NAME)
    params = doc.addObject("App::FeaturePython", PARAM_NAME)
    add_length_param(params, "Length", 80.0)
    add_length_param(params, "Width", 50.0)
    add_length_param(params, "Thickness", 12.0)
    add_length_param(params, "HoleRadius", 8.0)

    body = doc.addObject("PartDesign::Body", BODY_NAME)
    base = doc.addObject("PartDesign::AdditiveBox", BASE_NAME)
    body.addObject(base)
    base.setExpression("Length", f"{PARAM_NAME}.Length")
    base.setExpression("Width", f"{PARAM_NAME}.Width")
    base.setExpression("Height", f"{PARAM_NAME}.Thickness")
    doc.recompute()

    hole = doc.addObject("PartDesign::SubtractiveCylinder", HOLE_NAME)
    body.addObject(hole)
    hole.setExpression("Radius", f"{PARAM_NAME}.HoleRadius")
    hole.setExpression("Height", f"{PARAM_NAME}.Thickness + 10 mm")
    hole.Placement.Base = App.Vector(25.0, 25.0, -5.0)
    doc.recompute()
    return doc, params, body, base, hole


def set_params(params, length, width, thickness, hole_radius):
    params.Length = App.Units.Quantity(f"{length} mm")
    params.Width = App.Units.Quantity(f"{width} mm")
    params.Thickness = App.Units.Quantity(f"{thickness} mm")
    params.HoleRadius = App.Units.Quantity(f"{hole_radius} mm")


def variant_readback(doc, params, base, hole, name):
    doc.recompute()
    values = {
        "length_mm": qmm(params.Length),
        "width_mm": qmm(params.Width),
        "thickness_mm": qmm(params.Thickness),
        "hole_radius_mm": qmm(params.HoleRadius),
    }
    expected = values["length_mm"] * values["width_mm"] * values["thickness_mm"] - math.pi * values["hole_radius_mm"] ** 2 * values["thickness_mm"]
    actual = float(hole.Shape.Volume)
    rel = abs(actual - expected) / max(abs(expected), 1.0)
    result = {
        "name": name,
        "parameters": values,
        "base": shape_stats(base),
        "result": shape_stats(hole),
        "expected_volume_mm3": expected,
        "volume_relative_error": rel,
        "body_tip": getattr(doc.getObject(BODY_NAME).Tip, "Name", None),
        "recompute_errors": [o.Name for o in doc.Objects if "Invalid" in str(getattr(o, "State", [])) or "Error" in str(getattr(o, "State", []))],
    }
    if not result["result"]["is_valid"] or result["result"]["solids"] != 1:
        raise RuntimeError(f"invalid solid in {name}: {result}")
    if rel > 1e-6:
        raise RuntimeError(f"unexpected volume in {name}: {result}")
    return result


def build(out: Path):
    doc, params, body, base, hole = create_model()
    variants = []
    variants.append(variant_readback(doc, params, base, hole, "BASELINE"))

    set_params(params, 96.0, 58.0, 14.0, 9.0)
    variants.append(variant_readback(doc, params, base, hole, "SIZE_SWEEP"))

    set_params(params, 72.0, 46.0, 10.0, 14.0)
    variants.append(variant_readback(doc, params, base, hole, "HOLE_STRESS"))

    # Restore the canonical baseline before native save/export.
    set_params(params, 80.0, 50.0, 12.0, 8.0)
    canonical = variant_readback(doc, params, base, hole, "BASELINE_RESTORED")

    invalid_gate = {
        "name": "DECLARED_INVALID_ENVELOPE",
        "candidate": {"length_mm": 40.0, "width_mm": 30.0, "thickness_mm": 8.0, "hole_radius_mm": 18.0},
        "executed": False,
        "reason": "hole radius would exceed the benchmark's declared contained-through-hole envelope; reject before boolean/recompute rather than treating an arbitrary residual solid as a useful design state",
    }

    native = out / "FREECAD_PARAMETRIC_BENCH.FCStd"
    step = out / "FREECAD_PARAMETRIC_BENCH.step"
    doc.recompute()
    doc.saveAs(str(native))
    Part.export([hole], str(step))

    receipt = {
        "schema": "oleander.3d.freecad-parametric-native.v1",
        "mode": "build",
        "freecad_version": App.Version(),
        "document": DOC_NAME,
        "native_master": native.name,
        "exchange": step.name,
        "representation": "PartDesign Body -> AdditiveBox -> SubtractiveCylinder",
        "parameter_owner": PARAM_NAME,
        "named_parameters": ["Length", "Width", "Thickness", "HoleRadius"],
        "base_expressions": expressions(base),
        "hole_expressions": expressions(hole),
        "reference_strategy": "origin/explicit placement + named parameter expressions; no incidental face/edge attachment",
        "variants": variants,
        "canonical": canonical,
        "invalid_gate": invalid_gate,
        "evidence_class": "NATIVE_EXECUTED_PENDING_REOPEN",
        "does_not_prove": ["Fusion parity", "manufacturing tolerance", "GD&T approval", "assembly fit", "engineering approval"],
    }
    (out / "BUILD_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    (out / "BUILD_SHA256.json").write_text(json.dumps({p.name: sha256(p) for p in [native, step, out / "BUILD_RECEIPT.json"]}, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    App.closeDocument(doc.Name)


def reopen(out: Path):
    native = out / "FREECAD_PARAMETRIC_BENCH.FCStd"
    step = out / "FREECAD_PARAMETRIC_BENCH.step"
    build_receipt = json.loads((out / "BUILD_RECEIPT.json").read_text())

    doc = App.openDocument(str(native))
    params = doc.getObject(PARAM_NAME)
    base = doc.getObject(BASE_NAME)
    hole = doc.getObject(HOLE_NAME)
    body = doc.getObject(BODY_NAME)
    if not all([params, base, hole, body]):
        raise RuntimeError("native reopen missing parameter/body/features")
    doc.recompute()
    reopened = variant_readback(doc, params, base, hole, "NATIVE_REOPEN")
    if reopened["parameters"] != build_receipt["canonical"]["parameters"]:
        raise RuntimeError({"native_parameter_mismatch": [reopened["parameters"], build_receipt["canonical"]["parameters"]]})
    if expressions(base) != build_receipt["base_expressions"] or expressions(hole) != build_receipt["hole_expressions"]:
        raise RuntimeError("native expression dependency graph changed after reopen")

    step_doc = App.newDocument("STEP_ROUNDTRIP")
    Part.insert(str(step), step_doc.Name)
    step_doc.recompute()
    step_shapes = [o for o in step_doc.Objects if hasattr(o, "Shape") and not o.Shape.isNull()]
    if not step_shapes:
        raise RuntimeError("STEP roundtrip contains no shape")
    step_solids = sum(len(o.Shape.Solids) for o in step_shapes)
    step_volume = sum(float(o.Shape.Volume) for o in step_shapes)
    canonical_volume = build_receipt["canonical"]["result"]["volume_mm3"]
    rel = abs(step_volume - canonical_volume) / max(abs(canonical_volume), 1.0)
    if step_solids < 1 or rel > 1e-6:
        raise RuntimeError({"step_solids": step_solids, "step_volume": step_volume, "canonical_volume": canonical_volume, "relative_error": rel})

    receipt = {
        "schema": "oleander.3d.freecad-parametric-reopen.v1",
        "mode": "reopen",
        "freecad_version": App.Version(),
        "native_reopen": reopened,
        "native_expression_graph_preserved": True,
        "step_roundtrip": {
            "shape_objects": len(step_shapes),
            "solids": step_solids,
            "volume_mm3": step_volume,
            "volume_relative_error": rel,
            "parameter_object_preserved": any(o.Name == PARAM_NAME for o in step_doc.Objects),
            "partdesign_body_preserved": any(o.TypeId == "PartDesign::Body" for o in step_doc.Objects),
            "semantic_loss": "STEP preserves B-Rep result geometry but not this FreeCAD PartDesign/named-parameter dependency graph",
        },
        "evidence_class": "RECOVERED_NATIVE_WITH_STEP_DCC_ROUNDTRIP",
        "promotion_scope": [
            "FreeCAD named-parameter expression dependency native execution",
            "PartDesign recompute sweep across declared variants",
            "native FCStd reopen stability",
            "STEP result-geometry roundtrip with parametric-history loss explicitly recorded",
        ],
        "holds": ["Fusion native runtime", "assembly fit", "manufacturing tolerance/GD&T", "engineering approval"],
    }
    if receipt["step_roundtrip"]["parameter_object_preserved"] or receipt["step_roundtrip"]["partdesign_body_preserved"]:
        raise RuntimeError("unexpected FreeCAD parametric semantics preserved in STEP roundtrip")
    (out / "REOPEN_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    App.closeDocument(step_doc.Name)
    App.closeDocument(doc.Name)


def main():
    mode = os.environ.get("OLEANDER_MODE", "").strip().lower()
    out = Path(os.environ.get("OLEANDER_OUT", ".")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if mode == "build":
        build(out)
    elif mode == "reopen":
        reopen(out)
    else:
        raise SystemExit("OLEANDER_MODE must be build or reopen")


if __name__ == "__main__":
    main()
