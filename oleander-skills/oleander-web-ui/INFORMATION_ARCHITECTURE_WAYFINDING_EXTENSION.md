# OLEANDER Information Architecture + Wayfinding Extension

Status: `CANDIDATE EXTENSION / WEB-UI`

Use when users must find, enter, move through, understand their location within, or recover inside a non-trivial information or route structure.

This extension supports the existing `oleander-route-wayfinding-ui` specialist and `oleander-web-ui` integration route. It does not replace project route topology, content authority or physical-spatial design ownership.

## Core principle

`USER GOAL → ENTRY POINT → CANONICAL HOME → PLACEMENT / GROUPING → LABEL → ORIENTATION → ROUTE DECISION → ROUTE MONITORING → DESTINATION RECOGNITION → RECOVERY → TASK TEST`.

Good content is not findable merely because every page exists. IA is the relationship between user goals and system structure; wayfinding is whether that structure remains legible from the user's current position.

## Task-first IA

Before drawing navigation, identify the important real tasks and plausible entry points. Inventory the content/screens/routes that support them.

Group primarily by user goal and recognizable mental model, not by internal team, database, code module or implementation architecture.

For each material object, decide its structural role deliberately:

- top-level navigation destination;
- page/route;
- tab or mode within a route;
- section within a page;
- filter/facet over peer items;
- cross-link from a related location;
- support/appendix/deep detail;
- search-only recovery result only when deliberate.

Importance alone does not earn a top-level navigation slot. Frequency, task-entry value and orientation consequence matter.

## Canonical-home rule

When the same content or decision appears in several contexts, preserve one Current canonical home and use cross-links, summaries or derived views elsewhere.

Do not duplicate full content merely to make every section appear self-contained. Duplicate homes create maintenance drift and uncertainty about which version is Current.

## Label discipline

Labels should use stable, recognizable user language and remain consistent across navigation, page titles, search results and breadcrumbs.

Reject label chains where the same object changes name at each level. Internal system names may appear as technical metadata, not as the primary user-facing wayfinding vocabulary unless the audience actually uses them.

## Four wayfinding questions

Every non-trivial route should make these states legible:

1. **Orientation** — Where am I now? What larger section/system am I inside?
2. **Route decision** — What valid paths can I take from here toward my goal?
3. **Route monitoring** — After I move, do I still understand whether I am progressing, branching or returning?
4. **Destination recognition** — Is it unmistakable that I arrived at the intended object/state?

Use the minimum appropriate cues: page title, current-nav state, breadcrumb/context path, stable route naming, visible progress, landmarks, section identity, map/topology cues or spatial relation.

Wayfinding cues are not decoration. If removing a breadcrumb/current-state marker/search path makes a deep route materially harder to orient in, that cue is load-bearing.

## Recovery contract

A robust system assumes wrong turns, stale links and incomplete memory.

Provide recovery appropriate to the surface:

- Back / Return behavior with state preservation where required;
- a known anchor/home/root;
- search for complex information spaces;
- breadcrumb/context route where hierarchy is material;
- sibling/related destinations;
- useful empty/error/404 states that expose a next route rather than a dead end.

Search is a recovery path, not a substitute for coherent IA.

## Cross-domain spatial transfer

Physical wayfinding concepts such as paths, edges, districts/zones, nodes/decision points and landmarks may help reason about digital or spatial systems. Use them only when the analogy clarifies real structure.

For actual landscapes, buildings, exhibitions or visitor routes, physical geometry, accessibility, sightlines, signage placement and field conditions require the appropriate spatial/design/technical owners. A software navigation analogy does not prove spatial wayfinding performance.

## Validation

Test the structure against real task prompts and unfamiliar-entry conditions.

Useful attacks include:

- drop into a deep route with no prior navigation history: can the user identify page, section and route home?
- find a named task/object from a plausible starting point;
- take one wrong branch and recover without restarting;
- return after interruption and re-identify current state;
- navigate with sparse/empty data;
- verify the destination title/state matches the link/search label that led there.

Do not call IA validated because the sitemap looks logical to its authors.

## Failure modes

Reject or revise when:

- global navigation mirrors internal implementation structure rather than user tasks;
- every important object is promoted to top-level navigation;
- similar content has several competing canonical homes;
- current location is visually or semantically ambiguous;
- labels mutate between link, route, heading and search result;
- a route depends on browser Back as its only escape;
- search is used to hide incoherent navigation;
- state transitions remove orientation or Return behavior;
- a diagram or map is visually attractive but does not reveal decision points and recovery paths;
- a wayfinding heuristic is reported as observed user performance without testing.

## Boundary

This extension does not impose a universal maximum navigation depth, breadcrumb pattern, color-zone system or 5-second/60-second threshold. Those are context-dependent probes, not automatic PASS criteria.

External study provenance: `jacob-balslev/skill-graph` information-architecture (repository license Apache-2.0 despite some exported skill frontmatter saying MIT) and `Deibler/universal-design-principles` wayfinding (MIT with explicit source-attribution notes). Only independently reformulated structural principles are retained.