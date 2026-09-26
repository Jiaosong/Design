# OLEANDER Product Decision Log v0.3.0

[← v0.3 Package](README.md)

**Purpose:** 保留重要产品选择的 rationale、alternatives 和 reopen condition。
**Boundary:** Product Decision Log 不拥有 OLEANDER Architecture / Project / Professional / Promotion authority。

---

# Decision Template

Each consequential product decision should include:

- Decision ID
- Date
- Status
- Decision
- Owner
- Context / problem
- Alternatives considered
- Rationale
- Consequence
- Evidence
- Reopen condition
- Linked PRD / metric / experiment

---

# PD-001｜Conversation is not Project State

**Date:** 2026-09-26
**Status:** ACCEPTED PRODUCT TENET
**Owner:** Product

**Decision**
Do not treat conversation history or model memory as authoritative project state.

**Alternatives**
1. Chat history as state
2. Model memory as state
3. Owner-native project carriers + chat projection

**Selected**
3.

**Rationale**
Long-lived professional project truth requires explicit Current, revision, authority and artifact identity.

**Reopen if**
Future platform provides explicit durable project-state semantics with equivalent authority/revision guarantees.

---

# PD-002｜Session Kernel is cross-product, not the whole product

**Status:** ACCEPTED

**Decision**
Keep HOME / FOCUS / STUDIO / MAP / ARTIFACTS / REVIEW / KNOWLEDGE / HISTORY as product structure. Session Kernel spans them.

**Rejected alternative**
Product = one universal session state machine.

**Rationale**
Universal interaction semantics are reusable; professional design process and product surfaces are richer and domain-authentic.

**Reopen if**
User research shows dedicated surfaces add no value beyond session interaction.

---

# PD-003｜Auto-advance reversible work

**Status:** ACCEPTED WORKING HYPOTHESIS

**Decision**
AI should continue reversible, authorized work without asking after every tool call.

**Alternative**
Confirm every action.

**Rationale**
Human-in-the-loop should occur at real decision boundaries, not every operational step.

**Guardrail**
Unauthorized Action Rate = 0.

**Reopen if**
Pilot users show persistent loss of control or inability to predict AI actions.

---

# PD-004｜Material alternatives over option count

**Status:** ACCEPTED

**Decision**
Count options only when mechanism / relation / consequence materially differs.

**Rejected alternative**
Three visual variants satisfy “three options.”

**Reopen if**
Users value rapid aesthetic variation as the primary workflow for a specific product/domain; that may become a separate mode, not global rule.

---

# PD-005｜Readback required after material making

**Status:** ACCEPTED

**Decision**
Material artifact changes require actual result readback before validated/done claim.

**Alternative**
Trust tool execution log.

**Rationale**
Execution success is not design success.

**Reopen if**
A specific deterministic tool provides equivalent verified result evidence; even then claim scope must remain bounded.

---

# PD-006｜Compare is a cross-surface mode

**Status:** WORKING DECISION

**Decision**
Treat Compare primarily as a mode across Studio / Review / Artifacts rather than isolated destination.

**Rationale**
Comparison happens in multiple design contexts.

**Reopen if**
Usability testing shows users need a persistent dedicated decision workspace.

**Experiment**
UX prototype / pilot.

---

# PD-007｜Design Map only for material relations

**Status:** ACCEPTED CONSTRAINT

**Decision**
Do not represent every project relationship. First-class relation requires material impact on judgment/change/integration/continuity/review.

**Rationale**
Avoid turning Design Map into administrative graph maintenance.

**Reopen if**
Automatic extraction becomes reliable and low-cost enough that broader graph density creates user value.

---

# PD-008｜No durable taste/competence profile from ordinary steering

**Status:** ACCEPTED HARD BOUNDARY

**Decision**
Session choices may adapt current support but do not create durable psychological, taste or ability claims.

**Rationale**
Single project choices are contextual and can be overgeneralized.

**Reopen if**
User explicitly opts into a defined profile product with transparent controls and separate validation.

---

