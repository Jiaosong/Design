# OLEANDER Architectural Portfolio / Publication Extension

**Role:** owner-local extension of `oleander-story-and-board`; not a new core Skill.
**Scope:** architectural portfolios, competition boards, design books, review spreads and other publication surfaces that consume authoritative architectural plans, sections, models, diagrams and renders.
**State:** installed extension under the existing `oleander-story-and-board` execution owner.

## Why this extension exists

Architectural presentation must not become a second architecture model. Mature architectural portfolios often recompose plans, sections, diagrams, sectional perspectives and details for a different reading distance, but the publication view remains a derivative of the Current architectural source of truth.

The governing chain is:

`CURRENT ARCHITECTURE → NATIVE MASTER → REVIEW VIEW → ANALYTICAL PROJECTION → PUBLICATION VIEW → PAGE / BOARD → ACTUAL READBACK`.

`PUBLICATION POLISH ≠ ARCHITECTURAL AUTHORITY`.

## Precedent digestion loop

When external portfolios, competition boards or architectural monographs are studied, convert them into reusable mechanisms rather than style imitation:

`MATURE WORK → VISIBLE FACT → DESIGN INFERENCE → TRANSFER RULE → PROJECT A/B → TARGET-MEDIUM READBACK → REPAIR / RETEST`.

For each transferred mechanism, record where useful:

`REFERENCE / VIEW → VISIBLE FACT → WHY IT WORKS → PROJECT FIT → ADOPT / ADAPT / REJECT / HOLD → AFFECTED CURRENT OBJECT → READBACK TEST`.

Do not copy project-specific graphics, palette, typography, iconography or composition as a default. Transfer the mechanism only when it improves the current project and survives project-specific evidence, geometry and reading conditions.

## One logical artifact, many justified views

For a material architectural object, prefer:

`ONE LOGICAL NATIVE OBJECT → N JUSTIFIED REPRESENTATIONS`

rather than redrawing independent presentation geometry.

Typical representation family:

- `AUTHORING_VIEW` — full native information needed to design and revise;
- `ARCH_REVIEW_VIEW` — target-scale architecture review view;
- `ANALYSIS_VIEW` — route, permission, state, daylight, structure or other bounded overlay derived from the same geometry;
- `PUBLICATION_VIEW` — portfolio/board version with controlled annotation and hierarchy;
- `DETAIL / SECTIONAL_VIEW` — dependent proof view whose locator resolves back to the native plan/section/model.

The publication layer may change crop, hierarchy, text density, lineweight mapping, tonal hierarchy and figure grouping. It may not silently change room topology, wall/opening geometry, core position, section datum, authoritative dimension, operating state or evidence status.

## Architectural proof roles

Do not ask every drawing to prove everything. Assign a primary proof role:

- **Plan = organization / topology / use proof.** It should expose walls, openings, rooms, circulation, cores, thresholds and representative use.
- **Section = spatial / vertical / environmental proof.** It should expose level relation, height, ground, vertical circulation, daylight, structure/envelope interfaces and materially relevant occupation.
- **Sectional perspective / axon = relational experience proof.** It may clarify spatial sequence, overlap and use but remains dependent on plan/section/model authority.
- **Detail = local constructive / interface proof.** It must have a locator in a parent plan/section and may not appear as an ungrounded decorative technical fragment.
- **Diagram = explanatory projection.** It explains a bounded relation such as flow, permission, phase or state and must bind to the Current geometry when the claim is spatial.
- **Render / image = experiential visualization.** It may validate a specific spatial or experiential judgment but cannot repair invalid geometry or upgrade an OPEN technical claim.

## Primary-visual rule for architectural spreads

Every architectural spread / board / review state should identify the relation that must control first read.

Use:

`DECISION / CLAIM → PRIMARY VISUAL OWNER → CO-DEPENDENT PROOF → SUPPORTING VIEWS → BACKGROUND / CONTEXT → REQUIRED CONSTRAINTS`.

