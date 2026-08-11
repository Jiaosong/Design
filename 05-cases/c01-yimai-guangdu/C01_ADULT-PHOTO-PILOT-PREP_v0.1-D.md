# C01｜Adult Photo Pilot Prep v0.1-D

## Status

`PILOT PREP TECHNICAL PASS / HUMAN TEST NOT RUN / SITE RG2 NOT RUN / E2 UNCHANGED`

This record prepares a small adult photo pilot. It contains **no participant results** and must not be cited as user validation.

## Pilot scope

- First cohort: adults only (18+).
- F02's existing first-round guidance is approximately 3–5 participants per group; v0.1-D uses 3–5 adults only as a process/coding calibration candidate, not a statistical sample.
- Every participant runs the C1/C2 core sequence.
- Each participant receives only one N04–N08 extension module. This is a **v0.1-D design judgment** to reduce fatigue and cross-module prompt contamination, not an established project fact or validated experimental optimum.
- No unnecessary real names, phone numbers, ID numbers, or other identity data are required.

## Three-part research chain

### 1. Participant RAW Runner

- stage submission locks earlier responses;
- records explicit answer state, raw wording, start/lock time, duration, object order and extension assignment;
- supports explicit absence, uncertainty and rejection;
- P1/P2/P3 images are bound locally and never serialized into JSON;
- early N0 stages do not expose later source claims.

### 2. Researcher Coding Shell

- loads RAW JSON read-only;
- requires anonymous coder ID;
- requires an explicit codebook version;
- SRE D1–D8 status structure follows the existing R03 protocol;
- only `SPONTANEOUS` allows depth 1–3;
- PLS-L / PLS-S / PLS-R / PLS-C retain the existing 0–2 protocol;
- this tool intentionally does not redefine the meaning of those dimensions.

### 3. Dual-Coding Reconciliation

- refuses comparison when `session_id` differs;
- refuses comparison when `codebook_version` differs;
- reports exact agreement and Cohen's kappa as technical metrics;
- returns `NON_ESTIMABLE` for single-category kappa cases;
- produces a disagreement list instead of silently reconciling coder differences.

The current R03 technical agreement gates remain the authority:

- PASS: kappa >= 0.75 **and** exact agreement >= 85%;
- REVISE: kappa 0.60–0.749 **or** exact agreement 75–84.9%;
- lower values: do not use the coding for design decisions;
- single-category kappa: `NON_ESTIMABLE`.

The reconciliation tool reports these metrics but does not itself promote evidence.

## Extension-module contract

### N04｜八股厅

Scenario branch only: indoor candidate / unavailable or closed / unknown. The learning mechanism must survive without assuming building occupation.

### N05｜毛氏宗祠

Tests who controls publication, range, anonymity, revision and withdrawal before memory becomes exhibition content.

### N06｜八角井

Separates past source narrative, current conditions requiring field observation, `UNKNOWN`, and matters a visitor should not decide.

### N07｜古巷

Tests public passage / short stop / permission / do-not-enter-do-not-shoot / insufficient-information decisions before revealing the boundary rule.

### N08｜手狮

Tests knowledge, teaching and commercialization permissions without assigning design-team authority over inheritor decisions.

## Technical preflight performed

The generated v0.1-D files were checked at 320×568, 390×844 and 1365×768:

- no horizontal overflow;
- no JavaScript errors in the tested flows;
- 18+ setup gate blocks ineligible/uncertain status;
- N0 has no source-information leakage;
- a silent blank cannot progress without an explicit response state;
- Coding Shell blocks load when codebook version is missing;
- reconciliation blocks different sessions;
- identical single-category coding returns exact agreement 1.000 and kappa `NON_ESTIMABLE`.

**Decision:** `PILOT PREP TECHNICAL PASS` only.

## Drive artifacts

Folder: `09_Adult-Photo-Pilot-Prep_v0.1-D` — `1J2fwxDfE0VhbVvaofy8Ov0XOsv2FvjiN`

- ZIP — `1COSRiQNSW076-knu73UOylYbQO6xkkAX`
- Adult Pilot Runner — `1VH4apfLD4v4qZn-9sA_o9vUg_cQXLP2j`
- Researcher Coding Shell — `1rBXCNvkNs1YPHJLRVfBKf-GNswJUhtxO`
- Dual-Coding Reconciliation — `1jvTpNhYUXSGdULhmt21WK8TsagZ977eY`
- Pilot Protocol — `1UAc0tmY7ky9bCR-heAL5H2SJZ1l_mlX4`
- Preflight Checklist — `1krRkz6EN1LRetkrq3OPUIOJbCIGo7fH8`
- Validation JSON — `1G6Y8lv-WQVg04d7SuB3KG8cIjx7Fz5Ux`

## Promotion boundary

The next status change requires **real adult participant RAW records**. The sequence is:

`adult pilot → independent dual coding → disagreement review → Keep / Revise / Reject`

Even after a real pilot is run, `HUMAN TEST RUN` does not automatically mean `VALIDATED`, and it does not automatically promote C01 to E3. Tourist RG2 remains a separate site-evidence gate.