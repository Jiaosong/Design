#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from validate_runtime_decisions import decide_known_failure, select_reliable_surface

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
CASES = ROOT / "evals" / "runtime" / "continuation_execution_cycle.jsonl"


def fail(msg: str) -> None:
    raise SystemExit(f"continuation-cycle validation failed: {msg}")


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


def decide_checkpoint_resume(checkpoint: dict, current_authority_fingerprint: str) -> dict:
    """Compile existing continuation rules without replaying already verified completed nodes."""
    state = checkpoint.get("checkpoint_state")
    if state == "CLOSED":
        return {"action": "DO_NOT_REOPEN_CLOSED_TASK", "target": None, "skipped_nodes": []}
    if state != "RESUMABLE":
        return {"action": "REVALIDATE_FRONTIER", "reason": "CHECKPOINT_NOT_RESUMABLE", "target": None, "skipped_nodes": []}
    if checkpoint.get("authority_fingerprint") != current_authority_fingerprint:
        return {"action": "REVALIDATE_FRONTIER", "reason": "AUTHORITY_FINGERPRINT_MISMATCH", "target": None, "skipped_nodes": []}
    if checkpoint.get("last_verified_artifact_readback") is not True:
        return {"action": "REVALIDATE_FRONTIER", "reason": "LAST_ARTIFACT_NOT_READBACK_VERIFIED", "target": None, "skipped_nodes": []}
    if checkpoint.get("stale_dependency") is True:
        return {"action": "REVALIDATE_FRONTIER", "reason": "STALE_DEPENDENCY_OR_HANDOFF", "target": None, "skipped_nodes": []}

    completed = list(checkpoint.get("completed_nodes") or [])
    target = checkpoint.get("next_allowed_action")
    if not target:
        return {"action": "HOLD_INVALID_FRONTIER", "reason": "MISSING_NEXT_ALLOWED_ACTION", "target": None, "skipped_nodes": completed}
    if target in completed:
        return {"action": "HOLD_INVALID_FRONTIER", "reason": "NEXT_ACTION_ALREADY_VERIFIED_COMPLETED", "target": None, "skipped_nodes": completed}
    return {"action": "RESUME_NEXT_ALLOWED_ACTION", "target": target, "skipped_nodes": completed}


def decide_repair_return(
    *,
    failed_node: str,
    next_ready_node: str | None,
    authority_match: bool,
    regression_passed: bool,
    failed_node_readback_passed: bool,
) -> dict:
    """Return to the failed DAG frontier after repair, then advance only after that frontier is readback-verified."""
    if not authority_match:
        return {"action": "REVALIDATE_FRONTIER", "target": None}
    if not regression_passed:
        return {"action": "HOLD_REPAIR_REGRESSION_NOT_PASS", "target": None}
    if not failed_node_readback_passed:
        return {"action": "RESUME_ORIGINAL_DAG_FRONTIER", "target": failed_node}
    if next_ready_node:
        return {"action": "ADVANCE_NEXT_READY_NODE", "target": next_ready_node}
    return {"action": "RESOLVE_NEXT_READY_NODE", "target": None}


def validate_contract_bindings() -> None:
    resolver = load_json(RESOLVER)
    if resolver.get("version") != "1.2" or resolver.get("implementation_revision") != "1.2.5":
        fail("P3 must bind current Resolver v1.2 implementation revision 1.2.5")

    continuation = resolver.get("continuation_checkpoint_policy", {})
    if continuation.get("cross_chat_restore_behavior") != "DISCOVER_EXISTING_FRONTIER_THEN_APPLY_DIRECT_RESUME_OR_REVALIDATE_RULES":
        fail("cross-chat restore behavior drifted")
    if continuation.get("resume_behavior") != "SKIP_ALREADY_VERIFIED_COMPLETED_NODES_AND_EXECUTE_NEXT_ALLOWED_ACTION":
        fail("resume must skip verified completed nodes")
    if continuation.get("blind_repeat_completed_mutation_forbidden") is not True:
        fail("blind replay of completed mutations must remain forbidden")
    if continuation.get("context_switch_or_compression_is_not_authority_change") is not True:
        fail("context switch alone must not force a new authority")

    continuous = resolver.get("continuous_execution_policy", {})
    failure_rule = continuous.get("failure_rule", "")
    if "ROOT_CAUSE_REPAIR_RETEST_THEN_CONTINUE_IF_NEXT_NODE_IS_READY" not in failure_rule:
        fail("continuous execution must retain repair/retest then continue behavior")
    loop = continuous.get("loop_sequence", [])
    required_loop = ["EXECUTE_READY_NODE", "SELECTIVE_READBACK", "REPAIR_AND_RETEST_IF_LEGAL_AND_NEEDED", "UPDATE_EXISTING_CHECKPOINT_IF_TRIGGERED", "RESOLVE_NEXT_READY_NODE", "CONTINUE_WHILE_ALLOWED"]
    if loop != required_loop:
        fail("continuous execution loop sequence drifted")


