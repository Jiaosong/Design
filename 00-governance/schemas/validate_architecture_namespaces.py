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
# merely to make the architecture look clean. Freeze their reviewed tree identity so
# ordinary future PRs cannot silently add more current work there. The practice/ SHA
# below includes the audited Legacy-location README added during Authority Integrity
# cleanup; changing it again requires explicit governance review in the same change.
FROZEN_LEGACY_ROOTS = {
    "practice": "6c44d003197c9aa31050b1f445e4670e48dd0843",
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
        'OLEANDER_AI_Governance_P0_v0.1.md',
        'OLEANDER_AI_Governance_P1_v0.1.md',
        'OLEANDER_AI_Runtime_Evidence_P2_v0.1.md',
    ],
}

PROJECT_FLOW_SCHEMA = ROOT / "00-governance" / "schemas" / "oleander-project-flow-v0.3.schema.json"


def fail(message):
    raise AssertionError(message)


def git_tree_sha(path: str):
    try:
        return subprocess.check_output(
            ["git", "rev-parse", f"HEAD:{path}"], cwd=ROOT, text=True
        ).strip()
    except subprocess.CalledProcessError:
        return None


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

    aig01 = (ROOT / "90-shared" / "OLEANDER_AIG-01_Evaluation_Regression_v0.1.md").read_text(encoding="utf-8")
    for stale_eval_label in ("`L1 Contract`", "`L2 Evidence`", "`L3 Task`", "`L4 Safety / Rights`", "`L5 Regression`"):
        if stale_eval_label in aig01:
            fail(f"AIG-01 reuses Knowledge Architecture L0-L7 namespace: {stale_eval_label}")
    for required_eval_label in ("EVAL-1 Contract", "EVAL-2 Evidence", "EVAL-3 Task", "EVAL-4 Safety / Rights", "EVAL-5 Regression"):
        if required_eval_label not in aig01:
            fail(f"AIG-01 missing explicit evaluation namespace: {required_eval_label}")

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

    if not PROJECT_FLOW_SCHEMA.exists():
        fail("missing project-flow machine contract")
    project_flow_schema = json.loads(PROJECT_FLOW_SCHEMA.read_text(encoding="utf-8"))
    project_props = project_flow_schema.get("properties", {}).get("project", {}).get("properties", {})
    project_required = set(project_flow_schema.get("properties", {}).get("project", {}).get("required", []))
    stale_project_keys = {"primary_layer", "primary_node", "supporting_nodes"} & set(project_props)
    if stale_project_keys:
        fail(f"project-flow schema still encodes old layer ownership: {sorted(stale_project_keys)}")
    if not {"project_level", "project_id"}.issubset(project_required):
        fail("project-flow schema must require explicit project_level + project_id")
    if "application_mapping" not in project_props or "application_primary_mapping" not in project_props:
        fail("project-flow schema must separate Application Mapping from Project Axis")
    if "knowledge_context" not in project_props:
        fail("project-flow schema must support Domain / exact L0-L7 knowledge context separately")

    project_id_schema = project_props.get("project_id", {})
    forbidden_project_pattern = project_id_schema.get("not", {}).get("pattern")
    if not forbidden_project_pattern:
        fail("project-flow schema must machine-reject reserved non-project namespaces in project_id")
    for reserved_id in ("C04", "B02", "CU01", "IP03", "SP04", "Priority-1", "AIG-01"):
        if re.fullmatch(forbidden_project_pattern, reserved_id) is None:
            fail(f"project_id exclusion pattern does not reject reserved namespace: {reserved_id}")
    for valid_project_id in ("PRJ-XJ01-CMF", "PG-30", "SYS-BLENDER-SURFACE", "PRAC-SPATIAL-2026"):
        if re.fullmatch(forbidden_project_pattern, valid_project_id) is not None:
            fail(f"project_id exclusion pattern wrongly rejects current Project ID: {valid_project_id}")

    print("ARCHITECTURE NAMESPACE GATE: PASS")
    print("- P0-P4 reserved for project axis")
    print("- L0-L7 reserved for Knowledge Architecture; AIG uses EVAL-* for evaluation layers")
    print("- Project Flow schema requires project_level + project_id")
    print("- project_id rejects Case / Application / Priority / AIG namespaces")
    print("- Application Mapping and Knowledge Context are machine-separated")
    print("- AIG-01/AIG-02/AIG-03 current contracts present")
    print("- superseded AI P0/P1/P2 current files absent")
    print("- governance/ parallel root absent")
    print("- legacy practice/ and tools/ roots frozen at reviewed tree SHAs")
    print("- new runtime event namespace: AIG3-E...")
    print("- current reasoning/skill/CI routing contains no known old AI-governance paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
