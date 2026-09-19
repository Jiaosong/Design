#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TRACE = ROOT / "C04_SYSENG_REQUIREMENT_TRACE_VV_v0.2.json"
INSTANCE = ROOT / "C04_SYSENG_PROCESS_INSTANCE_v0.2.json"

ALLOWED_RESULTS = {"PASS","FAIL","HOLD","NOT_RUN","UNVERIFIED","NOT_APPLICABLE"}
EXPECTED_STAGES = [f"SYSENG-DP{i}" for i in range(9)]
EXPECTED_BROWSER_STATE = "VERIFIED_FOR_CONFIGURED_CHROMIUM_DESKTOP_AND_MOBILE"

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

    if summary.get("verification_pass") != 5 or summary.get("verification_hold") != 1:
        fail("v0.2 must preserve 5 verification PASS / 1 HOLD")
    if summary.get("validation_pass") != 0:
        fail("runtime verification must not create validation PASS")
    if summary.get("integrated_interfaces_verified") != 1:
        fail("v0.2 must contain exactly one verified integrated interface")
    if summary.get("integrated_interfaces_open_or_hold") != 3:
        fail("v0.2 must preserve three open/hold interfaces")

    req6 = next((r for r in reqs if r["requirement_id"] == "C04-SYSREQ-006"), None)
    if not req6:
        fail("missing C04-SYSREQ-006")
    if req6["verification"].get("result") != "PASS":
        fail("C04-SYSREQ-006 configured browser verification must PASS")
    config = str(req6["verification"].get("configuration", ""))
    if "Chromium 151.0.7922.34" not in config or "desktop 1440x1000 + mobile 390x844" not in config:
        fail("C04-SYSREQ-006 verification configuration drift")
    if req6["validation"].get("result") != "NOT_RUN":
        fail("C04-SYSREQ-006 user validation must remain NOT_RUN")

    interfaces = trace.get("interface_verification", [])
    interface_ids = [x.get("interface_id") for x in interfaces]
    if len(interface_ids) != len(set(interface_ids)):
        fail("duplicate interface_id")
    if not interface_ids:
        fail("no interface verification records")

    by_if = {x["interface_id"]: x for x in interfaces}
    if by_if.get("IF-BROWSER-RUNTIME", {}).get("state") != EXPECTED_BROWSER_STATE:
        fail("browser runtime interface must be verified only for configured Chromium desktop/mobile")
    if by_if.get("IF-HCD-VALIDATION", {}).get("state") != "NOT_RUN":
        fail("HCD validation interface must remain NOT_RUN")
    if by_if.get("IF-DIGITAL-FALLBACK", {}).get("state") != "DEFINED / NOT_FIELD_VERIFIED":
        fail("digital fallback interface must remain NOT_FIELD_VERIFIED")
    if by_if.get("IF-STATUS-OFFICIAL", {}).get("state") != "NOT_IMPLEMENTED / HOLD":
        fail("official status interface must remain NOT_IMPLEMENTED / HOLD")

    stage_ids = [s.get("stage_id") for s in inst.get("stage_instances", [])]
    if stage_ids != EXPECTED_STAGES:
        fail(f"stage sequence mismatch: {stage_ids}")

    for s in inst["stage_instances"]:
        unknown = sorted(set(s.get("interface_refs", [])) - set(interface_ids))
        if unknown:
            fail(f"{s['stage_id']} references unknown interfaces {unknown}")
        if s.get("review_verdict") == "PASS":
            fail(f"{s['stage_id']} may not claim professional PASS in this candidate adoption exercise")

    dp7 = next(s for s in inst["stage_instances"] if s["stage_id"] == "SYSENG-DP7")
    if dp7.get("execution_state") != "BLOCKED" or dp7.get("review_verdict") != "HOLD":
        fail("SYSENG-DP7 must remain BLOCKED/HOLD after runtime verification")

    dp8 = next(s for s in inst["stage_instances"] if s["stage_id"] == "SYSENG-DP8")
    if dp8.get("execution_state") != "NOT_STARTED" or dp8.get("review_verdict") != "NOT_RUN":
        fail("SYSENG-DP8 must remain NOT_STARTED/NOT_RUN")

    change = trace.get("configuration_change_reopen", {})
    if change.get("change_id") != "C04-APP-CHANGE-V1_2-TO-V1_3":
        fail("latest configuration change must be v1.2→v1.3")
    affected = set(change.get("affected_requirements", []))
    if not {"C04-SYSREQ-002","C04-SYSREQ-005","C04-SYSREQ-006"}.issubset(affected):
        fail("v1.2→v1.3 change must reopen SYSREQ-002/005/006")
    if "C04-SYSREQ-006" not in affected:
        fail("runtime-affecting change must reopen SYSREQ-006")

    history = trace.get("configuration_change_history", [])
    if not history or history[0].get("change_id") != "C04-APP-CHANGE-V1-TO-V1_2":
        fail("v0.2 must preserve predecessor v1→v1.2 change history")

    print("PASS: C04 Systems Engineering v0.2 configured-runtime trace/process consistency")

if __name__ == "__main__":
    main()
