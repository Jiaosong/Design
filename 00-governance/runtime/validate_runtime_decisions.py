#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
TOOL_CONTRACT = RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json"
REGRESSION_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1.json"
CASES = ROOT / "evals" / "runtime" / "sticky_constraints_and_flow.jsonl"
P2_CASES = ROOT / "evals" / "runtime" / "known_failure_and_reliability.jsonl"


def fail(msg: str) -> None:
    raise SystemExit(f"runtime-decision validation failed: {msg}")


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


def decide_authority_snapshot(
    snapshot: dict | None,
    current_authority_fingerprint: str,
    current_github_head_sha: str | None,
    current_constraint_hash: str | None,
) -> dict:
    """Reuse a verified pointer snapshot only while its drift-sensitive inputs still match."""
    if not snapshot or snapshot.get("verified") is not True:
        return {"action": "REFRESH_AUTHORITY_SNAPSHOT", "reason": "MISSING_OR_UNVERIFIED"}
    if snapshot.get("authority_fingerprint") != current_authority_fingerprint:
        return {"action": "REFRESH_AUTHORITY_SNAPSHOT", "reason": "AUTHORITY_FINGERPRINT_CHANGED"}
    if current_github_head_sha is not None and snapshot.get("github_head_sha") != current_github_head_sha:
        return {"action": "REFRESH_AUTHORITY_SNAPSHOT", "reason": "GITHUB_HEAD_CHANGED"}
    if current_constraint_hash is not None and snapshot.get("active_constraint_hash") != current_constraint_hash:
        return {"action": "REFRESH_AUTHORITY_SNAPSHOT", "reason": "ACTIVE_CONSTRAINTS_CHANGED"}
    return {"action": "REUSE_VERIFIED_AUTHORITY_SNAPSHOT", "reason": "DRIFT_INPUTS_MATCH"}


def plan_selective_readback(
    mutation_domain: str,
    blast_radius_known: bool,
    cross_platform_pointer_changed: bool = False,
) -> dict:
    """Compile existing mutation-blast-radius policy into a bounded readback plan."""
    if cross_platform_pointer_changed or mutation_domain in {"AUTHORITY", "CROSS_PLATFORM_POINTER"}:
        return {
            "action": "AUTHORITY_AND_DRIFT_READBACK_REQUIRED",
            "scope": ["AUTHORITY_CARRIER", "CROSS_PLATFORM_POINTERS", "DRIFT_CHECK"],
        }
    if not blast_radius_known:
        return {"action": "WIDEN_READBACK", "scope": ["AFFECTED_FRONTIER_AND_DEPENDENCIES"]}
    plans = {
        "PRESENTATION_WEB": ["AFFECTED_PAGE_OR_COMPONENT", "RELEVANT_RESPONSIVE_RUNTIME_STATE"],
        "CODE_RUNTIME": ["AFFECTED_EXECUTION_PATH", "APPLICABLE_TESTS_OR_RUNTIME_READBACK"],
        "THREE_D_OBJECT": ["AFFECTED_OBJECT", "DEPENDENCIES", "GEOMETRY_VIEWPORT_RENDER_AS_APPLICABLE"],
    }
    return {
        "action": "SMALLEST_SUFFICIENT_ACTUAL_READBACK",
        "scope": plans.get(mutation_domain, ["BOUNDED_MUTATION_SCOPE", "AFFECTED_DEPENDENCIES"]),
    }


def decide_heavy_executor(
    *,
    lighter_adapter_sufficient: bool,
    frequent_design_judgment: bool,
    small_step_continuation: bool,
    validation_dominates: bool,
    long_low_judgment_repetitive: bool,
    substantial_cross_app_navigation: bool,
    gui_bound_unavailable_to_connectors: bool,
    large_bounded_batch: bool,
) -> dict:
    """Compile the existing escalation-only policy without vendor-specific thresholds."""
    if lighter_adapter_sufficient:
        return {"action": "USE_LIGHTER_CURRENT_ADAPTER", "output_ceiling": "NORMAL_OLEANDER_FLOW"}
    if frequent_design_judgment or small_step_continuation or validation_dominates:
        return {"action": "DO_NOT_ESCALATE_HEAVY_EXECUTOR", "output_ceiling": "NORMAL_OLEANDER_FLOW"}
    eligible = any(
        [
            long_low_judgment_repetitive,
            substantial_cross_app_navigation,
            gui_bound_unavailable_to_connectors,
            large_bounded_batch,
        ]
    )
    if eligible:
        return {"action": "HEAVY_EXECUTOR_ELIGIBLE", "output_ceiling": "EXECUTED"}
    return {"action": "USE_LIGHTER_ADAPTER_OR_HOLD", "output_ceiling": "NORMAL_OLEANDER_FLOW"}


