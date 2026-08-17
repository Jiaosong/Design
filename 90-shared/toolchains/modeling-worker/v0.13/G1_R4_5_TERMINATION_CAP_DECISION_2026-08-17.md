# G1 R4.5｜Explicit Sparse Termination-Cap Relation Decision｜2026-08-17

## Decision State

`MACHINE_PASS / EXACT_CONFIRMATION_EXECUTED / VISUAL_REVISE / ONE_DOF_ONSET_ONLY_INSUFFICIENT / WORKING_SOURCE / CANDIDATE_REVIEW_REOPENED / CANDIDATE_PROMOTION_NOT_RUN`

R4.5 successfully replaces the structurally insufficient distributed single-pole collapse with an explicit sparse Source-level cap relation. It proves that cap onset can be encoded, round-tripped and executed without a seventh Source family or mesh-local patch. However, the exact selected one-DOF relation does **not** yet satisfy the OLEANDER visual-quality gate.

No R4.5 cap variant is confirmed as current Working Source by this receipt.

## Batch Evidence

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.5 Termination Cap Relation`
- run `31989064902`
- result `SUCCESS`

Artifact:

- ID `9274847245`
- SHA-256 `ef85b8e1b4edd3c2c40cb558fff48db80495d82e512443d37bfd2f2c3f72f733`
- size `3,012,246 bytes`

Machine gate:

- `CAP_A_0_88` = PASS
- `CAP_B_0_89` = PASS
- `CAP_C_0_90` = FAIL / cap-region normal-turn
- `CAP_D_0_92` = FAIL / cap-region + near-pole normal-turn

### CAP_A_0_88

- sparse authority scalars = `49`
- onset position continuity error = `0.0 m`
- onset normal continuity = `0.0500154657°`
- confirmed-interface regression = `0.0 m`
- cap-region max normal turn = `3.5820125971°`
- near-pole max normal turn = `1.7013968684°`
- radial mean/max monotonic violations = `0 / 0`
- closure error = `0.0 m`
- native cap-relation roundtrip = PASS

### CAP_B_0_89

- cap-region max normal turn = `3.8972479540°`
- near-pole max normal turn = `1.7867356887°`

A was therefore selected for exact confirmation because it retained more fairness margin than B. This selection did not authorize confirmation or promotion.

## Exact Confirmation Evidence

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.5 Cap A Confirmation`
- run `31989922416`
- result `SUCCESS`

Artifact:

- ID `9275030125`
- SHA-256 `5a4f6f2cf18b560a7071ebeb15a5c1e9711bed732c5307b610d769c0d14971c2`
- size `3,658,525 bytes`

Native Working Source artifact:

- `OLEANDER_G1_R4_5_CAP_A_WORKING_SOURCE__v0_13.blend`
- SHA-256 `e46b46689116277734a4d5c6cf4d30844b30c987da49543e6400b9855898c024`
- live Source digest `24950e80163346e6d3b7101a763c1218ca64467e020782b028fdc2728546a210`

Exact confirmation checks all passed:

- selected onset `0.88` exact;
- confirmed R3 interface exact and locked;
- termination envelope exponent remains `0.34`;
- Machine gate PASS;
- Blender-native cap onset roundtrip PASS;
- native readback digest exact;
- six Source families retained;
- derived mesh remains non-authoritative;
- saved `.blend` retains the cap relation active;
- Broad / Strip / Grazing / Zebra exact-confirmation renders written;
- Candidate Promotion remains `NOT_RUN`.

## Exact Visual QA

Decision: `REVISE`.

### Improvement retained

Compared with the R4.4 baseline, CAP_A removes the previous long, concentrated right/front termination convergence from most of the tail. There is no visible onset kink, and the silhouette stays continuous. The new Source relation therefore addresses the **structural cause** diagnosed by R4.4.

### New failure exposed by exact Broad + fixed reflection rigs

The terminal field now reads as a locally appended cap rather than one continuous low-frequency surface flow:

1. **Broad** shows a distinct localized circular/elliptical terminal patch instead of a fully integrated tail-to-cap volume.
2. **Strip** closes into a compact high-contrast oval separated from the broader body reflection flow.
3. **Grazing** repeats the isolated terminal crescent/oval organization.
4. **Zebra** forms a localized hook / loop at the lower terminal field.

These features repeat across independent diagnostics and therefore cannot be classified as a single-light artifact.

The problem is not onset continuity: measured onset normal discontinuity is only `0.0500°`. The problem is the **pole-curvature target of the fixed cap law**. The current law derives a symmetric endpoint ellipse directly from the full onset pair means, which leaves too much terminal curvature amplitude and makes the cap visually discrete.

## Relation Sufficiency Decision

Final R4.5 classification:

`ONE_DOF_ONSET_ONLY_INSUFFICIENT_FOR_PROFESSIONAL_REFLECTION_FLOW`

R4.5 proves one useful DOF:

`termination_cap_onset_u`

but exact visual evidence now justifies one additional minimal Source-level DOF:

`termination_cap_pole_curvature_scale`

This is **not** permission to add more Source families, profile control points, sculpt fields or mesh-local corrections. It only controls the magnitude of the symmetric pole-curvature ellipse already required by the cap law; its aspect ratio remains derived from the onset pair means.

## R4.5.1 Authorization Boundary

Next exploration:

`R4.5.1｜Sparse Cap Pole-Curvature Scale`

Allowed:

- retain `termination_cap_onset_u = 0.88` as the selected onset;
- add exactly one numeric `termination_cap_pole_curvature_scale` on the existing `LOWER_RETURN_PROFILE` Source owner;
- keep endpoint ellipse aspect ratio derived from onset `mean(THUMB,OPPOSITE) : mean(TOP,LOWER)`;
- test a bounded professional scale range;
- extend Machine gate with cap normal-turn distribution / near-pole / radial monotonicity / interface zero-regression;
- only Machine-PASS variants enter exact shared Surface System Broad / Strip / Grazing / Zebra.

Forbidden:

- moving onset earlier than the confirmed interface outer bound;
- changing confirmed interface;
- changing envelope exponent `0.34`;
- changing profile/axis controls;
- seventh Source family;
- per-vertex/dense control;
- mesh-local cosmetic patch;
- hidden sculpt correction;
- Candidate Promotion.

## Current State

- `INTERFACE RELATION = CONFIRMED / LOCKED`
- `TERMINATION ENVELOPE = 0.34 / LOCKED BODY-TAIL BASELINE`
- `R4.4 STRUCTURAL CAUSE = CLOSED`
- `R4.5 CAP ONSET RELATION = METHOD PASS / VISUAL REVISE`
- `RIGHT / FRONT TERMINATION = REVISE / R4.5.1 AUTHORIZED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.

## Next Legal Action

`R4.5.1 curvature-scale vocabulary → Blender-native Source binding → Machine fairness/closure gate → bounded scale variants → exact Broad/Strip/Grazing/Zebra → decision`

This receipt does not establish Candidate Authority, Canonical Authority, Class-A, engineering CAD, manufacturing/tooling, ergonomic comfort, final CMF or Release.
