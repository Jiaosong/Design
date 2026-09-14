# OLEANDER Evidence / Formal Assurance Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P6**. Applies to Project-plane Evidence and Assurance objects and clarifies the logical interpretation of current P4 Validation as `P4 Formal Assurance`. It does not rename existing registry fields yet and does not replace specialist professional approval.

## 1. Core separation

Use three separate Project objects:

1. `EVIDENCE_RECORD` — what was observed/measured/captured/derived under stated conditions;
2. `ASSURANCE_ACTIVITY` — the formal act of checking/validating/auditing/reviewing a target;
3. `ASSURANCE_DECISION` — the authorized disposition resulting from the activity.

Hard rule:

`DATA / OBSERVATION ≠ ASSURANCE ACTIVITY ≠ PASS/FAIL DECISION`.

A screenshot, measurement, simulation output or interview transcript does not become PASS simply by existing.

## 2. P4 logical interpretation

Maintain compatibility with current `P4 Validation` records, but require `assurance_type`:

`VERIFICATION | VALIDATION | CERTIFICATION | INDEPENDENT_REVIEW | AUDIT | ACCEPTANCE`.

Do not treat all P4 objects as “validation” in the semantic sense.

## 3. Assurance meanings

### VERIFICATION
Question:
`Does the specified object/configuration satisfy the specified Requirement/Specification?`

Primary target:
`REQUIREMENT / SPECIFICATION / ACCEPTANCE CRITERION`.

### VALIDATION
Question:
`Does the realized system/design satisfy the underlying Need/intended use/scenario?`

Primary target:
`NEED / INTENT / INTENDED_USE / SCENARIO`.

### CERTIFICATION
Question:
`Has an authorized certifying body/process determined compliance for its defined scope?`

Requires explicit certification authority. Automated checks cannot self-certify.

### INDEPENDENT_REVIEW
Question:
`Does an appropriately independent reviewer accept/reject/revise the object against defined review criteria?`

Independence must be recorded; producer self-review cannot impersonate it.

### AUDIT
Question:
`Are required records/processes/configurations/provenance consistent with the audit criteria?`

Audit PASS does not automatically prove design or field performance.

### ACCEPTANCE
Question:
`Does the authorized accepting party accept the object/deliverable/configuration for the stated scope?`

Acceptance may include commercial/project-governance criteria beyond technical Verification.

## 4. Evidence Record contract

Minimum fields:

```yaml
evidence_id:
project_id:
evidence_type:
question_or_target:
source_or_method:
source_object_ref:
configuration_ref:
setup_or_condition:
operator_or_agent:
instrument_or_software:
version:
date:
observation_or_data:
units:
uncertainty:
limitations: []
provenance_refs: []
supports: []
contradicts: []
bounds: []
evidence_strength:
confidence:
does_not_establish: []
repeatability_or_reproducibility:
valid_until_or_revalidation_trigger:
status:
```

## 5. Evidence types

Controlled high-level set:

`DOCUMENTARY_SOURCE | FIELD_OBSERVATION | FIELD_MEASUREMENT | LAB_TEST | PROTOTYPE_TEST | USER_RESEARCH | OPERATIONAL_DATA | SIMULATION | MODEL_ANALYSIS | GEOMETRY_READBACK | MACHINE_CHECK | VISUAL_READBACK | MATERIAL_SAMPLE | MANUFACTURER_DATA | PRECEDENT_CASE | REGULATORY_RECORD | EXPERT_REVIEW | OTHER_CONTROLLED`.

Evidence type does not determine strength automatically.

## 6. Evidence status

`CAPTURED → CHECKED → ACCEPTED_FOR_USE | REJECTED → STALE | SUPERSEDED`.

Meaning:

- `CAPTURED` — evidence exists, provenance/quality not yet checked;
- `CHECKED` — source/method/configuration reviewed;
- `ACCEPTED_FOR_USE` — admissible for specified claim/question;
- `REJECTED` — invalid/unusable for intended claim;
- `STALE` — once valid but no longer valid for Current claim/configuration/time;
- `SUPERSEDED` — newer evidence intentionally replaces it for a defined role.

Rejected evidence remains in lineage when consequential.

## 7. Evidence strength and confidence

Keep separate.

### Evidence strength
How directly and robustly the evidence bears on the claim/question.

Use:
`CONTEXTUAL | INDIRECT | DIRECT_BOUNDED | STRONG_DIRECT | ASSURANCE_GRADE_FOR_SCOPE`.

### Confidence
Current confidence in interpretation/application.

