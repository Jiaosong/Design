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

## Material changes absorbed into OLEANDER

- Added Subject Grounding + One Signature.
- Added analytical grammar before styling.
- Added task -> content -> measure -> grid sequence.
- Added one-grid-per-surface discipline.
- Added position/size/whitespace-before-color hierarchy rule.
- Added 30-second first impression + 3-second first-read gate.
- Added structural-device truth rule.
- Added editable vector bridge with post-refinement data reconciliation.
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
