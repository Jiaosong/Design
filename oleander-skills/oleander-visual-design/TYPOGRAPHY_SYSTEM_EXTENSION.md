# OLEANDER Typography System Extension

Status: `CANDIDATE EXTENSION / VISUAL-DESIGN`

Use when typography is not merely a local styling choice but a repeatable cross-screen, cross-page or cross-media system that must remain readable, editable, responsive and technically deliverable.

## Core principle

`TYPE ROLE → TYPE RELATION → SCALE / RHYTHM → DELIVERY → ACTUAL READBACK`.

Do not begin by choosing a fashionable font or arbitrary size ladder. Resolve the communication role first, then choose and verify a type relation that can survive real content, languages, media and delivery constraints.

## Type-role contract

Before assigning exact families or sizes, name the roles actually required by the artifact, such as:

- display / campaign headline;
- section heading;
- body / long reading;
- caption / source note;
- label / control;
- data / numeric emphasis;
- code / technical notation;
- bilingual counterpart or CJK-specific role when needed.

Not every artifact needs every role. Adding roles without a communication need creates visual noise and maintenance burden.

Each role should record:

`ROLE → CONTENT TYPE → PRIORITY → FAMILY / FALLBACK → WEIGHT RANGE → SIZE / LINE-HEIGHT RANGE → TRACKING BEHAVIOR → MAX / MIN CONTENT STRESS → DELIVERY ROUTE`.

## Family selection

Choose families against the actual identity, language coverage, reading duty and technical environment. Evaluate:

- character and identity fit;
- CJK / Latin / numeral / punctuation coverage as required;
- long-copy readability versus display distinctiveness;
- available weights and styles;
- real licensing / project authorization;
- actual file/package availability;
- variable-font axes when materially useful;
- fallback behavior if the preferred family fails.

Do not treat a font-pairing list, archetype label, mood keyword or trend reference as decision authority. Those are candidate inputs only.

`FONT EXISTS ≠ FONT CAN BE DELIVERED`.

Availability, licensing and delivery are separate questions.

## Scale and rhythm

Build a relational scale rather than a collection of isolated numbers. Record:

- base reading size;
- display/heading/body ratios;
- line-height by role;
- paragraph spacing;
- measure / line length where continuous reading matters;
- tracking adjustments by role and script;
- optical-size or variable-font behavior when used;
- breakpoint or container conditions that change the relation.

A modular ratio may be tested as a starting hypothesis, but no universal ratio is OLEANDER truth. The real criterion is whether hierarchy, rhythm and fit remain convincing in actual target content.

## Content-stress gate

Typography must be tested with the hardest real strings, not only short placeholder copy.

Stress at minimum as applicable:

- longest approved headline;
- longest navigation/control label;
- shortest and longest bilingual pair;
- numerals, dates, units and technical symbols;
- source citations / footnotes;
- narrow mobile/container width;
- high-density and low-density states;
- localization expansion where relevant.

If a system only works with ideal short copy, it is not a robust system.

## Responsive type behavior

Responsive typography is not viewport-proportional enlargement.

Prefer bounded relations that preserve hierarchy and reading comfort. Recompose line breaks, width, measure and role scale as containers change. A headline may require a different wrap or size tier on narrow screens rather than continuous `vw` growth/shrinkage.

Check that visual order, semantic heading order and reading order remain aligned.

## Token / source-of-truth boundary

When a project has a design-token system, typography belongs in the Current token/source system rather than scattered one-off CSS values. When no token system exists, keep one explicit Current type specification and avoid inventing a parallel token framework solely for this extension.

The token schema must not replace visual judgment. A perfectly consistent token file can still encode a weak typographic system.

## Delivery and font-loading gate

For digital work, resolve the actual delivery route:

- project-owned/self-hosted font files when appropriate;
- framework/package route when authorized and verified;
- CDN only when explicitly permitted and suitable;
- preload/subsetting strategy when performance materially depends on it;
- fallback stack and metric shift risk;
- font-family naming identity between source files, CSS and installed packages.

Do not silently introduce third-party font requests, privacy exposure or an unverified external dependency merely because a web-font link is convenient.

For print, packaging or PDF delivery, hand off font embedding/outline/subset/rights requirements to `oleander-delivery-qc` and the print-production preflight route as appropriate.

## Actual readback

Review typography in rendered pixels and at intended reading distance. Check:

- first-read hierarchy without reading every word;
- body comfort and line length;
- line breaks and rag;
- widows/orphans where relevant;
- CJK punctuation and mixed-script rhythm;
- baseline and alignment relationships;
- clipping and overflow;
- font loading/fallback failure;
- display typography at thumbnail/far read;
- body/caption/source notes at near read;
- longest-string stress on desktop and narrow/mobile targets.

## Failure modes

Reject or revise when:

- the system defaults to a familiar AI/web font with no project reason;
- type family is chosen by mood keyword alone;
- multiple unrelated families compete without role logic;
- sizes are individually invented rather than relational;
- typography hierarchy depends only on font size;
- body contrast is weakened merely to look “premium”;
- display size works only on desktop;
- the preferred font is named but not actually loaded;
- a fallback silently changes line breaks or identity;
- source/font licensing or delivery is unresolved but the artifact is called final;
- token consistency is used as Design PASS.

## Boundary

This extension does not create a universal font-pairing catalog, fixed modular ratio, fixed line-length law or brand-archetype typography formula. Project Current Authority, actual language/content, target medium, rights and rendered Design Quality remain decisive.

External study provenance: `event4u-app/agent-config` typography-system and `TheGoat395/Codex-Skills` editorial-typography-systems. Their implementation-specific token scripts, font tables, fixed ratios and preset style mappings are not OLEANDER defaults.