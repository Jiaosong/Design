# OLEANDER Technical Drawing — Cross-Skill Visual Hierarchy Transfer

Status: `candidate / PR #172`

Purpose: translate proven visual-organization methods from mature design skills into technical drawing without importing UI decoration, flattening technical truth, or changing authoritative geometry.

## References inspected

Internal OLEANDER:
- `oleander-data-viz` candidate PR #176: Existing Mature Design First; Subject Grounding + One Signature; task → content → measure → grid; position/size/whitespace before color; 3-second + 30-second gates; editable-vector reconciliation.
- `oleander-story-and-board` PR #167: first-visual veto; one primary visual; perceptual mass; diagnostic-to-repair loop; far/mid/near readback.
- technical-drawing hierarchy training PR #170: cut/primary → structure/relation → edge/connection → dimension/note.

External skill research already materialized in PR #176:
- Anthropic `frontend-design`: subject-specific visual language, meaningful structural devices, one memorable signature.
- plugin87 design-review/design-taste/redesign: first-impression critique, unequal weight, grid/rhythm, anti-template checks.
- oskar-q grid systems: task/content determine the grid; position and size precede weight/color.
- declarative visualization systems: lock information grammar before styling.

These are reference inputs, not authorities over OLEANDER truth, drawing standards, project geometry, engineering, or field state.

## 1. Translation rule

Do not copy a UI/card aesthetic into drawings. Translate the underlying design operation:

| Source principle | Technical-drawing translation |
|---|---|
| one primary visual | one dominant technical/spatial claim per view |
| one memorable signature | one relationship may receive exceptional emphasis; all other accents remain restrained |
| position/size before color | hierarchy via placement, occupied area, stroke, void and proximity before hue |
| task → content → measure → grid | decision → required views/evidence → density → drawing field + annotation rail |
| 3s / 30s read | 3s claim → 30s system/logic → near-read evidence/detail |
| first-visual veto | a technically complete but flat/noisy sheet is REVISE |
| audit-first redesign | preserve authoritative geometry and solved design DNA; repair hierarchy without inventing information |

## 2. Visual hierarchy budget

Treat contrast as scarce.

Allocate visual authority in this order:

`H0 PRIMARY CLAIM / TECHNICAL SUBJECT`
`H1 PRIMARY GEOMETRY / CUT / LOAD-SPATIAL RELATION`
`H2 SECONDARY CONSTRUCTION / SUPPORT / EVIDENCE`
`H3 DIMENSION / CALLOUT / TRUTH-STATE QUALIFIER`
`H4 METADATA / SOURCE / REVISION`

Rules:
- H0/H1 own the strongest position, largest continuous field, and darkest/strongest strokes.
- H2 remains clearly recoverable at intended size but cannot create a second hero.
- H3 is aligned into predictable rails rather than scattered through the drawing.
- H4 stays visible and exact but visually quiet.
- Do not solve hierarchy with saturation alone.

## 3. Three reading distances

### 3 seconds — claim
Without reading body notes, the reviewer should identify:
- what object/system is being examined;
- the dominant cut/spatial/support/assembly relation;
- where the technical decision sits.

### 30 seconds — logic
The reviewer should recover:
- parent → child detail path;
- support/assembly/drainage/route/evidence chain;
- primary dimensions or decision points;
- where uncertainty changes the design.

### Near read — proof
The reviewer should recover:
- dimensions and qualifiers;
- material/part IDs;
- connection interfaces;
- source/truth state;
- maintenance/field/engineering open items;
- revision metadata.

Failure at any distance is independent. A beautiful 3-second read that removes near-read proof is not professional.

## 4. One dominant claim per view

Every view must name its single dominant claim in a `PRIMARY_CLAIM` layer/group.

Examples:
- section: `CUT + LEVEL RELATION`
- landscape node: `PATH / SUPPORT / DRAINAGE RELATION`
- assembly: `ASSEMBLY ORDER + SERVICE CLEARANCE`
- foundation: `LOAD PATH + BASE / SUBSTRATE INTERFACE`
- spatial analysis: `SOURCE SPINE + DECISION CONFLICT`
- evidence chain: `EVIDENCE → FINDING → CONSEQUENCE`

Supporting details may be numerous; perceptual protagonists may not.

