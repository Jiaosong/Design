# 2026-09-18｜External Design Option-Space Skills Digestion

Status: `DIGESTED / EXISTING-OWNER MAPPED / ONE CANDIDATE EXTENSION / NO NEW CORE SKILL / NO NEW PROJECT STATE / NO PROMOTION`

## Purpose

This study follows the already-merged external visual-execution digestion but asks a different question:

> Which external design Skills materially improve **design-option generation, option-space coverage, trade-off visibility, computational exploration, concept comparison or product/space方案形成** beyond what OLEANDER already owns?

The target is not to collect more style Skills. The target is to find missing executable design mechanisms and absorb only those that belong inside the existing OLEANDER Design Operating System.

## OLEANDER authority retained

Current owner remains:

`oleander-design-process`

Existing upstream/downstream owners remain unchanged:
- Research/source authority → `oleander-research`;
- native/parametric CAD identity → `oleander-3d-pipeline`;
- visual comparative presentation → `oleander-visual-design`;
- image treatment → `oleander-image-art-direction`;
- browser/digital runtime → relevant web/UI owner;
- specialist engineering/code/safety → specialist VALIDATION owner;
- release/package integrity → `oleander-delivery-qc`.

No external repository justifies a new OLEANDER project lifecycle, taxonomy, router, design-thinking framework, UI design framework, industrial-design framework or “generative design” core Skill.

## Source pins and rights boundary

Studied repository states:

1. `Abhinavbwj/Claude-skills-for-Computational-Designers@7a090c9ddc92e441b1419910673edbcfa7a962ed`
   - root license: MIT;
   - deep paths: `skills/design-automation/SKILL.md`, `skills/generative-design/SKILL.md`, `skills/cd-foundations/SKILL.md`.
2. `jacob-balslev/skill-graph@ee6f58e2f4adb9a9ac8fb43556e4c5f633a8361c`
   - root license: Apache-2.0;
   - reviewed design Skill frontmatter declares CC-BY-4.0;
   - deep paths: `marketplace/skills/ideation/SKILL.md`, `design-thinking/SKILL.md`, `journey-mapping/SKILL.md`, `prototyping/SKILL.md`.
3. `HahyeonJeon/gobbi@e5cef5f295d39ebdf4a2989b8636602d7fa68a03`
   - root license: MIT;
   - deep paths: `plugins/gobbi/skills/web/web-design/SKILL.md`, `checklists.md`.
4. `What0ff/snowe-ui-skill@92eeb724fcfa889cafe8cb47c219b7e80a8e2635`
   - license: MIT;
   - deep paths: `skill/snowe-ui-skill/references/exploration-protocol.md`, `quality-gates.md`, associated decision/visual-review scripts.
5. `AlpacaLabsLLC/skills-for-architects@e7e364497b2a47c088db2e47de6660344fcaf92d`
   - root license: MIT;
   - deep paths: `skills/workplace-programmer/SKILL.md`, `skills/zoning-envelope/SKILL.md`, `skills/studio/SKILL.md`.
6. `beiming183-cloud/AutoCAD-MCP@11f7c47e5038796a20451b38b23032e625b5aa26`
   - root license: MIT;
   - deep paths: `skills/industrial-product-design/SKILL.md`, `skills/industrial-product-design-gbt/SKILL.md`.
7. `caorachel-lab/frontend-posters@bc63c00f84b4d26576ac98ece7ec8fc5be27b063`
   - no readable root license found during this review;
   - research reference only;
   - deep paths: `SKILL.md`, `scripts/poster-qa.mjs`.
8. `Embretr/emmi@9c1ec0f55878d2eb7cd4c515995bd0e0c367a6ab`
   - no readable root license found during this review;
   - research reference only;
   - deep path: `design-shotgun/SKILL.md`.

No third-party source code or prose is copied into the OLEANDER runtime. The implemented extension is independently synthesized around OLEANDER's existing authority, option, evidence and review semantics.

---

# 1｜Material gap found

OLEANDER already had strong manual design exploration:

- Decision Question;
- Variable Budget;
- materially different options;
- source/evidence/assumption separation;
- editable/native artifact expectation;
- actual readback;
- independent Design Review;
- technical Validation Handoff;
- Current / Promotion separation.

The external study found one material executable gap:

> OLEANDER did not yet express a sufficiently granular contract for **large bounded design spaces** where variables, adjacency, allocations, constraints, performance signals or topology are explicit enough for computational generation / sampling / constraint solving / multi-objective search.

Without this contract, a project could plausibly:
- generate hundreds of options but only one concept family;
- convert hard requirements into penalties;
- invent variable ranges for solver convenience;
- call a weighted-score winner “best design”;
- call a Pareto set “approved options”;
- hide invalid candidate repairs;
- optimize dozens of low-leverage sliders;
- let an objective proxy be gamed;
- treat runtime crashes as design infeasibility;
- keep stale rankings after changing the evaluator;
- compare parameter rows instead of actual design artifacts.

