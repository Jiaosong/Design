#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
RECEIPT_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_RECEIPT_v1.0.json"
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


def validate_resolver() -> dict:
    data = load_json(RESOLVER)
    if data.get("version") != "1.2" or data.get("implementation_revision") != "1.2.4":
        fail("Current resolver must be v1.2 implementation revision 1.2.4")
    if data.get("status") != "ACTIVE_CURRENT":
        fail("Current resolver must remain ACTIVE_CURRENT")

    sticky = data.get("sticky_execution_constraints", {})
    if not sticky.get("required") or not sticky.get("resolve_before_owner_or_tool_selection"):
        fail("sticky execution constraints must be mandatory and pre-routing")
    required_rules = {
        "NO_IMAGE_GENERATION",
        "NO_NEW_SKILL",
        "NO_NEW_METHOD",
        "NO_NEW_FRAMEWORK",
        "USE_EXISTING_OLEANDER_METHODS_AND_SKILLS",
        "FULL_OLEANDER_FLOW_REQUIRED",
        "NO_PRODUCER_SELF_PROMOTION",
    }
    if not required_rules.issubset(set(sticky.get("normalized_rules", []))):
        fail("resolver sticky normalized rules incomplete")
    if sticky.get("generic_continue_does_not_revoke") is not True:
        fail("generic continue must not revoke constraints")
    if "ONLY_A_LATER_EXPLICIT_USER_INSTRUCTION" not in sticky.get("revocation_rule", ""):
        fail("constraint revocation must require later explicit user instruction")
    hard_effects = sticky.get("hard_effects", {})
    if "BLOCK_IMAGE_GENERATION_TOOLS" not in hard_effects.get("NO_IMAGE_GENERATION", ""):
        fail("NO_IMAGE_GENERATION must hard-block image generation tools")
    if "BLOCK_NEW_SKILL_CREATION" not in hard_effects.get("NO_NEW_SKILL", ""):
        fail("NO_NEW_SKILL must hard-block new Skill creation")

    continuation = data.get("continuation_checkpoint_policy", {})
    if continuation.get("generic_followup_same_task_default") != "RESUME_FROM_LAST_VERIFIED_CHECKPOINT":
        fail("same-task generic follow-up must resume from the last verified checkpoint")
    checkpoint_fields = {
        "checkpoint_state",
        "current_node",
        "last_verified_artifact",
        "resume_from",
        "next_allowed_action",
        "authority_fingerprint",
        "stale_reasons",
        "checkpoint_sequence",
        "checkpoint_updated_at",
    }
    if not checkpoint_fields.issubset(set(continuation.get("required_checkpoint_fields", []))):
        fail("continuation checkpoint fields incomplete")
    expected_states = {"RESUMABLE", "REVALIDATE", "BLOCKED", "CLOSED"}
    if not expected_states.issubset(set(continuation.get("checkpoint_states", []))):
        fail("continuation checkpoint states incomplete")
    revalidate_when = set(continuation.get("revalidate_when", []))
    if "AUTHORITY_FINGERPRINT_MISMATCH" not in revalidate_when or "PROJECT_OR_TASK_SWITCH" not in revalidate_when:
        fail("continuation checkpoint must revalidate on authority mismatch or task switch")
    if continuation.get("context_switch_or_compression_is_not_authority_change") is not True:
        fail("chat/context switch alone must not invalidate a verified checkpoint")
    if continuation.get("blind_repeat_completed_mutation_forbidden") is not True:
        fail("blind replay of completed mutation must be forbidden")
    if "SKIP_ALREADY_VERIFIED_COMPLETED_NODES" not in continuation.get("resume_behavior", ""):
        fail("resume behavior must skip already verified completed nodes")
    if continuation.get("cross_context_discovery_required_when") != "FOLLOWUP_OR_CONTINUATION_INTENT_WITHOUT_RELIABLE_LOCAL_TASK_POINTER":
        fail("cross-context frontier discovery trigger missing")
    discovery_sources = continuation.get("frontier_discovery_sources_in_order", [])
    expected_discovery_sources = [
        "EXPLICIT_CURRENT_REQUEST_PROJECT_TASK_OBJECT_KEYS",
        "CURRENT_PROJECT_STATE_OR_CURRENT_TASK_POINTER",
        "CURRENT_PROJECT_CONTROL_CARD",
        "ACTIVE_WORKING_OR_HOLD_EXECUTION_RECEIPTS",
    ]
    if discovery_sources != expected_discovery_sources:
        fail("frontier discovery source precedence drifted")
    match_keys = set(continuation.get("frontier_match_keys", []))
    if not {"PROJECT_ID_OR_SCOPE_ID", "LOGICAL_OBJECT_OR_CANONICAL_IDS", "AUTHORITY_FINGERPRINT"}.issubset(match_keys):
        fail("frontier discovery stable match keys incomplete")
    if continuation.get("chat_history_or_summary_is_not_checkpoint_authority") is not True:
        fail("chat history/summary must not become checkpoint authority")
    if "HOLD_AMBIGUOUS_FRONTIER" not in continuation.get("distinct_task_ambiguity_rule", ""):
        fail("multiple distinct frontiers must HOLD when Current cannot disambiguate")

    continuous = data.get("continuous_execution_policy", {})
    if continuous.get("purpose") != "AUTO_ADVANCE_READY_NODES_WITHIN_CURRENT_EXECUTION_TURN":
        fail("continuous execution policy missing")
    if continuous.get("no_artificial_one_node_stop") is not True:
        fail("continuous execution must forbid artificial one-node stop")
    if continuous.get("background_execution_forbidden") is not True:
        fail("continuous execution must not imply background work")
    advance_requires = set(continuous.get("advance_requires", []))
    required_advance = {
        "APPLICABLE_ACTUAL_READBACK_PASS_OR_TYPED_HANDOFF_ACCEPTED",
        "NEXT_NODE_READY",
        "AUTHORITY_FINGERPRINT_STILL_VALID",
        "SIDE_EFFECT_WITHIN_ALREADY_AUTHORIZED_CEILING",
        "NO_STOP_CONDITION",
    }
    if not required_advance.issubset(advance_requires):
        fail("continuous execution advance gates incomplete")
    stop_conditions = set(continuous.get("stop_conditions", []))
    required_stops = {
        "GENUINE_BLOCKER",
        "AUTHORITY_CONFLICT_OR_AMBIGUOUS_FRONTIER",
        "USER_DESIGN_OR_SCOPE_DECISION_REQUIRED",
        "IRREVERSIBLE_OR_HIGHER_SIDE_EFFECT_ACTION_NOT_ALREADY_AUTHORIZED",
        "FUTURE_CONDITION_OR_EXTERNAL_WAIT_REQUIRED",
        "TOOL_OR_RUNTIME_HARD_LIMIT",
    }
    if not required_stops.issubset(stop_conditions):
        fail("continuous execution stop conditions incomplete")
    if "NO_BLIND_RETRY_LOOP" not in continuous.get("failure_rule", ""):
        fail("continuous execution failure rule must forbid blind retry")

    flow = data.get("flow_completion_gate", {})
    if flow.get("does_not_mean_all_skills") is not True or flow.get("minimum_owner_set_still_applies") is not True:
        fail("full flow must not expand into all-Skill pipeline")
    phases = flow.get("phases", [])
    core = flow.get("core_phases_cannot_be_skipped_for_full_flow", [])
    required_phases = {
        "AUTHORITY_PREFLIGHT",
        "STICKY_CONSTRAINT_RESOLUTION",
        "EXISTING_KNOWLEDGE_METHOD_SKILL_RESOLUTION",
        "REQUIRED_NATIVE_OUTPUT_DEFINITION",
        "CAPABILITY_AND_MINIMUM_OWNER_SET",
        "REAL_EXECUTION",
        "ACTUAL_READBACK",
    }
    if not required_phases.issubset(set(phases)) or not required_phases.issubset(set(core)):
        fail("full-flow core phases incomplete")
    if "EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK" not in phases:
        fail("visual image-consumption phase missing")
    conditional = flow.get("conditional_required_phases", {})
    if conditional.get("EXISTING_VISUAL_AUTHORITY_AND_IMAGE_CONSUMPTION_CHECK") != "REQUIRED_WHEN_VISUAL_EXECUTION_BINDS_SEMANTIC_CONTENT_IMAGES":
        fail("visual image-consumption phase must be conditionally required")
    early = set(flow.get("early_stop_states_that_do_not_equal_completion", []))
    if not {"PR_OPENED", "CI_GREEN", "SELF_CHECK_PASS", "ARTIFACT_CREATED", "REGRESSION_PASS"}.issubset(early):
        fail("early-completion denylist incomplete")

    order = data.get("default_resolution_order", [])
    required_order = [
        "READ_APPLICABLE_PROJECT_STATE_SOURCE_AUTHORITY_CURRENT_TASK",
        "DISCOVER_ACTIVE_EXECUTION_FRONTIER_IF_CONTEXT_POINTER_MISSING",
        "RESOLVE_CONTINUATION_CHECKPOINT_IF_FOLLOWUP_INTENT",
        "REVALIDATE_AUTHORITY_IF_CHECKPOINT_REQUIRES",
        "RESOLVE_STICKY_EXECUTION_CONSTRAINTS",
        "ENFORCE_TOOL_OUTPUT_CREATION_AND_PROCESS_LOCKS",
        "VERIFY_REQUIRED_EXISTING_METHOD_AND_SKILL_FILES_WERE_ACTUALLY_READ",
        "RESOLVE_EXISTING_VISUAL_AUTHORITY_WHEN_VISUAL_OUTPUT_IS_REQUIRED",
        "LOOKUP_IMAGE_CONSUMPTION_REGISTER_BEFORE_CONTENT_IMAGE_BINDING",
        "BLOCK_DUPLICATE_SEMANTIC_IMAGE_OR_RESERVE_AVAILABLE_IMAGE",
        "DEFINE_REQUIRED_NATIVE_OUTPUT",
        "BUILD_APPLICABLE_FLOW_COMPLETION_CHECKLIST",
        "RESOLVE_EXECUTION_OWNER_MAP",
        "EXECUTE_ACTUAL_NATIVE_ARTIFACT",
        "ACTUAL_READBACK",
        "UPDATE_EXISTING_CONTINUATION_CHECKPOINT_AS_APPLICABLE",
        "AUTO_ADVANCE_READY_NODES_UNTIL_STOP_CONDITION",
        "VERIFY_FLOW_COMPLETION_GATE_BEFORE_CLOSURE_OR_COMPLETE_CLAIM",
        "EMIT_EXECUTION_RECEIPT",
    ]
    positions = []
    for token in required_order:
        if token not in order:
            fail(f"resolver order missing {token}")
        positions.append(order.index(token))
    if positions != sorted(positions):
        fail("constraint / frontier / continuation / auto-advance / image-consumption / full-flow resolver order is invalid")
    return data


