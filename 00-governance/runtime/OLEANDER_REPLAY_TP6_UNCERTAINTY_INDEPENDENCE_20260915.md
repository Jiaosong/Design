# OLEANDER TP6 Evidence / Formal Assurance Stress Replay — Metrology Decision Rules + NASA IV&V — 2026-09-15

Status: **DRAFT EXTERNAL REPLAY / NOT CURRENT / SOURCE-BOUNDED**.

Purpose: stress-test P6 `Evidence Record / Assurance Activity / Assurance Decision` using two external cases that exercise different failure modes:

1. measurement uncertainty near a specification boundary;
2. required reviewer independence.

The two cases are deliberately separate. Measurement uncertainty and reviewer independence are different assurance dimensions and must not be collapsed into one evidence-strength score.

---

## 1. External source basis

### A. Measurement uncertainty / conformity

Public-source facts, with explicit authoritative bindings verified 2026-09-15:

- ILAC G8:09/2019 provides guidance on decision rules and statements of conformity under ISO/IEC 17025:2017.
- https://ilac.org/publications-and-resources/ilac-guidance-series/
- ILAC G17:01/2021 provides guidance for evaluating/reporting measurement uncertainty in testing.
- https://ilac.org/publications-and-resources/ilac-guidance-series/
- NIST defines a decision rule as the rule describing how measurement uncertainty is taken into account when stating conformity with a specified requirement.
- https://www.nist.gov/glossary-term/21621
- NIST publications explain that uncertainty and the selected decision rule influence false-accept and false-reject risk.
- https://www.nist.gov/publications/assessment-conformity-decision-rules-and-risk-analysis
- A NIST/National Conference on Weights and Measures example illustrates guard banding: if equipment tolerance is ±10 units and test uncertainty is ±2 units, one guard-band approach passes only errors up to ±8 units.
- ISO/IEC Guide 98-4:2012 remains current and addresses the role of measurement uncertainty in conformity assessment.

### B. Independent Verification & Validation

Public-source facts:

- NASA distinguishes Verification (“building the product right”) from Validation (“building the right product”).
- NASA IV&V defines independence in technical, managerial and financial dimensions.
- https://standards.nasa.gov/sites/default/files/standards/NASA/B/0/NASA-STD-87398RevB.pdf
- NASA describes IV&V as objective independent examination providing assurance conclusions based on evidence from development artifacts and risks.
- NASA's active Software Assurance and Software Safety Standard includes IV&V requirements across the software lifecycle.
- https://standards.nasa.gov/standard/NASA/NASA-STD-87398

Source boundary:

- external metrology/NASA statements = source-supported;
- numerical replay cases below are OLEANDER stress fixtures using the published NIST guard-band illustration;
- no claim is made that one guard-band rule is universally mandated for every project or measurement.

---

# 2. P6 must separate measurement result from conformity decision

A measurement result is not itself a PASS/FAIL.

Minimum distinction:

```text
EVIDENCE RECORD
  measured value
  uncertainty
  method/condition/configuration
        ↓
ASSURANCE ACTIVITY
  requirement/specification
  decision rule
  risk policy / guard band where applicable
        ↓
ASSURANCE DECISION
  conformity disposition for that target and rule
```

This prevents a common collapse:

`measured point estimate inside tolerance → PASS`.

### Replay rule

`P6/UNC-RP02 MEASUREMENT_RESULT_AND_CONFORMITY_DECISION_ARE_DISTINCT; POINT_ESTIMATE_INSIDE_SPECIFICATION_DOES_NOT_SELF_GRANT_PASS_WHEN_UNCERTAINTY_OR_DECISION_RULE_IS_MATERIAL`.

---

# 3. Quantitative boundary stress fixture

Use the published NIST guard-band illustration:

```text
specified equipment tolerance: ±10 units
measurement/test uncertainty: ±2 units
illustrative guarded acceptance limit: ±8 units
```

This example is used only to test P6 semantics.

### Case A — measured error = +7.5

Under the stated illustrative guard-band rule:

```text
|7.5| ≤ 8
```

A conformity PASS can be supported **for that decision rule, configuration and condition**.

The decision still must record:

- measurement result;
- uncertainty basis;
- requirement/specification limit;
- decision rule;
- target configuration;
- result.

### Case B — measured error = +8.5

The point estimate remains inside the nominal ±10 specification interval but lies outside the illustrative guarded acceptance zone.

Therefore P6 must not report:

`PASS because 8.5 < 10`.

Depending on the governing decision rule, the correct assurance disposition may be non-acceptance, inconclusive/hold, or another explicitly defined statement. The replay must **not** rewrite this as factual proof that the true value is outside ±10.

### Case C — measured error = +10.5

The point estimate is outside the nominal specification interval. Measurement uncertainty and the stated decision rule still matter for the exact conformity statement/risk treatment; however the point estimate itself must not be hidden by a generic “uncertain” badge.

### Replay result

