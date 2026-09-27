#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from oleander_environment_resolver import build_current_execution_view
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
        "source_ingestion_never_sets_knowledge_current": "knowledge_current" in set(source_ingestion.get("forbidden_output_authority_fields") or []),
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
