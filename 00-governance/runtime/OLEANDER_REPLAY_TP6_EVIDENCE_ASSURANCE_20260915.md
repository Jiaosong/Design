# OLEANDER TP6 Evidence / Formal Assurance Stress Replay — 2026-09-15

Status: **DRAFT MULTI-CASE REPLAY / NOT CURRENT**.

Purpose: stress P6 against real OLEANDER records where evidence exists but does not justify the strongest conclusion.

Source-supported cases:

1. `SP04 / REQ-SCH / RG-01..RG-08` — reference/candidate evidence acquired while project-specific technical gates remain open.
2. `Image Lab / Professional Retest 01` — repair retest passes I01–I06 while Independent KEEP and ACTIVE remain open/not granted.
3. `Timer Light Basin v3.3` — render/calibration evidence passes within a bounded visualization scope while optical/material/thermal/DFM/electrical/tactile/user/deployment claims remain untested or separately gated.
4. Timer correction lineage — earlier claimed GitHub Actions run/artifact evidence was identified as invalid for the calibration and removed from authoritative files.

Not located as executed real-project evidence:

- a quantitative acceptance result lying near a threshold with explicit measurement uncertainty;
- a completed same-target contradictory-evidence adjudication between two admissible independent evidence sources.

Those remain `NOT_EVALUATED / OPEN` rather than simulated into reality.

---

# 1. SP04 — evidence acquisition is not project-specific assurance closure

The SP04 technical evidence request is explicit that evidence must apply to the **exact selected AWS 75.SI+ configuration and intended market/project**. It requests revision/date, exact fixing details, bracket/fastener family, spacing, corner/end distance, adjustment/tolerance requirements and applicability conditions.

The acceptance rule states that screenshots or isolated dimensions without revision + applicability conditions do not close the evidence gate.

The same record then reports:

```text
P0 Evidence Acquisition = ROUTE / METHOD / REQUEST CLOSURE COMPLETE
RG-01—RG-04 Project Technical Gates = OPEN
Project Issue = BLOCKED
```

Artifact-review gates can PASS while project technical gates remain OPEN.

The evidence-impact register makes the same distinction across RG-01..RG-08:

- reference evidence acquired ≠ exact project system selected;
- candidate fixing evidence acquired ≠ Schüco-permitted project fixing rules confirmed;
- anchor approval path identified ≠ project substrate/anchor/edge/embedment design complete;
- load-bearing candidates identified ≠ project reactions/capacities verified;
- reference thermal evidence acquired ≠ project ψ/fRsi/condensation criteria + actual fixing model complete;
- all RG-01..RG-07 open → no anchor row may be ISSUED.

## Replay result

`CONFIRMED`.

### Replay-derived rule

`P6/APP-RP04 EVIDENCE_EXISTENCE_OR_ACQUISITION_CLOSURE_DOES_NOT_GRANT_TARGET_ASSURANCE_WHEN_CONFIGURATION_CONDITION_OR_APPLICABILITY_GATES_REMAIN_UNRESOLVED`.

This is stronger than a generic source-quality rule: even technically credible evidence can remain inadmissible for a specific project claim.

---

# 2. Evidence state should distinguish acquisition from admissibility

SP04 shows at least four useful evidence-use states:

```text
ACQUIRED
APPLICABILITY_UNRESOLVED
ADMISSIBLE_FOR_TARGET
REJECTED_FOR_TARGET
```

An evidence item can exist, be traceable and even be useful as context while still being inadmissible for a project-specific assurance decision.

Recommended orthogonal fields:

```yaml
acquisition_state:
  NOT_ACQUIRED
  ACQUIRED
  SUPERSEDED

target_admissibility:
  NOT_EVALUATED
  APPLICABILITY_UNRESOLVED
  ADMISSIBLE
  ADMISSIBLE_WITH_LIMITATIONS
  REJECTED
```

### Replay-derived rule

`P6/ADM-RP04 EVIDENCE_ACQUISITION_STATE_AND_TARGET_ADMISSIBILITY_ARE_ORTHOGONAL; ACQUIRED_CANNOT_BE_INTERPRETED_AS_ADMISSIBLE`.

