#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GRAPH = ROOT / "00-governance" / "runtime" / "OLEANDER_ARCHITECTURE_CONTROL_GRAPH_v2.1.json"
EXPECTED_LAYERS = ["R-A", "R-B", "R-C", "R-D", "R-E", "R-F", "R-G", "R-H", "R-I", "R-J", "R-K"]
EXPECTED_PLANES = {"CONTROL_PLANE", "STATE_PLANE", "ACQUISITION_READER_PLANE", "EXECUTION_PLANE", "OBSERVABILITY_PLANE", "EVOLUTION_PLANE"}
EXPECTED_MATURITY = {
    "M0_DECLARED",
    "M1_DEFINED",
    "M2_FORMALIZED",
    "M3_MACHINE_BOUND",
    "M4_PROJECT_EXERCISED",
    "M5_INDEPENDENTLY_READBACK",
}
REQUIRED_OBSERVABILITY = {
    "project_or_scope_id",
    "current_task_id",
    "current_decision_object",
    "active_runtime_layer",
    "active_owner",
    "authority_fingerprint",
    "current_state",
    "stale_or_reopen_refs",
    "open_blockers",
    "last_verified_artifact_ref",
    "last_readback_ref",
    "current_receipt_refs",
    "dependency_health",
    "next_allowed_action",
    "observed_at",
}
REQUIRED_MACHINE_DENIES = {
    "AWARD_DESIGN_KEEP",
    "AWARD_DQ3_DQ5",
    "PROMOTE_CURRENT_AUTHORITY",
    "GRANT_STATUTORY_APPROVAL",
}
REQUIRED_RECOVERY_STEPS = {
    "DETECT",
    "IDENTIFY_OWNER_AND_BLAST_RADIUS",
    "PRESERVE_LAST_VERIFIED_STATE",
    "ACTUAL_READBACK",
    "RERUN_AFFECTED_REVIEWS",
}
REQUIRED_COMPAT_CLASSES = {
    "DOC_CLARIFICATION",
    "BACKWARD_COMPATIBLE_EXTENSION",
    "SEMANTIC_OWNER_CHANGE",
    "STATE_CONTRACT_CHANGE",
    "SCHEMA_BREAKING_CHANGE",
    "PROFESSIONAL_PROCESS_REVISION",
    "AUTHORITY_REPLACEMENT",
}


def fail(message: str) -> None:
    raise SystemExit(f"ARCHITECTURE CONTROL VALIDATION: FAIL: {message}")


def load_graph() -> dict:
    try:
        return json.loads(GRAPH.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"cannot load {GRAPH.relative_to(ROOT)}: {exc}")


def check_ref(ref: str) -> None:
    path = ROOT / ref
    if not path.exists():
        fail(f"referenced local carrier does not exist: {ref}")


