# OLEANDER External-Digestion Routing — Batch 8 — 2026-08-29

Status: `CANDIDATE ROUTING ADDENDUM / EXISTING-FIRST / NO CORE-SKILL PROMOTION`

Purpose: close the source-map residual `GAP-VAL-01 — Physical Prototype / Test Planning / Verification-Validation Matrix` through the existing Design Process owner without creating a parallel Validation/Test Engineering Skill.

## Current-first result

Existing OLEANDER already covers:
- Design Process Prototype Fidelity Matrix and minimum faithful prototype;
- requirement→verification traceability, proof class, acceptance and change impact;
- physical-product phase gates;
- measurement uncertainty;
- human factors;
- DFM/process capability;
- reliability/material specialist evidence;
- release-package QC.

The remaining material gap is physical/hybrid **test execution evidence**: article pedigree, configuration, fidelity-to-claim, setup/environment, as-run record, anomaly preservation and impacted-test reopening.

## Routing table

| Trigger / Required Native Output | Existing owner | Candidate extension | Professional source provenance |
|---|---|---|---|
| A design claim/requirement/need must be exercised on a physical, hybrid or operationally representative article and the result must survive configuration/change trace | `oleander-design-process` + relevant Research / 3D / specialist VALIDATION / Delivery owner | `oleander-design-process/PHYSICAL_PROTOTYPE_TEST_VV_EXECUTION_EXTENSION.md` | NASA Systems Engineering Handbook Appendices D/E/I + K-Dense `systems-engineer/AGENTS.md` (MIT) |

## Preferred execution order

`CLAIM / REQUIREMENT / NEED`
`→ DEVELOPMENT / VERIFICATION / VALIDATION PURPOSE`
`→ TEST OBJECTIVE`
`→ TEST ARTICLE PEDIGREE + CONFIGURATION`
`→ FIDELITY-TO-CLAIM`
`→ METHOD + SETUP / FIXTURE / ENVIRONMENT / SUPPORT EQUIPMENT`
`→ VARIABLES / OBSERVABLES / MEASUREMENT HANDOFF`
`→ PREDECLARED ACCEPTANCE / FAILURE / STOP CONDITION`
`→ RUN + AS-RUN CONFIGURATION`
`→ RAW / DERIVED EVIDENCE`
`→ RESULT / ANOMALY / RIVAL CAUSES`
`→ DESIGN DISPOSITION`
`→ CHANGE IMPACT + RETEST SET`
`→ CLAIM CEILING / EXTERNAL APPROVAL HOLD`.

## Ownership boundaries

### Design Process
Owns:
- why the test exists and which design claim/need it can change;
- prototype/test-article fidelity relative to the claim;
- developmental vs verification vs validation purpose;
- design disposition after result/anomaly;
- change impact and retest routing.

Does not own:
- laboratory accreditation;
- engineering, clinical, safety, regulatory or customer certification;
- arbitrary specialist test methods/thresholds;
- production process capability;
- field truth from an unrepresentative lab setup.

### Requirement Verification Traceability
Owns requirement/source/acceptance/proof/configuration/change trace. The Batch-8 extension executes the material physical/hybrid proof event; it does not replace the traceability extension.

### Research / Measurement Uncertainty
Owns measurand, measurement model, instrument/method, calibration, traceability, uncertainty and decision-impact semantics when a quantitative result is material.

### Specialist validation owners
Human Factors, Reliability, Materials, manufacturing/process capability and other domain owners continue to own their domain-specific evidence. Batch 8 only defines the common test-event trace and design-return contract.

### Delivery QC
Owns released evidence-package/file integrity, not experimental or engineering truth.

## Core separations

`PROTOTYPE LOOKS FINAL ≠ TEST ARTICLE REPRESENTATIVE`

`DEVELOPMENT TEST PASS ≠ REQUIREMENT VERIFIED`

`REQUIREMENT VERIFIED ≠ STAKEHOLDER NEED VALIDATED`

`LAB VALIDATION ≠ FIELD VALIDATION WHEN CONTEXT DIFFERS`

`ONE ARTICLE PASS ≠ RELIABILITY / PROCESS CAPABILITY / POPULATION CLAIM`

`SUMMARY CHART ≠ RAW / AS-RUN EVIDENCE`

`LOCAL DESIGN CHANGE ≠ PREVIOUS TESTS AUTOMATICALLY STILL VALID`

## No new identities

Do not create a new Core Skill for:
- prototype engineering;
- test engineering;
- V&V management;
- qualification testing;
- acceptance testing;
- test lab operations;
- certification.

A future separate owner would require repeated real-project evidence that the current Design Process + specialist-routing model cannot carry the work without authority conflict.

## Universal-rule firewall

Do not promote as global defaults:
- NASA program phases or review gates;
- breadboard / engineering unit / qualification unit / protoflight taxonomy;
- fixed T/A/I/D categories where another proof taxonomy is more suitable;
- fixed test counts, sample sizes, cycles, loads, safety factors, confidence targets, environmental profiles or durations;
- one fixture topology or test setup;
- one certification/acceptance sequence;
- one test-management/MBSE toolchain.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / SOURCE DIGESTED / NO PRACTICE / NO CROSS-CONTEXT / NO PROJECT USAGE / NO PROMOTION`.

Next valid maturity step is a controlled physical/hybrid practice with a deliberately imperfect test article, one real failure/anomaly, preserved as-run evidence and a bounded retest after repair.