def validate_receipt_contract() -> dict:
    data = load_json(RECEIPT_CONTRACT)
    if data.get("version") != "1.0" or data.get("policy_revision") != "1.1":
        fail("Execution Receipt must remain v1.0 policy revision 1.1")
    additional = set(data.get("policy_1_1_additional_required_core_fields", []))
    if additional != {"constraint_lock", "flow_completion"}:
        fail("policy 1.1 must add exactly constraint_lock and flow_completion")
    legacy = set(data.get("legacy_receipts_without_policy_1_1_fields", []))
    expected_legacy = {
        "EXR-20260818-PR246-IMAGE-OPS-ADAPTER",
        "EXR-20260818-PR248-CONTRACT-LAYER",
        "EXR-20260818-SKILL-RUNTIME-CLOSURE-v1.2",
    }
    if legacy != expected_legacy:
        fail("legacy Receipt allowlist must be explicit and exact")
    if data.get("closed_state_rule") != "IF_STATUS_IS_CLOSED_COMPLETION_GATE_MUST_BE_PASS_AND_INCOMPLETE_REQUIRED_PHASES_MUST_BE_EMPTY":
        fail("Receipt CLOSED state rule missing")

    image_ext = data.get("image_consumption_extension", {})
    if image_ext.get("required_when") != "VISUAL_EXECUTION_BINDS_SEMANTIC_CONTENT_IMAGE":
        fail("Receipt image-consumption extension missing or invalid")
    required_image_fields = {
        "register_path_or_authority",
        "lookup_performed",
        "reservations_or_consumptions",
        "conflicts",
        "blocked_assets",
        "release_actions",
        "verdict",
    }
    if not required_image_fields.issubset(set(image_ext.get("fields", []))):
        fail("Receipt image-consumption fields incomplete")

    checkpoint_ext = data.get("continuation_checkpoint_extension", {})
    if checkpoint_ext.get("required_when") != "SAME_TASK_EXECUTION_EXPECTED_TO_CONTINUE_ACROSS_TURNS_OR_HANDOFFS_AND_STATUS_IS_WORKING_OR_HOLD":
        fail("Receipt continuation checkpoint extension missing or invalid")
    required_checkpoint_fields = {
        "checkpoint_state",
        "current_node",
        "last_verified_artifact",
        "resume_from",
        "next_allowed_action",
        "authority_fingerprint",
        "stale_reasons",
        "checkpoint_sequence",
        "checkpoint_updated_at",
    }
    if not required_checkpoint_fields.issubset(set(checkpoint_ext.get("fields", []))):
        fail("Receipt continuation checkpoint fields incomplete")
    discovery_record_fields = {
        "discovery_trigger",
        "project_or_scope_key",
        "task_key",
        "object_or_canonical_ids",
        "candidate_frontiers",
        "selected_frontier",
        "selection_basis",
        "ambiguity_state",
    }
    if not discovery_record_fields.issubset(set(checkpoint_ext.get("frontier_discovery_record_fields", []))):
        fail("Receipt cross-context frontier discovery record fields incomplete")
    if checkpoint_ext.get("generic_continue_action") != "RESUME_NEXT_ALLOWED_ACTION_NOT_REPLAN_FROM_ZERO":
        fail("Receipt continuation rule must resume the next allowed action")
    if checkpoint_ext.get("context_switch_or_compression_is_not_authority_change") is not True:
        fail("Receipt checkpoint must survive context switch/compression when authority is unchanged")
    if checkpoint_ext.get("chat_history_or_summary_is_not_checkpoint_authority") is not True:
        fail("Receipt must not treat chat history/summary as checkpoint authority")
    if checkpoint_ext.get("checkpoint_is_runtime_state_not_project_state") is not True:
        fail("Receipt checkpoint must not become a second Project State")
    if checkpoint_ext.get("no_material_delta_no_new_receipt") is not True:
        fail("no-delta chat turn must not create a new receipt only for checkpointing")

    continuous_ext = data.get("continuous_execution_extension", {})
    required_continuous_fields = {
        "auto_advance_enabled",
        "nodes_executed_in_order",
        "node_readback_verdicts",
        "stop_reason",
        "final_current_node",
        "next_allowed_action",
    }
    if not required_continuous_fields.issubset(set(continuous_ext.get("fields", []))):
        fail("Receipt continuous-execution fields incomplete")
    if continuous_ext.get("auto_advance_requires_readback_between_dependent_mutations") is not True:
        fail("Receipt auto-advance must require readback between dependent mutations")
    if continuous_ext.get("background_execution_forbidden") is not True:
        fail("Receipt auto-advance must not imply background execution")

    route_ext = data.get("adapter_route_decision_extension", {})
    required_route_fields = {
        "required_capability_roles",
        "candidate_surfaces",
        "selected_surface",
        "selection_reasons",
        "availability_state",
        "authority_ceiling",
        "side_effect_class",
        "readback_surface",
        "fallback_surface",
    }
    if not required_route_fields.issubset(set(route_ext.get("fields", []))):
        fail("Receipt adapter route decision fields incomplete")
    if route_ext.get("vendor_name_is_not_selection_reason") is not True:
        fail("Receipt route decision must not select by vendor name")
    if route_ext.get("selected_surface_does_not_gain_authority") is not True:
        fail("selected adapter surface must not gain authority")
    return data


