# OLEANDER P6 Evidence / Assurance Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P6 SECOND PASS**. Semantic owner remains `OLEANDER_EVIDENCE_FORMAL_ASSURANCE_CONTRACT_v1.0.*`.

## 1. Purpose

P6 second pass makes admissibility, applicability, independence, uncertainty, contradiction and assurance disposition explicit enough to prevent evidence inflation.

Core invariant:

`EVIDENCE EXISTENCE ≠ EVIDENCE ADMISSIBILITY ≠ ASSURANCE ACTIVITY ≠ ASSURANCE DECISION ≠ PROMOTION`.

---

## 2. Assurance Type × Valid Target Matrix

| Assurance type | Primary valid target | Typical question | Invalid shortcut |
|---|---|---|---|
| `VERIFICATION` | Requirement/specification/acceptance criterion | does current configuration satisfy specified requirement? | Verify Need directly without requirement/criterion |
| `VALIDATION` | Need/Intent/Intended Use/Scenario | does realized system work for intended use/context? | infer from Requirement verification alone |
| `CERTIFICATION` | certifiable object/scope under recognized scheme | has authorized body certified this scope? | automated checker self-certifies |
| `INDEPENDENT_REVIEW` | design/research/technical/presentation object against review criteria | does independent reviewer accept/revise/reject? | producer self-review impersonates independence |
| `AUDIT` | records/process/configuration/provenance | are records/processes compliant with audit criteria? | audit PASS treated as performance proof |
| `ACCEPTANCE` | deliverable/configuration/scope | does authorized accepting party accept it? | acceptance treated as verification of all technical claims |

---

## 3. Evidence Admissibility Matrix

Before `ACCEPTED_FOR_USE`, check six gates:

1. `IDENTITY` — correct target/source identity;
2. `CONFIGURATION` — applicable version/baseline;
3. `CONDITION` — environment/scenario/population/site applicability;
4. `METHOD` — method/procedure appropriate and sufficiently documented;
5. `UNCERTAINTY` — uncertainty/error/limitations compatible with claim;
6. `PROVENANCE` — source chain resolvable.

Disposition:

| Gate result | Evidence status/use |
|---|---|
| all pass | admissible for stated claim/question |
| one uncertain but non-critical | `CHECKED` / bounded conditional use; claim ceiling lowered |
| configuration mismatch potentially material | `RECHECK_REQUIRED`; no Current promotion |
| method invalid for question | `REJECTED` for that claim; may remain useful elsewhere |
| provenance unresolved | not admissible for consequential claim |
| stale but historically valid | `HISTORICAL_ONLY` for Current claim |

Evidence admission is claim-specific; an Evidence Record may be accepted for one proposition and rejected for another.

---

## 4. Evidence Type × Maximum Default Claim Use Matrix

These are default ceilings, not automatic grants.

| Evidence type | Strongest typical direct use | Cannot establish by itself |
|---|---|---|
| `DOCUMENTARY_SOURCE` | bounded source/document proposition | installed/field performance unless document itself is field record |
| `FIELD_OBSERVATION` | observed condition/behavior | precise magnitude without measurement |
| `FIELD_MEASUREMENT` | measured field quantity under stated setup | broader population/time beyond sampling scope |
| `LAB_TEST` | behavior under test setup | field/in-use outcome without transfer evidence |
| `PROTOTYPE_TEST` | prototype configuration behavior | final installed system performance automatically |
| `USER_RESEARCH` | bounded user/stakeholder behavior/need/preference | universal need or long-term outcome without design/sampling support |
| `OPERATIONAL_DATA` | in-use behavior/performance over defined period | causal mechanism automatically |
| `SIMULATION` | modeled/predicted behavior | field truth |
| `MODEL_ANALYSIS` | bounded model relation/analysis | real-world outcome unless validated |
| `GEOMETRY_READBACK` | current represented geometry/dimension | technical adequacy beyond checked geometry |
| `MACHINE_CHECK` | rule/consistency/build condition checked | design quality or professional acceptance |
| `VISUAL_READBACK` | visible first-read/occlusion/hierarchy/representation behavior | source geometry correctness unless source-bound |
| `MATERIAL_SAMPLE` | sample property/appearance under stated conditions | installed assembly performance automatically |
| `MANUFACTURER_DATA` | product-stated property/context | independent project-specific installed performance |
| `PRECEDENT_CASE` | precedent fact/strategy/context | project performance proof |
| `REGULATORY_RECORD` | official rule/decision/applicability record | design compliance without project applicability check |
| `EXPERT_REVIEW` | bounded expert judgment | empirical/field fact unless evidence supplied |

