---
name: oleander-technical-drawing
description: Create, deepen, edit, reconstruct, and audit OLEANDER technical and spatial-analysis drawings as evidence-bound professional design documents. Use whenever the user mentions plans, sections, elevations, construction details, nodes, exploded/assembly drawings, fabrication drawings, dimensional drawings, lineweight, projection, section cuts, callouts, tolerances, material/CMF schedules, circulation/flow/mobility analysis, route hierarchy, direction arrows, parking/transit networks, exact/pixel-level drawing reconstruction, title blocks, SVG/DXF/PDF drawing output, Illustrator/CAD drafting, or asks to make a drawing more professional rather than merely more detailed.
compatibility: Works with CAD/vector tools, Blender or other geometry-authoring tools, Illustrator/Inkscape, SVG/DXF/PDF workflows, and OLEANDER review/delivery-QC conventions.
---

# OLEANDER Technical Drawing

Candidate revision: `v0.2 / PR #172`.

A technical drawing is a design-and-communication instrument, not a decorated screenshot. Preserve authoritative geometry and truth state first; then make spatial, constructive, dimensional and visual relationships readable enough that the intended reader does not need to guess.

This skill is independent from `oleander-3d-pipeline`, `oleander-story-and-board`, and `oleander-delivery-qc`:

- 3D pipeline owns model/exchange authority and derived axonometric geometry.
- Technical drawing owns 2D/2.5D drawing logic, spatial-analysis geometry, dimensional communication, detail hierarchy, technical reality checking and drawing-specific review.
- Story/board owns placement of approved drawings inside presentation surfaces.
- Delivery QC owns release-package preflight; it does not grant drawing-design approval.

`ARTIFACT EXISTS ≠ DRAWING PASS ≠ ENGINEERING PASS ≠ FIELD PASS ≠ MAIN KEEP`.

`NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS` applies to technical drawing sets. Simplification may improve hierarchy, but it must not delete necessary technical proof, audience/use information, maintenance logic, field-open conditions, network topology or dimensional truth state.

## 0. Execution router — resolve the drawing problem before drawing

Do not begin by selecting a visual style. Resolve these five axes first:

1. **Discipline** — architecture/interior, landscape/site, industrial/product, structural/support explanation, fabrication/assembly, spatial/design analysis, circulation/mobility analysis, or a declared hybrid.
2. **Maturity/status** — DESIGN STUDY, TECHNICAL EXPLANATION, COORDINATION, FABRICATION, CONSTRUCTION.
3. **Decision** — what exact uncertainty or relationship must the drawing close?
4. **Authority** — which source controls geometry, dimensions, materials, site facts, network relations and specialist design?
5. **Output condition** — physical sheet/display size, scale, vector/raster requirements, downstream CAD/Illustrator/PDF use and intended reader.

Then load the supporting reference appropriate to the task:

- `references/DISCIPLINE_PROFILES.md` — profession-specific view sets, checks and failure patterns.
- `references/GRAPHIC_SYSTEM.md` — line hierarchy, section/plan grammar, dimensions, callouts, hatches, typography, scale and multi-scale review.
- `references/ANALYSIS_DRAWING_SYSTEM.md` — spatial/design analysis truth states, evidence→finding→decision chains and analysis-specific visual hierarchy.
- `references/SPATIAL_TRANSLATION_PROTOCOL.md` — **mandatory whenever a source/project phenomenon is turned into simplified point/line/band/field/network/section/vector geometry**. Resolves `SOURCE / PHENOMENON → SPATIAL MODEL → GEOMETRIC ABSTRACTION → GRAPHIC CARRIER → VISUAL ENCODING`, including registration class and preserved/relaxed invariants before styling.
- `references/SOURCE_CARRIER_PRECEDENCE.md` — **mandatory whenever the source already contains a decision-relevant visual/spatial carrier** such as an official guide, map, GIS layer, CAD/model view, section, annotated photograph or technical diagram. Run it before redraw/generalization; classify carrier adequacy and default to reuse when the source is already sufficient/authoritative.
- `references/FLOW_DIRECTION_ANALYSIS.md` — mandatory for circulation, mobility, route hierarchy, direction markers, parking/transit networks or exact reconstruction of flow analysis. Adds route-edge/node graph, direction-marker taxonomy, base binding, FN-C0…FN-C3 and flow-specific machine/review gates.
- `references/REFERENCE_RECONSTRUCTION_FIDELITY.md` — required when reconstructing a supplied drawing/reference rather than adapting its system.
- `references/PIXEL_FORENSIC_PROTOCOL.md` — required for explicit pixel-level/exact reconstruction claims.
- `references/MULTILAYER_RELATION_RECONSTRUCTION.md` — required for stacked analytical atlases, repeated bases and callout-heavy references.
- `references/EDITORIAL_CALLOUT_FIDELITY.md` — required when side-icons, leader landing and dense route/street typography are material fidelity carriers.
- `references/REALITY_CHECK.md` — design action → system → reference → value/range → sensitivity → FIELD/engineer verify protocol.
- `templates/DRAWING_EXECUTION_TEMPLATE.md` — execution registers and TD-G0…TD-G8 review carrier.

A substantial task should not skip these because a previous drawing already exists. Existing pixels may be provenance, not current authority.

