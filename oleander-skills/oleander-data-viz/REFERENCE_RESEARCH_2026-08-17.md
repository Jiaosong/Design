# OLEANDER Data Viz — External GitHub Reference Research

Date: 2026-08-17  
Branch: `agent/data-viz-design-quality-v0.2`  
Purpose: strengthen the existing `oleander-data-viz` skill without replacing OLEANDER governance or inventing a parallel method.

## Sources actually inspected

1. Anthropic — `anthropics/skills/skills/frontend-design/SKILL.md`
   - Ground design in the real subject and audience.
   - Treat structure as information; numbering/dividers/labels must encode something real.
   - Use one memorable signature, then keep the rest restrained.
   - Work in design/critique passes instead of jumping from brief to code.

2. plugin87 — `plugin87/ux-ui-agent-skills`
   - `.claude/skills/design-review/SKILL.md`
   - `workflows/design-review.md`
   - `.claude/skills/redesign/SKILL.md`
   - `taste/design-taste.md`
   - Useful transfer: 30-second first impression, prioritized findings, audit-first redesign, anti-template checks, unequal visual weight, exact grid/rhythm, content-specific copy.
   - Not transferred as authority: weighted scores cannot override OLEANDER hard vetoes or independent KEEP requirements.

3. oskar-q — `oskar-q/grid-systems/SKILL.md`
   - Task and content determine the grid.
   - Causal chain: task -> content -> measure/density -> grid + typography + spacing -> layout.
   - One grid per surface; derive sub-layouts by span.
   - Position/size establish hierarchy before weight/color.
   - Data/images/captions snap to modules.
   - Poster/hero analytical surfaces need one dominant element; 60–80% is a useful starting diagnostic, not a mandatory template.

4. Observable — `observablehq/plot/README.md`
   - Layered marks + scales as a concise grammar of graphics.
   - Transfer: lock analytical grammar before styling.

5. Vega-Lite — `vega/vega-lite/README.md`
   - High-level grammar for visual analysis.
   - Transfer: explicit data/transform/mark/channel/scale/layer/facet contract.

6. RAWGraphs — `rawgraphs/rawgraphs-app/README.md`
   - Designer-oriented bridge between tabular data and editable SVG/vector graphics.
   - Transfer: preserve raw/clean/spec -> SVG -> design refinement -> reconciliation chain.

7. D3 — `d3/d3`
   - Low-level, web-standard data-driven graphics using SVG / Canvas / HTML.
   - Transfer: use D3 when the task genuinely needs custom marks, unusual spatial layout, bespoke interaction or controlled motion that a higher-level grammar cannot express cleanly.
   - Do not choose D3 merely for prestige; low-level freedom increases the burden of accessibility, responsive behavior, regression testing and reproducibility.

8. AntV G2 — `antvis/G2` v5
   - Progressive + declarative visualization grammar for dashboards, exploration and storytelling.
   - Rejects a fixed chart-typology approach in favor of marks, transforms, scales, coordinates and compositions, with data-driven animation and action-based interaction.
   - Transfer: tool choice should preserve the same analytical grammar across simple and advanced figures rather than switch to ad-hoc drawing as complexity grows.

9. kepler.gl — `keplergl/kepler.gl`
   - High-performance geolocation exploration built for large spatial datasets, with map state/layers and spatial aggregation.
   - Transfer: use a true spatial stack only when authoritative coordinates/CRS/geolocation data exist and the analytical question is geographic.
   - A relation-only or diagrammatic network must not be promoted to a geographic map simply because a mapping tool can render it.

10. Datawrapper — `datawrapper/datawrapper`
   - Inspected as a mature public data-visualization product/tool reference.
   - Transfer is limited to the product principle of fast, publication-oriented chart production; OLEANDER does not treat Datawrapper defaults as an aesthetic authority or allow tool defaults to replace project-specific hierarchy.

