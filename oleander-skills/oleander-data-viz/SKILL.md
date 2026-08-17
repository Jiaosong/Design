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
`RENDERER VALID != VISUALIZATION VALID != DESIGN KEEP`

This skill is governed by the current OLEANDER Independent Design Verdict Policy and Artifact Review System. A producer may finish and self-check a visualization, but may not self-promote it to `PIXEL KEEP`, `MAIN KEEP`, or `PROFESSIONAL FINISH PASS`.

## Environment

Use `C:\Users\Xianmu\.venvs\oleander\Scripts\python.exe`.

Core libraries include pandas, Polars, OpenPyXL, XlsxWriter, Matplotlib, Seaborn, Plotly, Kaleido, Altair, NetworkX, OpenCV, GeoPandas, Shapely, PyProj, Rasterio, Contextily, and OSMnx.

Use QGIS 4 for interactive GIS editing and Python/GeoPandas for reproducible spatial transformations. Do not bind scripts to QGIS 3 paths.

For routing among chart, graph, infographic, geographic and narrative renderers, also consult `ROUTING_AND_RENDERER_ADAPTERS_v0.1.md`. Renderer syntax belongs in adapters; design/truth policy remains here. For the current executable chart contract, align the project instance with Notion Canonical `T-DATAVIZ-OLEANDER-001｜OLEANDER Chart Spec v0.2`; the Skill owns reusable policy while the Chart Spec owns the fillable execution contract.

## 0. Existing Mature Design First

Before redrawing an existing project chart, map, network, analytical diagram, or evidence graphic:

1. Open the strongest Current-Authority-permitted mature artifact at intended viewing size.
2. Identify what already works: first-read, composition, proportion, hierarchy, relation grammar, typography, annotation rhythm, project specificity, and cross-media role.
3. Separate **content/truth problems** from **pixel/design problems**.
4. Preserve solved design DNA unless the current evidence or task requires a material change.
5. A cleaner or newer chart is not automatically better. Compare the candidate side-by-side against the strongest existing design.

Never replace a mature design with a generic dashboard, equal-card grid, technical-report graphic, or governance diagram merely because the new output is more structured or easier to generate.

## 0.5 Subject Grounding + One Signature

A visualization must look as though it belongs to its actual subject, not to a generic chart generator.

Before drawing, identify:

- the concrete subject and audience;
- the figure's single job;
- the subject's own structural vocabulary: material, spatial relation, process, terminology, measurement convention, or graphic vernacular;
- one justified **signature**: the single memorable visual move that best expresses the claim.

Spend visual boldness in one place. Keep surrounding elements restrained and functional. Numbering, dividers, bands, labels, icons, gradients, contours and other structural devices must encode something true about the content; do not add them as decoration.

## 1. Workflow

1. Inspect source files, units, missing values, time ranges, coordinate systems, category definitions, evidence status, and Current Authority.
2. Keep raw data unchanged; write cleaned data separately with a transformation log.
3. State the analytical question and the **one primary visual claim** the artifact is allowed to make.
4. Classify the information structure before choosing a renderer: comparison, trend, distribution, hierarchy, relation/topology, strict sequence, geographic, explanatory narrative, or mixed composition.
5. Choose the visual form from the question and data relationship, not decoration or a favorite template.
6. Create the Visual Contract below and instantiate the current `T-DATAVIZ-OLEANDER-001` Chart Spec before drawing.
7. Lock the analytical grammar: `data -> transform -> mark -> channel -> scale -> facet -> interaction -> annotation`.
8. Route to the simplest renderer family that can express the claim without loss.
9. Build the visualization reproducibly with editable structure.
10. Run data/GIS/topology checks as applicable.
11. Reopen the actual final artifact at intended display size and run the Design Quality Gate.
12. Compare against the strongest existing mature design where one exists.
13. Export and record `EXECUTED / SELF-CHECKED / REVIEW PENDING`; independent review is required for KEEP-class promotion.

## 2. Visual Contract

Record, at minimum:

