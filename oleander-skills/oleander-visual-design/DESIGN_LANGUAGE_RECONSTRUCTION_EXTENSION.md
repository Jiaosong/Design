# OLEANDER Design Language Reconstruction Extension

Status: `CANDIDATE EXTENSION / VISUAL-DESIGN + WEB-UI`

Use when an existing repository, website or multi-surface product must be read back into a persistent design-language record without mistaking accidental implementation repetition for intentional design authority.

This extension governs evidence extraction and reconstruction. It does not impose an external `DESIGN.md` schema, CLI, token format or documentation tool.

## Core principle

`PRODUCT SCOPE → CURRENT SOURCE / RENDER EVIDENCE → OBSERVATION LEDGER → RECURRENCE + OWNERSHIP + CONFIDENCE → INTENT CLASSIFICATION → NORMATIVE / OBSERVED / LOCAL / LEGACY → PERSISTENT DESIGN-LANGUAGE RECORD → REAPPLICATION CHECK`.

Repeated code or repeated pixels are evidence of implementation, not automatic proof of design intent.

## Mode selection

### Repository mode

Use when the actual product repository or authoritative source package is available.

Prefer evidence in this order:

1. explicit Current design/brand guidance;
2. named tokens/themes/variables and their active consumers;
3. shared primitives/components and documented variants;
4. representative routes/surfaces that actually import/use them;
5. local/surface-specific implementations.

Exclude proposals, examples, superseded code, unused packages and similarly named assets unless the Current product actually consumes them.

### Rendered-product mode

Use when only a public/live rendered product is available.

Inspect representative templates/states at the real target sizes. When runtime tooling permits, use DOM/computed styles/loaded public CSS or equivalent inspectable output to verify exact values. Screenshots are strong visual evidence for relationships but weak authority for exact hidden token names or internal ownership.

A reconstructed record from rendered evidence must remain explicitly `RECONSTRUCTED / OBSERVED` until source authority confirms intent.

## Observation ledger

For each candidate design rule/value, record:

- product/surface/page/state;
- viewport/carrier;
- visual/interaction role;
- observed value or relation;
- source location or rendered evidence;
- recurrence across materially different consumers;
- shared owner/component/token if visible;
- confidence;
- authority classification;
- implementation consequence if promoted into the persistent record.

Use a compact chain:

`ROLE → VALUE / RELATION → SOURCE → SCOPE → RECURRENCE → OWNERSHIP → CONFIDENCE → STATUS`.

## Intent classification

Classify each candidate before it becomes reusable guidance:

- `NORMATIVE CURRENT` — explicitly governed by Current design/brand/token/component authority;
- `SHARED IMPLEMENTATION EVIDENCE` — repeated through a real shared owner but not explicitly documented as design intent;
- `OBSERVED RECONSTRUCTION` — repeatedly visible/measurable in rendered output but internal authority is unknown;
- `LOCAL` — surface-specific choice with no evidence of broader intent;
- `LEGACY / SUPERSEDED` — no longer part of Current product;
- `CONFLICT / HOLD` — sources disagree or evidence is insufficient.

Do not silently promote `SHARED IMPLEMENTATION EVIDENCE` or `OBSERVED RECONSTRUCTION` to `NORMATIVE CURRENT`.

## Promotion gate for reusable rules

A candidate may enter the persistent design-language record when at least one strong authority path exists, such as:

- explicit Current guidance;
- a named shared token/component/variant with active cross-surface use;
- repeated rendered relation across materially different templates plus no conflicting Current source, clearly labeled reconstructed/observed;
- explicit user/project decision promoting the rule.

A repeated literal, utility class, one-off CSS declaration or frequently copied local pattern is not enough by itself.

## Exact-value gate

Exact values require stronger evidence than visual impressions.

For repository mode, use the Current source/token/theme/component authority.

For rendered-product mode, exact values should come from inspectable computed/public declarations or another measurable runtime source when available. If exact measurement is unavailable, record the relation qualitatively or leave the value open rather than guessing from pixels.

Do not invent internal token names from observed raw values.

## Rule vs inventory boundary

A persistent design-language record should capture governing relations, not dump every implementation detail.

Prefer:

- role and hierarchy;
- type roles and script behavior;
- color/surface semantics;
- spacing/alignment rhythm;
- shape/radius/elevation logic where intentional;
- image/crop behavior;
- component/state grammar;
- responsive recomposition rules;
- allowed/forbidden/context rules when authoritative.

Avoid:

- exhaustive component inventories with no design consequence;
- every discovered token/value;
- generated CSS syntax;
- audit methodology inside the design record;
- vague personality adjectives unsupported by Current sources;
- accidental code repetition presented as principle.

## Conflict handling

When implementation conflicts with explicit Current guidance:

1. preserve the Current guidance as authority;
2. record the implementation mismatch separately;
3. identify affected surfaces/owners;
4. route repair to the actual owner;
5. do not rewrite the design-language record to normalize the defect.

When two Current sources conflict, HOLD the rule and resolve authority before persistence.

## Reapplication check

After reconstructing a material rule, test whether it predicts or constrains at least one real surface not used as the sole discovery example.

Ask:

- Does the rule explain another Current surface?
- Does applying it reduce inconsistency without flattening meaningful task differences?
- Does it preserve the product's existing strong design rather than replacing it with a generic system?
- Does a counterexample reveal that the rule was only local?

`DOCUMENTED PATTERN ≠ VALIDATED DESIGN SYSTEM`.

## Cross-owner routing

- rendered/browser evidence → `oleander-web-ui` real browser readback;
- typography/iconography/brand rules → corresponding `oleander-visual-design` extensions;
- token/theme structure → `oleander-web-ui/SEMANTIC_UI_TOKEN_THEME_EXTENSION.md`;
- independent brief/render review → `RENDERED_BRIEF_REVIEW_EXTENSION.md`;
- source/rights uncertainty → `oleander-research`.

## Required output

Return or persist:

- audited product/surface scope;
- evidence mode;
- observation ledger;
- normative/observed/local/legacy classifications;
- exact-value authority state;
- reconstructed/persistent design-language record;
- conflicts/omissions kept outside the record;
- reapplication/counterexample check;
- unresolved authority HOLDs.

## Candidate boundary

This extension creates a controlled reconstruction of design language; it cannot infer private intent from pixels, promote accidental implementation patterns, or make a reconstructed website record equal to an authoritative design system.

External study provenance: `ibelick/ui-skills` `create-design-md` (MIT). OLEANDER retains the evidence/recurrence/intent-separation mechanisms while rejecting the external file schema, validation CLI, export targets and naming constraints as OLEANDER defaults.