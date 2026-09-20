from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
COMPILER_PATH = ROOT / "runtime" / "compile_project_receipts.py"
SPEC = importlib.util.spec_from_file_location("receipt_compiler", COMPILER_PATH)
assert SPEC and SPEC.loader
compiler = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(compiler)


def dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def stage(*, closed: bool, pass_review: bool, evidence_ref: str) -> dict:
    return {
        "stage_instance_id": "DSI-TEST-SE-SPW0-001",
        "stage_definition_ref": "structural-engineering-design-process.v1.json :: SE-SPW0",
        "stage_id": "SE-SPW0",
        "cycle": 1,
        "baseline_ref": "BASELINE-1",
        "execution_state": "CLOSED" if closed else "BLOCKED",
        "review_verdict": "PASS" if pass_review else "HOLD",
        "claim_ceiling": "BOUNDED_TEST",
        "inputs": ["INPUT-1"],
        "outputs": ["structural strategic constraints note"] if closed else [],
        "consequential_knowledge_mount_required": True,
        "knowledge_mount_refs": ["KM-1"],
        "granularity_binding_state": "LEGACY_STAGE_ONLY",
        "interface_refs": [],
        "evidence_refs": [evidence_ref],
        "review_refs": [evidence_ref] if pass_review else [],
        "open_items": [] if closed else ["professional structural basis remains open"],
        "stale_scope": [],
        "reopen_events": [],
        "exit_condition_state": "SATISFIED" if closed else "BLOCKED",
        "actual_readback_refs": [evidence_ref],
        "last_updated": "2026-09-20T00:00:00Z"
    }


def instance(stage_payload: dict, *, verdict: str = "HOLD") -> dict:
    return {
        "schema_version": "1.0",
        "kind": "DOMAIN_PROCESS_INSTANCE",
        "instance_id": "DPI-TEST-STRUCT-001",
        "project_id": "PRJ-TEST-001",
        "workstream_id": None,
        "decision_object_refs": list(stage_payload.get("decision_object_refs") or []),
        "process_definition_ref": "00-governance/schemas/structural-engineering-design-process.v1.json",
        "process_id": "STRUCTURAL_ENGINEERING_DESIGN_PROCESS",
        "process_version": "1.0",
        "domain": "Structural Engineering",
        "owner": "Structural Engineering professional process owner",
        "current_baseline": "BASELINE-1",
        "execution_state": "IN_PROGRESS",
        "professional_verdict": verdict,
        "claim_ceiling": "BOUNDED_TEST",
        "stage_instances": [stage_payload],
        "active_interface_refs": [],
        "open_items": [] if verdict == "PASS" else ["professional closure remains open"],
        "professional_receipt_refs": [],
        "integration_receipt_refs": [],
        "stale_scope": [],
        "reopen_events": [],
        "last_updated": "2026-09-20T00:00:00Z"
    }


def request(process_path: Path, output: Path, readback: Path, *, requested_result: str, reviewer_ref: str | None = None) -> dict:
    return {
        "object_type": "PROFESSIONAL_RECEIPT_COMPILATION_REQUEST",
        "schema_version": "1.0",
        "compilation_id": "COMP-TEST-001",
        "project_id": "PRJ-TEST-001",
        "workstream_id": None,
        "target_receipt_type": "STRUCTURAL_ENGINEERING_DESIGN_PROCESS_RECEIPT",
        "process_instance_ref": str(process_path),
        "process_instance_sha256": digest(process_path),
        "source_revision": "TEST-REV-1",
        "claim_ceiling": "BOUNDED_TEST",
        "requested_result": requested_result,
        "source_roots": [{"root_id": "TEST", "path": str(process_path.parent), "required_for_pass": True}],
        "interface_records": [],
        "review_binding": {"required": True, "reviewer_ref": reviewer_ref},
        "basis_of_structural_design_ref": None,
        "output_ref": str(output),
        "readback_ref": str(readback),
        "does_not_prove": ["professional approval"]
    }


