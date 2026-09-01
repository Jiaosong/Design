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
