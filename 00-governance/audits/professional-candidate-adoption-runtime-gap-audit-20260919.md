# OLEANDER Professional Candidate Adoption Runtime Gap Audit — 2026-09-19 / r5

## 1. Scope, authority and latest baseline

This audit is bound to:

- branch: `candidate/professional-stage-skill-composition-20260919-r5`;
- frozen comparison baseline: `origin/main@451accfa81216c3f5b094cb94cd4d50462767ce8`;
- target class: `PROFESSIONAL_PROCESS_DEFINITIONS`;
- Current authority invariant: Candidate evaluation may not mutate, impersonate or silently replace Current professional-process authority.

This r5 audit supersedes the earlier r2 audit conclusions where later Current evidence or independent review proved them too optimistic. The older records remain provenance; they are not silently rewritten into evidence they did not contain.

The major baseline changes between r2 and r5 are material:

1. `origin/main` advanced from `3110c53a...` through multiple governance/evidence merges to `be280aa1...`;
2. main gained stronger real C04 Systems Engineering requirement/V&V adoption evidence;
3. main later gained real C01 Interior and C04 Lighting project HOLD exercises; r5 consumes those real-project sources through the current Candidate revision without upgrading their HOLD/adoption ceiling;
4. independent read-only mechanism review found Current-authority mutation, Candidate-owner callability, pre-release successor-receipt, fake DAG/handoff and EV-state-prerequisite risks in the r2 candidate.

Those findings are treated as blocking corrections, not editorial comments.

## 2. Current / Candidate authority correction

### 2.1 Current Architecture / Structural / MEP machines are no longer mutated in place

The r2 candidate directly inserted `stage_execution_requirements` into already-Current Architecture, Structural and MEP machine definitions. Independent review correctly identified that as a Current-authority violation.

r5 restores these three machine files to Current main content with no routing-metadata mutation:

- `architecture-design-development-process.v1.json` — 18 stages;
- `structural-engineering-design-process.v1.json` — 9 stages;
- `building-services-mep-design-process.v1.json` — 9 stages.

Their 36 stages receive execution-composition semantics through:

`00-governance/runtime/OLEANDER_PROFESSIONAL_STAGE_EXECUTION_PROJECTION_v0.1.json`

This carrier is explicitly:

`NON_AUTHORITY_RUNTIME_COMPATIBILITY_PROJECTION`.

For every bound Current process it records exact machine path, Git blob and SHA256. It becomes stale if the Current machine changes. It owns execution routing only; it cannot modify professional-process semantics, award Professional PASS, award Design KEEP or mutate a Current process pointer.

### 2.2 Five OPEN Candidate machines carry stage execution requirements directly

The five OPEN Candidate domains remain Candidate and may carry additive stage execution semantics in their Candidate machine definitions:

| Domain | Candidate stages |
|---|---:|
| Interior Design | 8 |
| Landscape Architecture | 8 |
| Lighting Design | 10 |
| Digital Product / HCD | 8 |
| Systems Engineering | 9 |
| **Total** | **43** |

Therefore runtime composition coverage is:

`43 Candidate direct stages + 36 Current exact-revision projected stages = 79 / 79 stages`.

This is intentionally **not** the same claim as “79 Current machines were modified.”

## 3. Stage-specific capability / Skill composition

### 3.0 Canonical Professional Stage spine

The runtime, Contract, Architecture Map, Execution Receipt binding and Chat/CoS adapter now use one canonical top-level professional-stage order:

```text
Stage
→ Professional Question / Decision Object
→ Knowledge Inputs
→ Operational Knowledge Mount
→ Required Capability Roles
→ Current Execution Owners / Skills
→ Native Outputs
→ Actual Readback
→ Independent Review
→ Stage Closure
```

`Claim`, DD responsibility, interfaces, Tool/Adapter, visual-source checks, DAG/handoff internals, specialist/statutory boundaries and regression are subordinate bindings within these ten nodes. They do not create extra top-level Professional Stage steps.

Adapter regression now includes:

- `PROF-STAGE-009-CANONICAL-CHAIN-ORDER-EXACT` — machine readback order must equal the ten-step chain exactly;
- `PROF-STAGE-010-INDEPENDENT-REVIEW-BLOCKS-CLOSURE` — Native Output/Readback evidence without Independent Review remains HOLD;
- `PROF-STAGE-011-READBACK-AND-INDEPENDENT-REVIEW-ALLOW-CLOSURE` — decision-object-bound required native outputs must be `READBACK_COMPLETE`, Actual Readback must exist, Independent Review must PASS with a distinct reviewer, and exit conditions must be `SATISFIED` before Stage Closure PASS.

