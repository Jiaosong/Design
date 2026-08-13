import unittest
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from orchestrator import evaluate_provider_chain, evaluate_promotion, scan_contradictions, snapshot_payload_hash

H = "a" * 64


def authority_hit(provider_ref="ref", object_id="OBJ-1", source_id="SRC-1", state="CANDIDATE_AUTHORITY", sha=H):
    return {"object_id": object_id, "source_id": source_id, "authority_state": state, "sha256": sha, "provider_ref": provider_ref}


def bound_provider_snapshot(github_status="FOUND", github_hits=None):
    github_hits = [authority_hit("gh:file")] if github_hits is None and github_status == "FOUND" else (github_hits or [])
    return {
        "schema_version": "0.3", "kind": "PROVIDER_CHAIN", "lookup_mode": "BOUND_AUTHORITY", "object_id": "OBJ-1", "query": "SRC-1",
        "authority_binding": {"source_id": "SRC-1", "authority_state": "CANDIDATE_AUTHORITY", "sha256": H},
        "providers": [
            {"provider": "current_authority", "attempted": True, "status": "FOUND", "hits": [authority_hit("registry")], "observed_at": "2026-08-13T02:00:00Z"},
            {"provider": "github", "attempted": True, "status": github_status, "hits": github_hits, "observed_at": "2026-08-13T02:00:01Z"},
            {"provider": "drive", "attempted": True, "status": "NOT_FOUND", "hits": [], "observed_at": "2026-08-13T02:00:02Z"},
            {"provider": "file_library", "attempted": True, "status": "NOT_FOUND", "hits": [], "observed_at": "2026-08-13T02:00:03Z"},
            {"provider": "runtime", "attempted": True, "status": "NOT_FOUND", "hits": [], "observed_at": "2026-08-13T02:00:04Z"}
        ]
    }


def authority_card(evidence=None):
    return {
        "schema_version": "0.2",
        "object": {"name": "Candidate", "project_id": "SYS-MODELING-WORKER", "project_level": "P2", "case_id": None, "knowledge_position": "L7 Practice", "application_mapping": ["IP03"], "priority": "Priority-1"},
        "mode": "AUTHORITY", "decision_question": "Promote exact candidate?", "problem_layer": "Evidence",
        "authority_source": {"state": "CANDIDATE_AUTHORITY", "source_id": "SRC-1", "location": "registry", "sha256": H},
        "locked_variables": ["geometry"], "open_variables": [], "required_qa": ["Machine", "Visual", "Project"], "artifact_type": "release_package", "claim_types": ["rights", "release"],
        "evidence_state": evidence or {"digital": "PASS", "rights": "PASS"}, "next_allowed_action": "PROMOTION_REVIEW", "sync_persistence_trigger": "FULL_SYNC", "review_history": []
    }


def gate_bundle(card=None, wrong_object=False, transition=None):
    card = card or authority_card(); source = card["authority_source"]; obj = source["source_id"]
    transition = transition or {"kind": "CANONICAL_PROMOTION", "from_authority_state": "CANDIDATE_AUTHORITY", "target_authority_state": "CANONICAL_AUTHORITY", "target_design_state": "PROMOTED"}
    gates = ["Machine QA", "Visual QA", "Project QA", "Artifact Review", "Post-Generation Review", "Rights Gate", "Production Asset Persistence Gate", "AR-S09 Release Package Review"]
    receipts = []
    for i, gate in enumerate(gates):
        receipts.append({"gate": gate, "result": "PASS", "object_id": "OTHER" if wrong_object and i == 0 else obj, "source_id": obj, "authority_sha256": source["sha256"], "gate_version": "v1", "receipt_id": f"R-{i}", "executed_at": "2026-08-13T02:00:00Z", "evidence_ref": f"evidence:{i}"})
    return {"schema_version": "0.3", "kind": "GATE_RECEIPTS", "object_id": obj, "authority_binding": {"source_id": obj, "authority_state": source["state"], "sha256": source["sha256"]}, "transition": transition, "receipts": receipts}


def snapshot(system, semantic=None, observed="2026-08-13T02:00:00Z"):
    snap = {"status": "FOUND", "object_id": "AUTO-R29A", "source_ref": f"{system}:ref", "observed_at": observed, "revision": f"{system}-rev-1", "payload_sha256": "0" * 64, "fields": {"version": "v0.11", "authority_state": "CANONICAL_AUTHORITY", "design_state": "PROMOTED"}, "semantic": semantic or {"candidate_superseded": True, "pap_pass": True, "canonical_receipt_present": True}}
    snap["payload_sha256"] = snapshot_payload_hash(snap)
    return snap


