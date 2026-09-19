# Remote / Proxy Reality Reconstruction Extension

Status: `CANDIDATE EXTENSION / EXISTING RESEARCH OWNER / C04 PRACTICE-DERIVED / NO FIELD PROMOTION`

Owner: `oleander-research`

Use when:
- material site / building / spatial / operational information is unavailable, incomplete, inaccessible, time-limited or cannot be obtained at the current project stage;
- the project must continue beyond abstract concept and needs a **reality-near provisional model**;
- existing public / project / image / map / GIS / technical / operational evidence can constrain the missing information strongly enough to support bounded design exploration;
- the design must remain readily correctable when better evidence arrives.

This extension does **not** create measured field truth.

It formalizes:

`KNOWN REALITY ANCHORS → RELATIONS → PROXY VARIABLES → PLAUSIBLE ENVELOPE → CROSS-CHECKS → REALITY-NEAR PROVISIONAL MODEL → SENSITIVITY / ROBUSTNESS → DESIGN CONSEQUENCE → REOPEN WHEN BETTER EVIDENCE ARRIVES`.

It exists to prevent both failure modes:

1. **under-design** — “we cannot visit the site, therefore all spatial/professional work must stop”;
2. **fabricated certainty** — “we need a number, therefore an invented number becomes field truth”.

`NO FIELD DATA ≠ NO DESIGN`.

`PROXY REALITY ≠ FIELD MEASURED REALITY`.

---

## 1｜Existing-owner boundary

Use with, not instead of:

- `oleander-research/SKILL.md` — source authority, evidence / interpretation / assumption separation;
- `MEASUREMENT_UNCERTAINTY_EXTENSION.md` — uncertainty meaning when quantities affect a decision;
- `FIELD_SURVEY_REALITY_CAPTURE_EVIDENCE_EXTENSION.md` — when field evidence actually becomes available;
- `oleander-data-viz` — maps, comparison, uncertainty and spatial evidence visualization;
- `oleander-3d-pipeline` — proxy geometry / reconstruction artifacts;
- `oleander-technical-drawing` — NTS / provisional technical drawings after evidence boundaries are explicit;
- the applicable professional-domain process — for professional judgment, release and claim ceilings.

This extension owns **remote/proxy evidence reconstruction**, not:
- licensed survey;
- statutory/site approval;
- structural adequacy;
- code compliance;
- field safety;
- hydraulic performance;
- final construction geometry;
- user research;
- final professional-domain PASS.

---

## 2｜Truth vocabulary

Do not create a parallel global state system.

Use the existing OLEANDER truth separation:

- **EVIDENCE** — directly supported by an authoritative or traceable source;
- **INFERENCE** — derived from evidence through an explicit method;
- **ASSUMPTION** — plausible but unverified design test input;
- **DECISION** — current design choice made under the declared evidence ceiling.

C04 local `R1 / R2 / R3 / F` may remain project-local shorthand:
- `R1` = remote official / directly verified;
- `R2` = remote triangulated;
- `R3` = remote inferred / design-exploration only;
- `F` = field-only claim.

Do not promote these local labels into a new OLEANDER-wide state family.

---

## 3｜Core execution contract

`DECISION QUESTION + REQUIRED REALITY FIDELITY`
→ `CURRENT AUTHORITY / CLAIM CEILING`
→ `REALITY ANCHOR REGISTER`
→ `SOURCE FAMILY COVERAGE`
→ `RELATION GRAPH`
→ `PROXY VARIABLE REGISTER`
→ `LOW / BASE / HIGH OR OTHER BOUNDED ENVELOPE`
→ `INDEPENDENT CROSS-CHECKS`
→ `CONTRADICTION / RESIDUAL LOG`
→ `REALITY-NEAR PROXY MODEL`
→ `SENSITIVITY / ROBUSTNESS TEST`
→ `DESIGN CONSEQUENCE`
→ `FIELD / BETTER-SOURCE REPLACEMENT HOOK`.

