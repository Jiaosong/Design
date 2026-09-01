import json
import math
import os
from collections import Counter

import bpy
import bmesh


def _is_identity_scale(obj, eps=1e-6):
    return all(abs(v - 1.0) <= eps for v in obj.scale)


def _mesh_non_manifold_count(obj):
    if obj.type != "MESH" or obj.data is None:
        return 0
    bm = bmesh.new()
    try:
        bm.from_mesh(obj.data)
        return sum(1 for edge in bm.edges if not edge.is_manifold)
    finally:
        bm.free()


def _non_finite_vertex_count(obj):
    if obj.type != "MESH" or obj.data is None:
        return 0
    count = 0
    for vertex in obj.data.vertices:
        if not all(math.isfinite(v) for v in vertex.co):
            count += 1
    return count


def _missing_image_paths():
    missing = []
    for image in bpy.data.images:
        if image.source != "FILE" or not image.filepath:
            continue
        path = bpy.path.abspath(image.filepath)
        if not os.path.exists(path):
            missing.append({"image": image.name, "path": image.filepath})
    return missing


def audit_scene(scene):
    unit = scene.unit_settings
    object_ids = [obj.oleander.ole_id for obj in scene.objects if obj.oleander.ole_id]
    duplicates = sorted([ole_id for ole_id, n in Counter(object_ids).items() if n > 1])

    object_results = []
    for obj in scene.objects:
        meta = obj.oleander
        issues = []

        if not meta.ole_id:
            issues.append("MISSING_OLE_ID")
        elif meta.ole_id in duplicates:
            issues.append("DUPLICATE_OLE_ID")

        if not _is_identity_scale(obj):
            issues.append("UNAPPLIED_SCALE_REVIEW")

        if any(abs(v) > 1.0e7 for v in obj.location):
            issues.append("LARGE_COORDINATE_REVIEW")

        non_manifold = _mesh_non_manifold_count(obj)
        if non_manifold:
            issues.append("NON_MANIFOLD_GEOMETRY")

        non_finite = _non_finite_vertex_count(obj)
        if non_finite:
            issues.append("NON_FINITE_VERTEX")

        if meta.master_type != "BLENDER_NATIVE" and not meta.master_locator:
            issues.append("MISSING_MASTER_LOCATOR")

        if meta.geometry_authority in {"FIELD_OPEN", "VISUAL_ONLY"}:
            issues.append("GEOMETRY_AUTHORITY_OPEN")

        object_results.append(
            {
                "name": obj.name,
                "ole_id": meta.ole_id,
                "type": obj.type,
                "master_type": meta.master_type,
                "geometry_authority": meta.geometry_authority,
                "field_state": meta.field_state,
                "engineering_state": meta.engineering_state,
                "manufacturing_state": meta.manufacturing_state,
                "stale": meta.stale,
                "non_manifold_edges": non_manifold,
                "non_finite_vertices": non_finite,
                "issues": issues,
            }
        )

    missing_images = _missing_image_paths()
    geometry_issues = sum(
        1
        for result in object_results
        if any(i in result["issues"] for i in ("NON_MANIFOLD_GEOMETRY", "NON_FINITE_VERTEX"))
    )

    result = {
        "schema": "OLEANDER_BLENDER_AUDIT_v0.1",
        "blender_version": bpy.app.version_string,
        "scene": scene.name,
        "unit_system": unit.system,
        "unit_scale_length": unit.scale_length,
        "object_count": len(scene.objects),
        "duplicate_ole_ids": duplicates,
        "missing_image_paths": missing_images,
        "summary": {
            "GEOMETRY": "PASS" if geometry_issues == 0 else "REVIEW",
            "UNITS_AXES": "PASS" if unit.system != "NONE" else "REVIEW",
            "DEPENDENCIES": "PASS" if not missing_images else "REVIEW",
            "ROUND_TRIP": "NOT_RUN",
            "DIMENSION_AUTHORITY": "MIXED_REVIEW",
            "FIELD_VERIFIED": "MIXED_REVIEW",
            "ENGINEERING_APPROVAL": "MIXED_REVIEW",
            "CONSTRUCTABILITY": "OPEN",
            "DESIGN_QUALITY": "REVIEW_REQUIRED",
        },
        "objects": object_results,
    }
    return result


def audit_json(scene):
    return json.dumps(audit_scene(scene), indent=2, ensure_ascii=False)
