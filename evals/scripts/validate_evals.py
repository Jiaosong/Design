#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "evals" / "golden" / "skills.jsonl"
RETRIEVAL = ROOT / "evals" / "retrieval" / "golden_queries.jsonl"
P0 = ROOT / "90-shared" / "OLEANDER_AI_Governance_P0_v0.1.md"

REQUIRED_SKILLS = {
    "oleander-research",
    "oleander-data-viz",
    "oleander-3d-pipeline",
    "oleander-story-and-board",
    "oleander-delivery-qc",
}


def load_jsonl(path: Path):
    if not path.exists():
        raise AssertionError(f"missing file: {path.relative_to(ROOT)}")
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSON at {path.relative_to(ROOT)}:{lineno}: {exc}") from exc
    return rows


def require_fields(row, fields, context):
    missing = [f for f in fields if f not in row or row[f] in (None, "", [])]
    if missing:
        raise AssertionError(f"{context}: missing required fields: {', '.join(missing)}")


def validate_skill_cases(rows):
    ids = set()
    counts = Counter()
    required = ["case_id", "skill", "task", "required_outputs", "blockers", "pass_rule"]
    for row in rows:
        require_fields(row, required, row.get("case_id", "skill-case"))
        if row["case_id"] in ids:
            raise AssertionError(f"duplicate case_id: {row['case_id']}")
        ids.add(row["case_id"])
        counts[row["skill"]] += 1
        if row["skill"] not in REQUIRED_SKILLS:
            raise AssertionError(f"unknown skill in golden set: {row['skill']}")
        if not isinstance(row["required_outputs"], list) or len(row["required_outputs"]) < 3:
            raise AssertionError(f"{row['case_id']}: requires at least 3 required_outputs")
        if not isinstance(row["blockers"], list) or not row["blockers"]:
            raise AssertionError(f"{row['case_id']}: at least one blocker is required")
    missing_skills = REQUIRED_SKILLS - set(counts)
    if missing_skills:
        raise AssertionError(f"skills missing golden cases: {sorted(missing_skills)}")
    undercovered = {skill: n for skill, n in counts.items() if n < 2}
    if undercovered:
        raise AssertionError(f"each skill needs >=2 golden cases: {undercovered}")
    return counts


def validate_retrieval_cases(rows):
    ids = set()
    required = [
        "query_id",
        "query",
        "expected_canonical_sources",
        "forbidden_legacy_sources",
        "required_status",
        "required_truth_state",
        "required_warning",
    ]
    for row in rows:
        require_fields(row, required, row.get("query_id", "retrieval-case"))
        if row["query_id"] in ids:
            raise AssertionError(f"duplicate query_id: {row['query_id']}")
        ids.add(row["query_id"])
        if not isinstance(row["expected_canonical_sources"], list) or not row["expected_canonical_sources"]:
            raise AssertionError(f"{row['query_id']}: expected_canonical_sources must be non-empty list")
        if not isinstance(row["forbidden_legacy_sources"], list):
            raise AssertionError(f"{row['query_id']}: forbidden_legacy_sources must be a list")
    if len(rows) < 10:
        raise AssertionError("retrieval golden set requires at least 10 cases")


def validate_p0_protocol():
    if not P0.exists():
        raise AssertionError("missing P0 governance protocol")
    text = P0.read_text(encoding="utf-8")
    required_terms = [
        "AI Necessity Gate",
        "AI Eval Harness",
        "Retrieval & Context QA",
        "AI Change & Regression Gate",
        "NO-AI",
        "HOLD",
        "PROMOTE",
        "ROLLBACK",
    ]
    missing = [term for term in required_terms if term not in text]
    if missing:
        raise AssertionError(f"P0 protocol missing governance terms: {missing}")


def main():
    try:
        skill_rows = load_jsonl(SKILLS)
        retrieval_rows = load_jsonl(RETRIEVAL)
        counts = validate_skill_cases(skill_rows)
        validate_retrieval_cases(retrieval_rows)
        validate_p0_protocol()
    except AssertionError as exc:
        print(f"AI GOVERNANCE EVAL CORPUS: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("AI GOVERNANCE EVAL CORPUS: PASS")
    print(f"skill cases: {len(skill_rows)} | retrieval cases: {len(retrieval_rows)}")
    for skill in sorted(counts):
        print(f"- {skill}: {counts[skill]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
