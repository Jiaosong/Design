#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

TRANSFER_PARTS = {"WHEN", "DO_OR_EXPECT", "BECAUSE", "NOT_BEYOND", "REVALIDATE_WHEN"}
EXECUTABLE_RULES = {
    "P9/G9-RP02",
    "P9/OWN-RP03",
    "P9/TRF-RP02",
    "P9/CLM-RP02",
    "P9/BOUND-RP01",
    "P9/PATCH-RP02",
    "P9/GATE-RP02",
    "P9/B1-RP02",
    "P9/IR-RP01",
}


@dataclass(frozen=True)
class P9Finding:
    rule_id: str
    object_id: str | None
    message: str
    basis: dict[str, Any] | None = None


def oid(obj: dict[str, Any]) -> str | None:
    value = obj.get("id") or obj.get("object_id")
    return None if value is None else str(value)


def check_object(obj: dict[str, Any]) -> list[P9Finding]:
    if obj.get("semantic_class") != "G9_ADMISSION":
        return []

    findings: list[P9Finding] = []
    object_id = oid(obj)

    disposition_fields = (obj.get("existing_owner_action"), obj.get("new_object_decision"), obj.get("reject_decision"))
    if obj.get("lesson_summary_only") is True or not any(disposition_fields):
        findings.append(P9Finding(
            "P9/G9-RP02", object_id,
            "G9 replay must terminate in explicit existing-owner action, new-object decision or rejection, not lesson summary only",
        ))

    if obj.get("existing_owner_found") is True and obj.get("existing_owner_primary_responsibility_match") is True and obj.get("new_peer_object_created") is True and not obj.get("split_or_collision_gate_ref"):
        findings.append(P9Finding(
            "P9/OWN-RP03", object_id,
            "matching Current canonical owner preempts a new peer object unless a split/collision gate justifies new identity",
        ))

    transfer = set(obj.get("transfer_statement_parts_present", []))
    missing_transfer = sorted(TRANSFER_PARTS - transfer)
    if obj.get("cross_domain_transfer_claimed") is True and missing_transfer:
        findings.append(P9Finding(
            "P9/TRF-RP02", object_id,
            "cross-domain transfer requires WHEN/DO-BECAUSE/NOT-BEYOND/REVALIDATE-WHEN boundary",
            {"missing": missing_transfer},
        ))

    evidence = obj.get("supporting_evidence", [])
    strengths = {item.get("strength") for item in evidence if isinstance(item, dict) and item.get("strength")}
    refs = {item.get("ref") for item in evidence if isinstance(item, dict)}
    if obj.get("uses_direct_and_contextual_evidence") is True:
        if "DIRECT_PROJECT_REPLAY" not in strengths or "CONTEXTUAL_CROSS_DOMAIN" not in strengths or obj.get("evidence_strengths_flattened") is True:
            findings.append(P9Finding(
                "P9/CLM-RP02", object_id,
                "direct project replay and contextual cross-domain analogy must retain different evidence relation strengths",
                {"strengths": sorted(x for x in strengths if x), "refs": sorted(x for x in refs if x)},
            ))

    if obj.get("generalized_method_rule") is True and not obj.get("counterexample_or_does_not_establish"):
        findings.append(P9Finding(
            "P9/BOUND-RP01", object_id,
            "generalized method rule requires counterexample or explicit non-establishment boundary",
        ))

    if obj.get("safe_patch_candidate") is True and (obj.get("canonical_write_applied") is True or obj.get("current_promotion_applied") is True) and not obj.get("authorized_promotion_or_write_ref"):
        findings.append(P9Finding(
            "P9/PATCH-RP02", object_id,
            "safe additive patch candidate does not authorize canonical write or Current promotion",
        ))

    gates = obj.get("gates", {})
    if gates.get("R1") == "NOT_APPLICABLE" and gates.get("R2") == "NOT_APPLICABLE" and obj.get("other_professional_gates_bypassed") is True:
        findings.append(P9Finding(
            "P9/GATE-RP02", object_id,
            "R1/R2 not-applicable does not bypass K1–K5, B1, provenance/lifecycle or Independent Review",
        ))

    if gates.get("B1_CANDIDATE_BLOCK") == "PASS" and gates.get("B1_EXISTING_OWNER_FULL_BODY") == "PASS_BY_CANDIDATE_BLOCK":
        findings.append(P9Finding(
            "P9/B1-RP02", object_id,
            "bilingual parity of a new candidate block cannot self-grant B1 PASS to the existing owner full body",
        ))

    if obj.get("producer_side_synthesis") is True and gates.get("INDEPENDENT_REVIEW") == "PASS":
        findings.append(P9Finding(
            "P9/IR-RP01", object_id,
            "producer-side G9 synthesis cannot self-grant Independent Review PASS",
        ))

    return findings


def check_snapshot(snapshot: dict[str, Any]) -> list[P9Finding]:
    findings: list[P9Finding] = []
    for obj in snapshot.get("objects", []):
        findings.extend(check_object(obj))
    return sorted(findings, key=lambda f: (f.rule_id, f.object_id or ""))
