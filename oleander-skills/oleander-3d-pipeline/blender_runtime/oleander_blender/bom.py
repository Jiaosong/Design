import json
from collections import defaultdict

import bpy


def _dimensions_mm(scene, obj):
    scale = scene.unit_settings.scale_length or 1.0
    return [round(float(v) * scale * 1000.0, 3) for v in obj.dimensions]


def _group_key(scene, obj):
    meta = obj.oleander
    if meta.part_number.strip():
        return ("PART_NUMBER", meta.part_number.strip())
    return (
        "FALLBACK",
        meta.semantic_class.strip() or "UNCLASSIFIED",
        meta.object_class.strip(),
        meta.material_spec.strip(),
        meta.fabrication_process.strip(),
        tuple(_dimensions_mm(scene, obj)),
    )


def build_bom(scene):
    groups = defaultdict(list)
    for obj in scene.objects:
        groups[_group_key(scene, obj)].append(obj)

    items = []
    for index, (key, objects) in enumerate(sorted(groups.items(), key=lambda item: str(item[0])), start=1):
        first = objects[0]
        meta = first.oleander
        ids = [(obj.oleander.ole_id or obj.name) for obj in objects]
        items.append(
            {
                "item": index,
                "grouping": "PART_NUMBER" if key[0] == "PART_NUMBER" else "FALLBACK_SEMANTIC_DIMENSION",
                "part_number": meta.part_number,
                "semantic_class": meta.semantic_class,
                "object_class": meta.object_class,
                "material_spec": meta.material_spec,
                "fabrication_process": meta.fabrication_process,
                "dimensions_mm_reference": _dimensions_mm(scene, first),
                "quantity": len(objects),
                "ole_ids": ids,
                "assembly_ids": sorted({obj.oleander.assembly_id for obj in objects if obj.oleander.assembly_id}),
                "geometry_authority_states": sorted({obj.oleander.geometry_authority for obj in objects}),
                "manufacturing_states": sorted({obj.oleander.manufacturing_state for obj in objects}),
                "stale_count": sum(1 for obj in objects if obj.oleander.stale),
            }
        )

    return {
        "schema": "OLEANDER_BOM_v0.1",
        "scene": scene.name,
        "unit": "mm",
        "items": items,
        "authority_note": "BOM groups declared model objects. Quantity/material/process data remain subject to geometry, field, engineering and manufacturing authority states.",
    }


class OLEANDER_OT_build_bom(bpy.types.Operator):
    bl_idname = "oleander.build_bom"
    bl_label = "Build OLEANDER BOM"
    bl_description = "Build a governed quantity/BOM view from stable OLE object metadata without implying manufacturing release."

    def execute(self, context):
        bom = build_bom(context.scene)
        text = bpy.data.texts.get("OLEANDER_BOM.json") or bpy.data.texts.new("OLEANDER_BOM.json")
        text.clear()
        text.write(json.dumps(bom, indent=2, ensure_ascii=False))
        self.report({"INFO"}, f"BOM built: {len(bom['items'])} grouped item(s)")
        return {"FINISHED"}


CLASSES = (OLEANDER_OT_build_bom,)
