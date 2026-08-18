#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"

FILES = {
    "capability": RUNTIME / "OLEANDER_SKILL_CAPABILITY_CONTRACT_v0.1.json",
    "dag": RUNTIME / "OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1.json",
    "tool": RUNTIME / "OLEANDER_TOOL_ADAPTER_CONTRACT_v0.1.json",
    "artifact": RUNTIME / "OLEANDER_NATIVE_ARTIFACT_CONTRACT_v0.1.json",
    "regression": RUNTIME / "OLEANDER_EXECUTION_REGRESSION_CONTRACT_v0.1.json",
    "drift": RUNTIME / "OLEANDER_NOTION_GITHUB_DRIFT_CHECK_v0.1.json",
}

EXPECTED_IDS = {
    "capability": "OLEANDER_SKILL_CAPABILITY_CONTRACT",
    "dag": "OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT",
    "tool": "OLEANDER_TOOL_ADAPTER_CONTRACT",
    "artifact": "OLEANDER_NATIVE_ARTIFACT_CONTRACT",
    "regression": "OLEANDER_EXECUTION_REGRESSION_CONTRACT",
    "drift": "OLEANDER_NOTION_GITHUB_DRIFT_CHECK",
}

ALLOWED_STATUS = {"CANDIDATE_FOR_CURRENT", "ACTIVE_CURRENT"}


def fail(msg: str) -> None:
    raise SystemExit(f"execution-contract validation failed: {msg}")


def load(name: str) -> dict:
    path = FILES[name]
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"invalid JSON {path.name}: {exc}")
    if data.get("contract_id") != EXPECTED_IDS[name]:
        fail(f"{path.name} contract_id mismatch")
    if data.get("version") != "0.1":
        fail(f"{path.name} version must be 0.1")
    if data.get("status") not in ALLOWED_STATUS:
        fail(f"{path.name} status not allowed: {data.get('status')}")
    return data


def validate_capability(data: dict) -> None:
    required = set(data.get("required_fields", []))
    owners = data.get("owners", [])
    if len(owners) != 12:
        fail(f"capability owner declaration count must be 12, got {len(owners)}")
    ids = [o.get("skill_id") for o in owners]
    if len(ids) != len(set(ids)):
        fail("duplicate skill_id in capability declarations")
    for owner in owners:
        missing = sorted(required - set(owner))
        if missing:
            fail(f"{owner.get('skill_id')} missing capability fields {missing}")
        if owner.get("lifecycle_state") not in data.get("lifecycle_states", []):
            fail(f"{owner.get('skill_id')} invalid lifecycle state")
        if owner.get("routing_state") not in data.get("routing_states", []):
            fail(f"{owner.get('skill_id')} invalid routing state")


def validate_dag(data: dict) -> None:
    if not data.get("minimum_sufficient_owner_set"):
        fail("DAG must enforce minimum_sufficient_owner_set")
    if data.get("default_handoff_permission") != "READ_ONLY":
        fail("DAG default handoff permission must be READ_ONLY")
    roles = set(data.get("node_roles", []))
    for role in {"PRIMARY_OWNER", "SUPPORTING_OWNER", "READ_ONLY_CONSUMER", "VALIDATOR", "INDEPENDENT_REVIEWER"}:
        if role not in roles:
            fail(f"DAG missing node role {role}")


