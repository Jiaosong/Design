# Measurement Uncertainty / Units Extension

Status: `CANDIDATE EXTENSION / SUPPORT ONLY / NO CURRENT L5 PROMOTION`

Owner: `oleander-research`

Use when a design, field, prototype, CAD, production, color, environmental or performance claim depends on measured or computed quantitative evidence. This extension governs the evidence meaning of a number before that number is visualized, dimensioned, simulated or released.

Delivery QC may later check that a released file carries the right units/metadata. It does not replace this upstream evidence contract.

## Core contract

`MEASURAND / QUANTITY → MEASUREMENT MODEL → METHOD / INSTRUMENT / SOURCE → UNITS → CALIBRATION / TRACEABILITY → REPEATABILITY / RESOLUTION → UNCERTAINTY COMPONENTS / CORRELATION → PROPAGATION / SENSITIVITY → PLAUSIBILITY CHECK → RESULT + UNCERTAINTY → CLAIM / DECISION BOUNDARY`

## Evidence rules

1. **Name the measurand before reporting digits.** Define what quantity is being measured/computed, under what condition and at what object/state.
2. **Units stay attached to meaning.** A naked magnitude or silent unit conversion cannot become dimensional authority.
3. **Method and traceability travel with the result.** Instrument, source, calibration/reference or calculation lineage must be recoverable at the fidelity required by the claim.
4. **Resolution is not uncertainty.** Display precision, software decimal places and instrument resolution do not establish measurement confidence.
5. **Uncertainty sources must be modeled.** Include repeatability and material Type-B-like sources such as calibration/specification/boundary assumptions when relevant; do not silently omit a correction because its estimated center is zero.
6. **Correlation matters.** Shared instruments, shared calibration standards, fitted parameters or common source geometry can make inputs non-independent. Do not combine them as independent by habit.
7. **Propagation must fit the model.** Linear propagation can fail for nonlinear, bounded or strongly asymmetric cases. Use simulation/Monte-Carlo or another appropriate check when the linear approximation is not defensible.
8. **Plausibility is separate from dimensional consistency.** A result can have correct units and still be impossible or outside the model's valid regime.
9. **Uncertainty affects the decision.** Compare the uncertainty/range with the design tolerance, option difference, acceptance criterion or decision boundary. Do not report uncertainty as decorative metadata.

## Required output

- `measurand_and_condition`;
- `method_instrument_source`;
- `units_and_conversion_lineage`;
- `calibration_traceability_state`;
- `measurement_model`;
- `uncertainty_component_ledger`;
- `correlation_assumptions`;
- `propagation_or_sensitivity_method`;
- `plausibility_or_regime_check`;
- `reported_result_and_uncertainty_meaning`;
- `decision_impact`;
- `claim_ceiling / residual HOLD`.

## Failure attacks

Reject or revise when:

- extra decimal places are treated as extra evidence;
- CAD/export/viewbox units are inferred without embedded/external authority;
- instrument resolution is reported as total uncertainty;
- a shared calibration or derived parameter is duplicated and treated as independent;
- a linear error-propagation result crosses impossible bounds and no nonlinearity check is performed;
- a generic coverage factor or confidence convention is applied by habit without its assumptions;
- output looks dimensionally valid but magnitude/regime is implausible;
- uncertainty is smaller than the option difference only because a major source was omitted;
- numerical readback is promoted into engineering/field approval.

## Transfer boundary

External source study:
- `K-Dense-AI/scientific-agent-skills/skills/uncertainty-and-units/SKILL.md` — MIT.

Accepted: explicit measurement model, unit continuity, uncertainty budget thinking, correlation awareness, sensitivity coefficients, nonlinear/Monte-Carlo cross-check, calibrated reporting and plausibility checks.

Rejected as universal: fixed coverage factor, fixed significant-figure rule, exact library/software versions, CODATA version as permanent OLEANDER constant source, scientific-domain dimensionless-group catalog as generic design checklist, or GUM/JCGM implementation details where a different current professional standard controls.

Primary quantitative standards/authority remain task-specific (e.g. current metrology/field/engineering standard, certificate, supplier or project requirement).

## Candidate claim

`A MEASURED OR COMPUTED NUMBER IS NOT DIMENSIONAL / PERFORMANCE AUTHORITY UNTIL ITS QUANTITY, METHOD, UNIT, TRACEABILITY AND MATERIAL UNCERTAINTY BOUNDARY ARE KNOWN.`

## Maturity

`DOCUMENTED CANDIDATE EXTENSION / EXTERNAL-SOURCE-DIGESTED / PRACTICE NOT YET RUN / NO PROJECT USAGE / NO PROMOTION`.