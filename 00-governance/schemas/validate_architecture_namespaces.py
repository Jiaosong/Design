#!/usr/bin/env python3
import json
import re
import subprocess
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

# Legacy parallel roots already exist in historical/current main. Do not delete them
# merely to make the architecture look clean. Freeze their exact tree identity so
# ordinary future PRs cannot silently add more current work there. Any intentional
# migration/removal must explicitly review and update this frozen SHA in the same
# governance change.
FROZEN_LEGACY_ROOTS = {
    "practice": "fa29e287d3347cafa788bf904d760c2b8c11fd34",
    "tools": "45d7f97ac289704226c5b0a8a382ce2a38ec518f",
}
FORBIDDEN_NEW_ROOTS = {
    "governance": "use 00-governance or the relevant current domain path",
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
        "OLEANDER_AI_Governance_P0_v0.1.md",
        "OLEANDER_AI_Governance_P1_v0.1.md",
        "OLEANDER_AI_Runtime_Evidence_P2_v0.1.md",
    ],
}

PRACTICE_MAP_FILES = [
    ROOT / "06-practice" / "2026" / "PRAC-BUSINESS-2026" / "project-map.json",
    ROOT / "06-practice" / "2026" / "PRAC-CULTURE-2026" / "project-map.json",
    ROOT / "06-practice" / "2026" / "PRAC-IP-2026" / "project-map.json",
    ROOT / "06-practice" / "2026" / "PRAC-SPATIAL-2026" / "project-map.json",
]
PRACTICE_CURRENT_FILES = [
    ROOT / "06-practice" / "2026" / "README.md",
    ROOT / "06-practice" / "2026" / "PRAC-BUSINESS-2026" / "README.md",
    ROOT / "06-practice" / "2026" / "PRAC-CULTURE-2026" / "README.md",
    ROOT / "06-practice" / "2026" / "PRAC-IP-2026" / "README.md",
    ROOT / "06-practice" / "2026" / "PRAC-SPATIAL-2026" / "README.md",
]
LEGACY_PRIORITY_LABELS = ["P0 紧急", "P1 重要", "P2 一般", "P3 低"]
NODE_CODE_RE = re.compile(r"^(?:B|CU|IP|SP)\d{2}$")
PRIORITY_RE = re.compile(r"^Priority-[0-3](?:｜.*)?$")


def fail(message):
    raise AssertionError(message)


def git_tree_sha(path: str):
    try:
        return subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True
        ).strip()
    except subprocess.CalledProcessError:
        return None


def validate_practice_map(path: Path):
    if not path.exists():
        fail(f"missing current Practice project map: {path.relative_to(ROOT)}")
    data = json.loads(path.read_text(encoding="utf-8"))

    project = data.get("project") or {}
    project_id = project.get("id", "")
    if project.get("level") != "P2":
        fail(f"Practice map project must be P2: {path.relative_to(ROOT)}")
    if NODE_CODE_RE.fullmatch(project_id):
        fail(f"four-layer node used as project ID in {path.relative_to(ROOT)}: {project_id}")

    explicit_flag = data.get("node_codes_are_project_ids")
    spatial_flag = (data.get("architecture_baseline") or {}).get("spatial_nodes_are_project_ids")
    if explicit_flag is not False and spatial_flag is not False:
        fail(f"Practice map must explicitly deny node-code project identity: {path.relative_to(ROOT)}")

    for row in data.get("workstreams", []):
        node = row.get("node", "")
        workstream_id = row.get("id", "")
        if NODE_CODE_RE.fullmatch(workstream_id):
            fail(f"four-layer node used as workstream project ID in {path.relative_to(ROOT)}: {workstream_id}")
        if node and workstream_id == node:
            fail(f"workstream ID collapses to node code in {path.relative_to(ROOT)}: {node}")
        priority = row.get("delivery_priority")
        if priority is not None and not PRIORITY_RE.fullmatch(priority):
            fail(f"invalid delivery-priority namespace in {path.relative_to(ROOT)}: {priority}")

    for row in data.get("validations", []):
        validation_id = row.get("id", "")
        if NODE_CODE_RE.fullmatch(validation_id):
            fail(f"four-layer node used as validation project ID in {path.relative_to(ROOT)}: {validation_id}")


def main():
    for root_name, route in FORBIDDEN_NEW_ROOTS.items():
        if (ROOT / root_name).exists():
            fail(f"parallel top-level root is forbidden: {root_name}/; {route}")

    for root_name, expected_sha in FROZEN_LEGACY_ROOTS.items():
        actual_sha = git_tree_sha(root_name)
        if actual_sha != expected_sha:
            fail(
                f"frozen legacy root changed: {root_name}/ expected {expected_sha}, got {actual_sha}; "
                "new current work must use canonical roots. Intentional migration requires an explicit governance review/update."
            )

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

    for path in PRACTICE_MAP_FILES:
        validate_practice_map(path)

    for path in PRACTICE_CURRENT_FILES:
        if not path.exists():
            fail(f"missing current Practice authority file: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        for term in LEGACY_PRIORITY_LABELS:
            if term in text:
                fail(f"legacy P0-P3 delivery-priority label in current Practice authority: {path.relative_to(ROOT)}: {term!r}")

    print("ARCHITECTURE NAMESPACE GATE: PASS")
    print("- P0-P4 reserved for project axis")
    print("- AIG-01/AIG-02/AIG-03 current contracts present")
    print("- superseded AI P0/P1/P2 current files absent")
    print("- delivery priority namespace: Priority-0..Priority-3")
    print("- Business/Culture/IP/Spatial Practice maps deny node-code project identity")
    print("- governance/ parallel root absent")
    print("- legacy practice/ and tools/ roots frozen at reviewed tree SHAs")
    print("- new runtime event namespace: AIG3-E...")
    print("- current reasoning/skill/CI routing contains no known old AI-governance paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
