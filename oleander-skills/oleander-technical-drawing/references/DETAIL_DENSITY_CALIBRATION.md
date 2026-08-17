# OLEANDER Technical Drawing — Professional Detail Density Calibration

Status: `v0.1 / companion to oleander-technical-drawing v0.2 candidate`

Purpose: calibrate **technical depth at near-read** without destroying first-read hierarchy or manufacturing/field truth boundaries.

Professional density is not line count, note count, hatch count or the number of detail bubbles.

`DETAIL DENSITY = DECISION-COVERAGE × TRACEABILITY × GRAPHICAL PROOF`, not `MORE GRAPHICS`.

A dense drawing that still leaves the interface, controlling dimension, assembly path or verification state unclear is shallow. A sparse drawing can be professionally deep if every decision-critical layer is resolved and traceable.

## 1. Depth ladder

Use the following ladder as a diagnostic, not as a mandatory equal-weight checklist.

### D0 — Identity / control
- drawing/view ID;
- parent view / child detail relation;
- scale or explicit NTS;
- revision/status/truth boundary.

### D1 — Primary geometry / spatial relation
- cut/profile/assembly silhouette;
- main datum/level/axis;
- support, movement, load, drainage or route relation;
- existing/proposed/source geometry where relevant.

### D2 — Functional dimensions / datums
- controlling overall dimension;
- clear opening / fit / reach / clearance / level / offset / pitch as applicable;
- datum or reference line from which critical dimensions make sense;
- truth state attached to each non-authoritative dimension (`LOCKED TRAINING`, `RECOMMENDED`, `RANGE`, `FIELD VERIFY`, `TBD`).

### D3 — Build-up / material / component identity
- material or component IDs;
- actual layer sequence, where the sequence matters;
- substrate vs finish vs gasket/seal/isolation layer;
- adjacent materials remain graphically separable.

### D4 — Connection / fixing / interface
- interface geometry is drawn, not only described;
- mating/edge/bracket/base/fastener/weld/anchor zone is visible when it is part of the decision;
- connection ownership is clear: current authority, manufacturer, engineer, FIELD, or training fixture.

### D5 — Environment / safety / serviceability
As applicable:
- water path / drainage / weep / receiving condition;
- corrosion/isolation/finish boundary;
- safety edge / hand interface / clearance;
- assembly insertion/removal direction;
- tool envelope / inspection / cleaning / replacement access.

### D6 — Verification / unresolved closure
- engineering open items;
- FIELD VERIFY items;
- manufacturer/system verification;
- tolerances/fit not yet authorized;
- what would change the recommendation.

A professional detail normally spans several adjacent depth levels. It does **not** need every level if the decision does not require it.

## 2. Multi-zoom density rule

Use three nested information bands:

`3S = D1 PRIMARY RELATION`
`30S = D1 + D2 + D3 + parent/detail logic`
`NEAR READ = D2 + D3 + D4 + D5 + D6`

Do not distribute near-read density uniformly across the whole sheet. Concentrate it at the actual decision interfaces.

## 3. Evidence-artifact test

For a technical drawing, text saying a feature exists is weaker than a graphical artifact showing the relationship.

Examples:
- `REMOVABLE CONNECTION` note alone = insufficient if no removal direction/tool space is drawn;
- `DRAINAGE` note alone = insufficient if water direction/outlet/receiving side is absent;
- `FASTENER` note alone = insufficient if the mating/interface zone has no fixing geometry;
- `CMF BOUNDARY` note alone = insufficient if finish/substrate layers are visually indistinguishable;
- `FIELD VERIFY FOUNDATION` note alone = insufficient if the drawing gives the foundation a resolved final geometry without open-state graphics.

Text may qualify a technical relationship. It may not substitute for the relationship.

## 4. Density budget

High density belongs only where a technical decision is made.

### Primary field
Keep relatively low-to-medium near-read density:
- dominant geometry;
- controlling dimensions/datums;
- only decision-critical direct labels;
- parent callouts.

### Detail / annotation rail
Allow high near-read density:
- enlarged interfaces;
- component/material IDs;
- dimension chains;
- fixing/connection geometry;
- service/maintenance envelopes;
- open/verify register.

### Metadata/footer
Keep low contrast and low visual density:
- provenance;
- status;
- revision;
- does-not-prove text.

Uniformly high density is a professional-finish failure because it destroys hierarchy.

## 5. Architecture / interior calibration

