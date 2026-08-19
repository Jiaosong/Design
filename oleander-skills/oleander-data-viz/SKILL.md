---
name: oleander-data-viz
description: Produce accurate static, animated, interactive, spatial, and presentation-ready visualizations for Oleander. Use whenever the user mentions Oleander tables, XLSX/CSV analysis, animated charts, timelines, maps, diagrams, dashboards, research visualization, SVG/PNG/HTML/MP4 chart exports, or converting project data into visual evidence.
compatibility: Uses Python 3.13 environment C:\Users\Xianmu\.venvs\oleander and may use spreadsheets, QGIS 4, FFmpeg, ImageMagick, Plotly, GeoPandas, or Sites.
---

# Oleander Data Visualization

Transform project data into reproducible visual evidence. Preserve the source data and make every transformation auditable.

## Environment

Use `C:\Users\Xianmu\.venvs\oleander\Scripts\python.exe`.

Core libraries include pandas, Polars, OpenPyXL, XlsxWriter, Matplotlib, Seaborn, Plotly, Kaleido, Altair, NetworkX, OpenCV, GeoPandas, Shapely, PyProj, Rasterio, Contextily, and OSMnx.

Use QGIS 4 for interactive GIS editing and Python/GeoPandas for reproducible spatial transformations. Do not bind scripts to QGIS 3 paths.

## Workflow

1. Inspect source files, units, missing values, time ranges, coordinate systems, and category definitions.
2. Keep raw data unchanged; write cleaned data separately with a transformation log.
3. Choose the visual form from the analytical question, not decoration.
4. Create a visual specification: audience, claim, dimensions, units, palette, typeface, output size, and accessibility.
5. Build the visualization reproducibly.
6. Export:
   - SVG for Illustrator and boards;
   - PNG at explicit pixel dimensions for review;
   - HTML for interaction;
   - MP4/WebM/GIF only when motion adds meaning;
   - XLSX with source/clean/data-dictionary sheets when a table is part of delivery.
7. Validate totals, axes, labels, legends, frame order, map CRS, and export dimensions.

For landscape/site/terrain/hydrology/slope/aspect/environmental-analysis drawings, also resolve `LANDSCAPE_GIS_ANALYSIS_BINDING.md` before rendering or styling. It is a binding extension of this Skill, not a separate method or parallel Skill.

## Spatial authority preservation

Apply this gate to maps, routes, plans, sections, diagrams, spatial networks, site geometry, model projections, product geometry, technical nodes, and any other graphic where shape or relative position carries project meaning.

1. Resolve the current geometry / topology authority before layout. Distinguish **source geometry authority** from the **presentation layer**.
2. If a route, plan, section, map, model view, node geometry, or other spatial object is approved, locked, current, or is the strongest mature existing artifact, reuse that geometry directly. Do not redraw it from memory or from a downstream derivative.
3. **Layout must adapt to authoritative geometry; authoritative geometry must not be distorted to fit layout.** Non-uniform scaling, stretching, compressing, smoothing, straightening, resampling, route re-authoring, invented continuation, or aesthetic simplification is forbidden when it changes spatial reading.
4. When comparing modes, phases, scenarios, audiences, or journey variants, derive each view by **subset / mask / crop / highlight / direction overlay** on the same authoritative geometry. Do not replace the geometry with four newly normalized shapes merely for visual consistency.
5. Existing Mature Design First applies: if an older/current artifact expresses the authoritative geometry more clearly than a newer candidate, preserve the stronger geometry and edit only the weaker presentation layer. Newer file ≠ better authority.
6. Context photographs, renders, AI images, diagrams, UI screens, or board compositions may support spatial reading but never become geometry authority unless the current project authority explicitly promotes them.
7. A presentation-only transform is allowed only when the analytical object itself is explicitly schematic and no real spatial inference will be drawn from it. Mark it `PRESENTATION ONLY / NOT SPATIAL EVIDENCE`. Do not use such a transform in a main spatial-evidence figure.
8. Before promotion, compare the candidate against the strongest existing geometry at matched scale or through path/overlay inspection. Any material loss of topology, route shape, relative position, section profile, scale relationship, or spatial recognizability is a blocker regression.

