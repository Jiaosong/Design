import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from control_plane import (  # noqa: E402
    locate_asset,
    revision_breaker,
    run_check,
    select_gate_profile,
    validate_card,
)


def base_card():
    return {
        "schema_version": "0.2",
        "object": {
            "name": "Test Object",
            "project_id": "PRJ-XJ01-CMF",
            "project_level": "P2",
            "case_id": None,
            "knowledge_position": "L7 Practice",
            "application_mapping": ["IP03"],
            "priority": "Priority-1",
        },
        "mode": "EXPLORE",
        "decision_question": "Does A outperform B under fixed conditions?",
        "problem_layer": "Parameter",
        "authority_source": {"state": "WORKING_SOURCE", "source_id": "S1", "location": "x", "sha256": None},
        "locked_variables": ["geometry"],
        "open_variables": ["material"],
        "required_qa": ["Visual"],
        "artifact_type": "visual_cmf",
        "claim_types": [],
        "evidence_state": {"digital": "OPEN", "physical": "NOT_RUN"},
        "next_allowed_action": "COMPARE",
        "sync_persistence_trigger": "NONE",
        "review_history": [],
    }


class ControlPlaneTests(unittest.TestCase):
    def test_valid_explore_card(self):
        self.assertFalse([f for f in validate_card(base_card()) if f.level == "ERROR"])
        self.assertEqual(run_check(base_card())["status"], "PASS")

    def test_namespace_case_project_collision_fails(self):
        card = base_card()
        card["object"]["project_id"] = "C04-WS-04"
        codes = {f.code for f in validate_card(card)}
        self.assertIn("NAMESPACE_CASE_PROJECT_COLLISION", codes)

    def test_application_project_collision_fails(self):
        card = base_card()
        card["object"]["project_id"] = "IP03-WORK"
        codes = {f.code for f in validate_card(card)}
        self.assertIn("NAMESPACE_APPLICATION_PROJECT_COLLISION", codes)

    def test_candidate_requires_three_qa_layers(self):
        card = base_card()
        card["mode"] = "CANDIDATE"
        codes = {f.code for f in validate_card(card)}
        self.assertIn("GATE_PROFILE_CANDIDATE_QA", codes)

    def test_authority_triggers_existing_specialist_gates(self):
        card = base_card()
        card["mode"] = "AUTHORITY"
        card["authority_source"]["state"] = "CANONICAL_AUTHORITY"
        card["required_qa"] = ["Machine", "Visual", "Project"]
        card["artifact_type"] = "release_package"
        card["claim_types"] = ["rights", "reality", "engineering", "human_test", "release"]
        card["sync_persistence_trigger"] = "FULL_SYNC"
        profile = select_gate_profile(card)
        self.assertIn("Production Asset Persistence Gate", profile.specialist_gates)
        self.assertIn("AR-S09 Release Package Review", profile.specialist_gates)
        self.assertIn("Rights Gate", profile.specialist_gates)
        self.assertIn("Reality Gate", profile.specialist_gates)
        self.assertIn("Engineering Gate", profile.specialist_gates)
        self.assertIn("Human Test Gate", profile.specialist_gates)

    def test_repeated_revise_breaker_trips(self):
        card = base_card()
        entry = {
            "decision_question": card["decision_question"],
            "problem_layer": card["problem_layer"],
            "visual_result": "REVISE",
            "project_result": "PASS",
            "timestamp": None,
        }
        card["review_history"] = [dict(entry), dict(entry)]
        result = revision_breaker(card)
        self.assertTrue(result.tripped)
        self.assertEqual(result.next_allowed_action, "ROOT_CAUSE_RECLASSIFICATION")
        self.assertEqual(run_check(card)["status"], "BLOCKED")

    def test_breaker_does_not_trip_after_problem_layer_change(self):
        card = base_card()
        card["review_history"] = [
            {
                "decision_question": card["decision_question"],
                "problem_layer": "Parameter",
                "visual_result": "REVISE",
                "project_result": "PASS",
                "timestamp": None,
            },
            {
                "decision_question": card["decision_question"],
                "problem_layer": "Topology",
                "visual_result": "REVISE",
                "project_result": "PASS",
                "timestamp": None,
            },
        ]
        self.assertFalse(revision_breaker(card).tripped)

    def test_asset_locator_searches_registry_and_filesystem(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "XJ01_R02_calibration_master.obj"
            p.write_text("o test", encoding="utf-8")
            result = locate_asset("calibration_master", [td], {"assets": []})
            self.assertEqual(result["status"], "FOUND")
            self.assertTrue(result["filesystem_hits"])

        result = locate_asset(
            "R54",
            [],
            {"assets": [{"id": "STD-R54", "name": "R54 Product Rendering Standard", "location": "registry"}]},
        )
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["registry_hits"][0]["id"], "STD-R54")


if __name__ == "__main__":
    unittest.main()