def validate_cases() -> None:
    rows = load_jsonl(CASES)
    if len(rows) < 14:
        fail("sticky/full-flow/continuation/auto-advance regression corpus must have at least fourteen cases")
    ids = {r.get("case_id") for r in rows}
    required = {
        "LOCK-001-NO-IMAGE-STICKY",
        "LOCK-002-NO-NEW-SKILL-STICKY",
        "LOCK-003-EXPLICIT-REVOCATION-ONLY",
        "FLOW-001-FULL-FLOW-NO-EARLY-CLOSE",
        "FLOW-002-FULL-FLOW-MINIMUM-OWNERS",
        "FLOW-003-EXISTING-SKILL-READBACK",
        "RESUME-001-CONTINUE-LAST-VERIFIED-CHECKPOINT",
        "RESUME-002-AUTHORITY-STALE-REVALIDATE",
        "RESUME-003-BLOCKED-NO-BLIND-RETRY",
        "RESUME-004-CONTEXT-SWITCH-NOT-AUTHORITY-RESET",
        "RESUME-005-CROSS-CHAT-FRONTIER-DISCOVERY",
        "RESUME-006-MULTIPLE-DISTINCT-FRONTIERS-HOLD",
        "LOOP-001-AUTO-ADVANCE-READY-NODES",
        "LOOP-002-STOP-ON-SIDE-EFFECT-ESCALATION",
    }
    if not required.issubset(ids):
        fail(f"missing runtime cases {sorted(required - ids)}")
    by_id = {r["case_id"]: r for r in rows}
    if "NO_IMAGE_GENERATION" not in by_id["LOCK-001-NO-IMAGE-STICKY"].get("expected_active_constraints", []):
        fail("no-image sticky case does not preserve lock")
    if "CREATE_NEW_SKILL" not in by_id["LOCK-002-NO-NEW-SKILL-STICKY"].get("forbidden_actions", []):
        fail("no-new-skill case must block creation")
    if by_id["FLOW-001-FULL-FLOW-NO-EARLY-CLOSE"].get("expected_completion_gate") != "HOLD":
        fail("PR/CI early close case must HOLD")
    if "AUTOMATICALLY_RUN_MOTION" not in by_id["FLOW-002-FULL-FLOW-MINIMUM-OWNERS"].get("forbidden_actions", []):
        fail("full-flow minimum-owner case must forbid unnecessary Motion")
    if by_id["RESUME-001-CONTINUE-LAST-VERIFIED-CHECKPOINT"].get("expected_action") != "EXECUTE_NEXT_ALLOWED_ACTION":
        fail("same-task continue case must execute the next allowed action")
    if "EXECUTE_FROM_STALE_CHECKPOINT" not in by_id["RESUME-002-AUTHORITY-STALE-REVALIDATE"].get("forbidden_actions", []):
        fail("stale-authority case must block execution from stale checkpoint")
    if "REPEAT_FAILED_MUTATION_WITHOUT_NEW_EVIDENCE" not in by_id["RESUME-003-BLOCKED-NO-BLIND-RETRY"].get("forbidden_actions", []):
        fail("blocked checkpoint case must forbid blind retry")
    if by_id["RESUME-004-CONTEXT-SWITCH-NOT-AUTHORITY-RESET"].get("expected_checkpoint_state") != "RESUMABLE":
        fail("context-switch case must preserve resumable checkpoint when authority is unchanged")
    if by_id["RESUME-005-CROSS-CHAT-FRONTIER-DISCOVERY"].get("expected_selected_frontier") != "TASK-W03-CURRENT":
        fail("cross-chat discovery case must select the latest authority-matching frontier")
    if by_id["RESUME-006-MULTIPLE-DISTINCT-FRONTIERS-HOLD"].get("expected_action") != "HOLD_AMBIGUOUS_FRONTIER":
        fail("multiple distinct frontiers must hold rather than guess")
    loop1 = by_id["LOOP-001-AUTO-ADVANCE-READY-NODES"]
    if len(loop1.get("expected_nodes_executed_in_order", [])) < 4:
        fail("auto-advance case must prove more than one ready node continues")
    if "STOP_AFTER_FIRST_NODE_WITHOUT_REASON" not in loop1.get("forbidden_actions", []):
        fail("auto-advance case must forbid artificial one-node stop")
    if by_id["LOOP-002-STOP-ON-SIDE-EFFECT-ESCALATION"].get("expected_stop_reason") != "SIDE_EFFECT_ESCALATION_NOT_AUTHORIZED":
        fail("auto-advance must stop on unauthorized side-effect escalation")


