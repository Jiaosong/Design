import json

import bpy
from mathutils import Vector

from .dependency import mark_downstream_stale, object_id


def _mm_to_scene_units(context, value_mm):
    scale_length = context.scene.unit_settings.scale_length or 1.0
    return (value_mm / 1000.0) / scale_length


def _scene_units_to_mm(context, value_scene):
    scale_length = context.scene.unit_settings.scale_length or 1.0
    return value_scene * scale_length * 1000.0


def _unique_array_ole_id(source_id, index, occupied):
    if not source_id:
        return ""
    base = f"{source_id}_A{index:03d}"
    candidate = base
    revision = 2
    while candidate in occupied:
        candidate = f"{base}_R{revision:03d}"
        revision += 1
    occupied.add(candidate)
    return candidate


def _apply_object_scale(context, obj):
    """Apply scale without leaving the operator selection state mutated."""
    previous_active = context.view_layer.objects.active
    previous_selected = list(context.selected_objects)
    try:
        for selected in previous_selected:
            selected.select_set(False)
        obj.select_set(True)
        context.view_layer.objects.active = obj
        result = bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        if "FINISHED" not in result:
            raise RuntimeError("Blender transform_apply did not finish")
    finally:
        obj.select_set(False)
        for selected in previous_selected:
            if selected.name in bpy.data.objects:
                selected.select_set(True)
        if previous_active and previous_active.name in bpy.data.objects:
            context.view_layer.objects.active = previous_active


class OLEANDER_OT_apply_metric_dimensions(bpy.types.Operator):
    """Set active mesh dimensions from millimetres using the scene unit scale."""

    bl_idname = "oleander.apply_metric_dimensions"
    bl_label = "Apply mm Dimensions"
    bl_options = {"REGISTER", "UNDO"}

    x_mm: bpy.props.FloatProperty(name="X mm", default=1000.0, min=0.001)
    y_mm: bpy.props.FloatProperty(name="Y mm", default=1000.0, min=0.001)
    z_mm: bpy.props.FloatProperty(name="Z mm", default=1000.0, min=0.001)

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "MESH"
            and context.mode == "OBJECT"
        )

    def invoke(self, context, event):
        obj = context.active_object
        self.x_mm = _scene_units_to_mm(context, obj.dimensions.x)
        self.y_mm = _scene_units_to_mm(context, obj.dimensions.y)
        self.z_mm = _scene_units_to_mm(context, obj.dimensions.z)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        obj = context.active_object
        previous_mm = [
            _scene_units_to_mm(context, obj.dimensions.x),
            _scene_units_to_mm(context, obj.dimensions.y),
            _scene_units_to_mm(context, obj.dimensions.z),
        ]
        target_mm = [self.x_mm, self.y_mm, self.z_mm]
        target = Vector(tuple(_mm_to_scene_units(context, value) for value in target_mm))

        # A direct edit of one linked mesh instance must not silently rescale the
        # shared datablock for every other instance. Break data sharing first.
        broke_shared_data = bool(getattr(obj, "data", None) and obj.data.users > 1)
        if broke_shared_data:
            obj.data = obj.data.copy()

        obj.dimensions = target
        context.view_layer.update()
        _apply_object_scale(context, obj)
        context.view_layer.update()

        downstream = mark_downstream_stale(
            [object_id(obj)],
            reason="DIRECT_DIMENSION_CHANGE",
            scene=context.scene,
        )

        obj["oleander_last_direct_operation"] = "SET_DIMENSIONS_MM"
        obj["oleander_direct_previous_dimensions_mm"] = previous_mm
        obj["oleander_direct_dimensions_mm"] = target_mm
        obj["oleander_direct_broke_shared_data"] = broke_shared_data
        obj["oleander_direct_downstream_stale"] = json.dumps(downstream, sort_keys=True)
        self.report(
            {"INFO"},
            f"Dimensions set to {self.x_mm:.1f} × {self.y_mm:.1f} × {self.z_mm:.1f} mm; downstream stale: {len(downstream)}",
        )
        return {"FINISHED"}


class OLEANDER_OT_duplicate_linear(bpy.types.Operator):
    """Create a governed linked or unlinked linear duplicate set."""

    bl_idname = "oleander.duplicate_linear"
    bl_label = "Linear Duplicate"
    bl_options = {"REGISTER", "UNDO"}

    count: bpy.props.IntProperty(name="Count", default=3, min=2, max=10000)
    spacing_mm: bpy.props.FloatProperty(name="Spacing mm", default=600.0, min=0.0)
    axis: bpy.props.EnumProperty(
        name="Axis",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", "")],
        default="X",
    )
    linked: bpy.props.BoolProperty(name="Linked Mesh", default=True)

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.mode == "OBJECT"

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        source = context.active_object
        source_id = source.oleander.ole_id.strip() if hasattr(source, "oleander") else ""
        stable_source_ref = source_id or source.name
        occupied = {
            obj.oleander.ole_id
            for obj in bpy.data.objects
            if hasattr(obj, "oleander") and obj.oleander.ole_id
        }

        step = Vector((0.0, 0.0, 0.0))
        step[{"X": 0, "Y": 1, "Z": 2}[self.axis]] = _mm_to_scene_units(context, self.spacing_mm)
        collection = source.users_collection[0] if source.users_collection else context.collection

        created_names = []
        created_ids = []
        for idx in range(1, self.count):
            dup = source.copy()
            if getattr(source, "data", None) and not self.linked:
                dup.data = source.data.copy()
            dup.location = source.location + step * idx
            dup.name = f"{source.name}_A{idx:03d}"
            collection.objects.link(dup)

            # Object identity is instance identity. Never inherit the source OLE
            # ID into a duplicate, even when the mesh datablock is intentionally linked.
            if hasattr(dup, "oleander"):
                dup.oleander.ole_id = _unique_array_ole_id(source_id, idx, occupied)

            dup["oleander_array_source_id"] = stable_source_ref
            dup["oleander_array_index"] = idx
            dup["oleander_array_instance_role"] = "LINKED_MESH_INSTANCE" if self.linked else "UNLINKED_COPY"
            created_names.append(dup.name)
            created_ids.append(dup.oleander.ole_id if hasattr(dup, "oleander") else "")

        source["oleander_last_direct_operation"] = "LINEAR_DUPLICATE"
        source["oleander_array_count"] = self.count
        source["oleander_array_spacing_mm"] = self.spacing_mm
        source["oleander_array_axis"] = self.axis
        source["oleander_array_linked"] = self.linked
        source["oleander_array_created_names"] = json.dumps(created_names, ensure_ascii=False)
        source["oleander_array_created_ids"] = json.dumps(created_ids, ensure_ascii=False)
        self.report({"INFO"}, f"Created {len(created_names)} governed duplicates")
        return {"FINISHED"}


CLASSES = (
    OLEANDER_OT_apply_metric_dimensions,
    OLEANDER_OT_duplicate_linear,
)
