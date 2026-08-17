# OLEANDER Technical Drawing — Landscape Analysis Drawing Grammar

Status: `candidate extension / PR #172`

Use this module with `DISCIPLINE_PROFILES.md` and `ANALYSIS_DRAWING_SYSTEM.md` whenever the primary subject is landscape/site/public-realm analysis: topography, hydrology, vegetation, habitat, path systems, edges, views, microclimate, program/dwell fields, maintenance, seasonal change or a synthesis of those systems.

This module exists because a professional landscape analysis drawing must know what every line, node and field **is** before deciding how it looks.

`LINE STYLE != LANDSCAPE MEANING`

`NODE SYMBOL != LANDSCAPE EVENT`

`GREEN FILL != ECOLOGICAL SYSTEM`

`BLUE LINE != WATER FLOW`

`PATH PRESENT != ACCESS LOGIC DRAWN`

`TREE SYMBOL != VEGETATION EVIDENCE`

## 1. What landscape analysis drawings actually carry

Landscape analysis normally combines several different spatial ontologies on one recoverable site base:

1. **TOPOGRAPHY / GROUND** — ridge, valley, contour, slope, terrace, cut/fill, high/low points.
2. **HYDROLOGY / WATER** — drainage path, catchment, inlet, outlet, confluence, storage, flood/retention field, water edge.
3. **MOVEMENT / ACCESS** — road, trail, path, stair/ramp, desire line, junction, entrance, transfer, service/maintenance access, return.
4. **VEGETATION / HABITAT** — plant community, canopy, meadow, wetland, woodland edge, habitat patch, ecological corridor, restoration/management zone.
5. **EDGE / BARRIER / THRESHOLD** — cliff, retaining edge, water edge, fence, inaccessible slope, soft transition, narrow passage, threshold.
6. **VIEW / EXPERIENCE** — viewpoint, view corridor, framed view, reveal, enclosure/opening, compression/release, sound/wind/shade exposure.
7. **PROGRAM / DWELL / USE** — activity surface, rest field, event lawn, play zone, learning area, service zone.
8. **OPERATIONS / MAINTENANCE / STATE** — inspection path, service access, vegetation management, closed/degraded/unknown area, seasonal or operational change.

A landscape analysis is professional when these systems are separately recoverable and their interactions are visible. It is not professional merely because the sheet uses landscape colors, tree icons and arrows.

## 2. Landscape line semantics — define the line before drawing it

Every decision-relevant line should have an ontology/class before receiving color, dash or weight.

### Ground / topography lines

- `CONTOUR` — equal-elevation line. Never use as a generic terrain texture.
- `RIDGE` — local high-line / watershed divider when source-supported or explicitly derived.
- `VALLEY / SWALE AXIS` — local low-line where terrain concentrates flow or defines a spatial depression.
- `BREAKLINE` — abrupt grade/edge change such as top/bottom of bank, curb, wall, terrace edge.
- `SECTION / TRANSECT CUT` — analytical cut line; not a physical site feature.

### Water / hydrology lines

- `SURFACE FLOW PATH` — direction of runoff over terrain.
- `CHANNEL / WATERCOURSE` — persistent or episodic water carrier.
- `DRAINAGE CONNECTION` — designed or existing hydraulic link.
- `WATERSHED / CATCHMENT BOUNDARY` — area divide; not a flow route.
- `OVERFLOW / BYPASS` — state-dependent hydraulic continuation.

A watershed boundary and a drainage path may be visually similar as lines but are opposite kinds of relations: one separates catchments, the other carries water.

### Movement lines

- `VEHICULAR ROAD / CARRIER` — road spatial object.
- `PEDESTRIAN PATH / TRAIL` — traversable pedestrian carrier.
- `CYCLE / SERVICE / MAINTENANCE ROUTE` — mode-specific carrier.
- `DESIRE LINE` — observed/inferred preferred movement; not automatically a built path.
- `ACCESS / CONNECTION` — explicit connection between systems.
- `RETURN / EXIT` — route with retreat/closure function.

