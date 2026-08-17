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

## Motion rules

- Keep axes and color scales stable across frames.
- Use a consistent entity key across time.
- Show time, units, and data source in every frame.
- Avoid animation when small multiples communicate the change better.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## Required output

Return the visualization, cleaned dataset, data dictionary, transformation note, source note, and a short statement of what the visual supports—and what it does not prove.

For source-bound spatial work, also return a geometry-authority note identifying the current source/locked object, the preservation operation, and any geometry regression check performed.

## Quality checks

- Reconcile displayed values with the cleaned table.
- Check color-blind legibility and grayscale hierarchy.
- Avoid truncated axes unless clearly justified.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For source-bound spatial work, verify that locked geometry/topology has not been materially distorted, re-authored, or replaced by a presentation-driven approximation.
- Treat non-uniform geometry distortion as a blocker unless the object is explicitly schematic and labelled presentation-only.
- Compare against the strongest mature existing spatial artifact before promoting a redesign; visual polish cannot override a spatial-authority regression.