### Spatial translation + source-carrier precedence routing rule — mandatory

For any spatial/design analysis, landscape/site analysis, route/node/field/view/threshold/drainage/ecological relation, source-map interpretation, or source-bound analytical redraw, the main router must execute this order before graphic polishing:

`SOURCE / PHENOMENON → SPATIAL MODEL → SOURCE-CARRIER ADEQUACY / PRECEDENCE → GEOMETRIC ABSTRACTION → GRAPHIC CARRIER → VISUAL ENCODING`.

1. Resolve Stage 1–2 in `SPATIAL_TRANSLATION_PROTOCOL.md`: what exists/is claimed, what the source proves/does not prove, and the real spatial ontology (`surface / corridor / centerline / edge / boundary / network / point event / threshold / view relation / field / sequence / other declared model`).
2. Before Stage 3, invoke `SOURCE_CARRIER_PRECEDENCE.md` when a visual/spatial source carrier exists. Classify `SOURCE_CARRIER_ABSENT | INSUFFICIENT | SUFFICIENT | AUTHORITY`.
3. If the source carrier is `SUFFICIENT` or `AUTHORITY`, default to `REUSE_DIRECT`. Any `TRACE_BOUNDED | DERIVE_REQUIRED | GENERALIZE_REQUIRED | SCHEMATIZE_SEPARATELY | REDRAW_JUSTIFIED` decision requires a material analytical, editability, transformation or output reason; aesthetic cleanliness, style matching, composition or easier coloring are not enough.
4. If new geometry is still required, return to `SPATIAL_TRANSLATION_PROTOCOL.md` and declare `TRACE | DERIVE | GENERALIZE | SCHEMATIZE | INFER | DESIGN`, registration class, preserved/relaxed invariants, carrier type, source binding and `does_not_prove` before selecting lineweight/color/icon/arrow treatment.
5. Only after this route is resolved may the task continue into `FLOW_DIRECTION_ANALYSIS`, `GRAPHIC_SYSTEM`, reconstruction/pixel modules, or technical reality/detail modules as applicable.

Hard boundaries:

`SEMANTIC IDENTIFICATION ≠ VALID SPATIAL TRANSLATION`.

`SOURCE EXISTS ≠ REDRAW REQUIRED`.

`CLEANER GRAPHIC ≠ BETTER SPATIAL TRANSLATION`.

`TOPOLOGY-BOUND / SEQUENCE-BOUND / DIAGRAM-ONLY ≠ MAP-BOUND`.

Machine structure check when the register is material: `tools/validate_spatial_translation.py`. Machine PASS proves register consistency only; it does not prove source interpretation, visual quality, field truth or Design KEEP.

### Reconstruction routing rule

If the task says `1:1`, `pixel-level`, `像素级复刻`, `exact reconstruction`, or equivalent, visual similarity is not enough. Route through the reconstruction references and keep these axes separate:

`REFERENCE FIDELITY ≠ SEMANTIC EDITABILITY ≠ TECHNICAL TRUTH ≠ DESIGN KEEP`.

If the reference is a flow/mobility diagram, also separate:

`PIXEL FIDELITY ≠ FLOW TOPOLOGY FIDELITY ≠ ROUTE-TO-BASE BINDING ≠ DIRECTION-MARKER FIDELITY`.

## 1. Declare drawing status before drawing

Every sheet/view must declare one of these states:

1. `DESIGN STUDY` — explores geometry, proportion, relation or assembly logic; not fabrication/construction authority.
2. `TECHNICAL EXPLANATION` — communicates how a design is intended to work using source-grounded or explicitly provisional information.
3. `COORDINATION` — coordinates interfaces between systems/disciplines; unresolved interfaces remain open.
4. `FABRICATION` — may drive making only when dimensions, tolerances, materials, finishes, interfaces and responsible authority are resolved for that scope.
5. `CONSTRUCTION` — may drive site construction only when required field/engineering/code approvals and project authority are resolved.

Never visually imitate a fabrication/construction drawing while the truth state is only study or explanation. Use explicit markers such as `NTS`, `PROVISIONAL`, `FIELD OPEN`, `VERIFY`, `ENGINEERING REVIEW REQUIRED`, or `NOT FOR CONSTRUCTION` where applicable.

### Status cannot be inferred from appearance

A dense title block, many dimensions, realistic fasteners or professional hatch do not upgrade a study. Promotion depends on authority and review, not visual resemblance to issued construction/fabrication documents.

## 2. Resolve source authority

Before editing geometry, create a compact authority table:

| Information | Current authority | Revision/date | Allowed use | Open conflict |
|---|---|---|---|---|
| geometry | CAD/BIM/model/survey/etc. | ... | derive views only / editable | ... |
| dimensions | measured/locked/design-recommended | ... | verified / provisional | ... |
| material/finish | CMF schedule/spec | ... | approved / candidate | ... |
| structure/connection | engineer/detail/reference | ... | explanatory / approved | ... |
| site/context | survey/map/field/source | ... | observed / inferred | ... |
| circulation/network | plan/map/reference/observed route | ... | source / derived / inference / decision | ... |
| safety/access | code/specialist/project rule | ... | review / approved | ... |
| manufacturer/system | supplier technical data | ... | bounded candidate / selected | ... |

