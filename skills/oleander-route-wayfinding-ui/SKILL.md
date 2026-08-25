---
name: oleander-route-wayfinding-ui
description: OLEANDER route, map, node, navigation, and wayfinding UI skill for travel, exploration, spatial apps, game maps, route modes, current location cues, Return, optional reading layers, and source-grounded relational mapping.
status: candidate
version: 0.1.1
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

#### World-viewport framing gate
Treat mobile composition as **crop / pan / focus over one stable world**, not as a smaller copy of the full network.

Required checks:
- **world identity:** the same authoritative route/world geometry remains underneath every viewport state; viewport changes may alter crop, pan, zoom and emphasis, but must not redraw a more convenient route;
- **crop before scale-down:** first solve context by cropping, panning, progressive disclosure or segment focus. Scale the whole network down only when the task genuinely requires network overview;
- **anchor safe zone:** the active/current node or committed route object must enter a stable readable zone that is not covered by persistent controls, browser chrome, bottom navigation or optional explanation;
- **context continuity:** at least one persistent landmark, route segment, portal or spatial relationship should survive between adjacent viewport states so the user can understand where the camera/viewport moved;
- **node target integrity:** mobile target size and label readability must not be sacrificed merely to keep the entire network visible;
- **world-first proportion:** when ROUTE is the primary task, visible world/route field must occupy enough of the frame to read as an environment or spatial field rather than a decorative card inside a dashboard;
- **overlay restraint:** mode controls, status, explanation and optional reading must not force the world into a mini-map-sized remainder unless those controls are the current primary task;
- **truth boundary stability:** `RELATIONAL / NTS / NOT GPS / FIELD OPEN / STATUS UNKNOWN` semantics persist through crop/focus states and are never visually lost because the viewport moved.

Promotion test:
> **If the phone must shrink the whole network to explain context, framing has failed. Crop / pan / focus before scale-down.**

A full-network overview may still exist as a deliberate state. The failure is using overview-scale as the default merely because it is easier to fit.

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
6. **World-viewport framing** — lock one world geometry, define overview vs exploration scale, active-anchor safe zone, crop/pan continuity landmarks, and controls that may overlap the world.
7. **Mobile composition** — test crop/pan/focus before all-at-once miniaturization; verify target size, near-read and world-first proportion at target viewport.
8. **Interaction** — define node focus, route mode, back/Return, keyboard, touch, and interrupted navigation.
9. **Motion handoff** — route movement must explain continuity, not merely draw a decorative line.
10. **Visual composition handoff** — ensure route itself remains the primary visual when ROUTE is the task.
11. **Independent review** — compare with source and strongest existing design, including a full-network overview vs exploration-viewport framing comparison.

## Hard failure conditions
- source route and optional content are merged without authority;
- a relational path is presented as precise GPS geometry;
- source labels are silently renamed as facts;
- every node is persistently labeled on mobile;
- full network is shrunk until node targets/text become unusable;
- default mobile ROUTE behaves as an all-at-once mini-map merely to keep the complete network visible;
- crop/focus states redraw, bend or re-order the authoritative route instead of changing viewport only;
- active/current anchor sits persistently under navigation, modal, browser chrome or explanation controls;
- adjacent viewport states remove every continuity landmark, making pan/focus feel like unrelated maps;
- route world is reduced to a decorative card while dashboard controls own first read without task justification;
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
  "viewport": {
    "default_role":"exploration|overview",
    "anchor_safe_zone":"defined",
    "continuity_landmarks":["G01","segment:G01-G02"],
    "world_geometry_locked":true
  },
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
WORLD-VIEWPORT ROLE: OVERVIEW / EXPLORATION / FOCUS
WORLD GEOMETRY LOCKED: YES / NO
ANCHOR SAFE ZONE:
CROP / PAN CONTINUITY LANDMARKS:
ALL-AT-ONCE MINI-MAP RISK:
OPTIONAL-CONTENT SEPARATION:
TRUTH BOUNDARY:
SOURCE ↔ UI CONTRADICTIONS:
RUNTIME DEFECTS:
INDEPENDENT VERDICT REQUIRED: YES
```

## Source lineage
Adapted for OLEANDER from information-architecture/wayfinding principles, game-map/HUD patterns, mobile interaction practice, and C04 lessons around official route source extraction, relational maps, Return priority, separation of route authority from optional reading systems, and the failure mode where a full route world is miniaturized into a dashboard-like mobile map.