---

## 5. Evidence Independence / Corroboration Matrix

Evidence quantity is not independence.

### Independence dimensions
- source origin;
- data generation process;
- method/instrument;
- analyst/reviewer;
- configuration/context;
- funding/vendor interest where material.

| Pattern | Corroboration value |
|---|---|
| same source reposted by several sites | LOW / one origin |
| several manufacturer pages using same internal test | LOW to MODERATE, not independent |
| independent field measurement + unrelated simulation agreeing | MODERATE/HIGH if methods applicable |
| two reviewers interpreting same image | reviewer independence only, not source independence |
| separate user samples in comparable contexts | potentially stronger, subject to sampling/method |
| independent methods contradict | not averaged away; trigger contradiction review |

No source-count scoring should override independence/applicability analysis.

---

## 6. Evidence Applicability / Transfer Matrix

Transfer from Evidence configuration/context A to Claim context B requires explicit reasoning.

| Changed dimension | Default transfer disposition |
|---|---|
| same target, same configuration, same conditions | direct applicability possible |
| same target, minor version change proven semantically irrelevant | conditional carry-forward |
| geometry/material/interface changed within tested tolerance envelope | conditional; applicability review required |
| target changed outside tested envelope | no direct transfer |
| different site/environment/population | indirect/contextual unless transfer model validated |
| prototype to final | conditional only when changed variables/materials/scale do not invalidate result |
| simulation to field | prediction only until field validation |
| precedent to current project | contextual/indirect only |
| manufacturer property to installed assembly | indirect until installation/system applicability established |

Transfer decision records `what is invariant + what changed + why evidence remains applicable + residual uncertainty`.

---

## 7. Uncertainty / Precision Matrix

For quantitative evidence, report no more precision than method supports.

Minimum applicable fields:
- measured/modelled value;
- unit;
- resolution;
- accuracy/calibration state;
- repeatability/repeat count;
- sample size/coverage;
- environment/setup;
- processing/transformation;
- tolerance/acceptance boundary.

| Condition | Disposition |
|---|---|
| uncertainty negligible relative to acceptance margin | normal bounded use |
| uncertainty overlaps acceptance threshold | `INCONCLUSIVE` unless decision rule explicitly handles uncertainty |
| uncertainty unknown but material | HOLD/re-measure/re-model; do not claim exact PASS |
| displayed precision exceeds instrument/model support | evidence-quality fail |
| transformed/derived value lacks propagation/accounting of uncertainty where material | re-analysis required |

---

## 8. Assurance Readiness Matrix

An Assurance Activity may enter `READY` only when all required rows pass.

| Readiness dimension | Required |
|---|---|
| target identity/configuration | exact |
| assurance type | explicit |
| question/target Requirement or Need | explicit |
| method/procedure | explicit |
| acceptance/success criteria | explicit where applicable |
| conditions/environment | explicit |
| instrument/software/data version | where material |
| executor | explicit |
| decision/review authority | explicit |
| independence requirement | explicit |
| evidence outputs | planned |
| assumptions/unknowns affecting interpretation | exposed |
| rights/safety/privacy prerequisites | resolved where applicable |

Missing material readiness field = `PLANNED`, not `READY`.

---

## 9. Independence Levels

Use a controlled independence state for review/assurance:

- `SELF_CHECK` — producer checks own work;
- `PEER_SAME_TEAM` — another contributor/reviewer within same responsible team;
- `INDEPENDENT_PROJECT_REVIEW` — reviewer not responsible for producing scoped output;
- `EXTERNAL_SPECIALIST` — external/domain specialist independent of producer;
- `AUTHORIZED_PROFESSIONAL_OR_BODY` — legally/professionally authorized acceptance/certification.

