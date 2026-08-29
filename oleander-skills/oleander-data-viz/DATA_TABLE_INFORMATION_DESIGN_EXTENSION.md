# OLEANDER Data Table Information Design Extension

Status: `CANDIDATE EXTENSION / DATA-VIZ`

Use when a table itself is the primary analytical/readout object and the main problem is comparison, ranking, exact lookup, structured scanning, precision, totals, sorting or responsive/print transfer. This is not database-schema design and does not replace chart selection when a chart communicates the analytical question more clearly.

## Core contract

`READER QUESTION / ACTION → SOURCE SEMANTICS + UNITS + EVIDENCE PRECISION → COMPARISON TASK → ROW / COLUMN OWNERSHIP → ORDER / GROUP / TOTAL LOGIC → FORMATTING → MEDIUM / RESPONSIVE BEHAVIOR → COLD-READ + ACCESSIBILITY CHECK`.

A table is not a styled data dump. Its structure should make the intended comparison easier without changing the source meaning or implying unsupported precision.

## Reader-question gate

Before formatting, state:
- the reader's primary question;
- the action/decision the table supports;
- which dimensions/entities are compared;
- which metric(s) are primary and secondary;
- whether exact lookup, ranking, temporal scan or category comparison is the dominant use;
- what information is legally/operationally required even if not primary.

Columns that do not support the task are candidates for deletion, relocation or disclosure, not automatic deletion.

## Source semantics and precision

For each numeric field, preserve:
- source unit;
- denominator/base where relevant;
- whether value is measured, estimated, inferred or scenario-based;
- meaningful/significant precision supported by the source;
- missing/unknown/not-applicable semantics;
- transformations used for display.

`DISPLAY PRECISION MUST NOT EXCEED EVIDENCE PRECISION`.

Do not use export-level decimal places merely because they exist. Do not round away a material distinction. Precision is a source/decision question, not a fixed external formatting recipe.

## Row / column ownership

Make the comparison relation explicit:
- text/category labels usually own the lookup axis;
- numeric values should be aligned consistently for magnitude comparison when the medium supports it;
- headers must identify the metric and make units recoverable at the point of reading;
- grouped/compound headers must keep semantic association unambiguous;
- repeated labels may be frozen/repeated on scrolling or paginated variants when needed.

Alignment is a comparison tool, not an ideology. Do not force a pattern when it breaks the actual script, content type or medium.

## Order and grouping

Choose order from the reader question:
- ranking → order by the governing metric when appropriate;
- time → chronological unless another analytical task clearly overrides it;
- categories → meaningful domain order, grouped relation or alphabetical fallback;
- operational sequences → preserve the real process order when that is the point.

Never ship accidental database/query order as though it were a design decision.

## Totals, ratios and derived rows

Only show summary rows that are mathematically and semantically meaningful.

For each total/average/subtotal/rate:
- define the aggregation;
- confirm denominator/weighting where applicable;
- label the statistic explicitly;
- distinguish total from average/rate/index;
- do not total percentages/ratios merely because a column is numeric;
- do not create a grand total when combining unlike units/entities.

Visual emphasis on a total must not upgrade a questionable aggregation into a valid one.

## Density and medium transfer

There is no universal maximum row/column count. Diagnose density from the task and medium.

For slide/board/print/browser/mobile variants, consider:
- whether all rows must be visible at once;
- whether the comparison requires horizontal adjacency;
- whether grouping/splitting is safer than shrinking type;
- whether a chart + detail table pair is more appropriate;
- horizontal scrolling/frozen labels for browser use;
- column prioritization or alternate mobile representation;
- pagination/repeated headers in print.

Do not stack a complex table responsively if doing so destroys cross-column comparison or header ownership.

## Sort / interaction semantics

For interactive tables:
- enable sorting only on fields whose semantics support it;
- preserve a clear current sort state;
- use raw sortable values when formatted display values would sort incorrectly;
- keep keyboard/focus behavior and dynamic announcement with the actual web/accessibility owner;
- do not combine sorting with structures whose merged headers make the relationship ambiguous unless the implementation is explicitly solved.

A sortable-looking header that does not expose state or sorts formatted strings incorrectly is a functional defect.

## Cold-read and accessibility attacks

Test the actual target:
- can a new reader identify what the table compares?
- can they recover units and primary metric without a distant note?
- can they find the highest-risk row/value without scanning irrelevant columns?
- do missing/unknown values remain distinguishable from zero?
- do screen-reader/header relations remain coherent for web tables?
- does sort state remain announced and visible when sorting is material?
- does narrow/print transformation preserve the original comparison task?

USWDS guidance is useful for semantic table/header/sort/accessibility behavior, but component success in isolation is not project accessibility proof.

## Cross-owner routing

- chart vs table analytical form → core `oleander-data-viz`;
- browser semantics, focus, sortable-state announcement and responsive behavior → `oleander-web-ui` + `ACCESSIBLE_INTERACTION_EXTENSION.md`;
- publication/board table hierarchy → `oleander-story-and-board` / `oleander-visual-design` as presentation owners;
- spreadsheet-native production → spreadsheet tooling while preserving this information-design contract.

## Rejected external defaults

Do **not** promote as universal OLEANDER rules:
- fixed seconds-to-answer thresholds;
- fixed maximum columns/rows;
- fixed zebra-striping thresholds;
- fixed decimal-place recipes by metric type;
- mandatory K/M/B abbreviation;
- totals always at the bottom regardless of task/medium;
- fixed slide table size limits;
- right alignment as an exceptionless rule across every script/content type.

## Required output

Return the reader question/action, source/precision ledger, row/column ownership, ordering/grouping logic, summary-row semantics, redesigned table, medium variants where required, cold-read/accessibility findings, change log and unresolved data/semantic/implementation holds.

## Candidate boundary

This extension is independently reformulated from MIT-licensed `SkillMedev/skills` Data Table Design and cross-checked against current USWDS table/accessibility guidance. External fixed thresholds and formatting recipes are retained only as bounded diagnostics when a project source justifies them. Cross-context project evidence is still required before promotion.