The model exists only for the decision it supports.

Do not construct a “complete digital twin” when the project only needs a bounded relation, range or fit-check.

---

## 4｜Reality anchor register

Before estimating missing values, lock the facts and relations that the proxy model is **not allowed to contradict**.

Each anchor records:

- `anchor_id`;
- `claim / quantity / relation`;
- `source_ref`;
- `source_type`;
- `date / temporal relevance`;
- `geographic / object scope`;
- `unit / coordinate / reference system when material`;
- `authority / confidence`;
- `does_not_prove`;
- `consuming_proxy_variables[]`.

Typical anchors:

### A. Direct factual anchors
- official dimensions;
- published elevation differences;
- manufacturer dimensions;
- known building footprint;
- official route time;
- station / entrance / bridge / cable / road location;
- authoritative parcel / cadastral / planning geometry where available.

### B. Relational anchors
- A is above B;
- route branches after C;
- entrance faces street D;
- platform overlooks river E;
- room X connects to corridor Y;
- fixture row aligns with ceiling bay;
- retaining wall follows an existing contour break.

### C. Scale anchors
- known door / stair / tile / railing / vehicle / furniture / luminaire dimensions;
- published cable / equipment / structure dimensions;
- repeated standard object visible in images.

### D. Environmental / geospatial anchors
- DEM / terrain;
- satellite / orthophoto;
- land-cover;
- water history;
- street / path network;
- official mapping;
- public GIS;
- current operator maps.

### E. Operational anchors
- official opening / route duration;
- capacity / equipment rating;
- transport mode;
- service sequence;
- known closure / seasonal relation.

`ANCHOR EXISTS ≠ EVERY DERIVED VALUE IS TRUE`.

---

## 5｜Source-family coverage

Use the strongest available sources in this order when applicable:

1. project / client / owner Current sources;
2. government / official operator / first-party technical sources;
3. public authoritative GIS / remote sensing / mapping;
4. current technical documentation / manufacturer / product data;
5. multiple photographs / videos / panorama / street imagery;
6. public route / operation / construction / maintenance records;
7. high-quality precedent / analogous site data for plausibility only.

Analogs may constrain plausibility; they may not overwrite site-specific anchors.

When one source family is missing, increase uncertainty instead of filling the gap with a visually convenient value.

---

## 6｜Proxy variable register

Every material reconstructed quantity records:

- `variable_id`;
- `quantity_or_relation`;
- `unit`;
- `decision_role`;
- `evidence_refs[]`;
- `derivation_method`;
- `low / base / high` or another justified interval/distribution;
- `central_value_meaning`;
- `confidence / uncertainty meaning`;
- `correlated_variables[]`;
- `hard_constraints[]`;
- `soft_constraints[]`;
- `plausibility_refs[]`;
- `sensitivity_rank`;
- `designs_consuming_this_variable[]`;
- `falsifier / reopen_trigger`;
- `future_field_or_authoritative_replacement_method`.

A single “best guess” without an envelope is not sufficient when the variable materially affects design.

---

## 7｜Allowed reconstruction methods

Choose the minimum method needed for the decision.

### 7.1 Direct derivation
Use published anchors and explicit equations.

Example:
`vertical difference / known horizontal or chord distance`.

Do not mislabel the resulting metric. A cable chord ratio is not terrain grade.

### 7.2 Multi-source triangulation
Use two or more materially independent source families to constrain the same relation or quantity.

Examples:
- official map topology + public imagery;
- route duration + network distance + terrain;
- manufacturer dimension + image scale;
- DEM + known elevation anchor + panorama ordering.

Two copies of the same underlying source are not independent evidence.

### 7.3 Image-scale reconstruction
Use:
- known object scale;
- repeated references;
- perspective/vanishing geometry;
- camera-height/body-scale plausibility;
- multiple images/viewpoints where possible.

