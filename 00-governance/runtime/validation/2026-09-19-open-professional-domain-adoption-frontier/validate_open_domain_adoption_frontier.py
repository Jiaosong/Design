#!/usr/bin/env python3
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
MATRIX = HERE / "OPEN_DOMAIN_ADOPTION_FRONTIER_v0.1.json"
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

def check_path(rel: str, label: str) -> None:
    p = ROOT / rel
    if not p.exists():
        fail(f"{label} missing: {rel}")

def main() -> None:
    data = json.loads(MATRIX.read_text(encoding="utf-8"))
    arch = ARCH.read_text(encoding="utf-8")

    domains = data.get("domains", [])
    names = [d.get("domain") for d in domains]
    if set(names) != EXPECTED or len(names) != len(EXPECTED):
        fail(f"domain set drift: {names}")

    for domain, line in OPEN_LINES.items():
        if line not in arch:
            fail(f"{domain} is no longer OPEN as expected by this diagnostic; regenerate frontier before using it")

    for d in domains:
        name = d["domain"]
        if d.get("current_status") != "OPEN":
            fail(f"{name}: matrix must not claim Current/promotion")
        if d.get("professional_pass") is not False:
            fail(f"{name}: professional_pass must remain false in this snapshot")
        if d.get("current_promotion") is not False:
            fail(f"{name}: current_promotion must remain false in this snapshot")

        cand = d.get("candidate_definition", {})
        check_path(cand["prose"], f"{name} candidate prose")
        check_path(cand["machine"], f"{name} candidate machine definition")

        machine = json.loads((ROOT / cand["machine"]).read_text(encoding="utf-8"))
        if not machine.get("execution_depth_contract"):
            fail(f"{name}: execution_depth_contract missing")
        stages = machine.get("stages", [])
        if not stages:
            fail(f"{name}: no professional stages")
        for st in stages:
            if not st.get("required_native_outputs"):
                fail(f"{name}/{st.get('stage_id')}: no native outputs")
            if not st.get("required_readback"):
                fail(f"{name}/{st.get('stage_id')}: no readback")
            if not st.get("reopen_triggers"):
                fail(f"{name}/{st.get('stage_id')}: no reopen trigger")
            if not st.get("does_not_prove"):
                fail(f"{name}/{st.get('stage_id')}: no does-not-prove boundary")

        project = d.get("project_adoption", {})
        if project.get("exists"):
            receipt = project.get("receipt")
            if not receipt:
                fail(f"{name}: project adoption exists but receipt is missing")
            check_path(receipt, f"{name} project adoption receipt")

        practice = d.get("practice_reapplication", {})
        if practice.get("exists"):
            receipt = practice.get("receipt")
            if not receipt:
                fail(f"{name}: practice reapplication exists but receipt is missing")
            check_path(receipt, f"{name} practice receipt")

    by = {d["domain"]: d for d in domains}

    interior = by["Interior Design"]
    if interior["practice_reapplication"]["exists"] or interior["project_adoption"]["exists"]:
        fail("Interior snapshot is usage-empty; regenerate if real evidence is adopted")

    lighting = by["Lighting Design"]
    if not lighting["practice_reapplication"]["exists"]:
        fail("Lighting synthetic practice evidence unexpectedly missing")
    if lighting["practice_reapplication"].get("project_exercise_counted") is not False:
        fail("Lighting synthetic practice may not be counted as project exercise")
    if lighting["project_adoption"]["exists"]:
        fail("Lighting real project adoption now exists; regenerate frontier")

    for name in ("Landscape Architecture", "Digital Product / HCD", "Systems Engineering"):
        if not by[name]["project_adoption"]["exists"]:
            fail(f"{name}: expected bounded project adoption evidence")

    se = by["Systems Engineering"]["project_adoption"]
    if se.get("validation_pass") != 0:
        fail("Systems Engineering adoption must not report validation PASS in this snapshot")
    if se.get("integrated_interfaces_verified") != 0:
        fail("Systems Engineering adoption must not report integrated interface VERIFIED in this snapshot")

    failures_path = ROOT / "evals/failure/failure_cases.jsonl"
    failure_ids = {
        json.loads(line)["case_id"]
        for line in failures_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    for required in ("FAIL-041", "FAIL-042"):
        if required not in failure_ids:
            fail(f"shared professional-parity regression missing: {required}")

    depth = data.get("definition_depth_readback", {})
    if set(depth.get("shared_regression_ids", [])) != {"FAIL-041", "FAIL-042"}:
        fail("definition-depth shared regression binding drift")
    if set(depth.get("domains", {})) != EXPECTED:
        fail("definition-depth domain set drift")
    if not all(v.get("execution_depth_contract_present") for v in depth["domains"].values()):
        fail("definition-depth readback contains missing execution-depth contract")

    print("PASS: open professional-domain adoption frontier is internally consistent")

if __name__ == "__main__":
    main()
