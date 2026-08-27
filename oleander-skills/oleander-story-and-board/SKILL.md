---
name: oleander-story-and-board
description: Turn Oleander research, data, design logic, renders, and brand strategy into coherent boards, reports, decks, storyboards, and promotional narratives. Use whenever the user mentions Oleander project compilation, exhibition boards, design books, presentations, brand stories, scripts, storyboards, key visuals, InDesign, Illustrator, Figma, PowerPoint, or connecting analysis to a persuasive narrative.
compatibility: May use Notion, documents, presentations, PDF, Figma, InDesign, Illustrator, Photoshop, After Effects, Premiere, and LibreOffice.
---

# Oleander Story and Board

Build a single evidence-to-story spine so reports, boards, decks, and films tell the same project rather than becoming unrelated artifacts.

## Narrative spine

Define:

1. Context: what situation exists?
2. Tension: what is missing, changing, or contested?
3. Insight: what did research reveal?
4. Proposition: what does Oleander do?
5. System: how does the design work?
6. Experience: what will people see, feel, and do?
7. Proof: what evidence, analysis, or prototype supports it?
8. Invitation: what should the audience believe or do next?

Every section should have one primary claim and one primary visual.

## Existing mature design / evidence first

Before rebuilding a board visual, identify the strongest current spatial/design evidence already available. Reuse, edit, currentize, restructure, or deepen it before creating a substitute.

For maps, routes, plans, sections, model views, product geometry, technical nodes, diagrams, and other spatial evidence:

- The board is a **presentation layer**, not a new geometry authority.
- Preserve locked/current/strongest mature geometry. Do not stretch, flatten, straighten, re-author, simplify, or normalize it merely to make the page cleaner.
- If a layout conflicts with authoritative geometry, change the grid, crop, sequence, image scale, or page allocation — **not the evidence geometry**.
- For alternative journeys, phases, audience modes, states, or scenarios, show differences by masking/highlighting/subsetting the authoritative source. Do not redraw every variant into a visually uniform but spatially false shape.
- If an older/current artifact has stronger spatial credibility than a new derivative, keep the stronger artifact as the design source and revise only the presentation layer. Newer file ≠ stronger design.
- Context images and renders may establish atmosphere or spatial character, but they must not visually imply a false exact correspondence to map/node geometry.

A visually stronger board that weakens spatial truth is a regression and must be REVISE/REJECT rather than promoted.

## Mixed-media evidence-role gate

When one page or sequence combines source-grounded imagery, renders, models, diagrams, sections, nodes, or prototypes, assign an explicit evidence role to each medium before layout.

Default spatial roles are:

- **Landscape / site image / source-grounded scene**: proves the experienced field, context, atmosphere, or first-read relation that is actually supported by the source.
- **Model / axon / clay study**: proves relative geometry, scale relation, sequence, massing, or spatial logic; it does not automatically prove atmosphere, field conditions, material truth, or implementation.
- **Section / node / technical drawing**: proves how a relationship can be dimensioned, supported, assembled, maintained, or checked; it does not automatically prove engineering approval, field validation, or construction readiness.
- **Render / AI-assisted visualization / prototype image**: proves a visualized design hypothesis or experience candidate only within its declared source and design boundaries.

For each primary mixed-media composition:

1. Write `PROVES` and `DOES NOT PROVE` for every medium before deciding size or placement.
2. A derivative medium must not silently become a stronger authority than the source object it was created to explain.
3. Do not allow a clean clay model, diagram, or render to become the project hero merely because it is graphically easier to control than the real landscape, product, object, or evidence source.
4. If the project claim is experiential or landscape-first, source-grounded landscape/context should normally carry the first read; the model should support the spatial relation and the technical drawing should support near-read proof.
5. If the decision question is explicitly geometric, structural, or assembly-led, a model/section/node may become the primary visual, but the role change must be intentional and named.
6. When two media show the same relation, make the correspondence readable through shared IDs, anchors, callouts, camera/section references, or adjacency. Do not rely on visual resemblance alone.
7. `Render PASS`, `Model PASS`, `Prototype PASS`, and `Field PASS` remain separate verdicts. Presentation hierarchy must not collapse them.
8. Evidence boundaries must remain adjacent to the visual when a viewer could otherwise over-read what that medium proves.
9. Run a first-read test without captions: if the viewer would infer the wrong authority or think a derivative image is the real project evidence, revise the hierarchy.
10. Run a near-read test with captions: the technical/support media must remain legible after being visually subordinated.

A mixed-media page is REVISE if it is visually polished but causes the viewer to mistake a derivative model/render/prototype for the underlying source authority.

### Interactive 3D evidence-viewer binding — candidate extension

When a model is embedded in a Web/portfolio viewer, extend the mixed-media gate rather than treating interactivity as a new evidence authority.

Declare before styling:

- `MODEL_ROLE = PRIMARY_DESIGN_OBJECT | TECHNICAL_PROOF | PROCESS_EVIDENCE | DECORATIVE_PREVIEW`;
- `PRIMARY_PROJECT_EVIDENCE`;
- `MODEL_SOURCE_ID / MODEL_SOURCE_VERSION / MODEL_SOURCE_HASH` when the source is resolved;
- `VIEW_STATES` and whether they are camera/view changes of the same source object;
- `FALLBACK_STATE` for model-load failure or unsupported runtime;
- `TRUTH_BOUNDARY` and `DOES_NOT_PROVE`.

Rules:

1. `camera-controls`, orbit, pan, zoom, hotspots, annotations, animation, AR entry, or other viewer capabilities change interaction with the carrier; they do not upgrade source, Field, Engineering, Reality, or Design authority.
2. A technical-proof viewer must not become the first-read project hero merely because motion, depth, or WebGL makes it more visually attractive than the current source-grounded project object.
3. Axon / side / section / detail states must be same-object views or named derived views with traceable source identity. A view-state switch may not silently redraw or replace the model.
4. A load failure must fail closed. Preserve model role, source status, truth boundary, and a deliberate poster/fallback; never insert unrelated or generated substitute geometry merely to avoid an empty frame.
5. The fallback poster is a carrier state, not a second model authority. If only the poster is verified, do not claim interactive-model runtime PASS.
6. Keep public-facing truth language human-readable; keep exact source/version/hash identity in the internal receipt/metadata when public codes would harm the work reading.
7. If pan/target controls can move the viewer away from the intended proof, provide a reset/recenter path or use bounded view states.
8. Screen-space annotations may improve legibility, but they must not imply occlusion, dimension, attachment, or geometry that the underlying model does not contain.
9. Responsive recomposition may change viewer size, rail position, control layout, or copy measure; it may not hide the model role/truth state on the narrow carrier.
10. Review the settled state after view transitions. A transition frame in which two views appear co-primary is a REVISE even if the final state is correct.

Required attacks:

- **MODEL-OFF** — remove/fail the model; the project claim and primary source authority must survive.
- **HERO-TAKEOVER** — thumbnail/first-read check; a support model may not outrank the project object it explains.
- **VIEW-STATE SAME-OBJECT** — switch all declared views and confirm source identity/anchors do not drift.
- **LOAD-FAIL / FALLBACK** — force an invalid or missing source and read back the real fallback pixels.
- **RESPONSIVE NATIVE VIEWPORT** — desktop and narrow carrier must preserve role/truth/status without horizontal overflow or global shrink.
- **SETTLING** — read the post-transition settled state, not only the trigger or first animation frame.
- **SOURCE-ID** — unresolved source bytes keep the viewer Candidate/HOLD; no approximate recovery by redraw or AI substitution.
- **CONTEXT-OFF** — model alone must not make a stronger site/material/engineering claim than its declared role.

Promotion test:

> Remove or fail the interactive model: the project claim and source authority must survive. Restore the model: it may deepen technical reading but must not silently become the project's stronger truth source.

## Assembly workflow

1. Pull approved claims and sources from Notion.
2. Pull validated charts from `oleander-data-viz`.
3. Pull model manifests and approved renders from `oleander-3d-pipeline`.
4. Create a content inventory before layout.
5. Resolve the strongest current design/evidence source for every primary visual; record which objects are locked and may not be re-authored by layout.
6. Establish grid, hierarchy, type system, palette, caption style, image treatment, and page/board numbering around those authority objects.
7. Produce a low-fidelity sequence before polishing.
8. Reuse the same narrative IDs across report sections, boards, deck slides, and film scenes.
9. Run content, visual, and production reviews separately.
10. For spatial primary visuals, perform an authority-preservation comparison against the strongest existing artifact before promotion.

## Deliverable variants

- Board: distance-readable hierarchy, restrained text, explicit sequence.
- Report/book: evidence depth, citations, cross-references, appendices.
- Deck: one decision or claim per slide.
- Brand story: human motivation, distinctive promise, proof, voice.
- Film storyboard: scene purpose, image, motion, narration, sound, duration, source assets.

## Required output

Return the narrative outline, content inventory, page/board/scene map, missing-assets list, production specification, and final editable/source deliverable.

For any layout containing source-bound spatial evidence, include a short authority-preservation note naming the source object and confirming what was kept unchanged versus presentation-only edits.

## Quality checks

- Claims match approved research.
- No placeholder or unlicensed asset reaches final output.
- Captions identify what, where, when, and why it matters.
- Text remains readable at target print/view distance.
- The conclusion follows from the evidence rather than visual mood alone.
- The first visual remains the real project object, journey, landscape, product, or spatial relation — not a methodology dashboard explaining it.
- Locked/current geometry is not distorted by layout convenience.
- A redesign cannot be promoted if it is visually polished but spatially less credible than the best existing artifact.
- Mixed-media compositions preserve explicit evidence roles and do not promote derivative media beyond what they can prove.
- Interactive 3D viewers preserve model/source role, fail closed on load failure, and pass MODEL-OFF / HERO-TAKEOVER / native-viewport readback before candidate promotion.
