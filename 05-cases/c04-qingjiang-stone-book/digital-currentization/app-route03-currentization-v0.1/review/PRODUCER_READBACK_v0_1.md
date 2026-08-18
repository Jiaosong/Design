# C04 App ROUTE-03 Currentization Module — Producer Readback v0.1

Project: `PRJ-C04-QINGJIANG-SHISHU`  
Workstream: `PRJ-C04-DIGITAL-INTERACTION`  
Artifact: `C04_APP_ROUTE03_CURRENTIZATION_v0_1`  
Status: `EXECUTABLE MODULE CANDIDATE / NOT APP CURRENT / INDEPENDENT FINISHED-PIXEL DESIGN REVIEW REQUIRED`

## 1. Authority reconciliation
- Current C04 project structure remains external to this module; this artifact does not promote project state.
- `ROUTE-03 = LOCKED CURRENT` is consumed as route geometry/source carrier authority.
- The later discovered App v1.27 is treated as `USER-OWNED CANDIDATE PROVENANCE / UNSYNCED`, not automatically Current.
- v1.27 product/IA improvements are inherited selectively: four top-level destinations, route-context descendants, Return Guard, mobile target baseline, Reduced Motion and fail-closed UNKNOWN.
- v1.27 embedded custom 18-node guide-route geometry is not retained as current route geometry authority.

## 2. Existing-first execution
No full App rebuild was attempted. This bounded module answers one material delta only:

> Can the mature v1.27 interaction architecture consume the exact locked ROUTE-03 source carrier without maintaining a second route curve, while preserving mobile exploration and Return interruption?

The answer is implemented as an executable integration module, not asserted as a design verdict.

## 3. Exact design / implementation delta
- exact `ROUTE-03` SVG copied as source-bound local asset;
- presentation derivative changes only root `viewBox`/height to isolate the route-map field for mobile viewport use;
- no route path, node, label, or text geometry is redrawn in the derivative;
- mobile world is a pannable viewport rather than a shrunken full-sheet mini-map;
- behavior grammar: `INTENT → SCOUT → COMMIT → REVEAL → RETREAT / RETURN`;
- 44px+ interaction targets;
- Return can interrupt COMMIT/REVEAL immediately;
- `STATUS UNKNOWN / NTS / NOT GPS` remains visible;
- optional reading is explicitly separated from route authority and field proximity remains open;
- Reduced Motion removes transition waits/animations rather than hiding only CSS effects.

## 4. Runtime evidence
Executed in System Chromium / Playwright via `page.set_content` with exact local CSS/JS/SVG bytes inlined because direct file/localhost navigation is blocked on the execution surface.

Tested: `390 × 844`, `430 × 932`, mode change, source-anchor commit, reveal, Return interruption, resume, keyboard pan, Reduced Motion, console/page errors.

Machine/runtime result: no recorded JS/page errors; document width equals viewport width at both target sizes; Reduced Motion reports zero running animations in the tested state.

This proves runtime behavior only. `Runtime PASS ≠ Design PASS`.

## 5. Producer defect discovery and repair
During actual screenshot readback, three defects were found and repaired before packaging:
1. Programmatic initial scroll incorrectly pushed behavior from INTENT to SCOUT → corrected.
2. Butterfly Cliff context could open while the world viewport still showed a different area → commit now centers the exact anchor before context reveal.
3. Directly embedding the full technical source sheet exposed its title/footer inside the App viewport → replaced with a viewBox-only presentation derivative; route geometry/content remains unchanged.

These are producer repairs, not an independent quality verdict.

## 6. Skill routing actually applied
Relevant current candidate stack:
`oleander-route-wayfinding-ui → oleander-game-ui → oleander-ui-visual-composition → oleander-ui-interaction → oleander-motion → oleander-mobile-game-ui`.

Applied concerns: source topology before styling; world-first/anti-dashboard; mobile route as a viewport into a larger world; Return recoverability; interruption/re-entry; 44–48px touch targets; Reduced Motion; no unauthorized XP/completion/mandatory 13/13 logic.

## 7. Open items / blockers
- The actual v1.27 portable source exists in File Library, but was not materialized as writable source bytes in the active runtime, GitHub, or connected Drive. Therefore this module is **not falsely merged into v1.27**.
- Full App regression across TODAY / ROUTE / MY BOOK / SERVICE and READ / R06 / R13 remains required after source materialization.
- Route-to-Rxx physical proximity remains `FIELD OPEN`; this module does not create proximity truth.
- Live status, GPS, distance, slope, accessibility, safety, operational capacity and field conditions are not validated.
- Independent finished-pixel Design Crit is pending. Producer does not issue `KEEP / MAIN / Design PASS`.

## 8. Truth boundary
`FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT GPS / STATUS UNKNOWN`
