"""Governed Blender-side adapter for authoritative CAD process sidecars.

This candidate module remains outside the installed OLEANDER Blender Runtime core
until its dedicated professional integration workflow is validated. It does not
implement a B-Rep kernel. It serializes solved sketch intent into a deterministic
CAD build request, fingerprints that request, binds an external sidecar response
to a Blender display derivative, and marks the display stale when upstream CAD
intent changes.

Authority boundary:
- request source: SOLVED_SKETCH_INTENT
- CAD master: external FREECAD_OCCT_BREP
- Blender object: DISPLAY_DERIVATIVE_ONLY
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable, Sequence

import bpy

REQUEST_SCHEMA = "OLEANDER_CAD_BUILD_REQUEST_v0.1"
RESPONSE_SCHEMA = "OLEANDER_CAD_BUILD_RESPONSE_v0.1"
DISPLAY_SCHEMA = "OLEANDER_CAD_DISPLAY_DERIVATIVE_v0.1"


class CADSidecarContractError(ValueError):
    pass


def _canonical_bytes(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def payload_sha256(payload: dict) -> str:
    return hashlib.sha256(_canonical_bytes(payload)).hexdigest()


def file_sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _point2(value: Sequence[float]) -> list[float]:
    if len(value) != 2:
        raise CADSidecarContractError("profile points must have exactly two coordinates")
    return [float(value[0]), float(value[1])]


def build_request(*, request_id: str, ole_id: str, revision: int, editable_source: str, solver: str, solver_state: str, profile_points_mm: Iterable[Sequence[float]], extrusion_depth_mm: float, holes: Iterable[dict] = ()) -> dict:
    if not request_id or not ole_id or not editable_source or not solver:
        raise CADSidecarContractError("request identity/source fields must be non-empty")
    if int(revision) < 1:
        raise CADSidecarContractError("revision must be >= 1")
    if solver_state not in {"OK", "FULLY_CONSTRAINED", "UNDER_CONSTRAINED"}:
        raise CADSidecarContractError(f"unsupported solver_state: {solver_state}")
    points = [_point2(point) for point in profile_points_mm]
    if len(points) < 3:
        raise CADSidecarContractError("closed CAD profile requires at least three points")
    if float(extrusion_depth_mm) <= 0.0:
        raise CADSidecarContractError("extrusion depth must be positive")
    features = [{"feature_id": f"{ole_id}::CAD-F001", "kind": "EXTRUDE", "depth_mm": float(extrusion_depth_mm)}]
    for index, hole in enumerate(holes, start=2):
        center = _point2(hole["center_mm"])
        radius = float(hole["radius_mm"])
        if radius <= 0.0:
            raise CADSidecarContractError("hole radius must be positive")
        features.append({"feature_id": f"{ole_id}::CAD-F{index:03d}", "kind": "THROUGH_HOLE", "center_mm": center, "radius_mm": radius, "through_all": True})
    return {
        "schema": REQUEST_SCHEMA,
        "request_id": request_id,
        "ole_id": ole_id,
        "revision": int(revision),
        "units": "mm",
        "source": {"solver": solver, "solver_state": solver_state, "editable_source": editable_source, "authority": "SOLVED_SKETCH_INTENT"},
        "profile": {"kind": "POLYLINE", "closed": True, "points_mm": points},
        "features": features,
    }


def write_request(path: str | Path, request: dict) -> str:
    if request.get("schema") != REQUEST_SCHEMA:
        raise CADSidecarContractError("unexpected CAD request schema")
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(request))
    return file_sha256(path)


def load_response(path: str | Path) -> dict:
    response = json.loads(Path(path).read_text(encoding="utf-8"))
    if response.get("schema") != RESPONSE_SCHEMA:
        raise CADSidecarContractError("unexpected CAD response schema")
    if response.get("status") != "PASS":
        raise CADSidecarContractError(f"CAD sidecar response is not PASS: {response.get('error') or 'unknown error'}")
    authority = response.get("authoritative") or {}
    if authority.get("master_type") != "CAD_NATIVE":
        raise CADSidecarContractError("sidecar response lost CAD_NATIVE master type")
    if authority.get("geometry_authority") != "FREECAD_OCCT_BREP":
        raise CADSidecarContractError("sidecar response lost FreeCAD/OCCT authority")
    return response


def bind_display_derivative(*, response: dict, display_payload: dict, collection=None, existing_object=None):
    if response.get("schema") != RESPONSE_SCHEMA or response.get("status") != "PASS":
        raise CADSidecarContractError("cannot bind non-PASS CAD response")
    if display_payload.get("schema") != DISPLAY_SCHEMA:
        raise CADSidecarContractError("unexpected CAD display derivative schema")
    if display_payload.get("master_type") != "CAD_NATIVE" or display_payload.get("geometry_authority") != "FREECAD_OCCT_BREP":
        raise CADSidecarContractError("display payload lost authoritative CAD provenance")
    if display_payload.get("units") != "mm":
        raise CADSidecarContractError("only mm CAD display payloads are supported")
    vertices = display_payload.get("vertices_mm") or []
    triangles = display_payload.get("triangles") or []
    if not vertices or not triangles:
        raise CADSidecarContractError("CAD display derivative is empty")
    mesh = bpy.data.meshes.new(f"{response['ole_id']}_CAD_DISPLAY_MESH")
    mesh.from_pydata(vertices, [], triangles)
    mesh.update()
    if existing_object is None:
        obj = bpy.data.objects.new(f"{response['ole_id']}_CAD_DISPLAY", mesh)
        (collection or bpy.context.collection).objects.link(obj)
    else:
        obj = existing_object
        old_mesh = obj.data if getattr(obj, "type", None) == "MESH" else None
        obj.data = mesh
        if old_mesh is not None and old_mesh.users == 0:
            bpy.data.meshes.remove(old_mesh)
    authoritative = response["authoritative"]
    obj["ole_id"] = response["ole_id"]
    obj["cad_request_id"] = response["request_id"]
    obj["cad_request_revision"] = int(response["revision"])
    obj["cad_request_sha256"] = response["request_sha256"]
    obj["master_type"] = "CAD_NATIVE"
    obj["master_locator"] = authoritative["fcstd"]["path"]
    obj["source_step"] = authoritative["step"]["path"]
    obj["source_step_sha256"] = authoritative["step"]["sha256"]
    obj["source_brep"] = authoritative["brep"]["path"]
    obj["source_brep_sha256"] = authoritative["brep"]["sha256"]
    obj["geometry_authority"] = "DISPLAY_DERIVATIVE_ONLY"
    obj["authoritative_geometry_kernel"] = "FREECAD_OCCT_BREP"
    obj["units_contract"] = "mm"
    obj["cad_stale"] = False
    if hasattr(obj, "oleander"):
        obj.oleander.stale = False
    return obj


def update_stale_state(obj, current_request: dict) -> bool:
    current_sha = payload_sha256(current_request)
    bound_sha = str(obj.get("cad_request_sha256", ""))
    stale = not bound_sha or bound_sha != current_sha
    obj["cad_stale"] = bool(stale)
    if hasattr(obj, "oleander"):
        obj.oleander.stale = bool(stale)
    return bool(stale)


def assert_response_matches_request(response: dict, request: dict) -> None:
    if response.get("request_id") != request.get("request_id"):
        raise CADSidecarContractError("CAD response request_id mismatch")
    if response.get("ole_id") != request.get("ole_id"):
        raise CADSidecarContractError("CAD response OLE ID mismatch")
    if int(response.get("revision", -1)) != int(request.get("revision", -2)):
        raise CADSidecarContractError("CAD response revision mismatch")
    if response.get("request_sha256") != payload_sha256(request):
        raise CADSidecarContractError("CAD response request SHA mismatch")