Authority order is project-specific; do not invent a universal hierarchy. A render, AI image, presentation diagram or raster screenshot does not become dimensional authority merely because it looks resolved. If a derived view conflicts with the authoritative geometry, the authority wins until a documented design revision changes it.

### Source snapshot requirement

For a material drawing revision, bind the drawing to the exact source revision or source object ID when available. Record enough identity that another reviewer can distinguish:

`CURRENT AUTHORITY` vs `DERIVED DRAWING` vs `REFERENCE` vs `SUPERSEDED/HISTORY`.

Do not let recency alone revive obsolete geometry.

## 3. Build a drawing set, not an isolated picture

Choose only the views needed to answer the drawing's decision question. Typical set logic:

- `GA / GENERAL ARRANGEMENT`: overall location, orientation and principal relations.
- `PLAN`: horizontal organization, clearances, interfaces and movement.
- `ELEVATION`: vertical relation, envelope, alignment and finish boundaries.
- `SECTION`: cut relation, depth, level, support, ground/water/build-up and human scale.
- `LONGITUDINAL PROFILE`: route/grade/sequence/drainage relationship when required.
- `FLOW / CIRCULATION ANALYSIS`: editable base-bound route graph, route hierarchy, nodes, direction markers, entries/exits, labels, modes and operational states.
- `DETAIL / NODE`: local interface, fixing, edge, joint, drainage, safety or maintenance condition.
- `EXPLODED / ASSEMBLY`: part identity and assembly order; not a substitute for exact interface detail.
- `PART / FABRICATION`: manufacturable geometry, dimensions, tolerance and finish for one part/scope.
- `CMF / MATERIAL MAP`: material ID, boundary, direction, finish and schedule linkage.
- `INSTALLATION / MAINTENANCE`: access, removal, replacement, inspection or sequence when feasibility depends on it.

A detail must have a traceable parent view. A parent view must show where the detail comes from. Do not let an attractive exploded axon replace plan/section information needed to resolve interfaces.

A circulation analysis must have a traceable spatial base. Do not let route labels or large arrows replace missing route geometry, branch/merge structure or base binding.

### Node ladder

Use the smallest necessary ladder:

`CONTEXT / GA → PARENT PLAN OR SECTION → INTERFACE DETAIL → CONNECTION ENLARGEMENT → COMPONENT / FOUNDATION / EDGE DETAIL`

Each child view must answer a question the parent cannot answer at its scale. A child detail that only repeats information is clutter, not depth.

## 4. Discipline-specific routing

Do not use one generic drafting recipe across all design fields. Apply the relevant profile in `references/DISCIPLINE_PROFILES.md`.

At minimum:

- **Architecture/interior** must resolve grids/levels, cut/beyond, build-up, clearances and coordination boundaries.
- **Landscape/site** must distinguish existing/proposed/inferred/FIELD OPEN, slope/grade/drainage/edge/vegetation and maintenance realities.
- **Industrial/product** must preserve CAD authority, part/assembly relation, functional dimensions, mating surfaces, serviceability and CMF state.
- **Structural/support explanation** must make support/load-transfer intent and substrate/interface logic visible while keeping specialist sizing authority separate.
- **Fabrication/assembly** requires controlling geometry, tolerance basis, material/finish state, interfaces and assembly feasibility before permission to make.
- **Spatial/design analysis** must keep source/evidence/inference/constraint/decision states distinguishable and graphically traceable.
- **Circulation/mobility analysis** must preserve route-edge/node topology, route hierarchy, spatial-base binding, direction-marker meaning, external continuation, route-linked labels and mode-symbol ownership.

For hybrid work, declare which profile governs each view or technical question.

## 5. Projection and view coherence

For orthographic work:

- declare projection method when relevant;
- keep plan/elevation/section geometry aligned to the same locked source;
- identify section/cut direction explicitly;
- use consistent datums, levels, grids or local reference axes;
- do not silently change camera, crop, orientation or scale between comparison views;
- use hidden lines only when they add decision-relevant information;
- use local enlargements for dense interfaces rather than forcing all detail into the parent view;
- when a detail is rotated for readability, clearly indicate orientation so rotation is not mistaken for geometry change.

For axonometric/exploded views, lock camera/projection and derive geometry from the authoritative model where possible. Labels and explanatory graphics remain separate vector layers from the geometry source.

### Cross-view invariant

The same interface cannot be drawn one way in plan, another way in section and a third way in exploded view unless a documented state/variant explains the difference. Cross-view contradiction is a geometry failure, not a presentation preference.

### Flow-network coherence invariant

For circulation/mobility work, the network is also a geometry system. The same route/node cannot silently move, reconnect, reverse direction or change class between views/panels unless a documented state/scenario explains the difference.

For analytical atlases:

`GEOMETRY_MASTER ≠ RENDERED_BASE_INSTANCE`.

Use one recoverable source geometry where appropriate, but record per-panel transform, visibility/occlusion, line/tone treatment and theme/network state. Reusing one identical rendered base in every panel is wrong when the source intentionally fades, omits, masks or emphasizes different base objects.

## 5A. Flow / circulation / mobility analysis gate

When movement, access, mobility or directional sequence is the main subject, load `references/FLOW_DIRECTION_ANALYSIS.md` and build a `FLOW_NETWORK_REGISTER`.