The main plan or section may legitimately occupy most of a page. Supporting diagrams should not gain equal visual mass merely because the grid has equal modules.

When two views are genuinely co-dependent, such as `PLAN ↔ SECTION` or `NORMAL ↔ DEGRADED`, the relationship between them may be the visual owner.

## Representation style, treatment and effect contract

Architectural publication style is not a final coat applied after layout. It is a controlled visual grammar that must reinforce the architectural proof role, project Design DNA, reading condition and evidence ceiling.

Use:

`COMMUNICATION ROLE → DESIRED CHARACTER → STRUCTURAL CARRIER → TREATMENT VARIABLES → EFFECT BUDGET → EFFECT-OFF BASELINE → ACTUAL READBACK`.

Do not start from a fashionable rendering or graphic effect and search for somewhere to use it.

### Style variables to resolve

Where material to the project, define the minimum sufficient relations among:

- line character and lineweight hierarchy;
- cut mass / poche / fill / hatch behavior;
- monochrome, neutral and accent-color roles;
- saturation, contrast and lightness range;
- paper/background/void behavior;
- context density and context fading;
- texture, grain, noise and material abstraction;
- shadow direction, softness, depth and opacity;
- image realism level and documentary ↔ staged position;
- collage, cutout, model-like, diagrammatic or photoreal treatment where justified;
- entourage density, scale, posture and narrative role;
- crop, bleed, frame and edge pressure;
- typography/image/drawing relation;
- plan/section/axon/render cross-media coherence.

For each material rule record, where useful:

`ROLE → INVARIANT → VARIABLE → ALLOWED RANGE → EXCEPTION → FAILURE SIGN → READBACK`.

Do not invent a universal OLEANDER architectural house style. Project Current Design DNA, the architectural claim and the actual medium decide the treatment.

### Candidate representation modes are not presets

Different projects or pages may legitimately use different representation modes. Examples include:

- **technical / monochrome precision** — line, poche, controlled grey and sparse accent;
- **restrained chromatic drawing** — strong architectural base with limited semantic or narrative color;
- **collage / material narrative** — layered textures, cutouts and deliberately non-photoreal depth when openness, occupation or material character is the communication goal;
- **atmospheric render** — controlled light/material/environment for experiential or sensory proof;
- **diagrammatic / graphic abstraction** — reduced geometry for one bounded relation such as flow, phase or permission;
- **hybrid** — native linework plus selective image, texture, tone or 3D depth when each layer has a clear role.

These are reference modes, not a style menu. Selection must follow the page's proof role and project-specific character. A collage is not automatically more conceptual; a photoreal render is not automatically more resolved; a monochrome plan is not automatically more professional.

### Treatment ownership and operator boundary

Static image/graphic treatment should use the Current `T-VISUAL-IMAGE-OPS-001` operator contract when actual image processing is required. The publication owner may define the intended relation, but the operator is selected through:

`DESIGN INTENT → OPERATOR ROLE → MINIMUM SUFFICIENT OPERATOR SET → PARAMETER BOUNDS → EFFECT BUDGET → EFFECT-OFF BASELINE → READBACK`.

Typical bounded operators may include:

- crop / mask / clipping;
- opacity and blend relations;
- tonal / contrast / color adjustment;
- controlled gradient or local depth cue;
- texture / grain / paper field;
- shadow or ambient separation;
- vector-safe highlight / outline / annotation effects;
- layer compositing and source-linked replacement.

Temporal effects remain owned by `oleander-motion`; 3D material/light/camera output remains owned by `oleander-3d-pipeline`; authoritative architectural geometry remains upstream in DESIGN. Publication composition does not gain those authorities merely because it combines their outputs.

### Effect budget

Every material effect should answer **what relation it makes easier to read**.

Useful effect roles may include:

- separate figure from context;
- establish depth order;
- focus attention on a threshold or spatial owner;
- distinguish an operational state;
- reveal material or light character;
- unify heterogeneous source media without falsifying them;
- create a bounded signature moment.

Reject or reduce an effect when:

- the architecture becomes unreadable with the effect removed;
- multiple effects compete for first read;
- glow, blur, grain, texture, gradient or shadow becomes the primary evidence;
- a treatment hides weak geometry, circulation, junctions or annotations;
- a collage implies factual continuity between unrelated sources;
- atmospheric lighting or weather implies a verified site condition that is not actually known;
- generated or composited people, sky, planting, damage, material aging or context are read as field evidence;
- an effect survives only at screen zoom and collapses at target print/view scale.

`EFFECT STRENGTH ≠ DESIGN STRENGTH`.

`ATMOSPHERE ≠ EVIDENCE`.

### Style system, signature and exception

Use the existing OLEANDER `SYSTEM_RULE / SIGNATURE_MOVE / LOCAL_EXCEPTION / EXPERIMENT` distinction for publication style.

- **SYSTEM_RULE:** recurring base drawing/typography/color/treatment relation required for coherence;
- **SIGNATURE_MOVE:** limited memorable treatment reserved for a few high-value views;
- **LOCAL_EXCEPTION:** justified deviation because a drawing/media role needs a different treatment;
- **EXPERIMENT:** unpromoted visual treatment under A/B readback.

Do not repeat a signature on every page until it becomes decorative noise. Do not force every drawing into one treatment when plan, section, diagram and render require different proof conditions.

### Cross-media style coherence

Coherence means shared visual logic, not identical filters.

Across plan, section, axon, render and diagram, preserve where applicable:

- common hierarchy of architecture versus context;
- stable semantic color roles;
- compatible line/cut mass relations;
- consistent text/caption behavior;
- deliberate relationship between photographic/material texture and vector geometry;
- controlled transitions between technical, diagrammatic and atmospheric views.

A render may be atmospheric while the plan remains restrained monochrome, provided both express the same project character and do not contradict the architecture or state semantics.

### Style / treatment readback

Add these tests when style or effects materially contribute to the publication:

1. **Effect-off test:** remove nonessential texture, shadow, grain, glow, gradient, collage atmosphere or post-processing. Does the architectural proof still survive?
2. **Grayscale test:** does hierarchy survive when color character is removed?
3. **Low-detail / thumbnail test:** does the intended owner remain dominant without relying on fine decoration?
4. **Near-read test:** do texture, shadow and image treatment preserve openings, wall edges, furniture, dimensions, captions and status notes?
5. **Cross-media test:** do plan, section, axon and render feel deliberately related without being cosmetically identical?
6. **Truth-boundary test:** could a viewer mistake a treatment, collage, weather, people or material effect for observed/verified fact?
7. **Variation test:** does a local stylistic exception remain an exception, or has it silently changed the project-wide visual system?

If effects improve mood but weaken any of these tests, keep the architecture and reduce the effect.

## Publication reduction of architectural drawings

Do not place a technical CAD sheet into a portfolio by simple scaling-down.

At the declared publication scale, re-evaluate:

- cut-wall / poche legibility;
- opening and door-swing legibility;
- stair/core readability;
- furniture/equipment density;
- room-tag and dimension collisions;
- context weight;
- section/elevation/detail markers;
- figure title, scale, legend and status boundary;
- crop and orientation;
- relation between drawing and adjacent explanatory views.

Typical publication reduction may:

- keep wall/cut geometry strong;
- keep major openings, stairs/cores, representative furniture and principal room identities;
- reduce minor dimensions, grids, minor IDs and technical notes;
- move full schedules and complete dimension chains to a technical/support view;
- fade context without deleting context required to understand access, ground, orientation or site relation.

Reduction must remain reversible to the Current source and must not erase an uncertainty, assumption, OPEN/HOLD state or critical qualification.

## Same-base state and overlay rule

For spatial state comparisons such as `NORMAL / AFTER-HOURS / ALERT / PROTECTED / DEGRADED`, default to the same base architecture geometry and change only the variables that actually change:

- door / threshold state;
- permission boundary;
- active route;
- occupied or unavailable territory;
- operational annotation;
- materially justified state-specific object.