This is a real gap, not merely different terminology.

Accepted implementation owner:

`oleander-design-process/COMPUTATIONAL_OPTION_SPACE_EXTENSION.md`.

---

# 2｜Abhinavbwj / Computational Designers

## Useful mechanism

### A. Constraint-first design automation

The design-automation material distinguishes:
- hard constraints;
- soft constraints;
- graph relations;
- adjacency;
- non-adjacency;
- area/capacity;
- geometry decoding;
- repair;
- ranking over a feasible set.

This gives a more executable bridge from:

`PROGRAM / RELATION → OPTION`

than ordinary prose ideation.

### B. Spatial relationship representations

Useful representations include:
- adjacency matrix;
- graph;
- bubble/spring diagram;
- planar/topological arrangement;
- relative-position constraints;
- allocation grid.

OLEANDER transfer:

These are **relationship prototypes**, not professional plans. Their value is making relational structure explicit before detailed geometry.

### C. Multi-objective design space

The generative-design material clearly distinguishes:
- large search space;
- objective definition;
- hard feasibility;
- Pareto trade-offs;
- diversity;
- convergence;
- sensitivity;
- surrogate evaluation;
- candidate clustering / representative selection.

The most important transfer is not the evolutionary algorithm itself. It is:

`OPTION SPACE ≠ ONE OPTIMUM`

and:

`PARETO SET = OBSERVED TRADE-OFF EVIDENCE, NOT DESIGN APPROVAL`.

### D. Fitness-function failure

Useful failure knowledge:

> a solver can efficiently produce technically high-scoring but designically irrelevant candidates when the objective function poorly represents intent.

OLEANDER transfer:

Every objective requires:
- represented design relation;
- method;
- validity range;
- proxy limitation;
- known-good/bad preflight;
- actual artifact readback;
- orthogonal check for critical finalists.

## Rejected from Core

Not imported as universal OLEANDER rules:
- any fixed room-size/program number;
- any fixed algorithm/population/generation count;
- named solver/tool as default;
- Galapagos / Wallacei / Octopus / Opossum / Forma as required workflow;
- solver ranking as a design decision;
- fixed structural/environmental threshold detached from Current authority.

---

# 3｜Skill Graph / Ideation + Prototyping

## Useful mechanism

### A. Divergence and judgment should not collapse into one step

The ideation material makes a strong process distinction:

`DIVERGE → THEN CONVERGE`

rather than judging every idea as it appears.

OLEANDER transfer is narrower:

- during option-space expansion, hard infeasibility may still be rejected immediately;
- soft/taste ranking should not kill unfamiliar candidates before the field exists;
- discriminating criteria should be stated before final results where practical;
- selection criteria must not be retrofitted only to justify a preferred option.

### B. Materially different selected candidates

Useful check:

> if selected winners are variants of the same underlying idea, the divergent field did not spread.

OLEANDER strengthens this into **concept-family deduplication**:
- topology;
- allocation model;
- circulation model;
- interface model;
- structural/support logic;
- behavior niche;
- product architecture.

Thousands of parameter points in one family do not equal broad design exploration.

### C. Prototype as a learning vehicle

The prototyping material reinforces an existing OLEANDER rule:

`PROTOTYPE QUALITY = ABILITY TO ANSWER THE CURRENT QUESTION`

not visual polish.

No new Prototype Skill is created because OLEANDER already owns Prototype Fidelity and Physical Prototype / V&V extensions.

## Rejected from Core

Not transferred as global rules:
- fixed “20 ideas” requirement;
- fixed Crazy-8 counts/timing;
- dot voting;
- NUF as universal decision method;
- impact/effort matrix as universal convergence method;
- any popularity-vote route to Design KEEP.

---

# 4｜Gobbi / Web Design

## Useful mechanism

Gobbi provides a crisp failure criterion:

> different color, typography, spacing, icon style or wording does not by itself make a materially different concept.

This is strongly consistent with OLEANDER's existing option rules.

Useful transfer as regression language:
- compare consequential changes in hierarchy;
- action model;
- information flow;
- interaction strategy;
- state communication.

No new UI mechanism is created because this is already conceptually owned by `oleander-design-process` + `oleander-web-ui`.

## Why it is not a new extension

OLEANDER already has:
- materially different alternatives;
- Best Existing First;
- same-object repair vs reopening;
- browser readback;
- independent Design Review;
- interface architecture and state semantics.

The external material therefore acts as **cross-check / anti-regression evidence**, not a new architecture.

---

# 5｜Snowe UI

## Useful mechanism

