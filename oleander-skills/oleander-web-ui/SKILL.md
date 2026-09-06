---
name: oleander-web-ui
description: Coordinate Oleander web/UI production as an end-to-end browser-delivery route while reusing the existing UI specialist Candidate owners for visual composition, interaction, route/wayfinding and game/mobile-game UI when applicable. Use for responsive browser integration, cross-specialist handoff, state/browser readback and final web delivery coordination.
compatibility: Candidate composite route, not a replacement specialist owner. Generic UI defaults to repo-native HTML/CSS/JS/SVG plus real browser readback. Figma is explicit-only for an explicitly requested editable Figma deliverable or continuation/repair of an existing authoritative Figma source. Existing UI specialist owners and minimum-sufficient-owner routing remain authoritative.
---

# Oleander Web UI

Coordinate real, editable browser interfaces without duplicating the specialist skills that already exist in the OLEANDER execution-owner system.

## Lifecycle role

- Primary: `PRESENTATION`
- Secondary: `DESIGN`, `VALIDATION`
- Status: `CANDIDATE_COMPOSITE_ROUTE`
- Upstream: `oleander-design-process`, `oleander-visual-design`, `oleander-data-viz`
- Downstream: `oleander-motion`, `oleander-delivery-qc`

## Existing specialist ownership — mandatory reuse

Before web/UI execution, resolve the Current Skill Capability Contract and minimum sufficient owner set. Reuse these existing Candidate specialists when their authority is required:

- `oleander-ui-visual-composition` — static screen hierarchy, typography, imagery and depth treatment;
- `oleander-ui-interaction` — interaction state logic, interruption and re-entry;
- `oleander-route-wayfinding-ui` — route topology/state/Return-recovery interface;
- `oleander-game-ui` — authorized game-like UI execution;
- `oleander-mobile-game-ui` — authorized mobile-game UI execution.

This core route must **not** copy those specialist methods into itself, claim their specialist authority, or automatically run all of them. Select the minimum sufficient existing owner set for the actual task.

`CORE ROUTE ≠ HIDDEN REPLACEMENT SKILL`

`11-CORE IDENTITY ≠ INSTALLED EXECUTION OWNER`

## Specialist extension routing

After resolving the minimum sufficient owner set, read the minimum relevant Candidate extension when the task exposes one of these deeper integration problems:

- `INFORMATION_ARCHITECTURE_WAYFINDING_EXTENSION.md` — user-task entry points, canonical homes, placement/labels, deep-route orientation, Return/recovery and wayfinding semantics;
- `RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION.md` — hierarchy-to-space translation, content-driven breakpoints, reflow, state footprints and responsive media;
- `ACCESSIBLE_INTERACTION_EXTENSION.md` — semantic primitives, keyboard/focus behavior, programmatic names/states, dynamic announcements and user-preference modes;
- `SEMANTIC_UI_TOKEN_THEME_EXTENSION.md` — semantic token roles, theme mappings, raw-value bypass control and rendered state × theme verification.

Typography/iconography/brand-rule/design-language reconstruction may co-route to the relevant `oleander-visual-design` extensions when those are system-level concerns. These files deepen integration and review; they do not replace the existing route/interaction/visual specialist owners.

Preferred order when IA, layout and accessibility all apply:

`TASK / IA → WAYFINDING SEMANTICS → WITHIN-PAGE LAYOUT → INTERACTION STATE → ACCESSIBILITY CROSS-CHECK → MOTION → REAL BROWSER RETEST`.

Token/theme work sits under the Current design authority throughout this route. It may be resolved before or during implementation when shared semantic roles are material; it is not a final visual-polish substitute.

Accessibility is not deferred to the end; the final cross-check repeats checks that should already have shaped primitive, DOM, focus and state choices during implementation.

## What this core route owns

Only the integration layer:

- end-to-end repo-native web/UI delivery contract;
- Required Native Output coordination across selected specialists;
- one Current editable browser source identity;
- cross-specialist HTML/CSS/JS/SVG integration;
- responsive/browser target matrix;
- cross-specialist handoff integrity;
- actual browser readback coordination;
- return of technical defects to VALIDATION and visual defects to PRESENTATION/DESIGN.

It does not own specialist visual-composition semantics, interaction-state authority, route topology truth, game authorization, motion timing theory, backend correctness or promotion.

## Required sequence

`CURRENT AUTHORITY → STICKY CONSTRAINTS → EXISTING SPECIALIST OWNER RESOLUTION → MINIMUM SUFFICIENT OWNER SET → REQUIREMENT COVERAGE MAP → SOURCE-ASSET ROLE PASS → REFERENCE DECOMPOSITION WHEN APPLICABLE → REQUIRED NATIVE OUTPUT → INFORMATION / STATE MODEL → EDITABLE HTML/CSS/JS/SVG INTEGRATION → REAL BROWSER → DESKTOP/MOBILE + HIGH-RISK STATE READBACK → RENDERED DELTA REVIEW → VISUAL + INTERACTION CRIT → REPAIR → RETEST`

## Requirement coverage map

Before material implementation, convert the user/project request into a compact acceptance map. Each material requirement should resolve to:

