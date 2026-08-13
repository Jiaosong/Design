# Modeling Worker v0.12｜E2 Precision Classification

Status: `MACHINE_QA_PRECISION_RECLASSIFICATION / NO DESIGN THRESHOLD RELAXATION / E2 NOT PASS YET`

## Trigger

First real E2 run `31663166342` successfully:
- replayed E1;
- passed E1 machine fairness;
- verified the recorded E1 Human M4.5 PASS receipt;
- constructed and rendered the E2 three-patch network;
- saved the E2 Blender source.

E2 then failed closed with:
`MACHINE_FAIL_REVISE_M3_M4`.

The failure was limited to the declared second-derivative seam residual:
- front runtime residual: `1.7560624912567418e-06`;
- rear runtime residual: `2.068203875171837e-06`;
- declared design threshold: `1e-06`.

All other observed E2 metrics passed their declared thresholds, including seam position, seam tangent angle, patch Jacobian, adjacent-normal jump and curvature-rate proxies.

## Classification

The E2 compiler constructs cubic Bézier seam rows analytically using:

`B0 = A3`

`B1 = 2*A3 - A2`

`B2 = 4*A3 - 4*A2 + A1`

which is the explicit parametric C2 construction used by this benchmark.

The first E2 QA implementation converted the compiled JSON/Python-float cage into Blender `mathutils.Vector` before evaluating the C2 residual. The measured `~1.8–2.1e-06` residual is therefore a **runtime representation residual**, not sufficient evidence that the compiler-space C2 relationship itself is wrong.

This classification does **not** convert the failed run into PASS. It requires a new execution.

## Required correction

Separate two evidence classes:

1. `COMPILER_C2_RESIDUAL`
   - calculated directly from the raw JSON/Python-float cage before Blender vector conversion;
   - remains subject to the original design threshold `max_second_derivative_error <= 1e-06`;
   - is the authority for whether the compiled relationship satisfies the declared C2 contract.

2. `RUNTIME_FLOAT_REPRESENTATION_RESIDUAL`
   - calculated from Blender `mathutils.Vector` evaluation;
   - retained as runtime evidence only;
   - may not replace or weaken compiler-space C2 evidence;
   - must remain within a separately declared narrow runtime representation tolerance.

The current candidate runtime tolerance is `5e-06`, chosen only to bound the already observed Blender representation scale while remaining materially below visible surface-error scales. It is **not** a replacement for the `1e-06` compiler C2 threshold.

## No-design-change rule

The precision correction must not change:
- center Control Cage;
- front/rear termination boundaries;
- C2 relationship formulas;
- design fairness thresholds;
- patch fairness thresholds;
- Human M4.5 review criteria.

If the corrected compiler-space calculation still fails, E2 must return to M3/M4.

If compiler-space C2 passes but runtime residual exceeds its separate bound, the Blender execution path must be revised before Human M4.5 review.

## Authority boundary

Until a corrected run passes both evidence classes and Human E2 M4.5 review:

`E2 = REVISE / NOT PASS`

`Modeling Worker v0.12 = SYSTEM CANDIDATE / NOT CANONICAL`