The professional stage still declares capability semantics, not Skill IDs:

- `required_capability_roles[]`;
- `supporting_capability_roles[]`;
- `multi_skill_required_when[]`;
- `single_owner_allowed_when[]`;
- `owner_set_recompute_triggers[]`;
- `forbidden_substitutions[]`;
- `composition_readback_requirements[]`.

Current runtime coverage is:

- 79 professional stages;
- 308 unique required/supporting capability-role labels;
- 0 current roles using the unnamed fallback route.

The governing invariant is:

`MINIMUM SUFFICIENT OWNER SET != MINIMUM SKILL COUNT`.

The minimum set is the smallest legal owner set that still covers every active material capability, native output, readback, authority boundary and triggered review.

### 3.1 Owner-set recomputation

Recompute is required when professional stage, decision object/claim, required native output/readback, interface maturity, owner/tool availability, release condition or actual readback materially changes.

Prior-stage owners are not sticky by default. Unaffected verified outputs may be reused; only affected capability/output bindings reopen unless dependency analysis proves wider staleness.

### 3.2 Candidate Skill / Candidate Body boundary

r2 incorrectly allowed Candidate UI Skill identities to appear in a “resolved owner set” as if Candidate status plus implementation paths were enough to execute.

r5 closes that gap:

- `CANDIDATE_OWNER` is a capability match / bounded evaluation suggestion, not Current callable execution authority;
- `CANDIDATE_BODY` is likewise non-Current;
- either result remains HOLD unless an explicit legal Current project/specialist binding owns that role;
- a Candidate Skill does not become installed merely because a Candidate professional process needs that capability.

This matters directly to HCD-DP3/D4: candidate UI visual/interaction owners no longer satisfy Current owner coverage.

## 4. Professional-stage Knowledge Mount runtime gate

All 79 professional stages already declare both:

- `knowledge_inputs[]`;
- `knowledge_mount_requirement`.

All eight process definitions also bind the existing Knowledge Integrity / Operational Mount owner. The remaining gap was runtime enforcement: a Chat/CoS professional-stage preflight could previously resolve Skills without proving that consequential knowledge had actually been admitted for the task/claim.

r5 wires this into `oleander_chat_resolver_adapter.py`.

For each active stage, declared knowledge inputs are active by default. Any omitted declared input requires explicit N/A / not-triggered reasoning.

Every task/claim mount record used for consequential execution must preserve:

- `knowledge_ref`;
- `use_role`;
- `operational_eligibility`;
- `eligibility_scope`;
- `claim_ceiling`;
- `applicability`;
- `conditions[]`;
- `unresolved_items[]`;
- `freshness_state`;
- `freshness_or_revalidation_trigger`;
- `does_not_prove[]`;
- `review_basis`;
- `satisfies_knowledge_inputs[]`.

The stage fails closed when:

- an active knowledge input has no usable mount;
- the mount is OE1 / not eligible;
- freshness is stale, unknown or requires revalidation;
- mount scope does not cover the active declared input;
- a declared input is omitted without an explicit reason.

Accepted runtime eligibility/freshness does not prove Design KEEP or Professional PASS.

Adapter regression now proves:

- Current Architecture ADD-00 can PASS the execution preflight through exact-revision Current projection + valid OE3 Current Knowledge Mounts + installed owners;
- the same stage HOLDs when a mounted knowledge object requires revalidation;
- the same stage HOLDs when active knowledge inputs have no mount;
- Candidate HCD stages HOLD on Candidate UI owners rather than treating them as Current callable.

## 5. Multi-Skill DAG and typed handoff truth boundary

The runtime may determine that a stage **requires** a Multi-Skill DAG. That determination alone is not a DAG artifact.

r2 records used exercise JSON paths as `multi_skill_dag_ref_or_single_owner_justification` and `typed_handoff_refs` without actual DAG/handoff artifacts. Independent review correctly identified this as false evidence.

r5 records therefore distinguish:

- `multi_skill_dag_required` — preflight requirement only;
- materialized DAG ref — actual runtime artifact, required before EV5 when multiple Current owners remain;
- typed-handoff refs — actual handoff artifacts, not prose or the exercise file itself.

Current OPEN Candidate records do **not** claim materialized DAG/handoff evidence where it does not exist. This remains an adoption blocker where applicable.

## 6. HOLD, release and receipt semantics

r2 generated files named `SUCCESSOR_RECEIPT` while the release condition was explicitly `UNSATISFIED`. That was semantically contradictory.

r5 separates the records:

### Before release

- bounded exercise/reapplication;
- `evaluation receipt`;
- continuation checkpoint;
- affected capability/output bindings;
- unaffected verified bindings;
- selective retest plan;
- `successor_receipt_ref = null`.

