# PRESENTATION training evidence — responsive state continuity

- GAP → Responsive state continuity: an already-selected UI object can lose identity when desktop and compact layouts reorganize.
- SOURCE → Material Design / Google, `https://m1.material.io/`. Public guidance states that objects should remain in one environment without breaking continuity as they transform and reorganize. Site rights note: content/code are Apache 2.0 unless otherwise specified. Apple HIG Design Principles (2026-06-08) independently states that adaptive layouts should preserve a person's context and use natural animations to ease transitions; Apple documentation remains Apple copyrighted/proprietary reference material.
- ARTIFACT → Editable HTML/CSS/JS practice prototype; real Chromium desktop transition keyframe + compact settled state + Reduced Motion + 390px mobile. No generated image; text remains editable DOM/vector text.
- A/B → A rebuilds the responsive layout and resets selected `RETURN` to `ROUTE`; B1 preserves state but fades the whole interface away/reappears; B2 preserves DOM/state identity and uses native View Transition only for spatial reorganization.
- READBACK → A ends `ROUTE / SETTLED`; B1 ends `RETURN / SETTLED` but visually implies disappearance; B2 keeps `RETURN` before/mid/after transition, under Reduced Motion, and at 390px mobile.
- FAILURE/ROOT CAUSE → Responsive adaptation was treated as layout replacement rather than transformation of the same semantic object. State continuity and visual continuity were conflated.
- REPAIR/RETEST → Keep stable object/state identity; animate only the changed spatial relation when that motion clarifies relocation; retest mid-transition, settled, Reduced Motion, and actual compact viewport.
- TRANSFER RULE → `PRESERVE OBJECT ID + STATE → CHANGE LAYOUT RELATION → USE CONTINUITY MOTION ONLY IF IT CLARIFIES RELOCATION → RETEST MID / SETTLED / REDUCED / MOBILE`. `RESPONSIVE RELOCATION ≠ OBJECT RECREATION`.
- BOUNDARY → Do not copy Material/Apple visual identity, components, easing presets, colors, typography, or proprietary signatures. This evidence proves runtime state/spatial continuity only; it does not prove usability, comprehension, preference, or accessibility outcome.
- STATUS → `PRACTICE_EVIDENCE / MOTION×RESPONSIVE MATERIAL DELTA / NO PROJECT WRITE / NOT ACTIVE`.

## Existing-owner routing

Current `oleander-motion` already owns `MOT-03 Spatial Continuity`, `MOT-08 Motion Accessibility`, and real runtime attack. Current `oleander-web-ui` Candidate already covers responsive layout/browser integration. Combined coverage exceeds the threshold for a parallel Skill; absorb only this evidence into the existing training frontier. Candidate/Installed boundaries remain unchanged.
