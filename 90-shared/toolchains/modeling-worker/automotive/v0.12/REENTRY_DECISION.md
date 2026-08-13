# Automotive v0.12｜Freeform Surface Re-entry Decision

Status: `RE-ENTER / SYSTEM BENCHMARK CANDIDATE / M2 OPEN / M6+ BLOCKED`

## Authority boundary

Automotive v0.11 R29A remains the current promoted `CANONICAL_AUTHORITY` for the historical Modeling Worker execution benchmark. This v0.12 work does not mutate, downgrade or overwrite that authority.

This new benchmark asks a different question: can the worker derive editable, quality-stable freeform geometry from explicit design relationships rather than primarily from section-array interpolation and local topology patches?

No Class-A, engineering CAD, manufacturing, crash/aero, production panel or homologation authority is claimed.

## Re-entry reason

Post-promotion review identified a method-level gap rather than a single R29A parameter defect:

- overall silhouette still carries a single-bubble tendency;
- greenhouse / cowl / A-pillar / roof / C-pillar flow lacks independent low-frequency control;
- shoulder, belt, rocker and rear-haunch hierarchy is under-resolved;
- front/rear termination uses mesh-closure logic rather than independent volume/surface networks;
- local fender revisions demonstrate parameter-patching debt;
- smooth shading and clay/grazing renders can mask insufficient curvature fairness;
- the current QA chain does not make G1/G2, curvature comb, curvature-rate or reflection-flow evidence first-class.

Therefore the smallest responsible re-entry is not `R30` and not M7/M8 detail. The benchmark re-enters at `M2 Volume Skeleton`, then rebuilds M3/M4 before a new `M4.5 Surface Fairness Gate`.

## Locked inputs inherited from v0.11 for fair comparison

Unless an M2 decision explicitly reopens them:
- wheel OD contract `0.700 m`;
- wheelbase / track package used by the accepted v0.11 benchmark;
- broad overall length/width/height class;
- semantic distinction between Primary / Secondary / Detail geometry;
- deterministic receipts and machine/human QA separation;
- PAP and Promotion boundaries.

These are comparison controls, not automotive engineering hard points.

## Open design variables

### M2 Volume Skeleton

Establish independently controllable low-frequency volumes:
- `VOL-HOOD`
- `VOL-CABIN`
- `VOL-SHOULDER`
- `VOL-REAR-HAUNCH`
- `VOL-LOWER-BODY`
- `VOL-FRONT-TERMINATION`
- `VOL-REAR-TERMINATION`

Decision target: remove the need for one section family to carry all of hood, cabin, shoulder and termination behavior.

### M3 Relationship Graph + Primary Curves

Required first-class curves include at minimum:
- side silhouette;
- plan silhouette;
- centerline/roof flow;
- hood crown;
- shoulder;
- belt reference;
- rocker/lower tension;
- front/rear wheel-opening trajectories;
- A-pillar and C-pillar trajectories;
- front and rear termination flow curves.

Required relationship classes include:
- hood ↔ fender tangency/curvature intent;
- shoulder ↔ wheel crown flow;
- cabin ↔ shoulder proportion;
- rocker ↔ shoulder tension;
- rear haunch ↔ rear opening curvature;
- front/rear termination ↔ longitudinal body flow.

### M4 Low-Frequency Control Cage

The cage must remain sparse enough that a designer or agent can modify:
- cabin gesture;
- shoulder acceleration;
- hood tension;
- rear haunch mass;
- termination volume;

without inserting local wheel-detail topology.

Cage edits must declare influence/falloff. A local defect may not be solved by uncontrolled global cage densification.

## M4.5 Surface Fairness Gate

Before M5 may pass, the benchmark must produce machine-readable evidence for the applicable set of:
- G0/G1/G2 intent and measured proxies;
- tangent-angle jump distribution;
- curvature combs;
- curvature-rate spikes;
- unintended inflections;
- sample/control spacing regularity;
- zebra and reflection-strip continuity;
- silhouette derivative stability;
- termination/pole influence.

At least the following views/evidence families are required for human review:
- Side silhouette;
- Front 3Q / Rear 3Q;
- Top/plan;
- broad reflection strips along hood→fender→shoulder;
- broad reflection strips across cabin→shoulder→haunch;
- front/rear termination reflection views;
- wheel-arch local zebra only after the broad body volumes pass.

`Smooth shading` is rendering behavior only and cannot satisfy this gate.

## Blockers

Until M4.5 PASS:
- M5 Primary Surface Freeze = BLOCKED;
- M6 Component Architecture = BLOCKED;
- M7 Secondary Geometry = BLOCKED;
- M8 Detail/Instances = BLOCKED;
- M9 CMF Binding = BLOCKED;
- M10 final benchmark coherence = BLOCKED.

This prevents premature wheel, liner, glazing, spoke or material work from hiding upstream surface defects.

## First executable milestone

`E0 Relationship-Surface Contract` is the first milestone. It must demonstrate:

`Decision Question → Volume Skeleton → explicit Relationship Graph → Primary Curves → LOW Control Cage → quantitative sampled-curve fairness evidence → fail-closed M4.5 state`

without generating or promoting final automotive body topology.

The generic executable contract lives under:
`90-shared/toolchains/modeling-worker/v0.12/`

Automotive consumes that system contract as a benchmark; it does not redefine the system architecture.
