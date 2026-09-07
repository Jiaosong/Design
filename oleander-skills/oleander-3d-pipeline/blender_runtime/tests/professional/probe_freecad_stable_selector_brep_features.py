"""OLEANDER bounded Direct B-Rep feature probe using geometric selectors.

This probe deliberately avoids persistent EdgeN/FaceN indexes. Each authoritative
revision rebuilds a simple OCCT solid and re-resolves feature inputs from a
geometric selector rule before applying fillet/chamfer/thickness operations.

Validated bounded operations:
- vertical straight-edge selector -> fillet
- vertical straight-edge selector -> chamfer
- top planar-face selector -> inward thickness/shell

This is not general direct-face modeling or topological naming parity.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import FreeCAD as App
import Part

OUT = Path(os.environ.get("OLEANDER_DIRECT_BREP_DIR", "/tmp/oleander-direct-brep"))
OUT.mkdir(parents=True, exist_ok=True)
FCSTD = OUT / "oleander_stable_selector_brep.FCStd"
MANIFEST = OUT / "oleander_stable_selector_brep.json"
DISPLAY = OUT / "oleander_stable_selector_brep_display.json"
checks: list[str] = []

EDGE_SELECTOR_ID = "SELECTOR::VERTICAL_STRAIGHT_OUTER_EDGES"
TOP_FACE_SELECTOR_ID = "SELECTOR::TOP_PLANAR_FACE"


def check(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)
    checks.append(label)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def normalize_single_solid(shape, label: str):
    check(shape.isValid(), f"{label}_valid")
    check(len(shape.Solids) == 1, f"{label}_single_solid")
    solid = shape.Solids[0]
    check(solid.isValid(), f"{label}_normalized_valid")
    check(solid.ShapeType == "Solid", f"{label}_normalized_solid")
    check(solid.Volume > 0.0, f"{label}_positive_volume")
    return solid


def select_vertical_straight_outer_edges(shape, tol: float = 1e-7):
    """Re-resolve box-like outer vertical edges from geometry, not EdgeN IDs."""
    z_span = shape.BoundBox.ZLength
    selected = []
    descriptors = []
    for edge in shape.Edges:
        verts = edge.Vertexes
        if len(verts) != 2:
            continue
        a = verts[0].Point
        b = verts[1].Point
        dx = abs(a.x - b.x)
        dy = abs(a.y - b.y)
        dz = abs(a.z - b.z)
        if dx <= tol and dy <= tol and abs(dz - z_span) <= tol:
            selected.append(edge)
            descriptors.append({
                "midpoint_xy_mm": [round((a.x + b.x) * 0.5, 9), round((a.y + b.y) * 0.5, 9)],
                "z_span_mm": round(dz, 9),
                "length_mm": round(edge.Length, 9),
            })
    descriptors.sort(key=lambda item: (item["midpoint_xy_mm"][0], item["midpoint_xy_mm"][1]))
    return selected, descriptors


def select_top_planar_face(shape, tol: float = 1e-7):
    """Resolve the unique planar face on the maximum-Z boundary."""
    zmax = shape.BoundBox.ZMax
    selected = []
    descriptors = []
    for face in shape.Faces:
        box = face.BoundBox
        if box.ZLength > tol or abs(box.ZMax - zmax) > tol:
            continue
        # For a planar top face, normal at an interior UV point must align +Z.
        try:
            u0, u1, v0, v1 = face.ParameterRange
            normal = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
        except Exception:
            continue
        if abs(normal.x) <= 1e-6 and abs(normal.y) <= 1e-6 and normal.z > 0.999999:
            selected.append(face)
            c = face.CenterOfMass
            descriptors.append({
                "center_mm": [round(c.x, 9), round(c.y, 9), round(c.z, 9)],
                "area_mm2": round(face.Area, 9),
                "normal": [round(normal.x, 9), round(normal.y, 9), round(normal.z, 9)],
            })
    return selected, descriptors


def fillet_preflight(shape, radius_mm: float) -> None:
    # Bounded OLEANDER contract: reject obviously unsafe radius before OCCT call.
    limit = 0.5 * min(shape.BoundBox.XLength, shape.BoundBox.YLength)
    if not math.isfinite(radius_mm) or radius_mm <= 0.0 or radius_mm >= limit:
        raise ValueError(f"fillet radius {radius_mm} mm violates bounded limit < {limit} mm")


def build_revision(width_mm: float, revision: int) -> dict:
    base = normalize_single_solid(Part.makeBox(width_mm, 50.0, 10.0), f"r{revision}_base")

    edges, edge_desc = select_vertical_straight_outer_edges(base)
    check(len(edges) == 4, f"r{revision}_vertical_selector_count")
    check(len(edge_desc) == 4, f"r{revision}_vertical_selector_descriptors")

    fillet_preflight(base, 2.0)
    fillet = normalize_single_solid(base.makeFillet(2.0, edges), f"r{revision}_fillet")
    check(fillet.Volume < base.Volume, f"r{revision}_fillet_volume_reduction")

    # Resolve again from the base; do not reuse edge handles from another feature.
    chamfer_edges, chamfer_desc = select_vertical_straight_outer_edges(base)
    check(len(chamfer_edges) == 4, f"r{revision}_chamfer_selector_count")
    chamfer = normalize_single_solid(base.makeChamfer(2.0, chamfer_edges), f"r{revision}_chamfer")
    check(chamfer.Volume < base.Volume, f"r{revision}_chamfer_volume_reduction")

    top_faces, top_desc = select_top_planar_face(base)
    check(len(top_faces) == 1, f"r{revision}_top_face_selector_count")
    shell = normalize_single_solid(base.makeThickness(top_faces, -2.0, 0.0001), f"r{revision}_shell")
    check(shell.Volume < base.Volume, f"r{revision}_shell_volume_reduction")
    check(abs(shell.BoundBox.XLength - base.BoundBox.XLength) < 1e-6, f"r{revision}_shell_outer_width_preserved")
    check(abs(shell.BoundBox.YLength - base.BoundBox.YLength) < 1e-6, f"r{revision}_shell_outer_depth_preserved")
    check(abs(shell.BoundBox.ZLength - base.BoundBox.ZLength) < 1e-6, f"r{revision}_shell_outer_height_preserved")

    return {
        "revision": revision,
        "width_mm": width_mm,
        "base": base,
        "fillet": fillet,
        "chamfer": chamfer,
        "shell": shell,
        "selectors": {
            "vertical_edges": {"selector_id": EDGE_SELECTOR_ID, "selected_count": len(edges), "descriptors": edge_desc},
            "chamfer_vertical_edges": {"selector_id": EDGE_SELECTOR_ID, "selected_count": len(chamfer_edges), "descriptors": chamfer_desc},
            "top_face": {"selector_id": TOP_FACE_SELECTOR_ID, "selected_count": len(top_faces), "descriptors": top_desc},
        },
    }


def metrics(shape) -> dict:
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
        "edge_count": len(shape.Edges),
        "face_count": len(shape.Faces),
    }


def add_feature_object(doc, name: str, ole_id: str, role: str, shape, selector_id: str, revision: int):
    obj = doc.addObject("Part::Feature", name)
    obj.Label = name
    obj.Shape = shape
    obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
    obj.OLE_ID = ole_id
    obj.addProperty("App::PropertyString", "OLE_Role", "OLEANDER")
    obj.OLE_Role = role
    obj.addProperty("App::PropertyString", "OLE_SelectorID", "OLEANDER")
    obj.OLE_SelectorID = selector_id
    obj.addProperty("App::PropertyInteger", "OLE_Revision", "OLEANDER")
    obj.OLE_Revision = revision
    obj.addProperty("App::PropertyString", "OLE_Authority", "OLEANDER")
    obj.OLE_Authority = "FREECAD_OCCT_BREP"
    return obj


def main() -> None:
    r1 = build_revision(80.0, 1)
    r2 = build_revision(100.0, 2)
    check(r1["selectors"]["vertical_edges"]["selected_count"] == r2["selectors"]["vertical_edges"]["selected_count"] == 4, "selector_count_stable_across_rebuild")
    check(r1["selectors"]["top_face"]["selected_count"] == r2["selectors"]["top_face"]["selected_count"] == 1, "top_face_selector_stable_across_rebuild")
    check(r2["fillet"].Volume > r1["fillet"].Volume, "fillet_rebuild_changes_geometry")
    check(r2["chamfer"].Volume > r1["chamfer"].Volume, "chamfer_rebuild_changes_geometry")
    check(r2["shell"].Volume > r1["shell"].Volume, "shell_rebuild_changes_geometry")

    # Deterministic positive failure: bounded preflight rejects unsafe radius
    # before invoking OCCT instead of depending on kernel-specific failure behavior.
    try:
        fillet_preflight(r2["base"], 30.0)
    except ValueError as exc:
        check("violates bounded limit" in str(exc), "oversized_fillet_expected_failure")
    else:
        raise AssertionError("oversized_fillet_expected_failure")

    doc = App.newDocument("OLEANDER_STABLE_SELECTOR_BREP")
    base_obj = add_feature_object(doc, "OLE_BASE_R002", "OLE_BREP::BASE_002", "BASE_SOLID", r2["base"], "NONE", 2)
    fillet_obj = add_feature_object(doc, "OLE_FILLET_R002", "OLE_BREP::FILLET_002", "FILLET", r2["fillet"], EDGE_SELECTOR_ID, 2)
    chamfer_obj = add_feature_object(doc, "OLE_CHAMFER_R002", "OLE_BREP::CHAMFER_002", "CHAMFER", r2["chamfer"], EDGE_SELECTOR_ID, 2)
    shell_obj = add_feature_object(doc, "OLE_SHELL_R002", "OLE_BREP::SHELL_002", "SHELL", r2["shell"], TOP_FACE_SELECTOR_ID, 2)
    doc.recompute()
    doc.saveAs(str(FCSTD))
    check(FCSTD.exists() and FCSTD.stat().st_size > 0, "fcstd_saved")

    # Export each authoritative variant independently for downstream comparison.
    step_paths = {}
    for role, obj in (("fillet", fillet_obj), ("chamfer", chamfer_obj), ("shell", shell_obj)):
        path = OUT / f"oleander_{role}_R002.step"
        obj.Shape.exportStep(str(path))
        check(path.exists() and path.stat().st_size > 0, f"{role}_step_exported")
        step_paths[role] = {"path": str(path), "sha256": file_sha256(path)}

    # Blender display derivative uses the fillet variant; other variants remain
    # separate authoritative STEP outputs recorded in the manifest.
    vertices, facets = fillet_obj.Shape.tessellate(0.25)
    check(bool(vertices) and bool(facets), "fillet_display_tessellation")
    display = {
        "schema": "OLEANDER_STABLE_SELECTOR_BREP_DISPLAY_v0.1",
        "master_type": "CAD_NATIVE",
        "geometry_authority": "FREECAD_OCCT_BREP",
        "display_authority": "DISPLAY_DERIVATIVE_ONLY",
        "feature_ole_id": fillet_obj.OLE_ID,
        "feature_role": "FILLET",
        "selector_id": EDGE_SELECTOR_ID,
        "revision": 2,
        "units": "mm",
        "source_fcstd": str(FCSTD),
        "source_fcstd_sha256": file_sha256(FCSTD),
        "source_step": step_paths["fillet"]["path"],
        "source_step_sha256": step_paths["fillet"]["sha256"],
        "vertices_mm": [[v.x, v.y, v.z] for v in vertices],
        "triangles": [list(face) for face in facets],
        "bbox_mm": metrics(fillet_obj.Shape)["bbox_mm"],
    }
    DISPLAY.write_text(json.dumps(display, sort_keys=True), encoding="utf-8")
    check(DISPLAY.exists() and DISPLAY.stat().st_size > 0, "display_payload_written")

    App.closeDocument(doc.Name)
    reopened = App.openDocument(str(FCSTD))
    for name, ole_id, selector_id in (
        ("OLE_FILLET_R002", "OLE_BREP::FILLET_002", EDGE_SELECTOR_ID),
        ("OLE_CHAMFER_R002", "OLE_BREP::CHAMFER_002", EDGE_SELECTOR_ID),
        ("OLE_SHELL_R002", "OLE_BREP::SHELL_002", TOP_FACE_SELECTOR_ID),
    ):
        obj = reopened.getObject(name)
        check(obj is not None, f"{name}_reopen")
        check(obj.OLE_ID == ole_id, f"{name}_ole_id_reopen")
        check(obj.OLE_SelectorID == selector_id, f"{name}_selector_reopen")
        check(obj.OLE_Authority == "FREECAD_OCCT_BREP", f"{name}_authority_reopen")
        check(obj.Shape.isValid() and len(obj.Shape.Solids) == 1, f"{name}_solid_reopen")

    result = {
        "schema": "OLEANDER_FREECAD_STABLE_SELECTOR_BREP_FEATURES_v0.1",
        "status": "PASS",
        "dependency_state": "RUNTIME_PROBED",
        "freecad_version": ".".join(str(x) for x in App.Version()[:3]),
        "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN"),
        "selector_contract": {
            EDGE_SELECTOR_ID: "two-vertex straight edge; XY endpoint delta ~0; Z span equals authoritative solid height",
            TOP_FACE_SELECTOR_ID: "unique zero-Z-span face on ZMax boundary with +Z planar normal"
        },
        "revision1": {
            "width_mm": 80.0,
            "selectors": r1["selectors"],
            "base": metrics(r1["base"]),
            "fillet": metrics(r1["fillet"]),
            "chamfer": metrics(r1["chamfer"]),
            "shell": metrics(r1["shell"]),
        },
        "revision2": {
            "width_mm": 100.0,
            "selectors": r2["selectors"],
            "base": metrics(r2["base"]),
            "fillet": metrics(r2["fillet"]),
            "chamfer": metrics(r2["chamfer"]),
            "shell": metrics(r2["shell"]),
        },
        "artifacts": {
            "fcstd": {"path": str(FCSTD), "sha256": file_sha256(FCSTD)},
            "steps": step_paths,
            "display": {"path": str(DISPLAY), "sha256": file_sha256(DISPLAY)},
        },
        "checks": checks,
        "expected_failure_cases": {"oversized_fillet_preflight": "PASS"},
        "non_claims": [
            "P0_B_DIRECT_BREP_PASS",
            "persistent_topological_naming",
            "direct_face_push_pull",
            "direct_face_translate_rotate",
            "split_trim",
            "general_shell_robustness",
            "general_fillet_chamfer_robustness",
            "brep_healing_parity",
            "engineering_approval",
        ],
    }
    MANIFEST.write_text(json.dumps(result, sort_keys=True), encoding="utf-8")
    print("OLEANDER_FREECAD_STABLE_SELECTOR_BREP=" + json.dumps(result, sort_keys=True))


main()
