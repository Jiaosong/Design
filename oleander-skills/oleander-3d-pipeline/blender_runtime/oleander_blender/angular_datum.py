"""OLEANDER angular measurement, datum and construction-guide foundation.

This module adds deterministic angle quantize/nudge plus editable reference-only
angle/datum/construction guides. These guides aid modeling but never become
model-geometry, field, engineering, manufacturing or CAD constraint authority.
"""

from __future__ import annotations

import math

import bpy
from mathutils import Vector

from .dependency import mark_downstream_stale, object_id
from .measurement_system import GUIDE_COLLECTION, mm_to_scene_units


ANGLE_STEP_ITEMS = (
    ("0.1", "0.1°", "Fine product/surface adjustment"),
    ("0.5", "0.5°", "Fine mechanical/product adjustment"),
    ("1", "1°", "General precision rotation"),
    ("5", "5°", "General design rotation"),
    ("15", "15°", "Architectural/spatial rotation"),
    ("30", "30°", "Coarse angular layout"),
    ("45", "45°", "Orthogonal diagonal layout"),
    ("90", "90°", "Orthogonal layout"),
)

AXIS_ITEMS = (("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""))
PLANE_ITEMS = (("XY", "XY", ""), ("XZ", "XZ", ""), ("YZ", "YZ", ""))
ORIGIN_ITEMS = (
    ("WORLD_ORIGIN", "World Origin", "Use world origin"),
    ("CURSOR", "3D Cursor", "Use 3D cursor"),
    ("ACTIVE_ORIGIN", "Active Origin", "Use active object origin"),
)


def _reject_transform_authority(obj):
    if len(obj.constraints):
        raise ValueError(f"{obj.name} has external transform authority via Blender constraints")


def _guide_collection(scene):
    collection = bpy.data.collections.get(GUIDE_COLLECTION)
    if collection is None:
        collection = bpy.data.collections.new(GUIDE_COLLECTION)
    if collection.name not in scene.collection.children:
        try:
            scene.collection.children.link(collection)
        except RuntimeError:
            pass
    collection.hide_render = True
    return collection


def _origin(context, origin_mode):
    if origin_mode == "WORLD_ORIGIN":
        return Vector((0.0, 0.0, 0.0))
    if origin_mode == "CURSOR":
        return context.scene.cursor.location.copy()
    if origin_mode == "ACTIVE_ORIGIN":
        if context.active_object is None:
            raise ValueError("Active Origin guide requires an active object")
        context.view_layer.update()
        return context.active_object.matrix_world.translation.copy()
    raise ValueError(f"unsupported guide origin mode: {origin_mode}")


def _next_guide_id(scene, kind):
    key = "oleander_guide_counter"
    counter = int(scene.get(key, 0)) + 1
    scene[key] = counter
    return f"OLE_GUIDE::{kind}::{counter:04d}"


def _mark_reference(obj, guide_id, kind):
    obj.hide_render = True
    obj.show_in_front = True
    obj["oleander_reference_guide"] = True
    obj["oleander_guide_id"] = guide_id
    obj["oleander_guide_kind"] = kind
    obj["oleander_guide_authority"] = "REFERENCE_ONLY_NOT_MODEL_GEOMETRY"


def quantize_world_rotation(scene, objects, step_degrees, axes=(True, True, True)):
    """Quantize object world Euler rotation after whole-batch authority preflight."""
    step_degrees = float(step_degrees)
    if step_degrees <= 0.0 or step_degrees > 360.0:
        raise ValueError("rotation step must be > 0 and <= 360 degrees")
    batch = list(objects)
    for obj in batch:
        _reject_transform_authority(obj)
    step = math.radians(step_degrees)
    results = []
    for obj in batch:
        matrix = obj.matrix_world.copy()
        before = matrix.to_euler(obj.rotation_mode if obj.rotation_mode != "QUATERNION" else "XYZ")
        after = before.copy()
        for index, enabled in enumerate(axes):
            if enabled:
                after[index] = round(before[index] / step) * step
        location = matrix.translation.copy()
        scale = matrix.to_scale()
        obj.rotation_mode = "XYZ"
        obj.rotation_euler = after
        obj.location = location
        obj.scale = scale
        results.append({
            "name": obj.name,
            "ole_id": object_id(obj),
            "before_degrees": [math.degrees(value) for value in before],
            "after_degrees": [math.degrees(value) for value in after],
            "step_degrees": step_degrees,
        })
    for view_layer in scene.view_layers:
        view_layer.update()
    for item in results:
        if item["ole_id"]:
            mark_downstream_stale([item["ole_id"]], reason="ANGULAR_QUANTIZE_ROTATION", scene=scene)
    return results


def nudge_world_rotation(scene, obj, axis, amount_degrees):
    if axis not in {"X", "Y", "Z"}:
        raise ValueError(f"unsupported rotation axis: {axis}")
    _reject_transform_authority(obj)
    amount_degrees = float(amount_degrees)
    index = {"X": 0, "Y": 1, "Z": 2}[axis]
    obj.rotation_mode = "XYZ"
    before = obj.rotation_euler.copy()
    obj.rotation_euler[index] += math.radians(amount_degrees)
    for view_layer in scene.view_layers:
        view_layer.update()
    oid = object_id(obj)
    downstream = mark_downstream_stale([oid], reason="ANGULAR_NUDGE_ROTATION", scene=scene) if oid else []
    return {
        "name": obj.name,
        "ole_id": oid,
        "axis": axis,
        "amount_degrees": amount_degrees,
        "before_degrees": [math.degrees(v) for v in before],
        "after_degrees": [math.degrees(v) for v in obj.rotation_euler],
        "downstream_stale": downstream,
    }


def create_angle_guide(context, plane, radius_mm, sweep_degrees, minor_step_degrees=5.0, major_every=3, origin_mode="WORLD_ORIGIN", labels=True):
    if plane not in {"XY", "XZ", "YZ"}:
        raise ValueError(f"unsupported angle-guide plane: {plane}")
    radius_mm = float(radius_mm)
    sweep_degrees = float(sweep_degrees)
    minor_step_degrees = float(minor_step_degrees)
    major_every = int(major_every)
    if radius_mm <= 0.0:
        raise ValueError("angle-guide radius must be positive")
    if not (0.0 < sweep_degrees <= 360.0):
        raise ValueError("angle-guide sweep must be > 0 and <= 360 degrees")
    if minor_step_degrees <= 0.0 or major_every < 1:
        raise ValueError("angle-guide minor step must be positive and major_every >= 1")
    ratio = sweep_degrees / minor_step_degrees
    intervals = int(round(ratio))
    if abs(ratio - intervals) > 1e-8:
        raise ValueError("angle-guide sweep must be an integer multiple of minor angle step")
    if intervals > 720:
        raise ValueError("angle-guide would exceed 720 angular intervals")

    scene = context.scene
    origin = _origin(context, origin_mode)
    radius = mm_to_scene_units(scene, radius_mm)
    minor_tick = mm_to_scene_units(scene, max(1.0, min(10.0, radius_mm * 0.03)))
    major_tick = minor_tick * 2.0
    guide_id = _next_guide_id(scene, "ANGLE")

    def point(angle_rad, r):
        c, s = math.cos(angle_rad), math.sin(angle_rad)
        if plane == "XY":
            return Vector((r * c, r * s, 0.0))
        if plane == "XZ":
            return Vector((r * c, 0.0, r * s))
        return Vector((0.0, r * c, r * s))

    vertices = [Vector((0.0, 0.0, 0.0))]
    edges = []
    arc_indices = []
    for index in range(intervals + 1):
        angle = math.radians(minor_step_degrees * index)
        arc_indices.append(len(vertices))
        vertices.append(point(angle, radius))
        if index:
            edges.append((arc_indices[-2], arc_indices[-1]))
        tick_len = major_tick if index % major_every == 0 else minor_tick
        inner = point(angle, radius - tick_len)
        inner_index = len(vertices)
        vertices.append(inner)
        edges.append((arc_indices[-1], inner_index))
    edges.append((0, arc_indices[0]))
    edges.append((0, arc_indices[-1]))

    mesh = bpy.data.meshes.new(f"{guide_id}_MESH")
    mesh.from_pydata([tuple(v) for v in vertices], edges, [])
    mesh.update()
    obj = bpy.data.objects.new(guide_id, mesh)
    obj.location = origin
    obj.display_type = "WIRE"
    _mark_reference(obj, guide_id, "ANGLE_GUIDE")
    obj["oleander_angle_plane"] = plane
    obj["oleander_angle_radius_mm"] = radius_mm
    obj["oleander_angle_sweep_degrees"] = sweep_degrees
    obj["oleander_angle_minor_step_degrees"] = minor_step_degrees
    obj["oleander_angle_major_every"] = major_every
    obj["oleander_angle_intervals"] = intervals
    collection = _guide_collection(scene)
    collection.objects.link(obj)

    label_names = []
    if labels:
        for index in range(0, intervals + 1, major_every):
            value = minor_step_degrees * index
            curve = bpy.data.curves.new(f"{guide_id}_LABEL_{index:03d}", type="FONT")
            curve.body = f"{value:g}°"
            curve.align_x = "CENTER"
            curve.size = mm_to_scene_units(scene, max(5.0, min(20.0, radius_mm * 0.06)))
            label = bpy.data.objects.new(f"{guide_id}_LABEL_{index:03d}", curve)
            label.location = origin + point(math.radians(value), radius + major_tick * 2.2)
            _mark_reference(label, guide_id, "ANGLE_LABEL")
            label["oleander_guide_parent_id"] = guide_id
            collection.objects.link(label)
            label_names.append(label.name)
    obj["oleander_angle_labels"] = str(label_names)
    return obj


def create_datum_axis(context, axis, length_mm, origin_mode="WORLD_ORIGIN"):
    if axis not in {"X", "Y", "Z"}:
        raise ValueError(f"unsupported datum axis: {axis}")
    length_mm = float(length_mm)
    if length_mm <= 0.0:
        raise ValueError("datum-axis length must be positive")
    scene = context.scene
    origin = _origin(context, origin_mode)
    half = mm_to_scene_units(scene, length_mm) * 0.5
    direction = Vector((1.0, 0.0, 0.0)) if axis == "X" else Vector((0.0, 1.0, 0.0)) if axis == "Y" else Vector((0.0, 0.0, 1.0))
    guide_id = _next_guide_id(scene, "DATUM_AXIS")
    mesh = bpy.data.meshes.new(f"{guide_id}_MESH")
    mesh.from_pydata([tuple(-direction * half), tuple(direction * half)], [(0, 1)], [])
    mesh.update()
    obj = bpy.data.objects.new(guide_id, mesh)
    obj.location = origin
    obj.display_type = "WIRE"
    _mark_reference(obj, guide_id, "DATUM_AXIS")
    obj["oleander_datum_axis"] = axis
    obj["oleander_datum_length_mm"] = length_mm
    obj["oleander_datum_origin_mode"] = origin_mode
    _guide_collection(scene).objects.link(obj)
    return obj


def create_datum_plane(context, plane, size_mm, origin_mode="WORLD_ORIGIN"):
    if plane not in {"XY", "XZ", "YZ"}:
        raise ValueError(f"unsupported datum plane: {plane}")
    size_mm = float(size_mm)
    if size_mm <= 0.0:
        raise ValueError("datum-plane size must be positive")
    scene = context.scene
    origin = _origin(context, origin_mode)
    half = mm_to_scene_units(scene, size_mm) * 0.5
    if plane == "XY":
        vertices = [(-half, -half, 0), (half, -half, 0), (half, half, 0), (-half, half, 0)]
    elif plane == "XZ":
        vertices = [(-half, 0, -half), (half, 0, -half), (half, 0, half), (-half, 0, half)]
    else:
        vertices = [(0, -half, -half), (0, half, -half), (0, half, half), (0, -half, half)]
    guide_id = _next_guide_id(scene, "DATUM_PLANE")
    mesh = bpy.data.meshes.new(f"{guide_id}_MESH")
    mesh.from_pydata(vertices, [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)], [])
    mesh.update()
    obj = bpy.data.objects.new(guide_id, mesh)
    obj.location = origin
    obj.display_type = "WIRE"
    _mark_reference(obj, guide_id, "DATUM_PLANE")
    obj["oleander_datum_plane"] = plane
    obj["oleander_datum_size_mm"] = size_mm
    obj["oleander_datum_origin_mode"] = origin_mode
    _guide_collection(scene).objects.link(obj)
    return obj


def create_construction_line(context, axis, length_mm, offset_mm=0.0, origin_mode="WORLD_ORIGIN"):
    if axis not in {"X", "Y", "Z"}:
        raise ValueError(f"unsupported construction-line axis: {axis}")
    length_mm = float(length_mm)
    offset_mm = float(offset_mm)
    if length_mm <= 0.0:
        raise ValueError("construction-line length must be positive")
    scene = context.scene
    origin = _origin(context, origin_mode)
    length = mm_to_scene_units(scene, length_mm)
    offset = mm_to_scene_units(scene, offset_mm)
    if axis == "X":
        vertices = [(0, offset, 0), (length, offset, 0)]
    elif axis == "Y":
        vertices = [(offset, 0, 0), (offset, length, 0)]
    else:
        vertices = [(offset, 0, 0), (offset, 0, length)]
    guide_id = _next_guide_id(scene, "CONSTRUCTION")
    mesh = bpy.data.meshes.new(f"{guide_id}_MESH")
    mesh.from_pydata(vertices, [(0, 1)], [])
    mesh.update()
    obj = bpy.data.objects.new(guide_id, mesh)
    obj.location = origin
    obj.display_type = "WIRE"
    _mark_reference(obj, guide_id, "CONSTRUCTION_LINE")
    obj["oleander_construction_axis"] = axis
    obj["oleander_construction_length_mm"] = length_mm
    obj["oleander_construction_offset_mm"] = offset_mm
    obj["oleander_construction_origin_mode"] = origin_mode
    _guide_collection(scene).objects.link(obj)
    return obj


class OLEANDER_OT_quantize_rotation(bpy.types.Operator):
    bl_idname = "oleander.quantize_rotation"
    bl_label = "Quantize Rotation"
    bl_options = {"REGISTER", "UNDO"}

    step_degrees: bpy.props.EnumProperty(name="Step", items=ANGLE_STEP_ITEMS, default="15")
    axis_x: bpy.props.BoolProperty(name="X", default=True)
    axis_y: bpy.props.BoolProperty(name="Y", default=True)
    axis_z: bpy.props.BoolProperty(name="Z", default=True)

    def execute(self, context):
        try:
            quantize_world_rotation(context.scene, context.selected_objects, float(self.step_degrees), (self.axis_x, self.axis_y, self.axis_z))
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_nudge_rotation(bpy.types.Operator):
    bl_idname = "oleander.nudge_rotation"
    bl_label = "Nudge Rotation"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(name="Axis", items=AXIS_ITEMS, default="Z")
    amount_degrees: bpy.props.FloatProperty(name="Degrees", default=5.0, precision=3)

    def execute(self, context):
        if context.active_object is None:
            self.report({"ERROR"}, "Select an active object")
            return {"CANCELLED"}
        try:
            nudge_world_rotation(context.scene, context.active_object, self.axis, self.amount_degrees)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_create_angle_guide(bpy.types.Operator):
    bl_idname = "oleander.create_angle_guide"
    bl_label = "Create Angle Guide"
    bl_options = {"REGISTER", "UNDO"}

    plane: bpy.props.EnumProperty(name="Plane", items=PLANE_ITEMS, default="XY")
    radius_mm: bpy.props.FloatProperty(name="Radius mm", default=500.0, min=0.001)
    sweep_degrees: bpy.props.FloatProperty(name="Sweep °", default=90.0, min=0.001, max=360.0)
    minor_step_degrees: bpy.props.FloatProperty(name="Minor °", default=5.0, min=0.001)
    major_every: bpy.props.IntProperty(name="Major Every", default=3, min=1)
    origin_mode: bpy.props.EnumProperty(name="Origin", items=ORIGIN_ITEMS, default="WORLD_ORIGIN")
    labels: bpy.props.BoolProperty(name="Labels", default=True)

    def execute(self, context):
        try:
            create_angle_guide(context, self.plane, self.radius_mm, self.sweep_degrees, self.minor_step_degrees, self.major_every, self.origin_mode, self.labels)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_create_datum_axis(bpy.types.Operator):
    bl_idname = "oleander.create_datum_axis"
    bl_label = "Create Datum Axis"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(name="Axis", items=AXIS_ITEMS, default="X")
    length_mm: bpy.props.FloatProperty(name="Length mm", default=3000.0, min=0.001)
    origin_mode: bpy.props.EnumProperty(name="Origin", items=ORIGIN_ITEMS, default="WORLD_ORIGIN")

    def execute(self, context):
        try:
            create_datum_axis(context, self.axis, self.length_mm, self.origin_mode)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_create_datum_plane(bpy.types.Operator):
    bl_idname = "oleander.create_datum_plane"
    bl_label = "Create Datum Plane"
    bl_options = {"REGISTER", "UNDO"}

    plane: bpy.props.EnumProperty(name="Plane", items=PLANE_ITEMS, default="XY")
    size_mm: bpy.props.FloatProperty(name="Size mm", default=2000.0, min=0.001)
    origin_mode: bpy.props.EnumProperty(name="Origin", items=ORIGIN_ITEMS, default="WORLD_ORIGIN")

    def execute(self, context):
        try:
            create_datum_plane(context, self.plane, self.size_mm, self.origin_mode)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_OT_create_construction_line(bpy.types.Operator):
    bl_idname = "oleander.create_construction_line"
    bl_label = "Create Construction Line"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(name="Axis", items=AXIS_ITEMS, default="X")
    length_mm: bpy.props.FloatProperty(name="Length mm", default=3000.0, min=0.001)
    offset_mm: bpy.props.FloatProperty(name="Offset mm", default=0.0)
    origin_mode: bpy.props.EnumProperty(name="Origin", items=ORIGIN_ITEMS, default="WORLD_ORIGIN")

    def execute(self, context):
        try:
            create_construction_line(context, self.axis, self.length_mm, self.offset_mm, self.origin_mode)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        return {"FINISHED"}


class OLEANDER_PT_angular_datum(bpy.types.Panel):
    bl_label = "Angular + Datum"
    bl_idname = "OLEANDER_PT_angular_datum"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Deterministic angular tools")
        row = layout.row(align=True)
        row.operator("oleander.quantize_rotation", text="Angle Snap")
        row.operator("oleander.nudge_rotation", text="Angle Nudge")
        guides = layout.box()
        guides.label(text="Reference-only construction")
        guides.operator("oleander.create_angle_guide", text="Angle Guide")
        row = guides.row(align=True)
        row.operator("oleander.create_datum_axis", text="Datum Axis")
        row.operator("oleander.create_datum_plane", text="Datum Plane")
        guides.operator("oleander.create_construction_line", text="Construction Line")
        guides.label(text="Guides are not dimensional/field authority", icon="INFO")


OPERATOR_CLASSES = (
    OLEANDER_OT_quantize_rotation,
    OLEANDER_OT_nudge_rotation,
    OLEANDER_OT_create_angle_guide,
    OLEANDER_OT_create_datum_axis,
    OLEANDER_OT_create_datum_plane,
    OLEANDER_OT_create_construction_line,
)

PANEL_CLASSES = (OLEANDER_PT_angular_datum,)