Minimum semantic graph:

`BASE_GEOMETRY → ROUTE_EDGE → ROUTE_NODE → ROUTE_CLASS → DIRECTION_MARKER → ENTRY/EXIT/CONTINUATION → ROUTE LABEL/STATE/SPEED → MODE SYMBOL`.

Hard rules:

1. A flow line is not a decorative polyline. It must have an explicit analytical/traversal role and, when applicable, a base carrier.
2. A direction arrow is an event on a route or analytical vector. Record its function class and owner; do not apply one generic marker family to route direction, callout pointers, external continuation and orientation marks indiscriminately.
3. Directed edges that require direction evidence must own markers; marker orientation must follow local route tangent within the declared reconstruction/design tolerance.
4. Primary/secondary/local/external/closed/service classes remain separate objects and graphic classes when the information is decision-relevant.
5. Branch/merge/junction/entry/exit positions are topology, not decorative placement.
6. Street names, speed labels and state labels must bind to the correct route/street edge. Correct text on the wrong segment is a relation failure.
7. Parking/transit/bicycle/service symbols must bind to a registered route/node or be explicitly classified as free-standing context.
8. For strict reconstruction, inventory recoverable route classes, edge/node topology, marker policy and repeated symbol density before pixel polishing.
9. If source-route carrier recovery is materially low, stop font/antialiasing/JPEG micro-tuning and return to topology/base binding. Do not describe structural route omissions as renderer residual.
10. `FN-C0…FN-C3` flow-network claim level remains separate from `RF-C0…RF-C3` reconstruction fidelity and from TD/Design review.

Machine structure check: `tools/validate_flow_network.py`.

Machine PASS proves only registered graph consistency. It does not prove complete source inventory, route planning validity, visual fidelity, pixel fidelity, site truth or Design KEEP.

## 6. Scale is a decision tool

Choose view scale from the technical question rather than habit. Use `references/GRAPHIC_SYSTEM.md` for the scale-selection logic.

- Context scale answers `WHERE / SYSTEM RELATION`.
- Arrangement scale answers `PRINCIPAL GEOMETRY / MOVEMENT / LEVEL / CLEARANCE`.
- Network scale answers `ROUTE / NODE / BRANCH / DIRECTION / MODE / CONTINUATION`.
- Detail scale answers `BUILD-UP / JOINT / EDGE / FIXING / DRAINAGE / TRANSITION`.
- Component/fabrication scale answers `EXACT PART / DATUM / HOLE / SLOT / RADIUS / TOLERANCE / MATING`.

Write scale per view or mark intentionally `NTS`. If a scaled drawing is placed into a board/web page and digitally resized, do not leave a false printed scale statement. Use a trustworthy scale bar or update the view metadata.

## 7. Dimensioning is a design test

Dimensions must communicate design intent, not merely fill empty space.

Before adding a dimension, classify it as:

- `AUTHORITY / VERIFIED` — measured or locked by the approved source;
- `LOCKED DESIGN VALUE` — approved design value but not necessarily field-measured;
- `DESIGN RECOMMENDATION` — selected design value with rationale;
- `RECOMMENDED RANGE` — bounded design range where a single number is not yet authoritative;
- `REFERENCE` — informational only, not controlling;
- `DERIVED / NOT FIELD MEASURED` — calculated or measured from bounded source geometry/image;
- `FIELD VERIFY` — cannot be closed remotely/currently;
- `TBD` — unresolved and not safe to guess.

Rules:

1. Dimension from stable datums/interfaces instead of arbitrary visible edges when function depends on datum relationships.
2. Prefer the minimum controlling dimension set; avoid redundant or contradictory closed chains.
3. Show critical clearances, gaps, offsets, thicknesses, radii/chamfers, hole/slot position and interface heights where they affect fit, safety, assembly, drainage, access, maintenance or visual intent.
4. Tolerance only what has a functional/manufacturing reason and an appropriate authority basis. Do not invent precision to make a sheet look professional.
5. Keep nominal size, tolerance, field uncertainty and design range conceptually separate.
6. If a dimension is source-derived by calculation or image/geometry measurement, record method, units and uncertainty outside or alongside the drawing record.
7. Do not duplicate a controlling dimension across views unless the drawing convention requires it and discrepancy risk is managed.
8. A qualifier such as `FIELD VERIFY`, `REF`, `RANGE` or `TBD` must remain visually bound to the value it qualifies.
9. Dimension chains must reflect functional control. A visually complete chain that creates contradictory closure remains a failure.
10. Where field geometry is unknown, locate the interface to a field datum/verification point instead of inventing the field surface.

Mechanical GD&T may use ASME Y14.5 or the project's designated GPS standard when applicable, but this skill does not imply GD&T competence or compliance by default. Discipline-specific engineering review remains required.

## 8. Technical reality check — do not invent professional-looking certainty

For every critical technical issue involving structure/support, foundations, anchors, fasteners, slopes, drainage, safety, clearances, materials, manufacturing or tolerances, use the protocol in `references/REALITY_CHECK.md`:

`DESIGN ACTION → SYSTEM → APPLICABLE STANDARD / ENGINEERING REFERENCE → RECOMMENDED VALUE OR RANGE → SENSITIVE FACTORS → FIELD / ENGINEER VERIFY ITEMS`

