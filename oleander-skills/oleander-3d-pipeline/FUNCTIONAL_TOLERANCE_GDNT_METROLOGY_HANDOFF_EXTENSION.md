# Functional Tolerance / GD&T-GPS / Metrology Handoff Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-3d-pipeline`

Use when fit, location, orientation, profile, runout, surface relation, free-state behavior or tolerance accumulation materially affects a part/assembly and the CAD model must hand that design intent to Technical Drawing / MBD-PMI / metrology / manufacturing validation without losing function.

This extension does **not** make `oleander-3d-pipeline` a metrology lab or engineering-signoff owner. It governs the traceable handoff from functional geometry to a feature-level verification contract.

## Core contract

`FUNCTION / FAILURE MODE → ASSEMBLY / SERVICE RELATION → FUNCTIONAL DATUM STRATEGY → CONTROLLED FEATURE / INTERFACE → BASIC / SIZE / FORM / ORIENTATION / LOCATION / PROFILE RELATION → TOLERANCE STACK / VARIATION MODEL → GD&T-GPS / PMI EXPRESSION → INSPECTION FEATURE MAP → MEASUREMENT METHOD + DATUM SIMULATION → UNCERTAINTY / DECISION RULE HANDOFF → RESULT / NONCONFORMANCE → DESIGN OR PROCESS RETURN`

## Core separations

`DATUM LABEL ≠ FUNCTIONAL DATUM STRATEGY`

`NOMINAL DIMENSION ≠ ACCEPTABLE VARIATION`

`SIZE PASS ≠ POSITION / ORIENTATION / PROFILE PASS`

`PMI PRESENT ≠ PMI SEMANTICS VALID`

`CMM REPORT ≠ MEASUREMENT AUTHORITY WITHOUT METHOD / DATUM / TRACEABILITY / UNCERTAINTY`

`MEASUREMENT PASS ≠ MANUFACTURING PROCESS CAPABLE`

`GD&T SYMBOLS ≠ ENGINEERING SIGNOFF`

## Functional-tolerance rules

1. **Function comes before the callout.** Start from the failure or performance consequence: bind, leak, looseness, collision, optical/visual misalignment, uneven gap, seal failure, runout, service interference or another project-specific condition.
2. **Datums derive from real locating relations.** Record which surfaces/axes/planes/features establish the part coordinate frame in assembly, use, inspection or service and why their precedence matters.
3. **Control type follows the geometric relation.** Keep size, form, orientation, location, profile and runout conceptually distinct. Do not replace a relation-control problem with extra plus/minus dimensions because the drawing looks simpler.
4. **Tolerance stack is a design model, not a spreadsheet ritual.** Identify contributors, direction/sensitivity, correlations, assembly states and whether the decision needs deterministic worst-case, statistical variation, Monte Carlo or another justified method. No method is universal.
5. **Material-condition / envelope / modifier semantics are standard-dependent.** ASME Y14.5 and ISO GPS do not share every rule. Name the governing Current standard or keep the exact interpretation on HOLD.
6. **MBD/PMI must survive exchange semantically.** STEP/AP242/JT/native PMI presence is not sufficient; datum identities, modifiers, feature associations and revision must remain interpretable after exchange when they are claim-bearing.
7. **Inspection maps to the controlled characteristic.** A two-point diameter, pin gauge, height gauge, CMM scan or optical system can answer different questions. Choose the method that actually observes the required feature relation.
8. **Datum simulation / alignment is part of the measurement method.** A result referenced to a convenient best-fit frame may disagree with the design's functional datum frame without either dataset being numerically corrupt.
9. **Sampling/filtering can change the observed form.** When profile/form/surface is material, point density, scan path, fitting method, filter/outlier treatment and inaccessible regions remain part of the evidence boundary.
10. **Uncertainty and decision rules return from Research / metrology authority.** The inspection plan must declare when uncertainty can affect conforming/nonconforming classification; do not invent a universal guard band.
11. **Revision identity is mandatory.** CAD/PMI/drawing/balloon/inspection program/report must be traceable to the same relevant object/configuration revision before a PASS can propagate.
12. **Nonconformance must preserve rival causes.** Possible design tightness, datum interpretation, real process shift, fixture/workholding, measurement method, environment and software/program changes remain separable until evidence resolves them.

