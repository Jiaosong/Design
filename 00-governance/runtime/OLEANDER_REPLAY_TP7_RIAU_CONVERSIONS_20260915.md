# OLEANDER TP7 Risk / Issue / Assumption / Unknown Conversion Replay — 2026-09-15

Status: **DRAFT EXTERNAL REPLAY / NOT CURRENT / SOURCE-BOUNDED**.

External cases:

1. Cloudflare 1.1.1.1 incident of 2025-07-14 — issue introduction, dormant condition, impact trigger, detection, incident declaration, repair, validation and resolution.
2. NASA Systems Engineering Handbook guidance on TBRs/assumptions — unresolved values, responsible owner, rationale, resolution action/date, and assumption confirmation before baselining.

Purpose: stress-test TP7 conversion semantics without forcing every OPEN condition into Risk, Issue, Assumption or Unknown.

---

## 1. Source facts

### Cloudflare case

Public timeline documents:

- 2025-06-06 17:38 — configuration error introduced with no production impact or alert; the misconfiguration remained dormant.
- 2025-07-14 21:48 — a later configuration change triggered a global network refresh and impact started.
- 21:54 — a BGP origin hijack became visible but Cloudflare explicitly identified it as related/non-causal rather than the outage cause.
- 22:01 — impact detected and incident declared.
- 22:20 — revert initiated; a manually triggered restoration action was validated in testing locations before broader execution.
- 22:54 — normal traffic levels observed / impact ended.
- 22:55 — incident resolved.
- follow-up work included staged addressing deployments, deprecating legacy systems, improved documentation/test coverage and safer rollback behavior.

### NASA assumption / TBR guidance

NASA Systems Engineering Handbook guidance states, in substance:

- unresolved values may be represented as To Be Resolved (TBR) with a best estimate, rationale, resolution action, responsible owner and target resolution time;
- assumptions should be explicit and should be confirmed before the associated requirement/document is baselined.

Source boundary:

- Cloudflare/NASA statements above are source-supported;
- OLEANDER conversion semantics below are analytical mappings;
- no residual-risk acceptance authority is inferred where the public source does not show one.

---

# 2. Issue existence, detection and impact are different times

The Cloudflare defect existed before it was detected and before it caused impact.

Therefore an Issue cannot be modeled with only:

```text
OPENED_AT
CLOSED_AT
```

Minimum timeline dimensions should support:

```yaml
introduced_or_effective_at:
impact_started_at:
detected_at:
declared_at:
contained_at:
repair_implemented_at:
retest_completed_at:
impact_ended_at:
resolved_at:
```

Not every Issue has every timestamp.

### Replay rule

`P7/ISS-RP06 ISSUE_EXISTENCE_DETECTION_DECLARATION_AND_IMPACT_START_ARE_DISTINCT_TEMPORAL_EVENTS; DETECTION_TIME_MUST_NOT_BE_REWRITTEN_AS_ISSUE_ORIGIN`.

This is critical for latent design defects, data errors, safety defects and operational incidents.

---

# 3. Dormant Issue is not automatically Risk

The June 6 Cloudflare configuration error was an actual misconfiguration, although it had not yet produced observable service impact.

OLEANDER distinction:

```text
RISK
= uncertain future event/condition and consequence to an objective

ISSUE
= adverse condition/problem that actually exists, whether or not impact has yet occurred or the team has detected it
```

An undetected Issue may exist historically before `detected_at`.

### Replay rule

`P7/ISS-RP07 EXISTING_LATENT_DEFECT_OR_NONCONFORMING_CONDITION_IS_AN_ISSUE_ONCE_ESTABLISHED_BY_EVIDENCE; LACK_OF_CURRENT_IMPACT_OR_PRIOR_DETECTION_DOES_NOT_RETROACTIVELY_MAKE_IT_A_RISK`.

Do not fabricate a prior Risk record simply because a later Issue existed.

---

# 4. Risk realization creates lineage; it does not mutate object identity

Where a prior Risk record genuinely exists and the uncertain event occurs, preferred semantics are:

```text
RISK R-17
status = REALIZED
      ↓ realized_as
ISSUE I-42
```

The Risk remains historical evidence of prior anticipation/decision context. The Issue receives its own timeline, root-cause, repair and closure lifecycle.

### Replay rule

`P7/LINE-RP03 RISK_REALIZATION_CREATES_OR_LINKS_AN_ISSUE_OBJECT_AND_PRESERVES_RISK_LINEAGE; DO_NOT_MUTATE_THE_RISK_RECORD_IN_PLACE_INTO_AN_ISSUE`.

New Risk terminal/disposition concept:

```text
REALIZED_AS_ISSUE
```

This is a Risk outcome/disposition, not a new Object Class.

---

# 5. Correlated event is not causal event

