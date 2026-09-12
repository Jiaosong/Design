#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_continuation_cycle import decide_checkpoint_resume
from validate_execution_locks import (
    decide_continuous_execution,
    evaluate_flow_completion,
    guard_checkpoint_mutation,
    resolve_continuation_frontier,
    resolve_sticky_constraints,
    validate_resolver,
)


ADAPTER_ID = "chat_on_steroids_oleander_resolver_adapter"
ROOT = Path(__file__).resolve().parents[2]


def _directive(
    *,
    frontier: dict | None,
    checkpoint_resume: dict | None,
    mutation_guard: dict | None,
    flow_completion: dict | None,
    auto_advance: dict | None,
) -> dict:
    """Compile existing Resolver decisions into a transient conversation directive."""
    if checkpoint_resume and checkpoint_resume.get("action") == "DO_NOT_REOPEN_CLOSED_TASK":
        return {"action": "STOP_CLOSED_TASK", "target": None, "basis": "CONTINUATION_CHECKPOINT"}

    if flow_completion and flow_completion.get("completion_gate") == "PASS":
        return {"action": "STOP_FLOW_COMPLETION_GATE_PASS", "target": None, "basis": "FLOW_COMPLETION_GATE"}

    if mutation_guard and mutation_guard.get("allowed") is False:
        return {
            "action": mutation_guard.get("action", "REFRESH_FRONTIER_BEFORE_MUTATION"),
            "target": None,
            "basis": "CHECKPOINT_SEQUENCE_GUARD",
        }

    if frontier:
        frontier_action = frontier.get("action", "")
        if frontier_action.startswith("HOLD_") or frontier_action.startswith("REVALIDATE_"):
            return {"action": frontier_action, "target": None, "basis": "FRONTIER_RESOLVER"}

    if checkpoint_resume:
        resume_action = checkpoint_resume.get("action", "")
        if resume_action.startswith("HOLD_") or resume_action.startswith("REVALIDATE_"):
            return {
                "action": resume_action,
                "target": checkpoint_resume.get("target"),
                "basis": "CONTINUATION_CHECKPOINT",
            }

    if auto_advance:
        if auto_advance.get("continue_allowed") is True:
            return {
                "action": auto_advance.get("action", "AUTO_ADVANCE_NEXT_READY_NODE"),
                "target": auto_advance.get("target"),
                "basis": "CONTINUOUS_EXECUTION_POLICY",
            }
        auto_action = auto_advance.get("action", "")
        if auto_action and auto_action != "HOLD_NO_READY_NODE_BEFORE_FLOW_COMPLETION":
            return {"action": auto_action, "target": auto_advance.get("target"), "basis": "CONTINUOUS_EXECUTION_POLICY"}

    if checkpoint_resume and checkpoint_resume.get("action") == "RESUME_NEXT_ALLOWED_ACTION":
        return {
            "action": "EXECUTE_NEXT_ALLOWED_ACTION",
            "target": checkpoint_resume.get("target"),
            "basis": "CONTINUATION_CHECKPOINT",
        }

    if frontier and frontier.get("action") == "RESUME_FROM_DISCOVERED_FRONTIER":
        return {
            "action": "LOAD_SELECTED_FRONTIER_CHECKPOINT",
            "target": frontier.get("selected_frontier"),
            "basis": "FRONTIER_RESOLVER",
        }

    return {"action": "PROCEED_WITH_EXISTING_OLEANDER_PREFLIGHT", "target": None, "basis": "RESOLVER"}


def run_preflight(payload: dict) -> dict:
    """Run a side-effect-free OLEANDER conversation preflight over caller-supplied Current evidence."""
    resolver = validate_resolver()
    identity = {
        "adapter_id": ADAPTER_ID,
        "authority_ceiling": "EXECUTION_ADAPTER_ONLY",
        "state_owner": False,
        "resolver_path": "00-governance/runtime/OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json",
        "resolver_version": resolver["version"],
        "resolver_implementation_revision": resolver["implementation_revision"],
        "resolver_status": resolver["status"],
    }

    frontier = None
    candidates = payload.get("candidate_frontiers")
    if candidates is not None:
        frontier = resolve_continuation_frontier(
            list(candidates),
            dict(payload.get("request_keys") or {}),
            payload.get("current_authority_fingerprint"),
            bool(payload.get("current_authority_identifies_one_active_task", True)),
        )

    checkpoint_resume = None
    checkpoint = payload.get("checkpoint")
    if checkpoint is not None:
        checkpoint_resume = decide_checkpoint_resume(
            dict(checkpoint),
            str(payload.get("current_authority_fingerprint") or ""),
        )

    constraint_lock = None
    if "constraint_sources" in payload:
        constraint_lock = resolve_sticky_constraints(list(payload.get("constraint_sources") or []))

    mutation_guard = None
    if "mutation_guard" in payload:
        guard = dict(payload.get("mutation_guard") or {})
        mutation_guard = guard_checkpoint_mutation(
            int(guard["current_sequence"]),
            int(guard["expected_sequence"]),
        )

    flow_completion = None
    if "flow_completion" in payload:
        flow_completion = evaluate_flow_completion(dict(payload.get("flow_completion") or {}))

    auto_advance = None
    if "auto_advance" in payload:
        args = dict(payload.get("auto_advance") or {})
        if flow_completion is not None:
            args["flow_completion_gate"] = flow_completion["completion_gate"]
        auto_advance = decide_continuous_execution(**args)

    directive = _directive(
        frontier=frontier,
        checkpoint_resume=checkpoint_resume,
        mutation_guard=mutation_guard,
        flow_completion=flow_completion,
        auto_advance=auto_advance,
    )

    return {
        "adapter": identity,
        "intent": payload.get("intent"),
        "frontier": frontier,
        "checkpoint_resume": checkpoint_resume,
        "constraint_lock": constraint_lock,
        "mutation_guard": mutation_guard,
        "flow_completion": flow_completion,
        "auto_advance": auto_advance,
        "conversation_directive": directive,
        "does_not_prove": [
            "PROJECT_STATE",
            "DESIGN_QUALITY",
            "ARTIFACT_CORRECTNESS",
            "COMPLETION_WITHOUT_FLOW_GATE_EVIDENCE",
        ],
    }