If two unrelated claims require equal visual authority, split the view rather than create two competing heroes.

## 5. Grid, drawing field and annotation rail

Use one compositional system per sheet:

`SHEET MARGIN → HEADER → PRIMARY DRAWING FIELD → ANNOTATION / DETAIL RAIL → EVIDENCE / TITLE FOOTER`

A fixture may vary proportions, but it must expose stable groups:
- `HIERARCHY_FRAME`
- `PRIMARY_CLAIM`
- `ANNOTATION_RAIL`
- `METADATA_RAIL` where needed.

Rules:
- primary geometry sits inside the largest coherent field;
- detail enlargements align to a rail or shared edge rather than float arbitrarily;
- long notes align to one or two controlled text measures;
- captions and callouts align to the view they explain;
- near-alignments are failures unless a deliberate offset is visible;
- do not use an equal-card grid for non-parallel technical relations.

## 6. Whitespace is technical structure

Negative space is not unused space. Reserve it to:
- separate primary geometry from annotation;
- create clean leader landing zones;
- isolate a detail from its parent without losing traceability;
- keep truth-state notes visible but subordinate;
- protect the dominant relation at distance.

Do not fill every void with legends, extra dimensions, hatch, people, icons or method copy.

## 7. Channel priority

Prefer this sequence when creating emphasis:

`POSITION → AREA / SCALE → PROXIMITY / GROUPING → STROKE / WEIGHT → TONE / PATTERN → COLOR`

Color is a redundant semantic carrier, never the only carrier for source/evidence/inference/decision or existing/proposed/open states.

## 8. Density zoning

High information density is acceptable when spatially organized.

Use:
- **hero density**: primary geometry + only decision-critical labels;
- **support density**: details, dimensions, interfaces;
- **metadata density**: sources/status/revision.

Do not distribute all information uniformly. Equal density produces equal visual weight.

## 9. Typography roles

Use role tokens rather than ad-hoc font changes:
- `SHEET_TITLE`
- `PRIMARY_CLAIM`
- `VIEW_TITLE`
- `TECH_LABEL`
- `DIMENSION`
- `QUALIFIER`
- `SOURCE_STATE`
- `METADATA`

Create hierarchy first with size/weight/position and spacing. Avoid multiple decorative typefaces or oversized status language.

## 10. Signature rule

One exceptional visual move is permitted when it clarifies the actual technical claim:
- a continuous load-path spine;
- a cut profile;
- a return route;
- a source/evidence/decision overlay;
- an exploded assembly axis.

It must encode a real relationship and survive grayscale. A second equally loud signature is normally a hierarchy failure.

## 11. Diagnostic-to-repair loop

Use:

`3s FIRST READ → 30s LOGIC READ → NEAR-READ PROOF → MISMATCH → CAUSE → ONE MATERIAL REPAIR → REOPEN`

Typical repairs:
- equal-weight panels → enlarge primary field; compress support into a rail;
- labels read first → reduce note contrast and align them to annotation rail;
- details float → align them to one edge and make parent callout explicit;
- color carries status → add line/pattern/ID redundancy;
- technical subject feels small → remove decorative framing before enlarging text;
- crowded field → move non-critical notes out, not delete required proof.

## 12. Non-transferable patterns

Do not import:
- card walls;
- UI pills/status badges as primary composition;
- decorative gradients;
- arbitrary rounded panels;
- generic hero typography that outranks geometry;
- forced 12-column grids;
- visual effects that cannot be tied to technical meaning.

The goal is not to make drawings resemble product websites. It is to make their hierarchy as intentional as mature editorial/UI/data-viz work while retaining drawing truth and discipline conventions.

## 13. Golden-fixture requirements

Every visual-hierarchy Golden candidate must:
- keep authoritative/training geometry unchanged unless the fixture explicitly tests geometry change;
- expose `HIERARCHY_FRAME`, `PRIMARY_CLAIM`, `ANNOTATION_RAIL` stable groups;
- preserve prior required technical groups and truth-state IDs;
- demonstrate one dominant relation at 3 seconds;
- reveal system logic by 30 seconds;
- preserve technical proof at near read;
- remain legible in grayscale;
- not self-promote from structural/visual author self-check.

Machine checks may confirm IDs/vector structure. Only actual visual readback can judge perceptual hierarchy.