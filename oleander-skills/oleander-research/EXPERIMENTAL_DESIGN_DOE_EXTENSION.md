# Experimental Design / DOE Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-research`

Use this extension when a design/research decision depends on comparing several factors, combinations, operating conditions or treatments and a simple current A/B experiment cannot isolate interactions, nuisance variation or independent replication.

This extension does **not** replace Current `KN-METHOD-AB-EXPERIMENT-001`. A/B remains appropriate for a genuinely two-condition controlled comparison. This extension begins where the evidence question becomes multi-factor, nested, blocked, repeated, sequential or interaction-sensitive.

## Core contract

`DECISION / CLAIM → EXPERIMENTAL UNIT → FACTORS / TREATMENTS → RESPONSE / MEASUREMENT → NUISANCE FACTORS → DESIGN FAMILY → RANDOMIZATION / BLOCKING / REPLICATION → RUN ORDER / ASSIGNMENT RECORD → EXECUTION → ANALYSIS HANDOFF → EVIDENCE BOUNDARY`

## Before choosing a design

Record:

- the decision this evidence must support;
- the independent experimental unit — the level at which treatment is actually assigned;
- factors and factor levels/ranges that are authorized by Current source or explicit experiment assumption;
- response variables and measurement authority;
- known nuisance factors such as batch, day, operator, site, device, material lot or position;
- which interactions could plausibly change the decision;
- feasibility/safety boundaries for combinations;
- whether the task is screening, interaction estimation, optimization, repeated-measures comparison or simulation-space exploration.

Do not choose factorial, fractional, response-surface or other DOE structures because they are sophisticated. The design must follow the decision question and unit structure.

## Evidence design rules

1. **Independent unit before replicate count.** Repeated readings from one treated object do not automatically create independent experimental replication.
2. **Nuisance variation must be designed around before data collection.** Randomize, block, stratify or explicitly retain the confounding/HOLD; do not repair a structurally confounded experiment only in post-analysis.
3. **Run order is evidence metadata.** When drift, warm-up, fatigue, aging, weather, operator learning or material lot can matter, assignment/run order must be reproducible and inspectable.
4. **Interactions matter when factors act together.** Do not serially run one-factor-at-a-time comparisons and claim that the result establishes the best combined setting when interactions were not tested.
5. **Aliasing is a claim ceiling.** A reduced/fractional design may be efficient, but effects that remain structurally confounded cannot be named as uniquely identified causes.
6. **Optimization follows model fitness.** A two-level comparison cannot by itself prove curvature or an interior optimum.
7. **Simulation DOE is not physical validation.** Space-filling or parameter-sweep evidence remains bounded to the model and its assumptions until reality is checked.

## Required output

For a material DOE task, produce:

- `decision_question`;
- `experimental_unit`;
- `factor_response_ledger`;
- `nuisance_factor_ledger`;
- `design_choice_and_reason`;
- `randomization_blocking_replication_contract`;
- `run_or_assignment_schedule` with reproducible identity/seed where applicable;
- `interaction_or_alias_boundary`;
- `measurement_authority`;
- `analysis_handoff`;
- `claim_ceiling / residual HOLD`.

## Failure attacks

Reject or revise when:

- repeated measurements are counted as independent samples;
- all A conditions are run before all B conditions while time/batch can matter;
- one factor is varied at a time while a decision depends on interactions;
- a fractional/screening design is interpreted as if all effects were separately identified;
- unsafe or physically impossible factor combinations are generated because a generic DOE matrix says so;
- source/tool defaults become project parameters without authority;
- statistical significance is promised before the experiment runs;
- experiment runtime success is promoted as design/project success.

## Transfer boundary

External source study:
- `K-Dense-AI/scientific-agent-skills/skills/experimental-design/SKILL.md` — MIT;
- core DOE reference `references/factorial_and_doe.md` — same MIT repository.

Accepted: decision-first experiment structure, independent unit, randomization, blocking, replication, multi-factor interaction awareness, aliasing boundary, reproducible run order.

Rejected as universal OLEANDER truth: biomedical examples, sample-size heuristics, fixed factor counts, specific software/library requirements, a universal DOE family, or any numeric screening/optimization threshold without Current source and context.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.