def decide_known_failure(
    *,
    current_failure_signature: str,
    current_applicability: str,
    materially_new_context: bool,
    prior_repair_applied: bool,
    known_failure_records: list[dict],
) -> dict:
    """Reuse a bounded transferable repair path; do not turn every recurrence into new research."""
    required = {
        "failure_signature",
        "root_cause_class",
        "affected_layer",
        "repair_rule",
        "regression_test",
        "applicability",
    }
    matches: list[dict] = []
    for record in known_failure_records:
        if not required.issubset(record):
            continue
        applicability = record.get("applicability") or []
        if isinstance(applicability, str):
            applicability = [applicability]
        if record.get("failure_signature") != current_failure_signature:
            continue
        if current_applicability not in applicability and "*" not in applicability:
            continue
        matches.append(record)

    if not matches:
        return {"state": "NO_KNOWN_FAILURE_MATCH", "action": "USE_NORMAL_ROOT_CAUSE_ANALYSIS"}

    distinct_paths = {
        (m["root_cause_class"], m["repair_rule"], m["regression_test"])
        for m in matches
    }
    if len(distinct_paths) > 1:
        return {"state": "HOLD", "action": "HOLD_AMBIGUOUS_KNOWN_FAILURE"}

    record = matches[0]
    if materially_new_context:
        return {
            "state": "MATERIALLY_NEW_CONTEXT",
            "action": "RECLASSIFY_ROOT_CAUSE_OR_RESEARCH_AS_NEEDED",
            "repair_rule": record["repair_rule"],
            "regression_test": record["regression_test"],
        }
    if prior_repair_applied:
        return {
            "state": "EXECUTION_DRIFT",
            "code": "KNOWN_FAILURE_RECURRED",
            "action": "BLOCK_KNOWN_INVALID_PATH_REAPPLY_REPAIR_RULE_AND_RUN_REGRESSION",
            "repair_rule": record["repair_rule"],
            "regression_test": record["regression_test"],
        }
    return {
        "state": "KNOWN_FAILURE_MATCH",
        "action": "APPLY_EXISTING_REPAIR_RULE_AND_REQUIRED_REGRESSION_TEST",
        "repair_rule": record["repair_rule"],
        "regression_test": record["regression_test"],
    }


def classify_surface_reliability(candidate: dict) -> str:
    """Classify only after authority/capability/side-effect routing has produced candidates."""
    if candidate.get("supports_required_operation") is not True:
        return "BLOCKED_UNSUPPORTED"
    availability = candidate.get("availability_state", "UNKNOWN")
    if availability == "UNAVAILABLE":
        return "BLOCKED_UNAVAILABLE"
    if availability not in {"AVAILABLE", "DEGRADED", "UNKNOWN"}:
        return "BLOCKED_INVALID_LIVENESS"
    unresolved_known_failure = (
        candidate.get("known_failure_applies") is True
        and candidate.get("known_failure_unresolved") is True
        and candidate.get("revalidation_passed") is not True
    )
    current_verified_failure = (
        candidate.get("latest_verified_outcome") == "FAILURE"
        and candidate.get("revalidation_passed") is not True
    )
    if unresolved_known_failure:
        return "BLOCKED_KNOWN_FAILURE"
    if current_verified_failure:
        return "BLOCKED_CURRENT_FAILURE"
    if availability == "AVAILABLE":
        return "PRIMARY_ELIGIBLE"
    if availability == "DEGRADED":
        return "FALLBACK_ELIGIBLE"
    return "PROBE_REQUIRED"


