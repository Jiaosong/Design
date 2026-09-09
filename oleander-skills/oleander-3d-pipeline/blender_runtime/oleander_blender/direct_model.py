import hashlib
import json

import bmesh
import bpy
from mathutils import Vector

from .dependency import mark_downstream_stale, object_id


CAD_DIRECT_EDIT_INTENT_SCHEMA = "OLEANDER_CAD_DIRECT_EDIT_INTENT_v0.1"


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


def _unit_scale_applied(obj, tolerance=1e-6):
    return all(abs(float(value) - 1.0) <= tolerance for value in obj.scale)


def _rounded_vector(values, digits=6):
    return [round(float(value), digits) for value in values]


def _face_semantic_descriptor(context, face):
    """Describe a selected display face without persisting a topology ordinal."""
    mm_per_scene_unit = _scene_units_to_mm(context, 1.0)
    center = face.calc_center_median()
    normal = face.normal.normalized()
    coordinates = [vert.co for vert in face.verts]
    minimum = [min(point[axis] for point in coordinates) for axis in range(3)]
    maximum = [max(point[axis] for point in coordinates) for axis in range(3)]
    return {
        "selector_semantics": "BLENDER_SELECTED_DISPLAY_FACE_INTENT",
        "normal_local": _rounded_vector(normal, 9),
        "center_local_mm": _rounded_vector((value * mm_per_scene_unit for value in center), 6),
        "area_mm2": round(float(face.calc_area()) * mm_per_scene_unit * mm_per_scene_unit, 6),
        "edge_count": len(face.edges),
        "edge_lengths_mm": sorted(
            round(float(edge.calc_length()) * mm_per_scene_unit, 6)
            for edge in face.edges
        ),
        "bbox_local_mm": {
            "min": _rounded_vector((value * mm_per_scene_unit for value in minimum), 6),
            "max": _rounded_vector((value * mm_per_scene_unit for value in maximum), 6),
        },
    }


def _canonical_direction(vector):
    """Return a deterministic sign for one geometric direction."""
    result = vector.normalized()
    for component in result:
        if abs(float(component)) <= 1e-9:
            continue
        if component < 0.0:
            result.negate()
        break
    return result


def _face_tangent_basis(face):
    """Derive a deterministic geometry-based U/V tangent basis without edge ordinals."""
    normal = face.normal.normalized()
    candidates = []
    for edge in face.edges:
        direction = edge.verts[1].co - edge.verts[0].co
        length = float(direction.length)
        if length <= 1e-12:
            continue
        direction = _canonical_direction(direction)
        # Longest geometric edge wins. Equal-length ties are broken by the
        # direction components, never by BMesh edge index/order.
        key = (
            -round(length, 12),
            -round(abs(float(direction.x)), 12),
            -round(abs(float(direction.y)), 12),
            -round(abs(float(direction.z)), 12),
            -round(float(direction.x), 12),
            -round(float(direction.y), 12),
            -round(float(direction.z), 12),
        )
        candidates.append((key, direction))
    if not candidates:
        raise ValueError("Selected face has no stable tangent direction")
    candidates.sort(key=lambda item: item[0])
    tangent_u = candidates[0][1]
    tangent_v = normal.cross(tangent_u)
    if tangent_v.length <= 1e-12:
        raise ValueError("Selected face tangent basis is degenerate")
    tangent_v.normalize()
    return tangent_u, tangent_v


