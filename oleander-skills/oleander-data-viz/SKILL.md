---
name: oleander-data-viz
description: Produce accurate and professionally designed static, animated, interactive, spatial, and presentation-ready visualizations for Oleander. Use whenever the user mentions Oleander tables, XLSX/CSV analysis, animated charts, timelines, maps, diagrams, dashboards, research visualization, SVG/PNG/HTML/MP4 chart exports, or converting project data into visual evidence.
compatibility: Uses Python 3.13 environment C:\Users\Xianmu\.venvs\oleander and may use spreadsheets, QGIS 4, FFmpeg, ImageMagick, Plotly, GeoPandas, or Sites.
---

# Oleander Data Visualization

Transform project data into reproducible visual evidence **and a professionally readable visual artifact**. Preserve the source data and make every transformation auditable.

`DATA CORRECTNESS != DESIGN QUALITY`  
`EXPORT SUCCESS != PROFESSIONAL FINISH`  
`TRACEABILITY != FIRST-READ CLARITY`

This skill is governed by the current OLEANDER Independent Design Verdict Policy and Artifact Review System. A producer may finish and self-check a visualization, but may not self-promote it to `PIXEL KEEP`, `MAIN KEEP`, or `PROFESSIONAL FINISH PASS`.

## Environment

Use `C:\Users\Xianmu\.venvs\oleander\Scripts\python.exe`.

Core libraries include pandas, Polars, OpenPyXL, XlsxWriter, Matplotlib, Seaborn, Plotly, Kaleido, Altair, NetworkX, OpenCV, GeoPandas, Shapely, PyProj, Rasterio, Contextily, and OSMnx.

Use QGIS 4 for interactive GIS editing and Python/GeoPandas for reproducible spatial transformations. Do not bind scripts to QGIS 3 paths.

## 0. Existing Mature Design First

Before redrawing an existing project chart, map, network, analytical diagram, or evidence graphic:

1. Open the strongest Current-Authority-permitted mature artifact at intended viewing size.
2. Identify what already works: first-read, composition, proportion, hierarchy, relation grammar, typography, annotation rhythm, project specificity, and cross-media role.
3. Separate **content/truth problems** from **pixel/design problems**.
4. Preserve solved design DNA unless the current evidence or task requires a material change.
5. A cleaner or newer chart is not automatically better. Compare the candidate side-by-side against the strongest existing design.

Never replace a mature design with a generic dashboard, equal-card grid, technical-report graphic, or governance diagram merely because the new output is more structured or easier to generate.

## 1. Workflow

1. Inspect source files, units, missing values, time ranges, coordinate systems, category definitions, evidence status, and Current Authority.
2. Keep raw data unchanged; write cleaned data separately with a transformation log.
3. State the analytical question and the **one primary visual claim** the artifact is allowed to make.
4. Choose the visual form from the question and data relationship, not decoration.
5. Create the Visual Contract below before drawing.
6. Build the visualization reproducibly with editable structure.
7. Run data/GIS checks.
8. Reopen the actual final artifact at intended display size and run the Design Quality Gate.
9. Compare against the strongest existing mature design where one exists.
10. Export and record `EXECUTED / SELF-CHECKED / REVIEW PENDING`; independent review is required for KEEP-class promotion.

## 2. Visual Contract

Record, at minimum:

- `audience`
- `question`
- `primary_claim`
- `source_authority`
- `truth_boundary / does_not_prove`
- `visual_form`
- `primary_mark_or_relation`
- `secondary_context`
- `units / denominator / scale_rule`
- `lineweight_or_mark_hierarchy`
- `annotation_budget`
- `far_read / mid_read / near_read`
- `intended_output_size`
- `editable_source`
- `accessibility_equivalent`

If the claim cannot be stated in one sentence without explanation, the figure is not ready to draw.

## 3. Form Selection

Choose the simplest form that preserves the analytical relationship:

