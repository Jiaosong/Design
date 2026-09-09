#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
RECEIPT_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_RECEIPT_v1.0.json"
TOOL_CONTRACT = RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json"
RECEIPT_DIR = RUNTIME / "receipts"
CASES = ROOT / "evals" / "runtime" / "sticky_constraints_and_flow.jsonl"


def fail(msg: str) -> None:
    raise SystemExit(f"execution-lock validation failed: {msg}")


def load_json(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.relative_to(ROOT)}: {exc}")


def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    rows: list[dict] = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except Exception as exc:
            fail(f"invalid JSONL {path.relative_to(ROOT)}:{lineno}: {exc}")
    return rows


def require_present(obj: dict, fields: list[str] | set[str], context: str) -> None:
    missing = [f for f in fields if f not in obj or obj[f] in (None, "")]
    if missing:
        fail(f"{context} missing fields {missing}")


def _ids(value) -> set[str]:
    if value is None:
        return set()
    if isinstance(value, str):
        return {value}
    return {str(x) for x in value}


def _parse_ts(value: str | None) -> datetime:
    if not value:
        return datetime.min
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return datetime.min


def resolve_continuation_frontier(
    candidates: list[dict],
    request_keys: dict,
    current_authority_fingerprint: str | None,
    current_authority_identifies_one_active_task: bool = True,
) -> dict:
    """Pure deterministic resolver over existing frontier records."""
    active = [c for c in candidates if c.get("status", "WORKING") in {"WORKING", "HOLD"}]
    if not active:
        return {"state": "HOLD", "action": "HOLD_NO_ACTIVE_FRONTIER", "selected_frontier": None}

    project_key = request_keys.get("project_id") or request_keys.get("scope_id")
    task_key = request_keys.get("task_id")
    object_keys = _ids(request_keys.get("object_or_canonical_ids"))
    native_ref = request_keys.get("current_native_master_or_ref")

    def matches(c: dict) -> bool:
        if project_key and (c.get("project_id") or c.get("scope_id")) != project_key:
            return False
        if task_key and c.get("task_id") != task_key:
            return False
        if object_keys and not object_keys.intersection(_ids(c.get("object_or_canonical_ids"))):
            return False
        if native_ref and c.get("current_native_master_or_ref") != native_ref:
            return False
        return True

    scoped = [c for c in active if matches(c)]
    if not scoped:
        return {"state": "HOLD", "action": "HOLD_NO_MATCHING_FRONTIER", "selected_frontier": None}

    distinct_tasks = {(c.get("project_id") or c.get("scope_id"), c.get("task_id")) for c in scoped}
    if len(distinct_tasks) > 1 and not task_key and not current_authority_identifies_one_active_task:
        return {
            "state": "HOLD",
            "action": "HOLD_AMBIGUOUS_FRONTIER",
            "selected_frontier": None,
            "candidate_count": len(scoped),
        }

    if current_authority_fingerprint:
        matching = [c for c in scoped if c.get("authority_fingerprint") == current_authority_fingerprint]
        if matching:
            scoped = matching
        else:
            best = max(
                scoped,
                key=lambda c: (int(c.get("checkpoint_sequence", -1)), _parse_ts(c.get("checkpoint_updated_at"))),
            )
            return {
                "state": "REVALIDATE",
                "action": "REVALIDATE_AUTHORITY_BEFORE_MUTATION",
                "selected_frontier": best.get("task_id"),
                "frontier": best,
            }

    best = max(
        scoped,
        key=lambda c: (int(c.get("checkpoint_sequence", -1)), _parse_ts(c.get("checkpoint_updated_at"))),
    )
    return {
        "state": best.get("checkpoint_state", "RESUMABLE"),
        "action": "RESUME_FROM_DISCOVERED_FRONTIER",
        "selected_frontier": best.get("task_id"),
        "frontier": best,
    }


