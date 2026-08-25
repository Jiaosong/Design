# Landscape GIS Analysis Drawing Binding

Status: **BINDING EXTENSION / NO NEW PARALLEL SKILL**

This binding extends `oleander-data-viz` for landscape-architecture site analysis, terrain analysis, hydrology, slope/aspect, environmental synthesis, and competition/portfolio analytical drawings. It inherits Spatial Authority Preservation, Cartographic Task Hierarchy, Visual Layer Binding, Small-Multiple Comparability, and OLEANDER Artifact Review. It does not replace GIS correctness with presentation styling.

## 1. Precision ceiling gate

**Graphic refinement must never be described as GIS precision refinement unless the source authority actually improves.**

Distinguish three layers explicitly:

1. **Source precision** — native DEM/raster/vector resolution, sampling density, positional accuracy, CRS/datum, NoData, temporal resolution, and provenance.
2. **Analytical precision** — derivations such as slope, aspect, curvature, flow direction, flow accumulation, catchment, solar exposure, or classification computed from the source.
3. **Graphic/readability precision** — contours, hillshade, line hierarchy, labels, sections, insets, masking, opacity, texture and board composition.

Rules:
- Resampling, smoothing, spline interpolation, contour generation, hillshade, blur, texture, glow or a higher-resolution export **does not increase source precision**.
- A display-interpolated surface may be used only when it improves continuous landform reading and is labelled `DERIVED DISPLAY / DOES NOT INCREASE SOURCE PRECISION`.
- If the desired spatial claim requires a finer source than the current authority can support, stop presentation refinement and route upstream to real source acquisition / materialization.
- Never let a fine-looking contour, drainage line or shaded-relief surface imply more spatial certainty than the underlying raster or sample grid supports.

Hard failure: `LOW-RES SOURCE → SMOOTH VISUAL → CLAIMED HIGH-PRECISION GIS`.

## 2. Landscape analytical drawing, not GIS dashboard

For portfolio, board, competition, landscape, architecture or spatial-design delivery, do not default to a software-export look, card dashboard or wall of raster cells.

The target is a **landscape analytical drawing**:

`SPATIAL BASE → ONE ANALYTICAL VARIABLE → SPATIAL FINDING → DESIGN CONSEQUENCE`

A strong figure should read as a designed spatial argument, not as a screenshot of GIS software and not as a UI dashboard placed around a map.

## 3. Continuous terrain first

When the question concerns terrain, valley, ridge, slope, drainage or spatial compression, continuous landform must become the first spatial carrier.

Preferred hierarchy:

`RELIEF / CONTOUR STRUCTURE → WATER / RIDGE / VALLEY → ANALYSIS OVERLAY → ANNOTATION → SUPPORTING STATISTICS`

- Contours are structural geometry, not decorative texture.
- Index contours and intermediate contours must have different line weights when scale permits.
- Hillshade is subordinate to contour/terrain structure; it must reveal landform rather than create atmospheric blur.
- Use multidirectional or otherwise carefully controlled relief where available; avoid muddy low-contrast hillshade that softens the entire figure.
- Water must read crisply against terrain and retain its geographic role.

Failure: first read is `blur / tint / cells / cards`, while ridge, valley and terrain shape remain vague.

## 4. Raw raster/grid exits MAIN when it dominates the drawing

Source cells, sample points and raw raster classes remain valid evidence, but they do not automatically deserve to be the dominant presentation grammar.

- Keep raw cell/sample display in QC, evidence inset, method panel or source-readback page when needed.
- In MAIN analytical drawings, translate valid raster evidence into the spatial grammar appropriate to the question: continuous terrain, threshold band, vector boundary, direction field, extracted hierarchy, contour, section, or small multiple.
- Do not hide the source granularity; disclose it in a compact precision note or evidence inset.
- Never vectorize or smooth a raster into false geometry merely to escape the cell look.

Rule: **SOURCE GRANULARITY STAYS VISIBLE TO AUDIT; IT DOES NOT HAVE TO OWN THE FIRST VISUAL READ.**

## 5. One analytical variable owns each panel

Avoid one-map-does-everything synthesis.

Use one dominant question per figure or panel:
- terrain morphology;
- slope;
- aspect;
- flow direction;
- flow accumulation;
- watershed/catchment;
- land cover;
- water history;
- solar/exposure;
- environmental synthesis.

For related variables, prefer locked-extent small multiples. Keep the same extent, north, scale, base geometry, contour interval and comparison domain wherever the comparison meaning requires it.

Do not let decorative variation become a second variable.

## 6. Hydrology must read as hierarchy, not colored noise

When source resolution and derivation support it, hydrology should communicate a flow hierarchy:

`SURFACE → FLOW DIRECTION → CONVERGENCE → ACCUMULATION HIERARCHY → CATCHMENT / SUBCATCHMENT`

- Differentiate minor/major accumulation with line width, value threshold, or ordered lightness.
- Convergence points may be explicit nodes.
- Catchment/subcatchment boundaries use a separate vector grammar.
- A sampled D8 accumulation grid must not be drawn as a synthetic channel network unless a defensible extraction step has been executed and documented.
- `D8 CONVERGENCE ≠ DRAINAGE NETWORK ≠ HYDRAULIC CAPACITY ≠ FLOOD PATH`.

