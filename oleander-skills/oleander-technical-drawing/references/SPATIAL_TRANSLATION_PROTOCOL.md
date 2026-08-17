# OLEANDER Technical Drawing — Spatial Translation Protocol

Status: `candidate extension / PR #172`

Use this protocol whenever a technical, spatial-analysis, landscape, circulation, node, section or diagram drawing turns a real/project spatial condition into simplified graphic geometry.

This protocol exists to prevent a common failure:

> the producer correctly names a phenomenon, but then draws an arbitrary line, dot, arrow or blob that is only visually suggestive of that phenomenon.

Knowing **what** an object is does not prove that its drawing is a valid representation of that object.

`SEMANTIC IDENTIFICATION != SPATIAL TRANSLATION`

`SPATIAL TRANSLATION != VISUAL STYLING`

`KNOWN MEANING != VALID GEOMETRY`

`NAMED PATH != DRAW ANY PATH LINE`

`NAMED NODE != PLACE ANY DOT`

`NAMED FIELD != DRAW ANY BLOB`

`GRAPHIC SIMPLIFICATION != PERMISSION TO INVENT SPATIAL RELATION`

## 1. Mandatory five-stage translation chain

Before a decision-relevant graphic carrier is drawn, record the full chain:

`SOURCE / PHENOMENON → SPATIAL MODEL → GEOMETRIC ABSTRACTION → GRAPHIC CARRIER → VISUAL ENCODING`

A drawing may simplify at stages 3–5. It may not skip stages 1–2.

### Stage 1 — SOURCE / PHENOMENON

What actually exists, is observed, is documented, is derived, or is deliberately proposed?

Examples:
- mapped river body;
- survey contour;
- official path network;
- observed desire line;
- known transfer between cable station and walking route;
- source-grounded viewpoint area;
- inferred drainage direction from a DEM;
- design-proposed rest zone;
- unknown threshold whose existence is known but exact limits are not.

Required fields:
- source/object ID;
- source revision/date;
- truth state: `SOURCE / OBSERVED / DERIVED / INFERENCE / ASSUMPTION / DECISION / UNKNOWN`;
- what the source actually proves;
- what it does not prove.

### Stage 2 — SPATIAL MODEL

Translate the phenomenon into its real spatial structure before deciding its graphic shape.

Ask:
- Is it a **surface**, **volume**, **corridor**, **centerline**, **edge**, **boundary**, **network**, **point event**, **threshold zone**, **view relation**, **catchment**, **patch**, **gradient**, or **sequence**?
- Does it have width/extent, or is a line genuinely the correct spatial model?
- Is its topology known?
- Is its position known?
- Is its orientation known?
- Does it connect to other objects?
- Is it continuous, intermittent, seasonal, optional or state-dependent?

Examples:
- a pedestrian path is normally a **traversable corridor/surface**; a centerline is a later abstraction;
- a river is normally a **water body/edge pair**, not automatically a centerline;
- an ecological corridor is usually a **band/patch continuity relation**, not automatically a thin green line;
- a junction is a **topological connection event**, not a dot;
- a viewpoint is a **viewer position/zone + orientation + visibility relation + target**, not an eye icon;
- a threshold is often a **transition band/zone**, not a point;
- a watershed is a **separating boundary**, while surface flow is a **transport relation**.

If the spatial model cannot be stated, drawing must stop.

### Stage 3 — GEOMETRIC ABSTRACTION

Choose a geometry that is appropriate to the spatial model and evidence level.

Allowed abstraction families include:
- `TRACE` — source geometry is directly traced/reused within the declared accuracy;
- `DERIVE` — geometry is computed from source data/model by a declared method;
- `GENERALIZE` — source geometry is simplified while preserving declared invariants;
- `SCHEMATIZE` — topology/sequence/relationship is intentionally unfolded or regularized; map accuracy is not claimed;
- `INFER` — bounded geometry expresses a reasoned but unverified condition;
- `DESIGN` — geometry is a proposed design response rather than an observed/source condition.

Every abstraction must declare its **registration class**:
- `MAP_BOUND` — intended to retain source location/orientation on the base;
- `BASE_RELATION_BOUND` — tied to a source object/corridor but not exact geometry;
- `TOPOLOGY_BOUND` — preserves connectivity/order but not map position;
- `SEQUENCE_BOUND` — preserves experiential/operational order only;
- `DIAGRAM_ONLY` — explanatory relation with no spatial registration claim.

Hard rule:

> `SCHEMATIZE / TOPOLOGY_BOUND / SEQUENCE_BOUND / DIAGRAM_ONLY` geometry must not be visually presented as if it were a map-accurate trace on the source base.

If schematic geometry is overlaid on a map-like base, its distortion and non-registration must be unmistakable.

## 2. Spatial invariants — decide what must survive simplification

Before simplifying geometry, record which invariants are preserved.

