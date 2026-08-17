# OLEANDER Technical Drawing — Node Semantics & Spatial-Event Grammar

Status: `candidate extension / PR #172`

Use this module with `ANALYSIS_DRAWING_SYSTEM.md` and `FLOW_DIRECTION_ANALYSIS.md` whenever a drawing contains route nodes, junctions, stations, observation points, service points, thresholds, rest points, content points, transfer points, return/exit points, conflicts, callout targets, or repeated node symbols.

A node is not a circle, pin, icon or label. A node is a **spatial/network event with an explicit role and owner**.

`NODE SYMBOL != NODE SEMANTICS`

`CONTENT POINT != ROUTE JUNCTION`

`LABELLED PLACE != NETWORK NODE`

`NODE POSITION != NODE FUNCTION`

`BIGGER DOT != MORE IMPORTANT NODE`

`ONE SYMBOL FAMILY != ONE NODE TYPE`

## 1. What a node actually is

Before drawing a node, answer:

1. **What event happens here?**
2. **What spatial object/carrier makes that event possible?**
3. **Which system owns the node?**
4. **Which edges/paths/fields connect to it?**
5. **Does it change route choice, mode, direction, speed, state, body behavior, content depth, service access, or safety condition?**
6. **Is stopping/dwelling part of the node, or is it only a pass-through relation?**
7. **Is the node source-grounded, derived, inferred, provisional, or design-created?**
8. **Would the node still be understandable if its text label were hidden?**

If these cannot be answered, the node is not ready to draw.

## 2. Node taxonomy

Do not force all projects to use every class. Classify only what exists.

### `JUNCTION`
A topological branch/merge/intersection in a traversable or analytical network.

Required evidence:
- connected edge set;
- degree;
- branch/merge state;
- owning network;
- source/base carrier.

### `ENTRY_EXIT`
A boundary crossing into or out of the site, analytical frame, route system or service zone.

Required evidence:
- entering/exiting edge;
- boundary/carrier;
- continuation state;
- whether it is bidirectional.

### `TRANSFER / INTERCHANGE`
A change of mobility mode or network family, e.g. BOAT → CABLE, CABLE → WALK.

Required evidence:
- incoming mode/edge;
- outgoing mode/edge;
- transfer object/space;
- service/decision implication if applicable.

### `DECISION`
A point where the user must choose between materially different routes/actions/states.

Required evidence:
- available alternatives;
- decision trigger;
- information/service required;
- Return/fail-closed relation where applicable.

A bend in a path is not automatically a decision node.

### `STOP / REST / RECOVERY`
A node whose primary event is dwell, pause, lean, sit, recover or wait.

Required evidence:
- body/use carrier;
- dwell relation;
- access/egress relation;
- service/maintenance/open-state boundary where relevant.

### `OBSERVATION / VIEW`
A node where a defined spatial/view relation becomes available.

Required evidence:
- viewer position or bounded viewing field;
- target/scene relation;
- body orientation or view direction when material;
- visibility/evidence state.

A scenic label alone does not establish an observation node.

### `CONTENT / READING`
A node that carries optional interpretation, story, scientific/cultural reading or media content.

Required evidence:
- content owner;
- physical/digital/paper carrier;
- optionality;
- relation to the scene or route.

Critical rule: `CONTENT NODE != ROUTE AUTHORITY` unless a separate route/topology source establishes that role.

### `SERVICE`
A node providing information, ticketing, orientation, water, staff help, facilities, charging or other service.

Required evidence:
- service type;
- access relation;
- operating/unknown state if applicable;
- fallback relation.

### `RETURN / RETREAT`
A node whose primary purpose is route closure, retreat choice, exit recognition, fail-closed guidance or recovery of orientation.

Required evidence:
- return/exit edge(s);
- trigger or decision state;
- alternative/continuation relation;
- degraded/closed/unknown behavior when relevant.

A Return node should not be visually subordinated to optional content when Return is decision-critical.

### `THRESHOLD / TRANSITION`
A spatial event where enclosure, aperture, grade, material, light, sound, speed or body relation changes materially.

Examples:
- open → compressed;
- dry → wet edge;
- exterior → interior;
- free movement → controlled passage.

Required evidence:
- before/after carriers;
- transition zone or boundary;
- direction/sequence when applicable.

### `CONFLICT / CROSSING`
A point where modes, flows, edges, service actions or users conflict or cross.