11. AntV — `antvis/chart-visualization-skills`
   - The repository separates a generic `chart-visualization` routing skill from renderer-specific skills such as `antv-g2-chart`, `antv-g6-graph` and `antv-x6-editor`.
   - The generic skill is intentionally task/type oriented: inspect the data/request, choose a chart family, construct a structured request, render, and return the result. This is useful for intent routing but is not a sufficient professional-design gate for OLEANDER.
   - The G2-specific skill contains runtime/version constraints and precise API guardrails. Transfer: **design policy and renderer syntax must remain separate layers**. A renderer adapter can prove that code is legal for a given library; it cannot prove visual hierarchy, evidence quality or professional finish.
   - The repo also maintains dedicated evaluation datasets and targeted rerun IDs for G2/G6/X6 retrieval/code accuracy. Transfer: after a skill change, OLEANDER should retain focused regression cases for the exact failure mode rather than rely only on broad generic prompts.

## Tool routing extracted from the comparison

Use the highest-level deterministic system that can express the analytical claim without loss:

1. **Plot / Vega-Lite / G2 class** — default for standard analytical charts, layered marks, faceting and common interactions.
2. **RAWGraphs / vector bridge** — when a designer needs an editable SVG handoff for typographic/compositional refinement.
3. **D3 class** — when custom geometry, bespoke interaction, spatial layout or motion is materially necessary and cannot be expressed cleanly above.
4. **GeoPandas / QGIS / kepler.gl class** — only for real geographic data with authoritative CRS/coordinates or explicit exploratory geolocation analysis.
5. **SVG/HTML direct drawing** — acceptable for relational/diagrammatic systems when the object is not pretending to be a statistical or geographic chart; all semantics must remain machine-readable in a companion data/spec file.

Tool sophistication is not a quality score. A simpler declarative chart with stronger truth/hierarchy outranks a more technically elaborate custom visualization that obscures the claim.

## Skill architecture extracted from the comparison

Keep three layers separate:

1. **Visualization design policy** — analytical question, truth boundary, hierarchy, composition, annotation, accessibility and independent review. This is `oleander-data-viz` core.
2. **Intent / form router** — decide whether the task is comparison, trend, distribution, topology, flow, geographic, explanatory diagram, etc., and select the appropriate representation/tool family.
3. **Renderer adapter** — tool/version-specific syntax, runtime constraints, export behavior and debugging rules for G2, D3, QGIS, Plotly, etc.

`RENDERER VALID != VISUALIZATION VALID != DESIGN KEEP`.

This prevents renderer documentation from bloating the design skill and prevents a technically legal chart from being promoted simply because its API usage is correct.

## Evaluation architecture extracted from the comparison

For changed visualization skills, maintain both:

- **broad golden cases** covering truth/accessibility/data correctness;
- **targeted regression cases** keyed to the exact discovered failure, e.g. equal-weight network, card-wall evidence diagram, cleaner-but-weaker redesign, or vector-refinement data drift.

Rerun targeted cases after each material skill change before broad promotion. Retrieval/code-syntax evals and actual visual-design evals remain different gates.

## Material changes absorbed into OLEANDER

- Added Subject Grounding + One Signature.
- Added analytical grammar before styling.
- Added task -> content -> measure -> grid sequence.
- Added one-grid-per-surface discipline.
- Added position/size/whitespace-before-color hierarchy rule.
- Added 30-second first impression + 3-second first-read gate.
- Added structural-device truth rule.
- Added editable vector bridge with post-refinement data reconciliation.
- Added tool-routing rule: highest-level deterministic grammar first; custom D3/geo stacks only when the claim requires them.
- Added explicit separation of visualization design policy / intent router / renderer adapter.
- Added targeted visual-quality regression cases alongside existing broad golden cases.
- Added diagnostic review lenses without allowing score averaging to defeat OLEANDER hard vetoes.

## What remains uniquely OLEANDER

- Current Authority / Source Authority / truth boundaries.
- Evidence / Inference / Assumption / Decision / Unknown separation.
- Existing Mature Design First.
- NO COMPRESSION / NO LOSS.
- Artifact existence != Design quality.
- Independent Design Verdict Policy; producer cannot self-KEEP.
- FIELD / survey / engineering / implementation boundaries.
- Project-specific role hierarchy such as Route / Service / Return > optional reading when applicable.

## Does not prove

Reading these repositories does not prove the revised OLEANDER skill is better. Promotion requires real practice artifacts, regression cases, actual-preview review and independent verdict evidence.
