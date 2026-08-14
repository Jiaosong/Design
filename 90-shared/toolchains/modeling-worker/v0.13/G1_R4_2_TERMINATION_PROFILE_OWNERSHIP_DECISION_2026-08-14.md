# G1 R4.2｜Termination Profile-Convergence Ownership Decision｜2026-08-14

## Decision State

`OPPOSITE_LOWER_PROFILE_CONVERGENCE_RELATION_SUSPECTED / DIAGNOSTIC_OWNERSHIP_CLASSIFIED / SOURCE_UNCHANGED / CANDIDATE_PROMOTION_NOT_RUN`

R4.2 performs no Source edit and no mesh generation. It decomposes the exact confirmed Working Source into profile-amplitude convergence, sector normal-turn, full angular hotspot, and GRIP_AXIS tangent rotation near the termination.

This is routing evidence only. It authorizes a bounded Source-level experiment on the identified existing profile relationship; it does not authorize Candidate Promotion, Canonical Promotion, Class-A, engineering CAD, manufacturing validation or Release.

## Evidence Identity

Execution head:

`8cb9e7ca8241de1d204d929e49280d3e0e88bc36`

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.2 Termination Profile Ownership`
- run `31801400152`
- result `SUCCESS`

Artifact:

- ID `9219421087`
- SHA-256 `825c52cb193ef0cb87a3a3950f4485c8714263c46403aa698bf9ce935dcb8ae7`
- size `4,880 bytes`

## Source Lock

The probe uses:

- confirmed R3 interface relation unchanged;
- termination envelope exponent fixed at `0.34`;
- no control-point edit;
- no topology / mesh dependency;
- Source digest unchanged before / after analysis.

## Main Measurements

- pre-cap maximum surface normal turn (`u <= 0.98`): `0.6494460683636728°`
- near-pole maximum surface normal turn (`u >= 0.995`): `7.896415221255525°`
- near-pole maximum GRIP_AXIS tangent turn: `1.8956786866011623°`
- near-pole maximum OPPOSITE-side relative-convergence derivative to PALM: `33.4956781920013 / u`

The surface termination turn is therefore materially larger than the GRIP_AXIS tangent rotation in the same near-pole region.

## Sector / Hotspot Routing

At `u = 0.995`:

- hotspot `theta = 252.5°`
- max surface turn `1.8930147062°`
- sector turns: TOP `0.5192°`, THUMB `0.9000°`, LOWER `1.2461°`, OPPOSITE `1.7864°`

At `u = 0.998`:

- hotspot `theta = 240.0°`
- max surface turn `4.7899986813°`
- sector turns: TOP `1.5429°`, THUMB `2.4006°`, LOWER `3.9510°`, OPPOSITE `4.2881°`

At `u = 0.999`:

- hotspot `theta = 232.5°`
- max surface turn `7.8964152213°`
- sector turns: TOP `3.9085°`, THUMB `5.0354°`, LOWER `7.2406°`, OPPOSITE `7.1762°`

The full angular hotspot stays in the OPPOSITE→LOWER quadrant as the surface approaches the pole.

## Relative Profile Convergence

`OPPOSITE_SIDE_PLAN` is the fastest profile to converge toward the PALM amplitude ratio near the endpoint.

Relative-ratio derivative to PALM:

- `u = 0.995`: THUMB `10.8527`, OPPOSITE `18.6639`, LOWER `6.2524`
- `u = 0.998`: THUMB `16.5807`, OPPOSITE `28.4565`, LOWER `9.5026`
- `u = 0.999`: THUMB `19.5285`, OPPOSITE `33.4957`, LOWER `11.1749`

This aligns with the local normal-field hotspot: the strongest relation change is not distributed equally across all four profile families.

## Decision

Classification:

`OPPOSITE_LOWER_PROFILE_CONVERGENCE_RELATION_SUSPECTED`

All four routing checks pass:

1. near-pole hotspots remain in the OPPOSITE→LOWER quadrant;
2. OPPOSITE_SIDE_PLAN has the fastest relative convergence to PALM;
3. OPPOSITE or LOWER sector normal-turn dominates TOP / THUMB near the pole;
4. surface hotspot turn exceeds GRIP_AXIS tangent turn.

Therefore the next legal Source re-entry is the existing **OPPOSITE / LOWER terminal profile relationship**, not GRIP_AXIS, not the shared envelope exponent, and not topology.

## Existing Relation to Re-enter

Current R2 penultimate profile controls:

- `PALM_PROFILE[4] = 0.058`
- `THUMB_SIDE_PLAN[4] = 0.044`
- `OPPOSITE_SIDE_PLAN[4] = 0.034`
- `LOWER_RETURN_PROFILE[4] = 0.050`

All profiles then terminate at raw endpoint control value `0.003` before the shared envelope collapses the cross-section to the pole.

The large OPPOSITE-side gap at the penultimate control is consistent with the measured rapid relative catch-up near the endpoint. R4.3 may therefore test bounded changes to the existing OPPOSITE / LOWER penultimate controls only.

## Next Legal Action

`R4.3 bounded OPPOSITE / LOWER terminal-profile relation batch → existing Machine QA → source-space sector probe → fixed termination Strip/Grazing/Zebra → visual decision`

R4.3 must:

- retain the confirmed interface relation;
- retain exponent `0.34`;
- retain GRIP_AXIS / PALM / THUMB unchanged;
- modify only existing profile control points, through Blender-native Source objects;
- restore the native Source after each diagnostic batch;
- render each passing direction independently;
- use visual judgment, not lowest analytic turn, as the final design layer.

## Authority Boundary

- `INTERFACE RELATION = CONFIRMED / LOCKED`
- `TERMINATION ENVELOPE = 0.34 / NATIVE / LOCKED FOR R4.3`
- `TERMINATION OWNERSHIP = OPPOSITE / LOWER PROFILE CONVERGENCE SUSPECTED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.