Snowe's strongest transferable ideas are:
- calibrate depth to consequence/uncertainty/reversibility;
- identify live trade-offs;
- generate candidates from causes, not style labels;
- use matched proof slices;
- preserve strongest rejected alternative;
- reopen when evidence invalidates the decision;
- stop at evidence saturation rather than endless exploration.

These mostly already exist in OLEANDER under:
- Decision Question;
- Variable Budget;
- causal design reasoning;
- Prototype Fidelity;
- option comparison;
- actual readback;
- reopen trigger;
- Current/supersession.

### Material reinforcement

The option-space extension adopts the stronger idea:

> representative candidates must be compared as **matched artifacts** when the design consequence is spatial, visual, physical or interactive.

Parameter tables and charts are not enough for Design Review.

## Rejected from Core

- Snowe-specific depth taxonomy as a new OLEANDER project state;
- Snowe datasets;
- Snowe UI design language;
- fixed UI-specific candidate structure.

---

# 6｜Architecture Studio / workplace programming + zoning envelope

## Useful mechanism

### A. Conserved resource reasoning

The workplace programmer explicitly names an important real-design relation:

> adding area to one constrained category means taking it from somewhere else.

The external Skill embeds fixed office ratios that are not suitable for OLEANDER, but the underlying mechanism is cross-domain:

`TOTAL CAPACITY → DONOR → RECEIVER → RECOMPUTED TOTAL → CONSTRAINT CHECK`.

OLEANDER generalizes this to:
- area;
- mass;
- cost;
- power;
- energy;
- schedule/time;
- storage;
- attention;
- information density;
- operations/staffing.

This becomes the **Conserved-resource budget gate**.

### B. Persistent program state

`program.json` demonstrates that design allocations should be stateful and recomputed rather than repeatedly restated in prose.

OLEANDER already has structured Current/project-state patterns, so no parallel `program.json` architecture is imported.

### C. Zoning envelope

The zoning-envelope Skill is useful as a reminder that regulatory/site envelopes are **constraints / evidence artifacts**, not design方案 themselves.

OLEANDER transfer:

`ENVELOPE VALIDITY ≠ MASSING DESIGN QUALITY`.

## Explicit rejection

Never import:
- “circulation always 27%”;
- fixed workplace percentages;
- generic room sizes/capacity ratios;
- US-specific legal requirements into unrelated jurisdictions;
- an envelope viewer as regulatory approval;
- simplified lot polygons as surveyed geometry.

All such values require Current source, jurisdiction and project applicability.

---

# 7｜AutoCAD-MCP industrial-product-design

## Finding: high detail but low net-new delta

This external Skill is unusually granular and aligns closely with OLEANDER:
- brief/source authority;
- product architecture;
- at least several materially different concepts;
- same-scale multi-view review;
- native CAD authority;
- document/revision identity;
- configuration/motion;
- render truth;
- product form;
- service;
- DFM;
- human factors;
- validation separation;
- NOT_EVALUATED;
- handoff.

OLEANDER already owns these through:
- `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md`;
- `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md`;
- `PHYSICAL_PROTOTYPE_TEST_VV_EXECUTION_EXTENSION.md`;
- `DFM_DFA_PROCESS_CAPABILITY_EXTENSION.md`;
- `HUMAN_FACTORS_VALIDATION_EXTENSION.md`;
- `oleander-3d-pipeline` geometry and CAD authority.

Therefore **no second Industrial Product Skill is created**.

## Minor reinforcement only

Useful anti-regression questions retained:
- concept options must vary architecture/silhouette/use relation, not fillet/color;
- same-scale multi-view evidence is stronger than one hero camera;
- document/revision/configuration identity matters through mutable CAD work;
- a geometry-valid / attractive render does not self-certify product design.

These are not new Core rules; they confirm current OLEANDER direction.

---

# 8｜Frontend Posters

## Useful mechanism

This Skill demonstrates:
- actual previews rather than text-only style descriptions;
- real copy/assets across alternatives;
- fixed-canvas editable HTML;
- render QA;
- thumbnail-scale readback.

These are useful for poster/editorial execution but were already covered by the prior visual-execution digestion and OLEANDER visual/native-output rules.

## No new Design Process delta

Not transferred:
- default three directions;
- restrained / expressive / wildcard trio;
- 1080×1440 default;
- poster-specific QA markers as universal artifact schema;
- its style presets.

The general rule already exists:

`REAL COMPARABLE ARTIFACTS > TEXT-ONLY OPTION DESCRIPTIONS`.

---

# 9｜Design Shotgun

## Useful mechanism

The workflow makes real side-by-side HTML alternatives and keeps superseded iterations, which reinforces:
- actual artifact comparison;
- no-loss iteration history;
- comparison before implementation.

## Rejected / not generalized

Do not import:
- taste memory across unrelated projects;
- automatic bias toward prior approved fonts/colors/layouts;
- mandatory difference by font + palette + layout;
- fixed N variants;
- browser board as universal chooser.

