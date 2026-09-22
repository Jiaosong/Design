# OLEANDER Enterprise Orchestration Roadmap

Status: candidate roadmap. No Current architecture, owner or promotion state is changed by this file.

## A. EV2 - Federated truth-safe model

Implemented candidate scope:

- one envelope, eight modules: ERP / PLM / MES / BPM / QMS / MBSE / Knowledge Graph / Agent Runtime;
- module-to-Current-owner mapping;
- Project/Case namespace separation;
- Work Package remains derived coordination object, not P5;
- canonical Job State reuse;
- configuration/baseline/change projection;
- operation/readback projection with MES fail-closed completion;
- BPM process/handoff/exception projection;
- QMS NCR/CAPA/effectiveness semantics;
- MBSE requirement/interface/verification-vs-validation semantics;
- Knowledge Graph provenance with zero authority effect;
- Agent session/lease/action/side-effect/reconciliation semantics;
- typed digital thread with source-bound relations;
- explicit open-gap register;
- v0.3.1 separates projection freshness from enterprise readiness;
- v0.3.1 separates source-binding coverage from triggered-module coverage and exposes exact scope counts.

EV2 exit condition: structural/reference evaluation passes while real-case count remains zero and promotion remains ineligible.

## B. EV3 - Representative project projections

Run three materially different real sources:

1. **C01** - multi-workstream design + presentation/detail dependencies; focus ERP/BPM/PLM/QMS and owner routing.
2. **C04** - evidence -> design -> native artifact -> professional/technical review -> HOLD/no-promotion; focus MBSE/QMS/KG + project controls.
3. **Fallingwater / complex 3D** - capability/tool -> native artifact -> readback -> multi-output review; focus PLM/MES/Agent Runtime/QMS.

For every case:

`CURRENT SOURCE SET -> v0.3.1 projection -> source-by-source readback -> digital-thread trace queries -> contradiction scan -> rebuild test`

Required metrics:

- authority duplication = 0;
- invented authority objects = 0;
- state-family collapse = 0;
- untraceable digital-thread relation = 0;
- false Design KEEP / Professional PASS / Promotion = 0;
- MES complete without readback = 0;
- CAPA closed without effectiveness readback = 0;
- MBSE verification collapsed into validation = 0;
- agent uncertain side effect allowed to advance = 0;
- stale dependency missed = 0;
- projection freshness never reported as enterprise readiness;
- `module_source_binding_coverage` never displayed as triggered/completeness coverage;
- `module_scope_counts` sum to 8 and match module headers exactly;
- projection removal leaves Current behavior unchanged.

## C. EV4 - Independent strict review

Independent reviewers attack:

- architecture pollution / second system-of-record risk;
- ERP/PLM/MES/BPM/QMS/MBSE semantic leakage;
- source identity and authority transfer errors;
- process/status flattening;
- freshness/readiness confusion;
- source-binding/completeness confusion;
- physical-vs-digital execution confusion;
- quality-vs-professional approval confusion;
- verification-vs-validation confusion;
- graph provenance vs canonical truth confusion;
- agent authorization, lease, duplicate mutation and partial-side-effect recovery;
- real usefulness for planning/coordination, not only schema elegance.

Producer self-review cannot satisfy EV4.

## D. EV5 - Promotion-ready integration candidate

Only after EV3 + EV4:

- propose append-only bindings into existing Architecture Control Graph;
- expose read/query surfaces through existing Control Plane / Reader / dashboard;
- bind existing Runtime Layer Interface handoffs where justified;
- preserve Notion as canonical Knowledge authority;
- preserve Git/GitHub as governed version/persistence surfaces;
- preserve CoS/agents as execution transport under capability/authorization/checkpoint contracts;
- do not create R-L or a new project/knowledge database.

No new mutation path is enabled unless an existing Current owner already legally owns it.

## E. Post-adoption increments

After human adoption, add narrowly and measure usefulness:

- portfolio/program workload and blocker views;
- work-package/resource demand planning;
- PLM configuration/change trace dashboard;
- MES/native-execution readback view where actually triggered;
- BPM queue/handoff/exception view;
- QMS NCR/CAPA/effectiveness queue;
- MBSE requirement/interface/V&V trace queries;
- Knowledge Graph provenance and impact analysis;
- Agent Runtime session/lease/side-effect/recovery observability;
- bounded scheduler recommendations.

Recommendations never grant authority or promotion.

## F. Explicitly deferred candidates

Authoritative event sourcing, distributed transaction coordination, finance/accounting authority, generalized MES shop-floor control and autonomous agent mutation authority are not part of this candidate. Each would require separate authority and controlled-evolution treatment because they materially change Current contracts.
