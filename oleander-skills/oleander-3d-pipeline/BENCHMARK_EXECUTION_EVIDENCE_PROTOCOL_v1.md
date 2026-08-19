# OLEANDER 3D Benchmark Execution Evidence Protocol v1

Status: CANDIDATE / reusable 3D Skill training delta

Purpose: prevent a submitted script, green workflow, or generated artifact from being misreported as proof that the intended 3D benchmark revision actually executed under the declared runtime.

## Core separation

`IMPLEMENTED ≠ INVOKED ≠ EXECUTED ≠ RECEIPT_VALID ≠ EXPERIMENT_SUCCESS ≠ EVIDENCE_PASS ≠ DESIGN_PASS`

A benchmark is useful only when these states are recorded independently.

## 1. Target execution identity

Every benchmark run must bind:
- repository commit or immutable source identity;
- target benchmark/revision ID;
- exact executable/runtime identity;
- exact command/script entrypoint;
- expected output carrier/receipt;
- baseline revision when an A/B claim is made.

A workflow that installs Blender but runs only revision A cannot be cited as runtime evidence for revision B merely because revision B exists in the same branch.

Fail: `FAIL_TARGET_REVISION_NOT_EXECUTED`.

## 2. Runtime witness

Machine execution PASS requires runtime evidence captured by the executing environment, not inferred from YAML or documentation.

Minimum witness:
- application + version/build/status;
- platform/device/backend where material;
- command/entrypoint;
- exit state;
- output receipt path;
- output readback;
- source commit/revision binding.

For retained evidence, capture artifact/output hashes where practical.

Fail: `HOLD_RUNTIME_WITNESS_MISSING` / `FAIL_OUTPUT_READBACK_MISSING`.

## 3. Baseline/candidate comparability

For controlled A/B benchmarks:
- execute baseline and candidate in the same locked runtime when possible;
- otherwise record the runtime delta and mark comparability partial;
- lock camera/render/settings/metric carrier when those variables are not under test;
- record the exact Source edit scope;
- keep unrelated Source deltas forbidden.

A baseline from an old runtime may remain provenance but cannot silently become a controlled comparison baseline.

Fail: `HOLD_BENCHMARK_COMPARABILITY_UNRESOLVED`.

## 4. Execution PASS versus experiment outcome

Infrastructure/contract execution and the experimental hypothesis are different gates.

Examples:
- Blender launches, target revision runs, receipts are valid, but folds increase: **Execution PASS / Experiment REJECT**.
- Blender launches, target revision runs, hood–fender relation improves, held-out view is not reviewed: **Execution PASS / Experiment SCREENED / Reference Fidelity HOLD**.
- workflow is green because only unit tests ran and target Blender command was skipped: **Target Execution NOT PROVEN**.

CI should fail on broken execution, malformed/missing evidence, authority violations, or hard contract breaches. A correctly executed design experiment may record a negative result without being rewritten as an infrastructure failure.

## 5. Promotion boundary

No benchmark execution receipt may by itself promote:
- Reference Fidelity PASS;
- Design KEEP / MAIN KEEP;
- Class-A continuity;
- physical CMF;
- engineering/manufacturing feasibility;
- field truth.

Those require their own evidence/review gates.

## 6. Required receipt

Use `oleander.3d.benchmark-execution-receipt.v1` with at least:
- `benchmark_id`
- `source_commit`
- `target_revision`
- `runtime`
- `invocation`
- `output_readback`
- `baseline_comparison`
- `execution_result`
- `experiment_result`
- `evidence_result`
- `design_result`
- `does_not_prove`

## 7. Hard rules

- `WORKFLOW_SUCCESS_WITHOUT_TARGET_INVOCATION` is not runtime execution evidence.
- A target revision must identify itself in the produced receipt/artifact.
- A/B claims require explicit baseline and candidate execution identities.
- Negative experimental results are retained as benchmark evidence when execution is valid.
- A machine receipt cannot self-promote visual/design quality.
