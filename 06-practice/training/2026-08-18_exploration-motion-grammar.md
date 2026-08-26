# 2026-08-18｜Game UI / Interaction Practice Evidence｜Exploration Motion Grammar

## Identity / Authority Boundary
Historical title alias: `2026-08-18｜Game UI / Interaction L5｜Exploration Motion Grammar`.
This file is supporting Practice Evidence / training narrative. It is not a second Current L5 Canonical knowledge object and does not self-authorize `KEEP / MAIN / Design PASS`.

## Training question
How can an exploration interface feel authored across multiple screens without degenerating into unrelated `fade / reveal / glow / withdraw` effects or a dashboard overlay?

## Real project trigger
Current C04 Digital Companion material states:
- ROUTE: `BASE ROUTE strong / DISCOVERY weak`;
- exploration should come from route choice, local reveal, and personal trace rather than task completion;
- CH11 still lists `Motion Grammar` as an unformed Expansion candidate;
- R06 and R13 already require different behavioral reading conditions, so one generic transition cannot serve every state.

This is a material delta from the prior Shared Container Continuity practice. That earlier practice tested one parent→child transition and one dominant motion carrier. This practice tests **cross-screen behavioral consistency**.

## Existing skills reused
- `skills/oleander-game-ui/SKILL.md` — world first, anti-dashboard, state-specific HUD, reversible exploration.
- `skills/oleander-ui-interaction/SKILL.md` — state before animation, interruption, Return priority, progressive disclosure, reduced-motion equivalence.
- Prior Motion training — Shared Container Continuity: `ONE CAUSAL STATE CHANGE → ONE DOMINANT MOTION CARRIER`.
- OLEANDER Artifact Review System v1.1 — Compliance and Professional Design are separate gates.

No new parallel skill was created.

## Practice asset
`06-practice/training/assets/OLEANDER_C04_EXPLORATION_MOTION_GRAMMAR_R01.svg`

Editable 1920×1080 vector state-board using one constant world geometry and four sampled states:
1. SEEK / WORLD FIRST
2. FOCUS / ONE ACTIVE OBJECT
3. REVEAL / EXPLANATION SECOND
4. RETURN / PRIORITY INTERRUPT

The full grammar tested is:

`SEEK → APPROACH → FOCUS → ENTER → REVEAL → WITHDRAW → RETURN`

The asset is intentionally schematic and source-bounded. It does not claim C04 field geometry, production UI, GPS truth, live service state, or target-runtime validation.

## Producer-side Design Readback / Independent Review Boundary
### Gate 1 — Compliance evidence
**PASS FOR TRAINING**
- explicit project/training identity;
- source/truth boundary is visible;
- one world geometry is preserved between states;
- no compulsory checkpoint, XP, completion rate, or invented route fact;
- Return remains visually and semantically higher priority than optional explanation.

### Producer-side visual/design readback
**SUPPORTS TRAINING CANDIDATE ONLY — NOT AN INDEPENDENT VERDICT**

Observed checks:
- First visual: world/route reads before dashboard chrome in the training board.
- Composition: dominant landscape field remains stable; overlays occupy bounded secondary regions.
- Proportion: route, markers, focus halo, and reveal layer have a legible visual scale order.
- Hierarchy: world > active route/object > explanation > metadata.
- Typography: initial Cairo render used a non-CJK font and produced missing-glyph boxes; SVG was switched to `Noto Sans CJK SC` and re-rendered.
- Material/spatial reality: schematic training language only; NOT a field/terrain claim.
- Scale: HOLD for project transfer — no C04 field scale or device ergonomics is proven by this board.
- Node readability: one active node, no peer competition in the specimen.
- Interaction/narrative: sampled states encode different information roles rather than only different visual effects.

### Independent Professional Design Review
**NOT RUN / HOLD**
Producer-side readback, editable-asset existence, runtime evidence, CI, or training quality observations do not authorize `KEEP / MAIN / Design PASS`.

