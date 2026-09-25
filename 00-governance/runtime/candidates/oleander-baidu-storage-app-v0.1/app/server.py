from __future__ import annotations

import asyncio
import copy
import os
import re
import time
from typing import Any

import mcp.types as types
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .policy import (
    DELETE_TOOLS,
    READ_TOOLS,
    SHARE_TOOLS,
    WRITE_TOOLS,
    PolicyError,
    StoragePolicy,
)
from .result_filter import _DROP, filter_json_text, filter_object
from .upstream import BaiduMcpSession, UpstreamError


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT_DIR, ".env"))

APP_NAME = "OLEANDER 百度网盘"
APP_VERSION = "0.1.0-candidate"
UPSTREAM_PREFIX = "baidu_"
CACHE_TTL_SECONDS = 60

POLICY = StoragePolicy.from_env()

mcp = FastMCP(
    APP_NAME,
    instructions=(
        "OLEANDER bounded Baidu Netdisk storage surface. Storage is not Project State or Current Authority. "
        f"All path-addressable operations are restricted to {POLICY.root}. "
        "Do not infer Design KEEP, professional PASS, Promotion, KI/OE or project decisions from storage operations."
    ),
    stateless_http=True,
    json_response=True,
    streamable_http_path="/mcp",
)

_tool_cache: tuple[float, list[Any]] | None = None
_tool_cache_lock = asyncio.Lock()


def _safe_error_message(exc: Exception) -> str:
    message = str(exc)
    message = re.sub(r"(?i)(access_token=)[^&\s'\"<>]+", r"\1<redacted>", message)
    token = os.getenv("BAIDU_NETDISK_ACCESS_TOKEN", "").strip()
    if token:
        message = message.replace(token, "<redacted>")
    return message


def _token_configured() -> bool:
    return bool(
        os.getenv("BAIDU_NETDISK_ACCESS_TOKEN", "").strip()
        or os.getenv("BAIDU_NETDISK_ACCESS_TOKEN_FILE", "").strip()
    )


def _tool_annotations(name: str) -> types.ToolAnnotations:
    if name in READ_TOOLS:
        return types.ToolAnnotations(
            readOnlyHint=True,
            destructiveHint=False,
            idempotentHint=True,
            openWorldHint=False,
        )
    if name in DELETE_TOOLS:
        return types.ToolAnnotations(
            readOnlyHint=False,
            destructiveHint=True,
            idempotentHint=False,
            openWorldHint=False,
        )
    return types.ToolAnnotations(
        readOnlyHint=False,
        destructiveHint=False,
        idempotentHint=False,
        openWorldHint=False,
    )


def _local_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="oleander_storage_status",
            title="OLEANDER 百度网盘状态",
            description=(
                "Read the configured OLEANDER Baidu storage policy, root and connection readiness. "
                "This is read-only and does not contact project authority."
            ),
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
            annotations=types.ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
        ),
        types.Tool(
            name="oleander_storage_probe",
            title="检查百度网盘连接",
            description=(
                "Contact the configured official Baidu Netdisk MCP endpoint, verify the access token, "
                "and report which upstream tools are visible through the OLEANDER allowlist. Read-only."
            ),
            inputSchema={"type": "object", "properties": {}, "additionalProperties": False},
            annotations=types.ToolAnnotations(
                readOnlyHint=True,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=True,
            ),
        ),
        types.Tool(
            name="oleander_storage_bootstrap",
            title="初始化 OLEANDER 网盘目录",
            description=(
                f"Create the bounded {POLICY.root} root and standard PROJECTS/KNOWLEDGE/SHARED-ASSETS/ARCHIVE folders. "
                "This creates storage folders only and never creates Project State, a Project Registry or Current Authority."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "confirm": {
                        "type": "string",
                        "description": "Exact value CREATE_OLEANDER_VAULT to create missing folders.",
                    }
                },
                "required": ["confirm"],
                "additionalProperties": False,
            },
            annotations=types.ToolAnnotations(
                readOnlyHint=False,
                destructiveHint=False,
                idempotentHint=True,
                openWorldHint=False,
            ),
        ),
    ]


async def _load_upstream_tools(force: bool = False) -> list[Any]:
    global _tool_cache
    now = time.monotonic()
    if not force and _tool_cache and (now - _tool_cache[0]) < CACHE_TTL_SECONDS:
        return _tool_cache[1]
    async with _tool_cache_lock:
        now = time.monotonic()
        if not force and _tool_cache and (now - _tool_cache[0]) < CACHE_TTL_SECONDS:
            return _tool_cache[1]
        if not _token_configured():
            return []
        async with BaiduMcpSession() as upstream:
            tools = await upstream.list_tools()
        _tool_cache = (time.monotonic(), tools)
        return tools


