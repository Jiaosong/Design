from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "schemas"
VALIDATOR_PATH = SCHEMA_DIR / "validate_project_closure_objects.py"
SPEC = importlib.util.spec_from_file_location("closure_validator", VALIDATOR_PATH)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


def load(name: str):
    return json.loads((SCHEMA_DIR / name).read_text(encoding="utf-8"))


def project_flow_base():
    return {
        "project": {"name": "Test", "project_level": "P2", "project_id": "PRJ-TEST-001"},
        "decision_question": "Can the current bounded claim proceed?",
        "design_state": "CANDIDATE",
        "authority": {"design": {"state": "CANDIDATE_AUTHORITY", "source": "TEST", "hash": None}},
        "fidelity": "FID1_DESIGN_VALIDATION",
        "locked_variables": [],
        "open_variables": [],
        "exit_condition": "All triggered promotion prerequisites close.",
        "persistence": {"policy": "RECEIPT_ONLY", "pap_required": False, "pap_status": "NOT_TRIGGERED"},
        "promotion": {"eligible": False, "decision": "PROMOTE", "reason": "schema guard test"}
    }


class ProjectClosureObjectTests(unittest.TestCase):
    def test_hold_templates_validate(self):
        for name in (
            "cross-disciplinary-integration-receipt.v1.template.json",
            "structural-engineering-design-process-receipt.v1.template.json",
            "building-services-mep-design-process-receipt.v1.template.json",
            "project-requirement-acceptance-baseline.v1.template.json",
            "project-configuration-change-register.v1.template.json",
            "project-risk-hazard-register.v1.template.json",
            "project-operational-acceptance-compilation.v1.template.json",
            "project-specialist-owner-binding.v1.template.json",
        ):
            with self.subTest(name=name):
                self.assertEqual([], validator.validate_payload(load(name)))

    def test_structural_stage_enum_matches_current_process(self):
        schema = load("structural-engineering-design-process-receipt.v1.schema.json")
        process = load("structural-engineering-design-process.v1.json")
        schema_ids = set(schema["$defs"]["stageRecord"]["properties"]["stage_id"]["enum"])
        process_ids = {row["stage_id"] for row in process["stages"]}
        self.assertEqual(process_ids, schema_ids)

    def test_mep_stage_enum_matches_current_process(self):
        schema = load("building-services-mep-design-process-receipt.v1.schema.json")
        process = load("building-services-mep-design-process.v1.json")
        schema_ids = set(schema["$defs"]["stageRecord"]["properties"]["stage_id"]["enum"])
        process_ids = {row["stage_id"] for row in process["stages"]}
        self.assertEqual(process_ids, schema_ids)

    def test_integration_pass_fails_when_critical_interface_blocked(self):
        payload = load("cross-disciplinary-integration-receipt.v1.template.json")
        payload["integration_verdict"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_integration_pass_valid_when_closed(self):
        payload = load("cross-disciplinary-integration-receipt.v1.template.json")
        row = payload["critical_interfaces"][0]
        row.update({"actual_maturity": "VERIFIED", "disposition": "CLOSED", "authority_state": "RESOLVED", "readback_refs": ["RB-1"]})
        payload["unresolved_major_critical_interfaces"] = []
        payload["blocked_interfaces"] = []
        payload["unresolved_authority_conflicts"] = []
        payload["integrated_readback_refs"] = ["RB-1"]
        payload["reviewer_independence_state"] = "NOT_REQUIRED"
        payload["integration_verdict"] = "PASS"
        payload["promotion_ceiling"] = "BOUNDED_CURRENT_CLAIM"
        self.assertEqual([], validator.validate_payload(payload))

    def test_structural_pass_fails_without_native_readback_and_check(self):
        payload = load("structural-engineering-design-process-receipt.v1.template.json")
        payload["result"] = "PASS"
        payload["blocking_open_items"] = []
        payload["stage_records"][0]["status"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_structural_pass_valid_when_closed(self):
        payload = load("structural-engineering-design-process-receipt.v1.template.json")
        row = payload["stage_records"][0]
        row.update({
            "status": "PASS",
            "native_output_refs": ["STRUCT-BASIS-1"],
            "actual_readback_refs": ["STRUCT-RB-1"],
            "checking_state": "PASS",
            "interface_state": "PASS",
            "open_items": [],
        })
        payload["independent_check"] = {"required": True, "state": "PASS", "reviewer_ref": "CHECKER-1", "review_input_refs": ["STRUCT-BASIS-1"]}
        payload["blocking_open_items"] = []
        payload["result"] = "PASS"
        self.assertEqual([], validator.validate_payload(payload))

    def test_mep_pass_fails_when_commissioning_open(self):
        payload = load("building-services-mep-design-process-receipt.v1.template.json")
        payload["result"] = "PASS"
        payload["blocking_open_items"] = []
        payload["stage_records"][0].update({"status": "PASS", "native_output_refs": ["MEP-1"], "actual_readback_refs": ["RB-1"], "open_items": []})
        self.assertTrue(validator.validate_payload(payload))

    def test_mep_pass_valid_when_closed(self):
        payload = load("building-services-mep-design-process-receipt.v1.template.json")
        payload["stage_records"][0].update({"status": "PASS", "native_output_refs": ["MEP-1"], "actual_readback_refs": ["RB-1"], "open_items": []})
        payload["system_tracks"][0].update({"status": "PASS", "design_refs": ["MEP-1"], "commissioning_state": "PASS", "evidence_refs": ["CX-1"]})
        payload["professional_review"] = {"required": True, "state": "PASS", "reviewer_ref": "MEP-REVIEWER-1", "review_input_refs": ["MEP-1", "CX-1"]}
        payload["blocking_open_items"] = []
        payload["result"] = "PASS"
        self.assertEqual([], validator.validate_payload(payload))

    def test_requirement_pass_fails_when_requirement_unverified(self):
        payload = load("project-requirement-acceptance-baseline.v1.template.json")
        payload["status"] = "CURRENT"
        payload["blocking_requirement_ids"] = []
        payload["baseline_verdict"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_requirement_pass_valid_when_verified(self):
        payload = load("project-requirement-acceptance-baseline.v1.template.json")
        req = payload["requirements"][0]
        req.update({"applicability": "APPLICABLE", "verification_state": "PASS", "evidence_refs": ["TEST-1"]})
        payload["status"] = "CURRENT"
        payload["blocking_requirement_ids"] = []
        payload["baseline_verdict"] = "PASS"
        self.assertEqual([], validator.validate_payload(payload))

    def test_validation_required_must_pass_for_baseline_pass(self):
        payload = load("project-requirement-acceptance-baseline.v1.template.json")
        req = payload["requirements"][0]
        req.update({"applicability": "APPLICABLE", "verification_state": "PASS", "evidence_refs": ["TEST-1"], "validation_required": True, "validation_state": "NOT_RUN"})
        payload["status"] = "CURRENT"
        payload["blocking_requirement_ids"] = []
        payload["baseline_verdict"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_duplicate_requirement_id_rejected(self):
        payload = load("project-requirement-acceptance-baseline.v1.template.json")
        payload["requirements"].append(copy.deepcopy(payload["requirements"][0]))
        self.assertTrue(validator.validate_payload(payload))

    def test_configuration_pass_requires_propagated_changes(self):
        payload = load("project-configuration-change-register.v1.template.json")
        payload["status"] = "CURRENT"
        payload["baselines"][0]["state"] = "CURRENT"
        payload["open_issue_ids"] = []
        payload["changes"] = [{
            "change_id": "CHG-1", "in_claim": True, "source_ref": "SRC-1", "owner_ref": "OWNER-1",
            "change_class": "INTERFACE", "affected_refs": ["OBJ-1"], "approval_state": "APPROVED",
            "propagation_state": "PENDING", "reacceptance_required": True, "reacceptance_state": "NOT_RUN"
        }]
        payload["register_verdict"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_risk_pass_requires_mitigation_evidence(self):
        payload = load("project-risk-hazard-register.v1.template.json")
        payload["status"] = "CURRENT"
        payload["blocking_risk_ids"] = []
        payload["risks"][0]["state"] = "CLOSED"
        payload["register_verdict"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_operational_pass_requires_real_closeout(self):
        payload = load("project-operational-acceptance-compilation.v1.template.json")
        payload["status"] = "CURRENT"
        payload["operational_verdict"] = "PASS"
        self.assertTrue(validator.validate_payload(payload))

    def test_specialist_binding_pass_rejects_candidate_or_generic_skill_substitution(self):
        payload = load("project-specialist-owner-binding.v1.template.json")
        payload.update({
            "status": "CURRENT",
            "owner_kind": "PROJECT_ORGANIZATION_SPECIALIST",
            "owner_ref": "OLEANDER Technical Drawing",
            "authorization_ref": "PROJECT-AUTH-1",
            "authorization_state": "VERIFIED",
            "scope_refs": ["DRAWING-SCOPE-1"],
            "required_native_outputs": ["PLAN", "SECTION"],
            "binding_verdict": "PASS",
        })
        self.assertTrue(validator.validate_payload(payload))

    def test_specialist_binding_pass_valid_when_explicitly_authorized(self):
        payload = load("project-specialist-owner-binding.v1.template.json")
        payload.update({
            "status": "CURRENT",
            "owner_kind": "PROJECT_ORGANIZATION_SPECIALIST",
            "owner_ref": "PROJECT-CAD-BIM-SPECIALIST-01",
            "authorization_ref": "PROJECT-AUTH-1",
            "authorization_state": "VERIFIED",
            "scope_refs": ["DRAWING-SCOPE-1"],
            "required_native_outputs": ["PLAN", "SECTION"],
            "binding_verdict": "PASS",
        })
        self.assertEqual([], validator.validate_payload(payload))

    def test_project_flow_promotion_rejects_candidate_technical_drawing_owner(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = load("oleander-project-flow-v0.3.schema.json")
        payload = project_flow_base()
        payload["technical_drawing_execution"] = {
            "triggered": True,
            "owner_state": "CANDIDATE_BODY_HOLD",
            "owner_ref": None,
            "required_native_outputs": ["PLAN"],
            "hold_reason": "Candidate body is not Current callable authority."
        }
        self.assertTrue(list(jsonschema.Draft202012Validator(schema).iter_errors(payload)))

    def test_project_flow_promotion_requires_binding_ref_for_project_specialist(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = load("oleander-project-flow-v0.3.schema.json")
        payload = project_flow_base()
        payload["technical_drawing_execution"] = {
            "triggered": True,
            "owner_state": "PROJECT_SPECIALIST_BOUND",
            "owner_ref": "PROJECT-CAD-BIM-SPECIALIST-01",
            "binding_ref": None,
            "binding_hash": None,
            "required_native_outputs": ["PLAN"],
            "hold_reason": None
        }
        self.assertTrue(list(jsonschema.Draft202012Validator(schema).iter_errors(payload)))

    def test_project_flow_promotion_accepts_explicit_project_specialist_binding(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = load("oleander-project-flow-v0.3.schema.json")
        payload = project_flow_base()
        payload["technical_drawing_execution"] = {
            "triggered": True,
            "owner_state": "PROJECT_SPECIALIST_BOUND",
            "owner_ref": "PROJECT-CAD-BIM-SPECIALIST-01",
            "binding_ref": "PROJECT_SPECIALIST_OWNER_BINDING:PSOB-1",
            "binding_hash": "abc123",
            "required_native_outputs": ["PLAN"],
            "hold_reason": None
        }
        self.assertEqual([], list(jsonschema.Draft202012Validator(schema).iter_errors(payload)))

    def test_project_flow_promotion_rejects_open_project_controls(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema = load("oleander-project-flow-v0.3.schema.json")
        payload = project_flow_base()
        payload["project_requirement_acceptance"] = {"triggered": True, "status": "HOLD", "baseline_ref": None, "blocking_requirement_ids": ["REQ-1"], "stale": False}
        payload["configuration_change_control"] = {"triggered": True, "status": "HOLD", "register_ref": None, "open_issue_ids": ["CHG-1"], "stale": False}
        payload["risk_hazard_control"] = {"triggered": True, "status": "HOLD", "register_ref": None, "blocking_risk_ids": ["RISK-1"], "stale": False}
        payload["operational_acceptance"] = {"triggered": True, "status": "HOLD", "compilation_ref": None, "blocking_items": ["DEFECT-1"], "stale": False}
        self.assertTrue(list(jsonschema.Draft202012Validator(schema).iter_errors(payload)))


if __name__ == "__main__":
    unittest.main()
