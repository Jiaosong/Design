# OLEANDER 3D Bounded Causal Iteration Protocol v1

Status: CANDIDATE / reusable 3D Skill training delta

Benchmark provenance: Porsche 911 992.2 V68–V72.
- V68 showed an iteration can alter topology without improving the declared boundary defect and can regress protected normals/folds.
- V71 materially reduced complete rear-aperture XZ straddles `118 → 34` while preserving bounds/folds/manifoldness.
- V72 continued the same locked operation under an explicit iteration cap: `118 → 34 → 4 → 2 → 2`; the first three cycles materially reduced the target defect and the fourth cycle immediately stopped on stagnation.

## Core rule

`REPEATED_EXECUTION ≠ JUSTIFIED_ITERATION`

`CONTINUE only while TARGET DEFECT MATERIALLY IMPROVES + PROTECTED INVARIANTS PASS + ITERATION BUDGET REMAINS`

`ZERO / STAGNATION / REGRESSION / MAX_BUDGET → STOP`

Use this protocol when the same causally bounded operation may need multiple passes: local topology refinement, controlled solver relaxation, sparse relation correction, projection fitting, convergence repair, or other repeatable 3D operations.

## 1. Declare the iteration contract before repeating

Record:
- candidate/baseline identity;
- semantic target defect or metric;
- target direction (`LOWER_IS_BETTER`, `HIGHER_IS_BETTER`, `ZERO_REQUIRED`, or an explicit bounded relation);
- operation family that is allowed to repeat;
- parameters that remain locked across cycles;
- protected invariants;
- material-improvement rule;
- maximum additional cycles;
- stop conditions;
- rollback/LKG.

Do not create an iteration loop only because the previous result was unsatisfactory.

## 2. One causal question per loop

Every cycle must address the same declared causal question.

If the semantic owner, representation, operator family, target carrier, camera, reference, or protected geometry changes, close the current iteration receipt and start a new experiment/reclassification.

### FORBIDDEN
- changing several unrelated Source families while calling them iterations of one experiment;
- widening tolerances and moving target boundaries in the same convergence loop;
- changing measurement definition mid-loop to manufacture improvement;
- continuing after the failure has moved from Parameter to Relation / Geometry / Topology / Architecture / Evidence.

## 3. Material improvement is explicit

For each cycle record target metric before/after and whether the delta satisfies the declared material-improvement rule.

Examples:
- count defect: `after < before`;
- RMSE: improvement must exceed a declared epsilon, not merely floating-point noise;
- clearance: move into/through a declared range;
- topology conflict: conflict count must decrease without protected regression.

A cycle that executes but does not materially improve the target is `STAGNATION`, even if geometry changes.

## 4. Protected invariants have veto power

Each cycle checks the applicable invariants, for example:
- Source digest/control count;
- world bounds / hard points / axles;
- folds / normal reversals / manifoldness;
- previously locked SIDE/FRONT/REAR metrics;
- hierarchy / assembly / interface ownership;
- camera/evidence lock;
- units / origin / dependency identity.

Any hard invariant regression stops the loop immediately. A better target metric cannot average away a protected regression.

## 5. Required stop conditions

At minimum declare:
- `TARGET_REACHED`
- `STAGNATION_NO_MATERIAL_IMPROVEMENT`
- `PROTECTED_INVARIANT_REGRESSION`
- `MAX_ITERATION_BUDGET_REACHED`

Additional domain-specific stop conditions are allowed.

The first applicable hard stop ends the loop. Do not run “one more try” without opening a new evidence-backed experiment.

## 6. Iteration budget

Set a finite cycle limit before execution. The limit is an execution-safety boundary, not a promise that all cycles should be consumed.

When the target is still unresolved at the limit or at stagnation:
- preserve the best comparable LKG;
- classify remaining failure;
- route to Parameter / Relation / Geometry / Topology / Architecture / Evidence;
- if needed, change representation in a new experiment.

## 7. Negative convergence is useful evidence

A monotonic sequence that stalls can still reveal the remaining operator/representation limit.

Example benchmark:
`118 → 34 → 4 → 2 → 2`

The final `2 → 2` is not a reason to continue. It is evidence that the current operator/tolerance has reached a local execution limit under the locked representation. That result should trigger residual diagnostics rather than unbounded repetition.

## 8. Required receipt

Use `oleander.3d.bounded-causal-iteration-receipt.v1` with:
- `experiment_id`
- `baseline_revision`
- `candidate_revision`
- `target_metric_id`
- `target_direction`
- `operation_family`
- `locked_variables`
- `protected_invariants`
- `material_improvement_rule`
- `max_iterations`
- `iterations`
- `stop_conditions`
- `stop_reason`
- `result`
- `rollback_lkg`
- `does_not_prove`

## 9. Result states

Use:
- `PASS_TARGET_REACHED`
- `HOLD_STAGNATION_RECLASSIFY`
- `FAIL_PROTECTED_INVARIANT_REGRESSION`
- `HOLD_MAX_ITERATION_BUDGET_REACHED`
- `FAIL_ITERATION_CONTRACT_VIOLATED`

## 10. Promotion boundary

A bounded iteration PASS proves only that the declared target was reached under the locked operation/invariants. It does not prove:
- correct relation ownership;
- reference fidelity;
- surface fairness/Class-A;
- aperture/interface closure unless that was the exact complete target;
- engineering/manufacturing truth;
- physical CMF;
- Design KEEP / MAIN KEEP.
