# OLEANDER Game UI Skill Stack v0.1

Status: `CANDIDATE / NOT PROMOTED`

This stack groups five candidate specialist Skills for routing/testing. It is not an independent execution owner and must not behave like a monolithic hidden Skill.

## Skills
1. `oleander-game-ui` — game-facing hierarchy, HUD, world/UI cohesion, anti-dashboard, game feeling without unauthorized gamification.
2. `oleander-mobile-game-ui` — touch ergonomics, safe areas, thumb zones, gesture discoverability, narrow-screen density, Reduced Motion.
3. `oleander-ui-visual-composition` — First Visual Gate, hierarchy, composition, typography, imagery, depth, project specificity, professional finish.
4. `oleander-route-wayfinding-ui` — source-grounded route extraction, node hierarchy, route modes, wayfinding, Return, relational maps, optional-content separation.
5. `oleander-ui-interaction` — state machines, focus, interruption, Return priority, input routing, re-entry, progressive disclosure.

## Existing OLEANDER owners remain authoritative for their domains
- `oleander-motion` remains the temporal timing/easing/continuity/runtime owner.
- `oleander-story-and-board` remains story/claim/visual sequencing authority.
- `oleander-delivery-qc` remains packaging/export/runtime delivery QC.
- existing research/data/3D Skills are unchanged.

The candidate stack extends these capabilities; it does not replace them.

## Current routing rule｜MINIMUM SUFFICIENT OWNER SET

The old default-full-chain interpretation is superseded. Do **not** automatically run:

`game-ui → visual-composition → interaction → motion → mobile → review`.

Resolve the required native output first, then include only owners that contribute a required artifact, state behavior, runtime gate or independent review.

### Game-like static screen / pixel-composition task
Primary candidate owner:

`oleander-game-ui`

Add `oleander-ui-visual-composition` only when composition/typography/imagery/depth requires specialist work.

Do not add `oleander-ui-interaction`, `oleander-motion` or `oleander-mobile-game-ui` unless interaction, temporal behavior or mobile recomposition is actually required.

### Interaction/state defect
Primary candidate owner:

`oleander-ui-interaction`

Add:
- `oleander-motion` only when the defect includes timing/easing/transition/interruption behavior;
- `oleander-mobile-game-ui` only for narrow-screen/touch/safe-area constraints;
- `oleander-ui-visual-composition` only if the state defect also changes first-read/hierarchy.

### Route / wayfinding screen
Primary candidate owner:

`oleander-route-wayfinding-ui`

Add by need:
- `oleander-data-viz` for data/GIS encoding;
- `oleander-game-ui` for authorized game-like world/UI cohesion;
- `oleander-ui-interaction` for route state/Return interaction;
- `oleander-motion` for temporal route behavior;
- `oleander-mobile-game-ui` for mobile ergonomics;
- `oleander-ui-visual-composition` for screen-level visual hierarchy.

The route owner must not redraw or distort source-authoritative route geometry merely to satisfy layout.

### Mobile-only recomposition
Primary candidate owner:

`oleander-mobile-game-ui`

Consume an upstream screen/state artifact with `READ_ONLY` or `MUTATE_PRESENTATION_ONLY` permission. Do not silently redefine desktop/source semantics.

### Motion-only delta
Primary installed owner:

`oleander-motion`

Static effect-state semantics remain with the originating visual owner / `T-VISUAL-IMAGE-OPS-001`; Motion owns temporal behavior only.

### Pixel polish only
Primary candidate owner:

`oleander-ui-visual-composition`

`oleander-game-ui` is added only if anti-dashboard/world cohesion/game-language judgment is materially needed.

### Independent review
Add an `INDEPENDENT_REVIEWER` node only when Professional Design promotion/review is required. Producer self-check cannot serve as the independent verdict.

## DAG handoff permissions

Use the Current `OLEANDER_MULTI_SKILL_EXECUTION_DAG_CONTRACT_v0.1`:

- default = `READ_ONLY`;
- `DERIVE` for a new downstream derivative;
- `MUTATE_PRESENTATION_ONLY` for crop/layout/styling that preserves upstream semantics;
- `MUTATE_AUTHORIZED_SOURCE` only when Current Authority explicitly grants it.

No candidate specialist may silently overwrite another owner's authoritative master.

## Non-negotiable OLEANDER rules
- Current Notion Root Authority + live Registry precede this router.
- `USE EXISTING → EDIT/CURRENTIZE → RESTRUCTURE → DEEPEN → ADD GAP → REBUILD ONLY WITH REASON`.
- `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`.
- `NO LOSS` does not mean “run every Skill”.
- `Artifact existence ≠ Design quality`.
- `Runtime/CI PASS ≠ Design PASS`.
- `Regression PASS ≠ Design KEEP`.
- `Concept Keep ≠ Pixel Keep`; `Pixel Fail ≠ Design Delete`.
- Producer self-evaluation is forbidden for final quality status when independent review is required.
- External skill/source material is evidence/inspiration only, not project authority.

## Promotion gate
These files remain `candidate` until all are true:
1. frontmatter/schema lint passes;
2. machine-readable candidate Golden Cases are executed;
3. no regression against existing OLEANDER design review baseline;
4. no conflict with Existing Mature Design First / independent review / no-loss rules;
5. at least one real UI object is reviewed using the relevant minimum sufficient owner set and findings are materially useful;
6. independent reviewer approves promotion.

Do not mark these Skills `current`, `approved`, or `promoted` merely because a PR merges.
