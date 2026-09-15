#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CLOSED = {"CLOSED", "RESOLVED", "PASS", "ACCEPTED"}
CAUSAL_ROLES = {
    "LATENT_CONDITION",
    "TRIGGER_EVENT",
    "CONTRIBUTING_FACTOR",
    "ROOT_CAUSE",
    "PROPAGATION_FACTOR",
    "DETECTION_FAILURE",
    "RECOVERY_LIMITATION",
    "NON_CAUSAL_COINCIDENT_EVENT",
}
ASSUMPTION_GATES = {
    "NECESSARY_TO_PROCEED",
    "PROPOSITION_EXPLICIT",
    "AUTHORITY_ACCEPTED",
    "CONSEQUENCE_IF_FALSE",
    "VALIDATION_ROUTE",
    "CLAIM_CEILING",
    "EXPIRY_TRIGGER",
}

EXECUTABLE_RULES = {
    "P7/ISS-RP02",
    "P7/ROOT-RP02",
    "P7/ISS-RP03",
    "P7/ISS-RP04",
    "P7/LINE-RP02",
    "P7/UNK-RP02",
    "P7/RSK-RP04",
    "P7/ISS-RP05",
    "P7/ISS-RP06",
    "P7/ISS-RP07",
    "P7/LINE-RP03",
    "P7/ROOT-RP03",
    "P7/ROOT-RP04",
    "P7/ISS-RP08",
    "P7/ISS-RP09",
    "P7/UNK-RP03",
    "P7/UNK-RP04",
    "P7/ASM-RP05",
    "P7/ROOT-RP05",
    "P7/ISS-RP10",
}


@dataclass(frozen=True)
class P7Finding:
    rule_id: str
    object_id: str | None
    message: str
    basis: dict[str, Any] | None = None


def oid(obj: dict[str, Any]) -> str | None:
    value = obj.get("id") or obj.get("object_id")
    return None if value is None else str(value)


