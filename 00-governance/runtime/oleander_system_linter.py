#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from oleander_environment_resolver import build_current_execution_view
from oleander_design_system_runtime import (
    admit_source,
    resolve_bounded_product_action_guard,
    resolve_browser_capture_ingress_guard,
)
from oleander_execution_runtime import ExecutionLedger
from oleander_system_gateway import validate_system_manifest


ROOT = Path(__file__).resolve().parents[2]
WORKSPACE_ROOT = ROOT.parent.parent if ROOT.parent.name == ".worktrees" else ROOT

MANIFEST = ROOT / "00-governance" / "runtime" / "OLEANDER_SYSTEM_MANIFEST_v0.2.json"
ADAPTER = ROOT / "00-governance" / "runtime" / "OLEANDER_COS_HARNESS_ADAPTER_v0.2.json"
PROVIDER = ROOT / "00-governance" / "runtime" / "OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.2.json"
PROVIDER_V01 = ROOT / "00-governance" / "runtime" / "OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json"
PRIMITIVES = ROOT / "00-governance" / "runtime" / "OLEANDER_EXECUTION_RUNTIME_PRIMITIVES_v0.1.json"
CORE_PRIMITIVES = ROOT / "00-governance" / "runtime" / "OLEANDER_CORE_INTERFACE_PRIMITIVES_v0.1.json"
SURFACES = ROOT / "00-governance" / "runtime" / "OLEANDER_SHARED_EXECUTION_SURFACES_v0.1.json"
DISPOSITION = ROOT / "00-governance" / "runtime" / "OLEANDER_SYSTEM_COMPONENT_DISPOSITION_v0.2.json"
BENCHMARK_V01 = ROOT / "00-governance" / "runtime" / "runtime_provider_spikes" / "results" / "OLEANDER_RUNTIME_PROVIDER_BENCHMARK_20260926.json"
DESIGN_SYSTEM_ARCH = ROOT / "00-governance" / "runtime" / "OLEANDER_DESIGN_SYSTEM_ARCHITECTURE_v0.1.md"
DESIGN_SYSTEM_OBJECTS = ROOT / "00-governance" / "runtime" / "OLEANDER_DESIGN_SYSTEM_OBJECT_MODEL_v0.1.json"
SURFACE_RELIABILITY = ROOT / "00-governance" / "runtime" / "OLEANDER_SURFACE_RELIABILITY_BOUNDARY_v0.1.json"
PROJECT_WORKSPACE = ROOT / "00-governance" / "runtime" / "OLEANDER_PROJECT_WORKSPACE_BINDING_v0.1.json"
SOURCE_INGESTION = ROOT / "00-governance" / "runtime" / "OLEANDER_SOURCE_INGESTION_PIPELINE_v0.1.json"
DERIVED_INTEGRITY = ROOT / "00-governance" / "runtime" / "OLEANDER_DERIVED_ARTIFACT_INTEGRITY_v0.1.json"
SOURCE_TRANSCRIPTION = ROOT / "00-governance" / "runtime" / "OLEANDER_SOURCE_TRANSCRIPTION_CONTRACT_v0.1.json"
HOST_RUNTIME = ROOT / "00-governance" / "runtime" / "OLEANDER_HOST_RUNTIME_CONTRACT_v0.1.json"
DSH_ADAPTER = ROOT / "00-governance" / "runtime" / "OLEANDER_DSH_HOST_ADAPTER_v0.1.json"
PRODUCT_SHELL = ROOT / "apps" / "oleander-design-system" / "index.html"
PRODUCT_HOST = ROOT / "apps" / "oleander-design-system" / "host.py"
PROJECT_MIGRATION = ROOT / "00-governance" / "runtime" / "OLEANDER_PROJECT_REPOSITORY_MIGRATION_INVENTORY_20260927.json"
SURFACE_VIEW = ROOT / "00-governance" / "runtime" / "OLEANDER_SURFACE_VIEW_CONTRACT_v0.1.json"
HOST_RUNTIME_PROBE = ROOT / "00-governance" / "runtime" / "oleander_host_runtime_probe.py"

FORBIDDEN_AUTHORITY = {
    "project_state",
    "project_current",
    "current",
    "design_decision",
    "design_keep",
    "professional_pass",
    "artifact_current",
    "knowledge_authority",
    "source_authority",
    "promotion",
    "release_authority",
    "statutory_approval",
}


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one object")
    return value