Cloudflare explicitly separated the BGP hijack visible during the outage from the outage root cause.

P7 must therefore distinguish:

```text
TEMPORALLY_RELATED
CONTEXTUALLY_RELATED
CONTRIBUTING_CAUSE
TRIGGER
ROOT_CAUSE
NON_CAUSAL_COINCIDENT_EVENT
```

### Replay rule

`P7/ROOT-RP03 TEMPORAL_OR_CONTEXTUAL_COINCIDENCE_CANNOT_BE_PROMOTED_TO_CONTRIBUTING_OR_ROOT_CAUSE_WITHOUT_CAUSAL_BASIS`.

This protects postmortems from narrative overreach.

---

# 6. Trigger and root cause can be different

In the Cloudflare case:

- earlier configuration error created the latent defect;
- later change/refresh activated the impact path.

Therefore P7 root-cause records need to distinguish at least:

```text
LATENT_CONDITION
TRIGGER_EVENT
CONTRIBUTING_FACTOR
ROOT_CAUSE
PROPAGATION_FACTOR
DETECTION_FAILURE
RECOVERY_LIMITATION
```

These are causal roles, not separate Issue objects by default.

### Replay rule

`P7/ROOT-RP04 INCIDENT_CAUSAL_MODEL_MAY_REQUIRE_LATENT_CONDITION_TRIGGER_PROPAGATION_DETECTION_AND_RECOVERY_ROLES; ONE_GENERIC_ROOT_CAUSE_FIELD_IS_INSUFFICIENT_FOR_MATERIAL_INCIDENTS`.

---

# 7. Repair, retest, impact end and Issue closure remain separate

Cloudflare initiated the revert at 22:20, observed normal traffic at 22:54 and marked the incident resolved at 22:55. It also validated restoration actions in testing locations before broader execution.

This supports the existing orthogonal model:

```text
repair implemented
≠ retest passed
≠ impact ended
≠ issue closed
```

### Replay rule

`P7/ISS-RP08 REPAIR_IMPLEMENTED_RETEST_COMPLETED_IMPACT_ENDED_AND_ISSUE_RESOLVED_ARE_DISTINCT_STATES_OR_EVENTS_AND_MUST_NOT_COLLAPSE_TO_ONE_DONE_TIMESTAMP_WHEN_MATERIAL`.

---

# 8. Issue closure may create new Risks

Cloudflare's postmortem identified follow-up improvements even after the specific incident was resolved.

Therefore:

```text
ISSUE CLOSED
```

does not mean:

```text
ALL RELATED RISK = ZERO
```

A resolved Issue may create:

- prevention work;
- residual Risk;
- new Risk about similar failure modes;
- technical-debt actions.

### Replay rule

`P7/ISS-RP09 ISSUE_RESOLUTION_MAY_GENERATE_NEW_OR_RESIDUAL_RISK_AND_PREVENTION_ACTIONS; CLOSURE_CANNOT_AUTO_SET_RELATED_RISK_TO_ZERO`.

Public Cloudflare material demonstrates mitigation work, but does not expose a formal authorized residual-risk acceptance decision. That specific chain remains `NOT_EVALUATED`.

---

# 9. Unknown can carry a controlled provisional value without becoming an Assumption

NASA's TBR guidance exposes an important refinement.

An unresolved value may need a provisional working estimate so design/analysis can continue. OLEANDER should not force two bad choices:

1. leave the field blank and block all work; or
2. silently convert the estimate into an accepted Assumption/Fact.

Add an Unknown resolution mode:

```yaml
unknown_resolution_mode:
  NO_WORKING_VALUE
  TBR_PROVISIONAL_VALUE
  INVESTIGATION_IN_PROGRESS
  EXTERNAL_DECISION_PENDING
  OTHER_EXPLICIT

provisional_value:
provisional_value_basis:
resolution_owner:
resolution_action:
resolution_due:
claim_ceiling_while_unresolved:
```

### Replay rule

`P7/UNK-RP03 UNKNOWN_MAY_CARRY_EXPLICIT_TBR_PROVISIONAL_VALUE_WITH_OWNER_RATIONALE_RESOLUTION_ACTION_AND_CEILING_WITHOUT_BECOMING_FACT_OR_ACCEPTED_ASSUMPTION`.

---

# 10. Unknown → Assumption requires a semantic admission event

An Assumption is stronger than a provisional TBR value because the project deliberately accepts a proposition as a working premise.

Conversion requires at least:

```text
UNKNOWN U
  ↓ explicit assumption admission
ASSUMPTION A
```

with:

- proposition;
- accepting authority;
- necessity to proceed;
- consequence if false;
- validation/resolution route;
- expiry/reopen trigger;
- claim ceiling.

### Replay rule

