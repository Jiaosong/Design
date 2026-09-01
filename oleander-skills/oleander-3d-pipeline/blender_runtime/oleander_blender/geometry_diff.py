import hashlib
import json
import math


def _round(value, places=6):
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return round(value, places)
    return value


def object_geometry_signature(obj):
    data = obj.data
    payload = {
        "name": obj.name,
        "type": obj.type,
        "location": [_round(v) for v in obj.location],
        "rotation": [_round(v) for v in obj.rotation_euler],
        "scale": [_round(v) for v in obj.scale],
        "dimensions": [_round(v) for v in obj.dimensions],
    }

    if obj.type == "MESH" and data:
        payload.update({
            "vertices": len(data.vertices),
            "edges": len(data.edges),
            "polygons": len(data.polygons),
            "bounds": [[_round(v) for v in corner] for corner in obj.bound_box],
        })
    elif data:
        payload["data_name"] = data.name

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["sha256"] = hashlib.sha256(encoded).hexdigest()
    return payload


def store_baseline(obj):
    signature = object_geometry_signature(obj)
    obj["oleander_geometry_baseline"] = json.dumps(signature, sort_keys=True)
    return signature


def load_baseline(obj):
    raw = obj.get("oleander_geometry_baseline")
    if not raw:
        return None
    try:
        return json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return None


def diff_from_baseline(obj):
    before = load_baseline(obj)
    after = object_geometry_signature(obj)
    if not before:
        return {"status": "NO_BASELINE", "before": None, "after": after, "changed": []}

    changed = []
    for key in sorted(set(before) | set(after)):
        if key == "sha256":
            continue
        if before.get(key) != after.get(key):
            changed.append({"field": key, "before": before.get(key), "after": after.get(key)})

    return {
        "status": "CHANGED" if changed else "UNCHANGED",
        "before": before,
        "after": after,
        "changed": changed,
    }
