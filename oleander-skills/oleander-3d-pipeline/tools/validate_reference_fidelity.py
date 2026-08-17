#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path
HERE=Path(__file__).resolve()
CONTRACT=HERE.parents[1]/"contracts"/"REFERENCE_REPRODUCTION_FIDELITY_CONTRACT_v1.json"
def fail(code,detail): raise SystemExit(f"{code}: {detail}")
def validate(data,contract):
 ref=data.get("reference_lock") or {}
 for key in contract["required_reference_fields"]:
  if key not in ref or ref[key] in (None,"",[]): fail("FAIL_REFERENCE_REVISION_MIXED",f"missing reference_lock.{key}")
 if ref["dimension_revision"]!=ref["visual_revision"]: fail("FAIL_REFERENCE_REVISION_MIXED","dimension_revision != visual_revision")
 counts={k:0 for k in contract["view_minimum"]}
 for v in data.get("views",[]):
  role=v.get("role")
  if role in counts: counts[role]+=1
 for role,minimum in contract["view_minimum"].items():
  if counts[role]<minimum: fail("INSUFFICIENT_REFERENCE_VIEW_COVERAGE",f"{role}={counts[role]} < {minimum}")
 hard=data.get("hard_points") or []
 if not hard: fail("FAIL_HARD_POINT_CONTRACT","hard_points missing")
 th=contract["thresholds"]
 for h in hard:
  if h.get("authority")=="OFFICIAL":
   err=abs(float(h["candidate"])-float(h["target"]))/max(abs(float(h["target"])),1e-12)
   if err>th["official_hard_point_relative_error_max"]: fail("FAIL_HARD_POINT_CONTRACT",f"{h.get('id')} relative error {err}")
 landmarks={x.get("id"):x for x in data.get("landmarks",[])}
 for lid in contract["required_landmarks"]:
  if lid not in landmarks: fail("FAIL_REFERENCE_LANDMARK_ERROR",f"missing landmark {lid}")
 for lid,item in landmarks.items():
  err=float(item.get("normalized_error",1e9))
  limit=th["critical_landmark_normalized_error_max"] if item.get("critical",False) else (th["identity_landmark_normalized_error_max"] if item.get("class")=="IDENTITY" else th["primary_landmark_normalized_error_max"])
  if err>limit: fail("FAIL_REFERENCE_LANDMARK_ERROR",f"{lid} normalized error {err} > {limit}")
 if data.get("source_digest_before")!=data.get("source_digest_after"): fail("FAIL_MULTI_VIEW_FIDELITY","Source digest changed across fidelity views")
 if data.get("per_view_geometry_override",False): fail("FAIL_MULTI_VIEW_FIDELITY","per-view geometry override forbidden")
 if data.get("silhouette_gate")!="PASS": fail("REVISE_PRIMARY_SILHOUETTE","silhouette gate not PASS")
 if data.get("reference_fidelity_gate")!="PASS": fail("FAIL_MULTI_VIEW_FIDELITY","reference fidelity gate not PASS")
 if data.get("design_quality_gate")=="PASS" and not data.get("independent_reference_review",False): fail("FAIL_MULTI_VIEW_FIDELITY","Design PASS requires independent reference review")
def main():
 ap=argparse.ArgumentParser();ap.add_argument("receipt");args=ap.parse_args()
 validate(json.loads(Path(args.receipt).read_text()),json.loads(CONTRACT.read_text()))
 print("REFERENCE FIDELITY RECEIPT PASS")
if __name__=="__main__": main()