def _wrap_tool(tool: Any) -> types.Tool | None:
    name = str(tool.name)
    if not POLICY.tool_allowed(name):
        return None
    schema = POLICY.augment_schema(name, copy.deepcopy(tool.inputSchema or {}))
    description = (tool.description or "Baidu Netdisk operation").strip()
    boundary = (
        f" OLEANDER boundary: path-addressable operations are restricted to {POLICY.root}; "
        "storage state is not Project State, Design KEEP or Promotion."
    )
    if name in DELETE_TOOLS:
        boundary += " Delete is high-risk and requires server enablement plus explicit delete acknowledgement."
    if name in SHARE_TOOLS:
        boundary += " Share-link creation is disabled unless server policy explicitly enables it."
    return types.Tool(
        name=UPSTREAM_PREFIX + name,
        title=f"百度网盘｜{tool.title or name}",
        description=description + boundary,
        inputSchema=schema,
        outputSchema=copy.deepcopy(getattr(tool, "outputSchema", None)),
        annotations=_tool_annotations(name),
        _meta={
            "oleander/storageRoot": POLICY.root,
            "oleander/upstreamTool": name,
            "oleander/authorityEffect": "NONE",
        },
    )


@mcp._mcp_server.list_tools()
async def _list_tools() -> list[types.Tool]:
    tools = _local_tools()
    try:
        upstream_tools = await _load_upstream_tools()
    except Exception:
        upstream_tools = []
    for tool in upstream_tools:
        wrapped = _wrap_tool(tool)
        if wrapped:
            tools.append(wrapped)
    return tools


def _error_result(message: str, code: str = "OLEANDER_STORAGE_ERROR") -> types.ServerResult:
    return types.ServerResult(
        types.CallToolResult(
            content=[types.TextContent(type="text", text=f"{code}: {message}")],
            structuredContent={"status": "error", "code": code, "message": message},
            isError=True,
            _meta={"oleander/authorityEffect": "NONE"},
        )
    )


def _filter_upstream_result(result: types.CallToolResult) -> types.CallToolResult:
    content: list[Any] = []
    for item in result.content:
        if isinstance(item, types.TextContent):
            content.append(
                types.TextContent(
                    type="text",
                    text=filter_json_text(item.text, POLICY.root),
                    annotations=item.annotations,
                    _meta=item._meta,
                )
            )
        else:
            content.append(item)

    structured = result.structuredContent
    if structured is not None:
        filtered = filter_object(structured, POLICY.root)
        if filtered is _DROP:
            structured = {"status": "filtered", "reason": "outside OLEANDER storage root"}
        elif isinstance(filtered, dict):
            structured = filtered
        else:
            structured = {"result": filtered}

    meta = dict(result._meta or {})
    meta.update(
        {
            "oleander/storageRoot": POLICY.root,
            "oleander/authorityEffect": "NONE",
            "oleander/doesNotProve": [
                "storage success does not prove Project State change",
                "storage success does not prove Design KEEP",
                "storage success does not prove Promotion",
            ],
        }
    )
    return types.CallToolResult(
        content=content,
        structuredContent=structured,
        isError=result.isError,
        _meta=meta,
    )


async def _bootstrap_storage() -> types.ServerResult:
    targets = [
        POLICY.root,
        f"{POLICY.root}/PROJECTS",
        f"{POLICY.root}/KNOWLEDGE",
        f"{POLICY.root}/SHARED-ASSETS",
        f"{POLICY.root}/ARCHIVE",
    ]
    results = []
    try:
        async with BaiduMcpSession() as upstream:
            for path in targets:
                prepared = POLICY.prepare_arguments("make_dir", {"path": path, "rtype": 1})
                result = await upstream.call_tool("make_dir", prepared)
                results.append({"path": path, "is_error": bool(result.isError)})
    except Exception as exc:
        return _error_result(_safe_error_message(exc), "BAIDU_UPSTREAM_ERROR")
    return types.ServerResult(
        types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text="OLEANDER_VAULT bootstrap completed; folder creation results were returned. This does not create project authority.",
                )
            ],
            structuredContent={"status": "ok", "root": POLICY.root, "folders": results},
            _meta={"oleander/authorityEffect": "NONE"},
        )
    )


