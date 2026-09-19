#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from validate_continuation_cycle import decide_checkpoint_resume
from validate_execution_locks import (
    decide_continuous_execution,
    evaluate_flow_completion,
    guard_checkpoint_mutation,
    resolve_continuation_frontier,
    resolve_sticky_constraints,
    validate_resolver,
)


ADAPTER_ID = "chat_on_steroids_oleander_resolver_adapter"
ADAPTER_REVISION = "1.2"
ROOT = Path(__file__).resolve().parents[2]
CAPABILITY_CONTRACT = ROOT / "00-governance" / "runtime" / "OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.json"
OWNER_MAP = ROOT / "00-governance" / "runtime" / "OLEANDER_NOTION_TO_GITHUB_EXECUTION_OWNER_MAP_v1.0.json"
CONTROL_GRAPH = ROOT / "00-governance" / "runtime" / "OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
KNOWLEDGE_MOUNT_CONTRACT = ROOT / "00-governance" / "knowledge-integrity-and-operational-mount-v1.0.md"
CLOSURE_INTENTS = {"COMPLETE", "CLOSE", "KEEP", "FINALIZE", "PROMOTE_KEEP", "STOP_COMPLETE"}
STRUCTURAL_EVIDENCE_CLASSES = {
    "STRUCTURE_COUNT",
    "PERSISTENCE_COUNT",
    "REACTION_COUNT",
    "PAGE_COUNT",
    "OBJECT_COUNT",
    "HASH_ONLY",
    "CI_GREEN",
    "RENDER_EXISTS",
    "FILE_EXISTS",
    "NODE_DESTINATION_EXISTS",
}
STRUCTURAL_DIMENSIONS = {
    "STRUCTURE_PERSISTENCE",
    "DELIVERY_INTEGRITY",
    "RUNTIME_INTEGRITY",
    "GEOMETRY_READBACK",
}
CANONICAL_PROFESSIONAL_STAGE_EXECUTION_CHAIN = [
    "PROFESSIONAL_STAGE",
    "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
    "KNOWLEDGE_INPUTS",
    "OPERATIONAL_KNOWLEDGE_MOUNT",
    "REQUIRED_CAPABILITY_ROLES",
    "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
    "NATIVE_OUTPUTS",
    "ACTUAL_READBACK",
    "INDEPENDENT_REVIEW",
    "STAGE_CLOSURE",
]


