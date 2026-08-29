# Cross-context Practice — Data-table Information Design — Laboratory Comparison

Status: `CROSS_CONTEXT_EVIDENCE / CONTROLLED PRACTICE / SYNTHETIC DATA / NO_PROJECT_USAGE / NO_PROMOTION`

## Why this context is materially different

Batch-4 `SK-DV-004` attacks an executive/report table pasted from a raw export. This practice uses a fictional laboratory comparison where exact lookup, measurement uncertainty, mixed units, non-detects and method differences matter more than ranking.

## Second-source cross-check

W3C WAI table tutorials were used as a bounded accessibility cross-check. They emphasize programmatic header/data relationships, captions/summaries for orientation, preserving structural relationships in responsive forms, and using actual table semantics rather than visual layout tables.

Sources:
- `https://www.w3.org/WAI/tutorials/tables/`
- `https://www.w3.org/WAI/tutorials/tables/tips/`
- `https://www.w3.org/WAI/ARIA/apg/patterns/table/examples/sortable-table/`

Rights boundary: no W3C sample table/code is copied. The practice uses independently generated synthetic data and only transfers semantic requirements.

## Reader question / action

Primary question: **Which material samples have comparable measurements, and where does method/uncertainty make direct comparison unsafe?**

Decision supported: choose samples for a follow-up material test, not declare a production winner.

Therefore ranking is secondary; method comparability and evidence precision are primary.

## Synthetic raw input

| sample | mass_g | absorption_pct | absorption_sd | method | surface_temp_C | note |
|---|---:|---:|---:|---|---:|---|
| A | 42.3471 | 18.2 | 0.8 | M1 | 23.1 | measured |
| B | 41.9018 | 18.9 | 0.9 | M1 | 23.0 | measured |
| C | 43.2 | 19.0 |  | M2 | 22.9 | sd not reported |
| D | 42.0100 | 0 | 0.7 | M1 | 23.2 | instrument result = non-detect, not zero |
| E | 42.5522 | 18.35 | 0.82 | M1 | 23.1 | two-decimal source export |

Synthetic data only.

## Source / precision ledger

| Field | Evidence precision | Display rule | Missing / special state |
|---|---|---|---|
| mass | scenario authority supports 0.1 g only | display 1 decimal | none |
| absorption | source values vary; comparison only needs 0.1% | display 1 decimal | D = `ND`, not `0.0` |
| uncertainty | present only when reported | same precision as absorption | C = `not reported` |
| method | categorical authority | exact ID | M1 and M2 not silently pooled |
| temperature | 0.1 °C | display 0.1 °C | context/support only |

`DISPLAY PRECISION ≤ EVIDENCE PRECISION` is applied even though the raw export contains more decimals.

## Redesigned table

**Caption:** Synthetic absorption comparison — method and uncertainty retained

| Sample | Method | Mass (g) | Absorption (%) | SD (%) | Surface temp (°C) | Comparison state |
|---|---|---:|---:|---:|---:|---|
| A | M1 | 42.3 | 18.2 | 0.8 | 23.1 | comparable within M1 |
| B | M1 | 41.9 | 18.9 | 0.9 | 23.0 | comparable within M1 |
| E | M1 | 42.6 | 18.4 | 0.8 | 23.1 | comparable within M1 |
| D | M1 | 42.0 | ND | 0.7 | 23.2 | non-detect; do not treat as zero |
| C | M2 | 43.2 | 19.0 | not reported | 22.9 | method differs; direct rank HOLD |

No grand total or average is shown because mixing method M2, ND and missing uncertainty would imply a false common statistical basis.

## Header / structure contract

For an HTML implementation:
- use a real data table;
- provide one programmatic caption/accessible name;
- column headers own their data columns;
- `Method` and `Comparison state` remain explicit rather than buried in footnotes;
- if grouped headers are introduced later, preserve programmatic associations rather than relying on visual proximity;
- if sortable, sorting controls are operable elements and current sort state is visible/programmatic;
- `ND`, `not reported` and numeric zero remain distinct strings/states.

## Sort attack

Permitted candidate sorts:
- Sample ID;
- Method;
- Mass;
- Temperature.

Absorption sort is **conditionally misleading** because `ND`, M1/M2 and missing SD complicate ranking. If enabled, it must preserve those states and cannot present the sorted order as a performance leaderboard.

## Responsive attack

Do not collapse each row into unrelated stacked cards if the task is cross-sample comparison. Preferred bounded options:
- horizontal scroll with the Sample/Method context remaining recoverable;
- split into two simpler tables only if the reader question is also split (e.g. M1 comparison vs M2 hold);
- a mobile detail view may support single-sample lookup, but it is not a substitute for the comparison view.

## Readback verdict

**KEEP as cross-context evidence:** reader-question-first structure, precision discipline, missingness semantics and aggregate restraint transfer to scientific/laboratory data.

**Material delta:** table design must explicitly preserve **method comparability / measurement-state semantics**, not only units and denominators, when they govern whether values can be compared.

**REJECT:** sorting every numeric-looking column, converting ND to zero, or averaging all rows for visual completeness.

**HOLD:** no real laboratory authority, statistical review, live HTML, screen-reader or assistive-technology test. This is controlled information-design evidence only.