Why:

Visual difference is not necessarily **conceptual difference**, and prior taste should not silently steer a new project unless that preference is valid authority for the new context.

---

# 10｜Resulting OLEANDER extension

Implemented candidate:

`oleander-skills/oleander-design-process/COMPUTATIONAL_OPTION_SPACE_EXTENSION.md`

The extension introduces no new lifecycle stage. It deepens Design Process option formation only when justified.

Key executable contracts:

1. **Option-space contract**
   - baseline identity;
   - variables/domains;
   - authority;
   - hard/soft constraints;
   - conserved budgets;
   - unknowns;
   - generation/evaluation method;
   - diversity;
   - stop condition.

2. **Variable authority**
   - every domain/range/options set has source/rationale;
   - OPEN vs LOCKED is explicit;
   - redundant sliders do not inflate diversity.

3. **Hard / soft / objective separation**
   - requirements do not become penalties for convenience;
   - preferences remain tradeable;
   - objective metrics state proxy limitations.

4. **Conserved-resource reconciliation**
   - donor / receiver / delta / recomputed total.

5. **Generation-mode routing**
   - enumeration;
   - CSP/CP/integer;
   - DOE/sampling;
   - evolutionary/multi-objective;
   - novelty/quality-diversity;
   - surrogate-assisted.

6. **Spatial relationship route**
   - typed graph edges;
   - adjacency matrix/bubble/topological pre-geometry;
   - geometry decoder;
   - repair log;
   - path-check claim ceiling.

7. **Model preflight**
   - baseline;
   - known feasible;
   - known infeasible;
   - objective perturbation;
   - decoder identity;
   - invalid-candidate rate;
   - tool/evaluator binding.

8. **Divergence integrity**
   - soft judgment separated from field expansion;
   - criteria not retrofitted;
   - concept-family deduplication;
   - coverage evidence.

9. **Failure telemetry**
   - generated;
   - valid;
   - hard-infeasible;
   - runtime/evaluator failure;
   - repaired;
   - duplicate;
   - unverified.

10. **Sensitivity**
    - test leverage before optimizing every exposed variable.

11. **Pareto semantics**
    - trade-off set, not winner;
    - representative regions/families;
    - no weighted-score shortcut to Design KEEP.

12. **Diversity / convergence**
    - objective improvement cannot hide family collapse.

13. **Objective gaming attack**
    - known false positives / false negatives;
    - orthogonal evaluation;
    - claim ceiling.

14. **Matched artifact comparison**
    - same source/program;
    - same scale/state/camera where relevant;
    - actual editable artifacts.

15. **Design Review separation**
    - solver filtering ≠ Design Review;
    - `KEEP / REVISE / REJECT / HOLD` remains human/design authority.

16. **Run identity + stale-result propagation**
    - source/evaluator/variable changes reopen old results.

---

# 11｜Golden regression coverage

Added to `evals/golden/skills.jsonl`:

- `SK-DES-013` — spatial adjacency / CSP / invalid geometry / concept-family collapse;
- `SK-DES-014` — multi-objective / Pareto / post-hoc weights / matched artifact review;
- `SK-DES-015` — high-dimensional parameter set / sensitivity / conserved-resource donor-receiver;
- `SK-DES-016` — objective gaming / runtime failure vs design failure / repair logging / stale re-evaluation.

These cases are intentionally different. One broad “generative design” case would not catch the distinct failure mechanisms.

---

# 12｜What remains unchanged

No change to:
- 11 Core Skill identities;
- lifecycle roles;
- Master Protocol;
- Project State taxonomy;
- Source Authority hierarchy;
- Promotion authority;
- Design KEEP authority;
- field/engineering approval;
- Notion/GitHub system architecture;
- existing product/HF/DFM extensions;
- web/UI specialist ownership;
- visual-execution Current from PR #647.

No existing Skill is superseded.

---

# 13｜Maturity boundary

Current maturity target for this batch:

`EXTERNAL OPTION-SPACE MECHANISMS DIGESTED → EXISTING OWNER MAPPED → CANDIDATE EXTENSION IMPLEMENTED → GOLDEN REGRESSION ADDED → CI/READBACK REQUIRED → REAL PROJECT REAPPLICATION REQUIRED`.

This batch cannot claim:
- cross-project maturity;
- a superior optimizer;
- professional architecture/engineering approval;
- that computational options are better than manually designed options;
- Design KEEP from machine metrics;
- Promotion.

Required future evidence:

At least one real design project should use the extension on a materially open option space and preserve:
- one invalid or failed candidate path;
- one actual evaluator/proxy weakness or explicit attack result;
- representative editable artifacts;
- Design Review independent of numerical ranking;
- evidence that the extension improved exploration quality without creating unnecessary process overhead.

`MORE OPTIONS ≠ BETTER DESIGN`.
