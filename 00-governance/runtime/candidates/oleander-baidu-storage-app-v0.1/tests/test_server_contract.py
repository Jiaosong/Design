from __future__ import annotations

import asyncio
import unittest

import mcp.types as types

from app import server


class FakeTool:
    def __init__(self, name: str, schema: dict | None = None) -> None:
        self.name = name
        self.title = name
        self.description = f"fake {name}"
        self.inputSchema = schema or {"type": "object", "properties": {}}
        self.outputSchema = None


class ServerContractTests(unittest.TestCase):
    def test_local_status_tools_exist_without_baidu_token(self) -> None:
        names = {t.name for t in server._local_tools()}
        self.assertEqual(
            names,
            {"oleander_storage_status", "oleander_storage_probe", "oleander_storage_bootstrap"},
        )

    def test_wrap_read_tool_sets_read_only_annotation(self) -> None:
        wrapped = server._wrap_tool(FakeTool("file_list"))
        self.assertIsNotNone(wrapped)
        self.assertEqual(wrapped.name, "baidu_file_list")
        self.assertTrue(wrapped.annotations.readOnlyHint)

    def test_unknown_upstream_tool_is_hidden(self) -> None:
        self.assertIsNone(server._wrap_tool(FakeTool("dangerous_new_tool")))

    def test_delete_hidden_default_policy(self) -> None:
        self.assertIsNone(server._wrap_tool(FakeTool("file_del")))

    def test_status_call_has_no_authority_effect(self) -> None:
        request = types.CallToolRequest(
            method="tools/call",
            params=types.CallToolRequestParams(name="oleander_storage_status", arguments={}),
        )
        result = asyncio.run(server._call_tool_request(request)).root
        self.assertFalse(result.isError)
        self.assertEqual(result.structuredContent["authority_effect"], "NONE")

    def test_error_sanitizer_redacts_access_token_query(self) -> None:
        msg = server._safe_error_message(
            RuntimeError("request failed https://mcp-pan.baidu.com/sse?access_token=SECRET123&x=1")
        )
        self.assertNotIn("SECRET123", msg)
        self.assertIn("<redacted>", msg)


if __name__ == "__main__":
    unittest.main()
