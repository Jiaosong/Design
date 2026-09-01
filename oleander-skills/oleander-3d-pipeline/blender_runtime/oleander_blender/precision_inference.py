"""OLEANDER precision display, component measurement and inference candidates.

Display precision changes formatting only. BBox clearance is explicitly an
axis-aligned approximation, not true surface clearance. Mesh inference exposes
world-space endpoint/midpoint/face-center/origin candidates without claiming a
CAD sketch solver or persistent geometric constraints.
"""

from __future__ import annotations

import json
import math

import bpy
from mathutils import Vector

from .measurement_system import scene_units_to_mm, mm_to_scene_units
from .dependency import object_id

LINEAR_DECIMALS_KEY = "oleander_display_linear_decimals"
ANGLE_DECIMALS_KEY = "oleander_display_angle_decimals"
PRECISION_SNAPSHOT_KEY = "oleander_precision_snapshot"


def set_display_precision(scene, linear_decimals=2, angle_decimals=2):
    linear_decimals = int(linear_decimals)
    angle_decimals = int(angle_decimals)
    if not 0 <= linear_decimals <= 6:
        raise ValueError("linear display decimals must be between 0 and 6")
    if not 0 <= angle_decimals <= 6:
        raise ValueError("angle display decimals must be between 0 and 6")
    scene[LINEAR_DECIMALS_KEY] = linear_decimals
    scene[ANGLE_DECIMALS_KEY] = angle_decimals
    return {"linear_decimals": linear_decimals, "angle_decimals": angle_decimals}


def display_precision(scene):
    return {
        "linear_decimals": int(scene.get(LINEAR_DECIMALS_KEY, 2)),
        "angle_decimals": int(scene.get(ANGLE_DECIMALS_KEY, 2)),
    }


def format_mm(scene, value_mm):
    digits = display_precision(scene)["linear_decimals"]
    return f"{float(value_mm):.{digits}f} mm"


def format_degrees(scene, value_degrees):
    digits = display_precision(scene)["angle_decimals"]
    return f"{float(value_degrees):.{digits}f}°"


def component_measurement(scene, a, b):
    delta = b.matrix_world.translation - a.matrix_world.translation
    delta_mm = [scene_units_to_mm(scene, value) for value in delta]
    distance_mm = scene_units_to_mm(scene, delta.length)
    precision = display_precision(scene)
    return {
        "schema": "OLEANDER_COMPONENT_MEASUREMENT_v0.1",
        "a": object_id(a) or a.name,
        "b": object_id(b) or b.name,
        "signed_delta_mm": delta_mm,
        "absolute_delta_mm": [abs(value) for value in delta_mm],
        "origin_distance_mm": distance_mm,
        "formatted": {
            "dx": format_mm(scene, delta_mm[0]),
            "dy": format_mm(scene, delta_mm[1]),
            "dz": format_mm(scene, delta_mm[2]),
            "distance": format_mm(scene, distance_mm),
        },
        "display_precision": precision,
        "authority": "WORLD_ORIGIN_MEASUREMENT",
    }


def _world_bbox_minmax(obj):
    points = [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]
    mins = Vector(tuple(min(point[i] for point in points) for i in range(3)))
    maxs = Vector(tuple(max(point[i] for point in points) for i in range(3)))
    return mins, maxs


def bbox_clearance(scene, a, b):
    """Axis-aligned world-bounding-box separation; never true surface clearance."""
    amin, amax = _world_bbox_minmax(a)
    bmin, bmax = _world_bbox_minmax(b)
    gaps = []
    overlaps = []
    for axis in range(3):
        if amax[axis] < bmin[axis]:
            gap = bmin[axis] - amax[axis]
            overlap = 0.0
        elif bmax[axis] < amin[axis]:
            gap = amin[axis] - bmax[axis]
            overlap = 0.0
        else:
            gap = 0.0
            overlap = min(amax[axis], bmax[axis]) - max(amin[axis], bmin[axis])
        gaps.append(scene_units_to_mm(scene, gap))
        overlaps.append(scene_units_to_mm(scene, overlap))
    separated_axes = [index for index, value in enumerate(gaps) if value > 0.0]
    euclidean_lower_bound = math.sqrt(sum(gaps[index] ** 2 for index in separated_axes))
    return {
        "schema": "OLEANDER_BBOX_CLEARANCE_v0.1",
        "a": object_id(a) or a.name,
        "b": object_id(b) or b.name,
        "axis_gap_mm": gaps,
        "axis_overlap_mm": overlaps,
        "bbox_separation_lower_bound_mm": euclidean_lower_bound,
        "intersecting_aabbs": not separated_axes,
        "authority": "AABB_APPROXIMATION_ONLY_NOT_SURFACE_CLEARANCE",
    }