Required evidence:
- conflicting edges/modes;
- crossing geometry;
- priority/state/mitigation if known.

### `TERMINUS / CONTINUATION`
A true network termination or explicit continuation beyond the visible frame.

Do not render an external continuation as an ordinary dead-end node.

### `CALLOUT TARGET`
A graphical annotation target only. It is not automatically a spatial/network node.

This class must never enter route degree/topology calculations unless a separate spatial node occupies the same location.

## 3. Multi-role nodes

One physical place may carry several roles, but one graphic symbol should not silently collapse them.

Example:

`CABLE SOUTH STATION`
- primary role = `TRANSFER`;
- secondary role = `SERVICE`;
- possible role = `DECISION`;
- not automatically = `CONTENT` or `OBSERVATION`.

Record:

`PRIMARY ROLE + SECONDARY ROLES + OWNERSHIP + STATE`.

Use one dominant graphic carrier and subordinate role markers/labels rather than stacking unrelated icons.

## 4. NODE SEMANTICS REGISTER

For serious analysis or strict reconstruction, create a register with at least:

`NODE_ID`
`NODE_CLASS`
`PRIMARY_ROLE`
`SECONDARY_ROLES`
`OWNER_SYSTEM`
`SOURCE / AUTHORITY`
`SPATIAL_CARRIER`
`PAGE / MODEL POSITION`
`POSITION_CONFIDENCE`
`CONNECTED_EDGE_IDS`
`DEGREE`
`INCOMING / OUTGOING / BIDIRECTIONAL`
`MODE_CHANGE`
`DIRECTION_CHANGE`
`DECISION_REQUIRED`
`DWELL_ALLOWED / EXPECTED`
`CONTENT_OPTIONALITY`
`STATE_BEHAVIOR`
`RETURN / FAIL-CLOSED RELATION`
`BODY / VIEW ORIENTATION`
`GRAPHIC_CARRIER_ID`
`LABEL / CALLOUT IDS`
`TRUTH STATE`
`DOES-NOT-PROVE`

Not every field applies to every node; irrelevant fields should be `N/A`, not invented.

## 5. Node topology vs node meaning

Topology and meaning are separate dimensions.

A degree-3 node may be:
- a route junction;
- a transfer station;
- a conflict crossing;
- or merely three analytical lines meeting at one annotation target.

Therefore:

`DEGREE != FUNCTION`.

Likewise, a content point may sit on a degree-2 path without changing route topology.

For every node, test both:

### Topological test
- what edges actually connect?
- is the node required to maintain graph coherence?

### Event test
- what changes here for user/system/space?
- does the event justify a distinct node identity?

## 6. Graphic expression grammar

Node graphics should encode role without turning the sheet into an icon legend.

Recommended channel priority:

`POSITION → CONNECTION GEOMETRY → SHAPE / BOUNDARY → SIZE → STROKE / FILL → SYMBOL → COLOR → TEXT`.

Text is last, not first.

### Junction
Show the connected geometry clearly. The junction can often be understood from the edge topology before any dot is added.

### Decision
Use a visible branch/alternative relation and place the decision marker at the actual choice point. Do not place a large icon nearby and call it a decision node.

### Transfer
Show incoming and outgoing mode carriers meeting at the transfer space/object. Mode icons may reinforce the relation but cannot substitute for it.

### Stop / rest
Show the body/use footprint or dwell zone where scale permits. A chair/rest pictogram without spatial carrier is insufficient for detailed analysis.

### Observation
Show viewpoint + target/view field/orientation where decision-relevant. A camera/eye icon alone is not an observation relation.

### Return
Show return edge/exit/continuation and decision priority. Return cannot exist only as a text label detached from the network.

### Threshold
Show the actual before/after spatial condition or transition band. A vertical line labelled `THRESHOLD` is insufficient unless it corresponds to a real boundary/condition.

## 7. Node size and hierarchy

Do not size nodes by narrative enthusiasm.

Node graphic weight should respond to:
- decision criticality;
- network role;
- safety/return priority;
- legibility at target scale;
- whether the node is primary claim or supporting context.

It should **not** automatically respond to:
- amount of text;
- cultural importance alone;
- number of facts attached;
- desire to make all Rxx/POI labels visible.

Optional content points should normally remain subordinate to route/return/service nodes when the drawing's primary claim is journey or circulation.

## 8. Node-to-line ownership

Every network node must make edge ownership explicit.

