#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRACE = ROOT / "C04_SYSENG_REQUIREMENT_TRACE_VV_v0.1.json"
INSTANCE = ROOT / "C04_SYSENG_PROCESS_INSTANCE_v0.1.json"

ALLOWED_RESULTS = {"PASS","FAIL","HOLD","NOT_RUN","UNVERIFIED","NOT_APPLICABLE"}
EXPECTED_STAGES = [f"SYSENG-DP{i}" for i in range(9)]

def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

def main() -> None:
    trace = json.loads(TRACE.read_text(encoding="utf-8"))
    inst = json.loads(INSTANCE.read_text(encoding="utf-8"))

    if trace.get("professional_disposition") != "HOLD":
        fail("trace professional_disposition must remain HOLD")
    if inst.get("professional_verdict") != "HOLD":
        fail("process instance professional_verdict must remain HOLD")
    if inst.get("execution_state") != "BLOCKED":
        fail("process instance execution_state must remain BLOCKED")

    reqs = trace.get("requirements", [])
    if len(reqs) != 6:
        fail(f"expected 6 bounded requirements, got {len(reqs)}")

    ids = [r.get("requirement_id") for r in reqs]
    if len(ids) != len(set(ids)):
        fail("duplicate requirement_id")

    required_req_fields = {
        "requirement_id","source_need_goal","atomic_requirement","rationale","priority",
        "acceptance_failure_condition","allocation","verification","validation","status","reopen_trigger"
    }
    for r in reqs:
        missing = sorted(required_req_fields - set(r))
        if missing:
            fail(f"{r.get('requirement_id')} missing fields {missing}")
        for kind in ("verification","validation"):
            obj = r[kind]
            if obj.get("result") not in ALLOWED_RESULTS:
                fail(f"{r['requirement_id']} invalid {kind} result {obj.get('result')}")
        af = r["acceptance_failure_condition"]
        if not af.get("pass") or not af.get("fail"):
            fail(f"{r['requirement_id']} missing pass/fail condition")
        if not r["allocation"].get("architecture_elements"):
            fail(f"{r['requirement_id']} missing architecture allocation")

    summary = trace.get("coverage_summary", {})
    calc = {
        "requirements_total": len(reqs),
        "verification_pass": sum(r["verification"]["result"] == "PASS" for r in reqs),
        "verification_hold": sum(r["verification"]["result"] == "HOLD" for r in reqs),
        "validation_pass": sum(r["validation"]["result"] == "PASS" for r in reqs),
        "validation_not_run": sum(r["validation"]["result"] == "NOT_RUN" for r in reqs),
        "validation_not_applicable": sum(r["validation"]["result"] == "NOT_APPLICABLE" for r in reqs),
    }
    for key, value in calc.items():
        if summary.get(key) != value:
            fail(f"coverage_summary drift for {key}: expected {value}, got {summary.get(key)}")
    if summary.get("validation_pass") != 0:
        fail("bounded exercise must not claim validation PASS")

    interfaces = trace.get("interface_verification", [])
    interface_ids = [x.get("interface_id") for x in interfaces]
    if len(interface_ids) != len(set(interface_ids)):
        fail("duplicate interface_id")
    if not interface_ids:
        fail("no interface verification records")

    stage_ids = [s.get("stage_id") for s in inst.get("stage_instances", [])]
    if stage_ids != EXPECTED_STAGES:
        fail(f"stage sequence mismatch: {stage_ids}")

    for s in inst["stage_instances"]:
        unknown = sorted(set(s.get("interface_refs", [])) - set(interface_ids))
        if unknown:
            fail(f"{s['stage_id']} references unknown interfaces {unknown}")
        if s.get("review_verdict") == "PASS":
            fail(f"{s['stage_id']} may not claim PASS in this candidate adoption exercise")

    dp7 = next(s for s in inst["stage_instances"] if s["stage_id"] == "SYSENG-DP7")
    if dp7.get("execution_state") != "BLOCKED" or dp7.get("review_verdict") != "HOLD":
        fail("SYSENG-DP7 must remain BLOCKED/HOLD")

    dp8 = next(s for s in inst["stage_instances"] if s["stage_id"] == "SYSENG-DP8")
    if dp8.get("execution_state") != "NOT_STARTED" or dp8.get("review_verdict") != "NOT_RUN":
        fail("SYSENG-DP8 must remain NOT_STARTED/NOT_RUN")

    change = trace.get("configuration_change_reopen", {})
    affected = set(change.get("affected_requirements", []))
    if not affected:
        fail("change/reopen record has no affected requirements")
    unknown_req = sorted(affected - set(ids))
    if unknown_req:
        fail(f"change record references unknown requirements {unknown_req}")
    if "C04-SYSREQ-006" not in affected:
        fail("runtime-affecting configuration change must reopen SYSREQ-006")

    by_if = {x["interface_id"]: x for x in interfaces}
    if by_if.get("IF-BROWSER-RUNTIME", {}).get("state") != "BLOCKED":
        fail("browser runtime interface must remain BLOCKED")
    if by_if.get("IF-HCD-VALIDATION", {}).get("state") != "NOT_RUN":
        fail("HCD validation interface must remain NOT_RUN")

    print("PASS: C04 Systems Engineering trace/process consistency")

if __name__ == "__main__":
    main()