def _load_json(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return data


def _owner_contract_map() -> dict[str, dict]:
    contract = _load_json(CAPABILITY_CONTRACT)
    owners = contract.get("owners") or []
    return {str(owner.get("skill_id")): owner for owner in owners if isinstance(owner, dict) and owner.get("skill_id")}


def _professional_process_rows() -> list[dict]:
    graph = _load_json(CONTROL_GRAPH)
    rows = graph.get("professional_domain_process_state") or []
    return [row for row in rows if isinstance(row, dict)]


def _professional_machine_row(process_ref: str) -> tuple[dict, str]:
    for row in _professional_process_rows():
        if row.get("machine_schema_ref") == process_ref:
            return row, "CURRENT"
        if row.get("candidate_machine_schema_ref") == process_ref:
            return row, "CANDIDATE"
    raise ValueError(f"professional process_ref is not registered in the Current control graph: {process_ref}")


def _match_stage_capability_rule(role: str, rule: dict) -> bool:
    match = dict(rule.get("match") or {})
    if match.get("fallback") is True:
        return True
    if role in {str(x) for x in match.get("exact_any") or []}:
        return True
    if any(role.startswith(str(prefix)) for prefix in match.get("starts_with_any") or []):
        return True
    if any(str(token) in role for token in match.get("contains_any") or []):
        return True
    return False


def _stage_capability_rule(role: str, owner_map: dict) -> dict:
    routing = dict(owner_map.get("professional_stage_capability_routing") or {})
    rules = routing.get("rules") or []
    for rule in rules:
        if isinstance(rule, dict) and _match_stage_capability_rule(role, rule):
            return rule
    raise ValueError(f"no professional-stage capability routing rule matched {role}")


def _stage_execution_requirements(
    *,
    process_ref: str,
    process_mode: str,
    process_path: Path,
    stage: dict,
    owner_map: dict,
) -> tuple[dict, str]:
    direct = stage.get("stage_execution_requirements")
    if isinstance(direct, dict):
        if process_mode == "CURRENT":
            raise ValueError(
                f"{process_ref} is Current authority and may not gain stage_execution_requirements in place; "
                "use the exact-revision runtime compatibility projection"
            )
        return dict(direct), "CANDIDATE_PROCESS_DEFINITION"

    if process_mode != "CURRENT":
        raise ValueError(
            f"{process_ref}:{stage.get('stage_id')} Candidate stage lacks stage_execution_requirements"
        )

    projection_ref = str(
        owner_map.get("current_professional_stage_execution_projection_ref") or ""
    )
    if not projection_ref:
        raise ValueError("Current professional-stage execution projection ref missing")
    projection = _load_json(ROOT / projection_ref)
    if projection.get("semantic_class") != "NON_AUTHORITY_RUNTIME_COMPATIBILITY_PROJECTION":
        raise ValueError("Current professional-stage execution projection missing or authority class drifted")
    process_entry = next(
        (
            entry
            for entry in projection.get("processes") or []
            if isinstance(entry, dict) and entry.get("current_machine_ref") == process_ref
        ),
        None,
    )
    if not isinstance(process_entry, dict):
        raise ValueError(f"Current professional process has no runtime execution projection: {process_ref}")
    actual_sha256 = hashlib.sha256(process_path.read_bytes()).hexdigest()
    if process_entry.get("current_machine_sha256") != actual_sha256:
        raise ValueError(f"Current stage execution projection SHA256 stale for {process_ref}")
    stage_projection = dict(
        (process_entry.get("stages") or {}).get(str(stage.get("stage_id") or "")) or {}
    )
    if not stage_projection:
        raise ValueError(
            f"Current professional stage missing runtime execution projection: {process_ref}#{stage.get('stage_id')}"
        )
    return stage_projection, "CURRENT_EXACT_REVISION_RUNTIME_PROJECTION"


def _evaluate_stage_knowledge_mounts(stage: dict, spec: dict) -> dict:
    declared_inputs = [str(x) for x in stage.get("knowledge_inputs") or []]
    active_inputs = [str(x) for x in spec.get("active_knowledge_inputs") or []]
    if not active_inputs and declared_inputs:
        active_inputs = list(declared_inputs)
    unknown_active = sorted(set(active_inputs) - set(declared_inputs))
    if unknown_active:
        raise ValueError(
            f"active knowledge inputs are not declared by {stage.get('stage_id')}: {unknown_active}"
        )

    omitted_reasons = {
        str(k): str(v).strip()
        for k, v in dict(spec.get("omitted_knowledge_input_reasons") or {}).items()
    }
    hold_reasons: list[str] = []
    omitted: list[dict] = []
    for knowledge_input in declared_inputs:
        if knowledge_input in active_inputs:
            continue
        reason = omitted_reasons.get(knowledge_input, "")
        if not reason:
            hold_reasons.append(f"KNOWLEDGE_INPUT_OMISSION_REASON_REQUIRED:{knowledge_input}")
        omitted.append({"knowledge_input": knowledge_input, "reason": reason or None})

    records = spec.get("knowledge_mount_records") or []
    if not isinstance(records, list):
        raise ValueError("knowledge_mount_records must be an array")
    coverage = {knowledge_input: [] for knowledge_input in active_inputs}
    normalized_records: list[dict] = []
    required_fields = {
        "knowledge_ref",
        "use_role",
        "operational_eligibility",
        "eligibility_scope",
        "claim_ceiling",
        "applicability",
        "conditions",
        "unresolved_items",
        "freshness_state",
        "freshness_or_revalidation_trigger",
        "does_not_prove",
        "review_basis",
        "satisfies_knowledge_inputs",
    }
    allowed_roles = {"PRIMARY", "SUPPORTING", "CONDITIONAL", "CONTEXT", "COUNTEREVIDENCE"}
    allowed_oe = {"OE1", "OE2", "OE3", "OE1_NOT_ELIGIBLE", "OE2_CONDITIONAL", "OE3_ELIGIBLE"}
    allowed_fresh = {"CURRENT", "REVALIDATED_CURRENT"}

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            hold_reasons.append(f"KNOWLEDGE_MOUNT_RECORD_NOT_OBJECT:{index}")
            continue
        missing = sorted(required_fields - set(record))
        if missing:
            hold_reasons.append(
                f"KNOWLEDGE_MOUNT_RECORD_MISSING_FIELDS:{index}:{','.join(missing)}"
            )
            continue
        role = str(record.get("use_role") or "")
        oe = str(record.get("operational_eligibility") or "")
        freshness = str(record.get("freshness_state") or "")
        satisfies = [str(x) for x in record.get("satisfies_knowledge_inputs") or []]
        if role not in allowed_roles:
            hold_reasons.append(f"KNOWLEDGE_MOUNT_USE_ROLE_INVALID:{index}:{role}")
        if oe not in allowed_oe:
            hold_reasons.append(f"KNOWLEDGE_MOUNT_OE_INVALID:{index}:{oe}")
        if freshness not in allowed_fresh:
            hold_reasons.append(f"KNOWLEDGE_MOUNT_FRESHNESS_REVALIDATION_REQUIRED:{index}:{freshness}")
        if oe in {"OE1", "OE1_NOT_ELIGIBLE"}:
            hold_reasons.append(f"KNOWLEDGE_MOUNT_NOT_ELIGIBLE:{index}:{record.get('knowledge_ref')}")
        if not isinstance(record.get("conditions"), list):
            hold_reasons.append(f"KNOWLEDGE_MOUNT_CONDITIONS_NOT_ARRAY:{index}")
        if not isinstance(record.get("unresolved_items"), list):
            hold_reasons.append(f"KNOWLEDGE_MOUNT_UNRESOLVED_ITEMS_NOT_ARRAY:{index}")
        if not isinstance(record.get("does_not_prove"), list) or not record.get("does_not_prove"):
            hold_reasons.append(f"KNOWLEDGE_MOUNT_DOES_NOT_PROVE_REQUIRED:{index}")
        unknown_satisfies = sorted(set(satisfies) - set(active_inputs))
        if unknown_satisfies:
            hold_reasons.append(
                f"KNOWLEDGE_MOUNT_COVERS_UNDECLARED_ACTIVE_INPUT:{index}:{','.join(unknown_satisfies)}"
            )
        record_usable = (
            oe in {"OE2", "OE3", "OE2_CONDITIONAL", "OE3_ELIGIBLE"}
            and freshness in allowed_fresh
            and not missing
        )
        for knowledge_input in satisfies:
            if knowledge_input in coverage and record_usable:
                coverage[knowledge_input].append(str(record.get("knowledge_ref") or ""))
        normalized_records.append({
            "knowledge_ref": record.get("knowledge_ref"),
            "use_role": role,
            "operational_eligibility": oe,
            "eligibility_scope": record.get("eligibility_scope"),
            "claim_ceiling": record.get("claim_ceiling"),
            "applicability": record.get("applicability"),
            "conditions": record.get("conditions"),
            "unresolved_items": record.get("unresolved_items"),
            "freshness_state": freshness,
            "freshness_or_revalidation_trigger": record.get("freshness_or_revalidation_trigger"),
            "does_not_prove": record.get("does_not_prove"),
            "review_basis": record.get("review_basis"),
            "satisfies_knowledge_inputs": satisfies,
            "usable_for_declared_scope": record_usable,
        })

    for knowledge_input, refs in coverage.items():
        if not refs:
            hold_reasons.append(f"ACTIVE_KNOWLEDGE_INPUT_NOT_COVERED:{knowledge_input}")

    return {
        "gate": "HOLD" if hold_reasons else "PASS",
        "contract_ref": str(KNOWLEDGE_MOUNT_CONTRACT.relative_to(ROOT)).replace("\\", "/"),
        "knowledge_mount_requirement": stage.get("knowledge_mount_requirement"),
        "declared_knowledge_inputs": declared_inputs,
        "active_knowledge_inputs": active_inputs,
        "omitted_knowledge_inputs": omitted,
        "mount_records": normalized_records,
        "active_input_coverage": coverage,
        "hold_reasons": list(dict.fromkeys(hold_reasons)),
        "does_not_prove": [
            "KNOWLEDGE_CLEAN_IMPLIES_UNIVERSAL_ELIGIBILITY",
            "OPERATIONAL_ELIGIBILITY_IMPLIES_DESIGN_KEEP",
            "OPERATIONAL_ELIGIBILITY_IMPLIES_PROFESSIONAL_PASS",
        ],
    }


def _valid_project_binding(binding: dict | None, *, expected_class: str) -> bool:
    if not isinstance(binding, dict):
        return False
    if str(binding.get("owner_id") or "").strip() == "":
        return False
    if str(binding.get("authority_ref") or "").strip() == "":
        return False
    if binding.get("callable") is not True:
        return False
    if str(binding.get("owner_class") or "") != expected_class:
        return False
    return True


def evaluate_professional_stage_composition(
    spec: dict | None,
    *,
    closure_requested: bool = False,
) -> dict | None:
    """Resolve one professional stage's capability roles into the existing owner map."""
    if spec is None:
        return None
    process_ref = str(spec.get("process_ref") or "").strip().replace("\\", "/")
    stage_id = str(spec.get("stage_id") or "").strip()
    if not process_ref or not stage_id:
        raise ValueError("professional_stage_execution requires process_ref and stage_id")

    row, process_mode = _professional_machine_row(process_ref)
    process_path = (ROOT / process_ref).resolve()
    if not process_path.is_file() or ROOT.resolve() not in process_path.parents:
        raise ValueError(f"professional process_ref is not a readable repository file: {process_ref}")
    machine = _load_json(process_path)
    stage = next((s for s in machine.get("stages") or [] if s.get("stage_id") == stage_id), None)
    if not isinstance(stage, dict):
        raise ValueError(f"stage_id {stage_id} not found in {process_ref}")

    professional_question = str(stage.get("professional_question") or "").strip()
    if not professional_question:
        raise ValueError(f"{stage_id} has no professional_question")
    stage_instance_readback = dict(spec.get("stage_instance_readback") or {})
    if stage_instance_readback:
        readback_stage_id = str(stage_instance_readback.get("stage_id") or "")
        if readback_stage_id and readback_stage_id != stage_id:
            raise ValueError(
                f"stage_instance_readback stage_id {readback_stage_id} does not match {stage_id}"
            )
    decision_object_refs = [
        str(x)
        for x in (
            stage_instance_readback.get("decision_object_refs")
            or spec.get("decision_object_refs")
            or []
        )
    ]

    candidate_binding = None
    hold_reasons: list[str] = []
    if process_mode == "CANDIDATE":
        requested_mode = str(spec.get("candidate_evaluation_mode") or "")
        required_mode = str(row.get("candidate_evaluation_mode") or "")
        if requested_mode != required_mode or required_mode != "BOUNDED_NON_CURRENT_PROJECT_EXERCISE":
            hold_reasons.append("CANDIDATE_REQUIRES_EXPLICIT_BOUNDED_NON_CURRENT_PROJECT_EXERCISE")
        if row.get("state") != "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN" or row.get("current_process_ref") is not None:
            hold_reasons.append("CANDIDATE_GRAPH_AUTHORITY_BOUNDARY_DRIFT")
        evolution_ref = str(row.get("candidate_evolution_ref") or "")
        if not evolution_ref:
            hold_reasons.append("CANDIDATE_EVOLUTION_REF_MISSING")
        else:
            evolution_path = ROOT / evolution_ref
            evolution = _load_json(evolution_path)
            machine_sha256 = hashlib.sha256(process_path.read_bytes()).hexdigest()
            binding = dict(evolution.get("candidate_definition_binding") or {})
            if evolution.get("target_ref") != process_ref or binding.get("machine_ref") != process_ref:
                hold_reasons.append("CANDIDATE_EVOLUTION_TARGET_BINDING_MISMATCH")
            if binding.get("machine_sha256") != machine_sha256:
                hold_reasons.append("CANDIDATE_EVOLUTION_MACHINE_HASH_STALE")
            if evolution.get("state") == "EVR_REJECTED":
                hold_reasons.append("CANDIDATE_EVOLUTION_REJECTED")
            candidate_binding = {
                "domain": row.get("domain"),
                "graph_state": row.get("state"),
                "current_process_ref": row.get("current_process_ref"),
                "candidate_evolution_ref": evolution_ref,
                "candidate_evolution_state": evolution.get("state"),
                "machine_sha256": machine_sha256,
                "evaluation_mode": required_mode,
            }

    owner_map = _load_json(OWNER_MAP)
    requirements, requirements_source = _stage_execution_requirements(
        process_ref=process_ref,
        process_mode=process_mode,
        process_path=process_path,
        stage=stage,
        owner_map=owner_map,
    )
    required_roles = [str(x) for x in requirements.get("required_capability_roles") or []]
    supporting_roles = [str(x) for x in requirements.get("supporting_capability_roles") or []]
    if not required_roles:
        raise ValueError(f"{stage_id} has no required_capability_roles")

    active_supporting = [str(x) for x in spec.get("active_supporting_capability_roles") or []]
    unknown_supporting = sorted(set(active_supporting) - set(supporting_roles))
    if unknown_supporting:
        raise ValueError(f"active supporting roles are not declared by {stage_id}: {unknown_supporting}")
    omitted_reasons = {
        str(k): str(v).strip()
        for k, v in dict(spec.get("omitted_supporting_reasons") or {}).items()
    }
    omitted_supporting: list[dict] = []
    for role in supporting_roles:
        if role in active_supporting:
            continue
        reason = omitted_reasons.get(role, "")
        if not reason:
            hold_reasons.append(f"SUPPORTING_CAPABILITY_OMISSION_REASON_REQUIRED:{role}")
        omitted_supporting.append({"capability_role": role, "reason": reason or None})

    knowledge_mount_readback = _evaluate_stage_knowledge_mounts(stage, spec)
    hold_reasons.extend(
        f"KNOWLEDGE:{reason}" for reason in knowledge_mount_readback.get("hold_reasons", [])
    )
    owner_contracts = _owner_contract_map()
    project_bindings = dict(spec.get("project_owner_bindings") or {})
    reviewer_binding = spec.get("independent_reviewer_binding")
    unavailable_owner_ids = {str(x) for x in spec.get("unavailable_owner_ids") or []}
    active_roles = required_roles + active_supporting
    coverage: list[dict] = []
    resolved_owner_ids: list[str] = []
    reusable_skill_owner_ids: list[str] = []
    producer_owner_ids: list[str] = []
    reviewer_owner_ids: list[str] = []

    for role in active_roles:
        rule = _stage_capability_rule(role, owner_map)
        rule_id = str(rule.get("rule_id") or "")
        resolution_class = str(rule.get("resolution_class") or "")
        owner_ids: list[str] = []
        state = "RESOLVED"
        reason = None

        if resolution_class == "INDEPENDENT_REVIEWER_REQUIRED":
            if not _valid_project_binding(
                reviewer_binding if isinstance(reviewer_binding, dict) else None,
                expected_class="INDEPENDENT_REVIEWER",
            ):
                state = "HOLD"
                reason = "INDEPENDENT_REVIEWER_BINDING_REQUIRED"
            elif str(reviewer_binding.get("independence_state") or "") != "INDEPENDENT":
                state = "HOLD"
                reason = "INDEPENDENT_REVIEWER_BINDING_NOT_INDEPENDENT"
            else:
                owner_ids = [str(reviewer_binding["owner_id"])]
                reviewer_owner_ids.extend(owner_ids)
        elif resolution_class in {"PROJECT_OR_SPECIALIST_OWNER_REQUIRED", "NO_DEDICATED_OWNER_HOLD"}:
            project_binding = project_bindings.get(role)
            if not _valid_project_binding(
                project_binding if isinstance(project_binding, dict) else None,
                expected_class="PROJECT_SPECIALIST",
            ):
                state = "HOLD"
                reason = "PROJECT_OR_SPECIALIST_OWNER_BINDING_REQUIRED"
            else:
                owner_ids = [str(project_binding["owner_id"])]
                producer_owner_ids.extend(owner_ids)
        else:
            explicit_project_binding = project_bindings.get(role)
            if _valid_project_binding(
                explicit_project_binding if isinstance(explicit_project_binding, dict) else None,
                expected_class="PROJECT_SPECIALIST",
            ):
                owner_ids = [str(explicit_project_binding["owner_id"])]
                producer_owner_ids.extend(owner_ids)
            else:
                declared_owner_refs = [str(x) for x in rule.get("owner_refs") or []]
                for owner_id in declared_owner_refs:
                    owner = owner_contracts.get(owner_id)
                    if owner is None:
                        state = "HOLD"
                        reason = f"OWNER_NOT_IN_CURRENT_CAPABILITY_CONTRACT:{owner_id}"
                        break
                    if owner_id in unavailable_owner_ids:
                        state = "HOLD"
                        reason = f"OWNER_UNAVAILABLE:{owner_id}"
                        break
                    routing_state = str(owner.get("routing_state") or "")
                    implementation_paths = owner.get("implementation_paths") or []
                    if resolution_class == "EXISTING_OWNER" and routing_state != "INSTALLED_OWNER":
                        state = "HOLD"
                        reason = f"OWNER_NOT_INSTALLED:{owner_id}"
                        break
                    if resolution_class == "CANDIDATE_OWNER":
                        state = "HOLD"
                        reason = f"CANDIDATE_OWNER_NOT_CURRENT_CALLABLE:{owner_id}"
                        break
                    if resolution_class == "CANDIDATE_BODY_REQUIRES_CALLABILITY":
                        if routing_state != "CANDIDATE_BODY" or not implementation_paths:
                            state = "HOLD"
                            reason = f"CANDIDATE_BODY_NOT_CALLABLE:{owner_id}"
                            break
                    if not implementation_paths:
                        state = "HOLD"
                        reason = f"OWNER_HAS_NO_IMPLEMENTATION_PATH:{owner_id}"
                        break
                    owner_ids.append(owner_id)
                    reusable_skill_owner_ids.append(owner_id)
                    producer_owner_ids.append(owner_id)

        if state == "HOLD":
            hold_reasons.append(f"{role}:{reason}")
        else:
            resolved_owner_ids.extend(owner_ids)
        coverage.append({
            "capability_role": role,
            "required_or_supporting": "REQUIRED" if role in required_roles else "SUPPORTING",
            "routing_rule_id": rule_id,
            "resolution_class": resolution_class,
            "state": state,
            "owner_ids": owner_ids,
            "reason": reason,
        })

    producer_set = set(producer_owner_ids)
    reviewer_set = set(reviewer_owner_ids)
    if producer_set.intersection(reviewer_set):
        hold_reasons.append("INDEPENDENT_REVIEWER_COLLAPSED_INTO_PRODUCER")

    unique_owner_ids = list(dict.fromkeys(resolved_owner_ids))
    unique_skill_owner_ids = list(dict.fromkeys(reusable_skill_owner_ids))
    multi_skill_required = len(unique_owner_ids) > 1
    declared_native_outputs = [str(x) for x in stage.get("required_native_outputs") or []]
    actual_outputs = [str(x) for x in stage_instance_readback.get("outputs") or []]
    output_execution_bindings = [
        dict(x)
        for x in stage_instance_readback.get("output_execution_bindings") or []
        if isinstance(x, dict)
    ]
    decision_bound = (
        str(stage_instance_readback.get("granularity_binding_state") or "")
        == "DECISION_OBJECT_BOUND"
    )
    readback_complete_native_outputs = {
        str(binding.get("required_native_output") or "")
        for binding in output_execution_bindings
        if binding.get("resolution_state") == "READBACK_COMPLETE"
        and binding.get("artifact_refs")
        and binding.get("readback_refs")
    }
    missing_readback_complete_native_outputs = sorted(
        set(declared_native_outputs) - readback_complete_native_outputs
    )
    actual_readback_refs = [
        str(x) for x in stage_instance_readback.get("actual_readback_refs") or []
    ]
    review_refs = [str(x) for x in stage_instance_readback.get("review_refs") or []]
    review_verdict = str(stage_instance_readback.get("review_verdict") or "NOT_RUN")
    exit_condition_state = str(
        stage_instance_readback.get("exit_condition_state") or "NOT_EVALUATED"
    )

    closure_hold_reasons: list[str] = []
    if closure_requested:
        if not decision_object_refs:
            closure_hold_reasons.append("DECISION_OBJECT_REF_REQUIRED_FOR_STAGE_CLOSURE")
        if decision_bound:
            if missing_readback_complete_native_outputs:
                closure_hold_reasons.append(
                    "NATIVE_OUTPUT_BINDINGS_NOT_READBACK_COMPLETE_FOR_STAGE_CLOSURE:"
                    + ",".join(missing_readback_complete_native_outputs)
                )
        elif not actual_outputs:
            closure_hold_reasons.append("NATIVE_OUTPUTS_REQUIRED_FOR_STAGE_CLOSURE")
        if not actual_readback_refs:
            closure_hold_reasons.append("ACTUAL_READBACK_REQUIRED_FOR_STAGE_CLOSURE")
        if not review_refs:
            closure_hold_reasons.append("INDEPENDENT_REVIEW_REF_REQUIRED_FOR_STAGE_CLOSURE")
        if review_verdict != "PASS":
            closure_hold_reasons.append(
                f"INDEPENDENT_REVIEW_PASS_REQUIRED_FOR_STAGE_CLOSURE:{review_verdict}"
            )
        if not _valid_project_binding(
            reviewer_binding if isinstance(reviewer_binding, dict) else None,
            expected_class="INDEPENDENT_REVIEWER",
        ):
            closure_hold_reasons.append(
                "INDEPENDENT_REVIEWER_BINDING_REQUIRED_FOR_STAGE_CLOSURE"
            )
        elif str(reviewer_binding.get("independence_state") or "") != "INDEPENDENT":
            closure_hold_reasons.append(
                "INDEPENDENT_REVIEWER_NOT_INDEPENDENT_FOR_STAGE_CLOSURE"
            )
        elif str(reviewer_binding.get("owner_id") or "") in producer_set:
            closure_hold_reasons.append(
                "INDEPENDENT_REVIEWER_COLLAPSED_INTO_PRODUCER_FOR_STAGE_CLOSURE"
            )
        if exit_condition_state != "SATISFIED":
            closure_hold_reasons.append(
                f"STAGE_EXIT_CONDITIONS_NOT_SATISFIED:{exit_condition_state}"
            )
    hold_reasons.extend(closure_hold_reasons)
    gate = "HOLD" if hold_reasons else "PASS"
    stage_closure_gate = (
        "PASS"
        if closure_requested and not closure_hold_reasons and gate == "PASS"
        else "HOLD"
        if closure_requested
        else "NOT_EVALUATED"
    )
    canonical_execution_chain = [
        {"step": "PROFESSIONAL_STAGE", "state": "RESOLVED", "value": stage_id},
        {
            "step": "PROFESSIONAL_QUESTION_OR_DECISION_OBJECT",
            "state": "RESOLVED" if professional_question else "HOLD",
            "professional_question": professional_question,
            "decision_object_refs": decision_object_refs,
        },
        {
            "step": "KNOWLEDGE_INPUTS",
            "state": "RESOLVED" if knowledge_mount_readback.get("declared_knowledge_inputs") else "HOLD",
            "values": knowledge_mount_readback.get("active_knowledge_inputs"),
        },
        {
            "step": "OPERATIONAL_KNOWLEDGE_MOUNT",
            "state": knowledge_mount_readback.get("gate"),
            "mount_refs": [
                item.get("knowledge_ref")
                for item in knowledge_mount_readback.get("mount_records", [])
                if item.get("knowledge_ref")
            ],
        },
        {
            "step": "REQUIRED_CAPABILITY_ROLES",
            "state": "RESOLVED" if required_roles else "HOLD",
            "values": required_roles,
        },
        {
            "step": "CURRENT_EXECUTION_OWNERS_OR_SKILLS",
            "state": "HOLD" if any(x.get("state") == "HOLD" for x in coverage) else "RESOLVED",
            "owner_ids": unique_owner_ids,
        },
        {
            "step": "NATIVE_OUTPUTS",
            "state": (
                "READBACK_COMPLETE"
                if decision_bound and not missing_readback_complete_native_outputs
                else "READBACK_BOUND"
                if actual_outputs
                else "DECLARED"
            ),
            "required": declared_native_outputs,
            "actual": actual_outputs,
            "readback_complete_native_outputs": sorted(readback_complete_native_outputs),
            "missing_readback_complete_native_outputs": missing_readback_complete_native_outputs,
        },
        {
            "step": "ACTUAL_READBACK",
            "state": "PASS" if actual_readback_refs else "NOT_RUN",
            "refs": actual_readback_refs,
        },
        {
            "step": "INDEPENDENT_REVIEW",
            "state": review_verdict,
            "refs": review_refs,
            "reviewer_owner_ids": list(dict.fromkeys(reviewer_owner_ids)),
        },
        {
            "step": "STAGE_CLOSURE",
            "state": stage_closure_gate,
            "exit_condition_state": exit_condition_state,
        },
    ]
    return {
        "gate": gate,
        "action": (
            "HOLD_STAGE_CLOSURE_CHAIN"
            if closure_requested and closure_hold_reasons
            else "HOLD_PROFESSIONAL_STAGE_EXECUTION_CHAIN"
            if gate == "HOLD"
            else "PROFESSIONAL_STAGE_EXECUTION_CHAIN_READY"
        ),
        "process_ref": process_ref,
        "process_mode": process_mode,
        "domain": row.get("domain"),
        "stage_id": stage_id,
        "stage_name": stage.get("stage_name"),
        "professional_question": professional_question,
        "decision_object_refs": decision_object_refs,
        "canonical_stage_execution_chain": list(CANONICAL_PROFESSIONAL_STAGE_EXECUTION_CHAIN),
        "canonical_stage_execution_readback": canonical_execution_chain,
        "stage_execution_requirements_source": requirements_source,
        "candidate_binding": candidate_binding,
        "knowledge_mount_readback": knowledge_mount_readback,
        "required_capability_roles": required_roles,
        "declared_supporting_capability_roles": supporting_roles,
        "active_supporting_capability_roles": active_supporting,
        "omitted_supporting_capabilities": omitted_supporting,
        "capability_coverage": coverage,
        "resolved_owner_set": unique_owner_ids,
        "reusable_skill_owner_ids": unique_skill_owner_ids,
        "project_or_specialist_owner_ids": sorted(producer_set - set(unique_skill_owner_ids)),
        "independent_reviewer_owner_ids": list(dict.fromkeys(reviewer_owner_ids)),
        "required_native_outputs": declared_native_outputs,
        "actual_native_outputs": actual_outputs,
        "actual_readback_refs": actual_readback_refs,
        "independent_review_refs": review_refs,
        "independent_review_verdict": review_verdict,
        "stage_exit_condition_state": exit_condition_state,
        "stage_closure_gate": stage_closure_gate,
        "multi_skill_dag_required": multi_skill_required,
        "typed_handoff_required": multi_skill_required,
        "hold_reasons": list(dict.fromkeys(hold_reasons)),
        "does_not_prove": [
            "PROFESSIONAL_PASS",
            "DESIGN_KEEP",
            "FIELD_TRUTH",
            "STATUTORY_APPROVAL",
            "CANDIDATE_ADOPTION",
        ],
    }


def _closure_requested(payload: dict, flow_completion: dict | None) -> bool:
    intent = str(payload.get("intent") or "").strip().upper()
    if bool(payload.get("completion_claim_requested")):
        return True
    if intent in CLOSURE_INTENTS:
        return True
    if flow_completion and flow_completion.get("completion_gate") == "PASS":
        return True
    return False


def evaluate_skill_consumption(evidence: dict | None, *, closure_requested: bool) -> dict | None:
    """Fail closed at closure unless the Current canonical Skill implementations were actually read."""
    if evidence is None:
        if not closure_requested:
            return None
        return {
            "gate": "HOLD",
            "action": "HOLD_SKILL_CONSUMPTION_EVIDENCE_REQUIRED",
            "missing_owner_ids": [],
            "missing_canonical_reads": [],
            "reason": "CLOSURE_REQUIRES_SKILL_CONSUMPTION_EVIDENCE",
        }

    required_owner_ids = [str(x) for x in evidence.get("required_owner_ids") or []]
    resolution_state = str(evidence.get("resolution_state") or "")
    if not required_owner_ids:
        if resolution_state in {"NO_DEDICATED_OWNER", "NO_SKILL_REQUIRED"}:
            return {
                "gate": "PASS",
                "action": "SKILL_CONSUMPTION_NOT_APPLICABLE_WITH_EXPLICIT_RESOLUTION",
                "required_owner_ids": [],
                "resolved_owners": [],
            }
        return {
            "gate": "HOLD",
            "action": "HOLD_SKILL_CONSUMPTION",
            "missing_owner_ids": [],
            "missing_canonical_reads": [],
            "reason": "OWNER_SET_OR_EXPLICIT_NO_OWNER_RESOLUTION_REQUIRED",
        }

    owners = _owner_contract_map()
    actual_read_paths = {str(path) for path in evidence.get("actual_read_paths") or []}
    claimed_states = {
        str(k): str(v)
        for k, v in dict(evidence.get("claimed_lifecycle_states") or {}).items()
    }
    missing_owner_ids: list[str] = []
    missing_canonical_reads: list[dict] = []
    lifecycle_mismatches: list[dict] = []
    resolved_owners: list[dict] = []

    for owner_id in required_owner_ids:
        owner = owners.get(owner_id)
        if owner is None:
            missing_owner_ids.append(owner_id)
            continue
        implementation_paths = [str(path) for path in owner.get("implementation_paths") or []]
        skill_paths = [path for path in implementation_paths if path.endswith("/SKILL.md")]
        canonical_read_paths = skill_paths or implementation_paths
        matched_reads = sorted(set(canonical_read_paths).intersection(actual_read_paths))
        if not matched_reads:
            missing_canonical_reads.append({
                "owner_id": owner_id,
                "expected_one_of": canonical_read_paths,
            })
        claimed = claimed_states.get(owner_id)
        actual_state = str(owner.get("lifecycle_state") or "")
        if claimed and claimed != actual_state:
            lifecycle_mismatches.append({
                "owner_id": owner_id,
                "claimed": claimed,
                "current": actual_state,
            })
        resolved_owners.append({
            "owner_id": owner_id,
            "lifecycle_state": actual_state,
            "routing_state": owner.get("routing_state"),
            "canonical_read_paths": matched_reads,
            "candidate_boundary": actual_state == "CANDIDATE",
        })

    if missing_owner_ids or lifecycle_mismatches:
        return {
            "gate": "FAIL",
            "action": "REVISE_SKILL_CONSUMPTION",
            "required_owner_ids": required_owner_ids,
            "resolved_owners": resolved_owners,
            "missing_owner_ids": missing_owner_ids,
            "missing_canonical_reads": missing_canonical_reads,
            "lifecycle_mismatches": lifecycle_mismatches,
            "reason": "CURRENT_OWNER_IDENTITY_OR_LIFECYCLE_MISMATCH",
        }
    if missing_canonical_reads:
        return {
            "gate": "HOLD",
            "action": "HOLD_SKILL_CONSUMPTION",
            "required_owner_ids": required_owner_ids,
            "resolved_owners": resolved_owners,
            "missing_owner_ids": [],
            "missing_canonical_reads": missing_canonical_reads,
            "lifecycle_mismatches": [],
            "reason": "CURRENT_CANONICAL_SKILL_NOT_ACTUALLY_READ",
        }
    return {
        "gate": "PASS",
        "action": "SKILL_CONSUMPTION_VERIFIED",
        "required_owner_ids": required_owner_ids,
        "resolved_owners": resolved_owners,
        "missing_owner_ids": [],
        "missing_canonical_reads": [],
        "lifecycle_mismatches": [],
        "does_not_prove": ["SKILL_PROMOTION", "DESIGN_QUALITY", "FINAL_KEEP"],
    }


def _quality_record(value) -> tuple[str, list[str], str | None]:
    if isinstance(value, str):
        return value, [], None
    if not isinstance(value, dict):
        return "", [], None
    evidence_classes = value.get("evidence_classes")
    if evidence_classes is None and value.get("evidence_class") is not None:
        evidence_classes = [value.get("evidence_class")]
    return (
        str(value.get("result") or ""),
        [str(x) for x in (evidence_classes or [])],
        str(value.get("reason")) if value.get("reason") else None,
    )


def evaluate_quality_acceptance(evidence: dict | None, *, closure_requested: bool) -> dict | None:
    """Separate professional quality from structure/persistence/readback existence evidence."""
    if evidence is None:
        if not closure_requested:
            return None
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE_EVIDENCE_REQUIRED",
            "reason": "CLOSURE_REQUIRES_EXPLICIT_QUALITY_ACCEPTANCE_OR_NOT_APPLICABLE_REASON",
        }

    if evidence.get("applicable") is False:
        reason = str(evidence.get("not_applicable_reason") or "").strip()
        if reason:
            return {
                "gate": "PASS",
                "action": "QUALITY_ACCEPTANCE_NOT_APPLICABLE",
                "not_applicable_reason": reason,
            }
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE",
            "reason": "NOT_APPLICABLE_REQUIRES_REASON",
        }

    required_dimensions = [str(x) for x in evidence.get("required_dimensions") or []]
    gate_results = dict(evidence.get("gate_results") or {})
    if not required_dimensions:
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE",
            "reason": "TASK_DERIVED_REQUIRED_QUALITY_DIMENSIONS_MISSING",
            "incomplete_dimensions": [],
        }

    incomplete_dimensions: list[str] = []
    failed_dimensions: list[str] = []
    weak_evidence_dimensions: list[str] = []
    not_applicable_without_reason: list[str] = []
    normalized_results: dict[str, dict] = {}

    for dimension in required_dimensions:
        result, evidence_classes, reason = _quality_record(gate_results.get(dimension))
        normalized_results[dimension] = {
            "result": result,
            "evidence_classes": evidence_classes,
            "reason": reason,
        }
        if result == "FAIL":
            failed_dimensions.append(dimension)
            continue
        if result in {"", "HOLD"}:
            incomplete_dimensions.append(dimension)
            continue
        if result == "NOT_APPLICABLE":
            if not reason:
                not_applicable_without_reason.append(dimension)
            continue
        if result != "PASS":
            incomplete_dimensions.append(dimension)
            continue
        if not evidence_classes:
            incomplete_dimensions.append(dimension)
            continue
        if dimension not in STRUCTURAL_DIMENSIONS and set(evidence_classes).issubset(STRUCTURAL_EVIDENCE_CLASSES):
            weak_evidence_dimensions.append(dimension)

    professional_dimensions = [d for d in required_dimensions if d not in STRUCTURAL_DIMENSIONS]
    scope_coverage_confirmed = evidence.get("scope_coverage_confirmed") is True
    independent_review_required = bool(evidence.get("independent_review_required", False)) or bool(professional_dimensions)
    review = evidence.get("independent_review") if isinstance(evidence.get("independent_review"), dict) else {}
    reviewer_role = str(review.get("reviewer_role") or "").upper()
    review_verdict = str(review.get("verdict") or "").upper()
    producer_self_promotion = bool(evidence.get("producer_self_promotion")) or reviewer_role in {
        "PRODUCER",
        "SAME_EXECUTOR",
        "SELF",
    }
    independent_review_missing = independent_review_required and (
        review_verdict != "PASS" or not reviewer_role or producer_self_promotion
    )

    if producer_self_promotion or failed_dimensions:
        return {
            "gate": "FAIL",
            "action": "REVISE_QUALITY_ACCEPTANCE",
            "required_dimensions": required_dimensions,
            "gate_results": normalized_results,
            "failed_dimensions": failed_dimensions,
            "incomplete_dimensions": incomplete_dimensions,
            "weak_evidence_dimensions": weak_evidence_dimensions,
            "not_applicable_without_reason": not_applicable_without_reason,
            "scope_coverage_confirmed": scope_coverage_confirmed,
            "independent_review_missing": independent_review_missing,
            "producer_self_promotion": producer_self_promotion,
            "reason": "PROFESSIONAL_QUALITY_FAIL_OR_SELF_PROMOTION",
        }

    if (
        incomplete_dimensions
        or weak_evidence_dimensions
        or not_applicable_without_reason
        or not scope_coverage_confirmed
        or independent_review_missing
    ):
        return {
            "gate": "HOLD",
            "action": "HOLD_QUALITY_ACCEPTANCE",
            "required_dimensions": required_dimensions,
            "gate_results": normalized_results,
            "failed_dimensions": [],
            "incomplete_dimensions": incomplete_dimensions,
            "weak_evidence_dimensions": weak_evidence_dimensions,
            "not_applicable_without_reason": not_applicable_without_reason,
            "scope_coverage_confirmed": scope_coverage_confirmed,
            "independent_review_missing": independent_review_missing,
            "producer_self_promotion": False,
            "reason": "PROFESSIONAL_QUALITY_EVIDENCE_INCOMPLETE_OR_SCOPE_TOO_NARROW",
        }

    return {
        "gate": "PASS",
        "action": "QUALITY_ACCEPTANCE_VERIFIED",
        "required_dimensions": required_dimensions,
        "gate_results": normalized_results,
        "scope_coverage_confirmed": True,
        "independent_review_missing": False,
        "producer_self_promotion": False,
        "does_not_prove": ["FIELD_TRUTH", "ENGINEERING_APPROVAL", "HUMAN_TEST_PASS_UNLESS_EXPLICITLY_GATED"],
    }


