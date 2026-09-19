# Practice — Architectural Portfolio / School-Project Publication Digestion — 2026-09-19

**Skill owner:** `oleander-story-and-board` with upstream `oleander-design-process` / architectural CAD-native authority.
**Purpose:** digest mature architectural portfolio and school-project presentation mechanisms into reusable OLEANDER practice without copying a visual style or creating a new core Skill.
**Evidence state:** external public references are precedent / presentation evidence only. They do not establish project geometry, code, engineering or field truth.

## Public references inspected

1. Studio Matrx, **Drawings in the Portfolio**
   https://www.studiomatrx.org/students/the-design-portfolio/drawings-in-the-portfolio
   Mechanisms observed: portfolio-size redraw/recomposition, cut/edge/surface/annotation line-weight hierarchy, poche, telling crop, graphic scale, restrained color and actual arm's-length readback.

2. CEPT Portfolio, **SECOND HOME: Learning with Nature and Neighbourhood**
   https://portfolio.cept.ac.in/fa/learning-spaces-beyond-schooling-ar2028-spring-2021/second-home-learning-with-nature-and-neighbourhood-spring-2021-ug190274
   Mechanisms observed: research/activity/site/design-development sequence eventually resolves into plans, celebration section, long/short sections, elevation and wall section instead of ending in conceptual analysis.

3. Behance, **Schools for Palestine: Architecture Competition**
   https://www.behance.net/gallery/215575259/Schools-for-Palestine-Architecture-Competition
   Mechanisms observed: deployment sequence, phases, master plan, 3D section, axonometric/modularity/activity diagrams and final board form one project chain; adverse-condition logic is communicated through architectural states rather than one decorative diagram.

4. Behance, **WORKING DRAWING I — International School Project**
   https://www.behance.net/gallery/208334451/WORKING-DRAWING-I-International-School-Project
   Mechanisms observed: general notes/schedules → layout → plans → sections → wall section; technical depth is a coordinated scale cascade rather than isolated details.

5. Behance, **Perspective Sections for a National Competition**
   https://www.behance.net/gallery/240600507/Perspective-Sections-for-a-National-Competition
   Mechanisms observed: perspective section can be a major communication carrier for spatial clarity and program hierarchy when it remains grounded in the building model.

6. ArchDaily, **The Best Architecture Portfolio Designs**
   https://www.archdaily.com/872418/the-best-architecture-portfolio-designs
   Mechanisms observed: strong portfolios use different representation techniques while maintaining a coherent editorial system; creativity and visual identity must not overpower the architectural work; photoreal renders are strongest when complemented by architectural drawings and other forms of representation.

7. ArchDaily, **Rendering Styles: Different Techniques and How to Achieve Them**
   https://www.archdaily.com/960434/rendering-styles-different-techniques-and-how-to-achieve-them
   Mechanisms observed: architectural rendering is not synonymous with photorealism; collage, sketch and other modes support different narrative/communication roles and audiences.

8. ArchDaily, **Architects' Diverse Positions on Visualization: From Hyper-Realistic Renderings to Digital Collages**
   https://www.archdaily.com/941870/architects-diverse-positions-on-visualization-from-hyper-realistic-renderings-to-digital-collages
   Mechanisms observed: visualization mode changes how design is perceived; digital collage can communicate architectural quality without claiming photographic reality, while hyperreal imagery can prematurely close interpretation if used uncritically during design development.

9. Show It Better, **Realistic Site Plan**
   https://www.showitbetter.co/courses/realistic-site-plan/
   Mechanisms observed: site-plan visual treatment is a layered workflow rather than one filter — base CAD, imagery, textures, shadows, vegetation/people, final adjustments and export are distinct operations that can be bounded and reviewed separately.

10. ArchDaily, **Representation as Argument: Lyndon Neri on What Juries Look for in Architecture Competitions**
    https://www.archdaily.com/1042630/representation-as-argument-lyndon-neri-on-what-juries-look-for-in-architecture-competitions
    Mechanisms observed: graphical representation is judged through linework, drawing quality, color balance, layout, hierarchy, annotation and text as a coordinated argument, not as isolated visual polish.

## Visible fact → inference → transfer rule

### P-01 Architecture is the visual subject

**Visible fact:** mature architectural presentations commonly let plans, sections or spatial drawings carry substantial visual area while diagrams remain subordinate.
**Inference:** the reader should first understand the building, not the producer's process apparatus.
**Transfer rule:** select a real architectural drawing as primary visual owner whenever the page's decision can be proved by that drawing. Governance, evidence state and method remain visible but normally occupy supporting weight.

### P-02 A crit-wall drawing is not automatically a portfolio drawing

**Visible fact:** a full technical drawing can collapse into a flat grey field when reduced.
**Inference:** publication scale is a separate communication condition.
**Transfer rule:** derive a `PUBLICATION_VIEW` from the same native geometry; re-map lineweight, poche, annotation density, crop, context and caption at final size. Never solve reduction by redrawing different architecture.

### P-03 Plan and section have different proof roles

