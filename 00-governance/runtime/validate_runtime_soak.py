#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_continuation_cycle import decide_checkpoint_resume
from validate_execution_locks import guard_checkpoint_mutation
from validate_runtime_decisions import decide_known_failure
from validate_runtime_resilience import (
    classify_review_independence,
    decide_execution_budget,
    decide_surface_probe,
    reconcile_partial_commit,
    review_requirement_satisfied,
)

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
P4_RECEIPT = RUNTIME / "receipts" / "EXR-20260909-PR499-CAD-DIRECT-P4-REPLAY.json"
P5_RECEIPT = RUNTIME / "receipts" / "EXR-20260909-P5-CROSS-PROJECT-SURFACE-ADOPTION.json"
CASES = ROOT / "evals" / "runtime" / "runtime_soak.jsonl"


def fail(msg: str) -> None:
    raise SystemExit(f"runtime-soak validation failed: {msg}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid or missing JSON {path.relative_to(ROOT)}: {exc}")


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as exc:
        fail(f"missing corpus {path.relative_to(ROOT)}: {exc}")
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{lineno}: {exc}")
    return rows


def validate_real_provenance() -> tuple[dict, dict]:
    p4 = load_json(P4_RECEIPT)
    p5 = load_json(P5_RECEIPT)
    if p4.get("task_id") != "P4-REAL-PROJECT-REPLAY-PR499" or p4.get("status") != "CLOSED":
        fail("P9 requires the real P4 replay receipt to remain CLOSED")
    if p4.get("continuation_checkpoint", {}).get("checkpoint_state") != "CLOSED":
        fail("P9 requires the real P4 checkpoint to remain CLOSED")
    if p5.get("task_id") != "P5-CROSS-PROJECT-SURFACE-ADOPTION-20260909" or p5.get("status") != "CLOSED":
        fail("P9 requires the real P5 adoption receipt to remain CLOSED")
    if p5.get("continuation_checkpoint", {}).get("checkpoint_state") != "CLOSED":
        fail("P9 requires the real P5 checkpoint to remain CLOSED")
    predecessor = p5.get("cross_project_adoption_evidence", {}).get("predecessor", {})
    if predecessor.get("task_id") != p4.get("task_id") or predecessor.get("replay_performed") is not False:
        fail("P9 requires P5 to preserve the real P4 closed/no-replay boundary")
    return p4, p5


def validate_platform_boundary() -> None:
    resolver = load_json(RESOLVER)
    continuous = resolver.get("continuous_execution_policy", {})
    if continuous.get("background_execution_forbidden") is not True:
        fail("P9 must not claim persistent background execution")
    if continuous.get("generic_child_agent_spawn_not_assumed") is not True:
        fail("P9 must not claim arbitrary child-agent concurrency")


def evaluate_event(event: dict, p5: dict) -> dict:
    kind = event.get("kind")
    if kind == "CHECKPOINT_GUARD":
        result = guard_checkpoint_mutation(
            int(event["current_sequence"]),
            int(event["expected_sequence"]),
        )
        return {"action": result["action"], "allowed": result["allowed"]}

    if kind == "CLOSED_CONTINUE":
        checkpoint = p5.get("continuation_checkpoint", {}) if event.get("checkpoint_source") == "P5_RECEIPT" else event["checkpoint"]
        result = decide_checkpoint_resume(checkpoint, event.get("current_authority_fingerprint", "P9-AUTH"))
        return {"action": result["action"], "target": result.get("target")}

    if kind == "PARTIAL_COMMIT":
        result = reconcile_partial_commit(event["legs"])
        return {
            "action": result["action"],
            "advance_allowed": result["advance_allowed"],
        }

    if kind == "SURFACE_PROBE":
        result = decide_surface_probe(event["health"], int(event["now_epoch"]))
        return {"action": result["action"], "probe_allowed": result["probe_allowed"]}

    if kind == "KNOWN_FAILURE":
        k = event["known_failure"]
        result = decide_known_failure(
            current_failure_signature=k["current_failure_signature"],
            current_applicability=k["current_applicability"],
            materially_new_context=k["materially_new_context"],
            prior_repair_applied=k["prior_repair_applied"],
            known_failure_records=k["known_failure_records"],
        )
        return {"action": result["action"], "state": result["state"]}

    if kind == "EXECUTION_BUDGET":
        result = decide_execution_budget(event["counters"], event.get("budget"))
        return {"action": result["action"], "continue_allowed": result["continue_allowed"]}

    if kind == "REVIEW_GATE":
        state = classify_review_independence(event["review"])
        satisfied = review_requirement_satisfied(event["task_class"], state)
        return {
            "action": "REVIEW_REQUIREMENT_SATISFIED" if satisfied else "HOLD_REVIEW_INDEPENDENCE_INSUFFICIENT",
            "independence_state": state,
            "requirement_satisfied": satisfied,
        }

    fail(f"unknown soak event kind {kind}")
    return {}


