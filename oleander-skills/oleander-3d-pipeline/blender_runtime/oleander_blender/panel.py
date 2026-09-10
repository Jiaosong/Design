import json

import bpy


class OLEANDER_PT_runtime_panel(bpy.types.Panel):
    bl_label = "OLEANDER Runtime"
    bl_idname = "OLEANDER_PT_runtime_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "OLEANDER"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        environment = context.scene.oleander_environment
        environment_box = layout.box()
        environment_box.label(text="Shared 3D Environment")
        environment_box.label(text="Role: project-neutral OLEANDER software", icon="WORLD")
        environment_box.prop(environment, "domain_workspace")
        environment_box.prop(environment, "project_profile_id")
        environment_box.prop(environment, "project_profile_locator")
        environment_box.prop(environment, "project_profile_state")
        environment_box.label(text="Project profiles configure; Runtime authority stays shared", icon="INFO")

        actions = layout.row(align=True)
        actions.operator("oleander.assign_identity", text="Assign / Repair ID")
        actions.operator("oleander.run_audit", text="Audit")

        row = layout.row(align=True)
        stale_on = row.operator("oleander.mark_stale", text="Mark Stale")
        stale_on.stale = True
        stale_off = row.operator("oleander.mark_stale", text="Clear Stale")
        stale_off.stale = False
        row.operator("oleander.export_manifest", text="Manifest")

        if obj is None:
            layout.label(text="Select an object to edit governed metadata")
            return

        meta = obj.oleander
        box = layout.box()
        box.label(text=f"Object: {obj.name}")
        box.prop(meta, "ole_id")
        box.prop(meta, "object_class")
        box.prop(meta, "semantic_class")
        box.prop(meta, "part_number")
        box.prop(meta, "master_type")
        if meta.master_type != "BLENDER_NATIVE":
            box.prop(meta, "master_locator")
        box.prop(meta, "geometry_authority")
        box.prop(meta, "material_authority")
        box.prop(meta, "material_spec")
        box.prop(meta, "fabrication_process")
        box.prop(meta, "evidence_state")
        box.prop(meta, "field_state")
        box.prop(meta, "engineering_state")
        box.prop(meta, "manufacturing_state")
        box.prop(meta, "design_review_state")
        box.prop(meta, "dependencies")
        box.prop(meta, "lod")
        box.prop(meta, "assembly_id")
        box.prop(meta, "stale")

        if obj.type == "MESH":
            direct_box = layout.box()
            direct_box.label(text="Direct Face · bounded v0.3")
            direct_box.label(text=f"Authority route: {meta.master_type}")
            if context.mode == "EDIT_MESH":
                direct_box.operator("oleander.direct_face_normal_move", text="Face Normal Move ±mm", icon="ORIENTATION_NORMAL")
                direct_box.operator("oleander.direct_face_tangent_move", text="Face Tangent Move U/V mm", icon="ORIENTATION_LOCAL")
                direct_box.operator("oleander.direct_face_rotate", text="Face Rotate U/V ±deg", icon="DRIVER_ROTATIONAL_DIFFERENCE")
                if meta.master_type == "BLENDER_NATIVE":
                    direct_box.label(text="One selected face · geometry U/V tangent basis")
                    direct_box.label(text="Normal / tangent / rotate edits propagate stale state")
                elif meta.master_type == "CAD_NATIVE":
                    direct_box.label(text="Normal + Tangent route through governed CAD sidecar", icon="INFO")
                    direct_box.label(text="Rotate prepares governed intent; execution gate remains separate")
                    direct_box.label(text="Display mesh is not CAD authority")
                else:
                    direct_box.label(text="No bounded direct-face route for this master", icon="ERROR")
            else:
                direct_box.label(text="Enter Mesh Edit Mode and select one face")

        audit_box = layout.box()
        audit_box.label(text="Last Audit")
        raw_summary = context.scene.get("oleander_last_audit_summary")
        if raw_summary:
            try:
                summary = json.loads(raw_summary)
                for key in (
                    "GEOMETRY",
                    "UNITS_AXES",
                    "OBJECT_DEPENDENCIES",
                    "RESOURCE_DEPENDENCIES",
                    "ROUND_TRIP",
                    "DIMENSION_AUTHORITY",
                    "FIELD_VERIFIED",
                    "ENGINEERING_APPROVAL",
                    "CONSTRUCTABILITY",
                    "DESIGN_QUALITY",
                ):
                    audit_box.label(text=f"{key}: {summary.get(key, 'UNKNOWN')}")
            except Exception:
                audit_box.label(text="Audit summary unreadable")
        else:
            audit_box.label(text="NOT RUN")

        audit_box.label(text="Audit is not engineering/design approval", icon="INFO")
