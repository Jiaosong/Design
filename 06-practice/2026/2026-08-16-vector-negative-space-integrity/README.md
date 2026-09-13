# 2026-08-16｜Vector Graphics｜Negative Space Integrity Lab

Status: `PRACTICE / TARGET-SCALE READBACK CLOSED / INDEPENDENT REVIEW OPEN / NOT PROMOTED`

## Current Knowledge Position
- Canonical ID: `PRAC-VEC-NEGSPACE-20260816`
- Canonical Practice authority: Notion Notes DB L7 carrier `PRAC-VEC-NEGSPACE-20260816`.
- GitHub role: reproducible source / parameters / review mirror; GitHub does not own Trust, Maturity, hierarchy or METHOD identity.
- Canonical source/provenance path: `06-practice/2026/2026-08-16-vector-negative-space-integrity/`
- Current METHOD invocation owner: `OPEN / NO SAFE L5 MATCH`.
- Current evidence boundary: bounded vector Practice; no brand, accessibility, production or project PASS.

Historical `L5 Practice Method Candidate` wording is provenance only and is superseded as a Current architecture identity.

## Decision Question
At small display sizes, how much negative-space compensation is needed for an oblique notch to remain a legible structural relation rather than disappear into a solid silhouette?

## Exercise
One fixed silhouette relation, three notch-width variants: `8 / 12 / 16 px`. Each variant is inspected at `64 / 32 / 16 px`. Values are exercise assumptions, not brand or production specifications.

## Actual Execution
- Figma file: https://www.figma.com/design/SmPIyFyHXtD5HT987PYd8y
- Root frame: `1:2`
- Natural canvas: `1600×1000`
- Created nodes: `34`
- Archived source: `figma-build.js`
- Archived parameters: `parameters.json`

The original file remained editable and reproducible. On 2026-09-13 the root-frame screenshot was successfully read back at its natural `1600×1000` size, closing the historical screenshot-capacity blocker.

## Target-scale Result｜2026-09-13
- `64 px`: A / 8, B / 12, C / 16 all KEEP for this exercise readback.
- `32 px`: all three remain materially open; A is the weakest.
- `16 px`:
  - A / 8: **REVISE** — approximately one-pixel minimum gap at the narrow edge; oblique relation is optically fragile.
  - B / 12: **REVISE / MARGINAL** — separation survives but remains edge-fragile.
  - C / 16: **KEEP FOR THIS EXERCISE READBACK** — separation remains visibly open at approximately `3–5 px` across the tested raster silhouette.

Observed failure is target-scale raster quantization of a narrowing oblique gap, not source-vector corruption. B/C are controlled mutations with all other variables fixed; C is the first existing variant that remains robust at 16 px in this bounded exercise.

## Current Rule Boundary
Transfer only the test structure:

`CRITICAL NEGATIVE SPACE → TARGET-SCALE RASTER ATTACK → OBSERVED FAILURE → GEOMETRIC REPAIR → SAME-SCALE RETEST`

Do **not** transfer `8 / 12 / 16 px` as universal tokens, ratios, logo rules, iconography standards, accessibility thresholds or production specifications.

## Validation / Promotion
- Exact Practice target-scale visual attack: CLOSED.
- Independent visual/iconography review: OPEN.
- Human/task validation: NOT RUN.
- Cross-context reusable METHOD evidence: INSUFFICIENT / OPEN.
- Trust / Evidence / Maturity promotion: NONE.
- Current Practice remains bounded and unverified until later gates close.

See `review.md` for the exact A/B/C verdict and failure→repair→retest record.
