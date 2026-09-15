# OLEANDER P7 Risk / Issue / Assumption / Unknown Matrices v1.1

Status: **DRAFT COMPANION / PRIORITY P7 SECOND PASS**. Semantic owner remains `OLEANDER_RISK_ISSUE_ASSUMPTION_UNKNOWN_CONTRACT_v1.0.*`.

## 1. Purpose

P7 second pass prevents different uncertainty/problem semantics from collapsing into one `OPEN` bucket.

Core invariant:

`FUTURE UNCERTAINTY = RISK; OBSERVED PROBLEM = ISSUE; AUTHORIZED TEMPORARY PROPOSITION = ASSUMPTION; MATERIAL KNOWLEDGE GAP = UNKNOWN`.

---

## 2. Risk Statement Quality Matrix

Preferred structure:
`Because of <CAUSE>, there is a possibility that <UNCERTAIN EVENT/CONDITION>, resulting in <CONSEQUENCE TO OBJECTIVE>`.

| Test | PASS condition |
|---|---|
| cause | plausible precursor/context named |
| uncertainty | event/condition is genuinely uncertain, not already observed |
| consequence | impact tied to project objective/object/claim |
| likelihood basis | qualitative/quantitative basis stated |
| impact basis | dimensions and hard boundaries stated |
| owner | one accountable current owner |
| trigger | observable indicator or review cadence |
| treatment | strategy + actions, not label only |
| residual risk | post-treatment uncertainty retained |

Observed failure already present → create Issue, not Risk.

---

## 3. Risk Impact Dimensions

Assess independently where applicable:
- safety/health;
- regulatory/accessibility/rights;
- technical/performance;
- user/experience;
- integration/interface;
- cost/resource;
- schedule;
- operational/maintenance;
- reputation/value;
- evidence/claim/promotion.

Do not average a hard safety/regulatory consequence away with low scores elsewhere.

ISO 31000 remains risk-guidance rather than a certification standard and emphasizes identification, analysis, evaluation, treatment, monitoring and communication; OLEANDER keeps that process but preserves project-specific authority and claim-ceiling semantics.

---

## 4. Likelihood / Exposure Basis Matrix

| Basis | Allowed expression |
|---|---|
| no defensible frequency/probability data | qualitative class + rationale |
| empirical frequency data applicable | quantitative or interval estimate with source/context |
| model-based probability | probability with model/assumption/uncertainty disclosure |
| expert elicitation | structured qualitative/quantitative estimate + expert basis |
| unknown material likelihood | `OPEN/UNKNOWN`, not invented number |

Risk exposure class is a decision aid, not truth rank.

---

## 5. Risk Treatment / Residual Risk Matrix

| Strategy | Minimum closure evidence |
|---|---|
| `AVOID` | risk source removed and downstream consequence checked |
| `REDUCE` | mitigation implemented + effectiveness evidence |
| `TRANSFER_SHARE` | responsibility/contract transfer proven; project residual exposure still assessed |
| `ACCEPT` | authorized risk acceptance + residual-risk basis |
| `EXPLOIT/ENHANCE` | opportunity action + downside interactions considered |
| `MONITOR` | trigger/threshold/review cadence explicit |

Treatment existence never means residual risk = 0.

---

## 6. Issue Severity / Repair Matrix

| Severity | Minimum governance |
|---|---|
| `MINOR` | owner + repair + local readback |
| `MATERIAL` | containment + root-cause assessment + corrective action + retest |
| `MAJOR` | root-cause evidence + affected-object graph + formal retest + promotion review |
| `CRITICAL` | immediate containment, authority escalation, affected promotion/claim block, independent/specialist review as applicable |

`CONTAINED ≠ REPAIRED ≠ RETESTED ≠ CLOSED`.

---

## 7. Root Cause Confidence Matrix

Root-cause state should be distinct from Issue status:

`UNKNOWN → HYPOTHESIZED → SUPPORTED → CONFIRMED`.

| State | Meaning |
|---|---|
| `UNKNOWN` | symptom known, cause not established |
| `HYPOTHESIZED` | plausible cause proposed |
| `SUPPORTED` | evidence materially supports cause but alternatives remain |
| `CONFIRMED` | repair/reproduction/retest or equivalent evidence sufficiently establishes cause for decision scope |

Issue may be contained before root cause confirmed, but material closure normally requires confirmed or explicitly bounded root cause.

---

## 8. Corrective Action / Anti-Repeat Matrix

For Material+ Issue:
`symptom → containment → root cause → corrective action → retest → regression protection`.

Repeated known failure after prior validated repair:
- same signature + same causal context → `KNOWN_FAILURE_RECURRED / EXECUTION_DRIFT`;
- same symptom but materially new causal context → new/linked Issue with re-analysis;
- do not restart broad research merely because the failure reappeared.

Regression protection may be validator/eval/test/checklist/tool fix depending on cause.

---

## 9. Assumption Admission Matrix

Create Assumption only if all pass:

