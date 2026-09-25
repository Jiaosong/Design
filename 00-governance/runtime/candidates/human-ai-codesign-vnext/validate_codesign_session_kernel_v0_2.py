from __future__ import annotations

import json
from pathlib import Path

from codesign_session_kernel_v0_2 import (
    ClassificationContext,
    apply_human_actions,
    apply_iteration_steer,
    classify_message,
    decide_auto_advance,
    decide_designer_support,
    decide_file_placement,
    partition_work_after_defer,
    plan_context_load,
    resolve_execution_route,
    validate_context_projection,
    validate_domain_adapter,
    validate_execution_route,
    validate_human_actions,
    validate_option_set,
    validate_phase_transition,
    validate_second_round_delta,
)


ROOT = Path(__file__).resolve().parent
FIXTURES = json.loads((ROOT / "codesign_session_kernel_fixtures_v0.2.json").read_text(encoding="utf-8"))


def _expect_subset(actual: dict, expected: dict, case_id: str) -> list[str]:
    failures: list[str] = []
    first_action = (actual.get("human_actions") or [None])[0]
    for key, expected_value in expected.items():
        if key == "human_action_level":
            actual_value = (first_action or {}).get("level")
        elif key == "human_action_action":
            actual_value = (first_action or {}).get("action")
        elif key == "durable_preference":
            actual_value = (first_action or {}).get("durable_preference")
        elif key == "referents":
            actual_value = (first_action or {}).get("referents")
        elif key == "referent_binding":
            actual_value = (first_action or {}).get("referent_binding")
        elif key == "human_action_reason":
            actual_value = (first_action or {}).get("reason")
        elif key == "human_action":
            actual_value = first_action
        elif key == "human_action_count":
            actual_value = len(actual.get("human_actions") or [])
        elif key == "human_actions_actions":
            actual_value = [x.get("action") for x in (actual.get("human_actions") or [])]
        elif key == "human_actions_referents":
            actual_value = [x.get("referents") for x in (actual.get("human_actions") or [])]
        elif key == "second_action_reason":
            actions = actual.get("human_actions") or []
            actual_value = actions[1].get("reason") if len(actions) > 1 else None
        elif key == "bound_referent_revision":
            bound = (first_action or {}).get("bound_referents") or []
            actual_value = bound[0].get("revision") if bound else None
        elif key == "bound_referent_lineage":
            bound = (first_action or {}).get("bound_referents") or []
            actual_value = bound[0].get("lineage_ref") if bound else None
        elif key == "human_action_route":
            actual_value = (first_action or {}).get("route_target")
        elif key == "binding_issue":
            actual_value = (first_action or {}).get("binding_issue")
        else:
            actual_value = actual.get(key)
        if actual_value != expected_value:
            failures.append(f"{case_id}:{key}:expected={expected_value!r}:actual={actual_value!r}")
    return failures


