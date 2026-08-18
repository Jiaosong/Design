---
name: oleander-data-viz
description: Produce accurate static, animated, interactive, spatial, and presentation-ready visualizations for Oleander. Use whenever the user mentions Oleander tables, XLSX/CSV analysis, animated charts, timelines, maps, diagrams, dashboards, research visualization, SVG/PNG/HTML/MP4 chart exports, or converting project data into visual evidence.
compatibility: Uses Python 3.13 environment C:\Users\Xianmu\.venvs\oleander and may use spreadsheets, QGIS 4, FFmpeg, ImageMagick, Plotly, GeoPandas, or Sites.
---

# Oleander Data Visualization

Transform project data into reproducible visual evidence. Preserve the source data and make every transformation auditable.

## Environment

Use `C:\Users\Xianmu\.venvs\oleander\Scripts\python.exe`.

Core libraries include pandas, Polars, OpenPyXL, XlsxWriter, Matplotlib, Seaborn, Plotly, Kaleido, Altair, NetworkX, OpenCV, GeoPandas, Shapely, PyProj, Rasterio, Contextily, and OSMnx.

Use QGIS 4 for interactive GIS editing and Python/GeoPandas for reproducible spatial transformations. Do not bind scripts to QGIS 3 paths.

## Workflow

1. Inspect source files, units, missing values, time ranges, coordinate systems, and category definitions.
2. Keep raw data unchanged; write cleaned data separately with a transformation log.
3. Choose the visual form from the analytical question, not decoration.
4. Create a visual specification: audience, claim, dimensions, units, palette, typeface, output size, and accessibility.
5. Build the visualization reproducibly.
6. Export:
   - SVG for Illustrator and boards;
   - PNG at explicit pixel dimensions for review;
   - HTML for interaction;
   - MP4/WebM/GIF only when motion adds meaning;
   - XLSX with source/clean/data-dictionary sheets when a table is part of delivery.
7. Validate totals, axes, labels, legends, frame order, map CRS, and export dimensions.

## Spatial authority preservation

Apply this gate to maps, routes, plans, sections, diagrams, spatial networks, site geometry, model projections, product geometry, technical nodes, and any other graphic where shape or relative position carries project meaning.

1. Resolve the current geometry / topology authority before layout. Distinguish **source geometry authority** from the **presentation layer**.
2. If a route, plan, section, map, model view, node geometry, or other spatial object is approved, locked, current, or is the strongest mature existing artifact, reuse that geometry directly. Do not redraw it from memory or from a downstream derivative.
3. **Layout must adapt to authoritative geometry; authoritative geometry must not be distorted to fit layout.** Non-uniform scaling, stretching, compressing, smoothing, straightening, resampling, route re-authoring, invented continuation, or aesthetic simplification is forbidden when it changes spatial reading.
4. When comparing modes, phases, scenarios, audiences, or journey variants, derive each view by **subset / mask / crop / highlight / direction overlay** on the same authoritative geometry. Do not replace the geometry with four newly normalized shapes merely for visual consistency.
5. Existing Mature Design First applies: if an older/current artifact expresses the authoritative geometry more clearly than a newer candidate, preserve the stronger geometry and edit only the weaker presentation layer. Newer file ≠ better authority.
6. Context photographs, renders, AI images, diagrams, UI screens, or board compositions may support spatial reading but never become geometry authority unless the current project authority explicitly promotes them.
7. A presentation-only transform is allowed only when the analytical object itself is explicitly schematic and no real spatial inference will be drawn from it. Mark it `PRESENTATION ONLY / NOT SPATIAL EVIDENCE`. Do not use such a transform in a main spatial-evidence figure.
8. Before promotion, compare the candidate against the strongest existing geometry at matched scale or through path/overlay inspection. Any material loss of topology, route shape, relative position, section profile, scale relationship, or spatial recognizability is a blocker regression.

For source-bound spatial graphics, record:
- geometry/topology source object and version;
- what was preserved unchanged;
- any subset/mask/crop operation;
- any transform and whether it is uniform;
- what the graphic supports and what it does not prove.

## Operational route-state semantics gate

Apply this gate whenever route, path, network, access, facility, service, or wayfinding graphics encode operational states such as `NORMAL`, `DEGRADED`, `CLOSED`, `UNKNOWN`, or equivalent project-specific states.

1. **Topology authority and state authority are separate.** A state overlay may change how a route is interpreted or used, but must not silently rewrite where the authoritative route exists.
2. Color may support state recognition but must not be the only carrier of state meaning. Pair hue with at least one additional visual channel appropriate to the medium: stroke pattern, marker geometry, line weight, endpoint treatment, text, icon, or fill pattern.
3. `CLOSED` must read as a hard operational interruption when that is the project meaning. A closed segment must not look like a lower-confidence or merely less-important open route.
4. `UNKNOWN` is not a weak form of `NORMAL`. When the current project authority requires fail-closed behavior, depict `UNKNOWN` as uncertain / not safely assumable open, and never normalize it into the same continuous open-path grammar.
5. `DEGRADED` must remain distinguishable from both `NORMAL` and `CLOSED`; use a reversible visual degradation such as long dash, reduced line weight, caution marker, or explicit state text without breaking the underlying topology.
6. Critical route-state graphics must survive grayscale / low-color review. Generate or inspect a grayscale derivative and confirm the states remain distinguishable without hue.
7. For screen-based interfaces, meaningful graphical state indicators must remain perceivable at the intended delivery size and should meet the applicable non-text contrast requirement. Do not use low-contrast status styling as a substitute for hierarchy.
8. State labels, legends, and endpoint behavior must agree. A line that visually continues forward must not be labelled `CLOSED`; an `UNKNOWN` label must not sit on a visually normal open path.
9. Multi-state figures must record the state source, timestamp/version where relevant, and whether the state is observed, reported, inferred, assumed, simulated, or placeholder. Visual polish must not promote an inferred or unknown state into observed fact.
10. Before promotion, inspect at least: color view, grayscale view, compact/target-size view, and the highest-risk transition (`NORMAL→DEGRADED`, `DEGRADED→CLOSED`, `UNKNOWN→known`). If state meaning becomes ambiguous in any required view, return `REVISE`.

