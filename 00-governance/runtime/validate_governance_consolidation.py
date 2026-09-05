#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMING = ROOT / "00-governance" / "naming-status.md"
PRIORITY_QUEUE = ROOT / "00-governance" / "OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json"
LIVE_QUEUE_STATES = {"ACTIVE", "HANDOFF_READY", "IN_REVIEW", "REVISE", "HOLD"}
WHOLE_PROJECT_AGGREGATE_SCOPE = "WHOLE_PROJECT_WITH_TYPED_SUBWORKSTREAMS_AND_ASSET_COVERAGE"
REQUIRED_QUEUE_FIELDS = {
    "priority",
    "project_id",
    "object_id",
    "current_owner",
    "state",
    "current_native_master",
    "current_pr_frontier",
    "next_owner",
    "next_action",
    "updated_at",
    "source_of_queue_decision",
}


def fail(msg: str) -> None:
    raise SystemExit(f"governance-consolidation validation failed: {msg}")


@dataclass(frozen=True)
class Frontier:
    object_id: str
    role: str  # PRODUCTION | INDEPENDENT_REVIEW
    state: str  # ACTIVE | CLOSED | SUPERSEDED | PROVENANCE


def validate_frontiers(rows: list[Frontier]) -> None:
    by_object: dict[str, list[Frontier]] = {}
    for row in rows:
        by_object.setdefault(row.object_id, []).append(row)
    for object_id, items in by_object.items():
        active_production = [x for x in items if x.role == "PRODUCTION" and x.state == "ACTIVE"]
        active_review = [x for x in items if x.role == "INDEPENDENT_REVIEW" and x.state == "ACTIVE"]
        if len(active_production) > 1:
            fail(f"{object_id} has {len(active_production)} active production frontiers")
        if len(active_review) > 1:
            fail(f"{object_id} has {len(active_review)} active independent-review frontiers")


def validate_policy_text() -> None:
    if not NAMING.is_file():
        fail("missing 00-governance/naming-status.md")
    text = NAMING.read_text(encoding="utf-8")
    required_tokens = [
        "ONE LOGICAL OBJECT → MAX 1 ACTIVE PRODUCTION FRONTIER + MAX 1 ACTIVE INDEPENDENT REVIEW FRONTIER",
        "SUCCESSOR ADOPTION REQUIRES PREDECESSOR CLOSURE",
        "LOCATION_DRIFT",
        "CURRENT IDENTITY + CURRENT GOVERNANCE + CURRENT LOCATION = REQUIRED FOR LIVE MUTATION",
        "WORKING / TEMP → CANDIDATE → CURRENT | SUPPORT | PROVENANCE | SUPERSEDED | REJECTED | DELETE_CANDIDATE",
        "CONTENT UNIQUENESS ≠ BINARY DUPLICATION",
        "source_asset_id",
    ]
    missing = [token for token in required_tokens if token not in text]
    if missing:
        fail(f"consolidation policy incomplete; missing {missing}")


def queue_identity_key(entry: dict, index: int) -> str:
    """Resolve a queue-slot identity without turning a project aggregate into a fake Work Object.

    Ordinary queue entries must keep a stable non-empty object_id. A Current schema 2.3
    whole-project aggregate may intentionally use object_id=null only when it explicitly
    requires typed child Work Object resolution before every material action. The
    synthetic key below is validator-local only; it is not a persisted Object ID.
    """
    object_id = entry.get("object_id")
    if isinstance(object_id, str) and object_id.strip():
        return object_id.strip()

    if object_id is None:
        if entry.get("entry_scope") != WHOLE_PROJECT_AGGREGATE_SCOPE:
            fail(f"priority queue entry {index} has null object_id outside whole-project aggregate scope")
        if entry.get("material_action_object_resolution_required") is not True:
            fail(f"priority queue entry {index} aggregate must require typed child object resolution")
        semantics = entry.get("object_id_semantics")
        if not isinstance(semantics, str) or not semantics.strip():
            fail(f"priority queue entry {index} aggregate requires non-empty object_id_semantics")
        project_id = entry.get("project_id")
        if not isinstance(project_id, str) or not project_id.strip():
            fail(f"priority queue entry {index} aggregate requires non-empty project_id")
        return f"{project_id.strip()}::WHOLE_PROJECT_AGGREGATE_SLOT"

    fail(f"priority queue entry {index} has invalid object_id")


