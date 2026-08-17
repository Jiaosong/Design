# OLEANDER Technical Drawing — Analysis Drawing System

Status: `v0.2 / companion to oleander-technical-drawing v0.2 candidate`

Analysis drawings are design-reasoning drawings. They explain **spatial conditions, relations, constraints, sequences, alternatives and consequences** using editable geometry and explicit truth states. They are not decorative infographics and they do not replace quantitative data visualization.

The visual hierarchy follows `GRAPHIC_SYSTEM.md` and `VISUAL_HIERARCHY_TRANSFER.md`: one dominant claim, position/area/whitespace before color, controlled annotation rails, and 3-second → 30-second → near-read sequencing.

## 1. Routing boundary

Use this module when the primary object is a spatial/design relationship:

- circulation, route hierarchy, return logic;
- visibility, view cone, enclosure/openness, compression/release;
- slope/grade bands, edge conditions, drainage direction;
- program adjacency, access, maintenance or conflict zones;
- existing/proposed/inferred/unknown spatial states;
- evidence → spatial finding → design consequence reasoning;
- scenario overlays where geometry, not statistical magnitude, is the primary carrier;
- sequence, system, interface and dependency diagrams tied to design geometry.

When circulation / mobility / route direction is the principal analytical carrier, also load `FLOW_DIRECTION_ANALYSIS.md`. A route network must be reconstructed as edges/nodes/direction markers bound to the base, not simplified into decorative arrows.

Route to `oleander-data-viz` when the primary object is quantitative data:

- distributions, counts, rates, time series, uncertainty intervals;
- statistical comparison or correlation;
- dashboards, KPI charts, Sankey/flow quantities;
- data tables where denominator/unit/missingness are the main truth problem.

A project may use both. Do not collapse them into one graphic simply for visual consistency.

## 2. Analysis truth-state grammar

Every analysis layer must declare one of:

- `SOURCE / OBSERVED` — directly supported by current authority;
- `DERIVED` — calculated from source geometry/data with method known;
- `EVIDENCE-BOUND` — supported by a bounded source but not fully field-verified;
- `INFERENCE` — reasoned interpretation from evidence;
- `ASSUMPTION` — provisional condition introduced to continue design;
- `CONSTRAINT / UNKNOWN` — known limit or unresolved state;
- `DECISION` — design response chosen by the project;
- `REJECTED / SUPERSEDED` — preserved for provenance but not current.

Do not encode these states with color alone. Use line/fill/dash/ID/label redundancy.

### Visual authority must not invert evidential authority
A `DECISION` may become the visually dominant conclusion because the drawing explains a design response, but its styling must not make it appear more *factual* than its evidence permits. Use hierarchy for reading order; use line/pattern/labels for truth state.

## 3. Required analysis sequence

A serious analysis diagram should answer:

`WHAT IS THE BASE → WHAT IS OBSERVED → WHAT IS DERIVED/INFERRED → WHAT CONSTRAINT EMERGES → WHAT DESIGN CONSEQUENCE FOLLOWS → WHAT REMAINS OPEN`.

If the conclusion cannot point back to a source/evidence layer, it is not analysis; it is an unsupported assertion.

## 4. Visual hierarchy contract

Before drawing, define:

- `PRIMARY_CLAIM` — the single spatial/design conclusion the figure exists to explain;
- `SOURCE_BASE` — geometry that must remain recoverable and undistorted;
- `SIGNATURE` — one meaningful relation allowed to receive exceptional emphasis;
- `ANNOTATION_RAIL` — legend, IDs, qualifiers and source notes;
- `3S_READ` — base + dominant relation/decision;
- `30S_READ` — evidence/inference/constraint logic;
- `NEAR_READ` — provenance, state, open items and method.

### Channel priority

Use:

`POSITION → AREA / SCALE → PROXIMITY → STROKE / PATTERN → TONE → COLOR`.

Do not use saturated color to compensate for a weak spatial composition.

### Contrast allocation

A normal analysis plan should visually behave approximately as:

1. primary claim / decision-critical relation — strongest;
2. source spine / principal evidence — clearly legible;
3. inference / constraint — distinct but subordinate;
4. context — quiet;
5. provenance / metadata — readable at near read.

This is perceptual hierarchy, not evidence hierarchy.

## 5. Spatial analysis plan grammar

Recommended layer order:

1. `BASE / SOURCE GEOMETRY`
2. `PRIMARY SPATIAL RELATION`
3. `EVIDENCE OVERLAY`
4. `INFERENCE / CONSTRAINT`
5. `DESIGN DECISION`
6. `TRUTH-STATE LEGEND`
7. `ANALYSIS CONCLUSION`

Keep the base quieter than the analytical claim but still recoverable. An overlay must not distort or redraw the authoritative base geometry to make the conclusion look stronger.

### Composition

Prefer an asymmetric analytical composition over equal panels when one relationship is primary:

`DOMINANT SPATIAL FIELD + NARROW ANNOTATION/LEGEND RAIL + QUIET FOOTER`.

- the spatial field should own most of the perceptual area;
- legends and explanatory conclusions align to the same rail when possible;
- labels stay near the geometry they describe or land on a common annotation edge;
- avoid floating rectangles for every fact;
- do not turn evidence, inference, constraint and decision into four equal cards.

### Source base discipline

The source base should be quiet, not invisible. It must remain possible to inspect whether the analysis overlay respects the source.

If the source needs to become visually louder for one local comparison, use a controlled highlight rather than redrawing its geometry.

## 6. Evidence → Spatial Finding → Design Consequence grammar