`REQUEST / SOURCE → TARGET REGION OR COMPONENT → REQUIRED STATE / BEHAVIOR → ACCEPTANCE EVIDENCE → STATUS`.

Use stable object/section/component identities. Name approved omissions explicitly. A page that looks complete but silently drops a requested asset, state, behavior or proof object is `REVISE`, not complete.

This map is a coordination artifact, not visible page copy.

## Source-asset role pass before IA lock

When real images, video, models, diagrams, maps or screenshots exist, classify them before final information architecture and layout density are frozen:

- source/master identity and authority;
- intended narrative role;
- usable resolution / aspect / crop tolerance;
- claim-bearing content that must survive crop or masking;
- target reading distance and responsive behavior;
- fallback or omission when the source is too weak.

Use:

`SOURCE ASSET INVENTORY → ROLE / AUTHORITY / USABILITY → NARRATIVE DUTY → IA / LAYOUT`.

Do not finish a generic layout first and then force evidence assets into leftover slots.

## Browser-stable source delivery｜project-feedback addition 2026-09-07

Real C04 browser use exposed a failure mode where layout, interaction and responsive structure executed correctly while required claim-bearing image carriers still failed because the browser depended on unstable remote thumbnail delivery. Treat this as project usage evidence for the Candidate route, not as promotion evidence.

`SOURCE AUTHORITY ≠ DELIVERY CARRIER`.

When a semantic/source asset is required for the page to make its claim:

1. preserve the source/master authority and provenance;
2. when authority permits, resolve exact bytes or a traceable derivative identity and hash before relying on browser delivery;
3. use a browser-stable, repo/deployment-controlled carrier when the external carrier is not reliably reproducible;
4. preserve crop/role/claim-bearing content through the derivative;
5. test the actual target viewport/state in the real browser;
6. classify failure locally as `ASSET DELIVERY FAIL` when layout/state behavior is otherwise intact.

Preferred sequence:

`SOURCE AUTHORITY → EXACT BYTES / DERIVATIVE IDENTITY → CONTROLLED DELIVERY CARRIER → HTML/CSS/JS BINDING → REAL BROWSER → VIEWPORT / STATE READBACK`.

Do not treat repeated opaque URL swapping as a repair strategy:

`REMOTE THUMBNAIL FAIL → ANOTHER REMOTE THUMBNAIL → ASSUME FIXED` = `REVISE`.

Current-role hygiene is part of integration integrity. Decide whether a generated file is `Native Master / Current Derivative / Support / Evidence / Provenance / Temporary` before using `CURRENT/current` naming. A convenient repo file does not become a second Current Authority merely because the browser consumes it.

This project feedback proves the failure mode and repair direction only. Final C04 browser closure is still separate; `CONTROLLED CARRIER EXISTS ≠ BROWSER PASS ≠ DESIGN KEEP`.

See `PROJECT_USAGE_FEEDBACK_CURRENT.md` for the bounded evidence record.

## Reference-led adaptation

When a concrete reference, adopted version, screenshot, existing page or authoritative visual example is provided, do not reduce “reference-first” to palette or surface styling. Before implementation record the reference's structural grammar:

- section rhythm and density;
- dominant grid / alignment anchors;
- typography roles and scale relationships;
- media scale, crop and placement behavior;
- component state model;
- continuity devices between sections;
- motion ownership and interaction rhythm.

Then translate those relationships to the actual project authority and content. After implementation, compare the real rendered result and name visible deltas. `SIMILAR COLOR ≠ REFERENCE FIDELITY`.

## Continuous page grammar

For continuous responsive sites, make the page read as one authored system rather than unrelated screen blocks stacked vertically. Continuity may come from shared spacing/type grammar, repeated alignment anchors, one background/material field, sticky media, controlled overlap, crop rhythm or deliberate section bridges.

Hard seams or abrupt background resets are acceptable only when they express a real narrative/state boundary. They must not appear merely because each section was designed independently.

For intentionally sparse content, reduce section count and strengthen real proof objects instead of generating filler cards, fake metrics, icon walls or unsupported testimonials.

## Stable semantic identity

For dynamic rendering, editable HTML, filters, reordering or persisted local state, bind content/state to stable semantic IDs rather than DOM order. Reordering or deleting modules must not cause saved edits, interaction state or QA evidence to attach to a different object.

Prefer identities derived from object/section role, e.g. `project-qingjiang-result` or `hero-positioning`, not `item-03` when the order can change.

## Live-editable HTML presentation route

When the Required Native Output is a browser-based PPT/deck that must remain directly editable after delivery, use:

`oleander-skills/oleander-story-and-board/LIVE_EDITABLE_HTML_PRESENTATION_EXTENSION.md`.

This route keeps the slide text as live DOM text and requires stable semantic edit IDs, explicit edit mode, local persistence, navigation/editing shortcut isolation, portable HTML export, and real round-trip verification. The exported artifact must reopen in a clean browser context with the edited text embedded and must still support navigation, editing and re-export.

Do not treat browser-local persistence alone as delivery. `LOCAL SAVE ≠ PORTABLE EXPORT`.

## Rules

