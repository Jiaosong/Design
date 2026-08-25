# G1 R2｜Topology vs Source Isolation Decision｜2026-08-14

## Decision State

`TOPOLOGY_INVARIANT_SOURCE_RELATION_SUSPECTED / REVISE / WORKING_SOURCE / CANDIDATE_REVIEW_REOPENED / CANDIDATE_PROMOTION_NOT_RUN`

This receipt records the bounded diagnostic decision after reconnecting the v0.13 sparse Blender-native editable Surface Source to the shared `OLEANDER Blender Surface System v1.20.0 / F1_DESIGN_VALIDATION` runtime and executing a same-Source topology A/B isolation.

It is diagnostic routing evidence only. It is not Candidate Promotion, Canonical Promotion, Class-A validation, engineering CAD validation, manufacturing validation, ergonomic validation or Release.

## Decision Question

Do the retained reflection defects materially change when only the **derived execution tessellation** is densified while the **same Blender-native sparse Working Source**, the same relation semantics, the same camera and the same Surface System diagnostics are retained?

The retained visual defects entering this isolation were:

1. `INTERFACE BASIN RIGHT TRANSITION` — reflection-band compression / hook.
2. `RIGHT / FRONT TERMINATION` — persistent pinch / crease-like convergence and Zebra compression.

## Evidence Identity

Validated implementation head before this immutable receipt:

`60977ec35088a4d1079c3d806e9baacea69dd948`

Fresh successful workflows on that head:

- Modeling Worker Blender Bridge / topology isolation: run `31773338713` — `SUCCESS`.
- Blender Surface System v1.20.0 CMF Lab regression: run `31773338717` — `SUCCESS`.
- Control Plane v0.3: run `31773338724` — `SUCCESS`.
- AI Governance Evals: run `31773338709` — `SUCCESS`.

Modeling evidence artifact:

- artifact ID: `9208969428`
- SHA-256: `648d59764a08fe6feba8031b8026cd8db2aea40b5ed8a141dc71b9729c372f93`
- size: `5,835,428 bytes`
- uploaded files: `22`

Runtime:

- Blender `5.2.0 LTS`
- Cycles
- Surface System API `oleander.blender-surface-system.f1-runtime.v1`
- Surface System fidelity `F1_DESIGN_VALIDATION`

## Source Authority Control

The isolation did not modify the sparse Working Source.

Source digest before isolation:

`4bd90a9629c7eab6211e4ba36e17268d79ee33f3ec59736add9d480c7a020eed`

Source digest after isolation:

`4bd90a9629c7eab6211e4ba36e17268d79ee33f3ec59736add9d480c7a020eed`

Per-family numeric error after the A/B run:

| Source family | Error |
|---|---:|
| GRIP_AXIS | 0.0 m |
| PALM_PROFILE | 0.0 m |
| THUMB_SIDE_PLAN | 0.0 m |
| OPPOSITE_SIDE_PLAN | 0.0 m |
| LOWER_RETURN_PROFILE | 0.0 m |
| INTERFACE_DECK_BOUNDARY | 0.0 m |

Therefore the visual A/B compares execution topology only; it is not confounded by a source edit.

## Derived Topology A/B

Both objects are explicitly `DERIVED_EXECUTION_NOT_AUTHORITY`.

### Baseline execution topology

- object: `OL_ISO_R2_BASE_TOPOLOGY`
- u rings: `56`
- circumferential samples: `72`
- vertices: `4,034`
- faces: `4,104`

### Dense execution topology

- object: `OL_ISO_R2_DENSE_TOPOLOGY`
- u rings: `112`
- circumferential samples: `144`
- vertices: `16,130`
- faces: `16,272`

Face-density ratio:

`3.9649122807017543×`

The dense topology is therefore materially denser without becoming source authority.

## Fixed Surface System Visual A/B

All comparisons use the same `HERO_CAM` and the same shared Surface System runtime. The only intentional execution change is tessellation density.

### STRIP

- mean absolute RGB difference: `0.0007428336909380088`
- p95 absolute RGB difference: `0.003`
- p99 absolute RGB difference: `0.015`
- max isolated channel difference: `0.5333333313465118`

### GRAZING

- mean absolute RGB difference: `0.0019729117718506237`
- p95 absolute RGB difference: `0.003`
- p99 absolute RGB difference: `0.047`
- max isolated channel difference: `0.40392159670591354`

### ZEBRA