### Ecological lines

- `ECOLOGICAL CORRIDOR` — a linear or banded continuity relation between habitat patches; not automatically a walking path.
- `VEGETATION EDGE` — boundary between plant communities/management regimes.
- `RIPARIAN EDGE` — water-land ecological interface.
- `RESTORATION LINK` — proposed ecological connection.

### Experience lines

- `VIEW AXIS / VIEW CORRIDOR CENTERLINE` — orientation from viewer to target or through an opening.
- `SEQUENCE / REVEAL PATH` — experiential sequence bound to actual movement; must not replace the route carrier itself.
- `SOUND / WIND / SHADE DIRECTION` — environmental vector when evidence or a declared design assumption supports it.

### Annotation-only lines

- `CALLOUT LEADER` — label-to-target relation only.
- `CROSS-LAYER CORRESPONDENCE` — links the same location across analytical layers.
- `DATUM / GUIDE` — graphic/technical reference only.

Annotation lines must never be counted as route, drainage or ecological topology.

## 3. Line register

For serious landscape analysis create a `LANDSCAPE_LINE_REGISTER` with at least:

`LINE_ID → SYSTEM → CLASS → WHAT IT IS → SOURCE/DERIVATION → OWNER OBJECT/FIELD → START/END OR CLOSED STATE → DIRECTIONAL? → MEASURABLE? → TRUTH STATE → GRAPHIC CLASS`.

A style name such as `primary`, `secondary`, `red`, `green` or `dashed` is not a sufficient line class.

### Hard question

Before keeping a line, ask:

> If its label and color disappear, can I still explain what spatial phenomenon this geometry represents?

If no, the line is under-defined.

## 4. Landscape node semantics — nodes are events in a landscape system

Landscape nodes are not one universal circle family.

### Topographic / hydrologic nodes

- `HIGH POINT / CREST`
- `LOW POINT`
- `SADDLE`
- `INFLOW / INLET`
- `OUTLET / DISCHARGE`
- `CONFLUENCE`
- `RETENTION / STORAGE NODE`
- `OVERFLOW CONTROL POINT`

These derive from terrain/water relations, not visitor-program importance.

### Movement / access nodes

- `JUNCTION / BRANCH / MERGE`
- `ENTRY / EXIT`
- `TRANSFER`
- `DECISION`
- `RETURN / RETREAT`
- `CROSSING / CONFLICT`
- `TERMINUS / EXTERNAL CONTINUATION`

### Experience / program nodes

- `OBSERVATION / VIEWPOINT`
- `DWELL / REST`
- `PLAY / ACTIVITY`
- `LEARNING / CONTENT`
- `EVENT / GATHERING`
- `SERVICE`
- `THRESHOLD / COMPRESSION / RELEASE`

### Ecological / management nodes

- `HABITAT HUB / PATCH CORE`
- `ECOLOGICAL STEPPING STONE`
- `RESTORATION NODE`
- `MAINTENANCE / INSPECTION NODE`

### Node geometry rule

A landscape node may be a point, small area, linear threshold, junction zone or field. Do not force every node into a dot.

The node geometry should follow the actual event:

- junction → connected edges prove the node;
- viewpoint → viewer position + orientation/view field prove the node;
- retention node → contributing flow + storage field + outlet prove the node;
- rest node → body/use area + access relation prove the node;
- threshold → before/after spatial condition and transition band prove the node.

`ICON + LABEL` without the proving spatial relation is not a completed node analysis.

## 5. Landscape node register

Use:

`NODE_ID → SYSTEM → NODE_CLASS → PRIMARY ROLE → SECONDARY ROLES → SPATIAL CARRIER → CONNECTED LINE/FIELD IDs → DEGREE/CONTRIBUTING RELATIONS → DIRECTION/STATE CHANGE → DWELL? → VIEW/BODY ORIENTATION → TRUTH STATE → SYMBOL CLASS`.

Keep topology and event semantics separate:

`DEGREE != FUNCTION`.

