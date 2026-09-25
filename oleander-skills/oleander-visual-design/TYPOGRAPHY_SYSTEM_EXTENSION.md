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

## Open-source candidate font registry

OLEANDER keeps a **candidate registry**, not a house-style font list. The registry exists to widen the search space, reduce repeated font hunting, and make common open-source families easy to test. It does **not** preselect a style, pair, or winner.

Selection behavior:

`PROJECT CONTENT / LANGUAGE / MEDIUM / READING DUTY → REGISTRY RETRIEVAL → 3–5 MATERIAL CANDIDATES → REAL-CONTENT SPECIMENS → RENDER / EMBED / FALLBACK CHECK → HUMAN SELECTION / MODIFICATION → PROJECT CURRENT`.

The system should autonomously shortlist and render candidates when the designer does not know the final style in advance. The designer should judge actual results rather than having to prescribe every typographic parameter before exploration.

### Registry tiers

**Core production candidates** — broad, stable families suited to repeated document/UI/editorial work when their exact release and license are verified for the project:

- CJK sans: Noto Sans CJK, Source Han Sans;
- CJK serif: Noto Serif CJK, Source Han Serif;
- Latin/system sans: Inter, IBM Plex Sans, Source Sans 3, Public Sans;
- Latin/editorial serif: Source Serif 4, Literata;
- code/data mono: JetBrains Mono, Source Code Pro, IBM Plex Mono;
- CJK technical mono: Sarasa Gothic / Sarasa Mono variants, Maple Mono CN.

**Expanded candidates** — retrieve when the design direction benefits from a different voice, proportion, reading texture, or regional script behavior:

- CJK / Chinese: LXGW WenKai, LXGW ZhenKai, LXGW Marker Gothic, Smiley Sans, Zhuque Fangsong;
- Latin sans: Roboto, Manrope, DM Sans, Work Sans, Space Grotesk, Barlow, Archivo, Montserrat, Lexend, Atkinson Hyperlegible;
- Latin serif/editorial: Lora, Merriweather, Newsreader, EB Garamond, Crimson Pro, Libre Baskerville, Fraunces;
- mono / technical: Fira Code, Cascadia Code;
- Japanese / Korean / regional: M PLUS, BIZ UDPGothic, BIZ UDPMincho, Zen Kaku Gothic New, Zen Old Mincho, Pretendard, plus the appropriate Noto CJK regional family.

### Role-oriented retrieval, not style-word mapping

The registry may be queried by practical role such as:

- long Chinese reading;
- bilingual Chinese/Latin editorial;
- compact UI;
- public-service / accessibility-sensitive copy;
- technical table / dimensions / code;
- expressive display headline;
- Japanese or Korean regional typography.

Do **not** map vague descriptors such as “premium”, “Eastern”, “technology”, “warm”, or “minimal” directly to a family. Those words may seed exploration only. The actual shortlist must be tested against content, script coverage, rendering, medium, and the emerging visual system.

### Candidate diversity and human steering

When typography materially affects the design direction, do not show several near-identical families as fake alternatives. Prefer a small set with materially different typographic behavior, then let the designer:

- keep one candidate;
- reject one or more;
- combine display/body roles from different candidates;
- ask for a neighboring direction;
- reopen the search if all candidates feel wrong.

OLEANDER may filter obvious duplicates or technically invalid candidates before presentation, but it should preserve at least one exploratory/wildcard option when doing so does not violate project constraints.

### Exact-source and runtime boundary

The registry stores discovery candidates only. Before a family becomes project Current, verify the exact release in use:

`TYPEFACE → EXACT FILE / VERSION → CHARACTER SET → LICENSE / ALLOWED USE → EMBEDDING / WEB DELIVERY → TARGET APP / BROWSER / OS → FALLBACK → RENDER READBACK`.

A family name in this registry is never sufficient evidence for licensing, glyph coverage, variable axes, Office/PDF embedding, web performance, or current upstream release status. Recheck those facts against the authoritative upstream source at the time of use.

Preview/beta families (for example a release explicitly marked pre-release or non-production-ready upstream) must remain exploratory until the project has verified that exact build.

### System integration

The machine-readable candidate list is stored next to this extension as `FONT_CANDIDATE_LIBRARY.json`. Reuse and refine that registry rather than creating a new font-selection Skill for each project.

`NEW PROJECT ≠ NEW FONT SKILL`.

Update the existing registry when a repeatable candidate, source fact, or practical role is learned. Create a separate specialist extension only when a genuinely distinct reusable capability exists and cannot be represented by this typography owner without distortion.