`MEASUREMENT UNCERTAINTY STRESS = CONFIRMED`.

### Machine refinement

Add quantitative assurance fields:

```yaml
measurand_or_metric:
measured_value:
unit:
measurement_uncertainty:
uncertainty_kind:
coverage_factor_or_probability:
specification_lower_limit:
specification_upper_limit:
decision_rule_id:
decision_rule_basis:
acceptance_zone:
guard_band:
false_accept_risk_basis:
false_reject_risk_basis:
conformity_statement:
```

Fields are conditionally required; projects without quantitative conformity decisions do not fabricate them.

---

# 4. Specification zone and acceptance zone are different

The replay reveals a critical semantic distinction:

```text
SPECIFICATION ZONE
= values allowed by the requirement/specification

ACCEPTANCE ZONE
= measurement-result region accepted under the selected decision rule
```

They may coincide under some rules, but must not be assumed identical.

### Replay rule

`P6/UNC-RP03 SPECIFICATION_ZONE_AND_ACCEPTANCE_ZONE_ARE_DISTINCT_WHEN_DECISION_RULE_OR_GUARD_BAND_MODIFIES_CONFORMITY_DECISION_BOUNDARY`.

This also prevents storing guard-banded acceptance limits back into the Requirement as though the Requirement itself changed.

---

# 5. Decision rule belongs to assurance, not to source truth

NIST emphasizes that the choice of decision rule affects acceptance/rejection risk. Therefore the decision rule is part of the Assurance Activity/Decision contract.

It is not automatically:

- a new Requirement;
- an Evidence Record property;
- proof that one measured value is the true value.

### Replay rule

`P6/UNC-RP04 DECISION_RULE_IS_ASSURANCE_LOGIC; IT_MUST_NOT_SILENTLY_REWRITE_THE_SOURCE_REQUIREMENT_OR_MEASURED_EVIDENCE`.

---

# 6. Boundary result needs more than binary PASS/FAIL

A mature assurance system must preserve the reason why a case was not accepted.

Starter distinction:

```text
PASS
ACCEPTED_WITH_LIMITATIONS
INCONCLUSIVE
HOLD
FAIL
NOT_EVALUATED
OUTSIDE_CLAIM
```

But for quantitative conformity, the receipt should additionally record a reason code such as:

```text
WITHIN_ACCEPTANCE_ZONE
OUTSIDE_ACCEPTANCE_ZONE
UNCERTAINTY_OVERLAPS_DECISION_BOUNDARY
DECISION_RULE_UNDEFINED
UNCERTAINTY_NOT_ESTABLISHED
TARGET_CONFIGURATION_MISMATCH
```

### Replay rule

`P6/DISP-RP02 ASSURANCE_DISPOSITION_REQUIRES_REASON_CODE_WHEN_PASS_FAIL_OR_INCONCLUSIVE_DEPENDS_ON_DECISION_BOUNDARY_OR_UNCERTAINTY`.

This prevents `FAIL` from ambiguously meaning either “item proven nonconforming” or “cannot accept under the selected rule.”

---

# 7. Evidence quantity is not evidence independence

The metrology case also reinforces the distinction between repeated documents and independent evidence.

Five reports that reproduce one calibration result are not five independent measurements.

Minimum source-dependence metadata:

```yaml
evidence_origin_id:
measurement_campaign_id:
shared_method_dependency:
shared_instrument_dependency:
shared_data_dependency:
source_independence_group:
```

### Replay rule

`P6/IND-RP02 EVIDENCE_COUNT_MUST_NOT_BE_USED_AS_INDEPENDENCE_COUNT; COMMON_DATA_METHOD_INSTRUMENT_OR_ORIGIN_DEPENDENCIES_REQUIRE_SHARED_INDEPENDENCE_GROUPING`.

---

# 8. NASA IV&V shows independence is multidimensional

NASA IV&V distinguishes:

- technical independence;
- managerial independence;
- financial independence.

Therefore a generic field:

```text
independent = true
```

is inadequate for assurance where a specific independence profile is required.

### Replay result

`INDEPENDENCE STRESS = CONFIRMED`.

### Refinement

Add:

```yaml
independence_profile:
  technical: SATISFIED | NOT_SATISFIED | NOT_REQUIRED | NOT_EVALUATED
  managerial: SATISFIED | NOT_SATISFIED | NOT_REQUIRED | NOT_EVALUATED
  financial: SATISFIED | NOT_SATISFIED | NOT_REQUIRED | NOT_EVALUATED
independence_requirement_basis:
independence_scope:
conflict_of_interest_state:
```

Important boundary:

- NASA IV&V may require a stronger profile than an ordinary project peer review.
- P6 must evaluate the independence profile required by the declared Assurance Type/contract, not impose NASA's full IV&V profile on every review.

### Replay rule