A three-way route junction may also be a decision node, but those are two different facts.

## 6. Landscape fields / areas — the third carrier after lines and nodes

Many landscape phenomena are not best represented as lines or points.

Use explicit field classes:

- `SLOPE BAND`
- `FLOOD / INUNDATION / RETENTION FIELD`
- `CATCHMENT`
- `PLANT COMMUNITY / CANOPY / MEADOW / WETLAND PATCH`
- `HABITAT PATCH`
- `SOIL / GROUND CONDITION`
- `MICROCLIMATE FIELD` — shade, wind exposure, solar, moisture only when sourced/derived/assumed explicitly.
- `PROGRAM / DWELL FIELD`
- `VISIBILITY / VIEW FIELD`
- `RISK / CONSTRAINT / CLOSED / UNKNOWN FIELD`
- `MAINTENANCE / MANAGEMENT ZONE`

A field boundary must state whether it is measured, mapped, derived, inferred, recommended or schematic.

Soft landscape transitions often should not be drawn with the same hard boundary as a surveyed parcel or wall.

## 7. Landscape analysis drawing families

Do not force every landscape question into one synthesis plan.

### A. Topography + hydrology

Show:

`GROUND → RIDGE/VALLEY → FLOW PATH → LOW POINT / CONFLUENCE → STORAGE/OUTLET → DESIGN CONSEQUENCE`.

Professional test: water movement can be traced from contributing ground to discharge/storage without reading prose.

### B. Movement + access

Show:

`CARRIER → EDGE/NODE → MODE → JUNCTION/TRANSFER → DESTINATION → RETURN/EXIT`.

Professional test: one can trace who moves where, on what spatial carrier, and what happens at branch/decision points.

### C. Vegetation + habitat

Show:

`PATCH / COMMUNITY → EDGE → CORRIDOR / GAP → RESTORATION OR MANAGEMENT ACTION`.

Professional test: green color is not the only evidence; plant/habitat structure and continuity are explicit.

### D. View + spatial experience

Show:

`VIEWER POSITION → ORIENTATION → VIEW FIELD/CORRIDOR → TARGET/OCCLUSION → SEQUENCE`.

Professional test: an eye icon is unnecessary to understand why the viewpoint exists.

### E. Body + edge + threshold

Show:

`APPROACH → BODY POSITION → EDGE/LEVEL CHANGE → PAUSE/PASS/RETURN → OPEN CONDITION`.

Use section/longitudinal profile when plan cannot prove body-ground relation.

### F. Program + dwell

Show:

`ACCESS → ACTIVITY FIELD → CAPACITY/INTENSITY BASIS → SUPPORTING SHADE/SEAT/WATER/SERVICE → ADJACENCY/CONFLICT`.

Do not let colored program blobs float without access and ground relation.

### G. Operations + maintenance

Show:

`ASSET/VEGETATION/WATER SYSTEM → SERVICE ACCESS → INSPECTION/REPLACEMENT/CONTROL POINT → STATE/FREQUENCY → FIELD OPEN`.

## 8. Same-site layered atlas rule

Professional landscape work often repeats one site base to isolate different systems. The layers may include topography/hydrology, ecology, circulation, public-space/program, landscape structure and infrastructure.

Use:

`ONE SOURCE SITE BASE → SYSTEM-SPECIFIC CARRIERS → SYSTEM-SPECIFIC NODES/FIELDS → INTERACTION/SYNTHESIS`.

Do not repeat identical linework with only a different color title. Each analytical layer must switch on the geometry needed to explain that system and quiet or omit unrelated carriers without changing source truth.

## 9. Landscape interaction grammar

The strongest landscape analysis usually explains interactions, not isolated inventories.

Examples:

- `RIDGE/VALLEY → DRAINAGE → WETLAND → PATH POSITION`;
- `SLOPE → ACCESSIBILITY → ROUTE HIERARCHY → REST/RETURN`;
- `CANOPY/EDGE → SHADE → DWELL → PROGRAM LOCATION`;
- `HABITAT PATCH → CORRIDOR → PATH CROSSING → CONFLICT/MITIGATION`;
- `VIEW CORRIDOR → VEGETATION OPENING → OBSERVATION NODE`;
- `WATER EDGE → FLOOD FIELD → SEASONAL ACCESS STATE`.

