import tempfile
import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from control_plane import locate_asset, revision_breaker, run_check, select_gate_profile, validate_card


def base_card():
    return {
        "schema_version":"0.2",
        "object":{"name":"Test Object","project_id":"PRJ-XJ01-CMF","project_level":"P2","case_id":None,"knowledge_position":"L7 Practice","application_mapping":["IP03"],"priority":"Priority-1"},
        "mode":"EXPLORE","decision_question":"Does A outperform B under fixed conditions?","problem_layer":"Parameter",
        "authority_source":{"state":"WORKING_SOURCE","source_id":"S1","location":"x","sha256":None},
        "locked_variables":["geometry"],"open_variables":["material"],"required_qa":["Visual"],"artifact_type":"visual_cmf","claim_types":[],
        "evidence_state":{"digital":"OPEN","physical":"NOT_RUN"},"next_allowed_action":"COMPARE","sync_persistence_trigger":"NONE","review_history":[]
    }


def architecture_card(established=True):
    c = base_card()
    c["decision_question"] = "Can the project architecture become clearer without becoming less?"
    c["problem_layer"] = "Architecture"
    c["preservation_review"] = {
        "established_objects_present": established,
        "global_fixed_chapter_count_applied": False,
        "decisions": []
    }
    if established:
        c["preservation_review"]["decisions"] = [{
            "object_id": "OBJ-EXISTING-01",
            "concept_state": "KEEP",
            "presentation_state": "REDRAW",
            "truth_evidence_state": "OPEN",
            "action": "REDRAW",
            "reason": "Current pixels are weak but the independent design function remains valid"
        }]
    return c