def guard_checkpoint_mutation(current_sequence: int, expected_sequence: int) -> dict:
    """Optimistic concurrency. Sequence is truth; lease is advisory metadata only."""
    if current_sequence != expected_sequence:
        return {
            "allowed": False,
            "state": "REVALIDATE_CONCURRENT_ADVANCE",
            "action": "REFRESH_FRONTIER_BEFORE_MUTATION",
        }
    return {"allowed": True, "state": "SEQUENCE_MATCH", "action": "PROCEED_WITH_AUTHORIZED_MUTATION"}


def resolve_uncertain_mutation(
    outcome_state: str,
    expected_postcondition_observed: bool,
    operation_is_idempotent_or_keyed: bool,
    retry_count: int,
    retry_limit: int,
) -> dict:
    """Verify-before-retry decision for remote side effects with uncertain outcomes."""
    if outcome_state == "CONFIRMED_SUCCESS":
        return {"action": "NO_RETRY", "normalized_outcome": "CONFIRMED_SUCCESS"}
    if outcome_state == "CONFIRMED_FAILURE":
        if operation_is_idempotent_or_keyed and retry_count < retry_limit:
            return {"action": "BOUNDED_SAFE_RETRY", "normalized_outcome": "CONFIRMED_FAILURE"}
        return {"action": "HOLD_RETRY_UNSAFE_OR_EXHAUSTED", "normalized_outcome": "CONFIRMED_FAILURE"}
    if outcome_state != "UNCERTAIN":
        return {"action": "HOLD_INVALID_OUTCOME_STATE", "normalized_outcome": "UNKNOWN"}
    if expected_postcondition_observed:
        return {"action": "NO_RETRY", "normalized_outcome": "CONFIRMED_SUCCESS"}
    if operation_is_idempotent_or_keyed and retry_count < retry_limit:
        return {"action": "BOUNDED_SAFE_RETRY", "normalized_outcome": "CONFIRMED_ABSENT_AFTER_READBACK"}
    return {"action": "HOLD_RETRY_UNSAFE_OR_EXHAUSTED", "normalized_outcome": "UNCERTAIN"}


