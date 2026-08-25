import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from scan_control_cards import scan_repository


def valid_card(problem_layer="Evidence", version="0.3"):
    card = {
        "schema_version": version,
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
    if version == "0.3":
        card["change_scope"] = {
            "kind": "NON_RESTRUCTURE",
            "surfaces": ["EVIDENCE_PACKAGE"],
            "established_object_baseline": [],
            "baseline_source": None,
            "greenfield_no_established_objects": False
        }
    return card


class RepositoryControlCardScanTests(unittest.TestCase):
    def write_json(self, root, relative, value):
        p = Path(root) / relative
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(value), encoding="utf-8")

    def test_arbitrary_filename_current_v03_card_is_discovered(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "90-shared/toolchains/example/arbitrary-name.json", valid_card("Evidence"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(len(result["discovered_current_control_cards"]), 1)
            self.assertEqual(result["discovered_current_control_cards"][0]["schema_version"], "0.3")

    def test_current_v02_card_outside_provenance_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "90-shared/toolchains/example/old-current.json", valid_card("Evidence", version="0.2"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(result["invalid_current_control_cards"][0]["errors"][0]["code"], "CURRENT_CONTROL_CARD_VERSION_DEPRECATED")

    def test_architecture_card_without_restructure_contract_fails(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "05-cases/example/current.json", valid_card("Architecture"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "FAIL")
            codes = {e["code"] for e in result["invalid_current_control_cards"][0]["errors"]}
            self.assertIn("NO_LOSS_ARCHITECTURE_SCOPE_CONTRADICTION", codes)
            self.assertIn("NO_LOSS_PRESERVATION_REVIEW_REQUIRED", codes)

    def test_delivery_restructure_outside_architecture_requires_review(self):
        with tempfile.TemporaryDirectory() as td:
            card = valid_card("Relation")
            card["change_scope"] = {
                "kind": "RESTRUCTURE",
                "surfaces": ["WEB", "FINAL_EDIT"],
                "established_object_baseline": ["PAGE-01"],
                "baseline_source": "CURRENT PUBLIC ARCHITECTURE",
                "greenfield_no_established_objects": False
            }
            self.write_json(td, "05-cases/example/current.json", card)
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "FAIL")
            codes = {e["code"] for e in result["invalid_current_control_cards"][0]["errors"]}
            self.assertIn("NO_LOSS_PRESERVATION_REVIEW_REQUIRED", codes)

    def test_architecture_greenfield_with_preservation_review_passes(self):
        with tempfile.TemporaryDirectory() as td:
            card = valid_card("Architecture")
            card["change_scope"] = {
                "kind": "RESTRUCTURE",
                "surfaces": ["PROJECT_ARCHITECTURE"],
                "established_object_baseline": [],
                "baseline_source": None,
                "greenfield_no_established_objects": True
            }
            card["preservation_review"] = {
                "global_fixed_chapter_count_applied": False,
                "decisions": []
            }
            self.write_json(td, "05-cases/example/current.json", card)
            self.assertEqual(scan_repository(Path(td))["status"], "PASS")

    def test_replay_and_example_zones_are_not_retroactively_migrated(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "00-governance/control-plane/replays/historical.json", valid_card("Architecture", version="0.2"))
            self.write_json(td, "00-governance/control-plane/examples/example.json", valid_card("Architecture", version="0.2"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["discovered_current_control_cards"], [])

    def test_legacy_top_level_roots_are_excluded(self):
        with tempfile.TemporaryDirectory() as td:
            self.write_json(td, "99-archive/old.json", valid_card("Architecture", version="0.2"))
            self.write_json(td, "practice/old.json", valid_card("Architecture", version="0.2"))
            self.write_json(td, "tools/old.json", valid_card("Architecture", version="0.2"))
            result = scan_repository(Path(td))
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["discovered_current_control_cards"], [])


if __name__ == "__main__":
    unittest.main()
