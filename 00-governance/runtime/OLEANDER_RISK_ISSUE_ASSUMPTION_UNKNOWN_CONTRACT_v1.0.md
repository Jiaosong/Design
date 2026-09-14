# OLEANDER Risk / Issue / Assumption / Unknown Contract v1.0

Status: **DRAFT GOVERNANCE EXTENSION / PRIORITY P7**. Applies to the `PROJECT` plane. It separates uncertainty/problem semantics that must not share one generic OPEN state.

## 1. Core separation

- `RISK` — an uncertain future event/condition that may affect objectives;
- `ISSUE` — a problem that has already occurred or is already observed;
- `ASSUMPTION` — an explicit proposition temporarily accepted so work can proceed;
- `UNKNOWN` — material missing knowledge that is not yet justified as an assumption.

Hard rules:

`RISK ≠ ISSUE ≠ ASSUMPTION ≠ UNKNOWN`.

`BLOCKED` is a disposition, not a semantic class.

`OPPORTUNITY` is normally positive Risk polarity, not a separate object class.

## 2. Risk contract

Minimum fields:

```yaml
risk_id:
project_id:
risk_polarity:
cause:
uncertain_event_or_condition:
consequence:
affected_objectives: []
affected_objects: []
likelihood_basis:
impact_basis:
exposure_class:
owner:
trigger_indicators: []
treatment_strategy:
treatment_actions: []
contingency:
residual_risk:
evidence_refs: []
review_due:
status:
```

Risk polarity:

`THREAT | OPPORTUNITY | MIXED`.

Risk state:

`IDENTIFIED → ANALYZED → EVALUATED → TREATMENT_PLANNED → TREATED → MONITORED → ACCEPTED | CLOSED`.

## 3. Risk rules

- likelihood/impact statements require a basis; do not invent numeric probabilities without evidence;
- exposure class may be qualitative when evidence is insufficient for quantitative risk;
- one hard safety/regulatory consequence cannot be averaged away by low cost/schedule impact;
- `ACCEPTED` means authorized residual risk acceptance, not disappearance;
- treatment effectiveness requires evidence/readback when consequential;
- risk becomes Issue when the uncertain event/condition actually occurs and produces an observed problem; keep the Risk lineage.

## 4. Risk treatment strategies

Controlled strategies:

`AVOID | REDUCE | TRANSFER_SHARE | ACCEPT | EXPLOIT | ENHANCE | MONITOR | OTHER_AUTHORIZED`.

The strategy label is not enough; material risks require actions, owner, trigger and residual-risk basis.

## 5. Issue contract

Minimum fields:

```yaml
issue_id:
project_id:
observed_problem:
detection_evidence: []
affected_objects: []
affected_claims: []
severity:
owner:
containment:
root_cause_state:
root_cause:
corrective_actions: []
verification_or_retest_refs: []
known_failure_signature:
reopen_rule:
status:
```

Issue severity:

`MINOR | MATERIAL | MAJOR | CRITICAL`.

Issue state:

`OPEN → TRIAGED → CONTAINED → ROOT_CAUSE_CONFIRMED → REPAIRED → RETESTED → CLOSED`.

## 6. Issue rules

- visible symptom is not automatically root cause;
- `CONTAINED` does not equal repaired;
- code/file change does not equal retested;
- material Issue cannot close before required retest/readback;
- recurring known failure after prior repair is `EXECUTION_DRIFT / KNOWN_FAILURE_RECURRED` unless materially new context is proven;
- failed fixes remain in lineage and must not be rewritten as success.

## 7. Root cause classes

Use controlled high-level classes when useful:

`AUTHORITY | REQUIREMENT | RELATION | GEOMETRY | DATA | MATERIAL | INTERFACE | CONFIGURATION | EXECUTION | TOOL_ENVIRONMENT | VISUAL_COMPOSITION | CONTENT | HUMAN_FACTOR | PROCESS | EVIDENCE | UNKNOWN_ROOT_CAUSE`.

These are diagnostic classes, not knowledge taxonomy.

## 8. Assumption contract

An Assumption is allowed only when the proposition is explicit and someone accepts the risk of proceeding under it.

Minimum fields:

```yaml
assumption_id:
project_id:
proposition:
why_needed:
scope:
affected_objects: []
affected_claims: []
consequence_if_false:
criticality:
owner:
accepting_authority:
validation_route:
evidence_refs: []
expiry_or_trigger:
containment_if_unresolved:
claim_ceiling_effect:
status:
```

Assumption criticality:

`LOW | MATERIAL | MAJOR | CRITICAL`.

State:

`PROPOSED → ACTIVE → CONFIRMED | REFUTED | EXPIRED`.

## 9. Assumption rules

- every active Assumption has an owner and consequence-if-false;
- Major/Critical assumption requires validation route + expiry/trigger + explicit claim ceiling effect;
- Assumption cannot silently become Fact because it appears repeatedly in documents;
- `CONFIRMED` requires accepted evidence/authority appropriate to proposition;
- `REFUTED` reopens affected objects/claims;
- `EXPIRED` cannot continue supporting promotion without renewed basis;
- unresolved Major/Critical assumption can survive only with explicit containment and bounded promotion scope.