- mean absolute RGB difference: `0.0013599421416129094`
- p95 absolute RGB difference: `0.0`
- p99 absolute RGB difference: `0.05`
- max isolated channel difference: `0.12941177189350128`

The images are **not claimed to be pixel-identical**. Local isolated channel differences remain. However, all three diagnostics stay well inside the declared topology-invariant heuristic bands (`mean <= 0.012`, `p99 <= 0.12`). A roughly fourfold face-count increase therefore does not materially reorganize the global diagnostic reading under this bounded A/B.

## Topology-Independent Analytic Source Probe

The source-space probe samples the analytic surface directly, independently of mesh tessellation:

- `97` u samples
- `144` theta samples
- longitudinal normal-turn span: `0.01 u`
- circumferential normal-turn span: `0.05 rad`

### Interface transition

- samples: `1,098`
- maximum combined normal-turn score: `52.04278831203538`
- strongest hotspot:
  - `u = 0.65`
  - `theta = 5.6286868376817125 rad` (`≈ -0.6545 rad` when wrapped)
  - `rho(interface) = 0.8771616462797075`
  - longitudinal normal turn = `8.333631086503974° / 0.01u`
  - circumferential normal turn = `51.37122159541644° / 0.05rad`

The strongest interface hotspots cluster around approximately:

- `u = 0.60–0.68`
- `rho = 0.86–0.89`
- negative-side / right-transition angular sector near `theta ≈ 5.63–5.67 rad`

This is important because the prior Machine QA checked the **outer** and **core** transition boundaries and reported low boundary discontinuity, but it did not test the **interior transition band** where the current probe finds the strongest normal-field swing.

### Termination

- samples: `4,032`
- maximum combined normal-turn score: `3.4497197412955436`

### Broad surface

- samples: `8,838`
- maximum combined normal-turn score: `4.874575832593821`

The interface transition is therefore the dominant analytic hotspot in this probe. The termination defect remains a valid visual observation, but this experiment does not show a comparably strong termination source-normal hotspot; a termination-specific local probe may still be required before altering its source relation.

## Decision

The current evidence does **not support derived tessellation density as the primary explanation for the interface reflection defect**.

Classification:

`TOPOLOGY_INVARIANT_SOURCE_RELATION_SUSPECTED`

Interpretation:

1. A ~`3.96×` face-count increase produces only small aggregate differences under fixed STRIP / GRAZING / ZEBRA diagnostics.
2. The Blender-native sparse Source is numerically identical before and after the isolation.
3. A topology-independent analytic probe finds a severe normal-field concentration inside the interface transition band, spatially consistent with the retained right-transition reflection defect.
4. Therefore the next legal re-entry is `Relation / Surface Source`, not a dense-mesh cosmetic patch.

This classification is a **diagnostic routing heuristic**, not Promotion evidence.

## QA Gap Exposed

The existing boundary-continuity checks are insufficient by themselves for this class of defect.

Current R2 Machine QA reports low normal discontinuity at the declared outer/core boundaries, yet the new analytic probe finds large normal rotation inside the transition band. Before evaluating an R3 relation correction, the machine gate should therefore add an **interior interface-transition fairness check** so the same failure mode cannot pass merely because both boundary samples are smooth.

## Next Legal Action

`Relation / Surface Source re-entry → add interior-transition fairness gate → test bounded R3 interface relation variants → re-run Machine QA → shared Surface System STRIP/GRAZING/ZEBRA → topology isolation only if needed`

For the interface relation, legal source-level variables may include the existing `INTERFACE_DECK_BOUNDARY` relationship controls such as transition span / `core_fraction` / inset relationship. Any R3 change must remain sparse, explicit and reversible.

Forbidden next actions:

- no mesh-local smoothing patch;
- no dense-topology promotion;
- no hidden sculpt correction;
- no Candidate Promotion;
- no Canonical Promotion;
- no claim that the termination defect is solved;
- no claim of Class-A, engineering or manufacturing validity.

## Authority Boundary

The six Blender-native sparse Source objects remain the editable `WORKING_SOURCE`.

All dense/execution meshes remain derived and non-authoritative.

Current state after this decision:

- `JOB STATE = R2_TOPOLOGY_VS_SOURCE_ISOLATION_EXECUTED`
- `DESIGN STATE = REVISE`
- `AUTHORITY STATE = WORKING_SOURCE`
- `CANDIDATE REVIEW = REOPENED`
- `CANDIDATE PROMOTION = NOT_RUN / BLOCKED`

v0.12 remains the current promoted canonical authority; v0.13 remains a reopened working-source experiment.
