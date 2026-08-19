# OLEANDER 3D Pipeline v2 — Current Routing Addendum

Status: CURRENT CANDIDATE / additive to `SKILL.md`; no existing v1 rule is deleted or weakened.

Purpose: change the execution architecture before adding more domain-specific rules. The core Skill remains the authority/evidence/review discipline. This addendum decides **how a modeling task enters the pipeline, which representation owns Source, and when a representation must be reopened instead of parameter-tuned**.

## Read order
1. `SKILL.md` — invariant authority, evidence, diagnostic, review and completion rules.
2. `00_CURRENT_V2_ROUTER.md` — current route selection and stage architecture.
3. one route protocol:
   - reference exists → `reference-reproduction/FEATURE_ALIGNED_CURVE_NETWORK_PROTOCOL_v1.md` plus existing reference protocols;
   - no reference / original product → `structure-to-form/STRUCTURE_TO_FORM_PROTOCOL_v1.md`;
   - domain-specific rules only after route selection, e.g. `domain-packs/automotive/AUTOMOTIVE_SURFACE_PACK_v1.md`.
4. executable route contract: `contracts/3D_MODELING_ROUTE_CONTRACT_v1.json`.

## Architecture
`Authority → Modeling Intent → Representation Router → Source Construction → Derived Geometry → Diagnostics → Evidence → Independent Design Review → Completion`

The producing runtime must not collapse these layers.

## Two primary entry routes
### A. REFERENCE_RECONSTRUCTION
Use when a specific existing object/version is being reproduced.

Required early gates:
`R0 Reference Lock → R1 Calibration → R2 Hard Points / Landmarks → R3 Identity / Feature Curves → R4 Section Network → R5 Primary Surface → R6 Aperture / Interface Architecture → R7 Secondary Identity → Review`.

### B. STRUCTURE_TO_FORM
Use when no reference object governs the design, or when the task is original product development.

Required early gates:
`S0 Product Intent → S1 Functional Decomposition → S2 Component Graph → S3 Interface / Motion Graph → S4 Package & Clearance → S5 Structural Topology → S6 Form Envelope → S7 Primary Surface → S8 Assembly / Manufacturing → S9 Secondary / CMF → Review`.

## Representation selection precedes modeling
The runtime must emit a `MODELING_ROUTE_RECEIPT` before primary geometry work. Allowed representation families:
- `PARAMETRIC_SOLID_CAD`
- `FEATURE_CURVE_STRUCTURED_SUBD`
- `PROFILE_REVOLVE`
- `SKELETON_SECTION_ASSEMBLY`
- `SOFT_MATERIAL_SIM_SCULPT_RETOPO`
- `TERRAIN_GIS_SPATIAL`
- `HYBRID`

Blender is an application, not a representation strategy.

## Source architecture
For controlled product/form work, prefer three explicit layers:
1. **Source controls** — hard points, datum, component graph, feature curves, section curves, boundary rails, sparse parameters.
2. **Generated construction** — structured cage / CAD features / patch network / assembly geometry.
3. **Derived evaluated surface** — SubD/tessellated/render/export geometry used for diagnostics and delivery.

Dense evaluated geometry must not become Source merely because it looks finished.

## CandidateSpec instead of runtime inheritance
New benchmark candidates should be data deltas where practical. A candidate spec records:
- candidate revision;
- parent Source revision / LKG gate baselines;
- route + representation family;
- protected families;
- changed controls and before/after values;
- expected geometric effect;
- rollback values;
- required fast/visual/delivery gates.

Do not create a new historical wrapper runtime when the only change is a Source parameter or one representation-family delta.

## Three-speed execution
### FAST LOOP
`Source controls → generated geometry → topology / bounds → sections / projection → gate-local receipts`.

### VISUAL LOOP
`Broad → Strip → Grazing → Zebra → orthographic + held-out 3/4 readback`.

### DELIVERY LOOP
native reopen / retained binary / exchange / final render / manifest / SHA / independent review package.

A candidate may fail visual quality while the engineering execution loop succeeds.

## Representation Escalation Gate
Trigger `STOP_PARAMETER_TUNING_REOPEN_REPRESENTATION` when any of the following is true:
- the same failure family survives 3 controlled Source edits with no material visual improvement;
- one view can only improve by repeatedly regressing another already-locked view;
- a required aperture/interface cannot be represented without destructive after-the-fact cutting;
- semantic form families require floating/overlapping visible blobs to imitate one continuous shell;
- topology/measurement repeatedly passes while held-out visual identity remains generic;
- a diagnostic requires legacy object-name assumptions absent from the current stage.

On trigger, test the representation vocabulary itself: feature curves, sections, boundary ownership, patch topology, measurement model, or route selection. Do not relax thresholds or add detail.

## Gate-local LKG
Store best-known baselines per gate, not only per whole candidate. A globally REJECTED candidate may establish a machine baseline for one comparable metric, but it cannot promote design quality or whole-version authority.

## Runtime composition rule
Stage consumers declare semantic capabilities, not legacy object names. A diagnostic must ask for e.g. `APERTURE_WINDSHIELD_BOUNDARY` capability and return `NOT_APPLICABLE_STAGE_HOLD` when the stage intentionally lacks it; it must not crash because `REF_WINDSHIELD` is absent.

## Completion boundary
v2 architecture changes execution quality, not design truth. `route selected`, `runtime green`, `projection pass`, `0 folds`, `SubD generated`, or `structured patches assembled` do not prove professional visual quality, Class-A continuity, engineering release, manufacturability, or reference fidelity.