def _load_jsonl(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[row["case_id"]] = row
    return rows


def run_self_test() -> dict:
    """Exercise adapter composition against the existing runtime regression corpora."""
    locks = _load_jsonl(ROOT / "evals" / "runtime" / "sticky_constraints_and_flow.jsonl")
    cycles = _load_jsonl(ROOT / "evals" / "runtime" / "continuation_execution_cycle.jsonl")

    checks: list[tuple[str, bool]] = []

    case = cycles["CYCLE-010-RAW-RECEIPT-CHECKPOINT-RESUMES"]
    result = run_preflight({
        "intent": "CONTINUE",
        "current_authority_fingerprint": case["current_authority_fingerprint"],
        "checkpoint": case["checkpoint"],
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == "EXECUTE_NEXT_ALLOWED_ACTION" and result["conversation_directive"]["target"] == case["expected_target"]))

    case = cycles["CYCLE-012-RAW-RECEIPT-CLOSED-NEVER-REOPENS"]
    result = run_preflight({
        "intent": "CONTINUE",
        "current_authority_fingerprint": case["current_authority_fingerprint"],
        "checkpoint": case["checkpoint"],
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == "STOP_CLOSED_TASK"))

    case = locks["RESUME-006-MULTIPLE-DISTINCT-FRONTIERS-HOLD"]
    result = run_preflight({
        "intent": "CONTINUE",
        "candidate_frontiers": case["candidate_frontiers"],
        "request_keys": {},
        "current_authority_identifies_one_active_task": case["current_authority_identifies_one_active_task"],
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == case["expected_action"]))

    case = locks["CONCURRENCY-002-SEQUENCE-MISMATCH-REVALIDATE"]
    result = run_preflight({
        "intent": "CONTINUE",
        "mutation_guard": {
            "current_sequence": case["current_sequence"],
            "expected_sequence": case["expected_sequence"],
        },
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == case["expected_action"]))

    case = locks["CHAT-PREFLIGHT-001-GENERIC-CONTINUE-PRESERVES-STICKY"]
    result = run_preflight({"intent": "CONTINUE", "constraint_sources": case["constraint_sources"]})
    checks.append((case["case_id"], set(result["constraint_lock"]["active_constraints"]) == set(case["expected_active_constraints"])))

    case = locks["CHAT-PREFLIGHT-003-INCOMPLETE-FLOW-BLOCKS-COMPLETE"]
    result = run_preflight({"intent": "CONTINUE", "flow_completion": case["flow_completion"]})
    checks.append((case["case_id"], result["flow_completion"]["completion_gate"] == case["expected_completion_gate"] and result["flow_completion"]["completion_claim_allowed"] is False))

    case = locks["CHAT-PREFLIGHT-006-FLOW-PASS-STOPS-AUTO-ADVANCE"]
    result = run_preflight({"intent": "CONTINUE", "auto_advance": case["auto_advance"]})
    checks.append((case["case_id"], result["conversation_directive"]["action"] == case["expected_action"]))

    failed = [case_id for case_id, passed in checks if not passed]
    if failed:
        raise RuntimeError(f"adapter self-test failed: {failed}")
    return {"status": "PASS", "adapter_id": ADAPTER_ID, "cases": [case_id for case_id, _ in checks]}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stateless Chat/CoS adapter for the existing OLEANDER continuation resolver."
    )
    parser.add_argument("input", nargs="?", help="JSON input file; omit or use '-' for stdin")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--self-test", action="store_true", help="Run adapter composition against existing OLEANDER eval cases")
    args = parser.parse_args()

    try:
        if args.self_test:
            print(json.dumps(run_self_test(), ensure_ascii=False, indent=2))
            return
        if not args.input or args.input == "-":
            payload = json.load(sys.stdin)
        else:
            with open(args.input, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        if not isinstance(payload, dict):
            raise ValueError("input must be one JSON object")
        result = run_preflight(payload)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "INVALID_PREFLIGHT_INPUT", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))


if __name__ == "__main__":
    main()