def _directive(
    *,
    frontier: dict | None,
    checkpoint_resume: dict | None,
    mutation_guard: dict | None,
    professional_stage_composition: dict | None,
    skill_consumption: dict | None,
    quality_acceptance: dict | None,
    flow_completion: dict | None,
    auto_advance: dict | None,
) -> dict:
    """Compile existing Resolver decisions into a transient conversation directive."""
    if checkpoint_resume and checkpoint_resume.get("action") == "DO_NOT_REOPEN_CLOSED_TASK":
        return {"action": "STOP_CLOSED_TASK", "target": None, "basis": "CONTINUATION_CHECKPOINT"}

    if mutation_guard and mutation_guard.get("allowed") is False:
        return {
            "action": mutation_guard.get("action", "REFRESH_FRONTIER_BEFORE_MUTATION"),
            "target": None,
            "basis": "CHECKPOINT_SEQUENCE_GUARD",
        }

    if frontier:
        frontier_action = frontier.get("action", "")
        if frontier_action.startswith("HOLD_") or frontier_action.startswith("REVALIDATE_"):
            return {"action": frontier_action, "target": None, "basis": "FRONTIER_RESOLVER"}

    if checkpoint_resume:
        resume_action = checkpoint_resume.get("action", "")
        if resume_action.startswith("HOLD_") or resume_action.startswith("REVALIDATE_"):
            return {
                "action": resume_action,
                "target": checkpoint_resume.get("target"),
                "basis": "CONTINUATION_CHECKPOINT",
            }

    if professional_stage_composition and professional_stage_composition.get("gate") != "PASS":
        return {
            "action": professional_stage_composition.get(
                "action", "HOLD_STAGE_CAPABILITY_OWNER_RESOLUTION"
            ),
            "target": professional_stage_composition.get("stage_id"),
            "basis": "PROFESSIONAL_STAGE_EXECUTION_CHAIN",
        }

    if skill_consumption and skill_consumption.get("gate") != "PASS":
        return {
            "action": skill_consumption.get("action", "HOLD_SKILL_CONSUMPTION"),
            "target": None,
            "basis": "SKILL_CONSUMPTION_GATE",
        }

    if quality_acceptance and quality_acceptance.get("gate") != "PASS":
        return {
            "action": quality_acceptance.get("action", "HOLD_QUALITY_ACCEPTANCE"),
            "target": None,
            "basis": "PROFESSIONAL_QUALITY_ACCEPTANCE_GATE",
        }

    if flow_completion and flow_completion.get("completion_gate") == "PASS":
        return {"action": "STOP_FLOW_COMPLETION_GATE_PASS", "target": None, "basis": "FLOW_COMPLETION_GATE"}

    if auto_advance:
        if auto_advance.get("continue_allowed") is True:
            return {
                "action": auto_advance.get("action", "AUTO_ADVANCE_NEXT_READY_NODE"),
                "target": auto_advance.get("target"),
                "basis": "CONTINUOUS_EXECUTION_POLICY",
            }
        auto_action = auto_advance.get("action", "")
        if auto_action and auto_action != "HOLD_NO_READY_NODE_BEFORE_FLOW_COMPLETION":
            return {"action": auto_action, "target": auto_advance.get("target"), "basis": "CONTINUOUS_EXECUTION_POLICY"}

    if checkpoint_resume and checkpoint_resume.get("action") == "RESUME_NEXT_ALLOWED_ACTION":
        return {
            "action": "EXECUTE_NEXT_ALLOWED_ACTION",
            "target": checkpoint_resume.get("target"),
            "basis": "CONTINUATION_CHECKPOINT",
        }

    if frontier and frontier.get("action") == "RESUME_FROM_DISCOVERED_FRONTIER":
        return {
            "action": "LOAD_SELECTED_FRONTIER_CHECKPOINT",
            "target": frontier.get("selected_frontier"),
            "basis": "FRONTIER_RESOLVER",
        }

    return {"action": "PROCEED_WITH_EXISTING_OLEANDER_PREFLIGHT", "target": None, "basis": "RESOLVER"}


