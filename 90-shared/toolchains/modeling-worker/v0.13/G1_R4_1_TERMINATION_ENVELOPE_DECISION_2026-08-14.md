# G1 R4.1｜Native Termination-Envelope Visual Decision｜2026-08-14

## Decision State

`SHARED_ENVELOPE_EXPONENT_VARIATION_INSUFFICIENT / TERMINATION_PROFILE_RELATION_REENTRY_REQUIRED / REVISE / WORKING_SOURCE / CANDIDATE_PROMOTION_NOT_RUN`

R4.1 tested the existing Blender-native `termination_envelope_exponent` relation after first closing its native Source ownership / readback / restore gap. None of the three bounded variants is accepted as the current termination correction.

This is a design-routing decision only. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Evidence Identity

Execution head:

`31d3dc7090d0974867d5126b89bae4e14e836061`

Workflow:

- `OLEANDER Modeling Worker v0.13 R4.1 Termination Envelope Batch`
- run `31800715037`
- result `SUCCESS`

Artifact:

- ID `9219241743`
- name `oleander-modeling-worker-v0-13-g1-r4-1-31800715037`
- SHA-256 `8f0ea7e46d4529ad2fe29b983830a596860661d1823a81a16815e782b2f2b7c1`
- size `3,924,882 bytes`

## Native Relation Authority Closure

Before variant testing, `termination_envelope_exponent` was made an explicit editable/readable Blender-native relation property on the existing `OL_SRC_LOWER_RETURN_PROFILE` Source object with semantics:

`SHARED_CROSS_SECTION_TERMINATION_ENVELOPE`

No seventh Source family was added.

The controlled native relation edit test:

- changed exponent by `+0.02`;
- changed only the `LOWER_RETURN_PROFILE` numeric Source family;
- produced derived-surface displacement `0.00043989202386365833 m`;
- restored every Source family to `0.0` error;
- passed native readback / rebuild / restore.

The full R2 Blender Bridge also re-ran successfully after this Authority change, including saved `.blend` reopen and native rebuild.

## Baseline

Current shared termination envelope:

`sin(pi*u)^0.34`

Source-space pole probe:

- pre-cap max normal turn (`u <= 0.98`): `0.6494467423938026°`
- near-pole max (`u >= 0.995`): `7.8963944467948775°`

The R4 topology isolation already established that this near-pole convergence is not materially reorganized by uniformly dense or pole-refined execution topology.

## R4.1 Professional Source-Relation Batch

### A｜E030 Minor Soften

`termination_envelope_exponent = 0.30`

- Machine QA: PASS
- dimensions: `0.1900 × 0.0807994 × 0.0996853 m`
- pre-cap max normal turn: `0.66767416°`
- near-pole max: `6.95832663°`

Visual difference vs E034:

- Strip mean RGB `0.00497446`, p99 `0.074`
- Grazing mean RGB `0.00423211`, p99 `0.058`
- Zebra mean RGB `0.00194664`, p99 `0.082`

Visual decision: the endpoint field changes slightly, but the right/front convergence remains. The improvement is insufficient to justify a Source correction.

### B｜E026 Balanced Soften

`termination_envelope_exponent = 0.26`

- Machine QA: PASS
- dimensions: `0.1900 × 0.0808382 × 0.0997576 m`
- pre-cap max normal turn: `0.68136931°`
- near-pole max: `6.23535083°`

Visual difference vs E034:

- Strip mean RGB `0.01012367`, p99 `0.231`
- Grazing mean RGB `0.00825455`, p99 `0.137`
- Zebra mean RGB `0.00397306`, p99 `0.125`

Visual decision: the dark termination field broadens and the cap becomes fuller, but the core Zebra convergence remains. This redistributes the defect rather than solving it.

### C｜E022 Strong Soften

`termination_envelope_exponent = 0.22`

- Machine QA: PASS
- dimensions: `0.1900 × 0.0808842 × 0.0998300 m`
- pre-cap max normal turn: `0.68979766°`
- near-pole max: `5.68653021°`

Visual difference vs E034:

- Strip mean RGB `0.01548259`, p99 `0.513`
- Grazing mean RGB `0.01200035`, p99 `0.231`
- Zebra mean RGB `0.00605670`, p99 `0.125`

Visual decision: the analytic near-pole metric improves most, but the cap becomes materially fuller while the problematic bent / convergent Zebra structure remains. Metric improvement is therefore not equivalent to design improvement.

## Decision

None of `E030 / E026 / E022` is selected.

Classification:

`SHARED_ENVELOPE_EXPONENT_VARIATION_INSUFFICIENT`

Interpretation:

1. Lowering the shared exponent monotonically reduces the near-pole source-space normal-turn maximum.
2. The local Strip / Grazing / Zebra convergence does **not** disappear correspondingly.
3. Stronger exponent changes increasingly modify the whole cap fullness and reflection field.
4. Therefore the single shared envelope scalar is not sufficient to correct the retained termination defect.
5. Continuing to optimize this scalar would over-change the global termination while leaving the core convergence pattern unresolved.

## Next Legal Action

`R4.2 topology-independent profile-convergence ownership probe`

R4.2 must make **no Source edit**. It must determine which existing relation actually owns the remaining termination convergence by measuring:

- post-envelope `PALM_PROFILE / THUMB_SIDE_PLAN / OPPOSITE_SIDE_PLAN / LOWER_RETURN_PROFILE` amplitudes near the endpoint;
- their longitudinal decay rates and relative-rate divergence;
- sector-specific normal turn at top / thumb / lower / opposite sectors;
- full angular hotspot location as `u → 1`;
- `GRIP_AXIS` tangent rotation as a separate reference.

Only after that ownership probe may a bounded Source-level profile relation batch be defined.

Forbidden:

- no further exponent micro-tuning;
- no mesh-local pole smoothing;
- no control-point edit before ownership is identified;
- no reopening the confirmed interface relation;
- no Candidate or Canonical Promotion.

## Authority Boundary

- `INTERFACE RELATION = CONFIRMED / LOCKED`
- `TERMINATION ENVELOPE AUTHORITY = NATIVE ROUNDTRIP CLOSED`
- `RIGHT / FRONT TERMINATION = REVISE / PROFILE-RELATION OWNERSHIP UNKNOWN`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`
- v0.12 remains current promoted canonical authority.
