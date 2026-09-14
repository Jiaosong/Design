# OLEANDER G9 Knowledge Distillation & Admission Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P9**. Applies to transfer from `PROJECT` / `RUNTIME_CONTROL` into the `KNOWLEDGE` plane. It binds to the Object Plane Architecture, Knowledge Classification Contract v1.1 draft and Professional Knowledge Content & Research Standard v1.0.

## 1. Purpose

Project work produces many facts, artifacts, failures, receipts and local decisions. Only a subset deserves promotion into reusable Knowledge.

Core rule:

`PROJECT SUCCESS ≠ REUSABLE KNOWLEDGE`.

`PROJECT FAILURE ≠ REUSABLE KNOWLEDGE`.

Reusable Knowledge exists only after the project-specific event is converted into a bounded, evidence-linked, reusable statement/method/case/practice with explicit transfer boundaries.

## 2. G9 is an admission route, not automatic promotion

`G9_REUSE_CANDIDATE` remains a `RUNTIME_CONTROL` object until Knowledge admission succeeds.

Flow:

`PROJECT / RUNTIME EVIDENCE → G9_REUSE_CANDIDATE → DEPROJECT → CLAIM–EVIDENCE REVIEW → COUNTEREXAMPLE / BOUNDARY → KNOWLEDGE CLASSIFICATION → CONTENT / RESEARCH GATES → CANDIDATE KNOWLEDGE → EXPLICIT PROMOTION`.

No project/runtime object changes plane merely because it has been reused once.

## 3. G9 trigger

Create a G9 candidate when one or more apply:

- a repair rule prevented a recurring material failure;
- a method/sequence reliably improved an outcome under known conditions;
- a project discovered a cross-disciplinary interface pattern that may recur;
- a benchmark/research synthesis changed project decisions and has reusable reasoning;
- a design technique produced a bounded improvement verified through actual readback;
- a failure revealed a transferable anti-pattern/root cause;
- a technical/evidence method produced reusable procedure/acceptance logic;
- a case is valuable as a bounded comparative precedent, including negative evidence;
- a new relation/claim materially extends an existing Knowledge object.

Do not create G9 candidates merely because a task completed.

## 4. G9 candidate minimum envelope

```yaml
g9_id:
schema_version:
object_plane: RUNTIME_CONTROL
project_id:
workstream_ids: []
decision_object_refs: []
source_project_objects: []
source_evidence_refs: []
source_receipt_refs: []
candidate_learning:
learning_type:
why_transferable:
known_scope:
known_failure_conditions: []
counterexamples: []
project_specific_elements_to_strip: []
provenance_to_preserve: []
possible_existing_knowledge_owner_refs: []
proposed_knowledge_role:
proposed_level:
claim_ceiling_ref:
owner:
status:
```

## 5. G9 candidate states

`CAPTURED → DEPROJECTING → EVIDENCE_BOUND → CLASSIFICATION_READY → CONTENT_REVIEW → CANDIDATE_KNOWLEDGE → PROMOTED | REJECTED | MERGED_INTO_EXISTING`.

Meanings:

- `CAPTURED` — potential reusable learning identified;
- `DEPROJECTING` — separating reusable rule from project-specific conditions;
- `EVIDENCE_BOUND` — claims linked to supporting/contradicting/bounding evidence;
- `CLASSIFICATION_READY` — Object Plane/Role/Level/relations/scope can be assigned;
- `CONTENT_REVIEW` — R1/R2/K1–K5/B1/IR applicability being assessed;
- `CANDIDATE_KNOWLEDGE` — reusable object/patch exists but is not Current;
- `PROMOTED` — explicit Knowledge promotion complete;
- `MERGED_INTO_EXISTING` — learning absorbed into existing canonical owner;
- `REJECTED` — not reusable/credible enough; provenance retained.

## 6. Existing-owner-first admission

Before creating a new Knowledge object:

1. search Current Knowledge owner by subject/responsibility;
2. inspect current full body;
3. determine whether the learning is:
   - a claim/evidence addition;
   - a boundary/failure-condition addition;
   - a method step/decision-rule refinement;
   - a Practice/Case child;
   - a genuinely new independent responsibility;
4. patch existing owner when possible;
5. create new identity only when atomic responsibility cannot fit without distortion.

`NEW LEARNING ≠ NEW PAGE`.

## 7. De-project operation

De-projecting does **not** mean deleting provenance.

Separate:

