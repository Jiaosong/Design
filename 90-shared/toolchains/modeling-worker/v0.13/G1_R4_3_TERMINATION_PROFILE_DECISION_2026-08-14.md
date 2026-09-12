# G1 R4.3｜Opposite / Lower Terminal-Profile Visual Decision｜2026-08-14

## Decision State

`BOUNDED_PROFILE_RELATION_VARIATION_INSUFFICIENT / TERMINATION_CONSTRUCTION_OWNERSHIP_REENTRY_REQUIRED / REVISE / WORKING_SOURCE / CANDIDATE_PROMOTION_NOT_RUN`

R4.3 tested the bounded native Source relationship identified by R4.2: the penultimate control values of `OPPOSITE_SIDE_PLAN` and `LOWER_RETURN_PROFILE`. None of the three professional variants is accepted as the current termination correction.

This is a design-routing decision only. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Evidence Identity

Execution head:

`cdc546b4e183647050e53ee297c42c6f488e8e16`

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.3 Termination Profile Batch`
- run `31801757761`
- result `SUCCESS`

Artifact:

- ID `9219661435`
- name `oleander-modeling-worker-v0-13-g1-r4-3-31801757761`
- SHA-256 `ec25800d16c5108c99a8059c56e0dcfbe6d3fb2b9cdcbbf8dc57e63293234896`
- size `3,919,992 bytes`

All three variants pass the existing Machine QA, native Source readback/restore, confirmed-interface lock, exponent `0.34` lock, endpoint-control `0.003` lock, derived-non-authority checks and shared Surface System execution.

## Baseline

Current R2 terminal controls:

- `OPPOSITE_SIDE_PLAN[4] = 0.034`
- `LOWER_RETURN_PROFILE[4] = 0.050`

R4.2 ownership probe baseline:

- pre-cap max surface turn: `0.6494460684°`
- near-pole max surface turn: `7.8964152213°`
- hotspot remains in the OPPOSITE→LOWER quadrant.

## A｜OPPOSITE Primary

Controls:

- `OPPOSITE_SIDE_PLAN[4] = 0.038`
- `LOWER_RETURN_PROFILE[4] = 0.050`

Machine dimensions:

- `0.1900 × 0.0816800 × 0.0996130 m`

Probe:

- pre-cap max surface turn: `0.5902931°`
- near-pole max surface turn: `7.7024321°`

Visual decision:

- the primary OPPOSITE convergence is reduced analytically;
- local Strip / Grazing / Zebra remain very close to baseline;
- the retained right/front closure still reads as a concentrated termination convergence.

Decision: `REJECT / INSUFFICIENT VISUAL CHANGE`.

## B｜Balanced Quadrant

Controls:

- `OPPOSITE_SIDE_PLAN[4] = 0.042`
- `LOWER_RETURN_PROFILE[4] = 0.052`

Machine dimensions:

- `0.1900 × 0.0826339 × 0.0996130 m`

Probe:

- pre-cap max surface turn: `0.5398711°`
- near-pole max surface turn: `7.4751660°`

Visual decision:

- opposite/lower convergence is reduced further;
- the termination becomes measurably fuller / wider;
- Strip and Grazing redistribute the dark field but do not remove the core convergence;
- Zebra retains the same basic right/front closure structure.

Decision: `REJECT / DEFECT REDISTRIBUTED NOT SOLVED`.

## C｜Defined Quadrant

Controls:

- `OPPOSITE_SIDE_PLAN[4] = 0.046`
- `LOWER_RETURN_PROFILE[4] = 0.054`

Machine dimensions:

- `0.1900 × 0.0835879 × 0.0996130 m`

Probe:

- pre-cap max surface turn: `0.5366311°`
- near-pole max surface turn: `7.2694230°`

Visual decision:

- analytic near-pole turn improves most in the batch;
- the cap / right-front field becomes still fuller;
- Zebra convergence remains present;
- the additional width change is not justified by a correspondingly cleaner termination.

Decision: `REJECT / OVER-CORRECTION WITHOUT CLOSURE`.

## Important Diagnostic Transition

R4.3 does reduce the profile-convergence component identified by R4.2. However, once that component is reduced, the remaining onset of the termination turn becomes comparable to the existing `GRIP_AXIS` tangent rotation near `u ≈ 0.995`, while the much larger turn closer to the pole still persists.

For example:

- GRIP_AXIS tangent turn near `u = 0.995`: approximately `1.87° / 0.002u`;
- R4.3-B surface hotspot at `u = 0.995`: approximately `1.42° / 0.002u`;
- R4.3-B surface hotspot at `u = 0.998`: approximately `4.19° / 0.002u`;
- R4.3-B surface hotspot at `u = 0.999`: approximately `7.48°` over the available near-pole span.

This means the remaining defect cannot be assigned to the OPPOSITE / LOWER penultimate relation alone. The current evidence now points to a mixed termination-construction question: endpoint axis tangent contribution plus the analytic single-pole collapse of the asymmetric cross-section.

## Decision

No R4.3 variant is selected.

Classification:

`BOUNDED_PROFILE_RELATION_VARIATION_INSUFFICIENT`

Interpretation:

1. R4.2 correctly identified an OPPOSITE / LOWER convergence component.
2. R4.3 proves that bounded correction of that component lowers the analytic turn but does not remove the visual pinch.
3. Stronger changes progressively widen the termination and therefore cannot be justified as a direct repair.
4. The remaining termination must be diagnosed at the **construction relationship** level rather than by continuing point-by-point profile tuning.

## Next Legal Action

`R4.4 diagnostic-only termination construction sufficiency probe`

R4.4 must make no authoritative Source edit. It should isolate, as diagnostic counterfactuals only:

- current full Working Source;
- GRIP_AXIS endpoint-tangent contribution;
- cross-section / single-pole-collapse contribution;
- their interaction near `u = 0.95–1.0`.

Only if that isolation proves one relation dominant may a new bounded Source-level correction be introduced. If neither existing relation can remove the visual defect without broad shape damage, the project may justify a new **sparse explicit termination-cap relation** at Source level; it must not become a mesh-local patch or hidden sculpt degree of freedom.

## Authority Boundary

- `INTERFACE RELATION = CONFIRMED / LOCKED`
- `TERMINATION ENVELOPE = 0.34 / LOCKED`
- `R4.3 PROFILE VARIANTS = ALL REJECTED`
- `RIGHT / FRONT TERMINATION = REVISE / CONSTRUCTION OWNERSHIP NOT YET CLOSED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.
