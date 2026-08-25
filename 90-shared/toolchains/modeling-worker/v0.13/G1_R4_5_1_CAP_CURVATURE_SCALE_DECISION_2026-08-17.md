# G1 R4.5.1｜Sparse Cap Pole-Curvature Scale Decision｜2026-08-17

## Decision

`MACHINE_PASS / VISUAL_REVISE / SAME_DOF_REFINEMENT_AUTHORIZED / WORKING_SOURCE / CANDIDATE_REVIEW_REOPENED / CANDIDATE_PROMOTION_NOT_RUN`

R4.5.1 validates the second sparse Source-level numeric DOF `termination_cap_pole_curvature_scale`, owned by the existing `LOWER_RETURN_PROFILE`. The DOF materially reduces the isolated terminal-cap reflection organization found in R4.5, while preserving the confirmed interface, onset `.88`, envelope exponent `.34`, exact closure and Blender-native roundtrip.

No R4.5.1 scale is confirmed by this receipt.

## Evidence

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.5.1 Cap Curvature Scale`
- run `31990720573` = `SUCCESS`
- head `b5299e65e417e5d01fc14c556a8873af4005f535`

Artifact:

- ID `9275287632`
- digest `sha256:1ce7bdfd8d0e73a4b2e0a9a55752ed35d5e4420ab87038aa89fee61961b2fbf9`
- size `3,432,675 bytes`

All global checks passed:

- authorization receipt bound;
- total numeric relation DOFs = `2`;
- onset locked at `.88`;
- existing `LOWER_RETURN_PROFILE` remains Source owner;
- native scale roundtrip = PASS;
- shared Blender Surface System runtime = PASS;
- derived geometry remains non-authoritative;
- native Source restores exactly after batch;
- Candidate Promotion = `NOT_RUN`.

## Machine Results

All explicit scale candidates carry `50` sparse authority scalars.

### SCALE_A_0_90 — PASS / machine preferred

- onset normal continuity = `0.0500794049°`
- confirmed-interface regression = `0.0 m`
- cap-region max normal turn = `2.5823917602°`
- near-pole max normal turn = `1.8993818618°`
- reflection-flow concentration ratio = `1.3595958834`
- radial monotonic violations = `0 / 0`
- closure error = `0.0 m`

### SCALE_B_0_92 — PASS

- cap-region max normal turn = `2.7668281354°`
- near-pole max normal turn = `1.8561021067°`
- concentration ratio = `1.4906659097`

### SCALE_C_0_94 — PASS

- cap-region max normal turn = `2.9587181756°`
- near-pole max normal turn = `1.8147493962°`
- concentration ratio = `1.6303728668`

### SCALE_D_0_96 — FAIL

- cap-region max normal turn = `3.1583485017°`
- near-pole max normal turn = `1.7751979140°`
- concentration ratio = `1.7791528916` > gate `1.75`

Machine ranking: `.90 → .92 → .94`.

## Visual QA

Decision: `REVISE`.

Compared with the rejected R4.5 scale `1.0` reference:

- `.90` gives the strongest useful change and is visually best of this batch;
- Broad terminal dimple/patch is reduced;
- Strip/Grazing terminal island is smaller and less detached;
- Zebra lower hook is reduced;
- `.92` and `.94` progressively return toward the rejected scale `1.0` organization.

However `.90` still fails the explicit visual gate:

1. Strip still closes into a readable compact terminal oval distinct from the broader body reflection field.
2. Grazing still shows a localized terminal crescent/island.
3. Broad still reads a localized terminal patch rather than a completely integrated tail-to-cap volume.
4. Zebra still retains a localized lower hook, though materially weaker than scale `1.0`.

Therefore `SCALE_A_0_90` is **not** confirmed.

## Same-DOF Refinement Authorization

The current evidence does **not** justify a third Source DOF. Machine trend is monotonic in the useful direction as pole-curvature scale decreases, while near-pole turn increases toward the existing `2.0°` hard gate. The next valid experiment is therefore a narrower search inside the already-authorized second DOF.

Authorized bounded values:

- `.86`
- `.88`
- `.90` retained as comparison/control

No other parameter may change.

The same Machine gates remain fixed. In particular:

- near-pole max normal turn remains `≤2.0°`;
- cap-region max normal turn remains `≤3.2°`;
- concentration ratio remains `≤1.75`;
- interface regression remains `0` within declared tolerance;
- onset `.88`, interface relation and envelope exponent `.34` remain locked.

## Current State

- `R4.4 structural cause = CLOSED`
- `R4.5 onset DOF = METHOD PASS / VISUAL REVISE`
- `R4.5.1 pole-curvature-scale DOF = METHOD PASS / FIRST BATCH VISUAL REVISE`
- `R4.5.1B same-DOF refinement = AUTHORIZED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current Canonical Authority.

No Candidate Authority, Canonical Promotion, Class-A, engineering CAD, manufacturing/tooling, ergonomic comfort, final CMF or Release is established here.
