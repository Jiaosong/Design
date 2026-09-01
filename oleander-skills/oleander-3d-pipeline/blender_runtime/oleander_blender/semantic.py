import json


DEFAULT_SCHEMA_VERSION = "OLEANDER_OBJECT_SEMANTICS_v0.1"


def semantic_payload(obj):
    meta = getattr(obj, "oleander_meta", None)
    payload = {
        "schema": DEFAULT_SCHEMA_VERSION,
        "object_name": obj.name,
        "object_type": obj.type,
        "ole_id": getattr(meta, "ole_id", "") if meta else "",
        "assembly_id": getattr(meta, "assembly_id", "") if meta else "",
        "lod": getattr(meta, "lod", "") if meta else "",
        "master_type": getattr(meta, "master_type", "") if meta else "",
        "master_locator": getattr(meta, "master_locator", "") if meta else "",
        "geometry_authority": getattr(meta, "geometry_authority", "") if meta else "",
        "material_authority": getattr(meta, "material_authority", "") if meta else "",
        "field_status": getattr(meta, "field_status", "OPEN") if meta else "OPEN",
        "engineering_status": getattr(meta, "engineering_status", "OPEN") if meta else "OPEN",
        "manufacturing_status": getattr(meta, "manufacturing_status", "OPEN") if meta else "OPEN",
        "semantic_class": obj.get("oleander_semantic_class", "UNCLASSIFIED"),
        "material_spec": obj.get("oleander_material_spec", ""),
        "fabrication_process": obj.get("oleander_fabrication_process", ""),
        "evidence_state": obj.get("oleander_evidence_state", "OPEN"),
    }
    return payload


def store_semantic_snapshot(obj):
    payload = semantic_payload(obj)
    obj["oleander_semantic_snapshot"] = json.dumps(payload, sort_keys=True)
    return payload
