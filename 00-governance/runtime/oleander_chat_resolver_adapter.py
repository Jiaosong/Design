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
ADAPTER_REVISION = "1.1"
ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_CONTRACT = ROOT / "00-governance" / "runtime" / "OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.json"
CLOSURE_INTENTS = {"COMPLETE", "CLOSE", "KEEP", "FINALIZE", "PROMOTE_KEEP", "STOP_COMPLETE"}
STRUCTURAL_EVIDENCE_CLASSES = {
    "STRUCTURE_COUNT",
    "PERSISTENCE_COUNT",
    "REACTION_COUNT",
    "PAGE_COUNT",
    "OBJECT_COUNT",
    "HASH_ONLY",
    "CI_GREEN",
    "RENDER_EXISTS",
    "FILE_EXISTS",
    "NODE_DESTINATION_EXISTS",
}
STRUCTURAL_DIMENSIONS = {
    "STRUCTURE_PERSISTENCE",
    "DELIVERY_INTEGRITY",
    "RUNTIME_INTEGRITY",
    "GEOMETRY_READBACK",
}


def _load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return data


def _owner_contract_map() -> dict[str, dict]:
    contract = _load_json(CAPABILITY_CONTRACT)
    owners = contract.get("owners") or []
    return {str(owner.get("skill_id")): owner for owner in owners if isinstance(owner, dict) and owner.get("skill_id")}


def _closure_requested(payload: dict, flow_completion: dict | None) -> bool:
    intent = str(payload.get("intent") or "").strip().upper()
    if bool(payload.get("completion_claim_requested")):
        return True
    if intent in CLOSURE_INTENTS:
        return True
    if flow_completion and flow_completion.get("completion_gate") == "PASS":
        return True
    return False


