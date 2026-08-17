# Reconstruction Fidelity Calibration Fixture

Fixture: `RF-CAL-01`  
Status: `SYNTHETIC CALIBRATION / NOT GOLDEN PROMOTED / NOT PROJECT AUTHORITY`

This fixture exists to prove that the reconstruction-fidelity workflow can detect and repair material drawing mismatches without conflating pixel similarity with technical correctness.

The v0.3 calibration intentionally removes the earlier weak idea that a high global similarity percentage could support a pixel-level claim. `98%+ equal pixels` is diagnostically interesting but categorically insufficient for RF-C3.

## Files

- `RF-CAL-01_REFERENCE_MASTER.svg` — synthetic editable vector reference.
- `RF-CAL-01_CANDIDATE_BAD.svg` — deliberate geometry, typography and stroke mismatch.
- `RF-CAL-01_CANDIDATE_MATCH.svg` — independently grouped editable vector candidate with the same visible geometry as the reference.
- `RF-CAL-01_ROIS.json` — critical/major title / primary geometry / dimensions / callout / title-block diagnostic regions.
- `RF-CAL-01_EXPECTED.json` — machine-readable tolerance-zero regression expectations and invariants.
- `RF-CAL-01_RF-C3_CONTRACT.json` — hard RF-C3 zero-difference contract.
- `RF-CAL-01_RUNTIME_READBACK_v0.3.json` — recorded tolerance-zero / edge-radius diagnostic readback.
- `RF-CAL-01_SOLVER_SPEC.json` — bounded E2/E3/E4 parameter search specification.
- `RF-CAL-01_SOLVER_RESULT.json` — actual coupled-solver recovery and renderer-mismatch finding.
- `../../tools/reference_fidelity.py` — same-canvas raster comparison and hard-contract tool.
- `../../tools/svg_parameter_solver.py` — bounded editable SVG parameter solver.
- `../../references/PIXEL_FORENSIC_PROTOCOL.md` — strict forensic reconstruction protocol.
- `../../references/PIXEL_SOLVER_PROTOCOL.md` — solver routing, coupling and renderer-lock protocol.

## Deliberate negative mutations

`CANDIDATE_BAD` contains four explicit reconstruction failures across three classes:

1. primary geometry shifted +5 px in X;
2. one interface rectangle stroke changed from 2.2 to 2.8 output units;
3. main title baseline moved +3 px;
4. main title size changed 32 → 31.

The rest of the fixture is intentionally held constant so the difference evidence remains attributable.

## Actual local render/readback — strict tolerance zero

Renderer used for the original v0.3 forensic calibration: Inkscape on the current execution machine, 1200×800 raster output.

### Negative candidate

Tolerance `0`:

- changed-pixel ratio: `0.0152739583`;
- mean absolute channel error: `2.6671239583`;
- RMSE: `23.7477145172`;
- maximum channel error: `238`;
- changed-pixel bounding box: `[92,81] → [824,521]`;
- estimated whole-page translation: `dx=0 / dy=0`.

The last point matters: the mismatch is not a page-registration problem. It is local geometry / typography / stroke error.

Edge disagreement remains substantial even when a 1–2 px neighborhood is allowed:

- reference unmatched edge ratio r0: `0.1422351234`;
- r1: `0.0945718433`;
- r2: `0.0590420900`.

Critical ROI readback at tolerance zero:

- `title` changed-pixel ratio: `0.1663384615`;
- `primary_geometry`: `0.0229124479`;
- `dimensions`: `0.0`;
- `callout`: `0.0073684211`;
- `title_block`: `0.0`.

Therefore the negative candidate is `REVISE_A2_A3_A4`. The fact that roughly 98.47% of the full canvas is unchanged has no passing authority.

### Matched candidate

Under the same locked synthetic render condition:

- exact-equal pixel ratio: `1.0`;
- changed-pixel ratio at tolerance 0: `0.0`;
- MAE: `0.0`;
- RMSE: `0.0`;
- maximum channel error: `0`;
- estimated translation: `dx=0 / dy=0`;
- edge unmatched r0/r1/r2: all `0.0`.

The matched candidate has different semantic group IDs / source bytes but rasterizes identically under the locked renderer. This demonstrates that file hash equality is not required for output-pixel equality, while editable/vector structure remains a separate requirement.

This result supports only `RF-C3 PIXEL-EXACT CANDIDATE IN THIS LOCKED SYNTHETIC FIXTURE`. It does not prove arbitrary-reference reconstruction capability and does not self-award independent review.

## Coupled solver regression

A first automatic solver pass exposed an important failure mode. When title baseline was solved while the title font size was still wrong, the temporary optimum moved to `y=104`. Correcting font size from `31 → 32` invalidated that baseline result.

Therefore exact reconstruction cannot use a permanently frozen one-pass sequence. The solver now cycles through dependent layers and reopens earlier parameters after downstream changes.

With reference and candidate both rasterized through the same CairoSVG comparison path, the coupled solver recovered:

- `primary_dx: 5 → 0`;
- `title_y: 108 → 105`;
- `title_font_size: 31 → 32`;
- `interface_stroke: 2.8 → 2.2`.

Final recorded readback:

- changed-pixel ratio: `0.0`;
- normalized MAE: `0.0`;
- edge mismatch r1: `0.0`.

This is a real automated parameter recovery on the synthetic fixture, not a hand-entered final candidate.

## Renderer mismatch regression

A second failure was equally important: optimizing against an Inkscape-rendered reference while rendering candidates through CairoSVG can prefer a false typography baseline even when the SVG parameter is otherwise correct.

Therefore:

`WRONG RENDERER → WRONG OPTIMUM`.

RF-C3 requires the solver and final comparison to use the declared locked renderer/font path. A cross-renderer solver result may be useful diagnostically but cannot be used as pixel-exact evidence.

## Claim model

- `RF-C0` — structural reconstruction;
- `RF-C1` — measured geometry fidelity;
- `RF-C2` — render-locked high fidelity with explained residuals;
- `RF-C3` — pixel-exact candidate: tolerance-zero, zero unexplained in-scope changed pixels, locked renderer/font/color environment, independent review pending.

Do not call RF-C2 “almost pixel-perfect”. If non-zero unexplained in-scope pixels remain, it is not RF-C3.

## Gate interpretation

- `RF-G0…RF-G5` can be exercised by this synthetic fixture.
- `RF-G6` remains an independent-review boundary; this README is producer evidence only.
- `RF PASS != TD PASS`.
- A reference can be matched perfectly and still be technically unsuitable for a current OLEANDER project.
- A project adaptation may intentionally deviate from the reference when current geometry, evidence, safety, engineering or FIELD truth requires it.
- Render-environment changes invalidate prior RF-C3 evidence and require a new strict run.