async def _call_tool_request(req: types.CallToolRequest) -> types.ServerResult:
    name = req.params.name
    arguments = dict(req.params.arguments or {})

    if name == "oleander_storage_status":
        return types.ServerResult(
            types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=(
                            f"OLEANDER Baidu Storage candidate {APP_VERSION}; root={POLICY.root}; "
                            f"token_configured={_token_configured()}; delete={POLICY.allow_delete}; share={POLICY.allow_share}."
                        ),
                    )
                ],
                structuredContent={
                    "app": APP_NAME,
                    "version": APP_VERSION,
                    "status": "CANDIDATE",
                    "storage_root": POLICY.root,
                    "token_configured": _token_configured(),
                    "delete_enabled": POLICY.allow_delete,
                    "share_enabled": POLICY.allow_share,
                    "authority_effect": "NONE",
                },
                _meta={"oleander/authorityEffect": "NONE"},
            )
        )

    if name == "oleander_storage_probe":
        if not _token_configured():
            return _error_result(
                "BAIDU_NETDISK_ACCESS_TOKEN is not configured",
                "BAIDU_CONFIGURATION_ERROR",
            )
        try:
            upstream_tools = await _load_upstream_tools(force=True)
        except Exception as exc:
            return _error_result(_safe_error_message(exc), "BAIDU_UPSTREAM_ERROR")
        exposed = []
        hidden = []
        for tool in upstream_tools:
            if POLICY.tool_allowed(str(tool.name)):
                exposed.append(str(tool.name))
            else:
                hidden.append(str(tool.name))
        return types.ServerResult(
            types.CallToolResult(
                content=[
                    types.TextContent(
                        type="text",
                        text=f"Baidu MCP connection succeeded; {len(exposed)} upstream tools are exposed by OLEANDER policy.",
                    )
                ],
                structuredContent={
                    "status": "connected",
                    "storage_root": POLICY.root,
                    "exposed_upstream_tools": exposed,
                    "hidden_upstream_tools": hidden,
                    "authority_effect": "NONE",
                },
                _meta={"oleander/authorityEffect": "NONE"},
            )
        )

    if name == "oleander_storage_bootstrap":
        if arguments.get("confirm") != "CREATE_OLEANDER_VAULT":
            return _error_result(
                "bootstrap requires confirm='CREATE_OLEANDER_VAULT'",
                "CONFIRMATION_REQUIRED",
            )
        return await _bootstrap_storage()

    if not name.startswith(UPSTREAM_PREFIX):
        return _error_result(f"unknown tool: {name}", "UNKNOWN_TOOL")

    upstream_name = name[len(UPSTREAM_PREFIX) :]
    try:
        prepared = POLICY.prepare_arguments(upstream_name, arguments)
    except PolicyError as exc:
        return _error_result(str(exc), "OLEANDER_POLICY_BLOCK")

    try:
        async with BaiduMcpSession() as upstream:
            result = await upstream.call_tool(upstream_name, prepared)
        return types.ServerResult(_filter_upstream_result(result))
    except UpstreamError as exc:
        return _error_result(_safe_error_message(exc), "BAIDU_CONFIGURATION_ERROR")
    except Exception as exc:
        return _error_result(_safe_error_message(exc), "BAIDU_UPSTREAM_ERROR")


mcp._mcp_server.request_handlers[types.CallToolRequest] = _call_tool_request


@mcp.custom_route("/healthz", methods=["GET", "OPTIONS"])
async def healthz(request: Request) -> Response:
    if request.method == "OPTIONS":
        return Response(status_code=204)
    return JSONResponse(
        {
            "status": "ok",
            "app": APP_NAME,
            "version": APP_VERSION,
            "candidate": True,
            "token_configured": _token_configured(),
            "storage_root": POLICY.root,
        }
    )


@mcp.custom_route("/policy", methods=["GET", "OPTIONS"])
async def policy_route(request: Request) -> Response:
    if request.method == "OPTIONS":
        return Response(status_code=204)
    return JSONResponse(
        {
            "storage_root": POLICY.root,
            "delete_enabled": POLICY.allow_delete,
            "share_enabled": POLICY.allow_share,
            "authority_effect": "NONE",
            "current_semantics": "REMOTE_BYTE_COPY_CLASS_ONLY_NOT_OLEANDER_CURRENT_AUTHORITY",
        }
    )


app = mcp.streamable_http_app()


class _OptionalBearerGuard(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        expected = os.getenv("OLEANDER_APP_BEARER_TOKEN", "").strip()
        if expected and request.url.path.startswith("/mcp"):
            observed = request.headers.get("authorization", "")
            if observed != f"Bearer {expected}":
                return JSONResponse(
                    {"error": "unauthorized", "message": "Valid OLEANDER app bearer token required."},
                    status_code=401,
                )
        return await call_next(request)


app.add_middleware(_OptionalBearerGuard)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    allow_credentials=False,
)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="127.0.0.1", port=port)
