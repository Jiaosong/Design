# OLEANDER Technical Drawing — Flow / Direction Analysis Grammar

Status: `candidate extension / PR #172`

Use with `ANALYSIS_DRAWING_SYSTEM.md` when the primary claim is circulation, mobility, route hierarchy, directional sequence, entry/exit, service flow, pedestrian/bicycle movement, traffic state, or another spatial network carried by lines, arrows, nodes and route-linked labels.

Use with `REFERENCE_RECONSTRUCTION_FIDELITY.md` and `MULTILAYER_RELATION_RECONSTRUCTION.md` when reconstructing a supplied flow/circulation analysis reference.

`FLOW LINE != DECORATIVE POLYLINE`

`ARROWHEAD != GENERIC DIRECTION ICON`

`NETWORK TOPOLOGY != VISUAL SIMILARITY`

`ROUTE LABEL PRESENT != ROUTE RELATION DRAWN`

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

## 3. Flow-network topology register

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

## 4. Route hierarchy is graphical, not only semantic

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

## 5. Flow line must be bound to the spatial base

Every route segment should answer:

`WHAT BASE EDGE / PATH / STREET / SPACE DOES THIS LINE REPRESENT?`

Possible binding states:

- `CENTERLINE-BOUND`;
- `EDGE-BOUND`;
- `CORRIDOR-BOUND`;
- `FREE ANALYTICAL VECTOR`;
- `UNKNOWN / UNRECOVERABLE`.

A route that drifts across buildings or ignores the source street/path geometry is not a minor pixel error. It is a spatial-relation failure.

## 6. Speed, street-name and mode-symbol binding

A speed or street label is not ordinary typography.

Record:

- owning route/street edge;
- baseline center in page coordinates;
- angle/tangent relationship;
- offset from the route;
- repetition policy;
- whether the label refers to the whole corridor or one segment.

Parking/transit/bicycle symbols must record their owning node/edge or explicit free-standing state. A visually accurate pin at the wrong road segment is a relation error.

## 7. Reconstruction-specific fidelity dimensions

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

## 8. Flow-specific pixel diagnostic

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

## 9. Multi-layer analytical atlas rule

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

## 10. Exact-reconstruction blocker sequence

Before claiming high fidelity, eliminate in this order:

1. wrong `GEOMETRY_MASTER`;
2. wrong per-panel transform/crop/visibility;
3. wrong route topology;
4. wrong route-to-base binding;
5. missing primary/secondary line classes;
6. wrong arrowhead position/orientation/scale;
7. wrong nodes/pins/mode-symbol density;
8. wrong speed/street label binding;
9. typography/stroke/color residuals;
10. renderer/JPEG/antialiasing residuals.

Do not tune item 9–10 while items 1–6 are materially wrong.

## 11. R3/JPEG truth boundary

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

## 12. Producer review questions

For every flow panel ask:

1. Can I trace the network without reading the prose?
2. Do I know which line is primary, secondary and continuation?
3. Are arrowheads attached to the actual route and tangent to it?
4. Do branches/merges occur at the same spatial locations as the source?
5. Do speed/street labels belong to the correct segments?
6. Are parking/transit/cycle symbols bound to actual nodes/edges?
7. Does the overlay respect the base geometry?
8. Is any conclusion carried only by a label because the route was simplified away?

If any critical answer is no, producer state remains `REVISE / REVIEW PENDING`.

Producer may not self-award KEEP.