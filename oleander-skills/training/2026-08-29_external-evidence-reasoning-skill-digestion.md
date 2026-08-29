# External Skill Digestion — Evidence Formation + System Coupling — 2026-08-29

Status: `SOURCE DIGESTION COMPLETE / CANDIDATE EXTENSIONS / PRACTICE OPEN / NO PROJECT USAGE / NO PROMOTION`

## Why this round changed after the knowledge-architecture repair

The Current Notion method toolbox no longer selects tools through a mechanical Design-Thinking stage sequence. Method routing now begins from decision purpose, evidence type, task class, risk, validation strength and traceability. Current knowledge also already owns Design Trade Study, A/B Controlled Experiment, Design Goal Contract and FMEA.

Therefore this round explicitly rejected generic “decision toolkit”, “A/B experimentation”, “FMEA” and large thinking-model catalogs as new Skill gaps. The material delta is narrower: evidence formation under multi-factor interaction, causal identification, quantitative uncertainty and system-interface coupling.

## Source 1 — K-Dense Experimental Design

Repository: `K-Dense-AI/scientific-agent-skills`

Files read:
- `LICENSE.md`
- `skills/experimental-design/SKILL.md`
- `skills/experimental-design/references/factorial_and_doe.md`

Rights: MIT.

Current comparison:
- Current A/B method covers controlled two-condition experiments.
- `oleander-research` covers source/evidence traceability but not multi-factor DOE structure, pseudoreplication, blocking, aliasing or interaction-aware run design.

Accepted delta:
- experimental unit before replicate count;
- randomization / blocking / replication as design decisions before collection;
- nuisance-factor and run-order control;
- factorial/interactions when combined factors matter;
- aliasing as a claim ceiling;
- screening / optimization / simulation design selected by question rather than fashion.

Rejected:
- biomedical/lab examples as OLEANDER defaults;
- fixed sample-size or factor-count heuristics;
- pyDOE3/Python implementation as required tooling;
- one DOE family as universal;
- statistical significance promised before execution.

Target: `oleander-research/EXPERIMENTAL_DESIGN_DOE_EXTENSION.md`.

## Source 2 — Magnus Data Scientist / Causal Inference

Repository: `magnus919/agent-skills`

Files read:
- `LICENSE.md`
- `data-scientist/SKILL.md`
- `data-scientist/references/causal-inference-framework.md`

Rights: MIT.

Current comparison:
- Current General Design Knowledge now contains causal hypothesis / discriminating-test reasoning at Design Goal level, but no dedicated causal-identification method for confounding, collider/mediator roles, observational identification or sensitivity.
- A/B experiment remains an upstream evidence-generation option, not the complete causal layer.

Accepted delta:
- data-generating/intervention process before estimator;
- DAG/assumption carrier;
- confounder vs mediator vs collider/selection distinction;
- explicit identification strategy;
- counterfactual discipline;
- sensitivity, placebo/negative-control and rival-explanation testing;
- causal conclusion bounded by identification assumptions.

Rejected:
- fixed IV F-statistic rule;
- fixed balance thresholds;
- one favored matching/weighting/DiD/RDD estimator;
- domain-specific economic/medical assumptions;
- regression/feature-importance as causal authority.

Target: `oleander-research/CAUSAL_IDENTIFICATION_EXTENSION.md`.

## Source 3 — K-Dense Uncertainty and Units

Repository: `K-Dense-AI/scientific-agent-skills`

Files read:
- `LICENSE.md`
- `skills/uncertainty-and-units/SKILL.md`

Rights: MIT.

Current comparison:
- Current Technical Drawing / 3D / Delivery QC preserve units and dimension authority.
- The missing layer is upstream quantitative evidence: measurement model, calibration/traceability, correlated uncertainty, propagation and decision impact.

Accepted delta:
- measurand first;
- units kept attached to quantity meaning;
- measurement model before calculation;
- uncertainty components and correlation;
- sensitivity contribution;
- nonlinear/Monte-Carlo check where linearization is weak;
- physical plausibility separate from dimensional consistency;
- uncertainty compared with decision/tolerance rather than reported decoratively.

Rejected:
- fixed coverage factor (`k=2`) as habit;
- fixed rounding/significant-figure policy as universal;
- exact Python library/version stack;
- CODATA/software version as permanent project authority;
- scientific dimensionless-group catalog as generic design checklist;
- GUM/JCGM mechanics where another Current professional standard controls.

Target: `oleander-research/MEASUREMENT_UNCERTAINTY_EXTENSION.md`.

## Source 4 — K-Dense Systems Engineer

Repository: `K-Dense-AI/scientific-agents`

Files read:
- `LICENSE.md`
- `scientific-agents/systems-engineer/AGENTS.md`

Rights: MIT.

Cross-check only:
- `d-wwei/systems-thinking/SKILL.md`, `anti-patterns.md`, `cognitive-protocol.md` tree reviewed.
- No repository license found in inspected tree. Classification: `LICENSE-UNCLEAR / HIGH-LEVEL COMPARISON ONLY`; no source prose/framework package transferred.

Current comparison:
- `oleander-design-process` already owns systems analysis, requirement/evidence coverage and design consequences.
- Current Trade Study and FMEA exist.
- Missing execution delta is explicit interface contract, coupling structure, integration sequencing and failure-split when local components individually pass.

Accepted delta:
- system boundary before local optimization;
- interface content including units/timing/state/ownership when material;
- bidirectional requirement→object/interface→verification trace;
- coupled-block/iteration visibility;
- rival explanations for integration failure;
- system-level verification for emergent behavior;
- verification vs validation kept distinct.

Rejected:
- ISO/IEC/IEEE 15288 lifecycle as mandatory OLEANDER process;
- V-model as universal project structure;
- DOORS/Jama/Cameo/PLM stack as required tooling;
- PDR/CDR/ORR sequence;
- fixed risk matrices or weight-perturbation percentages;
- domain-specific safety/compliance rules outside their jurisdiction.

Target: `oleander-design-process/SYSTEM_INTERFACE_COUPLING_EXTENSION.md`.

## Explicit no-delta / do-not-redigest list after Current repair

Do not create new generic Skills for:
- Design Trade Study / decision matrix;
- A/B controlled experiment;
- Design Goal Contract / outcome framing;
- FMEA;
- generic design-thinking stage toolbox;
- generic “30 mental models” catalog.

These are already Current, or the catalog form conflicts with Current decision/evidence/risk-based method routing.

## Proposed Golden regressions

- `SK-RES-003`: multi-factor experiment with pseudoreplication / batch confounding / OFAT interaction blindness.
- `SK-RES-004`: observational correlation with mediator/collider/confounder confusion promoted to causality.
- `SK-RES-005`: precise-looking measured dimension without method/traceability/material uncertainty.
- `SK-DES-007`: all components pass independently but an unverified unit/timing/state interface breaks integrated behavior.

## Maturity / adoption boundary

All four extensions remain:

`DOCUMENTED CANDIDATE / EXTERNAL SOURCE DIGESTED / GOLDEN REGRESSION PENDING UNTIL CENTRAL CORPUS WRITE + CI / PRACTICE OPEN / NO PROJECT USAGE / NO CURRENT L5 PROMOTION`.

This round optimizes the execution layer around the repaired knowledge logic. It does not re-author the user's Current Notion thinking model and does not promote external Skills as knowledge authority.