# PD-009｜Domain-native professional processes remain separate

**Status:** ACCEPTED HARD BOUNDARY

**Decision**
Shared Human–AI interaction model does not create one universal professional stage model.

**Rationale**
Architecture, product, HCD, engineering and other domains have different professional outputs, liabilities and validation.

**Reopen if**
Only at level of genuinely universal interaction semantics, never by erasing domain authority.

---

# PD-010｜v1 wedge = Verified Project Continuity + Human-steered Real Artifact Loop

**Status:** REFINED BY PD-015 / PD-016 / PD-017 / PD-018 / PD-020

**Decision**
Prioritize:
```text
Resume
→ Explore
→ Make
→ Readback
→ Human Steer
→ Second Round
→ Continue
```
before Team / Marketplace / broad cloud integrations.

**v0.3.2 refinement**
The wedge remains continuity + real artifact collaboration, but the launch-critical loop now explicitly includes Search-space Map, AI Option Triage, persistent Design Decision, Design Synthesis where useful, Artifact Action intended/actual delta, and Whole-design Check. This refinement prevents the product from becoming only a continuity/governance layer.

**Rationale**
This tests the highest-leverage differentiated value with the least platform breadth.

**Reopen if**
External users rank another pain materially higher or core loop fails to generate retention intent.

---

# PD-011｜External pilot thresholds must be frozen before run

**Status:** ACCEPTED RESEARCH RULE

**Decision**
Do not invent targets after results are visible.

**Rationale**
Avoid post-hoc success definition.

**Reopen**
Only with documented methodology correction; original analysis remains visible.

---

# PD-012｜PRD is not architecture authority

**Status:** ACCEPTED HARD BOUNDARY

**Decision**
Product docs can define product requirements but do not silently change Current architecture, Project State, artifact authority, professional process or Promotion.

**Rationale**
Avoid shadow governance created for portfolio/readability purposes.

**Reopen**
No planned reopen; any change requires formal architecture/governance path.

---

# PD-013｜CONTINUE is not RESUME

**Status:** ACCEPTED PRODUCT SEMANTIC

**Decision**
Separate:
- RESUME — reconstruct after session/context loss；
- CONTINUE — advance the current valid frontier / authorized path；
- RECOVER — resume after failure / partial completion / state conflict。

The Human word “继续” is resolved from current interaction context; it is not permanently mapped to RESUME.

**Rationale**
Treating every continuation as project reconstruction adds friction and can recompute an already stable frontier.

**Guardrail**
CONTINUE never automatically becomes consequential Human steer or Design Decision.

---

# PD-014｜Design Situation before forced Problem framing

**Status:** ACCEPTED PRODUCT SEMANTIC

**Decision**
FOCUS may begin from problem, opportunity, ambition, requirement, conflict or unknown. Problem Statement remains available when it is the correct framing, but is not a universal gateway.

**Rationale**
Architecture, spatial, brand, CMF and exploratory design are not always problem-removal exercises.

---

# PD-015｜Explore owns search-space awareness and AI triage

**Status:** WORKING P0 DECISION

**Decision**
EXPLORE must:
1. identify materially meaningful search dimensions / mechanism families；
2. expose important coverage gaps；
3. generate materially distinct directions；
4. triage obvious duplicates / hard-constraint failures / unsupported weak branches out of the presented set before Human review；
5. preserve lineage and genuine value trade-offs。

**Rejected alternative**
“Generate N options” is sufficient exploration.

**Reopen if**
External design studies show search-space mapping or triage adds review burden without improving decision usefulness.

---

# PD-016｜SYNTHESIZE is generative, not only simplification

**Status:** WORKING P0 DECISION

**Decision**
SYNTHESIZE may create a new coherent direction from multiple valid branches, findings, evidence and constraints. It must distinguish inherited, transformed, newly introduced, intentionally discarded and unresolved elements.

**Hard boundary**
Human MIX steer and AI Design Synthesis are related but not the same operation.

---

# PD-017｜Design Decision is a first-class persistent object

