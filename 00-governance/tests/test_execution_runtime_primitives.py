from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
sys.path.insert(0, str(RUNTIME))

from oleander_execution_runtime import ActionRequest, ActionRuntime, DurableJob, ExecutionLedger  # noqa: E402


class ExecutionRuntimePrimitiveTests(unittest.TestCase):
    def test_action_runtime_exposes_declared_primitive_operations(self) -> None:
        runtime = ActionRuntime()
        for operation in ("validate", "authorize", "defer", "resume", "execute", "observe_delta", "readback"):
            self.assertTrue(callable(getattr(runtime, operation, None)), operation)

    def test_ledger_rejects_project_authority_fields(self) -> None:
        ledger = ExecutionLedger()
        with self.assertRaises(ValueError):
            ledger.append(
                provider_id="native_cos",
                action_id="a1",
                event_type="EXECUTION_OBSERVED",
                outcome="TEST",
                payload={"project_state": {"shadow": True}},
            )

    def test_ledger_jsonl_is_append_only_runtime_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "execution.jsonl"
            ledger = ExecutionLedger(path)
            ledger.append(
                provider_id="native_cos",
                action_id="a2",
                event_type="ACTION_REQUESTED",
                outcome="RECEIVED",
                payload={"project_state_ref": "owner-native:state-1"},
            )
            ledger.flush()
            replay = ExecutionLedger(path).replay()
            self.assertEqual(1, len(replay))
            self.assertEqual("APPEND_ONLY_RUNTIME_EVIDENCE_NOT_PROJECT_STATE", replay[0]["semantic_class"])

    def test_oleander_deny_prevents_provider_execution(self) -> None:
        called = False

        def executor(_: ActionRequest) -> dict:
            nonlocal called
            called = True
            return {"ok": True}

        runtime = ActionRuntime()
        request = ActionRequest.from_dict({
            "action_id": "deny-1",
            "intent": "CONTINUE",
            "side_effect_class": "LOCAL_MUTATION",
            "oleander_guard_decision": "DENY",
            "provider_approval": "APPROVED",
        })
        result = runtime.execute(request, executor)
        self.assertEqual("BLOCKED_BY_OLEANDER", result["status"])
        self.assertFalse(called)

    def test_mutation_without_readback_is_partial(self) -> None:
        runtime = ActionRuntime()
        request = ActionRequest.from_dict({
            "action_id": "mut-1",
            "intent": "DEVELOP",
            "side_effect_class": "LOCAL_MUTATION",
            "oleander_guard_decision": "ALLOW",
        })
        result = runtime.execute(request, lambda _: {"actual_delta": "file changed"})
        self.assertEqual("PARTIAL", result["status"])
        self.assertTrue(result["readback_required"])

    def test_mutation_with_pass_readback_completes_execution_only(self) -> None:
        runtime = ActionRuntime()
        request = ActionRequest.from_dict({
            "action_id": "mut-2",
            "intent": "DEVELOP",
            "side_effect_class": "LOCAL_MUTATION",
            "oleander_guard_decision": "ALLOW",
        })
        result = runtime.execute(
            request,
            lambda _: {"actual_delta": "file changed"},
            readback=lambda _request, _result: {"status": "PASS", "observed": True},
        )
        self.assertEqual("COMPLETED", result["status"])
        self.assertFalse(result["changes_project_state"])
        self.assertFalse(result["changes_promotion_authority"])

    def test_provider_authority_forgery_fails_execution(self) -> None:
        runtime = ActionRuntime()
        request = ActionRequest.from_dict({
            "action_id": "forge-1",
            "intent": "CONTINUE",
            "side_effect_class": "READ_ONLY",
            "oleander_guard_decision": "ALLOW",
        })
        result = runtime.execute(request, lambda _: {"project_current": True})
        self.assertEqual("FAILED", result["status"])

    def test_deferred_provider_approval_resumes_through_same_pipeline(self) -> None:
        runtime = ActionRuntime()
        request = ActionRequest.from_dict({
            "action_id": "defer-1",
            "intent": "CONTINUE",
            "side_effect_class": "READ_ONLY",
            "oleander_guard_decision": "ALLOW",
            "provider_approval": "PENDING",
        })
        self.assertEqual("DEFERRED", runtime.execute(request, lambda _: {"ok": True})["status"])
        resumed = runtime.resume(request, lambda _: {"ok": True}, provider_approval="APPROVED")
        self.assertEqual("COMPLETED", resumed["status"])

    def test_durable_job_state_is_execution_only(self) -> None:
        job = DurableJob(job_id="job-1", action_id="action-1")
        failed = job.start(lambda: (_ for _ in ()).throw(RuntimeError("boom")))
        self.assertEqual("FAILED", failed["status"])
        self.assertEqual("DURABLE_EXECUTION_STATE_NOT_PROJECT_STATE", failed["semantic_class"])
        self.assertEqual("RETRY_PENDING", job.retry()["status"])
        completed = job.start(lambda: {"result": "ok"})
        self.assertEqual("COMPLETED", completed["status"])


if __name__ == "__main__":
    unittest.main()
