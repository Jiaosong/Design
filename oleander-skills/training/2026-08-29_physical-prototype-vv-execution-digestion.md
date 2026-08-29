# External / Professional Source Digestion — Physical Prototype + V&V Execution — 2026-08-29

Status: `SOURCE DIGESTION / CANDIDATE MATERIAL DELTA / NO CORE-SKILL INSTALL / NO PROMOTION`

## Gap

Source map owner: `GAP-VAL-01 — Physical Prototype / Test Planning / Verification-Validation Matrix`.

Residual chain before this batch:

`DESIGN CLAIM → TESTABLE REQUIREMENT → TEST ARTICLE PEDIGREE/FIDELITY → METHOD → FIXTURE/SETUP → VARIABLES/MEASUREMENTS → ACCEPTANCE/FAILURE → RUN → FAILURE EVIDENCE → SOURCE REPAIR → RETEST`.

## Current-first comparison

### `oleander-design-process/SKILL.md`
Current Design Process v0.2 already owns:
- Minimum Faithful Prototype;
- `UNKNOWN TYPE → MINIMUM VALID TEST MEDIUM → CLAIM LIMIT` Prototype Fidelity Matrix;
- actual readback/attack/repair;
- validation handoff and return;
- Change Propagation.

Missing residual: once physical/specialist validation is triggered, Current does not yet specify test-article pedigree, as-run configuration, developmental-vs-formal evidence, fixture/environment variables, failure/stop criteria, anomaly preservation or impacted-test reopening in one executable contract.

### `REQUIREMENT_VERIFICATION_TRACEABILITY_EXTENSION.md`
Already owns:
- atomic requirements;
- source/rationale;
- acceptance/failure conditions;
- verification method/proof class;
- configuration-bound evidence;
- change impact and reverify.

Missing residual: how the verification plan is executed as a real physical/hybrid test event and how the article/setup limits the claim.

### `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md`
Already owns physical design sequencing, payload/human/mechanism relations and validation HOLD. It does not define test execution evidence.

### Existing specialist owners
- Measurement uncertainty owns measurand/method/calibration/traceability/uncertainty.
- Human Factors owns representative human/task evidence.
- DFM/process capability owns manufacturing-process evidence.
- Reliability/durability owns population/life/failure evidence.
- Delivery QC owns released evidence-package integrity.

Therefore no new `oleander-validation`, test-engineering, prototype-lab or certification Core Skill is justified.

## Professional sources read

### NASA Systems Engineering Handbook — official professional source
Read 2026-08-29:
- Appendix D — Requirements Verification Matrix;
- Appendix E — Validation Plan / Validation Requirements Matrix;
- Appendix I — Verification and Validation Plan Outline.

Material mechanisms retained:
- verification and validation are different purposes;
- requirement-to-method/evidence planning should be explicit;
- validation may use physical models, simulation, fit-checks, dry-runs, tests and other evidence vehicles depending on the need;
- test-article pedigree must be defined so evidence is interpreted against the actual article;
- developmental/engineering evaluation must remain distinguishable from formal verification/validation;
- V&V implementation must identify system/unit flow, support equipment and facilities when material.

Rejected:
- NASA lifecycle, phase/review/certification structure as OLEANDER lifecycle;
- NASA article labels as OLEANDER maturity classes;
- aerospace qualification/acceptance sequences as universal;
- fixed verification-method abbreviations as mandatory;
- any implicit claim that NASA terminology supplies project engineering approval.

### K-Dense-AI `systems-engineer/AGENTS.md`
Repository license: MIT, already verified in Current source ledger.

Material comparison retained:
- verification = conformance to specified requirement; validation = fit to stakeholder need/context;
- V&V matrix binds requirement, method, procedure/evidence and configuration;
- verification of the wrong build is a traceability failure;
- failure diagnosis preserves interface/implementation/environment/procedure/configuration rival causes;
- as-run configuration and raw evidence should be preserved before corrective action.

Rejected:
- mandatory `shall` syntax;
- one V-model implementation;
- DOORS/Jama/Polarion/SysML tooling;
- fixed review sequence;
- domain-specific safety/certification standards as generic OLEANDER authority.

## Material Delta

Resulting extension:
`oleander-skills/oleander-design-process/PHYSICAL_PROTOTYPE_TEST_VV_EXECUTION_EXTENSION.md`

Accepted chain:

`CLAIM / REQUIREMENT / NEED → V OR V PURPOSE → TEST OBJECTIVE → ARTICLE PEDIGREE + CONFIG → FIDELITY-TO-CLAIM → METHOD / SETUP / ENVIRONMENT → VARIABLES / OBSERVABLES → PREDECLARED ACCEPTANCE + FAILURE / STOP → AS-RUN → RESULT / ANOMALY → DESIGN DISPOSITION → CHANGE IMPACT → RETEST → CLAIM CEILING`.

New high-value distinctions:
- `DEVELOPMENT TEST PASS ≠ REQUIREMENT VERIFIED ≠ NEED VALIDATED`;
- test-article appearance/fidelity does not determine evidence strength;
- article pedigree and configuration control the claim ceiling;
- fixture/setup/environment/support equipment are evidence conditions;
- failures/anomalies are frozen and captured before repair;
- change impact identifies a bounded retest set rather than keeping stale PASS or rerunning everything by habit.

## No-copy / universal-rule firewall

Do not install as OLEANDER defaults:
- breadboard/prototype/engineering-unit/qualification-unit/protoflight/flight-unit taxonomy;
- one test maturity ladder;
- NASA program phases or certification package;
- one T/A/I/D scheme;
- fixed sample count, repetitions, durations, load factors or environmental profiles;
- generic safety-factor or margin values;
- specific test-management software;
- formal verification status inferred from a developmental test merely because the same method was used.

## Golden regression target

Must reject a scenario where:
- a photoreal/production-looking prototype is assumed to have high evidence fidelity;
- the tested article differs from Current configuration;
- acceptance criteria were written after the run;
- fixture boundary conditions are omitted;
- a lab task PASS is used as field validation;
- raw evidence is replaced by a summary chart;
- the failed article is repaired before capture;
- a subsequent design change keeps previous tests PASS without impact analysis.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / OFFICIAL-SOURCE-CROSS-CHECKED / NO PRACTICE / NO CROSS-CONTEXT / NO PROJECT USAGE / NO INDEPENDENT KEEP / NO PROMOTION`.