def run_preflight(payload: dict) -> dict:
    """Run a side-effect-free OLEANDER conversation preflight over caller-supplied Current evidence."""
    resolver = validate_resolver()
    identity = {
        "adapter_id": ADAPTER_ID,
        "adapter_revision": ADAPTER_REVISION,
        "authority_ceiling": "EXECUTION_ADAPTER_ONLY",
        "state_owner": False,
        "resolver_path": "00-governance/runtime/OLEANDER_DEFAULT_SKILL_RESOLVER_v1.2.json",
        "resolver_version": resolver["version"],
        "resolver_implementation_revision": resolver["implementation_revision"],
        "resolver_status": resolver["status"],
    }

    frontier = None
    candidates = payload.get("candidate_frontiers")
    if candidates is not None:
        frontier = resolve_continuation_frontier(
            list(candidates),
            dict(payload.get("request_keys") or {}),
            payload.get("current_authority_fingerprint"),
            bool(payload.get("current_authority_identifies_one_active_task", True)),
        )

    checkpoint_resume = None
    checkpoint = payload.get("checkpoint")
    if checkpoint is not None:
        checkpoint_resume = decide_checkpoint_resume(
            dict(checkpoint),
            str(payload.get("current_authority_fingerprint") or ""),
        )

    constraint_lock = None
    if "constraint_sources" in payload:
        constraint_lock = resolve_sticky_constraints(list(payload.get("constraint_sources") or []))

    mutation_guard = None
    if "mutation_guard" in payload:
        guard = dict(payload.get("mutation_guard") or {})
        mutation_guard = guard_checkpoint_mutation(
            int(guard["current_sequence"]),
            int(guard["expected_sequence"]),
        )

    flow_completion = None
    if "flow_completion" in payload:
        flow_completion = evaluate_flow_completion(dict(payload.get("flow_completion") or {}))

    closure_requested = _closure_requested(payload, flow_completion)
    professional_stage_composition = evaluate_professional_stage_composition(
        dict(payload.get("professional_stage_execution"))
        if isinstance(payload.get("professional_stage_execution"), dict)
        else None,
        closure_requested=closure_requested,
    )
    skill_consumption = evaluate_skill_consumption(
        dict(payload.get("skill_consumption")) if isinstance(payload.get("skill_consumption"), dict) else None,
        closure_requested=closure_requested,
    )
    quality_acceptance = evaluate_quality_acceptance(
        dict(payload.get("quality_acceptance")) if isinstance(payload.get("quality_acceptance"), dict) else None,
        closure_requested=closure_requested,
    )

    auto_advance = None
    if "auto_advance" in payload:
        args = dict(payload.get("auto_advance") or {})
        if flow_completion is not None:
            args["flow_completion_gate"] = flow_completion["completion_gate"]
        auto_advance = decide_continuous_execution(**args)

    directive = _directive(
        frontier=frontier,
        checkpoint_resume=checkpoint_resume,
        mutation_guard=mutation_guard,
        professional_stage_composition=professional_stage_composition,
        skill_consumption=skill_consumption,
        quality_acceptance=quality_acceptance,
        flow_completion=flow_completion,
        auto_advance=auto_advance,
    )

    return {
        "adapter": identity,
        "intent": payload.get("intent"),
        "closure_requested": closure_requested,
        "frontier": frontier,
        "checkpoint_resume": checkpoint_resume,
        "constraint_lock": constraint_lock,
        "mutation_guard": mutation_guard,
        "professional_stage_composition": professional_stage_composition,
        "skill_consumption": skill_consumption,
        "quality_acceptance": quality_acceptance,
        "flow_completion": flow_completion,
        "auto_advance": auto_advance,
        "conversation_directive": directive,
        "does_not_prove": [
            "PROJECT_STATE",
            "DESIGN_QUALITY_WITHOUT_QUALITY_ACCEPTANCE_GATE",
            "ARTIFACT_CORRECTNESS",
            "COMPLETION_WITHOUT_FLOW_AND_ACCEPTANCE_EVIDENCE",
            "STRUCTURE_OR_PERSISTENCE_PASS_IS_PROFESSIONAL_KEEP",
            "OWNER_SET_RESOLUTION_IS_PROFESSIONAL_PASS",
        ],
    }