Root cause preventing MAIN promotion: **the grammar has formed reviewable training evidence, but independent Professional Design Review, current C04 production-surface binding, and target-runtime validation remain open.**

## Failure knowledge
### Failure 1 — effect vocabulary mistaken for behavior grammar
`fade / reveal / glow / withdraw` describes rendering techniques, not user-state semantics. Using them as the whole motion system allows every screen to feel unrelated while still appearing animated.

Correction: define verbs by information role first: SEEK, APPROACH, FOCUS, ENTER, REVEAL, WITHDRAW, RETURN; assign animation only after the state meaning is fixed.

### Failure 2 — explanation can quietly become a dashboard
A reveal panel can be visually polished yet still replace the world and recreate the same UI-overlay problem.

Correction: world geometry remains continuous; reveal occupies a bounded secondary layer and is reversible.

### Failure 3 — residual selected state after withdrawal
Persistent glow, panel residue, or route emphasis makes the UI imply that an object remains active after the user has left it.

Correction: WITHDRAW is an explicit grammar verb whose job is to clear explanatory and selected-state residue before restoring exploration.

### Failure 4 — typography fallback broke the artifact
The first vector preview rendered Chinese as missing-glyph boxes under an unsuitable font family.

Correction: render with an installed CJK vector font (`Noto Sans CJK SC`) and reopen the final PNG preview before review. File generation alone was not counted as design success.

### Invalid method
Adding more glow, particles, scan lines, or longer easing does not fix weak discovery structure. Visual intensity cannot substitute for state meaning.

## Skill delta
Modified existing `oleander-game-ui` from v0.1.0 to v0.1.1.

Previous gap:
- the skill named discovery / approach / focus / reveal / route continuity separately, but did not require a reusable cross-screen behavior grammar or a coverage test;
- therefore a product could technically satisfy the listed states while TODAY, ROUTE, READ, MY BOOK, and Return still felt like unrelated products.

Change:
- added `Exploration motion grammar gate`;
- defined the reusable reversible grammar and semantic role of each verb;
- added a multi-screen coverage test;
- added workflow step for grammar mapping before game-feeling polish;
- added hard-failure conditions for unrelated peer-screen transition idioms, panel-first Reveal, and stale state after Withdraw;
- added `EXPLORATION GRAMMAR COVERAGE` to review output.

Reason:
Cross-screen consistency must be judged at the level of behavior semantics, not by whether every screen contains animation.

## Cross-project transfer
Applicable to:
- C04 Digital Companion: TODAY / ROUTE / READ / R06 / R13 / MY BOOK / SERVICE-RETURN transitions;
- other OLEANDER map, museum, travel, spatial companion, and game-like exploration interfaces;
- web/mobile products where a stable world/canvas is progressively focused and explained;
- 3D viewers where the same scene is approached, focused, inspected, withdrawn, and returned from.

Not applicable without modification to:
- transactional forms where exploration is not the primary behavior;
- genuinely different scenes whose world geometry changes by authority;
- irreversible destructive actions, payment, or consent flows;
- safety-critical flows where immediate explicit UI must replace immersive layering;
- motion that exists only for brand expression with no state transition.

## Runtime / environment note
Chromium 144 exists in the environment, but both direct headless capture and Playwright navigation to local `file://` / localhost were blocked by the runtime administrator policy during this run. Therefore:
- editable SVG + Cairo PNG preview = EXECUTED and visually reviewed by the producer;
- browser target-runtime interaction validation = HOLD;
- no browser PASS is claimed.

## Promotion status
- Training artifact: `EXECUTED / CANDIDATE EVIDENCE / INDEPENDENT REVIEW HOLD`
- Skill delta: `CANDIDATE / MATERIAL DELTA`
- C04 project asset promotion: `NO`
- FIELD OBSERVED / MEASURED: unchanged / not proven