Do not infer a consequential dimension from one distorted photograph unless the uncertainty remains broad enough for that limitation.

### 7.4 Network / route reconstruction
Use:
- official topology;
- map/GIS path;
- branch/return sequence;
- route time;
- elevation/terrain;
- stop/queue/read/rest allowance;
- current operational constraints.

Route timing is a model, not a field observation.

### 7.5 Terrain / section reconstruction
Use:
- DEM / contour / remote terrain;
- published elevation anchors;
- visible ridge/valley relations;
- hydrologic/topographic consistency.

Remote DEM is not a construction surface or survey.

### 7.6 Capacity / operational scenario
Use:
- published component capacity;
- queue / station / route / node bottleneck logic;
- low/base/high operational factor;
- stress-test scenarios.

Do not propagate a component rating into total system capacity without the actual bottleneck relation.

### 7.7 Domain-typical geometry
May be used only as a **plausibility prior**, never as direct evidence.

Examples:
- typical door height;
- furniture scale;
- common slab/ceiling zone;
- ordinary human reach;
- common luminaire body sizes.

If a project decision depends on the exact value, replace the prior with actual evidence or keep a range/HOLD.

---

## 8｜Reality-near constraint rules

A proxy model is acceptable for bounded design exploration only when all applicable rules hold.

### RNC-01 Hard-anchor preservation
No proxy variable may contradict a stronger Current anchor without an explicit contradiction record.

### RNC-02 Topology before metric precision
Preserve:
- adjacency;
- order;
- branch structure;
- above/below;
- inside/outside;
- approach/return;
- visibility/blocking;
before pretending exact dimensions are known.

### RNC-03 Range before pseudo-precision
Prefer:
- `8–14 min`;
- `approx. 3–6 m`;
- `low / base / high`;
over unsupported decimal precision.

### RNC-04 Independent-cue preference
For consequential variables, seek at least two materially independent cues when reasonably available.

If only one weak cue exists:
- widen the range;
- lower the claim ceiling;
- raise sensitivity;
- do not fabricate a second source.

This is a preference, not a universal numeric gate.

### RNC-05 Cross-variable consistency
Related values must close together.

Examples:
- segment times must reconcile with total route time;
- floor-to-floor height must reconcile with visible stairs / levels;
- room area must reconcile with plan footprint;
- drainage direction must reconcile with terrain;
- fixture spacing must reconcile with ceiling/module geometry.

### RNC-06 Temporal consistency
A precise but stale source may be less useful than a less precise current source for an operational/current-condition question.

### RNC-07 No unsupported propagation
Do not transfer confidence from one anchored element to adjacent unobserved elements merely because they appear nearby.

### RNC-08 No analog overwrite
Precedent / typical values may only bound plausibility.

### RNC-09 Reconstruct only what the decision consumes
Avoid inventing complete site detail that no current design decision requires.

### RNC-10 Reversible design under uncertainty
Where uncertainty is material, prefer design decisions that remain valid or adjustable across the plausible envelope.

---

## 9｜Reality divergence test

Before a proxy variable/model is consumed, attack it for divergence from reality.

Check as applicable:

1. **source contradiction** — does another credible source disagree?
2. **topology contradiction** — does the model break known adjacency/order/branch relations?
3. **scale contradiction** — is the inferred scale incompatible with known objects?
4. **terrain contradiction** — do elevation, slope, valley/ridge and water direction disagree?
5. **time-distance contradiction** — do route time, distance and terrain become implausible together?
6. **capacity contradiction** — does a local capacity exceed another known bottleneck?
7. **image-perspective contradiction** — does the inferred geometry fail across another viewpoint?
8. **domain plausibility contradiction** — would the value be extraordinary without evidence?
9. **temporal contradiction** — are sources describing different versions / seasons / construction states?
10. **professional-interface contradiction** — does the proxy conflict with architecture/civil/structure/MEP/operations authority?

Do not resolve contradictions by averaging them away.