Check:
- edge endpoint coordinates actually meet the node;
- connected-edge list matches geometry;
- arrow/direction events do not float through the node without relation;
- node class does not contradict edge class;
- a content/callout node is not accidentally counted as a branch;
- external continuation is not converted to a dead-end dot;
- transfer nodes connect distinct mode families rather than merely overlaying two icons.

`NODE NEAR LINE != NODE CONNECTED TO LINE`.

## 9. Node-to-field ownership

Some nodes belong primarily to a field, not a route.

Examples:
- event point inside an activity field;
- observation point inside a view field;
- rest point inside a recovery zone;
- service point inside an arrival/service field.

Record the field owner explicitly. Do not force every node into route topology.

## 10. Node-to-callout distinction

A black dot at the end of a leader is normally an annotation anchor, not a route node.

Strict reconstruction must distinguish:

`CALLOUT ANCHOR → TARGET OBJECT`

from

`NETWORK NODE → CONNECTED EDGES`.

If both occupy the same page position, preserve separate semantic IDs.

This avoids one of the most common multilayer reconstruction errors: a visually correct black dot being incorrectly promoted into network topology.

## 11. Node expression at different scales

### Context / masterplan scale
Show only nodes that materially affect route/system reading:
- entry/exit;
- transfer;
- major decision;
- major service;
- Return;
- selected anchor observations if they are part of the primary claim.

### Analysis scale
Add:
- secondary decisions;
- conflicts;
- thresholds;
- local observation/rest/content nodes;
- mode/state ownership.

### Detail scale
Show:
- actual body footprint;
- interface/fixing/service relation;
- approach/egress;
- operating zone;
- maintenance/inspection access;
- FIELD OPEN boundary.

Do not use one identical pictogram at all three scales.

## 12. Truth boundary

A node symbol can overstate certainty.

Separate:
- `SOURCE / OBSERVED NODE`;
- `DERIVED NODE`;
- `INFERRED NODE`;
- `DESIGN NODE`;
- `PROVISIONAL / FIELD OPEN NODE`;
- `UNRECOVERABLE NODE`.

A precise point symbol does not prove precise coordinates.

For non-survey relational drawings, state explicitly when node position means only:
- sequence;
- adjacency;
- network relation;
- approximate/bounded location.

## 13. Reconstruction fidelity

When reconstructing a node-heavy reference, compare more than symbol pixels:

### Semantic fidelity
- node class;
- owner system;
- connected edges;
- event role;
- optionality/state.

### Geometry fidelity
- page position;
- connection landing;
- symbol centroid;
- symbol-to-edge offset;
- dwell/view/threshold field relation.

### Graphic fidelity
- shape;
- size;
- stroke/fill;
- icon family;
- label offset;
- repetition density.

A perfect circle at the wrong network event is a failed node reconstruction.

## 14. Node-specific blockers

Automatic `REVISE / HOLD` when:

- a node is drawn but its event/function is undefined;
- a content/POI node is promoted to route junction without route evidence;
- a route junction exists in text but connected geometry does not meet;
- a transfer node shows mode icons but the two mode carriers do not connect;
- a Return node is a label without a return/exit carrier;
- a view node is an eye/camera icon without viewpoint/target relation where that relation matters;
- a callout anchor is counted as a route/network node;
- node degree in the register disagrees with actual geometry;
- all node classes are flattened into one identical dot/icon family when role distinction is decision-relevant;
- node size visually implies importance/precision unsupported by the drawing;
- a precise node symbol implies surveyed coordinates where the source is only relational;
- a child/detail node cannot point back to a parent location;
- a node's primary relation exists only in prose.

## 15. Producer review questions

For every material node ask:

1. What exactly happens here?
2. What spatial/network system owns it?
3. What geometry proves that role?
4. Which edges/fields connect to it?
5. Does its degree match the graph?
6. Does the user change direction, mode, state, speed, body action, attention, or content depth here?
7. Is stopping actually possible/expected, or did I draw a stop icon because the label sounded important?
8. Is it route-critical, service-critical, Return-critical, or optional content?
9. If I hide the text, can I still infer the node's role from geometry?
10. Could this symbol be misread as a different node type?
11. Am I implying precise location or field truth that the source does not support?
12. Is the node represented consistently across plan/section/axon/analysis panels?

If a critical answer is no, producer state remains `REVISE / REVIEW PENDING`.

Producer may record evidence and defects; producer may not self-award `KEEP / MAIN KEEP / PROFESSIONAL FINISH PASS`.
