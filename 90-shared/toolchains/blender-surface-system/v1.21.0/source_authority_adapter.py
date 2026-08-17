from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

try:
    import bpy
except ImportError:  # Allows deterministic contract/unit tests outside Blender.
    bpy = None

SYSTEM_NAME = "OLEANDER Blender Surface System"
SYSTEM_VERSION = "v1.21.0"
ADAPTER_API = "oleander.blender-surface-system.source-authority-adapter.v1"
SOURCE_COLLECTION_DEFAULT = "OLEANDER_SOURCE_AUTHORITY"
DERIVED_DIAGNOSTIC_ROLE = "DERIVED_DIAGNOSTIC_NOT_AUTHORITY"

_ALLOWED_SCALARS = (str, int, float, bool, type(None))


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def _normalized(value: Any) -> Any:
    if isinstance(value, _ALLOWED_SCALARS):
        return value
    if isinstance(value, dict):
        return {str(k): _normalized(value[k]) for k in sorted(value)}
    if isinstance(value, (list, tuple)):
        return [_normalized(v) for v in value]
    try:
        return [_normalized(v) for v in value]
    except TypeError:
        return str(value)


def canonical_json(data: Any) -> str:
    return json.dumps(
        _normalized(data),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_digest(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def validate_context_binding(binding: dict[str, Any], contract: dict[str, Any]) -> dict[str, Any]:
    surface = binding["surface_system"]
    source = binding["source_authority"]
    diagnostics = binding["diagnostic_policy"]
    checks = {
        "system_name_matches": surface.get("system") == SYSTEM_NAME == contract.get("system"),
        "system_version_matches": surface.get("version") == SYSTEM_VERSION == contract.get("version"),
        "adapter_api_matches": surface.get("adapter_api") == ADAPTER_API == contract.get("adapter_api"),
        "source_collection_matches": source.get("collection") == contract["source_authority"]["collection"],
        "expected_source_set_matches": sorted(source.get("expected_objects", ()))
        == sorted(contract["source_authority"]["expected_objects"]),
        "source_owner_retained": binding.get("source_owner") == "MODELING_WORKER_v0.13",
        "diagnostic_proxy_required": diagnostics.get("diagnostic_proxy_required") is True,
        "source_before_after_gate_required": diagnostics.get("source_before_after_digest_gate_required") is True,
        "source_material_mutation_forbidden": diagnostics.get("source_material_mutation_forbidden") is True,
        "project_target_material_mutation_forbidden": diagnostics.get("project_target_material_mutation_forbidden") is True,
        "promotion_impact_none": diagnostics.get("promotion_impact") == "NONE",
    }
    for key, ok in checks.items():
        _require(ok, f"Source Authority Adapter binding failed: {key}")
    return {
        "status": "PASS",
        "system": SYSTEM_NAME,
        "version": SYSTEM_VERSION,
        "adapter_api": ADAPTER_API,
        "checks": checks,
    }


def _rounded(value: float, digits: int = 10) -> float:
    return round(float(value), digits)


def _vector(values: Iterable[float]) -> list[float]:
    return [_rounded(v) for v in values]


def _matrix(obj: Any) -> list[list[float]]:
    return [[_rounded(v) for v in row] for row in obj.matrix_world]


def _custom_properties(obj: Any) -> dict[str, Any]:
    props: dict[str, Any] = {}
    for key in sorted(obj.keys()):
        if key == "_RNA_UI":
            continue
        props[str(key)] = _normalized(obj[key])
    return props


def _curve_geometry(obj: Any) -> dict[str, Any]:
    splines: list[dict[str, Any]] = []
    for spline in obj.data.splines:
        record: dict[str, Any] = {
            "type": str(spline.type),
            "cyclic_u": bool(spline.use_cyclic_u),
            "order_u": int(getattr(spline, "order_u", 0)),
            "use_endpoint_u": bool(getattr(spline, "use_endpoint_u", False)),
        }
        if spline.type == "BEZIER":
            record["bezier_points"] = [
                {
                    "co": _vector(point.co),
                    "handle_left": _vector(point.handle_left),
                    "handle_right": _vector(point.handle_right),
                    "handle_left_type": str(point.handle_left_type),
                    "handle_right_type": str(point.handle_right_type),
                }
                for point in spline.bezier_points
            ]
        else:
            record["points"] = [
                {
                    "co": _vector(point.co),
                    "weight": _rounded(getattr(point, "weight", point.co[3] if len(point.co) > 3 else 1.0)),
                }
                for point in spline.points
            ]
        splines.append(record)
    return {
        "dimensions": str(obj.data.dimensions),
        "resolution_u": int(obj.data.resolution_u),
        "splines": splines,
    }


def _mesh_geometry(obj: Any) -> dict[str, Any]:
    return {
        "vertices": [_vector(vertex.co) for vertex in obj.data.vertices],
        "edges": [[int(v) for v in edge.vertices] for edge in obj.data.edges],
        "polygons": [[int(v) for v in polygon.vertices] for polygon in obj.data.polygons],
    }


def object_snapshot(obj: Any) -> dict[str, Any]:
    record: dict[str, Any] = {
        "name": str(obj.name),
        "type": str(obj.type),
        "matrix_world": _matrix(obj),
        "custom_properties": _custom_properties(obj),
    }
    if obj.type == "CURVE":
        record["geometry"] = _curve_geometry(obj)
    elif obj.type == "MESH":
        record["geometry"] = _mesh_geometry(obj)
    elif obj.type == "EMPTY":
        record["empty"] = {
            "display_type": str(obj.empty_display_type),
            "display_size": _rounded(obj.empty_display_size),
            "location": _vector(obj.location),
        }
    return record


def snapshot_source_collection(
    collection: Any,
    expected_names: Iterable[str] | None = None,
) -> dict[str, Any]:
    _require(collection is not None, "Source collection is required")
    objects = sorted(list(collection.objects), key=lambda item: item.name)
    names = [obj.name for obj in objects]
    expected = sorted(str(name) for name in expected_names) if expected_names is not None else None
    if expected is not None:
        _require(names == expected, f"Source object set mismatch: expected {expected}, got {names}")

    records = [object_snapshot(obj) for obj in objects]
    payload = {
        "schema": "oleander.blender-surface-system.source-authority-snapshot.v1",
        "system": SYSTEM_NAME,
        "system_version": SYSTEM_VERSION,
        "adapter_api": ADAPTER_API,
        "collection": str(collection.name),
        "objects": records,
    }
    payload["source_sha256"] = canonical_digest(payload)
    return payload


def assert_source_unchanged(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    before_sha = str(before["source_sha256"])
    after_sha = str(after["source_sha256"])
    _require(before_sha == after_sha, f"Source authority mutated during diagnostic session: {before_sha} != {after_sha}")
    return {
        "status": "PASS",
        "check": "SOURCE_AUTHORITY_UNCHANGED_DURING_DIAGNOSTIC",
        "before_sha256": before_sha,
        "after_sha256": after_sha,
    }


def source_edit_detected(before: dict[str, Any], after: dict[str, Any]) -> bool:
    return str(before["source_sha256"]) != str(after["source_sha256"])


def _require_blender() -> None:
    _require(bpy is not None, "This operation must run inside Blender")


def diagnostic_proxy(
    target_obj: Any,
    collection: Any,
    source_snapshot: dict[str, Any],
    name: str | None = None,
) -> Any:
    """Create a disposable evaluated-mesh proxy; never mutate target/source material slots."""
    _require_blender()
    _require(target_obj is not None, "Diagnostic target object is required")
    _require(collection is not None, "Diagnostic collection is required")
    _require(target_obj.type in {"MESH", "CURVE", "SURFACE", "FONT", "META"}, f"Unsupported diagnostic target type: {target_obj.type}")

    depsgraph = bpy.context.evaluated_depsgraph_get()
    evaluated = target_obj.evaluated_get(depsgraph)
    mesh = bpy.data.meshes.new_from_object(evaluated, depsgraph=depsgraph)
    proxy_name = name or f"{target_obj.name}__OL_DIAGNOSTIC_PROXY"
    proxy = bpy.data.objects.new(proxy_name, mesh)
    collection.objects.link(proxy)
    proxy.matrix_world = target_obj.matrix_world.copy()
    proxy["OLEANDER_AUTHORITY"] = "DERIVED_EXECUTION_NOT_AUTHORITY"
    proxy["OLEANDER_ROLE"] = DERIVED_DIAGNOSTIC_ROLE
    proxy["OLEANDER_EDITABLE"] = False
    proxy["OLEANDER_DIAGNOSTIC_SOURCE_OBJECT"] = str(target_obj.name)
    proxy["OLEANDER_SOURCE_SNAPSHOT_SHA256"] = str(source_snapshot["source_sha256"])
    proxy["OLEANDER_SURFACE_SYSTEM"] = SYSTEM_NAME
    proxy["OLEANDER_SURFACE_SYSTEM_VERSION"] = SYSTEM_VERSION
    proxy["OLEANDER_SOURCE_ADAPTER_API"] = ADAPTER_API
    return proxy


def assign_diagnostic_material(proxy: Any, material: Any) -> None:
    _require_blender()
    _require(proxy.get("OLEANDER_ROLE") == DERIVED_DIAGNOSTIC_ROLE, "Refusing material mutation on non-diagnostic object")
    proxy.data.materials.clear()
    proxy.data.materials.append(material)


def remove_diagnostic_proxy(proxy: Any) -> None:
    _require_blender()
    _require(proxy.get("OLEANDER_ROLE") == DERIVED_DIAGNOSTIC_ROLE, "Refusing to delete non-diagnostic object")
    mesh = proxy.data
    bpy.data.objects.remove(proxy, do_unlink=True)
    if mesh and mesh.users == 0:
        bpy.data.meshes.remove(mesh)


def write_snapshot(snapshot: dict[str, Any], path: str | Path) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out