def evaluate_skill_consumption(evidence: dict | None, *, closure_requested: bool) -> dict | None:
    """Fail closed at closure unless the Current canonical Skill implementations were actually read."""
    if evidence is None:
        if not closure_requested:
            return None
        return {
            "gate": "HOLD",
            "action": "HOLD_SKILL_CONSUMPTION_EVIDENCE_REQUIRED",
            "missing_owner_ids": [],
            "missing_canonical_reads": [],
            "reason": "CLOSURE_REQUIRES_SKILL_CONSUMPTION_EVIDENCE",
        }

    required_owner_ids = [str(x) for x in evidence.get("required_owner_ids") or []]
    resolution_state = str(evidence.get("resolution_state") or "")
    if not required_owner_ids:
        if resolution_state in {"NO_DEDICATED_OWNER", "NO_SKILL_REQUIRED"}:
            return {
                "gate": "PASS",
                "action": "SKILL_CONSUMPTION_NOT_APPLICABLE_WITH_EXPLICIT_RESOLUTION",
                "required_owner_ids": [],
                "resolved_owners": [],
            }
        return {
            "gate": "HOLD",
            "action": "HOLD_SKILL_CONSUMPTION",
            "missing_owner_ids": [],
            "missing_canonical_reads": [],
            "reason": "OWNER_SET_OR_EXPLICIT_NO_OWNER_RESOLUTION_REQUIRED",
        }

    owners = _owner_contract_map()
    actual_read_paths = {str(path) for path in evidence.get("actual_read_paths") or []}
    claimed_states = {
        str(k): str(v)
        for k, v in dict(evidence.get("claimed_lifecycle_states") or {}).items()
    }
    missing_owner_ids: list[str] = []
    missing_canonical_reads: list[dict] = []
    lifecycle_mismatches: list[dict] = []
    resolved_owners: list[dict] = []

    for owner_id in required_owner_ids:
        owner = owners.get(owner_id)
        if owner is None:
            missing_owner_ids.append(owner_id)
            continue
        implementation_paths = [str(path) for path in owner.get("implementation_paths") or []]
        skill_paths = [path for path in implementation_paths if path.endswith("/SKILL.md")]
        canonical_read_paths = skill_paths or implementation_paths
        matched_reads = sorted(set(canonical_read_paths).intersection(actual_read_paths))
        if not matched_reads:
            missing_canonical_reads.append({
                "owner_id": owner_id,
                "expected_one_of": canonical_read_paths,
            })
        claimed = claimed_states.get(owner_id)
        actual_state = str(owner.get("lifecycle_state") or "")
        if claimed and claimed != actual_state:
            lifecycle_mismatches.append({
                "owner_id": owner_id,
                "claimed": claimed,
                "current": actual_state,
            })
        resolved_owners.append({
            "owner_id": owner_id,
            "lifecycle_state": actual_state,
            "routing_state": owner.get("routing_state"),
            "canonical_read_paths": matched_reads,
            "candidate_boundary": actual_state == "CANDIDATE",
        })

    if missing_owner_ids or lifecycle_mismatches:
        return {
            "gate": "FAIL",
            "action": "REVISE_SKILL_CONSUMPTION",
            "required_owner_ids": required_owner_ids,
            "resolved_owners": resolved_owners,
            "missing_owner_ids": missing_owner_ids,
            "missing_canonical_reads": missing_canonical_reads,
            "lifecycle_mismatches": lifecycle_mismatches,
            "reason": "CURRENT_OWNER_IDENTITY_OR_LIFECYCLE_MISMATCH",
        }
    if missing_canonical_reads:
        return {
            "gate": "HOLD",
            "action": "HOLD_SKILL_CONSUMPTION",
            "required_owner_ids": required_owner_ids,
            "resolved_owners": resolved_owners,
            "missing_owner_ids": [],
            "missing_canonical_reads": missing_canonical_reads,
            "lifecycle_mismatches": [],
            "reason": "CURRENT_CANONICAL_SKILL_NOT_ACTUALLY_READ",
        }
    return {
        "gate": "PASS",
        "action": "SKILL_CONSUMPTION_VERIFIED",
        "required_owner_ids": required_owner_ids,
        "resolved_owners": resolved_owners,
        "missing_owner_ids": [],
        "missing_canonical_reads": [],
        "lifecycle_mismatches": [],
        "does_not_prove": ["SKILL_PROMOTION", "DESIGN_QUALITY", "FINAL_KEEP"],
    }


def _quality_record(value) -> tuple[str, list[str], str | None]:
    if isinstance(value, str):
        return value, [], None
    if not isinstance(value, dict):
        return "", [], None
    evidence_classes = value.get("evidence_classes")
    if evidence_classes is None and value.get("evidence_class") is not None:
        evidence_classes = [value.get("evidence_class")]
    return (
        str(value.get("result") or ""),
        [str(x) for x in (evidence_classes or [])],
        str(value.get("reason")) if value.get("reason") else None,
    )


