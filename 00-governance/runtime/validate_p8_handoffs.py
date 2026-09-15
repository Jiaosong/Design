#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

CLOSED = {"PASS", "ACCEPT", "ACCEPT_WITH_LIMITATION", "OUTSIDE_CLAIM", "NOT_APPLICABLE"}
REFERENCE_ROLES = {"REFERENCE_ONLY", "COORDINATION_REFERENCE", "ONE_DIRECTIONAL_REFERENCE"}
SOURCE_ROLES = {"SOURCE_MASTER", "EDITABLE_MASTER"}

EXECUTABLE_RULES = {
    "P8/ART-RP01",
    "P8/LOSS-RP02",
    "P8/HAND-RP02",
    "P8/HAND-RP03",
    "P8/HAND-RP04",
    "P8/AUTH-RP02",
    "P8/HAND-RP05",
    "P8/RTRIP-RP01",
    "P8/ROLE-RP02",
    "P8/HAND-RP06",
    "P8/HAND-RP07",
    "P8/LOSS-RP03",
    "P8/HAND-RP08",
    "P8/HAND-RP09",
    "P8/LOSS-RP04",
    "P8/ROLE-RP03",
    "P8/HAND-RP10",
    "P8/HAND-RP11",
    "P8/HAND-RP12",
    "P8/LOSS-RP05",
    "P8/HAND-RP13",
    "P8/RTRIP-RP02",
    "P8/AUTH-RP03",
    "P8/LOSS-RP06",
}


@dataclass(frozen=True)
class P8Finding:
    rule_id: str
    object_id: str | None
    message: str
    basis: dict[str, Any] | None = None


def oid(obj: dict[str, Any]) -> str | None:
    value = obj.get("id") or obj.get("object_id")
    return None if value is None else str(value)


