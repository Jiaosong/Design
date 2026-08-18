# OLEANDER 3D Reference Reproduction — Regression Baseline & Promotion Protocol v1

Use this protocol when iterative reference-reproduction work has at least one previously measured candidate and the next revision changes only one causal family.

It exists because a locally better modeling method can still produce a globally worse reproduction.

`Newer revision ≠ Better candidate`

`More sophisticated representation ≠ Higher reference fidelity`

`Local fix PASS ≠ Global regression-free PASS`

## 1. Last-known-good baseline

Before an experimental edit, persist the current best measured candidate as `LAST_KNOWN_GOOD` (LKG).

The LKG receipt must bind:
- candidate revision and commit;
- Source/control digest;
- native asset identity;
- locked hard points;
- every previously passed fidelity metric and threshold;
- render/evaluated-projection evidence ids;
- Design / Reference Fidelity state;
- does-not-prove boundary.

A newer experiment does not replace LKG merely because it builds or because its targeted local metric improves.

### FAIL
`FAIL_LKG_BASELINE_MISSING` when a comparative edit begins without a recoverable measured baseline.

---

## 2. Regression locks

Every metric/family outside the declared edit scope becomes a regression lock.

Examples:
- editing greenhouse interface locks wheelbase, wheel openings, lower envelope and front/rear hard points;
- editing lower bumper return locks roof/greenhouse/upper silhouette;
- editing front cross-section locks side silhouette and rear profile;
- changing a diagnostic measurement implementation locks geometry and Source digest.

For each lock record:
- metric/family id;
- baseline value;
- threshold;
- allowed numerical drift, if any;
- baseline evidence source;
- candidate value;
- status `PASS / REGRESSED / NOT_COMPARABLE`.

### FORBIDDEN
- dropping a previously passed gate because the new revision targets another family;
- changing the reference target or threshold to make an experiment pass;
- comparing an analytic/source proxy in one revision with final evaluated geometry in another without marking `NOT_COMPARABLE`.

### FAIL
`REJECT_REGRESSION_LOCK_BROKEN` if any locked metric exceeds its declared tolerance.

---

## 3. Experimental branch semantics

Experimental revisions are classified as `CANDIDATE_EXPERIMENT`, not CURRENT authority.

Allowed outcomes:
- `PROMOTE_OVER_LKG` — targeted defect improves and all regression locks remain valid;
- `KEEP_LKG_REJECT_EXPERIMENT` — experiment regresses any locked gate or worsens visual/reference fidelity;
- `KEEP_LKG_HOLD_EXPERIMENT` — measurement/evidence is invalid or incomparable;
- `REBASE_EXPERIMENT_ON_LKG` — local method is useful but must be reapplied without the regression.

A rejected experiment remains provenance; it must not silently become the base of the next revision.

### FAIL
`FAIL_REJECTED_EXPERIMENT_BECAME_BASELINE`.

---

## 4. View-scoped failure routing

Reference-reproduction edits should be scoped by the view/metric that actually failed.

If SIDE upper/lower, front-cabin ratios and rear-backlight ratios already pass, a later front/rear profile experiment may not reopen them unless new evidence proves the old measurement invalid.

Preferred sequence:
1. lock hard points;
2. lock SIDE top/bottom envelope;
3. lock greenhouse landmarks/ratios;
4. measure FRONT profile;
5. measure REAR profile;
6. edit the failing cross-section family only;
7. rerun every lock;
8. only then move to surface-flow diagnostics and detail.

### FAIL
`REVISE_FAILURE_SCOPE_TOO_BROAD` when an edit modifies unrelated passed families without a causal justification.

---

## 5. Measurement-method changes are tool changes, not geometry changes

If a fidelity gate changes because the measurement implementation changes (render alpha, compositor mask, evaluated mesh scan, projection camera calibration), classify the operation as `DIAGNOSTIC_TOOL_CHANGE`.

During a diagnostic-tool change:
- Source and candidate geometry are immutable;
- previous measurement is retained as provenance;
- the new method must be validated against known geometry or a deterministic fixture;
- results from different methods are not directly comparable until equivalence or supersession is established;
- no geometry edit may be justified by a measurement already known to be invalid.

### FAIL
- `FAIL_MEASUREMENT_TOOL_MUTATED_GEOMETRY`
- `HOLD_MEASUREMENT_METHOD_NOT_VALIDATED`

---

## 6. Promotion condition

An experiment can replace LKG only when all are true:
1. build/execution evidence is valid;
2. the targeted failure metric is improved or resolved;
3. every regression lock is PASS;
4. measurement methods are valid and comparable;
5. current reference revision remains locked;
6. independent visual/reference review is not REJECT when such review is required.

Machine promotion must emit a `REGRESSION_PROMOTION_RECEIPT` with:
- `baseline_revision`;
- `candidate_revision`;
- `edit_scope`;
- `target_metric_delta`;
- `regression_locks`;
- `measurement_method_ids`;
- `promotion_decision`;
- `visual_review_state`;
- `does_not_prove`.

`Process PASS` may coexist with `KEEP_LKG_REJECT_EXPERIMENT`.

`Projection PASS` does not independently authorize promotion.

`Design / Reference Fidelity REJECT` vetoes MAIN promotion even when regression locks pass.

---

## 7. Best-known per-gate baseline

A single historical revision is not sufficient when different revisions establish different best measured gates.

Maintain a `BEST_KNOWN_GATE_BASELINE` table in addition to any whole-candidate LKG. For every stable comparable metric, the regression baseline is the best valid value already achieved under the same reference revision and measurement method, even when that value came from an experiment that was not promoted for unrelated visual/design reasons.

Example: if V23 establishes a REAR profile RMSE of `0.117` while V22 was `0.272`, a later aperture experiment may not compare only against V22 and accept `0.242` as an improvement. The REAR profile lock must use the V23 best-known value unless the measurement method or reference changed and comparability is explicitly invalidated.

### MUST CHECK
- each lock records `baseline_revision` and `baseline_evidence_source`, not only a scalar value;
- best-known values are selected per metric/gate;
- a candidate may reuse a local method from a visually rejected experiment, but cannot discard that experiment's valid best-known measurement;
- if the target metric itself is temporarily allowed to regress for a deliberate trade study, the state is `HOLD/REJECT`, never automatic promotion;
- whole-candidate Design/Reference state and per-gate numeric baselines remain separate concepts.

### FORBIDDEN
- choosing an older weaker baseline merely because it makes the new candidate look improved;
- replacing `BEST_KNOWN_GATE_BASELINE` with `last commit` or `last CI success`;
- silently resetting gate history after an experimental branch.

### FAIL
- `FAIL_WEAKER_REGRESSION_BASELINE_SELECTED`
- `REJECT_BEST_KNOWN_GATE_REGRESSION`
