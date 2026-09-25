from __future__ import annotations

import json
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> None:
    migration = load_json("OLEANDER_HUMAN_AI_CODESIGN_MIGRATION_MAP_v0.1.json")
    control = load_json("OLEANDER_HUMAN_AI_CODESIGN_CONTROL_CARD_v0.1.json")
    evals = load_json("OLEANDER_HUMAN_AI_CODESIGN_EVALS_v0.1.json")
    plugin = load_json("OLEANDER_CODESIGN_PLUGIN_REFERENCE_v0.3.0_CANDIDATE.json")
    architecture = (ROOT / "OLEANDER_HUMAN_AI_CODESIGN_ARCHITECTURE_v0.1_CANDIDATE.md").read_text(encoding="utf-8")
    kernel = (ROOT / "OLEANDER_CODESIGN_SESSION_KERNEL_CONTRACT_v0.2.md").read_text(encoding="utf-8")
    kernel_spec = load_json("OLEANDER_CODESIGN_SESSION_KERNEL_SPEC_v0.2.json")
    kernel_schema = load_json("OLEANDER_CODESIGN_SESSION_CONTEXT_EPHEMERAL_v0.4.schema.json")
    kernel_validation = load_json("OLEANDER_CODESIGN_SESSION_KERNEL_VALIDATION_v0.2.json")
    local_bridge_readback = load_json("OLEANDER_CHAT_COS_LOCAL_EXECUTION_READBACK_v0.1.json")

    expected_layers = {f"R-{c}" for c in "ABCDEFGHIJK"}
    actual_layers = set(migration["runtime_layer_mapping"])
    assert actual_layers == expected_layers, (actual_layers, expected_layers)

    assert len(migration["views"]) == 3
    assert len(migration["design_arenas"]) == 6
    assert control["mode"] == "CANDIDATE"
    assert control["change_scope"]["kind"] == "RESTRUCTURE"
    assert control["sync_persistence_trigger"] == "NONE"
    assert len(evals["cases"]) >= 10
    assert plugin["role"] == "HUMAN_AI_CODESIGN_SESSION_KERNEL_REFERENCE_IMPLEMENTATION"
    assert plugin["plugin_version"] == "0.3.0"
    assert plugin["kernel_contract"] == "OLEANDER_CODESIGN_SESSION_KERNEL_CONTRACT_v0.2.md"
    assert plugin["local_execution_bridge"] == "codesign_chat_cos_bridge_v0_1.py"
    assert (ROOT / plugin["local_execution_bridge"]).exists()
    package_path = ROOT / plugin["package_filename"]
    assert package_path.exists(), package_path
    assert hashlib.sha256(package_path.read_bytes()).hexdigest() == plugin["package_sha256"]
    package_source = ROOT / plugin["package_source"]
    assert sum(1 for p in package_source.rglob("*") if p.is_file()) == plugin["package_file_count"]
    assert (package_source / "references/kernel-spec.json").read_bytes() == (ROOT / plugin["kernel_machine_spec"]).read_bytes()
    assert (package_source / "references/session-context.schema.json").read_bytes() == (ROOT / plugin["session_context_schema"]).read_bytes()
    assert "CURRENT_AUTHORITY" in plugin["consumes_not_owns"]
    assert "PROJECT_STATE" in plugin["consumes_not_owns"]
    assert "PLUGIN_PROJECT_STATE" in plugin["forbidden_parallel_structures"]
    assert kernel_spec["authority_position"] == "EPHEMERAL_INTERACTION_ORCHESTRATOR_ONLY"
    assert kernel_spec["execution_surface_model"]["default_conversation_surface"] == "CHAT"
    assert kernel_spec["execution_surface_model"]["route_projection_authority"] == "NONE"
    assert kernel_spec["local_capability_routes"]["BAIDU_STORAGE"] == {
        "execution_surface": "COS_LOCAL",
        "adapter_ref": "oleander-baidu-storage@oleander-personal",
        "adapter_version": "0.1.1",
        "transport": "stdio",
        "authority_effect": "NONE",
        "selected_use": "LOCAL_OLEANDER_VAULT_STORAGE_READ_WRITE_ADAPTER",
        "write_rule": "RECOMPUTE_EXISTING_MUTATION_GUARD;EXECUTION_INTENT_ALONE_IS_NOT_PERMISSION",
    }
    assert kernel_schema["properties"]["ephemeral_only"]["const"] is True
    assert kernel_schema["properties"]["execution_route"] == {"$ref": "#/$defs/executionRoute"}
    execution_route_schema = kernel_schema["$defs"]["executionRoute"]
    assert execution_route_schema["properties"]["authority_effect"]["const"] == "NONE"
    assert execution_route_schema["properties"]["changes_work_intent"]["const"] is False
    assert execution_route_schema["properties"]["changes_mutation_permission"]["const"] is False
    interaction_schema = kernel_schema["properties"]["interaction"]
    assert "human_actions" in interaction_schema["required"]
    assert "human_action" not in interaction_schema["properties"]
    human_action_schema = kernel_schema["$defs"]["humanAction"]
    assert {"binding_issue", "route_target"} <= set(human_action_schema["required"])
    assert human_action_schema["properties"]["route_target"]["enum"] == [
        "NONE",
        "SESSION_ITERATION",
        "EXISTING_PROJECT_DECISION_AUTHORITY",
        "EXISTING_DESIGN_REVIEW_AUTHORITY",
        "EXISTING_PROMOTION_AUTHORITY",
    ]
    assert kernel_spec["authority_routes"] == {
        "DESIGN_DECISION": "EXISTING_PROJECT_DECISION_AUTHORITY",
        "DESIGN_KEEP": "EXISTING_DESIGN_REVIEW_AUTHORITY",
        "PROMOTION_DECISION": "EXISTING_PROMOTION_AUTHORITY",
    }
    option_required = set(kernel_schema["$defs"]["option"]["required"])
    assert {"parent_refs", "preserved_invariants", "branch_status"} <= option_required
    option_readback_required = set(
        kernel_schema["$defs"]["option"]["properties"]["readback_bindings"]["items"]["required"]
    )
    assert {"artifact_content_sha256", "verified_invariant_refs"} <= option_readback_required
    round_trace_properties = kernel_schema["properties"]["round_trace"]["properties"]
    assert {"decision_rights_proof", "invariant_readback_bindings"} <= set(round_trace_properties)
    rights_proof = kernel_schema["$defs"]["decisionRightsProof"]
    assert rights_proof["properties"]["source"]["const"] == "OWNER_NATIVE_PROJECTION"
    assert rights_proof["properties"]["effect_scope"]["const"] == "ITERATION_STEER"
    assert rights_proof["properties"]["authority_ceiling"]["const"] == "ITERATION_STEER_ONLY"
    round_readback_required = set(round_trace_properties["readbacks"]["items"]["required"])
    assert {"artifact_content_sha256", "verified_invariant_refs"} <= round_readback_required
    assert "decision_rights_proof" in kernel_spec["second_round_required_fields"]
    assert "invariant_readback_bindings" in kernel_spec["second_round_required_fields"]
    round_verified_required = set(round_trace_properties.keys())
    schema_second_round_required = set(
        kernel_schema["properties"]["round_trace"]["allOf"][0]["then"]["required"]
    )
    assert set(kernel_spec["second_round_required_fields"]) <= schema_second_round_required <= round_verified_required
    guard_schema = kernel_schema["properties"]["guard"]
    guard_properties = guard_schema["properties"]
    assert {"decision_rights_status", "active_user_constraints", "owner_permission", "native_target_state"} <= set(guard_properties)
    project_guard_required = set(guard_schema["allOf"][0]["then"]["required"])
    assert {
        "logical_object_identity",
        "authority_revision",
        "source_revision",
        "expected_checkpoint_sequence",
        "observed_checkpoint_sequence",
        "carrier_readback_status",
        "resolver_provenance",
        "decision_rights_status",
        "active_user_constraints",
        "owner_permission",
        "native_target_state",
    } <= project_guard_required
    assert "PROJECT_STATE_OWNER" in kernel_spec["forbidden_authority_roles"]
    assert "PROMOTION_OWNER" in kernel_spec["forbidden_authority_roles"]
    assert kernel_validation["status"] == "PASS"
    assert kernel_validation["case_count"] >= 103
    assert local_bridge_readback["status"] == "PASS_CHAT_DEFAULT_TO_LOCAL_BAIDU_STORAGE"
    assert local_bridge_readback["source_surface"] == "CHAT"
    assert local_bridge_readback["execution_surface"] == "COS_LOCAL"
    assert local_bridge_readback["handoff_mode"] == "INLINE_COS_BRIDGE"
    assert local_bridge_readback["provider_readback"]["probe_status"] == "connected"
    assert local_bridge_readback["provider_readback"]["storage_root"] == "/OLEANDER_VAULT"
    assert local_bridge_readback["provider_readback"]["quota_errno"] == 0
    assert local_bridge_readback["write_path"]["negative_write_probe"]["execution_state"] == "NOT_EXECUTED"
    assert local_bridge_readback["write_path"]["negative_write_probe"]["guard_decision"] == "HOLD"
    assert local_bridge_readback["authority_effect"] == "NONE"
    assert "EXECUTION_SURFACE_ROUTING_PROJECTION" in plugin["owns"]
    assert "CONTINUITY_EXECUTION_INTENT" in plugin["consumes_not_owns"]
    assert "PLUGIN_LOCAL_EXECUTION_QUEUE" in plugin["forbidden_parallel_structures"]

    forbidden = set(migration["forbidden_new_parallel_structures"])
    required_forbidden = {
        "SECOND_CURRENT_AUTHORITY",
        "PLUGIN_PROJECT_STATE",
        "PLUGIN_CHECKPOINT_DATABASE",
        "PLUGIN_ARTIFACT_REGISTRY",
        "PLUGIN_PERSISTENCE_STORE",
        "AI_OWNED_PROMOTION_AUTHORITY",
    }
    assert required_forbidden <= forbidden

    for phrase in (
        "FRAME → EXPLORE → MAKE → LOOK → CRITIQUE → STEER → DEVELOP → repeat",
        "Governance Substrate",
        "Human steering contract",
        "CURRENT UNCHANGED",
    ):
        assert phrase in architecture, phrase

    for phrase in (
        "UNDERSTAND → EXPLORE → MAKE → LOOK → CRITIQUE → STEER → LEARN",
        "RESOLVE → RESUME → ROUTE → GUARD → HANDOFF → REPORT",
        "conversation context != project state",
        "Four-axis interaction model",
        "Second-round Human-feedback delta",
        "Domain adapter protocol",
        "Chat-default execution-surface routing",
    ):
        assert phrase in kernel, phrase

    print("PASS: Human-AI Co-Design vNext candidate structural invariants")


if __name__ == "__main__":
    main()
