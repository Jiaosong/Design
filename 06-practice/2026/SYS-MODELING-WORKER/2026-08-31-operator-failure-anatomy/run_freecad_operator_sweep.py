#!/usr/bin/env python3
import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

DOC_NAME = "OLEANDER_OPERATOR_FAILURE_ANATOMY"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def finite(v):
    try:
        return float(v)
    except Exception:
        return None


def shape_stats(shape):
    if shape is None:
        return {"is_null": True, "is_valid": False}
    try:
        is_null = bool(shape.isNull())
    except Exception:
        is_null = True
    if is_null:
        return {"is_null": True, "is_valid": False}
    try:
        valid = bool(shape.isValid())
    except Exception:
        valid = False
    b = shape.BoundBox
    return {
        "is_null": False,
        "is_valid": valid,
        "shape_type": shape.ShapeType,
        "solids": len(shape.Solids),
        "shells": len(shape.Shells),
        "faces": len(shape.Faces),
        "edges": len(shape.Edges),
        "vertices": len(shape.Vertexes),
        "volume_mm3": finite(shape.Volume),
        "area_mm2": finite(shape.Area),
        "bbox_mm": {
            "size": [float(b.XLength), float(b.YLength), float(b.ZLength)],
            "min": [float(b.XMin), float(b.YMin), float(b.ZMin)],
            "max": [float(b.XMax), float(b.YMax), float(b.ZMax)],
        },
    }


def attempt(label, fn, **meta):
    record = {"label": label, **meta}
    try:
        shape = fn()
        record["kernel_returned"] = True
        record["stats"] = shape_stats(shape)
        record["kernel_success"] = bool(
            not record["stats"].get("is_null") and record["stats"].get("is_valid")
        )
        return record, shape
    except Exception as exc:
        record["kernel_returned"] = False
        record["kernel_success"] = False
        record["exception_type"] = type(exc).__name__
        record["exception"] = str(exc)
        record["failure_mode"] = "KERNEL_EXCEPTION"
        return record, None


def nearly(a, b, tol=1e-8):
    return a is not None and b is not None and abs(float(a) - float(b)) <= tol


def same_as_base(stats, base_stats, tol=1e-8):
    if not stats or not stats.get("is_valid"):
        return False
    exact_keys = ("shape_type", "solids", "shells", "faces", "edges", "vertices")
    if any(stats.get(k) != base_stats.get(k) for k in exact_keys):
        return False
    if not nearly(stats.get("volume_mm3"), base_stats.get("volume_mm3"), tol):
        return False
    if not nearly(stats.get("area_mm2"), base_stats.get("area_mm2"), tol):
        return False
    return all(nearly(a, b, tol) for a, b in zip(stats["bbox_mm"]["size"], base_stats["bbox_mm"]["size"]))


def classify_generic(record):
    if not record.get("kernel_returned"):
        record.setdefault("failure_mode", "KERNEL_EXCEPTION")
        record["semantic_success"] = False
    elif not record.get("kernel_success"):
        record["failure_mode"] = "INVALID_RETURNED_SHAPE"
        record["semantic_success"] = False
    else:
        record["failure_mode"] = "SUCCESS"
        record["semantic_success"] = True
    return record


def top_face(shape):
    return max(shape.Faces, key=lambda f: float(f.CenterOfMass.z))


def add_feature(doc, name, label, shape):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = label
    obj.Shape = shape
    return obj


def select_last_semantic_success(records, shapes, predicate=lambda r: True):
    chosen = None
    for rec, shape in zip(records, shapes):
        if rec.get("semantic_success") and shape is not None and predicate(rec):
            chosen = (rec, shape)
    return chosen


