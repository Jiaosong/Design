# OLEANDER Technical Drawing — Discipline Profiles

Use this reference after `SKILL.md` has established drawing status, source authority and truth state. It prevents one generic drafting recipe from being applied to architecture, landscape, product and connection work.

The profiles are routing contracts, not substitute codes. Project/jurisdiction standards and responsible specialist review remain authoritative.

## A. Architecture / Interior / Spatial System

### Primary questions
- Where is the object/system located relative to grids, levels, envelope and circulation?
- What is cut, what is beyond, and what is hidden?
- What controls clear dimension, level, build-up, interface and access?
- Which condition repeats, and which is unique?
- What must coordinate with structure, MEP, fire, waterproofing, façade or interior systems?

### Minimum view logic
1. GA / key plan when location is not self-evident.
2. Plan showing controlling grids/levels/interfaces.
3. Section through the condition that actually resolves vertical relation.
4. Elevation only when face/alignment/finish boundary cannot be understood from plan/section.
5. Detail callout from the parent plan/section.
6. Local enlargement for dense edge/joint/interface conditions.

### Mandatory checks when applicable
- structural zone and finish/build-up are not conflated;
- finished level vs structural level is explicit;
- headroom/clearance, access, egress and maintenance zones are not hidden by presentation graphics;
- waterproofing/drainage/fire/acoustic boundaries are not invented when unresolved;
- repeated module dimensions do not contradict overall control dimensions;
- material finish boundary matches the actual assembly boundary.

### Failure patterns
- beautiful section with no level datum;
- detail not traceable to a parent view;
- finish thickness visually treated as structure;
- wall/floor build-up copied from a precedent without project authority;
- raster render used to decide hidden construction.

## B. Landscape / Site / Public Realm

### Primary questions
- What is existing, proposed, inferred and field-open?
- How do route, level, slope, edge, drainage, vegetation, soil, water and maintenance interact?
- Which dimensions are site-controlled and therefore cannot be closed without survey/field evidence?
- What is the human/safety relationship at edges, steps, ramps, seating, platforms, paths and water?

### Minimum view logic
1. Site/route context locating the intervention within the real landscape system.
2. Plan showing path/edge/vegetation/water/structure relations.
3. Section perpendicular or otherwise relevant to slope/edge/valley/water relation.
4. Longitudinal section/profile when gradient, sequence or drainage is decision-critical.
5. Node detail for edge/support/drainage/fixing/material transition.
6. Maintenance/access diagram when replacement, cleaning, vegetation management or inspection affects feasibility.

### Mandatory checks when applicable
- existing grade and proposed grade are visually distinct;
- slope/level values are VERIFIED, RECOMMENDED RANGE or FIELD VERIFY — never silently mixed;
- drainage direction, low points and discharge intent are visible if water management matters;
- root zone/soil volume/planting depth is not fabricated from imagery;
- safety edge and fall-risk relation is readable at human scale;
- interface with rock/soil/water uses explicit field-open boundaries where site truth is absent;
- no drawing implies a normal/open condition when operational state is UNKNOWN/CLOSED/DEGRADED.

### Remote-research rule
When `FIELD OBSERVED=0` or `FIELD MEASURED=0`, continue design instead of stopping, but every critical technical variable must use:

`RECOMMENDED VALUE or RANGE + BASIS + SENSITIVITY + FIELD VERIFY ITEM`

This is design continuation, not field validation.

### Failure patterns
- precise retaining/foundation geometry inferred from landscape photography;
- arbitrary slope percentage added to make the drawing look technical;
- generic railing/anchor copied without relation to actual substrate;
- vegetation symbols used as decorative fill and mistaken for planting evidence;
- no maintenance path to a component that is shown as replaceable.

## C. Industrial / Product / Furniture / Equipment

### Primary questions
- Which CAD/model is geometry authority?
- Which dimensions control form, fit, function, interchangeability, assembly or tactile intent?
- Which surfaces are datum/interface surfaces?
- What can be manufactured/assembled in the proposed order?
- Which CMF properties are approved, candidate or process-dependent?