| Gate | PASS condition |
|---|---|
| `NECESSARY_TO_PROCEED` | project decision cannot reasonably wait for full evidence |
| `PROPOSITION_EXPLICIT` | falsifiable/confirmable statement exists |
| `AUTHORITY_ACCEPTED` | someone authorized accepts proceeding risk |
| `CONSEQUENCE_IF_FALSE` | impact visible |
| `VALIDATION_ROUTE` | evidence/action can confirm/refute or expiry is explicit |
| `CLAIM_CEILING` | dependent claims bounded |
| `EXPIRY_TRIGGER` | time/event/review trigger exists for Material+ |

If there is not enough basis even to formulate a responsible proposition, keep `UNKNOWN`.

---

## 10. Assumption Criticality Matrix

| Criticality | Minimum burden |
|---|---|
| LOW | owner + scope |
| MATERIAL | consequence-if-false + validation route |
| MAJOR | accepting authority + validation route + expiry + containment + affected claims |
| CRITICAL | all above + promotion block unless explicit bounded containment/authority acceptance |

Repeated textual use does not increase assumption truth status.

---

## 11. Unknown Classification Matrix

Unknown subclasses are diagnostic only:
- `FACT_UNKNOWN` — factual state missing;
- `MEASUREMENT_UNKNOWN` — value requires measurement;
- `REQUIREMENT_UNKNOWN` — controlling requirement/applicability unresolved;
- `AUTHORITY_UNKNOWN` — who controls/approves unresolved;
- `INTERFACE_UNKNOWN` — interaction/consumer/variable relationship unresolved;
- `USER_CONTEXT_UNKNOWN` — stakeholder/use evidence missing;
- `FUTURE_CONDITION_UNKNOWN` — future condition unresolved but not responsibly probabilized;
- `METHOD_UNKNOWN` — valid test/analysis route unclear;
- `SCOPE_UNKNOWN` — project/claim boundary unclear.

Subclass does not create a new semantic object family.

---

## 12. Unknown → Assumption Conversion Matrix

Conversion is **never automatic**.

Required conversion record:
`unknown_ref + proposed proposition + basis + why assumption is necessary + accepting authority + consequence_if_false + validation/expiry + claim ceiling`.

If any required field absent, Unknown remains open.

---

## 13. Conversion / Lineage Matrix

| From | To/link | Rule |
|---|---|---|
| Risk | Issue | when uncertain event occurs; retain risk history |
| Unknown | Evidence/Decision/Requirement | resolution result linked |
| Unknown | Assumption | only through explicit admission gate |
| Assumption | Confirmed/Refuted via Evidence | evidence/configuration bound |
| Issue | Risk | repair introduces new future uncertainty |
| Issue | Requirement/Change | corrective action may create new controlled obligation/change |
| Risk | Decision | risk-informed choice; risk object remains visible |

Semantic conversion does not delete source lineage.

---

## 14. Promotion Impact Matrix

| Object state | Promotion behavior |
|---|---|
| evaluated Risk with authorized residual risk | may permit bounded promotion |
| unevaluated Major/Critical Risk | blocks affected promotion |
| open Major/Critical Issue | blocks affected promotion unless lawfully outside claim/contained by authority |
| active Major/Critical Assumption | requires explicit containment + claim ceiling + validation route |
| refuted/expired assumption | affected claims/decisions reopen |
| material Unknown | resolve or explicit OUTSIDE_CLAIM |
| critical Unknown | cannot disappear into notes; blocks dependent promotion |

---

## 15. Blocked Disposition Matrix

`BLOCKED` requires:
`blocked_object + blocking_dependency + owner + unblock_condition + next_check`.

If the blocking relationship itself needs independent state/history/authority, model a `MATERIAL_DEPENDENCY` or `ISSUE`; otherwise do not invent a generic Blocker object.

---

## 16. Validator additions for P7 v1.1

- `P7/RSK-M01`: Risk statement distinguishes cause/event/consequence and event remains uncertain.
- `P7/RSK-M02`: numeric likelihood requires defensible empirical/model/elicitation basis.
- `P7/RSK-M03`: treatment closure records effectiveness and residual risk; treatment presence cannot imply zero risk.
- `P7/ISS-M01`: Material+ Issue tracks containment/root-cause/corrective-action/retest separately.
- `P7/ROOT-M01`: root-cause confidence state cannot be inferred from repair alone.
- `P7/ANTI-M01`: recurrent known failure routes to anti-repeat/drift before new research unless material new context exists.
- `P7/ASM-M01`: Assumption admission passes necessary/proposition/authority/consequence/validation/ceiling/expiry gates as applicable.
- `P7/UNK-M01`: Unknown→Assumption conversion requires explicit conversion record.
- `P7/LINE-M01`: Risk→Issue or Unknown→resolution preserves source lineage.
- `P7/PROM-M01`: Major/Critical R/I/A/U state maps explicitly to promotion/claim-ceiling effect.

## 17. External calibration boundary

ISO 31000:2018 remains the current published edition while a revision is under development; its core identify/analyze/evaluate/treat/monitor/communicate structure and NASA's risk-informed decision/continuous risk management guidance are used only to calibrate P7. OLEANDER's Issue/Assumption/Unknown separation remains its own project-runtime semantic contract.
