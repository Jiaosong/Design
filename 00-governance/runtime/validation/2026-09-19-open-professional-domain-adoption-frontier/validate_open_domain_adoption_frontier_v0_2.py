#!/usr/bin/env python3
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MATRIX = HERE / "OPEN_DOMAIN_ADOPTION_FRONTIER_v0.2.json"
ARCH = ROOT / "00-governance/runtime/OLEANDER_CURRENT_ARCHITECTURE_MAP_v2.1.md"

EXPECTED = {
    "Interior Design",
    "Landscape Architecture",
    "Lighting Design",
    "Digital Product / HCD",
    "Systems Engineering",
}

OPEN_LINES = {
    "Interior Design": "Interior Design          = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
    "Landscape Architecture": "Landscape Architecture   = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
    "Lighting Design": "Lighting Design          = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
    "Digital Product / HCD": "Digital Product / HCD    = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
    "Systems Engineering": "Systems Engineering      = CONTRACT_ENVELOPE_AVAILABLE / DOMAIN PROCESS OPEN",
}


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def check_path(rel: str, label: str) -> Path:
    p = ROOT / rel
    if not p.exists():
        fail(f"{label} missing: {rel}")
    return p


def git_blob_sha(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    try:
        blob = subprocess.check_output(
            ["git", "rev-parse", f":{rel}"],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
        ).strip()
        canonical = subprocess.check_output(
            ["git", "cat-file", "blob", blob],
            cwd=ROOT,
        )
    except subprocess.CalledProcessError:
        fail(f"bound evidence is not staged/tracked in Git: {rel}")
    expected = hashlib.sha1(
        f"blob {len(canonical)}\0".encode("ascii") + canonical
    ).hexdigest()
    if expected != blob:
        fail(f"Git canonical blob verification failed: {rel}")
    return blob


def main() -> None:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    arch = ARCH.read_text(encoding="utf-8")

    if data.get("schema_version") != "oleander-open-domain-adoption-frontier/0.2":
        fail("unexpected frontier schema_version")
    if not data.get("supersedes", {}).get("path", "").endswith(
        "OPEN_DOMAIN_ADOPTION_FRONTIER_v0.1.json"
    ):
        fail("v0.2 must record v0.1 diagnostic supersession")

    domains = data.get("domains", [])
    names = [d.get("domain") for d in domains]
    if set(names) != EXPECTED or len(names) != len(EXPECTED):
        fail(f"domain set drift: {names}")

    for domain, line in OPEN_LINES.items():
        if line not in arch:
            fail(
                f"{domain} is no longer OPEN as expected by this diagnostic; "
                "regenerate frontier before use"
            )

    bindings = data.get("source_bindings", [])
    if not bindings:
        fail("source_bindings missing")

    seen = set()
    for binding in bindings:
        rel = binding.get("path")
        sha = binding.get("blob_sha")
        role = binding.get("role")
        if not rel or not sha or not role:
            fail(f"incomplete source binding: {binding}")
        if rel in seen:
            fail(f"duplicate source binding: {rel}")
        seen.add(rel)
        path = check_path(rel, "bound evidence")
        actual = git_blob_sha(path)
        if actual != sha:
            fail(
                f"stale frontier binding for {rel}: expected {sha}, got {actual}; "
                "regenerate v0.2"
            )

    for domain in domains:
        name = domain["domain"]
        if domain.get("current_status") != "OPEN":
            fail(f"{name}: matrix must not claim Current/promotion")
        if domain.get("professional_pass") is not False:
            fail(f"{name}: professional_pass must remain false in this snapshot")
        if domain.get("current_promotion") is not False:
            fail(f"{name}: current_promotion must remain false in this snapshot")

        candidate = domain.get("candidate_definition", {})
        check_path(candidate["prose"], f"{name} candidate prose")
        machine_path = check_path(candidate["machine"], f"{name} candidate machine")
        if git_blob_sha(machine_path) != candidate.get("machine_blob_sha"):
            fail(f"{name}: candidate machine blob binding drift")

        machine = json.loads(machine_path.read_text(encoding="utf-8"))
        if not machine.get("execution_depth_contract"):
            fail(f"{name}: execution_depth_contract missing")
        stages = machine.get("stages", [])
        if not stages:
            fail(f"{name}: no professional stages")
        for stage in stages:
            sid = stage.get("stage_id")
            if not stage.get("required_native_outputs"):
                fail(f"{name}/{sid}: no native outputs")
            if not stage.get("required_readback"):
                fail(f"{name}/{sid}: no readback")
            if not stage.get("reopen_triggers"):
                fail(f"{name}/{sid}: no reopen trigger")
            if not stage.get("does_not_prove"):
                fail(f"{name}/{sid}: no does-not-prove boundary")

        project = domain.get("project_adoption", {})
        if project.get("exists") is not True:
            fail(f"{name}: v0.2 expects a real-project bounded exercise")
        if project.get("project_exercise_counted") is not True:
            fail(f"{name}: project exercise must be counted as bounded adoption evidence")
        receipt = project.get("receipt")
        if not receipt:
            fail(f"{name}: project receipt missing")
        check_path(receipt, f"{name} project receipt")

        if domain.get("independent_professional_review") not in (
            "NOT_RUN",
            "NOT_RUN_FOR_REAL_PROJECT",
        ):
            fail(
                f"{name}: independent professional review unexpectedly closed; "
                "regenerate frontier"
            )

    by = {d["domain"]: d for d in domains}

    interior = by["Interior Design"]
    if interior["domain_native_execution_chain"]["state"] != "NOT_ESTABLISHED":
        fail("Interior native execution state drift")
    if not {"FAIL-057", "FAIL-058"} <= set(interior.get("regression_ids", [])):
        fail("Interior real-project regressions missing")

    lighting = by["Lighting Design"]
    practice = lighting.get("practice_reapplication", {})
    if not practice.get("exists"):
        fail("Lighting synthetic practice evidence missing")
    if practice.get("project_exercise_counted") is not False:
        fail("Lighting synthetic practice may not be counted as project exercise")
    if lighting["domain_native_execution_chain"]["state"] != "NOT_ESTABLISHED":
        fail("Lighting native execution state drift")
    if not {"FAIL-059", "FAIL-060", "FAIL-061"} <= set(
        lighting.get("regression_ids", [])
    ):
        fail("Lighting real-project regressions missing")

    systems = by["Systems Engineering"]["project_adoption"]
    if systems.get("validation_pass") != 0:
        fail("Systems Engineering adoption must not report validation PASS")
    if systems.get("integrated_interfaces_verified") != 0:
        fail("Systems Engineering adoption must not report integrated interface VERIFIED")

    failures_path = ROOT / "evals/failure/failure_cases.jsonl"
    failure_ids = {
        json.loads(line)["case_id"]
        for line in failures_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    required_failures = {
        "FAIL-009", "FAIL-010", "FAIL-011", "FAIL-012",
        "FAIL-013", "FAIL-014", "FAIL-015", "FAIL-016", "FAIL-017",
        "FAIL-018", "FAIL-019",
        "FAIL-023", "FAIL-024", "FAIL-025", "FAIL-026", "FAIL-027",
        "FAIL-028", "FAIL-029", "FAIL-030",
        "FAIL-031", "FAIL-032", "FAIL-033", "FAIL-034", "FAIL-035",
        "FAIL-036", "FAIL-037", "FAIL-038", "FAIL-039", "FAIL-040",
        "FAIL-041", "FAIL-042", "FAIL-043", "FAIL-044",
        "FAIL-057", "FAIL-058", "FAIL-059", "FAIL-060", "FAIL-061",
    }
    missing = sorted(required_failures - failure_ids)
    if missing:
        fail(f"frontier regression bindings missing: {missing}")

    depth = data.get("definition_depth_readback", {})
    if set(depth.get("shared_regression_ids", [])) != {"FAIL-041", "FAIL-042"}:
        fail("definition-depth shared regression binding drift")
    if set(depth.get("domains", {})) != EXPECTED:
        fail("definition-depth domain set drift")
    if not all(
        value.get("execution_depth_contract_present")
        for value in depth["domains"].values()
    ):
        fail("definition-depth readback contains missing execution-depth contract")

    conclusion = data.get("cross_domain_conclusion", {})
    if conclusion.get("definition_granularity") != (
        "MEETS CURRENT EXECUTION-DEPTH FLOOR FOR ALL FIVE CANDIDATE DEFINITIONS"
    ):
        fail("definition granularity conclusion drift")
    if conclusion.get("adoption_granularity") != "NOT CLOSED":
        fail("adoption granularity may not be reported closed in this snapshot")

    print(
        "PASS: v0.2 open-domain adoption frontier is current, "
        "evidence-bound and non-promotional"
    )


if __name__ == "__main__":
    main()