def _canonical_json(payload):
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def _build_cad_direct_edit_intent(obj, distance_mm, descriptor):
    if not hasattr(obj, "oleander"):
        raise ValueError("CAD direct edit requires OLEANDER metadata")
    ole_id = obj.oleander.ole_id.strip()
    master_locator = obj.oleander.master_locator.strip()
    if not ole_id:
        raise ValueError("CAD direct edit requires a stable OLE ID")
    if not master_locator:
        raise ValueError("CAD direct edit requires a governed CAD master locator")
    return {
        "schema": CAD_DIRECT_EDIT_INTENT_SCHEMA,
        "ole_id": ole_id,
        "units": "mm",
        "operation": "FACE_NORMAL_MOVE",
        "parameters": {"distance_mm": float(distance_mm)},
        "target": descriptor,
        "authority": {
            "master_type": "CAD_NATIVE",
            "master_locator": master_locator,
            "required_kernel": "FREECAD_OCCT_BREP",
            "blender_role": "DISPLAY_DERIVATIVE_ONLY",
            "display_mutation": "NONE",
        },
        "resolution": {
            "policy": "SEMANTIC_REBIND_FAIL_CLOSED",
            "ambiguous_result": "HOLD",
            "missing_result": "HOLD",
            "prohibited_persistence": [
                "FaceN",
                "EdgeN",
                "VertexN",
                "subshape_ordinal",
                "polygon_index",
            ],
        },
    }


def _selected_governed_edit_face(context):
    obj = context.active_object
    if not _unit_scale_applied(obj):
        raise ValueError("Apply object scale before governed mm face editing")
    if getattr(obj, "data", None) is None:
        raise ValueError("Direct Face requires editable mesh data")
    if obj.data.users > 1:
        raise ValueError("Shared mesh data is HOLD; make the mesh single-user before face editing")
    if obj.data.shape_keys is not None:
        raise ValueError("Shape-key controlled mesh is outside bounded Direct Face scope")

    bm = bmesh.from_edit_mesh(obj.data)
    bm.normal_update()
    selected_faces = [face for face in bm.faces if face.select]
    if len(selected_faces) != 1:
        raise ValueError("Select exactly one mesh face")
    face = selected_faces[0]
    if face.normal.length <= 1e-12:
        raise ValueError("Selected face has no stable normal")
    return obj, bm, face


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


