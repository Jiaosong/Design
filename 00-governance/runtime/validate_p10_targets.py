#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

PASS_STATES = {"PASS", "ACCEPTED"}
EXECUTABLE_RULES = {
    "P10/MED-RP02",
    "P10/MED-RP03",
    "P10/READ-RP02",
    "P10/BOUND-RP02",
    "P10/ASSET-RP02",
    "P10/ASSET-RP03",
    "P10/ROLE-RP03",
    "P10/SEQ-RP02",
    "P10/MOTION-RP02",
    "P10/MED-RP04",
}


@dataclass(frozen=True)
class P10Finding:
    rule_id: str
    object_id: str | None
    message: str
    basis: dict[str, Any] | None = None


def oid(obj: dict[str, Any]) -> str | None:
    value = obj.get("id") or obj.get("presentation_release_id") or obj.get("presentation_asset_id")
    return None if value is None else str(value)


def check_release(obj: dict[str, Any]) -> list[P10Finding]:
    findings: list[P10Finding] = []
    object_id = oid(obj)
    source_revision = obj.get("source_revision")
    vector = obj.get("medium_readback_vector", {})

    for medium, value in vector.items() if isinstance(vector, dict) else []:
        if isinstance(value, dict):
            result = value.get("result")
            bound_revision = value.get("source_revision")
            target_condition_id = value.get("target_condition_id")
        else:
            result = value
            bound_revision = None
            target_condition_id = None
        if result in PASS_STATES:
            if obj.get("reusable_or_carry_forward_claimed") is True and (not bound_revision or not target_condition_id):
                findings.append(P10Finding(
                    "P10/MED-RP02", object_id,
                    "reusable medium PASS must bind result to source revision and explicit target condition",
                    {"medium": medium, "result": result, "source_revision": bound_revision, "target_condition_id": target_condition_id},
                ))
            if obj.get("medium_pass_reused_without_target_condition") is True and not target_condition_id:
                findings.append(P10Finding(
                    "P10/MED-RP03", object_id,
                    "medium PASS without target-condition identity is insufficient for reuse/carry-forward",
                    {"medium": medium},
                ))

    if obj.get("browser_target_pass") is True and any(obj.get(k) is True for k in (
        "design_keep_closed_from_browser",
        "professional_acceptance_closed_from_browser",
        "field_validity_closed_from_browser",
    )):
        findings.append(P10Finding(
            "P10/READ-RP02", object_id,
            "browser target PASS may close rendering/interaction/boundary assertions only, not Design Crit/professional/field acceptance",
        ))

    if obj.get("simulated_or_derived_user_facing_state") is True:
        required_targets = set(obj.get("targets_exposing_simulation", []))
        boundary_targets = set(obj.get("truth_boundary_readable_targets", []))
        missing = sorted(required_targets - boundary_targets)
        if missing:
            findings.append(P10Finding(
                "P10/BOUND-RP02", object_id,
                "simulation/derived-state truth boundary must be readable in the same target conditions where users consume it",
                {"missing_boundary_targets": missing},
            ))

    deployment = obj.get("deployment_status")
    external = obj.get("external_content_readback")
    if deployment in PASS_STATES and obj.get("external_content_pass_inferred_from_deployment") is True and external not in PASS_STATES:
        findings.append(P10Finding(
            "P10/MED-RP04", object_id,
            "host/deployment success and user-visible external content readback are separate target-condition results",
            {"deployment_status": deployment, "external_content_readback": external},
        ))

    if obj.get("section_or_page_count_change_used_as_content_loss_proof") is True:
        if not obj.get("count_scope_labels") or obj.get("source_mutation_inferred_from_count_change") is True:
            findings.append(P10Finding(
                "P10/SEQ-RP02", object_id,
                "section/page/authoring/protected-identity counts need scope labels; count change alone is not content loss or source mutation",
            ))

    if obj.get("reduced_motion_state_present") is True and obj.get("reduced_motion_separate_style_identity") is True and not obj.get("information_architecture_or_semantic_role_changed"):
        findings.append(P10Finding(
            "P10/MOTION-RP02", object_id,
            "reduced motion is a target-condition override within the same presentation system unless information architecture/semantic role changes",
        ))

    return findings


def check_asset(obj: dict[str, Any]) -> list[P10Finding]:
    findings: list[P10Finding] = []
    object_id = oid(obj)

    chunks = obj.get("runtime_instances", [])
    if len(chunks) > 1 and obj.get("semantic_source_id") and obj.get("declared_independent_source_count") == len(chunks):
        findings.append(P10Finding(
            "P10/ASSET-RP02", object_id,
            "runtime/transport chunk count cannot inflate semantic visual-source count",
            {"runtime_instances": chunks, "semantic_source_id": obj.get("semantic_source_id")},
        ))

    if obj.get("manifest_revision") and obj.get("current_source_revision") and obj.get("manifest_revision") != obj.get("current_source_revision") and obj.get("manifest_claimed_complete_current_coverage") is True:
        findings.append(P10Finding(
            "P10/ASSET-RP03", object_id,
            "older asset/dependency manifest may support lineage but cannot claim complete current-revision coverage",
            {"manifest_revision": obj.get("manifest_revision"), "current_source_revision": obj.get("current_source_revision")},
        ))

    if obj.get("runtime_slot_role") or obj.get("visual_semantic_role"):
        if obj.get("design_review_state_promoted_from_runtime_role") is True or obj.get("source_authority_promoted_from_runtime_role") is True:
            findings.append(P10Finding(
                "P10/ROLE-RP03", object_id,
                "runtime slot/visual semantic role is distinct from design-review state and source authority",
            ))

    return findings


def check_snapshot(snapshot: dict[str, Any]) -> list[P10Finding]:
    findings: list[P10Finding] = []
    for obj in snapshot.get("objects", []):
        cls = obj.get("semantic_class")
        if cls == "PRESENTATION_RELEASE":
            findings.extend(check_release(obj))
        elif cls == "PRESENTATION_ASSET":
            findings.extend(check_asset(obj))
    return sorted(findings, key=lambda f: (f.rule_id, f.object_id or ""))
