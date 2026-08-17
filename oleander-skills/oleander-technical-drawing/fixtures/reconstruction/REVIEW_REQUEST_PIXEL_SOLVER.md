# Independent Review Request — Pixel Solver Regression

Object: `RF-CAL-01 coupled parameter solver`  
Producer state: `EXECUTED / SELF-CHECKED / REVIEW PENDING`  
Promotion: `NO SELF-KEEP`

Review the actual fixture source, solver spec/result, and generated same-renderer outputs. Do not treat CI or zero synthetic pixel difference as Design KEEP.

## Required independent checks

1. Verify that `RF-CAL-01_CANDIDATE_BAD.svg` contains the declared four mutations and no hidden raster reference.
2. Verify the solver spec exposes only bounded visual reconstruction parameters and does not expose project technical truth for optimization.
3. Verify the recorded coupled-cycle finding: a baseline solved while font size is wrong becomes invalid after the font size correction, so earlier parameters must reopen.
4. Verify the final recovered values equal the reference values under the declared CairoSVG comparison path.
5. Verify the final tolerance-zero comparison is actually zero in the synthetic fixture.
6. Verify the renderer-mismatch conclusion by comparing the Inkscape-reference / CairoSVG-candidate diagnostic provenance. Decide whether `WRONG RENDERER → WRONG OPTIMUM` is sufficiently demonstrated.
7. Confirm that the solver trace cannot silently warp the reference or candidate outside declared bounded parameters.
8. Confirm that RF-C3 remains separate from vector editability, technical truth, TD-G0…TD-G8, engineering/field state and MAIN promotion.
9. For the Water World transfer case, confirm that failure to materialize the exact remote reference bytes correctly blocks RF-C3 while allowing bounded RF-C0/RF-C1 continuation.

## Verdict format

Return one of:

- `KEEP AS RECONSTRUCTION TOOL CANDIDATE`
- `REVISE`
- `REJECT`
- `HOLD`

Then list concrete blocker(s), required repair, and what the verdict does **not** prove.