Independence requirement depends on consequence. A high-impact `KEEP_MAIN`, professional acceptance or Critical interface closure cannot be upgraded by `SELF_CHECK` merely because the checklist is complete.

---

## 10. Multi-Target Assurance Matrix

For one activity testing N targets:

- record one result per target;
- global activity summary may be derived only after per-target results exist;
- any global PASS must define aggregation rule;
- one failed Critical target blocks global PASS for scope unless explicitly outside claim;
- `INCONCLUSIVE` target stays visible and cannot be silently omitted.

Example:

`REQ-01 PASS`
`REQ-02 FAIL`
`REQ-03 INCONCLUSIVE`

Valid global summary: `FAIL / MIXED_RESULT`, not `PASS 2/3` when REQ-02 is mandatory.

---

## 11. Assurance Decision Matrix

| Activity outcome | Possible formal disposition | Promotion effect |
|---|---|---|
| criteria fully met | `PASS` or bounded `ACCEPTED` | may raise applicable ceiling only |
| criterion failed | `FAIL / REVISE / REJECT` | blocks affected promotion |
| evidence insufficient/uncertain | `INCONCLUSIVE / HOLD / OPEN` | no PASS carry-forward |
| minor accepted limitation within authority | `ACCEPTED_WITH_LIMITATIONS` | claim ceiling explicitly bounded |
| activity executed but analysis pending | no assurance decision yet | none |
| producer self-check only where independence required | cannot satisfy independent gate | none |

`PASS` is never a generic quality token; its meaning comes from assurance type + target + configuration + criteria.

---

## 12. Contradiction Resolution Matrix

When evidence conflicts:

| Check | Possible finding |
|---|---|
| identity | actually different objects |
| configuration | different revisions/configurations |
| condition | different scenarios/environments/populations |
| method | method-dependent result |
| date/freshness | one source stale |
| uncertainty | results overlap within uncertainty |
| true contradiction remains | claim ceiling lowered; new research/test/decision required |

True material contradiction blocks `ASSURED_FOR_SCOPE` until resolved or explicitly bounded by authority.

Do not delete or demote contradictory evidence merely because it complicates the narrative.

---

## 13. Claim-Ceiling Grant Matrix

An Assurance Decision grants only named dimensions.

Examples:
- geometry verification → technical/geometric ceiling only;
- accessibility professional review → compliance/professional ceiling for explicit scope;
- user validation → field/experience ceiling for tested population/scenario;
- independent design review → design-quality ceiling;
- audit → process/provenance ceiling;
- certification → certification/compliance state defined by certifying authority.

Every decision should record:
`granted_ceiling_dimensions + unchanged_dimensions + explicit exclusions`.

---

## 14. Validator additions for P6 v1.1

- `P6/ADM-M01`: Evidence accepted for use must pass applicable identity/configuration/condition/method/uncertainty/provenance gates.
- `P6/ADM-M02`: Evidence admission is claim-specific; acceptance for one Claim cannot auto-propagate to unrelated Claim types.
- `P6/IND-M01`: source count cannot substitute for independence analysis where corroboration matters.
- `P6/APP-M01`: cross-configuration/context Evidence transfer requires explicit applicability basis.
- `P6/UNC-M01`: material uncertainty overlapping acceptance threshold prevents unconditional PASS.
- `P6/RDY-M01`: Assurance cannot enter READY with unresolved material target/configuration/method/criteria/authority prerequisites.
- `P6/INDP-M01`: required independent assurance cannot be satisfied by SELF_CHECK.
- `P6/MULTI-M01`: multi-target Assurance must record per-target disposition before global summary.
- `P6/CONTRA-M01`: true material contradiction blocks strongest assurance ceiling until resolved/bounded.
- `P6/CEIL-M01`: Assurance Decision must name ceiling dimensions granted and dimensions not established.

## 15. External calibration boundary

NASA's Requirements Verification Matrix and Validation Plan explicitly separate requirement verification from validation against stakeholder/customer needs and intended use. P6 preserves that distinction and generalizes it to OLEANDER design/research/project assurance without treating NASA's domain-specific process as OLEANDER authority.