Use:
`LOW | MODERATE | HIGH | OPEN`.

Multiple weak sources do not automatically create strong evidence.

## 8. Evidence applicability

Before use, check:

- target object identity;
- configuration/version;
- conditions/environment;
- population/user/site/material relevance;
- method validity;
- uncertainty/error;
- date/freshness;
- contradiction/bounds;
- claim type and claim ceiling.

Evidence accepted for one claim may be invalid for another.

## 9. `does_not_establish`

Consequential Evidence Records should explicitly state common overclaim boundaries when material.

Examples:
- simulation does not establish field performance;
- manufacturer data does not establish installed project performance;
- render does not establish construction feasibility;
- user preference does not establish universal need;
- precedent does not establish identical performance;
- one test condition does not establish untested states;
- code/geometry check does not establish lived experience.

## 10. Measurement uncertainty

For quantitative evidence where uncertainty matters, record the applicable subset of:

- instrument resolution/accuracy;
- calibration state;
- sampling method;
- repeat count;
- environmental conditions;
- operator method;
- data processing/transformation;
- tolerance/acceptance boundary;
- known systematic/random error.

Do not fabricate precision beyond the evidence.

## 11. Assurance Activity contract

```yaml
assurance_activity_id:
project_id:
assurance_type:
target_objects: []
target_requirements_or_needs: []
question:
method:
procedure_ref:
conditions:
configuration_under_test:
acceptance_criteria: []
executor:
reviewer_or_authority:
independence_state:
planned_evidence_outputs: []
actual_evidence_outputs: []
limitations: []
result_per_target: []
status:
reopen_triggers: []
```

## 12. Assurance Activity state

`PLANNED → READY → EXECUTED → ANALYZED → PASS | FAIL | INCONCLUSIVE → CLOSED | REOPENED`.

Rules:

- `PLANNED` is not evidence;
- `EXECUTED` means the procedure ran, not that the result passed;
- `ANALYZED` means results have been interpreted against criteria;
- `PASS/FAIL/INCONCLUSIVE` must be recorded per target when multiple targets exist;
- `CLOSED` requires evidence/result/decision lineage and reopen rule;
- failed/inconclusive run is retained, not rewritten.

## 13. Readiness gate

An Assurance Activity cannot become `READY` until applicable items are resolved:

- exact target identity/version/configuration;
- assurance question;
- method/procedure;
- acceptance criteria;
- conditions/environment;
- required instruments/software/data;
- operator/executor;
- authority/reviewer;
- evidence outputs;
- safety/rights/privacy prerequisites;
- known open assumptions that affect interpretation.

## 14. Verification-specific contract

A Verification Activity requires:

- at least one Requirement/specification target;
- Current requirement version;
- exact object/configuration under test;
- method and acceptance criteria;
- per-target result;
- accepted evidence.

`VERIFICATION PASS` cannot exist without a target Requirement/specification.

## 15. Validation-specific contract

A Validation Activity requires:

- at least one Need/Intent/Intended Use/Scenario target;
- representative context or an explicit limitation if not representative;
- success criteria tied to intended use/outcome;
- evidence that addresses the system as used/experienced, not just requirement compliance.

`VALIDATION PASS` cannot be inferred solely from Verification PASS.

## 16. Certification / professional approval boundary

Only an explicitly authorized external/internal professional/certifying authority may grant a state requiring that authority.

OLEANDER may prepare evidence, checklists and preflight, but must record:

`PROFESSIONAL_SIGNOFF = OPEN` until actual authorized acceptance exists.

## 17. Assurance Decision contract

`ASSURANCE_DECISION` captures the formal disposition after activity/evidence review.

Minimum fields:

```yaml
assurance_decision_id:
project_id:
assurance_activity_ref:
target_objects: []
target_claims_or_requirements: []
evidence_refs: []
result_summary:
per_target_disposition: []
accepted_limitations: []
claim_ceiling_granted:
open_items: []
retest_requirements: []
decision_authority:
independent_review_ref:
status:
decided_at:
reopen_triggers: []
```

State:

`DRAFT → ISSUED → ACCEPTED → REOPENED | SUPERSEDED | WITHDRAWN`.

## 18. Decision vocabulary

For formal project assurance use explicit dispositions as applicable:

`PASS | FAIL | INCONCLUSIVE | REVISE | REJECT | HOLD | OPEN | ACCEPTED_WITH_LIMITATIONS`.

Do not force every assurance type into PASS/FAIL if the formal decision is a bounded acceptance/review judgment.

## 19. Per-target result rule

