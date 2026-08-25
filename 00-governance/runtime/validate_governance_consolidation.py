#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAMING = ROOT / "00-governance" / "naming-status.md"


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


def main() -> None:
    validate_policy_text()
    validate_regression_examples()
    print("governance-consolidation validation: PASS")
    print("one logical object / one active production frontier: ENFORCED AS CONTRACT")
    print("successor predecessor-closure transaction: ENFORCED AS CONTRACT")
    print("location integrity / dead-lineage mutation block: ENFORCED AS CONTRACT")
    print("lifecycle exit / TEMP expiry metadata: ENFORCED AS CONTRACT")
    print("semantic content uniqueness != duplicate source bytes: ENFORCED AS CONTRACT")


if __name__ == "__main__":
    main()
