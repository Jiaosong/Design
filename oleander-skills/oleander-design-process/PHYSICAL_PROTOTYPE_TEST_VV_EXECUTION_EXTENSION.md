# Physical Prototype / Test / Verification–Validation Execution Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a design claim cannot be closed by visual readback, CAD inspection, simulation, browser evidence or generic requirement traceability alone and must be tested on a physical, hybrid or operationally representative article.

This extension turns an existing requirement/validation handoff into an executable evidence plan. It does **not** create a laboratory, certification, human-subjects, safety, engineering or regulatory approval authority inside OLEANDER.

## Existing-owner boundary

Use with, not instead of:
- `REQUIREMENT_VERIFICATION_TRACEABILITY_EXTENSION.md` for requirement/source/acceptance/evidence/change trace;
- `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md` and the main Design Process Prototype Fidelity Matrix for choosing the minimum faithful representation;
- `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md` when measured quantities require method/calibration/traceability/uncertainty;
- `DFM_DFA_PROCESS_CAPABILITY_EXTENSION.md` for process-capability/manufacturing evidence;
- Human Factors / Reliability / Material / specialist validation owners when the claim belongs to them;
- `oleander-delivery-qc` for released evidence-package/file integrity.

## Core contract

`DESIGN CLAIM / REQUIREMENT / NEED → V OR V PURPOSE → TEST OBJECTIVE → TEST ARTICLE PEDIGREE + CONFIGURATION → FIDELITY-TO-CLAIM CHECK → METHOD → SETUP / FIXTURE / ENVIRONMENT / SUPPORT EQUIPMENT → INPUT / CONTROL / DISTURBANCE VARIABLES → OBSERVABLES / MEASUREMENTS → PREDECLARED ACCEPTANCE + FAILURE / STOP CONDITION → RUN ID + AS-RUN RECORD → RESULT + ANOMALY → CLAIM DISPOSITION → SOURCE REPAIR / DESIGN RETURN → IMPACTED-TEST REOPEN → RETEST → EVIDENCE CEILING`

## Three evidence classes

Keep these distinct even when they use the same physical article:

1. **Developmental / learning test** — reduces uncertainty, finds failure modes, tunes geometry/process or compares options. Useful evidence, but not formal requirement closure unless its predeclared configuration/method/authority also satisfy the verification contract.
2. **Verification** — asks whether a specified requirement or constraint is satisfied by the relevant configuration using an appropriate proof method and acceptance criterion.
3. **Validation** — asks whether the resulting design/system satisfies the actual stakeholder need, task and intended context at adequate representativeness.

`DEVELOPMENT TEST PASS ≠ REQUIREMENT VERIFIED ≠ NEED VALIDATED`.

## Test-article pedigree rule

Every material physical result must identify what was actually tested.

Record:
- article ID and revision/build state;
- source/master configuration it represents;
- geometry/material/process/firmware/software/assembly differences from Current;
- substitute parts, mock components or simulated loads;
- wear/history/reuse state when it can affect the result;
- whether the article is destructive-test-only, reusable, one-off, representative or intentionally simplified;
- which claims the article can and cannot support.

Do not inherit external labels such as breadboard, engineering unit, qualification unit or protoflight unit as universal OLEANDER maturity classes. Projects may use their own article classes, but each class must define its actual pedigree and claim limit.

## Fidelity-to-claim gate

Before execution, ask:

`CAN THIS ARTICLE + SETUP EXPOSE THE FAILURE MODE OR PERFORMANCE RELATION THAT THE CLAIM DEPENDS ON?`

Examples:
- foam volume mockup may test reach, envelope or gross access but not hinge wear or sealing;
- 3D print may test assembly access but not production-material creep unless the material/process is relevant;
- benchtop mechanism may test kinematic sequence but not field contamination or long-term durability;
- final-looking CMF sample may test appearance/tactile direction but not internal structural performance;
- lab usability test may verify a task flow but cannot automatically validate field use if environmental/social constraints materially differ.

Higher visual fidelity does not expand the evidence ceiling by itself.

## V&V matrix row

For each material claim, maintain a row or equivalent object with at least:

`CLAIM / REQUIREMENT ID`
`→ PURPOSE: DEVELOPMENT / VERIFICATION / VALIDATION`
`→ OBJECT / INTERFACE`
`→ TEST ARTICLE + CONFIGURATION`
`→ METHOD`
`→ REQUIRED FIDELITY / ENVIRONMENT`
`→ SETUP / FIXTURE / SUPPORT EQUIPMENT`
`→ INPUT / CONTROL / DISTURBANCE VARIABLES`
`→ OBSERVABLE / MEASURAND`
`→ ACCEPTANCE / FAILURE / STOP CONDITION`
`→ PROCEDURE / RUN ID`
`→ RAW / DERIVED EVIDENCE LOCATION`
`→ RESULT: PASS / FAIL / BOUNDED / HOLD`
`→ ANOMALY / DEVIATION`
`→ DESIGN DISPOSITION`
`→ REOPEN / RETEST LINKS`
`→ CLAIM CEILING`

The matrix is a traceability/execution object, not a scorecard. A blank row is an unresolved proof obligation, not a hidden PASS.

## Test planning rules

