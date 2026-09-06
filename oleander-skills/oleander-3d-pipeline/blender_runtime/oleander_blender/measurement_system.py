import json
import math

import bpy
from mathutils import Vector

from .dependency import mark_downstream_stale, object_id


PROFILE_KEY = "oleander_measurement_profile"
MINOR_STEP_KEY = "oleander_measurement_minor_step_mm"
MAJOR_EVERY_KEY = "oleander_measurement_major_every"
SNAP_STEP_KEY = "oleander_measurement_snap_step_mm"
DEFAULT_RULER_KEY = "oleander_measurement_default_ruler_mm"
SNAPSHOT_KEY = "oleander_measurement_snapshot"
EVENTS_KEY = "oleander_measurement_events"
EVENT_COUNTER_KEY = "oleander_measurement_event_counter"
GUIDE_COUNTER_KEY = "oleander_guide_counter"
GUIDE_COLLECTION = "OLEANDER_GUIDES"

PROFILES = {
    "PRODUCT_FINE": {
        "label": "Product Fine",
        "minor_step_mm": 0.5,
        "major_every": 10,
        "snap_step_mm": 0.5,
        "default_ruler_mm": 100.0,
    },
    "PRODUCT": {
        "label": "Product",
        "minor_step_mm": 1.0,
        "major_every": 10,
        "snap_step_mm": 1.0,
        "default_ruler_mm": 500.0,
    },
    "FURNITURE_INTERIOR": {
        "label": "Furniture / Interior",
        "minor_step_mm": 10.0,
        "major_every": 10,
        "snap_step_mm": 10.0,
        "default_ruler_mm": 3000.0,
    },
    "ARCHITECTURE": {
        "label": "Architecture",
        "minor_step_mm": 100.0,
        "major_every": 10,
        "snap_step_mm": 100.0,
        "default_ruler_mm": 10000.0,
    },
    "SITE": {
        "label": "Site / Landscape",
        "minor_step_mm": 1000.0,
        "major_every": 5,
        "snap_step_mm": 500.0,
        "default_ruler_mm": 50000.0,
    },
}

