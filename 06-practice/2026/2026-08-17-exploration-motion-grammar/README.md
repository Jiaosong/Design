# OLEANDER Exploration Motion Grammar Lab — 2026-08-17

## Decision question
How can a multi-step exploration experience stop behaving like a collection of isolated `fade / reveal / glow / withdraw` effects and become one legible, reversible behavioral motion grammar?

## Existing-first check
- Reused `oleander-motion` canonical method and AR-S10 rather than creating a parallel motion framework.
- Reused the 2026-08-14 MOT-02 result: task-bearing state change leads; secondary motion follows only when it encodes subordinate state relation.
- This round does **not** repeat MOT-02 timing/state hierarchy. It targets MOT-03 Spatial Continuity + Narrative across a multi-step journey.
- Project trigger: recent C04/QJ digital review reported that motion remained mainly fade/reveal/glow/withdraw and had not formed a complete exploration behavior grammar.

## Practice
Two real HTML/CSS/JS candidates share the same abstract mountain/route scene.

### Candidate A — effect-first
`ARRIVE / CONFIRM / ENTER / ORIENT / RETURN` are presented mainly by fade, glow and reveal. Appearance changes but source/destination, spatial continuity and return logic are not encoded.

Decision: `REJECT`.

### Candidate B — behavior grammar
Training sequence:

`APPROACH → CONFIRM → ENTER → ORIENT → RETURN`

This sequence is a project-derived example, **not** a universal required vocabulary.

Behavior rules tested:
- persistent world/route remains visible across adjacent states;
- world relationship changes before a dominant overlay is introduced;
- forward and backward navigation use the same spatial grammar;
- relation panel appears only where a decision/relationship needs explanation;
- RETURN restores the same continuity instead of using a separate exit effect;
- Reduced Motion preserves state, copy, route relation and return logic with near-instant transitions.

## Runtime execution
Runtime: system Chromium through Playwright `page.set_content` because direct `file://` navigation is blocked by administrator policy.

Executed sequence:
`0 → 1 → 2 → 3 → 4 → 3 → 2 → 1 → 0`

Observed desktop world transforms:
- APPROACH: identity;
- CONFIRM: scale 1.025 / translate -16,4;
- ENTER: scale 1.065 / translate -38,12;
- ORIENT: scale 1.035 / translate -62,16;
- RETURN: identity;
- reverse path reproduces the same intermediate transforms in reverse order.

Reduced Motion test: computed world transition duration `1e-06s`; ORIENT state text and relation copy remain present.

## Design Crit
### v1 — REVISE
Desktop first-read was strong, but the actual 390×844 runtime proof exposed:
- absolute node labels clipping at scene edges;
- relation card competing with route information;
- return guidance and state chip crowding one another;
- desktop world translation amplitude too strong for the narrow viewport.

### v2 — KEEP / PRACTICE ASSET
Repairs:
- hide non-critical absolute node labels on small screens while retaining topology markers;
- reduce world translation/scale amplitude on mobile;
- center the current relation card inside the safe reading zone;
- separate return guidance and state chip vertically.

390×844 retest: `scrollWidth == clientWidth == 390`; no page-level horizontal overflow.

## Independent design-quality result
- First visual gate: PASS for v2 — Candidate B reads as one route/world before UI detail.
- Composition: PASS desktop and mobile after v2 repair.
- Hierarchy: PASS — world/route → current relation → state text; overlay does not become the primary world.
- Typography: PASS for training use; secondary metadata remains subordinate.
- Spatial realism: N/A as site proof; abstract relation scene only.
- Scale: RELATIONAL / NTS only.
- Interaction/narrative: PASS for the designed grammar; NOT USER TESTED.
- Reduced Motion information equivalence: PASS in executed runtime.
- Professional finish: KEEP as a training/runtime calibration asset, not as a C04 production screen.

## Failure knowledge
- Smooth transitions do not create continuity if every screen behaves as a new overlay.
- `fade / glow / reveal` are reinforcement effects, not behavioral verbs.
- Desktop motion quality cannot override mobile clipping/crowding.
- Reverse/back behavior must be tested as a sequence, not inferred from forward animation.
- A world-first experience becomes UI-first if each state transition replaces the world with a dominant panel.

## Skill delta
Existing `oleander-motion` is extended with `Exploration behavior grammar gate` under MOT-03/Narrative. No new Skill is created.

Candidate reusable rule:
`Journey / Task State → Behavioral Verb → Persistent World/Object → Relationship Change → Motion Mechanism → Reverse/Recovery → Reduced Motion`

## Transfer boundary
Applies to route/travel interfaces, museum/exhibition journeys, game-like discovery, spatial interpretation, onboarding with persistent objects, product assembly/disassembly and other multi-state experiences where continuity matters.

Does not require every experience to use `approach → confirm → enter → orient → return`, does not prove user comprehension, and does not replace field, engineering, accessibility or implementation validation.
