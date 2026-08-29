# External Skill Digestion — Data-table Information Design — 2026-08-29

Status: `CANDIDATE EXTENSION EVIDENCE / NO_PROMOTION`

## Sources read

1. `SkillMedev/skills/skills/data-table-design/SKILL.md`
   - root license: MIT.
   - read: reader-question framing, alignment, precision, sorting, totals, density, headers, before/after artifact and quality bar.
2. U.S. Web Design System table guidance and table accessibility tests.
   - cross-check: semantic headers, captions, sortable-state behavior, raw sort values, focusable scroll containers and project-level accessibility testing.

## Current comparison

Current `oleander-data-viz` already preserves units, evidence states, uncertainty and analytical truth, but tables had no dedicated Candidate extension for comparison ownership, source precision, summary-row semantics and medium transfer. This is a narrow extension to Data Viz, not a new data-design Core Skill.

## Accepted material delta

- define reader question/action before formatting;
- `display precision ≤ evidence precision`;
- preserve units, denominator and missing/unknown semantics at point of reading;
- explicit row/column ownership and deliberate sort/group order;
- totals/averages/rates only when mathematically meaningful;
- remove/relocate columns only against task/mandatory-content logic;
- responsive/print variants must preserve the original comparison task;
- sortable tables require actual state, raw sort semantics and accessibility implementation evidence.

## Rejected / bounded-only

Not promoted as universal rules:
- fixed seconds-to-answer metric;
- fixed max rows/columns;
- fixed zebra-striping threshold;
- fixed decimal-place recipes;
- K/M/B as mandatory abbreviation;
- totals always at bottom;
- right-align every numeric field without exception;
- fixed slide table limits.

## Output

Created `oleander-data-viz/DATA_TABLE_INFORMATION_DESIGN_EXTENSION.md`.
Golden regression target: `SK-DV-004`.

## Maturity

`EXTERNAL STUDY + OFFICIAL COMPONENT CROSS-CHECK → CANDIDATE EXTENSION / SUPPORT / SCOPED / NO_PROJECT_USAGE / NO_PROMOTION`.