No new Evidence object type is required.

---

# 3. Applicability requires explicit target binding

For project-specific technical evidence, the decision must bind at least the material applicability dimensions relevant to the claim, such as:

- exact system / product / profile / version;
- opening or configuration type;
- dimensions/load class;
- substrate;
- market/jurisdiction;
- environmental/operating conditions;
- document revision/supersession state.

This is not a universal fixed checklist; the target claim determines which dimensions are material.

### Replay-derived rule

`P6/APP-RP05 ASSURANCE_USING_EXTERNAL_REFERENCE_OR_VENDOR_EVIDENCE_MUST_RECORD_TARGET_APPLICABILITY_DIMENSIONS_AND_UNRESOLVED_MATERIAL_DIMENSIONS_BLOCK_DIRECT_PROJECT_CLOSURE`.

Vendor/reference evidence may remain contextual or candidate evidence instead of being discarded.

---

# 4. Artifact QA PASS and technical assurance are independent targets

SP04 reports AR common/specific and final-artifact review PASS while the technical gates remain OPEN/BLOCKED.

Therefore:

```text
DRAWING / DATA / DOCUMENTATION / RELEASE QA PASS
≠
PROJECT TECHNICAL VERIFICATION PASS
```

### Replay-derived rule

`P6/TGT-RP01 ASSURANCE_TARGET_IDENTITY_MUST_BE_PRESERVED; PASS_FOR_ARTIFACT_QUALITY_OR_RELEASE_CANNOT_BE_REUSED_AS_TECHNICAL_REQUIREMENT_VERIFICATION_WITHOUT_A_SEPARATE_TARGET_DECISION`.

This is a concrete example of why P6 cannot collapse all reviews into one generic “validated” state.

---

# 5. Image Lab — repair retest is not Independent Review

`Professional Retest 01` states:

```text
I01–I06 REPAIR RETEST PASS
INDEPENDENT KEEP OPEN
ACTIVE NOT GRANTED
```

The same source bytes were used, and six repair checks passed, including source-resolution logic. Yet the report explicitly refuses to grant Independent KEEP or ACTIVE.

## Replay result

`CONFIRMED`.

### Replay-derived rule

`P6/INDP-RP02 PRODUCER_OR_REPAIR_RETEST_PASS_CANNOT_SATISFY_AN_INDEPENDENT_REVIEW_REQUIREMENT_OR_GRANT_DOWNSTREAM_ACTIVE_CURRENT_STATE`.

This operationalizes independence as a target obligation, not a descriptive label.

---

# 6. Assurance activity can PASS while promotion remains HOLD

The Image Lab example demonstrates:

- all local retest criteria passed;
- the derivative remains a source-limited support crop;
- Independent KEEP remains open;
- ACTIVE is not granted.

Therefore the Assurance Decision needs to state what it grants, leaves unchanged and excludes.

### Replay-derived rule

`P6/CEIL-RP04 PASS_DECISION_MUST_NAME_GRANTED_UNCHANGED_AND_EXCLUDED_DOWNSTREAM_STATES_OR_CLAIM_CEILINGS_WHERE_AMBIGUOUS_PROMOTION_IS_POSSIBLE`.

This reinforces the existing P6 claim-ceiling decision rule with real replay evidence.

---

# 7. Source-resolution evidence is bounded by derivative role

The Image Lab runtime detects that a nominal 1200×1200 output request samples only roughly 393×393 effective source pixels, so the export is held; a 400×400 support crop is allowed with `UPSCALE_CAUTION`.

The same report explicitly says the 400×400 derivative is:

- source-limited;
- digital support only;
- not a retail print hero;
- not new evidence;
- not a quality upgrade of the original source.

This shows that a quantitative/computational check can produce a bounded assurance outcome rather than a global quality state.

### Replay-derived rule

