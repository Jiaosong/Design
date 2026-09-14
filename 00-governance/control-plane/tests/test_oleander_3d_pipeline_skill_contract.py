from __future__ import annotations

import json
import re
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / "oleander-skills/oleander-3d-pipeline/SKILL.md"
CONTRACT = ROOT / "oleander-skills/oleander-3d-pipeline/contracts/BLENDER_3D_AUTHORITY_DIAGNOSTIC_CONTRACT_v1.json"
EVALS = ROOT / "oleander-skills/oleander-3d-pipeline/evals/evals.json"
RECEIPTS = ROOT / "oleander-skills/oleander-3d-pipeline/contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json"

EXECUTION_FIELDS = ("INPUT", "MUST CHECK", "ALLOWED", "FORBIDDEN", "EVIDENCE", "FAIL")


class Oleander3DPipelineSkillContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.evals = json.loads(EVALS.read_text(encoding="utf-8"))
        cls.receipts = json.loads(RECEIPTS.read_text(encoding="utf-8"))

    def _section_text(self, number: int) -> str:
        match = re.search(
            rf"^## {number}\. .+?(?=^## {number + 1}\. |\Z)" if number < 15
            else r"^## 15\. .+?(?=^## Cross-section invariant|\Z)",
            self.skill,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(match, f"missing Skill section {number}")
        return match.group(0)

    def test_all_15_sections_have_execution_grammar(self):
        self.assertEqual(
            self.contract["section_execution_fields"],
            ["INPUT", "MUST_CHECK", "ALLOWED", "FORBIDDEN", "EVIDENCE", "FAIL"],
        )
        for number in range(1, 16):
            section = self._section_text(number)
            for field in EXECUTION_FIELDS:
                self.assertIn(f"### {field}", section, f"section {number} missing {field}")

    def test_state_and_authority_model_is_explicit(self):
        self.assertEqual(
            self.contract["authority_order"],
            [
                "MASTER_PROTOCOL",
                "PROJECT_STATE",
                "SOURCE_AUTHORITY",
                "CURRENT_TASK",
                "CURRENT_PRODUCTION_ASSET",
            ],
        )
        self.assertEqual(
            set(self.contract["state_model"]),
            {
                "SOURCE_OR_WORKING_SOURCE",
                "DERIVED_EXECUTION",
                "DERIVED_DIAGNOSTIC_NOT_AUTHORITY",
                "VISUALIZATION_OR_RENDER_SCENE",
                "REFERENCE_EVIDENCE",
            },
        )
        self.assertIn("NO_FILE_RECENCY_AS_AUTHORITY", self.contract["hard_prohibitions"])
        self.assertIn("NO_VISUALIZATION_AS_SOURCE_AUTHORITY", self.contract["hard_prohibitions"])
        self.assertFalse(self.contract["blender_surface_system"]["source_owner_transfer_allowed"])

    def test_every_contract_section_has_checks_evidence_and_failure_codes(self):
        sections = self.contract["section_contracts"]
        self.assertEqual(len(sections), 15)
        expected_prefixes = [f"{i:02d}_" for i in range(1, 16)]
        self.assertEqual(
            [key[:3] for key in sections],
            expected_prefixes,
        )
        for key, section in sections.items():
            self.assertTrue(section["required_checks"], key)
            self.assertTrue(section["required_evidence"], key)
            self.assertTrue(section["failure_codes"], key)
            self.assertEqual(len(section["required_checks"]), len(set(section["required_checks"])), key)
            self.assertEqual(len(section["failure_codes"]), len(set(section["failure_codes"])), key)

    def test_blender_source_diagnostic_is_fail_closed_and_proxy_only(self):
        sequence = self.contract["source_aware_diagnostic_sequence"]
        self.assertLess(
            sequence.index("SNAPSHOT_SOURCE_IDENTITY_TRANSFORM_PROPERTIES_AND_EDITABLE_GEOMETRY"),
            sequence.index("RUN_CONTROLLED_DIAGNOSTIC_VIEWS"),
        )
        self.assertLess(
            sequence.index("RUN_CONTROLLED_DIAGNOSTIC_VIEWS"),
            sequence.index("SNAPSHOT_SOURCE_AFTER_DIAGNOSTIC"),
        )
        self.assertIn("ASSIGN_DIAGNOSTIC_MATERIAL_TO_PROXY_ONLY", sequence)
        self.assertIn("FAIL_CLOSED_ON_UNAUTHORIZED_SOURCE_CHANGE", sequence)
        self.assertIn(
            "NO_SOURCE_MATERIAL_SLOT_MUTATION_FOR_DIAGNOSTIC_ONLY_WORK",
            self.contract["hard_prohibitions"],
        )
        self.assertEqual(
            self.contract["blender_surface_system"]["diagnostic_proxy_role"],
            "DERIVED_DIAGNOSTIC_NOT_AUTHORITY",
        )
        self.assertIn("FAIL_SOURCE_MUTATED_DURING_DIAGNOSTIC", self.skill)
        self.assertIn("FAIL_DIAGNOSTIC_TARGET_IS_AUTHORITATIVE", self.skill)

    def test_sparse_edit_delta_is_auditable_and_reversible(self):
        required = set(self.contract["source_edit_delta_required_fields"])
        self.assertEqual(
            required,
            {
                "source_family",
                "control_name",
                "unit",
                "previous_value",
                "new_value",
                "allowed_range",
                "locked_dependencies",
                "predicted_geometric_effect",
                "sensitive_regions",
                "forbidden_side_effects",
                "rollback_value",
            },
        )
        priority = self.contract["sparse_edit_priority"]
        self.assertEqual(priority[0], "LOCKED_GLOBAL_PROPORTIONS_AND_INTERFACES")
        self.assertIn(
            "ONE_NEW_EXPLICIT_SPARSE_DOF_IF_EXISTING_CONTROLS_ARE_PROVEN_INSUFFICIENT",
            priority,
        )
        self.assertEqual(
            priority[-1],
            "SOURCE_FAMILY_OR_TOPOLOGY_EXPANSION_ONLY_IF_RELATION_MODEL_IS_PROVEN_INADEQUATE",
        )

    def test_surface_diagnostic_views_have_question_inspection_failures_and_pairs(self):
        specs = self.contract["diagnostic_view_specs"]
        self.assertEqual(set(specs), {"BROAD", "STRIP", "GRAZING", "ZEBRA"})
        for view, spec in specs.items():
            self.assertTrue(spec["question"], view)
            self.assertTrue(spec["inspect"], view)
            self.assertTrue(spec["failure_signatures"], view)
            self.assertEqual(len(spec["required_pair"]), 2, view)
            self.assertTrue(all(item.endswith(("REFERENCE", "CANDIDATE")) for item in spec["required_pair"]), view)
            self.assertIn(f"### {view}" if view != "ZEBRA" else "### ZEBRA / REFLECTION-LINE", self.skill)
        self.assertEqual(specs["ZEBRA"]["does_not_prove"], ["G2", "G3", "CLASS_A"])
        self.assertIn("NO_ZEBRA_ONLY_CLASS_A_G2_G3_CLAIM", self.contract["hard_prohibitions"])

    def test_controlled_comparison_lock_set_is_complete(self):
        locks = set(self.contract["controlled_comparison_locks"])
        required = {
            "CAMERA_TRANSFORM_AND_PROJECTION",
            "FOCAL_LENGTH_OR_ORTHOGRAPHIC_SCALE",
            "CROP_AND_ASPECT",
            "COLOR_MANAGEMENT_AND_EXPOSURE",
            "WORLD_AND_BACKGROUND",
            "LIGHT_TRANSFORMS_SIZE_ENERGY_SHAPE",
            "DIAGNOSTIC_MATERIAL",
            "RENDER_SAMPLES_AND_DENOISE_POLICY_WHEN_RELEVANT",
        }
        self.assertEqual(locks, required)
        self.assertIn("FAIL_RIG_LOCK_DRIFT", self.skill)

    def test_spatial_and_cmf_rules_prevent_false_proof(self):
        hard = set(self.contract["hard_prohibitions"])
        self.assertIn("NO_FIELD_ZERO_AS_STOP_CONDITION", hard)
        self.assertIn("NO_TEXTURE_NOISE_TO_MASK_GEOMETRY_FAILURE", hard)
        self.assertIn("FIELD_OPEN", self.skill)
        self.assertIn("INSUFFICIENT_PHYSICAL_CMF_EVIDENCE", self.skill)
        self.assertIn("FAIL_INVENTED_SITE_PRECISION", self.skill)

    def test_technical_output_and_exchange_are_editable_and_non_authoritative(self):
        hard = set(self.contract["hard_prohibitions"])
        self.assertIn("NO_RASTER_TEXT_AS_SUBSTITUTE_FOR_REQUIRED_VECTOR_TECHNICAL_TEXT", hard)
        self.assertIn("NO_EXCHANGE_EXPORT_AS_SILENT_SOURCE_PROMOTION", hard)
        self.assertIn("EDITABLE_VECTOR_TECHNICAL_OUTPUT", self.skill)
        self.assertIn("ROUNDTRIP_REPORT", self.skill)
        self.assertIn("FAIL_EXPORT_PROMOTED_TO_SOURCE", self.skill)

    def test_artifact_manifest_fields_prove_recoverability_not_design_quality(self):
        self.assertEqual(
            self.contract["artifact_manifest_required_fields"],
            [
                "path",
                "role",
                "state_class",
                "bytes",
                "sha256",
                "application_version",
                "dependencies",
                "recoverability",
                "validation_status",
            ],
        )
        self.assertIn("FAIL_RETAINED_BINARY_UNRECOVERABLE", self.skill)
        self.assertIn("Artifact existence ≠ Design quality", self.skill)

    def test_quality_gates_are_separated(self):
        self.assertEqual(self.contract["review_gates"]["machine_execution"], ["PASS", "FAIL"])
        self.assertEqual(
            self.contract["review_gates"]["evidence"],
            ["PASS", "INSUFFICIENT", "CONTRADICTED"],
        )
        self.assertEqual(
            self.contract["review_gates"]["design_quality"],
            ["KEEP", "REVISE", "REJECT", "HOLD"],
        )
        self.assertTrue(self.contract["independent_review_required_for_main_keep"])
        self.assertIn("FAIL_GATE_COLLAPSE", self.skill)
        self.assertIn("Process PASS ≠ MAIN KEEP", self.skill)

    def test_failure_routing_requires_isolation_and_rejected_targets(self):
        checks = self.contract["section_contracts"]["14_failure_routing"]["required_checks"]
        self.assertIn("ISOLATION_TEST", checks)
        self.assertIn("REJECTED_EDIT_TARGETS", checks)
        self.assertIn("HOLD_ROOT_CAUSE_UNRESOLVED", self.skill)

    def test_completion_refuses_false_native_or_main_claims(self):
        codes = self.contract["section_contracts"]["15_completion"]["failure_codes"]
        self.assertIn("PARTIAL_REQUIRED_NATIVE_VALIDATION_MISSING", codes)
        self.assertIn("FAIL_FALSE_COMPLETION_CLAIM", codes)
        self.assertIn("HOLD_REQUIRED_REVIEW_MISSING", codes)
        self.assertIn("fabricated native-app PASS", self.skill)

    def test_receipt_schemas_cover_all_sections(self):
        self.assertEqual(
            self.contract["receipt_schema_path"],
            "oleander-skills/oleander-3d-pipeline/contracts/BLENDER_3D_RECEIPT_SCHEMAS_v1.json",
        )
        sections = self.receipts["sections"]
        self.assertEqual(len(sections), 15)
        self.assertEqual(
            list(sections),
            [
                "01_authority",
                "02_state_classification",
                "03_blender_source_authority",
                "04_sparse_edit",
                "05_surface_diagnostics",
                "06_geometry_topology",
                "07_spatial_models",
                "08_materials_cmf",
                "09_camera_render",
                "10_technical_outputs",
                "11_exchange_roundtrip",
                "12_production_artifacts",
                "13_review_gates",
                "14_failure_routing",
                "15_completion",
            ],
        )
        for key, spec in sections.items():
            self.assertIn("receipt", spec, key)
            self.assertTrue(
                spec.get("required_fields") or spec.get("row_required_fields"),
                f"{key} missing required field definition",
            )

    def test_receipt_schemas_preserve_critical_boundaries(self):
        sections = self.receipts["sections"]
        self.assertIn(
            "DERIVED_DIAGNOSTIC_NOT_AUTHORITY",
            sections["02_state_classification"]["state_enum"],
        )
        self.assertEqual(
            sections["05_surface_diagnostics"]["view_enum"],
            ["BROAD", "STRIP", "GRAZING", "ZEBRA"],
        )
        self.assertIn(
            "FIELD_MEASURED",
            sections["07_spatial_models"]["evidence_class_enum"],
        )
        self.assertIn(
            "SHADER_APPEARANCE",
            sections["08_materials_cmf"]["claim_level_enum"],
        )
        self.assertEqual(
            sections["13_review_gates"]["design_enum"],
            ["KEEP", "REVISE", "REJECT", "HOLD"],
        )
        self.assertEqual(
            sections["15_completion"]["final_status_enum"],
            ["COMPLETE_TO_REQUESTED_SCOPE", "PARTIAL", "HOLD", "FAIL"],
        )
        self.assertIn("does not self-authorize design quality", self.receipts["boundary"])

    def test_evals_cover_every_section_and_critical_sections_multiple_times(self):
        items = self.evals["evals"]
        self.assertGreaterEqual(len(items), 15)
        covered = Counter()
        ids = set()
        for item in items:
            self.assertNotIn(item["id"], ids)
            ids.add(item["id"])
            self.assertTrue(item["prompt"].strip())
            self.assertTrue(item["expected_behavior"].strip())
            self.assertTrue(item["sections"])
            self.assertTrue(item["must_include"])
            self.assertTrue(item["must_not"])
            for section in item["sections"]:
                self.assertIn(section, range(1, 16))
                covered[section] += 1
        self.assertEqual(set(covered), set(range(1, 16)))
        for critical in (3, 4, 5, 9, 13, 14, 15):
            self.assertGreaterEqual(covered[critical], 2, f"critical section {critical} under-covered")

    def test_evals_include_recent_oleander_failure_modes(self):
        corpus = "\n".join(
            item["prompt"] + "\n" + item["expected_behavior"]
            for item in self.evals["evals"]
        )
        for phrase in (
            "Broad、Strip、Grazing、Zebra",
            "Class-A",
            "MAIN KEEP",
            "FIELD=0",
            "高模",
            "beauty render",
            "Apply",
            "地形 mesh",
        ):
            self.assertIn(phrase, corpus)


if __name__ == "__main__":
    unittest.main()
