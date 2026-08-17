---
name: oleander-route-wayfinding-ui
description: OLEANDER route, map, node, navigation, and wayfinding UI skill for travel, exploration, spatial apps, game maps, route modes, current location cues, Return, optional reading layers, and source-grounded relational mapping.
status: candidate
version: 0.1.0
---

# OLEANDER Route & Wayfinding UI

## Purpose
Translate route evidence and spatial relationships into a usable designed wayfinding system without confusing source facts, inferred topology, optional content, and visual storytelling.

This skill is for maps, game-like route fields, guide nodes, journey modes, POIs, scene markers, Return paths, and contextual navigation.

## Authority model
Always separate these layers:

```text
SOURCE ROUTE AUTHORITY
→ extracted nodes / edges / order / service relationships
→ relational translation
→ designed wayfinding UI
→ optional interpretation / reading / memory layers
```

Never let the downstream UI overwrite upstream route authority.

For each route element record:
- object ID;
- source;
- source type;
- observed/extracted relation;
- inference if any;
- design translation;
- does-not-prove boundary.

## Core principles
### 1. Answer five questions
Every route interface must help the user answer:
1. Where am I / what is my current context?
2. What is around or ahead?
3. Where can I go?
4. What changes if I choose this path?
5. How do I return / recover?

### 2. Guide authority ≠ optional content
Do not merge route/POI authority with interpretive or collectible content unless Current Authority explicitly says they are the same system.

Examples:
- GUIDE nodes may define navigation;
- reading nodes may be optional overlays;
- journal/memory entries may record experience;
- none should silently redefine the physical route.

### 3. Preserve topology before geometry
If only order/connectivity is supported, show a relational map and label it accordingly. Do not imply GPS precision, scale, walking time, slope, live closure, or exact geometry without evidence.

### 4. Translate, do not photocopy
When converting an official or source map:
- extract node names;
- extract node order;
- extract branches/returns;
- extract portals/services;
- extract route variants;
- preserve meaningful directional tendency when supported;
- redesign hierarchy, density, interaction, and visual language for the target product.

Do not reproduce the source board's visual clutter or force all source labels into one mobile viewport.

### 5. One world, multiple readings
Prefer one stable route/world skeleton with different route modes, highlights, focus states, and progressive disclosure over drawing separate contradictory maps for each mode.

### 6. Mobile route views are viewports into a larger world
Do not miniaturize an entire desktop/visitor-center map until everything is tiny.

Use:
- pan/scroll/segment exploration;
- focus-on-node;
- label-on-approach;
- portals and anchor landmarks;
- compact route-mode switching;
- current-node context;
- Return/exit always recoverable.

### 7. Node hierarchy
Define at least three node levels when the network is dense:
- portal/service anchors;
- major route/scene anchors;
- secondary POIs.

Not every node needs a persistent label.

### 8. Route mode hierarchy
If there are multiple route modes, avoid equal-weight large buttons unless choosing among routes is the primary task.

Prefer compact mode index + active route summary + highlighted path.

### 9. Return is not merely another node
Return/recovery is a persistent system behavior. It may be visually quiet in normal exploration, but must become dominant when risk, closure, unknown status, or end-of-route context requires it.

### 10. Truth boundary is visible enough to prevent false reading
Use concise boundary labels such as:
- `RELATIONAL / NTS`;
- `NOT GPS`;
- `FIELD OPEN`;
- `STATUS UNKNOWN`.

Do not turn these into a governance dashboard. Place them where they prevent misinterpretation without stealing first read.

## Workflow
1. **Source extraction** — list nodes, exact source labels, order, branches, portals, services, route variants.
2. **Evidence classification** — mark `EVIDENCE / INFERENCE / ASSUMPTION / DECISION`.
3. **Topology model** — define nodes and edges before styling.
4. **Product translation** — define what the user needs at default, focus, route-choice, Return, unknown/closed, and optional-reading states.
5. **Node hierarchy** — classify portal / major / secondary / optional content.
6. **Mobile composition** — use a viewport/scroll/pan/focus strategy rather than all-at-once miniaturization.
7. **Interaction** — define node focus, route mode, back/Return, keyboard, touch, and interrupted navigation.
8. **Motion handoff** — route movement must explain continuity, not merely draw a decorative line.
9. **Visual composition handoff** — ensure route itself remains the primary visual when ROUTE is the task.
10. **Independent review** — compare with source and strongest existing design.

## Hard failure conditions
- source route and optional content are merged without authority;
- a relational path is presented as precise GPS geometry;
- source labels are silently renamed as facts;
- every node is persistently labeled on mobile;
- full network is shrunk until node targets/text become unusable;
- route modes become a dashboard of equal-weight cards;
- Return exists visually but cannot interrupt or recover;
- route animation obscures current location or destination;
- new visual curve contradicts supported direction/order without disclosure;
- route line style dominates the landscape/world without task justification.

## Required data shape
Recommended machine-readable structure:

```json
{
  "nodes": [{"id":"G01","label":"...","role":"portal|major|secondary|service","source":"..."}],
  "edges": [{"from":"G01","to":"G02","relation":"ordered","confidence":"high"}],
  "modes": [{"id":"A","sequence":["G01","G02"],"return_policy":"..."}],
  "boundaries": {"gps":false,"live_status":false,"field_verified":false}
}
```

## Review output
```text
SOURCE AUTHORITY:
EXTRACTED TOPOLOGY:
PORTALS / SERVICES:
MAJOR / SECONDARY NODES:
ROUTE MODES:
CURRENT-CONTEXT CUE:
RETURN / RECOVERY:
MOBILE DENSITY:
OPTIONAL-CONTENT SEPARATION:
TRUTH BOUNDARY:
SOURCE ↔ UI CONTRADICTIONS:
RUNTIME DEFECTS:
INDEPENDENT VERDICT REQUIRED: YES
```

## Source lineage
Adapted for OLEANDER from information-architecture/wayfinding principles, game-map/HUD patterns, mobile interaction practice, and C04 lessons around official route source extraction, relational maps, Return priority, and separation of route authority from optional reading systems.