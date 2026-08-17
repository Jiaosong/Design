# OLEANDER Technical Drawing — Reality Check Protocol

Use this protocol whenever a drawing includes dimensions, structural/support assumptions, foundations, anchors, fasteners, drainage, safety edges, slopes, clearances, materials, manufacturing details or any other technical statement that can be mistaken for real-world authority.

The goal is to continue design rigorously when evidence is incomplete without fabricating certainty.

## 1. Six-step technical reality chain

For every critical technical issue, record:

`DESIGN ACTION → SYSTEM → APPLICABLE STANDARD / ENGINEERING REFERENCE → RECOMMENDED VALUE OR RANGE → SENSITIVE FACTORS → FIELD / ENGINEER VERIFY ITEMS`

### 1. DESIGN ACTION
What must the design physically do?

Examples:
- support a deck edge;
- keep a path drained;
- allow a panel to be removed;
- prevent a hand-contact sharp edge;
- maintain a clear walking width;
- fix a product shell to an internal frame.

Do not start from a copied detail. Start from the action.

### 2. SYSTEM
What physical system performs the action?

Examples:
- steel frame + plate + anchors;
- timber joist + concealed clip;
- surface fall + slot drain + outlet;
- aluminum extrusion + insert + screw;
- concrete foundation + base plate;
- removable cover + captive fastener.

The system must be compatible with the authoritative geometry and project material strategy.

### 3. APPLICABLE STANDARD / ENGINEERING REFERENCE
Identify the actual domain that controls the decision:
- project specification;
- jurisdictional building/landscape/accessibility/safety code;
- current national/international drawing or engineering standard;
- manufacturer technical data;
- tested system data;
- published engineering reference;
- comparable built precedent only as bounded supporting evidence.

Do not treat a precedent image as a technical standard.

If the full normative requirement has not been checked, write `REFERENCE DOMAIN IDENTIFIED / COMPLIANCE NOT CLAIMED`.

### 4. RECOMMENDED VALUE OR RANGE
Use the strongest truthful state available:

- `VERIFIED VALUE`
- `LOCKED DESIGN VALUE`
- `RECOMMENDED VALUE`
- `RECOMMENDED RANGE`
- `REFERENCE VALUE`
- `FIELD VERIFY`
- `TBD`

A range is preferable to false precision when multiple technically plausible values remain.

For a recommendation, record why it was selected:
- geometry;
- ergonomics;
- manufacturer range;
- comparable system;
- safety margin;
- maintenance access;
- material/process constraint;
- calculation or scenario analysis.

### 5. SENSITIVE FACTORS
List what could materially change the recommendation.

Typical factors:
- substrate strength/type;
- actual field geometry;
- corrosion/exposure class;
- loads and combinations;
- vibration/fatigue;
- waterproofing/drainage;
- thermal movement;
- material tolerance;
- manufacturing process;
- installer access;
- maintenance/replacement method;
- user population;
- operational state;
- supplier change;
- local code interpretation.

### 6. FIELD / ENGINEER VERIFY ITEMS
State what closes the open condition.

Examples:
- site measurement;
- survey level;
- substrate test;
- structural calculation;
- manufacturer confirmation;
- prototype fit test;
- mock-up;
- drainage test;
- slip test;
- accessibility review;
- tolerance stack review;
- fabrication sample.

`FIELD VERIFY` must identify the thing to verify, not merely display a generic disclaimer.

## 2. Evidence ladder

Use this order when gathering technical evidence:

1. Current project authority / approved geometry/specification.
2. Applicable law/code/standard or responsible specialist requirement.
3. Manufacturer/system technical data for the actual or bounded candidate system.
4. Published engineering/design reference.
5. Built precedent with known system/context.
6. Calculation / geometry-derived inference.
7. Image-derived estimate.
8. AI-generated or stylistic reference.

Lower levels may support design exploration but cannot silently override higher authority.

## 3. Image-derived measurement boundary

If a dimension is estimated from a photo/render/map/screenshot:
- identify the reference object or scale source;
- record perspective/camera uncertainty where relevant;
- state the measurement method;
- record an uncertainty/range rather than false precision;
- mark the dimension as `DERIVED / NOT FIELD MEASURED`;
- prohibit fabrication/construction promotion from that estimate alone.

AI-generated imagery cannot serve as a measurement source for hidden or invented geometry.

## 4. Structural/support boundary

A technical drawing may show support intent without proving structural adequacy.

Separate:
- **geometry relation** — what touches/connects where;
- **design intent** — what is intended to support/carry/retain;
- **recommended member/interface family** — bounded design choice;
- **engineering sizing** — specialist authority;
- **field substrate/foundation truth** — measured/verified authority.

Never use visual plausibility as proof of member sizing, anchor capacity, foundation adequacy or stability.

## 5. Safety/access boundary

For fall edges, stairs, ramps, paths, hand/contact zones, egress, barriers, lighting or other safety-sensitive conditions:
- identify jurisdiction and applicable rule domain before claiming compliance;
- show geometric relationship needed for design review;
- keep unverified dimensions/status explicit;
- distinguish normal, degraded, closed and unknown operational states when the project uses state-based operation;
- do not depict `UNKNOWN` as normally open/usable.

## 6. Material/CMF reality boundary

Separate:
- substrate/material family;
- finish/coating;
- texture/process;
- measurable performance property;
- visual target;
- candidate vs approved state.

A render can communicate visual intent but cannot prove gloss, roughness, corrosion class, slip resistance, coating thickness, hardness, fire rating or durability.

## 7. Fabrication tolerance boundary

Tolerance requires a reason.

Before adding a tolerance, identify:
- functional interface;
- manufacturing process capability;
- inspection method;
- tolerance stack consequence;
- applicable project/industry standard.

If those are absent, retain nominal design intent and mark tolerance as open rather than adding generic ± values.

## 8. Remote-design continuation rule

Missing field evidence is not an excuse to stop design prematurely.

When field closure is unavailable, the required response is:

`CONTINUE DESIGN WITH BOUNDED RECOMMENDATION → SHOW RANGE/ASSUMPTION → IDENTIFY SENSITIVITY → CREATE FIELD-VERIFY SLOT → KEEP PROMOTION GATE OPEN`

This preserves professional depth without pretending the field has been validated.

## 9. Reality-check register

For complex work, maintain a register with these fields:

| item_id | drawing/view | design_action | system | authority/reference | value/range | truth_state | sensitive_factors | close_by | status |
|---|---|---|---|---|---|---|---|---|---|

Critical unresolved items must be visible in `DRAWING_QA`, not hidden in prose appendices.

## 10. Hard blockers

The drawing cannot be promoted for fabrication/construction if any critical item has:
- invented field dimension;
- unsupported structural sizing;
- guessed foundation/substrate condition;
- safety compliance claimed without applicable rule check;
- candidate material presented as approved;
- generic tolerance with no functional/process basis;
- image-derived estimate presented as measured truth;
- unresolved source conflict silently reconciled;
- AI-generated detail treated as technical authority.