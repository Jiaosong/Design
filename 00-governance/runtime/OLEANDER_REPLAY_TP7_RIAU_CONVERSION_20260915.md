# OLEANDER TP7 Risk / Issue / Assumption / Unknown Conversion Replay — 2026-09-15

Status: **DRAFT MULTI-CASE REPLAY / NOT CURRENT**.

Purpose: test real semantic transitions among uncertainty/problem objects without inventing conversions that did not occur.

Real executed cases located:

1. `C04 C22 Route v3.5 → v3.8` — a producer-passed visual/route result was challenged by user review, structural defect was identified, prior revision became `REVISE / SUPERSEDED`, and a source-reanchored repair was produced/read back.
2. `C04 CH10 Resource Choreography v0.4` — first runtime PASS exposed a bounded presentation/interface defect, source-bounded repair was applied, then runtime readback passed while final design KEEP remained open.
3. `SP04 technical evidence acquisition` — unresolved project inputs are explicitly left open/blocking rather than silently converted into assumptions.

Not found as executed real-project conversion evidence:

- an explicitly logged `Risk → realized Issue` transition;
- an explicitly authorized `Unknown → Assumption` transition;
- an `Assumption → Refuted → dependent reopen` transition;
- an explicitly accepted residual Risk after mitigation.

Those remain `NOT_EVALUATED / OPEN`.

---

# 1. Issue discovery can invalidate producer-level PASS without rewriting history

C22 Route v3.5 had producer-side first-read/route-clarity/detail/readback passes. Later user review identified that the result did not visually correspond to the official guide or real scenic-area morphology.

The defect was explicitly structural, not cosmetic:

- the route was artificially unfolded into an editorial loop;
- river/banks/cable/peak forest no longer inherited the official-guide composition;
- the line became the subject rather than the landscape;
- the result read as a designer-made route diagram rather than the actual scenic-area relationship.

The project then records:

`v3.5 Route = REVISE / SUPERSEDED`.

v3.8 re-anchors the result to the official guide while preserving the NTS/field-open boundary.

## Replay result

`CONFIRMED`.

### Replay-derived rule

`P7/ISS-RP02 NEW_MATERIAL_REVIEW_FINDING_MAY_CREATE_OR_ESCALATE_AN_ISSUE_AFTER_PRIOR_PRODUCER_PASS; PRIOR_PASS_REMAINS_HISTORICAL_RECEIPT_NOT_CURRENT_CLOSURE_PROOF`.

This prevents “passed once” from suppressing later legitimate defects.

---

# 2. Issue root cause needs scope and evidence, not merely a label

For C22 v3.5, the source does more than say “looks wrong.” It identifies a causal design mechanism:

`editorial route abstraction displaced official-guide landscape/river/cable/peak-forest morphology`.

The repair direction follows that diagnosis:

- restore official-guide first-read;
- restore river/bank/cable/peak-forest hierarchy;
- make walking route terrain-following rather than an invented loop;
- keep reading markers subordinate.

This is enough to move root-cause state beyond `UNKNOWN` toward at least `SUPPORTED` for the bounded visual/design issue.

### Replay-derived rule

`P7/ROOT-RP02 ISSUE_ROOT_CAUSE_STATE_MUST_BE_BOUND_TO_EVIDENCE_AND_SCOPE; A_REPAIR_DIRECTION_MATCHING_THE_DIAGNOSED_MECHANISM_CAN_SUPPORT_ROOT_CAUSE_WITHOUT_IMPLYING_UNIVERSAL_CAUSAL_PROOF`.

---

# 3. Repair implementation and Issue closure are separate

C22 v3.8 was produced and technically reopened, but Independent Design Review remained pending.

Therefore:

```text
ISSUE IDENTIFIED
→ REPAIR IMPLEMENTED
→ PRODUCER READBACK PASS
≠ ISSUE FULLY CLOSED
```

Closure depends on the issue’s declared acceptance/review route.

### Replay-derived rule

`P7/ISS-RP03 ISSUE_REPAIR_IMPLEMENTED_OR_PRODUCER_RETEST_PASS_CANNOT_SELF_CLOSE_AN_ISSUE_WHEN_INDEPENDENT_OR_HIGHER_LEVEL_REVIEW_IS_REQUIRED`.