class OLEANDER_OT_direct_face_normal_move(bpy.types.Operator):
    """Bounded face-normal direct edit with explicit authority routing."""

    bl_idname = "oleander.direct_face_normal_move"
    bl_label = "Face Normal Move"
    bl_description = (
        "Move one Blender-native mesh face along its local normal, or prepare a "
        "fail-closed CAD direct-edit intent without mutating a CAD display mesh"
    )
    bl_options = {"REGISTER", "UNDO"}

    distance_mm: bpy.props.FloatProperty(name="Distance mm", default=10.0)

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "MESH"
            and context.mode == "EDIT_MESH"
        )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if abs(float(self.distance_mm)) <= 1e-9:
            self.report({"ERROR"}, "Face Normal Move requires a non-zero distance")
            return {"CANCELLED"}
        try:
            obj, bm, face = _selected_governed_edit_face(context)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        descriptor = _face_semantic_descriptor(context, face)
        master_type = obj.oleander.master_type if hasattr(obj, "oleander") else "BLENDER_NATIVE"

        if master_type == "BLENDER_NATIVE":
            delta = face.normal.normalized() * _mm_to_scene_units(context, self.distance_mm)
            for vert in face.verts:
                vert.co += delta
            bm.normal_update()
            bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
            context.view_layer.update()

            downstream = mark_downstream_stale(
                [object_id(obj)],
                reason="DIRECT_FACE_NORMAL_MOVE",
                scene=context.scene,
            )
            obj["oleander_last_direct_operation"] = "FACE_NORMAL_MOVE"
            obj["oleander_direct_authority_route"] = "BLENDER_NATIVE"
            obj["oleander_direct_face_distance_mm"] = float(self.distance_mm)
            obj["oleander_direct_face_target_descriptor"] = _canonical_json(descriptor)
            obj["oleander_direct_downstream_stale"] = json.dumps(downstream, sort_keys=True)
            self.report(
                {"INFO"},
                f"Face moved {self.distance_mm:+.3f} mm in Blender-native authority; downstream stale: {len(downstream)}",
            )
            return {"FINISHED"}

        if master_type == "CAD_NATIVE":
            try:
                intent = _build_cad_direct_edit_intent(obj, self.distance_mm, descriptor)
            except ValueError as exc:
                self.report({"ERROR"}, str(exc))
                return {"CANCELLED"}
            encoded = _canonical_json(intent)
            obj["oleander_last_direct_operation"] = "CAD_DIRECT_EDIT_INTENT"
            obj["oleander_direct_authority_route"] = "CAD_NATIVE"
            obj["oleander_cad_direct_edit_intent"] = encoded
            obj["oleander_cad_direct_edit_intent_sha256"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
            obj["oleander_cad_direct_edit_state"] = "PENDING_SIDECAR"
            self.report(
                {"INFO"},
                "CAD direct-edit intent prepared; authoritative CAD and Blender display geometry remain unchanged",
            )
            return {"FINISHED"}

        self.report(
            {"ERROR"},
            f"Face Normal Move has no bounded authority route for {master_type}",
        )
        return {"CANCELLED"}


class OLEANDER_OT_direct_face_tangent_move(bpy.types.Operator):
    """Move one Blender-native face within its own tangent plane in millimetres."""

    bl_idname = "oleander.direct_face_tangent_move"
    bl_label = "Face Tangent Move"
    bl_description = (
        "Move one selected Blender-native face in a deterministic geometry-based U/V tangent basis; "
        "CAD-native tangent execution remains fail-closed until absorbed into the shared sidecar"
    )
    bl_options = {"REGISTER", "UNDO"}

    u_mm: bpy.props.FloatProperty(name="U mm", default=10.0)
    v_mm: bpy.props.FloatProperty(name="V mm", default=0.0)

    @classmethod
    def poll(cls, context):
        return (
            context.active_object is not None
            and context.active_object.type == "MESH"
            and context.mode == "EDIT_MESH"
        )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if abs(float(self.u_mm)) <= 1e-9 and abs(float(self.v_mm)) <= 1e-9:
            self.report({"ERROR"}, "Face Tangent Move requires a non-zero U/V displacement")
            return {"CANCELLED"}
        try:
            obj, bm, face = _selected_governed_edit_face(context)
            tangent_u, tangent_v = _face_tangent_basis(face)
        except ValueError as exc:
            self.report({"ERROR"}, str(exc))
            return {"CANCELLED"}

        master_type = obj.oleander.master_type if hasattr(obj, "oleander") else "BLENDER_NATIVE"
        if master_type != "BLENDER_NATIVE":
            self.report(
                {"ERROR"},
                f"Face Tangent Move has no absorbed shared-runtime route for {master_type}; fail-closed",
            )
            return {"CANCELLED"}

        descriptor = _face_semantic_descriptor(context, face)
        delta = (
            tangent_u * _mm_to_scene_units(context, self.u_mm)
            + tangent_v * _mm_to_scene_units(context, self.v_mm)
        )
        normal_component = abs(float(face.normal.normalized().dot(delta)))
        if _scene_units_to_mm(context, normal_component) > 1e-6:
            self.report({"ERROR"}, "Computed tangent move contains a normal component")
            return {"CANCELLED"}

        for vert in face.verts:
            vert.co += delta
        bm.normal_update()
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        context.view_layer.update()

        downstream = mark_downstream_stale(
            [object_id(obj)],
            reason="DIRECT_FACE_TANGENT_MOVE",
            scene=context.scene,
        )
        obj["oleander_last_direct_operation"] = "FACE_TANGENT_MOVE"
        obj["oleander_direct_authority_route"] = "BLENDER_NATIVE"
        obj["oleander_direct_face_tangent_uv_mm"] = [float(self.u_mm), float(self.v_mm)]
        obj["oleander_direct_face_tangent_u_local"] = _rounded_vector(tangent_u, 9)
        obj["oleander_direct_face_tangent_v_local"] = _rounded_vector(tangent_v, 9)
        obj["oleander_direct_face_target_descriptor"] = _canonical_json(descriptor)
        obj["oleander_direct_downstream_stale"] = json.dumps(downstream, sort_keys=True)
        self.report(
            {"INFO"},
            f"Face tangent move U={self.u_mm:+.3f} mm V={self.v_mm:+.3f} mm; downstream stale: {len(downstream)}",
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
    OLEANDER_OT_direct_face_normal_move,
    OLEANDER_OT_direct_face_tangent_move,
    OLEANDER_OT_duplicate_linear,
)