def check_object(obj: dict[str, Any]) -> list[P7Finding]:
    findings: list[P7Finding] = []
    object_id = oid(obj)
    cls = obj.get("semantic_class")

    if cls == "ISSUE":
        if obj.get("prior_producer_pass") is True and obj.get("material_review_finding") is True and obj.get("prior_pass_still_current_closure_proof") is True:
            findings.append(P7Finding(
                "P7/ISS-RP02", object_id,
                "later material review finding cannot be suppressed by an earlier producer PASS",
            ))

        root_state = obj.get("root_cause_state")
        if root_state in {"SUPPORTED", "CONFIRMED"} and (not obj.get("root_cause_evidence_ref") or not obj.get("root_cause_scope")):
            findings.append(P7Finding(
                "P7/ROOT-RP02", object_id,
                "supported/confirmed root-cause state requires evidence reference and bounded scope",
            ))

        if obj.get("closure_state") in CLOSED:
            if obj.get("higher_review_required") is True and obj.get("review_after_repair") not in {"PASS", "NOT_REQUIRED"}:
                findings.append(P7Finding(
                    "P7/ISS-RP03", object_id,
                    "repair or producer retest cannot self-close an issue while required higher review remains open",
                ))
            if obj.get("parent_state_auto_closed") is True:
                findings.append(P7Finding(
                    "P7/ISS-RP04", object_id,
                    "local issue closure cannot automatically close parent design/promotion/field/assurance state",
                ))
            if obj.get("repair_state") != "RETEST_PASSED" and obj.get("retest_required") is True:
                findings.append(P7Finding(
                    "P7/ISS-RP05", object_id,
                    "issue closure cannot collapse repair/retest lifecycle when retest is required",
                ))
            if obj.get("related_risk_set_to_zero_on_closure") is True:
                findings.append(P7Finding(
                    "P7/ISS-RP09", object_id,
                    "issue resolution cannot automatically set related future or residual risk to zero",
                ))

        if obj.get("repair_state") in {"IMPLEMENTED", "RETEST_PENDING", "RETEST_PASSED"}:
            missing_lineage = []
            if not obj.get("repair_refs"):
                missing_lineage.append("repair_refs")
            if obj.get("retest_required") is True and not obj.get("retest_refs"):
                missing_lineage.append("retest_refs")
            if obj.get("invalidated_prior_receipts_material") is True and not obj.get("supersedes_or_invalidates_receipts"):
                missing_lineage.append("supersedes_or_invalidates_receipts")
            if missing_lineage:
                findings.append(P7Finding(
                    "P7/LINE-RP02", object_id,
                    "issue repair lifecycle is missing material defect-repair-retest/invalidated-receipt lineage",
                    {"missing": missing_lineage},
                ))

        introduced = obj.get("introduced_or_effective_at")
        impact = obj.get("impact_started_at")
        detected = obj.get("detected_at")
        declared = obj.get("declared_at")
        if obj.get("detection_time_used_as_issue_origin") is True:
            findings.append(P7Finding(
                "P7/ISS-RP06", object_id,
                "detection time cannot be rewritten as issue origin when issue existence/impact timing is distinct",
                {"introduced_or_effective_at": introduced, "impact_started_at": impact, "detected_at": detected, "declared_at": declared},
            ))

        if obj.get("established_existing_defect") is True and obj.get("retroclassified_as_risk_due_no_prior_impact") is True:
            findings.append(P7Finding(
                "P7/ISS-RP07", object_id,
                "established latent defect remains an Issue; absence of prior impact/detection does not make it a Risk",
            ))

        if obj.get("causal_confidence_promoted_from_temporal_or_contextual_coincidence") is True:
            findings.append(P7Finding(
                "P7/ROOT-RP03", object_id,
                "temporal/contextual coincidence cannot be promoted to contributing/root cause without causal basis",
            ))

        causal_records = obj.get("causal_role_records", [])
        if obj.get("material_incident") is True and obj.get("single_generic_root_cause_used") is True and len(causal_records) < 2:
            findings.append(P7Finding(
                "P7/ROOT-RP04", object_id,
                "material incident needs role-capable causal model rather than one generic root-cause field when multiple roles matter",
            ))

        if obj.get("collapsed_done_timestamp") is True and any(obj.get(k) for k in ("repair_implemented_at", "retest_completed_at", "impact_ended_at", "resolved_at")):
            findings.append(P7Finding(
                "P7/ISS-RP08", object_id,
                "repair, retest, impact end and issue resolution are distinct events when material",
            ))

        if obj.get("containment_or_recovery_started") is True and obj.get("root_cause_state") not in {"SUPPORTED", "CONFIRMED"} and obj.get("action_urgency_promoted_root_cause_confidence") is True:
            findings.append(P7Finding(
                "P7/ROOT-RP05", object_id,
                "containment urgency cannot promote causal confidence",
            ))

        if obj.get("postmortem_required") is True and obj.get("failure_cause_recorded") is True and obj.get("detection_gap_material") is True:
            if not obj.get("why_not_detected_earlier") or not obj.get("new_detection_control_refs"):
                findings.append(P7Finding(
                    "P7/ISS-RP10", object_id,
                    "material issue postmortem must distinguish detection gap and record detection-control change where relevant",
                ))

    if cls == "RISK":
        if obj.get("risk_realization_disposition") == "REALIZED_AS_ISSUE":
            if not obj.get("realized_issue_ref") or obj.get("mutated_in_place_to_issue") is True:
                findings.append(P7Finding(
                    "P7/LINE-RP03", object_id,
                    "risk realization must preserve Risk identity and link a distinct Issue object",
                    {"realized_issue_ref": obj.get("realized_issue_ref")},
                ))
        if obj.get("created_post_hoc_from_issue") is True and not obj.get("prior_risk_record_ref"):
            findings.append(P7Finding(
                "P7/RSK-RP04", object_id,
                "post-hoc Issue cannot be backfilled as a pre-existing Risk without a prior Risk record",
            ))

    if cls == "UNKNOWN":
        mode = obj.get("unknown_resolution_mode")
        if obj.get("converted_to_assumption") is True and not obj.get("assumption_admission_event_ref"):
            findings.append(P7Finding(
                "P7/UNK-RP02", object_id,
                "unresolved input must remain Unknown when no authorized Assumption admission exists",
            ))
        if mode == "TBR_PROVISIONAL_VALUE":
            missing = [
                key for key in (
                    "provisional_value",
                    "provisional_value_basis",
                    "resolution_owner",
                    "resolution_action",
                    "resolution_due",
                    "claim_ceiling_while_unresolved",
                ) if obj.get(key) in {None, "", []}
            ]
            if missing:
                findings.append(P7Finding(
                    "P7/UNK-RP03", object_id,
                    "TBR provisional value may remain Unknown only with explicit rationale/owner/resolution/ceiling fields",
                    {"missing": missing},
                ))
            if obj.get("treated_as_fact_or_accepted_assumption") is True:
                findings.append(P7Finding(
                    "P7/UNK-RP03", object_id,
                    "TBR provisional value does not become fact or accepted Assumption by field population alone",
                ))
        if obj.get("converted_to_assumption") is True:
            gates = set(obj.get("assumption_admission_gates_satisfied", []))
            missing_gates = sorted(ASSUMPTION_GATES - gates)
            if not obj.get("assumption_admission_event_ref") or missing_gates:
                findings.append(P7Finding(
                    "P7/UNK-RP04", object_id,
                    "Unknown→Assumption conversion requires explicit authority admission and complete material admission gates",
                    {"missing_gates": missing_gates},
                ))

    if cls == "ASSUMPTION" and obj.get("assumption_state") == "REFUTED":
        affected = set(obj.get("affected_dependency_types", []))
        reopened = set(obj.get("reopened_dependency_types", []))
        missing = sorted(affected - reopened)
        if missing:
            findings.append(P7Finding(
                "P7/ASM-RP05", object_id,
                "refuted Assumption must propagate reopen/invalidity to affected typed dependencies",
                {"missing_reopen_types": missing},
            ))

    return findings


def check_snapshot(snapshot: dict[str, Any]) -> list[P7Finding]:
    findings: list[P7Finding] = []
    for obj in snapshot.get("objects", []):
        findings.extend(check_object(obj))
    return sorted(findings, key=lambda f: (f.rule_id, f.object_id or ""))
