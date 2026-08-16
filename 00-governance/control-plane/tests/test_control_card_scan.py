import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from scan_control_cards import scan_repository


def valid_card(problem_layer="Evidence"):
    card = {
        "schema_version": "0.2",
        "object": {
            "name": "Current card",
            "project_id": "SYS-TEST",
            "project_level": "P2",
            "case_id": None,
            "knowledge_position": "L7 Practice",
            "application_mapping": [],
            "priority": None
        },
        "mode": "CANDIDATE",
        "decision_question": "Is the current object valid?",
        "problem_layer": problem_layer,
        "authority_source": {"state": "WORKING_SOURCE", "source_id": "S1", "location": "x", "sha256": None},
        "locked_variables": [],
        "open_variables": [],
        "required_qa": ["Machine", "Visual", "Project"],
        "artifact_type": "documentation",
        "claim_types": [],
        "evidence_state": {"digital": "OPEN"},
        "next_allowed_action": "REVIEW",
        "sync_persistence_trigger": "NONE",
        "review_history": []
    }
    return card


class RepositoryControlCardScanTests(unittest.TestCase):
    def write_json(self, root, relative, value):
        p = Path(root) / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value), encoding="utf-8")

    def test_arbitrary_filename_current_card_is_discovered(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "90-shared/toolchains/example/E3_CONTROL_CARD.json", valid_card("Evidence"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(len(result["discovered_current_control_cards"]), 1)

    def test_architecture_card_without_preservation_review_fails(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "05-cases/example/current.json", valid_card("Architecture"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["invalid_current_control_cards"][0]["errors"][0]["code"], "NO_LOSS_PRESERVATION_REVIEW_REQUIRED")

    def test_architecture_card_with_preservation_review_passes(self):
        with tempfile.TemporaryDirectory() as td:
            card = valid_card("Architecture")
            card["preservation_review"] = {
                "established_objects_present": False,
                "global_fixed_chapter_count_applied": False,
                "decisions": []
            }
            self.write_json(td, "05-cases/example/current.json", card)
            self.assertEqual(scan_repository(Path(td))["status"], "PASS")

    def test_replay_and_example_zones_are_not_retroactively_migrated(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "00-governance/control-plane/replays/historical.json", valid_card("Architecture"))
            self.write_json(td, "00-governance/control-plane/examples/example.json", valid_card("Architecture"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["discovered_current_control_cards"], [])

    def test_legacy_top_level_roots_are_excluded(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "99-archive/old.json", valid_card("Architecture"))
            self.write_json(td, "practice/old.json", valid_card("Architecture"))
            self.write_json(td, "tools/old.json", valid_card("Architecture"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["discovered_current_control_cards"], [])


if __name__ == "__main__":
    unittest.main()
