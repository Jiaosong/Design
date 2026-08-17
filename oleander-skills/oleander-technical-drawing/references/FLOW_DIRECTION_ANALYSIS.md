# OLEANDER Technical Drawing — Flow / Direction Analysis Grammar

Status: `candidate extension / PR #172`

Use with `ANALYSIS_DRAWING_SYSTEM.md` when the primary claim is circulation, mobility, route hierarchy, directional sequence, entry/exit, service flow, pedestrian/bicycle movement, traffic state, or another spatial network carried by lines, arrows, nodes and route-linked labels.

Use with `REFERENCE_RECONSTRUCTION_FIDELITY.md` and `MULTILAYER_RELATION_RECONSTRUCTION.md` when reconstructing a supplied flow/circulation analysis reference.

`FLOW LINE != DECORATIVE POLYLINE`

`ARROWHEAD != GENERIC DIRECTION ICON`

`NETWORK TOPOLOGY != VISUAL SIMILARITY`

`ROUTE LABEL PRESENT != ROUTE RELATION DRAWN`

`LOW ROUTE-CARRIER RECALL != ANTIALIASING PROBLEM`

`GEOMETRY MASTER != RENDERED BASE INSTANCE`

## 1. What a professional flow analysis actually contains

A circulation/flow drawing is a graph tied to spatial base geometry.

Minimum semantic objects:

- `BASE_GEOMETRY` — streets, paths, blocks, edges, entrances or other spatial carriers;
- `ROUTE_EDGE` — one traversable or analytical segment;
- `ROUTE_NODE` — junction, entry, exit, stop, event, conflict or decision point;
- `DIRECTION_MARKER` — local direction attached to a route edge or continuation;
- `ROUTE_CLASS` — primary / secondary / local / optional / closed / service / etc.;
- `ENTRY_EXIT` — network boundary crossing or continuation beyond the current frame;
- `STATE / SPEED / CONDITION` — speed, accessibility, closure, priority or other route-linked condition;
- `ROUTE_LABEL` — name/ID bound to a specific segment;
- `MODE_SYMBOL` — pedestrian, cycle, transit, parking, service, etc., bound to a route/node rather than floating as an unrelated pictogram.

A thick colored line with one arrow at the end is not automatically a flow analysis.

## 2. Direction-marker grammar

Direction markers should be treated as **events on a route**, not oversized standalone graphics.

Record for each marker:

- owning route edge ID;
- marker position along the route (`start / interior / end / continuation`);
- orientation tangent to the local route segment;
- marker head length/width;
- marker-to-stroke ratio;
- fill/stroke state;
- whether the marker means travel direction, continuation, entry, exit, transition, or emphasis;
- whether both directions are allowed;
- whether the reference uses one marker per edge, only terminal markers, or repeated interior markers.

### Marker scaling

For SVG reconstruction, explicitly decide between `markerUnits="userSpaceOnUse"` and `markerUnits="strokeWidth"`.

Do not allow marker size to grow unintentionally with route stroke width. A common reconstruction failure is a correct route line with an arrowhead two or three times too large because the marker is stroke-scaled.

### Tangency

The arrowhead must be tangent to the route at the placement point. A visually close triangle that points along the wrong segment is a directional-relation error.

## 3. Direction-marker taxonomy — do not collapse unlike arrows

Before reconstruction, classify every visible arrow/triangle by function. At minimum distinguish:

1. `ROUTE_DIRECTION` — direction of travel/movement on a route edge;
2. `ENTRY_EXIT` — crossing into/out of the analytical frame or site;
3. `EXTERNAL_CONTINUATION` — the route continues beyond the current panel;
4. `ANALYTICAL_VECTOR` — a directional analytical force/relationship not bound to a traversable path;
5. `SEQUENCE_TRANSITION` — before/after or state transition;
6. `CALLOUT_POINTER` — annotation pointer, not movement;
7. `NORTH / ORIENTATION` — sheet/spatial orientation, not network direction.

These classes may look visually similar in a compressed reference but are not interchangeable. A generic SVG marker definition applied to all of them is a semantic failure unless the source genuinely uses one family with one meaning.

### Direction-marker register

Record:

`MARKER-ID → FUNCTION CLASS → OWNER EDGE/NODE → PAGE POSITION → LOCAL TANGENT → HEAD GEOMETRY → STROKE/FILL → REFERENCE CONFIDENCE`.

If the owner edge/node is unknown, state `UNRECOVERABLE / PARTIAL`; do not invent a network relation merely because an arrow is visible.

## 4. Flow-network topology register

Create a `FLOW_NETWORK_REGISTER` for serious circulation analysis or strict reconstruction.

For each `ROUTE_EDGE` record:

- edge ID;
- start node ID;
- end node ID;
- directed / bidirectional state;
- route class;
- source/base carrier ID;
- page-space path geometry;
- stroke class;
- dash/opacity/color;
- direction-marker IDs;
- state/speed label IDs;
- connected symbols/mode IDs;
- source truth state / reconstruction confidence.

For each `ROUTE_NODE` record:

- node ID;
- page-space coordinate;
- node class;
- connected edge IDs;
- degree / branch condition;
- source/base target;
- symbol/callout relation if any.

This makes branch/merge/continuation errors visible instead of hiding them inside one path string.

### Topology invariants

A strict reconstruction must explicitly test:

- every edge has valid start/end nodes;
- node degree matches the actual connected edge set;
- branch/merge locations remain attached to the same source spatial carrier;
- directed edges have direction evidence when the source shows it;
- bidirectional routes are not silently rendered one-way;
- frame continuations do not terminate as ordinary internal endpoints;
- separate route classes remain separate objects even when they overlap visually.

## 5. Route hierarchy is graphical, not only semantic

A professional flow analysis often uses more than one line class:

- primary route / major movement spine;
- secondary or exploratory route;
- local connector;
- external continuation;
- closed/reduced/degraded route;
- source road/path edge;
- correspondence/guide line.

Preserve relative hierarchy through:

`POSITION / GEOMETRY → STROKE WIDTH → OPACITY / DASH → MARKER SCALE → COLOR`.

Do not flatten every route into the same thick accent stroke.

### Route-class inventory before drawing

For strict reference reconstruction, inventory visible route classes **before** authoring SVG routes. Record at minimum:

`CLASS → REPRESENTATIVE PIXEL/STROKE SAMPLE → EDGE COUNT OR BOUNDED COUNT → MARKER POLICY → LABEL POLICY → BASE-BINDING TYPE`.

Do not infer class equality merely because two lines share hue. Width, opacity, dash, marker frequency and spatial role may encode different classes.

## 6. Flow line must be bound to the spatial base

Every route segment should answer:

`WHAT BASE EDGE / PATH / STREET / SPACE DOES THIS LINE REPRESENT?`

Possible binding states:

- `CENTERLINE-BOUND`;
- `EDGE-BOUND`;
- `CORRIDOR-BOUND`;
- `FREE ANALYTICAL VECTOR`;
- `UNKNOWN / UNRECOVERABLE`.

A route that drifts across buildings or ignores the source street/path geometry is not a minor pixel error. It is a spatial-relation failure.

### Base-binding audit

For each critical edge, compare at multiple stations, not only endpoints:

`ROUTE SAMPLE POINT → EXPECTED BASE CARRIER → CANDIDATE BASE CARRIER → NORMAL OFFSET / RELATION STATE`.

A route can have correct endpoints and still bow across the wrong spatial object. Endpoint alignment alone does not establish relation fidelity.

## 7. Speed, street-name and mode-symbol binding

A speed or street label is not ordinary typography.

Record:

- owning route/street edge;
- baseline center in page coordinates;
- angle/tangent relationship;
- offset from the route;
- repetition policy;
- whether the label refers to the whole corridor or one segment.

Parking/transit/bicycle symbols must record their owning node/edge or explicit free-standing state. A visually accurate pin at the wrong road segment is a relation error.

### Symbol-density fidelity

For references where repeated parking/transit/bicycle pins form a visible system, compare:

- count or bounded count by symbol class;
- spatial distribution along the network;
- node/edge ownership;
- clustering/repetition rhythm;
- symbol scale hierarchy.

One or two correctly drawn pins cannot stand in for a dense source network.

## 8. Reconstruction-specific fidelity dimensions

For flow/circulation reconstruction, add these checks to ordinary pixel/ROI comparison:

### Topology fidelity

- route-edge count;
- node count;
- branch/merge structure;
- edge connectivity;
- entry/exit count;
- directed/bidirectional state;
- continuation beyond panel/frame.

### Geometry fidelity

- route centerline/edge displacement;
- route-to-base binding;
- line intersections;
- segment angle/length;
- arrow placement/orientation;
- marker-to-line scale ratio.

### Graphic fidelity

- stroke-class hierarchy;
- line cap/join;
- marker shape;
- marker size;
- opacity/dash;
- color/tone;
- label/symbol density.

### Relation fidelity

- speed/name labels on correct edge;
- parking/transit/cycle symbols on correct node/edge;
- callout anchor targets correct route/zone;
- external continuation represented where visible in the source.

A full-page MAE can improve while all four of these remain wrong.

## 9. Flow-specific pixel diagnostic

For a supplied reference, isolate route-carrier pixels by panel and class where feasible.

Useful diagnostics:

- route-color mask intersection/union;
- reference-color recall — how much of the source route carrier the candidate recovers;
- candidate precision — how much of candidate route carrier lands on source route carrier;
- skeleton/centerline displacement;
- endpoint displacement;
- branch-point mismatch;
- arrowhead ROI mismatch;
- route-linked symbol density mismatch.

These metrics are diagnostics, not universal PASS thresholds.

If reference-color recall is very low, do not spend time tuning antialiasing or fonts first. The route system itself has not been reconstructed.

### Low-recall stop rule

When a route-carrier diagnostic shows that a material share of the source network is absent or displaced, freeze lower-priority pixel polishing and return to:

`EDGE INVENTORY → NODE/BRANCH TOPOLOGY → BASE BINDING → ROUTE CLASSES → DIRECTION MARKERS`.

Typography may continue only for labels needed to identify route ownership; cosmetic type, antialiasing, JPEG-noise matching and micro-icon color work are deferred.

This is a **repair-order rule**, not a fixed numeric threshold. The producer must show that route carrier/topology is substantially reconstructed before claiming lower-layer residuals are the dominant problem.

## 10. Multi-layer analytical atlas rule

When several panels reuse one site but show different thematic networks:

`GEOMETRY_MASTER != RENDERED_BASE_INSTANCE`.

Maintain:

- one canonical `GEOMETRY_MASTER` where recoverable;
- per-panel transform;
- per-panel visibility/occlusion mask;
- per-panel base line/tone class;
- per-panel theme overlay;
- per-panel route network.

Do not assume that one identical rendered base `<use>` can be copied into every panel simply because the underlying site is the same. Different panels may intentionally omit, fade, mask, crop or emphasize different base objects.

This distinction is essential for pixel reconstruction.

### Base-instance register

For each analytical panel record:

`PANEL-ID → GEOMETRY_MASTER REV → TRANSFORM → VISIBLE OBJECT SET / MASK → LINE/TONE CLASS → THEME OVERLAY → NETWORK REGISTER`.

Shared source geometry should prevent drift; per-panel rendering state should preserve what the reference actually shows.

## 11. Exact-reconstruction blocker sequence

Before claiming high fidelity, eliminate in this order:

1. wrong `GEOMETRY_MASTER`;
2. wrong per-panel transform/crop/visibility;
3. wrong route topology;
4. wrong route-to-base binding;
5. missing primary/secondary line classes;
6. wrong arrowhead function/position/orientation/scale;
7. wrong nodes/pins/mode-symbol density;
8. wrong speed/street label binding;
9. typography/stroke/color residuals;
10. renderer/JPEG/antialiasing residuals.

Do not tune item 9–10 while items 1–6 are materially wrong.

### Structural mismatch vs renderer residual

Classify remaining difference clusters before pixel polishing:

- `STRUCTURAL / TOPOLOGY` — missing/extra/misconnected route or node;
- `GEOMETRIC / BINDING` — route exists but is displaced from its source carrier;
- `DIRECTIONAL` — arrow function, tangent, position or bidirectionality wrong;
- `SYMBOL-DENSITY` — repeated network symbols missing/overgeneralized;
- `TYPOGRAPHIC` — correct relation but baseline/run/rotation differs;
- `RENDERER / JPEG` — geometry and semantics align, residual is rasterization/compression.