This aligns P7 with P6 independent-review semantics.

---

# 4. Local Issue closure can coexist with larger decision openness

CH10 v0.4 records a first PASS readback that exposed baked upstream HERO HOLD/interface markings at image edges. The repair was source-bounded crop only; no new scene generation/retouching was introduced. Runtime checks then passed.

This supports closing the **local carrier/readback defect** while the object remains:

`REAL PROJECT CH10 MUTATION CANDIDATE / BROWSER READBACK COMPLETE / NOT FINAL_KEEP`.

Therefore a local Issue can be closed without promoting the parent design/release state.

### Replay-derived rule

`P7/ISS-RP04 ISSUE_CLOSURE_IS_SCOPE_BOUND; CLOSING_A_LOCAL_DEFECT_DOES_NOT_CLOSE_PARENT_DESIGN_REVIEW_PROMOTION_OR_FIELD_OPEN_STATES`.

---

# 5. Issue lineage should retain defect → repair → retest

For repairable Issues, the useful machine lineage is not only `OPEN/CLOSED`.

Recommended fields:

```yaml
issue_id:
detected_by:
detected_at_revision:
problem_statement:
root_cause_state:
root_cause_statement:
affected_scope: []
repair_refs: []
retest_refs: []
closure_criteria: []
closure_authority:
closure_state:
supersedes_or_invalidates_receipts: []
new_risk_refs: []
```

### Replay-derived rule

`P7/LINE-RP02 ISSUE_CLOSURE_MUST_PRESERVE_DEFECT_REPAIR_RETEST_LINEAGE_AND_ANY_INVALIDATED_PRIOR_RECEIPTS`.

---

# 6. Unknown must not be converted merely to unblock work

SP04 contains multiple project-specific inputs that remain pending/hypothetical:

- exact manufacturer system/fixing rules;
- substrate/edge/embedment;
- project reactions/capacity;
- water/air layer route;
- thermal criteria/model;
- tolerance chain.

The project correctly keeps technical gates open/blocking instead of assuming values from generic reference evidence.

## Replay result

`CONFIRMED_BOUNDED`.

### Replay-derived rule

`P7/UNK-RP02 OPEN_OR_UNKNOWN_PROJECT_INPUT_MUST_REMAIN_UNKNOWN_WHEN_NO_AUTHORIZED_ASSUMPTION_ADMISSION_EXISTS_EVEN_IF_THIS_BLOCKS_DOWNSTREAM_WORK`.

This is a real non-conversion example and validates the anti-fabrication side of the Unknown contract.

---

# 7. Unknown → Assumption replay remains open

The P7 contract already requires explicit Assumption admission gates:

- necessary to proceed;
- proposition explicit;
- authority accepted;
- consequence if false;
- validation route;
- claim ceiling;
- expiry trigger.

However no reviewed source contains a complete executed event where a named Unknown is intentionally converted into an authorized Assumption and then tracked downstream.

Therefore:

`UNKNOWN_TO_ASSUMPTION_REAL_REPLAY = NOT_EVALUATED / OPEN`.

Do not infer such conversion from a project merely containing both Unknowns and Assumptions.

---

# 8. Assumption refutation replay remains open

No source-supported executed chain was found of:

```text
ASSUMPTION ACTIVE
→ contradicting evidence acquired
→ ASSUMPTION REFUTED
→ dependents identified
→ decisions/configurations/evidence reopened
→ repair/retest
```

Therefore:

`ASSUMPTION_REFUTATION_REAL_REPLAY = NOT_EVALUATED / OPEN`.

Existing P7 conversion rule remains draft but unclosed by replay.

---

# 9. Risk → Issue replay remains open

No reviewed source explicitly records a pre-existing Risk object whose uncertain event then occurred and was converted into an Issue while retaining lineage.

A discovered defect is not retroactively a Risk unless a prior Risk record exists.

Therefore:

`RISK_TO_ISSUE_REAL_REPLAY = NOT_EVALUATED / OPEN`.

