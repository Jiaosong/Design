"""OLEANDER governed inference engine v2.

This layer exposes deterministic geometric inference helpers for Blender-native
mesh workflows: parallel/perpendicular/collinear/intersection analysis,
extension-line projection, world-axis lock projection and temporary tracking
points. It never creates a persistent geometric constraint or claims a CAD
sketch solver.
"""

from __future__ import annotations

import json
import math

import bpy
from mathutils import Vector

from .dependency import object_id
from .measurement_system import mm_to_scene_units, scene_units_to_mm

TRACKING_POINTS_KEY = "oleander_tracking_points_v2"
INFERENCE_V2_SNAPSHOT_KEY = "oleander_inference_v2_snapshot"


def _safe_unit(vector, label="direction"):
    value = Vector(vector)
    if value.length <= 1e-12:
        raise ValueError(f"{label} must be non-zero")
    return value.normalized()


def _angle_0_90_degrees(a, b):
    ua = _safe_unit(a, "first direction")
    ub = _safe_unit(b, "second direction")
    cosine = max(-1.0, min(1.0, abs(ua.dot(ub))))
    return math.degrees(math.acos(cosine))


def _line_closest_points(p1, d1, p2, d2):
    p1 = Vector(p1)
    p2 = Vector(p2)
    d1 = _safe_unit(d1, "first direction")
    d2 = _safe_unit(d2, "second direction")
    w0 = p1 - p2
    a = d1.dot(d1)
    b = d1.dot(d2)
    c = d2.dot(d2)
    d = d1.dot(w0)
    e = d2.dot(w0)
    denom = a * c - b * b
    if abs(denom) <= 1e-12:
        return None
    t = (b * e - c * d) / denom
    s = (a * e - b * d) / denom
    return p1 + d1 * t, p2 + d2 * s, t, s


def analyze_infinite_lines(scene, p1, d1, p2, d2, linear_tolerance_mm=0.1, angular_tolerance_deg=0.1):
    """Analyze two infinite 3D lines without solving or mutating geometry."""
    linear_tolerance_mm = float(linear_tolerance_mm)
    angular_tolerance_deg = float(angular_tolerance_deg)
    if linear_tolerance_mm < 0.0:
        raise ValueError("linear tolerance must be non-negative")
    if not 0.0 <= angular_tolerance_deg <= 45.0:
        raise ValueError("angular tolerance must be between 0 and 45 degrees")

    p1 = Vector(p1)
    p2 = Vector(p2)
    u1 = _safe_unit(d1, "first direction")
    u2 = _safe_unit(d2, "second direction")
    angle = _angle_0_90_degrees(u1, u2)
    parallel = angle <= angular_tolerance_deg
    perpendicular = abs(90.0 - angle) <= angular_tolerance_deg
    tolerance_scene = mm_to_scene_units(scene, linear_tolerance_mm)

    # Distance from p2 to line 1 is sufficient for collinearity once directions are parallel.
    line_offset_scene = ((p2 - p1).cross(u1)).length
    collinear = parallel and line_offset_scene <= tolerance_scene

    closest = _line_closest_points(p1, u1, p2, u2)
    intersection = None
    closest_distance_scene = line_offset_scene if closest is None else (closest[0] - closest[1]).length
    if closest is not None and closest_distance_scene <= tolerance_scene:
        intersection = (closest[0] + closest[1]) * 0.5

    relations = []
    if collinear:
        relations.append("COLLINEAR")
    elif parallel:
        relations.append("PARALLEL")
    if perpendicular:
        relations.append("PERPENDICULAR")
    if intersection is not None and not collinear:
        relations.append("INTERSECTING")
    if not relations:
        relations.append("SKEW")

    return {
        "schema": "OLEANDER_INFERENCE_LINE_RELATION_v0.1",
        "relations": relations,
        "acute_angle_degrees": angle,
        "parallel": parallel,
        "perpendicular": perpendicular,
        "collinear": collinear,
        "intersecting": intersection is not None,
        "line_offset_mm": scene_units_to_mm(scene, line_offset_scene),
        "closest_distance_mm": scene_units_to_mm(scene, closest_distance_scene),
        "intersection_world_scene": [float(v) for v in intersection] if intersection is not None else None,
        "intersection_world_mm": [scene_units_to_mm(scene, v) for v in intersection] if intersection is not None else None,
        "linear_tolerance_mm": linear_tolerance_mm,
        "angular_tolerance_deg": angular_tolerance_deg,
        "authority": "GEOMETRIC_INFERENCE_CHECK_ONLY_NO_CONSTRAINT_SOLVER",
    }


