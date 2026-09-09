"""Bounded FreeCAD/OCCT executor for OLEANDER CAD direct-edit requests.

This is a process-sidecar service under the existing CAD Sidecar Integration
surface. It executes exactly one bounded operation: FACE_NORMAL_MOVE on the
uniquely re-resolved +Z planar top face of a rectangular prismatic single solid.
It never persists FaceN/EdgeN ordinals and returns HOLD, with no released output
artifacts, when semantic face resolution is missing or ambiguous.

This is not general push/pull, persistent topological naming, or P0-B parity.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path

import FreeCAD as App
import Part

REQUEST_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_REQUEST_v0.1"
RESPONSE_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_RESPONSE_v0.1"
DISPLAY_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_DISPLAY_DERIVATIVE_v0.1"
REQUIRED_KERNEL = "FREECAD_OCCT_BREP"
OPERATION = "FACE_NORMAL_MOVE"
TOL = 1e-6
MATCH_TOL_MM = 1e-4
MATCH_REL = 1e-6

REQUEST_PATH = Path(os.environ["OLEANDER_CAD_DIRECT_REQUEST"])
OUT = Path(os.environ["OLEANDER_CAD_DIRECT_DIR"])
OUT.mkdir(parents=True, exist_ok=True)
RESPONSE_PATH = OUT / "cad_direct_edit_response.json"
DISPLAY_PATH = OUT / "cad_direct_edit_display_derivative.json"

PROHIBITED = {"FaceN", "EdgeN", "VertexN", "subshape_ordinal", "polygon_index"}


def canonical_bytes(payload: dict) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def payload_sha256(payload: dict) -> str:
    return hashlib.sha256(canonical_bytes(payload)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def finite(value, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must be numeric") from exc
    require(math.isfinite(number), f"{label} must be finite")
    return number


def vector3(value, label: str) -> list[float]:
    require(isinstance(value, list) and len(value) == 3, f"{label} must contain 3 values")
    return [finite(v, label) for v in value]


def contains_ordinal(value) -> bool:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in PROHIBITED or contains_ordinal(child):
                return True
        return False
    if isinstance(value, list):
        return any(contains_ordinal(child) for child in value)
    if isinstance(value, str):
        return bool(re.fullmatch(r"(?:Face|Edge|Vertex)\d+", value.strip()))
    return False


def validate_request(request: dict) -> dict:
    require(isinstance(request, dict), "request must be an object")
    require(request.get("schema") == REQUEST_SCHEMA, "unexpected direct-edit request schema")
    require(request.get("units") == "mm", "only mm direct-edit requests are supported")
    request_id = str(request.get("request_id") or "").strip()
    ole_id = str(request.get("ole_id") or "").strip()
    require(bool(request_id) and bool(ole_id), "request identity fields must be non-empty")
    revision = int(request.get("revision", 0))
    require(revision >= 1, "revision must be >= 1")
    require(not contains_ordinal(request), "persistent topology ordinal is prohibited")

    source = request.get("source") or {}
    require(source.get("authority") == "CAD_DIRECT_EDIT_INTENT", "invalid source authority")
    require(source.get("intent_schema") == "OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1", "invalid intent schema")
    require(re.fullmatch(r"[0-9a-fA-F]{64}", str(source.get("intent_sha256") or "")) is not None, "invalid intent SHA256")
    require(source.get("required_kernel") == REQUIRED_KERNEL, "direct edit requires FreeCAD/OCCT authority")
    master_fcstd = Path(str(source.get("master_locator") or ""))
    require(str(master_fcstd), "missing master locator")
    require(master_fcstd.suffix.lower() == ".fcstd", "bounded master locator must resolve to FCStd")
    master_brep = master_fcstd.with_suffix(".brep")

    operation = request.get("operation") or {}
    require(operation.get("kind") == OPERATION, "only FACE_NORMAL_MOVE is supported")
    distance_mm = finite(operation.get("distance_mm"), "operation.distance_mm")
    require(abs(distance_mm) > 1e-9, "FACE_NORMAL_MOVE distance must be non-zero")

    selector = request.get("target_selector") or {}
    require(selector.get("kind") == "SEMANTIC_FACE_DESCRIPTOR", "semantic face descriptor required")
    require(selector.get("resolution_policy") == "SEMANTIC_REBIND_FAIL_CLOSED", "fail-closed rebind required")
    require(selector.get("ambiguous_result") == "HOLD", "ambiguous resolution must HOLD")
    require(selector.get("missing_result") == "HOLD", "missing resolution must HOLD")
    require(set(selector.get("prohibited_persistence") or []) == PROHIBITED, "topology persistence boundary mismatch")
    descriptor = selector.get("descriptor") or {}
    require(descriptor.get("selector_semantics") == "BLENDER_SELECTED_DISPLAY_FACE_INTENT", "unsupported selector semantics")
    normal = vector3(descriptor.get("normal_local"), "descriptor.normal_local")
    length = math.sqrt(sum(v * v for v in normal))
    require(length > 1e-9, "descriptor normal must be non-zero")
    normal = [v / length for v in normal]
    require(abs(normal[0]) <= 1e-6 and abs(normal[1]) <= 1e-6 and normal[2] > 0.999999, "first execution slice requires +Z planar face")
    center = vector3(descriptor.get("center_local_mm"), "descriptor.center_local_mm")
    area = finite(descriptor.get("area_mm2"), "descriptor.area_mm2")
    require(area > 0.0, "descriptor area must be positive")
    edge_count = int(descriptor.get("edge_count", 0))
    require(edge_count == 4, "first execution slice requires a four-edge planar face")
    edge_lengths = descriptor.get("edge_lengths_mm") or []
    require(len(edge_lengths) == edge_count, "descriptor edge lengths mismatch")
    edge_lengths = sorted(finite(v, "descriptor.edge_lengths_mm") for v in edge_lengths)
    require(all(v > 0.0 for v in edge_lengths), "descriptor edge lengths must be positive")
    bbox = descriptor.get("bbox_local_mm") or {}
    bbox_min = vector3(bbox.get("min"), "descriptor.bbox.min")
    bbox_max = vector3(bbox.get("max"), "descriptor.bbox.max")
    require(all(lo <= hi for lo, hi in zip(bbox_min, bbox_max)), "descriptor bbox is inverted")

    authority = request.get("authority") or {}
    require(authority.get("master_type") == "CAD_NATIVE", "master type must remain CAD_NATIVE")
    require(authority.get("geometry_authority") == REQUIRED_KERNEL, "geometry authority mismatch")
    require(authority.get("blender_role") == "DISPLAY_DERIVATIVE_ONLY", "Blender must remain display-only")
    require(authority.get("display_mutation") == "NONE", "request may not authorize display mutation")
    require(authority.get("execution_state") == "NOT_EXECUTED", "incoming request must be NOT_EXECUTED")

    return {
        "request_id": request_id,
        "ole_id": ole_id,
        "revision": revision,
        "distance_mm": distance_mm,
        "master_fcstd": master_fcstd,
        "master_brep": master_brep,
        "descriptor": {
            "normal": normal,
            "center_mm": center,
            "area_mm2": area,
            "edge_count": edge_count,
            "edge_lengths_mm": edge_lengths,
            "bbox_min_mm": bbox_min,
            "bbox_max_mm": bbox_max,
        },
        "request_sha256": payload_sha256(request),
    }


def face_normal(face):
    u0, u1, v0, v1 = face.ParameterRange
    normal = face.normalAt((u0 + u1) * 0.5, (v0 + v1) * 0.5)
    normal.normalize()
    return normal


def descriptor(face) -> dict:
    normal = face_normal(face)
    center = face.CenterOfMass
    bbox = face.BoundBox
    return {
        "normal": [normal.x, normal.y, normal.z],
        "center_mm": [center.x, center.y, center.z],
        "area_mm2": face.Area,
        "edge_count": len(face.Edges),
        "edge_lengths_mm": sorted(edge.Length for edge in face.Edges),
        "bbox_min_mm": [bbox.XMin, bbox.YMin, bbox.ZMin],
        "bbox_max_mm": [bbox.XMax, bbox.YMax, bbox.ZMax],
    }


def close_value(actual: float, expected: float) -> bool:
    tolerance = max(MATCH_TOL_MM, abs(expected) * MATCH_REL)
    return abs(actual - expected) <= tolerance


def descriptor_matches(actual: dict, target: dict) -> bool:
    dot = sum(a * b for a, b in zip(actual["normal"], target["normal"]))
    if dot < 0.999999:
        return False
    if not all(close_value(a, b) for a, b in zip(actual["center_mm"], target["center_mm"])):
        return False
    if not close_value(actual["area_mm2"], target["area_mm2"]):
        return False
    if actual["edge_count"] != target["edge_count"]:
        return False
    if not all(close_value(a, b) for a, b in zip(actual["edge_lengths_mm"], target["edge_lengths_mm"])):
        return False
    if not all(close_value(a, b) for a, b in zip(actual["bbox_min_mm"], target["bbox_min_mm"])):
        return False
    if not all(close_value(a, b) for a, b in zip(actual["bbox_max_mm"], target["bbox_max_mm"])):
        return False
    return True


def resolution_signature(desc: dict) -> str:
    normalized = {
        key: ([round(float(v), 9) for v in value] if isinstance(value, list) else round(float(value), 9) if isinstance(value, (int, float)) else value)
        for key, value in desc.items()
    }
    return payload_sha256(normalized)


def resolve_face(shape, target: dict) -> tuple[object | None, dict]:
    candidates = []
    for face in shape.Faces:
        try:
            actual = descriptor(face)
        except Exception:
            continue
        if descriptor_matches(actual, target):
            candidates.append((face, actual, resolution_signature(actual)))
    if not candidates:
        return None, {"state": "MISSING_HOLD", "candidate_count": 0, "candidate_signatures": []}
    if len(candidates) > 1:
        return None, {
            "state": "AMBIGUOUS_HOLD",
            "candidate_count": len(candidates),
            "candidate_signatures": sorted(item[2] for item in candidates),
        }
    face, actual, signature = candidates[0]
    return face, {
        "state": "RESOLVED_UNIQUE",
        "candidate_count": 1,
        "resolved_signature": signature,
        "resolved_descriptor": actual,
    }


def same_point(a, b) -> bool:
    return (a - b).Length <= TOL


def make_face(points, expected_normal):
    face = Part.Face(Part.makePolygon(points + [points[0]]))
    if face_normal(face).dot(expected_normal) < 0:
        face = face.reversed()
    return face


def adjacent_side(shape, p0, p1, top, bottom):
    found = []
    for face in shape.Faces:
        if face.isSame(top) or face.isSame(bottom):
            continue
        points = [vertex.Point for vertex in face.Vertexes]
        if any(same_point(v, p0) for v in points) and any(same_point(v, p1) for v in points):
            found.append(face)
    require(len(found) == 1, "bounded prism requires one side face per top edge")
    return found[0]


def normalize_replaced(shape):
    candidate = shape.copy()
    try:
        candidate.sewShape(1e-7)
    except TypeError:
        candidate.sewShape()
    try:
        candidate.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        candidate.fix()
    candidate = candidate.removeSplitter()
    if candidate.isValid() and len(candidate.Solids) == 1:
        return candidate
    shell = Part.makeShell(candidate.Faces)
    try:
        shell.sewShape(1e-7)
    except TypeError:
        shell.sewShape()
    try:
        shell.fix(1e-7, 1e-7, 1e-7)
    except TypeError:
        shell.fix()
    return Part.makeSolid(shell).removeSplitter()


def select_bottom(shape):
    zmin = shape.BoundBox.ZMin
    found = []
    for face in shape.Faces:
        bbox = face.BoundBox
        if bbox.ZLength > TOL or abs(bbox.ZMin - zmin) > TOL:
            continue
        normal = face_normal(face)
        if normal.z < -0.999999:
            found.append(face)
    require(len(found) == 1, "bounded prism requires one -Z bottom face")
    return found[0]


def move_resolved_top_face(shape, top, delta_mm: float):
    require(shape.isValid() and len(shape.Solids) == 1, "bounded direct edit requires one valid source solid")
    require(len(shape.Faces) == 6, "first execution slice requires an unmodified six-face rectangular prism")
    bbox = shape.BoundBox
    width, depth, height = bbox.XLength, bbox.YLength, bbox.ZLength
    require(width > TOL and depth > TOL and height > TOL, "source prism dimensions must be positive")
    require(abs(shape.Volume - width * depth * height) <= max(1e-4, shape.Volume * 1e-6), "source is outside rectangular-prism volume envelope")
    require(delta_mm > -height + TOL, "face move would collapse or invert the solid")
    require(top.BoundBox.ZLength <= TOL and abs(top.BoundBox.ZMax - bbox.ZMax) <= TOL, "resolved face is not the bounded top face")
    normal = face_normal(top)
    require(abs(normal.x) <= 1e-6 and abs(normal.y) <= 1e-6 and normal.z > 0.999999, "resolved face must have +Z normal")
    bottom = select_bottom(shape)
    points = [vertex.Point for vertex in top.OuterWire.OrderedVertexes]
    require(len(points) == 4, "bounded top face must have four vertices")
    area2 = sum(points[i].x * points[(i + 1) % 4].y - points[(i + 1) % 4].x * points[i].y for i in range(4))
    if area2 < 0:
        points.reverse()
    bottom_points = [App.Vector(point.x, point.y, bbox.ZMin) for point in points]
    moved_points = [point + normal * delta_mm for point in points]
    moved_top = make_face(moved_points, normal)
    replacements = [(top, moved_top)]
    for index in range(4):
        p0, p1 = points[index], points[(index + 1) % 4]
        q0, q1 = moved_points[index], moved_points[(index + 1) % 4]
        b0, b1 = bottom_points[index], bottom_points[(index + 1) % 4]
        old_side = adjacent_side(shape, p0, p1, top, bottom)
        replacements.append((old_side, make_face([b0, b1, q1, q0], face_normal(old_side))))
    require(len(replacements) == 5, "bounded face move must replace top plus four adjacent faces")
    replaced = shape.replaceShape(replacements)
    require(not replaced.isNull(), "replaceShape returned null")
    edited = normalize_replaced(replaced)
    require(edited.isValid() and len(edited.Solids) == 1, "edited shape must be one valid solid")
    expected_height = height + delta_mm
    require(close_value(edited.BoundBox.XLength, width), "edited X dimension drift")
    require(close_value(edited.BoundBox.YLength, depth), "edited Y dimension drift")
    require(close_value(edited.BoundBox.ZLength, expected_height), "edited Z dimension mismatch")
    expected_volume = width * depth * expected_height
    require(abs(edited.Volume - expected_volume) <= max(1e-4, expected_volume * 1e-6), "edited prism volume mismatch")
    return edited


def metrics(shape) -> dict:
    return {
        "bbox_mm": [shape.BoundBox.XLength, shape.BoundBox.YLength, shape.BoundBox.ZLength],
        "volume_mm3": shape.Volume,
        "solid_count": len(shape.Solids),
    }


def empty_artifact() -> dict:
    return {"path": "", "sha256": "0" * 64}


def write_hold(request: dict, validated: dict, shape, resolution: dict) -> None:
    source_metrics = metrics(shape)
    response = {
        "schema": RESPONSE_SCHEMA,
        "request_id": validated["request_id"],
        "ole_id": validated["ole_id"],
        "revision": validated["revision"],
        "status": "HOLD",
        "kernel": {"name": "FreeCAD", "version": ".".join(str(x) for x in App.Version()[:3]), "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN")},
        "request_sha256": validated["request_sha256"],
        "source_master": {
            "fcstd": {"path": str(validated["master_fcstd"]), "sha256": file_sha256(validated["master_fcstd"])},
            "brep": {"path": str(validated["master_brep"]), "sha256": file_sha256(validated["master_brep"])},
        },
        "resolution": resolution,
        "operation": {"kind": OPERATION, "distance_mm": validated["distance_mm"], "execution_state": "NOT_EXECUTED"},
        "authoritative": {"master_type": "CAD_NATIVE", "geometry_authority": REQUIRED_KERNEL, "fcstd": empty_artifact(), "step": empty_artifact(), "brep": empty_artifact()},
        "display_derivative": empty_artifact(),
        "measurements": {"units": "mm", "source_bbox_mm": source_metrics["bbox_mm"], "source_volume_mm3": source_metrics["volume_mm3"], "result_bbox_mm": [0.0, 0.0, 0.0], "result_volume_mm3": 0.0, "result_solid_count": 0},
        "error": None,
        "non_claims": ["general_brep_push_pull", "persistent_topological_naming", "P0_B_DIRECT_BREP_PASS", "engineering_approval", "manufacturing_release", "field_truth"],
    }
    RESPONSE_PATH.write_bytes(canonical_bytes(response))
    print("OLEANDER_CAD_DIRECT_EDIT_HOLD=" + json.dumps(response, sort_keys=True))


def write_fail(request: dict | None, error: Exception) -> None:
    request = request or {}
    response = {
        "schema": RESPONSE_SCHEMA,
        "request_id": str(request.get("request_id") or "UNKNOWN"),
        "ole_id": str(request.get("ole_id") or "UNKNOWN"),
        "revision": int(request.get("revision", 1) or 1),
        "status": "FAIL",
        "kernel": {"name": "FreeCAD", "version": ".".join(str(x) for x in App.Version()[:3]), "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN")},
        "request_sha256": payload_sha256(request) if request else "0" * 64,
        "source_master": {"fcstd": empty_artifact(), "brep": empty_artifact()},
        "resolution": {"state": "ERROR", "candidate_count": 0, "candidate_signatures": []},
        "operation": {"kind": str((request.get("operation") or {}).get("kind") or OPERATION), "distance_mm": float((request.get("operation") or {}).get("distance_mm") or 0.0), "execution_state": "NOT_EXECUTED"},
        "authoritative": {"master_type": "CAD_NATIVE", "geometry_authority": REQUIRED_KERNEL, "fcstd": empty_artifact(), "step": empty_artifact(), "brep": empty_artifact()},
        "display_derivative": empty_artifact(),
        "measurements": {"units": "mm", "source_bbox_mm": [0.0, 0.0, 0.0], "source_volume_mm3": 0.0, "result_bbox_mm": [0.0, 0.0, 0.0], "result_volume_mm3": 0.0, "result_solid_count": 0},
        "error": str(error),
        "non_claims": ["general_brep_push_pull", "persistent_topological_naming", "P0_B_DIRECT_BREP_PASS"],
    }
    RESPONSE_PATH.write_bytes(canonical_bytes(response))
    print("OLEANDER_CAD_DIRECT_EDIT_FAIL=" + json.dumps(response, sort_keys=True))


def main() -> None:
    request = None
    try:
        request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
        validated = validate_request(request)
        require(validated["master_fcstd"].is_file(), "authoritative FCStd master is missing")
        require(validated["master_brep"].is_file(), "authoritative BREP master is missing")
        shape = Part.Shape()
        shape.read(str(validated["master_brep"]))
        require(not shape.isNull(), "authoritative BREP could not be read")

        face, resolution = resolve_face(shape, validated["descriptor"])
        if face is None:
            write_hold(request, validated, shape, resolution)
            return

        source_metrics = metrics(shape)
        edited = move_resolved_top_face(shape, face, validated["distance_mm"])
        result_metrics = metrics(edited)
        stem = f"{validated['ole_id']}_R{validated['revision']:03d}"
        fcstd = OUT / f"{stem}.FCStd"
        step = OUT / f"{stem}.step"
        brep = OUT / f"{stem}.brep"

        doc = App.newDocument(f"OLEANDER_DIRECT_{validated['revision']:03d}")
        obj = doc.addObject("Part::Feature", "OLE_CAD_DIRECT_MASTER")
        obj.Label = stem
        obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
        obj.OLE_ID = validated["ole_id"]
        obj.addProperty("App::PropertyInteger", "OLE_Revision", "OLEANDER")
        obj.OLE_Revision = validated["revision"]
        obj.addProperty("App::PropertyString", "OLE_RequestSHA256", "OLEANDER")
        obj.OLE_RequestSHA256 = validated["request_sha256"]
        obj.addProperty("App::PropertyString", "OLE_Operation", "OLEANDER")
        obj.OLE_Operation = OPERATION
        obj.addProperty("App::PropertyFloat", "OLE_DistanceMM", "OLEANDER")
        obj.OLE_DistanceMM = validated["distance_mm"]
        obj.addProperty("App::PropertyString", "OLE_ResolutionSignature", "OLEANDER")
        obj.OLE_ResolutionSignature = resolution["resolved_signature"]
        obj.Shape = edited
        doc.recompute()
        doc.saveAs(str(fcstd))
        edited.exportStep(str(step))
        edited.exportBrep(str(brep))
        require(fcstd.is_file() and fcstd.stat().st_size > 0, "direct-edit FCStd not saved")
        require(step.is_file() and step.stat().st_size > 0, "direct-edit STEP not exported")
        require(brep.is_file() and brep.stat().st_size > 0, "direct-edit BREP not exported")

        step_shape = Part.Shape()
        step_shape.read(str(step))
        require(step_shape.isValid() and len(step_shape.Solids) == 1, "STEP round-trip is not one valid solid")
        require(abs(step_shape.Volume - edited.Volume) <= max(1e-4, edited.Volume * 1e-6), "STEP round-trip volume drift")
        vertices, facets = step_shape.tessellate(0.25)
        require(bool(vertices) and bool(facets), "direct-edit display tessellation is empty")
        display = {
            "schema": DISPLAY_SCHEMA,
            "master_type": "CAD_NATIVE",
            "geometry_authority": REQUIRED_KERNEL,
            "display_authority": "DISPLAY_DERIVATIVE_ONLY",
            "units": "mm",
            "request_id": validated["request_id"],
            "request_revision": validated["revision"],
            "request_sha256": validated["request_sha256"],
            "source_master": str(fcstd),
            "source_step": str(step),
            "source_step_sha256": file_sha256(step),
            "vertices_mm": [[v.x, v.y, v.z] for v in vertices],
            "triangles": [list(facet) for facet in facets],
            "source_bbox": {"x_length_mm": edited.BoundBox.XLength, "y_length_mm": edited.BoundBox.YLength, "z_length_mm": edited.BoundBox.ZLength},
            "source_volume_mm3": edited.Volume,
        }
        DISPLAY_PATH.write_bytes(canonical_bytes(display))

        response = {
            "schema": RESPONSE_SCHEMA,
            "request_id": validated["request_id"],
            "ole_id": validated["ole_id"],
            "revision": validated["revision"],
            "status": "PASS",
            "kernel": {"name": "FreeCAD", "version": ".".join(str(x) for x in App.Version()[:3]), "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN")},
            "request_sha256": validated["request_sha256"],
            "source_master": {
                "fcstd": {"path": str(validated["master_fcstd"]), "sha256": file_sha256(validated["master_fcstd"])},
                "brep": {"path": str(validated["master_brep"]), "sha256": file_sha256(validated["master_brep"])},
            },
            "resolution": resolution,
            "operation": {"kind": OPERATION, "distance_mm": validated["distance_mm"], "execution_state": "EXECUTED"},
            "authoritative": {
                "master_type": "CAD_NATIVE",
                "geometry_authority": REQUIRED_KERNEL,
                "fcstd": {"path": str(fcstd), "sha256": file_sha256(fcstd)},
                "step": {"path": str(step), "sha256": file_sha256(step)},
                "brep": {"path": str(brep), "sha256": file_sha256(brep)},
            },
            "display_derivative": {"path": str(DISPLAY_PATH), "sha256": file_sha256(DISPLAY_PATH)},
            "measurements": {
                "units": "mm",
                "source_bbox_mm": source_metrics["bbox_mm"],
                "source_volume_mm3": source_metrics["volume_mm3"],
                "result_bbox_mm": result_metrics["bbox_mm"],
                "result_volume_mm3": result_metrics["volume_mm3"],
                "result_solid_count": result_metrics["solid_count"],
            },
            "error": None,
            "non_claims": ["general_brep_push_pull", "persistent_topological_naming", "P0_B_DIRECT_BREP_PASS", "engineering_approval", "manufacturing_release", "field_truth"],
        }
        RESPONSE_PATH.write_bytes(canonical_bytes(response))
        print("OLEANDER_CAD_DIRECT_EDIT_RESPONSE=" + json.dumps(response, sort_keys=True))
    except Exception as exc:
        write_fail(request, exc)
        raise


main()