### Remote-design continuation rule

Missing field evidence is not a reason to stop design or reduce professional depth. If the field cannot yet be closed:

`CONTINUE DESIGN WITH BOUNDED RECOMMENDATION → SHOW VALUE/RANGE + BASIS → IDENTIFY SENSITIVITY → CREATE FIELD-VERIFY SLOT → KEEP PROMOTION GATE OPEN`.

This is mandatory for OLEANDER work with `FIELD OBSERVED=0` or `FIELD MEASURED=0` when technical decisions still need to be developed.

### Evidence ladder

Prefer, in order:

1. current project authority;
2. applicable code/standard/specialist requirement;
3. actual manufacturer/system technical data;
4. published engineering/design reference;
5. bounded built precedent;
6. calculation/geometry-derived inference;
7. image-derived estimate;
8. AI/stylistic reference.

Lower evidence may support exploration but cannot silently override higher authority.

## 9. Draw the construction/assembly logic that matters

A professional node drawing should let a qualified reader identify the intended relation without reconstructing it from prose.

When applicable, graphically resolve:

- primary load/support path or mounting logic;
- interfaces between parts/materials;
- plate/profile/member orientation;
- fastener/anchor/adhesive/weld location as evidence permits;
- edge treatment, joint, seam and tolerance/clearance condition;
- base/foundation/support relationship;
- drainage, water-shedding and corrosion-isolation intent;
- slip/trip/fall/safety edge condition;
- removal/replacement and maintenance access;
- assembly/disassembly order if it changes design feasibility;
- tool/hand/service clearance where access controls assembly;
- movement/thermal gap where movement materially affects the interface.

Text does not substitute for visible geometry. Conversely, visible geometry does not prove engineering adequacy. If structural sizing, anchorage, foundation, fire, waterproofing, electrical or other specialist design is unresolved, show the relationship needed for design coordination and mark the specialist scope open.

### Professional-node minimum

For a node presented as serious technical proof, the intended reader should be able to answer, where applicable:

`WHAT → WHERE → HOW BIG → WHAT MADE OF → HOW CONNECTED/SUPPORTED/DRAINED → HOW INSTALLED/MAINTAINED → WHAT IS STILL OPEN → WHICH SOURCE CONTROLS`.

If the reader must infer a critical connection from notes alone, the node is not complete.

## 10. Graphic hierarchy: first-read to near-read

Technical completeness cannot compensate for a flat drawing.

Default reading order:

`CUT / PRIMARY FORM → PRIMARY STRUCTURE OR SPATIAL RELATION → SECONDARY CONSTRUCTION / EDGE / INTERFACE → DIMENSION / LEADER / NOTE / HUMAN / MAINTENANCE SUPPORT → CONTEXT / FIELD-OPEN SUPPORT`.

For flow analysis:

`BASE CARRIER → PRIMARY ROUTE/NETWORK → SECONDARY/LOCAL ROUTES → DIRECTION/NODES/MODES → ROUTE-LINKED LABELS → CONTEXT`.

Use the fewest distinct graphic classes that reliably create this order at the actual delivery size. Lineweight values are output- and scale-dependent; do not treat one screen-pixel recipe as universal.

Hard rules:

- section cuts/primary profiles must read before annotations;
- primary route/network must read before route labels and editorial side-icons;
- secondary construction must remain visible at near-read without competing with the primary claim;
- route class differences must survive intended-size review when they carry different meanings;
- direction markers must not overpower the route carrier unless the source/design intent explicitly makes direction the primary claim;
- dimensions and leaders must terminate unambiguously and must not float as decorative graphics;
- humans, furniture, vegetation and maintenance figures establish use/scale only and never overpower the technical subject;
- hatch/material fills must distinguish states without burying linework;
- if a note competes with the object it describes, move/shorten/reduce the note before making all geometry heavier;
- adding more dimensions or notes is not a valid fix for poor hierarchy;
- existing/proposed/field-open states must not depend on color alone;
- line hierarchy must survive grayscale export and intended-size print/display review.

Review `FIRST READ`, `INTENDED SIZE` and `NEAR READ` separately. A clean thumbnail that loses construction or network evidence at print/detail scale remains `REVISE`.

Use `references/GRAPHIC_SYSTEM.md` for the full line/callout/hatch/typography/export grammar.

## 11. Annotation and vector integrity

Text, dimensions, leaders, symbols, title blocks, legends and core technical linework must remain vector in the editable source and vector-capable delivery formats whenever the format supports it.

- Do not rasterize labels merely to preserve appearance.
- Do not use AI-generated pseudo-text, pseudo-dimensions or image-rendered annotation as technical content.
- Raster imagery may appear as a referenced/context layer, but must not replace authoritative linework or dimensional information.
- Keep annotation on separable named layers/classes.
- Establish typography hierarchy for title, view title, dimension, note, qualifier and source/state label.
- Route/street/speed labels must remain bound to the correct network edge; a correctly rendered label on the wrong edge is not a typography-only error.
- Check collisions, overset/clipping, leader crossings and minimum readable size at the target print/view scale.
- Verify CJK/Latin font substitution/embedding in actual exported PDF/SVG when bilingual work is used.
- Do not outline all technical text by default; preserve editability unless the delivery contract requires outlined text.

