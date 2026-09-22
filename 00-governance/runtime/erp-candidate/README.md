# OLEANDER Enterprise Orchestration Candidate v0.3.1

Status: **EV2 EVAL READY / NON-AUTHORITATIVE / READ-ONLY CANDIDATE**

This package tests a unified enterprise orchestration/read model across **ERP + PLM + MES + BPM + QMS + MBSE + Knowledge Graph + Agent Runtime** without creating a second OLEANDER architecture, a second project-state database, a universal state machine, a persistent event ledger, or a distributed transaction manager.

v0.3.1 is a semantic-clarity successor to v0.3. The v0.3 schema, fixture, receipt and manifest remain in this directory as provenance.

## 1. Position inside Current OLEANDER

The candidate is one **federated projection envelope** over existing Current authority:

`R-A Authority -> R-B Knowledge -> R-C/R-D/R-E/R-F Design + Professional execution -> R-G Capability -> R-H Native execution -> R-I Readback/Review -> R-J Persistence/Promotion -> R-K bounded learning`

It does **not** create R-L.

The eight modules are concerns/views, not authority layers:

| Module | Candidate responsibility | Existing controlling authority |
|---|---|---|
| ERP | demand, schedule, resource-demand, portfolio/project/work visibility | Project Axis, Project State, Capability owners |
| PLM | configuration item, revision, baseline, supersession, change impact | Native Artifact, Project Configuration/Change, Git/version carriers, domain owners |
| MES | native/physical operation execution + actual readback | R-H native execution, project/fabrication/installation/commissioning owner, R-I readback |
| BPM | process instance, handoff, waiting/blocker/exception | Master Runtime, Execution DAG, checkpoints, layer interfaces |
| QMS | quality plan, NCR, CAPA, inspection/review, effectiveness | review/specialist/closure owners |
| MBSE | requirement, system element, interface, allocation, V&V, configuration baseline | requirement/acceptance, integration, domain owners; Systems Engineering remains Candidate where applicable |
| Knowledge Graph | typed node/edge/provenance/query projection | Notion canonical Knowledge + Reader + integrity/OE + Git provenance |
| Agent Runtime | session, lease, action, tool, handoff, side effect, readback | Resolver, Capability, DAG, checkpoint, Tool Adapter, Observability/Recovery, authorized mutation owner |

## 2. Core invariants

1. **One architecture only.** Modules are projections inside one envelope.
2. **Canonical identity first.** No module may synthesize an authority-bearing project, knowledge, artifact, requirement or owner identity from another namespace.
3. **Orthogonal states stay orthogonal.** Job, Project, Knowledge integrity/OE, DQ, Professional, Review, Configuration, Quality, Process and Agent state are separate facets.
4. **Cross-module links do not transfer authority.** Every digital-thread relation is projection-only and source-bound.
5. **No hidden promotion.** JOB/AGENT SUCCEEDED, PLM RELEASED, MES COMPLETE, BPM COMPLETED, QMS PASS, or MBSE VERIFICATION PASS do not imply DESIGN KEEP, PROFESSIONAL PASS, VALIDATION PASS or PROJECT PROMOTION.
6. **No distributed transaction manager.** Partial side effects are observed and reconciled through existing owners; uncertain effects force HOLD.
7. **Readback before completion.** MES completion, authorized agent side effects, QMS effectiveness and MBSE PASS states require explicit readback/evidence.
8. **Projection is rebuildable.** Activity/provenance observations are non-authoritative and disposable.

## 3. v0.3.1 semantic repair

Two ambiguous v0.3 signals are retired from the active schema.

### Projection freshness is not enterprise readiness

v0.3 used `projection_state=CURRENT_PROJECTION`. That label could be misread as project or enterprise readiness. v0.3.1 separates it into:

- `projection_freshness_state`: whether this projection was rebuilt against the source material actually read (`SOURCE_READBACK_CURRENT`, `SOURCE_READBACK_STALE`, `SOURCE_READBACK_UNKNOWN`).
- `enterprise_readiness_state`: candidate coordination readiness only (`NOT_EVALUATED`, `PARTIAL`, `HOLD`, `READY_FOR_EVALUATION`).

A source-current projection may still be `PARTIAL` or `HOLD`. Neither field grants Current authority, Design KEEP, Professional PASS, acceptance, release or Promotion.

### Source binding is not module completeness

v0.3 used `module_source_coverage`. v0.3.1 replaces it with:

