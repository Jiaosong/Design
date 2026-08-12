# Automotive v0.11｜R27 Circumferential Wheel-Arch Topology Gate

Status: `M5 MACHINE PASS / HUMAN VISUAL QA REVISE / R27 CLOSED AS LOCAL-ATTACHMENT SEARCH`

## Objective

R27 tested whether a circumferential wheel-opening system could replace the failed longitudinal-strip approximation while keeping the accepted non-wheel package locked.

## Locked Inputs retained throughout R27

- R09 wheel/cabin hard points
- R11 non-wheel transverse body tension
- R12 longitudinal interpolation logic
- R18/R20 termination topology
- R25 rounded x-z wheel-opening target
- no Source Boolean
- no global SubD
- no n-gon concealment
- M6/M7/M8 blocked

## Executed revision chain

### R27A｜Circumferential Nested Rings

`SHARED SHOULDER TRANSITION → BLEND1 → BLEND2 → INNER OPENING`

- 24 angle samples;
- one connected editable Source mesh;
- Machine M5 PASS;
- Human M5 REVISE: intermediate rings overshot the shared shoulder transition and read as a floating wheel-brow / bridge.

### R27B｜Monotonic Radial Bridge

- R27 topology retained;
- z/y ordering forced monotonic from shoulder transition to inner opening;
- Machine M5 PASS;
- Human M5 REVISE with material improvement: floating bridge suppressed, but hard fore/aft wheel-zone exits remained.

### R27C｜Tangential Radial Fan

- R27B z/y ordering retained;
- nested x-radii contracted through the arch and reconverged to shared endpoints;
- Machine M5 PASS;
- Human M5 REVISE: common attachment stations still produced hard vertical/diagonal exit reading.

### R27D｜Staggered Ring Attachments

- row4/5/6/7 assigned distinct longitudinal attachment stations;
- 24 explicit wheel-zone transition triangles + 4 historical termination triangles;
- Machine M5 PASS;
- first evidence exposed deterministic face-normal artifacts; normals were recalculated without changing geometry;
- orientation-fixed Human M5 REVISE: black slits closed, but the transition triangles remained visibly toothed in arch detail / grazing views.

### R27E｜Quad Attachment Collar

- staggered attachment stations retained;
- all 24 wheel-zone transition triangles replaced by 24 quad collars;
- full Source normals recalculated;
- Machine M5 PASS;
- topology evidence: one Source island, 4 triangles total, 3049 quads, 0 n-gons;
- Human M5 REVISE: tooth-like silhouette artifacts reduced, but the same attachment zone now produces radial highlight pinching / curvature teeth. The failure survives the triangle-to-quad change.

## R27 decision

**Retain the circumferential wheel-opening principle. Reject the premise that it can be solved by attaching a new ring system directly into the existing row4–row7 local cage.**

The accumulated evidence classifies the remaining defect as a broader **local fender patch architecture** problem:

`wheel opening + fender crown + shoulder + mid-body + rocker transition`

must be reconstructed as one local Primary patch rather than treating the wheel arch as an insert attached to an otherwise fixed lower body cage.

## Required next gate

`R28｜Local Fender Patch Architecture`

Required:
1. retain R09 hard points and R25 wheel-opening proportion target;
2. keep R11/R12 non-wheel body source locked outside a controlled local influence window;
3. reopen shoulder-to-rocker topology inside that local window;
4. construct wheel opening, fender crown and body transition in one patch topology rather than ring + attachment cells;
5. preserve one editable Source authority;
6. no Boolean / global SubD / n-gon concealment;
7. repeat the same 9-view M5 evidence matrix;
8. M6/M7/M8 remain blocked until Human M5 PASS.
