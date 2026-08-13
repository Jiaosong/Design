import unittest

from orchestrator import evaluate_provider_chain, evaluate_promotion, scan_contradictions


def provider_snapshot(statuses):
    providers = []
    for provider, status in zip(
        ["current_authority", "github", "drive", "file_library", "runtime"],
        statuses,
    ):
        providers.append(
            {
                "provider": provider,
                "attempted": True,
                "status": status,
                "hits": [{"id": "x"}] if status == "FOUND" else [],
            }
        )
    return {"schema_version": "0.3", "query": "asset", "providers": providers}


class OrchestrationTests(unittest.TestCase):
    def test_provider_finds_highest_resolved_hit(self):
        result = evaluate_provider_chain(
            provider_snapshot(["NOT_FOUND", "FOUND", "NOT_FOUND", "NOT_FOUND", "NOT_FOUND"])
        )
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["selected_provider"], "github")

    def test_provider_blocks_lower_hit_when_higher_unavailable(self):
        result = evaluate_provider_chain(
            provider_snapshot(["UNAVAILABLE", "FOUND", "NOT_FOUND", "NOT_FOUND", "NOT_FOUND"])
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["code"], "CB-03_HIGHER_AUTHORITY_GAP")

    def test_provider_may_stop_after_resolved_hit(self):
        snapshot = {
            "schema_version": "0.3",
            "query": "asset",
            "providers": [
                {"provider": "current_authority", "attempted": True, "status": "NOT_FOUND", "hits": []},
                {"provider": "github", "attempted": True, "status": "FOUND", "hits": [{"id": "g"}]},
            ],
        }
        result = evaluate_provider_chain(snapshot)
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["selected_provider"], "github")

    def test_provider_e0_only_after_all_not_found(self):
        result = evaluate_provider_chain(provider_snapshot(["NOT_FOUND"] * 5))
        self.assertTrue(result["e0_eligible"])
        self.assertEqual(result["status"], "UNLOCATED")

    def test_provider_blocks_incomplete_chain_before_e0(self):
        snapshot = provider_snapshot(["NOT_FOUND"] * 5)
        snapshot["providers"].pop()
        self.assertEqual(evaluate_provider_chain(snapshot)["status"], "BLOCKED")

    def test_promotion_requires_all_compiled_gates(self):
        card = {
            "schema_version": "0.2",
            "object": {
                "name": "Release Object",
                "project_id": "PRJ-XJ01-CMF",
                "project_level": "P2",
                "case_id": None,
                "knowledge_position": "L7 Practice",
                "application_mapping": ["IP03"],
                "priority": "Priority-1",
            },
            "mode": "AUTHORITY",
            "decision_question": "Is this release candidate ready for promotion?",
            "problem_layer": "Evidence",
            "authority_source": {"state": "CANONICAL_AUTHORITY", "source_id": "S1", "location": "registry", "sha256": None},
            "locked_variables": ["geometry", "material"],
            "open_variables": [],
            "required_qa": ["Machine", "Visual", "Project"],
            "artifact_type": "release_package",
            "claim_types": ["rights", "release"],
            "evidence_state": {"digital": "PASS", "rights": "PASS"},
            "next_allowed_action": "PROMOTION_REVIEW",
            "sync_persistence_trigger": "FULL_SYNC",
            "review_history": [],
        }
        gate_results = {
            "Machine QA": "PASS",
            "Visual QA": "PASS",
            "Project QA": "PASS",
            "Artifact Review": "PASS",
            "Post-Generation Review": "PASS",
            "Rights Gate": "PASS",
            "Production Asset Persistence Gate": "PASS",
            "AR-S09 Release Package Review": "NOT_RUN",
        }
        self.assertEqual(evaluate_promotion(card, gate_results)["status"], "BLOCKED")

    def test_promotion_returns_human_decision_not_auto_promote(self):
        card = {
            "schema_version": "0.2",
            "object": {
                "name": "Release Object",
                "project_id": "PRJ-XJ01-CMF",
                "project_level": "P2",
                "case_id": None,
                "knowledge_position": "L7 Practice",
                "application_mapping": ["IP03"],
                "priority": "Priority-1",
            },
            "mode": "AUTHORITY",
            "decision_question": "Is this release candidate ready for promotion?",
            "problem_layer": "Evidence",
            "authority_source": {"state": "CANONICAL_AUTHORITY", "source_id": "S1", "location": "registry", "sha256": None},
            "locked_variables": ["geometry", "material"],
            "open_variables": [],
            "required_qa": ["Machine", "Visual", "Project"],
            "artifact_type": "release_package",
            "claim_types": ["rights", "release"],
            "evidence_state": {"digital": "PASS", "rights": "PASS"},
            "next_allowed_action": "PROMOTION_REVIEW",
            "sync_persistence_trigger": "FULL_SYNC",
            "review_history": [],
        }
        gate_results = {
            "Machine QA": "PASS",
            "Visual QA": "PASS",
            "Project QA": "PASS",
            "Artifact Review": "PASS",
            "Post-Generation Review": "PASS",
            "Rights Gate": "PASS",
            "Production Asset Persistence Gate": "PASS",
            "AR-S09 Release Package Review": "PASS",
        }
        result = evaluate_promotion(card, gate_results)
        self.assertEqual(result["status"], "READY_FOR_HUMAN_DECISION")
        self.assertTrue(result["human_decision_required"])
        self.assertIn("CONTRADICTION_SCAN", result["post_promotion_actions"])

    def test_contradiction_scan_pass(self):
        expected = {"version": "v1", "authority_state": "CANONICAL_AUTHORITY", "design_state": "PROMOTED"}
        manifest = {
            "object_id": "X",
            "expected": expected,
            "systems": {
                system: {"status": "FOUND", "fields": dict(expected)}
                for system in ["notion", "github", "drive"]
            },
        }
        self.assertEqual(scan_contradictions(manifest)["status"], "PASS")

    def test_contradiction_scan_detects_mismatch(self):
        expected = {"version": "v1", "authority_state": "CANONICAL_AUTHORITY"}
        systems = {
            system: {"status": "FOUND", "fields": dict(expected)}
            for system in ["notion", "github", "drive"]
        }
        systems["drive"]["fields"]["version"] = "v0"
        result = scan_contradictions({"object_id": "X", "expected": expected, "systems": systems})
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any(finding["code"] == "CONTRADICTION" for finding in result["findings"]))


if __name__ == "__main__":
    unittest.main()
