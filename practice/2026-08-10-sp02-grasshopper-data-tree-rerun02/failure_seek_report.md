# Failure-seeking Report｜SP02 Rerun 02

## NOMINAL
- Base: 4 branches / 24 items / [6,6,6,6]
- Graft: 24 branches / 24 items / 1 each
- Flatten: 1 branch / 24 items
- Transpose: 6 branches / 24 items / [4,4,4,4,4,4]
- Status: `OFFLINE STRUCTURE PASS`

## REPEATABILITY
- Run 1 SHA256: `baf831e6a8b70201d5020ce764ad5c89818e1c2daba63fbfa5f938ea0a6bb3a9`
- Run 2 SHA256: `baf831e6a8b70201d5020ce764ad5c89818e1c2daba63fbfa5f938ea0a6bb3a9`
- Exact match: `True`
- Meaning: proves deterministic offline specification only, not Grasshopper runtime equivalence.

## ADVERSE
- Zone 2 intentionally reduced to 5 items.
- Transpose items per branch: `[4,4,4,4,4,3]`.
- Expected failure: branch `{5}` has 3 items.
- Decision: `EXPECTED MISMATCH DETECTED`; do not Flatten to hide it.

## FAILURE-SEEKING
- Empty branch: `{1}`.
- One null item in `{3}`.
- Item slots including null: 18.
- Decision: `SIM-FAIL / REWORK REQUIRED`.

## Runtime boundary
- Rhino / Grasshopper desktop: NOT EXECUTED.
- FREE_PUBLIC_COMPUTE: provider preflight only; public service disabled.
- CP2: OPEN.
- CP4: OPEN.
