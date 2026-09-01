import json


DEFAULT_SCHEMA_VERSION = "OLEANDER_OBJECT_SEMANTICS_v0.2"


def semantic_payload(obj):
    meta = getattr(obj, "oleander", None)
    payload = {
        "schema": DEFAULT_SCHEMA_VERSION,
        "object_name": obj.name,
        "object_type": obj.type,
        "ole_id": getattr(meta, "ole_id", "") if meta else "",
        "object_class": getattr(meta, "object_class", "") if meta else "",
        "semantic_class": getattr(meta, "semantic_class", "UNCLASSIFIED") if meta else "UNCLASSIFIED",
        "assembly_id": getattr(meta, "assembly_id", "") if meta else "",
        "lod": getattr(meta, "lod", 0) if meta else 0,
        "master_type": getattr(meta, "master_type", "") if meta else "",
        "master_locator": getattr(meta, "master_locator", "") if meta else "",
        "geometry_authority": getattr(meta, "geometry_authority", "") if meta else "",
        "material_authority": getattr(meta, "material_authority", "") if meta else "",
        "material_spec": getattr(meta, "material_spec", "") if meta else "",
        "fabrication_process": getattr(meta, "fabrication_process", "") if meta else "",
        "evidence_state": getattr(meta, "evidence_state", "OPEN") if meta else "OPEN",
        "field_state": getattr(meta, "field_state", "OPEN") if meta else "OPEN",
        "engineering_state": getattr(meta, "engineering_state", "OPEN") if meta else "OPEN",
        "manufacturing_state": getattr(meta, "manufacturing_state", "OPEN") if meta else "OPEN",
        "design_review_state": getattr(meta, "design_review_state", "OPEN") if meta else "OPEN",
        "dependencies": [
            item.strip()
            for item in (getattr(meta, "dependencies", "") if meta else "").split(",")
            if item.strip()
        ],
        "stale": bool(getattr(meta, "stale", False)) if meta else False,
    }
    return payload


def store_semantic_snapshot(obj):
    payload = semantic_payload(obj)
    obj["oleander_semantic_snapshot"] = json.dumps(payload, sort_keys=True)
    return payload
