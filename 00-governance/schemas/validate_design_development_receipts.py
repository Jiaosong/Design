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
        if status in {"PRESENT", "COMBINED"} and not entry.get("visible_heading_or_locator"):
            errors.append(
                f"{label}.{role}: {status} requires visible_heading_or_locator"
            )
        if status == "NOT_APPLICABLE_WITH_REASON" and not entry.get("reason"):
            errors.append(f"{label}.{role}: N/A requires reason")
        if pass_like and status == "MISSING":
            errors.append(f"{label}.{role}: PASS/KEEP cannot retain MISSING")


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


def validate_architecture(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
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
            if stage_id in seen_stage_ids:
                errors.append(f"{label}: duplicate stage_id {stage_id}")
            seen_stage_ids.add(stage_id)
        title = record.get("title")
        if not isinstance(title, str) or not title.strip():
            errors.append(f"{label}.title is required")
        elif title in GENERIC_TITLES:
            errors.append(f"{label}.title is generic and does not identify the decision object")

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

    if overall_pass:
        if payload.get("stale") is not False:
            errors.append("Architecture PASS requires stale=false")
        independent = payload.get("independent_plan_review")
        if not isinstance(independent, dict) or independent.get("status") != "PASS":
            errors.append("Architecture PASS requires independent_plan_review.status=PASS")
        elif independent.get("reviewer_independent_from_producer") is not True:
            errors.append("Architecture PASS requires an independent plan reviewer")
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
        errors.extend(validate_architecture(payload))
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
