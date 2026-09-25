from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def verify(wrapper: Path) -> dict[str, object]:
    params = StdioServerParameters(
        command="powershell.exe",
        args=[
            "-NoLogo",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(wrapper),
        ],
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            tool_names = sorted(tool.name for tool in tools.tools)

            probe = await session.call_tool("oleander_storage_probe", {})
            probe_data = probe.structuredContent or {}

            quota = await session.call_tool("baidu_get_quota", {})
            quota_errno = None
            if quota.content:
                for item in quota.content:
                    text = getattr(item, "text", None)
                    if not text:
                        continue
                    try:
                        parsed = json.loads(text)
                    except json.JSONDecodeError:
                        continue
                    quota_errno = parsed.get("errno")
                    break

            return {
                "transport": "stdio",
                "tool_count": len(tool_names),
                "required_tools_present": all(
                    name in tool_names
                    for name in (
                        "oleander_storage_status",
                        "oleander_storage_probe",
                        "baidu_get_quota",
                    )
                ),
                "probe_error": bool(probe.isError),
                "connection_status": probe_data.get("status"),
                "storage_root": probe_data.get("storage_root"),
                "quota_error": bool(quota.isError),
                "quota_errno": quota_errno,
                "authority_effect": probe_data.get("authority_effect"),
            }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("wrapper", type=Path)
    args = parser.parse_args()
    result = asyncio.run(verify(args.wrapper.resolve()))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    ok = (
        result["required_tools_present"] is True
        and result["probe_error"] is False
        and result["connection_status"] == "connected"
        and result["storage_root"] == "/OLEANDER_VAULT"
        and result["quota_error"] is False
        and result["quota_errno"] == 0
        and result["authority_effect"] == "NONE"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
