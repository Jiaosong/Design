"""Governed Blender-side adapter for authoritative CAD process sidecars.

This module is a shared, project-neutral professional backend adapter under the
installed OLEANDER Blender Runtime Current. It does not implement a B-Rep kernel
and does not make Blender mesh geometry authoritative CAD geometry. It serializes
solved sketch intent into deterministic CAD build requests, validates bounded
Direct Face interaction intents into deterministic direct-edit requests, binds
external sidecar responses to Blender display derivatives, and marks display
representations stale when upstream CAD intent changes.

Project profiles may configure routing inputs, but they must not replace this
adapter's authority contract or bypass response/readback validation.

Authority boundary:
- build request source: SOLVED_SKETCH_INTENT
- direct-edit request source: OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1
- CAD master: external FREECAD_OCCT_BREP
- Blender object: DISPLAY_DERIVATIVE_ONLY
- this adapter validates/serializes requests; it does not itself execute B-Rep mutation
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Iterable, Sequence

import bpy

REQUEST_SCHEMA = "OLEANDER_CAD_BUILD_REQUEST_v0.1"
RESPONSE_SCHEMA = "OLEANDER_CAD_BUILD_RESPONSE_v0.1"
DISPLAY_SCHEMA = "OLEANDER_CAD_DISPLAY_DERIVATIVE_v0.1"
DIRECT_EDIT_INTENT_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1"
DIRECT_EDIT_REQUEST_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_REQUEST_v0.1"

DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE = "FACE_NORMAL_MOVE"
DIRECT_EDIT_REQUIRED_KERNEL = "FREECAD_OCCT_BREP"
DIRECT_EDIT_BLENDER_ROLE = "DISPLAY_DERIVATIVE_ONLY"
DIRECT_EDIT_REBIND_POLICY = "SEMANTIC_REBIND_FAIL_CLOSED"
DIRECT_EDIT_HOLD = "HOLD"
DIRECT_EDIT_PROHIBITED_PERSISTENCE = {
    "FaceN",
    "EdgeN",
    "VertexN",
    "subshape_ordinal",
    "polygon_index",
}


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


def _finite_float(value, label: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise CADSidecarContractError(f"{label} must be numeric") from exc
    if not math.isfinite(number):
        raise CADSidecarContractError(f"{label} must be finite")
    return number


def _point2(value: Sequence[float]) -> list[float]:
    if len(value) != 2:
        raise CADSidecarContractError("profile points must have exactly two coordinates")
    return [_finite_float(value[0], "profile x"), _finite_float(value[1], "profile y")]


def _vector(value, size: int, label: str) -> list[float]:
    if not isinstance(value, (list, tuple)) or len(value) != size:
        raise CADSidecarContractError(f"{label} must contain exactly {size} coordinates")
    return [_finite_float(component, f"{label}[{index}]") for index, component in enumerate(value)]


def _contains_forbidden_topology_reference(value) -> bool:
    """Reject persisted topology ordinals anywhere in a direct-edit intent."""
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key) in DIRECT_EDIT_PROHIBITED_PERSISTENCE:
                return True
            if _contains_forbidden_topology_reference(child):
                return True
        return False
    if isinstance(value, (list, tuple)):
        return any(_contains_forbidden_topology_reference(child) for child in value)
    if isinstance(value, str):
        return bool(re.fullmatch(r"(?:Face|Edge|Vertex)\d+", value.strip()))
    return False


def _validate_direct_face_descriptor(target: dict) -> dict:
    if not isinstance(target, dict):
        raise CADSidecarContractError("direct-edit target must be an object")
    if _contains_forbidden_topology_reference(target):
        raise CADSidecarContractError("direct-edit target persists a prohibited topology ordinal")
    if target.get("selector_semantics") != "BLENDER_SELECTED_DISPLAY_FACE_INTENT":
        raise CADSidecarContractError("unsupported direct-edit selector semantics")

    normal = _vector(target.get("normal_local"), 3, "target.normal_local")
    normal_length = math.sqrt(sum(component * component for component in normal))
    if normal_length <= 1e-9:
        raise CADSidecarContractError("direct-edit target normal must be non-zero")
    center = _vector(target.get("center_local_mm"), 3, "target.center_local_mm")
    area = _finite_float(target.get("area_mm2"), "target.area_mm2")
    if area <= 0.0:
        raise CADSidecarContractError("direct-edit target area must be positive")

    try:
        edge_count = int(target.get("edge_count"))
    except (TypeError, ValueError) as exc:
        raise CADSidecarContractError("target.edge_count must be an integer") from exc
    if edge_count < 3:
        raise CADSidecarContractError("direct-edit target must have at least three edges")
    edge_lengths = target.get("edge_lengths_mm")
    if not isinstance(edge_lengths, list) or len(edge_lengths) != edge_count:
        raise CADSidecarContractError("target.edge_lengths_mm must match edge_count")
    normalized_lengths = [_finite_float(value, "target.edge_lengths_mm") for value in edge_lengths]
    if any(value <= 0.0 for value in normalized_lengths):
        raise CADSidecarContractError("target edge lengths must be positive")

    bbox = target.get("bbox_local_mm")
    if not isinstance(bbox, dict):
        raise CADSidecarContractError("target.bbox_local_mm must be an object")
    bbox_min = _vector(bbox.get("min"), 3, "target.bbox_local_mm.min")
    bbox_max = _vector(bbox.get("max"), 3, "target.bbox_local_mm.max")
    if any(low > high for low, high in zip(bbox_min, bbox_max)):
        raise CADSidecarContractError("target bbox min cannot exceed max")

    return {
        "selector_semantics": "BLENDER_SELECTED_DISPLAY_FACE_INTENT",
        "normal_local": normal,
        "center_local_mm": center,
        "area_mm2": area,
        "edge_count": edge_count,
        "edge_lengths_mm": normalized_lengths,
        "bbox_local_mm": {"min": bbox_min, "max": bbox_max},
    }


def validate_direct_edit_intent(intent: dict) -> dict:
    """Validate a bounded Blender Direct Face intent without resolving a CAD face."""
    if not isinstance(intent, dict) or intent.get("schema") != DIRECT_EDIT_INTENT_SCHEMA:
        raise CADSidecarContractError("unexpected CAD direct-edit intent schema")
    if _contains_forbidden_topology_reference(intent.get("target")):
        raise CADSidecarContractError("CAD direct-edit intent contains a prohibited persistent topology reference")

    ole_id = str(intent.get("ole_id") or "").strip()
    if not ole_id:
        raise CADSidecarContractError("CAD direct-edit intent requires a stable OLE ID")
    if intent.get("units") != "mm":
        raise CADSidecarContractError("CAD direct-edit intent currently supports mm only")
    if intent.get("operation") != DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        raise CADSidecarContractError(f"unsupported CAD direct-edit operation: {intent.get('operation')}")

    parameters = intent.get("parameters") or {}
    distance_mm = _finite_float(parameters.get("distance_mm"), "parameters.distance_mm")
    if abs(distance_mm) <= 1e-9:
        raise CADSidecarContractError("FACE_NORMAL_MOVE distance must be non-zero")

    authority = intent.get("authority") or {}
    if authority.get("master_type") != "CAD_NATIVE":
        raise CADSidecarContractError("CAD direct-edit intent lost CAD_NATIVE master type")
    master_locator = str(authority.get("master_locator") or "").strip()
    if not master_locator:
        raise CADSidecarContractError("CAD direct-edit intent requires a governed master locator")
    if authority.get("required_kernel") != DIRECT_EDIT_REQUIRED_KERNEL:
        raise CADSidecarContractError("CAD direct-edit intent must require FreeCAD/OCCT B-Rep authority")
    if authority.get("blender_role") != DIRECT_EDIT_BLENDER_ROLE:
        raise CADSidecarContractError("CAD direct-edit intent must keep Blender as display derivative only")
    if authority.get("display_mutation") != "NONE":
        raise CADSidecarContractError("CAD direct-edit intent may not authorize display-mesh mutation")

    resolution = intent.get("resolution") or {}
    if resolution.get("policy") != DIRECT_EDIT_REBIND_POLICY:
        raise CADSidecarContractError("CAD direct-edit intent must use fail-closed semantic rebind")
    if resolution.get("ambiguous_result") != DIRECT_EDIT_HOLD or resolution.get("missing_result") != DIRECT_EDIT_HOLD:
        raise CADSidecarContractError("ambiguous or missing CAD face resolution must HOLD")
    prohibited = set(resolution.get("prohibited_persistence") or [])
    if not DIRECT_EDIT_PROHIBITED_PERSISTENCE.issubset(prohibited):
        raise CADSidecarContractError("CAD direct-edit intent lost topology-persistence prohibitions")

    target = _validate_direct_face_descriptor(intent.get("target"))
    return {
        "ole_id": ole_id,
        "distance_mm": distance_mm,
        "master_locator": master_locator,
        "target": target,
        "intent_sha256": payload_sha256(intent),
    }


def build_direct_edit_request_from_intent(*, request_id: str, revision: int, intent: dict) -> dict:
    """Convert a validated Blender interaction intent into a deterministic CAD request.

    This function deliberately stops before CAD-face resolution or B-Rep mutation.
    A specialist executor must re-resolve the semantic descriptor against the
    authoritative CAD master and fail closed on ambiguity/missing targets.
    """
    request_id = str(request_id or "").strip()
    if not request_id:
        raise CADSidecarContractError("direct-edit request_id must be non-empty")
    if int(revision) < 1:
        raise CADSidecarContractError("direct-edit revision must be >= 1")
    validated = validate_direct_edit_intent(intent)
    return {
        "schema": DIRECT_EDIT_REQUEST_SCHEMA,
        "request_id": request_id,
        "ole_id": validated["ole_id"],
        "revision": int(revision),
        "units": "mm",
        "source": {
            "authority": "CAD_DIRECT_EDIT_INTENT",
            "intent_schema": DIRECT_EDIT_INTENT_SCHEMA,
            "intent_sha256": validated["intent_sha256"],
            "master_locator": validated["master_locator"],
            "required_kernel": DIRECT_EDIT_REQUIRED_KERNEL,
        },
        "operation": {
            "kind": DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE,
            "distance_mm": validated["distance_mm"],
        },
        "target_selector": {
            "kind": "SEMANTIC_FACE_DESCRIPTOR",
            "descriptor": validated["target"],
            "resolution_policy": DIRECT_EDIT_REBIND_POLICY,
            "ambiguous_result": DIRECT_EDIT_HOLD,
            "missing_result": DIRECT_EDIT_HOLD,
            "prohibited_persistence": sorted(DIRECT_EDIT_PROHIBITED_PERSISTENCE),
        },
        "authority": {
            "master_type": "CAD_NATIVE",
            "geometry_authority": DIRECT_EDIT_REQUIRED_KERNEL,
            "blender_role": DIRECT_EDIT_BLENDER_ROLE,
            "display_mutation": "NONE",
            "execution_state": "NOT_EXECUTED",
        },
    }


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


def write_direct_edit_request(path: str | Path, request: dict) -> str:
    if request.get("schema") != DIRECT_EDIT_REQUEST_SCHEMA:
        raise CADSidecarContractError("unexpected CAD direct-edit request schema")
    if request.get("authority", {}).get("execution_state") != "NOT_EXECUTED":
        raise CADSidecarContractError("direct-edit request writer cannot accept an executed-state claim")
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
