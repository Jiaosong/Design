# 2026-08-28｜External Skill Digestion｜High-Fidelity UI Design

Status: `DIGESTED / LICENSE UNCLEAR / HIGH-LEVEL MECHANISM ONLY / EXISTING OWNER EXTENDED`

## Source

- Repository: `axross/skills`
- Skill: `skills/high-fidelity-ui-design/SKILL.md`
- Reference read: `skills/high-fidelity-ui-design/references/tokens-and-theming.md`
- Repository license check: no root `LICENSE` file and no license-path hit found in the reviewed state.

Because repository-level reuse rights were not established, OLEANDER retains only independently synthesized high-level mechanisms and does not copy source prose, recipes, token names, fixed values or reference examples.

## Current comparison

OLEANDER already has:

- `oleander-web-ui` end-to-end browser integration;
- `ACCESSIBLE_INTERACTION_EXTENSION.md` for semantic primitives, focus, keyboard, state announcements and preferences;
- `RESPONSIVE_LAYOUT_COMPOSITION_EXTENSION.md`;
- `oleander-visual-design` typography/iconography/brand-rule extensions;
- real browser readback and independent Design Quality separation.

Therefore generic “high-fidelity UI” is already covered. The material delta is specifically semantic token/theme architecture.

## Material delta accepted

Implemented as:

`oleander-web-ui/SEMANTIC_UI_TOKEN_THEME_EXTENSION.md`.

Accepted mechanisms:

1. Separate primitive/reference values from semantic roles and bounded component overrides.
2. Treat raw-value bypasses in reusable components as a token-system gap or explicit local exception.
3. Define themes as semantic-role remappings rather than page/component forks or visual inversion.
4. Verify material component states across every supported appearance instead of proving only the default state.
5. Keep token wiring, accessibility/standards validation and visual Design Quality as separate evidence classes.
6. Perform migration/drift review when semantic roles change.

## Rejected / not transferred

- mandatory 8px grid;
- external token naming formula;
- fixed dark-background, white-opacity, elevation-overlay or accent recipes;
- any external palette/component-library values;
- contrast thresholds copied from the Skill snapshot instead of the current governing standard;
- assumption that dark mode must exist in every product;
- assumption that token consistency implies visual quality.

## OLEANDER correction

Project source/design authority owns token names and values. The extension only adds a role/verification architecture. `TOKEN PASS ≠ ACCESSIBILITY PASS ≠ DESIGN KEEP`.

## Maturity boundary

`CANDIDATE EXTENSION / NOT ACTIVE`. Requires a real multi-theme/product application and rendered state readback for stronger maturity.