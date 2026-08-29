# Causal Identification Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-research`

Use when a project or knowledge claim asks whether changing X caused, will cause, or is a material driver of Y. This extension protects OLEANDER from promoting correlation, temporal sequence, regression fit, before/after coincidence or visually persuasive diagrams into causal evidence.

This extension complements Current Design Goal / A-B / Trade Study methods. It does not replace them: goals say what outcome matters, experiments can generate evidence, trade studies compare alternatives; causal identification asks whether the evidence can support a cause-effect claim at all.

## Core contract

`CAUSE QUESTION → DATA-GENERATING / INTERVENTION PROCESS → CAUSAL ASSUMPTION MODEL → TREATMENT / EXPOSURE / OUTCOME → CONFOUNDERS / MEDIATORS / COLLIDERS / SELECTION → IDENTIFICATION STRATEGY → FALSIFICATION / SENSITIVITY → BOUNDED CAUSAL CONCLUSION`

## Causal question gate

Before analysis, record:

- the exact intervention/exposure and outcome;
- time ordering and plausible mechanism;
- what assigns or changes the intervention;
- plausible common causes;
- variables that may sit on the causal path rather than before it;
- selection/filtering mechanisms that determine what becomes observed;
- which relevant variables are unobserved or unavailable;
- what counterfactual comparison the claim implicitly requires.

A DAG or relation graph is an explicit assumption carrier, not proof. Every causal arrow must be treated as an assumption/evidence claim that can be challenged.

## Identification rules

1. **Correlation is not an identification strategy.** Association, regression, clustering, similarity or temporal coincidence alone cannot establish intervention effect.
2. **Adjustment is not automatically safer.** Controlling for a mediator can remove part of the effect being studied; conditioning on a collider/selection variable can introduce bias.
3. **Randomization earns a different claim class.** If treatment assignment is genuinely randomized and execution integrity holds, use that design as the primary identification route rather than observational adjustment.
4. **Observational causal claims need an explicit strategy.** Examples may include measured-confounder adjustment, natural-experiment structures, discontinuity, difference-in-differences, instruments or matched/synthetic comparisons, but the method name does not prove its assumptions.
5. **Identification assumptions remain visible.** Positivity/overlap, no interference, parallel trends, exclusion restrictions, continuity or no-unmeasured-confounding assumptions must remain connected to the claim when relevant.
6. **Sensitivity is part of the result.** Ask what plausible hidden bias, alternative timing, negative control, placebo condition or omitted variable would overturn the conclusion.
7. **Design consequence follows claim strength.** If causal identification is weak, the design may still use the finding as a bounded hypothesis/risk signal, but not as a proven driver.

## Required output

- `causal_question`;
- `intervention_outcome_definition`;
- `assumption_graph_or_relation_ledger`;
- `confounder_mediator_collider_selection_classification`;
- `available_vs_unobserved_variables`;
- `identification_strategy`;
- `assumption_failures_or_rival_explanations`;
- `falsification_sensitivity_plan_or_result`;
- `causal_claim_ceiling`;
- `design_consequence / HOLD`.

## Failure attacks

Reject or revise when:

- a before/after improvement is called causal without a credible comparison;
- regression coefficient or feature importance is renamed as causal effect;
- every available variable is adjusted for without role classification;
- a mediator or collider is treated as a generic confounder;
- a causal diagram is presented as empirical proof;
- one observational method's diagnostic threshold is promoted as universal truth;
- a null statistical result is described as proof of no causal effect;
- causality is claimed while material alternative explanations remain untested and unbounded.

## Transfer boundary

External source study:
- `magnus919/agent-skills/data-scientist/SKILL.md` — MIT;
- `data-scientist/references/causal-inference-framework.md` — same MIT repository.

Accepted: data-generating-process first, explicit causal assumptions, confounder/collider/mediator distinction, identification strategy, counterfactual discipline, sensitivity/falsification and bounded causal language.

Rejected as universal: fixed instrumental-variable strength cutoffs, fixed covariate-balance thresholds, one favored causal estimator, medical/economic domain assumptions, or statistical recipes detached from Current design/research context.

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.