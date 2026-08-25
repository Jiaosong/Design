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

## Evidence-state surface grammar gate

Apply whenever one analytical set mixes different epistemic / evidence states such as `SOURCE-BOUND`, `VERIFIED INPUT`, `DERIVED`, `REPORTED`, `INFERRED`, `HOLD`, `PENDING`, or `UNKNOWN`.

1. **Magnitude / topology and evidence maturity are separate semantic variables. Encode them through separate visual channels.** A value, route, area, direction or proportion must not change merely because its source is weaker or stronger.
2. Do not encode evidence maturity by shrinking bars, shortening lines, changing map geometry, lowering numeric values, or otherwise mutating the analytical mark. Uncertainty styling may surround or annotate a mark; it may not rewrite the mark's quantitative or spatial meaning.
3. Bind evidence state to an orthogonal carrier such as a provenance rail, panel boundary, slot treatment, endpoint glyph, stroke pattern, header token, or explicit status field. Critical states must survive grayscale / low-color review.
4. `HOLD / PENDING / UNKNOWN` may not receive a fabricated analytical mark merely to make a board look complete. Preserve the slot and show an explicit unavailable / unmaterialized state when omission would imply completeness.
5. Visual polish must not equalize maturity. A source-bound figure, a reported overlay and a HOLD slot may share family typography and layout, but they must not share a surface treatment that makes them first-read equivalents.
6. Conversely, evidence-state styling must not overpower the analytical claim. If the primary question is magnitude, route, shape or relationship, that analytical object remains the first-read carrier; provenance is a secondary but unmistakable layer.
7. `REPORTED / INFERRED` must remain distinguishable from `OBSERVED / VERIFIED`. A polished line or map overlay does not upgrade provenance.
8. Before promotion, run a **label-off evidence readback**: temporarily hide evidence-state words and confirm maturity remains distinguishable from non-text cues. Then run a **state-off analytical readback**: temporarily remove provenance styling and confirm the underlying magnitude/topology remains unchanged.
9. Record the state source and version where relevant. At minimum capture `FIGURE_ID / ANALYTICAL_OBJECT / EVIDENCE_STATE / STATE_SOURCE / STATE_VERSION_OR_DATE / VISUAL_CARRIER / DOES_NOT_PROVE`.

Hard failures:
- lower-confidence data is visually shortened, dimmed or geometrically altered in a way that can be read as a lower value;
- HOLD/UNKNOWN receives proxy values or an invented map/chart mark for visual completeness;
- evidence state exists only in paragraph text or a remote legend and disappears at first read;
- source-bound, derived, reported and HOLD states are visually identical after labels are removed;
- evidence-state styling changes locked route topology, axis values, data ranking or spatial authority;
- styling is so dominant that the viewer reads provenance before the actual analytical relationship when provenance is not the primary question.

Promotion test: **Hide the labels: evidence maturity must remain distinguishable, while numerical magnitude / topology must remain unchanged by the evidence-state styling.**

## Image-processing operator routing

Use `T-VISUAL-IMAGE-OPS-001` for layer isolation, clipping/masking, opacity, raster underlays, tonal normalization, texture/noise control and export adapters around a chart/map. Preserve authoritative values, topology and vector masters. Blur, glow, texture, pixelation, blend modes or masks may clarify hierarchy but may not change a value, conceal uncertainty, normalize `UNKNOWN`, or replace a source-grounded geometry relationship.

## Review inheritance

Open the actual SVG/PNG/PDF/interactive output. Run compact-size, grayscale/non-color, label-collision and source-value checks. For small multiples, additionally run the locked-domain comparability readback above. For mixed evidence-state sets, additionally run label-off evidence-state readback and state-off analytical readback. Renderer/library capability does not substitute for Professional Design Gate.