def validate_resolver() -> dict:
    data = load_json(RESOLVER)
    if data.get("version") != "1.2" or data.get("implementation_revision") != "1.2.5":
        fail("Current resolver must be v1.2 implementation revision 1.2.5")
    if data.get("status") != "ACTIVE_CURRENT":
        fail("Current resolver must remain ACTIVE_CURRENT")

    sticky = data.get("sticky_execution_constraints", {})
    required_rules = {
        "NO_IMAGE_GENERATION", "NO_NEW_SKILL", "NO_NEW_METHOD", "NO_NEW_FRAMEWORK",
        "USE_EXISTING_OLEANDER_METHODS_AND_SKILLS", "FULL_OLEANDER_FLOW_REQUIRED",
        "NO_PRODUCER_SELF_PROMOTION",
    }
    if not sticky.get("required") or not sticky.get("resolve_before_owner_or_tool_selection"):
        fail("sticky execution constraints must be mandatory and pre-routing")
    if not required_rules.issubset(set(sticky.get("normalized_rules", []))):
        fail("resolver sticky normalized rules incomplete")
    if sticky.get("generic_continue_does_not_revoke") is not True:
        fail("generic continue must not revoke constraints")

    continuation = data.get("continuation_checkpoint_policy", {})
    required_checkpoint_fields = {
        "checkpoint_state", "current_node", "last_verified_artifact", "resume_from",
        "next_allowed_action", "authority_fingerprint", "stale_reasons",
        "checkpoint_sequence", "checkpoint_updated_at", "expected_checkpoint_sequence",
        "executor_id", "execution_lease_state", "lease_acquired_at",
    }
    if continuation.get("generic_followup_same_task_default") != "RESUME_FROM_LAST_VERIFIED_CHECKPOINT":
        fail("same-task generic follow-up must resume from last verified checkpoint")
    if not required_checkpoint_fields.issubset(set(continuation.get("required_checkpoint_fields", []))):
        fail("continuation checkpoint fields incomplete")
    if continuation.get("chat_history_or_summary_is_not_checkpoint_authority") is not True:
        fail("chat history/summary must not become checkpoint authority")
    if "HOLD_AMBIGUOUS_FRONTIER" not in continuation.get("distinct_task_ambiguity_rule", ""):
        fail("multiple distinct frontiers must HOLD when Current cannot disambiguate")

    concurrency = data.get("execution_concurrency_policy", {})
    if concurrency.get("mode") != "OPTIMISTIC_CHECKPOINT_SEQUENCE":
        fail("execution concurrency must use optimistic checkpoint sequence")
    if concurrency.get("sequence_is_authoritative") is not True:
        fail("checkpoint sequence must be authoritative over lease hints")
    if concurrency.get("lease_metadata_is_advisory_only") is not True:
        fail("lease metadata must remain advisory")
    if concurrency.get("sequence_mismatch_state") != "REVALIDATE_CONCURRENT_ADVANCE":
        fail("sequence mismatch must force concurrent revalidation")
    if concurrency.get("global_lock_service_forbidden") is not True:
        fail("runtime must not create a global lock service")

    continuous = data.get("continuous_execution_policy", {})
    if continuous.get("no_artificial_one_node_stop") is not True:
        fail("continuous execution must forbid artificial one-node stop")
    if continuous.get("background_execution_forbidden") is not True:
        fail("continuous execution must not imply background work")

    flow = data.get("flow_completion_gate", {})
    if flow.get("does_not_mean_all_skills") is not True or flow.get("minimum_owner_set_still_applies") is not True:
        fail("full flow must preserve minimum sufficient owner set")
    early = set(flow.get("early_stop_states_that_do_not_equal_completion", []))
    if not {"PR_OPENED", "CI_GREEN", "SELF_CHECK_PASS", "ARTIFACT_CREATED"}.issubset(early):
        fail("early completion denylist incomplete")

    order = data.get("default_resolution_order", [])
    required_order = [
        "READ_APPLICABLE_PROJECT_STATE_SOURCE_AUTHORITY_CURRENT_TASK",
        "DISCOVER_ACTIVE_EXECUTION_FRONTIER_IF_CONTEXT_POINTER_MISSING",
        "RESOLVE_CONTINUATION_CHECKPOINT_IF_FOLLOWUP_INTENT",
        "RESOLVE_STICKY_EXECUTION_CONSTRAINTS",
        "GUARD_EXPECTED_CHECKPOINT_SEQUENCE_BEFORE_MUTATION",
        "EXECUTE_ACTUAL_NATIVE_ARTIFACT",
        "ACTUAL_READBACK",
        "UPDATE_EXISTING_CONTINUATION_CHECKPOINT_AS_APPLICABLE",
        "AUTO_ADVANCE_READY_NODES_UNTIL_STOP_CONDITION",
        "VERIFY_FLOW_COMPLETION_GATE_BEFORE_CLOSURE_OR_COMPLETE_CLAIM",
    ]
    positions = []
    for token in required_order:
        if token not in order:
            fail(f"resolver order missing {token}")
        positions.append(order.index(token))
    if positions != sorted(positions):
        fail("resolver execution/concurrency order is invalid")
    return data


