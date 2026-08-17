---
name: oleander-game-ui
description: OLEANDER game-interface design and review skill for HUDs, exploration interfaces, world overlays, game-like maps, journals, scene prompts, route feedback, and immersive product UI. Use when an interface must feel like a designed game surface rather than a generic app/dashboard while preserving product logic, accessibility, and project authority.
status: candidate
version: 0.1.0
---

# OLEANDER Game UI

## Purpose
Design and review game-facing UI as part of the world, not as a web dashboard laid over the world.

This skill controls visual hierarchy, HUD composition, world/UI cohesion, exploration feedback, scene-entry behavior, lightweight game feeling, and anti-dashboard quality. It does **not** authorize new product logic, routes, rewards, tasks, currencies, completion systems, or content facts.

## OLEANDER authority rules
1. Read the project authority chain before changing UI: `MASTER PROTOCOL → PROJECT STATE → SOURCE AUTHORITY → CURRENT TASK`.
2. Existing mature design is Design Source. Apply: `USE EXISTING → EDIT/CURRENTIZE → RESTRUCTURE → DEEPEN → ADD GAP → REBUILD ONLY WITH REASON`.
3. `Artifact existence ≠ Design quality`; `Runtime PASS ≠ Design PASS`; `Concept Keep ≠ Pixel Keep`; `Pixel Fail ≠ Design Delete`.
4. Producer output may report implementation facts and defects, but may not self-award `KEEP / MAIN / 9+ / Design PASS`.
5. Preserve project truth boundaries. Visual immersion may never imply field verification, GPS precision, live status, construction validity, or factual certainty that the source does not support.

## Core principles
### 1. Build the game interface, not a dashboard
Prefer authored clusters, world markers, compact HUD, contextual labels, progress traces, map cues, journals, reticles, state strips, diegetic or semi-diegetic signals, and direct manipulation over card grids and stat panels.

Reject by default:
- equal-weight card walls;
- nested cards;
- four-or-more peer dashboard controls competing with the world;
- large persistent explanatory headers over the play/exploration field;
- generic SaaS pills, metric cards, filter bars, and boxed summaries when an in-world or contextual expression is possible.

### 2. World first
Rank layers before styling:
1. world / landscape / playable or explorable object;
2. current objective, route, scene, or decision;
3. immediate feedback;
4. optional explanation;
5. flavor and decoration.

UI must not visually overpower the world unless safety, Return, error, or blocking state explicitly requires it.

### 3. Game feeling without compulsory gamification
Game feeling may come from:
- discovery;
- approach;
- focus/lock;
- scene entry;
- reveal;
- collection as memory;
- chapter/scroll progression;
- tactile imprint/record feedback;
- route continuity;
- reversible exploration.

Do not introduce XP, coins, chests, rarity, streaks, forced completion, mandatory checkpoints, quests, or reward economies unless they are already Current Authority.

### 4. UI/world cohesion
Derive perceptual language from the project world:
- geometry and silhouette;
- material cues;
- color roles;
- icon language;
- line behavior;
- motion language;
- density and negative space.

Do not apply generic neon, sci-fi glass, parchment, tactical HUD, or fantasy ornament merely because the interface is game-like.

### 5. State-specific HUD
Inventory actual states before polishing pixels. Typical states:
- world/default;
- approach/focus;
- scene entry;
- optional reveal;
- no-phone / digital-off;
- Return / exit;
- loading / unavailable / unknown;
- reduced-motion;
- keyboard/focus state.

Each state needs a reason for what appears, what retreats, and what remains interruptible.

## Workflow
1. **Authority readback** — identify immutable product logic, truth boundaries, existing mature visuals, and current delta.
2. **Screen intent** — state one primary user task and one primary visual object for each screen/state.
3. **World/HUD inventory** — list what belongs to world, route/objective, feedback, optional explanation, safety/Return, and flavor.
4. **Anti-dashboard pass** — remove panels, labels, boxes, and equal-weight controls that are not necessary for comprehension or recovery.
5. **Cohesion pass** — bind UI geometry/material/color/motion to the world and existing Design Source.
6. **Game-feeling pass** — add only stateful discovery/feedback behaviors that clarify approach, reveal, memory, or continuity.
7. **Responsive/mobile handoff** — invoke `oleander-mobile-game-ui` for touch, thumb-zone, target size, safe-area, and narrow-screen density.
8. **Interaction/motion handoff** — invoke `oleander-ui-interaction` and existing `oleander-motion` for interruption, re-entry, focus, reduced motion, and state transitions.
9. **Visual gate** — invoke `oleander-ui-visual-composition` for first read, composition, typography, depth, imagery, and professional finish.
10. **Independent review** — producer stops at evidence/defects; independent reviewer owns final quality verdict.

## Hard failure conditions
Mark the object `REVISE` for independent review if any are observed:
- UI reads as a generic dashboard before it reads as the project/world;
- world/landscape is visually subordinate without a safety reason;
- route/objective is unclear because decoration dominates;
- important interaction exists only as hidden/invisible hit areas;
- labels explain controls that should be self-evident through affordance;
- persistent glow, scan, breathing, floating, zoom, or particles exist without state meaning;
- Return/escape/safety is visually present but behaviorally blocked;
- the interface invents factual geography, status, measurement, or field certainty;
- game feeling depends on rewards/forced completion not authorized by Current Authority.

## Review output
Use this structure:

```text
OBJECT:
CURRENT AUTHORITY:
BEST EXISTING DESIGN SOURCE:
PRIMARY TASK:
PRIMARY VISUAL:
WORLD/HUD HIERARCHY:
ANTI-DASHBOARD FINDINGS:
GAME-FEELING FINDINGS:
WORLD/UI COHESION FINDINGS:
TRUTH-BOUNDARY FINDINGS:
RUNTIME EVIDENCE:
OPEN DEFECTS:
INDEPENDENT VERDICT REQUIRED: YES
```

No producer numeric quality score.

## Source lineage
Distilled and adapted for OLEANDER from external game-UI practice including `threejs-game-ui-designer` / `ui-patterns`, mobile game-UI ergonomics work, and OLEANDER's existing motion/first-visual governance. External sources are inspiration/evidence only and do not become project authority.