def mesh_edge_world_line(obj, edge_index):
    if obj.type != "MESH" or obj.data is None:
        raise ValueError("edge inference requires a mesh object")
    edge_index = int(edge_index)
    if edge_index < 0 or edge_index >= len(obj.data.edges):
        raise ValueError("edge index out of range")
    edge = obj.data.edges[edge_index]
    p0 = obj.matrix_world @ obj.data.vertices[edge.vertices[0]].co
    p1 = obj.matrix_world @ obj.data.vertices[edge.vertices[1]].co
    direction = p1 - p0
    if direction.length <= 1e-12:
        raise ValueError("edge has zero world-space length")
    return p0, direction


def compare_mesh_edges(scene, obj_a, edge_a, obj_b, edge_b, linear_tolerance_mm=0.1, angular_tolerance_deg=0.1):
    p1, d1 = mesh_edge_world_line(obj_a, edge_a)
    p2, d2 = mesh_edge_world_line(obj_b, edge_b)
    result = analyze_infinite_lines(scene, p1, d1, p2, d2, linear_tolerance_mm, angular_tolerance_deg)
    result.update({
        "a": object_id(obj_a) or obj_a.name,
        "a_edge": int(edge_a),
        "b": object_id(obj_b) or obj_b.name,
        "b_edge": int(edge_b),
    })
    return result


def extension_line_candidate(scene, obj, edge_index, target_world, snap_radius_mm):
    """Project a target to an edge's infinite line, but only outside the finite edge segment."""
    snap_radius_mm = float(snap_radius_mm)
    if snap_radius_mm <= 0.0:
        raise ValueError("snap radius must be positive")
    p0, direction = mesh_edge_world_line(obj, edge_index)
    target = Vector(target_world)
    length_sq = direction.length_squared
    parameter = (target - p0).dot(direction) / length_sq
    projection = p0 + direction * parameter
    distance_mm = scene_units_to_mm(scene, (target - projection).length)
    if 0.0 <= parameter <= 1.0 or distance_mm > snap_radius_mm:
        return None
    return {
        "kind": "EXTENSION",
        "object": object_id(obj) or obj.name,
        "edge_index": int(edge_index),
        "edge_parameter": float(parameter),
        "world_scene": [float(v) for v in projection],
        "world_mm": [scene_units_to_mm(scene, v) for v in projection],
        "distance_to_target_mm": distance_mm,
        "snap_radius_mm": snap_radius_mm,
        "authority": "TEMPORARY_INFERENCE_CANDIDATE_NO_CONSTRAINT",
    }


def axis_lock_projection(scene, anchor_world, target_world, axis):
    axis = str(axis).upper()
    vectors = {"X": Vector((1.0, 0.0, 0.0)), "Y": Vector((0.0, 1.0, 0.0)), "Z": Vector((0.0, 0.0, 1.0))}
    if axis not in vectors:
        raise ValueError("axis must be X, Y or Z")
    anchor = Vector(anchor_world)
    target = Vector(target_world)
    direction = vectors[axis]
    projected = anchor + direction * (target - anchor).dot(direction)
    return {
        "schema": "OLEANDER_AXIS_LOCK_PROJECTION_v0.1",
        "axis": axis,
        "anchor_world_scene": [float(v) for v in anchor],
        "target_world_scene": [float(v) for v in target],
        "projected_world_scene": [float(v) for v in projected],
        "projected_world_mm": [scene_units_to_mm(scene, v) for v in projected],
        "authority": "TRANSIENT_AXIS_INFERENCE_NO_TRANSFORM_MUTATION",
    }


def _tracking_points(scene):
    raw = scene.get(TRACKING_POINTS_KEY, "[]")
    try:
        data = json.loads(raw) if isinstance(raw, str) else []
    except json.JSONDecodeError:
        data = []
    return data if isinstance(data, list) else []


def tracking_points(scene):
    return list(_tracking_points(scene))


