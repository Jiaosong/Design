# OLEANDER Technical Drawing — Graphic System

This reference turns drawing hierarchy into an executable visual system. It does not prescribe one universal millimetre lineweight table; final lineweight depends on sheet size, scale, medium, printer/plotter, display density and project standards.

Use `VISUAL_HIERARCHY_TRANSFER.md` for the cross-skill provenance behind the expanded hierarchy rules.

For explicit `1:1 / pixel-level / exact reference reconstruction / 像素级复刻` work, also load `REFERENCE_RECONSTRUCTION_FIDELITY.md`. Reference fidelity and technical truth are separate review tracks: `RF PASS != TD PASS`.

## 0. Visual hierarchy contract

Before drawing, define:

- `PRIMARY_CLAIM` — one sentence / one technical-spatial relation;
- `3S_READ` — what must dominate before notes are read;
- `30S_READ` — what system, path, assembly or parent/detail logic must become clear;
- `NEAR_READ` — what technical proof must remain recoverable;
- `SIGNATURE` — at most one exceptional visual relation, and only if it encodes real information;
- `ANNOTATION_RAIL` — where dimensions/notes/callouts may accumulate without obscuring geometry;
- `METADATA_RAIL` — source/status/revision information that remains visible but quiet.

A drawing with no explicit primary claim tends to equalize every piece of information. Equal completeness is not hierarchy.

### Channel priority

Build emphasis in this order:

`POSITION → AREA / SCALE → PROXIMITY / GROUPING → STROKE / WEIGHT → TONE / PATTERN → COLOR`.

If bright color is required merely to make the primary object visible, first repair composition, scale, void and stroke hierarchy.

### Contrast budget

Treat high contrast as scarce. Reserve it for:
- the principal cut/profile;
- the dominant support/spatial/assembly relation;
- one decision-critical interface;
- one legitimate signature relation.

Status, metadata, long notes, contextual geometry and decoration must not consume the same contrast budget.

## 1. Reading hierarchy

Default technical ladder:

`H0 PRIMARY CLAIM / TECHNICAL SUBJECT`
`L1 CUT / PRIMARY FORM`
`L2 PRIMARY RELATION / STRUCTURE`
`L3 SECONDARY CONSTRUCTION / EDGE / INTERFACE`
`L4 DIMENSION / LEADER / NOTE / HUMAN / MAINTENANCE`
`L5 CONTEXT / FIELD-OPEN / REFERENCE SUPPORT`

The exact number of classes may be reduced if the drawing is simple. Do not add classes for decoration.

### Ratio logic
Use relative contrast rather than a fixed recipe. A useful calibration starting point is that each adjacent class is visibly but not dramatically weaker than the one above it. The old OLEANDER training ratio `3.0 : 1.7 : 0.9 : 0.5` is retained only as a screen-calibration example, not a standard or mandatory output value.

### 3-second first-read
At distance, without reading body notes, the viewer should identify:
- the technical/spatial subject;
- the cut/profile or primary object;
- the main spatial/support/assembly relation;
- the location of the technical decision.

If labels, title-block metadata, legends or status notes are the first thing read, hierarchy is wrong.

### 30-second logic read
Within roughly one inspection pass, the viewer should recover:
- parent → child detail path;
- support/load/assembly/drainage/route logic;
- primary dimensions or decision points;
- where uncertainty or FIELD/engineer-open state changes the design.

### Near-read test
At detail-reading distance, the viewer should still recover:
- secondary construction;
- interfaces/joints;
- dimensions;
- material IDs;
- qualifiers and field-open notes;
- maintenance/installation relations;
- source/revision metadata.

A clean thumbnail that deletes near-read evidence is over-simplified.

## 2. Composition / grid / rails

Use one coherent compositional system per sheet or controlled view:

`SHEET MARGIN → HEADER → PRIMARY DRAWING FIELD → ANNOTATION / DETAIL RAIL → EVIDENCE / TITLE FOOTER`.

The proportions may vary. The roles should not.

### Primary drawing field
- owns the largest continuous visual field;
- contains the dominant geometry, not long prose;
- should remain readable when annotation groups are temporarily hidden;
- may contain only decision-critical direct labels.

