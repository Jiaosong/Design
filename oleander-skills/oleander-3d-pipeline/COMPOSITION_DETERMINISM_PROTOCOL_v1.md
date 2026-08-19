# OLEANDER 3D Composition Determinism Protocol v1

Status: CANDIDATE / reusable 3D Skill training delta

Benchmark provenance: Porsche 911 992.2 V72–V75.
- Standalone V72 on the same head produced `9093 vertices / 18171 edges / 9080 faces / 0 folds / 0 non-manifold / 2 residual straddles`.
- V74 imported the same V72 declarations through the stacked `exec` composition chain without changing the pre-run identity and produced `8338 vertices / 16336 edges / 8000 faces / 94 folds / 0 non-manifold / 2 residual straddles` while bounds still matched.
- Source control digest remained unchanged. Therefore equal Source identity + equal bounds + equal high-level defect count did not guarantee equal Derived execution.
- The benchmark continuation was rerouted from stacked source composition to `standalone parent → native .blend persistence → reopen exact scene → diagnostic child`.

## Core separation

`SOURCE_IDENTITY_EQUAL ≠ DERIVED_COMPOSITION_EQUAL`

`STANDALONE_PASS ≠ COMPOSED_PASS`

`EQUAL_BOUNDS ≠ EQUAL_TOPOLOGY ≠ EQUAL_NORMAL_STATE`

`COMPOSITION_DRIFT → DOWNSTREAM_DIAGNOSTIC_EVIDENCE_INVALID`

Use this gate whenever a 3D execution is extended or composed through scripted inheritance, monkeypatching, nested `exec`, add-on wrappers, Geometry Nodes wrappers, scene-linking, procedural graph composition, runtime adapters, or other mechanisms where the same Source may be evaluated through multiple composition paths.

## 1. Declare composition identity

Record:
- Source identity/digest;
- parent revision and exact executable entrypoint;
- parent runtime/application/version;
- composition mechanism;
- child/wrapper identity;
- expected unchanged semantic scope;
- direct/standalone witness;
- composed witness;
- geometry signature fields required for parity.

A child that changes the intended Source or semantic scope is a new experiment, not a composition-parity test.

## 2. Minimum geometry signature

When geometry equality is expected, compare at minimum:
- vertex / edge / face / triangle counts as applicable;
- connected components;
- world bounds/dimensions;
- normal reversal/fold count or equivalent surface-orientation witness;
- non-manifold count where applicable;
- protected semantic IDs / control counts;
- declared target diagnostic counts;
- deterministic mesh/geometry digest when the representation supports it.

Bounds alone are never a sufficient composition witness.

## 3. Fail closed on same-Source Derived drift

If Source identity matches and composition is declared semantics-preserving, any unexplained geometry-signature mismatch is:

`FAIL_COMPOSITION_DETERMINISM`

Examples:
- same bounds but different topology count;
- same defect count but new folds;
- same Source digest but changed evaluated sampling/connectivity;
- same render silhouette but different hidden geometry or normal orientation.

Do not continue using the composed result as if it were the standalone parent.

## 4. Hidden mutable context is a risk boundary

Treat these as high-risk until parity is proven:
- stacked `exec` chains sharing mutable dictionaries;
- global monkeypatch functions whose lookup target can change by nesting depth;
- inherited historical namespaces;
- mutable global `REV`, `REFERENCE_CONTRACT`, `core`, `runtime`, or similarly shared routing objects;
- child scripts that mutate parent runtime state before parent execution;
- dynamic function replacement without an explicit composition receipt.

A green import/compile/runtime exit code does not prove composition determinism.

## 5. Preferred continuation routes

When composition parity fails, stop adding another inheritance layer.

Preferred routes, in order:
1. explicit module/function API with isolated context objects and parity tests;
2. deterministic regeneration from Source using one current runtime entrypoint;
3. persist the exact native parent artifact, hash it, reopen it in the same verified application/runtime, and run diagnostic-only child logic on the reopened scene;
4. only use a proxy/export carrier when its narrower evidence scope is explicitly declared.

For diagnostic continuation, `standalone parent → persisted native artifact → reopen/readback → child diagnostic` is preferred over an unverified stacked execution chain.

## 6. Reopened-artifact witness

Before a child diagnostic may interpret the reopened scene, verify it matches the parent receipt/hash:
- native file identity/hash;
- object/host identity;
- geometry signature;
- Source revision/digest reference;
- units/origin/axis where relevant;
- required diagnostic target state.

If reopen witness fails, the child diagnostic stops before drawing operator/design conclusions.

## 7. Downstream evidence quarantine

Evidence produced on a composition-drifted host is `NON_PROMOTABLE_DIAGNOSTIC_PROVENANCE` until rerun on a valid direct/reopened carrier.

This includes:
- tolerance A/B;
- fold diagnostics;
- projection metrics;
- topology tests;
- render comparisons;
- Design Crit based on the drifted geometry.

The evidence may help debug composition itself but may not be cited as evidence about the intended parent geometry.

## 8. Required receipt

Use `oleander.3d.composition-determinism-receipt.v1` with:
- `source_identity`
- `parent_revision`
- `parent_entrypoint`
- `runtime_identity`
- `composition_mechanism`
- `semantic_scope_expected_unchanged`
- `standalone_signature`
- `composed_signature`
- `comparison_checks`
- `composition_result`
- `downstream_evidence_state`
- `preferred_recovery_route`
- `does_not_prove`

## 9. Result states

Use:
- `PASS_COMPOSITION_DETERMINISTIC`
- `FAIL_COMPOSITION_DETERMINISM`
- `HOLD_SOURCE_OR_RUNTIME_NOT_COMPARABLE`
- `PASS_REOPENED_PARENT_WITNESS`

## 10. Promotion boundary

Composition Determinism PASS proves only that the compared execution paths preserve the declared representation/signature. It does not prove geometry quality, reference fidelity, Class-A continuity, engineering/manufacturing validity, physical CMF, Design KEEP or MAIN KEEP.
