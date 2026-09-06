#!/usr/bin/env python3
"""R03 dual-coder reliability calculator. No external dependencies."""
import csv, sys
from collections import Counter

def read(path):
    rows = {}
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or "record_id" not in reader.fieldnames:
            raise SystemExit(f"{path}: missing required record_id column.")
        for line_no, row in enumerate(reader, start=2):
            record_id = (row.get("record_id") or "").strip()
            if not record_id:
                raise SystemExit(f"{path}:{line_no}: blank record_id.")
            if record_id in rows:
                raise SystemExit(f"{path}:{line_no}: duplicate record_id {record_id!r}.")
            rows[record_id] = row
    return rows

def exact(a,b):
    return sum(x==y for x,y in zip(a,b))/len(a) if a else float("nan")

def cohen_kappa(a,b):
    n=len(a)
    if not n: return float("nan")
    cats=sorted(set(a)|set(b))
    if len(cats)<2: return None
    po=sum(x==y for x,y in zip(a,b))/n
    ca,cb=Counter(a),Counter(b)
    pe=sum((ca[c]/n)*(cb[c]/n) for c in cats)
    if abs(1-pe)<1e-12: return None
    return (po-pe)/(1-pe)

def weighted_kappa(a,b):
    if not a: return float("nan")
    vals=sorted(set(a)|set(b))
    if len(vals)<2: return None
    lo,hi=min(vals),max(vals)
    cats=list(range(lo,hi+1)); idx={c:i for i,c in enumerate(cats)}; k=len(cats); n=len(a)
    O=[[0.0]*k for _ in range(k)]; ra=[0]*k; cb=[0]*k
    for x,y in zip(a,b):
        i,j=idx[x],idx[y]; O[i][j]+=1; ra[i]+=1; cb[j]+=1
    E=[[ra[i]*cb[j]/n for j in range(k)] for i in range(k)]
    denom=(k-1)**2
    W=[[((i-j)**2)/denom for j in range(k)] for i in range(k)]
    num=sum(W[i][j]*O[i][j] for i in range(k) for j in range(k))
    den=sum(W[i][j]*E[i][j] for i in range(k) for j in range(k))
    return None if abs(den)<1e-12 else 1-num/den

def report(name,a,b,total,ordinal=False):
    ex=exact(a,b)
    kap=weighted_kappa([int(x) for x in a],[int(y) for y in b]) if ordinal else cohen_kappa(a,b)
    ktxt="NON_ESTIMABLE" if kap is None else f"{kap:.3f}"
    print(f"{name}: coverage={len(a)}/{total} exact={ex:.3f} kappa={ktxt}")

if len(sys.argv)!=3:
    raise SystemExit("Usage: python R03-reliability-calculator.py coderA.csv coderB.csv")

A,B=read(sys.argv[1]),read(sys.argv[2])
only_a=sorted(set(A)-set(B)); only_b=sorted(set(B)-set(A))
if only_a or only_b:
    raise SystemExit(f"record_id set mismatch: only_A={only_a} only_B={only_b}")
ids=sorted(A)
if not ids:
    raise SystemExit("No record_id values.")

for d in [f"SRE-D{i}" for i in range(1,9)]:
    pairs=[i for i in ids if A[i].get(d+"_status") and B[i].get(d+"_status")]
    report(d+" status",[A[i][d+"_status"] for i in pairs],[B[i][d+"_status"] for i in pairs],len(ids),False)
    pairs=[i for i in ids if A[i].get(d+"_depth","").isdigit() and B[i].get(d+"_depth","").isdigit()]
    report(d+" depth",[A[i][d+"_depth"] for i in pairs],[B[i][d+"_depth"] for i in pairs],len(ids),True)
for p in ["PLS-L","PLS-S","PLS-R","PLS-C"]:
    pairs=[i for i in ids if A[i].get(p,"").isdigit() and B[i].get(p,"").isdigit()]
    report(p,[A[i][p] for i in pairs],[B[i][p] for i in pairs],len(ids),True)