### Annotation rail
- align repeated notes/callouts/dimensions to one or two controlled measures;
- provide clean leader landing zones;
- keep note starts, baselines and detail frames deliberately aligned;
- move secondary notes to the rail before shrinking the primary geometry;
- if a rail becomes a dense report column, split the sheet/view rather than making all type smaller.

### Detail rail
- local enlargements should align to a shared edge/module;
- details still require traceable callouts from the parent view;
- do not create a gallery of equal boxes when details have different technical importance.

### Whitespace
Negative space is technical structure. Use it to:
- isolate the primary claim;
- separate parent from detail without losing traceability;
- protect leader/callout paths;
- keep FIELD/engineering-open notes visible but subordinate;
- reveal grouping through proximity rather than extra boxes.

Do not fill every void with hatch, humans, icons, notes, legends or dimensions.

## 3. Density zoning

Information density should be unequal by role:

- **Hero density** — primary geometry + decision-critical labels only;
- **Support density** — details, dimensions, interfaces, assembly/service information;
- **Metadata density** — source, status, revision and does-not-prove notes.

Uniform density produces uniform visual weight and usually a weak first read.

## 4. Section and cut grammar

- A section cut must be visually distinct from elements beyond the cut.
- Do not turn cut edges into oversized black bands that obscure local detail.
- Cut poche/hatch supports the cut; it must not become a decorative mass that hides interfaces.
- Separate `CUT`, `BEYOND`, `OVERHEAD/HIDDEN`, `EXISTING`, `PROPOSED`, `DEMOLISH/REMOVE` or other project states by line/pattern/label logic rather than color alone.
- Where terrain/rock/soil is uncertain, do not use detailed geological hatching that implies field evidence.
- Section fill should reinforce the silhouette/cut claim, not create a second high-contrast hero.

## 5. Plan / elevation grammar

- Primary boundaries and decision-critical interfaces read before furniture, vegetation, textures or context.
- Overhead/hidden information appears only when needed to resolve the decision.
- Repetition should use consistent symbol/line logic; do not redraw the same object with different visual authority across views.
- Existing/proposed distinctions must survive grayscale export.
- A plan with multiple overlays should reserve one visual channel hierarchy for `source/base → evidence/constraint → decision`, rather than giving every overlay equal opacity and weight.

## 6. Dimension grammar

Dimensions are technical relationships, not decorative typography.

- Dimension lines and extension lines remain subordinate to geometry.
- Arrowheads/ticks/terminators must be consistent within the set.
- Text orientation and reading direction remain consistent.
- Do not place a dimension through dense geometry when a clearer outside position exists.
- Avoid dimension stacking that creates visually equal chains with no clear control hierarchy.
- Place controlling dimensions nearest the object when that improves traceability; supporting/reference chains can sit farther out.
- Do not duplicate the same controlling dimension across multiple views unless project convention requires it and conflict risk is controlled.
- A `FIELD VERIFY`, `REF`, `RANGE`, `TBD` or similar state must be visually inseparable from the value it qualifies.
- Dimension clusters should align to predictable bands/rails, not form scattered halos around the object.

## 7. Callout / leader grammar

A leader must answer immediately:

`WHAT TEXT? → WHICH TARGET? → WHICH VIEW/DETAIL DOES IT BELONG TO?`

Rules:
- terminate on the actual feature/interface, not nearby empty space;
- avoid leader crossings where possible;
- avoid long leaders passing through unrelated geometry;
- use consistent elbow/landing behavior;
- align text landings to the annotation rail where practical;
- keep callout text in available negative space before adding boxes or heavy graphic devices;
- if many leaders converge, create a local enlargement instead of a leader forest;
- do not make every callout badge equally loud: decision-critical callouts outrank explanatory/support callouts.

## 8. Hatch / material fill grammar

Use hatch/pattern/fill to encode a real distinction:
- material family;
- cut condition;
- existing/proposed state;
- assembly zone;
- field-open/reference zone.

Do not use hatch merely to make a drawing look detailed.

Checklist:
- hatch density survives target output scale;
- pattern does not moiré or fill into solid black at export;
- adjacent materials remain distinct in grayscale;
- legend uses stable material IDs;
- pattern orientation does not imply a real grain/lay direction unless intended;
- fills do not consume more contrast than the boundary/interface they support.

