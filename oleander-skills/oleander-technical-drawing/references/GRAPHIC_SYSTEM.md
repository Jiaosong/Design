# OLEANDER Technical Drawing — Graphic System

This reference turns drawing hierarchy into an executable visual system. It does not prescribe one universal millimetre lineweight table; final lineweight depends on sheet size, scale, medium, printer/plotter, display density and project standards.

## 1. Reading hierarchy

Default order:

`L1 CUT / PRIMARY FORM`
`L2 PRIMARY RELATION / STRUCTURE`
`L3 SECONDARY CONSTRUCTION / EDGE / INTERFACE`
`L4 DIMENSION / LEADER / NOTE / HUMAN / MAINTENANCE`
`L5 CONTEXT / FIELD-OPEN / REFERENCE SUPPORT`

The exact number of classes may be reduced if the drawing is simple. Do not add classes for decoration.

### Ratio logic
Use relative contrast rather than a fixed recipe. A useful calibration starting point is that each adjacent class is visibly but not dramatically weaker than the one above it. The old OLEANDER training ratio `3.0 : 1.7 : 0.9 : 0.5` is retained only as a screen-calibration example, not a standard or mandatory output value.

### First-read test
At the intended board/sheet distance, the viewer should identify:
- the cut/profile or primary object;
- the main spatial/support relation;
- the location of the technical subject.

If labels are the first thing read, hierarchy is usually wrong.

### Near-read test
At detail-reading distance, the viewer should still recover:
- secondary construction;
- interfaces/joints;
- dimensions;
- material IDs;
- qualifiers and field-open notes.

If a clean thumbnail requires deleting near-read evidence, the drawing is over-simplified.

## 2. Section and cut grammar

- A section cut must be visually distinct from elements beyond the cut.
- Do not turn cut edges into oversized black bands that obscure local detail.
- Cut poche/hatch supports the cut; it must not become a decorative mass that hides interfaces.
- Separate `CUT`, `BEYOND`, `OVERHEAD/HIDDEN`, `EXISTING`, `PROPOSED`, `DEMOLISH/REMOVE` or other project states by line/pattern/label logic rather than color alone.
- Where terrain/rock/soil is uncertain, do not use detailed geological hatching that implies field evidence.

## 3. Plan / elevation grammar

- Primary boundaries and decision-critical interfaces read before furniture, vegetation, textures or context.
- Overhead/hidden information appears only when needed to resolve the decision.
- Repetition should use consistent symbol/line logic; do not redraw the same object with different visual authority across views.
- Existing/proposed distinctions must survive grayscale export.

## 4. Dimension grammar

Dimensions are technical relationships, not decorative typography.

- Dimension lines and extension lines remain subordinate to geometry.
- Arrowheads/ticks/terminators must be consistent within the set.
- Text orientation and reading direction remain consistent.
- Do not place a dimension through dense geometry when a clearer outside position exists.
- Avoid dimension stacking that creates visually equal chains with no clear control hierarchy.
- Place controlling dimensions nearest the object when that improves traceability; supporting/reference chains can sit farther out.
- Do not duplicate the same controlling dimension across multiple views unless the project convention requires it and conflict risk is controlled.
- A `FIELD VERIFY`, `REF`, `RANGE`, `TBD` or similar state must be visually inseparable from the value it qualifies.

## 5. Callout / leader grammar

A leader must answer three questions immediately:

`WHAT TEXT? → WHICH TARGET? → WHICH VIEW/DETAIL DOES IT BELONG TO?`

Rules:
- terminate on the actual feature/interface, not nearby empty space;
- avoid leader crossings where possible;
- avoid long leaders passing through unrelated geometry;
- use consistent elbow/landing behavior;
- keep callout text in available negative space before adding boxes or heavy graphic devices;
- if many leaders converge, create a local enlargement instead of a leader forest.

## 6. Hatch / material fill grammar

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
- pattern orientation does not imply a real grain/lay direction unless intended.

## 7. Human / furniture / vegetation / maintenance figures

These are scale/use evidence layers, not visual protagonists.

Use them to show:
- relative human scale;
- reach/access;
- circulation/use position;
- maintenance posture/tool envelope;
- occupancy or interface only when relevant.

Do not use them to imply measured site accuracy. A person standing on an inferred slope does not validate the slope.

## 8. Typography hierarchy

Technical text should support the drawing rather than become a layout poster.

Suggested roles:
- Sheet title / document identity
- View title + view ID + scale
- Critical qualifier / status (`NOT FOR CONSTRUCTION`, `FIELD VERIFY`, etc.)
- Material/part ID
- Dimension value
- Leader/note
- Source/reference note

Rules:
- preserve a small number of sizes/weights;
- use spacing/alignment to create hierarchy before excessive font changes;
- keep dimension and note text readable at final physical size;
- verify CJK/Latin fallback and font embedding/substitution in PDF;
- do not outline all text unless the delivery workflow explicitly requires it; preserve editability where possible.

## 9. Scale selection logic

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

## 10. Multi-scale review

Review every serious drawing in at least three modes:

1. **THUMBNAIL / DISTANCE** — composition and first-read hierarchy.
2. **INTENDED SIZE** — actual title/dimension/note readability and line survival.
3. **DETAIL ZOOM** — connection precision, collisions, callout targets and vector integrity.

A result can PASS one mode and FAIL another. Record them separately.

## 11. Color policy

Technical meaning must not depend on color alone.

Color may support:
- existing/proposed;
- material family;
- state or responsibility;
- editorial emphasis.

But every critical distinction needs redundant line/pattern/text semantics for grayscale printing and accessibility.

## 12. Raster/context imagery

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

## 13. Export visual checks

After export to PDF/SVG/DXF/PNG as applicable:
- compare against source at matched crop/scale;
- verify line hierarchy did not collapse;
- verify dashes, hatches and transparency did not change materially;
- verify CJK and Latin text survived;
- verify dimensions and leader targets remain aligned;
- verify vector text/linework remains vector where required;
- verify no clipping at artboard/page boundary;
- verify grayscale/print preview still preserves critical distinctions.

`SOURCE LOOKS GOOD` is not enough; the actual derivative must be reviewed.