def validate_soak() -> None:
    _, p5 = validate_real_provenance()
    validate_platform_boundary()
    rows = load_jsonl(CASES)
    if len(rows) != 1 or rows[0].get("case_id") != "P9-001-BOUNDED-INTERLEAVING-SOAK":
        fail("P9 must keep one bounded deterministic soak scenario")
    scenario = rows[0]
    events = scenario.get("events", [])
    expected_order = [
        "STALE_WRITER_BLOCKED",
        "CLOSED_P5_NOT_REOPENED",
        "PARTIAL_COMMIT_BLOCKS_ADVANCE",
        "FAILED_SURFACE_REPROBE_SUPPRESSED",
        "KNOWN_FAILURE_RECURRENCE_REUSES_REPAIR",
        "EXECUTION_BUDGET_STOPS_RUNAWAY_LOOP",
        "PARTIAL_REVIEW_BLOCKS_PROMOTION",
        "RECONCILED_COMMIT_CAN_ADVANCE",
        "REFRESHED_WRITER_SEQUENCE_MATCHES",
    ]
    if [e.get("event_id") for e in events] != expected_order:
        fail("P9 soak event order drifted")

    closed_frontiers = {"P4", "P5"}
    observed: list[dict] = []
    for event in events:
        mutation_target = event.get("mutation_target")
        if mutation_target in closed_frontiers:
            fail(f"P9 attempted mutation against closed frontier {mutation_target}")
        result = evaluate_event(event, p5)
        observed.append({"event_id": event["event_id"], **result})
        for key, expected in event.get("expected", {}).items():
            if result.get(key) != expected:
                fail(f"{event['event_id']} expected {key}={expected!r}, observed {result.get(key)!r}")

    by_id = {row["event_id"]: row for row in observed}
    if by_id["STALE_WRITER_BLOCKED"].get("allowed") is not False:
        fail("P9 stale writer was not blocked")
    if by_id["CLOSED_P5_NOT_REOPENED"].get("action") != "DO_NOT_REOPEN_CLOSED_TASK":
        fail("P9 reopened closed P5")
    if by_id["PARTIAL_COMMIT_BLOCKS_ADVANCE"].get("advance_allowed") is not False:
        fail("P9 advanced through a partial commit")
    if by_id["RECONCILED_COMMIT_CAN_ADVANCE"].get("advance_allowed") is not True:
        fail("P9 failed to advance after coherent reconciliation")
    if by_id["REFRESHED_WRITER_SEQUENCE_MATCHES"].get("allowed") is not True:
        fail("P9 failed to recover the refreshed writer after sequence re-read")


def main() -> None:
    validate_soak()
    print("runtime-soak validation: PASS")
    print("P9 deterministic interleaving uses real P4/P5 closed provenance: VERIFIED")
    print("P9 stale writer / closed task / partial commit / cooldown / known failure / budget / review gates: ENFORCED")
    print("P9 coherent reconciliation and refreshed sequence recover without state leakage: ENFORCED")
    print("P9 does not claim background workers, arbitrary child-agent concurrency, or platform scheduler proof: PRESERVED")


if __name__ == "__main__":
    main()