Record the cause, affected variables and claim impact.

---

## 10｜Decision-tolerance rule

The important question is not “is the proxy exact?” but:

> Is the remaining uncertainty small enough relative to the design decision being made?

Use the existing Measurement Uncertainty logic.

### Continue provisionally when
- the design decision remains the same across the plausible range;
- the relation/topology is stable;
- uncertainty does not cross a safety/compliance/technical decision boundary;
- the design is reversible or adjustable when better evidence arrives.

### Require sensitivity / alternatives when
- different plausible values lead to different design decisions;
- one variable dominates the design outcome;
- the range overlaps an acceptance boundary.

### HOLD the affected claim when
- the design only works at one narrow unverified value;
- safety, egress, accessibility, structure, drainage, code, legal boundary or other controlling professional claim depends on unknown actual geometry;
- contradictory sources cannot be reconciled within the current claim.

`DESIGN ROBUST ACROSS RANGE → PROVISIONAL CONTINUATION MAY BE VALID`.

`DESIGN WORKS ONLY AT ONE GUESS → HOLD`.

---

## 11｜Scenario discipline

Use scenario bands to keep design moving.

A common pattern may be:

`LOW / BASE / HIGH`

but the project may use another bounded representation when more appropriate.

Each scenario must state:
- what changes;
- why the range exists;
- which anchor constrains it;
- which design decisions change;
- which decisions remain stable;
- what future evidence replaces it.

Scenario values are not “three guesses”; they are a sensitivity model.

Do not use a universal percentage padding.

---

## 12｜Professional-domain consumption

The proxy model may feed different professional domains at different claim ceilings.

### Architecture
May support:
- site organization;
- massing/route relationships;
- approximate level/footprint coordination;
- option-space exploration.

Does not prove:
- survey;
- exact setbacks/boundaries;
- final accessibility/egress;
- construction geometry.

### Interior
May support:
- approximate room/ceiling/service-zone geometry;
- furniture/equipment fit studies;
- preliminary circulation and sightline tests;
- reconstruction from plans/photos/known elements.

Does not prove:
- final clear dimensions;
- code/accessibility/fire compliance;
- exact RCP/service positions;
- fabrication dimensions.

### Landscape
May support:
- route/topology;
- terrain/landform concept;
- viewpoint relationships;
- planting-zone/water-system concept;
- grading/drainage sensitivity studies.

Does not prove:
- survey surface;
- hydraulic performance;
- soil/vegetation condition;
- statutory accessibility/safety.

### Lighting
May support:
- approximate room/ceiling/material geometry;
- fixture family/position concept;
- preliminary scene and photometric sensitivity models.

Does not prove:
- final photometric result;
- glare/adaptation claim;
- installed aiming/focusing;
- commissioning.

### Structural
May support:
- span/support topology;
- structural concept-family exploration;
- approximate load-path geometry.

Does not prove:
- member capacity;
- connection adequacy;
- foundation adequacy;
- code compliance.

### MEP / Systems
May support:
- service-zone/interface planning;
- equipment-space scenarios;
- route coordination envelopes.

Does not prove:
- final loads/flows/pressure/voltage;
- equipment selection;
- commissioning.

### HCD / Digital
May support:
- environmental/device/connectivity scenarios;
- offline/degraded-state design;
- location/context assumptions.

Does not prove:
- user research;
- usability;
- live service state.

### Product / CMF
May support:
- scale reconstruction from known components;
- assembly hypothesis;
- material/process plausibility.

Does not prove:
- production tolerance;
- hidden assembly;
- certified material/process performance.

---

## 13｜Required outputs

For a consequential remote/proxy reconstruction, produce as applicable:

1. `REALITY_ANCHOR_REGISTER`
2. `SOURCE_COVERAGE_REGISTER`
3. `RELATION_GRAPH_OR_MAP`
4. `PROXY_VARIABLE_REGISTER`
5. `PROXY_MODEL_EDITABLE_ARTIFACT`
6. `SCENARIO_ENVELOPE`
7. `CONTRADICTION_RESIDUAL_LOG`
8. `SENSITIVITY_ROBUSTNESS_READBACK`
9. `FIELD_OR_BETTER_SOURCE_REPLACEMENT_REGISTER`
10. `REMOTE_PROXY_RECONSTRUCTION_RECEIPT`

The editable artifact may be:
- GIS;
- CSV/JSON;
- CAD/vector;
- SVG;
- Blender/native geometry;
- spreadsheet/model;
- HTML/JS;
- another owner-native source.

A screenshot is not the authoritative proxy model when an editable source exists.

---

## 14｜Receipt fields

A `REMOTE_PROXY_RECONSTRUCTION_RECEIPT` should record:

- decision question / consumer;
- Current authority refs;
- reconstruction scope;
- source refs / dates / freshness;
- reality anchors;
- proxy variable refs;
- method(s);
- range/uncertainty meaning;
- cross-checks;
- contradictions / unresolved residuals;
- sensitivity result;
- robust / sensitive decisions;
- claim ceiling;
- field-only or professional-HOLD items;
- next evidence that should replace each consequential proxy;
- does-not-prove.

---

## 15｜Failure attacks

Reject / revise when:

- a proxy value is labeled measured;
- one image gives an exact dimension with no scale/control lineage;
- one map source is traced into many derivative sites and counted as independent triangulation;
- official route time is converted to exact path length without terrain/stop uncertainty;
- a DEM is used as construction survey;
- a cable/equipment rating becomes site/system capacity;
- a typical door/furniture/human dimension becomes site fact;
- low/base/high values are arbitrary percentages around a guess;
- the “base” value is chosen because it looks good in the design;
- an analogy overrides stronger site evidence;
- the model violates known route/topology relations;
- uncertain adjacent regions inherit the confidence of an anchored region;
- an old image/map silently defines Current condition;
- a field-only safety/compliance/structural claim is promoted because the proxy looks realistic;
- a design survives only at one unverified narrow value but is still called robust;
- field/new authoritative evidence arrives and the proxy is not reopened.

---

## 16｜C04 practice provenance

C04 Remote Site Reconstruction v0.3 and QJ-A Remote Evidence are the first bounded project practice precedent for this extension.

Observed useful mechanisms:
- official/triangulated/inferred/field-only separation;
- current route topology reconstruction without claiming survey geometry;
- use of official cable length/elevation difference while explicitly refusing to call the chord ratio terrain grade;
- remote route time allocation reconciled with an official ~3-hour total;
- low/mid/high capacity stress tests;
- system capacity defined by bottleneck rather than cable rating;
- field-only dimensions/safety/structure/network/maintenance kept open;
- relation-level design allowed to continue.

Important C04 lesson:

`REALITY-NEAR PROXY = STRONGLY CONSTRAINED MODEL + EXPLICIT UNKNOWN`.

It is not:

`A CONVINCING DRAWING + UNSOURCED NUMBERS`.

---

## 17｜Maturity

Current maturity:

`CANDIDATE EXTENSION / EXISTING RESEARCH OWNER / C04 PRACTICE-DERIVED / FIELD-SURVEY OWNER ALIGNED / MEASUREMENT-UNCERTAINTY OWNER ALIGNED / GOLDEN REGRESSION REQUIRED / CROSS-DOMAIN REAPPLICATION REQUIRED / NO PROMOTION`.

Promotion requires:
- at least two domain-distinct project reapplications beyond C04 route/site evidence;
- one case where sensitivity forces an option/HOLD rather than a single “best guess”;
- one case where better field/authoritative evidence replaces a proxy and change propagation is correctly bounded;
- independent Research/professional review that the method improves realism without fabricating field truth.

`PROXY REALITY SHOULD REDUCE DESIGN DEVIATION, NOT HIDE EVIDENCE GAPS`.
