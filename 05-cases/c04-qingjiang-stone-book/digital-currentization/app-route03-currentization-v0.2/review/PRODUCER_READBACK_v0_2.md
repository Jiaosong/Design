# C04 App ROUTE-03 Currentization v0.2 — Producer / Runtime Readback

This record reports deterministic implementation and runtime facts only. It does not issue a design verdict.

## Executed architecture / states
- Boot at project-default `UNKNOWN`: SERVICE / Return first; APP_INIT is not shown ahead of fail-closed.
- OPEN prototype state + first entry: APP_INIT mode step appears.
- MODE: QUICK / DEEP / FAMILY with explicit non-persona/non-level framing.
- OFFLINE PREP: second v1.26 setup step appears before route entry and distinguishes embedded/currentization content from integration-only content.
- OPEN route: source-bound ROUTE-03 viewport, DEEP mode carried into route state.
- OPEN reveal: contextual relation explanation available.
- Return during REVEAL: immediate transition to RETURN/SERVICE.
- Digital OFF: optional explanation withdraws and selection/reveal state clears; route and Return remain.
- UNKNOWN selected in prototype control: closing the control returns to fail-closed SERVICE.
- Reduced Motion: tested with `prefers-reduced-motion: reduce`; running animation count = 0.
- Keyboard ArrowRight changes route viewport scroll position.
- measured visible button target minimum = 44 px; no sub-44 px buttons found in the tested state.
- JS error recorder remained empty in tested states.

## Persistence boundary
v1.26 uses `localStorage` for `readingMode`, `setupSeen`, `offlinePrepared`, `generated`, and `readLater`. v0.2 implements a scoped currentization state key and updates `readingMode/setupSeen/offlinePrepared`; however, the CDP `about:blank` execution surface returns `SecurityError` for localStorage. Therefore state mutation is runtime-observed, but cross-reload persistence is **not claimed as verified** in this pass.

## Deterministic defects found and repaired in v0.2
1. **APP_INIT originally appeared ahead of fail-closed.** Repaired to match v1.26/v1.27 ordering: UNKNOWN/CLOSED → SERVICE first; permitted state → APP_INIT/route.
2. **OFFLINE PREP was omitted.** Reintroduced as a second setup step, but old 18-node topology claims were not revived; current text points to ROUTE-03 and marks full R01–R13 pages as integration scope.
3. **Stale withdrawal timer overrode RETURN.** Digital OFF scheduled a later `INTENT`; Return now cancels pending behavior reset timers.
4. **Root data attributes were accidentally treated as controls.** Broad selectors could replay state handlers on unrelated clicks; selectors are now scoped to actual control groups.
5. **Touch target width defect.** System-sheet close control was 44 px high but under 44 px wide; repaired.
6. **Digital OFF initially left stale explanation visible.** OFF now performs withdrawal, clears selection/reveal, then restores route INTENT.
7. **APP_INIT retained stale RETURN behavior after leaving fail-closed.** `openSetup()` now clears pending behavior and enters `INTENT` before MODE/OFFLINE_PREP.
8. **System control could close onto a fail-closed route.** Closing the panel now re-applies fail-closed and lands SERVICE when state is UNKNOWN/CLOSED.

See `RUNTIME_READBACK_v0_2.json` and the 390×844 / 430×932 screenshots.

`Runtime/implementation facts ≠ Design PASS`.