1. Generic UI does not probe, recommend, or create Figma by default.
2. Preserve one Current editable source. Screenshot/PNG/video is evidence or derivative, not the UI master.
3. Do not reimplement an existing UI specialist merely because a general web route is convenient.
4. Define information hierarchy, state semantics, navigation, Return/back behavior, focus/keyboard behavior, loading/error/empty states when applicable before decorative motion.
5. Responsive design is not proportional shrinking. Recompose hierarchy, crop, density, navigation and interaction for target viewports while preserving claim and state meaning.
6. Use real browser readback. Static export is not browser PASS.
7. Design Quality and technical browser validation are separate gates. Browser success cannot grant Design KEEP.
8. Reuse existing components/tokens when Current and fit; do not force a component library over a stronger project-specific design.
9. Keep formal text editable. Do not bake UI text into raster imagery when it must remain live or localized.
10. Record external assets, fonts, dependencies, runtime assumptions, selected specialist owners and known fallback behavior.
11. Any backend, authentication, persistence, payment, security or service claim requires separate evidence; a front-end prototype does not prove production backend correctness.
12. Do not use measurement, DOM geometry, computed-style checks or automated screenshot statistics as automatic aesthetic approval. They are execution evidence and risk signals; full rendered Design Review remains separate.
13. When a reference is authoritative for direction, record structural deviations after render instead of silently replacing it with a generic house style.
14. When content is genuinely sparse, prefer fewer stronger sections and real evidence over fabricated density.
15. For live-editable HTML decks, persist edits by stable semantic IDs, not DOM order; suppress slide navigation shortcuts while editable text has focus; and verify export/reopen/re-edit/re-export before claiming the function is delivered.
16. When navigation/IA is non-trivial, resolve canonical homes, stable labels, orientation and Return/recovery before final within-page composition.
17. Breakpoint names from a framework are test conveniences, not sufficient design reasons; content failure defines the real breakpoint.
18. Automated accessibility scans do not replace keyboard/focus/semantic/user-preference interaction evidence.
19. When a shared token/theme system exists, reusable components should consume semantic roles rather than scattered raw values; theme coverage must be verified in real material states instead of inferred from variable wiring.
20. A theme remap, token lint or standards check cannot self-award visual quality. `TOKEN PASS ≠ ACCESSIBILITY PASS ≠ DESIGN PASS`.
21. A Source Authority that is valid in Drive or another archive is not automatically a stable browser delivery carrier; test the actual delivery path.
22. A source-carrier failure must not be inflated into a whole-Web design failure when the evidence isolates the defect to asset delivery.
23. Do not create unregistered `CURRENT/current` file identities merely to make integration convenient; Current role must be legitimate before the name is used.

## Visual / runtime readback

At minimum inspect required target sizes and highest-risk states. For ordinary responsive work, include desktop and mobile. Check first-read, hierarchy, dominant mass, typography, spacing, image behavior, interactive affordance, state contrast, overflow, clipping, keyboard focus, Return/back behavior and whether specialist handoffs survived integration.

When a reference/adopted version exists, add rendered delta review: compare section rhythm, dominant alignments, type hierarchy, media scale/crop, continuity and interaction/motion model. Record whether differences are required by project content, intentional improvements, or regressions.

For non-trivial IA, include at least one deep-entry orientation/recovery attack. For responsive work, inspect widths around the real content break rather than only canonical device snapshots. For accessible interaction, test keyboard/focus and material dynamic states in addition to source/automated checks.

When semantic token/themes are material, include representative high-risk component/page states in each supported appearance and verify raw-value bypasses have not created theme drift.

For live-editable decks, also test edit-mode entry/exit, save, navigation isolation, portable export, clean-context reopen, second edit and re-export. Recheck edited text for overflow and composition regression.

## Handoff

Return:
- Current editable source path/identity;
- selected specialist owner set and why each was needed;
- requirement coverage map status;
- source-asset role inventory for material assets;
- source-delivery carrier identity/hash and browser stability state when claim-bearing external assets are material;
- reference decomposition and rendered deltas when applicable;
- target viewports and states;
- component/token dependencies;
- semantic token/theme authority and material state × theme readback when applicable;
- IA/wayfinding canonical-home and recovery status when applicable;
- content-driven breakpoint/reflow evidence when applicable;
- keyboard/focus/semantic/preference evidence when applicable;
- actual browser evidence;
- live-edit/export round-trip evidence when that route is active;
- visual issues returned to the relevant visual owner;
- interaction/state issues returned to the relevant specialist;
- technical issues for `oleander-delivery-qc` or VALIDATION;
- motion states for `oleander-motion` when needed;
- project-usage feedback action when a material reusable rule was confirmed/falsified/repaired;
- what remains HOLD.

## Candidate boundary

This is a Candidate composite core route, not an installed execution owner. Real project integration, browser readback, regression cases and explicit promotion evidence are required before any stronger maturity claim. Existing specialist Candidate owners remain authoritative for their scopes. `BROWSER PASS ≠ DESIGN PASS`; `CANDIDATE CORE ROUTE ≠ DEFAULT PRODUCTION OWNER`.