`P6/RDY-RP02 QUANTITATIVE_READINESS_PASS_OR_LIMITED_ACCEPTANCE_MUST_REMAIN_BOUND_TO_DECLARED_OUTPUT_ROLE_AND_CANNOT_UPGRADE_SOURCE_EVIDENCE_QUALITY`.

---

# 8. Timer — simulation/render/calibration scope cannot cross into untested domains

Timer v3.3 records a four-gate render/calibration PASS and a locked Hero/CMF render profile.

The same report explicitly lists as NOT RUN:

- optical performance;
- measured material/gloss/transmission;
- thermal;
- DFM/DFA/tolerance;
- electrical;
- tactile/user recognition.

It also states that the screenshots are executable-WebGL render evidence only, not CAD validation, material testing, manufacturing proof or user-test results, and that integrated public-browser QA is a separate gate.

## Replay result

`CONFIRMED`.

### Replay-derived rule

`P6/CEIL-RP05 ASSURANCE_RESULT_MUST_CARRY_EXPLICIT_DOES_NOT_ESTABLISH_BOUNDARIES_FOR_ADJACENT_HIGH_RISK_CLAIMS_WHEN_THE_ARTIFACT_CAN_EASILY_BE_MISREAD_AS_BROADER_PROOF`.

And:

`P6/TRF-RP01 PROTOTYPE_SIMULATION_RENDER_OR_CALIBRATION_EVIDENCE_CAN_SUPPORT_ONLY_THE_TESTED_REPRESENTATION_PERFORMANCE_SCOPE_UNLESS_AN_EXPLICIT_VALIDATION_BRIDGE_EXISTS`.

---

# 9. Correction lineage — invalid evidence must be removed from current support but retained as audit lineage

Timer v3.3 states that earlier records claiming a specific GitHub Actions run/artifact were **not valid evidence for this calibration** and were removed from authoritative files.

This is a real evidence-correction event.

A correct assurance system must distinguish:

```text
EVIDENCE_RECORD_EXISTED_HISTORICALLY
→ FOUND_INAPPLICABLE_OR_INVALID_FOR_TARGET
→ REMOVED_FROM_CURRENT_ASSURANCE_BASIS
→ RETAINED_IN_CORRECTION / PROVENANCE LINEAGE
```

It must not silently erase the correction history, nor continue counting the invalid evidence.

### Replay-derived rule

`P6/CONTRA-RP02 EVIDENCE_FOUND_INVALID_OR_INAPPLICABLE_FOR_TARGET_MUST_BE_REMOVED_FROM_CURRENT_ASSURANCE_BASIS_WITH_CORRECTION_LINEAGE_PRESERVED`.

This is not yet a full “two admissible sources contradict” replay; it is a confirmed invalid-evidence correction case.

---

# 10. Evidence independence remains distinct from evidence count

The current real cases do not establish a completed independence adjudication among multiple nominally different sources.

However they reinforce the need to track source lineage because multiple documents can be contextual or derive from the same product/manufacturer evidence family.

For this TP6 replay:

`MULTI_SOURCE_INDEPENDENCE_STRESS = PARTIALLY_EVALUATED / NO_COMPLETE_REAL_ADJUDICATION_FOUND`.

Existing rule `P6/IND-M01` remains necessary but not fully replay-closed.

Do not infer independence from document count, URL count or carrier count.

---

# 11. Measurement uncertainty threshold replay remains OPEN

The searched current corpus contains:

- tolerances;
- hypothetical/pending engineering criteria;
- geometry-equivalence tolerance tests;
- source-resolution computations;
- uncertainty requirements in research/governance material.

But no located executed project case simultaneously contains:

1. measured value;
2. explicit measurement uncertainty;
3. formal acceptance threshold;
4. decision where the uncertainty interval straddles or approaches that threshold.

Therefore:

`TP6 QUANTITATIVE THRESHOLD + MEASUREMENT UNCERTAINTY STRESS = NOT_EVALUATED / OPEN`.

No synthetic 1200.2±1.0 example is treated as real-project evidence.

Existing `P6/UNC-M01` remains draft/theoretical until real replay or a sanctioned test fixture is run.

---

# 12. Assurance disposition needs more than PASS/FAIL

