# OLEANDER Accessible Interaction Extension

Status: `CANDIDATE EXTENSION / WEB-UI + VALIDATION`

Use when an interactive browser surface must remain operable and understandable through semantic structure, keyboard input, focus, assistive technology and user preference modes.

## Core principle

`SEMANTIC PRIMITIVE → OPERABLE INPUT → FOCUS MODEL → PROGRAMMATIC NAME / STATE → DYNAMIC ANNOUNCEMENT → USER PREFERENCE → REAL INTERACTION TEST`.

Accessibility is part of interaction architecture, not a post-render annotation layer.

## Native-primitive-first gate

Prefer the native element whose semantics already match the user action. Examples include button for same-page action, anchor for navigation, label for form control, fieldset/legend for grouped inputs, table for tabular data and details/summary for simple disclosure.

Custom roles are justified only when the native primitive cannot express the interaction and the complete keyboard/state contract is implemented and tested.

`ARIA ROLE ≠ BEHAVIOR`.

Adding a role without the expected keyboard, state and focus behavior is not an accessibility repair.

## Operability contract

For every material interactive element or composite widget, resolve as applicable:

- reachable by keyboard;
- expected activation keys;
- arrow-key/roving behavior when the pattern requires it;
- escape/cancel behavior;
- disabled/unavailable behavior;
- visible focus;
- focus entry, containment and exit;
- focus return after dismissal/navigation;
- rapid repeat/interruption behavior;
- pointer/touch target separate from visible icon geometry.

Do not make keyboard users traverse hidden, inert or duplicate controls.

## Name / role / state relation

Check that assistive technology receives a coherent relation among:

`VISIBLE LABEL ↔ PROGRAMMATIC NAME ↔ ROLE ↔ CURRENT STATE ↔ DESCRIPTION / ERROR RELATION`.

A visible label that disagrees with the accessible name is a defect. Placeholder-only labels, unlabeled icon buttons and status shown by color alone are not sufficient.

## Dynamic-state announcement

Loading, validation errors, save success, async completion, filtering results and other meaningful state changes may need programmatic announcement.

The goal is semantic equivalence, not a noisy live region for every visual change. Announce information that a sighted user receives and needs to continue the task.

Do not use motion, toast position or color as the only communication channel for critical state.

## Focus continuity

Treat focus as part of spatial/state continuity.

When opening, closing, navigating, reordering or replacing content, verify:

- where focus moves;
- whether that movement matches the visible state change;
- whether the user can recover to the triggering context;
- whether offscreen/removed elements retain impossible focus;
- whether route transitions preserve expected heading/landmark entry.

Focus movement that is technically valid but semantically surprising is still a usability defect.

## User preferences

Respect platform/browser preferences where applicable, including reduced motion, increased contrast/forced colors and text enlargement/zoom.

Reduced Motion must preserve task meaning and remove artificial temporal locks, not merely hide transforms while keeping the wait.

High-contrast/forced-color modes must preserve essential boundaries and state recognition rather than relying on author colors that disappear.

## Visual-order / semantic-order gate

Responsive reflow, CSS order, portals and overlays can create a mismatch between visual reading order, DOM/semantic order and keyboard focus order.

Check them together after layout changes. Do not “fix” focus order with positive `tabindex` to compensate for a structurally incorrect DOM.

## Verification

Use real interaction evidence when the runtime is available:

- keyboard-only task path;
- focus visibility and return;
- semantic tree / accessible-name inspection where available;
- screen-reader or platform accessibility inspection for high-risk patterns when available;
- reduced-motion preference;
- high-contrast/forced-colors where relevant;
- text zoom/enlargement and reflow;
- dynamic error/success/loading state.

Automated accessibility scanners are useful defect detectors, not complete accessibility proof.

## Failure modes

Reject or revise when:

- clickable `div/span` replaces a suitable native element without full behavior;
- ARIA is added to make invalid interaction appear compliant;
- pointer works but keyboard cannot complete the task;
- a modal/menu/dialog closes but focus is lost;
- visible label and accessible name diverge materially;
- validation or async success exists only visually;
- reduced motion still preserves artificial delay or task lock;
- responsive CSS reorders visual content away from semantic/focus order;
- automated zero-violation output is reported as full accessibility PASS;
- accessibility is deferred until after visual/interaction architecture is locked.

## Boundary

This extension is not a substitute for current WCAG, platform HIG, legal/regulatory requirements or expert assistive-technology testing when those are required. Specific numerical thresholds must come from the current applicable standard/project authority, not stale copied heuristics.

External study provenance: `jacob-balslev/skill-graph` a11y (repository license Apache-2.0; independently reformulated).