def validate_tool_adapter_routing() -> dict:
    data = load_json(TOOL_CONTRACT)
    if data.get("contract_id") != "OLEANDER_TOOL_ADAPTER_CONTRACT" or data.get("version") != "0.1":
        fail("Tool Adapter Contract identity/version drift")
    if data.get("status") != "ACTIVE_CURRENT":
        fail("Tool Adapter Contract must remain ACTIVE_CURRENT")

    routing = data.get("unified_adapter_routing_policy", {})
    for key in [
        "vendor_name_must_not_determine_route", "route_by_capability_role",
        "do_not_probe_every_connected_surface", "probe_selected_or_needed_fallback_only",
        "availability_is_runtime_fact_not_authority", "mutation_surface_must_not_exceed_authority_ceiling",
        "no_parallel_plugin_state_store", "no_new_surface_registry_entry_for_one_off_connector_use",
    ]:
        if routing.get(key) is not True:
            fail(f"unified adapter routing requires {key}=true")

    idempotency = data.get("remote_mutation_idempotency_policy", {})
    required_fields = {
        "operation_fingerprint", "expected_postcondition", "outcome_state",
        "verification_surface", "retry_decision",
    }
    if not required_fields.issubset(set(idempotency.get("record_fields", []))):
        fail("remote mutation idempotency fields incomplete")
    if idempotency.get("uncertain_outcome_action") != "VERIFY_POSTCONDITION_BEFORE_RETRY":
        fail("uncertain remote mutation must verify postcondition before retry")
    if idempotency.get("duplicate_side_effects_forbidden") is not True:
        fail("duplicate remote side effects must be forbidden")
    if idempotency.get("bounded_retry_only_when_safe_or_provider_keyed") is not True:
        fail("retry must be bounded and safe/idempotency-keyed")

    heavy = data.get("heavy_executor_policy", {})
    if heavy.get("default") != "ESCALATION_ONLY" or heavy.get("control_plane_role") is not False:
        fail("heavy executor must remain escalation-only and not control plane")
    return data


def validate_receipt_contract() -> dict:
    data = load_json(RECEIPT_CONTRACT)
    if data.get("version") != "1.0" or data.get("policy_revision") != "1.1":
        fail("Execution Receipt must remain v1.0 policy revision 1.1")
    additional = set(data.get("policy_1_1_additional_required_core_fields", []))
    if additional != {"constraint_lock", "flow_completion"}:
        fail("policy 1.1 must add exactly constraint_lock and flow_completion")

    cp = data.get("continuation_checkpoint_extension", {})
    required_cp = {
        "checkpoint_state", "current_node", "last_verified_artifact", "resume_from",
        "next_allowed_action", "authority_fingerprint", "stale_reasons",
        "checkpoint_sequence", "checkpoint_updated_at", "expected_checkpoint_sequence",
        "executor_id", "execution_lease_state", "lease_acquired_at",
    }
    if not required_cp.issubset(set(cp.get("fields", []))):
        fail("Receipt continuation checkpoint fields incomplete")
    if cp.get("checkpoint_is_runtime_state_not_project_state") is not True:
        fail("Receipt checkpoint must not become second Project State")

    concurrency = data.get("concurrency_guard_extension", {})
    if concurrency.get("required_when") != "REMOTE_OR_AUTHORITY_MUTATION_USES_A_RESUMABLE_CHECKPOINT":
        fail("Receipt concurrency guard extension missing")
    required_concurrency = {
        "expected_checkpoint_sequence", "observed_checkpoint_sequence",
        "executor_id", "execution_lease_state", "lease_acquired_at", "guard_verdict",
    }
    if not required_concurrency.issubset(set(concurrency.get("fields", []))):
        fail("Receipt concurrency guard fields incomplete")
    if concurrency.get("sequence_mismatch_verdict") != "REVALIDATE_CONCURRENT_ADVANCE":
        fail("Receipt concurrency mismatch verdict invalid")
    if concurrency.get("lease_metadata_is_advisory_only") is not True:
        fail("Receipt lease metadata must remain advisory")

    idem = data.get("remote_mutation_idempotency_extension", {})
    required_idem = {
        "operation_fingerprint", "expected_postcondition", "outcome_state",
        "verification_surface", "retry_decision",
    }
    if not required_idem.issubset(set(idem.get("fields", []))):
        fail("Receipt idempotency fields incomplete")
    if idem.get("uncertain_outcome_action") != "VERIFY_POSTCONDITION_BEFORE_RETRY":
        fail("Receipt uncertain mutation action invalid")
    if idem.get("duplicate_side_effects_forbidden") is not True:
        fail("Receipt must forbid duplicate side effects")

    if data.get("closed_state_rule") != "IF_STATUS_IS_CLOSED_COMPLETION_GATE_MUST_BE_PASS_AND_INCOMPLETE_REQUIRED_PHASES_MUST_BE_EMPTY":
        fail("Receipt CLOSED state rule missing")
    return data


