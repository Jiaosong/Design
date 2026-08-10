# R03｜Dry-run Integrity Report

Status: `PASS / WORKFLOW INTEGRITY ONLY`

Verified 2026-08-10 in headless Chromium / Playwright.

## Executed sequence

`N0a → N0b → PK → B1 → C1 → C2-0 → C2-1 → C2-2 → C2-3`

Observed:

- all 9 stages reached in order;
- no Back/Edit control appeared after stage lock;
- 9 stage records persisted;
- every stage record contained `started_at / locked_at / duration_ms`;
- randomized C2 object order was recorded;
- N0a/N0b early responses remained unchanged after later prompts;
- page-level JavaScript errors: `0`.

## Schema correction made during dry run

Participant raw data and researcher coding are now explicitly separated:

- participant raw export = raw response + stage exposure + timestamps/duration + object order;
- blind coder export = eight SRE status/depth fields + four PLS subtype fields;
- reconciliation is a third layer and cannot overwrite the raw participant or first-pass coder files.

## Boundary

This dry run does **not** establish:

- participant comprehension;
- two-coder reliability;
- historical truth;
- image-rights clearance;
- 2026 site conditions;
- design or learning effectiveness.

Decision: `R03 DRY-RUN PASS / SMALL ADULT PHOTO PILOT READY / HUMAN PILOT NOT RUN`.