## Required output

- `function_and_failure_consequence`;
- `assembly_service_relation`;
- `functional_datum_strategy`;
- `controlled_feature_interface`;
- `control_class_and_standard_authority`;
- `tolerance_stack_or_variation_model`;
- `gdt_gps_pmi_expression_state`;
- `inspection_feature_map`;
- `measurement_method_and_datum_simulation`;
- `sampling_filtering_access_limits`;
- `measurement_uncertainty_decision_rule_handoff`;
- `revision_configuration_binding`;
- `result_nonconformance_and_rival_causes`;
- `design_process_return`;
- `engineering_metrology_manufacturing_holds`.

## Failure attacks

Reject or revise when:

- the datum sequence is chosen only because the surfaces are easy to click or clamp;
- every relation is expressed as independent ± dimensions even when the functional relation is positional/orientational/profile-based;
- a hole diameter pass is called assembly-location pass without checking the governing location relation;
- tolerance-stack contributors are treated as independent by default;
- RSS is used automatically because production is high-volume, or worst-case automatically because it is “safer”;
- ASME and ISO GPS semantics are mixed without a translation/authority statement;
- a PMI icon or STEP AP242 export is called semantic proof without reopen/association checking;
- a CMM best-fit alignment replaces the product datum reference without disclosure;
- one hand-gage reading substitutes for a full-surface/profile/location control;
- point density, filtering or inaccessible regions materially affect a profile/form claim but are omitted;
- a report says PASS while calibration/traceability/uncertainty/decision-rule state can change the verdict;
- inspection report revision differs from the authoritative design revision;
- a borderline dimensional failure is attributed directly to machining before measurement/datum/program causes are tested.

## Transfer boundary

External source study:
- `K-Dense-AI/scientific-agents/scientific-agents/precision-engineering-specialist/AGENTS.md` — repository MIT.

Accepted material delta:
- GD&T/GPS as functional geometry rather than decorative notation;
- separation of size/form/orientation/location/profile/runout controls;
- datum reference frame and datum simulation as part of the design↔measurement contract;
- feature-level measurement planning rather than generic dimensional checking;
- task-specific metrology capability / uncertainty awareness;
- PMI/CMM/inspection revision binding;
- nonconformance diagnosis that separates design, process and measurement causes;
- design-for-metrology feedback when a feature is difficult or ambiguous to verify.

Rejected as universal OLEANDER truth:
- fixed guard-band or uncertainty/tolerance percentage;
- fixed temperature correction values or soak times;
- fixed CMM point density / stylus / filter settings;
- one ASME Y14.5 or ISO GPS revision as global authority;
- fixed MMC/LMC implementation examples detached from the governing standard;
- automatic deprecation/substitution of callouts without project/customer authority;
- Cpk/GR&R/SPC thresholds;
- named CMM/GD&T software as proof;
- AS9102/PPAP report structure as universal release route.

## Co-routing boundary

- Functional source geometry, native CAD, units, datums and assembly relations → existing `PARAMETRIC_CAD_GEOMETRY_VALIDATION_EXTENSION.md` first.
- DFM/DFA/process capability → `oleander-design-process/DFM_DFA_PROCESS_CAPABILITY_EXTENSION.md`.
- Measurement model, calibration, traceability, uncertainty → `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md`.
- Drawing/annotation carrier execution → Technical Drawing PR #172 Candidate lineage. This extension must not create a parallel Technical Drawing implementation on main.
- Released file/package integrity → `oleander-delivery-qc`.
- Signed dimensional acceptance, accredited metrology, manufacturing approval and customer-standard interpretation remain external professional/project authority.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.