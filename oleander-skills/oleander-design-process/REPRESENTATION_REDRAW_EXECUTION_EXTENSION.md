# OLEANDER Representation / Redraw Execution Extension

Status: `ACTIVE OWNER EXTENSION / oleander-design-process / CROSS-SKILL ROUTING`

Use when one authoritative project world must be redrawn into maps, GIS figures, plans, sections, axons, analytical cuts, experience frames, node drawings, state variants, realtime/blockout views or presentation derivatives without creating competing spatial facts.

This extension does **not** define a house style, fixed palette, fixed page template, universal GIS look, or a new presentation Skill. It binds representation choice to the existing OLEANDER Design Process and routes execution to existing owners.

## Trigger

Apply when any of the following is true:

- one project object must appear in several media or projections;
- GIS / imagery / archive / photo evidence must become design-readable;
- the task asks to redraw, trace, reconstruct, generalize, annotate, cut, project, explode, sequence, state-switch or restyle a source-bound object;
- analysis diagrams risk becoming disconnected from the same project geometry;
- a final board/film/realtime view requires a different visual language from the technical source while preserving truth;
- a remote/incomplete evidence base must be represented without pretending to be survey or field truth.

## Core rule

`ONE FACT WORLD → DECLARED REDRAW OPERATION → FIT-FOR-PURPOSE REPRESENTATION → ACTUAL READBACK`

Never use:

`NEW PAGE → NEW GEOMETRY`

unless the upstream design decision itself changed and that change is explicitly versioned.

The fixed elements are:

- Current / source authority;
- object identity and stable IDs;
- evidence class and confidence;
- geometry/topology facts that the source can actually support;
- claim ceiling / DOES_NOT_PROVE;
- project-level annotation / state grammar where Current authority defines one.

The variable elements are:

- projection;
- information density;
- crop;
- scale;
- line / fill / image treatment;
- diagram abstraction;
- camera;
- temporal state;
- atmosphere;
- presentation emphasis.

**STYLE IS A DECISION VARIABLE, NOT A PROJECT-WIDE TEMPLATE.**

Different figures may use materially different visual languages when their decision questions differ. Continuity is maintained by authority, IDs, annotation semantics, evidence/state grammar and narrative relations rather than identical styling.

## Professional-stage fit

For any professional Stage that uses representation as a working or release object, keep the Current stage spine:

`Stage → Professional Question / Decision Object → Knowledge Inputs → Operational Knowledge Mount → Required Capability Roles → Current Execution Owners / Skills → Native Outputs → Actual Readback → Independent Review → Stage Closure`

This extension only deepens the `Native Outputs / Actual Readback` path. It cannot award specialist professional closure.

## Representation question contract

Before redrawing, resolve:

`DECISION QUESTION → WHAT MUST BE PERCEIVED → SOURCE AUTHORITY → REQUIRED SCALE / VIEW CONDITION → REQUIRED REPRESENTATION → REDRAW OPS → OWNER → NATIVE MASTER → READBACK → CLAIM CEILING`

Examples:

- "Where does culture break spatially?" may require relation cuts, not a SWOT.
- "Where does design intervene?" may require a source-bound intervention masterplan, not a route dashboard.
- "How does the node work?" may require plan + section + ground/drainage + assembly + behavior, not a hero render.
- "What changes across rain/night/permission OFF?" may require same-base state redraw, not six unrelated illustrations.

## Canonical redraw operation vocabulary

Use one or more declared operations:

- `PRESERVE` — keep authority-bearing source unchanged.
- `TRACE` — extract only directly supportable visible/source geometry.
- `CLEAN` — remove noise, duplicate vertices, illegible labels or non-semantic clutter without changing the supported relation.
- `GENERALIZE` — reduce detail for a declared output scale while preserving decision-relevant topology/shape.
- `MASK` — hide non-relevant information without deleting source data.
- `EXTRACT` — isolate a material object/relation from a larger source.
- `CLASSIFY` — assign evidence, spatial, program, material, state or intervention classes.
- `OVERLAY` — add analysis/intervention/state information on top of the preserved base.
- `CUT` — derive section/cutaway/relation slice from a defined source world.
- `PROJECT` — transform the same geometry into plan/section/axon/perspective or another declared projection.
- `EXTRUDE` — produce bounded 3D massing from 2D geometry/height evidence; unknown height remains unknown.
- `EXPLODE` — separate known assembly layers/objects while preserving connection logic.
- `RECONSTRUCT` — combine multiple evidence sources into an explicitly confidence-bounded provisional object.
- `ANNOTATE` — add labels, dimensions, states, evidence marks or explanatory callouts.
- `SEQUENCE` — create ordered frames/shots from one world/state model.
- `STATE_SWITCH` — change operational/weather/time/permission layers on the same base.
- `ATMOSPHERE` — add non-authoritative experiential treatment; must remain presentation/experience evidence only.