If one Assurance Activity covers multiple Requirements/Claims/objects, record disposition per target.

Example:

`REQ-01 PASS`
`REQ-02 FAIL`
`REQ-03 INCONCLUSIVE`

Do not publish one global PASS that hides failed subtargets.

## 20. Evidence chain

Preferred chain:

`Question/Requirement/Need → Assurance Activity → Evidence Records → Analysis → Assurance Decision → Project Decision/Promotion`.

Evidence may also exist without formal assurance, but promotion must state how it was reviewed/admitted.

## 21. Field / simulation / prototype boundary

Keep contexts explicit:

- `SIMULATION` — computational/model-based predicted behavior;
- `PROTOTYPE_TEST` — behavior of a bounded prototype/configuration;
- `FIELD_OBSERVATION` — observed real-site/use condition;
- `FIELD_MEASUREMENT` — measured real-site/use condition;
- `OPERATIONAL_DATA` — in-use operation over stated period/context.

No automatic promotion across these contexts.

## 22. Visual and design evidence

Actual rendered/readback evidence is required for visual/design claims.

But:
- screenshot count is not quality;
- pixel existence is not Project Design KEEP;
- visual review cannot silently alter source geometry/data;
- design-quality KEEP must come from the applicable Project/Independent design-review authority.

## 23. Evidence contradiction

When accepted evidence conflicts:

- retain both records;
- verify identity/configuration/conditions;
- classify contradiction as true contradiction vs scope/configuration mismatch;
- lower claim ceiling or reopen assurance when material;
- do not delete inconvenient evidence;
- create a Decision/Research action when resolution is consequential.

## 24. Freshness / expiry

Evidence may become stale due to:

- configuration change;
- standard/regulation/product revision;
- calibration expiry;
- time-sensitive site/user/market condition;
- new contradictory evidence;
- method/software/model version change;
- changed scope/population/context.

Mutable evidence needs a revalidation trigger/date where applicable.

## 25. G9 / Knowledge transfer

Project assurance evidence does not automatically become Knowledge-plane Evidence.

Transfer route:

`Project Evidence/Assurance → G9 candidate → deproject/generalize → Claim–Evidence review → Knowledge classification → Content/Research gates → Knowledge promotion`.

Keep project-specific setup/configuration intact in provenance.

## 26. Failure modes

Fail/HOLD when:

- evidence lacks source/method/configuration/condition;
- activity marked PASS before analysis/criteria;
- one global PASS hides per-target FAIL/INCONCLUSIVE;
- Verification has no Requirement target;
- Validation has no Need/Intent/Scenario target;
- Verification is used as sole proof of Validation;
- professional/certification approval is synthesized from automation;
- simulation/prototype evidence is promoted to field proof;
- rejected/stale evidence remains supporting Current claim;
- contradictory evidence is removed rather than resolved/bounded;
- evidence precision exceeds method/instrument support;
- activity configuration differs from promoted object without applicability proof.

## 27. Validator floor

- `EVD-001` Evidence has source/method + condition + configuration + provenance;
- `EVD-002` evidence strength separate from confidence;
- `EVD-003` quantitative precision cannot exceed recorded uncertainty basis;
- `EVD-004` stale/rejected evidence cannot support Current promotion;
- `EVD-005` consequential evidence records `does_not_establish` when overclaim risk is material;
- `ASR-001` Assurance Activity target/question/method/criteria/configuration explicit before READY;
- `ASR-002` EXECUTED cannot imply PASS;
- `ASR-003` multi-target activity records per-target result;
- `VER-001` Verification resolves to Requirement/specification target;
- `VER-002` Verification PASS requires accepted evidence for Current configuration;
- `VAL-001` Validation resolves to Need/Intent/Intended Use/Scenario;
- `VAL-002` Validation not inferred solely from Verification;
- `CERT-001` certification/professional acceptance requires real authorized authority;
- `DEC-001` Assurance Decision binds activity + evidence + authority + ceiling;
- `CONTRA-001` material contradictory evidence retained and reopens/lowers ceiling as required;
- `FIELD-001` field claim requires field/operational evidence context;
- `G9-001` project assurance cannot bypass Knowledge distillation/content gates.

## 28. P6 closure condition

P6 is sufficiently refined for draft review when Evidence Record, Assurance Activity and Assurance Decision are separate; Verification/Validation/Certification/Review/Audit/Acceptance semantics are explicit; per-target results, evidence applicability/uncertainty/contradiction/freshness and claim-ceiling boundaries have machine-readable counterparts.