def main():
    out = Path(os.environ.get("OLEANDER_OUT", "out/FREECAD_OPERATOR")).resolve()
    cfg_path = Path(os.environ.get("OLEANDER_CONFIG", "operator_sweep.json")).resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(cfg_path.read_text())
    fc = cfg["freecad"]
    box_cfg = fc["box"]
    tol = float(fc["tolerance"])

    base = Part.makeBox(float(box_cfg["length"]), float(box_cfg["width"]), float(box_cfg["height"]))
    base_stats = shape_stats(base)
    min_dim = min(float(box_cfg["length"]), float(box_cfg["width"]), float(box_cfg["height"]))
    half_min = min_dim / 2.0

    fillet_records, fillet_shapes = [], []
    for radius in fc["fillet_radii"]:
        r = float(radius)
        rec, shape = attempt(
            f"fillet_r_{r:g}",
            lambda r=r: base.makeFillet(r, base.Edges),
            radius_mm=r,
            analytic_local_half_min_mm=half_min,
            inside_simple_convex_box_domain=bool(r < half_min),
        )
        classify_generic(rec)
        if rec.get("semantic_success") and same_as_base(rec["stats"], base_stats):
            rec["semantic_success"] = False
            rec["failure_mode"] = "VALID_SEMANTIC_NOOP"
        fillet_records.append(rec)
        fillet_shapes.append(shape)

    open_face = top_face(base)
    thickness_records, thickness_shapes = [], []
    for value in fc["thickness_values"]:
        t = float(value)
        rec, shape = attempt(
            f"thickness_inward_{t:g}",
            lambda t=t: base.makeThickness([open_face], -t, tol),
            thickness_mm=t,
            sign="inward_negative_offset",
            box_half_width_mm=float(box_cfg["width"]) / 2.0,
            box_half_length_mm=float(box_cfg["length"]) / 2.0,
        )
        classify_generic(rec)
        rec["semantic_noop_returned_base"] = bool(rec.get("kernel_success") and same_as_base(rec.get("stats"), base_stats))
        if rec["semantic_noop_returned_base"]:
            rec["semantic_success"] = False
            rec["failure_mode"] = "VALID_SEMANTIC_NOOP"
        thickness_records.append(rec)
        thickness_shapes.append(shape)

    sphere_radius = float(fc["sphere_radius"])
    sphere = Part.makeSphere(sphere_radius)
    shell = sphere.Shells[0]
    offset_records, offset_shapes = [], []
    for offset in fc["sphere_offsets"]:
        d = float(offset)
        expected_radius = sphere_radius + d
        rec, shape = attempt(
            f"sphere_shell_offset_{d:g}",
            lambda d=d: shell.makeOffsetShape(d, tol, join=0, fill=False),
            offset_mm=d,
            source_radius_mm=sphere_radius,
            analytic_expected_radius_mm=expected_radius,
            inside_regular_sphere_offset_domain=bool(expected_radius > 0.0),
        )
        classify_generic(rec)
        if rec.get("kernel_success") and shape is not None:
            observed_diameter = max(rec["stats"]["bbox_mm"]["size"])
            rec["observed_max_diameter_mm"] = observed_diameter
            if expected_radius > 0:
                expected_diameter = 2.0 * expected_radius
                rec["analytic_expected_diameter_mm"] = expected_diameter
                rec["diameter_abs_error_mm"] = abs(observed_diameter - expected_diameter)
                rec["semantic_success"] = rec["diameter_abs_error_mm"] <= 1e-8
                rec["failure_mode"] = "SUCCESS" if rec["semantic_success"] else "VALID_SEMANTIC_DRIFT"
            else:
                rec["semantic_success"] = False
                rec["failure_mode"] = "OUTSIDE_ANALYTIC_DOMAIN_RETURNED_SHAPE"
        offset_records.append(rec)
        offset_shapes.append(shape)

    low_fillet_ok = all(
        r["semantic_success"] for r in fillet_records if float(r["radius_mm"]) <= 3.0
    )
    fillet_high = [r for r in fillet_records if float(r["radius_mm"]) >= half_min]
    fillet_transition = any(not r["semantic_success"] for r in fillet_high)
    fillet_exception_observed = any(r.get("failure_mode") == "KERNEL_EXCEPTION" for r in fillet_high)
    fillet_invalid_return_observed = any(r.get("failure_mode") == "INVALID_RETURNED_SHAPE" for r in fillet_high)

    low_thickness_ok = all(
        r["semantic_success"] for r in thickness_records if float(r["thickness_mm"]) <= 4.0
    )
    thickness_high = [r for r in thickness_records if float(r["thickness_mm"]) >= 12.0]
    thickness_transition = any(not r["semantic_success"] for r in thickness_high)
    thickness_exception_observed = any(r.get("failure_mode") == "KERNEL_EXCEPTION" for r in thickness_high)
    valid_semantic_noop_observed = any(r.get("failure_mode") == "VALID_SEMANTIC_NOOP" for r in thickness_high)

    offset_regular = [r for r in offset_records if r["inside_regular_sphere_offset_domain"]]
    offset_regular_ok = all(r["semantic_success"] for r in offset_regular)
    offset_outside = [r for r in offset_records if not r["inside_regular_sphere_offset_domain"]]
    offset_domain_boundary_exercised = bool(offset_outside)
    offset_kernel_transition = all(not r["kernel_success"] for r in offset_outside)

    doc = App.newDocument(DOC_NAME)
    add_feature(doc, "BASE_BOX", "BASE BOX 40x24x12", base)
    low_fillet = next(((r, s) for r, s in zip(fillet_records, fillet_shapes) if r.get("semantic_success")), None)
    near_fillet = select_last_semantic_success(fillet_records, fillet_shapes)
    low_thickness = next(((r, s) for r, s in zip(thickness_records, thickness_shapes) if r.get("semantic_success")), None)
    near_thickness = select_last_semantic_success(thickness_records, thickness_shapes)
    regular_offset = select_last_semantic_success(
        offset_records,
        offset_shapes,
        lambda r: r.get("inside_regular_sphere_offset_domain", False) and float(r["offset_mm"]) < 0,
    )

    representative_names = []
    for name, label, pair in [
        ("FILLET_LOW", "Fillet low-radius valid", low_fillet),
        ("FILLET_NEAR", "Fillet last semantic-success sweep state", near_fillet),
        ("THICKNESS_LOW", "Thickness low semantic-success", low_thickness),
        ("THICKNESS_NEAR", "Thickness last semantic-success sweep state", near_thickness),
        ("OFFSET_SPHERE_INWARD", "Sphere shell inward regular offset", regular_offset),
    ]:
        if pair is not None and pair[1] is not None:
            add_feature(doc, name, label, pair[1])
            representative_names.append(name)
    doc.recompute()
    native = out / "FREECAD_OPERATOR_FAILURE_ANATOMY.FCStd"
    doc.saveAs(str(native))
    native_sha = sha256(native)
    App.closeDocument(doc.Name)

    reopen = App.openDocument(str(native))
    reopen.recompute()
    reopen_objects = {}
    reopen_ok = True
    for name in ["BASE_BOX"] + representative_names:
        obj = reopen.getObject(name)
        valid = bool(obj is not None and not obj.Shape.isNull() and obj.Shape.isValid())
        reopen_objects[name] = {
            "present": obj is not None,
            "valid": valid,
            "stats": shape_stats(obj.Shape) if obj is not None else None,
        }
        reopen_ok = reopen_ok and valid
    App.closeDocument(reopen.Name)

    contract = {
        "freecad_runtime_executed": True,
        "fillet_low_radius_semantic_success": low_fillet_ok,
        "fillet_boundary_transition_observed": fillet_transition,
        "fillet_kernel_exception_observed": fillet_exception_observed,
        "fillet_invalid_returned_shape_observed": fillet_invalid_return_observed,
        "thickness_low_value_semantic_success": low_thickness_ok,
        "thickness_boundary_transition_observed": thickness_transition,
        "thickness_kernel_exception_observed": thickness_exception_observed,
        "thickness_valid_semantic_noop_observed": valid_semantic_noop_observed,
        "sphere_regular_offset_semantic_success": offset_regular_ok,
        "sphere_nonpositive_radius_domain_exercised": offset_domain_boundary_exercised,
        "sphere_kernel_failure_outside_regular_domain": offset_kernel_transition,
        "native_reopen_valid": reopen_ok,
    }
    required = list(contract.values())
    overall = all(required)

    receipt = {
        "schema": "oleander.3d.operator-failure-anatomy.freecad.v2",
        "freecad_version": App.Version(),
        "config": cfg_path.name,
        "config_sha256": sha256(cfg_path),
        "base_box": base_stats,
        "fillet": fillet_records,
        "thickness": thickness_records,
        "sphere_offset": offset_records,
        "native": {"file": native.name, "bytes": native.stat().st_size, "sha256": native_sha},
        "reopen": reopen_objects,
        "contract": contract,
        "overall_pass": overall,
        "semantic_rule": "KERNEL_RETURN / IsValid is necessary but not sufficient; operator success requires a declared postcondition and a non-noop realized result.",
        "claim_boundary": cfg["claim_boundary"],
    }
    (out / "FREECAD_OPERATOR_RECEIPT.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    if not overall:
        raise SystemExit(7)


if __name__ == "__main__":
    main()
