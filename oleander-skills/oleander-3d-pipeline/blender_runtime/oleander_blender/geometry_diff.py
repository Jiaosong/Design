import hashlib
import json
import math


def _round(value, places=6):
    if isinstance(value, float):
        if not math.isfinite(value):
            return None
        return round(value, places)
    return value


def _feed(hasher, value):
    hasher.update(str(value).encode("utf-8"))
    hasher.update(b"|")


def _mesh_content_hash(data):
    """Hash raw editable mesh coordinates/topology without serializing the full mesh into the manifest."""
    hasher = hashlib.sha256()
    _feed(hasher, "OLEANDER_MESH_CONTENT_v0.2")
    _feed(hasher, len(data.vertices))
    _feed(hasher, len(data.edges))
    _feed(hasher, len(data.polygons))

    for vertex in data.vertices:
        for value in vertex.co:
            _feed(hasher, _round(float(value)))

    for edge in data.edges:
        for index in edge.vertices:
            _feed(hasher, int(index))

    for polygon in data.polygons:
        _feed(hasher, len(polygon.vertices))
        for index in polygon.vertices:
            _feed(hasher, int(index))

    return hasher.hexdigest()


def _serialize_rna_value(value):
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        return _round(value)
    if isinstance(value, (set, frozenset)):
        return sorted(str(item) for item in value)
    if hasattr(value, "__len__") and hasattr(value, "__iter__") and not isinstance(value, (str, bytes)):
        try:
            items = list(value)
        except TypeError:
            return None
        if all(isinstance(item, (bool, int, float, str)) for item in items):
            return [_serialize_rna_value(item) for item in items]
    return None


def _modifier_signature(obj):
    modifiers = []
    for modifier in obj.modifiers:
        item = {
            "name": modifier.name,
            "type": modifier.type,
            "show_viewport": bool(modifier.show_viewport),
            "show_render": bool(modifier.show_render),
        }
        properties = {}
        for prop in modifier.bl_rna.properties:
            identifier = prop.identifier
            if identifier in {"rna_type", "name", "type", "show_viewport", "show_render"}:
                continue
            if getattr(prop, "is_readonly", False):
                continue
            if prop.type not in {"BOOLEAN", "INT", "FLOAT", "STRING", "ENUM"}:
                continue
            try:
                value = getattr(modifier, identifier)
            except (AttributeError, TypeError, RuntimeError):
                continue
            serialized = _serialize_rna_value(value)
            if serialized is not None:
                properties[identifier] = serialized
        item["properties"] = properties
        modifiers.append(item)
    return modifiers


def object_geometry_signature(obj):
    data = obj.data
    payload = {
        "schema": "OLEANDER_GEOMETRY_SIGNATURE_v0.2",
        "type": obj.type,
        "location": [_round(float(v)) for v in obj.location],
        "rotation": [_round(float(v)) for v in obj.rotation_euler],
        "scale": [_round(float(v)) for v in obj.scale],
        "dimensions": [_round(float(v)) for v in obj.dimensions],
        "modifier_stack": _modifier_signature(obj),
    }

    if obj.type == "MESH" and data:
        payload.update(
            {
                "vertices": len(data.vertices),
                "edges": len(data.edges),
                "polygons": len(data.polygons),
                "bounds": [[_round(float(v)) for v in corner] for corner in obj.bound_box],
                "mesh_content_sha256": _mesh_content_hash(data),
            }
        )
    elif data:
        # Data-block naming is intentionally excluded: ordinary renames must
        # not become geometry changes. Type/transform/modifier state remains.
        payload["has_data"] = True

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
