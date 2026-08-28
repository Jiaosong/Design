# External Skill Digestion — Skill Graph IA + Layout + Accessibility

Status: `EXTERNAL STUDY / CANDIDATE EXTENSION EVIDENCE / NOT ACTIVE`
Date: 2026-08-28
Source: `jacob-balslev/skill-graph`
License observed: repository root `LICENSE` is Apache License 2.0. Some exported Skill frontmatter states MIT; repository-level license is treated as the safer transfer boundary.

## Scope read

Reviewed the public `information-architecture`, `layout-composition`, and `a11y` Skill contracts against current OLEANDER web/UI integration and specialist-owner boundaries.

## Information architecture — accepted delta

- start from real user tasks and entry points before navigation structure;
- deliberately choose structural role: nav/page/tab/section/filter/cross-link;
- one canonical home plus cross-links instead of duplicated competing homes;
- stable user-facing labels across nav/title/search/context;
- wayfinding includes location, siblings/choices, next action and recovery;
- validate structure against task prompts and unfamiliar-entry conditions.

## Layout composition — accepted delta

- hierarchy first, spatial structure second;
- scan pattern selected by content relation rather than visual fashion;
- breakpoints where content/relationship actually fails, not device names;
- explicit reflow decisions for stack/collapse/pin/move/disclose/crop;
- state footprints for loading/empty/error/partial conditions;
- responsive visual order must remain compatible with semantic/focus order.

## Accessibility — accepted delta

- semantic/native primitive choice is upstream architecture, not final audit polish;
- keyboard behavior, focus entry/exit/return and programmatic name/state are one interaction contract;
- ARIA without the corresponding behavior is not a fix;
- meaningful dynamic states need semantic equivalence for assistive technology;
- reduced-motion/high-contrast/text-reflow modes require actual interaction verification;
- automated scanners are risk detectors, not full accessibility proof.

## Rejected as universal defaults

- fixed navigation-depth, device-breakpoint, reading-width or timing thresholds;
- any exported Skill license metadata that conflicts with the repository root license;
- repository CLI/audit framework as an OLEANDER dependency;
- checklist success as proof of user performance or accessibility completion.

## OLEANDER output

- `oleander-web-ui/INFORMATION_ARCHITECTURE_WAYFINDING_EXTENSION.md`
- `oleander-web-ui/RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION.md`
- `oleander-web-ui/ACCESSIBLE_INTERACTION_EXTENSION.md`

## Boundary

These extensions support, not replace, existing specialist ownership such as route/wayfinding and interaction. Current standards, actual project routes, runtime/browser behavior and expert/assistive-technology testing remain authoritative where required.