**Visible fact:** strong projects repeatedly pair plans with long/short/celebration sections rather than using diagrams to explain all spatial relationships.
**Inference:** plan is strongest for organization/topology/use; section is strongest for vertical/spatial/environmental relation.
**Transfer rule:** assign each figure one principal proof role and use cross-view references when the design question spans plan and section.

### P-04 Sectional perspective is proof only when geometrically grounded

**Visible fact:** perspective sections can carry spatial/program hierarchy with high perceptual clarity.
**Inference:** their value comes from revealing the same architecture more legibly, not from license to invent a more attractive building.
**Transfer rule:** bind every sectional perspective to Current plan/section/model geometry. New bridges, stairs, voids, openings or structural depth reopen DESIGN before publication.

### P-05 Operational/adverse conditions should read as building states

**Visible fact:** resilient/mobile-school examples communicate deployment, phase and activity as a sequence tied to architectural organization.
**Inference:** a state diagram becomes stronger when the reader can see what changes in the same physical system.
**Transfer rule:** for `NORMAL / AFTER-HOURS / ALERT / PROTECTED / DEGRADED`, preserve one base architecture and vary only actual state variables: lock, threshold, route, permission, occupancy/availability or justified state-specific objects.

### P-06 Technical depth should form a traceable scale cascade

**Visible fact:** working-drawing portfolios progress from layout/plans/sections to wall section and details.
**Inference:** technical detail is credible when the reader can locate it in the larger building.
**Transfer rule:** use `WHOLE → PLAN/SECTION → LOCAL ZONE → ROOM/CORE/THRESHOLD → DETAIL`, with locators and consistent IDs. Isolated detail drawings do not prove project depth.

### P-07 Diagram should explain, not substitute

**Visible fact:** diagrams are most useful when they clarify program, activity, phasing or relations adjacent to actual architectural drawings.
**Inference:** a diagram has bounded explanatory authority.
**Transfer rule:** bind spatial diagrams to the Current geometry when a spatial claim is in question. Remove color/labels as an attack: if architecture disappears, the diagram is rescuing an unresolved design.

### P-08 Representation style follows communication role

**Visible fact:** mature portfolios can combine monochrome drawings, color diagrams, collage, model photography and photoreal rendering without one technique becoming universally mandatory.
**Inference:** representation mode is selected by what must be understood, the project character and the audience—not by software prestige or visual fashion.
**Transfer rule:** define `communication role → representation mode → treatment variables → readback`; do not impose a universal OLEANDER render look.

### P-09 Non-photoreal does not mean less rigorous

**Visible fact:** collage and other deliberately non-photoreal techniques are used by established practices to communicate spatial and material ideas while retaining an open-ended reading.
**Inference:** realism level is a communication variable, not a maturity score.
**Transfer rule:** choose collage/model-like/sketch/photoreal treatment according to claim. Preserve geometry/source boundaries and never let a non-photoreal image invent spatial facts.

### P-10 Effects reinforce hierarchy; they do not manufacture it

**Visible fact:** textures, shadows, gradients, vegetation, people and atmospheric adjustment are commonly layered after the base drawing/model is established.
**Inference:** these operations are treatments applied to an already legible architectural carrier.
**Transfer rule:** require an effect-off baseline. If removing texture/shadow/grain/color makes the spatial claim collapse, repair hierarchy or geometry before adding effects back.

### P-11 Coherence is not one filter everywhere

**Visible fact:** successful portfolios often maintain consistent titles, spacing, color logic and drawing hierarchy while individual projects/views use different media and image treatments.
**Inference:** visual identity comes from recurring relationships, not identical post-processing.
**Transfer rule:** establish system rules for hierarchy, typography, semantic color and context handling; reserve strong atmospheric/collage/graphic moves as signature or local exceptions.

### P-12 Render atmosphere is a bounded proof role

**Visible fact:** architectural visualization ranges from technical/diagrammatic to highly atmospheric imagery.
**Inference:** atmospheric rendering can communicate sensory intention and experience but may make unverified material, light, weather, occupation or context feel more certain than it is.
**Transfer rule:** bind each render to a stated experiential question and truth ceiling; atmosphere may support spatial intent but cannot promote geometry, engineering, field or material evidence.

## Publication drawing grammar extracted

At portfolio / board scale, test a minimum perceptual hierarchy:

`CUT / POCHE → PRIMARY BUILDING EDGES → OPENINGS / CORE / MAJOR USE → FURNITURE / CONTEXT → DIMENSION / GRID / ANNOTATION`.

Rules:

- physical wall thickness remains native geometry;
- plotted lineweight is a communication mapping, not wall thickness;
- color is an overlay that reinforces a valid black/grey drawing rather than replacing it;
- context may fade but access, ground, orientation or site relation needed for the claim must remain readable;
- captions identify the drawing and the architectural idea/proof it carries;
- graphic scale is preferred when drawings may be resized in publication;
- no aesthetic crop may hide a material failure or qualification.

## Style / treatment grammar extracted

Use project-specific style relations rather than named looks:

`LINE → MASS/POCHE → COLOR → TEXTURE → SHADOW/LIGHT → CONTEXT → ENTOURAGE → CROP/EDGE → TYPE → EFFECT BUDGET`.

For each material relation record:

`role / invariant / variable / allowed range / exception / failure / readback`.

Static treatment uses the existing `T-VISUAL-IMAGE-OPS-001` contract. Selection must start from design intent and the minimum sufficient operator set; menu-driven effect accumulation is rejected. Keep a recoverable effect-off/source baseline.

Useful treatment roles include figure-ground separation, depth ordering, material/sensory suggestion, state distinction and a bounded signature moment. They do not include hiding unresolved geometry, converting a collage into field evidence, or making a weak diagram look authoritative.

## Architectural spread grammar extracted

Use:

`PRIMARY CLAIM → PRIMARY ARCHITECTURAL VISUAL → CO-DEPENDENT PROOF → SUPPORTING DIAGRAM / DETAIL → BOUNDED CAPTION / STATUS`.

Avoid defaulting to:

`HEADLINE + EQUAL CARDS + SMALL PLAN + SMALL RENDER + MANY ICONS`.

The page grid organizes relationships; it does not require equal visual mass.

## Portfolio sequence transfer

For architecture, a useful causal sequence is:

`CONTEXT / TASK → USER / OPERATION → RELATIONS → MASSING → PLAN → CIRCULATION / CORE → SECTION → DAYLIGHT / FACADE → STRUCTURE / MEP FIT-BACK → ROOM / DETAIL → EXPERIENCE / PROOF`.

This is not a mandatory page count. A project may reorder or expand stages when its decision structure requires it. The rule is that architectural specificity should increase rather than disappear as the story progresses.

## Anti-patterns now explicitly rejected

- treating a CAD screenshot/export as a finished portfolio drawing without target-size readback;
- making every analytical module equal-sized and equal-weight;
- redrawing simplified presentation architecture that diverges from Current CAD/model geometry;
- using color zoning as the only way a plan becomes understandable;
- using generic stair/core icons instead of resolved plan geometry when the stage requires real planning;
- inventing a bridge, room, void, threshold or protected-space object inside an axon/render because it improves composition;
- using technical details with no parent locator;
- using rendering atmosphere to hide unresolved circulation, wall, opening, structure or evidence state;
- choosing photorealism merely to imply project maturity;
- applying one LUT/filter/grain/gradient/shadow recipe to every drawing regardless of proof role;
- using texture, glow, blur, shadow or contrast as the only source of hierarchy;
- compositing people, sky, vegetation, damage or weather so that a viewer may mistake them for observed site evidence;
- making collage fragments imply one continuous factual scene when their sources do not support that continuity;
- allowing governance/process graphics to become the visual subject of an architectural portfolio unless governance itself is the design question.

## KH-LY46 reverse-application pattern

KH-LY46 is a useful application case because its Current architecture contains multiple operating states and a native architectural design-development chain. **Always resolve the live `PROJECT_STATE` / Current stage before applying this Practice; this section does not freeze or reopen a project frontier.**

At whichever Current stage first provides the required native plan/section/model carrier, prepare publication-safe derivatives without changing design authority:

- Ground / upper plan native master;
- `ARCH_REVIEW_VIEW` at declared target scale;
- same-base `NORMAL / AFTER-HOURS / DEGRADED` operation views;
- permission / service / school-PE-route overlays from the same geometry;
- plan-linked section cuts and later sectional-perspective carriers;
- one portfolio publication view whose primary owner is the architectural plan, not the governance diagram;
- one style/treatment A/B in which the same native plan is tested as a restrained technical publication view versus a bounded hybrid/atmospheric publication treatment, with geometry locked;
- effect-off, grayscale and truth-boundary readback for any treatment that materially changes first read;
- thumbnail/distance + near-read before publication acceptance.

This Practice does **not** pre-approve any KH-LY46 plan geometry, project stage or portfolio layout and must not be used to reopen an already superseded execution frontier. It only establishes transfer rules to test against whichever artifacts are Current when invoked.

## What was not imported

The study does not import any reference project's:

- palette;
- font;
- board grid;
- fixed page count;
- wall thickness;
- dimension standard;
- structural system;
- room size;
- code assumption;
- site geometry;
- imagery or rendering style.

The new style/treatment rules above therefore do not import a reference look; they define how a project-specific look must be selected, bounded, implemented and read back.

Those remain project-specific decisions or specialist evidence.

## Practice closure

Reusable mechanism absorbed into existing owners:

`PRECEDENT STUDY → ARCHITECTURAL NATIVE MASTER → JUSTIFIED DERIVATIVE VIEWS → ARCHITECTURE-FIRST PUBLICATION → TARGET-MEDIUM READBACK`.

No new core Skill is created. `oleander-design-process` continues to own architecture; `oleander-story-and-board` owns publication projection; `oleander-3d-pipeline` and `oleander-data-viz` remain downstream native-medium owners where triggered; `oleander-technical-drawing` remains Candidate and is not promoted by this Practice.