- `audience`
- `question`
- `primary_claim / one_sentence_finding`
- `reading_mode`: `fast_scan | directed_read | exploration`; only add a clock-time target when the project has evidence for one
- `source_authority`
- `truth_boundary / does_not_prove`
- `information_structure`
- `visual_form`
- `visual_idea`
- `first_read_object / dominant_field`
- `first_read_label_budget`
- `renderer_family`
- `geometry_layout_engine`
- `engine_role`: `grammar | transform | scale | coordinate | layout | edge_routing | geometry`
- `renderer`: `SVG | Canvas | WebGL | other`
- `data_transform`
- `primary_mark_or_relation`
- `encoding_channels`
- `scale_rule`
- `secondary_context`
- `units / denominator`
- `lineweight_or_mark_hierarchy`
- `grid / alignment rule`
- `annotation_budget`
- `negative_space / hierarchy rule`
- `abstraction_budget`
- `far_read / mid_read / near_read`
- `signature`
- `semantic_svg_structure`: stable `group / id / data-role / layer` naming when SVG is material
- `spatial_authority_lock`: task-critical anchors that an automatic layout may not move/delete
- `deterministic_render`: renderer/version/font/fallback/canvas parameters when reproducibility is material
- `intended_output_size`
- `editable_source`
- `accessibility_equivalent`

If the claim cannot be stated in one sentence without explanation, the figure is not ready to draw.

### 2.1 Visual Idea Before Decoration

After the analytical grammar is valid, define how the claim becomes a visual event before styling details:

1. **Finding** — what single judgment should survive after the viewer leaves the page?
2. **Visual idea** — which proportion, path, field, comparison, area, number, spatial relation or typographic relationship can carry that finding directly?
3. **Dominant field** — what should control first-read, and what must remain quiet?
4. **Label budget** — which 2–5 labels/numbers/relations are necessary at first-read? Move the rest to directed/near reading.
5. **Remove Decoration Test** — remove gradients, stickers, ornamental lines, extra status colors, badges and effects. If the core relation collapses, revise the structure rather than restoring decoration.
6. **Series rhythm** — unify design DNA across a series, but do not force every page into the same template or reading speed.

`CHART TYPE != VISUAL IDEA`

A renderer can generate correct marks while the editorial composition remains weak.

## 2.5 Analytical Grammar Before Styling

Treat the figure as a declarative visual system before styling it.

1. **Data** — what records/geometry are authoritative?
2. **Transform** — filter, aggregate, bin, normalize, join, route, rank, calculate or infer. Every transform must be explicit.
3. **Mark** — point, line, area, bar, text, link, node, polygon, image, rule.
4. **Channel** — x/y, position, length, angle, size, color, opacity, shape, stroke pattern.
5. **Scale** — domain, zero rule, normalization, logarithmic/linear/ordinal, geographic projection where applicable.
6. **Facet/layer** — only when comparison or context requires it.
7. **Interaction** — filter, highlight, brush, zoom, state change; only when it changes understanding or task performance.
8. **Annotation** — claim-bearing labels, uncertainty, source, boundary and design implication.

Do not style around a weak grammar. If the data relationship cannot be stated clearly at this level, visual polish is premature.

## 3. Form Selection

Choose the simplest form that preserves the analytical relationship:

- categorical comparison / ranking -> bar or dot plot;
- ordered trend / time -> line or area only when area encoding is meaningful;
- distribution -> histogram, strip, box/violin, or small multiples as appropriate;
- relationship between numeric variables -> scatter / regression only when inference is justified;
- part-to-whole -> stacked bar by default; pie only for a small, meaningful one-time whole;
- process / causal sequence -> staged flow with explicit direction and no decorative branching;
- spatial relation -> GIS/map only when coordinates are authoritative; otherwise label as relational / diagrammatic;
- network / topology -> node-edge diagram only when topology itself is the claim;
- hierarchy -> tree/indented hierarchy/containment only when parent-child structure is real;
- evidence -> inference -> decision -> use a directional analytical strip or relation field, not a wall of cards;
- narrative interpretation -> structured text with semantic entity metadata only when prose is the primary reading mode.

Do not use a map-like graphic when the data supports only topology or relation. `RELATIONAL / NTS / NOT GEOREFERENCED` must appear on the figure itself when applicable.

### 3.1 Information Structure Before Template

Treat templates as renderers, never as evidence or design authority.

- Use `sequence-*` / timelines / roadmaps only when a strict order, time sequence or staged dependency is supported.
- Use `relation-*` / network only when pairwise or topological relations are the actual claim.
- Use hierarchy only when parent-child or containment relations are real.
- Use comparison forms only when dimensions are meaningfully comparable.
- Use list/grid forms only for genuinely parallel items; do not convert a causal or relational argument into equal cards for convenience.
- Do not turn a relation into a sequence because a sequence template looks cleaner.
- Do not turn uncertainty or branch choice into a forced order.

`INFORMATION STRUCTURE -> VISUAL FORM -> RENDERER`, never `TEMPLATE -> CLAIM`.

### 3.2 Graph / Network Layout Semantics

For graph engines such as G6, NetworkX, D3-force or custom SVG:

