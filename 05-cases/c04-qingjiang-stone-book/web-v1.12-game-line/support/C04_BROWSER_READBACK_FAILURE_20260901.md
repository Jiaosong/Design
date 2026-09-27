# C04 Browser Readback Failure — 2026-09-01

Status: **PRESENTATION READBACK / FAIL → HOLD / SAME OBJECT / NO OWNER TRANSFER**

- `PROJECT_ID=PRJ-C04-QINGJIANG-SHISHU`
- `OBJECT_ID=PRJ-C04-DIGITAL-INTERACTION`
- Current producer frontier: PR #465 / `agent/c04-web-v1-12-currentize-20260830`
- Workflow: `C04 Web Static Integrity`
- Run: `33461026776`
- Browser evidence artifact: `9783179425`
- Artifact SHA-256: `7776f59401ccb04ba10eb18e3bf8955ee1bdf4926ddf6e78d444362b75d9f2a4`
- Browser evidence size: `8,475,645` bytes

## What passed

Actual Chromium readback ran at:

- `1920×1080`
- `1366×768`
- `390×844`
- separate `prefers-reduced-motion: reduce` context

Across the tested cases:

- horizontal overflow = `0`;
- topbar and hero remained present;
- imprint interaction updated state;
- supplement drawer opened and closed;
- current My Book iframe remained visible/current;
- desktop PageDown advanced the reading sequence;
- no page runtime errors were recorded;
- reduced-motion media query matched and the tested imprint animation/hero transition reduced to none/0s.

These results are useful browser evidence but do not grant Design KEEP.

## Material failures

### F01 — external landscape delivery

The following Current external source bindings failed to load in the CI browser carrier:

- `https://www.eslygroup.com/uploadfile/image/20230718/v0ii0wjlhe.jpg`
- `https://www.eslygroup.com/uploadfile/image/20240522/1cce70abb.jpg`

The failure occurred at desktop and mobile sizes and directly matches the pre-existing runtime dependency HOLD in `C04_CLEAN_LANDSCAPE_RUNTIME_20260830.json` / `C04_PR465_COMPLETE_RUNTIME_DEPENDENCY_MANIFEST_20260830.json`.

Do not solve this by substituting a generic Qingjiang photo, old Web screenshot, AI/redraw, or another compression. Exact Source Authority remains required.

### F02 — mobile PageDown test assumption

The original verifier required desktop keyboard `PageDown` behavior even in the 390×844 mobile carrier. It moved only 1px. This is a validator-context mismatch, not evidence that the mobile page itself is non-scrollable: the same run successfully navigated mobile sections and produced mobile screenshots with a document height far beyond the viewport.

The verifier was repaired in-place so:

- desktop carriers retain keyboard PageDown testing;
- mobile carrier tests scroll advancement separately and declares the method in the report;
- no page design or interaction code is changed merely to satisfy a desktop-keyboard assumption on a touch-sized carrier.

Commit: `2ae525661a6c7129f6a8382515dee5756a322599`.

## Current disposition

`STATIC INTEGRITY PASS`

`BROWSER STRUCTURE / INTERACTION EVIDENCE PARTIAL PASS`

`EXTERNAL LANDSCAPE DELIVERY FAIL → PRESENTATION HOLD`

`VALIDATION HANDOFF = NOT READY`

The exact clean landscape source identity is known, and the earlier manifest already recorded exact local derivative preparation / binary-binding limitations. Presentation retains ownership until the landscape carrier is made stable without source substitution and a fresh browser readback passes.

`BROWSER SCRIPT EXECUTED ≠ BROWSER PASS ≠ DESIGN KEEP ≠ FIELD PASS`.