**Status:** ACCEPTED PRODUCT MODEL CHANGE

**Decision**
Consequential SELECT / MODIFY / MIX / REJECT / DEFER produces or updates a persistent Design Decision object with actor, authority basis, options considered, rationale when supplied, trade-offs, affected relations/artifacts, status, reopen condition and supersession lineage.

A Design Decision may originate from Compare, Focus, Review, People/Authority or a direct valid Human instruction. Compare is a common decision context, not a mandatory prerequisite.

**Rationale**
Human steer is an interaction event; Decision is durable project meaning. History records it but does not own it.

---

# PD-018｜Artifact action owns intended vs actual delta

**Status:** ACCEPTED P0 PRODUCT CONTRACT

**Decision**
Before material making/editing, OLEANDER identifies target artifact/revision and intended delta. After tool execution, it captures actual delta/new revision and performs readback. Rollback/recovery is recorded where the authoring surface supports it.

**Boundary**
OLEANDER owns the design-action contract; CAD/BIM/Figma/IDE/3D integrations own native tool execution.

---

# PD-019｜Action Guard supersedes write-only product semantics

**Status:** ACCEPTED PRODUCT SEMANTIC / RUNTIME MIGRATION PENDING

**Decision**
The product-level guard covers consequential reads/writes, sensitive data disclosure, external publish, provider boundaries, material cost, recoverability and blast radius.

The existing “Mutation Guard” term may remain as a write-specific runtime implementation/subcheck until the system is revised.

**Rationale**
A read-only tool call can still create confidentiality, cost or external-disclosure risk.

---

# PD-020｜VPCR + DRPR form the outcome pair

**Status:** WORKING METRIC DECISION

**Decision**
- VPCR measures whether long-running work can continue correctly.
- DRPR measures whether a materially important Design Question / unknown / decision object made traceable resolution progress.

**Hard boundary**
DRPR is not a synthetic Design Quality Score and does not allow AI to declare a design “better” from one aggregate score.

---

# PD-021｜Designer development is contextual, not profiling

**Status:** ACCEPTED P1 DIRECTION

**Decision**
OLEANDER may expose reasoning, trade-offs, failure learning, evidence consequences and optional reflection in the context of current work. Support may fade within a session when repeated explanation is unnecessary.

**Hard boundary**
Ordinary steering does not create a durable taste, competence, psychological or professional-qualification profile.

---

# PD-022｜OLEANDER is harness-agnostic; runtime providers are replaceable

**Status:** ACCEPTED PRODUCT ARCHITECTURE DIRECTION / SYSTEM ALIGNMENT OPEN

**Decision**
OLEANDER keeps product semantics, Project State/Current semantics, Human authority, Design Decision, Artifact identity, Action Guard policy, Claim Ceiling and Design Quality semantics in its own product kernel.

Agent harnesses and workflow platforms sit below a provider-neutral Runtime Contract and are replaceable execution providers.

**Reference provider strategy**
- DeepSeek Harness: preferred first runtime-adapter spike because its plugin/session/tool/sandbox/approval seams map well to OLEANDER runtime needs;
- Dify: optional bounded workflow/RAG/pilot provider, not core Project State or Session Kernel;
- COS/native execution: current reference path used to define the Runtime Contract before external provider adoption.

**Hard boundaries**
- provider session/event log ≠ Project State；
- provider approval ≠ Human Design Decision；
- provider tool permission ≠ OLEANDER Action Guard；
- provider completion ≠ Design / Artifact completion；
- provider removal must not make Project State unrecoverable；
- harness plugin granularity does not authorize OLEANDER Skill proliferation；
- workflow DAG does not become a universal professional process。

**Rejected alternatives**
1. Rewrite OLEANDER as one Dify workflow graph.
2. Make DeepSeek Harness session storage the canonical Project State.
3. Couple product semantics directly to one harness's plugin/event APIs.

**Reopen if**
A provider-neutral contract creates more maintenance cost than it removes, or a future runtime proves it can own the required semantics without creating a second authority/state system.