class ControlPlaneTests(unittest.TestCase):
    def test_valid_explore_card(self):
        self.assertFalse([f for f in validate_card(base_card()) if f.level == "ERROR"])
        self.assertEqual(run_check(base_card())["status"], "PASS")
    def test_schema_rejects_additional_property(self):
        c=base_card(); c["unexpected"]="x"; self.assertIn("SCHEMA_VALIDATION", {f.code for f in validate_card(c)})
    def test_schema_rejects_bad_evidence_value(self):
        c=base_card(); c["evidence_state"]["physical"]="MAYBE"; self.assertIn("SCHEMA_VALIDATION", {f.code for f in validate_card(c)})
    def test_schema_rejects_duplicate_qa(self):
        c=base_card(); c["required_qa"]=["Visual","Visual"]; self.assertIn("SCHEMA_VALIDATION", {f.code for f in validate_card(c)})
    def test_namespace_case_project_collision_fails(self):
        c=base_card(); c["object"]["project_id"]="C04-WS-04"; self.assertIn("NAMESPACE_CASE_PROJECT_COLLISION", {f.code for f in validate_card(c)})
    def test_application_project_collision_fails(self):
        c=base_card(); c["object"]["project_id"]="IP03-WORK"; self.assertIn("NAMESPACE_APPLICATION_PROJECT_COLLISION", {f.code for f in validate_card(c)})
    def test_candidate_requires_three_qa_layers(self):
        c=base_card(); c["mode"]="CANDIDATE"; self.assertIn("GATE_PROFILE_CANDIDATE_QA", {f.code for f in validate_card(c)})
    def test_authority_triggers_existing_specialist_gates(self):
        c=base_card(); c["mode"]="AUTHORITY"; c["authority_source"]["state"]="CANONICAL_AUTHORITY"; c["required_qa"]=["Machine","Visual","Project"]
        c["artifact_type"]="release_package"; c["claim_types"]=["rights","reality","engineering","human_test","release"]; c["sync_persistence_trigger"]="FULL_SYNC"
        g=select_gate_profile(c).specialist_gates
        for gate in ["Production Asset Persistence Gate","AR-S09 Release Package Review","Rights Gate","Reality Gate","Engineering Gate","Human Test Gate"]:
            self.assertIn(gate,g)
    def test_repeated_revise_breaker_trips(self):
        c=base_card(); e={"decision_question":c["decision_question"],"problem_layer":c["problem_layer"],"visual_result":"REVISE","project_result":"PASS","timestamp":None}; c["review_history"]=[dict(e),dict(e)]
        self.assertTrue(revision_breaker(c).tripped); self.assertEqual(run_check(c)["status"],"BLOCKED")
    def test_breaker_does_not_trip_after_problem_layer_change(self):
        c=base_card(); c["review_history"]=[{"decision_question":c["decision_question"],"problem_layer":"Parameter","visual_result":"REVISE","project_result":"PASS","timestamp":None},{"decision_question":c["decision_question"],"problem_layer":"Topology","visual_result":"REVISE","project_result":"PASS","timestamp":None}]
        self.assertFalse(revision_breaker(c).tripped)
    def test_asset_locator_searches_registry_and_filesystem(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"XJ01_R02_calibration_master.obj"; p.write_text("o test",encoding="utf-8")
            r=locate_asset("calibration_master",[td],{"assets":[]}); self.assertEqual(r["status"],"FOUND")
        r=locate_asset("R54",[],{"assets":[{"id":"STD-R54","name":"R54 Product Rendering Standard","location":"registry"}]}); self.assertEqual(r["status"],"FOUND")

    def test_architecture_requires_preservation_review(self):
        c=base_card(); c["problem_layer"]="Architecture"
        self.assertIn("NO_LOSS_PRESERVATION_REVIEW_REQUIRED", {f.code for f in validate_card(c)})
        self.assertEqual(run_check(c)["status"], "BLOCKED")

    def test_architecture_with_no_established_objects_can_start_clean(self):
        c=architecture_card(established=False)
        self.assertFalse([f for f in validate_card(c) if f.level == "ERROR"])
        self.assertEqual(run_check(c)["status"], "PASS")

    def test_established_objects_must_be_accounted_for(self):
        c=architecture_card(established=True); c["preservation_review"]["decisions"]=[]
        self.assertIn("NO_LOSS_ESTABLISHED_OBJECTS_UNACCOUNTED", {f.code for f in validate_card(c)})

    def test_fixed_global_chapter_count_is_rejected(self):
        c=architecture_card(); c["preservation_review"]["global_fixed_chapter_count_applied"]=True
        self.assertIn("SCHEMA_VALIDATION", {f.code for f in validate_card(c)})

    def test_compression_alone_cannot_justify_cut(self):
        c=architecture_card(); c["preservation_review"]["decisions"]=[{
            "object_id":"OBJ-EXISTING-01","concept_state":"DROP","presentation_state":"PROCESS","truth_evidence_state":"OPEN","action":"CUT","reason":"compression"
        }]
        self.assertIn("NO_LOSS_INVALID_REMOVAL_REASON", {f.code for f in validate_card(c)})

    def test_substantive_cut_reason_can_pass_machine_contract(self):
        c=architecture_card(); c["preservation_review"]["decisions"]=[{
            "object_id":"OBJ-EXISTING-01","concept_state":"DROP","presentation_state":"PROCESS","truth_evidence_state":"SUPERSEDED","action":"CUT","reason":"Superseded by a stronger authority object with the same function and preserved provenance"
        }]
        self.assertFalse([f for f in validate_card(c) if f.level == "ERROR"])

    def test_cut_cannot_delete_a_kept_concept(self):
        c=architecture_card(); c["preservation_review"]["decisions"]=[{
            "object_id":"OBJ-EXISTING-01","concept_state":"KEEP","presentation_state":"PROCESS","truth_evidence_state":"OPEN","action":"CUT","reason":"The current representation is visually weak"
        }]
        self.assertIn("NO_LOSS_CUT_STATE_MISMATCH", {f.code for f in validate_card(c)})

    def test_demote_action_and_presentation_state_must_agree(self):
        c=architecture_card(); c["preservation_review"]["decisions"]=[{
            "object_id":"OBJ-EXISTING-01","concept_state":"KEEP","presentation_state":"MAIN","truth_evidence_state":"OPEN","action":"DEMOTE_TO_SUPPORT","reason":"Independent function remains but it is secondary to the current public first-read"
        }]
        self.assertIn("NO_LOSS_DEMOTE_STATE_MISMATCH", {f.code for f in validate_card(c)})


if __name__=="__main__": unittest.main()