This gate follows the same truth discipline as spatial authority preservation: **state semantics may change interpretation, not source topology**, and `UNKNOWN` must never be presented as safely open merely because a continuous route line is aesthetically cleaner.

## Service-blueprint causality and recovery gate

Apply this gate whenever an OLEANDER diagram claims to explain how a service, journey, return path, operational handoff, failure mode, or backstage capability actually works.

1. Start from the **actor/task and journey stage**, not from a fixed four-lane template. Add only the lanes needed to explain the real causal chain: `Actor / Frontstage / Backstage / Support / Policy / Data / Owner / Capacity / Failure / Recovery / Evidence`.
2. A visually complete success path is insufficient. If a service can fail through outage, unknown state, capacity, staffing, missed handoff, access need, cancellation, fatigue, or equivalent project-specific conditions, inject the failure at the stage where it occurs.
3. Bind the user-visible state to the backstage state that justifies it. A frontstage `OPEN / CLOSED / UNKNOWN / DEGRADED` message must not exist without an identified confirmation source, owner, or explicit `OPEN / TBD` responsibility gap.
4. Failure inventory alone does not count as recovery design. Connect each high-risk failure to at least one visible action and one backstage/support response using the project-appropriate chain: `DETECT → INFORM → RECOVER → ESCALATE / MANUAL TAKEOVER → FEEDBACK`.
5. **Unknown operational values remain unknown.** Do not invent SLA, staffing level, transport capacity, response time, device uptime, or operator authority merely to make the blueprint look finished. Mark them `OPEN`, `TBD`, `ASSUMED`, `SIMULATED`, or the current project-specific evidence state.
6. Keep service roles distinct. Journey, frontstage, backstage, support system, policy, data, responsibility, and capacity may be related but are not interchangeable lanes. Do not collapse a responsibility gap into a generic “system” box.
7. Preserve journey continuity. The blueprint should make the main actor path readable before the backstage detail; failure/recovery detail may become near-read but must remain traceable to the stage and task it modifies.
8. For no-phone, degraded-network, closed, or fail-closed service conditions, prove that a non-digital frontstage/recovery path exists when the project authority requires one. A digital fallback screen is not sufficient evidence of physical/service continuity.
9. Review the blueprint at both whole-system and stage level. Whole-system read asks whether the causal spine is visible; stage read asks whether `actor → frontstage → backstage/support → owner → failure/recovery` is unambiguous for the highest-risk events.
10. Promotion requires separate verdicts for **diagram quality** and **operational truth**. A service blueprint may be `KEEP FOR TRAINING / DESIGN` while operator data, field state, capacity, accessibility, safety, SLA, or engineering remain `HOLD / OPEN`.

Default review chain:

`ACTOR / TASK → FRONTSTAGE STATE → BACKSTAGE CONFIRMATION → SUPPORT / OWNER → FAILURE INJECTION → RECOVERY → FEEDBACK`

Hard failures:
- success-only blueprint presented as operational completeness;
- failure cards detached from the stage/cause that produces them;
- visible service state with no source/owner or truth state;
- invented SLA/capacity/availability used to close empty boxes;
- digital-only recovery where the current journey requires paper/signage/staff/physical continuity;
- a visually polished blueprint whose responsibility and recovery gaps remain unreadable.

## Motion rules

- Keep axes and color scales stable across frames.
- Use a consistent entity key across time.
- Show time, units, and data source in every frame.
- Avoid animation when small multiples communicate the change better.
- Prefer After Effects for narrative motion graphics after analytical animation is validated.

## Required output

Return the visualization, cleaned dataset, data dictionary, transformation note, source note, and a short statement of what the visual supports—and what it does not prove.

For source-bound spatial work, also return a geometry-authority note identifying the current source/locked object, the preservation operation, and any geometry regression check performed.

## Quality checks

- Reconcile displayed values with the cleaned table.
- Check color-blind legibility and grayscale hierarchy.
- Avoid truncated axes unless clearly justified.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For source-bound spatial work, verify that locked geometry/topology has not been materially distorted, re-authored, or replaced by a presentation-driven approximation.
- Treat non-uniform geometry distortion as a blocker unless the object is explicitly schematic and labelled presentation-only.
- Compare against the strongest mature existing spatial artifact before promoting a redesign; visual polish cannot override a spatial-authority regression.
- For service blueprints, verify that the highest-risk failure is stage-bound, owner/source-bound, and connected to a visible recovery path; a clean lane structure alone is not a PASS.
