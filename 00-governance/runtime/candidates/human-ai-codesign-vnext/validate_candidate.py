from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> None:
    migration = load_json("OLEANDER_HUMAN_AI_CODESIGN_MIGRATION_MAP_v0.1.json")
    control = load_json("OLEANDER_HUMAN_AI_CODESIGN_CONTROL_CARD_v0.1.json")
    evals = load_json("OLEANDER_HUMAN_AI_CODESIGN_EVALS_v0.1.json")
    plugin = load_json("OLEANDER_CODESIGN_PLUGIN_REFERENCE_v0.2.1_CANDIDATE.json")
    architecture = (ROOT / "OLEANDER_HUMAN_AI_CODESIGN_ARCHITECTURE_v0.1_CANDIDATE.md").read_text(encoding="utf-8")
    kernel = (ROOT / "OLEANDER_CODESIGN_SESSION_KERNEL_CONTRACT_v0.1.md").read_text(encoding="utf-8")

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
    assert "CURRENT_AUTHORITY" in plugin["consumes_not_owns"]
    assert "PROJECT_STATE" in plugin["consumes_not_owns"]

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
        "PLUGIN_REMOVAL_SURVIVAL",
    ):
        assert phrase in kernel, phrase

    print("PASS: Human-AI Co-Design vNext candidate structural invariants")


if __name__ == "__main__":
    main()
