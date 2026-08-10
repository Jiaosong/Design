# FREE_PUBLIC_COMPUTE｜OLEANDER Rhino + Grasshopper Runtime

Status: `IMPLEMENTED / ATTEMPTED / PROVIDER-GATED / CONDITIONAL-WATCH READY / PUBLIC SERVICE DISABLED / CP2 OPEN / CP4 OPEN`

This mode exists to attempt **real McNeel Rhino.Compute + Grasshopper headless execution** without using the user's computer and without enabling Core-Hour billing.

## Runtime selection

`FREE_PUBLIC_COMPUTE` is a Resource Adapter mode inside the existing `oleander-3d-pipeline`; it is not a parallel OLEANDER method.

Current execution path:

```text
OLEANDER Runtime Job
  -> GitHub-hosted ephemeral runner
  -> GET https://compute.rhino3d.com/healthcheck
  -> Provider Selector
       AVAILABLE -> build SP02 GHX -> POST /grasshopper -> validate runtime report
       otherwise -> SKIP_SP02_PRESERVE_OPEN
  -> auditable receipt
```

The provider preflight is intentionally separated from the Grasshopper solve. A successful `/healthcheck` only permits a solve attempt; it is **not** runtime evidence and cannot promote CP2.

## Actual full attempt｜2026-08-10｜Run 4

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

## Provider-gated preflight｜2026-08-10｜Run 9

GitHub Actions run `31362931991` validated the new provider gate:

- GET `/healthcheck`: EXECUTED;
- HTTP response: `404`;
- provider state: `PUBLIC_SERVICE_DISABLED`;
- selector action: `SKIP_SP02_PRESERVE_OPEN`;
- SP02 fixture build: SKIPPED;
- SP02 `/grasshopper` solve: SKIPPED;
- CP2: `OPEN`;
- CP4: `OPEN`;
- evidence level: `PROVIDER_PREFLIGHT_ONLY`;
- artifact: `9053037470`.

This reduces repeated heavy requests while preserving the option to re-enter the real solve path if the provider ever returns `AVAILABLE`.

## Conditional watch validation｜2026-08-10｜Run 10

GitHub Actions run `31366794994` validated the condition-driven watch configuration:

- NO_PAID_RUNTIME gate: active;
- GET `/healthcheck`: EXECUTED;
- HTTP response: `404`;
- provider state: `PUBLIC_SERVICE_DISABLED`;
- selector action: `SKIP_SP02_PRESERVE_OPEN`;
- SP02 GHX build: SKIPPED;
- SP02 `/grasshopper` solve: SKIPPED;
- CP2: `OPEN`;
- CP4: `OPEN`;
- evidence level: `PROVIDER_PREFLIGHT_ONLY`;
- artifact: `9054448795`.

A weekly cron (`0 1 * * 1`) is present in the workflow as the intended low-cost provider watch. **GitHub scheduled workflows execute from the repository default branch; because this workflow is still in Draft PR #17, that cron is configuration-ready but not yet an active GitHub scheduler.** An external condition watch is used while the PR remains Draft.

## Current official service boundary

McNeel's current Compute documentation still defines `/healthcheck`, `/version`, Grasshopper solving, local development, and self-hosted production deployment. The historical public `compute.rhino3d.com` endpoint has been explicitly turned off; current guidance is to run your own Compute instance. Local Compute can use an existing Rhino licence, while server/cloud deployment uses Core-Hour Billing.

OLEANDER therefore does **not** invent a substitute public endpoint and does not silently switch to a paid server.

## Cost and credential boundary

- `RHINO_TOKEN` = Core-Hour billing token: **FORBIDDEN in this mode**.
- `RHINO_COMPUTE_TOKEN` = optional Rhino Accounts bearer auth for the historical McNeel public Compute path: may be used only if already provided as a repository secret; its value is never logged or archived.
- `RHINO_COMPUTE_KEY` = self-hosted server API key: not used by this public mode.
- If a path requires paid/server Core-Hour billing, the mode stops and records `PAID_PATH_REJECTED`.
- A service-disabled response cannot be reclassified as an authentication problem and must not trigger token acquisition as a workaround.

## Provider Selector

`check_public_compute_provider.py` probes `/healthcheck` and returns one of:

- `AVAILABLE` -> `ALLOW_SP02_SUBMISSION`;
- `PUBLIC_SERVICE_DISABLED` -> `SKIP_SP02_PRESERVE_OPEN`;
- `AUTH_REQUIRED` -> `SKIP_SP02_PRESERVE_OPEN`;
- `PAID_PATH_REJECTED` -> `SKIP_SP02_PRESERVE_OPEN`;
- `NETWORK_BLOCKED` -> `SKIP_SP02_PRESERVE_OPEN`;
- `UNAVAILABLE` -> `SKIP_SP02_PRESERVE_OPEN`;
- `UNKNOWN` -> `SKIP_SP02_PRESERVE_OPEN`.

Default rule: **lowest sufficient execution cost, no paid fallback, no evidence promotion from availability checks.**

## SP02 evidence promotion

CP2 starts at `OFFLINE_SURROGATE_ONLY` and may be promoted to `REAL_HEADLESS_GRASSHOPPER_EVIDENCE` only when all of the following are returned by a successful Compute solve:

- provider preflight returned `AVAILABLE`;
- an `OLEANDER_SP02_REPORT` was generated inside a real Grasshopper Python 3 component;
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

- `check_public_compute_provider.py` performs the no-paid `/healthcheck` preflight and writes `provider_preflight_receipt.json`.
- `build_sp02_fixture.py` downloads a pinned official McNeel `.ghx` scripting sample, selects its DataTree-access Python 3 component, replaces only that component's script with the locked SP02 tree test, and adds an `RH_OUT` group for Compute output collection.
- `run_sp02_public_compute.py` submits the generated definition to `/grasshopper`, validates the embedded report, classifies `PUBLIC_SERVICE_DISABLED`, and emits a receipt when the network attempt completes.
- `.github/workflows/oleander-free-public-compute.yml` runs the provider gate on a GitHub-hosted ephemeral runner and enters the heavier SP02 path only when the provider state is `AVAILABLE`.

Repository code existence, provider availability, and a successful CI job are not Rhino runtime evidence. Only a returned runtime report from a successful Compute solve may promote CP2.
