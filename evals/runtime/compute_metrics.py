#!/usr/bin/env python3
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVENTS = ROOT / "evals" / "runtime" / "runtime_events.jsonl"

VALID_SCOPES = {
    "GOVERNANCE-INFRA", "DESIGN-RUNTIME", "PRODUCT", "SPATIAL-ARCH",
    "WEBSITE", "BRAND", "DATA-VIZ", "KNOWLEDGE",
}
VALID_EVENT_TYPES = {
    "FAILURE_RECORD", "HUMAN_DECISION", "RECOMMENDATION_TEST",
    "RETRIEVAL_AUDIT", "PROVENANCE_AUDIT",
}
VALID_EVIDENCE = {"CONFIRMED", "PROVISIONAL", "REJECTED"}
VALID_ESCALATIONS = {"F0", "F1", "F2", "F3", "N-A"}
VALID_REALITY = {"SURVIVED", "PARTIAL", "FAILED", "N-A"}
VALID_REALITY_TEST_TYPES = {
    "PHYSICAL_PROTOTYPE", "SITE_MEASUREMENT", "USER_TEST", "BROWSER_DEVICE",
    "PRODUCTION_SAMPLE", "PROFESSIONAL_SIMULATION", "PROFESSIONAL_INSPECTION", "N-A",
}
VALID_TEST_SEVERITY = {"BASELINE", "STANDARD", "STRESS", "FAILURE", "N-A"}
VALID_AI_ROLES = {
    "Evidence Reader", "Variable Architect", "Scenario Generator", "Adversarial Critic",
    "Simulation Interpreter", "Process Archivist", "Other",
}
VALID_FAILURE_CATEGORIES = {
    "F-SOURCE", "F-STALE", "F-TRUTH", "F-RIGHTS", "F-SAFETY",
    "F-DATA", "F-GEOMETRY", "F-TOOL", "F-CONFLICT", "F-PROVENANCE",
}


def load_jsonl(path: Path):
    if not path.exists():
        raise AssertionError(f"missing runtime events: {path.relative_to(ROOT)}")
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise AssertionError(f"invalid JSON at runtime_events.jsonl:{lineno}: {exc}") from exc
        rows.append(row)
    return rows


def require_ai_provenance(row, ctx):
    if not row.get("ai_run_config"):
        raise AssertionError(f"{ctx}: requires ai_run_config")
    roles = row.get("ai_roles")
    if not isinstance(roles, list) or not roles:
        raise AssertionError(f"{ctx}: requires non-empty ai_roles")
    unknown_roles = set(roles) - VALID_AI_ROLES
    if unknown_roles:
        raise AssertionError(f"{ctx}: invalid ai_roles {sorted(unknown_roles)}")


