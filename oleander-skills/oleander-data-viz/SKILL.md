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

## Uncertainty-first scenario charts

Use this gate whenever a value is estimated, inferred, scenario-based, provisional, remotely researched, or awaiting FIELD correction.

1. Do not let a recommended value read as a measured scalar. A single bar, large numeral, or isolated point is `REVISE` when the underlying plausible range could change interpretation or a decision.
2. When uncertainty is decision-relevant, make the plausible range the primary visual mark and place the recommended or central estimate as a subordinate point inside that range. Dot-range, interval, or band forms are preferred over bars with decorative error marks.
3. Keep the following adjacent to the visual, not hidden in a distant footnote: unit, range definition, evidence class, confidence/quality state, and FIELD correction status when applicable.
4. Distinguish evidence provenance from probability. If line style, symbol, texture, or another channel encodes `SOURCE-GROUNDED / INFERRED / ASSUMPTION`, state explicitly that the channel does not represent likelihood unless it truly does.
5. Use plain-language uncertainty wording where possible. Do not imply statistical confidence intervals when the range is instead an engineering scenario, sensitivity band, expert estimate, or design allowance.
6. If uncertainty is so large that the visual cannot support a meaningful comparison or decision, do not force a ranked chart. State the limitation and keep the underlying values available in the data table.
7. The absence of measured field data is not a reason to collapse to a single neat number. Preserve `recommended value + reasonable range + basis + sensitivity + future FIELD correction item` when the project authority requires provisional advancement.
8. In critique, separately test first-read and truthfulness: the chart must be visually clear, but visual polish cannot upgrade `ASSUMPTION` to evidence or `PROVISIONAL` to measured fact.

Reference calibration: UK Office for National Statistics guidance on showing uncertainty in charts recommends uncertainty ranges when they materially change interpretation and favours range-oriented forms such as shaded bands or dot plots with ranges. OLEANDER extends that principle to non-statistical design scenarios by preserving the explicit evidence class and FIELD boundary.

## Motion rules

- Keep axes and color scales stable across frames.
- Use a consistent entity key across time.
- Show time, units, and data source in every frame.
- Avoid animation when small multiples communicate the change better.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## Required output

Return the visualization, cleaned dataset, data dictionary, transformation note, source note, and a short statement of what the visual supports—and what it does not prove.

## Quality checks

- Reconcile displayed values with the cleaned table.
- Check color-blind legibility and grayscale hierarchy.
- Avoid truncated axes unless clearly justified.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For provisional/scenario values, verify that range, evidence class and FIELD state remain legible at the intended viewing scale.
- Never treat chart export success, traceability, or numerical consistency as a substitute for a Design Crit or truth-state review.
