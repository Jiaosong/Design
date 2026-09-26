from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SERVER = ROOT / "00-governance" / "runtime" / "oleander_system_mcp.py"


class SystemMcpGatewayTests(unittest.TestCase):
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
        rows = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
        self.assertEqual([1, 2, 3], [row.get("id") for row in rows])
        self.assertEqual("oleander-system-gateway", rows[0]["result"]["serverInfo"]["name"])
        names = {tool["name"] for tool in rows[1]["result"]["tools"]}
        self.assertEqual(
            {
                "oleander_system_manifest",
                "oleander_system_context",
                "oleander_environment",
                "oleander_preflight",
                "oleander_system_self_test",
            },
            names,
        )
        self.assertEqual("PASS", rows[2]["result"]["structuredContent"]["status"])


if __name__ == "__main__":
    unittest.main()