def validate_cases() -> None:
    rows = load_jsonl(CASES)
    if len(rows) < 24:
        fail("runtime regression corpus must have at least twenty-four cases")
    ids = {r.get("case_id") for r in rows}
    required = {
        "LOCK-001-NO-IMAGE-STICKY", "LOCK-002-NO-NEW-SKILL-STICKY",
        "FLOW-001-FULL-FLOW-NO-EARLY-CLOSE",
        "RESUME-005-CROSS-CHAT-FRONTIER-DISCOVERY",
        "RESUME-006-MULTIPLE-DISTINCT-FRONTIERS-HOLD",
        "FRONTIER-001-EXECUTABLE-LATEST-SEQUENCE",
        "FRONTIER-002-EXECUTABLE-AUTHORITY-MISMATCH",
        "CONCURRENCY-001-SEQUENCE-MATCH-PROCEED",
        "CONCURRENCY-002-SEQUENCE-MISMATCH-REVALIDATE",
        "CONCURRENCY-003-STALE-LEASE-NEWER-SEQUENCE-WINS",
        "IDEMPOTENCY-001-UNCERTAIN-POSTCONDITION-FOUND",
        "IDEMPOTENCY-002-UNCERTAIN-ABSENT-SAFE-RETRY",
        "IDEMPOTENCY-003-UNCERTAIN-ABSENT-UNSAFE-HOLD",
    }
    if not required.issubset(ids):
        fail(f"missing runtime cases {sorted(required - ids)}")
    by_id = {r["case_id"]: r for r in rows}

    c = by_id["FRONTIER-001-EXECUTABLE-LATEST-SEQUENCE"]
    result = resolve_continuation_frontier(
        c["candidate_frontiers"], c["request_keys"], c["current_authority_fingerprint"], True
    )
    if result["selected_frontier"] != c["expected_selected_frontier"]:
        fail("executable frontier resolver did not choose highest valid checkpoint sequence")

    c = by_id["FRONTIER-002-EXECUTABLE-AUTHORITY-MISMATCH"]
    result = resolve_continuation_frontier(
        c["candidate_frontiers"], c["request_keys"], c["current_authority_fingerprint"], True
    )
    if result["state"] != c["expected_state"] or result["action"] != c["expected_action"]:
        fail("executable frontier resolver must revalidate authority mismatch")

    c = by_id["RESUME-006-MULTIPLE-DISTINCT-FRONTIERS-HOLD"]
    result = resolve_continuation_frontier(
        c["candidate_frontiers"], {}, None, c["current_authority_identifies_one_active_task"]
    )
    if result["action"] != "HOLD_AMBIGUOUS_FRONTIER":
        fail("multiple distinct frontiers must hold rather than guess")

    c = by_id["CONCURRENCY-001-SEQUENCE-MATCH-PROCEED"]
    if guard_checkpoint_mutation(c["current_sequence"], c["expected_sequence"])["allowed"] is not True:
        fail("matching checkpoint sequence must proceed")

    c = by_id["CONCURRENCY-002-SEQUENCE-MISMATCH-REVALIDATE"]
    result = guard_checkpoint_mutation(c["current_sequence"], c["expected_sequence"])
    if result["state"] != "REVALIDATE_CONCURRENT_ADVANCE" or result["allowed"] is not False:
        fail("checkpoint sequence mismatch must block mutation and revalidate")

    c = by_id["CONCURRENCY-003-STALE-LEASE-NEWER-SEQUENCE-WINS"]
    if guard_checkpoint_mutation(c["current_sequence"], c["expected_sequence"])["allowed"] is not False:
        fail("newer checkpoint sequence must beat stale lease metadata")

    for case_id in [
        "IDEMPOTENCY-001-UNCERTAIN-POSTCONDITION-FOUND",
        "IDEMPOTENCY-002-UNCERTAIN-ABSENT-SAFE-RETRY",
        "IDEMPOTENCY-003-UNCERTAIN-ABSENT-UNSAFE-HOLD",
    ]:
        c = by_id[case_id]
        result = resolve_uncertain_mutation(
            c["outcome_state"], c["expected_postcondition_observed"],
            c["operation_is_idempotent_or_keyed"], c["retry_count"], c["retry_limit"]
        )
        if result["action"] != c["expected_action"]:
            fail(f"{case_id} idempotency decision mismatch")


