# OLEANDER Technical Drawing — Analysis Drawing System

Status: `v0.1 / companion to oleander-technical-drawing v0.2 candidate`

Analysis drawings are design-reasoning drawings. They explain **spatial conditions, relations, constraints, sequences, alternatives and consequences** using editable geometry and explicit truth states. They are not decorative infographics and they do not replace quantitative data visualization.

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

## 3. Required analysis sequence

A serious analysis diagram should answer:

`WHAT IS THE BASE → WHAT IS OBSERVED → WHAT IS DERIVED/INFERRED → WHAT CONSTRAINT EMERGES → WHAT DESIGN CONSEQUENCE FOLLOWS → WHAT REMAINS OPEN`.

If the conclusion cannot point back to a source/evidence layer, it is not analysis; it is an unsupported assertion.

## 4. Spatial analysis plan grammar

Recommended layer order:

1. `BASE / SOURCE GEOMETRY`
2. `PRIMARY SPATIAL RELATION`
3. `EVIDENCE OVERLAY`
4. `INFERENCE / CONSTRAINT`
5. `DESIGN DECISION`
6. `TRUTH-STATE LEGEND`
7. `ANALYSIS CONCLUSION`

Keep the base quieter than the analytical claim but still recoverable. An overlay must not distort or redraw the authoritative base geometry to make the conclusion look stronger.

## 5. Evidence → Spatial Finding → Design Consequence grammar

Use stable IDs:

- `E-##` evidence;
- `F-##` spatial finding;
- `D-##` design consequence.

Each `F-##` must cite at least one evidence ID. Each `D-##` must cite at least one finding ID. Unknowns and assumptions stay visible inside the chain.

Bad pattern:

`pretty source image → bold conclusion → design claim`

Required pattern:

`EVIDENCE ID → bounded interpretation → spatial finding → design response → open verification item`.

## 6. Composition and reading hierarchy

Analysis drawings are reviewed at three scales:

- **distance / thumbnail** — the spatial question and dominant relation are clear;
- **intended size** — source, inference and decision remain distinguishable;
- **near read** — IDs, qualifiers, source notes and open items are legible.

Do not use equal visual weight for all arrows, zones and labels. One diagram should have one main analytical claim.

## 7. Editable-vector requirement

Core analysis geometry, arrows, labels, legends, IDs and explanatory text remain vector. Raster map/photo/image layers may support context but cannot contain the only copy of a critical label, route, boundary or conclusion.

Use stable `<g id="...">` groups or equivalent named CAD/vector layers so the analysis can be reconstructed and regression-tested.

## 8. Analysis-specific blockers

Automatic `REVISE / HOLD` triggers:

- conclusion has no traceable evidence/finding path;
- source and inference use indistinguishable visual semantics;
- unknown is silently drawn as confirmed;
- analysis overlay modifies source geometry without a design-revision record;
- decorative arrows or gradients obscure the actual relation;
- diagram becomes a generic method card with no project/spatial object;
- statistical magnitude is encoded without data-viz truth controls;
- analysis is technically correct but first-read is visually flat/noisy;
- decision appears more authoritative than the evidence allows.

## 9. Golden fixture coverage

The current fixture suite includes:

- `GD-05_SPATIAL_ANALYSIS_PLAN.svg` — base geometry + evidence overlays + inference + decision + state legend;
- `GD-06_EVIDENCE_SPATIAL_CONSEQUENCE.svg` — traceable E→F→D reasoning chain.

These are calibration assets with locked training geometry. They are not site evidence and do not prove a real project condition.