- `module_source_binding_coverage`: fraction of module headers with explicit `source_refs`; this is provenance coverage only.
- `module_triggered_coverage`: fraction of the eight modules whose `scope_state` is exactly `TRIGGERED`.
- `module_scope_counts`: exact counts for `TRIGGERED / PARTIAL / NOT_TRIGGERED / HOLD`.

The current Master Runtime reference projection therefore reports source-binding coverage `1.0`, triggered coverage `0.625`, and enterprise readiness `PARTIAL` rather than implying 100% enterprise completeness.

## 4. External reference patterns

The candidate borrows patterns, not authority:

- ISA-95 / IEC 62264: enterprise/business planning vs manufacturing operations/control separation and controlled information exchange.
- OMG BPMN 2.0.2: process-instance / activity / handoff / exception semantics.
- OMG SysML 2.0 + KerML + Systems Modeling API/Services: requirement/system/interface/V&V/configuration model discipline.
- W3C PROV-O / PROV: source-bound provenance/derived-from/attribution relations.

These references do not replace OLEANDER runtime layers, Project Axis, professional stages, Knowledge Architecture or promotion rules.

## 5. Active machine files

- `OLEANDER_ENTERPRISE_ORCHESTRATION_PROJECTION_v0.3.1.schema.json` - active envelope schema.
- `example_enterprise_projection_v0.3.1.json` - active rich cross-module fixture.
- `eval-output/example-master-runtime.enterprise.v0.3.1.json` - deterministic Master Runtime readback fixture.
- `OLEANDER_ENTERPRISE_MODULE_OWNER_MAPPING_v0.2.json` - module -> existing OLEANDER owner/layer/plane mapping.
- `OLEANDER_ENTERPRISE_REFERENCE_MODEL_v0.1.json` - external pattern register; non-authoritative.
- `OLEANDER_ENTERPRISE_CANDIDATE_GAP_REGISTER_v0.1.json` - explicit unresolved module gaps.
- `build_erp_projection.py` - conservative Master Runtime -> active projection builder.
- `validate_erp_candidate.py` - structural, authority, readiness and coverage validator.
- `OLEANDER_EVOLUTION_CANDIDATE_ERP_ORCHESTRATION_STAGE1_20260921.json` - controlled-evolution candidate record.
- `ERP_STAGE1_EVAL_RECEIPT_v0.3.1_20260922.json` - active structural/reference evaluation receipt.
- `ENTERPRISE_CANDIDATE_MANIFEST_v0.3.1.json` - active-file canonical hash manifest; self-excluded.

v0.1/v0.2/v0.3 schemas, fixtures, outputs and receipts remain retained as candidate provenance and are not the active model.

## 6. What the builder deliberately does not invent

A Master Runtime projection only materializes what the source actually supports.

- no finance/cost truth without a Current cost authority;
- no product BOM master without an existing configuration owner;
- no physical MES operation without actual execution source/readback;
- no requirement or validation result when source requirements/V&V are absent;
- no Agent session/action when runtime receipts are absent;
- no QMS CAPA without a real nonconformance/action/effectiveness chain;
- no Knowledge Graph lifecycle mutation.

Absent evidence is represented as `NOT_TRIGGERED`, `PARTIAL`, `HOLD`, empty source-bound arrays or unresolved digital-thread links, never fabricated completeness.

## 7. Stage-1 / EV2 acceptance

EV2 is limited to structural/reference evaluation. It requires:

- eight modules inside one envelope;
- schema + rich fixture validation;
- Master Runtime projection validation;
- Case Axis / Project Axis separation;
- zero authority duplication and zero state-family flattening;
- source-bound digital-thread relations;
- explicit partial-side-effect reconciliation;
- readiness derived from module scope/blockers/review state rather than manually asserted;
- source-binding coverage separated from triggered coverage;
- negative tests that block cross-system false closure/promotion;
- Current OLEANDER files remain unmodified solely for candidate evaluation.

EV3 remains blocked until representative **C01 + C04 + Fallingwater/3D** read-only projections run against real current sources and pass source-by-source contradiction/readback checks.

## 8. Promotion boundary

This package is not Current architecture. It does not enable a new write path. Future adoption must follow controlled evolution, independent review, human decision, exact-revision readback and append-only integration into existing Current carriers.

`ENTERPRISE VISIBILITY != ENTERPRISE AUTHORITY`
`DIGITAL THREAD != SYSTEM OF RECORD`
`SOURCE-CURRENT PROJECTION != ENTERPRISE READY`
`SOURCE BINDING COVERAGE != MODULE COMPLETENESS`
`PROCESS/EXECUTION COMPLETE != DESIGN/PROFESSIONAL/PROMOTION COMPLETE`