## 9. Human / furniture / vegetation / maintenance figures

These are scale/use evidence layers, not visual protagonists.

Use them to show:
- relative human scale;
- reach/access;
- circulation/use position;
- maintenance posture/tool envelope;
- occupancy or interface only when relevant.

Do not use them to imply measured site accuracy. A person standing on an inferred slope does not validate the slope.

## 10. Typography hierarchy

Technical text should support the drawing rather than turn it into a poster or admin UI.

Role tokens:
- `SHEET_TITLE / DOCUMENT IDENTITY`
- `PRIMARY_CLAIM`
- `VIEW_TITLE + VIEW ID + SCALE`
- `TECH_LABEL / MATERIAL / PART ID`
- `DIMENSION`
- `QUALIFIER / STATUS`
- `SOURCE_STATE`
- `METADATA`

Rules:
- preserve a small number of sizes/weights;
- use spacing/alignment to create hierarchy before excessive font changes;
- primary claim can be larger/bolder than a view title, but must not outrank the geometry it names;
- long status strings belong in metadata/truth rails, not repeated as pills across the drawing;
- keep dimension and note text readable at final physical size;
- verify CJK/Latin fallback and font embedding/substitution in PDF;
- do not outline all text unless the delivery workflow explicitly requires it; preserve editability where possible.

## 11. One-signature rule

One exceptional visual move is permitted when it clarifies the actual technical relation, for example:
- continuous load-path spine;
- dominant cut profile;
- assembly axis;
- drainage path;
- return route;
- evidence→decision overlay.

It must encode information, survive grayscale, and not create a second truth system. Multiple competing signatures trigger `REVISE`.

## 12. Scale selection logic

Choose scale from the decision, not habit.

### Context scale
Use when the question is location, route, system or site relation. Technical node information should not be forced into this scale.

### Object / arrangement scale
Use when the question is principal geometry, movement, clearances, levels, major material zones or system interfaces.

### Detail scale
Use when the question is build-up, joint, edge, fixing, drainage, base, transition or assembly sequence.

### Component / fabrication scale
Use when the question is exact part geometry, hole/slot/radius/chamfer, datum, tolerance, mating or manufacturing feature.

The scale must be explicitly written per view unless `NTS` is intentionally required. If a view is digitally rescaled inside a board/page, the displayed scale bar or written scale must not become false.

## 13. Multi-scale review

Review every serious drawing in at least three modes:

1. **3S / THUMBNAIL / DISTANCE** — one dominant claim + primary relation.
2. **30S / INTENDED SIZE** — system logic, parent/detail path, main technical relationships.
3. **NEAR READ / DETAIL ZOOM** — dimensions, connections, qualifiers, source state and vector integrity.

Record them separately. Passing one cannot average away failure in another.

### First-visual veto
A technically complete drawing is still `REVISE` when:
- four or more regions compete equally;
- annotation reads before geometry;
- metadata/title block dominates;
- there is no deliberate void or entry point;
- support detail has more contrast than the parent subject;
- a generic CAD export is merely placed into panels without compositional repair.

## 14. Diagnostic-to-repair loop

Do not stop at `flat`, `busy`, `weak hierarchy`.

Use:

`3S READ → 30S READ → NEAR READ → OBSERVED FAILURE → LIKELY CAUSE → ONE MATERIAL REPAIR → REOPEN`.

Examples:
- equal panels compete → enlarge primary field; compress support into one rail;
- labels read first → reduce note contrast, align text landings, protect primary void;
- detail appears detached → strengthen parent callout and shared alignment, not heavier borders;
- technical subject feels small → remove decorative framing/metadata competition before enlarging all type;
- unknown state looks resolved → change line/pattern/ID semantics, not just color;
- crowded primary field → move non-critical notes to rail; do not delete required proof.

## 15. Color policy

Technical meaning must not depend on color alone.

Color may support:
- existing/proposed;
- material family;
- state or responsibility;
- editorial emphasis.

But every critical distinction needs redundant line/pattern/text semantics for grayscale printing and accessibility.

Use color late. Position, scale, grouping, stroke and pattern should establish the hierarchy first.

## 16. Surface / materiality / gradient / texture expression

This layer is optional and subordinate to geometry, semantics and hierarchy. It exists to add material reading, tonal depth, density/state continuity or source-faithful visual character after the structural carrier is already correct.

