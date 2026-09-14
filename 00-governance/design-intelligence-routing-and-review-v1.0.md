# OLEANDER Design Intelligence Routing & Review System v1.0

**Status:** ACTIVE<br>
**Date:** 2026-09-14<br>
**Scope:** all OLEANDER design projects, methods, reusable skills and project outputs.<br>
**Position:** this system extends the existing OLEANDER project flow with design-intelligence routing and design-quality review. It does not replace the L0–L7 knowledge architecture, P0–P4 project axis, Artifact Review System, specialized technical gates, evidence governance, AIG governance, or Production Asset Persistence Gate.

## 1｜Canonical relationship to the existing OLEANDER architecture

OLEANDER must keep four concerns separate:

1. **Knowledge Architecture** — where reusable knowledge belongs: `L0 System → L1 Branch → L2 Domain → L3 Topic → L4 Framework / Cluster → L5 Knowledge Object / Index → L6 Evidence / Case → L7 Practice / Output`.
2. **Project Architecture** — where current work belongs: `P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`.
3. **Application Mapping** — where knowledge is being applied: Business / Culture / IP / Spatial.
4. **Execution & Review Flow** — how a current task reads knowledge, develops a design, validates it and promotes or rejects the result.

This file governs item 4 only. It must not create a second knowledge tree or reuse L/P/Application namespaces for review routing.

The current authority chain remains:

`MASTER PROTOCOL → PROJECT STATE → SOURCE AUTHORITY → CURRENT TASK`

The current cognitive method remains:

`Read → Frame → Hypothesize → Vary → Construct → Attack → Test → Decide → Archive`

Design Intelligence routing makes the `Read / Frame / Decide` portions explicit and connects them to existing knowledge objects and review gates.

## 2｜Four-plane operating model

### Plane A｜Knowledge Plane

Stores reusable design knowledge, methods, sources, evidence, cases and practice. Existing Notion/GitHub identity and relations remain authoritative.

Typical roles include:

- THEORY / Framework — explanatory models and professional design knowledge;
- METHOD — reusable procedures and decision methods;
- SOURCE / EVIDENCE — factual or professional support;
- CASE — precedent or case material;
- PRACTICE / OUTPUT — exercised or project-derived application.

Do not convert these roles into project stages. A METHOD may be called at several stages; a CASE may inform framing or critique; PRACTICE is not automatically authority for a new project.

### Plane B｜Project Plane

Stores the current design problem, project state and decisions under P0–P4.

The project does not copy the knowledge base into itself. It resolves and cites the minimum relevant current knowledge objects, then records project-specific decisions, evidence and outputs.

### Plane C｜Review Plane

Contains four independent review classes:

1. **Design Review** — professional design judgment.
2. **Artifact Review** — AR-G / AR-S integrity and final-artifact review.
3. **Specialized Technical Gates** — BA, accessibility, fabrication, code, field verification and other domain gates when triggered.
4. **Evidence / Truth Review** — whether factual and professional claims are supported to the stated level.

None substitutes for another.

### Plane D｜Learning Plane

G9 / post-use findings return to the Knowledge Plane only after their evidence, scope and maturity are explicit. Project experience is not silently promoted into a universal rule.

The loop is:

`Knowledge → Project → Design / Test / Review → Decision → Use / Feedback → Knowledge Candidate → Validation → Current Knowledge`

## 3｜Design Intelligence Packet

Before a Candidate enters Canonical Production, the current project should compile a lightweight **Design Intelligence Packet**. It is a project-runtime object, not a new L-level knowledge object by default.

Minimum fields:

- `design_question` — the decision to be made;
- `people_or_audience` — who experiences or uses the design;
- `context` — physical, cultural, operational, technical and temporal context relevant to the decision;
- `desired_change` — what should become different because of the design;
- `desired_experience` — intended reading / use / spatial / emotional outcome when applicable;
- `non_goals` — what this task is not trying to solve;
- `locked_variables`;
- `open_variables`;
- `key_design_tensions` — important trade-offs rather than fake universal maxima;
- `knowledge_routes` — current L4/L5 frameworks and methods actually used;
- `evidence_routes` — L6/source/evidence needed for factual or professional claims;
- `precedent_routes` — relevant cases when comparison is useful;
- `practice_routes` — relevant L7 practice examples, never treated as fact merely because they exist;
- `review_lenses` — design disciplines that must review the result;
- `cross_disciplinary_integration_trigger` — whether multiple coupled disciplines require the integration system;
- `technical_gate_triggers`;
- `claim_ceiling` — strongest claim the current evidence and task are allowed to support;
- `exit_condition`.