Possible invariants:
- `TOPOLOGY` — edge/node connectivity, branch/merge, containment;
- `ADJACENCY` — what touches or is next to what;
- `ORDER` — sequence along a route/process;
- `DIRECTION` — directional relation;
- `ORIENTATION` — alignment relative to north/river/slope/object;
- `POSITION` — location on the source base;
- `EXTENT` — spatial footprint or reach;
- `WIDTH / BANDNESS` — whether the phenomenon occupies a corridor rather than a centerline;
- `BOUNDARY TYPE` — hard edge, soft edge, uncertain transition, open continuation;
- `RELATIVE SCALE` — relative magnitude/width/spacing when decision-relevant;
- `ELEVATION / LEVEL RELATION`;
- `VISIBILITY / OCCLUSION`;
- `ACCESS / TRAVERSABILITY`;
- `STATE / SEASONALITY`.

A generalization is invalid if it destroys an invariant that carries the analytical claim.

Example:
- simplifying a trail curve may be acceptable if topology, junction locations and base corridor remain correct;
- moving the junction to make the composition cleaner is not acceptable when the junction itself is the analysis;
- collapsing a wide floodplain into a thin blue line is invalid when flood extent is the claim;
- drawing a precise view ray is invalid if only a broad observation zone is known.

## 3. GRAPHIC CARRIER — choose a carrier that matches the spatial model

Only after stages 1–3 may a graphic carrier be selected.

Typical translation choices:

### A. Surface / field → polygon, band, gradient or patterned field
Use for:
- water body;
- flood/retention extent;
- habitat patch;
- canopy/meadow/plant community;
- activity/rest field;
- slope band;
- visibility field;
- threshold zone;
- uncertainty envelope.

Do not reduce a field to a centerline merely because lines are visually cleaner.

### B. Corridor / traversable surface → band or edge pair; centerline only as an explicit abstraction
For a path, road, trail, cable corridor, drainage swale or ecological link:
- if width/edge matters, draw band/edges;
- if only topology is known, centerline may be used but must be labeled `CENTERLINE / TOPOLOGY ABSTRACT`;
- if only order is known, use a sequence diagram rather than pretending to map the route.

### C. Boundary / divide → boundary line
Use for:
- parcel/site edge;
- watershed divide;
- vegetation edge;
- water edge;
- management boundary;
- hard barrier;
- uncertain/soft transition with corresponding soft/uncertain graphic treatment.

A boundary is not a movement line.

### D. Point event → point only when the event is genuinely point-like
Use for:
- inlet/outlet device;
- surveyed marker;
- singular control point;
- small service object;
- exact junction after topology is already encoded by connected edges.

Do not use a point to substitute for a spatially extended rest area, threshold or observation field.

### E. Network event → connected geometry first, symbol second
A junction/branch/merge/transfer is proven by:
- connected edges/corridors;
- ownership and connectivity;
- mode/state transition when relevant.

The dot/icon is optional secondary encoding.

### F. View relation → viewer + orientation + target/field + occlusion state
Valid carriers may include:
- view cone/sector;
- view corridor;
- target envelope;
- screened/opened field;
- section/profile when vertical occlusion matters.

A single arrow from a point to a label is not enough when the claim concerns a real view.

### G. Threshold / compression / release → transition band, sequence or section
Use plan only if plan geometry actually proves the transition.
Use section/profile when body-ground/edge/enclosure relation is the real mechanism.

## 4. VISUAL ENCODING — style comes last

Stroke, color, opacity, hatch, symbol, arrowhead, label and icon are **visual encodings**, not spatial definitions.

Do not use styling to create a relation that the geometry has not earned.

Examples:
- a thick red line does not make an invented polyline a primary route;
- a blue arrow does not make an arbitrary vector a drainage path;
- a green dashed line does not make a path an ecological corridor;
- a large node symbol does not make a content point a route junction;
- a view icon does not make a location a viewpoint;
- a gradient does not make an area a microclimate field without a spatial model and basis.

## 5. Required `SPATIAL_TRANSLATION_REGISTER`

For each decision-relevant line, node, field or symbol create a register entry with:

- `id`
- `system`
- `semantic_class`
- `source_refs`
- `truth_state`
- `source_proves`
- `source_does_not_prove`
- `spatial_model`
- `translation_mode`: `TRACE | DERIVE | GENERALIZE | SCHEMATIZE | INFER | DESIGN`
- `registration_class`: `MAP_BOUND | BASE_RELATION_BOUND | TOPOLOGY_BOUND | SEQUENCE_BOUND | DIAGRAM_ONLY`
- `preserved_invariants`
- `relaxed_invariants`
- `geometry_type`: `POINT | LINE | CENTERLINE | EDGE_PAIR | BAND | POLYGON | FIELD | NETWORK | SECTION | VECTOR | SYMBOL_ONLY`
- `owner_base_object`
- `connected_object_ids`
- `derivation_method`
- `uncertainty_or_tolerance`
- `graphic_carrier_id`
- `visual_encoding_class`
- `does_not_prove`

No decision-relevant carrier is complete merely because `semantic_class` is known.

## 6. Translation-state ladder

