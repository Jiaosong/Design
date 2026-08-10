# Timer Light Basin v3.3｜Integrated Browser / Deployment Gate｜2026-08-10

## Current status

`STAGING_TRANSPORT_DEFINED / CONTRACT_CI_PASS / REAL_PACKAGE_NOT_STAGED / BROWSER_PHASE_NOT_RUN`

This record continues the locked v3.3 photography pipeline without reopening the four-gate render calibration. Round 3 proxy geometry remains non-authoritative and cannot replace or overturn the canonical render lock.

## 1｜Initial source-branch finding

The first integrated-browser workflow run (`31352749106`) correctly returned:

`BLOCKED_SOURCE_PACKAGE_INCOMPLETE`

The public GitHub branch did not contain 10 deploy-required assets (`index.html`, `styles.css`, two SVGs, two posters and four real GLBs). The browser phase was intentionally skipped. This established that the blocker was deployment-source completeness, not a photography-profile failure or a WebGL regression.

That source-branch model is now **superseded as the intended transport architecture**. The real GLBs do not need to be committed to the public branch merely to satisfy CI.

## 2｜Authority package

File Library remains the authoritative delivery source:

`/Oleander/Practice/Business/B02_Model-Offering/2026-08-07_Timer-Light-Basin/v3.3-web/OLEANDER_Zhizuo_TimerLightBasin_v3.3_AUDITED_2026-08-10.zip`

Locked package identity:

- outer ZIP SHA-256: `a4ca61701f8bac0c4991fe3789386cdaec84688e6fed90d1917d9be430a8e804`
- package root: `OLEANDER_Zhizuo_TimerLightBasin_v3.3_WEB`
- canonical `assets/pbr/timer_100_pbr.glb` SHA-256: `900e02510ab6b2b5176aa3723dba7981700dc79b5f217dbe481844a534ed7c66`
- 50% GLB SHA-256: `a058f9f5d7469276eece75b88673a39a78168080b5e3140715e1ee748fb88c84`
- 10% GLB SHA-256: `2979cf9247f473346cf2b418845eb2464492fc22c6fac033763b75ca5b4ea5a6`
- exploded GLB SHA-256: `1eefea32671f42951abe31f4c73f0ac69ff534412b2a1466f7954a4ddfe419ea`

The package contains its own `SHA256SUMS.txt`; required deployment files were independently checked against the archive before the staging contract was written.

## 3｜New staged-artifact architecture

The transport chain is now:

`File Library authoritative package → authenticated GitHub draft-release staging → SHA/package verification → Chromium/WebGL integrated QA → explicit release authorization → GitHub Pages overlay deployment`

A **draft release is staging transport only**. It is not publication approval. Public Pages deployment still requires the existing explicit release boundary.

GitHub implementation:

- authority manifest: `DEPLOYMENT_ARTIFACT_MANIFEST_v3.3.json`
- safe package verifier/extractor: `tests/timer-v33-stage-package.py`
- staged static server: `tests/serve-static-root.mjs`
- integrated browser gate: `tests/timer-v33-integrated.mjs`
- staged browser workflow: `.github/workflows/timer-v33-integrated-browser.yml`
- authorized Pages overlay workflow: `.github/workflows/timer-v33-staged-pages.yml`
- staging contract CI: `.github/workflows/timer-v33-staging-contract.yml`

Default staging identity:

- draft release tag: `timer-v3.3-audited-staging`
- asset: `OLEANDER_Zhizuo_TimerLightBasin_v3.3_AUDITED_2026-08-10.zip`

## 4｜Verification behavior

Before any browser or deployment step, `timer-v33-stage-package.py` enforces:

1. outer audited ZIP SHA-256;
2. safe archive paths / zip-slip rejection;
3. SHA-256 of 18 deploy-critical files;
4. complete package-internal `SHA256SUMS.txt` verification;
5. extraction only after every integrity gate passes.

The integrated browser stage then checks:

- document identity and HTTP response;
- Chromium WebGL context;
- `model-viewer` registration;
- Hero + CMF photography viewers ready;
- live photography canvases;
- state inspection models and `100 → 50 → 10 → 100` switching;
- CMF focus controls;
- exploded-stage controls;
- real GLB HTTP responses;
- local request / HTTP / page errors;
- full-page, Hero and CMF screenshot evidence plus machine-readable JSON.

## 5｜Contract CI result

GitHub Actions run `31353324608` completed **SUCCESS**.

Passed steps:

- Python / Node / JSON syntax checks;
- locked authority manifest validation;
- synthetic audited ZIP exercise through outer SHA, required-file SHA, internal `SHA256SUMS.txt`, safe extraction and result JSON.

Therefore the **staging contract implementation is executable**. It is no longer an untested design proposal.

## 6｜Authorized Pages boundary

`.github/workflows/timer-v33-staged-pages.yml` will only execute when:

`release_authorized = true`

After authorization it still must:

1. authenticate to the draft release;
2. download the exact staged asset;
3. pass package authority verification;
4. overlay the audited package into `website/practice/timer-light-basin-v3` only in the runner workspace;
5. pass existing E1 website checks;
6. pass the Timer Chromium/WebGL gate;
7. archive pre-deploy QA evidence;
8. only then upload and deploy the website to GitHub Pages.

QA success therefore cannot silently become publication approval.

## 7｜Remaining blocker

The repository currently has no GitHub Releases. The local execution environment also has no authenticated `gh` CLI/token surface for release creation or binary asset upload. Therefore the real audited ZIP has **not** been copied out of File Library into the GitHub draft-release staging layer in this run.

This is now a narrow transport/tooling blocker, not a design, geometry, photography or CI-contract blocker.

Do not solve it by committing the GLBs to the public branch or by rebuilding proxy geometry.

## 8｜Current authority conclusions

- four-gate photography calibration: **PASS / LOCKED**
- canonical external geometry equivalence: **PASS**
- Round 3 proxy-geometry regression: **REJECTED / NON-AUTHORITATIVE**
- audited deployment package identity: **LOCKED**
- staging architecture / verifier contract: **PASS**
- real audited package in draft-release staging: **NOT YET STAGED**
- full integrated browser QA against the real package: **NOT RUN**
- public Pages deployment: **NOT AUTHORIZED / NOT RUN**
- optical, thermal, electrical, DFM/DFA, tolerance, touch, material/colorimetry and other engineering validation: **NOT RUN / PENDING**