If a conclusion only appears as a text sentence while these carriers remain disconnected, the landscape relationship has not been drawn.

## 10. Case-derived calibration

The following professional-project patterns informed this module:

### Sasaki — Xinyang University South Bay Campus

The project explicitly states that topography and regional hydrology form the foundation of the masterplan; ridgelines and valleys become primary spatial features, while natural drainages, trails, recreation, habitat and stormwater functions are spatially coordinated. Lesson: **terrain/water are not background texture; they are organizing geometry that drives paths, program and landscape typology.**

### Sasaki — Chongming Island Xincunsha Master Plan

The plan studies hydrological connection and wildlife movement, uses water capture/treatment strategies, and describes nodes that connect the internal landscape system to the public waterfront. Lesson: **nodes are defined by what landscape systems they connect; water diagrams must carry capture/store/filter/reuse relationships, not generic blue arrows.**

### Turenscape — Sokolniki Park Tea Party Matrix

The design strategy explicitly separates nodes, grid and surfaces, then adds layers for allotment, circulation, landscape and architecture. Lesson: **landscape analysis can legitimately use repeated-site layered diagrams, but each layer must own a distinct spatial ontology.**

### Sasaki — Bonnet Springs Park

The circulator and designed hills jointly shape the main park areas; grading and micro-grading later make those sketched lines physically real. Lesson: **a landscape circulation line is not an abstract arrow: it can be the geometric armature that shapes topography, program boundaries, accessibility and sequence.**

### Sasaki — Emory University Framework Plan

The project presents open-space and connectivity systems as separate plan diagrams before recombining them into a framework. Lesson: **separate analytical systems when their carriers differ; synthesis comes after legible system drawings.**

## 11. Review questions

For each landscape-analysis drawing ask:

1. What exact phenomenon does every line represent?
2. Is that phenomenon really linear, or should it be a field/area?
3. What exact event does every node represent?
4. What geometry proves that node/event?
5. Are topography, drainage, movement, ecology, view and annotation lines kept semantically distinct?
6. Are program/green/hydrology colors attached to spatial carriers rather than floating labels?
7. Can water, movement, view or habitat continuity be traced without prose?
8. Does the analysis show interactions between systems rather than only inventory them?
9. Is a hard boundary being used for something that is actually a gradient/uncertain transition?
10. Does a section/profile exist where plan alone cannot prove slope, edge, water or body relation?
11. Are management, maintenance, seasonal and operational states visible when they materially affect the design?
12. With text hidden, would a landscape architect still understand the main spatial relationship?

Any critical `no` keeps the drawing at `REVISE / REVIEW PENDING`.

## 12. Landscape-analysis blockers

Automatic `REVISE` triggers include:

- contours used as decorative texture rather than elevation evidence;
- arrows drawn over terrain without a known drainage/movement/environmental meaning;
- watershed boundary mistaken for flow direction;
- all R/POI/content locations drawn as identical route nodes;
- green blobs called ecology without patch/corridor/edge/plant-community logic;
- tree symbols used as proof of species, age, root zone or planting density without source authority;
- viewpoint shown as an eye icon without viewer-target/view-field relation;
- activity/program zone shown without access, body/use or ground relation;
- hydrology shown only as blue color with no inlet/flow/storage/outlet relation;
- path network shown without junction/branch/return semantics;
- hard polygon boundaries used for uncertain ecological or microclimate gradients without qualification;
- landscape relationship stated only in prose while the site geometry remains unchanged;
- maintenance or seasonal state materially controls feasibility but is omitted.

Producer may self-check carrier semantics and structure, but cannot self-award `KEEP`, `MAIN`, `PROFESSIONAL FINISH`, `FIELD PASS` or Promotion.
