# Material Selection / Failure Analysis Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when material/process choice or a physical failure materially changes a product, spatial element, mechanism, finish or service decision. This extension closes the gap between material-property references and real-part behavior.

It does **not** replace Current FMEA. FMEA predicts/organizes possible failure modes; material failure analysis asks what physical mechanism actually explains an observed or anticipated failure and what material/process/geometry change follows.

## Core contract

`FUNCTION / LOAD / ENVIRONMENT / LIFE → FAILURE MODE / MECHANISM HYPOTHESES → MATERIAL + PROCESS + SECTION + FINISH AUTHORITY → AS-DESIGNED vs AS-BUILT STATE → PHYSICAL / MICROSTRUCTURAL / TEST EVIDENCE → MECHANICS / PROPERTY RECONCILIATION → ROOT-CAUSE BOUNDARY → CORRECTIVE DESIGN / PROCESS ACTION → RETEST / INSPECTION → CLAIM CEILING`

## Material reasoning rules

1. **Coupon property ≠ part behavior.** Datasheet/handbook values must be translated through real geometry, surface, thickness, process, temperature, environment, defects and load history when these affect the decision.
2. **Failure mechanism before preferred calculation.** Fatigue, brittle/ductile overload, wear, corrosion, creep, delamination, environmental cracking and process defect do not share one analysis route.
3. **As-built state matters.** Material cert, heat/process record, dimensions, surface finish, bonding/fastening condition and supplier lot can falsify a design-only root-cause story.
4. **Observed morphology is evidence, not a label.** Fracture/wear/corrosion features should support or weaken mechanism hypotheses; do not call a mode from appearance alone without reconciliation to loads/history/material state.
5. **Static pass does not prove cyclic life.** One FEA stress image, yield check or nominal strength value cannot substitute for duty-cycle/fatigue/fracture evidence when the failure is time/cycle dependent.
6. **Selection is multi-constraint.** Mechanical performance, environment, process, section, finish, serviceability, cost/supply and failure consequence may all matter; one highest property cannot decide the material by itself.
7. **Calculation must reconcile with reality.** If the predicted failure mode/life/margin conflicts with observed field/test evidence, reopen inputs/model/mechanism before declaring root cause.
8. **Corrective action needs a proving consequence.** Geometry/material/process/inspection change must state what failure mechanism it changes and what retest/inspection will verify it.

## Required output

- `function_load_environment_life`;
- `failure_mode_mechanism_hypotheses`;
- `material_process_section_finish_authority`;
- `as_designed_as_built_comparison`;
- `observed_test_microstructural_evidence`;
- `governing_property_or_mechanics_relation`;
- `reconciliation_with_history`;
- `root_cause_and_rival_explanations`;
- `corrective_action`;
- `retest_inspection_plan`;
- `residual_HOLD`.

## Failure attacks

Reject or revise when:

- a handbook/coupon strength is treated as guaranteed real-part capacity;
- the highest-strength/lightest material is selected without the actual failure/environment/process constraints;
- “fatigue” or “corrosion” is named without mechanism-bearing evidence;
- one static FEA or yield factor is used to clear cyclic durability;
- material/process nonconformance is never compared with drawing/spec authority;
- an external Goodman/Ashby/Marin/Jominy/API/ASTM recipe or numeric threshold is installed as universal OLEANDER truth;
- a fracture photograph is called a root-cause proof without load/material/process reconciliation;
- FMEA occurrence/severity values are used as physical failure evidence;
- a corrective action is accepted without retest/inspection or without stating which mechanism is changed.

## Transfer boundary

External source study:
- `wonsukchoi/domain-experts/roles/materials-engineer/SKILL.md` — MIT repository.

Accepted: real-part vs coupon distinction; load/environment/life first; mechanism-specific analysis; as-designed vs as-built/material-process verification; observed failure morphology as bounded evidence; reconciliation of calculation with field history; corrective action tied to retest.

Rejected as universal OLEANDER truth: fixed fatigue/endurance correction formulas, default Goodman/Gerber choice, fixed fracture-toughness fractions, section-size heuristics, one Ashby index, specific alloy rankings/heat-treatment recipes, or API/ASTM domain thresholds without Current source and project applicability.

## Co-routing boundary

- Population/time/service-life evidence → `RELIABILITY_DURABILITY_EVIDENCE_EXTENSION.md`.
- Measurement/calibration/uncertainty → `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md`.
- Geometry/drawing/manufacturing proof → 3D / Technical Drawing / VALIDATION owner.
- Hazard prioritization → Current FMEA or actual safety method; material failure analysis does not replace hazard analysis.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.