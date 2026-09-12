"""Governed Blender-side adapter for authoritative CAD process sidecars.

This module is a shared, project-neutral professional backend adapter under the
installed OLEANDER Blender Runtime Current. It does not implement a B-Rep kernel
and does not make Blender mesh geometry authoritative CAD geometry. It serializes
solved sketch intent into deterministic CAD build requests, validates bounded
Direct Face interaction intents into deterministic direct-edit requests, validates
typed specialist responses, binds external sidecar responses to Blender display
derivatives, and marks display representations stale when upstream CAD intent
changes.

Project profiles may configure routing inputs, but they must not replace this
adapter's authority contract or bypass response/readback validation.

Authority boundary:
- build request source: SOLVED_SKETCH_INTENT
- direct-edit request source: OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1
- CAD master: external FREECAD_OCCT_BREP
- Blender object: DISPLAY_DERIVATIVE_ONLY
- this adapter validates/serializes requests and validates/binds responses; it does not itself execute B-Rep mutation
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
DIRECT_EDIT_RESPONSE_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_RESPONSE_v0.1"
DIRECT_EDIT_DISPLAY_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_DISPLAY_DERIVATIVE_v0.1"

DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE = "FACE_NORMAL_MOVE"
DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE = "FACE_TANGENT_MOVE"
DIRECT_EDIT_OPERATION_FACE_ROTATE = "FACE_ROTATE"
DIRECT_EDIT_TANGENT_MAX_DISTANCE_MM = 20.0
DIRECT_EDIT_ROTATE_MAX_ANGLE_DEG = 10.0
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

_DIRECT_REQUEST_TOP_LEVEL_KEYS = {
    "schema",
    "request_id",
    "ole_id",
    "revision",
    "units",
    "source",
    "operation",
    "target_selector",
    "authority",
}
_DIRECT_REQUEST_SOURCE_KEYS = {
    "authority",
    "intent_schema",
    "intent_sha256",
    "master_locator",
    "required_kernel",
}
_DIRECT_REQUEST_NORMAL_OPERATION_KEYS = {"kind", "distance_mm"}
_DIRECT_REQUEST_TANGENT_OPERATION_KEYS = {"kind", "translation_local_mm"}
_DIRECT_REQUEST_ROTATE_OPERATION_KEYS = {"kind", "angle_deg", "axis_mode", "axis_origin_local_mm", "axis_direction_local"}
_DIRECT_TANGENT_INTENT_PARAMETER_KEYS = {"u_mm", "v_mm", "tangent_u_local", "tangent_v_local", "translation_local_mm"}
_DIRECT_ROTATE_INTENT_PARAMETER_KEYS = {"angle_deg", "axis_mode", "axis_origin_local_mm", "axis_direction_local"}
_DIRECT_REQUEST_SELECTOR_KEYS = {
    "kind",
    "descriptor",
    "resolution_policy",
    "ambiguous_result",
    "missing_result",
    "prohibited_persistence",
}
_DIRECT_REQUEST_AUTHORITY_KEYS = {
    "master_type",
    "geometry_authority",
    "blender_role",
    "display_mutation",
    "execution_state",
}
_DIRECT_FACE_DESCRIPTOR_KEYS = {
    "selector_semantics",
    "normal_local",
    "center_local_mm",
    "area_mm2",
    "edge_count",
    "edge_lengths_mm",
    "bbox_local_mm",
}
_DIRECT_FACE_BBOX_KEYS = {"min", "max"}
_DIRECT_RESPONSE_ARTIFACT_KEYS = {"path", "sha256"}


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


def _require_exact_keys(value, expected: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise CADSidecarContractError(f"{label} must be an object")
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise CADSidecarContractError(f"{label} keys mismatch; missing={missing}, extra={extra}")
    return value


def _require_sha256_hex(value, label: str) -> str:
    text = str(value or "").strip().lower()
    if not re.fullmatch(r"[0-9a-f]{64}", text):
        raise CADSidecarContractError(f"{label} must be a 64-character SHA256 hex digest")
    return text


def _contains_forbidden_topology_reference(value) -> bool:
    """Reject persisted topology ordinals anywhere in bounded direct-edit payloads."""
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


def _validate_direct_face_descriptor(target: dict, *, strict_keys: bool = False) -> dict:
    if not isinstance(target, dict):
        raise CADSidecarContractError("direct-edit target must be an object")
    if strict_keys:
        _require_exact_keys(target, _DIRECT_FACE_DESCRIPTOR_KEYS, "direct-edit face descriptor")
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
    if strict_keys:
        _require_exact_keys(bbox, _DIRECT_FACE_BBOX_KEYS, "target.bbox_local_mm")
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


def _dot3(a, b) -> float:
    return sum(float(x) * float(y) for x, y in zip(a, b))


def _length3(value) -> float:
    return math.sqrt(_dot3(value, value))


def _unit3(value, label: str) -> list[float]:
    vector = _vector(value, 3, label)
    length = _length3(vector)
    if length <= 1e-9:
        raise CADSidecarContractError(f"{label} must be non-zero")
    return [component / length for component in vector]


def _validate_tangent_intent_parameters(parameters: dict, target: dict) -> dict:
    parameters = _require_exact_keys(parameters, _DIRECT_TANGENT_INTENT_PARAMETER_KEYS, "FACE_TANGENT_MOVE parameters")
    u_mm = _finite_float(parameters.get("u_mm"), "parameters.u_mm")
    v_mm = _finite_float(parameters.get("v_mm"), "parameters.v_mm")
    tangent_u = _unit3(parameters.get("tangent_u_local"), "parameters.tangent_u_local")
    tangent_v = _unit3(parameters.get("tangent_v_local"), "parameters.tangent_v_local")
    translation = _vector(parameters.get("translation_local_mm"), 3, "parameters.translation_local_mm")
    normal = _unit3(target.get("normal_local"), "target.normal_local")
    if abs(_dot3(tangent_u, tangent_v)) > 1e-6:
        raise CADSidecarContractError("FACE_TANGENT_MOVE U/V basis must be orthogonal")
    if abs(_dot3(tangent_u, normal)) > 1e-6 or abs(_dot3(tangent_v, normal)) > 1e-6:
        raise CADSidecarContractError("FACE_TANGENT_MOVE basis must lie in target tangent plane")
    expected = [tangent_u[i] * u_mm + tangent_v[i] * v_mm for i in range(3)]
    if any(abs(a - b) > 1e-6 for a, b in zip(expected, translation)):
        raise CADSidecarContractError("FACE_TANGENT_MOVE translation does not match U/V interaction provenance")
    distance = _length3(translation)
    if distance <= 1e-9:
        raise CADSidecarContractError("FACE_TANGENT_MOVE translation must be non-zero")
    if distance > DIRECT_EDIT_TANGENT_MAX_DISTANCE_MM + 1e-9:
        raise CADSidecarContractError("FACE_TANGENT_MOVE exceeds bounded 20 mm specialist contract")
    if abs(_dot3(normal, translation)) > 1e-6:
        raise CADSidecarContractError("FACE_TANGENT_MOVE translation must remain in the target tangent plane")
    return {
        "kind": DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE,
        "translation_local_mm": translation,
        "interaction": {
            "u_mm": u_mm,
            "v_mm": v_mm,
            "tangent_u_local": tangent_u,
            "tangent_v_local": tangent_v,
        },
    }



def _validate_rotate_intent_parameters(parameters: dict, target: dict) -> dict:
    parameters = _require_exact_keys(parameters, _DIRECT_ROTATE_INTENT_PARAMETER_KEYS, "FACE_ROTATE parameters")
    angle_deg = _finite_float(parameters.get("angle_deg"), "parameters.angle_deg")
    if abs(angle_deg) <= 1e-9:
        raise CADSidecarContractError("FACE_ROTATE angle must be non-zero")
    if abs(angle_deg) > DIRECT_EDIT_ROTATE_MAX_ANGLE_DEG + 1e-9:
        raise CADSidecarContractError("FACE_ROTATE exceeds bounded 10 degree specialist contract")
    axis_mode = str(parameters.get("axis_mode") or "")
    if axis_mode not in {"U", "V"}:
        raise CADSidecarContractError("FACE_ROTATE axis_mode must be U or V")
    axis_origin = _vector(parameters.get("axis_origin_local_mm"), 3, "parameters.axis_origin_local_mm")
    axis_direction = _unit3(parameters.get("axis_direction_local"), "parameters.axis_direction_local")
    normal = _unit3(target.get("normal_local"), "target.normal_local")
    if abs(_dot3(axis_direction, normal)) > 1e-6:
        raise CADSidecarContractError("FACE_ROTATE axis must lie in the target tangent plane")
    center = _vector(target.get("center_local_mm"), 3, "target.center_local_mm")
    if any(abs(a - b) > 1e-6 for a, b in zip(axis_origin, center)):
        raise CADSidecarContractError("FACE_ROTATE first shared contract requires the axis through target face center")
    return {
        "kind": DIRECT_EDIT_OPERATION_FACE_ROTATE,
        "angle_deg": angle_deg,
        "axis_mode": axis_mode,
        "axis_origin_local_mm": axis_origin,
        "axis_direction_local": axis_direction,
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

    operation_kind = intent.get("operation")
    parameters = intent.get("parameters") or {}
    if operation_kind == DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        distance_mm = _finite_float(parameters.get("distance_mm"), "parameters.distance_mm")
        if abs(distance_mm) <= 1e-9:
            raise CADSidecarContractError("FACE_NORMAL_MOVE distance must be non-zero")
        normalized_operation = {"kind": DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE, "distance_mm": distance_mm}
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        normalized_operation = None
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_ROTATE:
        normalized_operation = None
    else:
        raise CADSidecarContractError(f"unsupported CAD direct-edit operation: {operation_kind}")

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
    if operation_kind == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        normalized_operation = _validate_tangent_intent_parameters(parameters, target)
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_ROTATE:
        normalized_operation = _validate_rotate_intent_parameters(parameters, target)
    return {
        "ole_id": ole_id,
        "operation": normalized_operation,
        "master_locator": master_locator,
        "target": target,
        "intent_sha256": payload_sha256(intent),
    }

def build_direct_edit_request_from_intent(*, request_id: str, revision: int, intent: dict) -> dict:
    """Convert a validated Blender interaction intent into a deterministic CAD request."""
    request_id = str(request_id or "").strip()
    if not request_id:
        raise CADSidecarContractError("direct-edit request_id must be non-empty")
    if int(revision) < 1:
        raise CADSidecarContractError("direct-edit revision must be >= 1")
    validated = validate_direct_edit_intent(intent)
    normalized_operation = validated["operation"]
    if normalized_operation["kind"] == DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        request_operation = {"kind": DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE, "distance_mm": normalized_operation["distance_mm"]}
    elif normalized_operation["kind"] == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        request_operation = {"kind": DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE, "translation_local_mm": normalized_operation["translation_local_mm"]}
    else:
        request_operation = {
            "kind": DIRECT_EDIT_OPERATION_FACE_ROTATE,
            "angle_deg": normalized_operation["angle_deg"],
            "axis_mode": normalized_operation["axis_mode"],
            "axis_origin_local_mm": normalized_operation["axis_origin_local_mm"],
            "axis_direction_local": normalized_operation["axis_direction_local"],
        }
    request = {
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
        "operation": request_operation,
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
    validate_direct_edit_request(request)
    return request

def validate_direct_edit_request(request: dict) -> dict:
    """Strictly validate a serialized direct-edit request before persistence/execution."""
    request = _require_exact_keys(request, _DIRECT_REQUEST_TOP_LEVEL_KEYS, "CAD direct-edit request")
    if request.get("schema") != DIRECT_EDIT_REQUEST_SCHEMA:
        raise CADSidecarContractError("unexpected CAD direct-edit request schema")

    request_id = str(request.get("request_id") or "").strip()
    ole_id = str(request.get("ole_id") or "").strip()
    if not request_id or not ole_id:
        raise CADSidecarContractError("CAD direct-edit request identity fields must be non-empty")
    try:
        revision = int(request.get("revision"))
    except (TypeError, ValueError) as exc:
        raise CADSidecarContractError("CAD direct-edit revision must be an integer") from exc
    if revision < 1:
        raise CADSidecarContractError("CAD direct-edit revision must be >= 1")
    if request.get("units") != "mm":
        raise CADSidecarContractError("CAD direct-edit request currently supports mm only")
    if _contains_forbidden_topology_reference(request):
        raise CADSidecarContractError("CAD direct-edit request contains a prohibited persistent topology reference")

    source = _require_exact_keys(request.get("source"), _DIRECT_REQUEST_SOURCE_KEYS, "CAD direct-edit request source")
    if source.get("authority") != "CAD_DIRECT_EDIT_INTENT":
        raise CADSidecarContractError("CAD direct-edit request source authority mismatch")
    if source.get("intent_schema") != DIRECT_EDIT_INTENT_SCHEMA:
        raise CADSidecarContractError("CAD direct-edit request lost intent schema provenance")
    intent_sha256 = _require_sha256_hex(source.get("intent_sha256"), "source.intent_sha256")
    master_locator = str(source.get("master_locator") or "").strip()
    if not master_locator:
        raise CADSidecarContractError("CAD direct-edit request requires a governed master locator")
    if source.get("required_kernel") != DIRECT_EDIT_REQUIRED_KERNEL:
        raise CADSidecarContractError("CAD direct-edit request must require FreeCAD/OCCT B-Rep authority")

    raw_operation = request.get("operation")
    if not isinstance(raw_operation, dict):
        raise CADSidecarContractError("CAD direct-edit operation must be an object")
    operation_kind = raw_operation.get("kind")
    if operation_kind == DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        operation = _require_exact_keys(raw_operation, _DIRECT_REQUEST_NORMAL_OPERATION_KEYS, "CAD direct-edit normal operation")
        distance_mm = _finite_float(operation.get("distance_mm"), "operation.distance_mm")
        if abs(distance_mm) <= 1e-9:
            raise CADSidecarContractError("FACE_NORMAL_MOVE request distance must be non-zero")
        normalized_operation = {"kind": operation_kind, "distance_mm": distance_mm}
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        operation = _require_exact_keys(raw_operation, _DIRECT_REQUEST_TANGENT_OPERATION_KEYS, "CAD direct-edit tangent operation")
        translation = _vector(operation.get("translation_local_mm"), 3, "operation.translation_local_mm")
        distance = _length3(translation)
        if distance <= 1e-9:
            raise CADSidecarContractError("FACE_TANGENT_MOVE request translation must be non-zero")
        if distance > DIRECT_EDIT_TANGENT_MAX_DISTANCE_MM + 1e-9:
            raise CADSidecarContractError("FACE_TANGENT_MOVE request exceeds bounded 20 mm specialist contract")
        normalized_operation = {"kind": operation_kind, "translation_local_mm": translation}
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_ROTATE:
        operation = _require_exact_keys(raw_operation, _DIRECT_REQUEST_ROTATE_OPERATION_KEYS, "CAD direct-edit rotate operation")
        angle_deg = _finite_float(operation.get("angle_deg"), "operation.angle_deg")
        if abs(angle_deg) <= 1e-9:
            raise CADSidecarContractError("FACE_ROTATE request angle must be non-zero")
        if abs(angle_deg) > DIRECT_EDIT_ROTATE_MAX_ANGLE_DEG + 1e-9:
            raise CADSidecarContractError("FACE_ROTATE request exceeds bounded 10 degree specialist contract")
        axis_mode = str(operation.get("axis_mode") or "")
        if axis_mode not in {"U", "V"}:
            raise CADSidecarContractError("FACE_ROTATE request axis_mode must be U or V")
        axis_origin = _vector(operation.get("axis_origin_local_mm"), 3, "operation.axis_origin_local_mm")
        axis_direction = _unit3(operation.get("axis_direction_local"), "operation.axis_direction_local")
        normalized_operation = {
            "kind": operation_kind,
            "angle_deg": angle_deg,
            "axis_mode": axis_mode,
            "axis_origin_local_mm": axis_origin,
            "axis_direction_local": axis_direction,
        }
    else:
        raise CADSidecarContractError(f"unsupported CAD direct-edit request operation: {operation_kind}")

    selector = _require_exact_keys(request.get("target_selector"), _DIRECT_REQUEST_SELECTOR_KEYS, "CAD direct-edit target selector")
    if selector.get("kind") != "SEMANTIC_FACE_DESCRIPTOR":
        raise CADSidecarContractError("CAD direct-edit request requires a semantic face descriptor")
    descriptor = _validate_direct_face_descriptor(selector.get("descriptor"), strict_keys=True)
    if selector.get("resolution_policy") != DIRECT_EDIT_REBIND_POLICY:
        raise CADSidecarContractError("CAD direct-edit request must use fail-closed semantic rebind")
    if selector.get("ambiguous_result") != DIRECT_EDIT_HOLD or selector.get("missing_result") != DIRECT_EDIT_HOLD:
        raise CADSidecarContractError("ambiguous or missing CAD request selector resolution must HOLD")
    prohibited = selector.get("prohibited_persistence")
    if not isinstance(prohibited, list) or set(prohibited) != DIRECT_EDIT_PROHIBITED_PERSISTENCE:
        raise CADSidecarContractError("CAD direct-edit request topology-persistence prohibition set mismatch")
    if operation_kind == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        normal = _unit3(descriptor["normal_local"], "target.normal_local")
        if abs(_dot3(normal, normalized_operation["translation_local_mm"])) > 1e-6:
            raise CADSidecarContractError("FACE_TANGENT_MOVE request translation must remain in target tangent plane")
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_ROTATE:
        normal = _unit3(descriptor["normal_local"], "target.normal_local")
        if abs(_dot3(normal, normalized_operation["axis_direction_local"])) > 1e-6:
            raise CADSidecarContractError("FACE_ROTATE request axis must remain in target tangent plane")
        if any(abs(a - b) > 1e-6 for a, b in zip(normalized_operation["axis_origin_local_mm"], descriptor["center_local_mm"])):
            raise CADSidecarContractError("FACE_ROTATE request axis must pass through target face center")

    authority = _require_exact_keys(request.get("authority"), _DIRECT_REQUEST_AUTHORITY_KEYS, "CAD direct-edit request authority")
    if authority.get("master_type") != "CAD_NATIVE":
        raise CADSidecarContractError("CAD direct-edit request lost CAD_NATIVE master type")
    if authority.get("geometry_authority") != DIRECT_EDIT_REQUIRED_KERNEL:
        raise CADSidecarContractError("CAD direct-edit request lost FreeCAD/OCCT geometry authority")
    if authority.get("blender_role") != DIRECT_EDIT_BLENDER_ROLE:
        raise CADSidecarContractError("CAD direct-edit request must keep Blender display-only")
    if authority.get("display_mutation") != "NONE":
        raise CADSidecarContractError("CAD direct-edit request may not authorize display mutation")
    if authority.get("execution_state") != "NOT_EXECUTED":
        raise CADSidecarContractError("CAD direct-edit request cannot arrive with an executed-state claim")

    return {
        "request_id": request_id,
        "ole_id": ole_id,
        "revision": revision,
        "units": "mm",
        "source": {
            "intent_sha256": intent_sha256,
            "master_locator": master_locator,
            "required_kernel": DIRECT_EDIT_REQUIRED_KERNEL,
        },
        "operation": normalized_operation,
        "target": descriptor,
        "execution_state": "NOT_EXECUTED",
        "request_sha256": payload_sha256(request),
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
    validate_direct_edit_request(request)
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(_canonical_bytes(request))
    return file_sha256(path)


def _validate_direct_artifact(record, label: str, *, released: bool) -> dict:
    record = _require_exact_keys(record, _DIRECT_RESPONSE_ARTIFACT_KEYS, label)
    path = str(record.get("path") or "")
    sha256 = _require_sha256_hex(record.get("sha256"), f"{label}.sha256")
    if released:
        if not path:
            raise CADSidecarContractError(f"{label} must expose a released artifact path")
        if sha256 == "0" * 64:
            raise CADSidecarContractError(f"{label} released artifact SHA cannot be zero")
    else:
        if path or sha256 != "0" * 64:
            raise CADSidecarContractError(f"{label} must remain unreleased on HOLD")
    return {"path": path, "sha256": sha256}


def validate_direct_edit_response(response: dict, *, allow_hold: bool = False) -> dict:
    """Validate a typed specialist response for the bounded Direct Face operation union."""
    if not isinstance(response, dict) or response.get("schema") != DIRECT_EDIT_RESPONSE_SCHEMA:
        raise CADSidecarContractError("unexpected CAD direct-edit response schema")

    request_id = str(response.get("request_id") or "").strip()
    ole_id = str(response.get("ole_id") or "").strip()
    if not request_id or not ole_id:
        raise CADSidecarContractError("CAD direct-edit response identity fields must be non-empty")
    try:
        revision = int(response.get("revision"))
    except (TypeError, ValueError) as exc:
        raise CADSidecarContractError("CAD direct-edit response revision must be an integer") from exc
    if revision < 1:
        raise CADSidecarContractError("CAD direct-edit response revision must be >= 1")
    request_sha256 = _require_sha256_hex(response.get("request_sha256"), "direct response request_sha256")

    kernel = response.get("kernel") or {}
    if kernel.get("name") != "FreeCAD" or not str(kernel.get("version") or "").strip():
        raise CADSidecarContractError("CAD direct-edit response lost FreeCAD runtime identity")
    if not str(kernel.get("occ_version") or "").strip():
        raise CADSidecarContractError("CAD direct-edit response lost OCCT runtime identity")

    operation = response.get("operation") or {}
    operation_kind = operation.get("kind")
    if operation_kind == DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        distance_mm = _finite_float(operation.get("distance_mm"), "direct response operation.distance_mm")
        if abs(distance_mm) <= 1e-9:
            raise CADSidecarContractError("CAD direct-edit response distance must be non-zero")
        normalized_operation = {"kind": operation_kind, "distance_mm": distance_mm}
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        translation = _vector(operation.get("translation_local_mm"), 3, "direct response operation.translation_local_mm")
        distance = _length3(translation)
        if distance <= 1e-9 or distance > DIRECT_EDIT_TANGENT_MAX_DISTANCE_MM + 1e-9:
            raise CADSidecarContractError("CAD tangent response translation is outside bounded contract")
        normalized_operation = {"kind": operation_kind, "translation_local_mm": translation}
    elif operation_kind == DIRECT_EDIT_OPERATION_FACE_ROTATE:
        angle_deg = _finite_float(operation.get("angle_deg"), "direct response operation.angle_deg")
        if abs(angle_deg) <= 1e-9 or abs(angle_deg) > DIRECT_EDIT_ROTATE_MAX_ANGLE_DEG + 1e-9:
            raise CADSidecarContractError("CAD rotate response angle is outside bounded contract")
        axis_mode = str(operation.get("axis_mode") or "")
        if axis_mode not in {"U", "V"}:
            raise CADSidecarContractError("CAD rotate response axis_mode must be U or V")
        axis_origin = _vector(operation.get("axis_origin_local_mm"), 3, "direct response operation.axis_origin_local_mm")
        axis_direction = _unit3(operation.get("axis_direction_local"), "direct response operation.axis_direction_local")
        normalized_operation = {
            "kind": operation_kind,
            "angle_deg": angle_deg,
            "axis_mode": axis_mode,
            "axis_origin_local_mm": axis_origin,
            "axis_direction_local": axis_direction,
        }
    else:
        raise CADSidecarContractError("CAD direct-edit response operation mismatch")

    authority = response.get("authoritative") or {}
    if authority.get("master_type") != "CAD_NATIVE":
        raise CADSidecarContractError("CAD direct-edit response lost CAD_NATIVE master type")
    if authority.get("geometry_authority") != DIRECT_EDIT_REQUIRED_KERNEL:
        raise CADSidecarContractError("CAD direct-edit response lost FreeCAD/OCCT geometry authority")

    resolution = response.get("resolution") or {}
    try:
        candidate_count = int(resolution.get("candidate_count"))
    except (TypeError, ValueError) as exc:
        raise CADSidecarContractError("CAD direct-edit response candidate_count must be an integer") from exc
    if candidate_count < 0:
        raise CADSidecarContractError("CAD direct-edit response candidate_count cannot be negative")

    measurements = response.get("measurements") or {}
    if measurements.get("units") != "mm":
        raise CADSidecarContractError("CAD direct-edit response measurements must use mm")
    source_bbox = _vector(measurements.get("source_bbox_mm"), 3, "direct response source_bbox_mm")
    result_bbox = _vector(measurements.get("result_bbox_mm"), 3, "direct response result_bbox_mm")
    source_volume = _finite_float(measurements.get("source_volume_mm3"), "direct response source_volume_mm3")
    result_volume = _finite_float(measurements.get("result_volume_mm3"), "direct response result_volume_mm3")
    try:
        result_solid_count = int(measurements.get("result_solid_count"))
    except (TypeError, ValueError) as exc:
        raise CADSidecarContractError("CAD direct-edit response result_solid_count must be an integer") from exc
    if source_volume <= 0.0:
        raise CADSidecarContractError("CAD direct-edit response source volume must be positive")

    status = response.get("status")
    if status == "PASS":
        if operation.get("execution_state") != "EXECUTED":
            raise CADSidecarContractError("PASS CAD direct-edit response must be EXECUTED")
        if resolution.get("state") != "RESOLVED_UNIQUE" or candidate_count != 1:
            raise CADSidecarContractError("PASS CAD direct-edit response requires one unique semantic face")
        _require_sha256_hex(resolution.get("resolved_signature"), "direct response resolved_signature")
        if result_solid_count != 1 or result_volume <= 0.0 or any(value <= 0.0 for value in result_bbox):
            raise CADSidecarContractError("PASS CAD direct-edit response must release one positive-volume result solid")
        for key in ("fcstd", "step", "brep"):
            _validate_direct_artifact(authority.get(key), f"authoritative.{key}", released=True)
        _validate_direct_artifact(response.get("display_derivative"), "display_derivative", released=True)
        if response.get("error") not in (None, ""):
            raise CADSidecarContractError("PASS CAD direct-edit response cannot carry an error")
    elif status == "HOLD":
        if not allow_hold:
            raise CADSidecarContractError("CAD direct-edit HOLD response is not bindable")
        if operation.get("execution_state") != "NOT_EXECUTED":
            raise CADSidecarContractError("HOLD CAD direct-edit response must remain NOT_EXECUTED")
        state = resolution.get("state")
        if state not in {"MISSING_HOLD", "AMBIGUOUS_HOLD"}:
            raise CADSidecarContractError("CAD direct-edit HOLD response has an invalid resolution state")
        if state == "MISSING_HOLD" and candidate_count != 0:
            raise CADSidecarContractError("MISSING_HOLD must have zero candidates")
        if state == "AMBIGUOUS_HOLD" and candidate_count <= 1:
            raise CADSidecarContractError("AMBIGUOUS_HOLD must have multiple candidates")
        for key in ("fcstd", "step", "brep"):
            _validate_direct_artifact(authority.get(key), f"authoritative.{key}", released=False)
        _validate_direct_artifact(response.get("display_derivative"), "display_derivative", released=False)
        if result_solid_count != 0 or abs(result_volume) > 1e-12 or any(abs(value) > 1e-12 for value in result_bbox):
            raise CADSidecarContractError("HOLD CAD direct-edit response may not release result geometry")
    else:
        raise CADSidecarContractError(f"unsupported CAD direct-edit response status: {status}")

    return {
        "request_id": request_id,
        "ole_id": ole_id,
        "revision": revision,
        "request_sha256": request_sha256,
        "status": status,
        "resolution_state": resolution.get("state"),
        "candidate_count": candidate_count,
        "execution_state": operation.get("execution_state"),
        "operation": normalized_operation,
        "distance_mm": normalized_operation.get("distance_mm"),
        "translation_local_mm": normalized_operation.get("translation_local_mm"),
        "angle_deg": normalized_operation.get("angle_deg"),
        "axis_mode": normalized_operation.get("axis_mode"),
        "axis_origin_local_mm": normalized_operation.get("axis_origin_local_mm"),
        "axis_direction_local": normalized_operation.get("axis_direction_local"),
        "source_bbox_mm": source_bbox,
        "result_bbox_mm": result_bbox,
        "source_volume_mm3": source_volume,
        "result_volume_mm3": result_volume,
        "result_solid_count": result_solid_count,
    }

def load_direct_edit_response(path: str | Path, *, allow_hold: bool = False) -> dict:
    response = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_direct_edit_response(response, allow_hold=allow_hold)
    return response


def assert_direct_edit_response_matches_request(response: dict, request: dict) -> None:
    validated_request = validate_direct_edit_request(request)
    validated_response = validate_direct_edit_response(response, allow_hold=True)
    if validated_response["request_id"] != validated_request["request_id"]:
        raise CADSidecarContractError("CAD direct-edit response request_id mismatch")
    if validated_response["ole_id"] != validated_request["ole_id"]:
        raise CADSidecarContractError("CAD direct-edit response OLE ID mismatch")
    if validated_response["revision"] != validated_request["revision"]:
        raise CADSidecarContractError("CAD direct-edit response revision mismatch")
    if validated_response["request_sha256"] != validated_request["request_sha256"]:
        raise CADSidecarContractError("CAD direct-edit response request SHA mismatch")
    request_operation = validated_request["operation"]
    response_operation = validated_response["operation"]
    if response_operation["kind"] != request_operation["kind"]:
        raise CADSidecarContractError("CAD direct-edit response operation kind mismatch")
    if request_operation["kind"] == DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        if abs(response_operation["distance_mm"] - request_operation["distance_mm"]) > 1e-9:
            raise CADSidecarContractError("CAD direct-edit response distance mismatch")
    elif request_operation["kind"] == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        if any(abs(a - b) > 1e-9 for a, b in zip(response_operation["translation_local_mm"], request_operation["translation_local_mm"])):
            raise CADSidecarContractError("CAD direct-edit response tangent translation mismatch")
    else:
        if abs(response_operation["angle_deg"] - request_operation["angle_deg"]) > 1e-9:
            raise CADSidecarContractError("CAD direct-edit response rotate angle mismatch")
        if response_operation["axis_mode"] != request_operation["axis_mode"]:
            raise CADSidecarContractError("CAD direct-edit response rotate axis mode mismatch")
        if any(abs(a - b) > 1e-9 for a, b in zip(response_operation["axis_origin_local_mm"], request_operation["axis_origin_local_mm"])):
            raise CADSidecarContractError("CAD direct-edit response rotate axis origin mismatch")
        if any(abs(a - b) > 1e-9 for a, b in zip(response_operation["axis_direction_local"], request_operation["axis_direction_local"])):
            raise CADSidecarContractError("CAD direct-edit response rotate axis direction mismatch")

def _validate_direct_edit_display_payload(display_payload: dict, response: dict) -> None:
    if not isinstance(display_payload, dict) or display_payload.get("schema") != DIRECT_EDIT_DISPLAY_SCHEMA:
        raise CADSidecarContractError("unexpected CAD direct-edit display derivative schema")
    if display_payload.get("master_type") != "CAD_NATIVE":
        raise CADSidecarContractError("CAD direct-edit display lost CAD_NATIVE master type")
    if display_payload.get("geometry_authority") != DIRECT_EDIT_REQUIRED_KERNEL:
        raise CADSidecarContractError("CAD direct-edit display lost FreeCAD/OCCT authority")
    if display_payload.get("display_authority") != DIRECT_EDIT_BLENDER_ROLE:
        raise CADSidecarContractError("CAD direct-edit display must remain DISPLAY_DERIVATIVE_ONLY")
    if display_payload.get("units") != "mm":
        raise CADSidecarContractError("CAD direct-edit display currently supports mm only")
    if display_payload.get("request_id") != response.get("request_id"):
        raise CADSidecarContractError("CAD direct-edit display request_id mismatch")
    if int(display_payload.get("request_revision", -1)) != int(response.get("revision", -2)):
        raise CADSidecarContractError("CAD direct-edit display request revision mismatch")
    if display_payload.get("request_sha256") != response.get("request_sha256"):
        raise CADSidecarContractError("CAD direct-edit display request SHA mismatch")
    authoritative = response.get("authoritative") or {}
    if str(display_payload.get("source_master") or "") != str((authoritative.get("fcstd") or {}).get("path") or ""):
        raise CADSidecarContractError("CAD direct-edit display master locator mismatch")
    if str(display_payload.get("source_step") or "") != str((authoritative.get("step") or {}).get("path") or ""):
        raise CADSidecarContractError("CAD direct-edit display STEP locator mismatch")
    if display_payload.get("source_step_sha256") != (authoritative.get("step") or {}).get("sha256"):
        raise CADSidecarContractError("CAD direct-edit display STEP SHA mismatch")
    vertices = display_payload.get("vertices_mm") or []
    triangles = display_payload.get("triangles") or []
    if not vertices or not triangles:
        raise CADSidecarContractError("CAD direct-edit display derivative is empty")


def bind_direct_edit_display_derivative(*, response: dict, display_payload: dict, request: dict | None = None, collection=None, existing_object=None):
    """Bind a validated Direct Face PASS response as a display-only Blender derivative."""
    validated = validate_direct_edit_response(response, allow_hold=False)
    if request is not None:
        assert_direct_edit_response_matches_request(response, request)
    _validate_direct_edit_display_payload(display_payload, response)

    generic_response = {
        "schema": RESPONSE_SCHEMA,
        "request_id": response["request_id"],
        "ole_id": response["ole_id"],
        "revision": response["revision"],
        "status": "PASS",
        "request_sha256": response["request_sha256"],
        "authoritative": response["authoritative"],
    }
    generic_display = dict(display_payload)
    generic_display["schema"] = DISPLAY_SCHEMA
    obj = bind_display_derivative(
        response=generic_response,
        display_payload=generic_display,
        collection=collection,
        existing_object=existing_object,
    )
    obj["cad_direct_edit_response_schema"] = DIRECT_EDIT_RESPONSE_SCHEMA
    obj["cad_direct_edit_display_schema"] = DIRECT_EDIT_DISPLAY_SCHEMA
    obj["cad_direct_edit_execution_state"] = validated["execution_state"]
    obj["cad_direct_edit_resolution_state"] = validated["resolution_state"]
    obj["cad_direct_edit_candidate_count"] = validated["candidate_count"]
    obj["cad_direct_edit_operation_kind"] = validated["operation"]["kind"]
    if validated["operation"]["kind"] == DIRECT_EDIT_OPERATION_FACE_NORMAL_MOVE:
        obj["cad_direct_edit_distance_mm"] = validated["distance_mm"]
    elif validated["operation"]["kind"] == DIRECT_EDIT_OPERATION_FACE_TANGENT_MOVE:
        obj["cad_direct_edit_translation_local_mm"] = validated["translation_local_mm"]
    else:
        obj["cad_direct_edit_angle_deg"] = validated["angle_deg"]
        obj["cad_direct_edit_axis_mode"] = validated["axis_mode"]
        obj["cad_direct_edit_axis_origin_local_mm"] = validated["axis_origin_local_mm"]
        obj["cad_direct_edit_axis_direction_local"] = validated["axis_direction_local"]
    return obj

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