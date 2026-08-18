#!/usr/bin/env python3
import json, sys
from pathlib import Path

PROMOTION={"NO","NO_PROMOTION","CANDIDATE_NOT_PROMOTED"}
MODES={"DISTANCE_READ","NEAR_READ","GRAYSCALE","PRINT_SCALE","MOBILE_CROP"}
RESULTS={"READBACK_COMPLETED","ISSUE_FOUND","HOLD"}
REVIEWER_ROLES={"PRODUCER_SELF_CHECK","INDEPENDENT_REVIEW"}


def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def text(v):
    return isinstance(v,str) and bool(v.strip())


def main():
    if len(sys.argv)!=2:
        fail("usage: validate_actual_preview_review.py PREVIEW_REVIEW.json")
    d=json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if d.get("promotion") not in PROMOTION:
        fail("preview review receipt must remain non-promoted")
    for key in ("review_id","artifact_id","artifact_ref","reviewer_role","review_result","does_not_prove"):
        if key not in d:
            fail(f"missing {key}")
    if not text(d["review_id"]) or not text(d["artifact_id"]) or not text(d["artifact_ref"]):
        fail("review/artifact identifiers must be non-empty")
    if d["reviewer_role"] not in REVIEWER_ROLES:
        fail("invalid reviewer_role")
    if d["review_result"] not in RESULTS:
        fail("invalid review_result; validator never accepts KEEP/PASS as a machine-awarded design state")
    if not isinstance(d["does_not_prove"],list) or not d["does_not_prove"]:
        fail("does_not_prove must be non-empty")

    views=d.get("views")
    if not isinstance(views,list) or not views:
        fail("views required")
    modes=set()
    for v in views:
        for key in ("view_id","mode","preview_ref","opened","observation"):
            if key not in v:
                fail(f"view missing {key}")
        if v["mode"] not in MODES:
            fail(f"{v['view_id']}: invalid mode")
        if v["opened"] is not True:
            fail(f"{v['view_id']}: actual preview must be explicitly recorded as opened")
        if not text(v["preview_ref"]) or not text(v["observation"]):
            fail(f"{v['view_id']}: preview_ref and observation required")
        modes.add(v["mode"])

    for required_mode in ("DISTANCE_READ","NEAR_READ"):
        if required_mode not in modes:
            fail(f"missing required actual-preview mode: {required_mode}")
    if d.get("color_semantic_dependency") is True and "GRAYSCALE" not in modes:
        fail("color-semantic dependency requires GRAYSCALE readback")
    if d["review_result"]=="ISSUE_FOUND" and not text(d.get("root_cause")):
        fail("ISSUE_FOUND requires root_cause")
    if d["review_result"]=="HOLD" and not text(d.get("hold_reason")):
        fail("HOLD requires hold_reason")

    print(f"PASS: actual-preview receipt structurally valid / views={len(views)} / result={d['review_result']}")
    print("NOTE: this proves review evidence was registered, not that the artifact deserves KEEP or Professional Design PASS.")

if __name__=='__main__': main()
