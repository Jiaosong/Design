#!/usr/bin/env python3
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / "evals" / "golden" / "skills.jsonl"
RETRIEVAL = ROOT / "evals" / "retrieval" / "golden_queries.jsonl"
FAILURES = ROOT / "evals" / "failure" / "failure_cases.jsonl"
AIG01 = ROOT / "90-shared" / "OLEANDER_AIG-01_Evaluation_Regression_v0.1.md"
AIG02 = ROOT / "90-shared" / "OLEANDER_AIG-02_Failure_Trust_Provenance_v0.1.md"
AIG03 = ROOT / "90-shared" / "OLEANDER_AIG-03_Runtime_Evidence_v0.1.md"
FAILURE_PLAYBOOK = ROOT / "evals" / "failure" / "FAILURE_ESCALATION_PLAYBOOK.md"
TRUST_CARD = ROOT / "evals" / "trust" / "AI_RECOMMENDATION_CARD.md"
PROVENANCE = ROOT / "evals" / "provenance" / "ASSET_PROVENANCE_MANIFEST_TEMPLATE.json"
RUNTIME_EVENTS = ROOT / "evals" / "runtime" / "runtime_events.jsonl"
RUNTIME_TEMPLATE = ROOT / "evals" / "runtime" / "RUNTIME_EVENT_TEMPLATE.json"
RUNTIME_METRICS = ROOT / "evals" / "runtime" / "compute_metrics.py"
RUNTIME_BASELINE = ROOT / "evals" / "runtime" / "BASELINE_2026-08-10.md"

REQUIRED_SKILLS = {
    "oleander-research",
    "oleander-data-viz",
    "oleander-3d-pipeline",
    "oleander-technical-drawing",
    "oleander-story-and-board",
    "oleander-delivery-qc",
}

FAILURE_CATEGORIES = {
    "F-SOURCE", "F-STALE", "F-TRUTH", "F-RIGHTS", "F-SAFETY",
    "F-DATA", "F-GEOMETRY", "F-TOOL", "F-CONFLICT", "F-PROVENANCE",
}

ESCALATION_LEVELS = {"F0", "F1", "F2", "F3"}


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


def require_nonempty_fields(row, fields, context):
    missing = [f for f in fields if f not in row or row[f] in (None, "", [])]
    if missing:
        raise AssertionError(f"{context}: missing required fields: {', '.join(missing)}")


def require_present_fields(row, fields, context):
    missing = [f for f in fields if f not in row]
    if missing:
        raise AssertionError(f"{context}: missing required fields: {', '.join(missing)}")


def validate_skill_cases(rows):
    ids = set()
    counts = Counter()
    required = ["case_id", "skill", "task", "required_outputs", "blockers", "pass_rule"]
    for row in rows:
        require_nonempty_fields(row, required, row.get("case_id", "skill-case"))
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
    nonempty_required = [
        "query_id", "query", "expected_canonical_sources", "required_status",
        "required_truth_state", "required_warning",
    ]
    presence_required = ["forbidden_legacy_sources"]
    for row in rows:
        context = row.get("query_id", "retrieval-case")
        require_nonempty_fields(row, nonempty_required, context)
        require_present_fields(row, presence_required, context)
        if row["query_id"] in ids:
            raise AssertionError(f"duplicate query_id: {row['query_id']}")
        ids.add(row["query_id"])
        if not isinstance(row["expected_canonical_sources"], list) or not row["expected_canonical_sources"]:
            raise AssertionError(f"{row['query_id']}: expected_canonical_sources must be non-empty list")
        if not isinstance(row["forbidden_legacy_sources"], list):
            raise AssertionError(f"{row['query_id']}: forbidden_legacy_sources must be a list")
    if len(rows) < 10:
        raise AssertionError("retrieval golden set requires at least 10 cases")


def validate_failure_cases(rows):
    ids = set()
    required = ["case_id", "trigger", "category", "minimum_escalation", "required_actions", "blocker"]
    for row in rows:
        require_nonempty_fields(row, required, row.get("case_id", "failure-case"))
        if row["case_id"] in ids:
            raise AssertionError(f"duplicate failure case_id: {row['case_id']}")
        ids.add(row["case_id"])
        if row["category"] not in FAILURE_CATEGORIES:
            raise AssertionError(f"{row['case_id']}: unknown failure category {row['category']}")
        if row["minimum_escalation"] not in ESCALATION_LEVELS:
            raise AssertionError(f"{row['case_id']}: invalid escalation {row['minimum_escalation']}")
        if not isinstance(row["required_actions"], list) or len(row["required_actions"]) < 2:
            raise AssertionError(f"{row['case_id']}: requires at least 2 recovery actions")
    if len(rows) < 8:
        raise AssertionError("AIG-02 failure set requires at least 8 cases")


