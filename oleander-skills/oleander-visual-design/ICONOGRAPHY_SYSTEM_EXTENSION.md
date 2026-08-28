# OLEANDER Iconography System Extension

Status: `CANDIDATE EXTENSION / VISUAL-DESIGN`

Use when icons, pictograms, symbols or UI glyphs form a repeated communication system rather than a one-off illustration.

## Core principle

`SEMANTIC INTENT → EXISTING SYSTEM → GLYPH / METAPHOR → GEOMETRIC LANGUAGE → STATE / SIZE → DELIVERY → RENDERED VERIFICATION`.

An icon is not decoration. It is a compressed semantic signal that must remain recognizable, consistent and technically real at the size where it is used.

## Existing-system-first gate

Before introducing a new icon, inspect the Current project for:

- existing icon family/library;
- brand pictogram language;
- stroke versus filled convention;
- grid and bounding-box convention;
- nominal stroke weight;
- corner/radius character;
- optical size behavior;
- baseline and text alignment;
- semantic metaphors already established;
- selected/active/disabled/error variants;
- licensed brand marks versus generic UI glyphs.

Do not introduce a second visual language merely because another library contains a more convenient glyph.

## Semantic contract

For each material icon, record when needed:

`INTENT → USER ACTION / OBJECT / STATE → VISIBLE LABEL RELATION → GLYPH SOURCE → STYLE VARIANT → SIZE → ACCESSIBILITY ROLE → FALLBACK / SUBSTITUTION`.

Choose by semantic intent first, not by visual resemblance alone. If no exact glyph exists, record the substitution and why it remains understandable.

## Geometry and family consistency

A coherent set should preserve a recognisable relationship among:

- viewBox/grid;
- stroke/fill mode;
- stroke weight and cap/join behavior;
- corner radius and terminal shape;
- optical mass;
- positive/negative-space ratio;
- level of detail at small sizes;
- directional conventions;
- badge/state additions.

When a genuinely custom pictogram is required, derive it from the Current family's geometry instead of drawing an unrelated SVG.

## Icon + text relationship

Determine whether the icon is:

- standalone actionable control;
- redundant reinforcement beside a visible label;
- navigation marker;
- status/state indicator;
- diagram/pictogram evidence;
- decorative and therefore hidden from assistive technology.

Do not remove text merely because an icon exists. For unfamiliar, high-risk or irreversible actions, text or an accessible label is usually still required.

## Size and optical readback

Do not assume one SVG scales perfectly everywhere. Test relevant sizes for:

- silhouette recognition;
- stroke survival;
- interior aperture closure;
- optical centering;
- alignment with text/cap height;
- touch/click target versus visible glyph size;
- high-contrast/dark/light states;
- export/rasterization where applicable.

The hit target and the glyph box are different objects.

## Source and delivery

Prefer authoritative existing assets and verified library glyphs. Record:

- library/family and version when relevant;
- exact glyph identity;
- source/master versus rendered derivative;
- license/brand-mark boundary;
- delivery form such as inline SVG, symbol sprite, framework component or project asset;
- known bundle/runtime implications when material.

A plausible name or code reference is not evidence that the asset exists. Verify the actual glyph and render.

## Failure modes

Reject or revise when:

- emoji substitutes for a required professional UI/pictogram system;
- multiple unrelated icon families are mixed without a deliberate role boundary;
- a custom SVG ignores the incumbent grid/stroke/radius language;
- a missing exact glyph is silently approximated;
- visual icon size is confused with accessible touch target;
- a brand logo is treated as an interchangeable generic icon;
- icon color alone carries a critical state;
- icon existence in code is treated as rendered proof;
- decorative icon tiles are repeated as filler rather than adding meaning.

## Boundary

This extension does not mandate Lucide, Heroicons, Phosphor, Tabler, Iconify or any other library. Library choice follows Current project/brand authority, license, platform and delivery needs.

External study provenance: `event4u-app/agent-config` iconography. Its Iconify-specific resolution and embedding path is implementation-specific evidence, not a universal OLEANDER dependency.