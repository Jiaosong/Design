# Game UI Visual Layer Binding

Status: **BINDING ONLY / REUSE EXISTING UI + MOTION SOURCES**

`oleander-game-ui` already defines world-first hierarchy and anti-dashboard quality. Do not add a generic game-effect catalogue.

## Existing sources to inherit

1. `oleander-ui-visual-composition` for first-read, hierarchy, typography, imagery, depth and professional finish.
2. `oleander-ui-interaction` for state/focus/interruption/re-entry.
3. `oleander-motion/MOTION_LIBRARY_EFFECT_ATLAS.md` for temporal effect mechanisms.
4. `oleander-route-wayfinding-ui` when the game-like surface contains route/map/navigation.
5. Current `oleander-game-ui-stack/README.md` routing and Golden Cases.
6. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
7. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for image compositing, masks, transparency, texture and bounded vector/raster effects.
8. Current Notion `KN-METHOD-COLOR-SYSTEM-001｜Color System｜角色—语义—媒介—生产—验证` whenever identity color, interaction color or operational/status color appear in the same surface.

## Existing visual boundary

The world/object/task remains primary. Project-specific geometry, material, color, icon and motion language take precedence over generic neon, sci-fi glass, tactical HUD, fantasy ornament, persistent glow, particles or scan effects. Game feeling must come from authorized stateful behavior and feedback, not unauthorized gamification.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for layer-based scene/UI assembly, masking, clipping, opacity, blend modes, texture, grading, local depth cues and bounded stylization. The effect-off screen must still carry world/object/task hierarchy. Photoshop/Illustrator effects may intensify an already-authorized game-like language, but must not default the project into neon/HUD/scan/glass aesthetics, invent environmental facts, or replace interaction behavior with static visual theatrics.

## Brand ↔ operational-state color separation gate

When a screen contains both brand identity and operational state, **do not let one brand palette silently become the state model**. First map color by role, then test the state semantics without brand color and without state color.

Required lanes:
- **Identity lane** — brand recognition, passive context, editorial continuity. It may disappear or become quieter without changing whether an action is safe/available.
- **Interaction lane** — focus, selection, hover/press, committed object, progress. These cues describe user interaction, not real-world operational truth.
- **Operational state lane** — availability / degraded / closed / unknown / critical recovery. These cues may override brand presence when the state affects safety, access, Return or fail-closed behavior.

Required checks:
1. **No semantic borrowing:** a brand accent must not imply `NORMAL`, `OPEN`, `SAFE`, `SELECTED` or `CURRENT` merely because the same hue is already prominent in the product.
2. **Redundant state coding:** critical states use at least one non-color channel such as label, icon/shape, boundary style, position or behavior. Color alone is never the only discriminator.
3. **UNKNOWN stays visually unresolved:** do not style UNKNOWN as a low-emphasis NORMAL state. It should remain explicitly unconfirmed and may route to Return / Service / fail-closed behavior.
4. **CLOSED can outrank identity:** when closure or recovery is the task, operational state may suppress brand chroma, decorative glow and optional game effects.
5. **Interaction ≠ operation:** selected/focused route nodes and operational availability must remain distinguishable when they coexist.
6. **Color-off test:** remove all chroma; NORMAL / DEGRADED / CLOSED / UNKNOWN must still be distinguishable at task size.
7. **Brand-off test:** neutralize the identity palette; operational meaning and Return priority must remain intact.
8. **State-off test:** neutralize semantic-state colors but keep icons/labels/geometry; the screen must not accidentally read every route as available because brand color remains.
9. **Medium boundary:** screen tokens do not prove print, signage, environmental, material or accessibility performance. Route to the Current Color System METHOD and target-medium proof when those claims matter.

Hard failures:
- `brand color everywhere = consistency` when that color is also used to encode operational state;
- CLOSED and UNKNOWN differ only by small text or hue;
- selection/focus styling can be mistaken for OPEN/NORMAL state;
- UNKNOWN inherits the same filled treatment as a confirmed available state;
- a fail-closed screen becomes visually optimistic after brand effects are added;
- grayscale removes the distinction between critical operational states;
- CI/contrast-tool success is treated as proof that semantic color architecture is correct.

Promotion test:
> **Remove brand color, then remove status color: identity may weaken, but CLOSED / UNKNOWN meaning and Return priority must still survive.**

Recommended review record:
```text
IDENTITY COLOR ROLE:
INTERACTION COLOR ROLE:
OPERATIONAL STATE TOKENS:
NON-COLOR REDUNDANCY:
NORMAL / DEGRADED / CLOSED / UNKNOWN DISTINCTION:
BRAND-OFF READBACK:
COLOR-OFF / GRAYSCALE READBACK:
STATE-OFF READBACK:
RETURN / FAIL-CLOSED PRIORITY:
MEDIUM / ACCESSIBILITY PROOF STATUS:
```

## Review inheritance

Use the existing stack order and independent review. A visually immersive screen may not imply stronger factual certainty, GPS status, field verification or product logic than Current Authority supports.