For a serious section/interface detail, inspect whether the drawing shows, where relevant:
- parent section callout and child detail ownership;
- level/datum relation;
- controlling overall/clear dimension;
- wall/floor/ceiling build-up as actual layers, not one block;
- substrate / finish / lining / trim separation;
- sill/head/jamb/edge return where the interface occurs;
- bracket/fixing zone;
- seal, isolation, drainage or movement allowance when applicable;
- material IDs and finish state;
- FIELD/engineer/manufacturer open items.

Do not invent fire, thermal, waterproofing, acoustic or structural performance layers merely to make the detail look professional.

## 6. Landscape / site calibration

For a path/edge/platform/node section, inspect whether the drawing shows, where relevant:
- parent terrain/path relation;
- path build-up or surface/support distinction;
- crossfall/longitudinal water intent;
- outlet/receiving condition;
- edge/safety relation;
- support/subgrade interface;
- foundation/subgrade state;
- removable/reversible parts when maintenance matters;
- cleaning/inspection access;
- terrain/rock/soil uncertainty without false geology.

A landscape node is not professionally deep if it has a platform silhouette and many notes but no water/support/edge/service logic.

## 7. Industrial / product calibration

For assembly and mating drawings, inspect whether the drawing shows, where relevant:
- part IDs and stable assembly order;
- assembly axis/direction;
- named datum/reference surface;
- controlling fit/gap/clearance;
- interface stack;
- fastener/fixing path where relevant;
- insertion/removal path;
- tool/service envelope;
- CMF state separate from CAD geometry authority;
- BOM/revision relationship;
- tolerance only when authority exists.

For synthetic training fixtures, exact values must be labelled `LOCKED TRAINING VALUE`; they are not manufacturing recommendations.

## 8. Structural/support explanation calibration

For a connection/foundation explanatory drawing, inspect whether the drawing shows, where relevant:
- load/support path;
- member → plate/bracket → fastener/anchor → substrate/foundation chain;
- contact/bearing/isolation/grout layer if part of the concept;
- water/corrosion separation;
- inspection/tool access;
- edge distance/embedment/plate/member dimensions only when genuinely authorized;
- explicit engineering/field open state.

Never add realistic-looking anchor sizes, reinforcement, weld symbols, plate thicknesses or foundation dimensions merely to increase apparent professionalism.

## 9. Dimension density calibration

Dimension count is not dimension quality.

Prefer:
1. controlling dimension / datum;
2. functional clearance/fit/level;
3. component/build-up dimension needed to resolve the decision;
4. supporting/reference dimensions.

Reject:
- repeated dimensions with no control hierarchy;
- dimensions copied across views that can drift;
- decorative micro-dimensions that do not govern anything;
- precise decimals on inferred/field-open geometry;
- dimensions visually detached from their truth state.

## 10. Annotation density calibration

Near-read annotation should behave like a technical index, not prose.

Prefer:
- stable IDs (`MAT-01`, `PART-03`, `D-05`, `FV-02`);
- short claim-bearing labels;
- aligned note landings;
- one explicit verify register rather than repeated warning prose;
- direct leaders to exact targets.

Split a detail when notes begin to explain relationships that the geometry cannot show clearly at the current scale.

## 11. Density failure modes

Automatic `REVISE` triggers:
- detail appears professional only because it contains many lines/hatches;
- annotation count increases but graphical proof does not;
- every interface has equal detail depth regardless of decision importance;
- material layers are named but not spatially drawn;
- fasteners/anchors are labelled but not located in an interface;
- serviceability is mentioned without a drawn access/removal envelope;
- FIELD/engineering-open items are hidden in footer text only;
- child detail contains more technical authority than its parent can trace;
- exact-looking dimensions imply unsupported site/engineering truth;
- text shrinks below intended-size readability to preserve excessive density.

## 12. Density review record

For each serious fixture/drawing record:

- `DENSITY_TARGET` — what decision requires near-read depth;
- `DEPTH_LEVELS_PRESENT` — D0…D6 actually represented;
- `GRAPHICAL_PROOF` — which relationships are drawn rather than merely stated;
- `CONTROL_DIMENSIONS` — controlling vs support/reference dimensions;
- `SERVICE / ENVIRONMENT` — maintenance/water/safety logic if applicable;
- `OPEN ITEMS` — FIELD / engineer / manufacturer / authority closure;
- `3S READ`;
- `30S READ`;
- `NEAR READ`;
- `OVER-DENSITY REMOVALS` — anything deleted because it added noise rather than proof.

`MORE DETAIL ≠ MORE PROFESSIONAL`.

`DECISION-COMPLETE + TRACEABLE + READABLE + TRUTH-BOUNDED = PROFESSIONAL DETAIL DEPTH CANDIDATE`.