def select_reliable_surface(candidates: list[dict]) -> dict:
    """Prefer verified liveness/reliability before lower execution overhead; never compute a global vendor score."""
    classified = [
        {**candidate, "reliability_class": classify_surface_reliability(candidate)}
        for candidate in candidates
    ]

    def choose(items: list[dict]) -> dict:
        return min(items, key=lambda c: (int(c.get("execution_overhead_rank", 9999)), str(c.get("surface_id", ""))))

    primary = [c for c in classified if c["reliability_class"] == "PRIMARY_ELIGIBLE"]
    if primary:
        selected = choose(primary)
        return {
            "action": "SELECT_RELIABLE_SURFACE",
            "selected_surface": selected.get("surface_id"),
            "classifications": classified,
        }
    fallback = [c for c in classified if c["reliability_class"] == "FALLBACK_ELIGIBLE"]
    if fallback:
        selected = choose(fallback)
        return {
            "action": "SELECT_FALLBACK_SURFACE",
            "selected_surface": selected.get("surface_id"),
            "classifications": classified,
        }
    probe = [c for c in classified if c["reliability_class"] == "PROBE_REQUIRED"]
    if probe:
        selected = choose(probe)
        return {
            "action": "PROBE_SELECTED_CANDIDATE",
            "selected_surface": selected.get("surface_id"),
            "classifications": classified,
        }
    return {"action": "HOLD_NO_RELIABLE_SURFACE", "selected_surface": None, "classifications": classified}


def validate_contract_bindings() -> None:
    resolver = load_json(RESOLVER)
    if resolver.get("version") != "1.2" or resolver.get("implementation_revision") != "1.2.6":
        fail("runtime decisions must bind current Resolver v1.2 implementation revision 1.2.6")
    continuation = resolver.get("continuation_checkpoint_policy", {})
    if "authority_fingerprint" not in set(continuation.get("required_checkpoint_fields", [])):
        fail("authority snapshot reuse must bind the existing authority_fingerprint carrier")
    if continuation.get("context_switch_or_compression_is_not_authority_change") is not True:
        fail("chat/context switch alone must not invalidate a verified authority snapshot")

    tool = load_json(TOOL_CONTRACT)
    selective = tool.get("selective_readback_policy", {})
    if selective.get("rule") != "READBACK_SCOPE_FOLLOWS_MUTATION_BLAST_RADIUS":
        fail("selective readback must compile the existing blast-radius policy")
    if selective.get("unknown_blast_radius") != "WIDEN_READBACK":
        fail("unknown blast radius must widen readback")
    if selective.get("authority_or_cross_platform_pointer_mutation") != "AUTHORITY_AND_DRIFT_READBACK_REQUIRED":
        fail("authority/pointer mutation must trigger authority + drift readback")

    heavy = tool.get("heavy_executor_policy", {})
    if heavy.get("default") != "ESCALATION_ONLY" or heavy.get("control_plane_role") is not False:
        fail("heavy executor must remain escalation-only and outside the control-plane role")
    if heavy.get("output_ceiling_before_standard_readback_review_completion_gate") != "EXECUTED":
        fail("heavy executor pre-review output ceiling must remain EXECUTED")

    liveness = tool.get("surface_liveness_policy", {})
    if set(liveness.get("states", [])) != {"AVAILABLE", "UNAVAILABLE", "DEGRADED", "UNKNOWN"}:
        fail("surface liveness states drifted")
    if "PREVIOUS_SELECTED_SURFACE_FAILED" not in set(liveness.get("probe_when", [])):
        fail("failed selected surface must trigger bounded liveness probe when it is reconsidered")
    if liveness.get("unknown_surface_does_not_block_when_another_verified_sufficient_surface_is_available") is not True:
        fail("unknown surface must not displace an already verified sufficient surface")
    routing = tool.get("unified_adapter_routing_policy", {})
    precedence = routing.get("selection_precedence", [])
    try:
        reliability_pos = precedence.index("CURRENT_VERIFIED_AVAILABILITY_AND_RELIABILITY")
        overhead_pos = precedence.index("LOWER_EXECUTION_OVERHEAD")
    except ValueError:
        fail("adapter selection must include verified reliability and execution overhead precedence")
    if reliability_pos >= overhead_pos:
        fail("verified liveness/reliability must outrank lower execution overhead")
    if routing.get("availability_is_runtime_fact_not_authority") is not True:
        fail("surface availability/reliability must remain runtime fact, not authority")

    regression = load_json(REGRESSION_CONTRACT)
    failure_policy = regression.get("transferable_failure_recurrence_policy", {})
    required_failure_fields = {
        "failure_signature",
        "root_cause_class",
        "affected_layer",
        "repair_rule",
        "regression_test",
        "applicability",
    }
    if not required_failure_fields.issubset(set(failure_policy.get("record_fields", []))):
        fail("transferable failure record fields incomplete")
    if failure_policy.get("trivial_or_one_off_execution_mistake_not_persisted") is not True:
        fail("trivial one-off failures must not pollute transferable failure memory")
    if failure_policy.get("recurrence_after_prior_repair_state") != "EXECUTION_DRIFT":
        fail("known failure recurrence must classify as execution drift")
    if failure_policy.get("recurrence_after_prior_repair_code") != "KNOWN_FAILURE_RECURRED":
        fail("known failure recurrence code missing")
    if failure_policy.get("no_global_failure_database") is not True:
        fail("P2 must not create a global failure database")
    if failure_policy.get("reuse_existing_practice_skill_validator_or_regression_carrier") is not True:
        fail("transferable failures must reuse existing OLEANDER carriers")