def mesh_inference_candidates(scene, obj, include_origin=True, max_candidates=10000):
    if obj.type != "MESH" or obj.data is None:
        raise ValueError("inference candidates require a mesh object")
    if max_candidates < 1:
        raise ValueError("max_candidates must be positive")
    candidates = []

    def add(kind, element_index, point):
        if len(candidates) >= max_candidates:
            raise ValueError(f"inference candidate count exceeds {max_candidates}")
        world = obj.matrix_world @ point if point is not None else obj.matrix_world.translation.copy()
        candidates.append({
            "kind": kind,
            "element_index": element_index,
            "world_scene": [float(v) for v in world],
            "world_mm": [scene_units_to_mm(scene, v) for v in world],
        })

    if include_origin:
        add("ORIGIN", -1, None)
    for vertex in obj.data.vertices:
        add("ENDPOINT", vertex.index, vertex.co)
    for edge in obj.data.edges:
        midpoint = (obj.data.vertices[edge.vertices[0]].co + obj.data.vertices[edge.vertices[1]].co) * 0.5
        add("MIDPOINT", edge.index, midpoint)
    for polygon in obj.data.polygons:
        add("FACE_CENTER", polygon.index, polygon.center)
    return {
        "schema": "OLEANDER_INFERENCE_CANDIDATES_v0.1",
        "object": object_id(obj) or obj.name,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "authority": "SNAP_CANDIDATE_ONLY_NO_CONSTRAINT_SOLVER",
    }


def nearest_inference_candidate(scene, obj, target_world, snap_radius_mm, allowed_kinds=None):
    snap_radius_mm = float(snap_radius_mm)
    if snap_radius_mm <= 0.0:
        raise ValueError("snap radius must be positive")
    target = Vector(target_world)
    data = mesh_inference_candidates(scene, obj)
    allowed = set(allowed_kinds or ("ORIGIN", "ENDPOINT", "MIDPOINT", "FACE_CENTER"))
    best = None
    best_distance = None
    for item in data["candidates"]:
        if item["kind"] not in allowed:
            continue
        point = Vector(item["world_scene"])
        distance_mm = scene_units_to_mm(scene, (point - target).length)
        if distance_mm <= snap_radius_mm and (best_distance is None or distance_mm < best_distance):
            best = dict(item)
            best_distance = distance_mm
    if best is None:
        return None
    best["distance_to_target_mm"] = best_distance
    best["snap_radius_mm"] = snap_radius_mm
    return best


def precision_snapshot(scene, selected_objects, active_object=None):
    selected = list(selected_objects)
    active = active_object if active_object in selected else (selected[0] if selected else None)
    result = {
        "schema": "OLEANDER_PRECISION_SNAPSHOT_v0.1",
        "display_precision": display_precision(scene),
        "selected_count": len(selected),
    }
    if len(selected) == 2:
        result["component_measurement"] = component_measurement(scene, selected[0], selected[1])
        result["bbox_clearance"] = bbox_clearance(scene, selected[0], selected[1])
    if active is not None and active.type == "MESH":
        candidates = mesh_inference_candidates(scene, active)
        result["active_inference_summary"] = {
            "object": candidates["object"],
            "candidate_count": candidates["candidate_count"],
            "counts": {
                kind: sum(1 for item in candidates["candidates"] if item["kind"] == kind)
                for kind in ("ORIGIN", "ENDPOINT", "MIDPOINT", "FACE_CENTER")
            },
            "authority": candidates["authority"],
        }
    scene[PRECISION_SNAPSHOT_KEY] = json.dumps(result, sort_keys=True)
    return result


class OLEANDER_OT_set_display_precision(bpy.types.Operator):
    bl_idname = "oleander.set_display_precision"
    bl_label = "Set Display Precision"
    bl_options = {"REGISTER", "UNDO"}

    linear_decimals: bpy.props.IntProperty(name="Linear decimals", default=2, min=0, max=6)
    angle_decimals: bpy.props.IntProperty(name="Angle decimals", default=2, min=0, max=6)

    def execute(self, context):
        try:
            set_display_precision(context.scene, self.linear_decimals, self.angle_decimals)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_precision_snapshot(bpy.types.Operator):
    bl_idname = "oleander.precision_snapshot"
    bl_label = "Precision Snapshot"
    bl_options = {"REGISTER"}

    def execute(self, context):
        try:
            result = precision_snapshot(context.scene, context.selected_objects, context.active_object)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Precision snapshot: {result['selected_count']} selected")
        return {"FINISHED"}


class OLEANDER_PT_precision_inference(bpy.types.Panel):
    bl_label = "Precision + Inference"
    bl_idname = "OLEANDER_PT_precision_inference"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        values = display_precision(context.scene)
        layout.label(text=f"Linear {values['linear_decimals']} dp / Angle {values['angle_decimals']} dp")
        layout.operator("oleander.set_display_precision", text="Set Display Precision")
        layout.operator("oleander.precision_snapshot", text="Measure + Inference Snapshot")
        layout.label(text="BBox clearance = approximation only", icon="INFO")
        layout.label(text="Inference points do not create constraints", icon="INFO")


OPERATOR_CLASSES = (OLEANDER_OT_set_display_precision, OLEANDER_OT_precision_snapshot)
PANEL_CLASSES = (OLEANDER_PT_precision_inference,)
