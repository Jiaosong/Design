#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

AIG_FILES = [
    ROOT / "90-shared" / "OLEANDER_AIG-01_Evaluation_Regression_v0.1.md",
    ROOT / "90-shared" / "OLEANDER_AIG-02_Failure_Trust_Provenance_v0.1.md",
    ROOT / "90-shared" / "OLEANDER_AIG-03_Runtime_Evidence_v0.1.md",
]
OLD_CURRENT_FILES = [
    ROOT / "90-shared" / "OLEANDER_AI_Governance_P0_v0.1.md",
    ROOT / "90-shared" / "OLEANDER_AI_Governance_P1_v0.1.md",
    ROOT / "90-shared" / "OLEANDER_AI_Runtime_Evidence_P2_v0.1.md",
]

# These parallel roots were used by older/experimental branches. Current OLEANDER
# authority uses 00-governance, 06-practice and 90-shared/toolchains instead.
FORBIDDEN_PARALLEL_ROOTS = {
    "governance": "use 00-governance or the relevant current domain path",
    "practice": "use 06-practice",
    "tools": "use 90-shared/toolchains for shared reusable toolchains, or a scoped current project path",
}

CURRENT_ROUTING_FILES = {
    ROOT / "90-shared" / "README.md": [
        "OLEANDER_AI_Governance_P0_v0.1.md",
        "OLEANDER_AI_Governance_P1_v0.1.md",
        "OLEANDER_AI_Runtime_Evidence_P2_v0.1.md",
    ],
    ROOT / "90-shared" / "OLEANDER_AI_Design_Reasoning_Protocol_v0.2.md": [
        "P0 governance prerequisite",
        "P0 gates are human-governed",
        "OLEANDER_AI_Governance_P0_v0.1.md",
    ],
    ROOT / "oleander-skills" / "REVIEW.md": [
        "## P0 AI governance checks",
        "P0 coverage",
        "OLEANDER_AI_Governance_P0_v0.1.md",
    ],
    ROOT / ".github" / "workflows" / "ai-governance-evals.yml": [
        "P0 + P1 + P2 governance",
        "/tmp/p2-metrics.txt",
        "### P2 current evidence",
    ],
    ROOT / "evals" / "runtime" / "compute_metrics.py": [
        "P2 RUNTIME EVIDENCE: PASS",
        "P2 RUNTIME EVIDENCE: FAIL",
    ],
    ROOT / "evals" / "scripts" / "validate_evals.py": [
        'OLEANDER_AI_Governance_P0_v0.1.md',
        'OLEANDER_AI_Governance_P1_v0.1.md',
        'OLEANDER_AI_Runtime_Evidence_P2_v0.1.md',
    ],
}


def fail(message):
    raise AssertionError(message)


def main():
    for root_name, route in FORBIDDEN_PARALLEL_ROOTS.items():
        path = ROOT / root_name
        if path.exists():
            fail(f"parallel top-level root is forbidden: {root_name}/; {route}")

    for path in AIG_FILES:
        if not path.exists():
            fail(f"missing current AIG contract: {path.relative_to(ROOT)}")

    for path in OLD_CURRENT_FILES:
        if path.exists():
            fail(f"superseded AI P0/P1/P2 file still present in current authority: {path.relative_to(ROOT)}")

    for path, forbidden_terms in CURRENT_ROUTING_FILES.items():
        if not path.exists():
            fail(f"missing current routing file: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for term in forbidden_terms:
            if term in text:
                fail(f"current-authority namespace pollution in {path.relative_to(ROOT)}: {term!r}")

    reasoning = (ROOT / "90-shared" / "OLEANDER_AI_Design_Reasoning_Protocol_v0.2.md").read_text(encoding="utf-8")
    if "## AIG-01 governance prerequisite" not in reasoning:
        fail("AI Design Reasoning Protocol must route through AIG-01")

    skill_review = (ROOT / "oleander-skills" / "REVIEW.md").read_text(encoding="utf-8")
    if "## AIG-01 AI governance checks" not in skill_review:
        fail("oleander-skills/REVIEW.md must route reusable skills through AIG-01")

    template = json.loads((ROOT / "evals" / "runtime" / "RUNTIME_EVENT_TEMPLATE.json").read_text(encoding="utf-8"))
    if template.get("event_id") != "AIG3-E...":
        fail("new runtime-event template must use AIG3-E... namespace")

    golden_rows = []
    for line in (ROOT / "evals" / "retrieval" / "golden_queries.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            golden_rows.append(json.loads(line))
    rq12 = next((row for row in golden_rows if row.get("query_id") == "RQ-012"), None)
    if rq12 is None:
        fail("RQ-012 missing from retrieval golden set")
    expected = rq12.get("expected_canonical_sources", [])
    if "GitHub:90-shared/OLEANDER_AIG-01_Evaluation_Regression_v0.1.md" not in expected:
        fail("RQ-012 must route current GitHub authority to AIG-01")
    forbidden = rq12.get("forbidden_legacy_sources", [])
    if "GitHub:90-shared/OLEANDER_AI_Governance_P0_v0.1.md" not in forbidden:
        fail("RQ-012 must retain the former P0 file only as forbidden legacy authority")

    print("ARCHITECTURE NAMESPACE GATE: PASS")
    print("- P0-P4 reserved for project axis")
    print("- AIG-01/AIG-02/AIG-03 current contracts present")
    print("- superseded AI P0/P1/P2 current files absent")
    print("- forbidden parallel roots absent: governance/ practice/ tools/")
    print("- new runtime event namespace: AIG3-E...")
    print("- current reasoning/skill/CI routing contains no known old AI-governance paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