def validate_tool(data: dict) -> None:
    if "final_project_artifact" not in data.get("shared_tool_must_not_own", []):
        fail("Tool Adapter must forbid final_project_artifact ownership")
    current = data.get("current_adapters", [])
    image_ops = next((a for a in current if a.get("canonical_tool_id") == "T-VISUAL-IMAGE-OPS-001"), None)
    if not image_ops:
        fail("missing T-VISUAL-IMAGE-OPS-001 adapter")
    consumers = image_ops.get("consumers", [])
    if len(consumers) != 11 or len(set(consumers)) != 11:
        fail("Image Ops adapter must have exactly 11 unique current consumers")
    expected_paths = {
        "oleander-research": "oleander-skills/oleander-research/VISUAL_LAYER_BINDING.md",
        "oleander-data-viz": "oleander-skills/oleander-data-viz/VISUAL_LAYER_BINDING.md",
        "oleander-3d-pipeline": "oleander-skills/oleander-3d-pipeline/VISUAL_LAYER_BINDING.md",
        "oleander-story-and-board": "oleander-skills/oleander-story-and-board/VISUAL_LAYER_BINDING.md",
        "oleander-motion": "oleander-skills/oleander-motion/VISUAL_LAYER_BINDING.md",
        "oleander-delivery-qc": "oleander-skills/oleander-delivery-qc/VISUAL_LAYER_BINDING.md",
        "oleander-ui-visual-composition": "skills/oleander-ui-visual-composition/VISUAL_LAYER_BINDING.md",
        "oleander-ui-interaction": "skills/oleander-ui-interaction/VISUAL_LAYER_BINDING.md",
        "oleander-route-wayfinding-ui": "skills/oleander-route-wayfinding-ui/VISUAL_LAYER_BINDING.md",
        "oleander-game-ui": "skills/oleander-game-ui/VISUAL_LAYER_BINDING.md",
        "oleander-mobile-game-ui": "skills/oleander-mobile-game-ui/VISUAL_LAYER_BINDING.md",
    }
    for consumer in consumers:
        rel = expected_paths.get(consumer)
        if not rel or not (ROOT / rel).is_file():
            fail(f"missing Image Ops binding for {consumer}: {rel}")


def validate_artifact(data: dict) -> None:
    vocab = data.get("provenance_vocabulary", [])
    if len(vocab) != len(set(vocab)):
        fail("duplicate provenance vocabulary")
    for token in {"SOURCE_VISIBLE", "VISUAL_PROXY", "INFERRED_FROM_MARK", "UNREADABLE", "REFERENCE_DERIVED_GEOMETRY", "UNKNOWN", "FIELD_OPEN"}:
        if token not in vocab:
            fail(f"Native Artifact Contract missing provenance token {token}")
    if data.get("default_permission") != "READ_ONLY":
        fail("Native Artifact default permission must be READ_ONLY")


def validate_regression(data: dict) -> None:
    if data.get("layers") != ["STRUCTURAL", "SEMANTIC", "VISUAL_ROI", "RUNTIME"]:
        fail("Regression layers must be STRUCTURAL, SEMANTIC, VISUAL_ROI, RUNTIME in order")
    if data.get("design_review_boundary") != "regression_pass_does_not_equal_design_keep":
        fail("Regression must preserve Design Review boundary")


def validate_drift(data: dict) -> None:
    states = set(data.get("drift_states", []))
    for state in {"CURRENT", "STALE", "MISSING", "DIVERGED", "ORPHANED_IMPLEMENTATION", "NOT_REQUIRED", "UNKNOWN"}:
        if state not in states:
            fail(f"Drift Check missing state {state}")
    modes = data.get("modes", {})
    if "LIVE_CROSS_PLATFORM_CHECK" not in modes or "GITHUB_STATIC_CHECK" not in modes:
        fail("Drift Check must separate static and live modes")


def validate_readme() -> None:
    readme = (RUNTIME / "README.md").read_text(encoding="utf-8")
    for path in FILES.values():
        if path.with_suffix(".md").name not in readme:
            fail(f"runtime README missing contract pointer {path.with_suffix('.md').name}")


def main() -> None:
    data = {name: load(name) for name in FILES}
    validate_capability(data["capability"])
    validate_dag(data["dag"])
    validate_tool(data["tool"])
    validate_artifact(data["artifact"])
    validate_regression(data["regression"])
    validate_drift(data["drift"])
    validate_readme()
    print("execution-contract validation: PASS")


if __name__ == "__main__":
    main()
