#!/usr/bin/env python3
import json, sys
from pathlib import Path

PROMOTION = {"NO", "NO_PROMOTION", "CANDIDATE_NOT_PROMOTED"}
ALT_STATES = {"DOCUMENTED", "NOT_APPLICABLE_WITH_REASON"}


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def main():
    if len(sys.argv) != 2:
        fail("usage: validate_analysis_contract.py ANALYSIS_CONTRACT.json")
    data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

    if data.get("promotion") not in PROMOTION:
        fail("analysis contract must remain non-promoted")

    required = {
        "contract_id", "decision_question", "object_scale", "temporal_snapshot",
        "representation_contract", "alternative_explanation_state",
        "limitations", "abstraction_budget", "does_not_prove"
    }
    missing = required - set(data)
    if missing:
        fail(f"missing root fields: {sorted(missing)}")

    for key in ("contract_id", "decision_question", "object_scale", "temporal_snapshot"):
        if not nonempty_text(data.get(key)):
            fail(f"{key} must be non-empty text")

    rep = data.get("representation_contract")
    if not isinstance(rep, dict):
        fail("representation_contract must be an object")
    for key in ("representation_type", "why_fit_for_question", "supports", "does_not_support"):
        if key not in rep:
            fail(f"representation_contract missing {key}")
    if not nonempty_text(rep.get("representation_type")) or not nonempty_text(rep.get("why_fit_for_question")):
        fail("representation type and fit rationale must be explicit")
    if not isinstance(rep.get("supports"), list) or not rep["supports"]:
        fail("representation_contract.supports must be non-empty")
    if not isinstance(rep.get("does_not_support"), list) or not rep["does_not_support"]:
        fail("representation_contract.does_not_support must be non-empty")

    alt_state = data.get("alternative_explanation_state")
    if alt_state not in ALT_STATES:
        fail("invalid alternative_explanation_state")
    if alt_state == "DOCUMENTED":
        if not isinstance(data.get("alternative_explanations"), list) or not data["alternative_explanations"]:
            fail("DOCUMENTED requires alternative_explanations")
    else:
        if not nonempty_text(data.get("alternative_explanation_reason")):
            fail("NOT_APPLICABLE_WITH_REASON requires alternative_explanation_reason")

    if not isinstance(data.get("limitations"), list) or not data["limitations"]:
        fail("limitations must be a non-empty list")
    if not isinstance(data.get("does_not_prove"), list) or not data["does_not_prove"]:
        fail("does_not_prove must be a non-empty list")

    budget = data.get("abstraction_budget")
    if not isinstance(budget, dict):
        fail("abstraction_budget must be an object")
    for key in ("task_critical_variables", "removed_or_relaxed_variables", "external_support_layers"):
        if key not in budget:
            fail(f"abstraction_budget missing {key}")
    critical = set(budget.get("task_critical_variables") or [])
    removed = set(budget.get("removed_or_relaxed_variables") or [])
    external = budget.get("external_support_layers")
    if not critical:
        fail("task_critical_variables cannot be empty")
    if not isinstance(external, dict):
        fail("external_support_layers must be an object mapping variable -> support layer")
    unresolved = (critical & removed) - set(external)
    if unresolved:
        fail(f"task-critical variables removed without explicit external support: {sorted(unresolved)}")
    for variable, layer in external.items():
        if variable not in removed:
            fail(f"external support declared for non-removed variable: {variable}")
        if not nonempty_text(layer):
            fail(f"external support layer for {variable} must be non-empty")

    print("PASS: analysis question / representation / abstraction contract structurally valid")
    print("NOTE: structure PASS does not prove the question is important, the representation is perceptually effective, or Design KEEP.")


if __name__ == "__main__":
    main()
