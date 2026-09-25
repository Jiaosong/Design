from __future__ import annotations

import asyncio
import base64
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

    def test_share_hidden_v0_1(self) -> None:
        self.assertIsNone(server._wrap_tool(FakeTool("file_sharelink_set")))

    def test_write_annotations_are_conservative(self) -> None:
        move = server._wrap_tool(FakeTool("file_move"))
        self.assertTrue(move.annotations.destructiveHint)
        self.assertFalse(move.annotations.openWorldHint)
        upload = server._wrap_tool(FakeTool("file_upload_by_url"))
        self.assertTrue(upload.annotations.destructiveHint)
        self.assertTrue(upload.annotations.openWorldHint)

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

    def test_unstructured_path_bearing_text_is_suppressed(self) -> None:
        upstream = types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text="outside file is /private/secret.pdf access_token=SECRET123",
                    _meta={"unsafe": "SECRET-META"},
                )
            ],
            _meta={"unsafe": "RESULT-SECRET"},
        )
        filtered = server._filter_upstream_result(upstream, "file_meta")
        self.assertNotIn("/private/secret.pdf", filtered.content[0].text)
        self.assertNotIn("SECRET123", filtered.content[0].text)
        self.assertNotIn("unsafe", filtered.meta)
        self.assertIsNone(filtered.content[0].meta)

    def test_non_text_content_is_suppressed(self) -> None:
        upstream = types.CallToolResult(
            content=[
                types.ImageContent(
                    type="image",
                    data=base64.b64encode(b"SECRET IMAGE").decode("ascii"),
                    mimeType="image/png",
                    _meta={"path": "/private/image.png"},
                )
            ],
            _meta={"path": "/private/image.png"},
        )
        filtered = server._filter_upstream_result(upstream, "file_image_list")
        self.assertTrue(all(isinstance(x, types.TextContent) for x in filtered.content))
        self.assertIn("SUPPRESSED", filtered.content[0].text)
        self.assertNotIn("path", filtered.meta)

    def test_json_result_filters_outside_paths_and_redacts_tokens(self) -> None:
        upstream = types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text='{"list":[{"path":"/private/a.pdf"},{"path":"/OLEANDER_VAULT/ok.pdf","note":"access_token=SECRET123"}]}',
                )
            ],
            structuredContent={
                "list": [
                    {"path": "/private/a.pdf"},
                    {"path": "/OLEANDER_VAULT/ok.pdf", "note": "access_token=SECRET123"},
                ]
            },
        )
        filtered = server._filter_upstream_result(upstream, "file_list")
        self.assertNotIn("/private/a.pdf", filtered.content[0].text)
        self.assertNotIn("SECRET123", filtered.content[0].text)
        self.assertEqual(len(filtered.structuredContent["list"]), 1)
        self.assertNotIn("SECRET123", filtered.structuredContent["list"][0]["note"])


if __name__ == "__main__":
    unittest.main()
