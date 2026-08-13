# OLEANDER Modeling Worker v0.12｜Relationship-Driven Freeform Surface System

Status: `SYSTEM CANDIDATE / RE-ENTER / NOT CANONICAL`

## Decision Question

Can `SYS-MODELING-WORKER` evolve from deterministic section/vertex/face generation into a worker that **understands explicit design relationships and generates quality-stable freeform surfaces**, while preserving auditability, deterministic execution, authority boundaries and fail-closed QA?

## Why v0.12 exists

v0.11 proved a reliable execution benchmark: hard points, editable source, semantic routing, secondary geometry, linked instances, material binding, multi-scale QA and PAP can remain stable through promotion. It did **not** establish Class-A or high-quality freeform-surface authority.

The v0.12 change is therefore architectural, not another local Automotive revision. v0.11 remains immutable historical CanonICAL benchmark authority; v0.12 begins a new Candidate chain.

## System objective

Replace the dominant construction assumption:

`Sections → vertices → faces`

with:

`Design relationships → primary curves → low-frequency control cage → fair evaluation surfaces → execution topology`

The worker must reason about relationships before topology and must expose surface quality as machine-readable evidence rather than relying on smooth shading.

## Canonical pipeline candidate

1. `M0 Decision Question / Authority Resolve`
2. `M1 Hard Points / Constraints`
3. `M2 Volume Skeleton`
4. `M3 Relationship Graph + Primary Curves`
5. `M4 Low-Frequency Control Cage`
6. `M4.5 Surface Fairness Gate`
7. `M5 Primary Surface Freeze`
8. `M6 Semantic Component Architecture`
9. `M7 Secondary Geometry`
10. `M8 Detail / Instances`
11. `M9 Material / CMF Binding`
12. `M10 Multi-Scale QA`
13. `PAP / Promotion when triggered`

`M4.5` is new inside the Modeling Contract, not a new portfolio-level governance gate. It is subordinate to existing Project/Visual/Artifact QA and cannot promote anything by itself.

## First-class design objects

### Relationship Graph

A relation is not a prose note. It must identify source, target, relation type, priority, intended visual effect and allowed variation.

Minimum relation classes:
- `ALIGN`
- `TANGENCY`
- `CURVATURE`
- `OFFSET`
- `PROPORTION`
- `TENSION`
- `FLOW`
- `BOUNDARY`
- `DEPENDENCY`

### Primary Curves

Primary curves carry design intent before surface tessellation. Typical roles include silhouette, centerline, shoulder, belt, rocker, crown, opening, transition and termination trajectories.

Every promoted curve must declare:
- semantic role;
- dependencies;
- locked/open variables;
- target continuity at endpoints/intersections;
- sampling policy;
- authority state.

### Low-Frequency Control Cage

The cage is the primary shape-control object. It must remain materially lower frequency than the evaluation/execution mesh. Local details may not force premature cage densification.

The cage must expose:
- semantic rows/columns or patches;
- dependency IDs;
- symmetry/asymmetry intent;
- boundary conditions;
- local edit influence;
- frequency/density budget.

### Fair Evaluation Surface

The evaluation surface is judged on shape quality, not polygon count. Execution topology is derived only after surface intent passes fairness review.

## M4.5 Surface Fairness Gate

Machine evidence must support the applicable subset of:
- positional continuity (`G0`);
- tangent continuity (`G1`);
- curvature continuity (`G2`) when requested by the contract;
- tangent-angle jump distribution;
- curvature-comb continuity;
- curvature sign changes / unintended inflection count;
- curvature-rate spikes;
- control-point / sample-spacing regularity;
- zebra/reflection-strip continuity evidence;
- highlight acceleration / compression flags;
- pole, triangle or termination influence zones;
- silhouette derivative stability.

A machine PASS means only that declared thresholds are met. Human Visual/Project QA still owns whether the surface expresses the intended design relationship.

## Fail-closed rules

- `Position relationship PASS != Surface fairness PASS`.
- `Smooth shading PASS != G1/G2 PASS`.
- `Quad topology != fair surface`.
- `Dense topology != quality`.
- `Zebra readable != design approved`.
- A local patch may not override an unresolved upstream Volume/Curve/Cage defect.
- Two consecutive same-question local fairness revisions without improvement trigger root-cause reclassification to M2/M3/M4.
- Secondary geometry and detail remain blocked while M4.5 is REVISE.
- Derived execution mesh never replaces editable Curve/Cage/Surface Source Authority.

## Authority model

Three separate authorities must be recorded:

1. `DESIGN_RELATIONSHIP_AUTHORITY` — accepted semantic relationships and locked variables.
2. `SURFACE_SOURCE_AUTHORITY` — editable primary curves/cage/evaluation surfaces.
3. `EXECUTION_GEOMETRY_AUTHORITY` — deterministic mesh or application-native implementation generated from the Surface Source.

For v0.12 Candidate work these remain `WORKING_SOURCE` or `CANDIDATE_AUTHORITY`; no Canonical promotion is implied.

## Application neutrality

Automotive v0.12 is the first stress test because it exposes fairness defects aggressively, but the system is application-neutral. The same contract must support product, furniture, appliance, spatial shell and other freeform modeling tasks without automotive-specific authority leaking into the system layer.

## Migration rule from v0.11

Retain from v0.11:
- deterministic job contracts;
- hard-point discipline;
- semantic IDs/dependencies;
- Machine/Visual/Project QA separation;
- secondary/detail/material dependency ordering;
- immutable receipts, PAP and Promotion boundaries.

Supersede as a default modeling assumption:
- section-array-first construction;
- topology-first local repair;
- smooth-shading-dominant fairness review;
- repeated parameter patching without upstream reclassification.

## Promotion criterion for v0.12

The system may not become Canonical merely because schemas/tests pass. Promotion requires at least one real freeform benchmark to demonstrate:

`Relationship intent → editable curves/cage → fair surface → deterministic execution geometry → machine fairness evidence → human design PASS → persistence/readback`

with no silent fallback to v0.11-style section/mesh patching as the primary shape method.
