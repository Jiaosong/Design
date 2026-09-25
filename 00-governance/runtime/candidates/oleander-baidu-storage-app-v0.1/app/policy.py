from __future__ import annotations

import copy
import json
import os
import posixpath
from dataclasses import dataclass
from typing import Any
from urllib.parse import unquote


READ_TOOLS = {
    "file_list",
    "file_doc_list",
    "file_image_list",
    "file_video_list",
    "file_meta",
    "file_keyword_search",
    "file_semantics_search",
    "user_info",
    "get_quota",
}

REMOTE_UPLOAD_TOOLS = {
    "file_upload_by_url",
    "file_upload_by_text",
    "file_upload_text",
    "file_upload_from_text",
}

WRITE_TOOLS = {
    "make_dir",
    "file_copy",
    "file_move",
    "file_rename",
} | REMOTE_UPLOAD_TOOLS

DELETE_TOOLS = {"file_del"}
SHARE_TOOLS = {"file_sharelink_set"}

CURRENT_ACK = "ACK_STORAGE_CURRENT_MUTATION"
OVERWRITE_ACK = "ACK_STORAGE_OVERWRITE"
DELETE_ACK = "ACK_STORAGE_DELETE"


class PolicyError(ValueError):
    pass


def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def normalize_root(root: str) -> str:
    root = unquote(root or "/OLEANDER_VAULT").replace("\\", "/").strip()
    if not root.startswith("/"):
        root = "/" + root
    root = root.rstrip("/") or "/"
    parts = [p for p in root.split("/") if p]
    if any(p in {".", ".."} for p in parts):
        raise PolicyError("invalid configured OLEANDER root")
    return "/" + "/".join(parts) if parts else "/"


def normalize_cloud_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip():
        raise PolicyError("cloud path must be a non-empty string")
    value = path
    for _ in range(3):
        decoded = unquote(value)
        if decoded == value:
            break
        value = decoded
    value = value.replace("\\", "/").strip()
    if not value.startswith("/"):
        raise PolicyError(f"cloud path must be absolute: {path!r}")
    parts = [p for p in value.split("/") if p]
    if any(p in {".", ".."} for p in parts):
        raise PolicyError(f"path traversal is forbidden: {path!r}")
    return "/" + "/".join(parts) if parts else "/"


def validate_leaf_name(value: Any, label: str) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise PolicyError(f"{label} must be a non-empty file/folder name")
    decoded = value
    for _ in range(3):
        next_value = unquote(decoded)
        if next_value == decoded:
            break
        decoded = next_value
    if decoded in {".", ".."} or "/" in decoded or "\\" in decoded:
        raise PolicyError(f"{label} must be a leaf name without path separators")


def is_within_root(path: str, root: str) -> bool:
    p = normalize_cloud_path(path)
    r = normalize_root(root)
    return p == r or p.startswith(r + "/")


def has_current_segment(path: str) -> bool:
    parts = [p.upper() for p in normalize_cloud_path(path).split("/") if p]
    return "CURRENT" in parts