PROFILE_ITEMS = tuple((key, value["label"], "") for key, value in PROFILES.items())
AXIS_ITEMS = (("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""))
ORIGIN_ITEMS = (
    ("WORLD_ORIGIN", "World Origin", "Create the ruler at world origin"),
    ("CURSOR", "3D Cursor", "Create the ruler at the 3D cursor"),
    ("ACTIVE_ORIGIN", "Active Origin", "Create the ruler at the active object's world origin"),
)


def mm_to_scene_units(scene, value_mm):
    scale_length = scene.unit_settings.scale_length or 1.0
    return (float(value_mm) / 1000.0) / scale_length


def scene_units_to_mm(scene, value_scene):
    scale_length = scene.unit_settings.scale_length or 1.0
    return float(value_scene) * scale_length * 1000.0


def vector_scene_to_mm(scene, vector):
    return [scene_units_to_mm(scene, component) for component in vector]


def measurement_profile(scene):
    profile_id = scene.get(PROFILE_KEY, "FURNITURE_INTERIOR")
    return profile_id if profile_id in PROFILES else "FURNITURE_INTERIOR"


def profile_values(scene):
    profile = PROFILES[measurement_profile(scene)]
    return {
        "profile": measurement_profile(scene),
        "minor_step_mm": float(scene.get(MINOR_STEP_KEY, profile["minor_step_mm"])),
        "major_every": int(scene.get(MAJOR_EVERY_KEY, profile["major_every"])),
        "snap_step_mm": float(scene.get(SNAP_STEP_KEY, profile["snap_step_mm"])),
        "default_ruler_mm": float(scene.get(DEFAULT_RULER_KEY, profile["default_ruler_mm"])),
    }


def set_profile(scene, profile_id):
    if profile_id not in PROFILES:
        raise ValueError(f"unknown measurement profile: {profile_id}")
    profile = PROFILES[profile_id]
    scene[PROFILE_KEY] = profile_id
    scene[MINOR_STEP_KEY] = float(profile["minor_step_mm"])
    scene[MAJOR_EVERY_KEY] = int(profile["major_every"])
    scene[SNAP_STEP_KEY] = float(profile["snap_step_mm"])
    scene[DEFAULT_RULER_KEY] = float(profile["default_ruler_mm"])
    return profile_values(scene)


def _append_event(scene, action, payload=None):
    counter = int(scene.get(EVENT_COUNTER_KEY, 0)) + 1
    scene[EVENT_COUNTER_KEY] = counter
    event = {
        "event_id": f"OLE_MEASURE_EVT::E{counter:04d}",
        "event_index": counter,
        "action": action,
        "payload": payload or {},
    }
    try:
        events = json.loads(scene.get(EVENTS_KEY, "[]"))
    except (TypeError, json.JSONDecodeError):
        events = []
    if not isinstance(events, list):
        events = []
    events.append(event)
    scene[EVENTS_KEY] = json.dumps(events, sort_keys=True, ensure_ascii=False)
    return event


def measurement_events(scene):
    try:
        value = json.loads(scene.get(EVENTS_KEY, "[]"))
    except (TypeError, json.JSONDecodeError):
        return []
    return value if isinstance(value, list) else []


def _apply_viewport_grid(context, profile):
    screen = getattr(context, "screen", None)
    if screen is None:
        return 0
    major_step_scene = mm_to_scene_units(context.scene, profile["minor_step_mm"] * profile["major_every"])
    updated = 0
    for area in screen.areas:
        if area.type != "VIEW_3D":
            continue
        for space in area.spaces:
            if space.type != "VIEW_3D":
                continue
            space.overlay.grid_scale = max(major_step_scene, 1e-12)
            space.overlay.grid_subdivisions = max(1, min(1024, int(profile["major_every"])))
            updated += 1
    return updated


def _world_bbox_points(obj):
    return [obj.matrix_world @ Vector(corner) for corner in obj.bound_box]


def measurement_snapshot(scene, selected_objects, active_object=None):
    for view_layer in scene.view_layers:
        view_layer.update()
    selected = list(selected_objects)
    active = active_object if active_object in selected else (selected[0] if selected else None)
    snapshot = {
        "schema": "OLEANDER_MEASUREMENT_SNAPSHOT_v0.1",
        "profile": measurement_profile(scene),
        "unit_system": scene.unit_settings.system,
        "scale_length": scene.unit_settings.scale_length,
        "selected_count": len(selected),
    }
    if active is not None:
        origin = active.matrix_world.translation
        bbox = _world_bbox_points(active)
        mins = Vector((min(point[i] for point in bbox) for i in range(3)))
        maxs = Vector((max(point[i] for point in bbox) for i in range(3)))
        snapshot["active"] = {
            "name": active.name,
            "ole_id": object_id(active),
            "world_origin_mm": vector_scene_to_mm(scene, origin),
            "dimensions_mm": vector_scene_to_mm(scene, active.dimensions),
            "world_bbox_min_mm": vector_scene_to_mm(scene, mins),
            "world_bbox_max_mm": vector_scene_to_mm(scene, maxs),
        }
    if len(selected) == 2:
        a, b = selected
        delta = b.matrix_world.translation - a.matrix_world.translation
        snapshot["pair"] = {
            "a": object_id(a) or a.name,
            "b": object_id(b) or b.name,
            "origin_delta_mm": vector_scene_to_mm(scene, delta),
            "origin_distance_mm": scene_units_to_mm(scene, delta.length),
        }
    return snapshot


def _reject_transform_authority(obj):
    if len(obj.constraints):
        raise ValueError(f"{obj.name} has external transform authority via Blender constraints")


def quantize_world_location(scene, objects, step_mm, axes=(True, True, True)):
    if step_mm <= 0.0:
        raise ValueError("snap step must be positive")
    step_scene = mm_to_scene_units(scene, step_mm)
    if step_scene <= 0.0:
        raise ValueError("snap step resolves to a non-positive scene value")
    results = []
    for obj in objects:
        _reject_transform_authority(obj)
        matrix = obj.matrix_world.copy()
        before = matrix.translation.copy()
        after = before.copy()
        for index, enabled in enumerate(axes):
            if enabled:
                after[index] = round(before[index] / step_scene) * step_scene
        matrix.translation = after
        obj.matrix_world = matrix
        results.append({
            "name": obj.name,
            "ole_id": object_id(obj),
            "before_mm": vector_scene_to_mm(scene, before),
            "after_mm": vector_scene_to_mm(scene, after),
        })
    for view_layer in scene.view_layers:
        view_layer.update()
    for item in results:
        if item["ole_id"]:
            mark_downstream_stale([item["ole_id"]], reason="MEASUREMENT_QUANTIZE_LOCATION", scene=scene)
    return results


def nudge_world_location(scene, obj, axis, amount_mm):
    if axis not in {"X", "Y", "Z"}:
        raise ValueError(f"unsupported nudge axis: {axis}")
    _reject_transform_authority(obj)
    matrix = obj.matrix_world.copy()
    before = matrix.translation.copy()
    after = before.copy()
    after[{"X": 0, "Y": 1, "Z": 2}[axis]] += mm_to_scene_units(scene, amount_mm)
    matrix.translation = after
    obj.matrix_world = matrix
    for view_layer in scene.view_layers:
        view_layer.update()
    oid = object_id(obj)
    downstream = mark_downstream_stale([oid], reason="MEASUREMENT_NUDGE", scene=scene) if oid else []
    return {
        "name": obj.name,
        "ole_id": oid,
        "axis": axis,
        "amount_mm": float(amount_mm),
        "before_mm": vector_scene_to_mm(scene, before),
        "after_mm": vector_scene_to_mm(scene, after),
        "downstream_stale": downstream,
    }


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


def _ruler_origin(context, origin_mode):
    if origin_mode == "WORLD_ORIGIN":
        return Vector((0.0, 0.0, 0.0))
    if origin_mode == "CURSOR":
        return context.scene.cursor.location.copy()
    if origin_mode == "ACTIVE_ORIGIN":
        if context.active_object is None:
            raise ValueError("Active Origin ruler requires an active object")
        context.view_layer.update()
        return context.active_object.matrix_world.translation.copy()
    raise ValueError(f"unsupported ruler origin mode: {origin_mode}")


def _format_mm(value_mm):
    if abs(value_mm) >= 1000.0 and abs(value_mm / 1000.0 - round(value_mm / 1000.0)) <= 1e-9:
        return f"{value_mm / 1000.0:g} m"
    return f"{value_mm:g} mm"


def create_ruler_guide(context, axis, length_mm, minor_step_mm, major_every, origin_mode="WORLD_ORIGIN", labels=True, label_every_major=1):
    if axis not in {"X", "Y", "Z"}:
        raise ValueError(f"unsupported ruler axis: {axis}")
    if length_mm <= 0.0 or minor_step_mm <= 0.0:
        raise ValueError("ruler length and minor step must be positive")
    if major_every < 1 or label_every_major < 1:
        raise ValueError("major_every and label_every_major must be >= 1")
    ratio = length_mm / minor_step_mm
    tick_intervals = int(round(ratio))
    if abs(ratio - tick_intervals) > 1e-6:
        raise ValueError("ruler length must be an integer multiple of minor step")
    if tick_intervals > 5000:
        raise ValueError("ruler would exceed 5000 minor intervals")
    major_count = tick_intervals // major_every + 1
    if labels and math.ceil(major_count / label_every_major) > 100:
        raise ValueError("ruler would exceed 100 labels; increase label interval")

    scene = context.scene
    origin_world = _ruler_origin(context, origin_mode)
    length_scene = mm_to_scene_units(scene, length_mm)
    step_scene = mm_to_scene_units(scene, minor_step_mm)
    minor_tick_mm = max(1.0, min(20.0, minor_step_mm * 0.25))
    major_tick_mm = max(minor_tick_mm * 2.0, min(50.0, minor_step_mm * 0.6))
    minor_tick_scene = mm_to_scene_units(scene, minor_tick_mm)
    major_tick_scene = mm_to_scene_units(scene, major_tick_mm)

    axis_index = {"X": 0, "Y": 1, "Z": 2}[axis]
    tick_index = {"X": 1, "Y": 0, "Z": 0}[axis]
    axis_vector = Vector((0.0, 0.0, 0.0))
    axis_vector[axis_index] = 1.0

    vertices = [Vector((0.0, 0.0, 0.0)), axis_vector * length_scene]
    edges = [(0, 1)]
    major_positions = []
    for index in range(tick_intervals + 1):
        base = axis_vector * (step_scene * index)
        is_major = index % major_every == 0
        tick_length = major_tick_scene if is_major else minor_tick_scene
        tip = base.copy()
        tip[tick_index] += tick_length
        start_index = len(vertices)
        vertices.extend((base, tip))
        edges.append((start_index, start_index + 1))
        if is_major:
            major_positions.append((index, tip.copy()))

    counter = int(scene.get(GUIDE_COUNTER_KEY, 0)) + 1
    scene[GUIDE_COUNTER_KEY] = counter
    guide_id = f"OLE_GUIDE::RULER::{counter:04d}"
    mesh = bpy.data.meshes.new(f"{guide_id}_MESH")
    mesh.from_pydata([tuple(vertex) for vertex in vertices], edges, [])
    mesh.update()
    ruler = bpy.data.objects.new(guide_id, mesh)
    ruler.location = origin_world
    ruler.hide_render = True
    ruler.show_in_front = True
    ruler.display_type = "WIRE"
    ruler["oleander_reference_guide"] = True
    ruler["oleander_guide_id"] = guide_id
    ruler["oleander_guide_kind"] = "WORLD_RULER"
    ruler["oleander_guide_authority"] = "REFERENCE_ONLY_NOT_MODEL_GEOMETRY"
    ruler["oleander_ruler_axis"] = axis
    ruler["oleander_ruler_length_mm"] = float(length_mm)
    ruler["oleander_ruler_minor_step_mm"] = float(minor_step_mm)
    ruler["oleander_ruler_major_every"] = int(major_every)
    ruler["oleander_ruler_origin_mode"] = origin_mode
    ruler["oleander_ruler_minor_intervals"] = int(tick_intervals)
    ruler["oleander_ruler_major_ticks"] = int(major_count)
    collection = _guide_collection(scene)
    collection.objects.link(ruler)

    label_names = []
    if labels:
        label_offset_scene = major_tick_scene + mm_to_scene_units(scene, max(2.0, minor_tick_mm * 0.5))
        for major_index, (tick_index_value, tip) in enumerate(major_positions):
            if major_index % label_every_major != 0:
                continue
            value_mm = tick_index_value * minor_step_mm
            curve = bpy.data.curves.new(f"{guide_id}_LABEL_{major_index:03d}", type="FONT")
            curve.body = _format_mm(value_mm)
            curve.size = mm_to_scene_units(scene, max(3.0, min(30.0, major_tick_mm * 0.5)))
            text = bpy.data.objects.new(f"{guide_id}_LABEL_{major_index:03d}", curve)
            text.location = origin_world + tip
            text.location[tick_index] += label_offset_scene
            if axis == "Z":
                text.rotation_euler.x = math.radians(90.0)
            text.hide_render = True
            text.show_in_front = True
            text["oleander_reference_guide"] = True
            text["oleander_guide_parent_id"] = guide_id
            text["oleander_guide_kind"] = "RULER_LABEL"
            collection.objects.link(text)
            label_names.append(text.name)
    ruler["oleander_ruler_labels"] = json.dumps(label_names, ensure_ascii=False)
    _append_event(scene, "CREATE_RULER", {
        "guide_id": guide_id,
        "axis": axis,
        "length_mm": float(length_mm),
        "minor_step_mm": float(minor_step_mm),
        "major_every": int(major_every),
        "labels": len(label_names),
    })
    return ruler


class OLEANDER_OT_set_measurement_profile(bpy.types.Operator):
    bl_idname = "oleander.set_measurement_profile"
    bl_label = "Set Measurement Profile"
    bl_options = {"REGISTER", "UNDO"}

    profile: bpy.props.EnumProperty(name="Profile", items=PROFILE_ITEMS, default="FURNITURE_INTERIOR")
    configure_native_snap: bpy.props.BoolProperty(name="Enable Increment Snap", default=True)
    configure_viewport_grid: bpy.props.BoolProperty(name="Match Viewport Grid", default=True)

    def invoke(self, context, event):
        self.profile = measurement_profile(context.scene)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        profile = set_profile(context.scene, self.profile)
        if self.configure_native_snap:
            context.scene.tool_settings.use_snap = True
            context.scene.tool_settings.snap_elements = {"INCREMENT"}
            if hasattr(context.scene.tool_settings, "use_snap_grid_absolute"):
                context.scene.tool_settings.use_snap_grid_absolute = True
        updated = _apply_viewport_grid(context, profile) if self.configure_viewport_grid else 0
        _append_event(context.scene, "SET_PROFILE", {"profile": self.profile, "viewports_updated": updated})
        self.report({"INFO"}, f"Measurement profile: {PROFILES[self.profile]['label']}; exact snap step {profile['snap_step_mm']:g} mm")
        return {"FINISHED"}


class OLEANDER_OT_measure_selection(bpy.types.Operator):
    bl_idname = "oleander.measure_selection"
    bl_label = "Measure Selection"
    bl_options = {"REGISTER"}

    def execute(self, context):
        snapshot = measurement_snapshot(context.scene, context.selected_objects, context.active_object)
        context.scene[SNAPSHOT_KEY] = json.dumps(snapshot, sort_keys=True, ensure_ascii=False)
        _append_event(context.scene, "MEASURE_SELECTION", {"selected_count": snapshot["selected_count"]})
        pair = snapshot.get("pair")
        if pair:
            self.report({"INFO"}, f"Origin distance: {pair['origin_distance_mm']:.3f} mm")
        elif snapshot.get("active"):
            dims = snapshot["active"]["dimensions_mm"]
            self.report({"INFO"}, f"Dimensions: {dims[0]:.3f} × {dims[1]:.3f} × {dims[2]:.3f} mm")
        else:
            self.report({"INFO"}, "No object selected; unit contract snapshot recorded")
        return {"FINISHED"}


class OLEANDER_OT_quantize_location(bpy.types.Operator):
    bl_idname = "oleander.quantize_location"
    bl_label = "Snap Location to mm Step"
    bl_options = {"REGISTER", "UNDO"}

    step_mm: bpy.props.FloatProperty(name="Step mm", default=10.0, min=0.000001)
    snap_x: bpy.props.BoolProperty(name="X", default=True)
    snap_y: bpy.props.BoolProperty(name="Y", default=True)
    snap_z: bpy.props.BoolProperty(name="Z", default=True)

    @classmethod
    def poll(cls, context):
        return bool(context.selected_objects) and context.mode == "OBJECT"

    def invoke(self, context, event):
        self.step_mm = profile_values(context.scene)["snap_step_mm"]
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if not any((self.snap_x, self.snap_y, self.snap_z)):
            self.report({"ERROR"}, "Enable at least one snap axis")
            return {"CANCELLED"}
        try:
            results = quantize_world_location(
                context.scene,
                context.selected_objects,
                self.step_mm,
                axes=(self.snap_x, self.snap_y, self.snap_z),
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        _append_event(context.scene, "QUANTIZE_LOCATION", {"step_mm": self.step_mm, "objects": results})
        self.report({"INFO"}, f"Snapped {len(results)} object(s) to {self.step_mm:g} mm step")
        return {"FINISHED"}


class OLEANDER_OT_nudge_location(bpy.types.Operator):
    bl_idname = "oleander.nudge_location"
    bl_label = "Nudge by mm"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(name="Axis", items=AXIS_ITEMS, default="X")
    amount_mm: bpy.props.FloatProperty(name="Amount mm", default=10.0)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        self.amount_mm = profile_values(context.scene)["snap_step_mm"]
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        try:
            result = nudge_world_location(context.scene, context.active_object, self.axis, self.amount_mm)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        _append_event(context.scene, "NUDGE_LOCATION", result)
        self.report({"INFO"}, f"Nudged {self.axis} by {self.amount_mm:g} mm")
        return {"FINISHED"}


class OLEANDER_OT_create_ruler_guide(bpy.types.Operator):
    bl_idname = "oleander.create_ruler_guide"
    bl_label = "Create World Ruler"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(name="Axis", items=AXIS_ITEMS, default="X")
    origin_mode: bpy.props.EnumProperty(name="Origin", items=ORIGIN_ITEMS, default="ACTIVE_ORIGIN")
    length_mm: bpy.props.FloatProperty(name="Length mm", default=3000.0, min=0.000001)
    minor_step_mm: bpy.props.FloatProperty(name="Minor Step mm", default=10.0, min=0.000001)
    major_every: bpy.props.IntProperty(name="Major Every", default=10, min=1, max=1000)
    labels: bpy.props.BoolProperty(name="Major Labels", default=True)
    label_every_major: bpy.props.IntProperty(name="Label Every Major", default=1, min=1, max=1000)

    def invoke(self, context, event):
        profile = profile_values(context.scene)
        self.length_mm = profile["default_ruler_mm"]
        self.minor_step_mm = profile["minor_step_mm"]
        self.major_every = profile["major_every"]
        if context.active_object is None:
            self.origin_mode = "CURSOR"
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        try:
            ruler = create_ruler_guide(
                context,
                self.axis,
                self.length_mm,
                self.minor_step_mm,
                self.major_every,
                origin_mode=self.origin_mode,
                labels=self.labels,
                label_every_major=self.label_every_major,
            )
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}
        self.report({"INFO"}, f"Created {ruler['oleander_guide_id']} — {self.length_mm:g} mm / {self.minor_step_mm:g} mm ticks")
        return {"FINISHED"}


class OLEANDER_PT_measurement_system(bpy.types.Panel):
    bl_label = "Scale / Ruler / Snap"
    bl_idname = "OLEANDER_PT_measurement_system"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"
    bl_parent_id = "OLEANDER_PT_runtime_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        profile = profile_values(scene)
        layout.label(text=f"Profile: {PROFILES[profile['profile']]['label']}")
        layout.label(text=f"Scene scale: 1 BU = {scene_units_to_mm(scene, 1.0):g} mm")
        layout.label(text=f"Minor / major: {profile['minor_step_mm']:g} / {profile['minor_step_mm'] * profile['major_every']:g} mm")
        layout.label(text=f"Exact snap: {profile['snap_step_mm']:g} mm")
        layout.operator("oleander.set_measurement_profile", icon="GRID")
        row = layout.row(align=True)
        row.operator("oleander.measure_selection", icon="DRIVER_DISTANCE")
        row.operator("oleander.quantize_location", icon="SNAP_ON")
        row = layout.row(align=True)
        row.operator("oleander.nudge_location", icon="ORIENTATION_GLOBAL")
        row.operator("oleander.create_ruler_guide", icon="RULER")
        raw = scene.get(SNAPSHOT_KEY)
        if raw:
            try:
                snapshot = json.loads(raw)
            except (TypeError, json.JSONDecodeError):
                snapshot = None
            if snapshot:
                active = snapshot.get("active")
                pair = snapshot.get("pair")
                if active:
                    dims = active.get("dimensions_mm", [0.0, 0.0, 0.0])
                    layout.label(text=f"Size: {dims[0]:.2f} × {dims[1]:.2f} × {dims[2]:.2f} mm")
                if pair:
                    layout.label(text=f"Pair distance: {pair.get('origin_distance_mm', 0.0):.3f} mm")
        layout.label(text="World ruler + quantize are metric authority")
        layout.label(text="Viewport grid is visual guidance only")


OPERATOR_CLASSES = (
    OLEANDER_OT_set_measurement_profile,
    OLEANDER_OT_measure_selection,
    OLEANDER_OT_quantize_location,
    OLEANDER_OT_nudge_location,
    OLEANDER_OT_create_ruler_guide,
)

PANEL_CLASSES = (OLEANDER_PT_measurement_system,)