def validate_protocol(path: Path, required_terms, label):
    if not path.exists():
        raise AssertionError(f"missing {label} governance protocol")
    text = path.read_text(encoding="utf-8")
    missing = [term for term in required_terms if term not in text]
    if missing:
        raise AssertionError(f"{label} protocol missing governance terms: {missing}")


def validate_aig02_assets():
    for path in (FAILURE_PLAYBOOK, TRUST_CARD, PROVENANCE):
        if not path.exists():
            raise AssertionError(f"missing AIG-02 execution file: {path.relative_to(ROOT)}")

    trust_text = TRUST_CARD.read_text(encoding="utf-8")
    trust_terms = ["Evidence basis", "Unknowns / conflicts", "What would falsify this", "Human action required", "Rollback path"]
    missing = [term for term in trust_terms if term not in trust_text]
    if missing:
        raise AssertionError(f"AI Recommendation Card missing fields: {missing}")

    try:
        manifest = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"invalid provenance manifest JSON: {exc}") from exc

    for field in ["manifest_version", "asset_id", "project", "object_version", "file", "origin", "creation", "ingredients", "actions", "known_unknowns", "c2pa"]:
        if field not in manifest:
            raise AssertionError(f"provenance manifest missing field: {field}")
    if manifest.get("c2pa", {}).get("content_credentials_present") is not False:
        raise AssertionError("template must not claim Content Credentials are present by default")


def validate_aig03_assets():
    for path in (RUNTIME_EVENTS, RUNTIME_TEMPLATE, RUNTIME_METRICS, RUNTIME_BASELINE):
        if not path.exists():
            raise AssertionError(f"missing AIG-03 runtime evidence file: {path.relative_to(ROOT)}")

    runtime_rows = load_jsonl(RUNTIME_EVENTS)
    if len(runtime_rows) < 1:
        raise AssertionError("AIG-03 requires at least one runtime evidence event")

    try:
        template = json.loads(RUNTIME_TEMPLATE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"invalid runtime event template JSON: {exc}") from exc

    for field in ["event_id", "occurred_at", "scope", "event_type", "evidence_status", "metric_eligible", "evidence_url", "outcome"]:
        if field not in template:
            raise AssertionError(f"runtime event template missing field: {field}")

    baseline = RUNTIME_BASELINE.read_text(encoding="utf-8")
    for term in ["Blocker escape rate", "Human override rate", "Recommendation → reality-test survival", "Asset provenance coverage", "N/A"]:
        if term not in baseline:
            raise AssertionError(f"runtime baseline missing metric/boundary term: {term}")


def main():
    try:
        skill_rows = load_jsonl(SKILLS)
        retrieval_rows = load_jsonl(RETRIEVAL)
        failure_rows = load_jsonl(FAILURES)
        counts = validate_skill_cases(skill_rows)
        validate_retrieval_cases(retrieval_rows)
        validate_failure_cases(failure_rows)
        validate_protocol(AIG01, [
            "AI Necessity Gate", "AI Eval Harness", "Retrieval & Context QA",
            "AI Change & Regression Gate", "NO-AI", "HOLD", "PROMOTE", "ROLLBACK",
        ], "AIG-01")
        validate_protocol(AIG02, [
            "Failure & Escalation", "Human-AI Trust Calibration", "Asset-level Provenance",
            "F0 SELF-CORRECT", "F1 HUMAN-REVIEW", "F2 DOMAIN-EXPERT", "F3 STOP-HOLD",
            "AI Recommendation Card", "C2PA compatibility direction",
        ], "AIG-02")
        validate_protocol(AIG03, [
            "Human Override Rate", "Recommendation → Reality-test Survival Rate",
            "Blocker Escape Rate", "Asset Provenance Coverage",
            "Retrieval Miss / Wrong-Authority Rate", "N/A — insufficient eligible evidence",
        ], "AIG-03")
        validate_aig02_assets()
        validate_aig03_assets()
    except AssertionError as exc:
        print(f"AI GOVERNANCE EVAL CORPUS: FAIL\n{exc}", file=sys.stderr)
        return 1

    print("AI GOVERNANCE EVAL CORPUS: PASS")
    print(f"skill cases: {len(skill_rows)} | retrieval cases: {len(retrieval_rows)} | failure cases: {len(failure_rows)}")
    for skill in sorted(counts):
        print(f"- {skill}: {counts[skill]}")
    print("- AIG-02 trust card: present")
    print("- AIG-02 provenance manifest: valid JSON / no false C2PA claim")
    print("- AIG-03 runtime evidence protocol + event corpus: present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())