- categorical comparison / ranking → bar or dot plot;
- ordered trend / time → line or area only when area encoding is meaningful;
- distribution → histogram, strip, box/violin, or small multiples as appropriate;
- relationship between numeric variables → scatter / regression only when inference is justified;
- part-to-whole → stacked bar by default; pie only for a small, meaningful one-time whole;
- process / causal sequence → staged flow with explicit direction and no decorative branching;
- spatial relation → GIS/map only when coordinates are authoritative; otherwise label as relational / diagrammatic;
- network / topology → node-edge diagram only when topology itself is the claim;
- evidence → inference → decision → use a directional analytical strip or relation field, not a wall of cards.

Do not use a map-like graphic when the data supports only topology or relation. `RELATIONAL / NTS / NOT GEOREFERENCED` must appear on the figure itself when applicable.

## 4. Visual Hierarchy Gate

A professional chart must establish unequal visual weight deliberately.

### 4.1 Hierarchy ladder

Use a five-level reading ladder instead of equal emphasis:

- **H0 / Claim:** one sentence or one primary spatial/metric relationship. Must dominate first-read.
- **H1 / Primary structure:** main series, route, axis, spatial field, or comparison.
- **H2 / Secondary structure:** context series, optional branches, supporting categories, or secondary nodes.
- **H3 / Evidence + uncertainty:** sources, ranges, confidence, missing/inferred state, field-open or scenario state.
- **H4 / Metadata:** IDs, version, date, file state, technical notes.

H3/H4 must remain readable but must not visually compete with H0/H1.

### 4.2 Line / mark semantics

For diagrams, networks and maps, line weight is semantic:

- primary route / backbone / measured series = strongest continuous mark;
- secondary relation / optional branch = clearly subordinate;
- inferred / conditional / field-open = distinct line pattern **plus a text/legend label**;
- annotation leader = lighter than the data structure it explains;
- decoration must never be stronger than evidence.

Do not encode evidence status by color alone. Preserve grayscale legibility.

### 4.3 Node hierarchy

Node size, fill and label prominence must follow **role**, not merely category count.

- route/service/return anchors outrank optional reading/content nodes when route authority is the task;
- optional nodes must not visually convert a network into a checklist;
- companion/secondary nodes may remain visible without becoming equal stops;
- a critical recovery/return node may receive emphasis only when the evidence and task justify it.

### 4.4 Return / fallback readability

For journey, service or operational diagrams, Return/fallback cannot live only in body copy or a legend. The return relation must be identifiable from the diagram itself without converting an open network into a fake single route.

## 5. Composition and Reading Distance

A chart is a composition, not only a plotting result.

For boards / portfolio / 1920×1080 presentation frames, explicitly test:

- **far read:** the primary claim and primary structure are legible without reading captions;
- **mid read:** the relation between major parts / series / zones is clear;
- **near read:** evidence state, units, source notes, uncertainty and IDs are available.

As a working presentation benchmark, a board may allocate the majority of visual weight to one dominant field, a secondary share to one major analytical drawing, a narrow share to evidence consequence, and the smallest share to source/meta. Do not turn these shares into a rigid template; preserve the project’s mature composition where stronger.

Avoid:

- equal-card grids;
- four or more equally loud mini-panels;
- giant explanatory text compensating for a weak figure;
- decorative contour / mountain / grid backgrounds that add no evidence;
- oversized legends;
- repeated status pills that make the artifact read like admin UI;
- overly polished graph geometry that falsely implies surveyed or measured precision.

## 6. Labels and Annotation

- Prefer direct labels when they reduce eye travel and collision.
- Keep labels attached to the structure they explain; avoid detached label clouds.
- Establish a label priority list before automatic placement.
- Resolve collisions by moving low-priority labels, not by shrinking everything equally.
- Use leaders consistently; leaders must not cross primary data marks unnecessarily.
- Annotate the turning point, exception, boundary, or design implication—not every datum.
- Preserve source terms, units and uncertainty exactly where they matter.

