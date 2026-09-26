# OLEANDER Product Review Bar v0.3.0

[← v0.3 Package](README.md)

**Purpose:** 给 PM / Design / Eng / AI / Domain Reviewer 一套一致的产品评审标准。

---

# 1｜Review Question

A mature review should answer:

> **Should we invest in this product decision now, for this customer, with this scope, and do we know how to tell whether it worked?**

It is not:
- “document is long”；
- “architecture is complex”；
- “demo looks impressive”。

---

# 2｜Bar 1 — Customer Problem

PASS_WORKING when:
- target user is explicit；
- real context is explicit；
- problem has evidence labels；
- current workaround is known；
- consequence is described；
- major assumptions remain visible。

RED FLAGS:
- solution looking for a problem；
- owner preference presented as market fact；
- “AI users” as one persona；
- no external validation plan。

---

# 3｜Bar 2 — Product Strategy

PASS_WORKING when:
- product wedge is explicit；
- non-goals are explicit；
- differentiation is about user value, not feature count；
- why-now logic exists；
- alternative solutions are understood；
- stop/reframe conditions exist。

RED FLAGS:
- roadmap = feature wishlist；
- every problem becomes P0；
- platform breadth before core value proof。

---

# 4｜Bar 3 — Requirements

PASS_WORKING when each P0 requirement has:
- user/context
- trigger
- input
- behaviour
- visible result
- Human/System allocation
- failure behaviour
- acceptance
- instrumentation

RED FLAGS:
- requirement describes implementation only；
- acceptance = “feature exists”；
- no degraded path；
- hidden authority assumption。

---

# 5｜Bar 4 — UX / Human Factors

PASS_WORKING when:
- first-use / re-entry flow is clear；
- ambiguity handling exists；
- progressive disclosure exists；
- Human stop is explainable；
- user can challenge/correct；
- system does not force internal terminology。

RED FLAGS:
- governance leaked into default UI；
- every action asks confirmation；
- opaque autonomy；
- system infers durable preference from casual feedback。

---

# 6｜Bar 5 — AI Product Quality

PASS_WORKING when:
- model uncertainty is bounded；
- authoritative sources are explicit；
- actions bind exact referents；
- exploration checks meaningful search-space gaps rather than only option count；
- AI triage preserves real Human value trade-offs；
- synthesis preserves lineage and unresolved conflict；
- artifact execution can compare intended delta with actual delta；
- Action Guard covers sensitive external read/disclosure as well as writes；
- eval dimensions are defined；
- fallback exists；
- model/provider changes trigger regression。

RED FLAGS:
- “model confidence” used as authority；
- many generated alternatives treated as exploration coverage；
- AI silently removes a branch whose weakness depends on Human value judgment；
- synthesis is only copy/paste MIX with no coherent mechanism；
- LLM evaluator is only source of truth；
- no false-completion test；
- no stale-state test。

---

# 7｜Bar 6 — Metrics

PASS_WORKING when:
- outcome metric(s) measure user value rather than model activity；
- formula has numerator/denominator；
- eligibility/exclusion defined；
- guardrails exist；
- events connect to outcomes；
- thresholds frozen before experiment。

RED FLAGS:
- generated output count；
- token count；
- session length；
- internal test pass presented as customer value；
- VPCR used as if continuity alone proves better design progress；
- DRPR converted into a synthetic design-quality score。

---

# 8｜Bar 7 — Experimentation

PASS_WORKING when:
- hypothesis pre-written；
- baseline/treatment defined；
- cohort defined；
- primary metric frozen；
- guardrail frozen；
- failure result retained；
- qualitative and quantitative evidence separated。

RED FLAGS:
- post-hoc success metric；
- no baseline；
- only owner self-use；
- one anecdote closes product hypothesis。

---

# 9｜Bar 8 — Delivery / Ownership

PASS_WORKING when:
- every launch-critical dependency has owner；
- RACI is explicit；
- cutline is explicit；
- unresolved dependencies are visible；
- no fictional team roles are presented as staffed。

RED FLAGS:
- “engineering will handle it”；
- no owner for privacy/security；
- no dependency on external authoring reality。

---

# 10｜Bar 9 — Launch Readiness

PASS_WORKING when:
- rollout stage defined；
- rollback defined；
- telemetry complete；
- support owner exists；
- privacy/security reviewed；
- launch-blocking risks closed or explicitly accepted by authorized owner。

RED FLAGS:
- build complete = launch ready；
- no rollback；
- no support；
- no incident model；
- no data retention decision。

---

# 11｜Bar 10 — Learning Loop

PASS_WORKING when:
- post-launch review cadence exists；
- product decision log exists；
- assumptions can be reopened；
- failed ideas remain recoverable；
- roadmap changes cite evidence。

RED FLAGS:
- launch treated as finish line；
- old rationale lost；
- success story only, no negative evidence。

---

# 12｜Current OLEANDER Self-assessment

This is descriptive, not a score.

**Strong / relatively mature**
- design-process problem decomposition
- requirement traceability
- Human authority semantics
- artifact/readback thinking
- failure / degraded semantics
- candidate interaction testing
- v0.3.2 co-design content model: Search-space / Triage / Synthesis / Decision / Artifact Action / Whole-design Check

**Material gaps before large-company product bar**
- v0.3.2 product-content → runtime/system parity
- external customer evidence
- market/competitive evidence
- frozen pilot thresholds
- implemented product analytics
- staffed ownership beyond solo stage
- security/privacy product baseline
- operational support
- rollout/rollback exercised
- business model validation
- longitudinal external retention

These gaps are now explicit workstreams rather than hidden omissions.