def validate(rows):
    ids = set()
    required = [
        "event_id", "occurred_at", "scope", "event_type", "project_object_version",
        "evidence_status", "metric_eligible", "evidence_url", "summary", "outcome",
    ]
    for row in rows:
        ctx = row.get("event_id", "runtime-event")
        missing = [k for k in required if k not in row or row[k] in (None, "")]
        if missing:
            raise AssertionError(f"{ctx}: missing required fields: {', '.join(missing)}")
        if row["event_id"] in ids:
            raise AssertionError(f"duplicate runtime event_id: {row['event_id']}")
        ids.add(row["event_id"])
        if row["scope"] not in VALID_SCOPES:
            raise AssertionError(f"{ctx}: invalid scope {row['scope']}")
        if row["event_type"] not in VALID_EVENT_TYPES:
            raise AssertionError(f"{ctx}: invalid event_type {row['event_type']}")
        if row["evidence_status"] not in VALID_EVIDENCE:
            raise AssertionError(f"{ctx}: invalid evidence_status {row['evidence_status']}")
        if not isinstance(row["metric_eligible"], bool):
            raise AssertionError(f"{ctx}: metric_eligible must be boolean")

        if row["event_type"] == "FAILURE_RECORD":
            for field in ["failure_category", "escalation", "detection_stage", "release_opportunity", "blocker_escaped"]:
                if field not in row:
                    raise AssertionError(f"{ctx}: FAILURE_RECORD missing {field}")
            if row["failure_category"] not in VALID_FAILURE_CATEGORIES:
                raise AssertionError(f"{ctx}: invalid failure_category {row['failure_category']}")
            if row["escalation"] not in VALID_ESCALATIONS:
                raise AssertionError(f"{ctx}: invalid escalation {row['escalation']}")
            if not isinstance(row["release_opportunity"], bool):
                raise AssertionError(f"{ctx}: release_opportunity must be boolean")
            if not isinstance(row["blocker_escaped"], bool):
                raise AssertionError(f"{ctx}: blocker_escaped must be boolean")
            if row["blocker_escaped"] and not row["release_opportunity"]:
                raise AssertionError(f"{ctx}: blocker_escaped cannot be true without release_opportunity")

        if row["event_type"] == "HUMAN_DECISION":
            if "human_override" not in row or not isinstance(row["human_override"], bool):
                raise AssertionError(f"{ctx}: HUMAN_DECISION requires boolean human_override")
            if not row.get("recommendation_id"):
                raise AssertionError(f"{ctx}: HUMAN_DECISION requires recommendation_id")
            require_ai_provenance(row, ctx)

        if row["event_type"] == "RECOMMENDATION_TEST":
            if not row.get("recommendation_id"):
                raise AssertionError(f"{ctx}: RECOMMENDATION_TEST requires recommendation_id")
            require_ai_provenance(row, ctx)
            if not row.get("reality_test_completed"):
                raise AssertionError(f"{ctx}: RECOMMENDATION_TEST must represent a completed qualifying reality test")
            if row.get("reality_test_type") not in VALID_REALITY_TEST_TYPES - {"N-A"}:
                raise AssertionError(f"{ctx}: requires qualifying reality_test_type")
            if row.get("test_severity") not in VALID_TEST_SEVERITY - {"N-A"}:
                raise AssertionError(f"{ctx}: requires test_severity")
            if row.get("reality_test_outcome") not in VALID_REALITY - {"N-A"}:
                raise AssertionError(f"{ctx}: invalid reality_test_outcome")
            if not row.get("reality_evidence_url"):
                raise AssertionError(f"{ctx}: requires reality_evidence_url")

        if row["event_type"] == "RETRIEVAL_AUDIT":
            payload = row.get("metric_payload") or {}
            for field in ["audited_queries", "retrieval_misses", "wrong_authority"]:
                if not isinstance(payload.get(field), int) or payload[field] < 0:
                    raise AssertionError(f"{ctx}: RETRIEVAL_AUDIT requires nonnegative integer {field}")
            if payload["retrieval_misses"] > payload["audited_queries"] or payload["wrong_authority"] > payload["audited_queries"]:
                raise AssertionError(f"{ctx}: retrieval numerators cannot exceed audited_queries")
            if row["metric_eligible"] and payload["audited_queries"] == 0:
                raise AssertionError(f"{ctx}: metric-eligible RETRIEVAL_AUDIT requires audited_queries > 0")

        if row["event_type"] == "PROVENANCE_AUDIT":
            payload = row.get("metric_payload") or {}
            for field in ["eligible_assets", "manifested_assets"]:
                if not isinstance(payload.get(field), int) or payload[field] < 0:
                    raise AssertionError(f"{ctx}: PROVENANCE_AUDIT requires nonnegative integer {field}")
            if payload["manifested_assets"] > payload["eligible_assets"]:
                raise AssertionError(f"{ctx}: manifested_assets cannot exceed eligible_assets")
            if row["metric_eligible"] and payload["eligible_assets"] == 0:
                raise AssertionError(f"{ctx}: metric-eligible PROVENANCE_AUDIT requires eligible_assets > 0")