### Project-specific facts to strip from reusable body when not essential
- project IDs/workstream IDs;
- one-off coordinates/dimensions;
- local file paths;
- PR numbers/CI logs;
- sync timestamps;
- receipt IDs;
- temporary tool/runtime state;
- client/person-specific confidential facts;
- local naming that is not part of the reusable mechanism.

### Provenance to preserve outside/alongside the reusable body
- source project/case identity;
- source evidence;
- original configuration/context;
- date/version;
- actual test/readback conditions;
- producer/reviewer;
- negative/failed attempts;
- lineage/supersession.

## 8. Transfer statement

Every material G9 candidate should be expressible as:

`WHEN [conditions/context] → APPLY/EXPECT [mechanism/rule/method] → BECAUSE [evidence/reasoning] → DO NOT GENERALIZE BEYOND [boundary] → REVALIDATE WHEN [trigger]`.

If the candidate cannot state its conditions/boundary, it is not ready for reusable Knowledge promotion.

## 9. Evidence floor

A reusable claim must resolve to Project/External evidence appropriate to the claim.

Keep:
- supports;
- contradicts;
- bounds;
- uncertainty;
- source strength;
- confidence;
- does-not-establish;
- configuration/context.

A successful single case may support a Practice or bounded Case without establishing a universal Theory/Method claim.

## 10. Counterexample requirement

For consequential generalization, actively ask:

- where did the rule fail?
- what materially different context might reverse it?
- what alternative mechanism explains the result?
- which variable was project-specific?
- what evidence would falsify the transfer rule?

No counterexample search is required for trivial documentation facts, but it is expected before broad Method/Theory/Framework claims.

## 11. Knowledge Plane routing

After de-project/evidence binding, resolve exactly one primary Object Plane = `KNOWLEDGE`, then apply the eight-axis contract:

`Object Plane × Subject Ownership × L0–L7 × Primary Knowledge Role × Framework Type [L4 only] × Typed Knowledge Relations × Knowledge State × Information Role`.

## 12. Level rules

Default reusable object = `L5 Knowledge Object`.

Use `L6` when primary responsibility is Source/Evidence/Case support.

Use `L7` for bounded Practice/Output/application evidence.

Use `L4` only after full admission:

`BREADTH + INTEGRATION + DELEGATION + BOUNDARY + REUSE`.

Long/important/cross-disciplinary/project-popular does not justify L4.

## 13. Primary Knowledge Role

Exactly one:

`INDEX | THEORY | METHOD | TOOL | SOURCE | EVIDENCE | CASE | PRACTICE`.

Do not create compound primary roles.

Secondary semantics use relations, Information Role, Framework Type or Application Mapping.

## 14. Human Knowledge Body contract

Canonical professional body should contain the applicable subset of:

1. Core Question;
2. Purpose;
3. Scope In / Scope Out;
4. Definitions / object of knowledge;
5. Core Claims;
6. Inputs / Preconditions;
7. Decision Logic / Mechanism;
8. Procedure / Method when applicable;
9. Outputs / Consequences;
10. Failure Conditions / Negative Evidence;
11. Evidence Basis;
12. Conditions / Uncertainty;
13. Limitations;
14. Applicability / Transfer Boundary;
15. Validation State;
16. Open Questions;
17. Related Knowledge.

The body is written for human professional understanding, not as an audit log.

## 15. Runtime/provenance separation

Do not pollute Human Knowledge Body with changing operational records such as:

- Notion page ID;
- latest GitHub commit;
- SHA256/digest;
- PR number;
- CI run;
- apply receipt;
- sync timestamp;
- D1 readback;
- migration batch;
- Current/Support migration history;
- runtime gate state.

Store these in:

`TECHNICAL_PROVENANCE | RUNTIME_METADATA | READBACK_HISTORY | LINEAGE`.

The body may link to provenance when needed but should not become the provenance ledger.

## 16. Claim as addressable knowledge unit

Long-term target:

`Knowledge Object → Claim → supported/bounded/contradicted by Evidence`.

Claim minimum:
- stable claim ID within object;
- bilingual claim text when formal bilingual body applies;
- claim type;
- evidence links;
- conditions;
- confidence;
- uncertainty;
- does-not-establish;
- validation state;
- last verified;
- supersession lineage.

Citation count at page level is not a substitute for claim-level support.

## 17. Content / Research gate admission

Apply when semantically relevant:

`R1 Research Conduct → R2 Study-Type Reporting → K1 Content → K2 Object → K3 Graph Semantics → K4 Metadata/Provenance/Retrieval → K5 Lifecycle/Reuse/Staleness → B1 Bilingual Semantic Parity → Independent Review`.

