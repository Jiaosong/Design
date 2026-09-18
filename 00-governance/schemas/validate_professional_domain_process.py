#!/usr/bin/env python3
"""Validate OLEANDER Professional Domain Process definition/instance objects.

This validator is deliberately narrow. It validates structure, closure evidence,
operational-mount linkage and runtime consistency; it does not infer professional
quality, Design KEEP, engineering/statutory approval, DQ maturity, interface
maturity, or Promotion.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # CI/runtime may intentionally expose only Python stdlib.
    Draft202012Validator = None  # type: ignore[assignment]


SCHEMA_PATH = Path(__file__).with_name("professional-domain-process.v1.schema.json")
EXAMPLE_PATH = Path(__file__).with_name("professional-domain-process.example.json")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def duplicate_values(values: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return sorted(duplicates)


def require_keys(
    obj: dict[str, Any], required: set[str], label: str, errors: list[str]
) -> None:
    missing = sorted(required - set(obj))
    if missing:
        errors.append(f"{label}: missing required keys: {', '.join(missing)}")


def require_nonempty_list(
    obj: dict[str, Any], key: str, label: str, errors: list[str]
) -> None:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        errors.append(f"{label}: {key} must be a non-empty array")


def validate_fallback_structure(payload: dict[str, Any]) -> list[str]:
    """Stdlib-only structural floor for CI environments without jsonschema."""

    errors: list[str] = []
    kind = payload.get("kind")
    common = {"schema_version", "kind"}

    if payload.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    if kind == "PROFESSIONAL_DOMAIN_PROCESS_DEFINITION":
        required = common | {
            "process_id",
            "domain",
            "version",
            "title",
            "purpose",
            "scope_in",
            "scope_out",
            "authority_position",
            "current_definition_ref",
            "trigger",
            "knowledge_binding",
            "stages",
            "interface_contract",
            "execution_binding",
            "assurance",
            "change_contract",
            "completion_contract",
        }
        require_keys(payload, required, "definition", errors)

        nested_requirements = {
            "trigger": {
                "project_flow_trigger",
                "design_question_types",
                "responsibility_triggers",
                "claim_ceiling_rule",
                "not_triggered_when",
                "mandatory_reopen_triggers",
            },
            "knowledge_binding": {
                "operational_mount_contract_ref",
                "consequential_knowledge_rule",
                "required_methods",
                "theory_routes",
                "source_routes",
                "evidence_routes",
                "precedent_case_routes",
                "practice_routes",
            },
            "interface_contract": {
                "integration_owner_ref",
                "inputs_from_domains",
                "outputs_to_domains",
                "shared_variables",
                "controlling_authority_requirements",
                "interface_maturity_policy",
                "allowed_open_interface_conditions",
                "integration_readback_requirements",
            },
            "execution_binding": {
                "required_native_outputs",
                "native_source_of_truth_rules",
                "execution_owner_requirements",
                "required_capabilities",
                "tool_adapter_requirements",
                "typed_handoff_contracts",
                "actual_readback_requirements",
            },
            "assurance": {
                "professional_review",
                "evidence_review",
                "technical_gates",
                "independent_review",
                "receipt_contract",
                "does_not_prove",
            },
            "change_contract": {
                "reopen_triggers",
                "stale_scope_rules",
                "upstream_impact_rules",
                "downstream_impact_rules",
                "interface_reopen_rules",
                "receipt_stale_rules",
            },
            "completion_contract": {
                "process_exit_conditions",
                "open_items_allowed",
                "professional_receipt",
                "promotion_effect",
                "claim_ceiling",
                "does_not_prove",
            },
        }
        for field, field_requirements in nested_requirements.items():
            value = payload.get(field)
            if isinstance(value, dict):
                require_keys(value, field_requirements, field, errors)
            elif field in payload:
                errors.append(f"{field}: expected object")

        for field in ("assurance", "completion_contract"):
            value = payload.get(field)
            if isinstance(value, dict):
                require_nonempty_list(value, "does_not_prove", field, errors)

        stages = payload.get("stages")
        if not isinstance(stages, list) or not stages:
            errors.append("definition: stages must be a non-empty array")
        else:
            stage_required = {
                "stage_id",
                "stage_name",
                "professional_question",
                "entry_conditions",
                "required_inputs",
                "knowledge_inputs",
                "knowledge_mount_requirement",
                "required_dd_dimensions",
                "required_native_outputs",
                "interface_requirements",
                "interface_bindings",
                "human_experience_consequences",
                "design_language_consequences",
                "technical_consequences",
                "content_projection_requirements",
                "required_readback",
                "professional_review_owner",
                "independent_review_requirement",
                "open_items_allowed",
                "exit_conditions",
                "reopen_triggers",
                "claim_ceiling",
                "does_not_prove",
            }
            binding_required = {
                "interface_binding_id",
                "source_domain",
                "source_stage_ref",
                "direction",
                "shared_variables",
                "coupling",
                "criticality",
                "required_maturity_to_enter",
                "required_maturity_to_close",
                "allowed_dispositions_on_exit",
                "native_source_of_truth",
                "change_reopen_rule",
            }
            for index, stage in enumerate(stages):
                if not isinstance(stage, dict):
                    errors.append(f"stages[{index}]: expected object")
                    continue
                label = f"stages[{index}]"
                require_keys(stage, stage_required, label, errors)
                require_nonempty_list(stage, "does_not_prove", label, errors)
                if not stage.get("independent_review_requirement"):
                    errors.append(
                        f"{label}: independent_review_requirement must be non-empty"
                    )
                bindings = stage.get("interface_bindings", [])
                if not isinstance(bindings, list):
                    errors.append(f"{label}.interface_bindings: expected array")
                    continue
                for binding_index, binding in enumerate(bindings):
                    if not isinstance(binding, dict):
                        errors.append(
                            f"{label}.interface_bindings[{binding_index}]: expected object"
                        )
                        continue
                    require_keys(
                        binding,
                        binding_required,
                        f"{label}.interface_bindings[{binding_index}]",
                        errors,
                    )

    elif kind == "DOMAIN_PROCESS_INSTANCE":
        required = common | {
            "instance_id",
            "project_id",
            "decision_object_refs",
            "process_definition_ref",
            "process_id",
            "process_version",
            "domain",
            "owner",
            "current_baseline",
            "execution_state",
            "professional_verdict",
            "claim_ceiling",
            "stage_instances",
            "active_interface_refs",
            "open_items",
            "professional_receipt_refs",
            "integration_receipt_refs",
            "stale_scope",
            "reopen_events",
            "last_updated",
        }
        require_keys(payload, required, "process instance", errors)
        stages = payload.get("stage_instances")
        if not isinstance(stages, list):
            errors.append("process instance: stage_instances must be an array")
        else:
            stage_required = {
                "stage_instance_id",
                "stage_definition_ref",
                "stage_id",
                "cycle",
                "baseline_ref",
                "execution_state",
                "review_verdict",
                "claim_ceiling",
                "inputs",
                "outputs",
                "consequential_knowledge_mount_required",
                "knowledge_mount_refs",
                "interface_refs",
                "evidence_refs",
                "review_refs",
                "open_items",
                "stale_scope",
                "reopen_events",
                "exit_condition_state",
                "actual_readback_refs",
                "last_updated",
            }
            for index, stage in enumerate(stages):
                if not isinstance(stage, dict):
                    errors.append(f"stage_instances[{index}]: expected object")
                    continue
                require_keys(stage, stage_required, f"stage_instances[{index}]", errors)
                granularity_state = stage.get(
                    "granularity_binding_state", "LEGACY_STAGE_ONLY"
                )
                if granularity_state == "DECISION_OBJECT_BOUND":
                    label = f"stage_instances[{index}]"
                    for key in (
                        "decision_object_refs",
                        "claim_refs",
                        "output_execution_bindings",
                    ):
                        require_nonempty_list(stage, key, label, errors)
                    output_bindings = stage.get("output_execution_bindings", [])
                    binding_required = {
                        "binding_id",
                        "decision_object_ref",
                        "claim_refs",
                        "knowledge_mount_refs",
                        "output_requirement_ref",
                        "required_native_output",
                        "required_capability_roles",
                        "tool_adapter_required",
                        "owner_set_ref",
                        "adapter_route_ref",
                        "artifact_refs",
                        "readback_refs",
                        "resolution_state",
                        "stale_if",
                        "does_not_prove",
                    }
                    if isinstance(output_bindings, list):
                        for binding_index, binding in enumerate(output_bindings):
                            if not isinstance(binding, dict):
                                errors.append(
                                    f"{label}.output_execution_bindings[{binding_index}]: expected object"
                                )
                                continue
                            binding_label = (
                                f"{label}.output_execution_bindings[{binding_index}]"
                            )
                            require_keys(
                                binding, binding_required, binding_label, errors
                            )
                            for key in (
                                "claim_refs",
                                "required_capability_roles",
                                "does_not_prove",
                            ):
                                require_nonempty_list(
                                    binding, key, binding_label, errors
                                )
    else:
        errors.append("kind is not a supported professional-domain-process object")

    return errors


def validate_semantics(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    kind = payload.get("kind")

    if kind == "PROFESSIONAL_DOMAIN_PROCESS_DEFINITION":
        stages = payload.get("stages", [])
        duplicate_stage_ids = duplicate_values(
            [stage.get("stage_id", "") for stage in stages if stage.get("stage_id")]
        )
        if duplicate_stage_ids:
            errors.append(
                "duplicate stage_id values: " + ", ".join(duplicate_stage_ids)
            )

        for stage in stages:
            stage_id = stage.get("stage_id", "<unknown>")
            bindings = stage.get("interface_bindings", [])
            duplicate_binding_ids = duplicate_values(
                [
                    binding.get("interface_binding_id", "")
                    for binding in bindings
                    if binding.get("interface_binding_id")
                ]
            )
            if duplicate_binding_ids:
                errors.append(
                    f"{stage_id}: duplicate interface_binding_id values: "
                    + ", ".join(duplicate_binding_ids)
                )

    elif kind == "DOMAIN_PROCESS_INSTANCE":
        stages = payload.get("stage_instances", [])
        duplicate_instance_ids = duplicate_values(
            [
                stage.get("stage_instance_id", "")
                for stage in stages
                if stage.get("stage_instance_id")
            ]
        )
        if duplicate_instance_ids:
            errors.append(
                "duplicate stage_instance_id values: "
                + ", ".join(duplicate_instance_ids)
            )

        execution_state = payload.get("execution_state")
        professional_verdict = payload.get("professional_verdict")
        if execution_state == "CLOSED":
            if professional_verdict in {"NOT_RUN", "HOLD"}:
                errors.append(
                    "process instance: CLOSED cannot use professional_verdict NOT_RUN or HOLD"
                )
            if not stages:
                errors.append("process instance: CLOSED requires stage_instances evidence")
            if not payload.get("professional_receipt_refs"):
                errors.append(
                    "process instance: CLOSED requires professional_receipt_refs"
                )
        if (
            execution_state in {"CURRENT", "CLOSED"}
            and professional_verdict == "PASS"
            and not payload.get("professional_receipt_refs")
        ):
            errors.append(
                "process instance: CURRENT/CLOSED PASS requires professional_receipt_refs"
            )
        if execution_state == "BLOCKED" and not payload.get("open_items"):
            errors.append("process instance: BLOCKED requires open_items")
        if execution_state == "STALE" and not payload.get("stale_scope"):
            errors.append("process instance: STALE requires stale_scope")

        for stage in stages:
            stage_instance_id = stage.get("stage_instance_id", "<unknown>")
            stage_state = stage.get("execution_state")
            exit_state = stage.get("exit_condition_state")
            verdict = stage.get("review_verdict")

            granularity_state = stage.get(
                "granularity_binding_state", "LEGACY_STAGE_ONLY"
            )
            if granularity_state == "DECISION_OBJECT_BOUND":
                stage_decision_refs = set(stage.get("decision_object_refs", []))
                stage_claim_refs = set(stage.get("claim_refs", []))
                process_decision_refs = set(payload.get("decision_object_refs", []))
                if not stage_decision_refs:
                    errors.append(
                        f"{stage_instance_id}: DECISION_OBJECT_BOUND requires decision_object_refs"
                    )
                if not stage_claim_refs:
                    errors.append(
                        f"{stage_instance_id}: DECISION_OBJECT_BOUND requires claim_refs"
                    )
                if not stage_decision_refs.issubset(process_decision_refs):
                    errors.append(
                        f"{stage_instance_id}: stage decision_object_refs must be included in process decision_object_refs"
                    )
                output_bindings = stage.get("output_execution_bindings", [])
                if not output_bindings:
                    errors.append(
                        f"{stage_instance_id}: DECISION_OBJECT_BOUND requires output_execution_bindings"
                    )
                duplicate_output_binding_ids = duplicate_values(
                    [
                        binding.get("binding_id", "")
                        for binding in output_bindings
                        if isinstance(binding, dict) and binding.get("binding_id")
                    ]
                )
                if duplicate_output_binding_ids:
                    errors.append(
                        f"{stage_instance_id}: duplicate output binding IDs: "
                        + ", ".join(duplicate_output_binding_ids)
                    )
                for binding in output_bindings:
                    if not isinstance(binding, dict):
                        continue
                    binding_id = binding.get("binding_id", "<unknown>")
                    decision_ref = binding.get("decision_object_ref")
                    if decision_ref not in stage_decision_refs:
                        errors.append(
                            f"{stage_instance_id}/{binding_id}: decision_object_ref must resolve within stage decision_object_refs"
                        )
                    binding_claims = set(binding.get("claim_refs", []))
                    if not binding_claims or not binding_claims.issubset(stage_claim_refs):
                        errors.append(
                            f"{stage_instance_id}/{binding_id}: claim_refs must be a non-empty subset of stage claim_refs"
                        )
                    binding_mounts = set(binding.get("knowledge_mount_refs", []))
                    stage_mounts = set(stage.get("knowledge_mount_refs", []))
                    if not binding_mounts.issubset(stage_mounts):
                        errors.append(
                            f"{stage_instance_id}/{binding_id}: knowledge_mount_refs must resolve within stage knowledge_mount_refs"
                        )
                    resolution_state = binding.get("resolution_state")
                    if resolution_state in {"ROUTED", "EXECUTED", "READBACK_COMPLETE"}:
                        if not binding.get("owner_set_ref"):
                            errors.append(
                                f"{stage_instance_id}/{binding_id}: {resolution_state} requires owner_set_ref"
                            )
                        if (
                            binding.get("tool_adapter_required") is True
                            and not binding.get("adapter_route_ref")
                        ):
                            errors.append(
                                f"{stage_instance_id}/{binding_id}: tool-backed {resolution_state} requires adapter_route_ref"
                            )
                    if resolution_state in {"EXECUTED", "READBACK_COMPLETE"} and not binding.get(
                        "artifact_refs"
                    ):
                        errors.append(
                            f"{stage_instance_id}/{binding_id}: {resolution_state} requires artifact_refs"
                        )
                    if resolution_state == "READBACK_COMPLETE" and not binding.get(
                        "readback_refs"
                    ):
                        errors.append(
                            f"{stage_instance_id}/{binding_id}: READBACK_COMPLETE requires readback_refs"
                        )

            if stage_state == "CLOSED":
                if exit_state != "SATISFIED":
                    errors.append(
                        f"{stage_instance_id}: CLOSED requires exit_condition_state=SATISFIED"
                    )
                if verdict in {"NOT_RUN", "HOLD"}:
                    errors.append(
                        f"{stage_instance_id}: CLOSED cannot use review_verdict NOT_RUN or HOLD"
                    )
                if verdict in {"PASS", "REVISE", "REJECT"}:
                    if not stage.get("outputs"):
                        errors.append(
                            f"{stage_instance_id}: CLOSED {verdict} requires outputs"
                        )
                    if not stage.get("review_refs"):
                        errors.append(
                            f"{stage_instance_id}: CLOSED {verdict} requires review_refs"
                        )
                    if not stage.get("actual_readback_refs"):
                        errors.append(
                            f"{stage_instance_id}: CLOSED {verdict} requires actual_readback_refs"
                        )
                if (
                    stage.get("consequential_knowledge_mount_required") is True
                    and not stage.get("knowledge_mount_refs")
                ):
                    errors.append(
                        f"{stage_instance_id}: CLOSED consequential-knowledge stage requires knowledge_mount_refs"
                    )
            if stage_state == "BLOCKED" and not stage.get("open_items"):
                errors.append(
                    f"{stage_instance_id}: BLOCKED requires at least one open_items entry"
                )
            if stage_state == "STALE" and not stage.get("stale_scope"):
                errors.append(
                    f"{stage_instance_id}: STALE requires at least one stale_scope entry"
                )

    return errors


def validate_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if Draft202012Validator is not None:
        schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
        errors.extend(
            f"schema: {error.message}"
            for error in sorted(
                validator.iter_errors(payload), key=lambda error: list(error.path)
            )
        )
    else:
        errors.extend(validate_fallback_structure(payload))
    errors.extend(validate_semantics(payload))
    return errors


def make_closed_instance(
    source: dict[str, Any], verdict: str = "PASS"
) -> dict[str, Any]:
    payload = copy.deepcopy(source)
    payload["execution_state"] = "CLOSED"
    payload["professional_verdict"] = verdict
    payload["professional_receipt_refs"] = [f"PROF-RECEIPT-{verdict}"]
    stage = payload["stage_instances"][0]
    stage["execution_state"] = "CLOSED"
    stage["review_verdict"] = verdict
    stage["exit_condition_state"] = "SATISFIED"
    stage["outputs"] = ["CIRCULATION_READBACK"]
    stage["review_refs"] = [f"STAGE-REVIEW-{verdict}"]
    stage["actual_readback_refs"] = [f"READBACK-{verdict}"]
    stage["consequential_knowledge_mount_required"] = True
    stage["knowledge_mount_refs"] = ["KM-EXAMPLE-OE2-001"]
    return payload


def run_self_tests() -> list[str]:
    """Regression cases for previously observed false-positive/false-negative closure."""

    failures: list[str] = []
    schema = load_json(SCHEMA_PATH)
    stage_required = set(schema["$defs"]["stageDefinition"]["required"])
    expected_stage_required = {
        "knowledge_mount_requirement",
        "human_experience_consequences",
        "design_language_consequences",
        "technical_consequences",
        "content_projection_requirements",
        "independent_review_requirement",
        "does_not_prove",
    }
    missing_stage_contract = sorted(expected_stage_required - stage_required)
    if missing_stage_contract:
        failures.append(
            "schema stageDefinition missing hardened fields: "
            + ", ".join(missing_stage_contract)
        )

    knowledge_required = set(
        schema["$defs"]["processDefinition"]["properties"]["knowledge_binding"][
            "required"
        ]
    )
    for field in {"operational_mount_contract_ref", "consequential_knowledge_rule"}:
        if field not in knowledge_required:
            failures.append(f"schema knowledge_binding missing {field}")

    interface_props = schema["$defs"]["processDefinition"]["properties"][
        "interface_contract"
    ]["properties"]
    if "interface_maturity_policy" not in interface_props:
        failures.append("schema interface_contract missing interface_maturity_policy")
    for forbidden in {
        "required_interface_maturity_to_enter",
        "required_interface_maturity_to_close",
    }:
        if forbidden in interface_props:
            failures.append(
                f"schema interface_contract retains duplicate maturity truth source: {forbidden}"
            )

    stage_instance_props = schema["$defs"]["stageInstance"]["properties"]
    for field in {
        "granularity_binding_state",
        "decision_object_refs",
        "claim_refs",
        "output_execution_bindings",
    }:
        if field not in stage_instance_props:
            failures.append(f"schema stageInstance missing granularity field: {field}")
    if "outputExecutionBinding" not in schema["$defs"]:
        failures.append("schema missing outputExecutionBinding definition")

    example = load_json(EXAMPLE_PATH)
    example_stage = example["stage_instances"][0]
    if example_stage.get("granularity_binding_state") != "DECISION_OBJECT_BOUND":
        failures.append("example must exercise DECISION_OBJECT_BOUND granularity")
    positive_errors = validate_payload(example)
    if positive_errors:
        failures.append("example must validate: " + " | ".join(positive_errors))

    closed_pass = make_closed_instance(example, "PASS")
    closed_pass_errors = validate_payload(closed_pass)
    if closed_pass_errors:
        failures.append(
            "evidence-complete CLOSED PASS must validate: "
            + " | ".join(closed_pass_errors)
        )

    closed_reject = make_closed_instance(example, "REJECT")
    closed_reject_errors = validate_payload(closed_reject)
    if closed_reject_errors:
        failures.append(
            "evidence-complete CLOSED REJECT must remain legal: "
            + " | ".join(closed_reject_errors)
        )

    missing_stage_evidence = make_closed_instance(example, "PASS")
    stage = missing_stage_evidence["stage_instances"][0]
    stage["outputs"] = []
    stage["review_refs"] = []
    stage["actual_readback_refs"] = []
    stage["knowledge_mount_refs"] = []
    evidence_errors = validate_payload(missing_stage_evidence)
    if not evidence_errors:
        failures.append("CLOSED PASS with empty stage evidence was false-accepted")

    missing_granularity = copy.deepcopy(example)
    missing_granularity["stage_instances"][0]["output_execution_bindings"] = []
    granularity_errors = validate_payload(missing_granularity)
    if not granularity_errors:
        failures.append(
            "DECISION_OBJECT_BOUND stage with no output execution bindings was false-accepted"
        )

    mismatched_decision = copy.deepcopy(example)
    mismatched_decision["stage_instances"][0]["output_execution_bindings"][0][
        "decision_object_ref"
    ] = "ARCH-PLAN-NOT-IN-STAGE"
    mismatch_errors = validate_payload(mismatched_decision)
    if not mismatch_errors:
        failures.append(
            "output execution binding with unresolved decision object was false-accepted"
        )

    missing_process_receipt = make_closed_instance(example, "PASS")
    missing_process_receipt["professional_receipt_refs"] = []
    receipt_errors = validate_payload(missing_process_receipt)
    if not receipt_errors:
        failures.append("CLOSED PASS with no professional receipt was false-accepted")

    empty_process = make_closed_instance(example, "REJECT")
    empty_process["stage_instances"] = []
    empty_errors = validate_payload(empty_process)
    if not empty_errors:
        failures.append("CLOSED process with zero stage instances was false-accepted")

    return failures


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=Path, nargs="?")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    self_test_failures = run_self_tests()
    if self_test_failures:
        print("PROFESSIONAL DOMAIN PROCESS SELF-TEST: FAIL")
        for error in self_test_failures:
            print(f"- {error}")
        return 1

    if args.self_test and args.json_file is None:
        print("PROFESSIONAL DOMAIN PROCESS SELF-TEST: PASS")
        return 0

    if args.json_file is None:
        parser.error("json_file is required unless --self-test is used")

    payload = load_json(args.json_file)
    errors = validate_payload(payload)
    if errors:
        print("PROFESSIONAL DOMAIN PROCESS VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PROFESSIONAL DOMAIN PROCESS VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