def validate_dag(layers_by_id: dict[str, dict]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            fail(f"primary dependency cycle detected at {node}; feedback must use feedback_edges")
        if node in visited:
            return
        visiting.add(node)
        for dep in layers_by_id[node].get("dependencies", []):
            visit(dep)
        visiting.remove(node)
        visited.add(node)

    for layer_id in EXPECTED_LAYERS:
        visit(layer_id)


def main() -> None:
    graph = load_graph()

    if graph.get("schema") != "oleander.architecture-control-graph.v2.1":
        fail("unexpected schema id")
    if graph.get("logical_object_id") != "OLEANDER-CURRENT-ARCHITECTURE-CONTROL":
        fail("logical object identity drift")
    if graph.get("version") != "2.1":
        fail("control graph must be v2.1")
    if graph.get("system_architecture_count") != 1:
        fail("OLEANDER must declare exactly one Current system architecture")
    if graph.get("master_runtime_count") != 1:
        fail("OLEANDER must declare exactly one Master Runtime")

    canonical = graph.get("canonical_markdown_ref")
    if canonical != "00-governance/runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md":
        fail("canonical markdown pointer drift")
    check_ref(canonical)

    master = graph.get("master_runtime", {})
    if master.get("ref") != "00-governance/complex-project-master-runtime-v1.0.md":
        fail("Master Runtime pointer drift")
    check_ref(master["ref"])

    order = graph.get("runtime_layer_order")
    if order != EXPECTED_LAYERS:
        fail(f"runtime layer order must be exactly {EXPECTED_LAYERS}")

    vocabulary = set(graph.get("maturity_vocabulary", []))
    if vocabulary != EXPECTED_MATURITY:
        fail("architecture-module maturity vocabulary drift")

    obs = set(graph.get("observability_required_fields", []))
    if obs != REQUIRED_OBSERVABILITY:
        fail("minimum observability field contract drift")

    planes = graph.get("planes", [])
    plane_ids = {p.get("id") for p in planes}
    if plane_ids != EXPECTED_PLANES:
        fail("cross-cutting plane set must be CONTROL/STATE/ACQUISITION_READER/EXECUTION/OBSERVABILITY/EVOLUTION")
    for plane in planes:
        if not plane.get("owns") or not plane.get("refs") or not plane.get("does_not_prove"):
            fail(f"incomplete plane contract: {plane.get('id')}")
        for ref in plane["refs"]:
            check_ref(ref)

    layers = graph.get("layers", [])
    ids = [layer.get("id") for layer in layers]
    if ids != EXPECTED_LAYERS:
        fail("layers array must contain each R-A..R-K exactly once in canonical order")
    if len(set(ids)) != 11:
        fail("duplicate runtime layer id")
    layers_by_id = {layer["id"]: layer for layer in layers}

    for layer in layers:
        layer_id = layer["id"]
        if not layer.get("name"):
            fail(f"{layer_id} missing name")
        if not layer.get("owner_refs"):
            fail(f"{layer_id} missing canonical owner_refs")
        for ref in layer["owner_refs"]:
            check_ref(ref)
        if layer.get("maturity") not in EXPECTED_MATURITY:
            fail(f"{layer_id} invalid maturity")
        if not layer.get("state_objects"):
            fail(f"{layer_id} missing state_objects")
        if not layer.get("control_actions"):
            fail(f"{layer_id} missing control_actions")
        if not layer.get("reopen_rule"):
            fail(f"{layer_id} missing reopen_rule")
        if not layer.get("observability"):
            fail(f"{layer_id} missing observability projection")
        if not layer.get("machine_cannot_award"):
            fail(f"{layer_id} missing machine authority boundary")

        for key in ("dependencies", "conditional_dependencies", "reopen_targets", "conditional_reopen_targets", "feedback_targets"):
            for target in layer.get(key, []):
                if target not in layers_by_id:
                    fail(f"{layer_id} {key} references unknown layer {target}")
                if key in {"dependencies", "conditional_dependencies"} and target == layer_id:
                    fail(f"{layer_id} may not depend on itself")

    validate_dag(layers_by_id)

    feedback = graph.get("feedback_edges", [])
    if not feedback:
        fail("bounded feedback edge must be explicit")
    for edge in feedback:
        if edge.get("from") not in layers_by_id or edge.get("to") not in layers_by_id:
            fail("feedback edge references unknown layer")
        if edge.get("automatic_promotion") is not False:
            fail("G9 feedback may not auto-promote knowledge")

    professional = graph.get("professional_domain_process_state", [])
    by_domain = {row.get("domain"): row for row in professional}
    architecture = by_domain.get("Architecture")
    if not architecture:
        fail("Architecture process state missing")
    if architecture.get("state") != "FORMALIZED_PROJECT_EXERCISED":
        fail("Architecture reference-process state drift")
    check_ref(architecture.get("current_process_ref"))
    check_ref(architecture.get("machine_schema_ref"))
    if architecture.get("project_exercised_claim") is not True:
        fail("Architecture project-exercised reference claim drift")
    for domain in ("Structural Engineering", "Building Services / MEP"):
        row = by_domain.get(domain)
        if not row or row.get("state") != "FORMALIZED_MACHINE_BOUND":
            fail(f"{domain} must resolve as FORMALIZED_MACHINE_BOUND on the current main baseline")
        if row.get("project_exercised_claim") is not False:
            fail(f"{domain} may not infer project-exercised maturity from Current schema/document status")
        check_ref(row.get("current_process_ref"))
        check_ref(row.get("machine_schema_ref"))

    for domain, row in by_domain.items():
        if domain in {"Architecture", "Structural Engineering", "Building Services / MEP"}:
            continue
        if row.get("state") != "CONTRACT_ENVELOPE_AVAILABLE_PROCESS_OPEN":
            fail(f"{domain} must not be auto-promoted beyond current evidence")
        if row.get("current_process_ref") is not None:
            fail(f"{domain} declares a process ref while state remains PROCESS_OPEN")

    rights = graph.get("decision_rights", {})
    machine_denies = set(rights.get("machine_may_not", []))
    if not REQUIRED_MACHINE_DENIES.issubset(machine_denies):
        fail("machine/human authority firewall incomplete")
    if "HUMAN_PROMOTION_DECISION" not in set(rights.get("project_authority", [])):
        fail("human promotion authority missing")
    if "STATUTORY_OR_LICENSED_APPROVAL_WHERE_APPLICABLE" not in set(rights.get("external_authority", [])):
        fail("external statutory authority boundary missing")

    control_domains = graph.get("control_domains", {})
    file_domain = control_domains.get("FILE_ARTIFACT_MANAGEMENT", {})
    reader_domain = control_domains.get("AI_FILE_AND_READER", {})
    if file_domain.get("artifact_invariant") != "ONE_LOGICAL_ARTIFACT_ONE_CURRENT_REVISION_N_REPRESENTATIONS":
        fail("file/artifact logical identity invariant missing")
    if set(file_domain.get("representation_roles", [])) != {"SOURCE", "NATIVE", "CANONICAL", "PREVIEW", "PACKAGE"}:
        fail("file/artifact representation-role set drift")
    if file_domain.get("location_integrity_required") is not True or file_domain.get("blind_age_delete_forbidden") is not True:
        fail("file location/deletion safety boundary incomplete")
    for ref in file_domain.get("owner_refs", []):
        check_ref(ref)

    expected_read_ops = {"LIST", "SEARCH", "FIND", "READ", "MATERIALIZE", "PARSE_RENDER", "READBACK"}
    if set(reader_domain.get("read_operations", [])) != expected_read_ops:
        fail("AI file/Reader read-depth contract drift")
    if reader_domain.get("minimum_sufficient_access") is not True:
        fail("AI file handling must use minimum sufficient access")
    if reader_domain.get("canonical_derivative_separation_required") is not True:
        fail("Reader canonical/derivative separation must remain required")
    if reader_domain.get("partial_or_stale_readback_fails_closed") is not True:
        fail("partial/stale Reader readback must fail closed")
    required_firewall = {"CAN_READ_NOT_CAN_EDIT", "CAN_MATERIALIZE_NOT_CAN_OVERWRITE", "CAN_DERIVE_NOT_CAN_PROMOTE", "DERIVATIVE_INDEX_NOT_CANONICAL_AUTHORITY"}
    if not required_firewall.issubset(set(reader_domain.get("mutation_firewall", []))):
        fail("AI file/Reader mutation firewall incomplete")
    for ref in reader_domain.get("owner_refs", []):
        check_ref(ref)

    evolution = graph.get("evolution", {})
    evolution_contract = evolution.get("contract_ref")
    if evolution_contract != "00-governance/runtime/OLEANDER_EVOLUTION_CANDIDATE_CONTRACT_v1.0.json":
        fail("controlled evolution candidate contract pointer drift")
    check_ref(evolution_contract)
    if evolution.get("mode") != "CONTROLLED_EVOLUTION_NO_DIRECT_SELF_PROMOTION":
        fail("evolution mode must forbid direct self-promotion")
    if evolution.get("candidate_may_modify_live_baseline_during_eval") is not False:
        fail("evolution candidate may not modify its live evaluation baseline")
    if evolution.get("human_promotion_required") is not True:
        fail("evolution adoption requires human promotion")
    if evolution.get("rollback_required") is not True or evolution.get("migration_provenance_required") is not True:
        fail("evolution requires rollback and migration provenance")
    if evolution.get("one_success_may_universalize_rule") is not False:
        fail("one project success may not universalize an OLEANDER rule")
    required_evolution_steps = {"FREEZE_CURRENT_BASELINE", "GENERATE_ISOLATED_VARIANTS", "RUN_TARGET_SPECIFIC_EVALS", "RUN_CONSTRAINT_AND_REGRESSION_GATES", "INDEPENDENT_REVIEW", "HUMAN_PROMOTION_DECISION", "ACTUAL_READBACK", "POST_ADOPTION_MONITORING"}
    if not required_evolution_steps.issubset(set(evolution.get("loop", []))):
        fail("controlled evolution loop incomplete")
    protected = set(evolution.get("protected_targets", []))
    for required in {"CURRENT_AUTHORITY_IDENTITY", "ACTIVE_USER_CONSTRAINTS", "HUMAN_PROMOTION_RIGHT", "STATUTORY_LICENSED_AUTHORITY"}:
        if required not in protected:
            fail(f"evolution protected target missing: {required}")

    recovery = graph.get("recovery", {})
    if not REQUIRED_RECOVERY_STEPS.issubset(set(recovery.get("sequence", []))):
        fail("recovery sequence does not preserve bounded verified state/readback")
    if len(recovery.get("failure_classes", {})) < 8:
        fail("failure/recovery coverage too thin")

    compatibility = graph.get("compatibility", {})
    if set(compatibility.get("change_classes", [])) != REQUIRED_COMPAT_CLASSES:
        fail("architecture compatibility change classes drift")
    if "OLD_RECEIPT_NOT_SILENTLY_REINTERPRETED" not in set(compatibility.get("invariants", [])):
        fail("receipt compatibility boundary missing")

    invariants = set(graph.get("hard_invariants", []))
    for invariant in {
        "ONE_SYSTEM_ARCHITECTURE",
        "ONE_MASTER_RUNTIME",
        "EXACTLY_11_RUNTIME_LAYERS",
        "NO_MACHINE_DESIGN_PROMOTION",
        "PRESERVE_VALID_STATE_DURING_RECOVERY",
        "READ_SURFACE_IS_NOT_AUTHORITY",
        "ONE_LOGICAL_ARTIFACT_ONE_CURRENT_REVISION_N_REPRESENTATIONS",
        "EVOLUTION_CANDIDATE_NO_SELF_PROMOTION",
        "EVOLUTION_REQUIRES_FROZEN_BASELINE_EVAL_REVIEW_HUMAN_PROMOTION",
        "EVOLUTION_REQUIRES_ROLLBACK_AND_PROVENANCE",
    }:
        if invariant not in invariants:
            fail(f"missing hard invariant {invariant}")

    print("ARCHITECTURE CONTROL VALIDATION: PASS")
    print("system_architecture_count=1")
    print("master_runtime_count=1")
    print("runtime_layers=11")
    print("professional_reference_process=Architecture")
    print("control_graph_version=2.1")
    print("operational_planes=6")
    print("file_artifact_control=PASS")
    print("knowledge_reader_control=PASS")
    print("controlled_evolution=PASS")


if __name__ == "__main__":
    main()