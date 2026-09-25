from __future__ import annotations

import asyncio
import json

from app.policy import StoragePolicy
from app.upstream import BaiduMcpSession


async def main() -> int:
    policy = StoragePolicy.from_env()
    async with BaiduMcpSession() as upstream:
        tools = await upstream.list_tools()
    exposed = [str(tool.name) for tool in tools if policy.tool_allowed(str(tool.name))]
    hidden = [str(tool.name) for tool in tools if not policy.tool_allowed(str(tool.name))]
    print(
        json.dumps(
            {
                "status": "connected",
                "storage_root": policy.root,
                "exposed_upstream_tools": exposed,
                "hidden_upstream_tools": hidden,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
