# OLEANDER Complex Project Master Runtime v1.0

**Status:** ACTIVE / CURRENT PROJECT-RUNTIME ORCHESTRATION CONTRACT  
**Date:** 2026-09-14  
**Owner:** OLEANDER Governance  
**Scope:** all OLEANDER projects whose design, execution, evidence, technical review, persistence or cross-disciplinary dependencies require coordinated runtime decisions.  
**Authority position:** subordinate to the unique OLEANDER Current Authority / namespace governance; authoritative for cross-module project-runtime orchestration only.

## 1｜Purpose

This file closes the project-runtime authority gap between existing OLEANDER modules. It is deliberately thin.

It does **not** replace or duplicate:

- the L0–L7 Knowledge Architecture;
- the P0–P4 Project Axis;
- Project / Source Authority;
- `design-intelligence-routing-and-review-v1.0.md`;
- `cross-disciplinary-design-integration-v1.0.md`;
- `oleander-project-flow-v0.3.md`;
- Artifact Review, specialist technical gates, Evidence / Truth Review or PAP;
- the existing Project Control Card / Control Plane;
- independent professional design judgment.

Its job is to decide **which existing owner runs, what state becomes stale, what must reopen, and whether the current project state is runnable or promotion-ready**.

## 2｜Canonical project-runtime chain

```text
CURRENT AUTHORITY / PROJECT AUTHORITY / SOURCE AUTHORITY
                         │
                         ▼
            COMPLEX PROJECT MASTER RUNTIME
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
  Knowledge Plane   Project Plane   Design Intelligence
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              Integration Trigger Resolve
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
     discipline-local          materially coupled
          route                integration route
             │                       │
             │            Cross-Disciplinary Integration
             └───────────┬───────────┘
                         ▼
              Execution / Prototype Runtime
                         ▼
       Artifact / Discipline / Technical / Evidence Review
                         ▼
               Integration Readback when triggered
                         ▼
          Independent Whole-System Design Decision
                         ▼
                Persistence / Promotion
                         ▼
                         G9
                         ▼
           bounded reusable learning re-entry
```

The Master compiles this chain; it does not absorb the detailed contracts owned by each module.

## 3｜Master-owned responsibilities

The Master owns only eight cross-module questions:

1. **Invocation** — which current module / review / specialist gate must run for this decision object?
2. **Precedence** — which authority governs when outputs disagree?
3. **State propagation** — which downstream states become stale after a material change?
4. **Handoff** — what minimum identity / state / receipt must cross each module boundary?
5. **Claim ceiling** — what claims remain legal under current evidence and open states?
6. **Promotion eligibility** — have all triggered responsibilities closed sufficiently for a human promotion decision?
7. **Re-entry** — what validated project learning may return to existing knowledge owners at G9?
8. **Version / supersession** — which runtime contract is Current and which prior contract becomes provenance?

## 4｜Precedence by question type

There is no single universal winner. Precedence depends on the question.

### 4.1 Identity / authority

`Current Authority / Project Authority / Source Authority > runtime convenience > generated artifact`.

An unresolved authority conflict produces `HOLD`; no module may solve it by creating a parallel Current object.

### 4.2 Factual / technical truth

Applicable verified sources, field evidence, engineering / code / safety / accessibility requirements and project-specific measured evidence govern their own truth domain.

Design intent cannot override a factual or hard technical failure.

### 4.3 Cross-disciplinary coherence

For a claim that depends on coupled disciplines:

`current Integration Readback / CROSS_DISCIPLINARY_INTEGRATION_RECEIPT > isolated discipline PASS`.

### 4.4 Design quality

For `KEEP / REVISE / REJECT / HOLD`:

`Independent whole-system design judgment > Artifact PASS / Technical PASS / Evidence completeness / Integration PASS`.

### 4.5 Promotion

Promotion is bounded by the **lowest applicable valid claim ceiling** and every applicable unresolved blocker.

The machine runtime reports claim-ceiling inputs but does not pretend that unrelated domain-specific claim strings have a universal numeric ordering.

## 5｜Knowledge Plane contract

The project runtime consumes the current OLEANDER knowledge graph; it does not turn the graph into a workflow.

Knowledge classification is resolved independently through:

`Domain / Topic → Content Level → Knowledge Role → Framework Type (L4 only) → typed relations → authority / trust / evidence state`.

Current target layers are:

- `CURRENT_AUTHORITY_LAYER` — Current knowledge / authority carriers;
- `SUPPORT_EXTENSION_LAYER` — reusable supporting knowledge;
- `PROVENANCE_LINEAGE_LAYER` — lineage / history, searchable but excluded from Current structural authority.

Runtime routing rules:

