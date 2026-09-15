#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / "00-governance" / "runtime"
DEFAULT_FIXTURES = RUNTIME / "OLEANDER_TYPED_READER_FIXTURES_v0.1.json"

QUERY_TO_PLANE = {
    "KNOWLEDGE_QUERY": "KNOWLEDGE",
    "PROJECT_QUERY": "PROJECT",
    "RUNTIME_CONTROL_QUERY": "RUNTIME_CONTROL",
    "PRESENTATION_QUERY": None,
    "HISTORY_QUERY": None,
}

STATE_FIELDS = [
    "retrieval_space",
    "governance_state",
    "authority_state",
    "design_review_state",
    "content_state",
    "research_state",
    "professional_state",
    "bilingual_state",
    "independent_review_state",
    "freshness_state",
    "review_evidence_class",
    "allowed_use",
]


def die(msg: str) -> None:
    raise SystemExit(f"typed-reader failed: {msg}")


def load(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        die(f"cannot read {path}: {exc}")


def by_id(snapshot: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(o["id"]): o for o in snapshot.get("objects", []) if o.get("id")}


def select_object(snapshot: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    objects = snapshot.get("objects", [])
    expected_plane = QUERY_TO_PLANE.get(query.get("plane"))

    candidates = objects
    if expected_plane:
        candidates = [o for o in candidates if o.get("plane") == expected_plane]

    object_id = query.get("object_id")
    if object_id:
        matches = [o for o in candidates if o.get("id") == object_id]
    else:
        semantic_key = query.get("semantic_key")
        matches = [o for o in candidates if o.get("semantic_key") == semantic_key]

    if not matches:
        die("no eligible object for query")
    if len(matches) > 1:
        current = [o for o in matches if o.get("is_current")]
        if len(current) == 1:
            return current[0]
        die("ambiguous query: multiple eligible objects")
    return matches[0]


def independent_states(obj: dict[str, Any]) -> dict[str, Any]:
    return {k: obj[k] for k in STATE_FIELDS if k in obj}


def related_support(snapshot: dict[str, Any], target_id: str) -> list[dict[str, Any]]:
    objects = by_id(snapshot)
    out: list[dict[str, Any]] = []
    for rel in snapshot.get("relations", []):
        if rel.get("to") != target_id:
            continue
        if rel.get("type") not in {"SUPPORTS_BOUNDED_SCOPE", "SUPPORTS_CLAIM", "EVIDENCED_BY"}:
            continue
        source = objects.get(str(rel.get("from")))
        if not source:
            continue
        out.append({
            "relation": rel.get("type"),
            "id": source.get("id"),
            "title": source.get("title"),
            "semantic_class": source.get("semantic_class"),
            "scope_kind": source.get("scope_kind"),
            "assurance_result": source.get("assurance_result"),
            "target_results": source.get("target_results"),
            "does_not_establish": source.get("does_not_establish", []),
            "states": independent_states(source),
        })
    return out


def warnings_for(obj: dict[str, Any], support: list[dict[str, Any]]) -> list[str]:
    warnings: list[str] = []
    if obj.get("retrieval_space") == "CURRENT" and obj.get("professional_state") in {
        "NOT_PROVEN_PROFESSIONAL_PASS", "OPEN", "REVISE", "HOLD"
    }:
        warnings.append("CURRENT_RETRIEVAL_DOES_NOT_IMPLY_PROFESSIONAL_PASS")
    if obj.get("design_review_state") in {"REVISE", "HOLD", "OPEN"}:
        if any(s.get("assurance_result") for s in support):
            warnings.append("BOUNDED_SUPPORT_RESULT_COEXISTS_WITH_UNRESOLVED_PARENT_DESIGN_STATE")
    if obj.get("target_results") and len(set(obj["target_results"].values())) > 1:
        warnings.append("MIXED_TARGET_RESULTS_PRESERVED")
    return warnings


def render(snapshot: dict[str, Any], query: dict[str, Any]) -> dict[str, Any]:
    obj = select_object(snapshot, query)
    support = related_support(snapshot, str(obj.get("id"))) if query.get("include_related_support") else []

    return {
        "schema": "OLEANDER_TYPED_READER_PROJECTION_v0.1",
        "snapshot_id": snapshot.get("snapshot_id"),
        "as_of": snapshot.get("as_of"),
        "query": query,
        "identity": {
            "id": obj.get("id"),
            "title": obj.get("title"),
            "plane": obj.get("plane"),
            "semantic_class": obj.get("semantic_class"),
            "semantic_key": obj.get("semantic_key"),
            "scope_key": obj.get("scope_key"),
            "is_current": obj.get("is_current"),
        },
        "states": independent_states(obj),
        "target_results": obj.get("target_results"),
        "related_support": support,
        "warnings": warnings_for(obj, support),
        "single_aggregate_pass_badge": False,
        "reader_boundary": "PROJECTION_ONLY_DOES_NOT_PROMOTE_OR_RECLASSIFY_SOURCE_STATE",
    }


def load_fixture(path: Path, fixture_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    data = load(path)
    for fixture in data.get("fixtures", []):
        if fixture.get("fixture_id") == fixture_id:
            return fixture["snapshot"], fixture["query"]
    die(f"fixture not found: {fixture_id}")


def main() -> None:
    ap = argparse.ArgumentParser(description="OLEANDER plane-aware typed Reader prototype")
    ap.add_argument("--snapshot", type=Path)
    ap.add_argument("--query", help="JSON query string")
    ap.add_argument("--fixture-file", type=Path, default=DEFAULT_FIXTURES)
    ap.add_argument("--fixture-id")
    ap.add_argument("--compact", action="store_true")
    args = ap.parse_args()

    if args.fixture_id:
        snapshot, query = load_fixture(args.fixture_file, args.fixture_id)
    elif args.snapshot and args.query:
        snapshot = load(args.snapshot)
        try:
            query = json.loads(args.query)
        except Exception as exc:
            die(f"invalid query JSON: {exc}")
    else:
        die("provide --fixture-id or --snapshot plus --query")

    projection = render(snapshot, query)
    print(json.dumps(projection, ensure_ascii=False, indent=None if args.compact else 2, sort_keys=True))


if __name__ == "__main__":
    main()
