from __future__ import annotations

import json
from typing import Any

from .policy import is_within_root


def filter_object(value: Any, root: str) -> Any:
    """Remove result records that explicitly point outside the configured root.

    User/quota results have no path and pass through. This is a response-level
    defense in depth; request path guards remain the primary boundary.
    """
    if isinstance(value, list):
        out = []
        for item in value:
            filtered = filter_object(item, root)
            if filtered is not _DROP:
                out.append(filtered)
        return out
    if isinstance(value, dict):
        path = value.get("path") or value.get("remote_path")
        if isinstance(path, str) and not is_within_root(path, root):
            return _DROP
        out = {}
        for key, child in value.items():
            filtered = filter_object(child, root)
            if filtered is not _DROP:
                out[key] = filtered
        return out
    return value


def filter_json_text(text: str, root: str) -> str:
    try:
        parsed = json.loads(text)
    except Exception:
        return text
    filtered = filter_object(parsed, root)
    if filtered is _DROP:
        filtered = {"status": "filtered", "reason": "outside OLEANDER storage root"}
    return json.dumps(filtered, ensure_ascii=False)


class _Drop:
    pass


_DROP = _Drop()
