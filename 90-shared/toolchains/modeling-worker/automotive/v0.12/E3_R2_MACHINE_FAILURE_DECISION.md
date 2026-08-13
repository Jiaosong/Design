# Modeling Worker v0.12｜E3 R2 Machine Failure Decision

Status: `E3 R2 MACHINE FAIL / ARCHITECTURE REVISE / COMPILER C2 MATH PASS / REAR-HALF FAIRNESS FAIL / PAP BLOCKED / PROMOTION BLOCKED`

## Decision Question

Can v0.12 replace the rejected E3 R1 single-center-cage Automotive application architecture with genuinely independent low-frequency hood/cowl, cabin, shoulder/rear-haunch, lower-body and termination source structures while preserving C2/fairness and making each volume legible at first reading?

## Immutable failed execution evidence

GitHub Actions run: `31667359613` / Modeling Worker v0.12 run #28  
Head SHA entering the run: `a39fe49ce653da2912b55c0948ac4d70cd1f5726`  
AI Governance Evals: run `31667359606` — `SUCCESS`  
R2 execution result: `MACHINE_FAIL_REVISE_E3_R2_ARCHITECTURE`  
The R2 artifact-upload step was skipped because the executable returned fail-closed exit code `5`; this is corrected separately so future failed R2 evidence is persisted.

E1, E2 and E3 R1 baseline all replayed successfully in the same run before R2. Therefore this R2 failure is not attributed to an environment change or loss of accepted generic method evidence.

## What R2 proved

The R2 architectural direction is materially stronger than R1 and is retained for revision:

- five independent low-frequency source stations were created;
- source authority is explicit station `position / tangent / curvature` jets;
- four analytic longitudinal surface patches are compiled before execution topology;
- the rejected R1 `4×4` center cage is not reused;
- semantic source edits changed exactly their declared source keys;
- every semantic edit produced a working-fidelity visible geometric effect (`>= 0.04 m` proxy);
- execution topology remained derived and mesh stitching did not become Surface Source Authority.

These are partial architectural PASS findings. They do not override the machine failure.

## Compiler-space continuity

The degree-5 longitudinal patch compiler satisfied the declared shared-jet C2 relationship in raw compiler space at all three seams:

- seam 1: position `0`, tangent approximately `8.54e-7°`, second derivative approximately `1.21e-14`;
- seam 2: position `0`, tangent approximately `1.21e-6°`, second derivative approximately `6.47e-15`;
- seam 3: position `0`, tangent approximately `1.21e-6°`, second derivative approximately `1.24e-14`.

Therefore the compiler-space relationship equation is not the root cause of the design failure.

## Runtime representation finding

Blender `mathutils` float representation produced second-derivative seam residuals above the retained runtime representation tolerance of `5e-6`:

- seam 1: approximately `6.66e-6`;
- seam 2: approximately `5.27e-6`;
- seam 3: approximately `8.27e-6`.

This is classified as a runtime representation issue, not permission to relax the original compiler design threshold. No threshold is changed by this receipt.

The current R2 machine boolean combines compiler-space continuity with this runtime representation condition; later precision classification may separate them more explicitly, but that cannot convert the present R2 to PASS because independent geometric fairness failures also exist.

## Real geometric fairness failure

Base surface rear-half fairness fails at working fidelity:

- `CABIN-CROWN → REAR-HAUNCH`: max adjacent normal jump approximately `8.72°` > `8°`;
- `REAR-HAUNCH → REAR-TERMINATION`: max adjacent normal jump approximately `8.86°` > `8°`.

The front termination→hood and hood→cabin patches remain inside the same normal-flow threshold.

Semantic edit variants confirm the same root area rather than a generic compiler failure:

- shoulder edit drives rear-half max adjacent normal jump to approximately `11.6–11.8°`;
- rear-haunch edit drives rear-half normal jump to approximately `11.85–11.87°` and rear patch curvature-rate proxy to approximately `15.97` > `15`;
- lower-body edit remains visible but rear-half normal flow still exceeds the gate.

Thus the retained architecture has enough independent control authority, but its rear-haunch / rear-termination jet values and rear shoulder acceleration are too aggressive for the current fairness contract.

## Root cause

`Architecture R2 concept = RETAIN`  
`R2 source-jet values / rear-half relationship tuning = REVISE`

Do **not** revert to R1 and do **not** solve by densifying the execution mesh.

## Next allowed action

Revise only the R2 source stations and semantic edit magnitudes at the rear half:

1. reduce the `STA-REAR-HAUNCH` shoulder/upper-volume lateral and vertical acceleration;
2. make `STA-REAR-TERMINATION` shoulder/upper-volume positions continue the haunch more gradually;
3. reduce rear-biased `VOL-SHOULDER` and `VOL-REAR-HAUNCH` semantic deltas while retaining the `>= 0.04 m` working-fidelity legibility condition;
4. keep compiler-space C2 thresholds unchanged;
5. preserve runtime precision evidence separately; do not use it to hide geometric fairness failure;
6. replay E1 → E2 → R1 → R2 and persist the failed or passed R2 evidence;
7. only after R2 Machine PASS perform Human Hero / Side / Top / Zebra + semantic-variant Project/Visual QA.

PAP and system Promotion remain blocked. No Class-A, engineering, manufacturing, final Automotive design or production authority is implied.