def check_object(obj: dict[str, Any]) -> list[P8Finding]:
    findings: list[P8Finding] = []
    object_id = oid(obj)
    cls = obj.get("semantic_class")

    if cls == "SUPPORT_PACKAGE":
        artifacts = obj.get("artifacts", [])
        semantic_count = obj.get("semantic_object_count")
        if obj.get("file_count_promoted_to_object_count") is True or (
            semantic_count is not None and len(artifacts) > semantic_count and obj.get("one_file_one_semantic_object") is True
        ):
            findings.append(P8Finding(
                "P8/ART-RP01", object_id,
                "artifact/file count cannot be promoted to semantic object count without independent semantic responsibilities",
            ))

    if cls != "HANDOFF":
        return findings

    role = obj.get("handoff_role") or obj.get("carrier_role")
    disposition = obj.get("disposition")
    material = obj.get("material_cross_software_handoff") is True
    preserved = obj.get("preserved_dimensions")
    lost = obj.get("lost_dimensions")
    unknown = obj.get("unknown_dimensions")

    if material and any(value is None for value in (preserved, lost, unknown)):
        findings.append(P8Finding(
            "P8/HAND-RP02", object_id,
            "material handoff must declare preserved, lost and unknown semantic dimensions relative to intended consumer role",
        ))

    if material:
        missing_contract = [
            key for key in ("exchange_requirement_id", "purpose", "producer_role", "consumer_role", "required_information_classes")
            if obj.get(key) in {None, "", []}
        ]
        if missing_contract:
            findings.append(P8Finding(
                "P8/HAND-RP03", object_id,
                "material cross-software handoff needs a purpose-scoped exchange/information contract before PASS/FAIL is meaningful",
                {"missing": missing_contract},
            ))

    if role in REFERENCE_ROLES and disposition in {"REJECT", "FAIL"} and obj.get("roundtrip_required") is False and obj.get("rejection_reason") == "NATIVE_ROUNDTRIP_NOT_PRESERVED":
        findings.append(P8Finding(
            "P8/HAND-RP04", object_id,
            "one-directional reference handoff must not fail solely for lacking unclaimed round-trip authoring semantics",
        ))

    if obj.get("consumer_import_or_edit_capable") is True and obj.get("source_change_authority_transferred") is True and not obj.get("authority_transfer_event_ref"):
        findings.append(P8Finding(
            "P8/AUTH-RP02", object_id,
            "import/edit capability does not grant source change authority; authority after handoff must be explicit",
        ))
        findings.append(P8Finding(
            "P8/AUTH-RP03", object_id,
            "technical editability/import capability cannot transfer definition owner or Source Master status without authority event",
        ))

    if obj.get("exchange_reopen_status") == "PASS" and (
        obj.get("native_authoring_state_promoted_from_exchange") is True or obj.get("professional_design_state_promoted_from_exchange") is True
    ):
        findings.append(P8Finding(
            "P8/HAND-RP05", object_id,
            "exchange reopen PASS closes only declared exchange invariants and cannot promote native authoring or professional design state",
        ))

    if obj.get("roundtrip_tested") is True and obj.get("roundtrip_acceptance_basis") == "BYTE_HASH_ONLY" and obj.get("byte_identity_controlled_property") is not True:
        findings.append(P8Finding(
            "P8/RTRIP-RP01", object_id,
            "round-trip acceptance must use purpose-appropriate semantic invariants unless byte identity itself is controlled",
        ))

    if obj.get("runtime_delivery_format_pass") is True and obj.get("native_parametric_authoring_preserved_claim") is True and not obj.get("native_authoring_evidence_ref"):
        findings.append(P8Finding(
            "P8/ROLE-RP02", object_id,
            "runtime delivery format success cannot imply preservation of native parametric authoring semantics without evidence",
        ))

    if obj.get("downstream_package_or_deployment_incomplete") is True and obj.get("unchanged_upstream_source_invalidated") is True:
        findings.append(P8Finding(
            "P8/HAND-RP06", object_id,
            "downstream package/deployment incompleteness blocks that handoff scope but cannot globally invalidate unchanged upstream source",
        ))

    per_role = obj.get("per_role_results", {})
    if isinstance(per_role, dict) and len(set(per_role.values())) > 1 and obj.get("global_handoff_status") in {"PASS", "FAIL"} and not obj.get("aggregation_policy"):
        findings.append(P8Finding(
            "P8/HAND-RP07", object_id,
            "divergent per-role/information-class results require preserved scoped results and explicit aggregation before global status",
            {"per_role_results": per_role},
        ))

    required_info = set(obj.get("required_information_classes", []))
    unknown_info = set(obj.get("unknown_dimensions", []))
    if unknown_info:
        intersects_required = bool(required_info & unknown_info) or obj.get("unknown_loss_intersects_required_scope") is True
        if intersects_required and disposition in {"PASS", "ACCEPT"}:
            findings.append(P8Finding(
                "P8/LOSS-RP03", object_id,
                "unknown loss intersecting required information/authority cannot be ignored by bounded handoff PASS",
                {"unknown_required": sorted(required_info & unknown_info)},
            ))
        if not intersects_required and obj.get("global_hold_due_unknown_outside_claim") is True:
            findings.append(P8Finding(
                "P8/LOSS-RP05", object_id,
                "unknown loss outside declared exchange purpose must not globalize HOLD",
            ))

    if obj.get("file_open_or_import_success") is True and disposition in {"PASS", "ACCEPT"}:
        if not obj.get("consumer_task_readback_complete") or not obj.get("declared_required_dimensions_readback_complete"):
            findings.append(P8Finding(
                "P8/HAND-RP08", object_id,
                "file open/import success is not handoff PASS without declared exchange-purpose and required-information readback",
            ))

    layers = obj.get("layer_results", {})
    if isinstance(layers, dict):
        lower_pass = any(layers.get(k) in CLOSED for k in ("L1_FORMAT_SYNTAX", "L2_SCHEMA_NORMATIVE_CONFORMANCE"))
        higher_auto = any(layers.get(k) == "AUTO_GRANTED_FROM_LOWER_LAYER" for k in (
            "L4_PROJECT_INFORMATION_REQUIREMENT_CONFORMANCE",
            "L5_CONSUMER_TASK_READBACK",
            "L6_ROUNDTRIP_OR_EDITABILITY_EQUIVALENCE",
            "L7_SOURCE_AUTHORITY_CONTINUITY",
        ))
        if lower_pass and higher_auto:
            findings.append(P8Finding(
                "P8/HAND-RP09", object_id,
                "format/schema layer PASS cannot auto-grant project-information, task, round-trip or authority layers",
            ))

        if layers.get("L2_SCHEMA_NORMATIVE_CONFORMANCE") in CLOSED and layers.get("L4_PROJECT_INFORMATION_REQUIREMENT_CONFORMANCE") == "AUTO_GRANTED_FROM_SCHEMA":
            findings.append(P8Finding(
                "P8/HAND-RP10", object_id,
                "format/schema conformance and project-information requirement conformance are independent results",
            ))

    if role in SOURCE_ROLES and obj.get("loss_severity") in {"CLAIM_AFFECTING", "AUTHORITY_BREAKING"} and disposition in {"PASS", "ACCEPT"}:
        findings.append(P8Finding(
            "P8/LOSS-RP02", object_id,
            "loss acceptable for derivative role may be authority-breaking for Source/Edit Master role",
        ))
    if obj.get("same_loss_used_for_multiple_roles") is True and obj.get("loss_acceptability_role_scoped") is not True:
        findings.append(P8Finding(
            "P8/LOSS-RP04", object_id,
            "same information loss must be evaluated by carrier role, consumer purpose and exchange requirement",
        ))

    if obj.get("exchange_derivative_replaces_source_master") is True or obj.get("exchange_derivative_replaces_editable_master") is True:
        findings.append(P8Finding(
            "P8/ROLE-RP03", object_id,
            "valid exchange derivative may own declared delivery content but cannot silently replace native Source/Edit Master responsibility",
        ))

    per_object = obj.get("per_object_or_information_class_results", {})
    if isinstance(per_object, dict) and len(set(per_object.values())) > 1 and obj.get("global_handoff_status") in {"PASS", "FAIL"} and not obj.get("aggregation_policy"):
        findings.append(P8Finding(
            "P8/HAND-RP11", object_id,
            "material mixed per-object/per-information-class failures must be preserved; global summary requires aggregation rule",
        ))

    if obj.get("declared_exchange_requirement_exists") is True and obj.get("fidelity_judged_against_total_native_equivalence") is True:
        findings.append(P8Finding(
            "P8/HAND-RP12", object_id,
            "cross-software fidelity must be judged against declared exchange requirements, not unbounded native-model equivalence",
        ))

    if obj.get("producer_export_validation_complete") is True and obj.get("consumer_behavior_material") is True and obj.get("consumer_task_readback_complete") is not True and disposition in {"PASS", "ACCEPT"}:
        findings.append(P8Finding(
            "P8/HAND-RP13", object_id,
            "producer export validation cannot substitute for consumer task readback when downstream interpretation/behavior is material",
        ))

    if role in REFERENCE_ROLES and obj.get("roundtrip_required") is False and obj.get("failed_only_due_roundtrip") is True:
        findings.append(P8Finding(
            "P8/RTRIP-RP02", object_id,
            "reference/one-directional exchange must not fail solely for unclaimed round-trip equivalence",
        ))
    if role == "EDITABLE_MASTER" and disposition in {"PASS", "ACCEPT"} and obj.get("roundtrip_required") is True and obj.get("roundtrip_status") not in CLOSED:
        findings.append(P8Finding(
            "P8/RTRIP-RP02", object_id,
            "editable-master handoff cannot cite reference-exchange success as proof of required round-trip equivalence",
        ))

    if obj.get("loss_observation_state") == "UNKNOWN_NOT_TESTED" and obj.get("loss_severity") == "NONE":
        findings.append(P8Finding(
            "P8/LOSS-RP06", object_id,
            "not-tested loss dimension cannot be recorded as no loss",
        ))

    return findings


def check_snapshot(snapshot: dict[str, Any]) -> list[P8Finding]:
    findings: list[P8Finding] = []
    for obj in snapshot.get("objects", []):
        findings.extend(check_object(obj))
    return sorted(findings, key=lambda f: (f.rule_id, f.object_id or ""))
