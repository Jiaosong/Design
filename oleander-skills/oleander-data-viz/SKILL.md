---
name: oleander-data-viz
description: Produce accurate static, animated, interactive, spatial, and presentation-ready visualizations for Oleander. Use whenever the user mentions Oleander tables, XLSX/CSV analysis, animated charts, timelines, maps, diagrams, dashboards, research visualization, SVG/PNG/HTML/MP4 chart exports, or converting project data into visual evidence.
compatibility: Cross-conversation capability-first. Resolve the actual execution surface per run. May use Python/pandas/Polars/OpenPyXL/XlsxWriter/Matplotlib/Plotly/GeoPandas/QGIS/FFmpeg/ImageMagick or other verified tools when they preserve the required native output. The validated OLEANDER Pro Design Toolchain is Candidate-only until explicit promotion; machine-specific local paths are never a global requirement.
---

# Oleander Data Visualization

Transform project data into reproducible visual evidence. Preserve the source data and make every transformation auditable.

## Environment

Inherit the Current OLEANDER production environment and execution routing. Resolve the Skill/Owner and Required Native Output first, then probe the actual execution surface for this run.

Preferred runtime order for data visualization work:

`ACTUALLY EXPOSED AGENT EXECUTION → ACTIVE SHARED RUNTIME WHEN FIT → VALIDATED CANDIDATE RUNTIME FOR VALIDATION/TRAINING/SUPPORT OR EXPLICITLY LABELED BOUNDED REAPPLICATION → VERIFIED FREE/INCLUDED CLOUD → USER_WEB_MANUAL → CAPABILITY_HOLD`

The Candidate professional shared runtime is located at `90-shared/toolchains/pro-design/` and is governed by `00-governance/runtime/OLEANDER_PRO_DESIGN_TOOLCHAIN_RUNTIME_v0.1.json`. Its Python / ImageMagick / FFmpeg capabilities must be probed per run and must remain labelled Candidate until existing review/promotion requirements are satisfied. Candidate runtime PASS does not make it a default Production Owner.

Legacy machine-specific environment previously used by this Skill: `C:\Users\Xianmu\.venvs\oleander\Scripts\python.exe`. Preserve this as provenance only. It may be used if that exact authorized runtime is actually exposed in a run, but it is **not** the global environment, is not required for another conversation, and must never force local installation.

Core libraries may include pandas, Polars, OpenPyXL, XlsxWriter, Matplotlib, Seaborn, Plotly, Kaleido, Altair, NetworkX, OpenCV, GeoPandas, Shapely, PyProj, Rasterio, Contextily, and OSMnx when the resolved runtime actually provides them.

Use QGIS for interactive GIS editing only when a verified callable/manual execution surface is actually available and the required native output benefits from it; use Python/GeoPandas for reproducible spatial transformations when available. Do not bind scripts to QGIS 3 paths. A documented QGIS version is not execution evidence.

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
8. Record the actual execution surface, runtime/tool version, source/master identity, derived outputs, and any cross-software information loss. Never infer execution from a documented tool or a visually correct derivative.

## Uncertainty-first scenario charts

Apply this gate whenever a displayed value is estimated, inferred, scenario-based, provisional, remotely researched, or awaiting FIELD correction and the uncertainty could materially change interpretation or a design decision.

1. **Recommended value ≠ measured value.** Do not let a recommendation or central estimate read as a measured scalar merely because one number is needed for design advancement.
2. When a plausible range is decision-relevant, make the range the primary quantitative mark and keep the recommended/central value subordinate within it. Use an interval, dot-range, band, or another form that preserves the actual uncertainty structure rather than a precise bar with decorative error marks.
3. Keep unit, range definition/basis, evidence class, confidence/quality state, and FIELD correction status adjacent to the visual when they materially change interpretation; do not hide them in a distant footnote.
4. **Evidence provenance ≠ probability.** If symbol, line style, texture, or another channel encodes `SOURCE-GROUNDED / INFERRED / ASSUMPTION` or another project truth state, state what that channel means. Do not imply that an evidence class is a likelihood scale unless it truly is one.
5. Do not call a design scenario, sensitivity band, expert estimate, allowance, or provisional range a statistical confidence interval unless the statistical method and interval definition actually support that claim.
6. If uncertainty is so large that the visual no longer supports a meaningful ranking/comparison, do not force a ranked chart through polish. State the limitation and preserve the underlying values/table.
7. FIELD absence is not permission to collapse a provisional design value to one neat number. When the project authority permits provisional advancement, preserve the relevant `recommended value + reasonable range + basis + sensitivity + FIELD correction item` structure.
8. Review first-read and truthfulness separately. A range chart can be visually clear and still be semantically wrong; visual polish cannot upgrade `ASSUMPTION` to evidence or `PROVISIONAL` to measured fact.
9. Synthetic calibration data must be labelled synthetic. Example truth-state labels inside a synthetic specimen are test semantics, not project evidence.

For reusable work, record enough of the following to reconstruct the visual claim:
- central/recommended value;
- low/high bounds or explicit range representation;
- units;
- what the range means and how it was derived;
- evidence/truth state;
- confidence/quality state when applicable;
- sensitivity drivers;
- FIELD/measurement correction item;
- `does_not_prove` boundary.

This gate generalizes uncertainty-communication practice to OLEANDER design scenarios while preserving a strict boundary between statistical uncertainty, engineering/design ranges, evidence provenance, and field truth.

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

## Motion rules

- Keep axes and color scales stable across frames.
- Use a consistent entity key across time.
- Show time, units, and data source in every frame.
- Avoid animation when small multiples communicate the change better.
- Prefer browser-native motion, the existing Blender ACTIVE shared runtime, or a verified FFmpeg execution surface when those preserve the required output. The validated Pro Design Toolchain FFmpeg path is Candidate-only for validation/training/support or explicitly labelled bounded reapplication until promoted. Use After Effects or another specialist motion tool only when that actual environment is available and its native medium is required; it is never a default dependency.

## Required output

Return the visualization, cleaned dataset, data dictionary, transformation note, source note, and a short statement of what the visual supports—and what it does not prove.

For source-bound spatial work, also return a geometry-authority note identifying the current source/locked object, the preservation operation, and any geometry regression check performed.

For provisional/scenario charts, also return the range definition/basis, evidence/truth state, confidence/quality state when used, and any FIELD correction item that materially changes interpretation.

For material cross-software output, also record the Current editable/native source, actual runtime used, derivative formats, units/CRS where applicable, known information loss/bakes, and reopen/readback result.

## Quality checks

- Reconcile displayed values with the cleaned table.
- Check color-blind legibility and grayscale hierarchy.
- Avoid truncated axes unless clearly justified.
- Use project-safe relative paths.
- Preserve editable vector or source output.
- For provisional/scenario values, verify that range, unit, evidence/truth state and FIELD boundary remain legible at the intended viewing scale when decision-relevant.
- Never treat chart export success, traceability, or numerical consistency as a substitute for Design Crit or truth-state review.
- For source-bound spatial work, verify that locked geometry/topology has not been materially distorted, re-authored, or replaced by a presentation-driven approximation.
- Treat non-uniform geometry distortion as a blocker unless the object is explicitly schematic and labelled presentation-only.
- Compare against the strongest mature existing spatial artifact before promoting a redesign; visual polish cannot override a spatial-authority regression.
- `TOOL DOCUMENTED ≠ TOOL CALLABLE`; `CANDIDATE RUNTIME PASS ≠ ACTIVE PRODUCTION ROUTE`; record actual runtime evidence before claiming execution.
