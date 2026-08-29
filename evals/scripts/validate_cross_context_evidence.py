#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORPUS = ROOT / "evals" / "cross-context" / "batch4_20260829.jsonl"
EXPECTED_SKILLS = {
    "oleander-web-ui",
    "oleander-design-process",
    "oleander-visual-design",
    "oleander-data-viz",
    "oleander-story-and-board",
}
REQUIRED_FIELDS = {
    "case_id",
    "skill",
    "extension",
    "first_context",
    "second_context",
    "second_source",
    "practice_file",
    "retained_delta",
    "holds",
    "maturity",
    "forbidden_promotion",
}


def load_rows(path: Path):
    if not path.exists():
        raise AssertionError(f"missing cross-context corpus: {path.relative_to(ROOT)}")
    rows = []
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rows.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSON at {path.relative_to(ROOT)}:{lineno}: {exc}") from exc
    return rows


def main():
    rows = load_rows(CORPUS)
    if len(rows) != 5:
        raise AssertionError(f"batch4 cross-context corpus must contain exactly 5 rows, found {len(rows)}")

    ids = set()
    skills = set()
    for row in rows:
        missing = sorted(REQUIRED_FIELDS - row.keys())
        if missing:
            raise AssertionError(f"{row.get('case_id', 'unknown')}: missing fields {missing}")
        if any(row[field] in (None, "", []) for field in REQUIRED_FIELDS):
            raise AssertionError(f"{row['case_id']}: required fields must be non-empty")
        if row["case_id"] in ids:
            raise AssertionError(f"duplicate cross-context case_id: {row['case_id']}")
        ids.add(row["case_id"])
        skills.add(row["skill"])

        if row["maturity"] != "CROSS_CONTEXT_EVIDENCE":
            raise AssertionError(f"{row['case_id']}: maturity must remain CROSS_CONTEXT_EVIDENCE")
        if row["first_context"] == row["second_context"]:
            raise AssertionError(f"{row['case_id']}: second context must be materially different")
        if not isinstance(row["holds"], list) or len(row["holds"]) < 2:
            raise AssertionError(f"{row['case_id']}: at least two unresolved holds are required")
        if not isinstance(row["forbidden_promotion"], list) or "ACTIVE" not in row["forbidden_promotion"]:
            raise AssertionError(f"{row['case_id']}: must explicitly forbid ACTIVE promotion")

        practice_path = ROOT / row["practice_file"]
        if not practice_path.exists():
            raise AssertionError(f"{row['case_id']}: missing practice evidence {row['practice_file']}")
        practice_text = practice_path.read_text(encoding="utf-8")
        required_terms = [
            "CROSS_CONTEXT_EVIDENCE",
            "materially different",
            "Second-source cross-check",
            "Readback verdict",
            "HOLD",
        ]
        missing_terms = [term for term in required_terms if term not in practice_text]
        if missing_terms:
            raise AssertionError(f"{row['case_id']}: practice file missing terms {missing_terms}")

    if skills != EXPECTED_SKILLS:
        raise AssertionError(f"cross-context skill coverage mismatch: {sorted(skills)}")

    print("Cross-context evidence: PASS")
    print(f"cases={len(rows)} skills={len(skills)} maturity=CROSS_CONTEXT_EVIDENCE")


if __name__ == "__main__":
    main()
