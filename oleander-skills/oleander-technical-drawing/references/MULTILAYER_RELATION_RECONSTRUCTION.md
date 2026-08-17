# OLEANDER Technical Drawing — Multilayer / Relationship Reconstruction

Status: `candidate extension / PR #172`

Use together with `REFERENCE_RECONSTRUCTION_FIDELITY.md` when the supplied reference is not one isolated drawing but a **stacked analytical diagram, exploded thematic atlas, multi-panel axonometric, or callout-heavy editorial technical figure**.

This extension was created after an actual reconstruction calibration exposed a critical failure mode: a candidate can become visually close, vector-shaped and same-canvas registered while the **relationships are not semantically reconstructed**.

`VECTOR PATHS != SEMANTIC EDITABILITY`

`LABEL PRESENT != RELATION DRAWN`

`PIXEL SIMILARITY != RELATIONSHIP FIDELITY`

## 1. Repeated-base genealogy

Before local tracing, determine whether several panels reuse one base geometry.

Create `BASE_GENEALOGY_REGISTER`:

- base object / site / assembly ID;
- panels that reuse it;
- transformation from master base to each panel;
- intentional omissions/fades;
- layer-specific overlays;
- vertical/exploded correspondence anchors.

If the same building/site/assembly appears in several analytical layers, reconstruct one shared master base whenever practical. Do not redraw each panel independently and allow silent drift.

### Blockers

- repeated base geometry drifts between panels;
- thematic overlay is aligned to a locally redrawn base rather than the shared authority;
- exploded vertical guide lines do not land on corresponding source objects;
- a panel crop or scale change is not recorded.

## 2. Relationship evidence register

Every analytical label or callout that claims a spatial/system relation must be classified.

For each relation record:

- `REL-ID`;
- source panel;
- claim/label;
- carrier type;
- source target(s);
- candidate target(s);
- topology;
- confidence/recoverability;
- state.

Allowed carrier types include:

- zone / filled field;
- route / path / network;
- arrow / vector direction;
- boundary / edge;
- leader + anchor;
- vertical/exploded correspondence line;
- node / point event;
- repeated symbol instance;
- adjacency / overlap / enclosure;
- sequence / before-after state.

Required state:

- `DRAWN` — relationship is recoverable from geometry without relying on prose;
- `PARTIAL` — some carrier geometry exists but target/topology is incomplete;
- `TEXT-ONLY` — statement is written but not graphically demonstrated;
- `UNRECOVERABLE` — source raster does not support reliable reconstruction.

A technical/analysis reconstruction with important `TEXT-ONLY` relations cannot pass relationship fidelity even if its global pixel error is low.

## 3. Semantic editability gate

A file is not professionally editable merely because it consists of SVG paths.

Distinguish:

1. `RASTER SUBSTITUTE` — embedded/reference pixels carry the actual drawing;
2. `PATH-CLOUD TRACE` — raster edges/glyphs are converted to many anonymous paths;
3. `STRUCTURED VECTOR` — geometry is separated into stable drawing groups;
4. `SEMANTIC VECTOR` — routes, zones, leaders, symbols, labels and repeated bases are reconstructable as meaningful editable objects.

Strict reconstruction requiring editability targets level 4 for in-scope technical/analytical relations.

Automatic tracing may support extraction, but a path-cloud trace is **evidence for visual recovery only**, not completion.

### Blockers

- text glyphs converted to anonymous paths when editable typography is required;
- one giant path cloud contains routes, buildings, symbols and leaders together;
- repeated icons are independently traced rather than represented as instances/components;
- route topology cannot be edited without selecting dozens/hundreds of unrelated paths;
- callout leader and its anchor/label cannot be traced as one relationship object.

## 4. Callout-network topology

Callouts in analytical diagrams are not decorative annotation.

Reconstruct:

`LABEL / SYMBOL → LEADER ROUTE → ELBOW(S) → ANCHOR → TARGET OBJECT / ZONE`.

Record leader topology when it is visually important:

- start and end anchor;
- elbow count and coordinates;
- horizontal/vertical/angled segment grammar;
- dot/ring/arrow terminator;
- target object ID;
- crossing/occlusion condition.

A leader that terminates near the correct area but not on the intended object is a relationship error, not a typography-only error.

## 5. Symbol family / icon dictionary

Dense professional diagrams often use a coherent icon family around the main drawing.

Create `SYMBOL_DICTIONARY` with:

- symbol ID;
- canonical component geometry;
- fill/stroke palette;
- scale range;
- orientation policy;
- label relationship;
- source confidence;
- instance coordinates.

Do not reconstruct every repeated icon as an unrelated bitmap trace. Shared symbol grammar is part of fidelity.

## 6. Foreground/base contrast register

In thematic multilayer diagrams the same base often becomes quiet while one overlay is promoted.

Record per panel:

- base line/tone class;
- thematic overlay line/tone/color class;
- callout line class;
- symbol/icon class;
- context/vegetation class;
- vertical-guide class.

Pixel similarity is insufficient if the foreground/background hierarchy changes and the analytical reading order collapses.

## 7. Dense-raster decomposition loop