- use body / Current metadata, not title prefixes, as semantic authority;
- `Canonical Parent / Children` means structural hierarchy only;
- Domain placement, Method invocation, Source / Evidence support, Project use, semantic Related and Supersession remain separate relations;
- `UNRESOLVED` relation state is not an empty relation set;
- a known graph conflict lowers routing confidence or produces HOLD for decisions that depend on that unresolved relation;
- provenance may inform history but cannot become a Current parent or authority by convenience.

## 6｜Project Plane contract

Projects remain under `P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`.

The Master never uses L0–L7 identity as Project identity and never uses project state as Knowledge maturity.

Each runtime decision is bound to at least:

`project_id / optional workstream_id / decision_object_id / authority_snapshot_ref / knowledge_snapshot_ref`.

## 7｜Design Intelligence trigger

Every material design Candidate resolves a current `DESIGN_INTELLIGENCE_PACKET` before promotion-relevant production.

If that packet is missing, stale or blocked, the Master does not invent a design route. It returns the project to Design Intelligence resolution.

Design Intelligence determines:

- Design Question and intent;
- relevant current knowledge / evidence routes;
- review lenses;
- technical / evidence triggers;
- cross-disciplinary integration trigger;
- current claim ceiling.

## 8｜Cross-disciplinary integration trigger

Use `cross-disciplinary-design-integration-v1.0.md` when at least one material decision has consequential dependency across discipline owners, system owners or shared variables.

Trigger evidence includes:

- one decision materially changes two or more discipline outputs;
- one discipline consumes another's material output;
- a shared variable has multiple material consumers;
- an interface needs joint acceptance;
- local optimization can damage whole-system intent or experience;
- a material change propagates through several subsystem dependencies;
- the claim requires an integrated prototype / model / state flow / rehearsal / field readback.

No material coupling → Integration may be `NOT_REQUIRED`.  
Material coupling → an Integration Packet and current Integration Receipt become promotion dependencies.

## 9｜State propagation

The Master propagates **staleness and reopen requirements**, not design conclusions.

```text
Authority change
  → invalidate affected routing assumptions
  → refresh dependent packets / receipts

Material design-intent change
  → reopen affected discipline review
  → reopen affected interfaces
  → stale dependent integration conclusions

Shared-variable / interface change
  → propagate through dependency map
  → reopen acceptance contracts / joint decisions / artifacts / gates that consume it

Technical or evidence failure
  → lower affected claim ceiling
  → block dependent promotion claims

Integration failure
  → block whole-system integration claim
  → preserve still-valid local discipline evidence

Independent Design REVISE / REJECT
  → block Design KEEP / Promotion
  → preserve valid technical evidence rather than falsifying it
```

Propagation is dependency-scoped. A local change does not invalidate unrelated verified work.

## 10｜Canonical change-impact classes

Reuse the existing integration vocabulary:

- `NON_MATERIAL`
- `LOCAL_MATERIAL`
- `INTERFACE_MATERIAL`
- `COUPLED_SYSTEM`
- `PROMOTION_BREAKING`

Material changes require `propagation_state=APPLIED` before promotion readiness. `NON_MATERIAL` may be `NOT_REQUIRED` when no downstream state consumes the change.

## 11｜Canonical review set

The Master records one explicit state for each review class without merging their meanings:

- `ARTIFACT`
- `TECHNICAL`
- `EVIDENCE`
- `DISCIPLINE`
- `DESIGN`
- `PERSISTENCE`

For a non-triggered review use `triggered=false / result=N_A / receipt_ref=null`.

For a triggered promotion-relevant review:

- Artifact / Technical / Evidence / Discipline / Persistence must resolve to the applicable `PASS` state;
- Design must resolve to `KEEP`;
- `NOT_RUN / FAIL / HOLD / REVISE / REJECT` remains open and cannot be averaged away;
- an executed result requires a traceable receipt/readback reference.

## 12｜Machine-readable Master Runtime state

The Master reuses the existing Control Plane orchestration schema rather than creating a second Project State database.

Canonical machine carrier:

`00-governance/control-plane/orchestration.schema.json` → `kind=MASTER_RUNTIME_STATE`.

Validator / evaluator:

`python 00-governance/control-plane/orchestrator.py master-runtime <STATE.json>`

Minimum machine state includes:

```text
schema_version = 0.3
master_runtime_version = 1.0
project_id / workstream_id / decision_object_id
authority_snapshot_ref
knowledge_snapshot_ref
design_intelligence packet + state + claim ceiling
integration trigger + packet + receipt + state + verdict + open interface/authority counts + claim ceiling
six review classes
dependency states
material change / propagation states
open blockers
promotion_requested
```

Machine outcomes:

- `BLOCKED` — invalid or contradictory runtime state;
- `IN_PROGRESS` — required review / packet / closure work remains;
- `RECONCILIATION_REQUIRED` — stale dependency, integration state, authority conflict or material change propagation must be reconciled;
- `RUNNABLE` — runtime state is coherent and no known prerequisite blocks continuation;
- `READY_FOR_HUMAN_DECISION` — promotion prerequisites are closed, but Promotion itself has **not** been awarded.

