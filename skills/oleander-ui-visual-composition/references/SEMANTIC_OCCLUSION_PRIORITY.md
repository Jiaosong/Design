# Semantic Occlusion Priority Gate

Use this reference whenever mobile/scene UI contains multiple labels, route nodes, status chips, explanations, or controls that can collide at target size.

## Why this gate exists

`AABB no-overlap ≠ rendered no-occlusion.` Layout rectangles are implementation evidence, not final visual proof. Real glyphs, card fills, focal anchors, route geometry and protected controls can still occlude one another while box diagnostics report success.

This gate extends `oleander-ui-visual-composition`; it is not a separate Skill.

## 1. Assign semantic occlusion class before placement

- `P0 — RETURN / SAFETY / TRUTH`: Return, emergency/safety actions, CLOSED/UNKNOWN truth-state, or other information that changes whether/how the user should proceed. P0 owns protected screen zones and may not be displaced by optional content.
- `P1 — ACTIVE ANCHOR`: the currently focused world/object/node label. Usually the only full local label shown by default in a dense scene.
- `P2 — SECONDARY CONTEXT`: nearby route/object labels that preserve orientation. May shorten to an ID or one-line name.
- `P3 — TERTIARY ANCHOR`: spatial context that can remain as an anchor/icon without text.
- `P4 — OPTIONAL / DEFERRED`: explanatory or low-priority labels that may hide until focus/reveal.

Priority describes occlusion rights, not visual size. P0 can remain visually quiet while still owning a protected zone.

## 2. Protected zones

Define protected zones before collision solving:
- Return/safety action zone;
- truth/state zone when UNKNOWN/CLOSED/safety changes interpretation;
- safe-area/system-chrome zone;
- evidence-bearing focal region when a label/card would hide the object/relation the screen asks the user to inspect.

Optional explanation, decorative UI, P2/P3 labels and generated tooltips may not take these zones.

## 3. Degradation ladder

When crowding increases, degrade lower-priority labels in this order:

`FULL LABEL → SHORT LABEL → ANCHOR-ONLY → HIDE → FOCUS/REVEAL RECOVERY`

Do not solve crowding by globally shrinking every label.

A hidden/degraded label must recover when its object becomes active if the product still needs that information.

## 4. Anchor integrity

Collision resolution may change leader length or label side only within a bounded relationship that remains unmistakable.

Hard failure:
- moving a label to an unrelated empty region so that it appears to belong to a different node/object;
- leader crossing that changes ownership;
- label remaining visible after its anchor is offscreen/occluded in a way that implies false spatial registration.

## 5. Required tests

1. `WORST-COLLISION` — force maximum realistic label density at native target width.
2. `RETURN-SAFE` — P0 Return cannot be occluded/displaced by optional content.
3. `TRUTH-SAFE` — UNKNOWN/CLOSED/safety cannot disappear behind lower-priority UI.
4. `GLYPH-READBACK` — judge rendered pixels/screenshots, not AABB metrics alone.
5. `ANCHOR-INTEGRITY` — collision handling does not migrate ownership to a false anchor.
6. `DEGRADATION` — P2/P3 step through short/anchor-only before hide when route context requires.
7. `FOCUS-RECOVERY` — hidden/degraded content returns when the object becomes active.
8. `LANDSCAPE/EVIDENCE-SAFE` — labels/cards do not cover the visual evidence the prompt asks the user to inspect.

## 6. Hard failures

- every node is forced to remain a full label in a dense scene;
- Return/safety/truth is visually or physically displaced by optional explanation;
- all labels are uniformly shrunk to preserve simultaneous visibility;
- collision solver moves a label to a misleading anchor;
- AABB checks are used as the final no-occlusion proof without target-size screenshot review;
- hiding all secondary context makes route/world orientation fail;
- card fills hide the evidence-bearing scene while their text remains legible;
- label visibility implies GPS/AR registration that the project has not validated.

## 7. Review record

Record:

```text
SURFACE_ID:
TARGET_VIEWPORT:
P0_PROTECTED_ZONES:
ACTIVE_ANCHOR:
P2_SECONDARY_LABELS:
P3_ANCHORS:
P4_OPTIONAL_CONTENT:
WORST_COLLISION_READBACK:
RETURN_SAFE_RESULT:
TRUTH_SAFE_RESULT:
ANCHOR_INTEGRITY_RESULT:
GLYPH_SCREENSHOT_RESULT:
FOCUS_RECOVERY_RESULT:
DOES_NOT_PROVE:
```

## Promotion test

`At native target size, force the worst collision: P0 controls and truth must survive; lower-priority labels may degrade, but must not migrate to a misleading anchor.`

## Boundary

This gate does not prove accessibility compliance, AR/GPS tracking, field status, or regulated safety-interface conformance. Those require their own higher-authority validation.
