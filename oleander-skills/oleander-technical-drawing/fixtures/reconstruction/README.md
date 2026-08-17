# Reconstruction Fidelity Calibration Fixture

Fixture: `RF-CAL-01`  
Status: `SYNTHETIC CALIBRATION / NOT GOLDEN PROMOTED / NOT PROJECT AUTHORITY`

This fixture exists to prove that the reconstruction-fidelity workflow can detect material drawing mismatches without conflating pixel similarity with technical correctness.

## Files

- `RF-CAL-01_REFERENCE_MASTER.svg` — synthetic editable vector reference.
- `RF-CAL-01_CANDIDATE_BAD.svg` — deliberate geometry, typography and stroke mismatch.
- `RF-CAL-01_CANDIDATE_MATCH.svg` — independently grouped editable vector candidate with the same visible geometry as the reference.
- `RF-CAL-01_ROIS.json` — title / primary geometry / dimensions / callout / title-block diagnostic regions.
- `RF-CAL-01_EXPECTED.json` — machine-readable regression expectations and invariants.
- `../../tools/reference_fidelity.py` — same-canvas raster comparison tool.

## Deliberate negative mutations

`CANDIDATE_BAD` contains four explicit reconstruction failures across three classes:

1. primary geometry shifted +5 px in X;
2. one interface rectangle stroke changed from 2.2 to 2.8 output units;
3. main title baseline moved +3 px;
4. main title size changed 32 → 31.

The rest of the fixture is intentionally held constant so the difference evidence remains attributable.

## Actual local render/readback

Renderer used for this calibration: Inkscape on the current execution machine, 1200×800 raster output.

At tolerance `2` channel values:

### Negative candidate

- exact-equal pixel ratio: `0.9847260417`
- changed-pixel ratio above tolerance: `0.01519375`
- mean absolute channel error: `2.6671239583`
- RMSE channel error: `23.7477145172`
- maximum channel error: `238`

The important result is not the global percentage. The negative candidate must be diagnosed as `REVISE` because the mismatch lands in critical title/primary-geometry ROIs and includes a known A2 geometry-anchor displacement.

Recorded ROI readback at tolerance 2 also shows why global similarity cannot decide the verdict:

- `title` changed-pixel ratio: `0.1652923077`;
- `primary_geometry` changed-pixel ratio: `0.0228588446`;
- `dimensions` changed-pixel ratio: `0.0`;
- `callout` changed-pixel ratio: `0.0072982456` because its target relation crosses the shifted geometry;
- `title_block` changed-pixel ratio: `0.0`.

### Matched candidate

- exact-equal pixel ratio: `1.0`
- changed-pixel ratio above tolerance: `0.0`
- mean absolute channel error: `0.0`
- RMSE channel error: `0.0`
- maximum channel error: `0`

The matched candidate has different semantic group IDs / source bytes but rasterizes identically under the locked renderer. This demonstrates why file hash equality is not required for visible reconstruction fidelity, while editable/vector structure still remains a separate requirement.

## Local source identities from calibration run

- reference SVG SHA-256: `43723ec255fa038971a1b33f4ae801405fe9c353a539004a3990575c26d444e1`
- bad candidate SVG SHA-256: `d1c6c48f7f6ca279736d1942eff38d86e687c88c829e99be3d1bb9769e8bc585`
- matched candidate SVG SHA-256: `aa534b22ded35b9490fba9aaacd6255f512619b3cddff943a52ca1c9a36d408b`
- reference raster SHA-256: `b9c4e68484ffb3f1f6bf68350ee59ed4bc7cd6ae0b9db9e861b51dcf96061340`
- matched raster SHA-256: `b9c4e68484ffb3f1f6bf68350ee59ed4bc7cd6ae0b9db9e861b51dcf96061340`

Raster previews are generated evidence and are intentionally not source authority.

## Gate interpretation

- `RF-G0…RF-G5` can be exercised by this synthetic fixture.
- `RF-G6` remains an independent-review boundary; this README is producer evidence only.
- `RF PASS != TD PASS`.
- A reference can be matched perfectly and still be technically unsuitable for a current OLEANDER project.
- A project adaptation may intentionally deviate from the reference when current geometry, evidence, safety, engineering or FIELD truth requires it.
