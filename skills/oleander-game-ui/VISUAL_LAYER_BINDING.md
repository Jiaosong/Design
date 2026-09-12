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

## Existing visual boundary

The world/object/task remains primary. Project-specific geometry, material, color, icon and motion language take precedence over generic neon, sci-fi glass, tactical HUD, fantasy ornament, persistent glow, particles or scan effects. Game feeling must come from authorized stateful behavior and feedback, not unauthorized gamification.

## Cross-screen family grammar gate

Apply when multiple peer screens belong to one product family but serve materially different primary tasks, for example TODAY / ROUTE / MY BOOK / SERVICE.

Consistency must come from **shared visual roles and bounded invariants**, not from forcing every screen into the same card shell.

Lock or bound across peer screens:
- safe-area and edge rhythm;
- typography role mapping and baseline behavior;
- stroke, radius, spacing and quiet-metadata vocabulary;
- active-anchor treatment;
- Return / recovery placement and priority;
- primary-object-to-chrome proportion;
- HUD density ceiling;
- state/status semantics.

Allow to vary by task:
- primary object silhouette and composition;
- local information density;
- content geometry;
- mode-specific controls;
- optional explanation layer;
- state-specific emphasis required by the task.

Required readback:
1. **Title-off test** — obscure screen titles; each mode should remain identifiable from its primary object and composition.
2. **Color-off test** — inspect grayscale/non-color output; family cohesion must not depend on accent color alone.
3. **Compact test** — inspect at approximately 50% scale; shared roles should remain coherent while task identity remains distinct.
4. **Template-lock test** — if peer screens become indistinguishable when labels change, consistency is being produced by duplicated templates rather than product grammar.
5. **Family-drift test** — if task-specific variation also changes typography roles, recovery placement, spacing logic, anchor semantics or HUD density without reason, the family has fragmented.

Hard failures:
- identical central card shells are reused across unrelated tasks and labels carry most mode identity;
- color or logo is the primary evidence that screens belong to one product;
- one screen becomes panel/dashboard-first while peer screens remain world/object-first without a task or safety reason;
- navigation chrome becomes more stable and visually dominant than the screen-specific primary object;
- mode identity disappears when titles are removed;
- a task-specific composition breaks Return/safety semantics or established interaction authority merely to look different.

Promotion test: **If screen titles and accent color are removed, peer screens should still feel like one product while each screen remains identifiable by its task-specific primary object.**

This gate complements the existing Exploration Motion Grammar. Motion grammar controls reusable behavioral semantics across states; family grammar controls reusable visual roles across peer screens. Neither requires identical layouts.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for layer-based scene/UI assembly, masking, clipping, opacity, blend modes, texture, grading, local depth cues and bounded stylization. The effect-off screen must still carry world/object/task hierarchy. Photoshop/Illustrator effects may intensify an already-authorized game-like language, but must not default the project into neon/HUD/scan/glass aesthetics, invent environmental facts, or replace interaction behavior with static visual theatrics.

## Review inheritance

Use the existing stack order and independent review. A visually immersive screen may not imply stronger factual certainty, GPS status, field verification or product logic than Current Authority supports. For multi-screen products, additionally run the title-off, color-off, compact, template-lock and family-drift tests before any family-consistency claim.