Rules:
- gates remain independent;
- R2 PASS never grants R1 PASS;
- Structure PASS never grants Content PASS;
- valid graph classification never grants professional research/content quality;
- UNKNOWN / VALIDATION OPEN / HOLD are allowed;
- do not fabricate certainty to complete migration.

## 18. Bilingual body

Formal bilingual content should preserve same-level semantics:

`Same Claim / Same Evidence / Same Confidence / Same Boundary / Same Status / Same Numbers / Same Units / Same Version`.

An English abstract does not make a Chinese professional body bilingual-complete.

## 19. Knowledge State separation

Display separately:

- Taxonomy / Level + Role;
- Authority/Retrieval: CURRENT / SUPPORT / PROVENANCE / EXCLUDED;
- Governance;
- Evidence;
- Trust;
- Freshness;
- Content;
- Research R1/R2;
- Bilingual;
- Graph state.

Forbidden inferences:

- `CURRENT → TRUSTED`;
- `L4 → MATURE`;
- `VERIFIED → HIGHER TAXONOMY LEVEL`;
- `USED BY MANY PROJECTS → FRAMEWORK`.

## 20. Knowledge relation boundary

Knowledge graph relations include:

`REQUIRES_CONCEPT | EXTENDS | REFINES | CONTRASTS_WITH | IMPLEMENTS | CONSTRAINED_BY | SUPPORTS_CLAIM | CONTRADICTS_CLAIM | BOUNDS_CLAIM` plus structural/domain/application/lifecycle relations.

Do **not** import Project Runtime semantics such as:

`depends_on | stale_if | shared-variable propagation | reopen` as if they were Knowledge dependency relations.

## 21. Practice / Case admission

A bounded project application may remain valuable without becoming a universal Method.

Use:
- `CASE` when the main responsibility is “what happened in this context and why it matters”;
- `PRACTICE` when main responsibility is “how knowledge was actually applied/tested in bounded work”;
- `EVIDENCE` when main responsibility is a supporting/refuting observation/test/source.

Keep negative/failed cases when they improve transfer boundaries.

## 22. Knowledge promotion request

Minimum:

```yaml
knowledge_promotion_id:
g9_ref:
target_existing_object_or_new_candidate:
object_plane: KNOWLEDGE
classification:
claim_evidence_ledger_ref:
content_gate_results:
research_gate_results:
bilingual_state:
independent_review_ref:
provenance_ref:
open_limitations: []
requested_retrieval_state:
promotion_authority:
readback_refs: []
decision:
```

## 23. Promotion blockers

Block Current promotion when material:

- Object Plane unresolved;
- duplicate canonical owner unresolved;
- L4 admission incomplete;
- primary Role ambiguous;
- consequential Claim lacks evidence/ceiling;
- material contradiction unresolved/hidden;
- Human Knowledge Body still dominated by runtime/provenance logs;
- required R1/R2/K1–K5/B1/IR gate not passed/explicitly N/A;
- stale mutable evidence not revalidated;
- bilingual semantics materially diverge;
- independent review has unresolved Critical/Major objection.

## 24. Validator floor

- `G9-001` project completion cannot auto-create Knowledge object;
- `G9-002` candidate records source project/evidence/provenance;
- `G9-003` de-project removes local operational clutter without deleting provenance;
- `G9-004` reusable rule states scope/boundary/revalidation trigger;
- `G9-005` existing Knowledge owner checked before new object;
- `G9-006` single-case success cannot silently become universal Method/Theory;
- `KNCLS-001` exactly one primary Knowledge Role;
- `KNCLS-002` L5 default; L4 requires five-gate admission;
- `KNREL-001` Project runtime dependency semantics forbidden as Knowledge dependency substitute;
- `KNCNT-001` Human Knowledge Body separated from runtime/provenance/readback;
- `KNCNT-002` consequential Claims resolve to Claim–Evidence relations;
- `KNCNT-003` content/research/bilingual/graph/trust/freshness states remain separate;
- `PROM-001` Knowledge Current requires explicit applicable gates + authority + readback;
- `B1-001` bilingual formal body preserves semantic parity.

## 25. P9 closure condition

P9 is sufficiently refined for draft review when G9 candidate lifecycle, existing-owner-first, de-project/provenance split, transfer/counterexample/evidence logic, eight-axis classification, Human Knowledge Body, claim-level evidence and promotion gates all have machine-readable counterparts.
