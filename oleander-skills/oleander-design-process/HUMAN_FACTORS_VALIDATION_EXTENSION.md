# Human Factors Validation Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-design-process`

Use when a design decision depends on fit between human capability and a physical/digital task: reach, clearance, grip, force, posture, repetition, task sequence, cognitive demand, error, timing or accessibility in use.

OLEANDER already contains Human Factors knowledge, interaction theory and ergonomics practices. This extension does **not** create a new Human Factors knowledge domain. It closes the execution gap from `population/task evidence → design dimension/behavior → prototype/task validation`.

## Core contract

`TARGET POPULATION → TASK + ENVIRONMENT + PPE / CONDITIONS → DEMAND DECOMPOSITION → HUMAN EVIDENCE SOURCE → DESIGN VARIABLE / RANGE → PROTOTYPE OR RUNTIME → REPRESENTATIVE TASK TEST → OBSERVED PERFORMANCE / ERROR / LOAD → DESIGN REVISION → REVALIDATION TRIGGER`

## Human-evidence rules

1. **There is no single “average user.”** Anthropometric and capability variables are distributions; the relevant population and variable must be named.
2. **Percentile direction follows failure mode.** Clearance, reach, force, visibility and adjustability can require different population edges. Never install one global 5th–95th percentile rule.
3. **Data source fit matters.** General-population anthropometry cannot automatically represent a project population, clothing/PPE condition, age group, disability context or task posture.
4. **Digital-human or render fit is predictive evidence only.** It can reveal collision/reach hypotheses; it cannot prove comfort, force tolerance, fatigue, pain, error or real-use success.
5. **Instrument scores are diagnostic carriers.** RULA/REBA/NIOSH/SUS/TLX/Fitts-style or other named methods answer bounded questions; the score is not a universal safety/usability certificate.
6. **Heuristic review ≠ task validation.** A visually coherent control layout can still fail during the actual sequence.
7. **Representative task evidence matters more than participant convenience.** Record why the tested people/tasks/conditions cover the decision risk.
8. **Observed error is system evidence.** Do not default to “user error” or training as the repair before testing design/task causes.
9. **Change reopens validation.** Tooling, geometry, load, PPE, environment, frequency, sequence or interface-state changes can invalidate prior human-fit evidence.

## Required output

- `target_population_and_exclusions`;
- `task_environment_condition`;
- `physical_cognitive_demand_map`;
- `human_data_or_method_source`;
- `design_variable_and_failure_direction`;
- `prediction_or_prototype_state`;
- `participant_task_condition_coverage`;
- `observed_performance_error_load`;
- `design_consequence_and_revision`;
- `revalidation_trigger`;
- `residual_HOLD`.

## Failure attacks

Reject or revise when:

- one 50th-percentile body is used as universal design authority;
- “5th–95th” is copied as a global rule without variable/population/failure-direction reasoning;
- a render pose or digital mannequin is treated as ergonomic proof;
- a standards table value is used without confirming population/task applicability and current edition when materially required;
- one expert heuristic review is called user validation;
- SUS or another summary score hides task errors, completion failures or unsafe workarounds;
- a convenience sample of designers/staff is called representative without scope;
- training, warnings or more breaks are prescribed before an avoidable design/task cause is tested;
- no revalidation occurs after a material task/geometry/load change.

## Transfer boundary

External source study:
- `wonsukchoi/domain-experts/roles/human-factors-engineer/SKILL.md` — MIT repository.
- OLEANDER Current Human Factors knowledge and existing NASA HIDH-derived Practice remain higher internal context for project routing.

Accepted: population variability; task-envelope first; physical/cognitive demand decomposition; method-to-demand matching; representative-user/task validation; error-as-system evidence; revalidation after change.

Rejected as universal OLEANDER truth: automatic percentile bands, fixed RULA/REBA/NIOSH/SUS action thresholds, universal vigilance timing, one Fitts target-size rule, ANSI/HFES values detached from population/context, or named software/digital-human tooling as proof.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.