Do not redraw a different simplified building for each state when the claim is that one building changes operation.

If the publication view requires a geometry change to work visually, the change belongs upstream in DESIGN, not in the presentation file.

## Sectional-perspective integrity

A sectional perspective or axon must resolve to the Current plan/section/model relation. Before KEEP as publication evidence, check:

- cut line / cut volume corresponds to a real parent view;
- floor and opening relationships match the parent geometry;
- stairs/cores are not invented for composition;
- structural/envelope depth is not visually asserted beyond the current evidence ceiling;
- people/furniture clarify use and scale rather than hide unresolved circulation;
- labels and overlays do not replace geometry.

If a sectional perspective introduces an upper bridge, new void, stair, room, facade opening or other architectural relation absent from Current geometry, reopen DESIGN first.

## Detail cascade

When a project needs multi-scale architectural proof, use a traceable cascade:

`WHOLE BUILDING / SITE → PLAN OR SECTION → LOCAL ZONE → ROOM / CORE / THRESHOLD → DETAIL / INTERFACE`.

Each lower-scale view should have a locator or reference path back to its parent. Do not present isolated details simply to create the appearance of technical depth.

## Architectural portfolio sequence

Sequence follows the project's causal design development rather than a generic portfolio template. A common architecture pattern is:

`CONTEXT / TASK → USERS / OPERATIONS → RELATIONS → MASSING → PLAN → CIRCULATION / CORE → SECTION → DAYLIGHT / FACADE → STRUCTURE / MEP FIT-BACK → ROOM / DETAIL → EXPERIENCE / PROOF`.

Project-specific state systems, civil-protection conditions, phasing, landscape or other first-order logic may enter earlier when required by Current Authority.

Avoid the weak sequence:

`ANALYSIS CARDS → CONCEPT DIAGRAMS → RANDOM RENDERS → SMALL PLANS`.

The architecture must become progressively more explicit as the publication advances.

## Target-medium readback

Architectural publication requires both whole and near readback at the real delivery condition.

Run as applicable:

1. **Five-second / distance read:** what becomes the first meaningful read?
2. **Thumbnail read:** does the intended plan/section owner still dominate?
3. **Grayscale / color-off test:** does hierarchy survive without decorative color?
4. **Label-reduced test:** can a trained reader still identify architecture without explanatory prose rescuing weak geometry?
5. **Near read:** are wall junctions, doors, cores, furniture, tags, scale and status notes legible?
6. **Cross-view read:** do plan, section, axon and detail describe the same architecture?
7. **State comparison read:** is the base building stable while the intended operational variables change?
8. **No-loss read:** do claim boundaries, OPEN/HOLD conditions and material qualifications remain visible where required?
9. **Style/effect-off read:** does the proof survive without nonessential visual treatment, and do retained effects have a declared role rather than decorative accumulation?

`PAGE EXISTS ≠ PUBLICATION PASS`.

`ATTRACTIVE BOARD ≠ ARCHITECTURE KEEP`.

## Handoff contract

Architectural publication input should identify:

- Current native architectural master and revision;
- authoritative versus reconstructed / assumed geometry state;
- target page/board size and reading distance;
- intended primary claim / decision for each spread;
- views allowed to derive from the native master;
- required status/legend/claim-ceiling information;
- dependencies that must update if geometry changes;
- unresolved specialist items that presentation may not hide.

Output should include:

- narrative / spread map;
- primary-visual ownership map;
- content inventory and missing-asset list;
- publication-view specification;
- editable board/book source;
- actual target-medium readback evidence;
- dependency/reopen note for any Current architecture change.

## Claim ceiling

This extension can establish a professional architecture-publication workflow and preserve the relation between Current design and portfolio/board derivatives. It cannot by itself prove:

- architecture Design KEEP;
- technical-drawing / construction-document issue status;
- field, survey or cadastral truth;
- structural, fire, accessibility, civil-protection or MEP compliance;
- rendering truth beyond the underlying model/evidence;
- final release readiness without Delivery QC.