def add_tracking_point(scene, world_point, label=""):
    points = _tracking_points(scene)
    highest = 0
    for item in points:
        token = str(item.get("tracking_id", ""))
        if token.startswith("OLE_TRACK::T"):
            try:
                highest = max(highest, int(token.rsplit("T", 1)[1]))
            except ValueError:
                pass
    point = Vector(world_point)
    record = {
        "tracking_id": f"OLE_TRACK::T{highest + 1:04d}",
        "label": str(label or ""),
        "world_scene": [float(v) for v in point],
        "world_mm": [scene_units_to_mm(scene, v) for v in point],
        "authority": "TEMPORARY_TRACKING_POINT_NO_GEOMETRY_AUTHORITY",
    }
    points.append(record)
    scene[TRACKING_POINTS_KEY] = json.dumps(points, sort_keys=True)
    return record


def remove_tracking_point(scene, tracking_id):
    points = _tracking_points(scene)
    kept = [item for item in points if item.get("tracking_id") != tracking_id]
    if len(kept) == len(points):
        raise ValueError("tracking point not found")
    scene[TRACKING_POINTS_KEY] = json.dumps(kept, sort_keys=True)
    return True


def clear_tracking_points(scene):
    count = len(_tracking_points(scene))
    scene[TRACKING_POINTS_KEY] = "[]"
    return count


def nearest_tracking_point(scene, target_world, snap_radius_mm):
    snap_radius_mm = float(snap_radius_mm)
    if snap_radius_mm <= 0.0:
        raise ValueError("snap radius must be positive")
    target = Vector(target_world)
    best = None
    best_distance = None
    for item in _tracking_points(scene):
        point = Vector(item["world_scene"])
        distance_mm = scene_units_to_mm(scene, (point - target).length)
        if distance_mm <= snap_radius_mm and (best_distance is None or distance_mm < best_distance):
            best = dict(item)
            best_distance = distance_mm
    if best is not None:
        best["distance_to_target_mm"] = best_distance
        best["snap_radius_mm"] = snap_radius_mm
    return best


def inference_v2_snapshot(scene):
    result = {
        "schema": "OLEANDER_INFERENCE_V2_SNAPSHOT_v0.1",
        "tracking_points": _tracking_points(scene),
        "tracking_point_count": len(_tracking_points(scene)),
        "authority": "INFERENCE_STATE_ONLY_NO_CONSTRAINT_SOLVER",
    }
    scene[INFERENCE_V2_SNAPSHOT_KEY] = json.dumps(result, sort_keys=True)
    return result


class OLEANDER_OT_add_cursor_tracking_point(bpy.types.Operator):
    bl_idname = "oleander.add_cursor_tracking_point"
    bl_label = "Track 3D Cursor"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        record = add_tracking_point(context.scene, context.scene.cursor.location)
        self.report({"INFO"}, f"Added {record['tracking_id']}")
        return {"FINISHED"}


class OLEANDER_OT_clear_tracking_points(bpy.types.Operator):
    bl_idname = "oleander.clear_tracking_points"
    bl_label = "Clear Tracking Points"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        count = clear_tracking_points(context.scene)
        self.report({"INFO"}, f"Cleared {count} tracking point(s)")
        return {"FINISHED"}


class OLEANDER_OT_inference_v2_snapshot(bpy.types.Operator):
    bl_idname = "oleander.inference_v2_snapshot"
    bl_label = "Inference v2 Snapshot"
    bl_options = {"REGISTER"}

    def execute(self, context):
        result = inference_v2_snapshot(context.scene)
        self.report({"INFO"}, f"Inference v2: {result['tracking_point_count']} tracking point(s)")
        return {"FINISHED"}


class OLEANDER_PT_inference_v2(bpy.types.Panel):
    bl_label = "Inference Engine v2"
    bl_idname = "OLEANDER_PT_inference_v2"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        layout.label(text=f"Tracking points: {len(_tracking_points(context.scene))}")
        row = layout.row(align=True)
        row.operator("oleander.add_cursor_tracking_point", text="Track Cursor")
        row.operator("oleander.clear_tracking_points", text="Clear")
        layout.operator("oleander.inference_v2_snapshot", text="Snapshot")
        layout.label(text="Parallel / perpendicular / collinear / intersection", icon="INFO")
        layout.label(text="Checks + transient inference; no solver", icon="INFO")


OPERATOR_CLASSES = (
    OLEANDER_OT_add_cursor_tracking_point,
    OLEANDER_OT_clear_tracking_points,
    OLEANDER_OT_inference_v2_snapshot,
)
PANEL_CLASSES = (OLEANDER_PT_inference_v2,)
