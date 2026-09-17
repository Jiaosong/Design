import copy
import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
VALIDATOR = ROOT / "00-governance/schemas/validate_design_development_receipts.py"
DD_TEMPLATE = ROOT / "00-governance/schemas/design-quality-development-receipt.v1.template.json"
ARCH_TEMPLATE = ROOT / "00-governance/schemas/architecture-design-development-receipt.v1.template.json"


def load_validator():
    spec = importlib.util.spec_from_file_location("design_development_receipt_validator", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DesignDevelopmentReceiptContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = load_validator()
        cls.dd = json.loads(DD_TEMPLATE.read_text(encoding="utf-8"))
        cls.arch = json.loads(ARCH_TEMPLATE.read_text(encoding="utf-8"))

    def test_fail_safe_templates_are_structurally_valid(self):
        self.assertEqual(self.validator.validate_payload(copy.deepcopy(self.dd)), [])
        self.assertEqual(self.validator.validate_payload(copy.deepcopy(self.arch)), [])

    def test_generic_design_body_title_is_rejected(self):
        payload = copy.deepcopy(self.dd)
        payload["body_structure"]["title"] = "Analysis"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("title is generic" in error for error in errors), errors)

    def test_design_keep_rejects_missing_body_responsibility(self):
        payload = copy.deepcopy(self.dd)
        payload["result"] = "KEEP"
        payload["stale"] = False
        payload["independent_design_review"] = {
            "status": "KEEP",
            "reviewer_independent_from_producer": True,
            "reason": "bounded test reviewer"
        }
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("cannot retain MISSING" in error for error in errors), errors)

    def make_valid_design_keep(self):
        payload = copy.deepcopy(self.dd)
        payload["result"] = "KEEP"
        payload["stale"] = False
        payload["design_maturity"] = "DQ1_DIRECTION"
        payload["in_claim_blocking_design_fail_count"] = 0
        for field in (
            "design_language_state",
            "experience_state",
            "human_relation_state",
            "sensory_state",
            "detail_craft_state",
            "adaptation_state",
            "meaning_memory_state",
            "coherence_state",
            "content_projection_state",
        ):
            payload[field] = "KEEP"
        payload["genericity_attack"] = {
            "status": "PASS",
            "findings": ["bounded test attack passed"],
        }
        payload["independent_design_review"] = {
            "status": "KEEP",
            "reviewer_independent_from_producer": True,
            "reason": "bounded test reviewer",
            "reviewer_id": "TEST-INDEPENDENT-REVIEWER",
            "review_input_bindings": [
                {
                    "artifact_ref": payload["artifact_refs"][0],
                    "revision_or_hash": "TEST-IMMUTABLE-REVISION-001",
                }
            ],
        }
        for entry in payload["body_structure"]["section_coverage"]:
            entry["status"] = "PRESENT"
            entry["visible_heading_or_locator"] = entry["semantic_role"]
            entry["reason"] = None
        for readback in payload["readback_conditions"]:
            readback["status"] = "PASS"
        return payload

    def test_design_keep_requires_all_declared_readbacks_to_pass(self):
        payload = self.make_valid_design_keep()
        payload["readback_conditions"][0]["status"] = "REVISE"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(
            any("every declared readback_condition to be PASS" in error for error in errors),
            errors,
        )

    def test_design_keep_requires_every_artifact_to_have_readback(self):
        payload = self.make_valid_design_keep()
        payload["artifact_refs"].append("SECOND-NATIVE-ARTIFACT")
        errors = self.validator.validate_payload(payload)
        self.assertTrue(
            any("every artifact_ref to participate in readback_conditions" in error for error in errors),
            errors,
        )

    def test_design_keep_requires_coherence_and_genericity_closure(self):
        payload = self.make_valid_design_keep()
        payload["coherence_state"] = "REVISE"
        payload["genericity_attack"]["status"] = "HOLD"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("coherence_state=KEEP" in error for error in errors), errors)
        self.assertTrue(any("genericity_attack.status" in error for error in errors), errors)

    def test_applicable_comparison_requires_real_option_set_and_fixed_conditions(self):
        payload = copy.deepcopy(self.dd)
        payload["candidate_comparison"] = {
            "applicable": True,
            "candidate_refs": ["ONLY-ONE"],
            "fixed_comparison_conditions": [],
            "decision": "",
        }
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("at least two candidate_refs" in error for error in errors), errors)
        self.assertTrue(any("fixed_comparison_conditions" in error for error in errors), errors)
        self.assertTrue(any("bounded decision" in error for error in errors), errors)

    def test_dq4_dq5_require_independent_reviewer_even_without_keep(self):
        payload = copy.deepcopy(self.dd)
        payload["design_maturity"] = "DQ4_DISTINCTIVE_RESOLVED_SYSTEM"
        payload["independent_design_review"]["reviewer_independent_from_producer"] = False
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("DQ4_DISTINCTIVE_RESOLVED_SYSTEM requires" in error for error in errors), errors)

    def test_dq5_requires_cross_context_transfer_and_counterevidence_boundary(self):
        payload = copy.deepcopy(self.dd)
        payload["design_maturity"] = "DQ5_PROVEN_CROSS_CONTEXT_LANGUAGE"
        payload["independent_design_review"]["reviewer_independent_from_producer"] = True
        payload["cross_context_validation"] = {
            "context_refs": ["ONLY-ONE-CONTEXT"],
            "material_difference_between_contexts": "",
            "identity_relation_preserved": "",
            "counterevidence_or_none_reason": "",
            "transfer_boundary": "",
            "does_not_prove": [],
        }
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("at least two distinct real context_refs" in error for error in errors), errors)
        self.assertTrue(any("transfer_boundary" in error for error in errors), errors)
        self.assertTrue(any("counterevidence_or_none_reason" in error for error in errors), errors)
        self.assertTrue(any("does_not_prove boundary" in error for error in errors), errors)

    def test_oe2_mount_requires_conditions_and_boundary(self):
        payload = copy.deepcopy(self.dd)
        payload["body_structure"]["knowledge_mount_refs"] = ["KM-TEST-001"]
        payload["knowledge_mounts"] = [{
            "source_mount_record_ref": "KM-TEST-001",
            "mount_record_revision_or_hash": "sha256:test",
            "knowledge_ref": "KN-TEST",
            "use_role": "CONDITIONAL",
            "eligibility_snapshot": "OE2",
            "claim_ceiling": "TEST_ONLY",
            "applicability": "bounded test",
            "conditions": [],
            "does_not_prove": [],
            "review_basis": "test"
        }]
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("OE2 requires explicit conditions" in error for error in errors), errors)
        self.assertTrue(any("OE2 requires does_not_prove boundary" in error for error in errors), errors)

    def test_oe1_cannot_drive_in_claim_decision(self):
        payload = copy.deepcopy(self.dd)
        payload["body_structure"]["knowledge_mount_refs"] = ["KM-TEST-001"]
        payload["knowledge_mounts"] = [{
            "source_mount_record_ref": "KM-TEST-001",
            "mount_record_revision_or_hash": "sha256:test",
            "knowledge_ref": "KN-TEST",
            "use_role": "PRIMARY",
            "eligibility_snapshot": "OE1",
            "claim_ceiling": "NONE",
            "applicability": "not eligible",
            "conditions": [],
            "does_not_prove": ["in-claim decision"],
            "review_basis": "test"
        }]
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("OE1 cannot be a PRIMARY/SUPPORTING" in error for error in errors), errors)

    def test_mount_snapshot_cannot_exist_without_r_b_mount_record_ref(self):
        payload = copy.deepcopy(self.dd)
        payload["knowledge_mounts"] = [{
            "knowledge_ref": "KN-TEST",
            "use_role": "CONTEXT",
            "eligibility_snapshot": "OE2",
            "mount_record_revision_or_hash": "sha256:test",
            "claim_ceiling": "TEST_ONLY",
            "applicability": "bounded test",
            "conditions": ["bounded"],
            "does_not_prove": ["OE authority"],
            "review_basis": "test"
        }]
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("requires body_structure.knowledge_mount_refs" in error for error in errors), errors)

    def test_design_keep_rejects_dimension_hold(self):
        payload = self.make_valid_design_keep()
        payload["experience_state"] = "HOLD"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("experience_state=KEEP" in error for error in errors), errors)

    def test_not_applicable_dimension_requires_reason(self):
        payload = copy.deepcopy(self.dd)
        payload["human_relation_state"] = "NOT_APPLICABLE_WITH_REASON"
        payload.pop("human_relation_reason", None)
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("requires human_relation_reason" in error for error in errors), errors)

    def test_v10_legacy_in_progress_dimension_remains_read_compatible(self):
        payload = copy.deepcopy(self.dd)
        payload["schema_version"] = "1.0"
        payload.pop("in_claim_blocking_design_fail_count", None)
        payload["human_relation_state"] = "IN_PROGRESS"
        errors = self.validator.validate_payload(payload)
        self.assertEqual(errors, [])

    def test_v10_pre_body_receipt_remains_read_compatible(self):
        payload = copy.deepcopy(self.dd)
        payload["schema_version"] = "1.0"
        payload.pop("body_structure", None)
        payload.pop("in_claim_blocking_design_fail_count", None)
        errors = self.validator.validate_payload(payload)
        self.assertEqual(errors, [])

    def test_v10_legacy_single_candidate_comparison_remains_read_compatible(self):
        payload = copy.deepcopy(self.dd)
        payload["schema_version"] = "1.0"
        payload.pop("in_claim_blocking_design_fail_count", None)
        payload["candidate_comparison"] = {
            "applicable": True,
            "candidate_refs": ["LEGACY-SINGLE-CANDIDATE"],
            "fixed_comparison_conditions": ["legacy bounded condition"],
            "decision": "historical bounded decision",
        }
        errors = self.validator.validate_payload(payload)
        self.assertEqual(errors, [])

    def test_v11_rejects_legacy_in_progress_dimension(self):
        payload = copy.deepcopy(self.dd)
        payload["human_relation_state"] = "IN_PROGRESS"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("IN_PROGRESS" in error for error in errors), errors)

    def test_v11_triggered_conditional_dimension_requires_state_field(self):
        payload = copy.deepcopy(self.dd)
        payload["triggered_design_dimensions"].append("DD-05_HUMAN_RELATION")
        payload.pop("human_relation_state", None)
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("human_relation_state" in error for error in errors), errors)

    def test_design_keep_rejects_dq0(self):
        payload = self.make_valid_design_keep()
        payload["design_maturity"] = "DQ0_UNDEFINED"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("DQ0_UNDEFINED" in error for error in errors), errors)

    def test_v11_keep_requires_exact_independent_review_binding(self):
        payload = self.make_valid_design_keep()
        payload["independent_design_review"]["review_input_bindings"] = []
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("review_input_bindings" in error for error in errors), errors)

    def test_v11_genericity_na_requires_reason(self):
        payload = copy.deepcopy(self.dd)
        payload["genericity_attack"] = {
            "status": "NOT_APPLICABLE_WITH_REASON",
            "findings": [],
            "reason": None,
        }
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("genericity_attack" in error and "reason" in error for error in errors), errors)

    def test_v11_keep_rejects_na_for_native_or_decision_body_roles(self):
        for role in ("NATIVE_ARTIFACT_READBACK", "DECISION_MATURITY_CLAIM_CEILING"):
            payload = self.make_valid_design_keep()
            entry = next(
                item for item in payload["body_structure"]["section_coverage"]
                if item["semantic_role"] == role
            )
            entry["status"] = "NOT_APPLICABLE_WITH_REASON"
            entry["visible_heading_or_locator"] = None
            entry["reason"] = "synthetic N/A"
            errors = self.validator.validate_payload(payload)
            self.assertTrue(any(role in error for error in errors), (role, errors))

    def test_architecture_pass_rejects_missing_and_placeholder_readback(self):
        payload = copy.deepcopy(self.arch)
        payload["result"] = "PASS"
        payload["stale"] = False
        payload["stage_body_records"][0]["stage_verdict"] = "PASS_AT_CLAIM_CEILING"
        payload["independent_plan_review"] = {
            "status": "PASS",
            "reviewer_independent_from_producer": True,
            "reason": "bounded test reviewer"
        }
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("cannot retain MISSING" in error for error in errors), errors)

    def test_architecture_generic_stage_title_is_rejected(self):
        payload = copy.deepcopy(self.arch)
        payload["stage_body_records"][0]["title"] = "Review"
        errors = self.validator.validate_payload(payload)
        self.assertTrue(any("title is generic" in error for error in errors), errors)


if __name__ == "__main__":
    unittest.main()