def validate_p1_cases() -> None:
    rows = load_jsonl(CASES)
    by_id = {row.get("case_id"): row for row in rows}
    required = {
        "CACHE-001-VERIFIED-SNAPSHOT-REUSE",
        "CACHE-002-AUTHORITY-DRIFT-REFRESH",
        "CACHE-003-GITHUB-HEAD-DRIFT-REFRESH",
        "READBACK-001-UNKNOWN-BLAST-RADIUS-WIDEN",
        "READBACK-002-AUTHORITY-MUTATION-DRIFT-READBACK",
        "READBACK-003-THREE-D-BOUNDED-READBACK",
        "WORK-001-LIGHTER-ADAPTER-SUFFICIENT",
        "WORK-002-DESIGN-JUDGMENT-NO-ESCALATION",
        "WORK-003-GUI-BOUND-HEAVY-ELIGIBLE",
    }
    missing = required - set(by_id)
    if missing:
        fail(f"missing P1 runtime cases {sorted(missing)}")

    for case_id in ["CACHE-001-VERIFIED-SNAPSHOT-REUSE", "CACHE-002-AUTHORITY-DRIFT-REFRESH", "CACHE-003-GITHUB-HEAD-DRIFT-REFRESH"]:
        c = by_id[case_id]
        result = decide_authority_snapshot(
            c.get("snapshot"),
            c["current_authority_fingerprint"],
            c.get("current_github_head_sha"),
            c.get("current_constraint_hash"),
        )
        if result["action"] != c["expected_action"] or result["reason"] != c["expected_reason"]:
            fail(f"{case_id} snapshot decision mismatch")

    for case_id in ["READBACK-001-UNKNOWN-BLAST-RADIUS-WIDEN", "READBACK-002-AUTHORITY-MUTATION-DRIFT-READBACK", "READBACK-003-THREE-D-BOUNDED-READBACK"]:
        c = by_id[case_id]
        result = plan_selective_readback(
            c["mutation_domain"], c["blast_radius_known"], c.get("cross_platform_pointer_changed", False)
        )
        if result["action"] != c["expected_action"]:
            fail(f"{case_id} selective-readback decision mismatch")
        for token in c.get("expected_scope_contains", []):
            if token not in result["scope"]:
                fail(f"{case_id} readback scope missing {token}")

    for case_id in ["WORK-001-LIGHTER-ADAPTER-SUFFICIENT", "WORK-002-DESIGN-JUDGMENT-NO-ESCALATION", "WORK-003-GUI-BOUND-HEAVY-ELIGIBLE"]:
        c = by_id[case_id]
        result = decide_heavy_executor(**c["inputs"])
        if result["action"] != c["expected_action"] or result["output_ceiling"] != c["expected_output_ceiling"]:
            fail(f"{case_id} heavy-executor decision mismatch")