def _loads_filelist(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise PolicyError("filelist must be valid JSON") from exc
    if not isinstance(value, list):
        raise PolicyError("filelist must be a list")
    return [x for x in value if isinstance(x, dict)]


def _loads_raw_filelist(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise PolicyError("filelist must be valid JSON") from exc
    if not isinstance(value, list):
        raise PolicyError("filelist must be a list")
    return value


@dataclass(frozen=True)
class StoragePolicy:
    root: str = "/OLEANDER_VAULT"
    allow_delete: bool = False

    @classmethod
    def from_env(cls) -> "StoragePolicy":
        return cls(
            root=normalize_root(os.getenv("OLEANDER_BAIDU_ROOT", "/OLEANDER_VAULT")),
            allow_delete=env_bool("OLEANDER_ALLOW_DELETE", False),
        )

    def tool_allowed(self, name: str) -> bool:
        if name in READ_TOOLS or name in WRITE_TOOLS:
            return True
        if name in DELETE_TOOLS:
            return self.allow_delete
        if name in SHARE_TOOLS:
            # v0.1 intentionally keeps fsid-only sharing unsupported because
            # proving every fsid belongs to /OLEANDER_VAULT requires an
            # authenticated metadata preflight that has not yet been validated.
            return False
        return False

    def augment_schema(self, tool_name: str, schema: dict[str, Any]) -> dict[str, Any]:
        out = copy.deepcopy(schema or {"type": "object", "properties": {}})
        out.setdefault("type", "object")
        props = out.setdefault("properties", {})
        if tool_name in WRITE_TOOLS | DELETE_TOOLS:
            props["oleander_current_ack"] = {
                "type": "string",
                "description": (
                    f"Required only when this operation mutates a /CURRENT/ storage path. "
                    f"Exact value: {CURRENT_ACK}. This acknowledges byte-storage mutation only; "
                    "it is not Design KEEP or Current Authority."
                ),
            }
            props["oleander_overwrite_ack"] = {
                "type": "string",
                "description": f"Required only for overwrite semantics. Exact value: {OVERWRITE_ACK}.",
            }
        if tool_name in DELETE_TOOLS:
            props["oleander_delete_ack"] = {
                "type": "string",
                "description": f"Required for every delete. Exact value: {DELETE_ACK}.",
            }
        return out

    def prepare_arguments(self, tool_name: str, arguments: dict[str, Any] | None) -> dict[str, Any]:
        if not self.tool_allowed(tool_name):
            raise PolicyError(f"tool is not allowed by OLEANDER storage policy: {tool_name}")

        args = copy.deepcopy(arguments or {})
        current_ack = args.pop("oleander_current_ack", None)
        overwrite_ack = args.pop("oleander_overwrite_ack", None)
        delete_ack = args.pop("oleander_delete_ack", None)

        validate_leaf_name(args.get("filename"), "filename")
        for index, item in enumerate(_loads_filelist(args.get("filelist"))):
            validate_leaf_name(item.get("newname"), f"filelist[{index}].newname")

        if tool_name in {"file_list", "file_doc_list", "file_image_list", "file_video_list", "file_keyword_search", "file_semantics_search"}:
            args["dir"] = args.get("dir") or self.root

        if tool_name in REMOTE_UPLOAD_TOOLS:
            args["dir"] = args.get("dir") or self.root

        path_roles = self._path_roles(tool_name, args)
        for role, path in path_roles:
            if not is_within_root(path, self.root):
                raise PolicyError(f"{role} escapes configured OLEANDER root {self.root}: {path}")

        current_mutation = any(
            mutates and has_current_segment(path)
            for mutates, _, path in self._mutation_paths(tool_name, args)
        )
        if current_mutation and current_ack != CURRENT_ACK:
            raise PolicyError(
                f"mutation touching /CURRENT/ requires oleander_current_ack={CURRENT_ACK!r}"
            )

        if self._requests_overwrite(tool_name, args) and overwrite_ack != OVERWRITE_ACK:
            raise PolicyError(
                f"overwrite semantics require oleander_overwrite_ack={OVERWRITE_ACK!r}"
            )

        if tool_name in DELETE_TOOLS:
            if not self.allow_delete:
                raise PolicyError("delete is disabled by server policy")
            if delete_ack != DELETE_ACK:
                raise PolicyError(f"delete requires oleander_delete_ack={DELETE_ACK!r}")

        return args

    def _path_roles(self, tool_name: str, args: dict[str, Any]) -> list[tuple[str, str]]:
        found: list[tuple[str, str]] = []
        for key in ("dir", "path", "remote_path", "dest"):
            value = args.get(key)
            if isinstance(value, str) and value:
                found.append((key, value))
        for index, item in enumerate(_loads_filelist(args.get("filelist"))):
            for key in ("path", "dest"):
                value = item.get(key)
                if isinstance(value, str) and value:
                    found.append((f"filelist[{index}].{key}", value))
        if tool_name in DELETE_TOOLS:
            for index, item in enumerate(_loads_raw_filelist(args.get("filelist"))):
                if isinstance(item, str) and item:
                    found.append((f"filelist[{index}]", item))
        return found

    def _mutation_paths(self, tool_name: str, args: dict[str, Any]) -> list[tuple[bool, str, str]]:
        out: list[tuple[bool, str, str]] = []
        filelist = _loads_filelist(args.get("filelist"))

        if tool_name == "file_copy":
            for i, item in enumerate(filelist):
                if isinstance(item.get("dest"), str):
                    out.append((True, f"filelist[{i}].dest", item["dest"]))
                if isinstance(item.get("path"), str):
                    out.append((False, f"filelist[{i}].path", item["path"]))
                target = self._effective_target(tool_name, item)
                if target:
                    out.append((True, f"filelist[{i}].effective_target", target))
            return out

        if tool_name in {"file_move", "file_rename", "file_del"}:
            if tool_name == "file_del":
                for i, item in enumerate(_loads_raw_filelist(args.get("filelist"))):
                    if isinstance(item, str):
                        out.append((True, f"filelist[{i}]", item))
            for i, item in enumerate(filelist):
                if isinstance(item.get("path"), str):
                    out.append((True, f"filelist[{i}].path", item["path"]))
                if isinstance(item.get("dest"), str):
                    out.append((True, f"filelist[{i}].dest", item["dest"]))
                target = self._effective_target(tool_name, item)
                if target:
                    out.append((True, f"filelist[{i}].effective_target", target))
            return out

        if tool_name == "make_dir" and isinstance(args.get("path"), str):
            out.append((True, "path", args["path"]))
        elif tool_name in REMOTE_UPLOAD_TOOLS and isinstance(args.get("dir"), str):
            out.append((True, "dir", args["dir"]))
            filename = args.get("filename")
            if isinstance(filename, str) and filename:
                out.append((True, "effective_target", self._join_target(args["dir"], filename)))
        return out

    @staticmethod
    def _join_target(directory: str, leaf: str) -> str:
        validate_leaf_name(leaf, "target name")
        normalized_dir = normalize_cloud_path(directory)
        return normalize_cloud_path(normalized_dir.rstrip("/") + "/" + leaf)

    @classmethod
    def _effective_target(cls, tool_name: str, item: dict[str, Any]) -> str | None:
        source = item.get("path")
        newname = item.get("newname")
        if tool_name in {"file_copy", "file_move"}:
            dest = item.get("dest")
            if not isinstance(dest, str) or not dest:
                return None
            if isinstance(newname, str) and newname:
                leaf = newname
            elif isinstance(source, str) and source:
                leaf = posixpath.basename(normalize_cloud_path(source))
            else:
                return None
            return cls._join_target(dest, leaf)
        if tool_name == "file_rename":
            if not isinstance(source, str) or not source or not isinstance(newname, str) or not newname:
                return None
            parent = posixpath.dirname(normalize_cloud_path(source)) or "/"
            return cls._join_target(parent, newname)
        return None

    @staticmethod
    def _requests_overwrite(tool_name: str, args: dict[str, Any]) -> bool:
        if str(args.get("ondup", "")).lower() == "overwrite":
            return True
        if args.get("rtype") in {4, "4"}:
            return True
        return False