For R1/R3 raster references with many panels and micro-icons, use:

`FULL SHEET → PANEL/STACK SEGMENTATION → SHARED BASE → THEME OVERLAY → CALLOUT NETWORK → SYMBOL DICTIONARY → TYPOGRAPHY → MICRODETAIL → SAME-SIZE RENDER → RELATION AUDIT → PIXEL/ROI DIFF`.

Do not start by tracing every visible pixel at once.

If automatic tracing is used, quarantine it in an `EXTRACTION_AID` group and rebuild in-scope relations semantically before claiming editable reconstruction.

## 8. Multilayer ROI contract

A single full-page metric can hide one failed panel.

For each panel/stack layer create at minimum:

- panel bounding ROI;
- one primary relationship ROI;
- one callout/leader ROI;
- one symbol/icon ROI;
- one typography ROI when recoverable;
- repeated-base correspondence anchors.

Report metrics per panel and relationship. A panel with a critical relation mismatch remains `REVISE` even if the full-page metric improves.

## 9. Producer verdict boundary

The producer may record only:

- `EXECUTED`;
- `SELF-CHECKED`;
- `REVIEW PENDING`;
- `REVISE`;
- `REJECT`.

The producer may not award `PIXEL KEEP`, `MAIN KEEP`, `PROFESSIONAL FINISH PASS`, or equivalent.

Independent review must reopen the candidate itself and inspect both:

1. visual fidelity / pixel or anchor evidence;
2. relationship fidelity — whether claims are actually drawn rather than merely written.

## 10. New reconstruction blockers exposed by calibration

Automatic `REVISE / REJECT` triggers:

- same-canvas path trace with no semantic relationship reconstruction;
- relationship present only as a label;
- visually similar leader line with wrong target/topology;
- panel-by-panel redrawing causes repeated-base drift;
- base/overlay contrast order is reversed;
- repeated icons have no reusable symbol logic;
- full-page metric hides a failed thematic layer;
- low-resolution text is guessed rather than marked `UNRECOVERABLE / SUBSTITUTE`;
- candidate uses semantic guide lines that do not match the source simply to make the relation clearer;
- raster/path-cloud extraction aid is presented as final professional editable source.

`RF PIXEL FIDELITY + RELATIONSHIP FIDELITY + SEMANTIC EDITABILITY` must be reviewed as separate axes.

## 11. Dual-track repair — do not let pixel similarity defeat editability

The actual atlas calibration exposed another failure: a raw path-cloud trace can score better on full-page pixel metrics than a cleaner semantic reconstruction. That does **not** make the trace the better reconstruction.

Maintain two explicit internal tracks until the semantic rebuild has closed enough visual gaps:

- `VISUAL_EXTRACTION_TRACK` — may contain quarantined trace/path-cloud evidence used to locate shapes, tones and repeated geometry;
- `SEMANTIC_REBUILD_TRACK` — shared bases, routes, zones, callouts, symbols and text rebuilt as editable objects.

Rules:

1. Never promote `VISUAL_EXTRACTION_TRACK` merely because its MAE/changed-pixel ratio is lower.
2. The final editable candidate must derive its in-scope relationships from `SEMANTIC_REBUILD_TRACK`.
3. A repeated base may remain `STRUCTURED VECTOR` if rebuilding every architectural edge semantically has no decision value, but routes/zones/callout topology/symbol instances/text must reach `SEMANTIC VECTOR` when they carry the analytical claim.
4. Once the semantic structure is stable, run `PIXEL_SOLVER_PROTOCOL` only on bounded parameters such as panel transforms, group translations, label baselines, stroke widths and symbol scales. Do not use the solver to collapse semantic objects back into anonymous traces.
5. Compare both tracks during repair. If the semantic track loses a visible relationship or panel hierarchy that the extraction track still exposes, the valid state is `REVISE`, not permission to publish the trace.

Recommended repair loop:

`EXTRACTION AID → SHARED BASE REGISTER → SEMANTIC RELATIONS → CALLOUT/SYMBOL REBUILD → SAME-SIZE RENDER → PANEL/RELATION DIFF → BOUNDED SOLVER → REOPEN RELATION AUDIT`.

## 12. Machine semantic-reconstruction gate

Use `tools/validate_semantic_reconstruction.py` with a `RELATION_REGISTER.json` when a reconstruction claims semantic editability.

The machine gate checks only structural claims that are objectively testable:

- one master base exists and is reused with `<use>` across multiple panels;
- panels point to registered shared-base instances;
- relation IDs are unique and exist in the SVG;
- a relation marked `DRAWN` has non-text carrier geometry;
- carrier and target IDs exist;
- a callout, when declared, contains label + leader geometry + anchor + registered target;
- reusable symbol families actually have multiple `<use>` instances;
- the register remains non-promoted.

Synthetic regression fixture:

- `fixtures/reconstruction/ML-REL-01_SEMANTIC.svg`
- `fixtures/reconstruction/ML-REL-01_RELATION_REGISTER.json`

A structure PASS proves only that semantic reconstruction claims are wired coherently. It does **not** prove visual/pixel fidelity, professional finish, technical truth, or Design KEEP.
