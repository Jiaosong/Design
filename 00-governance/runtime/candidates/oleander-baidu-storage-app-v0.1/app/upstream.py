from __future__ import annotations

import os
from contextlib import AsyncExitStack
from typing import Any
from urllib.parse import urlencode

from mcp import ClientSession
from mcp.client.sse import sse_client


class UpstreamError(RuntimeError):
    pass


def read_access_token() -> str:
    token = os.getenv("BAIDU_NETDISK_ACCESS_TOKEN", "").strip()
    token_file = os.getenv("BAIDU_NETDISK_ACCESS_TOKEN_FILE", "").strip()
    if not token and token_file:
        try:
            token = open(token_file, "r", encoding="utf-8-sig").read().strip()
        except OSError as exc:
            raise UpstreamError("could not read BAIDU_NETDISK_ACCESS_TOKEN_FILE") from exc
    if not token:
        raise UpstreamError("BAIDU_NETDISK_ACCESS_TOKEN is not configured")
    return token


def upstream_url() -> str:
    base = os.getenv("OLEANDER_UPSTREAM_SSE", "https://mcp-pan.baidu.com/sse").strip()
    sep = "&" if "?" in base else "?"
    return f"{base}{sep}{urlencode({'access_token': read_access_token()})}"


class BaiduMcpSession:
    def __init__(self) -> None:
        self.stack = AsyncExitStack()
        self.session: ClientSession | None = None

    async def __aenter__(self) -> "BaiduMcpSession":
        try:
            streams = await self.stack.enter_async_context(
                sse_client(upstream_url(), timeout=10, sse_read_timeout=120)
            )
            self.session = await self.stack.enter_async_context(ClientSession(*streams))
            await self.session.initialize()
            return self
        except Exception:
            await self.stack.aclose()
            raise

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.stack.aclose()
        self.session = None

    async def list_tools(self) -> list[Any]:
        if not self.session:
            raise UpstreamError("upstream session is not initialized")
        return (await self.session.list_tools()).tools

    async def call_tool(self, name: str, arguments: dict[str, Any]) -> Any:
        if not self.session:
            raise UpstreamError("upstream session is not initialized")
        return await self.session.call_tool(name, arguments)