## 7. Plan–section coupling gate

For terrain-heavy landscape analysis, plan alone is often insufficient.

When vertical relation materially affects the argument, add one or more real linked sections:
- across-valley;
- along-ridge / along-slope;
- river-to-slope;
- node-specific terrain section.

Requirements:
- section cut line is visible on the plan;
- section uses the same terrain/source authority;
- horizontal/vertical exaggeration is disclosed;
- section labels correspond to real plan positions;
- section is analytical evidence, not an unrelated illustrative profile.

A generic sparkline in a side panel does not substitute for a mapped terrain section when section evidence is needed.

## 8. Master figure + supporting evidence rhythm

Strong landscape-analysis boards often use one dominant spatial field and several subordinate evidence objects.

Recommended composition:
- **60–75%** dominant plan/terrain/master figure when one main spatial claim exists;
- compact small maps, typology diagrams, sections, source/QC insets or statistics as support;
- numbered callouts connect supporting objects back to the main spatial field;
- imagery/render insets are allowed only when they explain a mapped location, design consequence or experience and do not replace evidence.

Do not split the page into equal-weight cards when the spatial argument has a clear dominant object.

## 9. Detail comes from line, density, object specificity and annotation—not blur

Professional analytical richness is created by:
- contour hierarchy;
- crisp hydrography;
- vegetation/object fields when source-grounded;
- terrain sections;
- exact callout lines;
- direct labels;
- measured spacing;
- controlled symbol families;
- dense near-read annotation around a clear far-read structure.

Do not simulate richness with atmospheric blur, generic texture, excessive transparency, glow or oversized soft raster overlays.

`FIRST READ = LAND FORM / ANALYTICAL CLAIM`
`NEAR READ = EVIDENCE / VALUES / OBJECT DETAIL / METHOD`

Both must work.

## 10. Aesthetic tone is a secondary binding

Project visual identity may influence paper tone, accent hue, annotation style, line texture and presentation rhythm, but it may not blur or recolor away cartographic structure.

For restrained landscape visual systems such as ink / water / paper / mineral palettes:
- terrain primarily reads through relief, line, value and density;
- hue remains a secondary analytical channel;
- one accent color may identify threshold/decision/callout;
- texture stays behind geometry;
- glow is forbidden when it makes contour, labels or hydrography less crisp.

**STYLE BINDS TO CARTOGRAPHY; CARTOGRAPHY DOES NOT DISSOLVE INTO STYLE.**

## 11. Analysis-to-design bridge

A landscape analysis figure is incomplete when it ends at a beautiful pattern with no consequence.

Use an explicit chain:

`EVIDENCE → SPATIAL FINDING → DESIGN / FIELD CONSEQUENCE`

But keep evidence and decision visually distinct. A design consequence must not be painted back onto the source map in a way that makes it look observed.

For uncertain / missing layers, preserve explicit `HOLD / UNKNOWN / FIELD OPEN` slots instead of filling them with proxy graphics.

## 12. Review protocol

Before promotion, open the actual master and derivatives and run:

1. **Source precision readback** — can the viewer tell what is source, derived, interpolated display and field-open?
2. **Terrain first-read** — can ridge/valley/water/primary landform be read before paragraph text?
3. **Variable isolation** — is there one dominant analytical question per panel?
4. **Main-vs-support hierarchy** — does the dominant spatial figure clearly outrank supporting charts/insets?
5. **Plan–section consistency** — mapped cuts and sections agree when sections are used.
6. **Hydrology semantics** — no sampled convergence is misrepresented as surveyed drainage or hydraulic truth.
7. **Near-read technical density** — labels, legends, values and annotations are precise without becoming a card dashboard.
8. **50% / distance read** — first claim and spatial object survive reduction.
9. **Grayscale read** — hierarchy survives without hue.
10. **Style removal test** — if paper texture, tint, glow and decorative wash are removed, the analytical drawing must still work.

Hard failures:
- graphic smoothness is presented as improved GIS precision;
- raw grid dominates MAIN despite not being the analytical object;
- a map becomes a UI/card dashboard;
- all variables are overlaid at equal weight;
- contour/hydrology becomes vague because of texture/blur;
- section/profile does not correspond to plan geometry;
- design consequence is visually indistinguishable from observed/source evidence;
- a missing layer is replaced by decorative proxy content.

## 13. Reference-derived visual lesson boundary

The transferable lesson from landscape-analysis references is **composition and analytical grammar**, not copied project content or copied geometry.

Reusable observations:
- one dominant masterplan/terrain field can carry most of the page;
- compact mobility/green/function maps can operate as evidence entry points;
- circular or free-form visual insets work only when tied to numbered mapped locations;
- continuous topography + vegetation/object detail + sections + technical callouts can create professional richness without a dashboard frame;
- dense near-read information can coexist with generous white space when the main spatial field remains clear.

Do not copy source projects' plans, routes, labels, vegetation patterns, renders, or design decisions into a new project.
