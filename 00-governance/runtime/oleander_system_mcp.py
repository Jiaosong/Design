#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from typing import Any, Callable

from oleander_system_gateway import (
    build_system_context,
    environment_snapshot,
    run_gateway,
    run_self_test,
    validate_system_manifest,
)


SERVER_NAME = "oleander-system-gateway"
SERVER_VERSION = "0.1.0"


TOOLS: list[dict[str, Any]] = [
    {
        "name": "oleander_system_manifest",
        "description": "Validate and read the non-authoritative OLEANDER System Manifest. Does not change Project State, Knowledge, Current or Promotion.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "oleander_system_context",
        "description": "Compose a typed OLEANDER System Context Envelope from caller-supplied owner-native refs. Missing Project/Authority fields remain unresolved and are never inferred from chat/session state.",
        "inputSchema": {
            "type": "object",
            "properties": {"payload": {"type": "object"}},
            "required": ["payload"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "oleander_environment",
        "description": "Read the canonical execution-surface registry together with bounded machine-local runtime observation. A stale local snapshot is reported as stale and never becomes authority.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
    {
        "name": "oleander_preflight",
        "description": "Run OLEANDER system-context resolution plus the existing resolver/runtime bridge before consequential continuation, mutation or closure. Optional live publication affects observability only.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "payload": {"type": "object"},
                "publish_live": {"type": "boolean", "default": False},
            },
            "required": ["payload"],
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": True},
    },
    {
        "name": "oleander_system_self_test",
        "description": "Run the bounded System Manifest / CoS authority-separation / resolver-compatibility self-test without changing Project State.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
    },
]


def _tool_result(value: Any) -> dict[str, Any]:
    return {
        "content": [{"type": "text", "text": json.dumps(value, ensure_ascii=False, sort_keys=True)}],
        "structuredContent": value if isinstance(value, dict) else {"value": value},
        "isError": False,
    }


def _call_tool(name: str, args: dict[str, Any]) -> dict[str, Any]:
    dispatch: dict[str, Callable[[], Any]] = {
        "oleander_system_manifest": lambda: {"validation": validate_system_manifest()},
        "oleander_system_context": lambda: build_system_context(dict(args.get("payload") or {})),
        "oleander_environment": environment_snapshot,
        "oleander_preflight": lambda: run_gateway(
            dict(args.get("payload") or {}), publish_live=bool(args.get("publish_live", False))
        ),
        "oleander_system_self_test": run_self_test,
    }
    if name not in dispatch:
        raise ValueError(f"unknown tool: {name}")
    if name in {"oleander_system_context", "oleander_preflight"} and not isinstance(args.get("payload"), dict):
        raise ValueError("payload must be one object")
    return _tool_result(dispatch[name]())


def _reply(request_id: Any, result: Any) -> None:
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": request_id, "result": result}, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _error(request_id: Any, code: int, message: str) -> None:
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def handle(message: dict[str, Any]) -> None:
    method = message.get("method")
    request_id = message.get("id")
    if request_id is None:
        return
    try:
        if method == "initialize":
            params = message.get("params") if isinstance(message.get("params"), dict) else {}
            requested = params.get("protocolVersion")
            _reply(request_id, {
                "protocolVersion": requested if isinstance(requested, str) else "2025-06-18",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            })
        elif method == "ping":
            _reply(request_id, {})
        elif method == "tools/list":
            _reply(request_id, {"tools": TOOLS})
        elif method == "tools/call":
            params = message.get("params")
            if not isinstance(params, dict) or not isinstance(params.get("name"), str):
                raise ValueError("tools/call requires params.name")
            arguments = params.get("arguments")
            if arguments is None:
                arguments = {}
            if not isinstance(arguments, dict):
                raise ValueError("tools/call arguments must be an object")
            _reply(request_id, _call_tool(params["name"], arguments))
        else:
            _error(request_id, -32601, f"method not found: {method}")
    except (KeyError, TypeError, ValueError, RuntimeError, OSError) as exc:
        _error(request_id, -32602, str(exc))


def main() -> None:
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            message = json.loads(raw)
        except json.JSONDecodeError as exc:
            _error(None, -32700, f"parse error: {exc}")
            continue
        if isinstance(message, dict):
            handle(message)


if __name__ == "__main__":
    main()
