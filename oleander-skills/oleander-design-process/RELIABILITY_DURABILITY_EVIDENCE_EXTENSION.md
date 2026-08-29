# Reliability / Durability Evidence Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a physical/digital-service design claim depends on surviving a stated duty cycle, environment, population or service life. This extension prevents one clean prototype, one final inspection or one generic MTBF number from being promoted into durability/reliability authority.

It does **not** replace Current FMEA. FMEA identifies and prioritizes failure modes; this extension asks what time/population/environment evidence can support a reliability or durability claim and how failures feed design revision.

## Core contract

`DESIGN OBJECT / FAILURE DEFINITION → DUTY + ENVIRONMENT + LIFE CONTEXT → POPULATION / CONFIGURATION → FAILURE-MECHANISM HYPOTHESES → EVIDENCE CLASS → TEST / FIELD PLAN → CENSORING + MIXTURE / CONFIGURATION RECORD → RESULT + UNCERTAINTY → ROOT-CAUSE / CORRECTIVE ACTION → RETEST / FIELD FEEDBACK → CLAIM CEILING`

## Evidence classes

Keep these distinct:

- **Predicted**: model/handbook/simulation based; bounded by input and mechanism assumptions.
- **Screened**: stress/screening found defects or margins; not a life demonstration by itself.
- **Demonstrated**: a defined test article/population passed a stated reliability/durability test under stated conditions.
- **Field-observed**: service/return evidence tied to actual configuration, duty and population.

`PREDICTED ≠ DEMONSTRATED ≠ FIELD-VALIDATED`.

## Required reasoning

1. Define failure: total loss, degraded function, cosmetic wear, unacceptable drift, service interruption or another observable condition.
2. Define the duty/environment that makes the claim meaningful: cycles, duration, load spectrum, temperature, humidity, contamination, handling, software state or service pattern as relevant.
3. Preserve configuration and cohort identity. Supplier lot, material revision, firmware/build, geometry revision and field context cannot be mixed silently.
4. Link proposed test stress to the intended field mechanism. Accelerating a different mechanism does not accelerate the intended evidence.
5. Treat censored/suspended units and no-failure units as part of the evidence structure; do not average only failed units.
6. Separate early-life defect, random/service variation and wear-out when evidence supports that distinction; do not use a generic bathtub curve as proof.
7. Tie any reliability result back to a material design decision, process/control change, service plan or explicit risk acceptance.
8. Re-test after a material corrective action; a closed ticket or updated drawing is not corrective-action effectiveness evidence.

## Required output

- `object_and_failure_definition`;
- `duty_environment_life_contract`;
- `population_configuration_cohort_ledger`;
- `failure_mechanism_hypotheses`;
- `evidence_class`;
- `test_or_field_plan`;
- `censoring_mixture_and_exclusion_rules`;
- `result_uncertainty_and_limitations`;
- `root_cause_or_rival_explanations`;
- `corrective_action_and_retest`;
- `claim_ceiling / residual HOLD`.

## Failure attacks

Reject or revise when:

- final inspection PASS is called long-life reliability;
- MTBF/MTTF/B10 or failure rate is stated without population, conditions and evidence basis;
- a lab stress profile is borrowed without mechanism/duty equivalence;
- failed units are excluded because they are inconvenient rather than because a documented competing-risk/configuration rule applies;
- mixed supplier lots or revisions are fitted as one homogeneous population without checking mixture;
- accelerated test passes but field failure activates another mechanism and the contradiction is ignored;
- FMEA occurrence numbers are treated as demonstrated reliability data;
- HALT/screening is treated as a pass/fail life certificate;
- a test run on one configuration is silently inherited by a changed material, geometry, firmware or process.

## Transfer boundary

External source study:
- `K-Dense-AI/scientific-agents/scientific-agents/reliability-engineer/AGENTS.md` — repository MIT.

Accepted: failure definition; reliability as time/population/conditions; mechanism-first reasoning; duty/environment mapping; censored and mixture population awareness; predicted vs demonstrated vs field evidence; accelerated-test mechanism matching; failure feedback and corrective-action retest.

Rejected as universal OLEANDER truth: fixed confidence targets, fixed Weibull/MTBF recipes, generic MIL/automotive/medical profiles, one acceleration equation, fixed screening stress, mandatory reliability software, or domain-specific release thresholds without Current project authority.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.