Use this stack when surface expression is material to the task:

`FLAT GEOMETRY → CHROMATIC FIELD → GRADIENT / TONAL MODULATION → TEXTURE SCALE → FINISH / EDGE BEHAVIOUR → MEDIUM / OPTICAL DECAY`.

### 16.1 Flat master first

Maintain a recoverable flat/vector master. Texture, gradient, glow, blur, shadow or noise may not be the only reason an object remains legible.

Hard rule:

`EFFECT OFF → GEOMETRY / RELATION / STATE STILL READS`.

If turning an effect off destroys the analytical or technical meaning, the effect has become an unauthorized semantic carrier and the upstream geometry/encoding must be repaired.

### 16.2 Gradient / tonal modulation

A gradient is not an automatic quality or “premium” device. Before using one, register:

`ROLE → AXIS / FIELD → STOPS → CONTRAST RANGE → OWNER / MASK → WHY → OFF-STATE`.

Legitimate roles include:
- restrained material-volume cue;
- source-visible tonal modulation in reconstruction;
- continuous scalar/density field where a continuous scale is actually valid;
- controlled emphasis falloff around one decision-critical object;
- state/time interpolation in a declared screen/animation context.

Rules:
- prefer low-span, neighboring tonal/chromatic shifts when the role is material depth rather than categorical data;
- do not use rainbow or multi-direction gradients without a declared encoding reason;
- do not let a smooth gradient imply measured continuity when the evidence is categorical, sparse or uncertain;
- in exact reconstruction, gradient geometry/stops/opacity are fidelity objects and must reproduce the reference rather than “improve” it;
- in technical/analysis drawings, any data-bearing gradient requires units/domain/scale/legend where needed;
- avoid generic glass/glow/aurora treatment unless the source or design system explicitly requires it.

### 16.3 Texture scale and variation

Do not treat `texture` as one global noise overlay. Separate at least these scales when relevant:

- `MICRO` — grain, stipple, paper tooth, fine surface noise;
- `MESO` — abrasion, weave, aggregate, repeated pattern, local irregularity;
- `MACRO` — vein, layer, grain direction, broad erosion/flow/stratification pattern.

For each texture family record:

`SCALE → DENSITY RANGE → DIRECTIONALITY → LOCAL MASK / OWNER → VARIATION SEED / PHASE → CONTRAST → FAILURE TRIGGER`.

Rules:
- texture must be owned by a material, state, field, object or source-visible region; no full-sheet anonymous noise by default;
- avoid identical repeated stamps and globally uniform grain when natural or material variation is part of the intended reading;
- preserve clean negative/critical channels where texture would reduce legibility;
- texture orientation may not imply a real lay/grain/flow direction unless that direction is intended or source-grounded;
- prefer editable SVG pattern/mask/procedural/vector methods when editability is required; raster texture may support appearance but cannot replace semantic geometry;
- for reference reconstruction, separate source-derived visual texture from recovered semantic objects and do not claim texture fidelity as data recovery.

### 16.4 Finish, edge and optical behaviour

Use opacity falloff, controlled highlight/shade, edge wear, local softness, blur or shadow only when they have a defined owner and reading role.

They may support:
- foreground/background separation;
- material edge behaviour;
- source-visible optical softness;
- a bounded depth cue;
- focus hierarchy in screen presentation.

They may not:
- fabricate material properties such as gloss/roughness/coating thickness;
- hide geometry conflicts;
- create false elevation or spatial depth in a map-bound analytical figure;
- turn a technical drawing into a pseudo-render that weakens line authority.

### 16.5 Effect attack tests

For a material visual layer, test at minimum:

`FLAT → GRADIENT OFF → TEXTURE OFF → GRAYSCALE → TARGET SIZE → SMALL SIZE → REVERSE / DARK-LIGHT VARIANT WHEN RELEVANT → PRINT / EMBOSS / MONO FALLBACK WHEN RELEVANT → NEAR READ → DISTANCE READ`.

A surface treatment is `REVISE` when:
- it is required to rescue weak geometry;
- it creates a second focal center without a decision reason;
- it turns categorical evidence into false continuity;
- it reads as decorative aging, random grain, glass/glow or “tech effect” unrelated to the project;
- it collapses at small size or blocks dimensions/labels/interfaces;
- the editable flat master cannot be recovered.