- stable node IDs and explicit `source/target` edges are mandatory;
- node/edge roles belong in data, not only in style;
- computational layout is a presentation transform unless the positions themselves are authoritative data;
- force, dagre, radial, circular, mindmap or grid layouts must not be read as measured geography, distance, chronology, rank or flow volume unless separately encoded and supported;
- overlap prevention, dragging, zooming, selection or collapse/expand are interaction behaviors, not evidence;
- interaction must not silently rewrite topology or evidence status;
- when a fixed relational composition is required for a board, prefer deterministic coordinates and preserve a machine-readable topology companion;
- task-critical anchors such as river/bank relation, station, Return, Service, true orientation or other Current-Authority geometry must be locked before automatic layout when the user task depends on them.

If layout position is not evidence, label or caption that boundary explicitly.

### 3.3 Design Core / Router / Renderer Adapter Separation

Keep three layers separate:

1. **Design core** — claim, evidence, truth boundary, hierarchy, composition, typography, annotation, accessibility and review.
2. **Intent/form router** — comparison, trend, distribution, topology, hierarchy, sequence, geographic, infographic, narrative text, etc.
3. **Renderer adapter** — version-specific syntax and runtime rules for G2, G6, Plotly, D3, QGIS, kepler.gl, SVG, AntV Infographic, T8, or other engines.

A renderer adapter may prove that code is valid for a library. It cannot establish source validity, analytical validity or professional visual quality.

For renderer choice, declare the engine's **role** explicitly. D3/G2/G6/Plot/Vega/ECharts/custom code may own grammar, transforms, scale, coordinate, layout, edge routing or geometry. They do not own final aesthetic judgment.

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

### 4.2 Position and size before decoration

Establish hierarchy first through **position, area, length, scale and whitespace**. Use weight and color later and more sparingly. If an element needs bright color merely to become visible, first check whether its position/size hierarchy is wrong.

### 4.3 Line / mark semantics

For diagrams, networks and maps, line weight is semantic:

- primary route / backbone / measured series = strongest continuous mark;
- secondary relation / optional branch = clearly subordinate;
- inferred / conditional / field-open = distinct line pattern **plus a text/legend label**;
- annotation leader = lighter than the data structure it explains;
- decoration must never be stronger than evidence.

Do not encode evidence status by color alone. Preserve grayscale legibility.

### 4.4 Node hierarchy

Node size, fill and label prominence must follow **role**, not merely category count.

- route/service/return anchors outrank optional reading/content nodes when route authority is the task;
- optional nodes must not visually convert a network into a checklist;
- companion/secondary nodes may remain visible without becoming equal stops;
- a critical recovery/return node may receive emphasis only when the evidence and task justify it.

### 4.5 Return / fallback readability

For journey, service or operational diagrams, Return/fallback cannot live only in body copy or a legend. The return relation must be identifiable from the diagram itself without converting an open network into a fake single route.

## 5. Composition, Grid and Reading Distance

A chart is a composition, not only a plotting result.

### 5.1 Task -> content -> measure -> grid

Build layout in this order:

`task -> required content -> reading measure/density -> grid -> typography/spacing -> placement`

Do not begin with a 12-column grid because it is familiar. The task and content determine the grid.

Use one coherent grid per surface; derive sub-layouts by span rather than introducing unrelated local grids. Every major element should align to the system on at least one axis. Small near-alignments read as mistakes; deliberate major breaks are allowed when they clearly serve the claim.

For data/diagram panels, snap images, plots, captions and evidence strips to whole modules. Captions align to the figure they describe. Keep baseline and spacing increments systematic.

### 5.2 Intended-size and Reading-mode Hierarchy

For boards / portfolio / 1920x1080 presentation frames, explicitly test:

- **far read:** the primary claim and primary structure are legible without reading captions;
- **mid read:** the relation between major parts / series / zones is clear;
- **near read:** evidence state, units, source notes, uncertainty and IDs are available.

Also classify the intended reading task as:

- **fast scan** — orientation / first judgment;
- **directed read** — inspect a named relation, comparison, exception or evidence layer;
- **exploration** — trace detail, filter, browse or compare multiple structures.

Do not impose a universal `3-second` or `30-second` threshold. Record a clock-time target only when the project has a real viewing condition, user task, exhibition distance, interface requirement or test protocol that justifies it.

A poster/hero analytical frame should normally have one clearly dominant element. As a diagnostic starting point, that dominant visual field often occupies roughly 60–80% of perceived attention/area, with secondary evidence and metadata substantially quieter. This is not a template or scoring rule; the strongest mature design remains the benchmark.

Avoid:

