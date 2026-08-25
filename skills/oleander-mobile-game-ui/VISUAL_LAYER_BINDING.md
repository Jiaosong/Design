# Mobile Game UI Visual Layer Binding

Status: **BINDING ONLY / MOBILE RECOMPOSITION, NOT A NEW STYLE**

This Skill is an ergonomics and mobile-resilience gate. It does not own an independent visual-effect style.

## Existing sources to inherit

1. `oleander-ui-visual-composition` for visual hierarchy and finish.
2. Existing browser-tested practice `06-practice/2026/2026-08-18-responsive-recomposition/`.
3. `oleander-motion` / `MOTION_LIBRARY_EFFECT_ATLAS.md` for Reduced Motion and temporal mechanisms.
4. `oleander-ui-interaction` for touch/focus/state parity.
5. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
6. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for mobile image preparation and bounded effects.

## Existing responsive visual rule

Do not merely stack or shrink a desktop composition. Preserve information, but allow breakpoint-specific order, span, emphasis and density to change when task priority requires it. A technically responsive layout can still be a visual REVISE if the first task is delayed or support content becomes co-primary.

Effects that cost target size, safe-area clarity, touch discoverability, native control or Reduced Motion equivalence must be reduced or removed.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for mobile-specific crops, layered image derivatives, masks, transparency, texture and bounded raster/vector effects while retaining the recoverable source. Re-evaluate blur radius, texture scale, glow spread, contrast and detail density at actual narrow viewports; an effect that works on desktop may collapse legibility or increase visual noise on mobile. Image-processing effects may not delay the primary task, obscure safe-area controls or replace Reduced Motion/state parity.

## Review inheritance

Run real narrow-viewport readback. Mobile runtime success proves operation only; independent visual review remains separate.
