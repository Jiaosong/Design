# C04｜Qingjiang Thirteen Imprints App / Game Map v1.3

Status: `RUNTIME-REPAIR SUCCESSOR / MAIN CANDIDATE / FIELD OPEN / NO_PROMOTION`

Predecessor:

`app-game-map-v1.2@d95ddf1ed9e4cce412a1ec1c1101e9201465a1a3`

v1.2 historical QC remains immutable. v1.3 exists because actual Chromium execution exposed runtime defects that static/source checks had not caught.

## Material delta from v1.2

Only two product defects are repaired:

1. **My Book default-state mutation**
   - v1.2 `S(x)` mutated the shared `DEF` array when no localStorage record existed;
   - after save → clear, a user-created entry could persist in the in-memory default set;
   - v1.3 copies the current list before `unshift`:
     `const d=[...G()]`.

2. **Print fallback handler collision**
   - v1.2 relied on `print.onclick=...`;
   - in the browser, `window.print` is already a global API and the named element binding is not a safe target;
   - the print button therefore did not switch to ROUTE or invoke the intended handler under actual Chromium execution;
   - v1.3 binds explicitly:
     `document.getElementById('print').onclick=...`.

No IA, content, route geometry, visual language, state model or field claim is redesigned.

## Runtime verification target

Dedicated Playwright verification uses the repository's existing browser runtime:

- Chromium desktop: 1440×1000;
- Chromium mobile: 390×844.

Coverage:
- TODAY / ROUTE / READ / MY BOOK / SERVICE view execution;
- UNKNOWN / FAIL-CLOSED service state;
- route mode + travel-focus state;
- imprint dialog → My Book save;
- My Book localStorage write / clear / default reset;
- print fallback → ROUTE → browser print call;
- page-level horizontal overflow;
- JavaScript runtime errors.

The browser gate is configuration-bounded. It does not claim Firefox/WebKit parity.

## Discovery history

### Browser run 1
Harness failure before product execution:
- wrong `tests/tests/serve-static-root.mjs` path.

### Browser run 2
Harness failure before product execution:
- readiness URL pointed at repository root without `index.html`.

### Browser run 3
Real product execution:
- 6 PASS / 6 FAIL across desktop + mobile;
- route-focus failure = test selector ambiguity, not product behavior;
- My Book clear failure = real v1.2 product defect;
- print fallback failure = real v1.2 product defect.

The two harness failures remain useful provenance and are not described as product failures.

## Verified browser result

Actual configured runtime verification is now complete.

Primary successful run:
- GitHub Actions run `35419536754` / run #4;
- Chrome for Testing `151.0.7922.34`;
- Playwright `chromium v1234`;
- desktop `1440×1000`;
- mobile `390×844`;
- result: `12 PASS / 0 FAIL`.

Latest evidence-head recheck:
- browser workflow run #14 / run ID `35419829083`;
- result: `PASS`.

Machine readback:
- `BROWSER_RUNTIME_READBACK_v1_3.json`;
- `QC_READBACK_v1_3.json`.

The result is configuration-bound and does not add Firefox/WebKit, user-validation, accessibility, field or live-service claims.

---

## Truth boundary

Unchanged:
- map is relationship/NTS, not measured geometry;
- no live operation claim;
- UNKNOWN stays fail-closed;
- route/safety/return do not depend on app completion;
- FIELD OBSERVED=0;
- FIELD MEASURED=0;
- G1F HOLD;
- NO_PROMOTION.

## Professional boundary

A future browser-runtime PASS may verify `C04-SYSREQ-006` and `IF-BROWSER-RUNTIME` only for the tested Chromium configurations.

It does **not** prove:
- representative-user success;
- usability;
- accessibility conformance;
- official live-status integration;
- physical/paper/human fallback;
- field truth;
- Systems Engineering professional PASS;
- HCD validation;
- promotion.

`STATIC PASS ≠ RUNTIME PASS`.

`RUNTIME VERIFICATION ≠ USER VALIDATION`.
