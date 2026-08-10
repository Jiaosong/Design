# Timer Light Basin v3.3｜Integrated Browser / Deployment Gate｜2026-08-10

## Status

`GATE_DEFINED / SOURCE_PACKAGE_INCOMPLETE / BROWSER_PHASE_NOT_RUN`

This record continues the locked v3.3 photography pipeline without reopening the four-gate render calibration. It also preserves the Round 3 regression ruling: proxy geometry is non-authoritative and cannot be used to overturn or replace the canonical render lock.

## What changed

A dedicated GitHub Actions gate now separates deployment-source completeness from browser/WebGL execution:

1. **Source-package preflight** — verify the complete deployable page shell, SVG/poster assets, required real GLBs, and the canonical `timer_100_pbr.glb` SHA-256.
2. **Integrated Chromium/WebGL QA** — only runs after preflight passes; checks WebGL, model-viewer registration, Hero + CMF photography viewers, state switching, exploded-stage controls, local HTTP/model responses, runtime errors, and captures evidence screenshots.

Gate implementation:
- workflow: `.github/workflows/timer-v33-integrated-browser.yml`
- browser script: `tests/timer-v33-integrated.mjs`
- initial run: GitHub Actions run `31352749106`

## Initial run result

The preflight correctly returned:

`BLOCKED_SOURCE_PACKAGE_INCOMPLETE`

The following 10 deploy-required files are absent from the GitHub branch:

1. `index.html`
2. `styles.css`
3. `assets/state_map.svg`
4. `assets/central_section.svg`
5. `assets/hero_poster.png`
6. `assets/exploded_poster.png`
7. `assets/pbr/timer_100_pbr.glb`
8. `assets/pbr/timer_50_pbr.glb`
9. `assets/pbr/timer_10_pbr.glb`
10. `assets/pbr/timer_exploded_sequence_v32.glb`

The browser phase was intentionally skipped after the preflight failure. This is the correct behavior: no substitute geometry, fake asset, or partial page is allowed to produce a visual-QA PASS.

## Authority comparison

The complete audited v3.3 package exists in File Library at:

`/Oleander/Practice/Business/B02_Model-Offering/2026-08-07_Timer-Light-Basin/v3.3-web`

Audited package:

`OLEANDER_Zhizuo_TimerLightBasin_v3.3_AUDITED_2026-08-10.zip`

The Library master contains the deploy shell and real model assets that are currently absent from the GitHub branch. Therefore the immediate deployment blocker is now classified as **GitHub deploy-source incompleteness**, not a photography-profile failure and not evidence of a WebGL rendering regression.

Canonical geometry identity remains:

- asset: `assets/pbr/timer_100_pbr.glb`
- SHA-256: `900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`

## Closure condition

Do not re-author the model or rebuild a proxy package. Close this gate only when the audited deployable package is made available to the GitHub deployment/CI runtime with asset identity preserved, then rerun the integrated-browser workflow.

Acceptable next-state evidence must include:
- source-package preflight PASS;
- canonical GLB SHA match PASS;
- Chromium/WebGL context PASS;
- Hero + CMF photography viewers ready;
- 100% → 50% → 10% → 100% state switching PASS;
- exploded sequence control PASS;
- required real model HTTP responses PASS;
- no local request/HTTP/page errors;
- archived full-page, Hero and CMF screenshots plus machine-readable result JSON.

## Boundary

This gate does **not** change these current conclusions:

- four-gate photography calibration: **PASS / LOCKED**;
- canonical external geometry equivalence: **PASS**;
- Round 3 proxy-geometry regression: **REJECTED / NON-AUTHORITATIVE**;
- full integrated browser/deployment QA: **NOT PASSED — SOURCE PACKAGE INCOMPLETE**;
- optical, thermal, electrical, DFM/DFA, tolerance, touch, material/colorimetry and other engineering validation: **NOT RUN / PENDING**.
