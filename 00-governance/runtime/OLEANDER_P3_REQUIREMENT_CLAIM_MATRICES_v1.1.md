# OLEANDER P3 Requirement / Constraint / Project Claim Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P3 SECOND PASS**. Semantic owner remains `OLEANDER_NEED_REQUIREMENT_CONSTRAINT_CLAIM_CONTRACT_v1.0.*`.

## 1. Purpose

P3 second pass makes Need/Requirement/Constraint/Project Claim machine-distinguishable enough to prevent hidden requirements, unverifiable obligations, unauthorized constraint relaxation and overclaim.

Core trace:

`NEED / EXTERNAL MANDATE / PARENT REQUIREMENT / AUTHORIZED DECISION → REQUIREMENT → DESIGN REALIZATION → VERIFICATION → NEED / INTENDED-USE VALIDATION → PROJECT CLAIM`.

No carrier or presentation object may replace this trace.

---

## 2. Requirement Atomicity Matrix

A Requirement should be split when independent parts can legitimately receive different dispositions.

| Pattern | Atomic? | Action |
|---|---:|---|
| one subject + one primary obligation + one acceptance result | YES | keep one Requirement |
| `shall X and Y`, X/Y can pass independently | NO | split into two Requirements |
| one performance target with several inseparable conditions | CONDITIONAL | keep one if one verification result governs the whole condition set |
| requirement + rationale in same sentence | NO | separate rationale field |
| requirement + implementation solution | usually NO | move solution to Decision/Constraint unless authorized implementation is itself mandatory |
| requirement + waiver exception | NO | Requirement remains; exception becomes Waiver/Deviation relation |
| one Requirement references several interfaces but one end-to-end acceptance condition | CONDITIONAL | keep system Requirement + derive interface Requirements where ownership/verification differs |

Atomicity test:
- can one clause PASS while another FAILS?
- do clauses have different owners?
- do clauses require different verification methods?
- can one clause change without legitimately changing the other?

Any `YES` normally requires split.

---

## 3. Requirement Origin / Derivation Matrix

| Origin | Legal Requirement source relation | Required rationale |
|---|---|---|
| stakeholder/user Need | `DERIVED_FROM NEED` | explain translation from desired outcome to verifiable obligation |
| external law/code/contract | `DERIVED_FROM EXTERNAL_MANDATE` | applicability/jurisdiction/version locator |
| parent Requirement | `REFINES / DERIVED_FROM REQUIREMENT` | allocation/decomposition basis |
| authorized Project Decision | `DERIVED_FROM DECISION` | why decision legitimately imposes obligation |
| interface acceptance need | `DERIVED_FROM INTERFACE / PARENT REQUIREMENT` | side ownership + exchanged condition |
| design preference | not mandatory by itself | remain preference/Decision criterion unless authorized |
| precedent/reference | not mandatory by itself | can inform rationale, not source authority |
| AI suggestion | not mandatory | hypothesis/reference only until independently authorized |

A Requirement with no resolvable origin is `UNAUTHORIZED_REQUIREMENT` until resolved.

---

## 4. Requirement Quality / Baseline Admission Matrix

Before `BASELINED`, each consequential Requirement must pass:

| Gate | PASS condition | Fail disposition |
|---|---|---|
| `R-Q01 ATOMIC` | one primary obligation | SPLIT |
| `R-Q02 SUBJECT` | identifiable system/product/service/actor subject | REWRITE |
| `R-Q03 NECESSARY` | traceable authorized origin | HOLD/REJECT |
| `R-Q04 CONDITIONED` | relevant scenario/environment/load/state explicit | REWRITE |
| `R-Q05 UNAMBIGUOUS` | no undefined subjective/indefinite terms material to acceptance | REWRITE |
| `R-Q06 SOLUTION_BOUNDARY` | WHAT not hidden HOW unless authorized | RECLASSIFY/REWRITE |
| `R-Q07 FEASIBLE` | no known unresolved impossible conflict | HOLD / Risk / Conflict resolution |
| `R-Q08 ACCEPTANCE` | measurable/observable acceptance boundary | REWRITE |
| `R-Q09 VERIFICATION_ROUTE` | method + config + condition + result type + owner + evidence carrier | REWRITE |
| `R-Q10 CHANGE_AUTHORITY` | owner + change authority resolved | HOLD |
| `R-Q11 VERSION` | stable version/configuration identifiable | HOLD |
| `R-Q12 TRACEABILITY` | upstream + downstream trace slots resolvable | HOLD for consequential requirement |