For source-bound spatial graphics, record:
- geometry/topology source object and version;
- what was preserved unchanged;
- any subset/mask/crop operation;
- any transform and whether it is uniform;
- what the graphic supports and what it does not prove.

## Landscape GIS analysis drawing gate

Apply this gate when GIS or spatial analysis must become a landscape-architecture / architecture / competition / portfolio analytical drawing rather than a raw GIS export or dashboard.

1. **Separate precision types before design.** Record `SOURCE PRECISION / ANALYTICAL PRECISION / GRAPHIC-READABILITY PRECISION`. Resampling, smoothing, contour generation, hillshade, blur, texture, glow, upscaling or higher export resolution never upgrades source precision.
2. **Route upstream when precision is insufficient.** If the spatial claim needs more detail than the current DEM/raster/vector/sample authority can support, stop graphic polishing and acquire/materialize a finer real source. Do not manufacture certainty with interpolation.
3. **Continuous terrain owns terrain questions.** For terrain, valley, ridge, slope or drainage analysis, first-read structure should normally be relief/contours/ridge-valley/water, followed by the analytical overlay. Contours are structural geometry, not decorative texture; hillshade must reveal form rather than soften it.
4. **Raw grid is evidence, not automatically MAIN grammar.** Preserve cells/sample points for audit, source inset or QC, but do not let a coarse grid dominate the main drawing when the analytical question is better represented by terrain, thresholds, flow hierarchy, sections or locked small multiples. Never smooth the grid into false geometry.
5. **One analytical variable owns each panel.** Prefer terrain / slope / aspect / flow direction / accumulation / catchment / land cover / water history / solar / synthesis as distinct panels or figures. For comparisons, lock extent, scale, north, base geometry and relevant visual domain.
6. **Hydrology reads as hierarchy.** Where the derivation supports it, communicate surface → direction → convergence → accumulation hierarchy → catchment/subcatchment. Sampled D8 convergence must not be presented as surveyed drainage, hydraulic capacity or flood path.
7. **Couple plan and section when vertical relation matters.** Show the section cut on plan, use the same source authority, disclose exaggeration, and maintain position correspondence. A generic side-panel sparkline does not substitute for a mapped terrain section.
8. **Use master-field + support rhythm.** One dominant terrain/masterplan/spatial field may occupy roughly 60–75% when the argument has a clear primary object. Supporting maps, sections, statistics, typologies and numbered image/render insets remain subordinate and spatially linked to the main field.
9. **Professional richness comes from line, density, object specificity and annotation.** Use contour hierarchy, crisp hydrography, source-grounded vegetation/object fields, exact callouts, sections, direct labels and near-read technical annotation. Do not simulate richness with blur, generic texture, glow, washed transparency or a wall of equal cards.
10. **Project style is secondary to cartography.** Palette, paper tone, ink/water language, material texture and accent color may bind the figure to a project identity, but must never blur contour, hydrography, labels, route/state meaning or evidence boundaries. `STYLE BINDS TO CARTOGRAPHY; CARTOGRAPHY DOES NOT DISSOLVE INTO STYLE.`
11. **Bridge analysis to consequence without collapsing truth states.** Use `EVIDENCE → SPATIAL FINDING → DESIGN / FIELD CONSEQUENCE`; keep source/derived evidence visually distinct from decisions. Preserve `HOLD / UNKNOWN / FIELD OPEN` slots rather than filling missing layers with decorative proxies.
12. **Review both distance and detail.** At far-read the viewer should see landform + one analytical claim; at near-read the viewer should inspect values, methods, annotations and source limits. Run grayscale, 50%/target-size, plan–section consistency, hydrology-semantics, source-precision and style-removal checks before promotion.

Hard failures:
- smooth/high-resolution-looking output is called higher-precision GIS while the source authority did not improve;
- raw coarse cells dominate MAIN solely because they are the source format;
- terrain/hydrology is made vague by blur, glow, paper texture or atmospheric effects;
- all analytical variables compete on one map at equal weight;
- plan and section do not correspond;
- sampled convergence is drawn as real drainage/flood infrastructure;
- design consequences visually masquerade as observed/source facts;
- missing evidence is replaced by proxy graphics.