class OrchestrationTests(unittest.TestCase):
    def test_schema_version_enforced(self):
        data = bound_provider_snapshot(); data["schema_version"] = "0.2"
        self.assertEqual(evaluate_provider_chain(data)["code"], "CB-03_PROVIDER_SCHEMA_INVALID")

    def test_bound_provider_exact_hit_allowed(self):
        result = evaluate_provider_chain(bound_provider_snapshot())
        self.assertEqual(result["status"], "FOUND"); self.assertEqual(result["actionability"], "ALLOWED")

    def test_bound_provider_nonmatching_found_blocks(self):
        bad = authority_hit("gh:wrong", source_id="OTHER")
        self.assertEqual(evaluate_provider_chain(bound_provider_snapshot(github_hits=[bad]))["code"], "CB-03_FOUND_NOT_AUTHORITY_BOUND")

    def test_discovery_hits_do_not_become_authority(self):
        data = bound_provider_snapshot(); data["lookup_mode"] = "DISCOVERY"; data["authority_binding"] = None
        result = evaluate_provider_chain(data)
        self.assertEqual(result["status"], "DISCOVERED"); self.assertNotEqual(result["actionability"], "ALLOWED")

    def test_discovery_e0_is_not_actionable_success(self):
        data = bound_provider_snapshot(github_status="NOT_FOUND", github_hits=[]); data["lookup_mode"] = "DISCOVERY"; data["authority_binding"] = None
        data["providers"][0] = {"provider": "current_authority", "attempted": True, "status": "NOT_FOUND", "hits": [], "observed_at": "2026-08-13T02:00:00Z"}
        result = evaluate_provider_chain(data)
        self.assertTrue(result["e0_eligible"]); self.assertEqual(result["actionability"], "BLOCKED")

    def test_promotion_rejects_wrong_object_gate_receipt(self):
        result = evaluate_promotion(authority_card(), gate_bundle(wrong_object=True))
        self.assertEqual(result["status"], "BLOCKED"); self.assertEqual(result["code"], "PROMOTION_GATES_OPEN")

    def test_promotion_rejects_open_evidence_even_if_claim_omitted(self):
        card = authority_card({"digital": "PASS", "rights": "PASS", "engineering": "OPEN"})
        self.assertEqual(evaluate_promotion(card, gate_bundle(card))["code"], "PROMOTION_EVIDENCE_OPEN")

    def test_promotion_rejects_illegal_transition(self):
        transition = {"kind": "FREEZE", "from_authority_state": "CANDIDATE_AUTHORITY", "target_authority_state": "FROZEN_AUTHORITY", "target_design_state": "FROZEN"}
        self.assertEqual(evaluate_promotion(authority_card(), gate_bundle(transition=transition))["code"], "PROMOTION_TRANSITION_INVALID")

    def test_promotion_ready_only_with_bound_receipts(self):
        result = evaluate_promotion(authority_card(), gate_bundle())
        self.assertEqual(result["status"], "READY_FOR_HUMAN_DECISION"); self.assertEqual(result["transition"]["target_authority_state"], "CANONICAL_AUTHORITY")

    def test_contradiction_detects_stale_snapshot(self):
        systems = {x: snapshot(x, observed="2026-08-12T00:00:00Z") for x in ["notion", "github", "drive"]}
        manifest = {"schema_version": "0.3", "kind": "CONTRADICTION_MANIFEST", "object_id": "AUTO-R29A", "scan_as_of": "2026-08-13T02:05:00Z", "max_age_seconds": 600, "expected": {"version": "v0.11", "authority_state": "CANONICAL_AUTHORITY", "design_state": "PROMOTED"}, "semantic_expected": {"candidate_superseded": True, "pap_pass": True, "canonical_receipt_present": True}, "systems": systems}
        self.assertEqual(scan_contradictions(manifest)["status"], "BLOCKED")

    def test_contradiction_detects_payload_hash_mismatch(self):
        systems = {x: snapshot(x) for x in ["notion", "github", "drive"]}; systems["drive"]["fields"]["version"] = "v0.10"
        manifest = {"schema_version": "0.3", "kind": "CONTRADICTION_MANIFEST", "object_id": "AUTO-R29A", "scan_as_of": "2026-08-13T02:05:00Z", "max_age_seconds": 600, "expected": {"version": "v0.11", "authority_state": "CANONICAL_AUTHORITY", "design_state": "PROMOTED"}, "semantic_expected": {"candidate_superseded": True, "pap_pass": True, "canonical_receipt_present": True}, "systems": systems}
        self.assertTrue(any(f["code"] == "SNAPSHOT_PAYLOAD_HASH_MISMATCH" for f in scan_contradictions(manifest)["findings"]))

    def test_contradiction_detects_semantic_mismatch(self):
        systems = {x: snapshot(x) for x in ["notion", "github", "drive"]}; systems["notion"]["semantic"]["candidate_superseded"] = False; systems["notion"]["payload_sha256"] = snapshot_payload_hash(systems["notion"])
        manifest = {"schema_version": "0.3", "kind": "CONTRADICTION_MANIFEST", "object_id": "AUTO-R29A", "scan_as_of": "2026-08-13T02:05:00Z", "max_age_seconds": 600, "expected": {"version": "v0.11", "authority_state": "CANONICAL_AUTHORITY", "design_state": "PROMOTED"}, "semantic_expected": {"candidate_superseded": True, "pap_pass": True, "canonical_receipt_present": True}, "systems": systems}
        self.assertTrue(any(f["code"] == "SEMANTIC_CONTRADICTION" for f in scan_contradictions(manifest)["findings"]))

    def test_contradiction_passes_when_bound_fresh_and_semantic(self):
        systems = {x: snapshot(x) for x in ["notion", "github", "drive"]}
        manifest = {"schema_version": "0.3", "kind": "CONTRADICTION_MANIFEST", "object_id": "AUTO-R29A", "scan_as_of": "2026-08-13T02:05:00Z", "max_age_seconds": 600, "expected": {"version": "v0.11", "authority_state": "CANONICAL_AUTHORITY", "design_state": "PROMOTED"}, "semantic_expected": {"candidate_superseded": True, "pap_pass": True, "canonical_receipt_present": True}, "systems": systems}
        self.assertEqual(scan_contradictions(manifest)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