### Only after release

The release condition must first be read back as actually satisfied. Then the affected bindings are selectively retested. Only after the retest executes may a successor receipt bind that result.

No current OPEN Candidate record claims that this post-release event has happened.

## 7. Candidate Evolution state machine hardening

The Candidate contract already described EV3/EV4/EV5 prerequisites, but r2 did not make the state strings fail closed against those prerequisites.

r5 `validate_architecture_control_graph.py` now machine-enforces:

### EV3_EVAL_PASSED

Requires, at minimum:

- `evaluation.result = PASS`;
- authentic real-project exercise counted;
- current Candidate revision exercised;
- task/claim Knowledge Mount gate PASS;
- stage composition actual readback.

### EV4_INDEPENDENT_REVIEWED

Requires EV3 conditions plus:

- independent domain-professional reviewer identity;
- independence state `INDEPENDENT`;
- review bound to the exact Candidate machine revision;
- review verdict PASS.

### EV5_PROMOTION_READY

Requires EV4 conditions plus:

- actual release-condition satisfaction readback;
- actual post-release selective affected-binding retest;
- successor receipt bound to that retest;
- actual Multi-Skill DAG + typed-handoff refs where the resolved Current owner set is multi-owner;
- no remaining adoption blockers.

EV5 still does not equal Current. EV6 still requires an authorized human adoption decision plus Current pointer mutation/readback.

## 8. Current evidence by OPEN domain

All five remain `EVH_HOLD`.

### 8.1 Interior Design — real C01 project HOLD evidence + current-revision replay

Latest main now contains `05-cases/c01-yimai-guangdu/interior-professional-process-exercise/v0.1/`, explicitly classified as `REAL PROJECT BOUNDED REAPPLICATION / BLOCKED / HOLD / NOT_CURRENT / NO_PROMOTION` against the Baguting learning-room hypothesis.

r5 consumes that real-project source through the current Candidate revision in:

`05-cases/c01-yimai-guangdu/interior-professional-process-reapplication/v0.1/`

Current classification:

- `real_project_exercise_counted = true` for bounded current-revision project reapplication evidence;
- this is not Interior professional adoption or a verified room design;
- task/claim Interior Knowledge Mount remains HOLD;
- authoritative room/base-building geometry, appointment/scope, required native Interior outputs/readback and independent Interior review remain open.

The earlier context-only classification is retained only as provenance in the comparison record; it is superseded by the new main real-project HOLD exercise plus current-revision replay.

### 8.2 Landscape Architecture — real C04 project HOLD evidence

The historical v0.1 C04 Landscape exercise remains provenance and binds its predecessor Candidate revision.

r5 adds a current-revision bounded reapplication in:

`05-cases/c04-qingjiang-stone-book/landscape-professional-process-exercise/v0.2/`

It is counted as real project context because it exercises the Candidate against actual C04 Landscape/site evidence, but remains HOLD because:

- task/claim Landscape Knowledge Mounts are not closed;
- `FIELD_OBSERVED=0 / FIELD_MEASURED=0 / G1F HOLD` remains controlling for site truth;
- independent Landscape professional review is NOT_RUN;
- no post-release selective retest has occurred.

### 8.3 Lighting Design — real C04 project HOLD evidence + current-revision replay

Latest main now contains `05-cases/c04-qingjiang-stone-book/lighting-professional-process-exercise/v0.1/`, explicitly classified as `REAL PROJECT BOUNDED REAPPLICATION / BLOCKED / HOLD / NOT_CURRENT / NO_PROMOTION` against the C04 P01 step-light concept.

r5 consumes that real-project source through the current Candidate revision in:

`05-cases/c04-qingjiang-stone-book/lighting-professional-process-reapplication/v0.1/`

Current classification:

- `real_project_exercise_counted = true` for bounded current-revision project reapplication evidence;
- no Lighting professional adoption, photometric/control/electrical/commissioning/field PASS is claimed;
- task/claim Lighting Knowledge Mount remains HOLD;
- specialist authority, required native Lighting outputs/readback and independent Lighting review remain open.

### 8.4 Digital Product / HCD — real C04 project HOLD evidence

r5 uses:

`05-cases/c04-qingjiang-stone-book/hcd-professional-process-exercise/v0.2/`

and preserves the v0.1 exercise as historical provenance only.

The current-revision preflight now exposes additional truthful blockers that r2 obscured:

- task/claim HCD Knowledge Mount gate HOLD;
- Candidate UI visual/interaction Skills are not Current callable owners;
- representative-user usability/accessibility evidence remains open;
- actual runtime/browser evidence remains bounded by the C04 project truth state;
- independent HCD review NOT_RUN;
- no real post-release selective retest or successor receipt.

