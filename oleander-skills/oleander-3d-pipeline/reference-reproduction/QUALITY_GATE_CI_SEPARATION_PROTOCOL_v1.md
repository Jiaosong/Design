# OLEANDER 3D Pipeline — Quality Gate / CI Separation Protocol v1

A design candidate that is correctly generated, measured and rejected is a **successful verification run**, not a broken pipeline.

Core separation:

`CI / EXECUTION PASS ≠ REFERENCE FIDELITY PASS ≠ DESIGN KEEP`

## CI SUCCESS may mean
- runtime executed deterministically;
- native asset persisted;
- evidence/diagnostics persisted;
- Source integrity checks passed;
- validators accepted receipt structure/provenance;
- quality result was correctly recorded as PASS / REVISE / REJECT / HOLD.

## CI FAILURE is reserved for
- runtime crash;
- missing artifact/evidence;
- invalid receipt/provenance;
- Source mutation when forbidden;
- invalid diagnostic mask;
- dishonest/inconsistent declared result;
- promotion attempted despite unmet gate.

## Promotion / quality workflows
A separate promotion condition may require `REFERENCE_FIDELITY_REVIEW_KEEP` or `DESIGN_QUALITY_KEEP`. Failing that condition must not rewrite the underlying execution evidence as if the toolchain crashed.

## V17 transfer
V17 correctly produced the Blender candidate and masks, but mask contamination caused an invalid diagnostic. That is a CI failure. In contrast, once V18 mask validity is proven, a genuine projection mismatch will be stored as `PROJECTION_MACHINE_SCREENING_FAIL` while the verification workflow can still succeed.