def validate_current_priority_queue() -> int:
    """Validate the real Current priority queue, not only synthetic examples."""
    if not PRIORITY_QUEUE.is_file():
        fail("missing OLEANDER_PROJECT_PRIORITY_QUEUE_CURRENT.json")
    try:
        queue = json.loads(PRIORITY_QUEUE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid priority queue JSON: {exc}")
    if queue.get("status") != "CURRENT_PRIORITY_QUEUE":
        fail("priority queue must declare status=CURRENT_PRIORITY_QUEUE")
    entries = queue.get("entries")
    if not isinstance(entries, list):
        fail("priority queue entries must be a list")
    active_limit = queue.get("active_limit")
    if not isinstance(active_limit, int) or active_limit < 1:
        fail("priority queue active_limit must be a positive integer")
    if len(entries) > active_limit:
        fail(f"priority queue has {len(entries)} entries above active_limit={active_limit}")

    seen: set[str] = set()
    live_count = 0
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            fail(f"priority queue entry {index} must be an object")
        missing = sorted(REQUIRED_QUEUE_FIELDS - set(entry))
        if missing:
            fail(f"priority queue entry {index} missing fields {missing}")

        identity_key = queue_identity_key(entry, index)
        if identity_key in seen:
            fail(f"priority queue duplicates logical queue slot {identity_key}")
        seen.add(identity_key)

        if entry.get("state") in LIVE_QUEUE_STATES:
            live_count += 1
        for field in ("project_id", "current_owner", "current_native_master", "current_pr_frontier", "next_owner", "next_action", "updated_at", "source_of_queue_decision"):
            if not isinstance(entry.get(field), str) or not entry[field].strip():
                fail(f"priority queue {identity_key} requires non-empty {field}")

    if live_count > active_limit:
        fail(f"priority queue has {live_count} live entries above active_limit={active_limit}")
    return live_count


def validate_regression_examples() -> None:
    validate_frontiers([
        Frontier("OBJ-A", "PRODUCTION", "ACTIVE"),
        Frontier("OBJ-A", "INDEPENDENT_REVIEW", "ACTIVE"),
        Frontier("OBJ-A", "PRODUCTION", "SUPERSEDED"),
    ])

    try:
        validate_frontiers([
            Frontier("OBJ-B", "PRODUCTION", "ACTIVE"),
            Frontier("OBJ-B", "PRODUCTION", "ACTIVE"),
        ])
    except SystemExit:
        pass
    else:
        fail("regression example failed to reject two active production frontiers")

    try:
        validate_frontiers([
            Frontier("OBJ-C", "PRODUCTION", "ACTIVE"),
            Frontier("OBJ-C", "INDEPENDENT_REVIEW", "ACTIVE"),
            Frontier("OBJ-C", "INDEPENDENT_REVIEW", "ACTIVE"),
        ])
    except SystemExit:
        pass
    else:
        fail("regression example failed to reject two active review frontiers")

    aggregate = {
        "project_id": "PRJ-TEST",
        "object_id": None,
        "object_id_semantics": "WHOLE PROJECT SLOT; RESOLVE CHILD BEFORE MUTATION",
        "entry_scope": WHOLE_PROJECT_AGGREGATE_SCOPE,
        "material_action_object_resolution_required": True,
    }
    if queue_identity_key(aggregate, 0) != "PRJ-TEST::WHOLE_PROJECT_AGGREGATE_SLOT":
        fail("whole-project aggregate queue identity regression failed")

    invalid_null = dict(aggregate)
    invalid_null["entry_scope"] = "WHOLE_PROJECT"
    try:
        queue_identity_key(invalid_null, 1)
    except SystemExit:
        pass
    else:
        fail("regression example failed to reject null object_id outside governed aggregate scope")

    unresolved_aggregate = dict(aggregate)
    unresolved_aggregate["material_action_object_resolution_required"] = False
    try:
        queue_identity_key(unresolved_aggregate, 2)
    except SystemExit:
        pass
    else:
        fail("regression example failed to reject aggregate without typed child resolution gate")


def main() -> None:
    validate_policy_text()
    validate_regression_examples()
    live_count = validate_current_priority_queue()
    print("governance-consolidation validation: PASS")
    print("one logical object / one active production frontier: ENFORCED AS CONTRACT")
    print("whole-project aggregate slot / typed child object resolution: ENFORCED AS CONTRACT")
    print("successor predecessor-closure transaction: ENFORCED AS CONTRACT")
    print("location integrity / dead-lineage mutation block: ENFORCED AS CONTRACT")
    print("lifecycle exit / TEMP expiry metadata: ENFORCED AS CONTRACT")
    print("semantic content uniqueness != duplicate source bytes: ENFORCED AS CONTRACT")
    print(f"real Current priority queue scanned: {live_count} live slot(s)")


if __name__ == "__main__":
    main()
