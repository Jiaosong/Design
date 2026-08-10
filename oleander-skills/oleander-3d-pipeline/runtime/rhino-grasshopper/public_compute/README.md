# FREE_PUBLIC_COMPUTE｜OLEANDER Rhino + Grasshopper Runtime

Status: `IMPLEMENTED / ATTEMPTED / BLOCKED — PUBLIC SERVICE DISABLED / CP2 OPEN / CP4 OPEN`

This mode exists to attempt **real McNeel Rhino.Compute + Grasshopper headless execution** without using the user's computer and without enabling Core-Hour billing.

## Runtime selection

`FREE_PUBLIC_COMPUTE` is a Resource Adapter mode inside the existing `oleander-3d-pipeline`; it is not a parallel OLEANDER method.

Execution path:

```text
OLEANDER Runtime Job
  -> GitHub-hosted ephemeral runner
  -> https://compute.rhino3d.com/grasshopper
  -> real Rhino.Compute / Grasshopper headless solve when public service is available
  -> response + runtime report + auditable receipt
```

## Actual attempt｜2026-08-10

GitHub Actions run `31360491115` executed the complete no-paid probe path on a GitHub-hosted runner:

- paid Core-Hour token gate: PASS (`RHINO_TOKEN` absent and forbidden);
- official McNeel-source GHX fixture generation: PASS;
- POST to `https://compute.rhino3d.com/grasshopper`: EXECUTED;
- HTTP response: `404`;
- server response message: `This server has been turned off`;
- CP2: `OPEN`;
- CP2 blocker: `PUBLIC_SERVICE_DISABLED`;
- CP4: `OPEN`;
- evidence level: `ATTEMPT_EVIDENCE_ONLY`.

This result does **not** mean the Grasshopper definition was solved. The request reached the public service endpoint but the service rejected execution before Rhino/Grasshopper runtime evidence could be produced.

Stable evidence is archived under `public_compute/attempts/`; original GitHub Actions evidence is run `31360491115`, artifact `9052171471`.

## Cost and credential boundary

- `RHINO_TOKEN` = Core-Hour billing token: **FORBIDDEN in this mode**.
- `RHINO_COMPUTE_TOKEN` = optional Rhino Accounts bearer auth for the historical McNeel public Compute path: may be used only if already provided as a repository secret; its value is never logged or archived.
- `RHINO_COMPUTE_KEY` = self-hosted server API key: not used by this public mode.
- If a path requires paid/server Core-Hour billing, the mode stops and records `PAID_PATH_REJECTED`.
- A service-disabled response cannot be reclassified as an authentication problem and must not trigger token acquisition as a workaround.

## SP02 evidence promotion

CP2 starts at `OFFLINE_SURROGATE_ONLY` and may be promoted to `REAL_HEADLESS_GRASSHOPPER_EVIDENCE` only when all of the following are returned by a successful public Compute solve:

- an `OLEANDER_SP02_REPORT` generated inside a real Grasshopper Python 3 component;
- BASE = 4 branches × 6 items;
- GRAFT = 24 branches × 1 item, using real `GH_Structure.Graft`;
- FLATTEN = 1 branch × 24 items, using real `GH_Structure.Flatten`;
- TRANSPOSE_BY_ITEM = 6 branches × 4 items;
- Rhino and Grasshopper assembly versions are reported;
- the generated GHX hash and HTTP receipt are preserved.

Any authentication requirement, network failure, public-service shutdown, service rejection, definition error, or topology mismatch leaves CP2 `OPEN` with the exact blocker.

## CP4 hard boundary

CP4 is **always OPEN** in `FREE_PUBLIC_COMPUTE` because the mode is headless. This mode does not claim or synthesize:

- Parameter Viewer GUI screenshots;
- Path Mapper canvas evidence;
- Grasshopper desktop canvas screenshots;
- Rhino desktop viewport screenshots.

Headless tree data may support CP2 if a real solve succeeds, but it can never be relabeled as CP4 GUI evidence.

## Implementation

- `build_sp02_fixture.py` downloads a pinned official McNeel `.ghx` scripting sample, selects its DataTree-access Python 3 component, replaces only that component's script with the locked SP02 tree test, and adds an `RH_OUT` group for Compute output collection.
- `run_sp02_public_compute.py` submits the generated definition to `/grasshopper`, validates the embedded report, classifies `PUBLIC_SERVICE_DISABLED`, and emits a receipt when the network attempt completes.
- `.github/workflows/oleander-free-public-compute.yml` runs the probe on a GitHub-hosted ephemeral runner so the user's workstation is not involved.

Repository code existence and a successful CI job are not Rhino runtime evidence. Only a returned runtime report from a successful Compute solve may promote CP2.