## 17. Temporal / dynamic expression routing

A static technical drawing does not own motion merely because motion looks more advanced. When time, interaction or state transition materially improves the communication, route the temporal layer to the existing `oleander-motion` skill rather than inventing a parallel motion system here.

Use the cross-skill sequence:

`STATIC / NO-MOTION BASELINE → STATE OR INFORMATION CHANGE → MOTION ROLE → STRUCTURAL EFFECT → TIMING / EASING OR PHYSICS → REDUCED-MOTION ALTERNATIVE → REAL RUNTIME READBACK`.

Relevant motion roles for drawing/data/analysis work include:
- `Continuity` — preserve object identity through view/state transitions;
- `Hierarchy` — move attention from old primary to new primary without dual-focus frames;
- `Attention` — reveal a material change/risk/decision only when necessary;
- `Narrative` — sequence evidence → finding → decision;
- `MOT-06 Data / Information Motion` — sorting, filtering, temporal change, update and uncertainty;
- `MOT-03 Spatial Continuity` — route, section, camera, layer or spatial-state continuity;
- `MOT-04 Brand Motion` — only when a repeatable temporal identity is part of the design system.

Prefer structural mechanisms such as:
- shared-element / shared-container continuity;
- mask/clip reveal;
- SVG path trace when path growth itself represents sequence/flow;
- topology-safe morph only when object identity is preserved;
- structured stagger tied to order or hierarchy;
- data interpolation/reorder with stable entity keys;
- controlled opacity/tone/material parameter transition;
- explode/assemble for actual assembly logic;
- scroll progress only when scroll position legitimately owns the narrative sequence.

Avoid by default:
- infinite floating;
- decorative parallax;
- generic logo reveals;
- glow trails;
- cursor followers;
- magnetic effects;
- gratuitous glitch/displacement;
- scroll-jacking;
- full-screen zoom transitions with no state/space reason.

Temporal hierarchy rule:

`OLD PRIMARY → CONTINUITY ANCHOR → OLD PRIMARY DOWNWEIGHT → NEW PRIMARY ACQUIRE → OLD STATE SUPPORT`.

A crossfade is not automatically correct. If old and new states both retain full first-visual weight in intermediate frames, the transition is `REVISE` even when easing is smooth.

For motion-dependent output, `AR-S10 Motion` and the runtime evidence contract from `oleander-motion` are mandatory. A storyboard, keyframe plan or rendered demo is not runtime validation. Reduced Motion must preserve the same information even if positional animation is removed.

For exact reconstruction of a static source, do not invent animation. For adaptation/interactive interpretation, record motion as a separate derivative and keep the static/source-fidelity claim independent.

## 18. Raster/context imagery

Raster imagery may be used as:
- site/reference underlay;
- render context;
- orthophoto/map context;
- photographic evidence.

It must not replace:
- technical text;
- dimensions;
- authoritative linework;
- geometry interfaces;
- section/detail construction information.

If AI imagery is used, it is a non-authoritative visualization layer only. Never derive hidden dimensions, connections, foundations or site facts from invented pixels.

## 19. Export visual checks

After export to PDF/SVG/DXF/PNG as applicable:
- compare against source at matched crop/scale;
- verify line hierarchy did not collapse;
- verify dashes, hatches and transparency did not change materially;
- verify gradient stops/masks, opacity, blend and texture phase/density did not change materially when those layers are part of the reviewed visual system;
- verify CJK and Latin text survived;
- verify dimensions and leader targets remain aligned;
- verify vector text/linework remains vector where required;
- verify no clipping at artboard/page boundary;
- verify grayscale/print preview still preserves critical distinctions;
- reopen at 3-second, 30-second and near-read scales;
- confirm primary field still dominates after export/resizing.

For explicit reconstruction work, do not stop at subjective side-by-side review. Use the separate reconstruction protocol to lock canvas/registration, reconstruct A0–A5 anchors, render the candidate under the declared comparison condition and generate overlay/difference/ROI evidence. A global pixel score cannot average away a failed critical ROI or a technical truth conflict.

`SOURCE LOOKS GOOD` is not enough; the actual derivative must be reviewed.