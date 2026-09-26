from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_system_gateway import build_system_context, environment_snapshot, run_gateway, validate_system_manifest  # noqa: E402


class SystemManagementGatewayTests(unittest.TestCase):
    def test_manifest_resolves_without_shadow_cos_authority(self) -> None:
        result = validate_system_manifest()
        self.assertEqual("PASS", result["status"])
        self.assertEqual([], result["missing_refs"])
        self.assertEqual([], result["forbidden_cos_ownership"])

    def test_context_does_not_invent_project_identity(self) -> None:
        context = build_system_context({"intent": "CONTINUE"})
        self.assertIsNone(context["project"]["project_id"])
        self.assertIsNone(context["project"]["project_state_ref"])
        self.assertEqual("RESOLUTION_CONTEXT_ONLY", context["authority_ceiling"])
        self.assertFalse(context["runtime"]["provider_session_is_project_state"])

    def test_explicit_project_identity_is_preserved_not_promoted(self) -> None:
        context = build_system_context({
            "intent": "CONTINUE",
            "project_id": "PRJ-TEST-001",
            "project_state_ref": "owner-native:test-state",
            "decision_object_id": "DEC-TEST-001"
        })
        self.assertEqual("PRJ-TEST-001", context["project"]["project_id"])
        self.assertEqual("owner-native:test-state", context["project"]["project_state_ref"])
        self.assertIn("project_current", context["does_not_prove"])

    def test_machine_local_environment_is_observation_only(self) -> None:
        environment = environment_snapshot()
        self.assertEqual("EXECUTION_ENVIRONMENT_OBSERVATION_NOT_AUTHORITY", environment["semantic_class"])
        self.assertIn(environment["machine_local_runtime_state"], {"FRESH", "STALE", "MISSING", "INVALID_TIMESTAMP"})
        self.assertEqual("CANONICAL_STATIC_REGISTRY_PLUS_CURRENT_LIVE_PROBE", environment["selection_rule"])

    def test_gateway_preserves_existing_resolver_decision(self) -> None:
        payload = {
            "intent": "CONTINUE",
            "task_id": "system-gateway-test",
            "status": "WORKING",
            "current_authority_fingerprint": "AUTH-GW-TEST-1",
            "checkpoint": {
                "checkpoint_state": "RESUMABLE",
                "authority_fingerprint": "AUTH-GW-TEST-1",
                "last_verified_artifact": {
                    "artifact_id": "ART-GW-TEST-1",
                    "hash_or_commit": "abc123",
                    "readback_verdict": "PASS"
                },
                "stale_reasons": [],
                "current_node": "ACTUAL_READBACK",
                "resume_from": "ACTUAL_READBACK",
                "next_allowed_action": "NEXT_NODE",
                "checkpoint_sequence": 2,
                "checkpoint_updated_at": "2026-09-26T00:00:00Z",
                "expected_checkpoint_sequence": 2,
                "executor_id": "COS-GW-TEST",
                "execution_lease_state": "NONE",
                "lease_acquired_at": "NOT_APPLICABLE"
            }
        }
        result = run_gateway(payload, publish_live=False)
        self.assertEqual("PASS", result["gateway"]["status"])
        self.assertEqual(
            "EXECUTE_NEXT_ALLOWED_ACTION",
            result["runtime_bridge"]["preflight"]["conversation_directive"]["action"]
        )
        self.assertFalse(result["gateway"]["changes_project_state"])
        self.assertFalse(result["gateway"]["changes_knowledge_authority"])


if __name__ == "__main__":
    unittest.main()