- equal-card grids;
- four or more equally loud mini-panels;
- giant explanatory text compensating for a weak figure;
- decorative contour / mountain / grid backgrounds that add no evidence;
- oversized legends;
- repeated status pills that make the artifact read like admin UI;
- overly polished graph geometry that falsely implies surveyed or measured precision;
- repeated identical section structures when the content relationships are different.

## 6. Labels and Annotation

- Prefer direct labels when they reduce eye travel and collision.
- Keep labels attached to the structure they explain; avoid detached label clouds.
- Establish a label priority list before automatic placement.
- Resolve collisions by moving low-priority labels, not by shrinking everything equally.
- Use leaders consistently; leaders must not cross primary data marks unnecessarily.
- Annotate the turning point, exception, boundary, or design implication—not every datum.
- Preserve source terms, units and uncertainty exactly where they matter.
- Copy must be concrete and claim-bearing. Remove fake section labels, filler superlatives and labels that only describe the layout rather than the data.

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

### 7.1 Semantic Entity Contract for Narrative + Figure Linking

Borrow the useful idea of semantic entity annotation from narrative-visualization systems, but bind it to OLEANDER truth states.

For important values, claims or named entities, preserve a machine-readable companion with fields such as:

- `entity_id`
- `display_text`
- `entity_type`
- `raw_value`
- `unit`
- `time_or_scope`
- `source_ref`
- `evidence_state`
- `claim_role`
- `assessment` only when the evaluative direction is justified
- `detail` for supporting arrays/relations when needed
- `does_not_prove`

The displayed prose may be concise, but raw value, unit, provenance and evidence state must remain recoverable. Semantic annotations may generate mini-charts or highlights; they must not manufacture certainty.

Unlike external systems that ban all scenario/simulated values, OLEANDER may use estimates, scenarios and simulations when the current protocol allows them **and** their state is explicit. Scenario data must never be serialized as observed fact.

### 7.2 Semantic SVG Contract

When SVG is a formal editable deliverable rather than only a transport format:

- preserve stable `id` values for material objects and groups;
- group objects by semantic role/layer, not only by paint order;
- use `data-role`, stable group names or an equivalent machine-readable convention where useful;
- keep displayed text as editable SVG `<text>` by default; convert to outlines only for a declared compatibility/rights reason and record that substitution;
- do not treat a large anonymous path cloud as semantic editability;
- keep source-data IDs / node IDs / entity IDs recoverable when the relationship is material;
- distinguish renderer-generated geometry from manually refined geometry and reconcile both against the data/spec;
- when deterministic regeneration matters, record renderer/version/font/fallback/canvas parameters and rerun a same-input check.

`SVG EXISTS != SEMANTIC SVG != DESIGN KEEP`

## 8. Deletion Test and First-Visual Veto

Before final export, hide the explanation and inspect only the artifact.

Run the first-read check appropriate to the declared `reading_mode` (`fast_scan / directed_read / exploration`). A fixed seconds threshold is allowed only when the project has a justified viewing/test condition.

1. What draws the eye first? Is it the right thing?
2. Can the viewer tell what the figure is for without the body copy at the intended viewing condition?
3. Is the primary claim visible in the marks/relations, or only in the title?
4. Can any panel, contour, icon, label, legend block, background field, status badge or ornamental effect be removed without weakening the claim? If yes, remove it.
5. Does the chart still work in grayscale and at a relevant reduced size?
6. Does it look like a project-specific analytical artifact or a generic dashboard/template?
7. Does any neat geometry overstate geographic, temporal, statistical, or engineering precision?
8. Is there one memorable signature rather than many competing effects?

First-visual failures have veto power. Diagnostic scores cannot average them away. Data correctness, source traceability and successful export cannot average them away either.

## 9. Motion Rules

- Keep axes and color scales stable across frames unless a deliberate scale change is explicitly shown.
- Use a consistent entity key across time.
- Show time, units, and data source in every analytical frame where needed for interpretation.
- Avoid animation when small multiples communicate the change better.
- Motion must reveal change, causality, sequence, filtering, threshold crossing, or spatial relation; decorative movement is not analysis.
- Network animation must not imply a single route order when the topology is open/branching.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## 10. Editable Vector Bridge

When a figure benefits from designer refinement, preserve this chain:

`raw data -> cleaned data -> reproducible chart spec/code -> SVG/vector output -> design refinement -> value/geometry reconciliation`

SVG/vector refinement may improve hierarchy, typography, annotation, grouping and composition, but must not silently change values, axes, topology, geometry meaning or evidence state. Reconcile the refined vector against the cleaned data/spec before release.

