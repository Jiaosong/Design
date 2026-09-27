#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable


RUNTIME_EVIDENCE_ONLY = "APPEND_ONLY_RUNTIME_EVIDENCE_NOT_PROJECT_STATE"
EXECUTION_AUTHORITY_CEILING = "EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY"

FORBIDDEN_AUTHORITY_FIELDS = {
    "artifact_current",
    "current",
    "design_decision",
    "design_keep",
    "knowledge_authority",
    "professional_pass",
    "project_current",
    "project_state",
    "promotion",
    "release_authority",
    "source_authority",
    "statutory_approval",
}

MUTATING_SIDE_EFFECTS = {
    "LOCAL_MUTATION",
    "REMOTE_MUTATION",
    "AUTHORITY_MUTATION",
    "RELEASE_MUTATION",
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _iter_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield str(key).lower()
            yield from _iter_keys(item)
    elif isinstance(value, list):
        for item in value:
            yield from _iter_keys(item)


def assert_runtime_evidence_only(value: Any) -> None:
    leaked = sorted(set(_iter_keys(value)) & FORBIDDEN_AUTHORITY_FIELDS)
    if leaked:
        raise ValueError(f"runtime evidence contains forbidden authority field(s): {', '.join(leaked)}")


@dataclass(frozen=True)
class ExecutionEvent:
    event_id: str
    provider_id: str
    provider_session_id: str | None
    action_id: str
    event_type: str
    outcome: str
    observed_at: str
    payload: dict[str, Any] = field(default_factory=dict)
    does_not_prove: list[str] = field(
        default_factory=lambda: [
            "PROJECT_CURRENT",
            "DESIGN_DECISION",
            "ARTIFACT_CURRENT",
            "DESIGN_KEEP",
            "PROFESSIONAL_PASS",
            "PROMOTION",
        ]
    )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        assert_runtime_evidence_only(data["payload"])
        data["semantic_class"] = RUNTIME_EVIDENCE_ONLY
        return data


class ExecutionLedger:
    """Append-only execution evidence.

    The ledger is deliberately incapable of carrying Project State, Current,
    Design Decision, Artifact Current or Promotion fields. A JSONL path may be
    supplied for durable runtime evidence, but that file is never an authority
    store and may be deleted without deleting owner-native project truth.
    """

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self._events: list[ExecutionEvent] = []
        if path and path.is_file():
            for raw in path.read_text(encoding="utf-8").splitlines():
                if not raw.strip():
                    continue
                row = json.loads(raw)
                assert_runtime_evidence_only(row.get("payload", {}))
                self._events.append(
                    ExecutionEvent(
                        event_id=str(row["event_id"]),
                        provider_id=str(row["provider_id"]),
                        provider_session_id=row.get("provider_session_id"),
                        action_id=str(row["action_id"]),
                        event_type=str(row["event_type"]),
                        outcome=str(row["outcome"]),
                        observed_at=str(row["observed_at"]),
                        payload=dict(row.get("payload") or {}),
                        does_not_prove=list(row.get("does_not_prove") or []),
                    )
                )

    @property
    def events(self) -> tuple[ExecutionEvent, ...]:
        return tuple(self._events)

    def append(
        self,
        *,
        provider_id: str,
        action_id: str,
        event_type: str,
        outcome: str,
        provider_session_id: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> ExecutionEvent:
        payload = dict(payload or {})
        assert_runtime_evidence_only(payload)
        event = ExecutionEvent(
            event_id=f"evt_{uuid.uuid4().hex}",
            provider_id=provider_id,
            provider_session_id=provider_session_id,
            action_id=action_id,
            event_type=event_type,
            outcome=outcome,
            observed_at=_now_iso(),
            payload=payload,
        )
        self._events.append(event)
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8", newline="\n") as fh:
                fh.write(json.dumps(event.to_dict(), ensure_ascii=False, sort_keys=True) + "\n")
        return event

    def flush(self) -> None:
        if not self.path:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.flush()
            os.fsync(fh.fileno())

    def replay(self) -> list[dict[str, Any]]:
        return [event.to_dict() for event in self._events]

    def project(self) -> dict[str, Any]:
        by_action: dict[str, str] = {}
        for event in self._events:
            by_action[event.action_id] = event.outcome
        return {
            "semantic_class": "DISPOSABLE_EXECUTION_PROJECTION_NOT_AUTHORITY",
            "event_count": len(self._events),
            "last_outcome_by_action": by_action,
            "does_not_prove": ["PROJECT_STATE", "PROJECT_CURRENT", "ARTIFACT_CURRENT", "PROMOTION"],
        }


@dataclass(frozen=True)
class ActionRequest:
    action_id: str
    intent: str
    target_ref: str | None
    side_effect_class: str
    oleander_guard_decision: str
    provider_id: str = "native_cos"
    provider_session_id: str | None = None
    provider_approval: str = "NOT_REQUIRED"
    external_disclosure: bool = False
    scoped_external_permission: bool = False
    material_cost_or_blast_radius: bool = False
    cost_or_blast_radius_authorized: bool = False
    project_state_ref: str | None = None
    decision_object_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "ActionRequest":
        action_id = str(value.get("action_id") or "").strip()
        if not action_id:
            raise ValueError("action_id is required")
        side_effect = str(value.get("side_effect_class") or "").strip().upper()
        if side_effect not in {"READ_ONLY", *MUTATING_SIDE_EFFECTS}:
            raise ValueError(f"unsupported side_effect_class: {side_effect!r}")
        guard = str(value.get("oleander_guard_decision") or "").strip().upper()
        if guard not in {"ALLOW", "DENY", "HOLD"}:
            raise ValueError("oleander_guard_decision must be ALLOW, DENY or HOLD")
        if bool(value.get("external_disclosure")) and not bool(value.get("scoped_external_permission")):
            if guard == "ALLOW":
                raise ValueError("external disclosure cannot be ALLOW without scoped_external_permission")
        if bool(value.get("material_cost_or_blast_radius")) and not bool(value.get("cost_or_blast_radius_authorized")):
            if guard == "ALLOW":
                raise ValueError("material cost/blast radius cannot be ALLOW without authorization")
        metadata = dict(value.get("metadata") or {})
        assert_runtime_evidence_only(metadata)
        return cls(
            action_id=action_id,
            intent=str(value.get("intent") or "CONTINUE").upper(),
            target_ref=value.get("target_ref"),
            side_effect_class=side_effect,
            oleander_guard_decision=guard,
            provider_id=str(value.get("provider_id") or "native_cos"),
            provider_session_id=value.get("provider_session_id"),
            provider_approval=str(value.get("provider_approval") or "NOT_REQUIRED").upper(),
            external_disclosure=bool(value.get("external_disclosure")),
            scoped_external_permission=bool(value.get("scoped_external_permission")),
            material_cost_or_blast_radius=bool(value.get("material_cost_or_blast_radius")),
            cost_or_blast_radius_authorized=bool(value.get("cost_or_blast_radius_authorized")),
            project_state_ref=value.get("project_state_ref"),
            decision_object_id=value.get("decision_object_id"),
            metadata=metadata,
        )


Executor = Callable[[ActionRequest], dict[str, Any]]
Readback = Callable[[ActionRequest, dict[str, Any]], dict[str, Any]]


class ActionRuntime:
    """Typed action pipeline below OLEANDER authority semantics."""

    def __init__(self, ledger: ExecutionLedger | None = None) -> None:
        self.ledger = ledger or ExecutionLedger()

    def validate(self, request: ActionRequest) -> dict[str, Any]:
        if not isinstance(request, ActionRequest):
            raise TypeError("request must be an ActionRequest")
        assert_runtime_evidence_only(request.metadata)
        return {
            "status": "PASS",
            "action_id": request.action_id,
            "side_effect_class": request.side_effect_class,
            "authority_ceiling": EXECUTION_AUTHORITY_CEILING,
        }

    def authorize(self, request: ActionRequest) -> dict[str, Any]:
        if request.oleander_guard_decision != "ALLOW":
            return {"status": "BLOCKED_BY_OLEANDER", "guard_decision": request.oleander_guard_decision}
        if request.provider_approval in {"DENIED", "REJECTED"}:
            return {"status": "BLOCKED_BY_PROVIDER", "provider_approval": request.provider_approval}
        if request.provider_approval in {"PENDING", "DEFERRED", "REQUIRED"}:
            return {"status": "DEFERRED", "provider_approval": request.provider_approval}
        return {"status": "ALLOW", "provider_approval": request.provider_approval}

    def observe_delta(self, raw: Any) -> dict[str, Any]:
        value = raw if isinstance(raw, dict) else {"value": raw}
        assert_runtime_evidence_only(value)
        return value

    def readback(self, request: ActionRequest, provider_result: dict[str, Any], callback: Readback) -> dict[str, Any]:
        value = callback(request, provider_result)
        if not isinstance(value, dict):
            raise ValueError("readback must return a dict")
        assert_runtime_evidence_only(value)
        return value

    def defer(self, request: ActionRequest, reason: str) -> dict[str, Any]:
        self.ledger.append(
            provider_id=request.provider_id,
            provider_session_id=request.provider_session_id,
            action_id=request.action_id,
            event_type="ACTION_DEFERRED",
            outcome="DEFERRED",
            payload={"reason": reason},
        )
        return {
            "status": "DEFERRED",
            "action_id": request.action_id,
            "reason": reason,
            "authority_ceiling": EXECUTION_AUTHORITY_CEILING,
        }

    def execute(
        self,
        request: ActionRequest,
        executor: Executor,
        *,
        readback: Readback | None = None,
    ) -> dict[str, Any]:
        self.validate(request)
        self.ledger.append(
            provider_id=request.provider_id,
            provider_session_id=request.provider_session_id,
            action_id=request.action_id,
            event_type="ACTION_REQUESTED",
            outcome="RECEIVED",
            payload={
                "intent": request.intent,
                "target_ref": request.target_ref,
                "side_effect_class": request.side_effect_class,
                "project_state_ref": request.project_state_ref,
                "decision_object_id": request.decision_object_id,
            },
        )

        authorization = self.authorize(request)
        if authorization["status"] == "BLOCKED_BY_OLEANDER":
            self.ledger.append(
                provider_id=request.provider_id,
                provider_session_id=request.provider_session_id,
                action_id=request.action_id,
                event_type="ACTION_GUARD_BLOCKED",
                outcome="BLOCKED_BY_OLEANDER",
                payload={"guard_decision": request.oleander_guard_decision},
            )
            return self._result(request, "BLOCKED_BY_OLEANDER")

        if authorization["status"] == "BLOCKED_BY_PROVIDER":
            self.ledger.append(
                provider_id=request.provider_id,
                provider_session_id=request.provider_session_id,
                action_id=request.action_id,
                event_type="PROVIDER_APPROVAL_BLOCKED",
                outcome="BLOCKED_BY_PROVIDER",
                payload={"provider_approval": request.provider_approval},
            )
            return self._result(request, "BLOCKED_BY_PROVIDER")
        if authorization["status"] == "DEFERRED":
            return self.defer(request, "PROVIDER_APPROVAL_PENDING")

        self.ledger.append(
            provider_id=request.provider_id,
            provider_session_id=request.provider_session_id,
            action_id=request.action_id,
            event_type="EXECUTION_STARTED",
            outcome="RUNNING",
            payload={"side_effect_class": request.side_effect_class},
        )
        try:
            raw = self.observe_delta(executor(request))
        except Exception as exc:  # runtime boundary intentionally normalizes provider exceptions
            self.ledger.append(
                provider_id=request.provider_id,
                provider_session_id=request.provider_session_id,
                action_id=request.action_id,
                event_type="EXECUTION_FAILED",
                outcome="FAILED",
                payload={"error_type": type(exc).__name__, "error": str(exc)},
            )
            return self._result(request, "FAILED", error=str(exc))

        self.ledger.append(
            provider_id=request.provider_id,
            provider_session_id=request.provider_session_id,
            action_id=request.action_id,
            event_type="EXECUTION_OBSERVED",
            outcome="EXECUTED",
            payload={"provider_result": raw},
        )

        if request.side_effect_class in MUTATING_SIDE_EFFECTS and readback is None:
            self.ledger.append(
                provider_id=request.provider_id,
                provider_session_id=request.provider_session_id,
                action_id=request.action_id,
                event_type="READBACK_REQUIRED",
                outcome="PARTIAL",
                payload={"reason": "MATERIAL_MUTATION_WITHOUT_ACTUAL_READBACK"},
            )
            return self._result(request, "PARTIAL", provider_result=raw, readback_required=True)

        readback_result: dict[str, Any] | None = None
        if readback is not None:
            readback_result = self.readback(request, raw, readback)
            verdict = str(readback_result.get("status") or readback_result.get("verdict") or "UNKNOWN").upper()
            self.ledger.append(
                provider_id=request.provider_id,
                provider_session_id=request.provider_session_id,
                action_id=request.action_id,
                event_type="READBACK_COMPLETED",
                outcome=verdict,
                payload={"readback": readback_result},
            )
            if verdict not in {"PASS", "VERIFIED", "CONFIRMED_SUCCESS"}:
                return self._result(
                    request,
                    "PARTIAL",
                    provider_result=raw,
                    readback=readback_result,
                )

        self.ledger.append(
            provider_id=request.provider_id,
            provider_session_id=request.provider_session_id,
            action_id=request.action_id,
            event_type="EXECUTION_COMPLETED",
            outcome="COMPLETED",
            payload={"readback_present": readback_result is not None},
        )
        return self._result(request, "COMPLETED", provider_result=raw, readback=readback_result)

    def resume(
        self,
        request: ActionRequest,
        executor: Executor,
        *,
        provider_approval: str,
        readback: Readback | None = None,
    ) -> dict[str, Any]:
        resumed = ActionRequest(**{**asdict(request), "provider_approval": provider_approval.upper()})
        self.ledger.append(
            provider_id=resumed.provider_id,
            provider_session_id=resumed.provider_session_id,
            action_id=resumed.action_id,
            event_type="ACTION_RESUMED",
            outcome="RESUMED",
            payload={"provider_approval": resumed.provider_approval},
        )
        return self.execute(resumed, executor, readback=readback)

    @staticmethod
    def _result(request: ActionRequest, status: str, **extra: Any) -> dict[str, Any]:
        return {
            "status": status,
            "action_id": request.action_id,
            "provider_id": request.provider_id,
            "authority_ceiling": EXECUTION_AUTHORITY_CEILING,
            "changes_project_state": False,
            "changes_knowledge_authority": False,
            "changes_promotion_authority": False,
            **extra,
        }


@dataclass
class DurableJob:
    """Provider-neutral durable-job state carrier.

    The native implementation is synchronous and intentionally small. Temporal
    or another provider may back the same operations later, but job history is
    execution state only and never Project State.
    """

    job_id: str
    action_id: str
    provider_id: str = "native_cos"
    status_value: str = "PENDING"
    attempts: int = 0
    heartbeat_at: str | None = None
    last_error: str | None = None
    result: dict[str, Any] | None = None

    def start(self, operation: Callable[[], dict[str, Any]]) -> dict[str, Any]:
        if self.status_value not in {"PENDING", "RETRY_PENDING", "RECOVERING"}:
            raise ValueError(f"job {self.job_id} cannot start from {self.status_value}")
        self.status_value = "RUNNING"
        self.attempts += 1
        self.heartbeat()
        try:
            value = operation()
            if not isinstance(value, dict):
                value = {"value": value}
            assert_runtime_evidence_only(value)
            self.result = value
            self.status_value = "COMPLETED"
            self.last_error = None
        except Exception as exc:
            self.status_value = "FAILED"
            self.last_error = str(exc)
        return self.status()

    def status(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "action_id": self.action_id,
            "provider_id": self.provider_id,
            "status": self.status_value,
            "attempts": self.attempts,
            "heartbeat_at": self.heartbeat_at,
            "last_error": self.last_error,
            "result": self.result,
            "semantic_class": "DURABLE_EXECUTION_STATE_NOT_PROJECT_STATE",
            "authority_ceiling": EXECUTION_AUTHORITY_CEILING,
        }

    def wait(self, timeout_seconds: float = 0.0) -> dict[str, Any]:
        if timeout_seconds > 0:
            time.sleep(min(timeout_seconds, 0.05))
        return self.status()

    def heartbeat(self) -> dict[str, Any]:
        if self.status_value not in {"RUNNING", "RECOVERING"}:
            return self.status()
        self.heartbeat_at = _now_iso()
        return self.status()

    def retry(self) -> dict[str, Any]:
        if self.status_value != "FAILED":
            raise ValueError("retry requires FAILED state")
        self.status_value = "RETRY_PENDING"
        return self.status()

    def cancel(self) -> dict[str, Any]:
        if self.status_value in {"COMPLETED", "CANCELLED"}:
            return self.status()
        self.status_value = "CANCELLED"
        return self.status()

    def recover(self) -> dict[str, Any]:
        if self.status_value not in {"FAILED", "PARTIAL", "INTERRUPTED"}:
            raise ValueError("recover requires FAILED, PARTIAL or INTERRUPTED state")
        self.status_value = "RECOVERING"
        self.heartbeat()
        return self.status()
