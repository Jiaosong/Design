# Automotive v0.11｜R29 HP Rebaseline Decision

Status: `R25 HP-CORRECT BASELINE RETAINED / R28A-C SUPERSEDED EXPLORATION / M5 REVISE`

## Why this decision was required

Earlier Human M5 reviews from R24 onward used a visible wheel implementation whose world-space tire envelope did not satisfy the locked M1 wheel hard point. The raw display/package wheel measured approximately 0.710 m in X and 1.0792 m in Z while the locked target OD is 0.700 m.

The wheel implementation was therefore corrected diagnostically, without changing Source body geometry, to an exact world-space X/Z envelope of approximately 0.700 m × 0.700 m while preserving wheel centers and Y thickness.

Because that implementation bug contaminated earlier wheel/body visual judgments, R25 and R28A were re-rendered under the same corrected wheel package before choosing the next Source architecture.

## A/B evidence

Run: `31617460813`

### R25 HP rebaseline
- artifact `9149881518`
- `MACHINE_PASS_VISUAL_REVIEW_REQUIRED`
- Source hash locked
- one Source island
- 4 termination triangles / 0 n-gons
- corrected wheel package exact

### R28A HP rebaseline
- artifact `9149881583`
- `MACHINE_PASS_VISUAL_REVIEW_REQUIRED`
- Source hash locked
- one Source island
- 4 termination triangles / 0 n-gons
- corrected wheel package exact

## Human M5 comparison

With the same corrected 0.700 m wheel package:

- R25 keeps a materially cleaner broad fender/body surface in Hero, Strip and Grazing views.
- R25 still has a cap-like local crown and fore/aft pinching around the wheel opening, so it is not M5 PASS.
- R28A introduces a more severe local surface defect: repeated transverse/radial corrugation in Grazing plus folded/sliver surfaces in front and rear arch detail.
- R28B crown inset and R28C zero-bulge tests did not remove the R28 local ridge, confirming that continued patch accumulation is not justified.

## Decision

Return to the simpler R25 Source architecture as the current HP-correct design baseline.

R28A, R28B and R28C are retained as evidence that the full U-boundary local patch architecture is not superior under the corrected package. They are `SUPERSEDED / AUDIT_ONLY`, not promoted Source authority.

The next revision is **R29｜HP-Correct Monotonic Nested Arch**.

R29 must remain a minimal wheel-zone M4 revision:
- keep R25 longitudinal/shared-endpoint Source topology;
- keep R25 rounded x-z opening target;
- use the corrected 0.700 m wheel package in all canonical evidence;
- fix only the non-monotonic vertical ordering of `CROWN → B1 → B2 → INNER` that currently overshoots above the inner wheel-opening boundary;
- do not reintroduce R27 circumferential attachment systems or R28 full-window patching;
- no Boolean / global SubD / n-gon;
- M6/M7/M8 remain blocked until Human M5 PASS.