def evaluate_quality_acceptance(evidence: dict | None, *, closure_requested: bool) -> dict | None:
    """Separate professional quality from structure/persistence/readback existence evidence."""
    if evidence is None:
        if not closure_requested:
            return None
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE_EVIDENCE_REQUIRED",
            "reason": "CLOSURE_REQUIRES_EXPLICIT_QUALITY_ACCEPTANCE_OR_NOT_APPLICABLE_REASON",
        }

    if evidence.get("applicable") is False:
        reason = str(evidence.get("not_applicable_reason") or "").strip()
        if reason:
            return {
                "gate": "PASS",
                "action": "QUALITY_ACCEPTANCE_NOT_APPLICABLE",
                "not_applicable_reason": reason,
            }
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE",
            "reason": "NOT_APPLICABLE_REQUIRES_REASON",
        }

    required_dimensions = [str(x) for x in evidence.get("required_dimensions") or []]
    gate_results = dict(evidence.get("gate_results") or {})
    if not required_dimensions:
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE",
            "reason": "TASK_DERIVED_REQUIRED_QUALITY_DIMENSIONS_MISSING",
            "incomplete_dimensions": [],
        }

    incomplete_dimensions: list[str] = []
    failed_dimensions: list[str] = []
    weak_evidence_dimensions: list[str] = []
    not_applicable_without_reason: list[str] = []
    normalized_results: dict[str, dict] = {}

    for dimension in required_dimensions:
        result, evidence_classes, reason = _quality_record(gate_results.get(dimension))
        normalized_results[dimension] = {
            "result": result,
            "evidence_classes": evidence_classes,
            "reason": reason,
        }
        if result == "FAIL":
            failed_dimensions.append(dimension)
            continue
        if result in {"", "HOLD"}:
            incomplete_dimensions.append(dimension)
            continue
        if result == "NOT_APPLICABLE":
            if not reason:
                not_applicable_without_reason.append(dimension)
            continue
        if result != "PASS":
            incomplete_dimensions.append(dimension)
            continue
        if not evidence_classes:
            incomplete_dimensions.append(dimension)
            continue
        if dimension not in STRUCTURAL_DIMENSIONS and set(evidence_classes).issubset(STRUCTURAL_EVIDENCE_CLASSES):
            weak_evidence_dimensions.append(dimension)

    professional_dimensions = [d for d in required_dimensions if d not in STRUCTURAL_DIMENSIONS]
    scope_coverage_confirmed = evidence.get("scope_coverage_confirmed") is True
    independent_review_required = bool(evidence.get("independent_review_required", False)) or bool(professional_dimensions)
    review = evidence.get("independent_review") if isinstance(evidence.get("independent_review"), dict) else {}
    reviewer_role = str(review.get("reviewer_role") or "").upper()
    review_verdict = str(review.get("verdict") or "").upper()
    producer_self_promotion = bool(evidence.get("producer_self_promotion")) or reviewer_role in {
        "PRODUCER",
        "SAME_EXECUTOR",
        "SELF",
    }
    independent_review_missing = independent_review_required and (
        review_verdict != "PASS" or not reviewer_role or producer_self_promotion
    )

    if producer_self_promotion or failed_dimensions:
        return {
            "gate": "FAIL",
            "action": "REVISE_QUALITY_ACCEPTANCE",
            "required_dimensions": required_dimensions,
            "gate_results": normalized_results,
            "failed_dimensions": failed_dimensions,
            "incomplete_dimensions": incomplete_dimensions,
            "weak_evidence_dimensions": weak_evidence_dimensions,
            "not_applicable_without_reason": not_applicable_without_reason,
            "scope_coverage_confirmed": scope_coverage_confirmed,
            "independent_review_missing": independent_review_missing,
            "producer_self_promotion": producer_self_promotion,
            "reason": "PROFESSIONAL_QUALITY_FAIL_OR_SELF_PROMOTION",
        }

    if (
        incomplete_dimensions
        or weak_evidence_dimensions
        or not_applicable_without_reason
        or not scope_coverage_confirmed
        or independent_review_missing
    ):
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE",
            "required_dimensions": required_dimensions,
            "gate_results": normalized_results,
            "failed_dimensions": [],
            "incomplete_dimensions": incomplete_dimensions,
            "weak_evidence_dimensions": weak_evidence_dimensions,
            "not_applicable_without_reason": not_applicable_without_reason,
            "scope_coverage_confirmed": scope_coverage_confirmed,
            "independent_review_missing": independent_review_missing,
            "producer_self_promotion": False,
            "reason": "PROFESSIONAL_QUALITY_EVIDENCE_INCOMPLETE_OR_SCOPE_TOO_NARROW",
        }

    return {
        "gate": "PASS",
        "action": "QUALITY_ACCEPTANCE_VERIFIED",
        "required_dimensions": required_dimensions,
        "gate_results": normalized_results,
        "scope_coverage_confirmed": True,
        "independent_review_missing": False,
        "producer_self_promotion": False,
        "does_not_prove": ["FIELD_TRUTH", "ENGINEERING_APPROVAL", "HUMAN_TEST_PASS_UNLESS_EXPLICITLY_GATED"],
    }


