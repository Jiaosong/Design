#!/usr/bin/env python3
from __future__ import annotations
import json, math, sys
from pathlib import Path
SCHEMA='oleander.3d.surface-fold-diagnostic.v1'
def req(c,m):
    if not c: raise ValueError(m)
def validate(d):
    for k in ('schema','candidate_revision','fold_count','folds','authority'): req(k in d,f'missing:{k}')
    req(d['schema']==SCHEMA,'bad:schema'); req(d['authority']=='DIAGNOSTIC_NOT_REFERENCE_AUTHORITY','bad:authority')
    req(isinstance(d['folds'],list),'bad:folds'); req(int(d['fold_count'])==len(d['folds']),'bad:fold_count')
    for i,f in enumerate(d['folds']):
        for k in ('edge_vertices','face_indices','normal_dot','center_m'): req(k in f,f'missing:fold[{i}].{k}')
        req(isinstance(f['edge_vertices'],list) and len(f['edge_vertices'])==2,f'bad:edge[{i}]')
        req(isinstance(f['face_indices'],list) and len(f['face_indices'])==2,f'bad:faces[{i}]')
        dot=float(f['normal_dot']); req(math.isfinite(dot) and dot<-.15,f'bad:normal_dot[{i}]')
        c=f['center_m']; req(isinstance(c,list) and len(c)==3 and all(math.isfinite(float(x)) for x in c),f'bad:center[{i}]')
    return d
def main():
    if len(sys.argv)!=2: print('usage: validate_surface_fold_diagnostic.py DIAGNOSTIC.json',file=sys.stderr);return 2
    try: validate(json.loads(Path(sys.argv[1]).read_text()))
    except Exception as e: print(f'SURFACE FOLD DIAGNOSTIC INVALID: {e}',file=sys.stderr);return 1
    print('SURFACE FOLD DIAGNOSTIC VALID');return 0
if __name__=='__main__':raise SystemExit(main())