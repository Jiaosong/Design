import json
import uuid
from datetime import datetime, timezone

import bpy

from .audit import audit_scene
from .configuration import configuration_names
from .dependency import dependency_ids
from .geometry_diff import diff_from_baseline
from .parametric import get_constraints, get_parameters
from .review_state import summarize_object_state
from .semantic import semantic_payload


def _new_ole_id(obj):
    slug = "".join(ch if ch.isalnum() else "_" for ch in obj.name.upper()).strip("_")
    slug = slug[:40] or "OBJECT"
    return f"OLE_{slug}_{uuid.uuid4().hex[:8].upper()}"


class OLEANDER_OT_assign_identity(bpy.types.Operator):
    bl_idname = "oleander.assign_identity"
    bl_label = "Assign / Repair OLE ID"
    bl_description = "Assign persistent OLEANDER identity to selected objects and repair collisions"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        selected = list(context.selected_objects)
        if not selected:
            self.report({"WARNING"}, "No selected objects")
            return {"CANCELLED"}

        occupied = {
            obj.oleander.ole_id
            for obj in bpy.data.objects
            if obj.oleander.ole_id and obj not in selected
        }
        assigned = set()
        changed = 0

        for obj in selected:
            current = obj.oleander.ole_id
            if not current or current in occupied or current in assigned:
                new_id = _new_ole_id(obj)
                while new_id in occupied or new_id in assigned:
                    new_id = _new_ole_id(obj)
                obj.oleander.ole_id = new_id
                changed += 1
            assigned.add(obj.oleander.ole_id)

        self.report({"INFO"}, f"OLEANDER identities updated: {changed}")
        return {"FINISHED"}


class OLEANDER_OT_run_audit(bpy.types.Operator):
    bl_idname = "oleander.run_audit"
    bl_label = "Run OLEANDER Audit"
    bl_description = "Audit geometry/runtime state without implying engineering, field or design approval"

    def execute(self, context):
        result = audit_scene(context.scene)
        payload = json.dumps(result, indent=2, ensure_ascii=False)
        text = bpy.data.texts.get("OLEANDER_AUDIT.json") or bpy.data.texts.new("OLEANDER_AUDIT.json")
        text.clear()
        text.write(payload)
        context.scene["oleander_last_audit_utc"] = datetime.now(timezone.utc).isoformat()
        context.scene["oleander_last_audit_summary"] = json.dumps(result["summary"], ensure_ascii=False)
        review_count = sum(1 for obj in result["objects"] if obj["issues"])
        self.report({"INFO"}, f"Audit complete. Objects requiring review: {review_count}")
        return {"FINISHED"}


class OLEANDER_OT_mark_stale(bpy.types.Operator):
    bl_idname = "oleander.mark_stale"
    bl_label = "Mark Selected Stale"
    bl_description = "Mark selected representations as stale after an upstream authority change"
    bl_options = {"REGISTER", "UNDO"}

    stale: bpy.props.BoolProperty(name="Stale", default=True)

    def execute(self, context):
        selected = list(context.selected_objects)
        if not selected:
            self.report({"WARNING"}, "No selected objects")
            return {"CANCELLED"}
        for obj in selected:
            obj.oleander.stale = self.stale
            if not self.stale and "oleander_stale_reason" in obj:
                del obj["oleander_stale_reason"]
        self.report({"INFO"}, f"Updated stale state on {len(selected)} object(s)")
        return {"FINISHED"}


class OLEANDER_OT_export_manifest(bpy.types.Operator):
    bl_idname = "oleander.export_manifest"
    bl_label = "Build Scene Manifest"
    bl_description = "Build an inspectable OLEANDER scene manifest as a Blender Text datablock"

    def execute(self, context):
        objects = []
        for obj in context.scene.objects:
            meta = obj.oleander
            geometry_diff = diff_from_baseline(obj)
            objects.append(
                {
                    "name": obj.name,
                    "ole_id": meta.ole_id,
                    "object_type": obj.type,
                    "object_class": meta.object_class,
                    "semantic_class": meta.semantic_class,
                    "part_number": meta.part_number,
                    "master_type": meta.master_type,
                    "master_locator": meta.master_locator,
                    "geometry_authority": meta.geometry_authority,
                    "material_authority": meta.material_authority,
                    "material_spec": meta.material_spec,
                    "fabrication_process": meta.fabrication_process,
                    "evidence_state": meta.evidence_state,
                    "field_state": meta.field_state,
                    "engineering_state": meta.engineering_state,
                    "manufacturing_state": meta.manufacturing_state,
                    "design_review_state": meta.design_review_state,
                    "dependencies": dependency_ids(obj),
                    "lod": meta.lod,
                    "assembly_id": meta.assembly_id,
                    "stale": meta.stale,
                    "stale_reason": obj.get("oleander_stale_reason", ""),
                    "location": list(obj.location),
                    "rotation_euler": list(obj.rotation_euler),
                    "scale": list(obj.scale),
                    "dimensions": list(obj.dimensions),
                    "geometry_diff_state": geometry_diff["status"],
                    "geometry_diff": geometry_diff["changed"],
                    "parameters": get_parameters(obj),
                    "constraints": get_constraints(obj),
                    "semantics": semantic_payload(obj),
                    "review": summarize_object_state(obj),
                }
            )

        manifest = {
            "schema": "OLEANDER_BLENDER_WORKBENCH_MANIFEST_v0.2",
            "generated_utc": datetime.now(timezone.utc).isoformat(),
            "blender_version": bpy.app.version_string,
            "blend_file": bpy.data.filepath,
            "scene": {
                "name": context.scene.name,
                "unit_system": context.scene.unit_settings.system,
                "unit_scale": context.scene.unit_settings.scale_length,
                "dependency_audit_state": context.scene.get("oleander_dependency_audit_state", "NOT_RUN"),
                "configurations": configuration_names(context.scene),
            },
            "objects": objects,
            "authority_note": "Manifest records declared states and deterministic runtime observations; it does not create field, engineering, manufacturing, constructability or design approval.",
        }

        payload = json.dumps(manifest, indent=2, ensure_ascii=False)
        text = bpy.data.texts.get("OLEANDER_MANIFEST.json") or bpy.data.texts.new("OLEANDER_MANIFEST.json")
        text.clear()
        text.write(payload)
        self.report({"INFO"}, f"Manifest built for {len(objects)} object(s)")
        return {"FINISHED"}