Do not baseline merely because wording contains `shall`.

---

## 5. Acceptance Criteria Testability Matrix

| Acceptance criterion form | Testability | Example treatment |
|---|---|---|
| exact threshold/range with unit and condition | HIGH | direct measurement/analysis route |
| binary observable behavior under named scenario | HIGH | demonstration/test/inspection |
| bounded ordinal rubric with explicit anchors | MODERATE | reviewer/user test with inter-rater/decision rule |
| qualitative expert judgement with named criteria | MODERATE/LOW | independent review; cannot masquerade as measurement |
| adjective only (`intuitive`, `premium`, `robust`) | LOW | operationalize or keep as Need/Claim, not baselined Requirement |
| “as appropriate”, “sufficient”, “etc.” | INVALID where material | rewrite |
| acceptance depends on external standard | CONDITIONAL | version + clause/source locator + applicability needed |

If a qualitative Need matters but cannot yet be reduced without distortion, preserve the Need and define a validation route; do not fabricate a pseudo-precise Requirement.

---

## 6. Requirement Conflict Resolution Matrix

| Conflict class | Example | Required route | Forbidden route |
|---|---|---|---|
| `HARD_CONSTRAINT_CONFLICT` | code vs site/client lock | authority/applicability + waiver/deviation or HOLD | weighted average |
| `REQUIREMENT_REQUIREMENT_CONFLICT` | two baselined obligations mutually impossible | owner/authority decision + requirement change/versioning | silently violate one |
| `RESOURCE_TRADEOFF` | weight/cost/performance all valid | explicit Decision/Trade Study while requirements remain visible | rewrite requirement after the fact |
| `INTERFACE_CONFLICT` | two sides demand incompatible exchanged condition | Interface + joint decision + controlled variable authority | local discipline decides alone |
| `AMBIGUITY_CONFLICT` | wording allows incompatible interpretations | requirement clarification/validation | technical optimization before meaning resolved |
| `STALE_REQUIREMENT_CONFLICT` | old version still consumed downstream | supersession/staleness propagation | treat both as current |
| `NEED_REQUIREMENT_MISMATCH` | verified requirement no longer satisfies underlying need | requirement validation/revision | claim success from verification alone |

---

## 7. Waiver / Deviation Matrix

| Case | Waiver/Deviation legal? | Minimum fields |
|---|---:|---|
| external/contract requirement has authorized tailoring route | YES, scoped | target requirement/constraint, authority, rationale, risk/evidence, scope, expiry/review, compensating controls |
| project-owned requirement intentionally relaxed | YES through authorized Change/Decision; use Waiver/Deviation if traceability benefits | same minimum evidence/impact fields |
| safety/accessibility/regulatory requirement with no authorized exception | NO | HOLD / redesign / professional authority resolution |
| “we cannot meet it in time” | not sufficient | schedule pressure is rationale input, not authority |
| precedent did it differently | not sufficient | precedent cannot authorize variance |
| variance applies only one prototype/test | CONDITIONAL | explicit bounded scope; must not leak into production baseline |

Waiver/Deviation does not delete the original Requirement/Constraint. It creates a controlled exception relation.

---

## 8. Need Validation Matrix

A Need can be `VALIDATED_FOR_SCOPE` only when the project has evidence that the Need is correctly understood for a stated stakeholder/context, not merely because stakeholders mentioned it once.

Potential evidence:
- repeated stakeholder/user evidence with sampling/context boundary;
- operational workflow/ConOps confirmation;
- field observation/POE;
- authoritative project/client objective;
- scenario/use-case evaluation;
- contradiction/negative-case review.

Need validation must record:
`population/stakeholder + context + evidence + contradictions + applicability + remaining uncertainty`.

A user quote is evidence of one participant statement, not a universal Need by itself.

---

## 9. Project Claim Type × Minimum Evidence Matrix

