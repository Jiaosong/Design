#!/usr/bin/env python3
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
INSTANCE = HERE / "C01_INTERIOR_PROCESS_INSTANCE_v0.1.json"
READBACK = HERE / "C01_INTERIOR_REMOTE_PROXY_READBACK_v0.1.json"
REGISTER = HERE / "C01_INTERIOR_EXISTING_CONDITION_PROXY_REGISTER_v0.1.csv"
SVG = HERE / "C01_INTERIOR_DAGONGHALL_SPATIAL_ENVELOPE_v0.1.svg"

def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")

def main() -> None:
    inst = json.loads(INSTANCE.read_text(encoding="utf-8"))
    rb = json.loads(READBACK.read_text(encoding="utf-8"))

    if inst.get("professional_verdict") != "HOLD" or inst.get("execution_state") != "BLOCKED":
        fail("Interior project instance must remain BLOCKED/HOLD")
    if "NO PROFESSIONAL PASS" not in inst.get("claim_ceiling", ""):
        fail("Interior project claim ceiling lost NO PROFESSIONAL PASS")

    expected = {
        "ID-PW0": ("CURRENT", "HOLD"),
        "ID-PW1": ("CURRENT", "HOLD"),
        "ID-PW2": ("CURRENT", "HOLD"),
        "ID-PW3": ("BLOCKED", "HOLD"),
        "ID-PW4": ("BLOCKED", "HOLD"),
        "ID-PW5": ("NOT_STARTED", "NOT_RUN"),
        "ID-PW6": ("NOT_STARTED", "NOT_RUN"),
        "ID-PW7": ("NOT_STARTED", "NOT_RUN"),
    }
    stages = {s["stage_id"]: s for s in inst.get("stage_instances", [])}
    if set(stages) != set(expected):
        fail(f"stage set drift: {sorted(stages)}")
    for sid, (execution, verdict) in expected.items():
        s = stages[sid]
        if (s.get("execution_state"), s.get("review_verdict")) != (execution, verdict):
            fail(f"{sid} expected {execution}/{verdict}, got {s.get('execution_state')}/{s.get('review_verdict')}")
        if s.get("review_verdict") == "PASS":
            fail(f"{sid} may not claim PASS")
        if execution in {"BLOCKED", "NOT_STARTED"} and not s.get("open_items"):
            fail(f"{sid} must preserve explicit open items")

    if rb.get("state") != "BOUNDED PROJECT EXERCISE / CONCEPT PROXY ONLY / SPATIAL COORDINATION HOLD / NO PROMOTION":
        fail("remote-proxy readback state drift")
    ceiling = rb.get("claim_ceiling", "")
    for token in ("NO SPATIAL COORDINATION", "NO TECHNICAL DESIGN", "NO FIRE-ACCESSIBILITY-MEP PASS", "NO PROMOTION"):
        if token not in ceiling:
            fail(f"readback claim ceiling missing {token}")

    proxies = rb.get("existing_condition_proxy_register", [])
    if len(proxies) != 10:
        fail(f"expected 10 readback proxy variables, got {len(proxies)}")
    proxy_ids = [p.get("variable_id") for p in proxies]
    if proxy_ids != [f"INT-PV-{i:02d}" for i in range(1, 11)]:
        fail(f"proxy id/order drift: {proxy_ids}")

    with REGISTER.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) != 10:
        fail(f"expected 10 CSV proxy variables, got {len(rows)}")
    if [r["variable_id"] for r in rows] != proxy_ids:
        fail("CSV/readback proxy ID mismatch")

    by_id = {r["variable_id"]: r for r in rows}
    required_unknown = {
        "INT-PV-08": ("RCP_services", "UNKNOWN", "NOT_EVIDENCED"),
        "INT-PV-09": ("floor_threshold_accessibility", "UNKNOWN", "NOT_EVIDENCED"),
        "INT-PV-10": ("fire_egress_capacity", "UNKNOWN", "NOT_EVIDENCED"),
    }
    for vid, (obj, value, evidence) in required_unknown.items():
        r = by_id[vid]
        if r["object_or_relation"] != obj or r["current_value_or_state"] != value or r["evidence_class"] != evidence:
            fail(f"{vid} must remain {obj} / {value} / {evidence}")
        if not r["replacement_evidence"]:
            fail(f"{vid} missing replacement evidence")

    for r in rows:
        if not r["allowed_use"] or not r["forbidden_use"] or not r["replacement_evidence"]:
            fail(f"{r['variable_id']} must preserve allowed/forbidden/replacement fields")

    if "20–30 people remains a design hypothesis" not in READBACK.read_text(encoding="utf-8"):
        fail("capacity hypothesis boundary missing from readback")

    svg = SVG.read_text(encoding="utf-8")
    if "<svg" not in svg or "PROXY" not in svg.upper():
        fail("editable spatial-envelope SVG must remain explicitly proxy-labelled")

    if stages["ID-PW3"].get("actual_readback_refs"):
        fail("ID-PW3 may not claim actual coordination readback while blocked")
    if stages["ID-PW4"].get("actual_readback_refs"):
        fail("ID-PW4 may not claim technical readback while blocked")

    print("PASS: C01 Interior remote/proxy project exercise remains bounded and internally consistent")

if __name__ == "__main__":
    main()