def _directive(
    *,
    frontier: dict | None,
    checkpoint_resume: dict | None,
    mutation_guard: dict | None,
    skill_consumption: dict | None,
    quality_acceptance: dict | None,
    flow_completion: dict | None,
    auto_advance: dict | None,
) -> dict:
    """Compile existing Resolver decisions into a transient conversation directive."""
    if checkpoint_resume and checkpoint_resume.get("action") == "DO_NOT_REOPEN_CLOSED_TASK":
        return {"action": "STOP_CLOSED_TASK", "target": None, "basis": "CONTINUATION_CHECKPOINT"}

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

    if skill_consumption and skill_consumption.get("gate") != "PASS":
        return {
            "action": skill_consumption.get("action", "HOLD_SKILL_CONSUMPTION"),
            "target": None,
            "basis": "SKILL_CONSUMPTION_GATE",
        }

    if quality_acceptance and quality_acceptance.get("gate") != "PASS":
        return {
            "action": quality_acceptance.get("action", "HOLD_QUALITY_ACCEPTANCE"),
            "target": None,
            "basis": "PROFESSIONAL_QUALITY_ACCEPTANCE_GATE",
        }

    if flow_completion and flow_completion.get("completion_gate") == "PASS":
        return {"action": "STOP_FLOW_COMPLETION_GATE_PASS", "target": None, "basis": "FLOW_COMPLETION_GATE"}

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
        "adapter_revision": ADAPTER_REVISION,
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

    closure_requested = _closure_requested(payload, flow_completion)
    skill_consumption = evaluate_skill_consumption(
        dict(payload.get("skill_consumption")) if isinstance(payload.get("skill_consumption"), dict) else None,
        closure_requested=closure_requested,
    )
    quality_acceptance = evaluate_quality_acceptance(
        dict(payload.get("quality_acceptance")) if isinstance(payload.get("quality_acceptance"), dict) else None,
        closure_requested=closure_requested,
    )

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
        skill_consumption=skill_consumption,
        quality_acceptance=quality_acceptance,
        flow_completion=flow_completion,
        auto_advance=auto_advance,
    )

    return {
        "adapter": identity,
        "intent": payload.get("intent"),
        "closure_requested": closure_requested,
        "frontier": frontier,
        "checkpoint_resume": checkpoint_resume,
        "constraint_lock": constraint_lock,
        "mutation_guard": mutation_guard,
        "skill_consumption": skill_consumption,
        "quality_acceptance": quality_acceptance,
        "flow_completion": flow_completion,
        "auto_advance": auto_advance,
        "conversation_directive": directive,
        "does_not_prove": [
            "PROJECT_STATE",
            "DESIGN_QUALITY_WITHOUT_QUALITY_ACCEPTANCE_GATE",
            "ARTIFACT_CORRECTNESS",
            "COMPLETION_WITHOUT_FLOW_AND_ACCEPTANCE_EVIDENCE",
            "STRUCTURE_OR_PERSISTENCE_PASS_IS_PROFESSIONAL_KEEP",
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
    acceptance = _load_jsonl(ROOT / "evals" / "runtime" / "design_acceptance_guard.jsonl")

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

    for case_id in sorted(acceptance):
        case = acceptance[case_id]
        result = run_preflight(case["payload"])
        checks.append((case_id, result["conversation_directive"]["action"] == case["expected_action"]))

    failed = [case_id for case_id, passed in checks if not passed]
    if failed:
        raise RuntimeError(f"adapter self-test failed: {failed}")
    return {"status": "PASS", "adapter_id": ADAPTER_ID, "adapter_revision": ADAPTER_REVISION, "cases": [case_id for case_id, _ in checks]}


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
