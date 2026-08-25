# Data Visualization Visual Layer Binding

Status: **BINDING ONLY / NO NEW METHODOLOGY**

`oleander-data-viz` already contains spatial-authority and route-state visual rules. Do not add a parallel generic effect system.

## Existing sources to inherit

1. Notion `T-DATAVIZ-OLEANDER-001｜OLEANDER Chart Spec v0.2｜数据—证据—视觉想法—SVG—交互契约`.
2. Notion `FW-DESIGN-VISUAL-COMM-001｜视觉传达与平面设计｜信息—层级—媒介—验证`.
3. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
4. `oleander-motion/MOTION_LIBRARY_EFFECT_ATLAS.md` only when temporal change carries analytical meaning.
5. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for vector-safe and raster-preview composition operators.

## Existing visual rules to apply

Use Chart Spec v0.2 D2 before rendering: one-sentence finding, first-read object / dominant field, visual idea, first-read label budget, negative space / hierarchy, abstraction budget, remove-decoration test and series rhythm.

The first visual must be carried by a data relationship, proportion, path, area, spatial relation or typographic relationship rather than decorative gradients, cards, outlines or multi-state color.

For animated data, reuse the Motion Effect Atlas mechanisms such as structured sequence and data reorder/filter/time interpolation; animation must not smooth away missing or uncertain data.

## Small-multiple comparability gate

Apply whenever two or more panels are intended to support direct comparison of the same question, quantity or state family.

1. **Same question + same unit requires a locked comparison domain by default.** Shared axes, baselines, color domains, bin boundaries, mark geometry and legend semantics must remain invariant across panels unless a different domain is analytically necessary and explicitly disclosed.
2. Local auto-normalization is a blocker when it makes materially different values appear visually equivalent. Do not let each panel independently stretch its own minimum/maximum merely to fill the frame.
3. If a panel must use a different scale, label the scale directly inside that panel and remove any visual cue that implies one-to-one magnitude comparison.
4. Preserve identical panel dimensions, plot-area dimensions, mark width/area rules, unit placement and reading order when these encode comparison. Decorative variation must not become a second comparison channel.
5. Prefer direct labels for the primary comparison values when label density permits. Legends may explain encoding but must not be required to discover the central difference.
6. Missing / HOLD / UNKNOWN panels must keep their slot in the comparison grammar when omission would falsely imply completeness. Use an explicit unavailable state instead of substituting proxy values or compressing the panel set.
7. Inspect the figure at target size and at approximately 50% scale. The intended ordering or difference should remain legible without reading paragraph text.
8. Before promotion, perform a **comparability readback**: verify that a viewer can correctly rank or distinguish the panels using the visual marks alone, then confirm the visual ranking matches the source values.

Hard failures:
- same-unit panels use undisclosed independent y-domains or color domains;
- area/length encodings change geometry between panels without semantic reason;
- a HOLD/UNKNOWN panel is silently removed and the remaining set reads as complete;
- visual ranking contradicts source ranking;
- styling differences overpower the analytical difference.

Promotion test: **If the comparison only becomes truthful after reading the numbers, the small-multiple visual encoding has failed.**

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for layer isolation, clipping/masking, opacity, raster underlays, tonal normalization, texture/noise control and export adapters around a chart/map. Preserve authoritative values, topology and vector masters. Blur, glow, texture, pixelation, blend modes or masks may clarify hierarchy but may not change a value, conceal uncertainty, normalize `UNKNOWN`, or replace a source-grounded geometry relationship.

## Review inheritance

Open the actual SVG/PNG/PDF/interactive output. Run compact-size, grayscale/non-color, label-collision and source-value checks. For small multiples, additionally run the locked-domain comparability readback above. Renderer/library capability does not substitute for Professional Design Gate.