Detailed implementation and review rules live in `LANDSCAPE_GIS_ANALYSIS_BINDING.md` and `VISUAL_LAYER_BINDING.md`.

## Operational route-state semantics gate

Apply this gate whenever route, path, network, access, facility, service, or wayfinding graphics encode operational states such as `NORMAL`, `DEGRADED`, `CLOSED`, `UNKNOWN`, or equivalent project-specific states.

1. **Topology authority and state authority are separate.** A state overlay may change how a route is interpreted or used, but must not silently rewrite where the authoritative route exists.
2. Color may support state recognition but must not be the only carrier of state meaning. Pair hue with at least one additional visual channel appropriate to the medium: stroke pattern, marker geometry, line weight, endpoint treatment, text, icon, or fill pattern.
3. `CLOSED` must read as a hard operational interruption when that is the project meaning. A closed segment must not look like a lower-confidence or merely less-important open route.
4. `UNKNOWN` is not a weak form of `NORMAL`. When the current project authority requires fail-closed behavior, depict `UNKNOWN` as uncertain / not safely assumable open, and never normalize it into the same continuous open-path grammar.
5. `DEGRADED` must remain distinguishable from both `NORMAL` and `CLOSED`; use a reversible visual degradation such as long dash, reduced line weight, caution marker, or explicit state text without breaking the underlying topology.
6. Critical route-state graphics must survive grayscale / low-color review. Generate or inspect a grayscale derivative and confirm the states remain distinguishable without hue.
7. For screen-based interfaces, meaningful graphical state indicators must remain perceivable at the intended delivery size and should meet the applicable non-text contrast requirement. Do not use low-contrast status styling as a substitute for hierarchy.
8. State labels, legends, and endpoint behavior must agree. A line that visually continues forward must not be labelled `CLOSED`; an `UNKNOWN` label must not sit on a visually normal open path.
9. Multi-state figures must record the state source, timestamp/version where relevant, and whether the state is observed, reported, inferred, assumed, simulated, or placeholder. Visual polish must not promote an inferred or unknown state into observed fact.
10. Before promotion, inspect at least: color view, grayscale view, compact/target-size view, and the highest-risk transition (`NORMAL→DEGRADED`, `DEGRADED→CLOSED`, `UNKNOWN→known`). If state meaning becomes ambiguous in any required view, return `REVISE`.

This gate follows the same truth discipline as spatial authority preservation: **state semantics may change interpretation, not source topology**, and `UNKNOWN` must never be presented as safely open merely because a continuous route line is aesthetically cleaner.

## Motion rules

- Keep axes and color scales stable across frames.
- Use a consistent entity key across time.
- Show time, units, and data source in every frame.
- Avoid animation when small multiples communicate the change better.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## Required output

Return the visualization, cleaned dataset, data dictionary, transformation note, source note, and a short statement of what the visual supports—and what it does not prove.

For source-bound spatial work, also return a geometry-authority note identifying the current source/locked object, the preservation operation, and any geometry regression check performed.

For landscape/site GIS analysis drawings, additionally return a precision note separating source precision from derived/display precision, and include mapped section authority when sections are part of the argument.

## Quality checks

- Reconcile displayed values with the cleaned table.
- Check color-blind legibility and grayscale hierarchy.
- Avoid truncated axes unless clearly justified.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For source-bound spatial work, verify that locked geometry/topology has not been materially distorted, re-authored, or replaced by a presentation-driven approximation.
- Treat non-uniform geometry distortion as a blocker unless the object is explicitly schematic and labelled presentation-only.
- Compare against the strongest mature existing spatial artifact before promoting a redesign; visual polish cannot override a spatial-authority regression.
- For landscape/site GIS analysis, verify the source-precision ceiling, terrain-first hierarchy, raw-grid role, one-variable-per-panel logic, hydrology semantics, plan–section correspondence, master-vs-support rhythm, near-read technical density, and style-removal robustness.