For formal SVG delivery, use the Semantic SVG Contract in §7.2: stable semantic groups/IDs, editable text, data-role or equivalent object roles, and a deterministic regeneration record where material. PNG is normally a review/readback preview, not a substitute for the editable SVG source.

Use browser-local or offline processing for sensitive data where practical; do not require server upload merely to obtain a polished vector artifact.

## 11. Export

Export as required:

- SVG for Illustrator / Inkscape / editable board use; for formal vector delivery, preserve semantic groups/IDs and editable text under §7.2;
- PNG at explicit pixel dimensions for actual-preview review; PNG does not replace the formal SVG unless the medium explicitly requires raster;
- HTML for interaction;
- MP4/WebM/GIF only when motion adds meaning;
- XLSX with source/clean/data-dictionary sheets when a table is part of delivery.

Preserve stable IDs, relative paths, source note, version and intended dimensions.

## 12. Required Output

Return or persist, as applicable:

1. visualization artifact;
2. editable source;
3. cleaned dataset;
4. data dictionary;
5. transformation note;
6. source / evidence note;
7. Visual Contract / current Chart Spec instance;
8. analytical grammar/spec;
9. semantic SVG structure note when SVG editability is material;
10. semantic entity companion when narrative/data linking is material;
11. statement of what the visual supports and does not prove;
12. actual-preview self-check under the declared reading mode;
13. strongest-existing benchmark reference when one exists;
14. independent review status.

## 13. Quality Checks

### Data / analytical

- Reconcile displayed values with the cleaned table.
- Check units, denominators, missing values, duplicates, ranges and formulas.
- Avoid truncated axes unless clearly justified.
- Validate map CRS / projection / NoData where applicable.
- Confirm data-to-artifact consistency.
- For graphs, verify stable node IDs, edge endpoints and topology independently of layout.
- For narrative entities, reconcile display text with raw value/unit/source/evidence state.

### Design / visual

- First-read claim is visible in the artifact itself under the intended reading mode.
- Primary / secondary / evidence / metadata hierarchy is unequal and intentional.
- Position/size/whitespace establish hierarchy before color carries it.
- One grid governs the surface; alignments are exact or deliberately broken.
- Lineweight and marker semantics survive grayscale.
- Labels do not collide with data or each other at intended size.
- Composition is not a dashboard/card wall unless the actual task is operational monitoring.
- Annotation density is controlled.
- Project specificity does not depend mainly on title text.
- Return/fallback is visually legible when it is part of the design claim.
- Source-traced vs placeholder geometry is unambiguous.
- Structural devices encode real information rather than decoration.
- A computational graph layout does not imply unsupported position/order/distance.
- Template selection matches the true information structure.
- A chart library/renderer owns declared grammar/layout/geometry responsibilities only; it does not substitute for editorial design judgment.
- Candidate does not regress against the strongest mature existing design.

### Accessibility / output

- Check color-blind legibility and grayscale hierarchy.
- Provide text/data equivalent for interactive or high-density graphics.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For formal SVG, verify stable semantic groups/IDs and editable text or record any justified outline substitution.
- Reopen the final export before recording status.

## 14. Diagnostic Review Lenses

For review, record findings by severity (`Critical / Major / Minor / Enhancement`) and inspect at least:

- Visual hierarchy and first-read;
- consistency/system coherence;
- accessibility and redundant semantics;
- task usability / interpretation cost;
- responsive/intended-size behavior;
- performance/export cost where relevant.

These are diagnostic lenses only. A high average score cannot override an OLEANDER hard veto, truth failure, or independent-review requirement.

## 15. Regression Discipline

After any material change to this skill:

1. rerun broad data/truth/accessibility cases;
2. rerun targeted visual regressions tied to the discovered failure mode;
3. keep renderer-syntax/API tests separate from visual-design tests;
4. compare against the strongest existing artifact where relevant;
5. do not promote a skill revision merely because code-generation or retrieval tests improved.

Targeted regressions should include, when applicable: equal-weight network, relation falsely converted to sequence, card-wall evidence diagram, cleaner-but-weaker redesign, unsupported geographic layout, renderer-valid-but-visually-generic output, narrative entity provenance loss, vector-refinement data drift, unjustified fixed read-time thresholds, anonymous-path-cloud falsely claimed as semantic SVG, and automatic layout moving task-critical spatial anchors.

## 16. Verdict

Producer status is limited to:

`EXECUTED / SELF-CHECKED / REVIEW PENDING / REVISE / REJECT`.

KEEP-class promotion requires independent visual/design readback under the current OLEANDER governance and regression-evaluation rules.