`READY_FOR_HUMAN_DECISION ≠ PROMOTED`.

## 13｜Runtime object identity envelope

Existing logical objects should converge on stable IDs and schema versions rather than spawning new namespaces:

- `DESIGN_INTELLIGENCE_PACKET`
- `CROSS_DISCIPLINARY_INTEGRATION_PACKET`
- `INTERFACE_REGISTER`
- `INTERFACE_ACCEPTANCE_CONTRACT`
- `JOINT_DECISION_RECORD`
- `CROSS_DISCIPLINARY_INTEGRATION_RECEIPT`
- `DESIGN_REVIEW_RECEIPT`

Shared envelope where applicable:

```text
object_id
schema_version
project_id / workstream_id / decision_object_id
authority_snapshot_ref
knowledge_snapshot_ref
source_revision
created_at / updated_at
owner
status
depends_on[]
stale_if[]
claim_ceiling
open_blockers[]
supersedes / superseded_by
readback_refs[]
```

The envelope does not require a new database when an existing Current project/runtime carrier can own the object.

## 14｜Promotion eligibility

Promotion eligibility requires all applicable conditions below:

1. Current Authority / Project / Source identity is resolved.
2. Design Intelligence Packet is current.
3. If integration is triggered, its packet and current receipt exist.
4. No in-claim `MAJOR / CRITICAL` interface remains open or blocked below required maturity.
5. No unresolved shared-variable / interface authority conflict remains.
6. No dependency consumed by the promoted claim is stale or requires reopen.
7. Every material change has propagated to affected downstream states.
8. All triggered Artifact / Technical / Evidence / Discipline / Persistence reviews meet their applicable PASS requirement.
9. Independent Design Review is `KEEP` for the intended claim.
10. No open blocker contradicts the promotion claim.
11. The intended promotion does not exceed the lowest applicable claim ceiling.
12. The machine evaluator returns `READY_FOR_HUMAN_DECISION` and the actual authorized human/authority transition still occurs separately.

## 15｜G9 re-entry

G9 is a bounded learning return, not automatic knowledge promotion.

Candidate reusable learning should preserve:

`observed project condition → failure/success pattern → causal hypothesis → repair → retest → transfer boundary → reusable candidate rule`.

Only validated transferable learning may revise an existing L4/L5 owner or enter the existing Candidate knowledge/skill process.

Project-specific dimensions, client facts, one-off field conditions and unresolved causal stories remain Project / Evidence / Provenance.

## 16｜Module map

| Concern | Current owner |
|---|---|
| Root authority / namespace | `00-governance/README.md` + Current root authority |
| Master cross-module orchestration | **this file** |
| Canonical project execution flow | `oleander-project-flow-v0.3.md` |
| Design intelligence / review routing | `design-intelligence-routing-and-review-v1.0.md` |
| Cross-disciplinary integration | `cross-disciplinary-design-integration-v1.0.md` |
| Control Card / machine orchestration | `00-governance/control-plane/` |
| Artifact review | `artifact-review-system-v1.0.md` + current extensions |
| Post-generation review | `post-generation-review-gate.md` |
| Production binary persistence | `production-asset-persistence-gate-v1.0.md` |
| Execution owner / capability routing | `00-governance/runtime/` + Skill Resolver |
| Reusable knowledge | current L0–L7 Knowledge Plane |

## 17｜Non-substitution invariants

`KNOWLEDGE RETRIEVAL ≠ PROJECT AUTHORITY`  
`ARTIFACT EXISTS ≠ DESIGN QUALITY`  
`DISCIPLINE PASS ≠ INTEGRATION PASS`  
`MODEL FEDERATION ≠ DESIGN COHERENCE`  
`CLASH-FREE ≠ EXPERIENCE-COHERENT`  
`TECHNICAL COORDINATION ≠ DESIGN SYNTHESIS`  
`TECHNICAL PASS ≠ DESIGN KEEP`  
`INTEGRATION PASS ≠ DESIGN KEEP`  
`RECEIPT COMPLETE ≠ WHOLE-SYSTEM EXCELLENCE`  
`PROTOTYPE PASS ≠ FIELD PASS`  
`G9 RECORD ≠ REUSABLE KNOWLEDGE`  
`READY_FOR_HUMAN_DECISION ≠ PROMOTED`

## 18｜Current execution formula

**Resolve Authority → Route Current Knowledge → Compile Design Intelligence → Resolve Integration Trigger → Execute / Prototype → Close Triggered Reviews → Read Back Integration → Independent Whole-System Design Decision → Persist when required → Human Promotion Decision → Deliver / Observe → G9 bounded re-entry.**

