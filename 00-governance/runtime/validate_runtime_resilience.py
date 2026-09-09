#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
RESOLVER = RUNTIME / "OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json"
TOOL_CONTRACT = RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json"
RECEIPT_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_RECEIPT_v1.0.json"
CASES = ROOT / "evals" / "runtime" / "runtime_resilience.jsonl"

DEFAULT_EXECUTION_BUDGET = {
    "node_advances": 12,
    "repair_attempts": 2,
    "adapter_failovers": 2,
    "runtime_probes": 4,
}


def fail(msg: str) -> None:
    raise SystemExit(f"runtime-resilience validation failed: {msg}")


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


def reconcile_partial_commit(legs: list[dict]) -> dict:
    """Reconcile multi-surface mutation legs without pretending to own a distributed transaction manager."""
    if not legs:
        return {"state": "HOLD", "action": "HOLD_EMPTY_RECONCILIATION_SET", "advance_allowed": False}

    allowed_states = {"CONFIRMED", "ABSENT", "UNCERTAIN"}
    invalid = [leg for leg in legs if leg.get("state") not in allowed_states]
    if invalid:
        return {"state": "HOLD", "action": "HOLD_INVALID_PARTIAL_COMMIT_STATE", "advance_allowed": False}

    uncertain = [leg for leg in legs if leg.get("state") == "UNCERTAIN"]
    if uncertain:
        return {
            "state": "PARTIAL_COMMIT",
            "action": "VERIFY_UNCERTAIN_LEGS_BEFORE_ADVANCE",
            "legs": [leg.get("surface_id") for leg in uncertain],
            "advance_allowed": False,
        }

    absent = [leg for leg in legs if leg.get("state") == "ABSENT"]
    if absent:
        retryable = [
            leg
            for leg in absent
            if leg.get("retry_safe") is True or leg.get("idempotent_or_provider_keyed") is True
        ]
        if len(retryable) == len(absent):
            return {
                "state": "PARTIAL_COMMIT",
                "action": "RECONCILE_MISSING_LEGS_BEFORE_ADVANCE",
                "legs": [leg.get("surface_id") for leg in absent],
                "advance_allowed": False,
            }

        confirmed = [leg for leg in legs if leg.get("state") == "CONFIRMED"]
        compensable = bool(confirmed) and all(leg.get("compensation_legal") is True for leg in confirmed)
        if compensable:
            return {
                "state": "PARTIAL_COMMIT",
                "action": "COMPENSATE_CONFIRMED_LEGS_BEFORE_ADVANCE",
                "legs": [leg.get("surface_id") for leg in confirmed],
                "advance_allowed": False,
            }
        return {
            "state": "HOLD",
            "action": "HOLD_PARTIAL_COMMIT_UNRECONCILED",
            "legs": [leg.get("surface_id") for leg in absent],
            "advance_allowed": False,
        }

    return {
        "state": "COHERENT_COMMIT",
        "action": "ADVANCE_AFTER_COHERENT_COMMIT",
        "legs": [leg.get("surface_id") for leg in legs],
        "advance_allowed": True,
    }


def decide_execution_budget(counters: dict, budget: dict | None = None) -> dict:
    """Bound one execution turn without reintroducing an artificial one-node stop."""
    limits = dict(DEFAULT_EXECUTION_BUDGET)
    if budget:
        for key, value in budget.items():
            if key in limits:
                limits[key] = int(value)
    exhausted = [
        key for key, limit in limits.items()
        if int(counters.get(key, 0)) >= limit
    ]
    if exhausted:
        return {
            "action": "STOP_EXECUTION_BUDGET_EXHAUSTED",
            "exhausted": exhausted,
            "limits": limits,
            "continue_allowed": False,
        }
    return {
        "action": "CONTINUE_WITHIN_EXECUTION_BUDGET",
        "exhausted": [],
        "limits": limits,
        "continue_allowed": True,
    }


def decide_surface_probe(health: dict, now_epoch: int) -> dict:
    """Use ephemeral cooldown/probe counters to avoid repeated liveness probes in one run."""
    availability = health.get("availability_state", "UNKNOWN")
    probe_attempts = int(health.get("probe_attempts_in_current_run", 0))
    max_probes = int(health.get("max_probe_attempts", 1))
    cooldown_until = int(health.get("probe_suppressed_until_epoch", 0) or 0)
    current_failure = health.get("latest_verified_outcome") == "FAILURE"

    if availability == "AVAILABLE" and not current_failure:
        return {"action": "USE_VERIFIED_SURFACE_NO_PROBE", "probe_allowed": False}
    if probe_attempts >= max_probes:
        return {"action": "HOLD_SURFACE_PROBE_BUDGET_EXHAUSTED", "probe_allowed": False}
    if now_epoch < cooldown_until:
        return {
            "action": "SUPPRESS_PROBE_DURING_COOLDOWN",
            "probe_allowed": False,
            "retry_after_epoch": cooldown_until,
        }
    return {"action": "ALLOW_SINGLE_REVALIDATION_PROBE", "probe_allowed": True}


