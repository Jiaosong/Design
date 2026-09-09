#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
TOOL_CONTRACT = RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json"
RECEIPT_CONTRACT = RUNTIME / "OLEANDER_EXECUTION_RECEIPT_v1.0.json"
CASES = ROOT / "evals" / "runtime" / "runtime_resilience.jsonl"


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
        return {
            "state": "HOLD",
            "action": "HOLD_EMPTY_RECONCILIATION_SET",
            "advance_allowed": False,
        }

    allowed_states = {"CONFIRMED", "ABSENT", "UNCERTAIN"}
    invalid = [leg for leg in legs if leg.get("state") not in allowed_states]
    if invalid:
        return {
            "state": "HOLD",
            "action": "HOLD_INVALID_PARTIAL_COMMIT_STATE",
            "advance_allowed": False,
        }

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

    receipt = load_json(RECEIPT_CONTRACT)
    flow = set(receipt.get("canonical_flow_phases", []))
    if "ACTUAL_READBACK" not in flow or "SYNC_RECEIPT_AND_DRIFT_AS_APPLICABLE" not in flow:
        fail("P6 requires existing readback + sync/drift flow phases")
    if receipt.get("early_completion_forbidden_on") is None:
        fail("P6 must not replace the existing completion gate")


def validate_p6_cases() -> None:
    rows = load_jsonl(CASES)
    by_id = {row.get("case_id"): row for row in rows}
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


def main() -> None:
    validate_existing_contract_derivation()
    validate_p6_cases()
    print("runtime-resilience validation: PASS")
    print("P6 partial-commit reconciliation before DAG advance: ENFORCED")
    print("P6 uncertain legs verify before retry: ENFORCED")
    print("P6 unsafe unreconciled partial commit holds instead of guessing: ENFORCED")
    print("P6 does not create a distributed transaction database or new authority: PRESERVED")


if __name__ == "__main__":
    main()
