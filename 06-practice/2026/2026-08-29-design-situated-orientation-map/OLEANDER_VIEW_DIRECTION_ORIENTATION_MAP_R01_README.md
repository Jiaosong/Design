# 2026-08-29｜Design Process / Route-Orientation / L5｜Situated Map Orientation

STATUS: `TRAINING_MODE / PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / UNVERIFIED / NO_PROJECT_USAGE / NO_PROMOTION`

## GAP
Recent DESIGN Practice evidence covered task→control grouping, environmental requirement→section, and site constraint→placement/orientation. This run tests a different boundary: whether **on-site orientation media is designed in the visitor's situated frame** (body direction + route direction + self-location + referenced view) rather than as an independent graphic object.

## KNOWLEDGE READ STATE
Read order followed Current authority:
1. Notion `OLEANDER｜设计知识库（Design）` root Current Authority.
2. Notion `OLEANDER Knowledge Retrieval & Lifecycle｜知识库机制 v1.0`.
3. GitHub main Skill Registry / REVIEW / Work Coordination / Priority Queue / Design Process Candidate.

Current Priority Queue contains `PRJ-C04-DIGITAL-INTERACTION`, owned by `PRESENTATION`; DESIGN therefore does not enter Project Mode or mutate that object.

No Legacy/K06/chronology carrier was used as default authority.

## EXTERNAL DISCOVERY

### Source A
National Park Service, Harpers Ferry Center — **Wayside Planning**  
URL: https://www.nps.gov/subjects/hfc/wayside-planning.htm  
Accessed: 2026-08-29  
Relevant content: NPS distinguishes map orientation by wayside context; for a low-profile wayside, the map should be oriented in the direction the visitor is looking.

### Source B
National Park Service — **Accessibility Guidelines for Interpretive Media / Wayside Exhibits**  
URL: https://www.nps.gov/features/hfc/guidelines/  
Accessed: 2026-08-29  
Relevant content: wayside exhibit sites should offer clear, unrestricted views of park features referenced by the exhibit; basic orientation is a visitor program that should be delivered accessibly.

### Rights boundary
NPS text is used only as a factual professional reference and independently paraphrased. No NPS logo, visual identity, map style, template, illustration, fixed dimensions, typography system, or copyrighted artwork is copied.

## CAPABILITY MAPPING / MATERIAL DELTA
Existing `oleander-design-process` already owns route/system analysis, relation diagrams, spatial reasoning, IA/user flow/state, options and deletion tests (>60% coverage).

External material delta:
- map orientation can depend on the viewer's situated facing direction in a defined wayside context;
- referenced-view visibility and panel placement are part of the orientation system;
- this creates a coupled spatial+information-design problem, not merely a map-styling problem.

Decision: **EXTEND through Practice evidence only**. No parallel Skill, no Current Rule change.

Rejected / not transferred:
- a universal prohibition on north-up maps;
- NPS-specific low-profile base dimensions;
- accessibility dimensions/standards not independently validated here;
- NPS cartographic identity or templates;
- claim that this synthetic exercise is compliant with any NPS project standard.

## DESIGN QUESTION / INPUTS / CONSTRAINTS / E-I-A-D
Question:
For a site-specific low-profile orientation point, can body direction, route direction, self-location and the referenced landmark remain mutually consistent after styling/labels are removed?

Inputs:
- synthetic trail bend;
- viewer faces east/right;
- visible landmark ahead;
- one low-profile panel;
- `YOU ARE HERE` anchor.

Constraints:
- NTS;
- no real site;
- no accessibility/fabrication/structural approval;
- no universal north-up rule.

EVIDENCE:
NPS distinguishes orientation by wayside context and requires referenced features to remain visible.

INFERENCE:
The map and its placement participate in situated route-reading; they are not independent graphic layers.

ADVERSE:
- visitor is moving;
- panel is placed in the landmark sightline;
- self-location anchor is shifted forward.

DESIGN CONSEQUENCE:
Co-orient body/map/view for this specific low-profile context; place the panel outside the critical referenced sightline; keep self-location exact.

## ARTIFACT / OPTIONS
Editable:
- `OLEANDER_VIEW_DIRECTION_ORIENTATION_MAP_R01.svg`

Rendered readback:
- full-size PNG;
- 50% grayscale PNG.

A / REJECT — North-up by default:
viewer faces east, map stays north-up, panel blocks the referenced landmark.

B / KEEP candidate — Body / Map / View Co-oriented:
map top matches forward view; YAH anchors the current position; panel moves outside the landmark sightline.

C / REVISE — Rotated Map, Wrong Anchor:
map rotation is correct but YAH is shifted to the next junction, making orientation untrustworthy.

## A/B / ATTACK
1. `ROTATION ATTACK`: A requires mental map rotation before action.
2. `SIGHTLINE ATTACK`: moving panel into the referenced view breaks the interpretation relation.
3. `LABEL-OFF`: B must preserve viewer→path→landmark geometry without prose.
4. `ANCHOR ATTACK`: C proves correct rotation does not compensate for false self-location.
5. `GRAY50`: relation must survive without hue.

## ACTUAL READBACK / FAILURE / ROOT CAUSE
First full-size PNG readback found a real artifact failure: the Chinese title rendered as missing-glyph boxes because the SVG used Arial.

Root cause:
`editable text existence ≠ readable text output`; font support is part of actual artifact readback.

Repair:
- replaced SVG text family with available `Noto Sans CJK SC` while keeping text as vector-editable text objects;
- regenerated full-size PNG and Gray50;
- reopened full-size output.

Retest:
- title renders correctly;
- A/B/C relations remain legible;
- no panel-text collision;
- the design rule survives grayscale.

## PROFESSIONAL CRIT
- first read: PASS after font repair;
- causal relation: PASS for bounded Practice;
- route / map / view coupling: PASS;
- counterexample quality: PASS (C);
- text/editability: PASS after repair;
- real wayfinding/accessibility/site validity: HOLD;
- independent professional review: HOLD.

## TRANSFER RULE
Bounded Practice claim:

`SITUATED VIEWER FRAME → SELF-LOCATION → ROUTE DIRECTION → REFERENCED VIEW → MEDIA ORIENTATION / PLACEMENT`

For **site-specific low-profile orientation media**, decorative styling and labels should not be the only thing making these relationships coherent.

This is explicitly **not** a universal north-up prohibition. NPS itself distinguishes large-area, repeated-location, kiosk and low-profile contexts.

## KNOWLEDGE WRITE HANDOFF
Write state: `PRACTICE_EVIDENCE / SUPPORT / SCOPED / UNVERIFIED`.

Suggested Existing Owner:
`oleander-design-process` / Route + IA + spatial-relation practice.

Relations to carry into KNOWLEDGE closure:
- Source: NPS Wayside Planning; NPS accessibility/wayside guidance.
- Domain: design process / wayfinding / information-spatial relation.
- Method relation: `oleander-design-process`.
- Evidence: editable SVG + rendered readback + repair note.
- Freshness: external web sources accessed 2026-08-29.
- Trust: `UNVERIFIED` pending independent/current professional review.

Do not migrate this directly to Current Rule. KNOWLEDGE owns Migration Closure / Relation Closure.

## STATUS
`PRACTICE_EVIDENCE / EXTERNAL-SOURCE-CALIBRATED / UNVERIFIED`

No `PROJECT_USAGE_EVIDENCE`, `VALIDATED_CANDIDATE`, or `ACTIVE` promotion.