def validate_new_receipts(contract: dict) -> int:
    legacy = set(contract.get("legacy_receipts_without_policy_1_1_fields", []))
    additional = contract.get("policy_1_1_additional_required_core_fields", [])
    constraint_fields = contract.get("constraint_lock_required_fields", [])
    flow_fields = contract.get("flow_completion_required_fields", [])
    constraint_record_fields = contract.get("constraint_record_required_fields", [])
    phase_values = set(contract.get("phase_result_values", []))
    checkpoint_fields = contract.get("continuation_checkpoint_extension", {}).get("fields", [])
    continuous_fields = contract.get("continuous_execution_extension", {}).get("fields", [])
    route_fields = contract.get("adapter_route_decision_extension", {}).get("fields", [])
    current_policy_count = 0

    for path in sorted(RECEIPT_DIR.glob("*.json")):
        r = load_json(path)
        rid = r.get("receipt_id")
        if rid in legacy:
            continue
        current_policy_count += 1
        require_present(r, additional, f"receipt:{rid}")
        lock = r["constraint_lock"]
        require_present(lock, constraint_fields, f"receipt:{rid}:constraint_lock")
        for item in lock.get("active_constraints", []):
            require_present(item, constraint_record_fields, f"receipt:{rid}:constraint")
        flow = r["flow_completion"]
        require_present(flow, flow_fields, f"receipt:{rid}:flow_completion")
        for phase, result in flow.get("phase_results", {}).items():
            if result not in phase_values:
                fail(f"receipt:{rid} invalid phase result {phase}={result}")
        if "continuation_checkpoint" in r:
            cp = r["continuation_checkpoint"]
            require_present(cp, checkpoint_fields, f"receipt:{rid}:continuation_checkpoint")
            if not isinstance(cp.get("checkpoint_sequence"), int) or cp["checkpoint_sequence"] < 0:
                fail(f"receipt:{rid} checkpoint_sequence must be non-negative integer")
        if "continuous_execution" in r:
            require_present(r["continuous_execution"], continuous_fields, f"receipt:{rid}:continuous_execution")
        if "adapter_route_decision" in r:
            require_present(r["adapter_route_decision"], route_fields, f"receipt:{rid}:adapter_route_decision")
        if r.get("status") == "CLOSED":
            if flow.get("completion_gate") != "PASS":
                fail(f"receipt:{rid} CLOSED requires completion_gate PASS")
            if flow.get("incomplete_required_phases"):
                fail(f"receipt:{rid} CLOSED cannot have incomplete required phases")
            if flow.get("completion_claim_allowed") is not True:
                fail(f"receipt:{rid} CLOSED requires completion_claim_allowed=true")
    if current_policy_count < 1:
        fail("at least one policy-1.1 execution receipt is required to prove adoption")
    return current_policy_count


def main() -> None:
    validate_resolver()
    contract = validate_receipt_contract()
    validate_cases()
    count = validate_new_receipts(contract)
    print("execution-lock validation: PASS")
    print("sticky negative constraints: ENFORCED")
    print("cross-context frontier discovery / continuation checkpoint: ENFORCED")
    print("continuous ready-node auto-advance with bounded stop conditions: ENFORCED")
    print("existing visual authority + image-consumption phase: ENFORCED")
    print("full-flow completion gate: ENFORCED")
    print(f"policy-1.1 receipts: {count}")


if __name__ == "__main__":
    main()