The real replay supports at least:

- `PASS` — criterion/target satisfied for defined scope;
- `PASS_BOUNDED` / `ACCEPTED_WITH_LIMITATIONS` — usable only under stated conditions/role;
- `INCONCLUSIVE` — evidence exists but cannot resolve target claim;
- `HOLD` — required admissibility/authority/critical evidence not closed;
- `FAIL` — criterion contradicted/not met;
- `NOT_EVALUATED` — target not tested.

These must not be aliases for one another.

### Replay-derived rule

`P6/DISP-RP01 ASSURANCE_DISPOSITION_MUST_DISTINGUISH_BOUNDED_ACCEPTANCE_INCONCLUSIVE_HOLD_FAIL_AND_NOT_EVALUATED_WHEN_THEIR_NEXT_ACTIONS_DIFFER`.

Recommended canonical starter set:

```text
PASS
ACCEPTED_WITH_LIMITATIONS
INCONCLUSIVE
HOLD
FAIL
NOT_EVALUATED
OUTSIDE_CLAIM
```

This is an Assurance Decision disposition, not a universal project state enum.

---

# 13. P6 normalized decision model after replay

```yaml
assurance_decision_id:
assurance_type:
target_refs: []
target_configuration_ref:
target_conditions: []
evidence_refs: []
evidence_acquisition_state:
target_admissibility:
independence_level:
uncertainty_state:
per_target_results: {}
aggregation_policy:
disposition:
grants: []
leaves_unchanged: []
excludes: []
does_not_establish: []
correction_lineage_refs: []
review_ref:
```

---

# 14. TP6 replay-derived rules

Existing rules confirmed:

- `P6/ASR-RP01` mixed results preserve per-target outcomes;
- `P6/ASR-RP02` summary requires explicit aggregation policy;
- `P6/EVD-RP03` bounded evidence records non-establishment;
- `P6/INDP-M01` independent review cannot be self-awarded;
- `P6/APP-M01` applicability matters;
- `P6/CONTRA-M01` contradictory/invalid evidence cannot be silently ignored.

New rules:

- `P6/APP-RP04` evidence acquisition closure ≠ target assurance closure;
- `P6/ADM-RP04` acquisition and target admissibility are orthogonal;
- `P6/APP-RP05` project-specific assurance records applicability dimensions;
- `P6/TGT-RP01` pass cannot move across different assurance targets;
- `P6/INDP-RP02` repair retest cannot satisfy Independent Review or grant ACTIVE;
- `P6/CEIL-RP04` pass decision names granted/unchanged/excluded downstream states where promotion ambiguity exists;
- `P6/RDY-RP02` quantitative readiness remains bounded to output role;
- `P6/CEIL-RP05` high-risk adjacent claims require explicit does-not-establish boundary;
- `P6/TRF-RP01` prototype/simulation/render evidence needs validation bridge before broader transfer;
- `P6/CONTRA-RP02` invalid/inapplicable evidence removed from current basis with correction lineage preserved;
- `P6/DISP-RP01` bounded acceptance / inconclusive / hold / fail / not-evaluated remain distinct.

---

# 15. TP6 disposition

```text
PROJECT-SPECIFIC APPLICABILITY REPLAY = CONFIRMED
ARTIFACT-QA VS TECHNICAL-ASSURANCE SEPARATION = CONFIRMED
REPAIR RETEST VS INDEPENDENT REVIEW = CONFIRMED
PROTOTYPE/RENDER VS ENGINEERING/FIELD CLAIM CEILING = CONFIRMED
INVALID-EVIDENCE CORRECTION LINEAGE = CONFIRMED
MULTI-SOURCE INDEPENDENCE ADJUDICATION = PARTIAL / OPEN
QUANTITATIVE THRESHOLD + MEASUREMENT UNCERTAINTY = NOT_EVALUATED / OPEN
```

Overall:

`TP6 EVIDENCE / ASSURANCE STRESS REPLAY = PARTIAL COMPLETE WITH MATERIAL DELTAS`.

No Current promotion is authorized.