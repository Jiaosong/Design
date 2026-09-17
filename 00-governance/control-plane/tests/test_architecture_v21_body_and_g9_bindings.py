import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
GRAPH = ROOT / "00-governance/runtime/OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
INTERFACE = ROOT / "00-governance/runtime/OLEANDER_RUNTIME_LAYER_INTERFACE_CONTRACT_v1.0.json"
DQ = ROOT / "00-governance/design-quality-and-design-development-specification-v1.0.md"
PROFESSIONAL = ROOT / "00-governance/professional-domain-process-contract-v1.0.md"


class ArchitectureV21BodyAndG9BindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.graph = json.loads(GRAPH.read_text(encoding="utf-8"))
        cls.interface = json.loads(INTERFACE.read_text(encoding="utf-8"))
        cls.layers = {row["id"]: row for row in cls.graph["layers"]}
        cls.interfaces = cls.interface["layers"]
        cls.dq_text = DQ.read_text(encoding="utf-8")
        cls.professional_text = PROFESSIONAL.read_text(encoding="utf-8")

    def test_r_d_and_r_e_expose_locator_records_without_moving_them_into_r_b(self):
        self.assertIn("DESIGN_DEVELOPMENT_BODY_RECORD", self.layers["R-D"]["state_objects"])
        self.assertIn("PROFESSIONAL_STAGE_BODY_RECORD", self.layers["R-E"]["state_objects"])
        self.assertNotIn("DESIGN_DEVELOPMENT_BODY_RECORD", self.layers["R-B"]["state_objects"])
        self.assertNotIn("PROFESSIONAL_STAGE_BODY_RECORD", self.layers["R-B"]["state_objects"])

        self.assertIn("WITHOUT_COPYING", self.interfaces["R-D"]["persistence_policy"])
        self.assertIn("WITHOUT_COPYING", self.interfaces["R-E"]["persistence_policy"])

    def test_r_i_consumes_body_locators_and_keeps_review_authority_bounded(self):
        r_i = self.interfaces["R-I"]
        self.assertIn("R-D:DESIGN_DEVELOPMENT_BODY_RECORD", r_i["inputs"])
        self.assertIn("R-E:PROFESSIONAL_STAGE_BODY_RECORD", r_i["inputs"])
        self.assertIn(
            "APPLICABLE_BODY_RECORD_BINDINGS_MATCH_CURRENT_NATIVE_AND_READBACK_REFS",
            r_i["exit_conditions"],
        )
        self.assertIn("BODY_RECORD_BINDING_STALE_OR_INCOMPLETE", r_i["failure_codes"])
        self.assertIn(
            "MAY_NOT_REWRITE_UPSTREAM_BODY_KNOWLEDGE_OR_PROFESSIONAL_AUTHORITY",
            r_i["claim_boundary"],
        )

    def test_r_k_remains_feedback_not_dependency_handoff(self):
        r_k = self.interfaces["R-K"]
        self.assertEqual(r_k["feedback_targets"], ["R-B"])
        self.assertEqual(r_k["handoff_targets"], [])
        self.assertIn("NEVER_AS_CURRENT_KNOWLEDGE_BY_DEFAULT", r_k["persistence_policy"])

    def test_design_quality_g9_boundary_separates_observation_knowledge_and_oe(self):
        for required in (
            "OBSERVED OUTCOME ≠ CAUSAL EXPLANATION",
            "PROJECT REOPEN ≠ KNOWLEDGE PROMOTION",
            "G9 CANDIDATE ≠ KI4 ≠ OE3",
        ):
            self.assertIn(required, self.dq_text)

    def test_professional_g9_boundary_does_not_promote_stage_pass_to_reusable_truth(self):
        for required in (
            "PROFESSIONAL STAGE PASS ≠ REUSABLE KNOWLEDGE",
            "PROJECT REOPEN ≠ KNOWLEDGE PROMOTION",
            "G9 CANDIDATE ≠ KI4 ≠ OE3",
        ):
            self.assertIn(required, self.professional_text)

    def test_design_quality_operational_detail_remains_substantive(self):
        for required in (
            "DECLARED OWNER ≠ OBSERVED OWNER",
            "PARAMETRIC POSSIBILITY ≠ DESIGN-PERMITTED RANGE",
            "DQ5 ≠ CURRENT REUSABLE KNOWLEDGE",
            "CAPABILITY ROUTE FOUND ≠ TOOL CALL SUCCEEDED",
            "MATRIX COMPLETE ≠ OWNER STATE COMPLETE",
            "TRACEABLE EXECUTION ≠ DESIGN KEEP",
        ):
            self.assertIn(required, self.dq_text)

    def test_professional_operational_detail_keeps_owner_boundaries(self):
        for required in (
            "PROFESSIONAL PASS ≠ DD KEEP",
            "CLASH-FREE ≠ INTERFACE ACCEPTED",
            "NATIVE FILE EXISTS ≠ NATIVE AUTHORITY RESOLVED",
            "SKILL INSTALLED ≠ SKILL SUFFICIENT FOR THIS CLAIM",
            "PRODUCER SELF-CHECK ≠ INDEPENDENT REVIEW",
            "CHANGE DETECTED ≠ WHOLE PROCESS RESET",
            "MASTER SUMMARY ≠ PROFESSIONAL SOURCE OF TRUTH",
        ):
            self.assertIn(required, self.professional_text)

    def test_body_receipt_supersession_reuses_existing_boundary_and_preserves_history(self):
        application = self.graph["current_supersession_boundary"]["body_receipt_native_application"]
        self.assertEqual(
            application["semantic_class"],
            "APPLICATION_OF_EXISTING_SUPERSESSION_BOUNDARY_NOT_NEW_STATE_REGISTRY_VERSION_DB_OR_RECEIPT_REWRITE",
        )
        self.assertTrue(application["historical_body_records_receipts_and_reviews_remain_immutable_provenance"])
        self.assertTrue(application["historical_receipt_stale_flag_is_not_rewritten_to_describe_later_supersession"])
        self.assertTrue(application["only_consumers_of_materially_changed_relation_become_stale"])
        self.assertTrue(
            application[
                "authority_binding_may_resolve_via_r_a_snapshot_layer_instance_or_handoff_without_retrofitting_historical_receipt_schema"
            ]
        )
        self.assertTrue(
            application[
                "authority_fingerprint_mismatch_blocks_direct_current_consumption_then_routes_only_affected_scope"
            ]
        )
        self.assertTrue(application["duplicate_body_or_receipt_current_registry_forbidden"])

    def test_supersession_routes_body_through_r_i_and_receipt_through_r_j(self):
        sequence = self.graph["current_supersession_boundary"]["body_receipt_native_application"]["successor_rebind_sequence"]
        self.assertIn("R_I_VERIFY_SUCCESSOR_BINDINGS_AND_RERUN_AFFECTED_REVIEW", sequence)
        self.assertIn("R_J_CONSUME_ONLY_CURRENT_NON_STALE_RECEIPT_FOR_PROMOTION", sequence)

        r_j_inputs = self.interfaces["R-J"]["inputs"]
        self.assertIn("R-D:DESIGN_QUALITY_DEVELOPMENT_RECEIPT", r_j_inputs)
        self.assertIn("R-E:DOMAIN_RECEIPT", r_j_inputs)
        self.assertNotIn("R-D:DESIGN_DEVELOPMENT_BODY_RECORD", r_j_inputs)
        self.assertNotIn("R-E:PROFESSIONAL_STAGE_BODY_RECORD", r_j_inputs)

    def test_owner_docs_forbid_rewriting_historical_receipts(self):
        for required in (
            "NEW NATIVE REVISION ≠ OLD DQ RECEIPT UPDATED",
            "SUPERSEDED DQ RECEIPT ≠ FALSE HISTORICAL EVIDENCE",
            "HISTORICAL RECEIPT IMMUTABLE ≠ CURRENT CLAIM ELIGIBLE",
        ):
            self.assertIn(required, self.dq_text)
        for required in (
            "NEW STAGE CYCLE / NATIVE REVISION ≠ OLD PROFESSIONAL RECEIPT REWRITTEN",
            "SUPERSEDED PROFESSIONAL EVIDENCE ≠ FALSE EVIDENCE",
            "HISTORICAL PROFESSIONAL RECEIPT ≠ CURRENT PROFESSIONAL CLAIM BY DEFAULT",
        ):
            self.assertIn(required, self.professional_text)


if __name__ == "__main__":
    unittest.main()