Do not call a visual change a redraw operation if it silently changes geometry, evidence status or professional truth.

## Source/master/derivative chain

For source-bound representation keep, where applicable:

`RAW SOURCE → CLEAN SOURCE → AUTHORITY / CONFIDENCE REGISTER → ANALYSIS MASTER → REPRESENTATION MASTER → PRESENTATION DERIVATIVE`

Rules:

1. Raw sources are never overwritten merely to simplify production.
2. A cleaned geometry is a derivative until its relation to the source is checked.
3. A reconstructed object keeps source-by-source confidence and unresolved regions.
4. Presentation derivatives do not become survey / field / engineering authority.
5. If a stronger Current source arrives, reopen all downstream figures that depend on the superseded geometry.

## GIS / cartographic redraw contract

For GIS/spatial-data work route deterministic transformations to `oleander-data-viz`.

Required checks:

- source CRS / coordinate basis;
- date/version and temporal mismatch;
- raw versus cleaned geometry identity;
- scale-specific generalization;
- source confidence / missing data;
- topology preservation;
- raster/vector alignment where relevant;
- exported editable master (for example GeoJSON/GPKG/SVG/PDF/vector source as applicable);
- does-not-prove boundary.

Do not reuse one geometry simplification indiscriminately at every scale.

A useful hierarchy is:

- regional / village scale: settlement, primary route, water, terrain, field/edge, major heritage/public objects;
- local/node scale: building edges, lane, threshold, wall, steps, ditch, well, local ground relation where evidence supports them;
- technical scale: only measured/authoritative levels, slopes, materials, joints and construction data.

`GIS AVAILABLE ≠ SURVEY AVAILABLE`.

When exact boundary/width/level/parcel/drainage is absent, keep the figure relational or scenario-based and label it accordingly.

## Photo / image redraw contract

Classify image use before treatment:

- `EVIDENCE IMAGE` — source/field/public evidence; only truth-preserving crop/tonal/readability operations.
- `ANALYTICAL OVERDRAW` — preserved evidence image plus explicit observation/inference/assumption layers.
- `SPATIAL NARRATIVE IMAGE` — experience/camera representation bound to a known or reconstructed world; does not prove exact construction.
- `TECHNICAL IMAGE` — drawing/model evidence; must route dimensions/material/assembly to the appropriate specialist owner.
- `STATE IMAGE` — same-base normal/degraded/rain/night/permission/maintenance variant.

For analytical overdraw, separate visual grammar for `OBSERVED / INFERRED / ASSUMPTION / DECISION`. Do not bake the overlay into the only surviving source.

## 3D / axon / projection contract

Route editable 3D/world execution to `oleander-3d-pipeline`.

Prefer:

`AUTHORITY 2D / TERRAIN / SOURCE GEOMETRY → SAME WORLD MODEL → LOCKED CAMERA/PROJECTION → MULTIPLE DERIVATIVES`

Use semantic LOD:

- decision-critical objects may carry more detail;
- contextual objects may stay massed;
- distant/background objects may be simplified.

Detail level must follow the decision question, not visual spectacle.

A plan, axon, section and camera view that claim the same object must be mutually compatible. A hero image cannot repair a weaker source geometry.

## Relation-cut contract

A relation cut is not a theme panel or SWOT.

Each cut should resolve, when evidence permits:

`LOCATOR → LOCAL BASE → RELATION / FAILURE → SECTION OR OTHER NECESSARY CUT → LIVED / SOURCE EVIDENCE → DESIGN CONSEQUENCE`

Only include a section when the relation is materially vertical, sectional, hydraulic, threshold-based, visual or construction-dependent.

## Node redraw contract

For a node presented as materially developed, require the minimum relevant set:

`CONTEXT / LOCATOR + PLAN + SECTION + GROUND / LEVEL / DRAINAGE + ASSEMBLY / EXPLODED + MATERIAL + HUMAN BEHAVIOR + OPERATING STATE`