### AI image boundary

AI-generated imagery may be used only as a non-authoritative visualization/reference layer. It cannot substitute for editable technical geometry, vector technical text, dimensional information, network topology, construction interfaces or field/engineering evidence.

## 12. Material / CMF communication

Where material or finish affects the drawing, use stable IDs linked to a schedule. Show, as applicable:

- substrate/material family;
- material/finish ID and approved/candidate/provisional state;
- finish boundary and transition;
- grain/brushing/weave/lay direction when function or appearance depends on it;
- coating/plating/anodizing/paint/texture/gloss specification only when source-grounded;
- substrate versus finish as separate concepts;
- edge/return/back-face treatment where visible or manufacturable;
- service/replacement implications when finish or cladding is removable;
- measurable performance properties only from applicable technical evidence.

Do not infer a hidden build-up solely from a render. Render appearance does not prove gloss, roughness, coating thickness, corrosion class, slip resistance, fire performance or durability.

## 13. Landscape/site truth and operational state

For landscape/site/public-realm work:

- distinguish existing, proposed, inferred and FIELD OPEN geometry;
- distinguish observed/measured slope from recommended or scenario slope;
- show drainage direction/low points/discharge intent where water management matters;
- do not invent root zone, geology, foundation or retaining conditions from imagery;
- make safety edges and body-scale relationships readable;
- include maintenance/access when replacement, cleaning, vegetation management or inspection changes feasibility;
- when the project has operational state logic, `UNKNOWN` must not be drawn as normal/open. Preserve NORMAL/DEGRADED/CLOSED/UNKNOWN and other current project state semantics where applicable;
- where route/access state is analyzed, bind closure/degraded/unknown states to explicit edges/nodes/zones rather than a detached legend only.

## 14. Product/fabrication truth

For industrial/product/furniture/equipment work:

- locked CAD/model outranks render silhouette for geometry;
- mating/interface dimensions are more important than decorative dimension density;
- exploded view must be backed by exact interface detail where fabrication/assembly depends on it;
- generic `±` tolerances are forbidden without functional/process basis;
- serviceability, tool access, cable/battery/component removal and assembly direction must be visible where relevant;
- candidate CMF states remain distinct from approved manufacturing specifications.

## 15. Sheet and document control

Every controlled drawing set should expose enough document metadata to identify exactly what is being reviewed:

- project/object ID;
- drawing/sheet ID and title;
- revision/status;
- date;
- author/owner and reviewer where required;
- scale or `NTS` per view;
- units;
- projection/orientation when relevant;
- source/authority revision;
- truth/status boundary;
- superseded/current state;
- discipline/profile;
- allowed/prohibited use when status could be misunderstood.

Use project title-block conventions; ISO 7200 is a reference for document-header field logic, not an automatic claim of full compliance.

## 16. OLEANDER Drawing Gates

A drawing must pass these gates independently. Do not collapse them into one score.

### `TD-G0 / INTENT & STATUS`
PASS when drawing purpose, audience, truth state and allowed use are explicit.

Blockers: unlabeled study presented as construction/fabrication authority; stale/superseded state shown as current; no defined technical decision.

### `TD-G1 / SOURCE AUTHORITY`
PASS when geometry, dimensions, materials, site/network facts and specialist assumptions trace to current authority or are explicitly provisional/open.

Blockers: invented dimensions; render/AI image treated as geometry authority; unresolved source conflict silently reconciled; old source revived by recency alone; inferred route/network state presented as observed fact.

### `TD-G2 / GEOMETRY, PROJECTION & NETWORK COHERENCE`
PASS when views agree with the same source, datum/orientation is coherent, cut/detail parentage is traceable, and decision-critical network topology remains internally/spatially coherent where applicable.

Blockers: plan/section mismatch; impossible assembly created by presentation edits; untraceable section/detail; unexplained view rotation or geometry drift; route edge crosses the wrong base carrier; missing/extra branch or merge; route/node silently reconnects across panels; directed/bidirectional state changes without documented scenario; one identical rendered base instance erases material per-panel visibility differences in a strict reconstruction.

### `TD-G3 / DIMENSIONAL INTENT`
PASS when controlling dimensions are sufficient, non-contradictory and correctly truth-labeled.

Blockers: missing critical interface dimension for claimed fabrication/construction scope; false precision; conflicting chains; unqualified derived/image-estimated value; generic tolerance without basis.

### `TD-G4 / CONSTRUCTION, ASSEMBLY & OPERATIONAL LOGIC`
PASS when the required interfaces and maintenance/assembly/operational conditions are graphically understandable for the declared scope.

Blockers: prose-only critical connection; physically impossible access/assembly; specialist design presented as resolved without authority; missing drainage/safety/service relation when decision-critical; operational closure/access conclusion exists only in prose or detached status legend while the affected route/zone is drawn as normal.

### `TD-G5 / DESIGN QUALITY & READABILITY`
PASS when first-read, intended-size and near-read hierarchy are all professional at target output condition.

Blockers: equal-weight visual noise; annotations dominate geometry; illegible detail; diagrammatic black cuts; missing technical evidence hidden by visual simplification; decorative hatch/figures overpower technical subject; flow network reduced to a few oversized generic arrows; primary/secondary/continuation routes flattened into one line class; direction markers visually dominate or point against local route tangent; repeated parking/transit/mode system simplified until the analytical density/reading changes materially.

