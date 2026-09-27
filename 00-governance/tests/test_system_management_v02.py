from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_system_gateway import build_system_context, current_capability_view, resolve_capability_route  # noqa: E402
from oleander_system_linter import run_lint  # noqa: E402


class SystemManagementV02Tests(unittest.TestCase):
    def test_core_interface_primitives_are_stable_handoffs_not_new_stores(self) -> None:
        contract = json.loads((RUNTIME / "OLEANDER_CORE_INTERFACE_PRIMITIVES_v0.1.json").read_text(encoding="utf-8"))
        self.assertEqual("REFERENCE_ENVELOPE_AND_HANDOFF_ONLY", contract["authority_ceiling"])
        self.assertEqual(
            {
                "AuthorityRef", "ProjectRef", "KnowledgeMount", "DecisionObject", "ProfessionalStageRef",
                "ActionRequest", "ExecutionRoute", "ArtifactRef", "ReadbackResult", "ReviewResult",
                "PersistenceReceipt", "LearningCandidate",
            },
            set(contract["primitives"]),
        )
        for primitive in contract["primitives"].values():
            self.assertTrue(primitive["owner_contracts"])
            self.assertNotIn("storage_path", primitive)
            self.assertNotIn("database", primitive)

    def test_runtime_provider_v02_is_successor_without_relabelling_v01_benchmark(self) -> None:
        v01 = json.loads((RUNTIME / "OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json").read_text(encoding="utf-8"))
        v02 = json.loads((RUNTIME / "OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.2.json").read_text(encoding="utf-8"))
        benchmark = json.loads((RUNTIME / "runtime_provider_spikes" / "results" / "OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json").read_text(encoding="utf-8"))
        self.assertEqual("00-governance/runtime/OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json", v02["supersedes"])
        self.assertEqual(set(v01["providers_under_spike"]), set(v02["providers_under_spike"]))
        self.assertTrue(set(v01["required_provider_operations"]).issubset(v02["required_provider_operations"]))
        self.assertTrue(set(v01["hard_invariants"]).issubset(v02["hard_invariants"]))
        self.assertTrue(set(v01["execution_ledger"]["forbidden_authority_fields"]).issubset(v02["execution_ledger"]["forbidden_authority_fields"]))
        self.assertEqual("00-governance/runtime/OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json", benchmark["contract_ref"])
        self.assertIn("simulated_provider_outcome", v02["v0_1_benchmark_compatibility"]["benchmark_fixture_only_fields"])
        self.assertNotIn("simulated_provider_outcome", v02["action_envelope_required_fields"])

    def test_phase2_linter_passes(self) -> None:
        result = run_lint()
        self.assertEqual("PASS", result["status"], json.dumps(result, indent=2))

    def test_gateway_capability_view_is_non_authority(self) -> None:
        view = current_capability_view({})
        self.assertEqual("CURRENT_EXECUTION_CAPABILITY_VIEW_NOT_PROJECT_AUTHORITY", view["semantic_class"])
        self.assertEqual("EXECUTION_CAPABILITY_ONLY", view["authority_ceiling"])

    def test_gateway_resolve_requires_verified_current_observation(self) -> None:
        route = resolve_capability_route({
            "request": {
                "required_capability_roles": ["DEPLOYMENT"],
                "side_effect_class": "REMOTE_MUTATION",
                "candidate_surface_ids": ["vercel_connector"],
            },
            "live_observations": {
                "vercel_connector": {"availability": "AVAILABLE", "observed_at": "2026-09-27T00:00:00Z"}
            },
        })
        self.assertEqual("ROUTED", route["status"])
        self.assertTrue(route["route_is_ephemeral"])
        self.assertIn("MUTATION_PERMISSION", route["does_not_prove"])

    def test_provider_removal_does_not_remove_owner_native_project_state_ref(self) -> None:
        context = build_system_context({
            "project_id": "PRJ-REMOVAL-TEST",
            "project_state_ref": "owner-native:project-state@R12",
            "runtime_provider_id": "provider-that-is-not-installed",
        })
        self.assertEqual("owner-native:project-state@R12", context["project"]["project_state_ref"])
        self.assertEqual("provider-that-is-not-installed", context["runtime"]["provider_id"])
        self.assertFalse(context["runtime"]["provider_session_is_project_state"])


if __name__ == "__main__":
    unittest.main()
