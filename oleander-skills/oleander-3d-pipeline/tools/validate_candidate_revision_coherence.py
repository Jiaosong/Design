#!/usr/bin/env python3
"""Validate that one artifact set names one candidate revision across machine receipts."""
from __future__ import annotations
import json,sys
from pathlib import Path

def req(c,m):
    if not c:raise ValueError(m)

def validate_bundle(base:Path):
    qa=json.loads((base/'REFERENCE_REPRO_QA.json').read_text())
    pr=json.loads((base/'REFERENCE_PROJECTION_RECEIPT.json').read_text())
    rg=json.loads((base/'REFERENCE_REGRESSION_PROMOTION_RECEIPT.json').read_text())
    sf=json.loads((base/'PRIMARY_BODY_SURFACE_RECEIPT.json').read_text())
    vals={
      'qa':qa.get('reference_fidelity_revision'),
      'projection':pr.get('candidate_revision'),
      'regression':rg.get('candidate_revision'),
      'surface':sf.get('revision')}
    for k,v in vals.items():req(isinstance(v,str) and v,f'missing_revision:{k}')
    target=vals['projection']
    req(all(v==target for v in vals.values()),f'candidate_revision_mismatch:{vals}')
    return vals

def main():
    if len(sys.argv)!=2:
        print('usage: validate_candidate_revision_coherence.py ARTIFACT_DIR',file=sys.stderr);return 2
    try:vals=validate_bundle(Path(sys.argv[1]))
    except Exception as e:
        print(f'CANDIDATE REVISION COHERENCE FAIL: {e}',file=sys.stderr);return 1
    print('CANDIDATE REVISION COHERENCE PASS',vals['projection']);return 0
if __name__=='__main__':raise SystemExit(main())