### `TD-G6 / VECTOR, ANNOTATION & SEMANTIC INTEGRITY`
PASS when vector text/dimensions/linework survive export and annotations/analysis objects target the intended geometry without collision, ambiguity or semantic decoupling.

Blockers: rasterized technical text where vector output is required; broken fonts; pseudo-text; orphan callouts; clipped content; CJK/Latin substitution materially changes the drawing; route labels/speed labels bound to the wrong edge; mode symbols float without intended owner; path-cloud trace presented as semantic editability; flow arrows exist without recoverable owner route/function when such ownership is required by the source/design logic.

### `TD-G7 / OUTPUT & ROUND-TRIP`
PASS when editable source and delivery derivatives open independently, scales/units remain correct, and the exported PDF/SVG/DXF reproduces the approved drawing state.

Blockers: wrong scale/units; missing links/fonts; stale export; non-recoverable source; export differs materially from reviewed source; a scaled view becomes falsely labelled after board/web resizing.

### `TD-G8 / INDEPENDENT REVIEW & PROMOTION`
Production author may supply evidence but must not self-promote the drawing to `MAIN KEEP`, `PIXEL KEEP`, `PROFESSIONAL FINISH PASS`, `FABRICATION APPROVED`, or `CONSTRUCTION APPROVED`. Use the current OLEANDER review path / responsible independent reviewer and keep engineering/field approval separate.

A CI/export PASS, checksum, artifact existence or owner claim cannot override `TD-G1`–`TD-G6`.

## 17. Design Quality Gate — drawing-specific crit

`TD-G5` is not a generic aesthetics score. Review these dimensions independently:

1. **First visual threshold** — is the main spatial/constructive/analytical claim immediately legible?
2. **Composition** — do views, negative space and annotations establish a deliberate reading path?
3. **Proportion/scale** — do human/object/component relationships read plausibly without overstating field accuracy?
4. **Line hierarchy** — do cut, primary, secondary and support information remain distinct?
5. **Typography/annotation** — are IDs, dimensions, route labels and notes precise, restrained and targetable?
6. **Node readability** — can interfaces or network junctions be understood without reconstructing them mentally?
7. **Material/build-up clarity** — are real material states and boundaries distinguishable from graphic texture?
8. **Technical/analytical depth** — are drainage, edge, maintenance, assembly, access, route topology, direction, nodes/modes or other decision-critical relations present?
9. **Cross-view coherence** — do plan/section/elevation/axon/detail/analysis panels describe one object/system or documented state variants?
10. **Professional completion** — does the final derivative survive intended-scale and near-read review without looking like a default CAD export, classroom diagram, generic infographic or AI illustration?

Any one critical blocker can force `REVISE/REJECT` even when the other gates pass.

## 18. Required review sequence

Use this order before adding new content:

1. Open the actual editable/source drawing and exported derivative.
2. Confirm status, discipline/analysis profile and source authority.
3. Confirm the technical or analytical decision each view must answer.
4. Check cross-view geometry/projection and detail parentage.
5. If flow/mobility is present, inventory/verify route classes, edge/node topology, branch/merge, direction-marker functions, base binding, labels and mode-symbol ownership before typography/pixel polishing.
6. Check the dimension set and unresolved critical interfaces.
7. Run the technical reality chain on safety/structure/foundation/drainage/material/tolerance decisions.
8. Check construction/assembly/maintenance/operational logic for the declared scope.
9. Review at thumbnail/distance scale for composition and first-read hierarchy.
10. Review at intended physical/display size for line/text/dimension/network survival.
11. Zoom to near-read/detail scale for connection, callout, material, dimensional and route/node clarity.
12. Inspect vector/text/export/semantic integrity and grayscale/color-independent semantics.
13. For reconstruction, separate structural/topology mismatch from typography and renderer/JPEG residual before assigning repair priority.
14. Produce only the verdict class allowed by the current review role; producer may use `EXECUTED / SELF-CHECKED / REVIEW PENDING / REVISE / REJECT` but not self-KEEP.
15. Repair the highest-order blocker first; do not add decorative complexity or micro-pixel tuning as a substitute.
16. Re-export and repeat actual-derivative readback after every material drawing change.

## 19. Required output contract

For a substantial drawing task, return or create:

- editable authoritative/derived source (`DWG/DXF/SVG/AI` or project-native equivalent as applicable);
- vector PDF/SVG/DXF derivative where applicable;
- preview PNG only as a review convenience, never as sole technical authority;
- `DRAWING_BRIEF` stating discipline, decision, audience, status, allowed use and prohibited claim;
- `AUTHORITY_MATRIX` for geometry/dimensions/material/site/network/specialist inputs;
- `DRAWING_MANIFEST` containing IDs, revision, units, scales, source authority, truth state and dependencies;
- `VIEW_SET` defining parent/child view logic and decision per view;
- `DIMENSION_REGISTER` for critical dimensions/ranges/field-open items when complexity warrants it;
- `DETAIL/CALLOUT_REGISTER` linking parent views and node IDs where complexity warrants it;
- `FLOW_NETWORK_REGISTER` for circulation/mobility/route-hierarchy work, including route edges/nodes/classes, direction-marker ownership, base binding, route labels, modes and external continuations;
- `MATERIAL/CMF_REGISTER` when material state matters;
- `REALITY_CHECK_REGISTER` for critical technical assumptions/ranges/sensitivities/closure items;
- reconstruction-specific source/anchor/ROI/semantic/pixel evidence when exact/high-fidelity reconstruction is requested;
- `DRAWING_QA` with TD-G0…TD-G8 status and blockers;
- multi-scale Design Crit for thumbnail / intended size / near-read;
- revision log that records material design changes rather than cosmetic file churn.