def _owner_exists(ref: str) -> bool:
    if ref.startswith(".mcp-runtime/"):
        return (WORKSPACE_ROOT / ref).exists()
    return (ROOT / ref).exists()


def _find_forbidden_keys(value: Any, forbidden: set[str], path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if str(key).lower() in forbidden:
                hits.append(child)
            hits.extend(_find_forbidden_keys(item, forbidden, child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(_find_forbidden_keys(item, forbidden, f"{path}[{index}]"))
    return hits


def run_lint() -> dict[str, Any]:
    manifest = _load(MANIFEST)
    adapter = _load(ADAPTER)
    provider = _load(PROVIDER)
    provider_v01 = _load(PROVIDER_V01)
    primitives = _load(PRIMITIVES)
    core_primitives = _load(CORE_PRIMITIVES)
    surfaces = _load(SURFACES)
    disposition = _load(DISPOSITION)
    benchmark_v01 = _load(BENCHMARK_V01)
    design_objects = _load(DESIGN_SYSTEM_OBJECTS)
    surface_reliability = _load(SURFACE_RELIABILITY)
    project_workspace = _load(PROJECT_WORKSPACE)
    source_ingestion = _load(SOURCE_INGESTION)
    derived_integrity = _load(DERIVED_INTEGRITY)
    source_transcription = _load(SOURCE_TRANSCRIPTION)
    host_runtime = _load(HOST_RUNTIME)
    dsh_adapter = _load(DSH_ADAPTER)
    project_migration = _load(PROJECT_MIGRATION)
    surface_view = _load(SURFACE_VIEW)
    source_admission_probe = admit_source({
        "source_id": "LINT-SOURCE",
        "source_kind": "TEXT",
        "original_ref": "lint:source",
        "fingerprint": "sha256:lint",
        "source_revision": "sha256:lint",
        "provenance": {"origin": "linter"},
    })
    source_forbidden_fields = {
        str(x).lower() for x in source_ingestion.get("forbidden_output_authority_fields") or []
    }
    source_output_authority_hits = _find_forbidden_keys(
        source_admission_probe.get("source") or {},
        source_forbidden_fields,
    )
    action_guard_allow_probe = resolve_bounded_product_action_guard(
        intent="CREATE_TRANSCRIPTION_REQUEST",
        target_ref="source:LINT-SOURCE/transcription/requests/TRQ-lint",
        side_effect_class="LOCAL_MUTATION",
        source_context={"source_id": "LINT-SOURCE", "source_revision": "sha256:lint"},
        action_authority_ceiling="SOURCE_TRANSCRIPTION_DERIVATIVE_ONLY",
        external_disclosure=False,
    )
    action_guard_hold_probe = resolve_bounded_product_action_guard(
        intent="CREATE_TRANSCRIPTION_REQUEST",
        target_ref="source:LINT-SOURCE/transcription/requests/TRQ-lint",
        side_effect_class="LOCAL_MUTATION",
        source_context={"source_id": "LINT-SOURCE", "source_revision": "sha256:lint"},
        action_authority_ceiling="SOURCE_TRANSCRIPTION_DERIVATIVE_ONLY",
        external_disclosure=True,
    )
    browser_capture_allow_probe = resolve_browser_capture_ingress_guard(
        url="https://example.com/lint",
        browser_profile={
            "browser_profile_id": "browser-profile:lint",
            "scope": "RESEARCH",
            "project_id": None,
            "capture_target": "SOURCE_INBOX",
        },
        capture_digest="sha256:" + ("a" * 64),
        external_disclosure=False,
    )
    browser_capture_hold_probe = resolve_browser_capture_ingress_guard(
        url="file:///C:/private.txt",
        browser_profile={
            "browser_profile_id": "browser-profile:lint",
            "scope": "RESEARCH",
            "project_id": None,
            "capture_target": "SOURCE_INBOX",
        },
        capture_digest="sha256:" + ("b" * 64),
        external_disclosure=False,
    )

    manifest_validation = validate_system_manifest()
    components = [x for x in disposition.get("components") or [] if isinstance(x, dict)]
    component_ids = [str(x.get("component_id")) for x in components]
    allowed_dispositions = set(disposition.get("allowed_dispositions") or [])
    invalid_dispositions = sorted({str(x.get("target_disposition")) for x in components if x.get("target_disposition") not in allowed_dispositions})
    missing_owner_refs = sorted({str(x.get("current_owner")) for x in components if isinstance(x.get("current_owner"), str) and not _owner_exists(str(x["current_owner"]))})
    missing_predecessor_refs = sorted({str(x.get("predecessor_owner")) for x in components if isinstance(x.get("predecessor_owner"), str) and not _owner_exists(str(x["predecessor_owner"]))})
    expected_core_primitives = {
        "AuthorityRef",
        "ProjectRef",
        "KnowledgeMount",
        "DecisionObject",
        "ProfessionalStageRef",
        "ActionRequest",
        "ExecutionRoute",
        "ArtifactRef",
        "ReadbackResult",
        "ReviewResult",
        "PersistenceReceipt",
        "LearningCandidate",
    }
    actual_core_primitives = set((core_primitives.get("primitives") or {}).keys())
    missing_core_owner_refs: list[str] = []
    for primitive in (core_primitives.get("primitives") or {}).values():
        if not isinstance(primitive, dict):
            continue
        for ref in primitive.get("owner_contracts") or []:
            if isinstance(ref, str) and not _owner_exists(ref):
                missing_core_owner_refs.append(ref)

    surface_rows = surfaces.get("surfaces") or {}
    connector_ceiling_violations: list[str] = []
    global_current_violations: list[str] = []
    misleading_roles: list[str] = []
    for surface_id, row in surface_rows.items():
        if not isinstance(row, dict):
            continue
        if surface_id.endswith("_connector") and row.get("authority_ceiling") != "EXECUTION_CAPABILITY_ONLY":
            connector_ceiling_violations.append(surface_id)
        if row.get("global_current_store") is True:
            global_current_violations.append(surface_id)
        role = str(row.get("role") or "")
        if role.startswith("CURRENT_"):
            misleading_roles.append(surface_id)

    forbidden_provider = set((provider.get("execution_ledger") or {}).get("forbidden_authority_fields") or [])
    forbidden_primitives = set((primitives.get("primitives") or {}).get("ExecutionLedger", {}).get("forbidden_authority_fields") or [])
    adapter_owns = {str(x).lower() for x in adapter.get("owns") or []}

    ledger_runtime_guard = False
    try:
        ExecutionLedger().append(
            provider_id="lint",
            action_id="lint-authority-leak",
            event_type="EXECUTION_OBSERVED",
            outcome="TEST",
            payload={"project_state": {"forbidden": True}},
        )
    except ValueError:
        ledger_runtime_guard = True

    capability_view = build_current_execution_view()
    local_snapshot = capability_view.get("local_snapshot") or {}
    stale_available = [
        str(row.get("surface_id"))
        for row in local_snapshot.get("surfaces") or []
        if isinstance(row, dict) and row.get("availability") == "AVAILABLE"
    ] if local_snapshot.get("state") == "STALE" else []

    expected_layers = [f"R-{chr(code)}" for code in range(ord("A"), ord("K") + 1)]
    actual_layers = list((manifest.get("architecture") or {}).get("counting_rule", {}).get("runtime_layer_ids") or [])
    reliability_stages = set((surface_reliability.get("stages") or {}).keys())
    expected_reliability_stages = {"R1_ADMISSION", "R2_IDENTITY", "R3_CAPABILITY", "R4_EXECUTION", "R5_RESULT"}
    project_non_equivalences = set((design_objects.get("project_model") or {}).get("hard_non_equivalences") or [])
    knowledge_non_equivalences = set((design_objects.get("knowledge_model") or {}).get("hard_non_equivalences") or [])
    reference_patterns = surface_reliability.get("reference_patterns") or {}
    dsh_reference = reference_patterns.get("deepseek_harness") or {}
    agy_reference = reference_patterns.get("dsh_agy_link") or {}
    migration_projects = [x for x in project_migration.get("projects") or [] if isinstance(x, dict)]

    checks = {
        "phase1_manifest_validation_pass": manifest_validation.get("status") == "PASS",
        "manifest_is_v02_successor": manifest.get("schema") == "oleander.system-manifest.v0.2" and manifest.get("supersedes") == "00-governance/runtime/OLEANDER_SYSTEM_MANIFEST_v0.1.json",
        "stable_runtime_layers_unchanged": actual_layers == expected_layers,
        "component_ids_unique": len(component_ids) == len(set(component_ids)),
        "component_dispositions_valid": not invalid_dispositions,
        "component_owner_refs_resolve": not missing_owner_refs,
        "component_predecessor_refs_resolve": not missing_predecessor_refs,
        "core_interface_primitive_set_exact": actual_core_primitives == expected_core_primitives,
        "core_interface_owner_refs_resolve": not missing_core_owner_refs,
        "core_interface_is_non_authority": core_primitives.get("authority_ceiling") == "REFERENCE_ENVELOPE_AND_HANDOFF_ONLY",
        "connector_authority_ceiling_enforced": not connector_ceiling_violations,
        "execution_surface_never_global_current": not global_current_violations,
        "no_connector_role_claims_current": not misleading_roles,
        "cos_forbidden_authority_ownership_absent": not (adapter_owns & FORBIDDEN_AUTHORITY),
        "provider_ledger_forbids_all_authority_fields": FORBIDDEN_AUTHORITY.issubset(forbidden_provider),
        "primitive_ledger_forbids_all_authority_fields": FORBIDDEN_AUTHORITY.issubset(forbidden_primitives),
        "provider_v02_is_strict_successor_not_benchmark_rewrite": (
            provider.get("supersedes") == "00-governance/runtime/OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json"
            and set(provider_v01.get("providers_under_spike") or []) == set(provider.get("providers_under_spike") or [])
            and set(provider_v01.get("required_provider_operations") or []).issubset(set(provider.get("required_provider_operations") or []))
            and set(provider_v01.get("hard_invariants") or []).issubset(set(provider.get("hard_invariants") or []))
            and set((provider_v01.get("execution_ledger") or {}).get("forbidden_authority_fields") or []).issubset(forbidden_provider)
            and benchmark_v01.get("contract_ref") == "00-governance/runtime/OLEANDER_RUNTIME_PROVIDER_CONTRACT_v0.1.json"
        ),
        "provider_v02_binds_cos_adapter_v02": (
            (provider.get("native_cos_mapping") or {}).get("adapter") == "00-governance/runtime/OLEANDER_COS_HARNESS_ADAPTER_v0.2.json"
            and "00-governance/runtime/OLEANDER_COS_HARNESS_ADAPTER_v0.2.json" in (provider.get("architecture_refs") or [])
        ),
        "provider_and_cos_bind_core_interface_contract": (
            provider.get("core_interface_contract") == "00-governance/runtime/OLEANDER_CORE_INTERFACE_PRIMITIVES_v0.1.json"
            and adapter.get("core_interface_contract") == "00-governance/runtime/OLEANDER_CORE_INTERFACE_PRIMITIVES_v0.1.json"
        ),
        "ledger_runtime_rejects_authority_fields": ledger_runtime_guard,
        "runtime_primitives_authority_ceiling": primitives.get("authority_ceiling") == "EXECUTION_CAPABILITY_AND_OBSERVABILITY_ONLY",
        "stale_local_snapshot_cannot_claim_available": not stale_available,
        "gateway_exposes_phase2_operations": {"capabilities", "resolve"}.issubset(set((manifest.get("gateway") or {}).get("operations") or [])),
        "design_system_successor_architecture_exists": DESIGN_SYSTEM_ARCH.is_file(),
        "design_system_successor_refs_are_non_authority": (manifest.get("design_system_successor") or {}).get("authority_ceiling") == "REFERENCE_AND_EXECUTION_ORCHESTRATION_ONLY",
        "surface_reliability_stage_set_exact": reliability_stages == expected_reliability_stages,
        "surface_reliability_is_non_authority": surface_reliability.get("authority_ceiling") == "EXECUTION_RELIABILITY_EVIDENCE_ONLY",
        "surface_reliability_separates_observation_interpretation_authority": {
            "OBSERVATION_IS_NOT_INTERPRETATION",
            "INTERPRETATION_IS_NOT_DERIVED_RELIABILITY_STATE",
            "DERIVED_RELIABILITY_STATE_IS_NOT_AUTHORITY_STATE",
        }.issubset(set(surface_reliability.get("hard_invariants") or [])),
        "surface_reliability_forbids_blind_mutating_fallback": "UNCERTAIN_MUTATION_SIDE_EFFECT_REQUIRES_READBACK_BEFORE_RETRY_OR_FALLBACK" in set(surface_reliability.get("hard_invariants") or []),
        "project_git_workspace_stores_are_separated": {
            "PROJECT_NE_REPOSITORY",
            "PROJECT_NE_RUNTIME_WORKSPACE",
            "PROJECT_NE_ARTIFACT_STORE",
            "PROJECT_NE_KNOWLEDGE_STORE",
            "GIT_BRANCH_NE_DESIGN_DIRECTION",
            "GIT_MERGE_NE_DESIGN_KEEP",
        }.issubset(project_non_equivalences),
        "knowledge_body_is_not_vector_index": "VECTOR_INDEX_NE_KNOWLEDGE" in knowledge_non_equivalences,
        "surface_view_cannot_bypass_action_runtime": "ACTION_RUNTIME" in str((design_objects.get("surface_view_model") or {}).get("rule") or ""),
        "dsh_and_agy_are_reference_patterns_not_authority": (
            dsh_reference.get("role") == "HOST_RUNTIME_REFERENCE"
            and agy_reference.get("role") == "PROVIDER_ADAPTER_RELIABILITY_REFERENCE"
            and agy_reference.get("do_not_copy_as_authority") is True
        ),
        "project_workspace_binding_is_non_authority": project_workspace.get("authority_ceiling") == "PROJECT_MATERIALIZATION_BINDING_ONLY",
        "project_workspace_forbids_materialization_authority_fields": {
            "project_current", "design_keep", "professional_pass", "promotion"
        }.issubset(set(project_workspace.get("forbidden_materialization_authority_fields") or [])),
        "source_ingestion_is_draft_only": source_ingestion.get("authority_ceiling") == "SOURCE_EXTRACTION_AND_KNOWLEDGE_DRAFT_ONLY",
        "source_ingestion_preserves_original_and_citations": {
            "PRESERVE_ORIGINAL", "BIND_CITATIONS", "CREATE_KNOWLEDGE_DRAFT"
        }.issubset(set(source_ingestion.get("pipeline") or [])),
        "source_ingestion_never_sets_knowledge_current": (
            "knowledge_current" in source_forbidden_fields
            and source_admission_probe.get("status") == "ADMITTED"
            and not source_output_authority_hits
        ),
        "source_ingestion_binds_derived_integrity_and_transcription_contracts": (
            source_ingestion.get("derived_integrity_contract") == "00-governance/runtime/OLEANDER_DERIVED_ARTIFACT_INTEGRITY_v0.1.json"
            and source_ingestion.get("transcription_contract") == "00-governance/runtime/OLEANDER_SOURCE_TRANSCRIPTION_CONTRACT_v0.1.json"
        ),
        "browser_capture_ingress_is_source_first_bounded_and_not_provider_proof": (
            {
                "BROWSER_PAGE_LOADED_NE_SOURCE_CAPTURED",
                "SOURCE_CAPTURED_NE_KNOWLEDGE_INGESTED",
                "BROWSER_CAPTURE_RECEIPT_NE_BROWSER_PROVIDER_BOUND",
                "BROWSER_CAPTURE_INGRESS_REQUIRES_ACTION_RUNTIME_AND_R5_READBACK",
            }.issubset(set(source_ingestion.get("hard_invariants") or []))
            and browser_capture_allow_probe.get("decision") == "ALLOW"
            and browser_capture_allow_probe.get("authority_ceiling") == "BOUNDED_EXECUTION_POLICY_ONLY"
            and "BROWSER_PROVIDER_BOUND" in set(browser_capture_allow_probe.get("does_not_prove") or [])
            and browser_capture_hold_probe.get("decision") == "HOLD"
        ),
        "derived_integrity_is_readback_only_and_source_bound": (
            derived_integrity.get("authority_ceiling") == "DERIVED_ARTIFACT_READBACK_ONLY"
            and {
                "SOURCE_INTEGRITY_NE_DERIVED_INTEGRITY",
                "DERIVED_FILE_PRESENT_NE_DERIVED_VERIFIED",
                "DERIVED_VERIFIED_NE_KNOWLEDGE_CURRENT",
            }.issubset(set(derived_integrity.get("hard_invariants") or []))
        ),
        "source_transcription_is_derivative_only_and_persistent_not_provider_bound": (
            source_transcription.get("authority_ceiling") == "SOURCE_TRANSCRIPTION_DERIVATIVE_ONLY"
            and {
                "TRANSCRIPTION_REQUEST_NE_TRANSCRIPT",
                "REQUEST_PERSISTED_NE_PROVIDER_BOUND",
                "PRODUCT_ACTION_NE_ACTION_GUARD_DECISION",
                "REQUEST_REUSE_REQUIRES_READBACK_BEFORE_MUTATION",
                "TRANSCRIPT_NE_STRUCTURED_KNOWLEDGE_BODY",
                "SOURCE_TRANSCRIPTION_NE_KNOWLEDGE_CURRENT",
            }.issubset(set(source_transcription.get("hard_invariants") or []))
            and (source_transcription.get("dsh_reference") or {}).get("role") == "TRANSIENT_SPEECH_PROVIDER_SEAM_REFERENCE_ONLY"
        ),
        "bounded_product_action_guard_is_non_authority_and_fail_closed": (
            action_guard_allow_probe.get("status") == "PASS"
            and action_guard_allow_probe.get("decision") == "ALLOW"
            and action_guard_allow_probe.get("authority_ceiling") == "BOUNDED_EXECUTION_POLICY_ONLY"
            and "KNOWLEDGE_CURRENT" in set(action_guard_allow_probe.get("does_not_prove") or [])
            and action_guard_hold_probe.get("status") == "HOLD"
            and action_guard_hold_probe.get("decision") == "HOLD"
        ),
        "transcription_request_reuse_contract_requires_readback_before_mutation": (
            "REQUEST_DIGEST_AND_SOURCE_REVISION_MUST_MATCH_RECEIPT_BEFORE_REQUEST_IS_REUSED"
            == str((source_transcription.get("persistence") or {}).get("request_readback") or "")
            and "BEFORE_ANY_MUTATION"
            in str((source_transcription.get("persistence") or {}).get("reuse_rule") or "")
            and "MUST_NOT_MANUFACTURE_ALLOW"
            in str((source_transcription.get("persistence") or {}).get("action_guard_rule") or "")
        ),
        "system_manifest_registers_derived_integrity_and_transcription": (
            (manifest.get("system_interfaces") or {}).get("derived_artifact_integrity") == "00-governance/runtime/OLEANDER_DERIVED_ARTIFACT_INTEGRITY_v0.1.json"
            and (manifest.get("system_interfaces") or {}).get("source_transcription_contract") == "00-governance/runtime/OLEANDER_SOURCE_TRANSCRIPTION_CONTRACT_v0.1.json"
            and (manifest.get("design_system_successor") or {}).get("derived_artifact_integrity") == "00-governance/runtime/OLEANDER_DERIVED_ARTIFACT_INTEGRITY_v0.1.json"
            and (manifest.get("design_system_successor") or {}).get("source_transcription_contract") == "00-governance/runtime/OLEANDER_SOURCE_TRANSCRIPTION_CONTRACT_v0.1.json"
        ),
        "host_runtime_contract_is_execution_only": host_runtime.get("authority_ceiling") == "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY",
        "host_runtime_forbids_project_knowledge_design_authority": {
            "PROJECT_STATE", "PROJECT_CURRENT", "KNOWLEDGE_AUTHORITY", "KNOWLEDGE_CURRENT", "DESIGN_KEEP", "PROMOTION"
        }.issubset(set((host_runtime.get("state_ownership") or {}).get("must_not_own") or [])),
        "dsh_adapter_is_reference_not_authority": (
            dsh_adapter.get("status") == "CANDIDATE_REFERENCE_ADAPTER"
            and dsh_adapter.get("authority_ceiling") == "EXECUTION_HOST_AND_SURFACE_LIFECYCLE_ONLY"
            and dsh_adapter.get("host_runtime_contract") == "00-governance/runtime/OLEANDER_HOST_RUNTIME_CONTRACT_v0.1.json"
        ),
        "design_system_product_shell_exists": PRODUCT_SHELL.is_file(),
        "design_system_local_host_exists": PRODUCT_HOST.is_file(),
        "host_runtime_probe_exists": HOST_RUNTIME_PROBE.is_file(),
        "surface_view_is_projection_only": (
            surface_view.get("authority_ceiling") == "UI_PROJECTION_ONLY"
            and "SURFACE_VIEW_IS_PROJECTION_NOT_REGISTRY" in set(surface_view.get("hard_invariants") or [])
            and "SURFACE_VIEW_MUST_NOT_INVENT_RELIABILITY" in set(surface_view.get("hard_invariants") or [])
        ),
        "browser_profile_is_not_project_state": (
            (surface_view.get("browser_profile") or {}).get("semantic_class") == "BROWSER_CONTEXT_PROJECTION_NOT_PROJECT_STATE"
            and "BROWSER_PROFILE_NE_PROJECT_STATE" in set((surface_view.get("browser_profile") or {}).get("rules") or [])
        ),
        "project_repository_migration_is_non_authority": project_migration.get("authority_ceiling") == "MIGRATION_READBACK_ONLY",
        "project_repository_migration_local_repos_ready": (
            project_migration.get("status") == "LOCAL_REPOSITORIES_READY"
            and len(migration_projects) == 4
            and all(row.get("migration_state") == "SPLIT_BRANCH_READY" for row in migration_projects)
            and all(row.get("local_repository_ready") is True for row in migration_projects)
            and all(row.get("local_repository_contains_split_history") is True for row in migration_projects)
            and all(row.get("split_is_subdirectory_rooted") is True for row in migration_projects)
        ),
        "project_repository_migration_project_state_resolution_is_fail_closed": (
            (project_migration.get("binding_progress") or {}).get("owner_native_project_state_verified") == 1
            and (project_migration.get("binding_progress") or {}).get("project_state_unresolved") == 3
            and "PUBLIC_STATUS_SUMMARY_NE_OWNER_NATIVE_PROJECT_STATE" in set(project_migration.get("hard_invariants") or [])
            and "BOOTSTRAP_MANIFEST_IS_LOCATOR_ONLY_NOT_PROJECT_STATE" in set(project_migration.get("hard_invariants") or [])
        ),
        "project_repository_migration_does_not_fake_remote_or_project_state": all(
            row.get("remote_repo_created") is None
            and row.get("remote_repo_pushed") is None
            and row.get("remote_repository_verification") == "UNVERIFIED"
            and row.get("remote_history_verification") == "UNVERIFIED"
            and "VERIFY_TARGET_REMOTE_EXISTENCE_AND_HISTORY" in set(row.get("next_actions") or [])
            and row.get("old_duplicate_retained") is True
            and (
                row.get("project_state_ref") is None
                or (
                    (row.get("project_state_evidence") or {}).get("owner_native_project_state_verified") is True
                    and isinstance(row.get("authority_ref"), str)
                    and bool(row.get("authority_ref"))
                )
            )
            for row in migration_projects
        ),
    }

    details = {
        "invalid_dispositions": invalid_dispositions,
        "missing_owner_refs": missing_owner_refs,
        "missing_predecessor_refs": missing_predecessor_refs,
        "missing_core_owner_refs": sorted(set(missing_core_owner_refs)),
        "connector_ceiling_violations": connector_ceiling_violations,
        "global_current_violations": global_current_violations,
        "misleading_current_roles": misleading_roles,
        "stale_available_surfaces": stale_available,
        "local_snapshot_state": local_snapshot.get("state"),
        "surface_reliability_stages": sorted(reliability_stages),
        "design_system_project_non_equivalences": sorted(project_non_equivalences),
        "project_workspace_authority_ceiling": project_workspace.get("authority_ceiling"),
        "source_ingestion_authority_ceiling": source_ingestion.get("authority_ceiling"),
        "source_ingestion_output_authority_hits": source_output_authority_hits,
        "bounded_product_action_guard_allow_probe": action_guard_allow_probe,
        "bounded_product_action_guard_hold_probe": action_guard_hold_probe,
        "derived_integrity_authority_ceiling": derived_integrity.get("authority_ceiling"),
        "source_transcription_authority_ceiling": source_transcription.get("authority_ceiling"),
        "host_runtime_authority_ceiling": host_runtime.get("authority_ceiling"),
        "surface_view_authority_ceiling": surface_view.get("authority_ceiling"),
        "project_repository_migration_status": project_migration.get("status"),
    }
    return {
        "status": "PASS" if all(checks.values()) else "FAIL",
        "checks": checks,
        "details": details,
        "does_not_prove": ["PROJECT_CURRENT", "DESIGN_QUALITY", "PROFESSIONAL_PASS", "PROMOTION"],
    }


def main() -> None:
    result = run_lint()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if result["status"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
