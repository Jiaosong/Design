# OLEANDER Data Viz — Routing and Renderer Adapters v0.1

Date: 2026-08-17  
Status: companion to `SKILL.md`; renderer routing only  
Authority: does not override OLEANDER Current Authority, Source Authority, truth boundaries, design review or independent verdict policy.

## Purpose

Separate three concerns that external visualization skill repositories often mix:

1. design/truth policy;
2. intent/form routing;
3. renderer/version syntax.

The core design policy lives in `SKILL.md`. This file helps choose the renderer family and defines what a renderer can and cannot prove.

`RENDERER VALID != VISUALIZATION VALID != DESIGN KEEP`

## Routing sequence

Route every task through these questions in order:

### A. What is the information structure?

- comparison / ranking
- time / ordered trend
- distribution
- numeric relationship
- part-to-whole
- hierarchy
- relation / topology
- strict sequence / dependency / timeline
- geographic / geospatial
- evidence -> inference -> decision
- narrative interpretation / semantic text
- mixed editorial composition

Do not select a renderer before this classification.

### B. What is authoritative?

- raw values only;
- topology only;
- coordinates / CRS;
- time order;
- parent-child structure;
- scenario / estimate / simulation;
- observed / measured;
- source-grounded relation;
- unknown / field-open.

The renderer must not manufacture an unsupported authority dimension.

### C. What is the minimum renderer capable of expressing the claim?

Prefer the highest-level deterministic system that preserves the claim without loss.

## Renderer families

### 1. Declarative statistical grammar

Examples: Observable Plot, Vega-Lite, AntV G2, Altair, Plotly for conventional charts.

Use for:
- bar / dot / line / area;
- scatter;
- distribution;
- layered analytical marks;
- faceting / small multiples;
- common interactive filtering/highlighting.

Required contract:
- data;
- transforms;
- marks;
- encoding channels;
- scales;
- layers/facets;
- interaction;
- annotations.

Do not escalate to D3 merely because custom code looks more advanced.

### 2. Graph / topology engine

Examples: AntV G6, NetworkX + SVG, D3 graph layouts.

Use only when nodes/edges/topology are the analytical object.

Required data:
- stable node IDs;
- explicit edge source/target;
- node role;
- edge role;
- evidence state;
- layout state: `authoritative | deterministic-diagrammatic | computational-layout`.

Renderer/layout rules:
- `force` is a computational layout, not evidence of distance or geography;
- `dagre` can communicate flow/dependency only if direction is real;
- radial/circular/grid positions are presentation unless explicitly data-driven;
- drag/zoom/select/collapse are behaviors, not evidence;
- topology must survive renderer changes.

When used on boards, prefer deterministic positions after exploration and preserve topology separately.

### 3. Infographic / information-structure renderer

Examples: AntV Infographic or custom SVG editorial diagram.

Use when information is primarily explanatory rather than quantitatively analytical.

Structure classifier:
- `list` = genuinely parallel items;
- `sequence` = real order/dependency/time;
- `compare` = explicit comparative dimensions;
- `hierarchy` = true parent-child/containment;
- `relation` = non-sequential relation/topology;
- `chart` = quantitative encoding;
- `mixed` = custom editorial composition when one template would distort meaning.

Hard guard:

`INFORMATION STRUCTURE -> VISUAL FORM -> TEMPLATE`

Never:
- convert relation into sequence for visual neatness;
- convert uncertainty into a completed roadmap;
- convert causal evidence into equal cards;
- use a decorative template as proof of structure.

Template presets are starting renderers, not final professional design.

### 4. Editable vector bridge

Examples: RAWGraphs -> SVG -> Illustrator/Inkscape; declarative chart -> SVG -> manual design refinement.

Use when:
- the analytical grammar is already correct;
- board/page typography and annotation need professional refinement;
- vector editability is required.

Preserve:
`raw -> clean -> spec -> SVG -> refined SVG -> reconciliation`

Manual refinement may change typography, grouping, annotation and composition. It may not silently change values, scale, topology, evidence state, route relation or meaning.

### 5. Custom D3 / low-level web graphics

Use only when a high-level grammar cannot express a material requirement:
- unusual mark geometry;
- bespoke interaction;
- custom layout;
- controlled analytical motion;
- non-standard compositing.

Additional burden:
- accessibility equivalent;
- responsive verification;
- deterministic data binding;
- regression testing;
- explicit scales/transforms;
- actual export/readback.

Low-level flexibility is not an aesthetic or analytical merit by itself.

### 6. Geographic stack

Examples: GeoPandas, QGIS, kepler.gl, MapLibre/deck.gl.

