# 2026-08-19｜Mobile UI / Typography / L5｜Semantic Occlusion Priority

Status: **TRAINING EXECUTED / PRODUCER KEEP-FOR-TRAINING CANDIDATE / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION**

## Project trigger

C04 runtime/responsive review already established that raw Label/UITransform AABB diagnostics are non-gating because layout boxes can exceed real glyph bounds; screenshot review remains authoritative for text occlusion. Recent training tightened responsive density, bilingual role pairing, world/screen depth ownership and responsive media art direction, but none defined which semantic objects are allowed to yield when real mobile collisions occur.

The current C04 ROUTE family contains a predictable collision stack: Return/safety/truth-state controls; active route anchor and explanation; secondary nodes; optional explanation; provenance/status text. A geometry-only “avoid overlap” rule is insufficient because collision resolution can preserve empty rectangles while still obscuring glyphs, focal anchors, Return, or evidence-bearing landscape.

## Existing Skill reused

Existing family: `oleander-ui-visual-composition` v0.1.2 on PR #278.

Gap before this round:
- professional-finish checks detected overlap but did not define semantic occlusion rights;
- Typographic Density Recomposition did not define collision degradation;
- Bilingual Role Pairing did not define which labels collapse first under crowding;
- no protected Return/safety/truth zone;
- no rule prevented a collision solver from moving a label to the wrong spatial anchor.

## Actual exercise

Editable 1920×1080 SVG compares two synthetic 390×844 mobile ROUTE compositions.

### REJECT
Every node/status/explanation appears as a full label. Collision handling is purely positional. R06/R13/status cards compete with route and focal scene; optional explanation invades the Return zone; box diagnostics could still report acceptable geometry while rendered glyph/card occlusion is severe.

### KEEP candidate
Semantic priority ladder:

`P0 RETURN / SAFETY / TRUTH → P1 ACTIVE ANCHOR → P2 SHORT SECONDARY LABEL → P3 ANCHOR-ONLY → P4 HIDE`

- P0 owns protected screen zones and cannot be displaced by optional content;
- only the active anchor receives a full local label by default;
- secondary nodes can shorten to ID-only;
- tertiary nodes can fall back to anchor-only;
- hidden labels remain recoverable through later focus/reveal rather than moving to a false anchor;
- truth state remains compact but visible.

## Design Crit

### Compliance / execution
**PASS FOR TRAINING EXECUTION**
- editable SVG;
- vector text;
- PNG and 50% grayscale derivatives rendered;
- final full-size PNG reopened for pixel review;
- no image generation;
- no GPS, field location, accessibility or runtime-engine claim.

### Producer frozen-rubric
**KEEP-FOR-TRAINING CANDIDATE**
- First visual: PASS — scene/route first, then one active label; Return survives.
- Composition: PASS — safe zones constrain UI without boxing the scene.
- Proportion: PASS — active label > secondary ID > anchor-only.
- Hierarchy: PASS — P0 truth/Return protected without becoming visual hero.
- Typography: PASS at training target scale.
- Material/spatial realism: schematic landscape only.
- Scale: 390×844 logic explicit; device/accessibility certification OPEN.
- Node readability: PASS — R06 full label, R13 short label, tertiary anchor distinguishable.
- Interaction/narrative: static priority/degradation model coherent; runtime collision engine OPEN.
- Professional finish: training-level candidate; no visible collision in KEEP current.

### Independent Professional Design Gate
**HOLD / REVIEW REQUIRED.** No independently attributable professional reviewer is available in this run. Producer readback is not promoted to independent KEEP.

## Failure knowledge

1. `AABB no-overlap ≠ rendered no-occlusion`.
2. Collision resolution without semantic priority can preserve geometry while destroying task hierarchy.
3. Moving a label to any empty region can create false spatial ownership.
4. Optional explanation must never consume Return/safety/truth zones.
5. “Shrink every label” repeats the scaled-down desktop failure.
6. Hiding every secondary label destroys route context; degradation needs intermediate states.
7. Full labels for every node turn the scene into a dashboard even when each label is individually legible.

## Repair method

`SEMANTIC PRIORITY → PROTECTED ZONES → FULL LABEL → SHORT LABEL → ANCHOR-ONLY → HIDE → FOCUS/REVEAL RECOVERY`

Required tests: `WORST-COLLISION / RETURN-SAFE / TRUTH-SAFE / GLYPH-READBACK / ANCHOR-INTEGRITY / DEGRADATION / FOCUS-RECOVERY`.

Promotion test:

> At native target size, force the worst collision: P0 controls and truth must survive; lower-priority labels may degrade, but must not migrate to a misleading anchor.

## Skill delta

Existing `oleander-ui-visual-composition` is extended with `references/SEMANTIC_OCCLUSION_PRIORITY.md`. The extension defines P0–P4 semantic occlusion classes, protected Return/safety/truth zones, a full→short→anchor-only→hide ladder, real-glyph screenshot readback instead of AABB-only acceptance, anchor-integrity/focus-recovery tests, and hard failures for false-anchor migration and optional-content takeover. This is not a new parallel Skill.

## Cross-project transfer

Applicable to C04 ROUTE/R06/R13 mobile overlays, maps and scene-anchored travel/museum companions, dense mobile dashboards with spatial annotations, product configurators/3D viewers with object labels, and technical/diagram viewers where labels must retain object ownership.

Not directly sufficient for regulated safety UIs governed by higher authority, AR/GPS labels without validated tracking, desktop analytical maps where simultaneous label visibility is itself the task, screen-reader/accessibility semantics, or non-spatial long-form reading surfaces.

## Truth boundary

`TRAINING ONLY / SYNTHETIC 390×844 LOGIC / NTS / NOT GPS / FIELD OPEN / NO IMAGE GENERATION / INDEPENDENT DESIGN REVIEW HOLD / NO_PROMOTION`.