1. **Start from the claim, not the available equipment.** Do not reverse-engineer a claim from whatever test rig is convenient.
2. **Declare the test objective before running.** One run may inform several questions, but each material conclusion needs a named claim and observable relation.
3. **Predeclare acceptance/failure where the activity is intended to close a requirement.** Developmental exploration can be open-ended, but it must not later be relabeled formal verification without checking whether the original setup and criteria were adequate.
4. **Separate controlled inputs, disturbances and measured outputs.** Unknown environmental or operator variation that can change the conclusion belongs in the evidence boundary.
5. **Fixture/setup is part of the test.** A fixture can create, suppress or redirect a failure mode. Record material constraints, preload, alignment, contact and boundary conditions when relevant.
6. **Support equipment has its own fitness boundary.** A load cell, jig, sensor, software script or simulator is not trustworthy merely because it produces numbers.
7. **As-run configuration outranks planned configuration.** Preserve deviations, substitutions, calibration state, setup changes and operator/procedure differences instead of silently editing the plan after execution.
8. **Raw evidence survives summary.** Preserve source readings/photos/video/logs/failure surfaces where practical; plots and final tables are derivatives.
9. **A failure is evidence, not noise to delete.** Preserve anomaly identity, reproduction attempts and rival explanations before repairing the design.
10. **Stop criteria protect evidence and safety.** When destructive escalation, damage, unsafe behavior, invalid instrumentation or invalid configuration makes further running misleading or unsafe, stop and classify the run rather than forcing completion.
11. **Validation requires contextual representativeness.** User, task, environment, maintenance/service condition and system integration must be representative enough for the need being claimed; otherwise retain a bounded validation result.
12. **One passing article does not establish production distribution, reliability or field performance.** Route those claims to the appropriate specialist/process evidence.

## Failure / anomaly loop

On material failure:

`FREEZE AS-RUN STATE → CAPTURE RAW EVIDENCE → CLASSIFY TEST-SETUP / ARTICLE / DESIGN / REQUIREMENT / ENVIRONMENT / MEASUREMENT RIVAL CAUSES → ROOT-CAUSE HYPOTHESIS → DESIGN OR TEST DISPOSITION → CONTROLLED CHANGE → IMPACT ANALYSIS → RETEST SET`

Do not repair the prototype first and reconstruct the failure from memory later.

A failed test may reveal:
- actual design defect;
- wrong requirement/acceptance criterion;
- article not representative;
- invalid fixture/boundary condition;
- measurement or calibration problem;
- procedure/operator inconsistency;
- environment/configuration mismatch;
- unknown mechanism requiring further developmental work.

## Change / regression rule

A material design, requirement, material, process, interface, software, fixture, environment or measurement-method change must identify which previous V&V evidence becomes stale.

Use:

`CHANGE → AFFECTED CLAIMS / REQUIREMENTS → AFFECTED FAILURE MODES / INTERFACES → PREVIOUS TESTS → REUSE JUSTIFICATION OR REOPEN → REQUIRED RETEST / ANALYSIS → NEW EVIDENCE ID`

Do not rerun the entire test corpus by habit, but do not preserve PASS because the changed feature appears visually local.

## Required output

- `claim_requirement_need_map`;
- `development_verification_validation_class`;
- `test_objective`;
- `test_article_pedigree_configuration`;
- `fidelity_to_claim_assessment`;
- `method_setup_fixture_environment`;
- `variables_observables_measurements`;
- `acceptance_failure_stop_conditions`;
- `procedure_run_and_as_run_record`;
- `raw_and_derived_evidence_identity`;
- `result_anomaly_and_rival_causes`;
- `design_disposition`;
- `change_impact_and_retest_set`;
- `claim_ceiling_and_external_holds`.

## Failure attacks

Reject or revise when:
- a beautiful prototype is treated as high-evidence because it looks final;
- prototype fidelity is named only as “low/mid/high” without stating what claim it can expose;
- a development experiment is retroactively called verification after it happened;
- a verification PASS is used to claim stakeholder/field validation;
- one article PASS is promoted to reliability, production capability or field performance;
- the test article differs materially from Current but the difference is omitted;
- acceptance criteria move after a failed run without requirement/change control;
- fixture or boundary conditions create the result but are absent from the report;
- only processed charts survive and raw/as-run evidence is unavailable;
- failures are discarded as outliers before a defensible cause is established;
- an article is repaired before the failed configuration/evidence is captured;
- a local design change leaves affected tests marked PASS without impact analysis;
- NASA V-model, test-article vocabulary or a fixed T/A/I/D matrix becomes mandatory OLEANDER lifecycle terminology.

## Source / transfer boundary

Professional sources studied:
- NASA Systems Engineering Handbook appendices for requirements verification matrix, validation planning and V&V plan/test-article pedigree — official professional reference;
- `K-Dense-AI/scientific-agents/scientific-agents/systems-engineer/AGENTS.md` — repository MIT; used only for traceability/configuration/V&V execution comparison.

Accepted bounded delta:
- explicit verification vs validation purpose;
- test-article pedigree/configuration and claim limits;
- physical models, simulations, fit-checks, procedure dry-runs and tests as different evidence vehicles selected by the claim;
- requirement/need-to-method-to-evidence matrix;
- as-run configuration and reproducibility record;
- developmental testing separated from formal closure;
- failure/anomaly capture before repair;
- change-impact-driven retest.

Rejected as universal:
- NASA program phases, review sequence or certification process;
- fixed T/A/I/D labels when another proof taxonomy is more appropriate;
- external test-article class names as OLEANDER maturity;
- mandatory aerospace qualification/acceptance sequence;
- fixed environmental profiles, test durations, sample counts or safety factors;
- one test-management/MBSE toolchain;
- prototype or lab PASS as field/manufacturing/regulatory approval.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE-CROSS-CHECKED / PRACTICE NOT YET RUN / NO CROSS-CONTEXT / NO PROJECT USAGE / NO PROMOTION`.