A dense figure that requires body text to decode its hierarchy is `REVISE`.

## 7. Evidence and Truth Encoding

Every visual must preserve the distinction between:

- observed / measured;
- source-grounded relation;
- inferred;
- estimated / scenario;
- assumed;
- unknown / field-open;
- decision / design consequence.

Use redundant semantics: line style, marker form, labels, captioning, and/or grouping. Never promote an inferred value or diagrammatic placeholder into measured fact through visual polish.

For source-traced spatial work, distinguish:

`SOURCE-TRACED RELATION` vs `DIAGRAMMATIC PLACEHOLDER` vs `FIELD / SURVEY OPEN`.

## 8. Deletion Test and First-Visual Veto

Before final export, hide the explanation and inspect only the artifact.

Ask:

1. What is read in the first 3 seconds?
2. Is the primary claim visible in the marks, or only in the title?
3. Can any panel, contour, icon, label, legend block, background field, or status badge be removed without weakening the claim? If yes, remove it.
4. Does the chart still work in grayscale and at 50% size?
5. Does it look like a project-specific analytical artifact or a generic dashboard/template?
6. Does any neat geometry overstate geographic, temporal, statistical, or engineering precision?

First-visual failures have veto power. Data correctness, source traceability and successful export cannot average them away.

## 9. Motion Rules

- Keep axes and color scales stable across frames unless a deliberate scale change is explicitly shown.
- Use a consistent entity key across time.
- Show time, units, and data source in every analytical frame where needed for interpretation.
- Avoid animation when small multiples communicate the change better.
- Motion must reveal change, causality, sequence, filtering, threshold crossing, or spatial relation; decorative movement is not analysis.
- Network animation must not imply a single route order when the topology is open/branching.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## 10. Export

Export as required:

- SVG for Illustrator / Inkscape / editable board use;
- PNG at explicit pixel dimensions for actual-preview review;
- HTML for interaction;
- MP4/WebM/GIF only when motion adds meaning;
- XLSX with source/clean/data-dictionary sheets when a table is part of delivery.

Preserve stable IDs, relative paths, source note, version and intended dimensions.

## 11. Required Output

Return or persist, as applicable:

1. visualization artifact;
2. editable source;
3. cleaned dataset;
4. data dictionary;
5. transformation note;
6. source / evidence note;
7. Visual Contract;
8. statement of what the visual supports and does not prove;
9. actual-preview self-check;
10. strongest-existing benchmark reference when one exists;
11. independent review status.

## 12. Quality Checks

### Data / analytical

- Reconcile displayed values with the cleaned table.
- Check units, denominators, missing values, duplicates, ranges and formulas.
- Avoid truncated axes unless clearly justified.
- Validate map CRS / projection / NoData where applicable.
- Confirm data-to-artifact consistency.

### Design / visual

- First-read claim is visible in the artifact itself.
- Primary / secondary / evidence / metadata hierarchy is unequal and intentional.
- Lineweight and marker semantics survive grayscale.
- Labels do not collide with data or each other at intended size.
- Composition is not a dashboard/card wall unless the actual task is operational monitoring.
- Annotation density is controlled.
- Project specificity does not depend mainly on title text.
- Return/fallback is visually legible when it is part of the design claim.
- Source-traced vs placeholder geometry is unambiguous.
- Candidate does not regress against the strongest mature existing design.

### Accessibility / output

- Check color-blind legibility and grayscale hierarchy.
- Provide text/data equivalent for interactive or high-density graphics.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- Reopen the final export before recording status.

## 13. Verdict

Producer status is limited to:

`EXECUTED / SELF-CHECKED / REVIEW PENDING / REVISE / REJECT`.

KEEP-class promotion requires independent visual/design readback under the current OLEANDER governance and regression-evaluation rules.
