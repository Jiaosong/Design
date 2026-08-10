# OLEANDER / 织作 — SP04-R05 Rule Coupling & Conflict Test

**Status: ACTUALLY EXECUTED**

Layer: Spatial / SP04 — Construction & Operation.

R05 searches for cases where every R04 single rule passes but the combined parameter request is impossible.

## Coupled variables
Wall thickness, edge ligament, opening gap, corner radius, opening count and a controlled opening width were swept together.

## Objective conflict
For an array of equal openings:
`required_span = 2×edge + count×opening_width + (count−1)×gap`

A case is an **emergent coupled conflict** when:
1. all R04 single rules pass;
2. corner radius fits the opening;
3. but the total requested span exceeds the 6000 mm training host.

## Executed matrix
- Total combinations: 43904
- Single-rule-pass combinations: 30704
- Clean coupled PASS: 22806
- Emergent coupled conflicts: 7898
- Conflict rate within single-rule PASS space: 25.72%

## Representative conflict
- thickness: 40 mm
- edge: 120 mm
- gap: 180 mm
- radius: 12 mm
- count: 8
- opening width: 600 mm
- packing margin: -300 mm
- result: **REFUSE GENERATION**

This is a training rule system, not structural or regulatory approval.
All values are training-only hypothetical parameters.
