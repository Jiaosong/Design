# External Skill Digestion — UX Writing / Content Design — 2026-08-29

Status: `CANDIDATE EXTENSION EVIDENCE / NO_PROMOTION`

## Sources read

1. `content-designer/ux-writing-skill`
   - root license: MIT.
   - read: `SKILL.md`, repository tree confirming `references/accessibility-guidelines.md`, `references/content-usability-checklist.md`, `references/patterns-detailed.md`, `references/voice-chart-template.md`, error/empty/onboarding templates and examples.
2. `hueyexe/frontend-agent-skills/ux-writing-content-design`
   - root license: MIT.
   - read: full Skill body including task/state/conversation-flow, consequence-revealing actions, error recovery, sensitive asks, localization/accessibility and implementation guidance.
3. Cross-check: GOV.UK Design System error-message guidance — error copy must identify what happened and how to fix it, preserve entered values and remain associated with the relevant field/state.

## Current comparison

Current `oleander-web-ui` already owns state/browser integration, accessibility routing, IA and responsive behavior, but had no focused Candidate extension for words as interaction/state material. Therefore the material delta is narrow and belongs under the existing web/UI owner; no new Core Skill is justified.

## Accepted material delta

- `task/state → content role → action consequence → system response → recovery/inverse` rather than isolated string polishing;
- distinguish label/helper/error/banner/dialog/empty/loading/success/notification roles;
- error handling as interaction recovery, not tone exercise;
- voice as persistent authority vs tone as state/stakes adaptation;
- sensitive asks and destructive actions require consequence/trust truth;
- localization, programmatic label/error association and dynamic state announcements must survive real implementation;
- copy must not invent backend availability, reversibility, cause or compliance truth.

## Rejected / bounded-only

Not promoted as universal rules:
- 40–60 character limits;
- fixed reading-grade targets;
- 85% active-voice target;
- fixed CTA word counts;
- mandatory sentence templates;
- generic “warm/helpful” voice as OLEANDER identity;
- conversion/comprehension uplift claims without project evidence.

## Output

Created `oleander-web-ui/CONTENT_DESIGN_MICROCOPY_EXTENSION.md`.
Golden regression target: `SK-WEB-009`.

## Maturity

`EXTERNAL STUDY → CANDIDATE EXTENSION / SUPPORT / SCOPED / NO_PROJECT_USAGE / NO_PROMOTION`.

Real UI application, actual browser/state readback and independent review remain required.