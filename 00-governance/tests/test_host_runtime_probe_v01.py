from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_host_runtime_probe import build_host_runtime_view, probe_cos_native, probe_dsh_host  # noqa: E402


class HostRuntimeProbeV01Tests(unittest.TestCase):
    def test_missing_dsh_is_visible_but_unavailable(self) -> None:
        result = probe_dsh_host("__oleander_missing_dsh_binary__")
        self.assertEqual("DSH_HOST", result["host_class"])
        self.assertEqual("UNAVAILABLE", result["availability"])
        self.assertFalse(result["capabilities_runtime_verified"])
        self.assertIn("PROJECT_CURRENT", result["does_not_prove"])

    def test_stale_cos_snapshot_never_claims_available(self) -> None:
        stale = {
            "snapshot_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
            "registry_identity": {"authority_ceiling": "EXECUTION_CAPABILITY_ONLY"},
            "cos_mcp_registry": [{"name": "Example", "enabled": True, "status": "ready", "source_kind": "local"}],
        }
        result = probe_cos_native(stale)
        self.assertEqual("STALE", result["status"])
        self.assertEqual("UNKNOWN", result["availability"])
        self.assertFalse(result["capabilities_runtime_verified"])

    def test_host_runtime_view_keeps_host_state_below_project_authority(self) -> None:
        stale = {
            "snapshot_at": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
            "registry_identity": {"authority_ceiling": "EXECUTION_CAPABILITY_ONLY"},
            "cos_mcp_registry": [],
        }
        result = build_host_runtime_view(
            local_host_ready=True,
            local_snapshot=stale,
            dsh_binary_override="__oleander_missing_dsh_binary__",
        )
        hosts = {row["host_runtime_id"]: row for row in result["hosts"]}
        self.assertEqual("AVAILABLE", hosts["design_system_local_host"]["availability"])
        self.assertEqual("UNAVAILABLE", hosts["dsh_host"]["availability"])
        self.assertEqual("UNKNOWN", hosts["cos_native"]["availability"])
        self.assertIn("PROJECT_CURRENT", result["does_not_prove"])


if __name__ == "__main__":
    unittest.main()