`P6/INDP-RP03 INDEPENDENCE_IS_PROFILED_AGAINST_THE_ASSURANCE_CONTRACT; ONE_BOOLEAN_INDEPENDENT_FLAG_CANNOT_SATISFY_A_MULTI_DIMENSIONAL_INDEPENDENCE_REQUIREMENT`.

---

# 9. Producer self-check can remain valid evidence without becoming independent review

NASA's independence distinction does not make producer testing useless. It means producer testing and independent assessment have different assurance roles.

OLEANDER consequence:

```text
SELF_CHECK PASS
≠ INDEPENDENT_REVIEW PASS
```

but:

```text
SELF_CHECK PASS
may remain valid bounded evidence for producer QA / verification scope.
```

### Replay rule

`P6/INDP-RP04 FAILURE_TO_MEET_REQUIRED_INDEPENDENCE_LEVEL_DOWNGRADES_THE_INDEPENDENT_REVIEW_CLAIM_NOT_NECESSARILY_THE_UNDERLYING_SELF_CHECK_EVIDENCE`.

This prevents over-invalidation.

---

# 10. Verification and Validation remain separate even under IV&V

NASA explicitly distinguishes whether a product is built correctly from whether it is the right product for mission/customer needs.

Therefore “independent” does not collapse Verification and Validation into one assurance type.

### Replay rule

`P6/ASR-RP03 INDEPENDENCE_MODIFIES_WHO_PERFORMS_OR_GOVERNS_ASSURANCE; IT_DOES_NOT_COLLAPSE_VERIFICATION_AND_VALIDATION_TARGET_SEMANTICS`.

---

# 11. Contradictory evidence handling

P6 should not resolve contradiction by source count.

If:

- evidence E1 supports conformity;
- evidence E2 contradicts or produces a materially different result;

then adjudication must compare at least:

- target identity/configuration;
- condition/environment;
- method;
- uncertainty;
- provenance/source dependence;
- authority/applicability;
- temporal validity.

Contradiction states:

```text
APPARENT_METHOD_DIFFERENCE
CONFIGURATION_MISMATCH
CONDITION_MISMATCH
UNCERTAINTY_COMPATIBLE
MATERIAL_CONTRADICTION
SUPERSEDED_EVIDENCE
UNRESOLVED
```

### Replay rule

`P6/CONTRA-RP03 CONTRADICTION_ADJUDICATION_MUST_COMPARE_TARGET_CONFIGURATION_CONDITION_METHOD_UNCERTAINTY_AND_SOURCE_DEPENDENCE_BEFORE_MAJORITY_OR_STRENGTH_AGGREGATION`.

No “3 sources beat 1 source” shortcut is allowed.

---

# 12. Claim ceiling effect

A near-boundary quantitative result may support a narrower claim than a robust result far inside the acceptance zone.

However P6 must not invent a continuous universal confidence score.

Instead the Assurance Decision records:

- granted claim ceiling;
- unchanged axes;
- excluded axes;
- limitation/decision-rule reason.

Example:

```text
PASS under calibration decision rule
→ may grant TECHNICAL_CONFORMITY for tested configuration
→ does not grant FIELD_IN_USE performance
→ does not grant product/system Validation
→ does not grant legal certification unless certification authority is present
```

### Replay rule

`P6/CEIL-RP06 QUANTITATIVE_CONFORMITY_PASS_GRANTS_ONLY_THE_DECLARED_TARGET_CEILING; IT_CANNOT_AUTO_PROMOTE_FIELD_VALIDATION_CERTIFICATION_OR_DESIGN_QUALITY`.

---

# 13. Required P6 machine refinements

Add:

1. quantitative decision-rule fields;
2. specification-zone vs acceptance-zone distinction;
3. assurance disposition reason codes;
4. source-dependence / independence-group metadata;
5. multidimensional independence profile;
6. independence requirement basis;
7. contradiction adjudication classification;
8. bounded claim-ceiling grant tied to decision rule/configuration.

No new top-level Object Class is required.

---

# 14. Replay-derived rules

- `P6/UNC-RP02`
- `P6/UNC-RP03`
- `P6/UNC-RP04`
- `P6/DISP-RP02`
- `P6/IND-RP02`
- `P6/INDP-RP03`
- `P6/INDP-RP04`
- `P6/ASR-RP03`
- `P6/CONTRA-RP03`
- `P6/CEIL-RP06`

---

# 15. TP6 disposition

`TP6 EVIDENCE / UNCERTAINTY / INDEPENDENCE STRESS REPLAY = COMPLETE_WITH_DELTAS`.

Previously open replay states resolve as:

- measurement uncertainty near threshold = `CONFIRMED_EXTERNAL_REPLAY`;
- multi-source independence = `CONFIRMED_AS_DEPENDENCY_GROUPING_REQUIREMENT`;
- independent-review dimensionality = `CONFIRMED_EXTERNAL_REPLAY`;
- binary PASS/FAIL insufficiency near decision boundary = `CONFIRMED`.

No Current promotion is authorized.
