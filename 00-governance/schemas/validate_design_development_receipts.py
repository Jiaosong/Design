#!/usr/bin/env python3
"""Validate shared Design Quality and Architecture DD receipts.

This validator is intentionally narrow. It validates schema structure and the
body/title/native-readback invariants required by the current OLEANDER shared
Design Quality and Architecture Design Development contracts. It does not infer
design quality, professional adequacy, statutory compliance, DQ maturity, or
Promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # Keep a fail-closed structural floor for stdlib-only CI.
    Draft202012Validator = None  # type: ignore[assignment]


ROOT = Path(__file__).resolve().parent
REPO_ROOT = ROOT.parents[1]
SCHEMAS = {
    "DESIGN_QUALITY_DEVELOPMENT_RECEIPT": ROOT / "design-quality-development-receipt.v1.schema.json",
    "ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT": ROOT / "architecture-design-development-receipt.v1.schema.json",
}

GENERIC_TITLES = {
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

DD_ROLES = {
    "TITLE_IDENTITY",
    "DEFINITION_SCOPE",
    "CURRENT_CONDITION_PROBLEM",
    "CANONICAL_KNOWLEDGE_EVIDENCE_INPUTS",
    "DESIGN_INTENT_CRITERIA",
    "DEVELOPMENT_MECHANISM_WORKFLOW",
    "NATIVE_ARTIFACT_READBACK",
    "FAILURE_COUNTEREXAMPLE_OPEN_ITEM",
    "DECISION_MATURITY_CLAIM_CEILING",
    "REOPEN_TRIGGER_NEXT_ACTION",
}

ARCH_ROLES = {
    "STAGE_QUESTION_SCOPE",
    "CURRENT_CONDITION_PROBLEM",
    "AUTHORITY_KNOWLEDGE_INPUTS",
    "ARCHITECTURAL_CRITERIA_INTENT",
    "DEVELOPMENT_COMPARISON_MECHANISM",
    "PROFESSIONAL_INTERFACES",
    "NATIVE_OUTPUT_SOURCE_OF_TRUTH",
    "ACTUAL_READBACK_FINDING",
    "FAILURE_OPEN_DOES_NOT_PROVE",
    "VERDICT_CLAIM_REOPEN_NEXT_ACTION",
}

ARCH_STAGE_IDS = {
    f"ADD-{index:02d}" for index in range(18)
}

ARCH_PHASE_KEYS = {
    "site_context",
    "users_operations",
    "program_room_brief",
    "adjacency",
    "zoning_options",
    "flow_systems",
    "circulation",
    "life_safety_aware_planning",
    "accessibility_aware_planning",
    "operations_security_hygiene",
    "system_fitback",
    "climate_daylight_acoustics",
    "ffe_room_use",
    "area_cost_maintenance",
    "code_matrix",
}

ARCH_PHASE_STATES = {
    "NOT_APPLICABLE_WITH_REASON",
    "OPEN",
    "IN_PROGRESS",
    "PASS_AT_CLAIM_CEILING",
    "REVISE",
    "BLOCKED_BY_AUTHORITY",
}

ARCH_CLOSED_PHASE_STATES = {
    "NOT_APPLICABLE_WITH_REASON",
    "PASS_AT_CLAIM_CEILING",
}

STRICT_DQ_SCHEMA_VERSION = "1.1"
PATH_LIKE_SUFFIXES = {
    ".json",
    ".md",
    ".skp",
    ".rb",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".pdf",
    ".csv",
    ".xlsx",
    ".dwg",
    ".dxf",
}


def looks_like_file_ref(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    normalized = value.replace("\\", "/")
    return "/" in normalized or Path(normalized).suffix.lower() in PATH_LIKE_SUFFIXES


def resolve_file_ref(ref: str, project_root: Path | None) -> Path | None:
    candidate = Path(ref)
    if candidate.is_absolute():
        return candidate
    normalized = ref.replace("\\", "/")
    if normalized.startswith(("00-governance/", "oleander-skills/", "skills/", "evals/", "90-shared/")):
        return REPO_ROOT / Path(normalized)
    if project_root is not None:
        return project_root / Path(normalized)
    return None


def validate_resolvable_file_ref(
    ref: Any,
    label: str,
    errors: list[str],
    project_root: Path | None,
) -> Path | None:
    if not looks_like_file_ref(ref):
        return None
    path = resolve_file_ref(ref, project_root)
    if path is None:
        return None
    if not path.is_file():
        errors.append(f"{label}: referenced file does not exist: {ref}")
        return None
    return path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("receipt root must be a JSON object")
    return payload


def validate_section_coverage(
    sections: Any,
    expected_roles: set[str],
    label: str,
    errors: list[str],
    *,
    pass_like: bool,
) -> None:
    if not isinstance(sections, list):
        errors.append(f"{label}: section_coverage must be an array")
        return

    roles = [
        entry.get("semantic_role")
        for entry in sections
        if isinstance(entry, dict)
    ]
    if len(sections) != 10 or len(set(roles)) != 10 or set(roles) != expected_roles:
        errors.append(
            f"{label}: must disposition each of the 10 semantic responsibilities exactly once"
        )

    for index, entry in enumerate(sections):
        if not isinstance(entry, dict):
            errors.append(f"{label}[{index}]: expected object")
            continue
        role = entry.get("semantic_role", f"index-{index}")
        status = entry.get("status")
        if status not in {"PRESENT", "COMBINED", "NOT_APPLICABLE_WITH_REASON", "MISSING"}:
            errors.append(f"{label}.{role}: invalid status {status!r}")
        if status in {"PRESENT", "COMBINED"}:
            locator = entry.get("visible_heading_or_locator")
            if not isinstance(locator, str) or not locator.strip():
                errors.append(
                    f"{label}.{role}: {status} requires non-empty string visible_heading_or_locator"
                )
        if status == "NOT_APPLICABLE_WITH_REASON":
            reason = entry.get("reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{label}.{role}: N/A requires non-empty string reason")
        if pass_like and status == "MISSING":
            errors.append(f"{label}.{role}: PASS/KEEP cannot retain MISSING")


def validate_string_array(
    value: Any,
    label: str,
    errors: list[str],
    *,
    min_items: int = 0,
    nonempty_items: bool = False,
) -> bool:
    """Mirror JSON-Schema string-array constraints in stdlib-only fallback paths."""
    if not isinstance(value, list):
        errors.append(f"{label} must be an array")
        return False
    if len(value) < min_items:
        errors.append(f"{label} requires at least {min_items} item(s)")
    for index, item in enumerate(value):
        if not isinstance(item, str):
            errors.append(f"{label}[{index}] must be a string")
        elif nonempty_items and not item.strip():
            errors.append(f"{label}[{index}] must be a non-empty string")
    return True


def validate_mounts(
    mounts: Any,
    label: str,
    errors: list[str],
    mount_record_refs: Any = None,
    *,
    strict_current_emission: bool = False,
    project_root: Path | None = None,
) -> None:
    if mounts is None:
        return
    if not isinstance(mounts, list):
        errors.append(f"{label}: knowledge_mounts must be an array")
        return
    refs = (
        [ref for ref in mount_record_refs if isinstance(ref, str) and ref.strip()]
        if isinstance(mount_record_refs, list)
        else []
    )
    if mounts and not refs:
        errors.append(
            f"{label}: non-empty knowledge_mounts requires body_structure.knowledge_mount_refs to R-B owner-issued mount records"
        )
    for index, mount in enumerate(mounts):
        if not isinstance(mount, dict):
            errors.append(f"{label}[{index}]: expected object")
            continue
        required = {
            "knowledge_ref",
            "use_role",
            "claim_ceiling",
            "applicability",
            "does_not_prove",
            "review_basis",
        }
        missing = sorted(required - set(mount))
        if missing:
            errors.append(f"{label}[{index}]: missing {', '.join(missing)}")
        has_new = "eligibility_snapshot" in mount
        has_legacy = "operational_eligibility" in mount
        if has_new == has_legacy:
            errors.append(
                f"{label}[{index}]: exactly one of eligibility_snapshot or legacy operational_eligibility is required"
            )
        eligibility = (
            mount.get("eligibility_snapshot") if has_new else mount.get("operational_eligibility")
        )
        if eligibility not in {"OE1", "OE2", "OE3"}:
            errors.append(f"{label}[{index}]: invalid eligibility snapshot {eligibility!r}")

        source_mount_ref = mount.get("source_mount_record_ref")
        if source_mount_ref is not None and source_mount_ref not in refs:
            errors.append(
                f"{label}[{index}]: source_mount_record_ref must match body_structure.knowledge_mount_refs"
            )
        if strict_current_emission and not has_new:
            errors.append(
                f"{label}[{index}]: schema_version 1.1 requires eligibility_snapshot rather than legacy operational_eligibility"
            )
        if has_new:
            if not isinstance(source_mount_ref, str) or not source_mount_ref.strip():
                if len(refs) != 1:
                    errors.append(
                        f"{label}[{index}]: new eligibility_snapshot requires source_mount_record_ref when the source mount cannot be uniquely inferred"
                    )
            revision = mount.get("mount_record_revision_or_hash")
            if not isinstance(revision, str) or not revision.strip():
                errors.append(
                    f"{label}[{index}]: new eligibility_snapshot requires mount_record_revision_or_hash"
                )
            resolved_mount = None
            if isinstance(source_mount_ref, str) and source_mount_ref.strip():
                resolved_mount = validate_resolvable_file_ref(
                    source_mount_ref,
                    f"{label}[{index}].source_mount_record_ref",
                    errors,
                    project_root,
                )
            elif len(refs) == 1:
                resolved_mount = validate_resolvable_file_ref(
                    refs[0],
                    f"{label}[{index}].source_mount_record_ref",
                    errors,
                    project_root,
                )
            if resolved_mount is not None and isinstance(revision, str):
                normalized_revision = revision.strip()
                expected_hash = None
                if normalized_revision.lower().startswith("sha256:"):
                    expected_hash = normalized_revision.split(":", 1)[1]
                elif len(normalized_revision) == 64 and all(
                    char in "0123456789abcdefABCDEF" for char in normalized_revision
                ):
                    expected_hash = normalized_revision
                if expected_hash and sha256_file(resolved_mount) != expected_hash.upper():
                    errors.append(
                        f"{label}[{index}]: mount_record_revision_or_hash does not match referenced mount bytes"
                    )
        if eligibility == "OE2":
            conditions = mount.get("conditions")
            if not isinstance(conditions, list) or not conditions:
                errors.append(f"{label}[{index}]: OE2 requires explicit conditions")
            does_not_prove = mount.get("does_not_prove")
            if not isinstance(does_not_prove, list) or not does_not_prove:
                errors.append(f"{label}[{index}]: OE2 requires does_not_prove boundary")
        if eligibility == "OE1" and mount.get("use_role") in {"PRIMARY", "SUPPORTING"}:
            errors.append(
                f"{label}[{index}]: OE1 cannot be a PRIMARY/SUPPORTING in-claim decision input"
            )


def validate_design_quality(
    payload: dict[str, Any], project_root: Path | None = None
) -> list[str]:
    errors: list[str] = []
    schema_version = payload.get("schema_version")
    if schema_version not in {"1.0", STRICT_DQ_SCHEMA_VERSION}:
        errors.append("schema_version must be 1.0 or 1.1")
    body = payload.get("body_structure")
    strict_current_emission = schema_version == STRICT_DQ_SCHEMA_VERSION
    legacy_pre_body = schema_version == "1.0" and not isinstance(body, dict)
    if strict_current_emission and not isinstance(body, dict):
        errors.append("schema_version 1.1 requires body_structure")

    if isinstance(body, dict):
        title = body.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append("body_structure.title is required")
        elif title in GENERIC_TITLES:
            errors.append("body_structure.title is generic and does not identify the decision object")

    if strict_current_emission and not isinstance(
        payload.get("in_claim_blocking_design_fail_count"), int
    ):
        errors.append(
            "schema_version 1.1 requires in_claim_blocking_design_fail_count"
        )
    keep = payload.get("result") == "KEEP"
    if isinstance(body, dict):
        validate_section_coverage(
            body.get("section_coverage"),
            DD_ROLES,
            "body_structure.section_coverage",
            errors,
            pass_like=keep,
        )
        validate_mounts(
            payload.get("knowledge_mounts"),
            "knowledge_mounts",
            errors,
            mount_record_refs=body.get("knowledge_mount_refs"),
            strict_current_emission=strict_current_emission,
            project_root=project_root,
        )
    elif not legacy_pre_body:
        errors.append("body_structure is required")

    if project_root is not None:
        if isinstance(body, dict):
            for index, ref in enumerate(body.get("knowledge_mount_refs", []) or []):
                validate_resolvable_file_ref(
                    ref,
                    f"body_structure.knowledge_mount_refs[{index}]",
                    errors,
                    project_root,
                )
        for index, ref in enumerate(payload.get("artifact_refs", []) or []):
            validate_resolvable_file_ref(
                ref, f"artifact_refs[{index}]", errors, project_root
            )
        dna_ref = payload.get("project_design_dna_ref")
        if dna_ref:
            validate_resolvable_file_ref(
                dna_ref, "project_design_dna_ref", errors, project_root
            )

    comparison = payload.get("candidate_comparison")
    if (
        strict_current_emission
        and isinstance(comparison, dict)
        and comparison.get("applicable") is True
    ):
        candidate_refs = comparison.get("candidate_refs")
        if not isinstance(candidate_refs, list) or len(candidate_refs) < 2:
            errors.append(
                "candidate_comparison: applicable comparison requires at least two candidate_refs"
            )
        fixed_conditions = comparison.get("fixed_comparison_conditions")
        if not isinstance(fixed_conditions, list) or not fixed_conditions:
            errors.append(
                "candidate_comparison: applicable comparison requires fixed_comparison_conditions"
            )
        decision = comparison.get("decision")
        if not isinstance(decision, str) or not decision.strip():
            errors.append(
                "candidate_comparison: applicable comparison requires a bounded decision"
            )

    maturity = payload.get("design_maturity")
    independent = payload.get("independent_design_review")
    if maturity in {"DQ4_DISTINCTIVE_RESOLVED_SYSTEM", "DQ5_PROVEN_CROSS_CONTEXT_LANGUAGE"}:
        if not isinstance(independent, dict) or independent.get("reviewer_independent_from_producer") is not True:
            errors.append(f"{maturity} requires an independent design reviewer")

    if maturity == "DQ5_PROVEN_CROSS_CONTEXT_LANGUAGE":
        cross_context = payload.get("cross_context_validation")
        if not isinstance(cross_context, dict):
            errors.append("DQ5_PROVEN_CROSS_CONTEXT_LANGUAGE requires cross_context_validation")
        else:
            context_refs = cross_context.get("context_refs")
            if (
                not isinstance(context_refs, list)
                or len(context_refs) < 2
                or len({ref for ref in context_refs if isinstance(ref, str) and ref.strip()}) < 2
            ):
                errors.append("DQ5 cross_context_validation requires at least two distinct real context_refs")
            for field in {
                "material_difference_between_contexts",
                "identity_relation_preserved",
                "counterevidence_or_none_reason",
                "transfer_boundary",
            }:
                value = cross_context.get(field)
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"DQ5 cross_context_validation requires non-empty {field}")
            boundary = cross_context.get("does_not_prove")
            if not isinstance(boundary, list) or not boundary:
                errors.append("DQ5 cross_context_validation requires does_not_prove boundary")

    if strict_current_emission:
        triggered = set(payload.get("triggered_design_dimensions") or [])
        for dimension, field in {
            "DD-05_HUMAN_RELATION": "human_relation_state",
            "DD-06_SENSORY": "sensory_state",
            "DD-11_MEANING_MEMORY": "meaning_memory_state",
        }.items():
            if dimension in triggered and field not in payload:
                errors.append(
                    f"schema_version 1.1: triggered {dimension} requires {field}"
                )

    conditional_dimension_reasons = {
        "human_relation_state": "human_relation_reason",
        "sensory_state": "sensory_reason",
        "meaning_memory_state": "meaning_memory_reason",
        "content_projection_state": "content_projection_reason",
    }
    for state_field, reason_field in conditional_dimension_reasons.items():
        if payload.get(state_field) == "NOT_APPLICABLE_WITH_REASON":
            reason = payload.get(reason_field)
            if not isinstance(reason, str) or not reason.strip():
                errors.append(f"{state_field}=NOT_APPLICABLE_WITH_REASON requires {reason_field}")

    genericity = payload.get("genericity_attack")
    if (
        strict_current_emission
        and isinstance(genericity, dict)
        and genericity.get("status") == "NOT_APPLICABLE_WITH_REASON"
    ):
        reason = genericity.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(
                "genericity_attack.status=NOT_APPLICABLE_WITH_REASON requires reason"
            )

    review_binding_required = strict_current_emission and (
        keep
        or maturity
        in {"DQ4_DISTINCTIVE_RESOLVED_SYSTEM", "DQ5_PROVEN_CROSS_CONTEXT_LANGUAGE"}
    )
    if review_binding_required:
        if not isinstance(independent, dict):
            errors.append("independent_design_review binding is required")
        else:
            reviewer_id = independent.get("reviewer_id")
            bindings = independent.get("review_input_bindings")
            if not isinstance(reviewer_id, str) or not reviewer_id.strip():
                errors.append(
                    "independent_design_review requires reviewer_id for consequential review"
                )
            if not isinstance(bindings, list) or not bindings:
                errors.append(
                    "independent_design_review requires exact review_input_bindings for consequential review"
                )
            else:
                artifact_refs = set(
                    ref
                    for ref in (payload.get("artifact_refs") or [])
                    if isinstance(ref, str)
                )
                for index, binding in enumerate(bindings):
                    if not isinstance(binding, dict):
                        errors.append(
                            f"independent_design_review.review_input_bindings[{index}] must be an object"
                        )
                        continue
                    artifact_ref = binding.get("artifact_ref")
                    revision = binding.get("revision_or_hash")
                    if artifact_ref not in artifact_refs:
                        errors.append(
                            f"independent_design_review.review_input_bindings[{index}].artifact_ref must match artifact_refs"
                        )
                    if not isinstance(revision, str) or not revision.strip():
                        errors.append(
                            f"independent_design_review.review_input_bindings[{index}] requires revision_or_hash"
                        )
                    if project_root is not None:
                        validate_resolvable_file_ref(
                            artifact_ref,
                            f"independent_design_review.review_input_bindings[{index}].artifact_ref",
                            errors,
                            project_root,
                        )

    if keep:
        if maturity == "DQ0_UNDEFINED":
            errors.append("KEEP cannot coexist with design_maturity=DQ0_UNDEFINED")
        if strict_current_emission and payload.get("in_claim_blocking_design_fail_count") != 0:
            errors.append(
                "schema_version 1.1 KEEP requires in_claim_blocking_design_fail_count=0"
            )
        if payload.get("stale") is not False:
            errors.append("KEEP requires stale=false")
        if not isinstance(independent, dict) or independent.get("status") != "KEEP":
            errors.append("KEEP requires independent_design_review.status=KEEP")
        elif independent.get("reviewer_independent_from_producer") is not True:
            errors.append("KEEP requires an independent reviewer")
        artifact_refs = payload.get("artifact_refs")
        if not artifact_refs:
            errors.append("KEEP requires artifact_refs")
        readback_conditions = payload.get("readback_conditions")
        if not isinstance(readback_conditions, list) or not readback_conditions:
            errors.append("KEEP requires readback_conditions")
        else:
            non_pass = [
                entry
                for entry in readback_conditions
                if not isinstance(entry, dict) or entry.get("status") != "PASS"
            ]
            if non_pass:
                errors.append("KEEP requires every declared readback_condition to be PASS")
            if isinstance(artifact_refs, list):
                covered_artifacts = {
                    entry.get("artifact_ref")
                    for entry in readback_conditions
                    if isinstance(entry, dict)
                    and isinstance(entry.get("artifact_ref"), str)
                    and entry.get("artifact_ref")
                }
                uncovered = sorted(
                    ref
                    for ref in artifact_refs
                    if isinstance(ref, str) and ref not in covered_artifacts
                )
                if uncovered:
                    errors.append(
                        "KEEP requires every artifact_ref to participate in readback_conditions: "
                        + ", ".join(uncovered)
                    )
        if payload.get("coherence_state") != "KEEP":
            errors.append("KEEP requires coherence_state=KEEP")
        core_dimension_fields = {
            "design_language_state",
            "experience_state",
            "detail_craft_state",
            "adaptation_state",
            "coherence_state",
        }
        for field in sorted(core_dimension_fields):
            value = payload.get(field)
            if value is not None and value != "KEEP":
                errors.append(f"KEEP requires core Design disposition {field}=KEEP, got {value}")
        conditional_dimension_fields = {
            "human_relation_state",
            "sensory_state",
            "meaning_memory_state",
            "content_projection_state",
        }
        for field in sorted(conditional_dimension_fields):
            value = payload.get(field)
            if value is not None and value not in {"KEEP", "NOT_APPLICABLE_WITH_REASON"}:
                errors.append(
                    f"KEEP cannot coexist with {field}={value}; use KEEP or NOT_APPLICABLE_WITH_REASON for declared dimension dispositions"
                )
        if not isinstance(genericity, dict) or genericity.get("status") not in {
            "PASS",
            "NOT_APPLICABLE_WITH_REASON",
        }:
            errors.append(
                "KEEP requires genericity_attack.status=PASS or NOT_APPLICABLE_WITH_REASON"
            )
        if strict_current_emission:
            coverage = body.get("section_coverage") or []
            by_role = {
                entry.get("semantic_role"): entry.get("status")
                for entry in coverage
                if isinstance(entry, dict)
            }
            for role in {
                "NATIVE_ARTIFACT_READBACK",
                "DECISION_MATURITY_CLAIM_CEILING",
            }:
                if by_role.get(role) not in {"PRESENT", "COMBINED"}:
                    errors.append(
                        f"schema_version 1.1 KEEP requires {role}=PRESENT or COMBINED"
                    )

    if payload.get("result") == "REVISE":
        root_cause = payload.get("root_cause")
        if not isinstance(root_cause, str) or not root_cause.strip():
            errors.append("REVISE requires root_cause")
    return errors


def validate_architecture(
    payload: dict[str, Any], project_root: Path | None = None
) -> list[str]:
    errors: list[str] = []

    if payload.get("receipt_type") != "ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT":
        errors.append("receipt_type must be ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT")
    if payload.get("triggered") is not True:
        errors.append("Architecture receipt requires triggered=true")
    trigger_reason = payload.get("trigger_reason")
    if (
        not isinstance(trigger_reason, list)
        or not trigger_reason
        or any(not isinstance(item, str) or not item.strip() for item in trigger_reason)
    ):
        errors.append("trigger_reason must be a non-empty array of non-empty strings")
    for field in ("project_stage", "claim_ceiling"):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} is required and must be non-empty")
    for field in ("open_items", "reopened_items"):
        value = payload.get(field)
        if not isinstance(value, list):
            errors.append(f"{field} is required and must be an array")
    root_does_not_prove = payload.get("does_not_prove")
    if (
        not isinstance(root_does_not_prove, list)
        or not root_does_not_prove
        or any(not isinstance(item, str) or not item.strip() for item in root_does_not_prove)
    ):
        errors.append("does_not_prove must be a non-empty array of non-empty strings")
    if payload.get("result") not in {"PASS", "REVISE", "REJECT", "HOLD"}:
        errors.append("result must be PASS, REVISE, REJECT, or HOLD")
    if not isinstance(payload.get("stale"), bool):
        errors.append("stale is required and must be boolean")
    independent_root = payload.get("independent_plan_review")
    if not isinstance(independent_root, dict):
        errors.append("independent_plan_review must be an object")
    else:
        if independent_root.get("status") not in {"PENDING", "PASS", "REVISE", "REJECT", "HOLD"}:
            errors.append("independent_plan_review.status is invalid")
        if not isinstance(independent_root.get("reviewer_independent_from_producer"), bool):
            errors.append("independent_plan_review.reviewer_independent_from_producer must be boolean")
        independent_reason = independent_root.get("reason")
        if not isinstance(independent_reason, str) or not independent_reason.strip():
            errors.append("independent_plan_review.reason is required")

    for field in (
        "jurisdiction_state",
        "program_authority_state",
        "occupancy_authority_state",
        "site_authority_state",
    ):
        value = payload.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"{field} is required and must be non-empty")

    records = payload.get("stage_body_records")
    if not isinstance(records, list) or not records:
        return ["stage_body_records must be a non-empty array"]

    overall_pass = payload.get("result") == "PASS"
    seen_stage_ids: set[str] = set()
    for index, record in enumerate(records):
        label = f"stage_body_records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{label}: expected object")
            continue
        stage_id = record.get("stage_id")
        if isinstance(stage_id, str):
            if stage_id not in ARCH_STAGE_IDS:
                errors.append(f"{label}: invalid architecture stage_id {stage_id}; expected ADD-00..ADD-17")
            if stage_id in seen_stage_ids:
                errors.append(f"{label}: duplicate stage_id {stage_id}")
            seen_stage_ids.add(stage_id)
        else:
            errors.append(f"{label}.stage_id is required")
        body_ref = record.get("body_ref")
        if not isinstance(body_ref, str) or not body_ref.strip():
            errors.append(f"{label}.body_ref is required")
        else:
            validate_resolvable_file_ref(body_ref, f"{label}.body_ref", errors, project_root)
        title = record.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{label}.title is required")
        elif title in GENERIC_TITLES:
            errors.append(f"{label}.title is generic and does not identify the decision object")
        if not isinstance(record.get("knowledge_mount_refs"), list):
            errors.append(f"{label}.knowledge_mount_refs must be an array")
        stage_claim_ceiling = record.get("claim_ceiling")
        if not isinstance(stage_claim_ceiling, str) or not stage_claim_ceiling.strip():
            errors.append(f"{label}.claim_ceiling is required")
        if not isinstance(record.get("open_items"), list):
            errors.append(f"{label}.open_items must be an array")
        reopen_triggers = record.get("reopen_triggers")
        if (
            not isinstance(reopen_triggers, list)
            or not reopen_triggers
            or any(not isinstance(item, str) or not item.strip() for item in reopen_triggers)
        ):
            errors.append(f"{label}.reopen_triggers must be a non-empty array of non-empty strings")
        if record.get("stage_verdict") not in {"PASS_AT_CLAIM_CEILING", "REVISE", "REJECT", "HOLD"}:
            errors.append(f"{label}.stage_verdict is invalid")

        stage_pass = record.get("stage_verdict") == "PASS_AT_CLAIM_CEILING"
        validate_section_coverage(
            record.get("section_coverage"), ARCH_ROLES, f"{label}.section_coverage", errors,
            pass_like=overall_pass or stage_pass,
        )

        if overall_pass and not stage_pass:
            errors.append(f"{label}: overall PASS requires PASS_AT_CLAIM_CEILING")
        if overall_pass or stage_pass:
            if not record.get("native_artifact_refs"):
                errors.append(f"{label}: PASS requires native_artifact_refs")
            if not record.get("readback_refs"):
                errors.append(f"{label}: PASS requires readback_refs")
        for ref_index, ref in enumerate(record.get("native_artifact_refs") or []):
            validate_resolvable_file_ref(
                ref,
                f"{label}.native_artifact_refs[{ref_index}]",
                errors,
                project_root,
            )
        for ref_index, ref in enumerate(record.get("readback_refs") or []):
            validate_resolvable_file_ref(
                ref,
                f"{label}.readback_refs[{ref_index}]",
                errors,
                project_root,
            )

    phase_status = payload.get("phase_status")
    phase_status_reasons = payload.get("phase_status_reasons")
    if not isinstance(phase_status, dict):
        errors.append("phase_status must be an object")
    else:
        missing_phase_keys = sorted(ARCH_PHASE_KEYS - set(phase_status))
        if missing_phase_keys:
            errors.append(f"phase_status missing required keys: {', '.join(missing_phase_keys)}")
        for phase, state in phase_status.items():
            if state not in ARCH_PHASE_STATES:
                errors.append(f"phase_status.{phase} has invalid state {state!r}")
            if state == "NOT_APPLICABLE_WITH_REASON":
                reason = (
                    phase_status_reasons.get(phase)
                    if isinstance(phase_status_reasons, dict)
                    else None
                )
                if not isinstance(reason, str) or not reason.strip():
                    errors.append(
                        f"phase_status.{phase}=NOT_APPLICABLE_WITH_REASON requires non-empty phase_status_reasons.{phase}"
                    )
    if phase_status_reasons is not None and not isinstance(phase_status_reasons, dict):
        errors.append("phase_status_reasons must be an object when present")

    cad_review = payload.get("architectural_cad_plan_review")
    if isinstance(cad_review, dict) and cad_review.get("applicable") is True:
        required_cad_fields = (
            "native_cad_ref",
            "target_scale",
            "machine_readback_result",
            "machine_readback_refs",
            "target_scale_plot_readback_refs",
            "architect_readback_result",
            "architect_readback_refs",
            "operational_review_refs",
            "wall_representation_state",
            "opening_host_binding_state",
            "core_packing_state",
            "claim_ceiling",
            "does_not_prove",
        )
        for field in required_cad_fields:
            value = cad_review.get(field)
            if value is None or value == "" or value == []:
                errors.append(f"architectural_cad_plan_review.{field} is required when applicable=true")
        validate_resolvable_file_ref(
            cad_review.get("native_cad_ref"),
            "architectural_cad_plan_review.native_cad_ref",
            errors,
            project_root,
        )
        for field in (
            "machine_readback_refs",
            "target_scale_plot_readback_refs",
            "architect_readback_refs",
            "operational_review_refs",
        ):
            for ref_index, ref in enumerate(cad_review.get(field) or []):
                validate_resolvable_file_ref(
                    ref,
                    f"architectural_cad_plan_review.{field}[{ref_index}]",
                    errors,
                    project_root,
                )
        if cad_review.get("architect_readback_result") == "PASS" and cad_review.get("machine_readback_result") != "PASS":
            errors.append("architectural CAD architect PASS requires machine_readback_result=PASS")
    elif isinstance(cad_review, dict) and cad_review.get("applicable") is False:
        reason = cad_review.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append("architectural_cad_plan_review.reason is required when applicable=false")

    cad_review_triggered = payload.get("architectural_cad_plan_review_triggered")
    if cad_review_triggered is True:
        if not isinstance(cad_review, dict) or cad_review.get("applicable") is not True:
            errors.append(
                "architectural_cad_plan_review_triggered=true requires architectural_cad_plan_review.applicable=true"
            )
    elif cad_review_triggered is False:
        if isinstance(cad_review, dict) and cad_review.get("applicable") is True:
            errors.append(
                "architectural_cad_plan_review_triggered=false cannot coexist with architectural_cad_plan_review.applicable=true"
            )
    elif cad_review_triggered is not None:
        errors.append("architectural_cad_plan_review_triggered must be boolean when present")

    add07_cad_native = any(
        record.get("stage_id") == "ADD-07"
        and any(
            isinstance(ref, str) and Path(ref.replace("\\", "/")).suffix.lower() in {".dwg", ".dxf"}
            for ref in (record.get("native_artifact_refs") or [])
        )
        for record in records
        if isinstance(record, dict)
    )
    if add07_cad_native and cad_review_triggered is not True:
        errors.append(
            "ADD-07 native DWG/DXF plan carrier requires architectural_cad_plan_review_triggered=true"
        )

    publication_state = payload.get("architecture_representation_publication_state")
    if isinstance(publication_state, dict) and publication_state.get("applicable") is True:
        required_publication_fields = (
            "current_native_master_refs",
            "publication_handoff_refs",
            "style_effect_material",
            "target_medium_readback_refs",
            "truth_boundary_state",
            "owner_boundary_state",
            "claim_ceiling",
            "does_not_prove",
            "reopen_triggers",
        )
        for field in required_publication_fields:
            value = publication_state.get(field)
            if value is None or value == "" or value == []:
                errors.append(
                    f"architecture_representation_publication_state.{field} is required when applicable=true"
                )
        for field in (
            "current_native_master_refs",
            "review_view_refs",
            "analysis_state_view_refs",
            "publication_handoff_refs",
            "effect_off_source_baseline_refs",
            "target_medium_readback_refs",
        ):
            for ref_index, ref in enumerate(publication_state.get(field) or []):
                validate_resolvable_file_ref(
                    ref,
                    f"architecture_representation_publication_state.{field}[{ref_index}]",
                    errors,
                    project_root,
                )
        if publication_state.get("representation_style_contract_ref"):
            validate_resolvable_file_ref(
                publication_state.get("representation_style_contract_ref"),
                "architecture_representation_publication_state.representation_style_contract_ref",
                errors,
                project_root,
            )
        style_effect_material = publication_state.get("style_effect_material")
        if style_effect_material is True:
            if not publication_state.get("representation_style_contract_ref"):
                errors.append(
                    "architecture_representation_publication_state.representation_style_contract_ref is required when style_effect_material=true"
                )
            if not publication_state.get("effect_off_source_baseline_refs"):
                errors.append(
                    "architecture_representation_publication_state.effect_off_source_baseline_refs is required when style_effect_material=true"
                )
        elif style_effect_material is False:
            reason = publication_state.get("style_effect_reason")
            if not isinstance(reason, str) or not reason.strip():
                errors.append(
                    "architecture_representation_publication_state.style_effect_reason is required when style_effect_material=false"
                )
        elif style_effect_material is not None:
            errors.append(
                "architecture_representation_publication_state.style_effect_material must be boolean"
            )
    elif isinstance(publication_state, dict) and publication_state.get("applicable") is False:
        reason = publication_state.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(
                "architecture_representation_publication_state.reason is required when applicable=false"
            )

    publication_triggered = payload.get("architecture_representation_publication_triggered")
    if publication_triggered is True:
        if not isinstance(publication_state, dict) or publication_state.get("applicable") is not True:
            errors.append(
                "architecture_representation_publication_triggered=true requires architecture_representation_publication_state.applicable=true"
            )
    elif publication_triggered is False:
        if isinstance(publication_state, dict) and publication_state.get("applicable") is True:
            errors.append(
                "architecture_representation_publication_triggered=false cannot coexist with architecture_representation_publication_state.applicable=true"
            )
    elif publication_triggered is not None:
        errors.append("architecture_representation_publication_triggered must be boolean when present")

    if overall_pass:
        if cad_review_triggered not in {True, False}:
            errors.append("Architecture PASS requires architectural_cad_plan_review_triggered=true or false")
        if publication_triggered not in {True, False}:
            errors.append("Architecture PASS requires architecture_representation_publication_triggered=true or false")
        missing_stage_ids = sorted(ARCH_STAGE_IDS - seen_stage_ids)
        extra_stage_ids = sorted(seen_stage_ids - ARCH_STAGE_IDS)
        if missing_stage_ids:
            errors.append(
                f"Architecture PASS requires stage_body_records for all ADD-00..ADD-17; missing: {', '.join(missing_stage_ids)}"
            )
        if extra_stage_ids:
            errors.append(
                f"Architecture PASS contains invalid extra stage ids: {', '.join(extra_stage_ids)}"
            )
        if isinstance(phase_status, dict):
            for phase in sorted(ARCH_PHASE_KEYS):
                state = phase_status.get(phase)
                if state not in ARCH_CLOSED_PHASE_STATES:
                    errors.append(
                        f"Architecture PASS requires phase_status.{phase}=PASS_AT_CLAIM_CEILING or NOT_APPLICABLE_WITH_REASON; got {state!r}"
                    )
        if payload.get("stale") is not False:
            errors.append("Architecture PASS requires stale=false")
        independent = payload.get("independent_plan_review")
        if not isinstance(independent, dict) or independent.get("status") != "PASS":
            errors.append("Architecture PASS requires independent_plan_review.status=PASS")
        elif independent.get("reviewer_independent_from_producer") is not True:
            errors.append("Architecture PASS requires an independent plan reviewer")
        if isinstance(cad_review, dict) and cad_review.get("applicable") is True:
            if cad_review.get("machine_readback_result") != "PASS":
                errors.append("Architecture PASS with CAD plan requires machine_readback_result=PASS")
            if cad_review.get("architect_readback_result") != "PASS":
                errors.append("Architecture PASS with CAD plan requires architect_readback_result=PASS")
            for field in ("wall_representation_state", "opening_host_binding_state", "core_packing_state"):
                if cad_review.get(field) != "PASS_AT_CLAIM_CEILING":
                    errors.append(f"Architecture PASS with CAD plan requires {field}=PASS_AT_CLAIM_CEILING")
        if isinstance(publication_state, dict) and publication_state.get("applicable") is True:
            if publication_state.get("truth_boundary_state") != "PASS_AT_CLAIM_CEILING":
                errors.append(
                    "Architecture PASS with publication handoff requires truth_boundary_state=PASS_AT_CLAIM_CEILING"
                )
            if publication_state.get("owner_boundary_state") != "PASS_AT_CLAIM_CEILING":
                errors.append(
                    "Architecture PASS with publication handoff requires owner_boundary_state=PASS_AT_CLAIM_CEILING"
                )
    return errors


def validate_schema(payload: dict[str, Any], schema_path: Path) -> list[str]:
    if Draft202012Validator is None:
        return []
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        f"schema: {error.message}"
        for error in sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    ]


def validate_payload(
    payload: dict[str, Any], project_root: Path | None = None
) -> list[str]:
    receipt_type = payload.get("receipt_type")
    schema_path = SCHEMAS.get(receipt_type)
    if schema_path is None:
        return [f"unsupported receipt_type: {receipt_type!r}"]

    errors = validate_schema(payload, schema_path)
    if receipt_type == "DESIGN_QUALITY_DEVELOPMENT_RECEIPT":
        errors.extend(validate_design_quality(payload, project_root=project_root))
    elif receipt_type == "ARCHITECTURE_DESIGN_DEVELOPMENT_RECEIPT":
        errors.extend(validate_architecture(payload, project_root=project_root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("receipt", type=Path)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help="Optional project root used to dereference path-like project artifact, Design DNA and Operational Mount refs.",
    )
    args = parser.parse_args()

    try:
        payload = load_json(args.receipt)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"DESIGN DEVELOPMENT RECEIPT VALIDATION: FAIL\n- {exc}")
        return 1

    project_root = args.project_root.resolve() if args.project_root is not None else None
    errors = validate_payload(payload, project_root=project_root)
    if errors:
        print("DESIGN DEVELOPMENT RECEIPT VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("DESIGN DEVELOPMENT RECEIPT VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