Use stable IDs:

- `E-##` evidence;
- `F-##` spatial finding;
- `D-##` design consequence.

Each `F-##` must cite at least one evidence ID. Each `D-##` must cite at least one finding ID. Unknowns and assumptions stay visible inside the chain.

Bad pattern:

`pretty source image → bold conclusion → design claim`

Required pattern:

`EVIDENCE ID → bounded interpretation → spatial finding → design response → open verification item`.

### Avoid the equal-card trap

A three-column E/F/D logic does not require nine equal boxes. Hierarchy may be created by:
- one dominant row/claim and quieter supporting rows;
- shared alignment rails rather than boxed cards;
- direct E→F→D traces;
- scale/weight differences tied to importance;
- more whitespace around the dominant chain.

Equal rectangles are acceptable only when the cases are genuinely parallel and equal in decision importance.

## 7. 3-second / 30-second / near-read

### 3 seconds
The viewer should understand:
- the main spatial object/base;
- the dominant conflict/opportunity/relation;
- the design consequence or question.

### 30 seconds
The viewer should be able to trace:
- evidence → finding → decision;
- source vs inference vs constraint;
- the principal decision point or spatial zone.

### Near read
The viewer should recover:
- source IDs;
- qualifiers/confidence/basis;
- unknown/open conditions;
- exact E/F/D traceability;
- does-not-prove boundary.

Do not make the title carry a conclusion the geometry cannot show.

## 8. Annotation and legend rail

Legends are supporting navigation, not a second hero.

- align state keys, conclusion text and provenance to one controlled rail where possible;
- use direct labels on important overlays to reduce eye travel;
- keep state semantics redundant in line/fill/dash/ID;
- use a compact legend to decode the system, not repeat every label;
- place long source notes in near-read metadata space;
- avoid oversized status blocks and repeated pills.

## 9. One-signature rule for analysis

One relationship may receive exceptional emphasis when it is the actual analytical insight:
- junction / bottleneck;
- return spine;
- view cone;
- conflict edge;
- drainage path;
- Evidence→Finding→Decision trace.

Do not also create a competing hero title, giant legend, bright background field and multiple accent colors. One signature; the rest supports it.

## 10. Editable-vector requirement

Core analysis geometry, arrows, labels, legends, IDs and explanatory text remain vector. Raster map/photo/image layers may support context but cannot contain the only copy of a critical label, route, boundary or conclusion.

Use stable `<g id="...">` groups or equivalent named CAD/vector layers so the analysis can be reconstructed and regression-tested.

Visual-hierarchy candidates should expose:
- `HIERARCHY_FRAME`
- `PRIMARY_CLAIM`
- `ANNOTATION_RAIL`

in addition to domain-specific groups.

## 11. Analysis-specific blockers

Automatic `REVISE / HOLD` triggers:

- conclusion has no traceable evidence/finding path;
- source and inference use indistinguishable visual semantics;
- unknown is silently drawn as confirmed;
- analysis overlay modifies source geometry without a design-revision record;
- decorative arrows or gradients obscure the actual relation;
- circulation is simplified to generic polylines/arrowheads that no longer preserve route topology, base binding, branch/merge structure or mode/state relations;
- direction markers are visually oversized, detached from route tangency, or used as decoration rather than route events;
- diagram becomes a generic method card with no project/spatial object;
- statistical magnitude is encoded without data-viz truth controls;
- analysis is technically correct but first-read is visually flat/noisy;
- decision appears more authoritative than the evidence allows;
- equal cards/panels create false equality among unequal evidence or decisions;
- legend/metadata visually dominates the spatial field;
- color carries the only distinction among source/evidence/inference/decision;
- multiple signatures compete for first-read.

## 12. Diagnostic-to-repair loop

Use:

`3S READ → 30S TRACE → NEAR-READ PROVENANCE → MISMATCH → CAUSE → ONE MATERIAL REPAIR → REOPEN`.

Typical repairs:
- source disappears → increase source legibility slightly; do not reduce overlay truth labels;
- inference looks factual → change pattern/ID/label while keeping readable weight;
- four overlays compete → identify the actual claim, demote support overlays and create one signature;
- legend reads first → narrow/quiet annotation rail and enlarge spatial field;
- E/F/D reads as admin cards → remove equal boxes, strengthen directional traces and row hierarchy;
- circulation looks like four decorative zigzags → rebuild route edge/node topology from the source/base before changing stroke/color;
- arrowheads look like icons → restore route-bound marker position, tangency and marker-to-line scale before adjusting aesthetics;
- conclusion only exists in prose → move the claim back into spatial geometry/relationship.

## 13. Golden fixture coverage

The current fixture suite includes:

- `GD-05_SPATIAL_ANALYSIS_PLAN.svg` — dominant spatial field + base geometry + evidence/inference/decision + annotation rail;
- `GD-06_EVIDENCE_SPATIAL_CONSEQUENCE.svg` — traceable E→F→D reasoning with unequal row hierarchy rather than a card wall.

These are calibration assets with locked training geometry. They are not site evidence and do not prove a real project condition.

## 14. Flow/circulation specialization

For circulation, mobility, route hierarchy, pedestrian/bicycle/service movement or directional sequence, load `FLOW_DIRECTION_ANALYSIS.md`.

The key distinction is:

`ANALYSIS CLAIM → NETWORK TOPOLOGY → ROUTE-TO-BASE BINDING → DIRECTION / STATE / MODE → GRAPHIC HIERARCHY`.

Do not start from `choose a color → draw arrows`.
