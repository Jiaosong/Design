from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"
VALIDATOR_PATH = SCHEMA_DIR / "validate_professional_execution_capability_plan.py"
TEMPLATE_PATH = SCHEMA_DIR / "professional-execution-capability-plan.v1.template.json"

SPEC = importlib.util.spec_from_file_location("professional_execution_capability_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def template():
    return json.loads(TEMPLATE_PATH.read_text(encoding="utf-8"))


class ProfessionalExecutionCapabilityPlanTests(unittest.TestCase):
    def test_hold_template_validates(self):
        self.assertEqual([], validator.validate_payload(template()))

    def test_candidate_only_cannot_be_executable(self):
        payload = template()
        row = payload["capabilities"][0]
        row.update({
            "execution_mode": "CANDIDATE_ONLY",
            "authority_state": "CANDIDATE_OWNER",
            "availability_state": "AVAILABLE",
            "selected_owner_ref": "candidate/owner",
            "execution_surface_ref": "candidate/runtime",
            "actual_readback_method": "candidate reopen",
            "independent_review_owner_ref": "REVIEWER-1",
        })
        payload["blocking_capability_ids"] = []
        payload["plan_verdict"] = "EXECUTABLE"
        self.assertTrue(validator.validate_payload(payload))

    def test_unknown_runtime_cannot_be_executable(self):
        payload = template()
        row = payload["capabilities"][0]
        row.update({
            "execution_mode": "AGENT_EXECUTABLE",
            "authority_state": "CURRENT_OWNER",
            "availability_state": "UNKNOWN",
            "selected_owner_ref": "oleander-3d-pipeline",
            "execution_surface_ref": "blender-runtime",
            "actual_readback_method": "reopen native model",
            "independent_review_owner_ref": "REVIEWER-1",
        })
        payload["blocking_capability_ids"] = []
        payload["plan_verdict"] = "EXECUTABLE"
        self.assertTrue(validator.validate_payload(payload))

    def test_current_callable_route_can_be_executable(self):
        payload = template()
        row = payload["capabilities"][0]
        row.update({
            "execution_mode": "AGENT_EXECUTABLE",
            "authority_state": "CURRENT_OWNER",
            "availability_state": "AVAILABLE",
            "selected_owner_ref": "oleander-data-viz",
            "execution_surface_ref": "repo-native-svg-csv-json",
            "tool_adapter_ref": "CURRENT-RUNTIME-ROUTE",
            "actual_readback_method": "reopen generated SVG and source data",
            "independent_review_owner_ref": "INDEPENDENT-REVIEWER-1",
            "open_items": [],
        })
        payload["blocking_capability_ids"] = []
        payload["plan_verdict"] = "EXECUTABLE"
        self.assertEqual([], validator.validate_payload(payload))

    def test_project_specialist_binding_can_be_executable(self):
        payload = template()
        row = payload["capabilities"][0]
        row.update({
            "execution_mode": "PROJECT_SPECIALIST_BOUND",
            "authority_state": "PROJECT_AUTHORIZED_SPECIALIST",
            "availability_state": "AVAILABLE",
            "selected_owner_ref": "PROJECT-STRUCTURAL-ENGINEER",
            "specialist_binding_ref": "PROJECT_SPECIALIST_OWNER_BINDING:PSOB-STRUCT-001",
            "execution_surface_ref": "PROJECT-AUTHORIZED-SOLVER",
            "tool_adapter_ref": None,
            "actual_readback_method": "checked calculation package + native model readback",
            "independent_review_owner_ref": "PROJECT-INDEPENDENT-CHECKER",
            "open_items": [],
        })
        payload["blocking_capability_ids"] = []
        payload["plan_verdict"] = "EXECUTABLE"
        self.assertEqual([], validator.validate_payload(payload))


if __name__ == "__main__":
    unittest.main()