| Project Claim type | Typical minimum evidence | Default ceiling caution |
|---|---|---|
| `FACTUAL_STATE` | Current authoritative source or accepted direct evidence | configuration/time bounded |
| `DESIGN_INTENT` | authorized Decision / design source | intention ≠ achieved performance |
| `COMPLIANCE` | applicable requirement/constraint trace + scoped professional/compliance review where required | automated checks alone insufficient |
| `PERFORMANCE_PREDICTION` | model/simulation/analysis with inputs/method/uncertainty | not field outcome |
| `TECHNICAL_FIT` | dimensional/technical verification under current configuration | not user/operational validation |
| `USER_EXPERIENCE` | bounded user/behavior/representative validation | render/expert opinion insufficient |
| `FIELD_CONDITION` | field observation/measurement | model/satellite/precedent cannot silently substitute |
| `OPERATIONAL_OUTCOME` | in-use/operational evidence | prototype may only predict |
| `VALUE_BENEFIT` | explicit benefit metric/decision frame + evidence | avoid marketing inference from preference |
| `RESEARCH_INTERPRETATION` | research evidence + method/boundary/contradiction | not Project fact unless applied/verified |
| `PRESENTATION_MESSAGE` | source-bound narrative argument | cannot raise upstream truth ceiling |

---

## 10. Claim Evidence-Relation Matrix

Every consequential Claim may have multiple typed evidence edges:

- `SUPPORTED_BY`
- `CONTRADICTED_BY`
- `BOUNDED_BY`

For each edge record:
`evidence_id + role(DIRECT/INDIRECT/CONTEXTUAL) + configuration + conditions + strength + confidence contribution + does_not_establish`.

Rules:
- contradiction is not a negative citation count; it must remain visible to the Claim reviewer;
- several dependent sources from the same origin do not become independent corroboration;
- confidence must consider evidence independence and applicability, not quantity alone;
- absence Claims must include actual search/inspection coverage.

---

## 11. Trace Coverage Matrix

For consequential Requirements, track four directions separately:

| Direction | Question |
|---|---|
| `UPSTREAM_ORIGIN` | Why does this Requirement exist? |
| `DOWNSTREAM_REALIZATION` | What design/system objects satisfy it? |
| `ASSURANCE` | How is this exact version/configuration verified? |
| `CHANGE_IMPACT` | What reopens if it changes? |

Trace completeness does not mean all relations must be one-to-one.

Root externally mandated Requirement may legitimately have no Need parent, but must retain Source Authority.

---

## 12. Requirement Version / Verification Carry-Forward Matrix

| Change | Old verification reusable? | Rule |
|---|---:|---|
| editorial wording only, semantics provably unchanged | CONDITIONAL | explicit equivalence review |
| acceptance threshold changed | NO | re-verification required |
| condition/environment changed | NO for affected scope | re-verification under new condition |
| source authority/version changed but requirement semantics confirmed equal | CONDITIONAL | applicability/equivalence readback |
| subject/allocation changed | NO | new trace + assurance |
| verification method changed only | existing result may remain historical | new method decision determines new assurance route |
| requirement split into atomic children | old result only reusable if it resolves per child without inference | otherwise re-assure |

`same requirement_id` must not be used to hide a semantic version change.

---

## 13. Validator additions for P3 v1.1

- `P3/REQ-M01`: baselined consequential Requirement passes all applicable R-Q01..R-Q12 gates.
- `P3/REQ-M02`: independent pass/fail clauses require split.
- `P3/REQ-M03`: mandatory Requirement source cannot be precedent/reference/AI suggestion alone.
- `P3/ACC-M01`: acceptance criterion with undefined subjective terms cannot baseline without operational definition.
- `P3/CONF-M01`: Requirement conflict requires typed conflict class before disposition.
- `P3/WVR-M01`: material variance requires authorized Waiver/Deviation or Requirement Change; note-only variance fails.
- `P3/NEED-M01`: single user quote cannot self-promote to universal validated Need.
- `P3/CLM-M01`: claim type must map to compatible evidence class and P1 claim-ceiling axes.
- `P3/CLM-M02`: contradiction/boundary evidence cannot be omitted from promotion review.
- `P3/TRACE-M01`: consequential Requirement must resolve upstream, realization, assurance and change-impact trace dimensions.
- `P3/VERS-M01`: semantic Requirement change invalidates automatic verification carry-forward.

## 14. External calibration boundary

ISO/IEC/IEEE 29148:2018 remains the current published requirements-engineering standard (confirmed in 2024, revision underway). NASA systems-engineering guidance separately emphasizes good-requirement quality, source/ID-based verification matrices, and distinct validation planning. These calibrate P3 structure without replacing OLEANDER authority.
