# 2026-08-18 Web / Responsive Composition — Responsive Recomposition

Status: **CANDIDATE / project-main validation pending**

## Problem
A desktop layout can pass structural responsive QA yet fail visually on mobile if its modules simply stack vertically and the resulting order delays the highest-priority task or gives support content too much weight.

## Trigger
Use when desktop and mobile contain the same information but the mobile first-read, task order, visual mass, or optional-content density no longer match the project's decision priority.

## Inputs
- current project authority and task priority;
- desktop composition and content roles;
- target mobile viewport(s);
- existing `oleander-story-and-board` hierarchy rules;
- `oleander-delivery-qc` responsive/browser checks.

## Visible Symptoms
- desktop modules merely fall downward on mobile;
- primary task appears late in the scroll;
- hero collapses to the same visual weight as support cards;
- optional reading becomes a co-primary block;
- technically valid mobile layout still reads like a shrunken desktop page.

## Cause
Responsive treatment is being used as geometry adaptation only. The breakpoint changes dimensions but does not reassign information roles.

## Technique
`TASK PRIORITY → BREAKPOINT ROLE → ORDER → SPAN → EMPHASIS → DENSITY → RECOVERY`

Preserve content and authority. At the breakpoint, allow order, span, hierarchy and density to change when the user task requires it.

## Parameters / Conditions
- no information deletion to manufacture simplicity;
- `SERVICE / RETURN > ROUTE > OBSERVATION > EXPLANATION > MEMORY > SHARE` remains authoritative for C04 task priority;
- Landscape First remains a primary visual principle where applicable;
- optional content remains recoverable;
- use real browser readback at desktop and mobile before any visual PASS.

## Aesthetic Judgment
A good mobile composition should look intentionally composed at that viewport. It should not advertise the history of the desktop grid through awkward stacking, late priority actions or equal-weight modules.

## Verification
A/B HTML practice executed with system Chromium through Playwright using `/usr/bin/chromium`.

- desktop: 1440 px viewport;
- mobile: 390 × 844 viewport;
- first browser readback: **REVISE** because label/title roles ran together on mobile;
- repair: labels and titles separated typographically;
- second desktop/mobile readback: **POST-READBACK PASS for practice artifact only**.

## Failure Condition
A mobile page may be technically responsive, have no overlap, no overflow and valid touch targets, yet still require REVISE when the desktop module order survives unchanged and causes the wrong first-read/task sequence.

## Counterexample
A simple article page whose reading order is already linear and task priority does not change across viewport widths may correctly stack without re-composition. Responsive reordering is not mandatory when it would add complexity without improving comprehension or task flow.

## Transfer Boundary
This practice does not replace C04 source pixels, route geometry, final typography authority, field evidence, accessibility testing, user testing or release QA. It tests responsive visual hierarchy only.

## Applicable Domains
Web, mobile web, interactive exhibits, responsive dashboards, portfolio pages, web reports.

## Application Mapping
Primary: C04 Digital / Web / Return-first. Secondary: cross-project OLEANDER responsive presentation systems.

## Evidence Gate
**PASS** for IBM Carbon responsive-grid evidence, current C04 responsive-validation boundary, and project priority mapping.

## Design Quality Gate
**POST-READBACK PASS for this calibration artifact only.** C04 production Web/PDF/MAIN remains separately governed.

## Version / Status
- Version: `v0.1`
- Status: `CANDIDATE`

## Artifact
- `OLEANDER_C04_RESPONSIVE_RECOMPOSITION_AB_v1.html`

## Capability Receipt
- required native output: editable HTML/CSS;
- browser runtime: `RUNNER_AVAILABLE` via `/usr/bin/chromium`;
- Playwright package: available; bundled browser absent, therefore system Chromium was explicitly selected;
- readback: executed at 1440 and 390 × 844;
- `STATIC EXPORT` label is not used because browser execution was actually completed.
