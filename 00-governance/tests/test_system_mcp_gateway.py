from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "00-governance" / "runtime" / "oleander_system_mcp.py"


class SystemMcpGatewayTests(unittest.TestCase):
    def _run_messages(self, messages: list[dict]) -> list[dict]:
        payload = "".join(json.dumps(row) + "\n" for row in messages)
        run = subprocess.run(
            [sys.executable, str(SERVER)],
            cwd=ROOT,
            input=payload,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        self.assertEqual(0, run.returncode, run.stderr)
        return [json.loads(line) for line in run.stdout.splitlines() if line.strip()]

    def test_stdio_protocol_lists_tools_and_runs_self_test(self) -> None:
        messages = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}},
            },
            {"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "oleander_system_self_test", "arguments": {}}},
        ]
        rows = self._run_messages(messages)
        self.assertEqual([1, 2, 3], [row.get("id") for row in rows])
        self.assertEqual("oleander-system-gateway", rows[0]["result"]["serverInfo"]["name"])
        names = {tool["name"] for tool in rows[1]["result"]["tools"]}
        self.assertEqual(
            {
                "oleander_system_manifest",
                "oleander_system_context",
                "oleander_environment",
                "oleander_capabilities",
                "oleander_resolve_surface",
                "oleander_preflight",
                "oleander_system_self_test",
            },
            names,
        )
        self.assertEqual("PASS", rows[2]["result"]["structuredContent"]["status"])

    def test_stdio_capability_view_and_route_are_execution_only(self) -> None:
        messages = [
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"}},
            },
            {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "oleander_capabilities",
                    "arguments": {
                        "live_observations": {
                            "vercel_connector": {"availability": "AVAILABLE", "observed_at": "2026-09-27T00:00:00Z"}
                        }
                    },
                },
            },
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "oleander_resolve_surface",
                    "arguments": {
                        "request": {
                            "required_capability_roles": ["DEPLOYMENT"],
                            "side_effect_class": "REMOTE_MUTATION",
                            "candidate_surface_ids": ["vercel_connector"]
                        },
                        "live_observations": {
                            "vercel_connector": {"availability": "AVAILABLE", "observed_at": "2026-09-27T00:00:00Z"}
                        }
                    },
                },
            },
        ]
        rows = self._run_messages(messages)
        capability = rows[1]["result"]["structuredContent"]
        route = rows[2]["result"]["structuredContent"]
        self.assertEqual("CURRENT_EXECUTION_CAPABILITY_VIEW_NOT_PROJECT_AUTHORITY", capability["semantic_class"])
        self.assertEqual("ROUTED", route["status"])
        self.assertEqual("EXECUTION_CAPABILITY_ONLY", route["selected_surface"]["authority_ceiling"])
        self.assertIn("MUTATION_PERMISSION", route["does_not_prove"])


if __name__ == "__main__":
    unittest.main()
