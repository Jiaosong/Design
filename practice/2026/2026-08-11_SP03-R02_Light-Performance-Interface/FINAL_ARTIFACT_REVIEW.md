# SP03-R02｜Light Role → Performance Interface｜Final Artifact Review

Final status: **POST-REVIEW PASS** for the synthetic performance-interface package.

Truth boundary: **PERFORMANCE INTERFACE VERIFIED ON SYNTHETIC TEST CELL / PROJECT REALITY OPEN**.

This does **not** claim project illuminance compliance, glare comfort, real material performance, real orientation, real weather/time validity, or user outcome.

## 1. Final verified runtime

- GitHub Actions run: `#6 / 31457344868`
- Runtime head SHA: `cb7cf10df2ee006de5143c9303be51b6d00fca13`
- Artifact ID: `9088638622`
- Artifact digest: `sha256:abe1512e849c17054fd8b92d89c8044f70b891a40da0dd04267a052328b02436`
- Radiance: `6.0a`
- evalglare: `3.06 release 01.10.2025`
- Runtime distribution: official LBNL `pyradiance==1.2.4` wheel binaries/libraries

Executed evidence:
- 2 aperture schemes × 4 sky cases = 8 real `rtrace -I+` workplane simulations;
- 288 sensors per case, 72 per role zone;
- 2 schemes × 2 directional clear skies × 4 role viewpoints = 16 real 800×800 angular-fisheye HDR renders;
- 16 real `evalglare` evaluations;
- A/B total skylight area held equal at 7.2 m².

## 2. Rejected intermediate states

1. **Run #1 — FAIL**: Ubuntu 24.04 had no `radiance` apt candidate. No simulation occurred.
2. **Run #2 — FAIL**: official LBNL runtime installed, but the exercise script overwrote `RAYPATH`; `rtrace` could not locate `rayinit.cal`.
3. **Run #3 — runtime PASS / artifact NEEDS REVISION**: first complete real Radiance run, but A/B OVC heatmaps used different color scales and the evalglare parser hard-coded an incomplete schema.
4. **Run #5 — runtime PASS / data NEEDS REVISION**: shared A/B heatmap scale fixed, but review found the old parser mislabelled the 14th evalglare field as `band_avlum` while evalglare 3.06 self-described it as `dgr`, and omitted later fields.
5. **Run #6 — corrected**: parser reads evalglare's own self-described 23-field schema; final visual and data artifacts reopened and reviewed.

A green workflow was never treated as final review.

## 3. Controlled comparison contract

Identical for A and B:
- synthetic room 12 × 6 × 3.6 m;
- workplane z = 0.8 m;
- 0.5 m sensor grid;
- 288 sensors;
- material hypotheses;
- sky cases;
- viewpoints;
- total skylight area = 7.2 m².

Only changed variable:
- Scheme A: four equal 1.2 m skylight widths;
- Scheme B: 0.8 / 2.4 / 1.0 / 0.6 m, mapped to ENTRY / STAY / TURN / BACKGROUND.

Exercise target role order: `STAY > TURN > ENTRY > BACKGROUND`.
The rank correlation is a custom Practice heuristic, not a lighting standard.

## 4. Final performance observations

Across the four exercise skies, mean role-rank Spearman:
- Scheme A: `0.30`
- Scheme B: `0.50`

Scheme B reaches exact intended role ordering under:
- OVC: `1.0`
- CLEAR_HIGH: `1.0`

But under directional skies:
- CLEAR_E: A = `0.4`, B = `0.4`
- CLEAR_W: A = `-0.4`, B = `-0.4`

Therefore **Scheme B is not universally better**. Directional sun can override the intended light-role sequence.

Uniformity trade-off across the exercise matrix:
- mean U0 A = `0.2343`; B = `0.1836`
- mean CV A = `1.7731`; B = `1.7987`

Glare evidence for clear east/west viewpoints:
- mean DGP A = `0.24636`; B = `0.24705`
- max DGP A = `0.281196`; B = `0.298364`

These values are simulation observations only. No project comfort threshold is applied.

## 5. Reproduction / numerical stability

Run #5 → Run #6, with unchanged physical inputs and ray settings:
- role-rank Spearman: identical in all 8 A/B × sky rows;
- mean illuminance: maximum relative change < 0.10%;
- role-zone means: maximum relative change < 0.31%;
- CV: maximum relative change < 0.22%;
- minimum illuminance / U0 are more sampling-sensitive, maximum relative change about 3.1%;
- DGP and E_v: identical for all 16 evaluated viewpoints.

Therefore reproduction is classified as **numerically stable, not byte-identical**. Stochastic/Monte-Carlo outputs must not be documented as byte-identical evidence.

## 6. OLEANDER Artifact Review System v1.0

### Common
- AR-G01 Identity & Naming — PASS
- AR-G02 Version & Status — PASS
- AR-G03 Completeness — PASS
- AR-G04 Internal Consistency — PASS
- AR-G05 Cross-file Consistency — PASS
- AR-G06 Evidence & Truth — PASS
- AR-G07 Open / Integrity — PASS
- AR-G08 Reproduction — PASS, numerical-stability basis
- AR-G09 Change Traceability — PASS
- AR-G10 Final Artifact Review — PASS

### Specific
- AR-S02 Model — PASS for the synthetic Radiance scene; Project Geometry Gate remains OPEN
- AR-S03 Data — PASS after evalglare schema correction
- AR-S04 Code / Parametric — PASS
- AR-S06 Visual — PASS: A/B OVC maps share the same lux scale; axes/units are explicit; no critical occlusion or overflow found
- AR-S07 Documentation — PASS
- AR-S09 Release Package — PASS after final package verification

## 7. Project-reality gates that remain OPEN

- real project geometry/orientation;
- verified material/glazing optical properties;
- actual location/weather/date/time;
- program-specific illuminance/glare criteria;
- user/task outcome validation.

No Candidate / Project Reality promotion is permitted until those inputs exist.

## 8. Practice rule promoted from R02

**Light Role is a target relationship, not a performance guarantee.**

A light-role strategy must be tested against at least one diffuse condition and opposed directional conditions before it can be treated as robust. If directional conditions invert the intended role hierarchy, the design must revise aperture distribution, control/shading, orientation, or the role target itself rather than hiding the failure in a single preferred rendering.

This is a **Practice rule candidate**, not a project lighting standard.
