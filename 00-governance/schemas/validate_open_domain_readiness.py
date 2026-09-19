from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "00-governance/open-domain-readiness/OPEN_DOMAIN_READINESS_REGISTER_v0.1.json"
ARCH_MAP = ROOT / "00-governance/runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md"

EXPECTED = {
    "Interior Design": {
        "state": "CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
        "doc": "00-governance/open-domain-readiness/INTERIOR_DESIGN_OPEN_DOMAIN_READINESS_v0.1.md",
        "failure": "FAIL-052",
    },
    "Lighting Design": {
        "state": "CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
        "doc": "00-governance/open-domain-readiness/LIGHTING_DESIGN_OPEN_DOMAIN_READINESS_v0.1.md",
        "failure": "FAIL-053",
    },
}


def fail(message: str) -> None:
    raise SystemExit(f"OPEN_DOMAIN_READINESS_FAIL: {message}")


def require_nonempty(obj: dict, field: str, label: str) -> None:
    value = obj.get(field)
    if value in (None, "", [], {}):
        fail(f"{label}.{field} must be non-empty")


def main() -> None:
    if not REGISTER.exists():
        fail(f"missing register: {REGISTER.relative_to(ROOT)}")
    if not ARCH_MAP.exists():
        fail(f"missing architecture map: {ARCH_MAP.relative_to(ROOT)}")

    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    arch = ARCH_MAP.read_text(encoding="utf-8")

    if data.get("authority_position") != "NON_CURRENT READINESS REGISTER / DOES NOT PROMOTE DOMAIN PROCESS":
        fail("register authority_position drift")

    domains = data.get("domains")
    if not isinstance(domains, list) or not domains:
        fail("domains must be a non-empty list")

    by_name = {d.get("domain"): d for d in domains}
    if set(by_name) != set(EXPECTED):
        fail(f"expected exactly {sorted(EXPECTED)}, got {sorted(by_name)}")

    for name, expected in EXPECTED.items():
        d = by_name[name]
        label = name.replace(" ", "_")

        if d.get("current_architecture_state") != expected["state"]:
            fail(f"{name}: current_architecture_state drift")

        if expected["state"] not in arch:
            # Architecture Map may format the domain name on the same line; require both tokens.
            if name not in arch or "DOMAIN PROCESS OPEN" not in arch:
                fail(f"{name}: Current Architecture Map no longer reads OPEN")

        if d.get("candidate_creation_state") != "BLOCKED_EXECUTION_CARRIER_ABSENT":
            fail(f"{name}: candidate creation must remain blocked while carrier is absent")

        if "DOMAIN_PROCESS_OPEN" not in d.get("claim_ceiling", ""):
            fail(f"{name}: claim ceiling must preserve DOMAIN_PROCESS_OPEN")

        for field in (
            "professional_scope_state",
            "current_source_basis",
            "existing_oleander_strengths",
            "missing_execution_carrier",
            "minimum_candidate_carrier_rule",
            "allowed_next_actions",
            "forbidden_shortcuts",
            "claim_ceiling",
        ):
            require_nonempty(d, field, label)

        rule = d["minimum_candidate_carrier_rule"]
        if not isinstance(rule.get("minimum_distinct_objects"), int) or rule["minimum_distinct_objects"] < 1:
            fail(f"{name}: minimum_distinct_objects must be positive")
        require_nonempty(rule, "must_include", f"{label}.minimum_candidate_carrier_rule")

        doc = ROOT / expected["doc"]
        if not doc.exists():
            fail(f"{name}: missing readiness document {expected['doc']}")
        prose = doc.read_text(encoding="utf-8")
        if "DOMAIN PROCESS OPEN" not in prose:
            fail(f"{name}: readiness prose must preserve OPEN state")
        if "NO CANDIDATE PROCESS YET" not in prose:
            fail(f"{name}: readiness prose must explicitly remain non-Candidate")

    failures = ROOT / "evals/failure/failure_cases.jsonl"
    if not failures.exists():
        fail("missing failure corpus")
    ids = []
    for line in failures.read_text(encoding="utf-8").splitlines():
        if line.strip():
            ids.append(json.loads(line)["case_id"])
    for expected in EXPECTED.values():
        if expected["failure"] not in ids:
            fail(f"missing regression {expected['failure']}")

    if not data.get("does_not_prove"):
        fail("register does_not_prove must be non-empty")

    print("OPEN_DOMAIN_READINESS_PASS")


if __name__ == "__main__":
    main()
