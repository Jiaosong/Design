# Automotive v0.11｜R29A Human M5 Decision

Status: `M5 PASS / WORKING SOURCE CANDIDATE / M6 MAY OPEN / NOT CANONICAL PROMOTION YET`

## Scope

This PASS applies to the OLEANDER Modeling Worker automotive primary-geometry benchmark. It is a modeling/surface-construction gate, not Class-A surfacing, engineering CAD, aerodynamic validation, manufacturing validation or homologation.

## Machine evidence

Canonical run: `31619362019`

Artifact: `9150618297` / `oleander-automotive-v0-11-r29a-31619362019`

Digest: `sha256:5fd16c8c38eb32a03c182bd86b0e11c558076536b17654eabe2cb79cecef9df0`

Machine gate passed with:
- one connected Source island;
- 2909 vertices / 2793 faces;
- 4 controlled termination triangles / 2789 quads / 0 n-gons;
- no Source Boolean or global SubD;
- 24 shared R25 endpoint reuses;
- exact canonical wheel hard-point package at 0.700 m OD via `wheel_hp_contract.py`;
- R25 rounded wheel-opening scale retained;
- shoulder-fed crown active;
- bounded crown influence;
- monotonic target relation `SHOULDER_CROWN > B1 > B2 > INNER_OPENING`;
- complete 9-view M5 evidence matrix.

Source hash for this executed candidate:
`d19224d2e33485ed5f6e333c5996133a07fd686cd4333caf28c37a83b7e552fb`

## Human M5 comparison

R29A was reviewed against both the HP-correct R25 baseline and R29 under the same corrected wheel package.

### PASS — Side / Package
- wheel/body scale remains coherent after the 0.700 m HP correction;
- front and rear openings retain the accepted rounded R25 target;
- crown growth does not create a new silhouette discontinuity severe enough to reopen M2/M3.

### PASS — Hero Front / Rear
- R29 shelf-like upper arch is materially removed;
- R25 isolated cap-like crown does not return;
- front/rear fender volume now reads as generated from the shoulder/body volume rather than attached as an independent brow.

### PASS — Strip / Grazing
- no R28-style radial corrugation or repeated tooth pattern;
- no R29 planar shelf remains as the dominant highlight event;
- broad surface flow remains materially cleaner than the rejected R27/R28 families.

### PASS — Arch Detail
- front upper arch is continuous enough for the current M5 benchmark;
- rear crown/opening transition is continuous enough for the current M5 benchmark;
- corrected near-side wheel no longer drives false penetration conclusions;
- no detached patch, black Source tear or obvious self-overlap remains.

### PASS — Source Wireframe
- R25 shared-endpoint Source topology family remains recognizable and editable;
- no hidden Boolean/SubD repair path was introduced;
- the wheel-zone correction remains bounded rather than turning into another full local patch architecture.

## Retained / superseded authority

Retained:
- R09 package/hard points;
- R11 non-wheel transverse tension;
- R12 longitudinal interpolation;
- R18/R20 terminations;
- R25 rounded opening scale and shared-endpoint topology family;
- canonical `wheel_hp_contract.py`;
- R29A shoulder-fed crown relation.

Superseded as Source authority, retained for audit:
- R27A-E circumferential attachment experiments;
- R28A-C full local patch family;
- R29 inward-rising shelf relation.

R30 draft was never executed or authoritative and is removed as a duplicate of the already implemented R29A direction.

## Gate transition

`M5 PASS → M6 COMPONENT ARCHITECTURE MAY OPEN`

M6 may establish semantic component boundaries and dependency IDs without changing the validated R29A primary surface.

M7 Secondary Geometry and M8 Detail/Instances remain blocked until M6 is reviewed.

No Notion/Drive canonical promotion and no PR merge are authorized by this decision alone.
