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
    assert kernel_schema["properties"]["ephemeral_only"]["const"] is True
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
    assert "artifact_content_sha256" in option_readback_required
    round_trace_properties = kernel_schema["properties"]["round_trace"]["properties"]
    assert {"decision_rights_proof", "invariant_readback_bindings"} <= set(round_trace_properties)
    rights_proof = kernel_schema["$defs"]["decisionRightsProof"]
    assert rights_proof["properties"]["source"]["const"] == "OWNER_NATIVE_PROJECTION"
    assert rights_proof["properties"]["effect_scope"]["const"] == "ITERATION_STEER"
    assert rights_proof["properties"]["authority_ceiling"]["const"] == "ITERATION_STEER_ONLY"
    round_readback_required = set(round_trace_properties["readbacks"]["items"]["required"])
    assert "artifact_content_sha256" in round_readback_required
    assert "decision_rights_proof" in kernel_spec["second_round_required_fields"]
    assert "invariant_readback_bindings" in kernel_spec["second_round_required_fields"]
    assert "PROJECT_STATE_OWNER" in kernel_spec["forbidden_authority_roles"]
    assert "PROMOTION_OWNER" in kernel_spec["forbidden_authority_roles"]
    assert kernel_validation["status"] == "PASS"
    assert kernel_validation["case_count"] >= 50

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
    ):
        assert phrase in kernel, phrase

    print("PASS: Human-AI Co-Design vNext candidate structural invariants")


if __name__ == "__main__":
    main()