class ProjectReceiptCompilerTests(unittest.TestCase):
    def test_blocked_stage_compiles_hold(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.json"
            evidence.write_text("{}\n", encoding="utf-8")
            process = root / "process.json"
            dump(process, instance(stage(closed=False, pass_review=False, evidence_ref=str(evidence))))
            output = root / "receipt.json"
            rb = root / "readback.json"
            req = root / "request.json"
            dump(req, request(process, output, rb, requested_result="HOLD"))
            _, _, result = compiler.compile_professional(req)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("HOLD", receipt["result"])
            self.assertEqual("HOLD", receipt["stage_records"][0]["status"])
            self.assertEqual("PASS", result["source_integrity_state"])
            self.assertEqual("NOT_REQUESTED", result["pass_readiness"])

    def test_requested_pass_never_emits_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "review.json"
            evidence.write_text("{}\n", encoding="utf-8")
            process = root / "process.json"
            dump(process, instance(stage(closed=True, pass_review=True, evidence_ref=str(evidence)), verdict="PASS"))
            output = root / "receipt.json"
            rb = root / "readback.json"
            req = root / "request.json"
            dump(req, request(process, output, rb, requested_result="PASS", reviewer_ref="INDEPENDENT-REVIEWER-1"))
            _, _, result = compiler.compile_professional(req)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("HOLD", receipt["result"])
            self.assertIn(result["pass_readiness"], {"READY_FOR_AUTHORIZED_REVIEW", "HOLD"})
            self.assertIn("COMPILER_CANNOT_GRANT_PROFESSIONAL_PASS; AUTHORIZED REVIEW/ADOPTION REQUIRED", receipt["blocking_open_items"])

    def test_fully_read_back_pass_candidate_stops_at_authorized_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            artifact = root / "structural-note.json"
            readback_src = root / "readback.json"
            review = root / "review.json"
            for path in (artifact, readback_src, review):
                path.write_text("{}\n", encoding="utf-8")
            row = stage(closed=True, pass_review=True, evidence_ref=str(review))
            row.update({
                "granularity_binding_state": "DECISION_OBJECT_BOUND",
                "decision_object_refs": ["STRUCT-DECISION-1"],
                "claim_refs": ["STRUCT-CLAIM-1"],
                "actual_readback_refs": [str(readback_src)],
                "output_execution_bindings": [{
                    "binding_id": "OEB-STRUCT-1",
                    "decision_object_ref": "STRUCT-DECISION-1",
                    "claim_refs": ["STRUCT-CLAIM-1"],
                    "knowledge_mount_refs": ["KM-1"],
                    "output_requirement_ref": "SE-SPW0:structural strategic constraints note",
                    "required_native_output": "structural strategic constraints note",
                    "required_capability_roles": ["structural professional reasoning"],
                    "tool_adapter_required": False,
                    "owner_set_ref": "OWNER-SET-STRUCT-1",
                    "adapter_route_ref": None,
                    "artifact_refs": [str(artifact)],
                    "readback_refs": [str(readback_src)],
                    "resolution_state": "READBACK_COMPLETE",
                    "stale_if": ["structural basis changes"],
                    "does_not_prove": ["statutory approval"]
                }]
            })
            process = root / "process.json"
            dump(process, instance(row, verdict="PASS"))
            output = root / "receipt.json"
            rb = root / "compiler-readback.json"
            req = root / "request.json"
            dump(req, request(process, output, rb, requested_result="PASS", reviewer_ref="INDEPENDENT-REVIEWER-1"))
            _, _, result = compiler.compile_professional(req)
            receipt = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual("HOLD", receipt["result"])
            self.assertEqual("PASS", receipt["stage_records"][0]["status"])
            self.assertEqual("READY_FOR_AUTHORIZED_REVIEW", result["pass_readiness"])

    def test_sha_mismatch_holds_source_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            evidence = root / "evidence.json"
            evidence.write_text("{}\n", encoding="utf-8")
            process = root / "process.json"
            dump(process, instance(stage(closed=False, pass_review=False, evidence_ref=str(evidence))))
            output = root / "receipt.json"
            rb = root / "readback.json"
            req_payload = request(process, output, rb, requested_result="HOLD")
            req_payload["process_instance_sha256"] = "0" * 64
            req = root / "request.json"
            dump(req, req_payload)
            _, _, result = compiler.compile_professional(req)
            self.assertEqual("HOLD", result["source_integrity_state"])
            self.assertIn("PROCESS_INSTANCE_SHA256_MISMATCH", result["hold_reasons"])

    def test_existing_closure_readback_hashes_and_validates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            closure = root / "closure.json"
            payload = json.loads((ROOT / "schemas" / "project-risk-hazard-register.v1.template.json").read_text(encoding="utf-8"))
            dump(closure, payload)
            readback = root / "readback.json"
            request_path = root / "request.json"
            dump(request_path, {
                "object_type": "PROJECT_CLOSURE_READBACK_REQUEST",
                "schema_version": "1.0",
                "compilation_id": "RB-TEST-001",
                "project_id": "PROJECT_ID",
                "object_refs": [{"ref": str(closure), "expected_sha256": digest(closure)}],
                "source_roots": [{"root_id": "TEST", "path": str(root), "required_for_pass": True}],
                "readback_ref": str(readback),
                "does_not_prove": ["professional approval"]
            })
            _, result = compiler.readback_closure_pack(request_path)
            self.assertEqual("PASS", result["source_integrity_state"])
            self.assertEqual("PASS", result["schema_validation_state"])


if __name__ == "__main__":
    unittest.main()