def validate_p2_cases() -> None:
    rows = load_jsonl(P2_CASES)
    by_id = {row.get("case_id"): row for row in rows}
    required = {
        "FAILURE-001-KNOWN-MATCH-REUSE-REPAIR",
        "FAILURE-002-RECURRENCE-EXECUTION-DRIFT",
        "FAILURE-003-MATERIAL-NEW-CONTEXT-RECLASSIFY",
        "FAILURE-004-NO-MATCH-NORMAL-ANALYSIS",
        "RELIABILITY-001-AVAILABLE-VERIFIED-PREFERRED",
        "RELIABILITY-002-UNRESOLVED-KNOWN-FAILURE-BLOCKS-PRIMARY",
        "RELIABILITY-003-UNKNOWN-ONLY-PROBE",
        "RELIABILITY-004-UNKNOWN-NOT-PROBED-WITH-VERIFIED-ALTERNATIVE",
        "RELIABILITY-005-ALL-BLOCKED-HOLD",
    }
    missing = required - set(by_id)
    if missing:
        fail(f"missing P2 runtime cases {sorted(missing)}")

    for case_id in [
        "FAILURE-001-KNOWN-MATCH-REUSE-REPAIR",
        "FAILURE-002-RECURRENCE-EXECUTION-DRIFT",
        "FAILURE-003-MATERIAL-NEW-CONTEXT-RECLASSIFY",
        "FAILURE-004-NO-MATCH-NORMAL-ANALYSIS",
    ]:
        c = by_id[case_id]
        result = decide_known_failure(
            current_failure_signature=c["current_failure_signature"],
            current_applicability=c["current_applicability"],
            materially_new_context=c["materially_new_context"],
            prior_repair_applied=c["prior_repair_applied"],
            known_failure_records=c["known_failure_records"],
        )
        if result["state"] != c["expected_state"] or result["action"] != c["expected_action"]:
            fail(f"{case_id} known-failure decision mismatch")
        if "expected_code" in c and result.get("code") != c["expected_code"]:
            fail(f"{case_id} recurrence code mismatch")
        if "expected_repair_rule" in c and result.get("repair_rule") != c["expected_repair_rule"]:
            fail(f"{case_id} repair-rule mismatch")
        if "expected_regression_test" in c and result.get("regression_test") != c["expected_regression_test"]:
            fail(f"{case_id} regression-test mismatch")

    for case_id in [
        "RELIABILITY-001-AVAILABLE-VERIFIED-PREFERRED",
        "RELIABILITY-002-UNRESOLVED-KNOWN-FAILURE-BLOCKS-PRIMARY",
        "RELIABILITY-003-UNKNOWN-ONLY-PROBE",
        "RELIABILITY-004-UNKNOWN-NOT-PROBED-WITH-VERIFIED-ALTERNATIVE",
        "RELIABILITY-005-ALL-BLOCKED-HOLD",
    ]:
        c = by_id[case_id]
        result = select_reliable_surface(c["candidates"])
        if result["action"] != c["expected_action"] or result.get("selected_surface") != c.get("expected_selected_surface"):
            fail(f"{case_id} reliability selection mismatch")
        classes = {x.get("surface_id"): x.get("reliability_class") for x in result["classifications"]}
        if "expected_blocked_surface" in c and not classes.get(c["expected_blocked_surface"], "").startswith("BLOCKED_"):
            fail(f"{case_id} expected failed surface was not blocked")
        if "expected_not_probed_surface" in c:
            sid = c["expected_not_probed_surface"]
            if result.get("selected_surface") == sid:
                fail(f"{case_id} unknown surface was selected for probe despite verified alternative")


def main() -> None:
    validate_contract_bindings()
    validate_p1_cases()
    validate_p2_cases()
    print("runtime-decision validation: PASS")
    print("verified authority snapshot reuse/refresh: ENFORCED")
    print("selective readback planning by mutation blast radius: ENFORCED")
    print("heavy executor escalation-only decision: ENFORCED")
    print("transferable known-failure reuse and recurrence drift classification: ENFORCED")
    print("surface liveness/reliability selection with bounded probing: ENFORCED")
    print("no new authority/state/failure-db/reliability-db/ontology carrier: PRESERVED")


if __name__ == "__main__":
    main()
