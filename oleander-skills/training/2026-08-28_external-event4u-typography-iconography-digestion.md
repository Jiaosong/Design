# External Skill Digestion — event4u Typography + Iconography

Status: `EXTERNAL STUDY / CANDIDATE EXTENSION EVIDENCE / NOT ACTIVE`
Date: 2026-08-28
Source: `event4u-app/agent-config`
License observed: MIT at repository level.

## Scope read

Reviewed the current public `typography-system` and `iconography` Skill contracts and compared them against existing `oleander-visual-design` / `oleander-web-ui` boundaries.

## Typography — accepted delta

- define communication roles before exact family/size values;
- separate font availability from actual delivery/loading route;
- treat typography as a repeatable system with source-of-truth discipline;
- verify that the chosen family actually loads and that fallback does not silently alter identity/layout;
- stress real long strings and responsive conditions;
- keep font delivery/privacy/licensing as a real production question.

## Typography — rejected as OLEANDER defaults

- curated pairing CSV as decision authority;
- fixed modular ratios, weights, line-heights or role sizes;
- brand-archetype → font-class formulas;
- DTCG/token tooling as mandatory when a project has no such Current system;
- project-specific scripts, CLI routes and package assumptions.

## Iconography — accepted delta

- semantic intent before glyph shape;
- incumbent icon-family inspection before adding a new set;
- preserve grid/stroke/fill/radius/optical-mass/metaphor relationships;
- distinguish visible glyph size from actionable hit target;
- verify that a referenced glyph actually exists and renders;
- declare substitutions instead of silently inventing a near match.

## Iconography — rejected as OLEANDER defaults

- Iconify as universal registry/runtime;
- Lucide/Heroicons/Phosphor/Tabler as default brand language;
- CDN/web-font embedding as a universal delivery route;
- external library naming conventions as OLEANDER semantic authority.

## OLEANDER output

- `oleander-visual-design/TYPOGRAPHY_SYSTEM_EXTENSION.md`
- `oleander-visual-design/ICONOGRAPHY_SYSTEM_EXTENSION.md`

## Boundary

External implementation detail is not installed runtime evidence. Documentation/CI cannot promote either extension to ACTIVE. Real project artifacts, font/icon source authority, rights, actual rendering and Independent Design Review remain required.