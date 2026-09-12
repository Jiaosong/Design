# G1 R4.4｜Termination Construction Sufficiency Decision｜2026-08-14

## Decision State

`SINGLE_POLE_COLLAPSE_CONSTRUCTION_DOMINANT_EXISTING_RELATION_SET_INSUFFICIENT / R4_5_EXPLICIT_SPARSE_TERMINATION_CAP_RELATION_JUSTIFIED_FOR_EXPLORATION / REVISE / WORKING_SOURCE / CANDIDATE_PROMOTION_NOT_RUN`

R4.4 isolates the remaining `RIGHT / FRONT TERMINATION` defect after R4, R4.1, R4.2 and R4.3 excluded simple topology density, pole-refined sampling, shared-envelope exponent micro-tuning and bounded OPPOSITE / LOWER penultimate-profile tuning as sufficient repairs.

R4.4 makes **no authoritative Source edit**. All construction counterfactuals are `DERIVED_EXECUTION_NOT_AUTHORITY` and exist only to test sufficiency of the current construction relationship.

This decision does not authorize Candidate Promotion, Canonical Promotion, Class-A, engineering CAD, manufacturing, ergonomic validation or Release.

## Evidence Identity

Execution head:

`6a0e5326a733982cc4c3f752d5ceb8b09e8a3152`

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.4 Construction Sufficiency`
- run `31804629133`
- result `SUCCESS`

Artifact:

- ID `9220749591`
- name `oleander-modeling-worker-v0-13-g1-r4-4-31804629133`
- SHA-256 `74e7c7b9a45916a23faf43fc0b4858e99e2dbe69d9a3386cae4c60f3a7099ae4`
- size `4,841,038 bytes`

The same execution head also completed successfully under:

- `OLEANDER Modeling Worker v0.13 Blender Bridge`
- `OLEANDER Blender Surface System v1.20.0 CMF Lab`
- `OLEANDER Control Plane v0.3`
- `AI Governance Evals`
- retained R3 / R4 regression workflows.

## Authority / Lock State

R4.4 verifies:

- Blender-native R2 Source rebuild succeeds;
- confirmed R3 interface is applied only as a reversible readback input;
- native Source is restored exactly after that readback;
- `INTERFACE_DECK_BOUNDARY.theta_center = TOP_MERIDIAN` remains locked;
- confirmed interface relation remains `u_halfspan=0.26 / theta_halfspan=1.06 / core_fraction=0.29 / depth=0.012`;
- shared termination-envelope exponent remains `0.34`;
- existing Machine QA remains PASS;
- no profile control point is edited;
- no GRIP_AXIS control point is edited;
- all counterfactual meshes use identical diagnostic sampling;
- every counterfactual remains `DERIVED_EXECUTION_NOT_AUTHORITY`;
- shared Blender Surface System v1.20.0 owns Strip / Grazing / Zebra rendering;
- Candidate Promotion remains `NOT_RUN`.

## Diagnostic Counterfactuals

Five equal-sampling diagnostic constructions were evaluated:

1. `BASELINE` — current confirmed Working Source construction.
2. `AXIS_TANGENT_NEUTRAL` — removes local GRIP_AXIS tangent rotation as the main changing term without editing GRIP_AXIS Source controls.
3. `CROSS_SECTION_SYMMETRY_NEUTRAL` — removes late thumb/opposite and top/lower asymmetry while retaining the current shared collapse construction.
4. `SINGLE_POLE_COLLAPSE_NEUTRAL` — freezes the shared tail-envelope amplitude through the diagnostic tail and postpones collapse to the final non-authoritative fan from `u=0.9995 → 1.0`.
5. `COMBINED_NEUTRAL` — combines axis, asymmetry and late-collapse neutralization.

The single-pole and combined counterfactuals are **not candidate geometries**. In particular, delaying collapse to the last fan intentionally creates a small terminal swirl / loop. Its purpose is causal isolation, not styling.

## Analytic Construction Probe

Method:

`LOCAL_DIFFERENTIAL_CONSTRUCTION_COUNTERFACTUAL`

Sampling:

- `theta_samples = 144`
- normal-turn span = `0.002u`
- near-pole classification range = `u >= 0.995`
- diagnostic intervention begins at `u = 0.94`

Direct R2 normal-field control versus the differential baseline differs by only:

`0.2701352264°`

which is inside the declared `0.5°` diagnostic-control tolerance.

### Near-pole maximum normal turn

| Counterfactual | max turn | reduction vs baseline |
|---|---:|---:|
| BASELINE | `7.6262592204°` | `0%` |
| AXIS_TANGENT_NEUTRAL | `7.2140628777°` | `5.4049610806%` |
| CROSS_SECTION_SYMMETRY_NEUTRAL | `7.3015018028°` | `4.2584104244%` |
| SINGLE_POLE_COLLAPSE_NEUTRAL | `1.1273043748°` | `85.2181214639%` |
| COMBINED_NEUTRAL | `0.2247932736°` | `97.0523782748%` |

Baseline pre-cap maximum remains approximately:

`0.6494447442°`

The dominant growth therefore occurs specifically as the current construction approaches the forced single pole.

## Fixed-Rig Visual Decision

All five constructions were rendered with the same local camera and shared Surface System under `STRIP / GRAZING / ZEBRA`.

### AXIS_TANGENT_NEUTRAL

The main right/front convergence remains visually organized almost the same way as baseline. Strip redistribution is visible, but the core closure reading persists. Grazing and Zebra show no corresponding reorganization large enough to support GRIP_AXIS tangent as the primary cause.

Decision:

`AXIS CONTRIBUTION PRESENT / NOT PRIMARY`.

### CROSS_SECTION_SYMMETRY_NEUTRAL

Pairwise late symmetry produces still smaller visual change. The same terminal convergence remains visible in Strip and Zebra.

Decision:

`ASYMMETRY CONTRIBUTION PRESENT / NOT PRIMARY`.

This is consistent with R4.2/R4.3: OPPOSITE / LOWER convergence contributes to the defect but does not own the remaining construction failure by itself.

### SINGLE_POLE_COLLAPSE_NEUTRAL

The extended tail convergence materially reorganizes. The long concentrated Strip/Zebra closure is removed from most of the tail and is instead compressed into the deliberately artificial final fan near the endpoint.

A small local swirl / loop appears at the final diagnostic collapse. This is expected and is **not** read as a solution. It demonstrates that the current defect is strongly coupled to how a nonzero asymmetric cross-section is continuously forced into one pole across the existing tail construction.

Decision:

`DISTRIBUTED SINGLE-POLE COLLAPSE IS PRIMARY CONSTRUCTION CAUSE`.

### COMBINED_NEUTRAL

The broad tail field is reduced further, while the deliberately delayed final collapse becomes an even more concentrated local loop. This confirms secondary axis/asymmetry interaction but does not change the primary routing conclusion.

Decision:

`SECONDARY INTERACTION CONFIRMED / NOT A CANDIDATE SHAPE`.

## Construction Sufficiency Decision

Final classification:

`SINGLE_POLE_COLLAPSE_CONSTRUCTION_DOMINANT_EXISTING_RELATION_SET_INSUFFICIENT`

Interpretation:

1. More execution tessellation does not solve the defect.
2. Sampling closer to the pole does not solve the defect.
3. Re-scaling the existing shared `sin(pi*u)^exponent` envelope does not solve it.
4. Bounded OPPOSITE / LOWER profile changes reduce one component but mostly widen the termination.
5. Removing axis tangent rotation alone has only a small effect.
6. Removing late cross-section asymmetry alone has only a small effect.
7. Diagnostic removal of the **distributed shared single-pole collapse** removes the great majority of the near-pole normal-turn growth.
8. Therefore the current sparse relation set does not contain an adequate degree of freedom for controlling *where and how* the asymmetric cross-section becomes a terminal cap.

This is a structural insufficiency diagnosis, not a request for more mesh DOF.

## R4.5 Authorization Boundary

R4.4 authorizes only the following next exploration:

`R4.5｜Explicit Sparse Termination-Cap Relation`

R4.5 may define **one explicit Source-level construction relation** that controls cap onset and collapse distribution while preserving the confirmed body/interface relations.

The relation must satisfy all of the following:

- sparse and semantically explicit;
- editable/readable through Blender-native Working Source;
- no mesh-local vertex ownership;
- no hidden sculpt correction;
- no per-vertex or dense control field;
- current confirmed interface remains locked;
- global shared envelope `0.34` remains the body/tail baseline outside the new bounded cap region unless later evidence explicitly justifies superseding it;
- OPPOSITE / LOWER point escalation remains forbidden without new evidence;
- the new relation must be reversible and included in Source snapshot/digest/roundtrip;
- Machine QA must be extended with a termination-cap fairness / closure gate before visual acceptance;
- only Machine-PASS variants may enter shared Surface System Strip/Grazing/Zebra review.

R4.4 does **not** pre-select the R4.5 parameterization. The next stage must first define the smallest relation vocabulary necessary to express cap onset and closure distribution without recreating a hidden sculpt system.

## Current Authority State

- `INTERFACE RELATION = CONFIRMED / LOCKED`
- `TERMINATION ENVELOPE = 0.34 / LOCKED AS BODY-TAIL BASELINE`
- `R4.1 ENVELOPE VARIANTS = REJECTED`
- `R4.3 PROFILE VARIANTS = REJECTED`
- `R4.4 CONSTRUCTION SUFFICIENCY = CLOSED`
- `RIGHT / FRONT TERMINATION = REVISE / R4.5 CAP-RELATION EXPLORATION AUTHORIZED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.

## Next Legal Action

`R4.5 relation vocabulary → Blender-native Source Authority binding → termination-cap Machine fairness/closure gate → bounded professional variants → fixed Strip/Grazing/Zebra → regression check against confirmed interface → decision receipt`
