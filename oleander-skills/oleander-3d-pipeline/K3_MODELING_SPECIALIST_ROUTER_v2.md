# OLEANDER 3D Specialist Modeling Extension v2 — K3 Execution Router Addendum

Status: CANDIDATE SPECIALIST EXTENSION / additive to `SKILL.md`.

## Architecture position
This file is **not** OLEANDER Current Authority, not a new Project Flow, not a new P-level, and not a new system Gate. It is a specialist modeling extension executed **inside** the existing OLEANDER architecture:

`OLEANDER Current Authority → Canonical Project Flow v0.3 → Project Control Plane v0.3 → K3 Execution Router → Modeling Contract / OLEANDER 3D Skill → triggered specialist review`.

The existing project structure remains:
`P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`.

The existing runtime structure remains:
`Design Intelligence → Execution Runtime → Evidence & Governance`, with `Exploration Loop + Canonical Production Loop`.

The existing Project Control Card remains the project execution control object. This addendum may emit specialist receipts but does not replace the Project Control Card, Decision Question, Locked/Open Variables, Design State, Authority State, or existing promotion logic.

## Purpose
Choose the correct modeling route and Source representation before geometry production, while preserving all existing Authority, Evidence, QA, Review, Persistence and Promotion rules in `SKILL.md` and Control Plane v0.3.

## Read order
1. OLEANDER current governance / Project Control Plane / Canonical Project Flow.
2. `SKILL.md` — 3D invariant authority, evidence, diagnostic, review and completion rules.
3. this K3 specialist addendum — modeling route and representation selection only.
4. one specialist route protocol:
   - reference exists → `reference-reproduction/FEATURE_ALIGNED_CURVE_NETWORK_PROTOCOL_v1.md` plus existing reference protocols;
   - no governing reference / original product → `structure-to-form/STRUCTURE_TO_FORM_PROTOCOL_v1.md`;
   - domain-specific pack only after route selection, e.g. `domain-packs/automotive/AUTOMOTIVE_SURFACE_PACK_v1.md`.
5. executable specialist contract: `contracts/3D_MODELING_ROUTE_CONTRACT_v1.json`.

## K3 modeling architecture
`Authority resolved by K2 → Modeling Intent → Representation Router → Source Construction → Derived Geometry → Diagnostics → K4 Review Router → K5 Evidence/Persistence when triggered`.

No specialist receipt may widen the authority or design state resolved by the Control Plane.

## Two specialist modeling routes
### A. REFERENCE_RECONSTRUCTION
Use when a specific existing object/version is being reproduced.

Internal specialist sequence:
`R0 Reference Lock → R1 Calibration → R2 Hard Points / Landmarks → R3 Identity / Feature Curves → R4 Section Network → R5 Primary Surface → R6 Aperture / Interface Architecture → R7 Secondary Identity → Review`.

### B. STRUCTURE_TO_FORM
Use when no existing object governs the exterior, or when the task is original product development.

Internal specialist sequence:
`S0 Product Intent → S1 Functional Decomposition → S2 Component Graph → S3 Interface / Motion Graph → S4 Package & Clearance → S5 Structural Topology → S6 Form Envelope → S7 Primary Surface → S8 Assembly / Manufacturing → S9 Secondary / CMF → Review`.

**R0–R7 and S0–S9 are specialist execution stage IDs only. They are not P0–P4 project structure, G0–G9 project Gates, or new OLEANDER system states.**

## Representation selection precedes modeling
The specialist runtime emits a `MODELING_ROUTE_RECEIPT` before primary geometry work. Allowed representation families:
- `PARAMETRIC_SOLID_CAD`
- `FEATURE_CURVE_STRUCTURED_SUBD`
- `PROFILE_REVOLVE`
- `SKELETON_SECTION_ASSEMBLY`
- `SOFT_MATERIAL_SIM_SCULPT_RETOPO`
- `TERRAIN_GIS_SPATIAL`
- `HYBRID`

Blender is a Capability, not a method or representation strategy.

## Source architecture
For controlled product/form work, prefer three explicit layers:
1. **Source controls** — hard points, datum, component graph, feature curves, section curves, boundary rails, sparse parameters.
2. **Generated construction** — structured cage / CAD features / patch network / assembly geometry.
3. **Derived evaluated surface** — SubD/tessellated/render/export geometry used for diagnostics and delivery.

Dense evaluated geometry must not become Source merely because it looks finished.

## CandidateSpec role
Where practical, new modeling candidates should be expressed as data deltas rather than new historical wrapper runtimes. A CandidateSpec may record:
- candidate revision;
- parent Source revision / comparable per-metric baseline;
- specialist route + representation family;
- protected families;
- changed controls and before/after values;
- expected geometric effect;
- rollback values;
- required specialist diagnostics.

A CandidateSpec is a **Technical Dependency / execution artifact**. It does not replace the Project Control Card, Candidate Gate, Authority transition, Decision Artifact, Project State, Current Task or Promotion review.

## Execution bands inside existing Fidelity / QA
These are execution bands, not new project loops or system gates:

### FAST
`Source controls → generated geometry → topology / bounds → sections / projection → specialist receipts`.
Use for preflight / low-cost design validation consistent with existing Fidelity policy and Machine QA.

### VISUAL
`Broad → Strip → Grazing → Zebra → orthographic + held-out 3/4 readback`.
Results feed the existing Visual QA + Project QA / Professional Design gate.

### DELIVERY
native reopen / retained binary / exchange / final render / manifest / SHA / review package.
Use only when the existing Control Plane / Fidelity / persistence triggers require it.

A successful execution band never changes Design State by itself.

## Repeated-revise routing — bind to existing CB-01
Do **not** create a new Representation Escalation Gate.

Control Plane `CB-01｜Repeated Revise Breaker` remains authoritative: after the same Decision Question receives **2 consecutive Visual/Project REVISE** results, stop automatic same-layer tuning and perform:
`Root Cause Reclassification: Parameter / Relation / Geometry / Topology / Architecture / Evidence`.

If that existing CB-01 reclassification identifies representation vocabulary as the root cause, K3 may route to `REOPEN_REPRESENTATION_MODEL` and test feature curves, sections, boundary ownership, patch topology, aperture architecture, measurement model or representation family. This is a specialist repair action under CB-01, not a sixth breaker or a new system Gate.

## Gate-local / metric-local baselines
Comparable best-known machine metrics may be retained per specialist diagnostic without promoting the whole candidate. A globally REJECTED candidate may establish a comparable diagnostic baseline, but it cannot promote Design State, Authority, MAIN status or professional quality.

## Runtime composition rule
Stage consumers declare semantic capabilities, not legacy object names. A diagnostic asks for e.g. `APERTURE_WINDSHIELD_BOUNDARY` capability and returns `NOT_APPLICABLE_STAGE_HOLD` when the specialist stage intentionally lacks it; it must not crash because a historical object name is absent.

## Completion boundary
This extension changes modeling execution quality only. `route selected`, `runtime green`, `projection pass`, `0 folds`, `SubD generated`, `structured patches assembled` or `package solved` do not prove Professional Design PASS, Class-A continuity, engineering release, manufacturability, reference fidelity, Field proof or Canonical promotion.