Use only when:
- coordinates are authoritative enough for the claim;
- CRS/projection is known or explicitly managed;
- geography is analytically material.

Required checks:
- CRS;
- units;
- projection;
- coordinate source;
- spatial transform;
- NoData / missing geometry;
- geographic vs schematic state.

A topology-only network must stay relational/diagrammatic even if a mapping engine could render it.

### 7. Narrative semantic text

Inspired by T8-style semantic entity annotation, but adapted to OLEANDER evidence states.

Use when prose is the primary reading mode and selected values/claims should remain machine-readable.

For each material entity preserve:
- `entity_id`;
- `display_text`;
- `entity_type`;
- `raw_value` when applicable;
- `unit`;
- `scope/time`;
- `source_ref`;
- `evidence_state`;
- `claim_role`;
- `assessment` only when justified;
- `detail` when needed for a mini-chart or relation;
- `does_not_prove`.

Do not use semantic highlighting to disguise weak evidence. Narrative text is an access layer, not a replacement for analytical evidence.

### 8. Raster visualization reconstruction

When the only source is an existing chart/infographic raster and the goal is an editable data-driven reconstruction, load `RASTER_TO_PARAMETRIC_RECONSTRUCTION.md`.

Route:

`REFERENCE SNAPSHOT -> ROI SEGMENTATION -> MARK-FAMILY DETECTION -> SOURCE_DATA.json -> VISUAL_ENCODING_SPEC.json -> PARAMETRIC GENERATOR -> EDITABLE SVG -> SAME-SIZE ROI READBACK -> SEMANTIC AUDIT -> DETERMINISTIC ROUNDTRIP`.

Required boundaries:

- measured pixel geometry is `REFERENCE_DERIVED_GEOMETRY`, not automatically original numeric data;
- inferred proxy values exist only to regenerate visible marks;
- unreadable labels/variables remain `UNREADABLE`;
- alluvial/network crossings require identity confidence rather than silent topology claims;
- skeleton/path fragments are not semantic layers until grouped and source meaning is bound;
- a repair that worsens the declared target ROI is rejected unless a necessary semantic/editability gain explicitly justifies the tradeoff;
- regenerating twice with zero diff proves determinism only, not reference fidelity or data truth.

Cross-skill rule:

`oleander-data-viz` owns data/encoding semantics. `oleander-technical-drawing` reconstruction modules may provide reference registration, path/geometry forensics and pixel/ROI evidence. `RF-C3 PIXEL MATCH != VR-C3 SEMANTIC DATA RECONSTRUCTION`.

## Renderer adapter rule

When a task explicitly uses a renderer/version, retrieve its current primary documentation or dedicated renderer skill and obey that syntax separately from OLEANDER design policy.

Examples derived from inspected external skills:
- AntV G2 v5: declarative Spec Mode and version-correct marks/encodes/transforms.
- AntV G6 v5: declarative `Graph` config with stable IDs/source/target and explicit layout/behaviors.
- AntV Infographic: structured DSL fields must match the chosen structural class.
- T8: semantic narrative annotations preserve raw values/metadata behind displayed prose.

Do not paste renderer-specific API documentation into the core OLEANDER design skill unless it changes design policy.

## Selection examples

### Example A — C04 route network

Authority: topology / cross-river relation / route-service-return roles; not survey coordinates.

Route:
`relation/topology -> graph/SVG relational diagram -> deterministic diagrammatic positions -> RELATIONAL / NTS / NOT GEOREFERENCED`

Not:
`kepler.gl map` or `force graph interpreted as geography`.

### Example B — capacity scenarios

Authority: scenario values with ranges, not field counts.

Route:
`comparison + uncertainty -> declarative chart grammar -> range/error/interval marks -> explicit SCENARIO state`

Not:
`single precise number rendered as measured fact`.

### Example C — Evidence -> Finding -> Consequence

Authority: directional reasoning, not time sequence.

Route:
`analytical relation -> custom editorial SVG / directional relation field`

Not:
`timeline/roadmap` unless chronology is actually part of the evidence.

### Example D — long research finding page

Authority: sourced values + interpretations + uncertainty.

Route:
`narrative text + semantic entity companion + linked figures`

Not:
`body copy containing untraceable numbers`.

## Review

A renderer can pass syntax/runtime checks while the artifact remains `REVISE` or `REJECT` for:
- weak first-read;
- wrong information structure;
- generic composition;
- layout implying unsupported facts;
- visual hierarchy failure;
- source/evidence loss;
- regression versus a stronger mature artifact.