No Multi-Skill DAG or typed handoff is claimed until a legal Current owner set actually exists and the graph is materialized.

### 8.5 Systems Engineering — reuse stronger main C04 V&V evidence

r5 does not replace the stronger main evidence:

`05-cases/c04-qingjiang-stone-book/systems-engineering-process-exercise/v0.1/`

including its real requirement/V&V trace and adoption receipt.

r5 only adds current Candidate revision composition/Knowledge replay in:

`05-cases/c04-qingjiang-stone-book/systems-engineering-process-exercise/v0.2/`

The current Candidate remains HOLD because task/claim Systems Engineering Knowledge Mounts and integrated validation/independent review are not closed. Main v0.1 evidence is reused rather than duplicated or weakened.

## 9. Cross-domain baseline-vs-candidate comparison

Machine evidence:

`00-governance/audits/professional-stage-skill-composition-baseline-candidate-comparison-20260919.json`

Current r5 comparison:

- baseline: 79 stages without stage-specific runtime composition closure in Chat/CoS;
- candidate: 43 OPEN Candidate stages directly carry execution requirements;
- 36 already-Current stages are covered by exact-revision non-authority runtime projection;
- total runtime composition coverage: 79/79;
- capability-role corpus: 308 unique roles / 0 unnamed fallback;
- real-project current-revision bounded reapplication counted: 5/5 OPEN domains — Interior, Landscape, Lighting, HCD, Systems;
- all five remain HOLD; real-project exercise count does not equal Professional PASS, Current adoption or Stage Closure;
- professional-stage task/claim Knowledge Mount gate: now active/fail-closed;
- Candidate Skill current callability: HOLD/non-Current;
- Current professional machine mutation for routing metadata: forbidden.

Local mechanism benchmark after the Knowledge Mount gate was added:

- case: Current Architecture ADD-00 exact-revision projection + valid OE3 Knowledge Mount + owner routing;
- warmup: 5;
- measured runs: 100;
- median: 4.360 ms;
- p95: 5.864 ms;
- max: 7.934 ms.

This is local Python/repository overhead only. It does not measure network retrieval, tool execution, connected-source latency, human review or real production duration.

## 10. Strict schema / CI correction

Earlier investigation found a real pre-existing Lighting strict-schema drift: live Lighting stage carriers used fields the shared strict schema did not admit, while CI could fall back to a weaker validator when `jsonschema` was absent.

r5 preserves the shared-schema repair and adds pinned `jsonschema==4.24.0` installation to the existing AI Governance workflow. This extends the existing validation path; it does not create another schema framework.

## 11. Current adoption blockers

Common blockers intentionally retained where applicable:

1. task/claim Knowledge Mount gate not closed on current Candidate revision;
2. release condition not satisfied;
3. no post-release selective affected-binding retest;
4. no successor receipt from such a retest;
5. required real Multi-Skill DAG / typed-handoff evidence not materialized where a multi-owner Current execution would apply;
6. independent domain-professional review NOT_RUN;
7. domain-specific field/user/specialist/validation evidence remains open as recorded by each Candidate;
8. Interior and Lighting now have real-project HOLD exercises and current-revision replays, but required domain-native outputs, Knowledge Mounts, specialist/appointment authority and independent review remain open;
9. the exact r5 mutation manifest must remain hash-consistent through final validation; any later file delta invalidates it and requires regeneration before the Candidate evidence is exact-revision complete.

## 12. Bounded verdict

Current r5 status:

`STAGE-SPECIFIC CAPABILITY ROUTING = IMPLEMENTED / 79-OF-79 RUNTIME COVERAGE`

`CURRENT PROFESSIONAL MACHINE AUTHORITY = PRESERVED / NO IN-PLACE ROUTING MUTATION`

`PROFESSIONAL-STAGE KNOWLEDGE MOUNT GATE = IMPLEMENTED / FAIL-CLOSED`

`CANDIDATE SKILL AS CURRENT CALLABLE OWNER = FORBIDDEN`

`PRE-RELEASE SUCCESSOR RECEIPT = FORBIDDEN`

`EV3 / EV4 / EV5 STATE PREREQUISITES = MACHINE-ENFORCED`

`PROFESSIONAL PROCESS ADOPTION = HOLD`

`EV5_PROMOTION_READY = NOT YET`

`EV6_CURRENT_ADOPTED = NO`

This audit does not prove Professional PASS, Design KEEP, field truth, user validation, engineering/statutory approval, project promotion or universal transferability.
