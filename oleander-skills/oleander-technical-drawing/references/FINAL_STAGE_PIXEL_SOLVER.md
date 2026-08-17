# OLEANDER Technical Drawing — Final-stage Typography / Symbol / Micro-flow Solver

Status: `candidate extension / PR #172`

Use only after geometry master, panel instances, thematic overlays, callout topology and flow-network topology are materially reconstructed. This module is for the last bounded residual stage, not for hiding missing structure.

`TYPOGRAPHY PIXELS != EDITABLE TEXT SEMANTICS`

`SYMBOL PIXELS != SYMBOL OWNERSHIP`

`MICRO-FLOW PIXELS != FLOW TOPOLOGY`

`LOWER ERROR != PRODUCER KEEP`

`BOUNDED RESIDUAL CARRIER != FULL-SHEET PATH CLOUD`

`BOUNDED ROI != AUTOMATICALLY SPARSE RESIDUAL`

`HIGH RESIDUAL COVERAGE = REOPEN SEMANTIC GEOMETRY`

## 1. Entry conditions

Do not enter this stage until all are true:

- main/body geometry is not a placeholder;
- per-panel base visibility/omission is materially reconstructed;
- thematic overlays have their own semantic and visual layers;
- circulation/mobility has a `FLOW_NETWORK_REGISTER`;
- labels/symbols have known semantic owners where recoverable;
- remaining error is localized to typography, symbols/nodes, micro-flow, leader landing, antialiasing, or compressed-raster residuals.

If route/base/theme recall is still materially low, return to the corresponding upstream module.

## 2. Dual representation is allowed only when explicit

For compressed R3 references, target-size fidelity may require a separate visual carrier while the editable semantic object remains recoverable.

Allowed pattern:

`EDITABLE SEMANTIC OBJECT + BOUNDED VISUAL CARRIER + NON-AUTHORITY STATUS`

Examples:

- editable `<text>` retained + bounded typography visual carrier;
- semantic parking/transit node retained + bounded symbol visual carrier;
- semantic route graph retained + bounded micro-flow visual carrier.

Forbidden pattern:

`REFERENCE → FULL-SHEET ANONYMOUS PIXEL PATHS → CALL IT EDITABLE / SEMANTIC / PIXEL-EXACT`

## 3. Typography final stage

Typography must be reviewed in text-only ROIs, not through full-page MAE.

Keep separate:

- text content;
- semantic owner;
- baseline position;
- line break;
- rotation/tangent relation;
- editable font/text source;
- target-size visual glyph carrier when exact source font/rendering is unavailable.

A source-derived glyph carrier may approximate antialiasing at target size, but it does not prove original font identity or editable source typography.

Record:

`TEXT-ID → OWNER → CONTENT → PAGE BBOX → BASELINE/ANGLE → EDITABLE SOURCE STATE → VISUAL CARRIER ID → SOURCE CLASS → CLAIM CEILING`.

## 4. Symbol / node final stage

Repeated nodes and editorial symbols must preserve semantic ownership even when a visual carrier is used.

Check:

- node/edge owner;
- count or bounded count;
- page-space position;
- scale;
- repeated family identity;
- clustering/distribution rhythm;
- source-derived visual carrier bounds;
- whether the visual carrier contains unrelated text/leader/base pixels.

A visually accurate parking pin on the wrong road remains a relation failure.

## 5. Micro-flow final stage

Micro-flow repair is limited to already-registered route systems.

Allowed targets:

- small arrowheads;
- thin secondary vectors;
- local branch stubs;
- terminal/continuation marks;
- route-edge antialiasing and color phase;
- compact mode nodes attached to the network.

Do not create new routes from residual pixels without adding them to the semantic flow register.

`MICRO VISUAL CARRIER != NEW ROUTE AUTHORITY`.

## 6. Residual solver boundary

Residual correction must be bounded by explicit ROI and semantic class.

Allowed:

- typography ROI;
- known symbol/icon ROI;
- P05/P06 flow/mobility body ROI;
- compact residual components satisfying size/class constraints;
- side-icon/callout-margin ROI.

Forbidden:

- full-page mismatch mask;
- whole-panel opaque repaint that erases semantic layers;
- residual carrier that absorbs labels, base, theme and flow into one anonymous object;
- using changed-pixel improvement to override a semantic/topology failure.

## 6A. Residual-carrier density gate

A residual carrier may be spatially bounded yet still be functionally equivalent to repainting the source.

Therefore record for every residual ROI:

- `roi_pixel_count`;
- `residual_pixel_count`;
- `residual_coverage_ratio`;
- `component_count` or run/path count;
- residual classes represented;
- whether the semantic object remains visually legible without the residual carrier;
- whether removing the residual carrier reveals a recognizably correct geometry or only a rough placeholder.

Interpretation:

- low residual coverage concentrated on antialiasing, glyph edges, tiny symbol details or local compressed-raster noise may remain in final-stage calibration;
- medium/high residual coverage is a diagnostic, not a success condition;
- if the carrier must repaint a large fraction of the ROI to make the semantic object resemble the reference, return to the semantic geometry / symbol / typography module first.

Do **not** use one universal percentage as a Design PASS threshold. Use the ratio as a stop signal together with semantic legibility and residual class.

Automatic `REVISE / REOPEN UPSTREAM` when any of these are true:

1. the residual carrier covers most of a small symbol/diagram ROI rather than only its local residuals;
2. the semantic object is not recognizably the same object when the residual layer is hidden;
3. residual runs reproduce broad fills, complete contours or full icon silhouettes that should belong to semantic geometry;
4. the residual layer contains multiple unrelated semantic classes;
5. `changed_pixel_ratio` improves sharply only because residual density increases sharply;
6. the carrier acts as a vectorized raster substitute rather than a correction layer.

Calibration example that triggered this gate:
- a waterfront-theory icon ROI reached near-zero `>12` pixel difference only after a bounded residual carrier covered about `67.9%` of the ROI;
- the semantic-only ROI remained visually and numerically far from the source;
- result: pixel repair succeeded, but semantic reconstruction was still `REVISE`; the correct action is to reopen the icon geometry, not promote the residual-heavy result.

`SPARSE RESIDUAL REPAIR != DENSE RESIDUAL REPAINT`.

## 7. Evaluation sequence

Run in this order:

1. `TYPOGRAPHY ROI` — baseline/linebreak/rotation/content and target-size glyph fidelity;
2. `SYMBOL/NODE ROI` — position/scale/family/ownership/density;
3. `MICRO-FLOW ROI` — secondary edges, local arrows, branch/continuation marks;
4. `RESIDUAL DENSITY` — verify that local carriers remain correction layers rather than repaint layers;
5. `FULL PAGE` — only after the local classes improve without upstream regression;
6. reopen `RELATION / FLOW / BASE / THEME` audits;
7. independent review.

Do not optimize global MAE first.

## 8. Claim boundary

A final-stage candidate may report measured producer diagnostics such as MAE/changed-pixel reduction, but remains:

`SELF-CHECKED / REVISE / REVIEW PENDING`

until an independent reviewer checks:

- semantic editability remains recoverable;
- visual carriers are bounded and non-authoritative;
- residual carriers remain sparse correction layers rather than dense repaints;
- no full-sheet path-cloud shortcut was introduced;
- symbol/node ownership remains correct;
- micro-flow remains bound to registered topology;
- remaining differences are honestly classified.

`FINAL-STAGE METRIC IMPROVEMENT != RF-C3 != DESIGN KEEP`.