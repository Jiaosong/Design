# PRESENTATION training evidence — responsive hierarchy continuity

- GAP → A desktop composition can look correct while mobile collapse reverses `PRIMARY → ACTION → PROOF → SUPPORT` because source order was optimized for the wide grid.
- SOURCE → W3C WAI `Understanding SC 1.3.2 Meaningful Sequence` (updated 2025-09-16) + MDN `Ordering flex items` / CSS `order` guidance (page modified 2026-04-20). W3C requires a meaningful programmatic sequence when order affects meaning; MDN documents that CSS visual reordering does not change DOM/sequential keyboard order and warns against using it to repair source-order problems. Rights: standards/documentation reference only; no visual identity, component style, typeface, palette, preset, prompt, or fixed layout copied.
- ARTIFACT → Editable HTML/CSS/JS; real Chromium `1440×900` + `390×844`; keyboard focus-order readback; mobile grayscale/contact sheet. No generated image.
- A/B → A uses source order `PROOF → PRIMARY → ACTION → SUPPORT`, so desktop grid looks acceptable but mobile begins with proof. B1 visually repairs mobile with CSS `order`, yet keyboard focus remains `proof → primary → secondary → support`. B2 rewrites source order to `PRIMARY → ACTION → PROOF → SUPPORT` and uses CSS Grid placement only for wide-screen composition.
- READBACK → B2 mobile visual and focus order both begin `primary → secondary → proof → support`; desktop retains the same visual composition as A/B1 while PRIMARY keeps the largest visual mass. B1 is a looks-correct counterexample: pixels pass, focus/semantic order fails.
- FAILURE/ROOT CAUSE → Desktop coordinates were allowed to dictate DOM/source order. The first repair treated hierarchy as a pixel-only problem and hid the contradiction with CSS ordering.
- REPAIR/RETEST → Keep meaningful source order independent of wide-screen coordinates; use Grid position/visual mass to compose desktop; collapse without priority reversal; retest actual mobile pixels, grayscale, and keyboard order.
- TRANSFER RULE → `DECLARE SEMANTIC PRIORITY → ENCODE MEANINGFUL SOURCE ORDER → COMPOSE DESKTOP WITH GRID POSITION / VISUAL MASS → COLLAPSE WITHOUT PRIORITY REVERSAL → RETEST PIXELS + KEYBOARD`. `RESPONSIVE HIERARCHY ≠ CSS ORDER PATCH`.
- BOUNDARY → Proves source/visual/focus ordering consistency in Chromium only; does not prove preference, comprehension, or full accessibility conformance. Equal-order layouts remain valid where content is genuinely independent/comparative.
- STATUS → `PRACTICE_EVIDENCE / RESPONSIVE-HIERARCHY MATERIAL DELTA / NO PROJECT WRITE / NOT ACTIVE`.

## Existing-owner routing

Current `oleander-web-ui` Candidate already owns responsive layout/browser readback and `oleander-story-and-board` owns PRESENTATION narrative hierarchy. Combined coverage is sufficient; absorb this as evidence only. No new Skill, Registry change, Candidate promotion, or Project Current write.