The packet is intentionally smaller than a full project brief. It exists to prevent design execution from starting without an explicit problem, knowledge route and review contract.

## 4｜Research and evidence are related but not identical

OLEANDER distinguishes:

`DESIGN RESEARCH → understanding / insight / opportunity`

from:

`EVIDENCE → support for a factual, professional or validation claim`.

The same source may serve both purposes, but the resulting claims must remain distinct.

Canonical transformation:

`Observation / Source → Insight → Design Intent → Principle / Hypothesis → Design Decision → Artifact → Experience / Outcome`

An insight may guide design without being promoted to a universal fact. A project decision may be valid even when some contextual variables remain OPEN. Conversely, attractive design logic cannot upgrade unsupported claims to evidence.

## 5｜Design Intent Graph

For major decisions, maintain an explainable chain:

`Problem → Evidence / Observation → Insight → Intent → Principle / Hypothesis → Decision → Artifact → Expected Experience → Test / Readback → Outcome`

The graph need not be a literal graph database for every task. It is a reasoning contract: important design elements should be explainable through this chain.

If an element cannot be connected to intent, use, system meaning or an explicit expressive decision, it is a candidate for removal or reclassification as decoration.

## 6｜Common Design Kernel

The following are **review questions**, not a universal scorecard:

1. **Intent** — is the reason for the design explicit and consequential?
2. **Context** — does the design respond to the actual people, place, task, medium and conditions?
3. **Concept** — is there a strong generative idea rather than a descriptive mood?
4. **Perception** — are hierarchy, figure/ground, sequence, scale, contrast and attention deliberately controlled?
5. **Use** — can people understand, operate, inhabit, navigate or read the design as intended?
6. **System** — do parts form a coherent set of relations rather than an accumulation of features?
7. **Craft** — are details, transitions, joints, typography, surfaces or interactions resolved to the required level?
8. **Inclusion** — are relevant differences in ability, language, culture, access and conditions considered?
9. **Experience** — does the actual temporal / spatial / interaction experience match the stated intent?
10. **Distinctiveness** — does the work have a reason to be remembered or differentiated where that matters?
11. **Adaptability** — can the design handle legitimate variations, states and future change without losing its principle?
12. **Proof** — what has actually been tested or read back, and what remains assumption?

Rules:

- do not average these twelve questions into one design score;
- do not force every discipline to weight them equally;
- a hard failure in use, safety, truth or a triggered professional requirement cannot be averaged away by visual strength;
- design judgment remains `KEEP / REVISE / REJECT / HOLD` with reasons.

## 7｜Discipline Review Lenses

OLEANDER does **not** create a new parallel knowledge taxonomy such as a second tree of `DKE-*` pages. The project resolver selects review lenses and retrieves the relevant existing L4/L5/L6/L7 knowledge through Domain / Topic / relation routing.

Typical lenses include:

- Strategy / framing;
- Research / human factors;
- Content / information architecture;
- Visual communication / typography;
- Brand / design language;
- Product / industrial design;
- CMF / material experience;
- Interaction / UX / UI;
- Service design;
- Spatial / architectural design;
- Landscape / site experience;
- Exhibition / interpretation;
- Wayfinding / environmental graphics;
- Lighting;
- Sound / soundscape;
- Data visualization;
- Motion / temporal design;
- Immersive / XR when applicable;
- Presentation / portfolio / board;
- Design-system / cross-touchpoint consistency;
- Computational / parametric design when it materially affects the design decision.

These are **runtime review lenses**, not new L2 Domains unless the Knowledge Architecture separately decides to create or rename a domain.

When two or more lenses materially constrain the same design decision, or when one discipline's output becomes another discipline's required input, also trigger `cross-disciplinary-design-integration-v1.0.md`. Multiple lenses running in parallel are not sufficient evidence of an integrated design.

## 8｜Discipline lens contract

Every triggered lens should identify:

- the design question it owns;
- relevant existing METHOD / THEORY objects;
- required source/evidence only when factual or professional claims depend on it;
- representative precedents or counterexamples where useful;
- failure signs;
- what can be judged through expert/design critique;
- what requires user, physical, field or technical validation;
- what it explicitly does not prove.

Examples:

### Spatial / architectural design lens

Owns spatial concept, approach/arrival, threshold, sequence, mass/void, section, circulation, scale, proportion, light, view, material experience, program relation, body, time and memory.

It does **not** replace the Built-asset High-Fidelity Gate, engineering review, code review or field verification.

### Product / industrial design lens

Owns form–function relation, human fit, affordance, ergonomics, proportion, product architecture, control/feedback, tactile logic and product character.

