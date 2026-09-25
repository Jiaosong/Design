"""Vercel ASGI entrypoint for the OLEANDER Baidu Storage MCP candidate.

Vercel routes this Python function under /api. We cannot use a Starlette Mount
here because mounted sub-applications do not receive their own ASGI lifespan;
FastMCP needs that lifespan to initialize the Streamable HTTP session manager.
This tiny proxy therefore rewrites only the HTTP/WebSocket path and delegates
all lifespan traffic unchanged to the original FastMCP application.
"""

from __future__ import annotations

from typing import Any

from app.server import app as oleander_baidu_app


class ApiPrefixProxy:
    def __init__(self, inner: Any, prefix: str = "/api") -> None:
        self.inner = inner
        self.prefix = prefix.rstrip("/")

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") in {"http", "websocket"}:
            path = str(scope.get("path", ""))
            if path == self.prefix:
                rewritten = "/"
            elif path.startswith(self.prefix + "/"):
                rewritten = path[len(self.prefix) :]
            else:
                rewritten = path
            scope = dict(scope)
            scope["path"] = rewritten
            raw_path = scope.get("raw_path")
            if isinstance(raw_path, (bytes, bytearray)):
                scope["raw_path"] = rewritten.encode("utf-8")
        await self.inner(scope, receive, send)


app = ApiPrefixProxy(oleander_baidu_app)