Use a separate translation claim from pixel fidelity, design quality and field truth.

### `ST-C0 / SEMANTIC IDENTIFIED`
The phenomenon/object is named and source-bound.

### `ST-C1 / SPATIAL MODEL RESOLVED`
Its real spatial structure is defined: field/corridor/boundary/network/node/threshold/view/etc.

### `ST-C2 / GEOMETRIC TRANSLATION RESOLVED`
A source-compatible abstraction is chosen; registration class and preserved/relaxed invariants are explicit.

### `ST-C3 / GRAPHIC CARRIER VALIDATED`
The vector carrier actually expresses that abstraction without inventing conflicting spatial relations; labels/style are secondary.

`ST-C3 != DESIGN KEEP != FIELD PASS != RF-C3`.

## 7. Stop rules

Stop drawing and return to source/spatial modelling when any of these occur:

1. the producer can name the object but cannot state its spatial model;
2. the source proves topology only, but the drawing invents map position/curvature;
3. the source proves a broad field, but the drawing invents a precise boundary;
4. a corridor is reduced to a line even though width/edge is decision-critical;
5. a viewpoint is drawn with a ray even though viewer position or target is uncertain;
6. a junction dot is placed without actual connected edges;
7. an ecological corridor is drawn as a line with no patch/edge/continuity basis;
8. a route is moved to improve composition while still appearing map-bound;
9. a schematic sequence is overlaid on a map without declaring non-registration;
10. the graphic carrier cannot be backtracked to source or derivation.

These are not aesthetic problems. They are translation failures.

## 8. Landscape-specific translation examples

### River / water body
If mapped banks are available:
`SOURCE BANKS → WATER SURFACE MODEL → TRACE/GENERALIZE POLYGON → WATER FIELD`.

If only river topology is known:
`SOURCE RELATION → CORRIDOR MODEL → TOPOLOGY_BOUND SCHEMATIC BAND`.
Do not draw a precise centerline or shoreline on a map-like base.

### Trail / visitor route
If path geometry is known:
`PATH SOURCE → TRAVERSABLE CORRIDOR → TRACE/GENERALIZE → PATH BAND/CENTERLINE`.

If only node order/network topology is known:
`ROUTE ORDER/GRAPH → NETWORK MODEL → SCHEMATIZE / TOPOLOGY_BOUND → UNFOLDED NETWORK`.
Do not invent bends and overlay them as geographic route geometry.

### Observation point
If viewpoint and target are known:
`VIEWER + TARGET + OCCLUSION SOURCE → VIEW RELATION → DERIVE/GENERALIZE → VIEW CONE/CORRIDOR`.

If only a broad observation area is known:
`OBSERVATION ZONE → VIEW OPPORTUNITY FIELD → INFER/BASE_RELATION_BOUND → SOFT VIEW FIELD`.
Do not draw a precise ray to a guessed target.

### R13-type compression threshold
If exact walls/edges are field-open:
`KNOWN EXPERIENCE EVENT → THRESHOLD MODEL → SCHEMATIZE/SEQUENCE_BOUND OR SECTION STUDY → TRANSITION BAND/SEQUENCE`.
Do not draw an invented narrow polygon on the plan as if it were measured geometry.

### Ecological corridor
If habitat patches and connectivity are supported:
`PATCHES + EDGE/GAP → CONTINUITY MODEL → DERIVE/GENERALIZE → BAND/FIELD CONNECTION`.
Do not use a single green line unless the ecological feature itself is genuinely linear.

## 9. Review test — translation before aesthetics

For every major carrier ask in order:

1. What source/project fact or design decision does it come from?
2. What is the real spatial ontology of that fact?
3. Why is this geometric abstraction appropriate?
4. Which spatial invariants are preserved?
5. Which invariants are intentionally relaxed?
6. Is it map-bound, topology-bound, sequence-bound or diagram-only?
7. Could a reviewer reconstruct the derivation without guessing?
8. If text, icons and color are hidden, does the geometry still express the intended relation?
9. Does the carrier imply more precision or truth than the source supports?
10. Would moving/reshaping the carrier for composition change the underlying claim?

Any critical `no` means `REVISE` before visual refinement.

## 10. Hard blockers

Automatic `REVISE / HOLD`:

- freehand/eyeballed analysis line with no source geometry or declared derivation;
- arbitrary route curvature added only to make the composition dynamic;
- arbitrary node placement because a label needs an anchor;
- arbitrary field blob used because a concept is spatially vague;
- topological information drawn as pseudo-geographic geometry;
- map-derived information redrawn with materially changed adjacency/branching/orientation;
- schematic geometry presented without registration disclosure;
- point/line/field carrier selected for visual convenience rather than spatial ontology;
- visual hierarchy praised while translation remains unverified;
- producer calls a carrier “conceptual” after it has already been drawn in a map-accurate visual register;
- labels and icons are the only reason a relation is understandable.

Producer may self-check the translation register but cannot self-award `KEEP`, `PROFESSIONAL FINISH`, `FIELD PASS` or Promotion.