Only the last class should be handled as pure renderer/JPEG cleanup.

## 12. R3/JPEG truth boundary

For compressed raster references, literal tolerance-zero pixel equality may be unavailable while preserving clean semantic vectors.

JPEG artifacts can affect:

- glyph edges;
- thin strokes;
- small arrowheads;
- pale guide lines;
- pastel fills;
- antialiased diagonals.

Do not inject artificial vector noise to imitate compression artifacts while claiming professional semantic editability.

For R3 sources, separate:

- `RECOVERABLE VECTOR / RELATION FIDELITY`;
- `RENDERED HIGH FIDELITY`;
- `SOURCE-COMPRESSION RESIDUAL`.

RF-C3 remains unavailable when exact original font/render/compression conditions are not verifiable.

Do not invoke `SOURCE-COMPRESSION RESIDUAL` while recoverable route topology, base binding, marker placement or symbol density is still materially incomplete.

## 13. Machine flow-network gate

Use `tools/validate_flow_network.py` with a `FLOW_NETWORK_REGISTER` whenever a reconstruction claims semantic flow-network editability.

The machine gate checks structural claims that are objectively testable:

- registered base geometry exists;
- required route classes exist and contain edges;
- edge IDs are unique and map to vector line/path/polyline carriers;
- each edge references valid start/end nodes;
- node degree and connected-edge lists agree with the graph;
- base-binding state is explicit;
- directed edges that require direction evidence own direction markers;
- each marker names its owner edge and stays within the declared tangent/marker-scale contract;
- route labels remain editable text bound to an existing edge;
- mode symbols bind to exactly one registered node or edge;
- external continuations use an explicit continuation/external route class;
- the register remains non-promoted.

Regression fixture:

- `fixtures/reconstruction/FLOW-01_NETWORK.svg`
- `fixtures/reconstruction/FLOW-01_NETWORK_REGISTER.json`

A machine `STRUCTURE PASS` does not prove:

- the reference network was completely inventoried;
- pixel/visual fidelity;
- route planning validity;
- project/site truth;
- independent Design KEEP.

## 14. Reconstruction acceptance ladder for flow panels

Do not jump directly from “there are arrows” to pixel fidelity. Use:

### `FN-C0 / NETWORK IDENTIFIED`
Panel segmentation, base, route classes and recoverable network objects have been inventoried.

### `FN-C1 / TOPOLOGY RECONSTRUCTED`
Recoverable edge/node/branch/continuation structure is rebuilt as editable objects. Major relations do not rely on prose.

### `FN-C2 / SPATIAL BINDING RECONSTRUCTED`
Route geometry is attached to the correct base carriers; markers, labels and mode symbols own the correct edges/nodes.

### `FN-C3 / VISUAL NETWORK FIDELITY CANDIDATE`
Route carrier, line-class hierarchy, direction-marker geometry, node/symbol density and panel rendering state are materially aligned to the reference under declared source limitations.

`FN-C3` is still not `RF-C3 PIXEL-EXACT`. The latter additionally requires the Pixel Forensic contract and source/render conditions that support an exact claim.

If the source is R3/JPEG, the normal ceiling may be `FN-C3 + RF-C2` rather than RF-C3.

## 15. Producer review questions

For every flow panel ask:

1. Can I trace the network without reading the prose?
2. Do I know which line is primary, secondary and continuation?
3. Are arrowheads attached to the actual route and tangent to it?
4. Do arrowheads mean the same thing as their source counterparts, rather than merely looking similar?
5. Do branches/merges occur at the same spatial locations as the source?
6. Do speed/street labels belong to the correct segments?
7. Are parking/transit/cycle symbols bound to actual nodes/edges and present at source-like density?
8. Does the overlay respect the base geometry at multiple sample stations, not only endpoints?
9. Does each panel render the shared base with the visibility/tone/omission state visible in that panel?
10. Is any conclusion carried only by a label because the route was simplified away?
11. Are remaining errors actually renderer/JPEG residuals, or are recoverable network objects still missing?

If any critical answer is no, producer state remains `REVISE / REVIEW PENDING`.

Producer may not self-award KEEP.
