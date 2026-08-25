# G1 R4.5.1B｜Same-DOF Cap Scale Refinement Decision｜2026-08-17

## Decision

`MACHINE_PASS / VISUAL_SELECT_SCALE_0_86_FOR_EXACT_CONFIRMATION / WORKING_SOURCE / CANDIDATE_REVIEW_REOPENED / CANDIDATE_PROMOTION_NOT_RUN`

This receipt selects `termination_cap_pole_curvature_scale = 0.86` for exact confirmation only. It does not confirm the relation and does not promote authority.

## Evidence

Workflow:
- `OLEANDER Modeling Worker v0.13 R4.5.1B Cap Scale Refinement`
- run `31991222377` = `SUCCESS`
- head `59ed4735a1ed7cc93d1725ff1f4a8893837a9afc`

Artifact:
- ID `9275437893`
- digest `sha256:49a74af4d8b3caa250c4eee431a23069429cc2175130798ac960c0101ec2169b`
- size `3,605,887 bytes`

Locked relation context:
- `termination_cap_onset_u = 0.88`
- confirmed R3 interface locked
- shared termination envelope exponent `0.34` locked
- Source owner remains `LOWER_RETURN_PROFILE`
- total cap relation numeric DOFs = `2`
- no third DOF, Source family, profile/axis control edit or mesh patch

## Machine Comparison

### 0.90 control — PASS / prior visual REVISE
- sparse authority scalars `50`
- onset normal continuity `0.0500794049°`
- cap-region max normal turn `2.5823917602°`
- near-pole max normal turn `1.8993818618°`
- concentration ratio `1.3595958834`
- interface regression `0.0 m`
- radial violations `0 / 0`

### 0.88 — PASS
- sparse authority scalars `50`
- onset normal continuity `0.0500921927°`
- cap-region max normal turn `2.4197534019°`
- near-pole max normal turn `1.9447264652°`
- concentration ratio `1.2442641396`
- interface regression `0.0 m`
- radial violations `0 / 0`

### 0.86 — PASS / selected for exact confirmation
- sparse authority scalars `50`
- onset normal continuity `0.0501049806°`
- cap-region max normal turn `2.2879481523°`
- near-pole max normal turn `1.9922871699°`
- concentration ratio `1.1484027940`
- interface regression `0.0 m`
- radial violations `0 / 0`
- exact closure retained
- Blender-native scale roundtrip retained

The `.86` candidate is close to the fixed near-pole hard gate `2.0°` but remains inside it. That gate is not relaxed.

## Visual Comparison

Compared under the same `100 mm` local inspection camera and shared Surface System Broad / Strip / Grazing / Zebra:

- `.86` produces the smallest remaining Broad terminal dimple;
- `.86` produces the smallest/least detached Strip terminal oval;
- `.86` produces the weakest Grazing terminal island;
- `.86` produces the weakest localized Zebra lower hook of the tested `.86/.88/.90` set;
- no new onset kink is visible;
- no obvious pointed-pole failure is visible at this diagnostic resolution.

Because near-pole Machine margin is narrow, `.86` must be replayed at exact-confirmation resolution and persisted as an active Blender-native Working Source before any confirmation decision.

## Next Legal Action

`R4.5.1B exact .86 confirmation → 768px Broad / Strip / Grazing / Zebra → native Source readback → .blend persistence → Human Visual decision`

Confirmation stage is parameter-frozen:
- onset `.88`
- pole-curvature scale `.86`
- interface relation locked
- envelope exponent `.34`
- all existing Source controls locked

Any exact-confirmation visual pinch, terminal island/hook, onset kink or Machine regression returns to REVISE. No parameter tuning is allowed inside confirmation.

## State
- `DESIGN STATE = REVISE / EXACT_CONFIRMATION_PENDING`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current Canonical Authority.

No Candidate Authority, Canonical Promotion, Class-A, engineering CAD, manufacturing/tooling, ergonomic comfort, final CMF or Release is established.
