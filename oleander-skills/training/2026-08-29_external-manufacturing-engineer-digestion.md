# External Skill Digestion — Manufacturing Engineer — 2026-08-29

Status: `SOURCE DIGESTION / CANDIDATE MATERIAL DELTA / NO INSTALL / NO PROMOTION`

## Source

- Repository: `wonsukchoi/domain-experts`
- Source file: `roles/manufacturing-engineer/SKILL.md`
- License: repository root `LICENSE` = MIT, verified 2026-08-29.
- Source maturity metadata: draft. This does not become OLEANDER maturity.

## Current-first comparison

Compared against Current / Candidate OLEANDER owners:

1. `oleander-design-process`
   - already owns design reasoning, physical product gates, form/serviceability, material failure, reliability and system-interface reasoning;
   - does not yet close the design→candidate manufacturing process→capability evidence→design return loop.
2. `oleander-3d-pipeline/PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md`
   - already owns native CAD, named parameters, datums/mates, purchased components and deterministic geometry checks;
   - explicitly states that valid geometry does not prove manufacturability or tolerance capability.
3. `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md`
   - already owns measurand/method/calibration/traceability/uncertainty/decision-boundary semantics;
   - does not own whether a process is repeatedly capable of a design characteristic.
4. Technical Drawing PR #172
   - owns Candidate drawing-carrier semantics and translation;
   - must not be converted into a manufacturing-engineering authority by this digestion.
5. Current FMEA
   - failure-mode/risk organization only; not manufacturing capability proof.

## Material Delta accepted

External source mechanisms that survive Current comparison:

- a design tolerance is a manufacturing promise that must be checked against a named process rather than assumed from CAD validity;
- datum/workholding relations should preserve the functional locating logic rather than fixture convenience;
- measurement-system fitness must be checked before interpreting process capability;
- process capability evidence is contextual and must remain attached to process/configuration/population state;
- containment such as sorting/reinspection does not prove corrective-action effectiveness;
- a discovered process/tolerance mismatch must return upstream before tooling/release is treated as closed;
- capability evidence must affect a design/process decision rather than remain a detached quality statistic.

## Current synthesis retained but not attributed to this external source

DFA/assembly reasoning in the resulting extension is primarily routed from existing OLEANDER `PHYSICAL_PRODUCT_PHASE_GATES_EXTENSION.md` and `PRODUCT_FORM_AFFORDANCE_SERVICEABILITY_EXTENSION.md`:
- assembly access;
- orientation / locating;
- fastening sequence;
- service / disassembly;
- error-proofing consequences.

The external Manufacturing Engineer source is **not** used as authority for a universal part-count-minimization framework.

## Rejected / bounded transfer

Do not install as universal OLEANDER truth:

- Cpk/Ppk = 1.33 / 1.67 or any fixed release threshold;
- GR&R 10% / 30% or any fixed measurement-system gate;
- automatic RSS when Cpk is high, or automatic worst-case for safety;
- fixed subgroup/sample sizes;
- fixed PFMEA severity/RPN/action-priority thresholds;
- fixed OEE target bands;
- shop-specific pin clearances or locator recipes;
- ASME Y14.5 / AIAG MSA / SPC / PPAP / APQP edition-specific process detached from project/customer authority;
- 3-2-1 fixture topology as a universal solution;
- one manufacturing software/tool stack.

## Resulting OLEANDER extension

`oleander-skills/oleander-design-process/DFM_DFA_PROCESS_CAPABILITY_EXTENSION.md`

Core bounded transfer:

`FUNCTION / ASSEMBLY REQUIREMENT → CANDIDATE PROCESS → FEATURE / DATUM / INTERFACE → PROCESS-FEATURE CAPABILITY QUESTION → TOOLING / WORKHOLDING → MEASUREMENT FITNESS → PROCESS EVIDENCE → DFM/DFA CONSEQUENCE → DESIGN OR PROCESS REVISION → RETEST / RELEASE EVIDENCE → CLAIM CEILING`

## Adversarial regression required

The resulting Golden case must fail at least these shortcuts:
- valid CAD export = manufacturable;
- unnamed-process generic DFM rules;
- single good part = capable process;
- process capability from unqualified measurement evidence;
- 100% inspection = corrective action;
- capability threshold imported from external source as universal;
- tooling ordered while process/tolerance mismatch remains unresolved.

## Maturity

`EXTERNAL-SOURCE-DIGESTED / DOCUMENTED CANDIDATE EXTENSION / PRACTICE NOT YET RUN / CROSS-CONTEXT NOT ESTABLISHED / PROJECT USAGE NOT ESTABLISHED / NO PROMOTION`.