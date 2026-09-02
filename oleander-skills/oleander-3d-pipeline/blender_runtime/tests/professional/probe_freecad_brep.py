"""OLEANDER professional dependency probe: FreeCAD/OCCT process sidecar.

Run with FreeCADCmd, not Blender Python. This validates a bounded authoritative
B-Rep process route, STEP/BREP round-trip, deterministic measurement and a
triangulated display derivative payload. PASS does not make P0-A or P0-B PASS.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path("/tmp/oleander-freecad-probe")
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_brep_master.FCStd"
STEP = OUT / "oleander_brep_master.step"
BREP = OUT / "oleander_brep_master.brep"
MANIFEST = OUT / "oleander_brep_manifest.json"
MESH = OUT / "oleander_brep_display_mesh.json"

checks: list[str] = []


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def bbox(shape):
    b = shape.BoundBox
    return {
        "x_min_mm": b.XMin,
        "x_max_mm": b.XMax,
        "y_min_mm": b.YMin,
        "y_max_mm": b.YMax,
        "z_min_mm": b.ZMin,
        "z_max_mm": b.ZMax,
        "x_length_mm": b.XLength,
        "y_length_mm": b.YLength,
        "z_length_mm": b.ZLength,
    }


def close(a: float, b: float, tol: float = 1e-5) -> bool:
    return abs(a - b) <= tol


def build_authoritative_shape(width_mm: float = 80.0):
    # Bounded direct B-Rep workflow: primitive -> OCCT fillet -> boolean cut.
    base = Part.makeBox(width_mm, 50.0, 10.0)
    check(base.isValid(), "brep_box_valid")
    check(base.ShapeType == "Solid", "brep_box_solid")

    # Apply a small constant-radius fillet to one stable edge in this controlled
    # fixture. This validates callable OCCT fillet behavior, not broad fillet
    # robustness or topological naming stability.
    filleted = base.makeFillet(2.0, [base.Edges[0]])
    check(filleted.isValid(), "brep_fillet_valid")
    check(filleted.ShapeType == "Solid", "brep_fillet_solid")

    hole = Part.makeCylinder(5.0, 10.0, App.Vector(width_mm * 0.25, 25.0, 0.0))
    result = filleted.cut(hole).removeSplitter()
    check(result.isValid(), "brep_boolean_cut_valid")
    check(result.ShapeType == "Solid", "brep_boolean_cut_solid")
    check(len(result.Solids) == 1, "brep_single_solid")
    check(result.Volume > 0.0, "brep_positive_volume")
    return result


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    shape = build_authoritative_shape(80.0)
    dims = bbox(shape)
    check(close(dims["x_length_mm"], 80.0), "brep_metric_width")
    check(close(dims["y_length_mm"], 50.0), "brep_metric_depth")
    check(close(dims["z_length_mm"], 10.0), "brep_metric_height")

    # A parameterized rebuild in the sidecar function changes authoritative B-Rep
    # deterministically, but this is not yet a native feature-tree rebuild gate.
    wider = build_authoritative_shape(100.0)
    check(close(wider.BoundBox.XLength, 100.0), "brep_parameterized_rebuild_width")
    check(wider.Volume > shape.Volume, "brep_parameterized_rebuild_volume_change")

    doc = App.newDocument("OLEANDER_BREP_MASTER")
    obj = doc.addObject("Part::Feature", "OLE_BREP_MASTER")
    obj.Label = "OLEANDER BRep Master"
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = "OLE_PRO_PRODUCT_BREP_001"
    obj.addProperty("App::PropertyLength", "Width", "OLEANDER")
    obj.Width = 80.0
    obj.addProperty("App::PropertyLength", "Depth", "OLEANDER")
    obj.Depth = 50.0
    obj.addProperty("App::PropertyLength", "Thickness", "OLEANDER")
    obj.Thickness = 10.0
    obj.addProperty("App::PropertyLength", "HoleRadius", "OLEANDER")
    obj.HoleRadius = 5.0
    obj.Shape = shape
    doc.recompute()
    doc.saveAs(str(FCSTD))
    check(FCSTD.exists() and FCSTD.stat().st_size > 0, "fcstd_master_saved")

    shape.exportStep(str(STEP))
    shape.exportBrep(str(BREP))
    check(STEP.exists() and STEP.stat().st_size > 0, "step_exported")
    check(BREP.exists() and BREP.stat().st_size > 0, "brep_exported")

    step_shape = Part.Shape()
    step_shape.read(str(STEP))
    check(step_shape.isValid(), "step_roundtrip_shape_valid")
    check(step_shape.ShapeType == "Solid", "step_roundtrip_solid")
    step_dims = bbox(step_shape)
    for key in ("x_length_mm", "y_length_mm", "z_length_mm"):
        check(close(step_dims[key], dims[key], 1e-4), f"step_roundtrip_{key}")
    check(
        math.isclose(step_shape.Volume, shape.Volume, rel_tol=1e-6, abs_tol=1e-4),
        "step_roundtrip_volume",
    )

    brep_shape = Part.Shape()
    brep_shape.read(str(BREP))
    check(brep_shape.isValid(), "brep_roundtrip_shape_valid")
    check(
        math.isclose(brep_shape.Volume, shape.Volume, rel_tol=1e-9, abs_tol=1e-6),
        "brep_roundtrip_volume",
    )

    vertices, facets = step_shape.tessellate(0.25)
    check(len(vertices) > 0 and len(facets) > 0, "display_tessellation_nonempty")
    mesh_payload = {
        "schema": "OLEANDER_CAD_DISPLAY_DERIVATIVE_v0.1",
        "source_master": str(FCSTD),
        "source_step": str(STEP),
        "source_step_sha256": sha256(STEP),
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "units": "mm",
        "vertices_mm": [[v.x, v.y, v.z] for v in vertices],
        "triangles": [list(face) for face in facets],
        "source_bbox": dims,
        "source_volume_mm3": shape.Volume,
    }
    MESH.write_text(json.dumps(mesh_payload, sort_keys=True), encoding="utf-8")
    check(MESH.exists() and MESH.stat().st_size > 0, "display_derivative_payload_written")

    manifest = {
        "schema": "OLEANDER_PROFESSIONAL_DEPENDENCY_PROBE_v0.1",
        "dependency": "FreeCAD + OpenCascade",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN"),
        "status": "PASS",
        "authoritative_master": str(FCSTD),
        "step": {"path": str(STEP), "sha256": sha256(STEP)},
        "brep": {"path": str(BREP), "sha256": sha256(BREP)},
        "display_derivative": str(MESH),
        "checks": checks,
        "non_claims": [
            "P0_A_PARAMETRIC_CAD_PASS",
            "P0_B_DIRECT_BREP_PASS",
            "native_sketch_feature_tree",
            "assembly_mates",
            "broad_fillet_robustness",
            "topological_naming_stability",
            "engineering_approval",
            "manufacturing_release",
        ],
    }
    MANIFEST.write_text(json.dumps(manifest, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_BREP_PROBE=" + json.dumps(manifest, sort_keys=True))


if __name__ == "__main__":
    main()
