# C04 / C22 v3.3 — Analysis Drawing Rebuild + QA

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Current delta: `DRW-C04-C22-01` + `DRW-C04-C22-05`  
Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`

## 0. Why v3.3 exists

v3.2 correctly repaired source-authority drift, but the analysis still depended too much on explanatory prose and did not yet make the main spatial relations carry enough of the reading by themselves.

v3.3 changes the drawing logic, not the project concept:

- keep the rebound C22 v3.0 relation carriers;
- enlarge the dominant spatial field and narrow the annotation rail;
- make `route / branch field / content-node / Return` roles visually distinct;
- make SEC-A transport and SEC-C body/compression/return relations visible in geometry rather than only in labels;
- keep R06 frozen and subordinate;
- keep evidence / finding / consequence / FIELD OPEN states explicit.

Closest calibration Skill remains `oleander-technical-drawing` PR #172. It is still draft/candidate and is used only as a gap detector; C04 Current Authority governs.

## 1. DRW-C04-C22-01 — Journey / Route Analysis

### Primary claim

`ARRIVAL / SERVICE → CABLE → MULTI-BRANCH WALKING FIELD → RETURN`

R01–R13 remain optional content identities on top of the route system; they do not become route authority.

### What is now actually drawn

- exact rebound C22 v3.0 relation carriers remain the base;
- arrival/service anchor is graphically distinct from optional content nodes;
- the cross-river cable relation is visible as a transport carrier;
- the south-bank multi-branch / loop condition is shown as a bounded evidence-reading field without claiming a survey polygon;
- R02/R05/R06/R07/R09/R12/R13 are explicitly subordinate optional content nodes;
- `CONTENT ≠ ROUTE` is attached to the network field rather than existing only as prose;
- Return remains visually present as a service principle while exact field return direction/live state stays open;
- the bottom sequence clarifies public journey order without pretending to be surveyed route direction.

### Flow claim boundary

`FN-C0 NETWORK IDENTIFIED / partial FN-C1 source-carrier preservation` only.

No full edge-node topology, survey, route planning, exact direction, distance, slope, time, GPS or live-operation claim is introduced.

## 2. DRW-C04-C22-05 — Relational Section Analysis

### Primary claim

The section set must let the viewer read:

`TRANSPORT / MOVING VIEW` and `APPROACH → COMPRESSION → RELEASE / RETURN`

without needing the right-hand prose first.

### What is now actually drawn

#### SEC-A
- existing source bank profiles and cable carrier remain the geometry basis;
- Qingjiang river relation is explicit;
- bidirectional transport is drawn as two opposed route events rather than one generic arrow;
- moving-view relation is attached to the cable field;
- 1056 m and `ΔH≈156 m` remain detached public references and explicitly `NOT SCALED`.

#### SEC-C / R13
- the existing two-sided convergence profiles remain visible;
- one continuous body-passage carrier crosses the section;
- three human-scale positions expose approach / compression / release sequencing;
- the compression region is shown as an analytical zone;
- Return / Exit is drawn as a continuation, not only written in the rail;
- W/H/surface/slip/guard/capacity remain FIELD VERIFY.

#### SEC-B / R06
- remains a low-weight frozen-context inset only;
- no new R06 geometry, dimensions, node family or technical scope is reopened.

## 3. Graphic hierarchy

Applied hierarchy:

`PRIMARY CLAIM → DOMINANT SPATIAL FIELD → SOURCE RELATION → ANALYTICAL RELATION → OPTIONAL CONTENT → ANNOTATION RAIL → METADATA`

Three reading distances were produced locally:

- full-size 1684×1189 PNG;
- 421×297 far-read derivative;
- grayscale derivative.

Observed producer-side results:

- C22-01 far read retains river/cable/branch-field/sequence hierarchy;
- C22-05 far read retains SEC-A cable relation and SEC-C body/compression/return sequence;
- grayscale still separates primary source geometry, analytical zones and secondary context;
- annotation rail does not own the first read.

These are producer readbacks only, not independent Design KEEP.

## 4. Artifact evidence

Local deterministic render environment: Inkscape SVG→PNG.

- `C04_C22_01_JOURNEY_ROUTE_ANALYSIS_v3_3.svg` — 13,067 bytes — SHA256 `ec72e6963160848fb31412bf03a188b6679e20f40fef2e1b5b492cf5a4db72ab`
- `C04_C22_01_JOURNEY_ROUTE_ANALYSIS_v3_3.png` — 305,094 bytes — SHA256 `194e0941adaa03bef168248c6e0a51b1123042f4a460d4e4d0e182d1c431c710`
- `C04_C22_05_RELATIONAL_SECTION_ANALYSIS_v3_3.svg` — 10,575 bytes — SHA256 `ac76c08a07b39b21952e5985fc0005a3b64f9d290a7255dba36cf7b7593a919f`
- `C04_C22_05_RELATIONAL_SECTION_ANALYSIS_v3_3.png` — 279,936 bytes — SHA256 `1efebd466e1fb6d325a4b30d3e34462434163248ae93c2b9eb2099ba73658ed6`

SVG XML parse: PASS.  
Inkscape render: PASS.  
Full-size preview reopen: executed.  
Far-read derivative reopen: executed.  
Grayscale derivative: generated.

## 5. Producer gate state

| gate | state |
|---|---|
| source authority | SELF-CHECKED / C22 source carriers retained |
| geometry / network coherence | SELF-CHECKED / no new route geometry authority claimed |
| analysis truth-state | SELF-CHECKED / source, evidence-bound, design principle and FIELD OPEN separated |
| relation drawn vs prose-only | materially improved; independent design verdict still required |
| vector/editability | SELF-CHECKED / core geometry, labels, markers and rails remain SVG vector |
| output round-trip | SELF-CHECKED / render + reopen executed |
| independent Design Review | PENDING |
| MAIN / Professional Finish / Promotion | NOT AWARDED |

## 6. Current state

`v3.2 = SOURCE-REBOUND PROVENANCE / superseded at analysis-presentation scope`

`v3.3 = EXECUTED / SOURCE-BOUND / SELF-CHECKED / INDEPENDENT DESIGN REVIEW PENDING`

No producer `PIXEL KEEP`, `MAIN KEEP`, `PROFESSIONAL FINISH PASS`, engineering approval, field approval, merge or project Promotion is implied.
