# OLEANDER Game UI Skill Stack v0.1

Status: `CANDIDATE / NOT PROMOTED`

This stack adds five independent skills rather than one monolithic UI methodology.

## Skills
1. `oleander-game-ui` — game-facing hierarchy, HUD, world/UI cohesion, anti-dashboard, game feeling without unauthorized gamification.
2. `oleander-mobile-game-ui` — touch ergonomics, safe areas, thumb zones, gesture discoverability, narrow-screen density, Reduced Motion.
3. `oleander-ui-visual-composition` — First Visual Gate, hierarchy, composition, typography, imagery, depth, project specificity, professional finish.
4. `oleander-route-wayfinding-ui` — source-grounded route extraction, node hierarchy, route modes, wayfinding, Return, relational maps, optional-content separation.
5. `oleander-ui-interaction` — state machines, focus, interruption, Return priority, input routing, re-entry, progressive disclosure.

## Existing OLEANDER skills remain authoritative for their domains
- `oleander-motion` remains the motion timing/continuity/runtime skill.
- `oleander-story-and-board` remains story/claim/visual sequencing authority.
- `oleander-delivery-qc` remains packaging/export/runtime delivery QC.
- existing research/data/3D skills are unchanged.

The new stack extends these skills; it does not replace them.

## Default routing

### Game-like app / HUD / exploration screen
`oleander-game-ui → oleander-ui-visual-composition → oleander-ui-interaction → oleander-motion → oleander-mobile-game-ui → independent review`

### Route / map / node screen
`oleander-route-wayfinding-ui → oleander-game-ui → oleander-ui-visual-composition → oleander-ui-interaction → oleander-motion → oleander-mobile-game-ui → independent review`

### Pixel polish only
`oleander-ui-visual-composition → oleander-game-ui (anti-dashboard/world cohesion check) → independent review`

### Interaction defect only
`oleander-ui-interaction → oleander-motion → oleander-mobile-game-ui if mobile → runtime evidence → independent review if design changed`

## Non-negotiable OLEANDER rules
- `MASTER PROTOCOL → PROJECT STATE → SOURCE AUTHORITY → CURRENT TASK` before skill execution.
- `USE EXISTING → EDIT/CURRENTIZE → RESTRUCTURE → DEEPEN → ADD GAP → REBUILD ONLY WITH REASON`.
- `NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS`.
- `Artifact existence ≠ Design quality`.
- `Runtime/CI PASS ≠ Design PASS`.
- `Concept Keep ≠ Pixel Keep`; `Pixel Fail ≠ Design Delete`.
- Producer self-evaluation is forbidden for final quality status.
- External skill/source material is evidence/inspiration only, not project authority.

## Promotion gate
These files are `candidate` until all are true:
1. frontmatter/schema lint passes;
2. Golden Cases are executed;
3. no regression against existing OLEANDER design review baseline;
4. no conflict with Existing Mature Design First / independent review / no-loss rules;
5. at least one real UI object is reviewed using the full stack and findings are materially useful;
6. independent reviewer approves promotion.

Do not mark these skills `current`, `approved`, or `promoted` merely because the PR merges.