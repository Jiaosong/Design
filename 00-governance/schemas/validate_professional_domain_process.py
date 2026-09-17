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
import sys
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # CI/runtime may intentionally expose only Python stdlib.
    Draft202012Validator = None  # type: ignore[assignment]


SCHEMA_PATH = Path(__file__).with_name("professional-domain-process.v1.schema.json")
EXAMPLE_PATH = Path(__file__).with_name("professional-domain-process.example.json")

INTERFACE_MATURITY_RANK = {
    "IDENTIFIED": 0,
    "DEFINED": 1,
    "COORDINATED": 2,
    "EXERCISED": 3,
    "VERIFIED": 4,
}


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

    if payload.get("schema_version") not in {"1.0", "1.1"}:
        errors.append("schema_version must be 1.0 or 1.1")

    if kind == "PROFESSIONAL_DOMAIN_PROCESS_DEFINITION":
        schema_version = payload.get("schema_version")
        if schema_version not in {"1.0", "1.1"}:
            errors.append("definition: schema_version must be 1.0 or 1.1")
        strict_definition = schema_version == "1.1"
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
            if strict_definition:
                stage_required.add("stage_body_contract")
            current_binding_required = {
                "requirement_id",
                "source_domain",
                "source_stage_ref",
                "direction",
                "shared_variables",
                "coupling_hypothesis",
                "criticality_hypothesis",
                "required_maturity_to_enter",
                "required_maturity_to_close",
                "allowed_dispositions_on_exit",
                "required_native_source_role",
                "requested_change_reopen_rule",
            }
            legacy_binding_required = {
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
                binding_field = (
                    "interface_binding_requirements"
                    if strict_definition
                    else "interface_bindings"
                )
                if binding_field not in stage:
                    errors.append(
                        f"{label}: schema_version {schema_version} requires {binding_field}"
                    )
                forbidden_binding_field = (
                    "interface_bindings"
                    if strict_definition
                    else "interface_binding_requirements"
                )
                if forbidden_binding_field in stage:
                    errors.append(
                        f"{label}: schema_version {schema_version} may not use {forbidden_binding_field}"
                    )
                require_nonempty_list(stage, "does_not_prove", label, errors)
                for required_list in {
                    "required_inputs",
                    "required_native_outputs",
                    "required_readback",
                    "exit_conditions",
                    "reopen_triggers",
                }:
                    require_nonempty_list(stage, required_list, label, errors)
                body_contract = stage.get("stage_body_contract")
                if strict_definition and not isinstance(body_contract, dict):
                    errors.append(f"{label}.stage_body_contract: expected object")
                elif strict_definition:
                    require_keys(
                        body_contract,
                        {
                            "title_rule",
                            "required_semantic_sections",
                            "knowledge_mount_rule",
                            "native_source_rule",
                            "readback_rule",
                            "open_failure_rule",
                            "verdict_reopen_rule",
                        },
                        f"{label}.stage_body_contract",
                        errors,
                    )
                    expected_body_roles = {
                        "PROFESSIONAL_QUESTION_SCOPE",
                        "CURRENT_CONDITION_PROBLEM",
                        "AUTHORITY_KNOWLEDGE_EVIDENCE_INPUTS",
                        "PROFESSIONAL_CRITERIA_INTENT",
                        "DEVELOPMENT_ANALYSIS_COMPARISON_MECHANISM",
                        "CROSS_DOMAIN_INTERFACES",
                        "NATIVE_OUTPUT_SOURCE_OF_TRUTH",
                        "ACTUAL_READBACK_FINDING",
                        "FAILURE_OPEN_DOES_NOT_PROVE",
                        "VERDICT_CLAIM_REOPEN_NEXT_ACTION",
                    }
                    body_roles = body_contract.get("required_semantic_sections")
                    if not isinstance(body_roles, list):
                        errors.append(
                            f"{label}.stage_body_contract.required_semantic_sections: expected array"
                        )
                    else:
                        string_body_roles = [
                            role for role in body_roles if isinstance(role, str)
                        ]
                        if (
                            len(body_roles) != 10
                            or len(string_body_roles) != 10
                            or len(set(string_body_roles)) != 10
                            or set(string_body_roles) != expected_body_roles
                        ):
                            errors.append(
                                f"{label}.stage_body_contract: required_semantic_sections must contain each of the 10 semantic responsibilities exactly once"
                            )
                if not stage.get("independent_review_requirement"):
                    errors.append(
                        f"{label}: independent_review_requirement must be non-empty"
                    )
                bindings = stage.get(binding_field, [])
                if not isinstance(bindings, list):
                    errors.append(f"{label}.{binding_field}: expected array")
                    continue
                for binding_index, binding in enumerate(bindings):
                    if not isinstance(binding, dict):
                        errors.append(
                            f"{label}.{binding_field}[{binding_index}]: expected object"
                        )
                        continue
                    require_keys(
                        binding,
                        current_binding_required
                        if strict_definition
                        else legacy_binding_required,
                        f"{label}.{binding_field}[{binding_index}]",
                        errors,
                    )
                    if not binding.get("shared_variables"):
                        errors.append(
                            f"{label}.{binding_field}[{binding_index}]: shared_variables must be non-empty"
                        )
                    enter = binding.get("required_maturity_to_enter")
                    close = binding.get("required_maturity_to_close")
                    if enter in INTERFACE_MATURITY_RANK and close in INTERFACE_MATURITY_RANK:
                        if INTERFACE_MATURITY_RANK[close] < INTERFACE_MATURITY_RANK[enter]:
                            errors.append(
                                f"{label}.{binding_field}[{binding_index}]: required_maturity_to_close may not be lower than required_maturity_to_enter"
                            )

        completion = payload.get("completion_contract")
        if isinstance(completion, dict):
            require_nonempty_list(
                completion,
                "process_exit_conditions",
                "completion_contract",
                errors,
            )
        change = payload.get("change_contract")
        if isinstance(change, dict):
            for required_list in {
                "reopen_triggers",
                "stale_scope_rules",
                "downstream_impact_rules",
                "receipt_stale_rules",
            }:
                require_nonempty_list(change, required_list, "change_contract", errors)

    elif kind == "DOMAIN_PROCESS_INSTANCE":
        schema_version = payload.get("schema_version")
        if schema_version not in {"1.0", "1.1"}:
            errors.append("process instance: schema_version must be 1.0 or 1.1")
        strict_instance = schema_version == "1.1"
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
        required |= (
            {"domain_state", "current_use_state", "process_exit_condition_state"}
            if strict_instance
            else {"execution_state"}
        )
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
            stage_required |= (
                {"domain_state", "current_use_state"}
                if strict_instance
                else {"execution_state"}
            )
            if strict_instance:
                stage_required.add("stage_body_record")
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
        schema_version = payload.get("schema_version")
        strict_definition = schema_version == "1.1"
        if schema_version not in {"1.0", "1.1"}:
            errors.append("definition: schema_version must be 1.0 or 1.1")
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
            if not isinstance(stage, dict):
                continue
            for required_list in {
                "required_inputs",
                "required_native_outputs",
                "required_readback",
                "exit_conditions",
                "reopen_triggers",
            }:
                value = stage.get(required_list)
                if not isinstance(value, list) or not value:
                    errors.append(
                        f"{stage_id}: {required_list} must be a non-empty array"
                    )
            binding_field = (
                "interface_binding_requirements"
                if strict_definition
                else "interface_bindings"
            )
            forbidden_binding_field = (
                "interface_bindings"
                if strict_definition
                else "interface_binding_requirements"
            )
            if binding_field not in stage:
                errors.append(
                    f"{stage_id}: schema_version {schema_version} requires {binding_field}"
                )
            if forbidden_binding_field in stage:
                errors.append(
                    f"{stage_id}: schema_version {schema_version} may not use {forbidden_binding_field}"
                )
            if not strict_definition and "stage_body_contract" in stage:
                errors.append(
                    f"{stage_id}: schema_version 1.0 legacy definition may not acquire v1.1 stage_body_contract in place"
                )
            bindings = stage.get(binding_field, [])
            duplicate_binding_ids = duplicate_values(
                [
                    binding.get(
                        "requirement_id"
                        if strict_definition
                        else "interface_binding_id",
                        "",
                    )
                    for binding in bindings
                    if binding.get(
                        "requirement_id"
                        if strict_definition
                        else "interface_binding_id"
                    )
                ]
            )
            if duplicate_binding_ids:
                errors.append(
                    f"{stage_id}: duplicate {binding_field} identity values: "
                    + ", ".join(duplicate_binding_ids)
                )
            for binding_index, binding in enumerate(bindings):
                if not isinstance(binding, dict):
                    continue
                if not binding.get("shared_variables"):
                    errors.append(
                        f"{stage_id}.{binding_field}[{binding_index}]: shared_variables must be non-empty"
                    )
                enter = binding.get("required_maturity_to_enter")
                close = binding.get("required_maturity_to_close")
                if enter in INTERFACE_MATURITY_RANK and close in INTERFACE_MATURITY_RANK:
                    if INTERFACE_MATURITY_RANK[close] < INTERFACE_MATURITY_RANK[enter]:
                        errors.append(
                            f"{stage_id}.{binding_field}[{binding_index}]: required_maturity_to_close may not be lower than required_maturity_to_enter"
                        )

        completion = payload.get("completion_contract")
        if isinstance(completion, dict):
            value = completion.get("process_exit_conditions")
            if not isinstance(value, list) or not value:
                errors.append(
                    "completion_contract: process_exit_conditions must be a non-empty array"
                )

        change = payload.get("change_contract")
        if isinstance(change, dict):
            for required_list in {
                "reopen_triggers",
                "stale_scope_rules",
                "downstream_impact_rules",
                "receipt_stale_rules",
            }:
                value = change.get(required_list)
                if not isinstance(value, list) or not value:
                    errors.append(
                        f"change_contract: {required_list} must be a non-empty array"
                    )

    elif kind == "DOMAIN_PROCESS_INSTANCE":
        stages = payload.get("stage_instances", [])
        strict_current_emission = payload.get("schema_version") == "1.1"
        if payload.get("schema_version") not in {"1.0", "1.1"}:
            errors.append("process instance: schema_version must be 1.0 or 1.1")
        if strict_current_emission:
            for field in {
                "domain_state",
                "current_use_state",
                "process_exit_condition_state",
            }:
                if field not in payload:
                    errors.append(
                        f"process instance: schema_version 1.1 requires {field}"
                    )
            if "execution_state" in payload:
                errors.append(
                    "process instance: schema_version 1.1 may not use legacy execution_state"
                )
        elif "execution_state" not in payload:
            errors.append(
                "process instance: schema_version 1.0 requires legacy execution_state"
            )
        else:
            for field in {
                "domain_state",
                "current_use_state",
                "process_exit_condition_state",
                "in_claim_blocking_open_item_count",
            }:
                if field in payload:
                    errors.append(
                        f"process instance: schema_version 1.0 legacy shape may not acquire v1.1 field {field} in place"
                    )
        if strict_current_emission and not isinstance(
            payload.get("in_claim_blocking_open_item_count"), int
        ):
            errors.append(
                "process instance: schema_version 1.1 requires in_claim_blocking_open_item_count"
            )
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

        current_use_state = payload.get("current_use_state")
        process_exit_state = payload.get("process_exit_condition_state")
        legacy_execution_state = payload.get("execution_state")
        professional_verdict = payload.get("professional_verdict")
        if process_exit_state == "SATISFIED":
            if professional_verdict in {"NOT_RUN", "HOLD"}:
                errors.append(
                    "process instance: SATISFIED exit cannot use professional_verdict NOT_RUN or HOLD"
                )
            if not stages:
                errors.append("process instance: SATISFIED exit requires stage_instances evidence")
            if not payload.get("professional_receipt_refs"):
                errors.append(
                    "process instance: SATISFIED exit requires professional_receipt_refs"
                )
        if (
            current_use_state == "CURRENT"
            and process_exit_state == "SATISFIED"
            and professional_verdict == "PASS"
            and not payload.get("professional_receipt_refs")
        ):
            errors.append(
                "process instance: CURRENT + SATISFIED + PASS requires professional_receipt_refs"
            )
        if current_use_state == "CURRENT" and process_exit_state == "SATISFIED" and professional_verdict == "PASS":
            if not any(
                isinstance(stage, dict)
                and stage.get("current_use_state") == "CURRENT"
                and stage.get("exit_condition_state") == "SATISFIED"
                and stage.get("review_verdict") == "PASS"
                for stage in stages
            ):
                errors.append(
                    "process instance: CURRENT + SATISFIED + PASS requires at least one CURRENT + SATISFIED + PASS stage"
                )
        if (
            strict_current_emission
            and process_exit_state == "SATISFIED"
            and payload.get("in_claim_blocking_open_item_count") != 0
        ):
            errors.append(
                "process instance: schema_version 1.1 SATISFIED requires in_claim_blocking_open_item_count=0"
            )
        if process_exit_state == "BLOCKED" and not payload.get("open_items"):
            errors.append("process instance: BLOCKED requires open_items")
        if current_use_state == "STALE" and not payload.get("stale_scope"):
            errors.append("process instance: STALE requires stale_scope")

        if not strict_current_emission:
            if legacy_execution_state == "CLOSED":
                if professional_verdict in {"NOT_RUN", "HOLD"}:
                    errors.append(
                        "process instance: legacy CLOSED cannot use professional_verdict NOT_RUN or HOLD"
                    )
                if not stages:
                    errors.append(
                        "process instance: legacy CLOSED requires stage_instances evidence"
                    )
                if not payload.get("professional_receipt_refs"):
                    errors.append(
                        "process instance: legacy CLOSED requires professional_receipt_refs"
                    )
            if legacy_execution_state == "BLOCKED" and not payload.get("open_items"):
                errors.append("process instance: legacy BLOCKED requires open_items")
            if legacy_execution_state == "STALE" and not payload.get("stale_scope"):
                errors.append("process instance: legacy STALE requires stale_scope")

        for stage in stages:
            stage_instance_id = stage.get("stage_instance_id", "<unknown>")
            current_stage_use = stage.get("current_use_state")
            exit_state = stage.get("exit_condition_state")
            legacy_stage_state = stage.get("execution_state")
            verdict = stage.get("review_verdict")
            body = stage.get("stage_body_record")

            if strict_current_emission:
                for field in {"domain_state", "current_use_state"}:
                    if field not in stage:
                        errors.append(
                            f"{stage_instance_id}: schema_version 1.1 requires {field}"
                        )
                if "execution_state" in stage:
                    errors.append(
                        f"{stage_instance_id}: schema_version 1.1 may not use legacy execution_state"
                    )
            elif "execution_state" not in stage:
                errors.append(
                    f"{stage_instance_id}: schema_version 1.0 requires legacy execution_state"
                )
            else:
                for field in {
                    "domain_state",
                    "current_use_state",
                    "stage_body_record",
                    "review_bindings",
                    "in_claim_blocking_open_item_count",
                }:
                    if field in stage:
                        errors.append(
                            f"{stage_instance_id}: schema_version 1.0 legacy shape may not acquire v1.1 field {field} in place"
                        )

            if strict_current_emission and not isinstance(
                stage.get("in_claim_blocking_open_item_count"), int
            ):
                errors.append(
                    f"{stage_instance_id}: schema_version 1.1 requires in_claim_blocking_open_item_count"
                )

            if strict_current_emission and not isinstance(body, dict):
                errors.append(
                    f"{stage_instance_id}: stage instance requires stage_body_record"
                )

            if strict_current_emission and isinstance(body, dict):
                title = body.get("title")
                generic_titles = {
                    "Analysis",
                    "Concept",
                    "Design Development",
                    "Final",
                    "Planning",
                    "Review",
                    "analysis",
                    "concept",
                    "design development",
                    "final",
                    "planning",
                    "review",
                }
                if title in generic_titles:
                    errors.append(
                        f"{stage_instance_id}: stage body title is generic and does not identify the decision object"
                    )

                section_coverage = body.get("section_coverage")
                expected_roles = {
                    "PROFESSIONAL_QUESTION_SCOPE",
                    "CURRENT_CONDITION_PROBLEM",
                    "AUTHORITY_KNOWLEDGE_EVIDENCE_INPUTS",
                    "PROFESSIONAL_CRITERIA_INTENT",
                    "DEVELOPMENT_ANALYSIS_COMPARISON_MECHANISM",
                    "CROSS_DOMAIN_INTERFACES",
                    "NATIVE_OUTPUT_SOURCE_OF_TRUTH",
                    "ACTUAL_READBACK_FINDING",
                    "FAILURE_OPEN_DOES_NOT_PROVE",
                    "VERDICT_CLAIM_REOPEN_NEXT_ACTION",
                }
                if not isinstance(section_coverage, list):
                    errors.append(
                        f"{stage_instance_id}: stage_body_record.section_coverage must be an array"
                    )
                else:
                    roles = [
                        entry.get("semantic_role")
                        for entry in section_coverage
                        if isinstance(entry, dict)
                        and isinstance(entry.get("semantic_role"), str)
                    ]
                    if (
                        len(section_coverage) != 10
                        or len(set(roles)) != 10
                        or set(roles) != expected_roles
                    ):
                        errors.append(
                            f"{stage_instance_id}: stage body must disposition each of the 10 semantic responsibilities exactly once"
                        )
                    for entry in section_coverage:
                        if not isinstance(entry, dict):
                            continue
                        status = entry.get("status")
                        if status in {"PRESENT", "COMBINED"} and not entry.get(
                            "visible_heading_or_locator"
                        ):
                            errors.append(
                                f"{stage_instance_id}: {entry.get('semantic_role')} {status} requires visible_heading_or_locator"
                            )
                        if (
                            status == "NOT_APPLICABLE_WITH_REASON"
                            and not entry.get("reason")
                        ):
                            errors.append(
                                f"{stage_instance_id}: {entry.get('semantic_role')} N/A requires reason"
                            )

                if verdict == "PASS":
                    if any(
                        isinstance(entry, dict) and entry.get("status") == "MISSING"
                        for entry in (section_coverage or [])
                    ):
                        errors.append(
                            f"{stage_instance_id}: PASS cannot retain MISSING stage-body responsibilities"
                        )
                    if not body.get("native_artifact_refs"):
                        errors.append(
                            f"{stage_instance_id}: PASS requires stage_body_record.native_artifact_refs"
                        )
                    if not body.get("readback_refs"):
                        errors.append(
                            f"{stage_instance_id}: PASS requires stage_body_record.readback_refs"
                        )
                    if not stage.get("actual_readback_refs"):
                        errors.append(
                            f"{stage_instance_id}: PASS requires actual_readback_refs"
                        )
                    if not stage.get("review_refs"):
                        errors.append(
                            f"{stage_instance_id}: PASS requires review_refs"
                        )
                    if strict_current_emission:
                        by_role = {
                            entry.get("semantic_role"): entry.get("status")
                            for entry in (section_coverage or [])
                            if isinstance(entry, dict)
                        }
                        for role in {
                            "NATIVE_OUTPUT_SOURCE_OF_TRUTH",
                            "ACTUAL_READBACK_FINDING",
                        }:
                            if by_role.get(role) not in {"PRESENT", "COMBINED"}:
                                errors.append(
                                    f"{stage_instance_id}: schema_version 1.1 PASS requires {role}=PRESENT or COMBINED"
                                )
                        bindings = stage.get("review_bindings")
                        if not isinstance(bindings, list) or not bindings:
                            errors.append(
                                f"{stage_instance_id}: schema_version 1.1 PASS requires exact review_bindings"
                            )
                        else:
                            review_refs = set(
                                ref
                                for ref in (stage.get("review_refs") or [])
                                if isinstance(ref, str)
                            )
                            native_refs = set(
                                ref
                                for ref in (body.get("native_artifact_refs") or [])
                                if isinstance(ref, str)
                            )
                            for binding_index, binding in enumerate(bindings):
                                if not isinstance(binding, dict):
                                    errors.append(
                                        f"{stage_instance_id}.review_bindings[{binding_index}]: expected object"
                                    )
                                    continue
                                if binding.get("review_ref") not in review_refs:
                                    errors.append(
                                        f"{stage_instance_id}.review_bindings[{binding_index}].review_ref must match review_refs"
                                    )
                                if binding.get("review_input_artifact_ref") not in native_refs:
                                    errors.append(
                                        f"{stage_instance_id}.review_bindings[{binding_index}].review_input_artifact_ref must match stage_body_record.native_artifact_refs"
                                    )
                                for field in {
                                    "reviewer_id",
                                    "review_input_revision_or_hash",
                                }:
                                    value = binding.get(field)
                                    if not isinstance(value, str) or not value.strip():
                                        errors.append(
                                            f"{stage_instance_id}.review_bindings[{binding_index}] requires {field}"
                                        )

            if exit_state == "SATISFIED":
                if verdict in {"NOT_RUN", "HOLD"}:
                    errors.append(
                        f"{stage_instance_id}: SATISFIED exit cannot use review_verdict NOT_RUN or HOLD"
                    )
                if verdict in {"PASS", "REVISE", "REJECT"}:
                    if not stage.get("outputs"):
                        errors.append(
                            f"{stage_instance_id}: SATISFIED {verdict} requires outputs"
                        )
                    if not stage.get("review_refs"):
                        errors.append(
                            f"{stage_instance_id}: SATISFIED {verdict} requires review_refs"
                        )
                    if not stage.get("actual_readback_refs"):
                        errors.append(
                            f"{stage_instance_id}: SATISFIED {verdict} requires actual_readback_refs"
                        )
                if (
                    stage.get("consequential_knowledge_mount_required") is True
                    and not stage.get("knowledge_mount_refs")
                ):
                    errors.append(
                        f"{stage_instance_id}: SATISFIED consequential-knowledge stage requires knowledge_mount_refs"
                    )
                if (
                    strict_current_emission
                    and stage.get("in_claim_blocking_open_item_count") != 0
                ):
                    errors.append(
                        f"{stage_instance_id}: schema_version 1.1 SATISFIED requires in_claim_blocking_open_item_count=0"
                    )
            if exit_state == "BLOCKED" and not stage.get("open_items"):
                errors.append(
                    f"{stage_instance_id}: BLOCKED requires at least one open_items entry"
                )
            if current_stage_use == "STALE" and not stage.get("stale_scope"):
                errors.append(
                    f"{stage_instance_id}: STALE requires at least one stale_scope entry"
                )
            if not strict_current_emission:
                if legacy_stage_state == "CLOSED":
                    if exit_state != "SATISFIED":
                        errors.append(
                            f"{stage_instance_id}: legacy CLOSED requires exit_condition_state=SATISFIED"
                        )
                    if verdict in {"NOT_RUN", "HOLD"}:
                        errors.append(
                            f"{stage_instance_id}: legacy CLOSED cannot use review_verdict NOT_RUN or HOLD"
                        )
                    if verdict in {"PASS", "REVISE", "REJECT"}:
                        if not stage.get("outputs"):
                            errors.append(
                                f"{stage_instance_id}: legacy CLOSED {verdict} requires outputs"
                            )
                        if not stage.get("review_refs"):
                            errors.append(
                                f"{stage_instance_id}: legacy CLOSED {verdict} requires review_refs"
                            )
                        if not stage.get("actual_readback_refs"):
                            errors.append(
                                f"{stage_instance_id}: legacy CLOSED {verdict} requires actual_readback_refs"
                            )
                if legacy_stage_state == "BLOCKED" and not stage.get("open_items"):
                    errors.append(
                        f"{stage_instance_id}: legacy BLOCKED requires open_items"
                    )
                if legacy_stage_state == "STALE" and not stage.get("stale_scope"):
                    errors.append(
                        f"{stage_instance_id}: legacy STALE requires stale_scope"
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
    if payload.get("schema_version") == "1.1":
        payload["domain_state"] = "DOMAIN_EXIT_COMPLETE"
        payload["current_use_state"] = "CURRENT"
        payload["process_exit_condition_state"] = "SATISFIED"
        payload.pop("execution_state", None)
    else:
        payload["execution_state"] = "CLOSED"
        payload.pop("domain_state", None)
        payload.pop("current_use_state", None)
        payload.pop("process_exit_condition_state", None)
    payload["professional_verdict"] = verdict
    payload["professional_receipt_refs"] = [f"PROF-RECEIPT-{verdict}"]
    stage = payload["stage_instances"][0]
    if payload.get("schema_version") == "1.1":
        stage["domain_state"] = "DOMAIN_STAGE_EXIT_COMPLETE"
        stage["current_use_state"] = "CURRENT"
        stage.pop("execution_state", None)
    else:
        stage["execution_state"] = "CLOSED"
        stage.pop("domain_state", None)
        stage.pop("current_use_state", None)
    stage["review_verdict"] = verdict
    stage["exit_condition_state"] = "SATISFIED"
    stage["outputs"] = ["CIRCULATION_READBACK"]
    stage["review_refs"] = [f"STAGE-REVIEW-{verdict}"]
    if payload.get("schema_version") == "1.1":
        stage["review_bindings"] = [
            {
                "review_ref": f"STAGE-REVIEW-{verdict}",
                "reviewer_id": "SELF-TEST-INDEPENDENT-REVIEWER",
                "review_input_artifact_ref": f"NATIVE-{verdict}",
                "review_input_revision_or_hash": f"SELF-TEST-REVISION-{verdict}",
                "independence_basis_ref_or_state": "SELF_TEST_DISTINCT_REVIEWER",
            }
        ]
        stage["in_claim_blocking_open_item_count"] = 0
        payload["in_claim_blocking_open_item_count"] = 0
    stage["actual_readback_refs"] = [f"READBACK-{verdict}"]
    stage["consequential_knowledge_mount_required"] = True
    stage["knowledge_mount_refs"] = ["KM-EXAMPLE-OE2-001"]
    body = stage.get("stage_body_record")
    if isinstance(body, dict):
        for entry in body.get("section_coverage", []):
            if not isinstance(entry, dict):
                continue
            if entry.get("status") == "MISSING":
                entry["status"] = "PRESENT"
                entry["visible_heading_or_locator"] = "SELF-TEST SATISFIED EVIDENCE"
                entry["reason"] = None
        body["native_artifact_refs"] = [f"NATIVE-{verdict}"]
        body["readback_refs"] = [f"READBACK-{verdict}"]
    return payload


def run_self_tests() -> list[str]:
    """Regression cases for previously observed false-positive/false-negative closure."""

    failures: list[str] = []
    schema = load_json(SCHEMA_PATH)
    stage_required = set(schema["$defs"]["stageDefinition"]["required"])
    expected_stage_required = {
        "stage_body_contract",
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

    example = load_json(EXAMPLE_PATH)
    positive_errors = validate_payload(example)
    if positive_errors:
        failures.append("example must validate: " + " | ".join(positive_errors))

    closed_pass = make_closed_instance(example, "PASS")
    closed_pass_errors = validate_payload(closed_pass)
    if closed_pass_errors:
        failures.append(
            "evidence-complete SATISFIED PASS must validate: "
            + " | ".join(closed_pass_errors)
        )

    closed_reject = make_closed_instance(example, "REJECT")
    closed_reject_errors = validate_payload(closed_reject)
    if closed_reject_errors:
        failures.append(
            "evidence-complete SATISFIED REJECT must remain legal: "
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
        failures.append("SATISFIED PASS with empty stage evidence was false-accepted")

    missing_process_receipt = make_closed_instance(example, "PASS")
    missing_process_receipt["professional_receipt_refs"] = []
    receipt_errors = validate_payload(missing_process_receipt)
    if not receipt_errors:
        failures.append("SATISFIED PASS with no professional receipt was false-accepted")

    empty_process = make_closed_instance(example, "REJECT")
    empty_process["stage_instances"] = []
    empty_errors = validate_payload(empty_process)
    if not empty_errors:
        failures.append("SATISFIED process with zero stage instances was false-accepted")

    return failures


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="backslashreplace")
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
