# 2026-09-19｜C04 Systems Engineering Runtime Interface Reapplication

Status: `PROJECT EXECUTION EVIDENCE / ACTUAL CHROMIUM READBACK / DEFECT→REPAIR→RETEST / ONE INTEGRATED INTERFACE VERIFIED / VALIDATION HOLD / NO PROMOTION`

## Purpose

Advance the existing Systems Engineering Candidate using a real project interface rather than adding more process prose.

Target:

`IF-BROWSER-RUNTIME = SPA Source ↔ Actual Browser Runtime`

Requirement:

`C04-SYSREQ-006`

> The current SPA interaction shall be verified in an actual browser/runtime before any interactive release PASS is claimed.

The work deliberately does **not** attempt to close:
- representative-user validation;
- accessibility conformance;
- field/paper/human fallback;
- official live-status integration;
- professional Systems Engineering review.

---

# Existing-first execution

Reused current repo infrastructure:
- `@playwright/test`;
- `tests/serve-static-root.mjs`;
- GitHub Actions Chromium installation;
- existing C04 APP source;
- existing Systems Engineering requirement/architecture/V&V trace.

No new browser-testing framework was created.

---

# Historical starting state

APP v1.2:

`C04_QINGJIANG_APP_GAME_MAP_v1_2_PORTABLE.html@d95ddf1ed9e4cce412a1ec1c1101e9201465a1a3`

Historical QC:
- source/static checks: PASS;
- `actual_live_browser = HOLD_ENVIRONMENT_ADMIN_BLOCK`.

SYSENG v0.1:
- verification PASS = 4;
- verification HOLD = 2;
- validation PASS = 0;
- integrated interfaces verified = 0;
- `IF-BROWSER-RUNTIME = BLOCKED`.

---

# Browser execution route

Configured test environments:
- Chromium desktop 1440×1000;
- Chromium mobile 390×844.

Successful run runtime:
- Chrome for Testing `151.0.7922.34`;
- Playwright `chromium v1234`.

## Run 1 — harness failure

Product was not executed.

Cause:
- Playwright config lived in `tests/`;
- webServer command used `node tests/serve-static-root.mjs`;
- actual resolution became `tests/tests/serve-static-root.mjs`.

Repair:
- `STATIC_ROOT=.. PORT=4174 node serve-static-root.mjs`.

Classification:

`HARNESS DEFECT ≠ PRODUCT DEFECT`.

## Run 2 — harness readiness failure

Product was still not executed.

Cause:
- readiness URL was repository root `/`;
- repo root has no `index.html`;
- static server returned 404 and Playwright timed out.

Repair:
- readiness URL changed to the actual APP HTML.

Classification:

`HARNESS READINESS DEFECT ≠ PRODUCT DEFECT`.

## Run 3 — real product execution

Result:

`6 PASS / 6 FAIL`

The failures were symmetric on desktop/mobile and split into three classes.

### A. Route focus failure — test defect

APP correctly changed:
- `#map[data-focus=walk]`;
- walk button became active.

The assertion used:

`[data-focus="walk"]`

which matched both:
- the walk button;
- the map container.

Playwright strict mode therefore failed.

Repair:
- selector narrowed to `.focus button[data-focus="walk"]`.

No product code change.

### B. My Book clear failure — real product defect

v1.2:

`function G(){... || DEF}`

`function S(x){const d=G(); d.unshift(x); ...}`

When localStorage was absent, `G()` returned the shared `DEF` array by reference.

`S()` then mutated that default array.

Observed consequence:
- initial defaults = 4;
- user adds one record;
- clear removes localStorage;
- in-memory defaults remain polluted = 5.

Repair in v1.3:

`const d=[...G()]`

before `unshift`.

This is a real state-integrity defect that static source checks had not caught.

### C. Print fallback failure — real product defect

v1.2 used:

`print.onclick=()=>{V('route'); setTimeout(()=>window.print(),50)}`

