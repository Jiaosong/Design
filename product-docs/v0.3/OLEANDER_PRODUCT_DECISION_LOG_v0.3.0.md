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

**Status:** WORKING PRODUCT HYPOTHESIS

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