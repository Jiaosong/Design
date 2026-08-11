# SP03-R02｜Light Role → Performance Interface

Final artifact status: **POST-REVIEW PASS**.

Truth state: **PERFORMANCE INTERFACE VERIFIED ON SYNTHETIC TEST CELL / PROJECT REALITY OPEN**.

## Purpose
Translate SP03-R01's conceptual light-role method into an explicit and reproducible performance interface without pretending that a synthetic test cell is a real project.

## Controlled A/B experiment
Identical in both schemes:
- synthetic room: 12 × 6 × 3.6 m;
- workplane z = 0.8 m;
- 0.5 m sensor grid, 288 sensors total, 72 in each role zone;
- exercise material hypotheses;
- identical four sky cases and viewpoints;
- total skylight area = 7.2 m².

Only skylight-area distribution changes:
- Scheme A｜Uniform: 1.2 / 1.2 / 1.2 / 1.2 m;
- Scheme B｜Sequence: 0.8 / 2.4 / 1.0 / 0.6 m mapped to ENTRY / STAY / TURN / BACKGROUND.

Exercise target rank: `STAY > TURN > ENTRY > BACKGROUND`.
The role-rank Spearman is a **custom Practice heuristic**, not a lighting standard.

## Final verified runtime
GitHub Actions run `#6 / 31457344868`
- runtime head SHA: `cb7cf10df2ee006de5143c9303be51b6d00fca13`
- artifact ID: `9088638622`
- artifact digest: `sha256:abe1512e849c17054fd8b92d89c8044f70b891a40da0dd04267a052328b02436`
- Radiance: `6.0a`
- evalglare: `3.06 release 01.10.2025`
- official LBNL `pyradiance==1.2.4` runtime package

Executed:
- 8 real `rtrace -I+` workplane simulations;
- 16 real 800×800 180° angular-fisheye HDR renders;
- 16 real `evalglare` evaluations;
- final glare CSV preserves evalglare's self-described 23-field schema.

## Performance observations
Mean role-rank Spearman across the four exercise skies:
- Scheme A: `0.30`
- Scheme B: `0.50`

By sky:
- OVC: A `0.6` / B `1.0`
- CLEAR_HIGH: A `0.6` / B `1.0`
- CLEAR_E: A `0.4` / B `0.4`
- CLEAR_W: A `-0.4` / B `-0.4`

Uniformity / glare trade-off:
- mean U0: A `0.2343` / B `0.1836`
- mean CV: A `1.7731` / B `1.7987`
- max DGP under clear east/west viewpoints: A `0.281196` / B `0.298364`

Therefore **Scheme B is not promoted as a universally better scheme**. It strengthens the intended role order under the diffuse and high-sun synthetic conditions, but directional sun can remove or invert the intended hierarchy. It also trades away uniformity and produces a slightly higher worst-case DGP in this matrix.

No project compliance or comfort threshold is claimed.

## Failure-seeking revision chain
1. Run #1 — FAIL: Ubuntu 24.04 had no `radiance` apt candidate; no simulation occurred.
2. Run #2 — FAIL: official runtime installed, but script-overwritten `RAYPATH` prevented `rayinit.cal` resolution.
3. Run #3 — runtime PASS / NEEDS REVISION: first complete real run; A/B heatmaps had incomparable color scales and glare parser was incomplete.
4. Run #5 — runtime PASS / NEEDS REVISION: shared visual scale fixed; Data Review found evalglare's 14th field was `dgr`, not the old hard-coded `band_avlum`, and later fields were omitted.
5. Run #6 — corrected: parser reads evalglare's self-described 23-field schema; final plots/HDR/data were reopened and reviewed.

A green workflow was never treated as final review.

## Reproduction
Run #5 → #6, unchanged physical inputs and ray settings:
- role-rank Spearman identical in all 8 A/B × sky rows;
- mean illuminance max relative change < 0.10%;
- role-zone mean max relative change < 0.31%;
- DGP and vertical illuminance identical for all 16 viewpoints;
- U0 is more sensitive to the sampled minimum, with max relative change about 3.1%.

Classification: **NUMERICALLY STABLE, NOT BYTE-IDENTICAL**.

## Artifact Review System v1.0
- AR-G01—G10 Common: PASS
- AR-S02 Model: PASS for synthetic scene / Project Geometry Gate OPEN
- AR-S03 Data: PASS after evalglare schema correction
- AR-S04 Code / Parametric: PASS
- AR-S06 Visual: PASS
- AR-S07 Documentation: PASS
- AR-S09 Release Package: PASS

See `FINAL_ARTIFACT_REVIEW.md` and `evidence_snapshot.json`.

## Practice rule candidate
**Light Role is a target relationship, not a performance guarantee.**

Before a light-role strategy is called robust, test at least one diffuse condition and opposed directional conditions. If directional conditions invert the intended hierarchy, revise aperture distribution, orientation, controls/shading, or the role target itself instead of hiding the failure in a preferred rendering.

## Truth boundaries / Reopen conditions
Still OPEN until a real project provides:
- real geometry/orientation;
- verified material and glazing optical properties;
- actual location/weather/date/time;
- program-specific illuminance and glare criteria;
- user/task outcome validation.

No Project Reality or Candidate promotion is allowed before these close.