Use `templates/DRAWING_EXECUTION_TEMPLATE.md` unless the project already has a stricter equivalent.

## 20. Anti-patterns — automatic REVISE/HOLD triggers

- `MORE NOTES = MORE PROFESSIONAL` — false. Fix hierarchy/geometry first.
- `MORE DIMENSIONS = MORE TECHNICAL` — false. Use controlling dimensions.
- `REALISTIC RENDER = DIMENSIONAL AUTHORITY` — false.
- `AI DETAIL LOOKS PLAUSIBLE = CONNECTION VALID` — false.
- `FIELD=0 = STOP DESIGN` — false. Continue with bounded recommendation + sensitivity + verify slot.
- `FIELD=0 = INVENT A PRECISE DETAIL` — also false.
- `EXPLODED VIEW = NODE DETAIL` — false when interface precision is still unresolved.
- `CAD DEFAULT LINEWEIGHT = PROFESSIONAL HIERARCHY` — false.
- `CLEAN THUMBNAIL = PROFESSIONAL DRAWING` — false if near-read evidence disappears.
- `A FEW BIG ARROWS = FLOW ANALYSIS` — false. Preserve graph topology, route classes, direction events and base binding.
- `STREET LABEL PRESENT = STREET NETWORK RECONSTRUCTED` — false.
- `ARROW LOOKS RIGHT = DIRECTION RELATION RIGHT` — false unless function, owner edge, position and tangent are right.
- `SHARED GEOMETRY = IDENTICAL PANEL BASE PIXELS` — false in multilayer atlases with panel-specific visibility/emphasis.
- `LOW FULL-PAGE MAE = FLOW FIDELITY` — false if route-carrier recall/topology remains poor.
- `JPEG RESIDUAL = EXCUSE FOR MISSING ROUTES` — false. Compression residual is considered only after recoverable structure is reconstructed.
- `EXPORT PASS = DRAWING PASS` — false.
- `DRAWING PASS = ENGINEERING/FIELD PASS` — false.
- `TRACEABILITY = VISUAL EXCELLENCE` — false.
- `LOGIC CORRECT = MAIN KEEP` — false.

## 21. Standards and jurisdiction routing

Use current discipline/project standards when required. Do not freeze a global project to one jurisdiction.

Before any compliance claim:

1. identify jurisdiction and discipline;
2. identify the responsible standard/code family;
3. verify current status/edition using an authoritative source;
4. distinguish drawing-convention standard from engineering/safety/performance standard;
5. obtain/check the applicable normative requirements when compliance is claimed;
6. keep project-specific requirements above generic convention guidance when legitimately authoritative.

As a cross-discipline professional anchor, this skill is informed by the published scopes of:

- ISO 128-1:2020 — fundamental requirements for technical drawing representation;
- ISO 128-2:2022 — basic conventions for lines, leaders and reference lines;
- ISO 128-3:2022 — views, sections and cuts;
- ISO 129-1:2018 + Amd 1:2020 — presentation of dimensions and associated tolerances (not the full meaning/application of tolerances);
- ISO 5455:1979 — drawing scales;
- ISO 5456-2:1996 — orthographic representation;
- ISO 7200:2004 — title-block/document-header data fields;
- ASME Y14.5-2018 (R2024) — GD&T when that standard is the project authority.

Runtime verification note: ISO states ISO 128-1:2020 remains current after its 2026 review; ISO 128-2:2022 is the published replacement for withdrawn ISO 128-2:2020; ISO 129-1:2018 remains published/current but has a new edition under development. Therefore future executions must verify status rather than assuming this list is permanently frozen.

These references define professional convention domains, not automatic compliance. If a task requires code/standard compliance, verify the applicable current edition, jurisdiction, discipline and purchased/full normative requirements before claiming compliance.

## 22. Skill success condition

This skill succeeds only when it improves both **technical truth discipline** and **drawing design quality**.

A successful result is not merely a file with dimensions or arrows. It is a recoverable, editable, source-bound drawing system in which the reader can distinguish:

`WHAT IS KNOWN → WHAT IS DESIGNED → WHAT IS RECOMMENDED → WHAT IS ONLY REFERENCE → WHAT REMAINS FIELD/ENGINEER OPEN`,

and, where spatial networks matter:

`WHAT IS THE BASE → WHAT CONNECTS → WHERE IT BRANCHES → WHICH WAY IT MOVES → WHAT MODE/STATE IT CARRIES → WHAT CONTINUES/ENDS → WHICH LABEL/SYMBOL BELONGS TO WHICH EDGE/NODE`,

while the drawing itself still meets the first-read, near-read, spatial/constructive/analytical clarity and professional-finish threshold required for OLEANDER MAIN consideration.