def validate_cases() -> None:
    rows = load_jsonl(CASES)
    by_id = {row.get("case_id"): row for row in rows}
    required = {
        "CYCLE-001-CROSS-CHAT-RESUME-SKIPS-VERIFIED",
        "CYCLE-002-CROSS-CHAT-AUTHORITY-DRIFT-REVALIDATES",
        "CYCLE-003-KNOWN-FAILURE-REPAIR-RETURNS-SAME-FRONTIER",
        "CYCLE-004-FAILED-REGRESSION-STAYS-BLOCKED",
        "CYCLE-005-RETESTED-FRONTIER-ADVANCES-NEXT-READY",
        "CYCLE-006-FALLBACK-RECOVERS-TO-PRIMARY-AFTER-REVALIDATION",
    }
    missing = required - set(by_id)
    if missing:
        fail(f"missing P3 continuation cases {sorted(missing)}")

    for case_id in [
        "CYCLE-001-CROSS-CHAT-RESUME-SKIPS-VERIFIED",
        "CYCLE-002-CROSS-CHAT-AUTHORITY-DRIFT-REVALIDATES",
    ]:
        c = by_id[case_id]
        result = decide_checkpoint_resume(c["checkpoint"], c["current_authority_fingerprint"])
        if result["action"] != c["expected_action"]:
            fail(f"{case_id} checkpoint action mismatch")
        if result.get("target") != c.get("expected_target"):
            fail(f"{case_id} checkpoint target mismatch")
        if "expected_reason" in c and result.get("reason") != c["expected_reason"]:
            fail(f"{case_id} checkpoint reason mismatch")
        for node in c.get("expected_skipped_nodes", []):
            if node not in result.get("skipped_nodes", []):
                fail(f"{case_id} did not preserve skipped verified node {node}")
        for node in c.get("forbidden_targets", []):
            if result.get("target") == node:
                fail(f"{case_id} replayed forbidden target {node}")

    c = by_id["CYCLE-003-KNOWN-FAILURE-REPAIR-RETURNS-SAME-FRONTIER"]
    k = c["known_failure"]
    failure_result = decide_known_failure(
        current_failure_signature=k["current_failure_signature"],
        current_applicability=k["current_applicability"],
        materially_new_context=k["materially_new_context"],
        prior_repair_applied=k["prior_repair_applied"],
        known_failure_records=k["known_failure_records"],
    )
    if failure_result["action"] != c["expected_failure_action"]:
        fail("CYCLE-003 known-failure repair path mismatch")
    cycle_result = decide_repair_return(
        failed_node=c["failed_node"],
        next_ready_node=c.get("next_ready_node"),
        authority_match=c["authority_match"],
        regression_passed=c["regression_passed"],
        failed_node_readback_passed=c["failed_node_readback_passed"],
    )
    if cycle_result["action"] != c["expected_cycle_action"] or cycle_result.get("target") != c["expected_target"]:
        fail("CYCLE-003 did not return to original DAG frontier")

    for case_id in ["CYCLE-004-FAILED-REGRESSION-STAYS-BLOCKED", "CYCLE-005-RETESTED-FRONTIER-ADVANCES-NEXT-READY"]:
        c = by_id[case_id]
        result = decide_repair_return(
            failed_node=c["failed_node"],
            next_ready_node=c.get("next_ready_node"),
            authority_match=c["authority_match"],
            regression_passed=c["regression_passed"],
            failed_node_readback_passed=c["failed_node_readback_passed"],
        )
        if result["action"] != c["expected_cycle_action"] or result.get("target") != c.get("expected_target"):
            fail(f"{case_id} repair-return decision mismatch")
        for node in c.get("forbidden_targets", []):
            if result.get("target") == node:
                fail(f"{case_id} advanced to forbidden target {node}")

    c = by_id["CYCLE-006-FALLBACK-RECOVERS-TO-PRIMARY-AFTER-REVALIDATION"]
    initial = select_reliable_surface(c["initial_candidates"])
    recovered = select_reliable_surface(c["revalidated_candidates"])
    if initial["action"] != c["expected_initial_action"] or initial.get("selected_surface") != c["expected_initial_surface"]:
        fail("CYCLE-006 initial fallback selection mismatch")
    if recovered["action"] != c["expected_recovered_action"] or recovered.get("selected_surface") != c["expected_recovered_surface"]:
        fail("CYCLE-006 primary recovery mismatch")
    if initial.get("selected_surface") == recovered.get("selected_surface"):
        fail("CYCLE-006 fallback became sticky after primary recovery")


def main() -> None:
    validate_contract_bindings()
    validate_cases()
    print("continuation-cycle validation: PASS")
    print("cross-chat restore skips verified completed nodes: ENFORCED")
    print("authority drift revalidates before execution: ENFORCED")
    print("known-failure repair returns to original DAG frontier: ENFORCED")
    print("failed regression blocks resume/advance: ENFORCED")
    print("readback-verified repaired frontier advances next ready node: ENFORCED")
    print("fallback is non-sticky and primary is restored after revalidation: ENFORCED")
    print("no new authority/project-state/checkpoint-db/plugin-state ontology: PRESERVED")


if __name__ == "__main__":
    main()
