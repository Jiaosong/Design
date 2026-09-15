#!/usr/bin/env python3
"""Validate OLEANDER Professional Domain Process definition/instance objects.

This validator is deliberately narrow. It validates structure and a few runtime
consistency invariants; it does not infer professional quality, Design KEEP,
engineering/statutory approval, DQ maturity, or Promotion.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # CI/runtime may intentionally expose only Python stdlib.
    Draft202012Validator = None  # type: ignore[assignment]


SCHEMA_PATH = Path(__file__).with_name("professional-domain-process.v1.schema.json")


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


def validate_fallback_structure(payload: dict[str, Any]) -> list[str]:
    """Stdlib-only structural floor for CI environments without jsonschema.

    The JSON Schema remains the full machine contract. This fallback deliberately
    checks the contract fields that are consequential to routing, integration,
    readback and reopen semantics so CI does not silently degrade to a top-level
    kind check when the optional jsonschema package is unavailable.
    """

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
                "required_interface_maturity_to_enter",
                "required_interface_maturity_to_close",
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

        stages = payload.get("stages")
        if not isinstance(stages, list) or not stages:
            errors.append("definition: stages must be a non-empty array")
        elif stages:
            stage_required = {
                "stage_id",
                "stage_name",
                "professional_question",
                "entry_conditions",
                "required_inputs",
                "knowledge_inputs",
                "required_dd_dimensions",
                "required_native_outputs",
                "interface_requirements",
                "interface_bindings",
                "required_readback",
                "professional_review_owner",
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
                require_keys(stage, stage_required, f"stages[{index}]", errors)
                bindings = stage.get("interface_bindings", [])
                if not isinstance(bindings, list):
                    errors.append(f"stages[{index}].interface_bindings: expected array")
                    continue
                for binding_index, binding in enumerate(bindings):
                    if not isinstance(binding, dict):
                        errors.append(
                            f"stages[{index}].interface_bindings[{binding_index}]: expected object"
                        )
                        continue
                    require_keys(
                        binding,
                        binding_required,
                        f"stages[{index}].interface_bindings[{binding_index}]",
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

        for stage in stages:
            stage_instance_id = stage.get("stage_instance_id", "<unknown>")
            execution_state = stage.get("execution_state")
            exit_state = stage.get("exit_condition_state")
            verdict = stage.get("review_verdict")

            if execution_state == "CLOSED" and exit_state != "SATISFIED":
                errors.append(
                    f"{stage_instance_id}: CLOSED requires exit_condition_state=SATISFIED"
                )
            if execution_state == "CLOSED" and verdict not in {"PASS", "N_A"}:
                errors.append(
                    f"{stage_instance_id}: CLOSED requires review_verdict PASS or N_A"
                )
            if execution_state == "BLOCKED" and not stage.get("open_items"):
                errors.append(
                    f"{stage_instance_id}: BLOCKED requires at least one open_items entry"
                )
            if execution_state == "STALE" and not stage.get("stale_scope"):
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", type=Path)
    args = parser.parse_args()

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