It does **not** replace fabrication, mechanical, material performance, safety or manufacturing validation.

### Visual / presentation lens

Owns message, argument, hierarchy, composition, grid, typography, image relation, density, rhythm, selection, page sequence, zoom level and final craft.

It does **not** treat clean export or AR-S08 compliance as proof of strong communication design.

### Interaction / service lens

Owns user goal, information architecture, task flow, state model, affordance, feedback, recovery, cognitive load, cross-channel handoff and temporal experience.

It does **not** treat functional completeness, accessibility compliance or code PASS as proof of excellent UX/service design.

## 9｜Design exploration and comparison

OLEANDER keeps the existing Comparison-First rule. When a design question is genuinely open, prefer controlled variants over a single unchallenged first answer.

Default logic:

`Frame → Hypotheses / Variants → Compare under fixed conditions → Attack → Test → Candidate`

Design exploration may stop when an acceptable corridor is stable. OLEANDER does not require artificial option counts or performative ideation when the decision is already constrained by authority, evidence or a locked design system.

## 10｜Multi-scale and temporal review

When relevant, design critique should deliberately move across:

- **Macro** — strategy / whole system / overall concept;
- **Meso** — sequence / family / chapter / subsystem;
- **Micro** — component / detail / junction / typography / interaction;
- **Temporal** — states, transitions, aging, season, use sequence or operational change;
- **Lifecycle** — fabrication / launch / use / maintenance / adaptation / retirement when applicable.

This prevents `micro detail richness` from substituting for weak overall design and prevents a strong concept from masking unresolved details.

## 11｜Design tensions and trade-offs

Good design often resolves competing values rather than maximizing every metric. Important tensions should be explicit, for example:

`clarity ↔ richness`<br>
`consistency ↔ variety`<br>
`novelty ↔ familiarity`<br>
`density ↔ calm`<br>
`control ↔ agency`<br>
`openness ↔ privacy`<br>
`durability ↔ lightness`<br>
`iconic expression ↔ contextual fit`<br>
`cost ↔ craft`.

For important tensions record:

`chosen position / reason / accepted cost / condition that would reopen the decision`.

## 12｜Benchmark and adversarial review

Internal improvement is insufficient for professional promotion. When design quality is material, compare against a bounded benchmark set:

- **Peer** — credible work solving comparable problems;
- **Aspirational** — work representing the intended quality ceiling;
- **Counterexample** — failure mode or direction the project explicitly avoids.

Benchmarking is not style copying. The comparison must identify transferable relations, decision quality, execution depth or failure modes.

Adversarial review actively seeks the strongest reason the current design might fail its stated intent.

## 13｜Responsibility overlays

Cross-cutting responsibilities are not new design domains and must not be deferred until final QA. Trigger them when materially relevant:

- accessibility;
- inclusion / equity;
- safety;
- privacy / data responsibility;
- cultural / community responsibility;
- ecology / biodiversity;
- carbon / resource use;
- circularity / repair / disassembly;
- resilience;
- maintenance / operations;
- rights / licensing.

Some overlays create hard technical gates; others create design obligations or evidence requirements. The project must distinguish the two.

## 14｜Integration with Canonical Project Flow

The existing dual-loop architecture remains. Design Intelligence refines it as follows.

### Exploration Sandbox

`Design Question → Knowledge Route → Frame / Intent → Hypotheses / Variants → Compare → Attack / Test → Reject / Branch / Candidate`

### Candidate Gate

In addition to the existing Candidate requirements, a Candidate intended for design-quality promotion should have:

- a resolvable Design Intelligence Packet;
- explicit relevant knowledge routes;
- triggered design review lenses;
- when applicable, a resolvable `CROSS_DISCIPLINARY_INTEGRATION_PACKET` with critical interfaces, owners, coupling / criticality, shared variables, required interface maturity, acceptance / readback basis and integration tests;
- known technical/evidence gate triggers;
- an explicit claim ceiling.

### Canonical Production

`Candidate → Contract Compile → Design Review Resolve → Cross-Disciplinary Integration Resolve when triggered → Authority Resolve → Capability Resolve → Execute → Machine QA → Visual QA → Project QA → Artifact Review → Triggered Design Review → Integration Readback when triggered → Specialized Technical Gates → Evidence / Truth Review → Independent Design Decision → Persistence when triggered → Promote / Revise / Reject → Artifact Register → Cross-System Sync`

Ordering may interleave in real work; for example design review can force another prototype before technical completion. The logical rule is that all triggered review classes must close before Promotion.

