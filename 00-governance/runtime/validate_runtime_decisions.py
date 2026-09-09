#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
TOOL_CONTRACT = RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json"
CASES = ROOT / "evals" / "runtime" / "sticky_constraints_and_flow.jsonl"


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


def validate_contract_bindings() -> None:
    resolver = load_json(RESOLVER)
    if resolver.get("version") != "1.2" or resolver.get("implementation_revision") != "1.2.5":
        fail("runtime decisions must bind current Resolver v1.2 implementation revision 1.2.5")
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


def validate_cases() -> None:
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


def main() -> None:
    validate_contract_bindings()
    validate_cases()
    print("runtime-decision validation: PASS")
    print("verified authority snapshot reuse/refresh: ENFORCED")
    print("selective readback planning by mutation blast radius: ENFORCED")
    print("heavy executor escalation-only decision: ENFORCED")
    print("no new authority/state/ontology carrier: PRESERVED")


if __name__ == "__main__":
    main()