def _load_jsonl(path: Path) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        rows[row["case_id"]] = row
    return rows


def run_self_test() -> dict:
    """Exercise adapter composition against the existing runtime regression corpora."""
    locks = _load_jsonl(ROOT / "evals" / "runtime" / "sticky_constraints_and_flow.jsonl")
    cycles = _load_jsonl(ROOT / "evals" / "runtime" / "continuation_execution_cycle.jsonl")
    acceptance = _load_jsonl(ROOT / "evals" / "runtime" / "design_acceptance_guard.jsonl")

    checks: list[tuple[str, bool]] = []

    case = cycles["CYCLE-010-RAW-RECEIPT-CHECKPOINT-RESUMES"]
    result = run_preflight({
        "intent": "CONTINUE",
        "current_authority_fingerprint": case["current_authority_fingerprint"],
        "checkpoint": case["checkpoint"],
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == "EXECUTE_NEXT_ALLOWED_ACTION" and result["conversation_directive"]["target"] == case["expected_target"]))

    case = cycles["CYCLE-012-RAW-RECEIPT-CLOSED-NEVER-REOPENS"]
    result = run_preflight({
        "intent": "CONTINUE",
        "current_authority_fingerprint": case["current_authority_fingerprint"],
        "checkpoint": case["checkpoint"],
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == "STOP_CLOSED_TASK"))

    case = locks["RESUME-006-MULTIPLE-DISTINCT-FRONTIERS-HOLD"]
    result = run_preflight({
        "intent": "CONTINUE",
        "candidate_frontiers": case["candidate_frontiers"],
        "request_keys": {},
        "current_authority_identifies_one_active_task": case["current_authority_identifies_one_active_task"],
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == case["expected_action"]))

    case = locks["CONCURRENCY-002-SEQUENCE-MISMATCH-REVALIDATE"]
    result = run_preflight({
        "intent": "CONTINUE",
        "mutation_guard": {
            "current_sequence": case["current_sequence"],
            "expected_sequence": case["expected_sequence"],
        },
    })
    checks.append((case["case_id"], result["conversation_directive"]["action"] == case["expected_action"]))

    case = locks["CHAT-PREFLIGHT-001-GENERIC-CONTINUE-PRESERVES-STICKY"]
    result = run_preflight({"intent": "CONTINUE", "constraint_sources": case["constraint_sources"]})
    checks.append((case["case_id"], set(result["constraint_lock"]["active_constraints"]) == set(case["expected_active_constraints"])))

    case = locks["CHAT-PREFLIGHT-003-INCOMPLETE-FLOW-BLOCKS-COMPLETE"]
    result = run_preflight({"intent": "CONTINUE", "flow_completion": case["flow_completion"]})
    checks.append((case["case_id"], result["flow_completion"]["completion_gate"] == case["expected_completion_gate"] and result["flow_completion"]["completion_claim_allowed"] is False))

    case = locks["CHAT-PREFLIGHT-006-FLOW-PASS-STOPS-AUTO-ADVANCE"]
    result = run_preflight({"intent": "CONTINUE", "auto_advance": case["auto_advance"]})
    checks.append((case["case_id"], result["conversation_directive"]["action"] == case["expected_action"]))

    for case_id in sorted(acceptance):
        case = acceptance[case_id]
        result = run_preflight(case["payload"])
        checks.append((case_id, result["conversation_directive"]["action"] == case["expected_action"]))

    hcd_process = "00-governance/schemas/digital-product-hcd-design-process.v0.1.candidate.json"
    omitted_hcd_support = {
        "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
        "INDEPENDENT_HCD_REVIEW_BINDING": "promotion/closure review not triggered in this bounded unit test",
    }
    def test_mounts(process_ref: str, stage_id: str) -> list[dict]:
        process = _load_json(ROOT / process_ref)
        stage = next(stage for stage in process["stages"] if stage["stage_id"] == stage_id)
        return [
            {
                "knowledge_ref": f"TEST-KNOWLEDGE-{stage_id}-{index + 1}",
                "use_role": "PRIMARY",
                "operational_eligibility": "OE3_ELIGIBLE",
                "eligibility_scope": f"bounded adapter self-test for {stage_id}",
                "claim_ceiling": "ADAPTER_SELF_TEST_ONLY",
                "applicability": "SELF_TEST_SCOPE_ONLY",
                "conditions": [],
                "unresolved_items": [],
                "freshness_state": "CURRENT",
                "freshness_or_revalidation_trigger": "revalidate when test fixture changes",
                "does_not_prove": ["PROFESSIONAL_PASS"],
                "review_basis": "adapter self-test fixture",
                "satisfies_knowledge_inputs": [knowledge_input],
            }
            for index, knowledge_input in enumerate(stage.get("knowledge_inputs") or [])
        ]

    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": hcd_process,
            "stage_id": "HCD-DP3",
            "candidate_evaluation_mode": "BOUNDED_NON_CURRENT_PROJECT_EXERCISE",
            "omitted_supporting_reasons": omitted_hcd_support,
            "knowledge_mount_records": test_mounts(hcd_process, "HCD-DP3"),
        },
    })
    comp = result["professional_stage_composition"]
    checks.append((
        "PROF-STAGE-001-HCD-DP3-CANDIDATE-OWNERS-HOLD",
        comp["gate"] == "HOLD"
        and any(
            "CANDIDATE_OWNER_NOT_CURRENT_CALLABLE:oleander-ui-interaction" in reason
            for reason in comp["hold_reasons"]
        )
        and any(
            "CANDIDATE_OWNER_NOT_CURRENT_CALLABLE:oleander-ui-visual-composition" in reason
            for reason in comp["hold_reasons"]
        )
        and {"oleander-design-process", "oleander-motion"}.issubset(set(comp["resolved_owner_set"])),
    ))

    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": hcd_process,
            "stage_id": "HCD-DP3",
            "omitted_supporting_reasons": omitted_hcd_support,
            "knowledge_mount_records": test_mounts(hcd_process, "HCD-DP3"),
        },
    })
    checks.append((
        "PROF-STAGE-002-CANDIDATE-MODE-MUST-BE-EXPLICIT",
        result["professional_stage_composition"]["gate"] == "HOLD"
        and "CANDIDATE_REQUIRES_EXPLICIT_BOUNDED_NON_CURRENT_PROJECT_EXERCISE"
        in result["professional_stage_composition"]["hold_reasons"],
    ))

    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": hcd_process,
            "stage_id": "HCD-DP4",
            "candidate_evaluation_mode": "BOUNDED_NON_CURRENT_PROJECT_EXERCISE",
            "omitted_supporting_reasons": omitted_hcd_support,
            "knowledge_mount_records": test_mounts(hcd_process, "HCD-DP4"),
        },
    })
    checks.append((
        "PROF-STAGE-003-SPECIALIST-GAP-HOLDS",
        result["professional_stage_composition"]["gate"] == "HOLD"
        and any(
            "USABILITY_RESEARCH:PROJECT_OR_SPECIALIST_OWNER_BINDING_REQUIRED" in reason
            for reason in result["professional_stage_composition"]["hold_reasons"]
        )
        and any(
            "ACCESSIBILITY_EVALUATION:PROJECT_OR_SPECIALIST_OWNER_BINDING_REQUIRED" in reason
            for reason in result["professional_stage_composition"]["hold_reasons"]
        ),
    ))

    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": hcd_process,
            "stage_id": "HCD-DP4",
            "candidate_evaluation_mode": "BOUNDED_NON_CURRENT_PROJECT_EXERCISE",
            "omitted_supporting_reasons": omitted_hcd_support,
            "knowledge_mount_records": test_mounts(hcd_process, "HCD-DP4"),
            "project_owner_bindings": {
                "USABILITY_RESEARCH": {
                    "owner_id": "project-hcd-research-specialist",
                    "owner_class": "PROJECT_SPECIALIST",
                    "authority_ref": "PROJECT_AUTHORITY/HCD_RESEARCH",
                    "callable": True,
                },
                "ACCESSIBILITY_EVALUATION": {
                    "owner_id": "project-accessibility-specialist",
                    "owner_class": "PROJECT_SPECIALIST",
                    "authority_ref": "PROJECT_AUTHORITY/ACCESSIBILITY",
                    "callable": True,
                },
            },
        },
    })
    checks.append((
        "PROF-STAGE-004-SPECIALIST-BINDINGS-UNBLOCK-ONLY-THEIR-ROLES",
        result["professional_stage_composition"]["gate"] == "HOLD"
        and {
            "project-hcd-research-specialist",
            "project-accessibility-specialist",
        }.issubset(set(result["professional_stage_composition"]["resolved_owner_set"]))
        and not any(
            "USABILITY_RESEARCH:PROJECT_OR_SPECIALIST_OWNER_BINDING_REQUIRED" in reason
            or "ACCESSIBILITY_EVALUATION:PROJECT_OR_SPECIALIST_OWNER_BINDING_REQUIRED" in reason
            for reason in result["professional_stage_composition"]["hold_reasons"]
        )
        and any(
            "CANDIDATE_OWNER_NOT_CURRENT_CALLABLE" in reason
            for reason in result["professional_stage_composition"]["hold_reasons"]
        ),
    ))

    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": hcd_process,
            "stage_id": "HCD-DP3",
            "candidate_evaluation_mode": "BOUNDED_NON_CURRENT_PROJECT_EXERCISE",
            "knowledge_mount_records": test_mounts(hcd_process, "HCD-DP3"),
            "active_supporting_capability_roles": ["INDEPENDENT_HCD_REVIEW_BINDING"],
            "omitted_supporting_reasons": {
                "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
            },
            "independent_reviewer_binding": {
                "owner_id": "oleander-design-process",
                "owner_class": "INDEPENDENT_REVIEWER",
                "authority_ref": "PROJECT_AUTHORITY/HCD_REVIEW",
                "callable": True,
                "independence_state": "INDEPENDENT",
            },
        },
    })
    checks.append((
        "PROF-STAGE-005-INDEPENDENT-REVIEW-CANNOT-COLLAPSE-INTO-PRODUCER",
        result["professional_stage_composition"]["gate"] == "HOLD"
        and "INDEPENDENT_REVIEWER_COLLAPSED_INTO_PRODUCER"
        in result["professional_stage_composition"]["hold_reasons"],
    ))

    architecture_process = "00-governance/schemas/architecture-design-development-process.v1.json"
    architecture_mounts = test_mounts(architecture_process, "ADD-00")
    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": architecture_process,
            "stage_id": "ADD-00",
            "knowledge_mount_records": architecture_mounts,
            "omitted_supporting_reasons": {
                "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
                "INDEPENDENT_ARCHITECTURE_REVIEW_BINDING": "closure review not triggered in this bounded unit test",
            },
        },
    })
    checks.append((
        "PROF-STAGE-006-CURRENT-EXACT-REVISION-PROJECTION-AND-KNOWLEDGE-PASS",
        result["professional_stage_composition"]["gate"] == "PASS"
        and result["professional_stage_composition"]["stage_execution_requirements_source"]
        == "CURRENT_EXACT_REVISION_RUNTIME_PROJECTION"
        and result["professional_stage_composition"]["knowledge_mount_readback"]["gate"] == "PASS",
    ))

    stale_mounts = test_mounts(architecture_process, "ADD-00")
    stale_mounts[0]["freshness_state"] = "REVALIDATION_REQUIRED"
    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": architecture_process,
            "stage_id": "ADD-00",
            "knowledge_mount_records": stale_mounts,
            "omitted_supporting_reasons": {
                "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
                "INDEPENDENT_ARCHITECTURE_REVIEW_BINDING": "closure review not triggered in this bounded unit test",
            },
        },
    })
    checks.append((
        "PROF-STAGE-007-STALE-KNOWLEDGE-MOUNT-HOLDS",
        result["professional_stage_composition"]["gate"] == "HOLD"
        and any(
            "KNOWLEDGE:KNOWLEDGE_MOUNT_FRESHNESS_REVALIDATION_REQUIRED" in reason
            for reason in result["professional_stage_composition"]["hold_reasons"]
        ),
    ))

    result = run_preflight({
        "intent": "EXECUTE",
        "professional_stage_execution": {
            "process_ref": architecture_process,
            "stage_id": "ADD-00",
            "omitted_supporting_reasons": {
                "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
                "INDEPENDENT_ARCHITECTURE_REVIEW_BINDING": "closure review not triggered in this bounded unit test",
            },
        },
    })
    checks.append((
        "PROF-STAGE-008-ACTIVE-KNOWLEDGE-WITHOUT-MOUNT-HOLDS",
        result["professional_stage_composition"]["gate"] == "HOLD"
        and any(
            "KNOWLEDGE:ACTIVE_KNOWLEDGE_INPUT_NOT_COVERED" in reason
            for reason in result["professional_stage_composition"]["hold_reasons"]
        ),
    ))

    chain_result = evaluate_professional_stage_composition({
        "process_ref": architecture_process,
        "stage_id": "ADD-00",
        "knowledge_mount_records": architecture_mounts,
        "omitted_supporting_reasons": {
            "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
            "INDEPENDENT_ARCHITECTURE_REVIEW_BINDING": "closure review not triggered in this bounded unit test",
        },
    })
    checks.append((
        "PROF-STAGE-009-CANONICAL-CHAIN-ORDER-EXACT",
        chain_result["canonical_stage_execution_chain"]
        == CANONICAL_PROFESSIONAL_STAGE_EXECUTION_CHAIN
        and [x["step"] for x in chain_result["canonical_stage_execution_readback"]]
        == CANONICAL_PROFESSIONAL_STAGE_EXECUTION_CHAIN,
    ))

    add00 = next(
        stage
        for stage in _load_json(ROOT / architecture_process)["stages"]
        if stage["stage_id"] == "ADD-00"
    )
    output_bindings = [
        {
            "required_native_output": output,
            "resolution_state": "READBACK_COMPLETE",
            "artifact_refs": [f"ARTIFACT-{index + 1}"],
            "readback_refs": [f"READBACK-{index + 1}"],
        }
        for index, output in enumerate(add00["required_native_outputs"])
    ]
    closure_spec = {
        "process_ref": architecture_process,
        "stage_id": "ADD-00",
        "knowledge_mount_records": architecture_mounts,
        "active_supporting_capability_roles": ["INDEPENDENT_ARCHITECTURE_REVIEW_BINDING"],
        "omitted_supporting_reasons": {
            "CROSS_DOMAIN_INTERFACE_COORDINATION": "not triggered in this bounded unit test",
        },
        "stage_instance_readback": {
            "stage_id": "ADD-00",
            "granularity_binding_state": "DECISION_OBJECT_BOUND",
            "decision_object_refs": ["ARCH-TEST-DECISION-001"],
            "outputs": list(add00["required_native_outputs"]),
            "output_execution_bindings": output_bindings,
            "actual_readback_refs": ["READBACK-ADD00-CLOSURE"],
            "review_refs": [],
            "review_verdict": "NOT_RUN",
            "exit_condition_state": "SATISFIED",
        },
    }
    result = evaluate_professional_stage_composition(
        closure_spec,
        closure_requested=True,
    )
    checks.append((
        "PROF-STAGE-010-INDEPENDENT-REVIEW-BLOCKS-CLOSURE",
        result["stage_closure_gate"] == "HOLD"
        and any(
            reason.startswith("INDEPENDENT_REVIEW")
            for reason in result["hold_reasons"]
        ),
    ))

    closure_spec["independent_reviewer_binding"] = {
        "owner_id": "project-architecture-independent-reviewer",
        "owner_class": "INDEPENDENT_REVIEWER",
        "authority_ref": "PROJECT_AUTHORITY/ARCH_INDEPENDENT_REVIEW",
        "callable": True,
        "independence_state": "INDEPENDENT",
    }
    closure_spec["stage_instance_readback"]["review_refs"] = ["REVIEW-ADD00-001"]
    closure_spec["stage_instance_readback"]["review_verdict"] = "PASS"
    result = evaluate_professional_stage_composition(
        closure_spec,
        closure_requested=True,
    )
    checks.append((
        "PROF-STAGE-011-READBACK-AND-INDEPENDENT-REVIEW-ALLOW-CLOSURE",
        result["gate"] == "PASS"
        and result["stage_closure_gate"] == "PASS"
        and result["canonical_stage_execution_readback"][-1]["state"] == "PASS"
        and not result["canonical_stage_execution_readback"][6][
            "missing_readback_complete_native_outputs"
        ],
    ))

    failed = [case_id for case_id, passed in checks if not passed]
    if failed:
        raise RuntimeError(f"adapter self-test failed: {failed}")
    return {"status": "PASS", "adapter_id": ADAPTER_ID, "adapter_revision": ADAPTER_REVISION, "cases": [case_id for case_id, _ in checks]}


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Stateless Chat/CoS adapter for the existing OLEANDER continuation resolver."
    )
    parser.add_argument("input", nargs="?", help="JSON input file; omit or use '-' for stdin")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--self-test", action="store_true", help="Run adapter composition against existing OLEANDER eval cases")
    args = parser.parse_args()

    try:
        if args.self_test:
            print(json.dumps(run_self_test(), ensure_ascii=False, indent=2))
            return
        if not args.input or args.input == "-":
            payload = json.load(sys.stdin)
        else:
            with open(args.input, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        if not isinstance(payload, dict):
            raise ValueError("input must be one JSON object")
        result = run_preflight(payload)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": "INVALID_PREFLIGHT_INPUT", "detail": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2) from exc

    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None, sort_keys=args.pretty))


if __name__ == "__main__":
    main()
