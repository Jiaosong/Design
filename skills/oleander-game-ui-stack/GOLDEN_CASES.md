# OLEANDER Game UI Stack — Golden Cases

Status: `CANDIDATE TEST SET`

These cases validate whether the five-skill stack improves design judgment without replacing project authority or encouraging self-evaluation.

## GC-01 — Mobile exploration route with real source authority
Input:
- official/source route map with nodes and route variants;
- mobile portrait target;
- game-like exploration intent;
- optional interpretation layer separate from guide authority.

Expected findings:
- extract topology before styling;
- preserve source order/direction without inventing GPS precision;
- avoid shrinking full desktop map into one phone viewport;
- separate GUIDE nodes from optional reading/content nodes;
- keep Return recoverable;
- reject dashboard-like route mode cards if route itself should be first read;
- invoke mobile target-size/safe-area checks.

Regression failure:
- skill recommends merging optional content IDs into source-route nodes without authority;
- skill calls a relational path GPS-accurate;
- skill deletes route information to make the screen cleaner.

## GC-02 — Landscape-first scene with optional reveal
Input:
- strong landscape/scene image;
- optional scientific/cultural relation reveal;
- digital-off/no-phone path.

Expected findings:
- landscape is primary visual;
- reveal is progressive disclosure;
- explanatory layer is quieter than scene;
- Digital OFF removes optional overlay immediately;
- no infinite decorative glow/scan unless it communicates state;
- Return remains available.

Regression failure:
- skill turns relation reveal into a technical dashboard;
- skill treats hidden UI as equivalent to no-phone product validity;
- skill self-awards Design PASS from runtime success.

## GC-03 — Compression / high-attention scene
Input:
- scene claims spatial/body compression;
- visual source is conceptual rather than field-verified.

Expected findings:
- visual claim must be carried by crop/space/depth, not only text;
- conceptual imagery remains labeled as conceptual;
- game HUD withdraws in high-attention state;
- Return/safety outranks optional interaction.

Regression failure:
- fake black masks are accepted as proof of real spatial geometry;
- UI effects imply verified site conditions.

## GC-04 — Memory / journal screen
Input:
- journal/memory object after route experience;
- game feeling requested without reward economy.

Expected findings:
- memory ritual may use page/imprint/trace/collection behavior;
- avoid XP, streak, 13/13, completion ledger unless authorized;
- object should feel authored, not like a generic card list;
- keyboard/touch activation states are specified.

Regression failure:
- skill invents achievements or mandatory completion;
- skill reduces the journal to a dashboard list because it is easier to implement.

## GC-05 — Generic dashboard anti-case
Input:
- screen with large title, four equal cards, tiny world image, persistent glow, bottom summary card, secondary detail card.

Expected findings:
- `oleander-game-ui` flags dashboard-first composition;
- `oleander-ui-visual-composition` identifies failed primary visual/hierarchy;
- recommends object/world-first restructuring before polish;
- does not solve by adding more glow, gradients, borders, or cards.

## GC-06 — Mobile runtime attack
Input:
- route node focus transition;
- Return button;
- Reduced Motion;
- keyboard and touch support.

Expected tests:
- rapid A→B target switch;
- Return during enter/focus;
- repeated activation;
- keyboard traversal and visible focus;
- touch target sizing;
- Reduced Motion with no decorative waits/locks;
- zero invisible focusable controls;
- console/page error smoke test.

Regression failure:
- Return is visually present but blocked by animation lock;
- Reduced Motion hides animation but preserves JS delay locks;
- pointer works while keyboard/touch equivalent fails.

## GC-07 — Existing Mature Design comparison
Input:
- mature existing screen and newer revised screen.

Expected findings:
- matched-scale comparison;
- identify gains and regressions separately;
- do not reward novelty/version number;
- preserve mature design when new pixels regress;
- `Pixel Fail ≠ Design Delete`.

Regression failure:
- newer version wins automatically;
- implementation cleanliness or CI is used as visual-quality evidence.

## Pass condition
A candidate skill stack passes Golden Cases only when:
- all expected findings appear where relevant;
- no regression failure appears;
- producer does not issue final self-verdict;
- independent reviewer confirms that the stack adds materially better findings than the prior generic review path.