def main() -> int:
    failures: list[str] = []
    results: list[dict] = []

    for case in FIXTURES["classification_cases"]:
        c = case.get("context", {})
        ctx = ClassificationContext(
            active_option_refs=tuple(c.get("active_option_refs", [])),
            pending_decision_ref=c.get("pending_decision_ref"),
            unambiguous_active_ref=c.get("unambiguous_active_ref"),
            actor_role=c.get("actor_role", "DESIGNER"),
            referent_metadata=c.get("referent_metadata", {}),
        )
        actual = classify_message(case["text"], ctx)
        case_failures = _expect_subset(actual, case["expect"], case["id"])
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES["second_round_cases"]:
        errors = validate_second_round_delta(case["trace"])
        case_failures: list[str] = []
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}")
        if "expect_error_contains" in case and case["expect_error_contains"] not in errors:
            case_failures.append(f"{case['id']}:missing_error={case['expect_error_contains']!r}:actual={errors!r}")
        if "expect_error_prefix" in case and not any(x.startswith(case["expect_error_prefix"]) for x in errors):
            case_failures.append(f"{case['id']}:missing_error_prefix={case['expect_error_prefix']!r}:actual={errors!r}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "errors": errors})

    for case in FIXTURES["option_set_cases"]:
        errors = validate_option_set(case["options"])
        case_failures = []
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}")
        if "expect_error_contains" in case and case["expect_error_contains"] not in errors:
            case_failures.append(f"{case['id']}:missing_error={case['expect_error_contains']!r}:actual={errors!r}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "errors": errors})

    for case in FIXTURES["phase_transition_cases"]:
        errors = validate_phase_transition(case["current"], case["next"])
        case_failures = []
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}")
        if "expect_error_contains" in case and case["expect_error_contains"] not in errors:
            case_failures.append(f"{case['id']}:missing_error={case['expect_error_contains']!r}:actual={errors!r}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "errors": errors})

    for case in FIXTURES["auto_advance_cases"]:
        actual = decide_auto_advance(**case["input"])
        case_failures = []
        if actual["decision"] != case["expect_decision"]:
            case_failures.append(f"{case['id']}:expected={case['expect_decision']}:actual={actual['decision']}")
        if "expect_reason" in case and actual.get("reason") != case["expect_reason"]:
            case_failures.append(f"{case['id']}:reason:expected={case['expect_reason']}:actual={actual.get('reason')}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES["domain_adapter_cases"]:
        errors = validate_domain_adapter(case["adapter"])
        case_failures = []
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}")
        if "expect_error_contains" in case and case["expect_error_contains"] not in errors:
            case_failures.append(f"{case['id']}:missing_error={case['expect_error_contains']!r}:actual={errors!r}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "errors": errors})

    for case in FIXTURES["defer_partition_cases"]:
        actual = partition_work_after_defer(case["work_items"], case["deferred"])
        case_failures = [] if actual == case["expect"] else [
            f"{case['id']}:expected={case['expect']!r}:actual={actual!r}"
        ]
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES["branch_transition_cases"]:
        actual = apply_iteration_steer(case["status"], case["action"], case["referents"])
        case_failures = [] if actual == case["expect"] else [
            f"{case['id']}:expected={case['expect']!r}:actual={actual!r}"
        ]
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES["human_action_validation_cases"]:
        errors = validate_human_actions(case["actions"])
        case_failures = []
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}")
        if "expect_error_prefix" in case and not any(x.startswith(case["expect_error_prefix"]) for x in errors):
            case_failures.append(f"{case['id']}:missing_error_prefix={case['expect_error_prefix']!r}:actual={errors!r}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "errors": errors})

    for case in FIXTURES["compound_transition_cases"]:
        actual = apply_human_actions(case["status"], case["actions"])
        case_failures = [] if actual == case["expect"] else [
            f"{case['id']}:expected={case['expect']!r}:actual={actual!r}"
        ]
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES["designer_support_cases"]:
        actual = decide_designer_support(**case["input"])
        case_failures = []
        if actual["mode"] != case["expect_mode"]:
            case_failures.append(f"{case['id']}:mode:expected={case['expect_mode']}:actual={actual['mode']}")
        if actual["fade_basis"] != case["expect_fade_basis"]:
            case_failures.append(f"{case['id']}:fade_basis:expected={case['expect_fade_basis']}:actual={actual['fade_basis']}")
        if actual.get("durable_skill_score") is not None:
            case_failures.append(f"{case['id']}:durable_skill_score_must_be_null")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES["context_projection_cases"]:
        errors = validate_context_projection(case["projection"])
        actual = plan_context_load(case["projection"])
        case_failures = []
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}")
        if "expect_error_contains" in case and case["expect_error_contains"] not in errors:
            case_failures.append(f"{case['id']}:missing_error={case['expect_error_contains']!r}:actual={errors!r}")
        if "expect_decision" in case and actual.get("decision") != case["expect_decision"]:
            case_failures.append(f"{case['id']}:decision:expected={case['expect_decision']}:actual={actual.get('decision')}")
        if "expect_selected_refs" in case and actual.get("selected_refs") != case["expect_selected_refs"]:
            case_failures.append(f"{case['id']}:selected_refs:expected={case['expect_selected_refs']!r}:actual={actual.get('selected_refs')!r}")
        if "expect_required_over_budget" in case and actual.get("required_over_budget") != case["expect_required_over_budget"]:
            case_failures.append(f"{case['id']}:required_over_budget:expected={case['expect_required_over_budget']!r}:actual={actual.get('required_over_budget')!r}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "errors": errors, "actual": actual})

    for case in FIXTURES["file_placement_cases"]:
        actual = decide_file_placement(case["file_fact"])
        case_failures = []
        if actual.get("placement") != case["expect_placement"]:
            case_failures.append(f"{case['id']}:placement:expected={case['expect_placement']}:actual={actual.get('placement')}")
        if actual.get("library_binary_write") != case["expect_library_binary_write"]:
            case_failures.append(f"{case['id']}:library_binary_write:expected={case['expect_library_binary_write']}:actual={actual.get('library_binary_write')}")
        failures.extend(case_failures)
        results.append({"id": case["id"], "status": "PASS" if not case_failures else "FAIL", "actual": actual})

    for case in FIXTURES.get("execution_route_cases", []):
        actual = resolve_execution_route(case.get("input") or {})
        errors = validate_execution_route(actual)
        case_failures = []
        for key, expected in (case.get("expect") or {}).items():
            if actual.get(key) != expected:
                case_failures.append(
                    f"{case['id']}:{key}:expected={expected!r}:actual={actual.get(key)!r}"
                )
        if "expect_errors" in case and errors != case["expect_errors"]:
            case_failures.append(
                f"{case['id']}:expected_errors={case['expect_errors']!r}:actual={errors!r}"
            )
        failures.extend(case_failures)
        results.append({
            "id": case["id"],
            "status": "PASS" if not case_failures else "FAIL",
            "actual": actual,
            "errors": errors,
        })

    output = {
        "schema": "oleander.codesign-session-kernel-validation.v0.2",
        "status": "PASS" if not failures else "FAIL",
        "case_count": len(results),
        "failures": failures,
        "results": results,
        "claim_ceiling": "REFERENCE_KERNEL_LOGIC_AND_INVARIANT_VALIDATION_ONLY / NOT CURRENT / NOT PROFESSIONAL PASS / NOT HUMAN TRIAL",
    }
    (ROOT / "OLEANDER_CODESIGN_SESSION_KERNEL_VALIDATION_v0.2.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{output['status']}: {len(results)} kernel cases; failures={len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