def validate_new_receipts(contract: dict) -> int:
    legacy = set(contract.get("legacy_receipts_without_policy_1_1_fields", []))
    additional = contract.get("policy_1_1_additional_required_core_fields", [])
    constraint_fields = contract.get("constraint_lock_required_fields", [])
    flow_fields = contract.get("flow_completion_required_fields", [])
    phase_values = set(contract.get("phase_result_values", []))
    cp_fields = contract.get("continuation_checkpoint_extension", {}).get("fields", [])
    concurrency_fields = contract.get("concurrency_guard_extension", {}).get("fields", [])
    idem_fields = contract.get("remote_mutation_idempotency_extension", {}).get("fields", [])
    current_policy_count = 0

    for path in sorted(RECEIPT_DIR.glob("*.json")):
        r = load_json(path)
        rid = r.get("receipt_id")
        if rid in legacy:
            continue
        current_policy_count += 1
        require_present(r, additional, f"receipt:{rid}")
        require_present(r["constraint_lock"], constraint_fields, f"receipt:{rid}:constraint_lock")
        flow = r["flow_completion"]
        require_present(flow, flow_fields, f"receipt:{rid}:flow_completion")
        for phase, result in flow.get("phase_results", {}).items():
            if result not in phase_values:
                fail(f"receipt:{rid} invalid phase result {phase}={result}")
        if "continuation_checkpoint" in r:
            cp = r["continuation_checkpoint"]
            base_cp = [f for f in cp_fields if f not in {
                "expected_checkpoint_sequence", "executor_id", "execution_lease_state", "lease_acquired_at"
            }]
            require_present(cp, base_cp, f"receipt:{rid}:continuation_checkpoint")
            if not isinstance(cp.get("checkpoint_sequence"), int) or cp["checkpoint_sequence"] < 0:
                fail(f"receipt:{rid} checkpoint_sequence must be non-negative integer")
        if "concurrency_guard" in r:
            require_present(r["concurrency_guard"], concurrency_fields, f"receipt:{rid}:concurrency_guard")
        if "remote_mutation_idempotency" in r:
            require_present(r["remote_mutation_idempotency"], idem_fields, f"receipt:{rid}:remote_mutation_idempotency")
        if r.get("status") == "CLOSED":
            if flow.get("completion_gate") != "PASS" or flow.get("incomplete_required_phases"):
                fail(f"receipt:{rid} CLOSED requires completed flow")
    if current_policy_count < 1:
        fail("at least one policy-1.1 execution receipt is required to prove adoption")
    return current_policy_count


def main() -> None:
    validate_resolver()
    validate_tool_adapter_routing()
    contract = validate_receipt_contract()
    validate_cases()
    count = validate_new_receipts(contract)
    print("execution-lock validation: PASS")
    print("executable frontier resolution: ENFORCED")
    print("optimistic checkpoint concurrency: ENFORCED")
    print("verify-before-retry idempotency: ENFORCED")
    print("cross-context continuation / auto-advance / routing: ENFORCED")
    print("sticky constraints + flow completion: ENFORCED")
    print(f"policy-1.1 receipts: {count}")


if __name__ == "__main__":
    main()
