# v3.3 Photography Pipeline QA

- Five governed modules present: **PASS**
- `PhotographyViewer.js` integration: **PASS**
- JavaScript syntax (`node --check`): **PASS**
- Local HTML file references: **PASS / 0 missing**
- Photography runtime `three 0.174.0`: **PINNED**
- Photography runtime `postprocessing 6.39.4`: **PINNED**
- `@google/model-viewer 4.1.0` inspection layer: **PINNED / DEPENDENCY SCOPE REVIEW OPEN**
- PBR delivery GLBs contain explicit `NORMAL`: **PASS**
- Complete AI-generated design-board/page referenced by formal page: **NO**
- Contact-shadow module restores renderer clear state after offscreen capture: **PASS**

## Browser calibration execution

GitHub Actions `Timer v3.3 Photography Calibration` run `31164980399` on 2026-08-07:

- calibration dependency install: **PASS**
- parent render dependency exposure: **PASS**
- Chromium install: **PASS**
- Vite calibration server: **PASS**
- four WebGL gate captures: **PASS**
- WebGL manifest generation: **PASS**
- calibration artifact upload: **PASS**

This closes the former `PHOTOGRAPHY_VISUAL_REGRESSION_BLOCKED` execution blocker. It proves that the governed calibration rig can execute and produce browser capture evidence in the recorded CI environment; it does not prove visual acceptance.

## Current visual decision

Latest recorded Round 2 human review remains:

- Housing highlight: **REJECT**
- Diffuser volume: **REJECT**
- Metal knob reflection: **PROVISIONAL PASS**
- Contact shadow falloff: **REJECT**

Therefore **NO FINAL HERO / CMF RENDER LOCK** is authorized by the successful capture run.

## Dependency governance

The parent package currently records `@google/model-viewer 4.1.0` together with photography `three 0.174.0`. npm reports a peer-resolution conflict because model-viewer 4.1.0 declares `three ^0.172.0`. Calibration CI deliberately isolates the photography render dependency scope rather than forcing an incompatible root install.

This remains an **OPEN dependency-architecture task**: inspection and photography runtimes must be separated or converged before claiming one installable unified package.

## Evidence boundary

- Optical / thermal / DFM / electrical / fabrication / safety / compliance / user validation: **NOT RUN**
- Browser capture quality does not establish measured material response, colorimetry, diffuser performance, manufacturing feasibility, or production readiness.

Status: `SOURCE_QA_PASS / BROWSER_CAPTURE_PASS / VISUAL_GATE_REJECTS_REMAIN / DEPENDENCY_SCOPE_OPEN / ENGINEERING_VALIDATION_PENDING`