`P7/UNK-RP04 UNKNOWN_TO_ASSUMPTION_IS_AN_EXPLICIT_AUTHORITY_EVENT_NOT_A_FIELD_FILL_OPERATION; TBR_PROVISIONAL_VALUE_ALONE_DOES_NOT_COMPLETE_THE_CONVERSION`.

NASA's guidance further supports that material assumptions should be confirmed before baselining the dependent requirement/document.

---

# 11. Assumption refutation creates explicit invalidation/reopen propagation

If evidence later refutes an Assumption, do not simply set:

```text
ASSUMPTION = FALSE
```

Required propagation:

```text
ASSUMPTION REFUTED
→ dependent Decisions
→ Requirements/Constraints derived from premise
→ Controlled Variables
→ Interfaces
→ Evidence/Assurance applicability
→ Baseline/Promotion
```

### Replay rule

`P7/ASM-RP05 REFUTED_ASSUMPTION_REQUIRES_TYPED_DEPENDENCY_PROPAGATION_TO_AFFECTED_DECISION_REQUIREMENT_VARIABLE_INTERFACE_ASSURANCE_AND_PROMOTION_SCOPE`.

The external cases support the need for this semantic rule; however a complete public executed assumption-refutation chain was not located in this replay. Therefore its real-case execution state remains `PARTIAL / NOT_FULLY_REPLAYED`.

---

# 12. Root-cause confidence remains independent from remediation urgency

A severe Issue may need containment before root cause is confirmed.

Cloudflare began recovery actions while investigating the complete incident chain.

Therefore:

```text
root_cause_state = HYPOTHESIZED / SUPPORTED
```

must not prevent urgent containment where evidence supports action.

Likewise, urgent containment must not be rewritten as root-cause confirmation.

### Replay rule

`P7/ROOT-RP05 CONTAINMENT_OR_RECOVERY_MAY_PROCEED_BEFORE_ROOT_CAUSE_CONFIRMATION; ACTION_URGENCY_CANNOT_PROMOTE_CAUSAL_CONFIDENCE`.

---

# 13. Detection control is part of Issue learning

The June 6 condition produced no user impact and therefore no alert. The later event triggered visible impact and alerts.

For material Issues, postmortem learning should record:

```yaml
existing_detection_controls:
why_not_detected_earlier:
detection_signal:
detection_latency:
new_detection_control_refs:
```

### Replay rule

`P7/ISS-RP10 MATERIAL_ISSUE_POSTMORTEM_SHOULD_DISTINGUISH_FAILURE_CAUSE_FROM_DETECTION_GAP_AND_RECORD_DETECTION_CONTROL_CHANGES_WHERE_RELEVANT`.

---

# 14. TP7 conversion matrix after replay

| From | To | Allowed? | Condition |
|---|---|---:|---|
| Risk | Issue | yes via link | event/condition actually realized; preserve Risk identity |
| Unknown | Assumption | yes via explicit admission | authority + consequence + validation + expiry + ceiling |
| Unknown | resolved Fact/Evidence | yes | investigation/evidence resolves truth |
| Unknown | TBR provisional value | yes without class change | explicit provisional marker + owner + due + ceiling |
| Assumption | Confirmed | yes | evidence supports proposition |
| Assumption | Refuted | yes | evidence contradicts; propagate reopen |
| Issue | Closed | yes | repair/retest/closure criteria + authority satisfied |
| Issue | Risk | not conversion | Issue may create/link a new residual/future Risk |
| Open | any R/I/A/U class | no automatic conversion | semantic basis required |

---

# 15. Remaining TP7 gaps

Closed by this replay:

- latent Issue versus Risk distinction;
- issue temporal model;
- Risk realization lineage semantics;
- causal-role decomposition;
- repair/retest/closure separation;
- Unknown/TBR provisional-value semantics;
- Unknown→Assumption admission rule.

Still open:

1. public executed case of an explicitly registered Risk becoming an Issue;
2. public executed Unknown→Assumption→Confirmed/Refuted chain;
3. public authorized residual-risk acceptance chain.

These remain replay gaps, not schema failures.

---

# 16. Replay-derived rules

- `P7/ISS-RP06`
- `P7/ISS-RP07`
- `P7/LINE-RP03`
- `P7/ROOT-RP03`
- `P7/ROOT-RP04`
- `P7/ISS-RP08`
- `P7/ISS-RP09`
- `P7/UNK-RP03`
- `P7/UNK-RP04`
- `P7/ASM-RP05`
- `P7/ROOT-RP05`
- `P7/ISS-RP10`

---

# 17. TP7 disposition

`TP7 R/I/A/U CONVERSION REPLAY = PARTIALLY_COMPLETE_WITH_MATERIAL_DELTAS`.

The model is materially stronger, but TP7 is not fully replay-closed because explicit prior-Risk realization, assumption-refutation and authorized residual-risk acceptance still lack complete public execution chains.

No Current promotion is authorized.