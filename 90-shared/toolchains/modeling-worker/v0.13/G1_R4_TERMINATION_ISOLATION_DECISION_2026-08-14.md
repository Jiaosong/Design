# G1 R4｜Termination Source vs Pole-Topology Isolation Decision｜2026-08-14

## Decision State

`TERMINATION_TOPOLOGY_INVARIANT_SOURCE_ENVELOPE_RELATION_SUSPECTED / REVISE / WORKING_SOURCE / CANDIDATE_PROMOTION_NOT_RUN`

This receipt records the bounded termination isolation after the interface relation was confirmed and locked.

The decision concerns only the open `RIGHT / FRONT TERMINATION` pinch / crease-like convergence. It is diagnostic routing evidence, not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Evidence Identity

Execution head:

`79ff421970080d3f956028b82b8448a333f9a435`

Workflow:

- `OLEANDER Modeling Worker v0.13 R4 Termination Isolation`
- run `31799721739`
- result `SUCCESS`

Artifact:

- ID `9218832715`
- name `oleander-modeling-worker-v0-13-g1-r4-termination-31799721739`
- SHA-256 `79704858bd9bb21b44a0bb493f7d157362aba3d24db45bf1cc7b44b340cca01a`
- size `2,997,767 bytes`

Confirmed interface relation remained locked during R4. The same termination Source was used for all topology variants.

## Same-Source Topology Isolation

Working Source digest for all variants:

`7cc3bf7ba0d6cf30d8f24d79912a6eb6a821761926a8a5aa5d74519e08640b91`

### Baseline

- `56 × 72`
- vertices `4,034`
- faces `4,104`
- last uniform ring `u = 0.9824561403508771`
- authority `DERIVED_EXECUTION_NOT_AUTHORITY`

### Dense

- `112 × 144`
- vertices `16,130`
- faces `16,272`
- last uniform ring `u = 0.9911504424778761`
- authority `DERIVED_EXECUTION_NOT_AUTHORITY`

### Pole-refined

- baseline circumferential sampling retained;
- extra analytic rings at `u = 0.99 / 0.995 / 0.998 / 0.9995`;
- vertices `4,322`
- faces `4,392`
- final sampled ring `u = 0.9995`;
- authority `DERIVED_EXECUTION_NOT_AUTHORITY`.

## Fixed Local Visual A/B/C

The right/front pinch remains visually in the same location and with the same overall reflection structure in baseline, dense and pole-refined diagnostics.

### Dense vs baseline

STRIP:
- mean absolute RGB `0.0005111506672074029`
- p99 `0.007`

GRAZING:
- mean absolute RGB `0.0009646172397454696`
- p99 `0.023`

ZEBRA:
- mean absolute RGB `0.0005821557425978578`
- p99 `0.007`

### Pole-refined vs baseline

STRIP:
- mean absolute RGB `0.00019749221913230032`
- p99 `0.0`

GRAZING:
- mean absolute RGB `0.0000023456649050028015`
- p99 `0.0`

ZEBRA:
- mean absolute RGB `0.000002272263223327779`
- p99 `0.0`

The pole-refined variant samples the analytic surface much closer to the endpoint yet does not materially reorganize the local Grazing or Zebra reading. Therefore the current evidence does not support endpoint tessellation density or the last pole-fan sampling as the primary cause of the retained pinch.

## Topology-Independent Source-Space Pole Probe

Current shared termination envelope exponent:

`0.34`

At `u = 0.90`:
- mean ring radius `0.014858376136614745 m`
- max normal turn over `0.002u` = `0.5069504010089578°`

At `u = 0.98`:
- mean ring radius `0.00283326303082109 m`
- max normal turn over `0.002u` = `0.6494467423938026°`

At `u = 0.995`:
- mean ring radius `0.0009946154641317742 m`
- max normal turn over `0.002u` = `1.8930130278993391°`

At `u = 0.998`:
- mean ring radius `0.0006126682176447362 m`
- max normal turn over `0.002u` = `4.789988180959502°`

At `u = 0.999`:
- mean ring radius `0.00045344910479259065 m`
- max normal turn over the available `0.0019u` span = `7.8963944467948775°`

The near-pole maximum is therefore more than twelve times the maximum measured at `u <= 0.98` in the same topology-independent probe.

## Decision

Classification:

`TERMINATION_TOPOLOGY_INVARIANT_SOURCE_ENVELOPE_RELATION_SUSPECTED`

Interpretation:

1. Local termination reflection structure is essentially invariant under a roughly fourfold uniform topology increase.
2. Adding analytic rings all the way to `u = 0.9995` also leaves Grazing and Zebra virtually unchanged.
3. The exact same Working Source is used across those variants.
4. The analytic Source field shows rapidly increasing normal rotation only as the cross-section collapses toward the pole.
5. Therefore the next legal re-entry is the **termination Source relation**, not a mesh-local pole repair.

## Authority Gap Exposed

The current implementation stores `termination_envelope_exponent` under `LOWER_RETURN_PROFILE`, but `g1_r2_core.point()` uses that one value to scale **PALM_PROFILE, THUMB_SIDE_PLAN, OPPOSITE_SIDE_PLAN and LOWER_RETURN_PROFILE together**.

Therefore it is functionally a shared cross-section termination relation, not merely a lower-return curve detail.

More importantly, the current Blender-native `OL_SRC_LOWER_RETURN_PROFILE` object and `extract_native_source()` roundtrip do not yet persist/read back this exponent as an editable native Source relation. R4.1 must close that Authority gap before testing exponent variants.

The fix must keep the existing six Source objects; no seventh Source family or new geometric degree of freedom is required. The exponent should become an explicit native property on `OL_SRC_LOWER_RETURN_PROFILE` with semantics identifying its shared termination-envelope effect, and it must enter the numeric snapshot/digest/roundtrip checks.

## Next Legal Action

`Blender-native termination-relation authority closure → bounded Source-level termination-envelope variants → existing Machine QA + pole probe → fixed local Strip/Grazing/Zebra → visual decision`

Forbidden:

- no mesh-local pole smoothing;
- no hidden sculpt correction;
- no topology promotion;
- no reopening the confirmed interface relation unless a termination variant causes a measured regression;
- no Candidate or Canonical Promotion.

## Current Boundary

- `INTERFACE RELATION = CONFIRMED / LOCKED FOR TERMINATION WORK`
- `RIGHT / FRONT TERMINATION = REVISE / SOURCE RELATION SUSPECTED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.
