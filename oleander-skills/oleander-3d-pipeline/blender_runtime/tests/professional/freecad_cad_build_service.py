"""Bounded FreeCAD/OCCT implementation of OLEANDER_CAD_BUILD_REQUEST_v0.1.

This executable CI/service module is run by FreeCADCmd. It creates an
AUTHORITATIVE CAD_NATIVE B-Rep from a solved polyline sketch intent request and
emits a response plus a typed triangulated Blender display derivative.

This is intentionally bounded: polyline profile + linear extrude + through holes.
It is a professional integration foundation, not a full PartDesign replacement.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import FreeCAD as App
import Part

REQUEST_SCHEMA = "OLEANDER_CAD_BUILD_REQUEST_v0.1"
RESPONSE_SCHEMA = "OLEANDER_CAD_BUILD_RESPONSE_v0.1"
DISPLAY_SCHEMA = "OLEANDER_CAD_DISPLAY_DERIVATIVE_v0.1"

REQUEST_PATH = Path(os.environ["OLEANDER_CAD_BUILD_REQUEST"])
OUT = Path(os.environ["OLEANDER_CAD_BUILD_DIR"])
OUT.mkdir(parents=True, exist_ok=True)
RESPONSE_PATH = OUT / "cad_build_response.json"
DISPLAY_PATH = OUT / "cad_display_derivative.json"


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


def validate_request(request: dict) -> None:
    require(request.get("schema") == REQUEST_SCHEMA, "unexpected request schema")
    require(request.get("units") == "mm", "only mm requests are supported")
    require(bool(request.get("request_id")), "missing request_id")
    require(bool(request.get("ole_id")), "missing ole_id")
    require(int(request.get("revision", 0)) >= 1, "invalid revision")
    source = request.get("source") or {}
    require(source.get("authority") == "SOLVED_SKETCH_INTENT", "invalid source authority")
    profile = request.get("profile") or {}
    require(profile.get("kind") == "POLYLINE", "only POLYLINE profiles are supported")
    require(profile.get("closed") is True, "profile must be closed")
    points = profile.get("points_mm") or []
    require(len(points) >= 3, "profile requires at least three points")
    for point in points:
        require(isinstance(point, list) and len(point) == 2, "invalid 2D profile point")
    features = request.get("features") or []
    require(features and features[0].get("kind") == "EXTRUDE", "first feature must be EXTRUDE")
    require(float(features[0].get("depth_mm", 0.0)) > 0.0, "extrude depth must be positive")


def profile_face(points_mm: list[list[float]]):
    points = [App.Vector(float(p[0]), float(p[1]), 0.0) for p in points_mm]
    edges = []
    for index, start in enumerate(points):
        end = points[(index + 1) % len(points)]
        require((end - start).Length > 1e-9, "profile contains zero-length edge")
        edges.append(Part.makeLine(start, end))
    wire = Part.Wire(edges)
    require(wire.isClosed(), "profile wire did not close")
    require(wire.isValid(), "profile wire invalid")
    face = Part.Face(wire)
    require(face.isValid(), "profile face invalid")
    require(face.Area > 0.0, "profile face has zero area")
    return face


def normalize_single_solid(shape, label: str):
    require(shape.isValid(), f"{label}: invalid shape")
    require(len(shape.Solids) == 1, f"{label}: expected one solid, got {len(shape.Solids)}")
    solid = shape.Solids[0]
    require(solid.isValid(), f"{label}: normalized solid invalid")
    require(solid.ShapeType == "Solid", f"{label}: normalized result is not Solid")
    require(solid.Volume > 0.0, f"{label}: non-positive volume")
    return solid


def build_shape(request: dict):
    profile = request["profile"]
    features = request["features"]
    face = profile_face(profile["points_mm"])
    depth = float(features[0]["depth_mm"])
    current = normalize_single_solid(face.extrude(App.Vector(0.0, 0.0, depth)), "extrude")

    for feature in features[1:]:
        kind = feature.get("kind")
        if kind != "THROUGH_HOLE":
            raise ValueError(f"unsupported feature kind: {kind}")
        center = feature["center_mm"]
        radius = float(feature["radius_mm"])
        require(radius > 0.0, "hole radius must be positive")
        cutter = Part.makeCylinder(
            radius,
            depth + 2.0,
            App.Vector(float(center[0]), float(center[1]), -1.0),
        )
        current = normalize_single_solid(
            current.cut(cutter).removeSplitter(),
            f"boolean {feature.get('feature_id')}",
        )
    return current


def write_fail_response(request: dict | None, error: Exception) -> None:
    request = request or {}
    response = {
        "schema": RESPONSE_SCHEMA,
        "request_id": str(request.get("request_id", "UNKNOWN")),
        "ole_id": str(request.get("ole_id", "UNKNOWN")),
        "revision": int(request.get("revision", 1) or 1),
        "status": "FAIL",
        "kernel": {
            "name": "FreeCAD",
            "version": ".".join(str(x) for x in App.Version()[:3]),
            "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN"),
        },
        "request_sha256": payload_sha256(request) if request else "0" * 64,
        "authoritative": {
            "master_type": "CAD_NATIVE",
            "geometry_authority": "FREECAD_OCCT_BREP",
            "fcstd": {"path": "", "sha256": "0" * 64},
            "step": {"path": "", "sha256": "0" * 64},
            "brep": {"path": "", "sha256": "0" * 64},
        },
        "display_derivative": {"path": "", "sha256": "0" * 64},
        "measurements": {
            "units": "mm",
            "bbox_mm": [0.0, 0.0, 0.0],
            "volume_mm3": 0.0,
            "solid_count": 0,
        },
        "error": str(error),
    }
    RESPONSE_PATH.write_bytes(canonical_bytes(response))
    print("OLEANDER_CAD_BUILD_FAIL=" + json.dumps(response, sort_keys=True))


def main() -> None:
    request = None
    try:
        request = json.loads(REQUEST_PATH.read_text(encoding="utf-8"))
        validate_request(request)
        request_sha = payload_sha256(request)
        shape = build_shape(request)

        stem = f"{request['ole_id']}_R{int(request['revision']):03d}"
        fcstd = OUT / f"{stem}.FCStd"
        step = OUT / f"{stem}.step"
        brep = OUT / f"{stem}.brep"

        doc = App.newDocument(f"OLEANDER_{stem}")
        obj = doc.addObject("Part::Feature", "OLE_CAD_MASTER")
        obj.Label = stem
        obj.addProperty("App::PropertyString", "OLE_ID", "OLEANDER")
        obj.OLE_ID = request["ole_id"]
        obj.addProperty("App::PropertyInteger", "OLE_Revision", "OLEANDER")
        obj.OLE_Revision = int(request["revision"])
        obj.addProperty("App::PropertyString", "OLE_RequestSHA256", "OLEANDER")
        obj.OLE_RequestSHA256 = request_sha
        obj.Shape = shape
        doc.recompute()
        doc.saveAs(str(fcstd))

        shape.exportStep(str(step))
        shape.exportBrep(str(brep))
        require(fcstd.exists() and fcstd.stat().st_size > 0, "FCStd master not saved")
        require(step.exists() and step.stat().st_size > 0, "STEP not exported")
        require(brep.exists() and brep.stat().st_size > 0, "BREP not exported")

        step_shape = Part.Shape()
        step_shape.read(str(step))
        step_solid = normalize_single_solid(step_shape, "STEP round-trip")
        require(abs(step_solid.Volume - shape.Volume) <= max(1e-4, shape.Volume * 1e-6), "STEP volume drift")

        vertices, facets = step_solid.tessellate(0.25)
        require(vertices and facets, "empty display tessellation")
        bbox = shape.BoundBox
        display = {
            "schema": DISPLAY_SCHEMA,
            "source_master": str(fcstd),
            "source_step": str(step),
            "source_step_sha256": file_sha256(step),
            "master_type": "CAD_NATIVE",
            "geometry_authority": "FREECAD_OCCT_BREP",
            "units": "mm",
            "request_id": request["request_id"],
            "request_revision": int(request["revision"]),
            "request_sha256": request_sha,
            "vertices_mm": [[v.x, v.y, v.z] for v in vertices],
            "triangles": [list(face) for face in facets],
            "source_bbox": {
                "x_length_mm": bbox.XLength,
                "y_length_mm": bbox.YLength,
                "z_length_mm": bbox.ZLength,
            },
            "source_volume_mm3": shape.Volume,
        }
        DISPLAY_PATH.write_bytes(canonical_bytes(display))

        response = {
            "schema": RESPONSE_SCHEMA,
            "request_id": request["request_id"],
            "ole_id": request["ole_id"],
            "revision": int(request["revision"]),
            "status": "PASS",
            "kernel": {
                "name": "FreeCAD",
                "version": ".".join(str(x) for x in App.Version()[:3]),
                "occ_version": getattr(Part, "OCC_VERSION", "UNKNOWN"),
            },
            "request_sha256": request_sha,
            "authoritative": {
                "master_type": "CAD_NATIVE",
                "geometry_authority": "FREECAD_OCCT_BREP",
                "fcstd": {"path": str(fcstd), "sha256": file_sha256(fcstd)},
                "step": {"path": str(step), "sha256": file_sha256(step)},
                "brep": {"path": str(brep), "sha256": file_sha256(brep)},
            },
            "display_derivative": {"path": str(DISPLAY_PATH), "sha256": file_sha256(DISPLAY_PATH)},
            "measurements": {
                "units": "mm",
                "bbox_mm": [bbox.XLength, bbox.YLength, bbox.ZLength],
                "volume_mm3": shape.Volume,
                "solid_count": 1,
            },
            "error": None,
        }
        RESPONSE_PATH.write_bytes(canonical_bytes(response))
        print("OLEANDER_CAD_BUILD_RESPONSE=" + json.dumps(response, sort_keys=True))
    except Exception as exc:
        write_fail_response(request, exc)
        raise


main()