### Minimum view logic
1. GA / assembly view with part IDs.
2. Orthographic views sufficient to define the controlled geometry.
3. Section for internal build-up/interfaces.
4. Exploded view for assembly order and BOM relation.
5. Part/detail view for critical features.
6. CMF/material map where surface state matters.
7. Datum/tolerance/GD&T only when the project authority and manufacturing rationale support it.

### Mandatory checks when applicable
- do not dimension a rendered silhouette when CAD is authority;
- dimensions are not duplicated across views without a clear controlling location;
- nominal, tolerance and finish allowance are distinct concepts;
- screw/insert/clip/adhesive/weld location is visible if it controls assembly;
- tool access, hand access, cable bend, battery/service access or removal direction is visible when relevant;
- candidate finishes are not written as approved specifications;
- texture/grain/brushing direction is identified when orientation matters.

### Failure patterns
- exploded view with no exact mating/interface detail;
- over-dimensioned part whose chains contradict the CAD;
- invented ± tolerance copied across all dimensions;
- hidden fastener that cannot physically be installed;
- CMF render appearance treated as measurable gloss/roughness authority.

## D. Structural / Connection / Support Explanation

This profile is for design communication and coordination. It does not grant structural design authority.

### Primary questions
- What carries what?
- Where does load/support transfer occur?
- What is the substrate/base condition?
- Which plate/member/fastener/anchor/weld/adhesive relationships are known, recommended or specialist-open?
- Can the connection be installed, inspected, drained and maintained?

### Minimum view logic
1. Parent section or assembly showing the support path.
2. Connection enlargement showing interfaces and orientation.
3. Secondary detail for bolt/anchor/weld/plate/base/foundation relation if the first detail remains ambiguous.
4. Installation/maintenance sequence if access is non-obvious.

### Required reality chain
For every critical connection family, record:

`DESIGN ACTION → STRUCTURAL/SUPPORT SYSTEM → APPLICABLE STANDARD OR ENGINEERING REFERENCE → RECOMMENDED SPECIFICATION OR RANGE → SENSITIVE FACTORS → FIELD/ENGINEER VERIFY ITEMS`

Examples of sensitive factors include substrate strength, corrosion exposure, edge distance, embedment, drainage, fatigue/vibration, waterproofing, installation tolerance, access and replaceability.

Do not invent member sizes, anchor diameters, embedment, plate thicknesses, concrete dimensions or weld sizes when their basis is unresolved. If a reasonable design-study range is necessary, state the basis and keep specialist approval open.

## E. Fabrication / Assembly Drawing

Use only when drawing status permits fabrication communication.

### Minimum content
- unique part/assembly ID and revision;
- units and scale;
- controlling dimensions;
- material/finish state;
- tolerance basis;
- interfaces/datums where relevant;
- quantity/BOM linkage if applicable;
- process-sensitive notes only when source-grounded;
- inspection or acceptance reference when required;
- revision cloud/change record for material revisions.

### Blockers
- open geometry authority;
- unresolved critical material or finish;
- guessed tolerance;
- missing mating interface;
- unverified drawing/model disagreement;
- inaccessible assembly operation;
- technical text/rules rasterized into non-editable imagery.

## F. Cross-discipline Node Ladder

Do not jump from an overall drawing straight to a micro-detail without parentage. Use the smallest ladder that closes the decision:

`CONTEXT / GA → PARENT PLAN OR SECTION → INTERFACE DETAIL → CONNECTION ENLARGEMENT → COMPONENT / FOUNDATION / EDGE DETAIL`

Every child detail must answer a question that the parent cannot answer at its current scale. If the child adds no new decision-relevant information, remove it.

## G. Drawing Completeness Test

Before calling a technical set professionally complete, ask whether the intended reader can answer, at the declared scope:

1. **WHAT** is the object/system?
2. **WHERE** is it located and oriented?
3. **HOW BIG** are the controlling relationships?
4. **WHAT IS IT MADE OF** and what is only candidate/provisional?
5. **HOW DOES IT CONNECT / SUPPORT / DRAIN / MOVE**?
6. **HOW IS IT USED / ACCESSED / MAINTAINED / REPLACED**?
7. **WHAT REMAINS UNKNOWN OR FIELD/ENGINEER OPEN**?
8. **WHICH SOURCE/REVISION CONTROLS**?

A visually polished sheet that cannot answer the applicable questions remains `REVISE` or `HOLD`.