#!/usr/bin/env python3
"""Regression validation for OLEANDER Complex Project Master Runtime v1.0."""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from orchestrator import evaluate_master_runtime  # noqa: E402


EXAMPLE = HERE / "examples" / "example-master-runtime.json"


def load_example() -> dict:
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    baseline = load_example()

    runnable = evaluate_master_runtime(copy.deepcopy(baseline))
    require(runnable["status"] == "RUNNABLE", f"baseline must RUNNABLE: {runnable}")

    promotion = copy.deepcopy(baseline)
    promotion["promotion_requested"] = True
    ready = evaluate_master_runtime(promotion)
    require(ready["status"] == "READY_FOR_HUMAN_DECISION", f"promotion prerequisites should close: {ready}")
    require(ready["human_decision_required"] is True, "machine must stop at human decision")

    stale = copy.deepcopy(promotion)
    stale["integration"]["state"] = "STALE"
    stale_result = evaluate_master_runtime(stale)
    require(stale_result["status"] == "RECONCILIATION_REQUIRED", "stale integration must reconcile")

    open_interface = copy.deepcopy(promotion)
    open_interface["integration"]["open_major_critical_interfaces"] = 1
    open_result = evaluate_master_runtime(open_interface)
    require(open_result["status"] == "RECONCILIATION_REQUIRED", "open major/critical interface must block readiness")

    pending_change = copy.deepcopy(promotion)
    pending_change["change_events"][0]["propagation_state"] = "PENDING"
    pending_result = evaluate_master_runtime(pending_change)
    require(pending_result["status"] == "RECONCILIATION_REQUIRED", "material change without propagation must reconcile")

    stale_dependency = copy.deepcopy(promotion)
    stale_dependency["dependencies"][0]["state"] = "STALE"
    dependency_result = evaluate_master_runtime(stale_dependency)
    require(dependency_result["status"] == "RECONCILIATION_REQUIRED", "stale dependency must reconcile")

    design_pass = copy.deepcopy(promotion)
    next(r for r in design_pass["reviews"] if r["review_type"] == "DESIGN")["result"] = "PASS"
    design_result = evaluate_master_runtime(design_pass)
    require(design_result["status"] == "IN_PROGRESS", "generic design PASS must not equal KEEP")

    contradictory = copy.deepcopy(baseline)
    contradictory["integration"]["triggered"] = False
    contradictory["integration"]["state"] = "NOT_REQUIRED"
    contradictory["integration"]["verdict"] = "N_A"
    # Intentionally leave packet/receipt in place: a non-triggered route may not claim integration closure.
    contradiction_result = evaluate_master_runtime(contradictory)
    require(contradiction_result["status"] == "BLOCKED", "contradictory integration state must block")

    print("OLEANDER_COMPLEX_PROJECT_MASTER_RUNTIME=PASS")
    print("cases=8")
    print("machine_promotion=FORBIDDEN; max=READY_FOR_HUMAN_DECISION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