### Replay-derived anti-inference rule

`P7/RSK-RP04 AN_ISSUE_DISCOVERED_AFTER_THE_FACT_MUST_NOT_BE_BACKFILLED_AS_A_PREEXISTING_RISK_WITHOUT_A_PRIOR_RISK_RECORD`.

This prevents false process maturity.

---

# 10. Residual risk acceptance replay remains open

No real source in the reviewed slice documents:

- risk likelihood/impact before treatment;
- treatment;
- residual likelihood/impact;
- accepting authority;
- explicit residual-risk acceptance.

Therefore:

`RESIDUAL_RISK_ACCEPTANCE_REPLAY = NOT_EVALUATED / OPEN`.

A mitigation action alone must not imply risk = zero or accepted.

Existing `P7/RSK-M03` remains necessary.

---

# 11. Problem-state model refinement

Replay supports an Issue lifecycle with a more explicit closure path:

```text
OPEN
→ TRIAGED
→ ROOT_CAUSE_OPEN | ROOT_CAUSE_SUPPORTED
→ REPAIR_PLANNED
→ REPAIR_IMPLEMENTED
→ RETEST_PENDING
→ RETEST_PASSED
→ REVIEW_PENDING when required
→ CLOSED
```

This should not replace project-native Issue status if existing owners already define one; it may be represented through orthogonal workflow fields where needed.

Recommended fields:

```yaml
repair_state:
  NOT_PLANNED
  PLANNED
  IMPLEMENTED
  RETEST_PENDING
  RETEST_PASSED
review_after_repair:
  NOT_REQUIRED
  PENDING
  PASS
  REVISE
```

### Replay-derived rule

`P7/ISS-RP05 REPAIR_STATE_AND_ISSUE_CLOSURE_STATE_ARE_ORTHOGONAL_WHEN_RETEST_OR_INDEPENDENT_REVIEW_REMAINS_REQUIRED`.

---

# 12. TP7 replay-derived rules

Confirmed existing rules:

- `P7/OPEN-RP01` generic OPEN cannot be force-classified;
- `P7/UNK-M01` Unknown cannot be silently converted into fact/assumption;
- `P7/ASM-M01` Assumption requires explicit admission;
- `P7/LINE-M01` conversions preserve lineage;
- `P7/ANTI-M01` known recurring failure should route through regression/anti-repeat handling.

New real-replay rules:

- `P7/ISS-RP02` later material review finding can create/escalate Issue after prior producer PASS;
- `P7/ROOT-RP02` root cause must be evidence/scope-bound;
- `P7/ISS-RP03` repair/retest does not self-close when higher review required;
- `P7/ISS-RP04` local Issue closure does not close parent promotion/design states;
- `P7/LINE-RP02` defect→repair→retest lineage and invalidated receipts retained;
- `P7/UNK-RP02` unresolved project input stays Unknown absent authorized assumption admission;
- `P7/RSK-RP04` post-hoc Issue cannot be backfilled as prior Risk;
- `P7/ISS-RP05` repair state and closure state can be orthogonal.

---

# 13. TP7 disposition

```text
ISSUE DISCOVERY AFTER PRODUCER PASS = CONFIRMED
ROOT-CAUSE-BOUNDED REPAIR = CONFIRMED
REPAIR → RETEST → HIGHER REVIEW BOUNDARY = CONFIRMED
LOCAL ISSUE CLOSURE VS PARENT STATE = CONFIRMED
UNKNOWN NON-CONVERSION = CONFIRMED_BOUNDED
RISK → ISSUE = NOT_EVALUATED / OPEN
UNKNOWN → AUTHORIZED ASSUMPTION = NOT_EVALUATED / OPEN
ASSUMPTION REFUTATION → REOPEN = NOT_EVALUATED / OPEN
RESIDUAL RISK ACCEPTANCE = NOT_EVALUATED / OPEN
```

Overall:

`TP7 R/I/A/U CONVERSION REPLAY = PARTIAL COMPLETE WITH ISSUE-LIFECYCLE DELTAS; THREE MAJOR CONVERSION PATHS REMAIN OPEN`.

No Current promotion is authorized.