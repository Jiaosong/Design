#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "validate_relationship_surface.py")
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)
EXAMPLE = ROOT / "examples" / "automotive_relationship_surface_candidate.json"


class ContractTests(unittest.TestCase):
    def load(self):
        return json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def test_example_contract_is_structurally_valid(self):
        data = self.load()
        self.assertEqual([], validator.validate_contract(data))

    def test_example_quantitative_curve_evidence_passes(self):
        data = self.load()
        results, errors = validator.evaluate_fairness(data)
        self.assertEqual([], errors)
        self.assertTrue(results)
        self.assertTrue(all(r["pass"] for r in results))
        self.assertLessEqual(results[0]["max_tangent_jump_deg"], 5.0)
        self.assertLessEqual(results[0]["spacing_cv"], 0.05)

    def test_m5_cannot_pass_before_surface_fairness(self):
        data = self.load()
        data["gate_state"]["M5"] = "PASS"
        errors = validator.validate_contract(data)
        self.assertTrue(any("M5 cannot PASS" in e for e in errors))

    def test_m6_plus_must_be_blocked_before_m5(self):
        data = self.load()
        data["gate_state"]["M6_plus_blocked"] = False
        errors = validator.validate_contract(data)
        self.assertTrue(any("M6+ must remain blocked" in e for e in errors))

    def test_smooth_shading_cannot_be_fairness_evidence(self):
        data = self.load()
        data["execution_geometry"]["smooth_shading_is_evidence"] = True
        errors = validator.validate_contract(data)
        self.assertTrue(any("smooth shading" in e.lower() for e in errors))

    def test_unknown_relationship_node_fails_closed(self):
        data = self.load()
        data["relationship_graph"]["edges"][0]["target"] = "RELNODE-MISSING"
        errors = validator.validate_contract(data)
        self.assertTrue(any("unknown node" in e for e in errors))

    def test_visible_kink_fails_tangent_threshold(self):
        data = self.load()
        ev = next(e for e in data["surface_fairness"]["evidence"] if e.get("kind") == "CURVE_SAMPLES")
        ev["points"] = [
            [-4, 0, 0], [-3, 0, 0], [-2, 0, 0], [-1, 0, 0],
            [0, 0, 1.0], [1, 0, 1.0], [2, 0, 1.0], [3, 0, 1.0], [4, 0, 1.0]
        ]
        results, errors = validator.evaluate_fairness(data)
        self.assertEqual([], errors)
        self.assertFalse(results[0]["pass"])
        self.assertTrue(any("max_tangent_jump_deg" in f for f in results[0]["failures"]))

    def test_relationships_must_precede_topology(self):
        data = self.load()
        data["relationship_graph"]["edges"] = []
        # The stdlib validator deliberately refuses an empty design-relation graph.
        errors = validator.validate_contract(data)
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