def rate(n, d):
    if d == 0:
        return "N/A — insufficient eligible evidence"
    return f"{n}/{d} = {100*n/d:.1f}%"


def aggregate(rows):
    by_scope = defaultdict(list)
    for row in rows:
        if row["evidence_status"] == "CONFIRMED" and row["metric_eligible"]:
            by_scope[row["scope"]].append(row)

    results = {}
    for scope, events in sorted(by_scope.items()):
        failures = [e for e in events if e["event_type"] == "FAILURE_RECORD" and e.get("escalation") in {"F1", "F2", "F3"}]
        release_failures = [e for e in failures if e.get("release_opportunity")]
        escaped = sum(bool(e.get("blocker_escaped")) for e in release_failures)
        prerelease = sum(e.get("detection_stage") == "PRE-RELEASE" for e in release_failures)

        decisions = [e for e in events if e["event_type"] == "HUMAN_DECISION"]
        overrides = sum(bool(e.get("human_override")) for e in decisions)

        reality = [e for e in events if e["event_type"] == "RECOMMENDATION_TEST" and e.get("reality_test_completed")]
        survived = sum(e.get("reality_test_outcome") == "SURVIVED" for e in reality)
        partial = sum(e.get("reality_test_outcome") == "PARTIAL" for e in reality)

        retrieval = [e for e in events if e["event_type"] == "RETRIEVAL_AUDIT"]
        audited_queries = sum(e["metric_payload"]["audited_queries"] for e in retrieval)
        retrieval_misses = sum(e["metric_payload"]["retrieval_misses"] for e in retrieval)
        wrong_authority = sum(e["metric_payload"]["wrong_authority"] for e in retrieval)

        provenance = [e for e in events if e["event_type"] == "PROVENANCE_AUDIT"]
        eligible_assets = sum(e["metric_payload"]["eligible_assets"] for e in provenance)
        manifested_assets = sum(e["metric_payload"]["manifested_assets"] for e in provenance)

        results[scope] = {
            "eligible_events": len(events),
            "confirmed_f1_f3_failures": len(failures),
            "release_opportunity_failures": len(release_failures),
            "blocker_escape_rate": rate(escaped, len(release_failures)),
            "pre_release_catch_rate": rate(prerelease, len(release_failures)),
            "human_override_rate": rate(overrides, len(decisions)),
            "recommendation_reality_survival_rate": rate(survived, len(reality)),
            "recommendation_partial_count": partial,
            "retrieval_miss_rate": rate(retrieval_misses, audited_queries),
            "wrong_authority_rate": rate(wrong_authority, audited_queries),
            "asset_provenance_coverage": rate(manifested_assets, eligible_assets),
        }
    return results


def print_report(results):
    print("P2 RUNTIME EVIDENCE: PASS")
    if not results:
        print("No confirmed metric-eligible events.")
        return
    for scope, m in results.items():
        print(f"\n[{scope}]")
        print(f"eligible events: {m['eligible_events']}")
        print(f"confirmed F1-F3 failures: {m['confirmed_f1_f3_failures']}")
        print(f"release-opportunity failures: {m['release_opportunity_failures']}")
        print(f"blocker escape rate: {m['blocker_escape_rate']}")
        print(f"pre-release catch rate: {m['pre_release_catch_rate']}")
        print(f"human override rate: {m['human_override_rate']}")
        print(f"recommendation -> reality-test survival: {m['recommendation_reality_survival_rate']}")
        print(f"partial reality-test outcomes: {m['recommendation_partial_count']}")
        print(f"retrieval miss rate: {m['retrieval_miss_rate']}")
        print(f"wrong-authority rate: {m['wrong_authority_rate']}")
        print(f"asset provenance coverage: {m['asset_provenance_coverage']}")


def main():
    try:
        rows = load_jsonl(EVENTS)
        validate(rows)
        results = aggregate(rows)
    except AssertionError as exc:
        print(f"P2 RUNTIME EVIDENCE: FAIL\n{exc}", file=sys.stderr)
        return 1
    print_report(results)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
