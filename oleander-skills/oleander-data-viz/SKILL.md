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

## Map label priority and collision gate

Apply this gate whenever a map, route network, diagram, or spatial interface contains enough labels that density can change route or decision readability.

1. Classify every label before placement. At minimum distinguish `P1 CRITICAL` (entry, exit, return, safety, decision, current target), `P2 IMPORTANT` (major named place or route relation), and `P3+ SUPPORT` (secondary POI, descriptive, interpretive, or redundant context).
2. **Priority controls retention rights, not only typography.** P1 labels must not disappear under ordinary density pressure. P2 labels should be protected whenever a collision-free or acceptably displaced position exists. P3+ labels may move, defer, cluster, abbreviate, or suppress before P1/P2 are sacrificed.
3. Do not use `show everything` as a completeness proxy. Complete data does not require complete simultaneous labeling. Hidden/suppressed labels remain in the source data and must be recoverable through zoom, interaction, legend, index, hover, selection, or a less-dense scale where applicable.
4. Use variable anchors / offsets before hiding important labels. Point labels should test multiple placements around the anchor; line labels should follow their geometry when that improves identification without false geometry.
5. Run collision checks at the actual delivery size, not only on a large authoring canvas. Re-run after font, language, responsive breakpoint, export scale, or label-content changes.
6. Keep label hierarchy aligned with route hierarchy. A support POI must not visually overpower entry, return, closure, hazard, or a route junction merely because its name is longer.
7. Suppression is a presentation operation only. It must not delete the underlying feature, alter topology, or imply that an unlabeled route/node does not exist.
8. When labels from different layers compete, define a deterministic placement / sort policy rather than relying on accidental draw order. Record which label classes win collisions.
9. For dense small-screen or fixed-scale maps, prefer fewer legible labels with preserved context over forcing all names into the viewport. If users still need access to all names, add an explicit retrieval mechanism rather than shrinking text below the intended reading threshold.
10. Promotion requires a matched-scale visual reopen at both the normal working scale and the densest expected delivery scale. If topology is correct but P1/P2 decisions become hard to find because of label clutter, the map is `REVISE`.

Implementation note: Mapbox symbol layers expose collision behavior, `text-variable-anchor`, padding, placement and sort-key mechanisms; equivalent tools in QGIS or custom SVG/HTML renderers may be used. The gate is tool-agnostic: the required outcome is deterministic priority, collision control, and preserved topology.

## Motion rules

- Keep axes and color scales stable across frames.
- Use a consistent entity key across time.
- Show time, units, and data source in every frame.
- Avoid animation when small multiples communicate the change better.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## Required output

Return the visualization, cleaned dataset, data dictionary, transformation note, source note, and a short statement of what the visual supports—and what it does not prove.

For source-bound spatial work, also return a geometry-authority note identifying the current source/locked object, the preservation operation, and any geometry regression check performed.

For dense labeled maps, also return the label-priority rule, collision/suppression behavior, and a compact-scale proof showing that critical labels remain readable.

## Quality checks

- Reconcile displayed values with the cleaned table.
- Check color-blind legibility and grayscale hierarchy.
- Avoid truncated axes unless clearly justified.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For source-bound spatial work, verify that locked geometry/topology has not been materially distorted, re-authored, or replaced by a presentation-driven approximation.
- Treat non-uniform geometry distortion as a blocker unless the object is explicitly schematic and labelled presentation-only.
- Compare against the strongest mature existing spatial artifact before promoting a redesign; visual polish cannot override a spatial-authority regression.
- For labeled maps, verify that P1/P2 labels survive the densest intended scale and that any suppressed P3+ labels remain present in the source dataset.
- Treat `all labels fit on the authoring canvas` as insufficient evidence; inspect the exported/delivery-scale pixels.
