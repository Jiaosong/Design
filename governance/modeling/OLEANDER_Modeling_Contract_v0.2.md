# OLEANDER Modeling Contract｜v0.2

**Status:** REVIEW  
**Parent:** OLEANDER Canonical Project Flow｜v0.3  
**Primary:** B04｜Metrics & Governance  
**Supporting:** IP03 / SP04

## Purpose

This contract governs how an OLEANDER design model becomes a trustworthy editable source. It corrects issues exposed by the Automotive v0.7 + R01 regression: bounding-box/manifold QA was too weak, detail arrived before primary geometry was reliable, locks could freeze relationships too early, and selective editing depended on object-name selectors instead of semantic dependencies.

## Canonical modeling sequence

`Decision Question → Hard Points / Proportion Skeleton → Envelope → Section Network → Primary Geometry / Surface → Construction & Surface QA → Component Architecture → Secondary Geometry → Detail / Instances → Material Binding → Multi-Scale QA → Candidate Authority`

## M0–M10

- M0｜Decision Question
- M1｜Hard Points & Proportion Skeleton
- M2｜Envelope / Package
- M3｜Section Network
- M4｜Primary Geometry / Primary Surface
- M5｜Construction & Surface QA
- M6｜Component Architecture
- M7｜Secondary Geometry
- M8｜Detail / Repetition / Instances
- M9｜Material / CMF Binding
- M10｜Multi-Scale Modeling QA

F0 usually covers M0–M3; F1 focuses M4–M6; F2 covers stable M7–M8 plus refined M5/M10; F3 adds presentation/material outputs without changing design authority.

**F1 does not mean a highly detailed model. It means primary geometric relationships are reliable.**

## Modeling quality gates

Integrity QA covers file/runtime/dimensions/transforms/normals/manifold/export validity.

Construction QA covers the source-model method: SubD topology and pinching, NURBS patch/continuity, CAD feature/datum stability, BIM host/grid/type logic, dependency and instance structure, section traceability and rebuild stability.

Design Geometry QA covers silhouette, proportion, stance, hierarchy, curvature tension, junction logic, component relations, detail density and interaction/use clearances.

Project QA checks the Decision Question, locked variables, dependent zones, exit condition and project intent.

Manifold PASS alone is never Surface Quality PASS.

## Mandatory diagnostics where relevant

`CLAY_BROAD / CLAY_STRIP / CLAY_GRAZING / SIDE_SILHOUETTE / SECTION_OVERLAY / ZEBRA / CURVATURE / WIREFRAME`

## Progressive Lock

`OPEN / LOCKED / DEPENDENCY_LOCKED / CONDITIONALLY_UNLOCKABLE / FROZEN`

A dependent relation may request controlled reopening through:

`Revision Request → Impact Analysis → Affected Components / Sections / Views → Unlock Decision → Selective Rebuild`

This prevents local patching from replacing necessary relational redesign.

## Semantic dependency

Use semantic component IDs and assemblies rather than canonical object-name wildcards.

Preferred:

`COMP-WHEEL-SPOKE → ASY-WHEEL → INST-WHEEL-FL/FR/RL/RR`

Legacy:

`*_SPOKE_* → 40 independent mesh targets`

The system maintains both a Design Semantic Graph and Technical Dependency Graph.

## Source / Derived / Export

Every model distinguishes:
- Editable Source
- Derived Model
- Export

Derived/render/export geometry never silently replaces editable-source authority.

## Revision Contract

A revision records source authority, Decision Question, semantic targets, parameters before/after, locks, conditional dependencies, expected affected geometry/views, budget, cache and promotion rules.

Worker output must include actual changed components/hashes, unexpected changes, affected views, QA and receipt.

## Selective execution

`Revision Contract → Dependency Resolve → Impact Graph → Changed Source Nodes → Derived Components → Affected Views → Selective Rebuild → Selective Render → QA`

Affected views should eventually be dependency-resolved rather than manually hard-coded.

## Cache

Artifact key = `Source Authority Hash + Normalized Contract + Worker Version + Runtime + Dependency Graph Version`.

Scopes: `JOB_LOCAL / PROJECT_LOCAL / PERSISTENT_CROSS_RUN`.

A job-local cache hit must not be described as persistent cross-run cache.

## Worker autonomy boundary

Workers may auto-repair deterministic technical faults. They must not autonomously optimize design variables. Design issues return a `REVISION_PROPOSAL` for design reasoning/human decision.

## Promotion

Authority remains progressive:

`NONE → WORKING_SOURCE → CANDIDATE_AUTHORITY → CANONICAL_AUTHORITY → FROZEN_AUTHORITY`

An asset can be `EXECUTION BENCHMARK PASS` while still `MODELING QUALITY REVISE`.

## Persistence

Promotion-only persistence remains mandatory:
- Exploration → temp/local
- Candidate → receipt/review evidence
- Promoted → Artifact Registry → Notion / GitHub / Google Drive

## R01 migration

R01 selective execution remains valid historical evidence. Its wildcard selector and expected object count map to Semantic Component IDs + Dependency Graph. R01 proved selective Worker execution; v0.2 upgrades the source-model architecture, surface/construction QA and dependency semantics.

## Review boundary

v0.2 remains REVIEW. Before a higher canonical promotion it must be applied to the automotive model from F0→F1 and at least one second geometry family.