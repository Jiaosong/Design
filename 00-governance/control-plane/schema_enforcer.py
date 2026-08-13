#!/usr/bin/env python3
"""Small dependency-free JSON-Schema subset enforcer for OLEANDER control-plane schemas.

Supported keywords are intentionally limited to the schema constructs used by the
checked-in Control Plane schemas: type, required, properties, additionalProperties,
enum, const, pattern, items, uniqueItems, minLength, minItems, minProperties,
oneOf, and local $ref.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_schema(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as fh:
        schema = json.load(fh)
    if not isinstance(schema, dict):
        raise ValueError("schema root must be an object")
    return schema


def _type_ok(value: Any, expected: str) -> bool:
    if expected == "object": return isinstance(value, dict)
    if expected == "array": return isinstance(value, list)
    if expected == "string": return isinstance(value, str)
    if expected == "null": return value is None
    if expected == "boolean": return isinstance(value, bool)
    if expected == "integer": return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number": return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def _resolve_ref(root: dict[str, Any], ref: str) -> dict[str, Any]:
    if not ref.startswith("#/"):
        raise ValueError(f"only local refs are supported: {ref}")
    node: Any = root
    for token in ref[2:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        node = node[token]
    if not isinstance(node, dict):
        raise ValueError(f"ref does not resolve to object: {ref}")
    return node


def validate_instance(value: Any, schema: dict[str, Any], *, root: dict[str, Any] | None = None, path: str = "$") -> list[dict[str, str]]:
    root = root or schema
    errors: list[dict[str, str]] = []

    if "$ref" in schema:
        return validate_instance(value, _resolve_ref(root, schema["$ref"]), root=root, path=path)

    if "oneOf" in schema:
        branches = schema["oneOf"]
        matches = [validate_instance(value, branch, root=root, path=path) for branch in branches]
        passing = [errs for errs in matches if not errs]
        if len(passing) != 1:
            errors.append({"path": path, "message": f"oneOf requires exactly one matching schema, got {len(passing)}"})
        return errors

    expected_type = schema.get("type")
    if expected_type is not None:
        allowed = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_type_ok(value, t) for t in allowed):
            errors.append({"path": path, "message": f"expected type {allowed}, got {type(value).__name__}"})
            return errors

    if "const" in schema and value != schema["const"]:
        errors.append({"path": path, "message": f"must equal {schema['const']!r}"})
    if "enum" in schema and value not in schema["enum"]:
        errors.append({"path": path, "message": f"must be one of {schema['enum']!r}"})

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append({"path": path, "message": f"length must be >= {schema['minLength']}"})
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append({"path": path, "message": f"does not match pattern {schema['pattern']}"})

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append({"path": path, "message": f"item count must be >= {schema['minItems']}"})
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, sort_keys=True, ensure_ascii=False) for item in value]
            if len(rendered) != len(set(rendered)):
                errors.append({"path": path, "message": "items must be unique"})
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, item in enumerate(value):
                errors.extend(validate_instance(item, item_schema, root=root, path=f"{path}[{i}]"))

    if isinstance(value, dict):
        if "minProperties" in schema and len(value) < schema["minProperties"]:
            errors.append({"path": path, "message": f"property count must be >= {schema['minProperties']}"})
        for key in schema.get("required", []):
            if key not in value:
                errors.append({"path": path, "message": f"missing required property {key}"})
        properties = schema.get("properties", {})
        if isinstance(properties, dict):
            for key, child_schema in properties.items():
                if key in value and isinstance(child_schema, dict):
                    errors.extend(validate_instance(value[key], child_schema, root=root, path=f"{path}.{key}"))
        additional = schema.get("additionalProperties", True)
        known = set(properties) if isinstance(properties, dict) else set()
        for key, child in value.items():
            if key in known:
                continue
            if additional is False:
                errors.append({"path": f"{path}.{key}", "message": "additional property is not allowed"})
            elif isinstance(additional, dict):
                errors.extend(validate_instance(child, additional, root=root, path=f"{path}.{key}"))

    return errors
