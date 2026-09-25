from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from codesign_session_kernel_v0_2 import (
    decide_auto_advance,
    resolve_execution_route,
    validate_execution_route,
)


BRIDGE_ID = "OLEANDER_CHAT_COS_LOCAL_EXECUTION_BRIDGE_v0.1"
AUTHORITY_CEILING = "EXECUTION_ROUTING_AND_TOOL_HANDOFF_ONLY"
BAIDU_PLUGIN_ID = "oleander-baidu-storage@oleander-personal"
READ_TOOLS = {
    "oleander_storage_status",
    "oleander_storage_probe",
    "baidu_user_info",
    "baidu_file_image_list",
    "baidu_file_video_list",
    "baidu_file_list",
    "baidu_file_doc_list",
    "baidu_file_meta",
    "baidu_get_quota",
    "baidu_file_keyword_search",
    "baidu_file_semantics_search",
}
WRITE_TOOLS = {
    "oleander_storage_bootstrap",
    "baidu_file_copy",
    "baidu_file_upload_by_url",
    "baidu_file_move",
    "baidu_file_rename",
    "baidu_make_dir",
}


def _codex_home() -> Path:
    configured = os.environ.get("CODEX_HOME", "").strip()
    return Path(configured) if configured else Path.home() / ".codex"


def _version_key(path: Path) -> tuple[int, ...]:
    try:
        return tuple(int(part) for part in path.name.split("."))
    except ValueError:
        return (0,)


def resolve_baidu_wrapper() -> tuple[Path, str]:
    root = _codex_home() / "plugins" / "cache" / "oleander-personal" / "oleander-baidu-storage"
    candidates = sorted((p for p in root.glob("*") if p.is_dir()), key=_version_key, reverse=True)
    for version_dir in candidates:
        wrapper = version_dir / "runtime" / "run_stdio_secure.ps1"
        manifest = version_dir / "plugin.json"
        if wrapper.is_file() and manifest.is_file():
            data = json.loads(manifest.read_text(encoding="utf-8-sig"))
            if data.get("name") == "oleander-baidu-storage":
                return wrapper, str(data.get("version") or version_dir.name)
    raise RuntimeError("OLEANDER_BAIDU_STORAGE_LOCAL_ADAPTER_NOT_INSTALLED")


def _write_gate(request: dict[str, Any]) -> dict[str, str]:
    context = request.get("mutation_context")
    if not isinstance(context, dict):
        return {"decision": "HOLD", "reason": "WRITE_REQUIRES_MUTATION_CONTEXT"}
    side_effect_class = str(context.get("side_effect_class") or "UNRESOLVED")
    if side_effect_class in {"NONE", "REVERSIBLE_LOCAL"}:
        return {"decision": "HOLD", "reason": "REMOTE_STORAGE_WRITE_CANNOT_BE_CLASSIFIED_AS_LOCAL_OR_NONE"}
    return decide_auto_advance(
        mutation_directive=str(context.get("mutation_directive") or "NORMAL"),
        side_effect_class=side_effect_class,
        guard_facts=context.get("guard_facts") if isinstance(context.get("guard_facts"), dict) else {},
        stop_facts=context.get("stop_facts") if isinstance(context.get("stop_facts"), dict) else {},
    )


