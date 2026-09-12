# C04 ROUTE CURRENT Lock｜2026-08-17

Project: `PRJ-C04-QINGJIANG-SHISHU`
Case: `C04`
Decision owner: user explicit correction in active conversation
State: `ROUTE-03 LOCKED CURRENT / DOWNSTREAM REFERENCE`

## LOCKED CURRENT object

### ROUTE
- object: `ROUTE-03`
- artifact: `ROUTE_03_QINGJIANG_ROUTE_CURRENTIZED`
- source topology: user-provided `qingjiang_route_guide_translated.svg`
- package bytes: `806723`
- package SHA-256: `977307610d1908c3951535b57222355c39fe262f0f2e3da68d803055a882aabb`
- Drive locked package ID: `1VDfnbuCG-dKRyRZKg2MKhjvljI4CYzIy`

## Not locked

### JOURNEY MODES
- `JOURNEY-04` is **NOT LOCKED**.
- It remains a working candidate / provenance artifact only.
- It must not be propagated as CURRENT because of the previous mistaken lock sync.

## Superseded / provenance only
- `ROUTE-01`
- `ROUTE-02`
- `JOURNEY-01`
- `JOURNEY-02`
- `JOURNEY-03`
- `JOURNEY-04` remains unlocked candidate/provenance unless explicitly locked later.

## Lock semantics
`LOCKED CURRENT` applies to `ROUTE-03` only and means downstream Route references should use this object revision.

It does **not** imply or self-award:
- `PIXEL KEEP`
- `MAIN KEEP`
- `PROFESSIONAL FINISH PASS`
- `FIELD PASS`
- project promotion

Independent design verdict remains a separate gate.

## Truth boundary
- relationship/topology guide, not survey geometry;
- no precise distance, slope, travel time, GPS or real-time operating-status claim;
- `FIELD OBSERVED=0`;
- `FIELD MEASURED=0`;
- `G1F HOLD`;
- `NO_PROMOTION`;
- `NTS / NOT FOR CONSTRUCTION`.

## Downstream rule
Until an explicit later authority decision supersedes this lock, use:

`ROUTE-03`

as the single CURRENT Route object for C04 downstream integration.

`JOURNEY-04` is not locked.