## 10. Unknown contract

Use Unknown when the project lacks enough justified information to form even a responsible Assumption.

Minimum fields:

```yaml
unknown_id:
project_id:
unknown_question:
why_material:
scope:
affected_objects: []
affected_claims: []
owner:
resolution_route:
required_source_or_evidence:
decision_deadline:
consequence_if_unresolved:
claim_ceiling_effect:
status:
```

State:

`OPEN → INVESTIGATING → RESOLVED | OUTSIDE_CLAIM`.

## 11. Unknown rules

- Unknown must not auto-convert into Assumption merely to keep work moving;
- if a temporary proposition is required, create a separate Assumption with authority/risk ownership;
- `OUTSIDE_CLAIM` is legal only when the promoted claim explicitly excludes the unknown;
- critical Unknown with no containment blocks promotion when it could invalidate the claim;
- resolution should identify the new Project object/evidence/decision that closed the unknown.

## 12. Blocked disposition

`BLOCKED` is orthogonal and may apply to Risk treatment, Issue repair, Assumption validation, Unknown resolution, Interface closure or other work.

A blocker should state:

`blocked_object + blocking_dependency + owner + unblock_condition + next_check`.

Do not create a generic Blocker object unless the blocking relation itself needs independent lifecycle/audit; otherwise use a Material Dependency or Issue.

## 13. Conversion relations

Allowed conversions/links preserve lineage:

- `RISK → realized_as → ISSUE`;
- `UNKNOWN → resolved_by → EVIDENCE / DECISION / REQUIREMENT / ASSUMPTION`;
- `ASSUMPTION → confirmed_by / refuted_by → EVIDENCE`;
- `ISSUE → caused_by → confirmed root-cause object/relation`;
- `ISSUE → creates → RISK` when repair introduces future uncertainty.

Do not delete the source object when semantics change.

## 14. Risk / Issue / Assumption / Unknown effect on Claim Ceiling

Each material object must state which claim-ceiling dimensions it constrains.

Examples:

- unresolved site geometry Unknown may cap technical/design claim;
- unverified user Assumption may cap experience/validation claim;
- open Critical accessibility Issue may block compliance/project promotion;
- accepted residual Risk may allow bounded promotion but must remain visible in scope/decision.

## 15. Promotion rules

### Risk
Promotion may proceed with open Risk only if:
- risk is evaluated;
- owner/treatment/trigger are explicit;
- residual risk is within authorized tolerance;
- no hard Critical boundary remains uncontained.

### Issue
Major/Critical Issue normally blocks affected promotion until retested/closed or explicitly excluded from claim by valid authority.

### Assumption
Major/Critical active Assumption requires explicit containment and claim ceiling; no silent promotion as Fact.

### Unknown
Material Unknown requires resolution or explicit `OUTSIDE_CLAIM`; Critical Unknown cannot disappear into footnotes.

## 16. Time and review

Risk and Assumption require review/expiry triggers where conditions can change.

Unknown requires a decision deadline when unresolved status threatens a project decision.

Issue requires reopen trigger when repair may regress.

Time passing alone does not close any object.

## 17. Failure modes

Fail/HOLD when:

- future uncertainty is logged as Issue before occurrence;
- observed problem is kept as Risk to avoid owning repair;
- Unknown is silently converted to Assumption;
- Assumption has no accepting authority/consequence-if-false;
- Major/Critical Assumption lacks validation/expiry/containment;
- Issue closes before retest/readback;
- repeated known failure is treated as novel research without material new context;
- risk numeric likelihood is invented without basis;
- residual risk is called zero merely because treatment exists;
- Critical Unknown/Issue/Assumption is hidden while dependent claim is promoted.

## 18. Validator floor

- `RSK-001` Risk has cause/event/consequence/objective/owner/basis;
- `RSK-002` numeric likelihood requires evidence basis;
- `RSK-003` accepted Risk records residual-risk authority basis;
- `RSK-004` realized Risk links to Issue without deleting lineage;
- `ISS-001` Issue has detection evidence + owner + severity;
- `ISS-002` material Issue cannot close before retest/readback;
- `ISS-003` containment cannot equal closure;
- `ISS-004` repeated known failure triggers drift/anti-repeat logic;
- `ASM-001` active Assumption has owner + consequence-if-false + accepting authority;
- `ASM-002` Major/Critical Assumption has validation route + expiry + containment + claim ceiling effect;
- `ASM-003` confirmed Assumption requires appropriate evidence;
- `ASM-004` refuted/expired Assumption reopens affected claims;
- `UNK-001` Unknown cannot auto-convert to Assumption;
- `UNK-002` material Unknown has owner + resolution route + consequence;
- `UNK-003` OUTSIDE_CLAIM must be explicit in promoted claim scope;
- `BLK-001` Blocked is disposition, not default semantic object class;
- `PROM-001` material R/I/A/U object constrains applicable claim ceiling/promotion.

## 19. P7 closure condition

P7 is sufficiently refined for draft review when the four semantic classes, independent state machines, conversion/lineage rules, claim-ceiling impacts, anti-repeat behavior and promotion blockers all have machine-readable counterparts.