The browser already exposes `window.print`.

Relying on the global named element `print` therefore did not safely bind the button.

Observed consequence:
- clicking `#print` did not switch to ROUTE;
- intended handler did not execute.

Repair in v1.3:

`document.getElementById('print').onclick=...`

This is a real runtime/browser-global collision.

---

# APP v1.3 successor

Source:

`C04_QINGJIANG_APP_GAME_MAP_v1_3_PORTABLE.html@99e0b88bc6eb8bae7d9b0f4e9a77f404ebeb7bb2`

Material product delta is limited to:
1. My Book shared-default mutation repair;
2. explicit print-button binding.

No IA / map geometry / visual language / field claim redesign.

Historical v1.2 source and QC remain immutable.

---

# Run 4 — successful configured runtime verification

GitHub Actions:
- PR #665;
- run ID `35419536754`;
- run #4;
- job `105834458437`;
- tested head `4d767315c435eb62e05647a6da9d3ab899440e71`.

Result:

`12 PASS / 0 FAIL`

Both desktop and mobile passed:
- five views / SERVICE-RETURN;
- UNKNOWN / FAIL-CLOSED;
- route mode + travel focus;
- imprint dialog → My Book;
- localStorage write / clear / default reset;
- print fallback → ROUTE → print;
- page-level horizontal overflow;
- runtime JavaScript error check on tested paths.

Evidence carrier:

`BROWSER_RUNTIME_READBACK_v1_3.json`.

---

# Systems Engineering consequence

SYSENG v0.2 now carries:

- requirements total = 6;
- verification PASS = 5;
- verification HOLD = 1;
- validation PASS = 0;
- validation NOT_RUN = 5;
- validation N/A = 1;
- integrated interface VERIFIED = 1;
- interfaces open/hold = 3.

Closed configuration-bounded interface:

`IF-BROWSER-RUNTIME = VERIFIED_FOR_CONFIGURED_CHROMIUM_DESKTOP_AND_MOBILE`.

Still open:
- `IF-DIGITAL-FALLBACK = DEFINED / NOT_FIELD_VERIFIED`;
- `IF-STATUS-OFFICIAL = NOT_IMPLEMENTED / HOLD`;
- `IF-HCD-VALIDATION = NOT_RUN`.

Therefore:

`SYSENG-DP7 = BLOCKED / HOLD`.

---

# Verification / validation firewall

This batch is important because it demonstrates the intended distinction in a real system:

`SOURCE CHECK PASS`
did not become
`RUNTIME VERIFICATION PASS`

until actual browser execution occurred.

Then:

`RUNTIME VERIFICATION PASS`
still does not become
`USER VALIDATION PASS`.

No representative users were involved.
No field fallback was exercised.
No official live service was integrated.
No independent Systems Engineering professional review was performed.

---

# Professional-execution maturity delta

Before:
- process definition deep;
- requirements/architecture trace deep;
- configuration reopen semantics existed;
- actual integrated interfaces verified = 0.

After:
- actual browser runtime executed;
- real product defects exposed;
- successor configuration created;
- defects repaired;
- same interface retested;
- configuration-bounded integrated interface verified = 1;
- unresolved interfaces remain explicitly open.

This is evidence-bearing professional execution rather than framework expansion.

---

# Claim ceiling

`ONE REAL CONFIGURATION-BOUND INTEGRATED RUNTIME INTERFACE VERIFIED / SYSTEM VALIDATION=0 / FIELD INTEGRATION OPEN / HCD VALIDATION OPEN / INDEPENDENT SE REVIEW NOT_RUN / PROCESS REMAINS CANDIDATE / NO PROMOTION`.

`ACTUAL RUNTIME VERIFICATION ≠ USER VALIDATION`.

`COMPONENT / CONFIGURATION PASS ≠ WHOLE SYSTEM PROFESSIONAL PASS`.
