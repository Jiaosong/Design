from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_environment_resolver import build_current_execution_view, machine_local_observations, resolve_execution_surface  # noqa: E402


class EnvironmentCapabilityResolverTests(unittest.TestCase):
    def test_stale_machine_snapshot_cannot_claim_available(self) -> None:
        stale = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        snapshot = {
            "snapshot_at": stale,
            "registry_identity": {"authority_ceiling": "EXECUTION_CAPABILITY_ONLY"},
            "cos_mcp_registry": [{"name": "Example MCP", "enabled": True, "status": "ready", "version": "1"}],
        }
        observed = machine_local_observations(snapshot)
        self.assertEqual("STALE", observed["state"])
        self.assertEqual("UNKNOWN", observed["surfaces"][0]["availability"])

    def test_fresh_cos_registry_ready_is_metadata_not_live_callability(self) -> None:
        fresh = datetime.now(timezone.utc).isoformat()
        snapshot = {
            "snapshot_at": fresh,
            "registry_identity": {"authority_ceiling": "EXECUTION_CAPABILITY_ONLY"},
            "cos_mcp_registry": [{"name": "Example MCP", "enabled": True, "status": "ready", "version": "1"}],
        }
        observed = machine_local_observations(snapshot)
        self.assertEqual("FRESH", observed["state"])
        surface = observed["surfaces"][0]
        self.assertEqual("UNKNOWN", surface["availability"])
        self.assertTrue(surface["declared_ready"])
        self.assertTrue(surface["requires_live_callability_probe"])
        view = build_current_execution_view(local_snapshot=snapshot)
        route = resolve_execution_surface({
            "required_capability_roles": ["MCP_TOOL_EXECUTION"],
            "side_effect_class": "READ_ONLY",
            "candidate_surface_ids": [surface["surface_id"]],
        }, view)
        self.assertEqual("HOLD_NO_VERIFIED_SURFACE", route["status"])

    def test_live_observation_can_route_verified_surface(self) -> None:
        view = build_current_execution_view(live_observations={
            "github_connector": {
                "availability": "AVAILABLE",
                "observed_at": datetime.now(timezone.utc).isoformat(),
                "reliability": "LIVE_TOOL_EXPOSURE",
            }
        })
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "REMOTE_MUTATION",
            "require_readback": True,
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("ROUTED", route["status"])
        self.assertEqual("github_connector", route["selected_surface"]["surface_id"])
        self.assertEqual("EXECUTION_CAPABILITY_ONLY", route["authority_ceiling"])

    def test_static_registry_alone_does_not_route_as_available(self) -> None:
        view = build_current_execution_view(live_observations={})
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "REMOTE_MUTATION",
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("HOLD_NO_VERIFIED_SURFACE", route["status"])

    def test_execution_surface_cannot_route_authority_mutation_without_existing_gate(self) -> None:
        view = build_current_execution_view(live_observations={
            "github_connector": {"availability": "AVAILABLE"}
        })
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "AUTHORITY_MUTATION",
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("HOLD_NO_VERIFIED_SURFACE", route["status"])

    def test_authorized_authority_mutation_may_use_transport_without_transferring_authority(self) -> None:
        view = build_current_execution_view(live_observations={
            "github_connector": {"availability": "AVAILABLE"}
        })
        route = resolve_execution_surface({
            "required_capability_roles": ["REPO_SOURCE_MUTATION"],
            "side_effect_class": "AUTHORITY_MUTATION",
            "authority_transition_authorized": True,
            "candidate_surface_ids": ["github_connector"],
        }, view)
        self.assertEqual("ROUTED", route["status"])
        self.assertEqual("EXECUTION_CAPABILITY_ONLY", route["selected_surface"]["authority_ceiling"])
        self.assertIn("MUTATION_PERMISSION", route["does_not_prove"])

    def test_release_transport_requires_existing_release_authority(self) -> None:
        view = build_current_execution_view(live_observations={
            "vercel_connector": {"availability": "AVAILABLE"}
        })
        blocked = resolve_execution_surface({
            "required_capability_roles": ["DEPLOYMENT"],
            "side_effect_class": "RELEASE_MUTATION",
            "candidate_surface_ids": ["vercel_connector"],
        }, view)
        self.assertEqual("HOLD_NO_VERIFIED_SURFACE", blocked["status"])
        routed = resolve_execution_surface({
            "required_capability_roles": ["DEPLOYMENT"],
            "side_effect_class": "RELEASE_MUTATION",
            "release_authority_verified": True,
            "candidate_surface_ids": ["vercel_connector"],
        }, view)
        self.assertEqual("ROUTED", routed["status"])
        self.assertEqual("EXECUTION_CAPABILITY_ONLY", routed["selected_surface"]["authority_ceiling"])

    def test_underspecified_request_does_not_pick_arbitrary_surface(self) -> None:
        view = build_current_execution_view(live_observations={
            "github_connector": {"availability": "AVAILABLE"}
        })
        route = resolve_execution_surface({"side_effect_class": "READ_ONLY"}, view)
        self.assertEqual("HOLD_INVALID_CAPABILITY_REQUEST", route["status"])


if __name__ == "__main__":
    unittest.main()