def validate_existing_contract_derivation() -> None:
    tool = load_json(TOOL_CONTRACT)
    remote = tool.get("remote_mutation_idempotency_policy", {})
    if remote.get("uncertain_outcome_action") != "VERIFY_POSTCONDITION_BEFORE_RETRY":
        fail("P6 must derive uncertain-leg handling from existing verify-before-retry semantics")
    if remote.get("duplicate_side_effects_forbidden") is not True:
        fail("P6 must preserve duplicate-side-effect prohibition")
    if remote.get("blind_retry_after_timeout_forbidden") is not True:
        fail("P6 must preserve blind-retry prohibition")
    selective = tool.get("selective_readback_policy", {})
    if selective.get("unknown_blast_radius") != "WIDEN_READBACK":
        fail("P6 reconciliation must preserve readback widening when blast radius is unknown")

    routing = tool.get("runtime_routing_policy", {})
    if routing.get("retry_policy") != "BOUNDED_EVIDENCE_DRIVEN_NO_BLIND_RETRY_LOOP":
        fail("P7 budget must derive from the existing bounded retry rule")
    liveness = tool.get("surface_liveness_policy", {})
    if set(liveness.get("states", [])) != {"AVAILABLE", "UNAVAILABLE", "DEGRADED", "UNKNOWN"}:
        fail("P7 must preserve existing liveness states")
    if liveness.get("do_not_probe_for_inventory_curiosity") is not True:
        fail("P7 must not probe surfaces merely for inventory curiosity")
    ephemeral = set(tool.get("ephemeral_persistence_policy", {}).get("ephemeral_by_default", []))
    if not {"TRANSIENT_ADAPTER_STATE", "SURFACE_LIVENESS_PROBES"}.issubset(ephemeral):
        fail("P7 surface health/cooldown must remain ephemeral runtime state")

    resolver = load_json(RESOLVER)
    continuous = resolver.get("continuous_execution_policy", {})
    if continuous.get("no_artificial_one_node_stop") is not True:
        fail("P7 budget must remain a bounded guard, not an artificial one-node stop")
    if "TOOL_OR_RUNTIME_HARD_LIMIT" not in set(continuous.get("stop_conditions", [])):
        fail("P7 budget must remain compatible with existing runtime hard-limit stops")

    receipt = load_json(RECEIPT_CONTRACT)
    flow = set(receipt.get("canonical_flow_phases", []))
    if "ACTUAL_READBACK" not in flow or "SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE" not in flow:
        fail("P6/P7 require existing readback + sync/drift flow phases")


def validate_p6_cases(by_id: dict[str, dict]) -> None:
    required = {
        "P6-001-ALL-LEGS-CONFIRMED-ADVANCE",
        "P6-002-UNCERTAIN-LEG-VERIFY-FIRST",
        "P6-003-ABSENT-IDEMPOTENT-LEG-RECONCILE",
        "P6-004-UNSAFE-MISSING-LEG-COMPENSATE",
        "P6-005-UNSAFE-UNCOMPENSABLE-HOLD",
    }
    missing = required - set(by_id)
    if missing:
        fail(f"missing P6 cases {sorted(missing)}")
    for case_id in sorted(required):
        case = by_id[case_id]
        result = reconcile_partial_commit(case["legs"])
        if result.get("state") != case["expected_state"]:
            fail(f"{case_id} state mismatch: {result}")
        if result.get("action") != case["expected_action"]:
            fail(f"{case_id} action mismatch: {result}")
        if result.get("advance_allowed") is not case["expected_advance_allowed"]:
            fail(f"{case_id} advance gate mismatch: {result}")


def validate_p7_cases(by_id: dict[str, dict]) -> None:
    budget_cases = {
        "P7-001-BUDGET-WITHIN-LIMIT-CONTINUE",
        "P7-002-NODE-ADVANCE-BUDGET-STOPS",
        "P7-003-REPAIR-BUDGET-STOPS",
    }
    probe_cases = {
        "P7-004-COOLDOWN-SUPPRESSES-REPROBE",
        "P7-005-COOLDOWN-EXPIRED-ALLOWS-ONE-PROBE",
        "P7-006-PROBE-BUDGET-EXHAUSTED-HOLDS",
        "P7-007-VERIFIED-AVAILABLE-NO-PROBE",
    }
    missing = (budget_cases | probe_cases) - set(by_id)
    if missing:
        fail(f"missing P7 cases {sorted(missing)}")

    for case_id in sorted(budget_cases):
        case = by_id[case_id]
        result = decide_execution_budget(case["counters"], case.get("budget"))
        if result.get("action") != case["expected_action"]:
            fail(f"{case_id} budget action mismatch: {result}")
        if result.get("continue_allowed") is not case["expected_continue_allowed"]:
            fail(f"{case_id} continue gate mismatch: {result}")

    for case_id in sorted(probe_cases):
        case = by_id[case_id]
        result = decide_surface_probe(case["health"], int(case["now_epoch"]))
        if result.get("action") != case["expected_action"]:
            fail(f"{case_id} probe action mismatch: {result}")
        if result.get("probe_allowed") is not case["expected_probe_allowed"]:
            fail(f"{case_id} probe gate mismatch: {result}")


def main() -> None:
    validate_existing_contract_derivation()
    rows = load_jsonl(CASES)
    by_id = {row.get("case_id"): row for row in rows}
    validate_p6_cases(by_id)
    validate_p7_cases(by_id)
    print("runtime-resilience validation: PASS")
    print("P6 partial-commit reconciliation before DAG advance: ENFORCED")
    print("P7 bounded execution budget without one-node stop: ENFORCED")
    print("P7 ephemeral surface probe cooldown and probe budget: ENFORCED")
    print("P7 surface health remains runtime fact, not authority or persistent score: PRESERVED")


if __name__ == "__main__":
    main()