Missing authoritative dimensions, levels, drainage or permissions remain `OPEN/HOLD`; do not invent them merely to complete the visual family.

`CONCEPT EXPLODED ≠ CONSTRUCTION EXPLODED`.

## Time / state redraw contract

Use one source-bound base where the physical world is unchanged.

A state set such as:

`NORMAL / EVENT / RAIN / NIGHT / PERMISSION OFF / MAINTENANCE`

should be derived through declared layer/state changes. Record:

- what changes;
- what remains invariant;
- state trigger/authority;
- operating consequence;
- fallback;
- what is simulated versus observed.

If geometry changes materially, create a new object/version rather than disguising the change as a state.

## Narrative / cinematic / realtime route

When representation depends on time, camera, interaction or playable traversal:

- `oleander-design-process` owns experience question / flow / decision;
- `oleander-3d-pipeline` owns editable world/model/carrier;
- `oleander-motion` owns temporal/state/camera/motion behavior;
- `oleander-web-ui` owns browser interaction/UI when triggered;
- `oleander-story-and-board` owns public narrative sequence / shot/page selection.

Use:

`SAME WORLD → CAMERA / STATE / ACTION → SEQUENCE → PLAYBACK / RUNTIME READBACK`

Do not create unrelated synthetic views merely to make a sequence visually varied.

## Style selection gate

Before styling a figure, choose the visual mode from the claim.

Possible modes include:

- documentary / evidence-led;
- cartographic;
- analytical;
- technical;
- material / assembly;
- editorial;
- cinematic / atmospheric;
- state / operational;
- realtime / interactive.

Ask:

1. What should be understood in the first 3–5 seconds?
2. What relation must survive if color/style is removed?
3. What is the authoritative object?
4. Which visual treatment would falsely imply precision or certainty?
5. Does this figure need consistency with another figure, or only a shared project grammar?

Continuity may use shared IDs, annotation syntax, evidence marks, caption structure, type roles or recurring alignment anchors. It does **not** require every page to use the same palette, line density, image treatment or composition.

## Owner routing

- research/source/rights/remote proxy → `oleander-research`;
- relation synthesis / decision question / option consequence → `oleander-design-process`;
- GIS/data/map transformation → `oleander-data-viz`;
- editable world / model / axon / projected model view → `oleander-3d-pipeline`;
- technical dimensions / line hierarchy / technical issue output → `oleander-technical-drawing` when triggered;
- composition / visual hierarchy / variable visual language → `oleander-visual-design` when its Candidate route is allowed;
- image crop/masking/compositing → `oleander-image-art-direction` when triggered;
- temporal/state/camera motion → `oleander-motion`;
- final page/board/film story → `oleander-story-and-board`;
- release/package verification → `oleander-delivery-qc`.

No downstream owner may upgrade the upstream evidence level.

## Required representation register

For every material figure keep:

`FIGURE_ID / DECISION QUESTION / PRIMARY CLAIM / SOURCE AUTHORITY / EVIDENCE STATE / REPRESENTATION MODE / REDRAW OPS / PRESERVED INVARIANTS / ALLOWED TRANSFORMS / FORBIDDEN TRANSFORMS / CURRENT OWNER / NATIVE MASTER / DERIVATIVES / TARGET SCALE / ACTUAL READBACK / DOES_NOT_PROVE / REOPEN TRIGGER`.

For a figure family derived from one base, also record `BASE_WORLD_ID`.

## Actual-readback attacks

At minimum test:

- source overlay / geometry compatibility where meaningful;
- first-read at target scale;
- relation-off or color-off test;
- same-source consistency across paired/sequence/state views;
- confidence/evidence markers remain legible;
- no presentation operation silently changes a professional claim;
- no figure is visually more precise than its evidence;
- missing data remains visible rather than aesthetically filled.

## Closure / HOLD

Representation closure means the figure accurately communicates the decision object at its intended scale and preserves authority.

It does **not** mean:

- site/survey closure;
- heritage approval;
- engineering/technical validation;
- professional-domain PASS;
- human-response validation;
- implementation permission;
- Design KEEP for the whole project.

When the source world is too weak for the requested figure, return the strongest honest lower-fidelity representation and a concrete evidence-acquisition requirement instead of drawing fictitious precision.
