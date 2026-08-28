# OLEANDER Semantic UI Token + Theme Extension

Status: `CANDIDATE EXTENSION / WEB-UI + VISUAL-DESIGN`

Use when a high-fidelity interface must express color, typography, spacing, shape, elevation or state through a reusable design-token system and support more than one appearance/theme without scattering raw values or per-component forks.

This extension governs token-role architecture and theme verification. It does not define project colors, spacing scales, component libraries or an OLEANDER house style.

## Core principle

`CURRENT DESIGN AUTHORITY → PRIMITIVE FACTS → SEMANTIC ROLES → OPTIONAL COMPONENT OVERRIDES → THEME MAPPINGS → RENDERED STATE MATRIX → REPAIR`.

Components should depend on stable semantic roles when a reusable token system exists. Raw values and primitive scales remain implementation facts; semantic roles explain why a value is used.

## Authority gate

Before creating or modifying tokens, resolve:

- Current brand/UI design authority;
- existing token/theme files and their ownership;
- active component consumers;
- light/dark/high-contrast or other supported appearances;
- whether values are source-approved, implementation-derived, reconstructed, provisional or deprecated;
- rights/source state for fonts/icons/assets represented by tokens.

Do not create a second token taxonomy merely because the existing names are imperfect. Extend or migrate the Current system deliberately when a real semantic gap exists.

## Token-layer contract

Prefer three separable layers when the product complexity justifies them:

1. **Primitive / reference values** — raw palette values, spacing units, radii, type values or other factual scales.
2. **Semantic roles** — surface, foreground, action, border, focus, success, warning, danger, muted, emphasis and other project-specific roles.
3. **Component overrides** — only where a component genuinely needs a stable specialization that cannot be expressed by the shared semantic layer.

Do not require all three layers for a small system. The point is role separation, not taxonomy size.

A component that repeatedly hardcodes a primitive because no semantic role exists exposes a token-system gap. Fix the gap at the appropriate shared layer unless the value is intentionally local.

## Naming and ownership

Token names should encode durable purpose rather than temporary appearance or file location.

Reject names that:

- become false when a color/value changes;
- bind a shared semantic role to one incidental component instance;
- duplicate an existing Current role under a synonym;
- hide state/variant meaning in undocumented numeric suffixes.

Project-specific naming remains authoritative. Do not import an external naming formula as a mandatory schema.

## Theme mapping contract

A theme is a mapping of semantic roles to appearance values, not an automatic inversion or a parallel component implementation.

For each supported theme/appearance:

- preserve the same semantic role meaning unless an explicit product decision changes it;
- map role values deliberately rather than filtering/inverting the rendered UI;
- verify images, logos, diagrams and data graphics independently instead of assuming a page-level inversion preserves truth;
- check elevation/boundary/state cues in the actual appearance;
- preserve user/system preference semantics when the project supports them;
- document components that require true theme-specific behavior rather than a simple token remap.

`SAME ROLE ≠ SAME RAW VALUE` and `DARK APPEARANCE ≠ INVERTED LIGHT APPEARANCE`.

## State × theme matrix

For material reusable components, verify the state set that actually exists in the product across each supported theme as applicable:

`DEFAULT / HOVER / PRESSED / SELECTED / FOCUS / DISABLED / ERROR / SUCCESS / LOADING / OTHER CURRENT STATE`

Do not invent states solely to fill a matrix. Do not claim theme coverage because the default state renders correctly.

Check:

- readable foreground/surface relation;
- critical boundary/focus visibility;
- state distinctions not carried by hue alone when accessibility/semantics require another cue;
- icon/image/data meaning preserved;
- no raw-value leakage causing one component to ignore the theme;
- visual hierarchy remains intentional after remapping.

Specific contrast thresholds come from the current applicable accessibility standard/project authority, not from an external Skill snapshot.

## Theme/readback evidence

Use actual rendered outputs for high-risk components and page states. Automated token linting or variable coverage may prove wiring, not perceptual quality.

Required distinction:

- token resolution/wiring = implementation evidence;
- standards-based contrast/state checks = accessibility evidence;
- rendered hierarchy/brand quality = Design Quality evidence.

`TOKEN PASS ≠ ACCESSIBILITY PASS ≠ DESIGN KEEP`.

## Migration / drift check

When introducing or changing a semantic role:

1. identify current consumers;
2. detect direct primitive/raw-value bypasses;
3. migrate intentionally or mark justified local exceptions;
4. compare before/after rendered states;
5. verify no unrelated component silently changed meaning;
6. record deprecated token aliases and removal conditions where necessary.

## Rejected external defaults

OLEANDER does not import:

- a mandatory 8px spacing grid;
- any fixed dark-background, opacity, elevation or accent recipe;
- external raw token names;
- external component library values;
- universal theme color choices;
- fixed contrast numbers copied from a Skill instead of the current governing standard.

## Required output

Return:

- Current token/theme authority;
- semantic-role map and any new role justification;
- raw/primitive bypass findings;
- theme mappings;
- material state × theme readback;
- standards/accessibility checks routed to the proper authority;
- migration/drift evidence;
- unresolved brand/accessibility/design-quality HOLDs.

## Candidate boundary

This extension makes high-fidelity token/theming work explicit and testable without making one external design system normative.

External study provenance: `axross/skills` `high-fidelity-ui-design`. The reviewed repository exposed no repository-level license file, so OLEANDER retains independently synthesized high-level token/theme mechanics only; external prose, fixed values, naming formulas and recipes are not copied.