For complex projects, discipline-level PASS does not close the system-level design. Critical cross-disciplinary interfaces must also close under `cross-disciplinary-design-integration-v1.0.md`.

## 15｜Design Review Receipt

For material design decisions, record a compact `DESIGN_REVIEW_RECEIPT` with at least:

- `design_question`;
- `design_intent`;
- `triggered_lenses`;
- `knowledge_routes`;
- `strongest_design_decision`;
- `weakest_or_open_design_decision`;
- `key_design_tensions`;
- `benchmark_basis` when used;
- `design_findings`;
- `evidence_backed_findings`;
- `assumptions_and_open_items`;
- `technical_gate_dependencies`;
- `integration_receipt_id`, current integration verdict and integration claim ceiling when triggered;
- `integration_blockers_or_open_interfaces` as a summary when triggered;
- `revision_priorities`;
- `design_verdict = KEEP / REVISE / REJECT / HOLD`;
- `promotion_ceiling`;
- reviewer / date / artifact or review-contract identity.

Machines may validate receipt completeness and invalid promotion combinations. Machines must not auto-award `KEEP` from field counts or averaged scores.

## 16｜Final Craft Review

Before presentation/release promotion, review the last-mile design resolution appropriate to the medium, including when applicable:

- spacing / alignment / optical balance;
- edge / joint / termination / transition;
- typography / crop / caption / legend;
- micro hierarchy / micro interaction;
- motion timing / easing / interruption;
- material / texture / light readback;
- export color / resolution / scale / media behavior;
- cross-page / cross-view / cross-touchpoint consistency.

Final Craft is a design-quality review. It does not replace AR-G10 or AR-S review.

## 17｜G9 learning and Knowledge Base write-back

After delivery / use / exhibition / operation, capture actual observations where available:

`Intended outcome → observed outcome → difference → reason / uncertainty → lesson candidate`.

Write-back rules:

1. project-specific findings remain Project / Practice unless generalization is justified;
2. a repeated lesson may become an L5 METHOD/Knowledge Object candidate only after scope, counterexample and validation are explicit;
3. external factual support belongs in SOURCE/EVIDENCE relations, not embedded as unattributed method truth;
4. counterexamples and failed attempts are retained when they materially improve future judgment;
5. superseded rules remain provenance, not parallel Current authority;
6. G9 can reopen a previously locked design conclusion when real use reveals material failure.

Useful reusable knowledge forms include:

- Design Principle;
- Pattern / Anti-pattern;
- Precedent / Counterexample;
- Failure Mode;
- Trade-off / Exception;
- User or Place Insight;
- Material / Spatial / Interaction Detail Pattern;
- Lesson Learned.

These are content forms inside the existing L0–L7 architecture, not a new hierarchy.

## 18｜Canonical invariants

`ARTIFACT EXISTENCE ≠ DESIGN QUALITY`<br>
`MACHINE PASS ≠ DESIGN KEEP`<br>
`TECHNICAL VALIDATION ≠ DESIGN QUALITY`<br>
`EVIDENCE CORRECTNESS ≠ VISUAL EXCELLENCE`<br>
`ACCESSIBILITY COMPLIANCE ≠ UX EXCELLENCE`<br>
`BUILT-ASSET FIDELITY ≠ SPATIAL QUALITY`<br>
`VISUAL REALISM ≠ PHYSICAL TRUTH`<br>
`CONSISTENCY ≠ UNIFORMITY`<br>
`DETAIL DENSITY ≠ CRAFT`<br>
`PROCESS PASS ≠ MAIN KEEP`<br>
`DESIGN KEEP ≠ AUTOMATIC PROMOTION`

## 19｜Promotion rule

Promotion is eligible only when:

1. the Design Question and project intent are resolved to the required level;
2. all triggered design review lenses have a recorded verdict;
3. AR-G and applicable AR-S gates pass;
4. specialized technical gates pass or remain explicitly outside the promoted claim;
5. evidence/truth boundaries support the promoted claim;
6. no unresolved blocker contradicts the result;
7. when cross-disciplinary integration is triggered, critical interfaces reach the required maturity for the promoted claim, no in-claim blocker contradicts the system, and a current `CROSS_DISCIPLINARY_INTEGRATION_RECEIPT` matches the promoted artifact / review-contract basis;
8. independent design judgment permits the intended promotion level;
9. PAP / release persistence requirements pass when triggered.

The governing principle is:

> **Knowledge informs design. Design judgment evaluates design. Technical gates validate technical claims. Evidence limits truth claims. Artifact and persistence systems protect deliverables. Promotion requires all triggered responsibilities to agree.**