async def _call_baidu_tool(wrapper: Path, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    params = StdioServerParameters(
        command="powershell.exe",
        args=["-NoLogo", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(wrapper)],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            names = {tool.name for tool in listed.tools}
            if tool_name not in names:
                raise RuntimeError(f"LOCAL_ADAPTER_TOOL_NOT_EXPOSED:{tool_name}")
            result = await session.call_tool(tool_name, arguments)
            content = []
            for item in result.content or []:
                text = getattr(item, "text", None)
                if text is not None:
                    content.append(text)
            return {
                "is_error": bool(result.isError),
                "structured_content": result.structuredContent,
                "text_content": content,
            }


def run_request(request: dict[str, Any]) -> dict[str, Any]:
    capability_id = str(request.get("capability_id") or "BAIDU_STORAGE")
    if capability_id != "BAIDU_STORAGE":
        raise ValueError(f"UNSUPPORTED_LOCAL_CAPABILITY:{capability_id}")
    tool_name = str(request.get("tool_name") or "oleander_storage_probe")
    arguments = request.get("arguments") or {}
    if not isinstance(arguments, dict):
        raise ValueError("arguments must be one object")
    if tool_name not in READ_TOOLS | WRITE_TOOLS:
        raise ValueError(f"TOOL_NOT_ALLOWED_BY_CHAT_COS_BRIDGE:{tool_name}")

    try:
        wrapper, adapter_version = resolve_baidu_wrapper()
        adapter_state = "INSTALLED_READY"
    except RuntimeError:
        wrapper = Path(".")
        adapter_version = "UNRESOLVED"
        adapter_state = "UNAVAILABLE"

    route = resolve_execution_route({
        "conversation_surface": str(request.get("conversation_surface") or "CHAT"),
        "capability_id": capability_id,
        "operation_class": "READ" if tool_name in READ_TOOLS else "WRITE",
        "workstation_online": request.get("workstation_online", True),
        "cos_bridge_available": True,
        "adapter_state": adapter_state,
    })
    route_errors = validate_execution_route(route)
    if route_errors:
        raise RuntimeError("INVALID_EXECUTION_ROUTE:" + ";".join(route_errors))
    if route.get("route_state") != "READY":
        return {
            "bridge_id": BRIDGE_ID,
            "authority_ceiling": AUTHORITY_CEILING,
            "route": route,
            "execution": {"state": "NOT_EXECUTED", "reason": route.get("route_reason")},
            "authority_effect": "NONE",
        }

    if tool_name in WRITE_TOOLS:
        gate = _write_gate(request)
        if gate.get("decision") != "CONTINUE":
            return {
                "bridge_id": BRIDGE_ID,
                "authority_ceiling": AUTHORITY_CEILING,
                "route": route,
                "execution": {"state": "NOT_EXECUTED", "reason": gate.get("reason"), "guard": gate},
                "authority_effect": "NONE",
            }
    else:
        gate = {"decision": "CONTINUE", "reason": "READ_ONLY_LOCAL_CAPABILITY_CALL"}

    result = asyncio.run(_call_baidu_tool(wrapper, tool_name, arguments))
    return {
        "bridge_id": BRIDGE_ID,
        "authority_ceiling": AUTHORITY_CEILING,
        "route": {**route, "adapter_version": adapter_version},
        "execution": {
            "state": "EXECUTED",
            "tool_name": tool_name,
            "guard": gate,
            "tool_result": result,
            "readback_required": tool_name in WRITE_TOOLS,
            "readback_state": "PROVIDER_RESULT_ONLY" if tool_name in WRITE_TOOLS else "ACTUAL_PROVIDER_READ",
        },
        "authority_effect": "NONE",
        "does_not_prove": [
            "TOOL_SUCCESS_DOES_NOT_PROVE_PROJECT_STATE_MUTATION",
            "TOOL_SUCCESS_DOES_NOT_PROVE_DESIGN_KEEP",
            "TOOL_SUCCESS_DOES_NOT_PROVE_PROMOTION",
        ],
    }


def run_self_test() -> dict[str, Any]:
    ready = resolve_execution_route({"capability_id": "BAIDU_STORAGE"})
    pending = resolve_execution_route({"capability_id": "BAIDU_STORAGE", "workstation_online": False})
    blocked_write = _write_gate({})
    checks = {
        "CHAT_DEFAULT_CONVERSATION_SURFACE": ready.get("conversation_surface") == "CHAT",
        "BAIDU_ROUTES_TO_INLINE_COS": ready.get("execution_surface") == "COS_LOCAL" and ready.get("handoff_mode") == "INLINE_COS_BRIDGE",
        "OFFLINE_FALLS_BACK_TO_EXISTING_EXECUTION_INTENT": pending.get("requires_execution_intent") is True and pending.get("handoff_mode") == "CONTINUITY_EXECUTION_INTENT",
        "WRITE_WITHOUT_GUARD_FAILS_CLOSED": blocked_write.get("decision") == "HOLD",
        "ROUTE_HAS_NO_AUTHORITY_EFFECT": ready.get("authority_effect") == "NONE",
    }
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("bridge self-test failed: " + ",".join(failed))
    return {"status": "PASS", "bridge_id": BRIDGE_ID, "checks": list(checks)}


def _load_request(path: str | None) -> dict[str, Any]:
    if not path or path == "-":
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError("request must be one JSON object")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="OLEANDER Chat-default to COS local capability bridge")
    parser.add_argument("request", nargs="?", help="JSON request path; omit/use '-' for stdin")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = run_self_test() if args.self_test else run_request(_load_request(args.request))
    except (ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "CHAT_COS_BRIDGE_FAILURE", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))


if __name__ == "__main__":
    main()
