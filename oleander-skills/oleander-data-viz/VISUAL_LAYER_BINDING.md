# Data Visualization Visual Layer Binding

Status: **BINDING ONLY / NO NEW METHODOLOGY**

`oleander-data-viz` already contains spatial-authority and route-state visual rules. Do not add a parallel generic effect system.

## Existing sources to inherit

1. Notion `T-DATAVIZ-OLEANDER-001｜OLEANDER Chart Spec v0.2｜数据—证据—视觉想法—SVG—交互契约`.
2. Notion `FW-DESIGN-VISUAL-COMM-001｜视觉传达与平面设计｜信息—层级—媒介—验证`.
3. Notion `OLEANDER Artifact Review System v1.1｜合规门 × 专业设计门`.
4. `oleander-motion/MOTION_LIBRARY_EFFECT_ATLAS.md` only when temporal change carries analytical meaning.
5. Current Notion `T-VISUAL-IMAGE-OPS-001｜OLEANDER Image Processing Operator Standard｜图层—蒙版—透明度—混合—滤镜—非破坏编辑` for vector-safe and raster-preview composition operators.
6. `LANDSCAPE_GIS_ANALYSIS_BINDING.md` whenever the task is landscape/site/terrain/hydrology/slope/aspect/environmental analysis or a competition/portfolio analytical drawing.

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

## Landscape GIS analytical-drawing routing

When a map is intended as landscape-architecture/site-analysis output rather than operational GIS software output, resolve `LANDSCAPE_GIS_ANALYSIS_BINDING.md` before visual styling.

Key bindings:

- **Precision ceiling first:** source precision, analytical precision and graphic/readability precision are different. Interpolation, contours, hillshade, smoothing or larger export size never upgrade source authority.
- **Continuous landform first:** for terrain questions, relief/contour/ridge/valley/water must read before UI-like cards, statistics or decorative atmosphere.
- **Raw grid is evidence, not automatically MAIN grammar:** preserve source granularity for audit, but move dominating sample/raster cells to QC/method insets when the analytical question is better expressed through continuous terrain, threshold bands, flow hierarchy, sections or small multiples.
- **One variable owns each panel:** terrain, slope, aspect, hydrology, solar and synthesis should not compete at equal weight in one map.
- **Plan–section coupling:** when vertical relation matters, mapped cut lines and sections must share the same spatial authority; a decorative sparkline does not substitute for terrain section evidence.
- **Hydrology semantics:** sampled D8 convergence must not be drawn as surveyed drainage, flood path or hydraulic capacity.
- **Master field + support rhythm:** one dominant spatial figure may occupy most of the board; supporting maps, sections, statistics and numbered insets remain subordinate and tied back to the master field.
- **Professional richness comes from line/density/object specificity/annotation:** blur, glow, texture and transparency may support atmosphere only if the cartographic structure remains crisp.
- **Style is secondary:** project palette and material tone bind to cartography; cartography must not dissolve into style.

Review at far-read, near-read, grayscale and with decorative style effects mentally/physically removed. If the analytical drawing only works because of tint, texture, blur or glow, return `REVISE`.

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for layer isolation, clipping/masking, opacity, raster underlays, tonal normalization, texture/noise control and export adapters around a chart/map. Preserve authoritative values, topology and vector masters. Blur, glow, texture, pixelation, blend modes or masks may clarify hierarchy but may not change a value, conceal uncertainty, normalize `UNKNOWN`, or replace a source-grounded geometry relationship.

## Review inheritance

Open the actual SVG/PNG/PDF/interactive output. Run compact-size, grayscale/non-color, label-collision and source-value checks. For small multiples, additionally run the locked-domain comparability readback above. For landscape/site GIS analytical drawings, additionally run the precision-ceiling, terrain-first, plan–section, hydrology-semantics, master-vs-support and style-removal checks defined in `LANDSCAPE_GIS_ANALYSIS_BINDING.md`. Renderer/library capability does not substitute for Professional Design Gate.
