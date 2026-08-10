# macOS Intel Rhino + GrasshopperPlayer Candidate

Status: `PLATFORM PREFLIGHTED / INSTALLER + LICENSE REQUIRED / NOT EXECUTED / CP2 OPEN / CP4 OPEN`

This provider exists because **Rhino.Compute being unsupported on macOS does not mean Rhino + Grasshopper execution is unsupported on macOS**. Rhino 8 for Mac supports Intel processors, and the official `GrasshopperPlayer` command can execute a `.gh` / `.ghx` without opening the Grasshopper window.

The current candidate uses GitHub's standard `macos-15-intel` hosted runner so the user's workstation is not involved and no Core-Hour billing path is needed at the environment level.

## Actual environment preflight

GitHub Actions run `31364240139` executed an environment-only preflight:

- macOS: `15.7.7`;
- architecture: `x86_64`;
- CPU: `Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz`;
- free disk: `110.12 GB`;
- Rhino 8 app: not installed;
- `rhinocode`: not installed;
- licensing attempt: none;
- Rhino Account login: none;
- evaluation request: none;
- Core-Hour token: forbidden / not used;
- CP2: `OPEN`;
- CP4: `OPEN`;
- evidence: `ENVIRONMENT_PREFLIGHT_ONLY`.

Artifact: `9053514012`, digest `sha256:ecc19af0068ccaeadce610c6d5072a3ed19943f5ce54b19e345df0be02aa4e46`.

## Why this path is technically relevant

Official McNeel documentation establishes three independent facts:

1. Rhino 8 for Mac supports Intel or Apple processors on supported macOS versions.
2. `GrasshopperPlayer` can load and execute `.gh` / `.ghx` without showing the Grasshopper window; `-_GrasshopperPlayer` is scriptable.
3. Rhino 8.11+ ships `rhinocode` on macOS, which can communicate with a running Rhino instance after `StartScriptServer` is started.

Therefore a GitHub-hosted Intel Mac can be treated as a **platform candidate** for a real Rhino + GrasshopperPlayer SP02 execution. This does not yet mean the runtime is available.

## Current hard blocker

`INSTALLER_AND_LICENSE_REQUIRED`

Rhino is not preinstalled on the GitHub image. McNeel's licensed installer requires access to a Rhino 8 license, while the free 90-day evaluation requires the user to create/log into a Rhino Account, accept the applicable conditions, and obtain an evaluation key. Those are human/account authority actions and are intentionally outside this repository automation.

The repo must never:

- create a Rhino account on behalf of the user;
- accept licensing/privacy conditions on the user's behalf;
- request a one-time evaluation without explicit user action;
- commit or log a Rhino license key;
- silently use `RHINO_TOKEN` / Core-Hour Billing;
- treat a copied standalone license file as portable across ephemeral hosts when McNeel documents standalone Mac license files as system-specific.

Managed LAN Zoo / Cloud Zoo deployment may be technically deployable, but only if the user or license administrator already has and explicitly authorizes that license method.

## SP02 runtime evidence design

The SP02 fixture is now provider-neutral. The embedded Grasshopper Python 3 component:

- executes real `GH_Structure` Base / Graft / Flatten / Transpose logic;
- reports real Rhino and Grasshopper assembly versions;
- prints the `OLEANDER_SP02_REPORT` marker;
- writes the same exact report to the path in `OLEANDER_SP02_REPORT_PATH` when that environment variable exists.

For the future macOS route:

```text
GitHub macos-15-intel
  -> authorized Rhino 8 installer
  -> authorized Rhino license method
  -> Rhino 8 for Mac
  -> GrasshopperPlayer SP02 GHX
  -> tree_report.json written inside Grasshopper runtime
  -> validate_sp02_runtime_report.py
  -> exact evidence receipt
  -> CP2 decision
```

`validate_sp02_runtime_report.py` validates an already-created real runtime report. The validator itself cannot create runtime evidence.

## CP2 boundary

CP2 stays `OPEN` until all of these exist in one actual run:

- supported Rhino 8 for Mac instance started;
- license accepted by Rhino without unresolved interactive gating;
- `GrasshopperPlayer` actually ran the SP02 definition;
- embedded component wrote `tree_report.json`;
- Rhino and Grasshopper versions are present;
- Base = 4 × 6;
- Graft = 24 × 1;
- Flatten = 1 × 24;
- Transpose = 6 × 4;
- report validator returns exact contract success;
- immutable run receipt and artifact are archived.

## CP4 boundary

CP4 stays `OPEN` even if the macOS GrasshopperPlayer path eventually succeeds. GrasshopperPlayer is intentionally headless with respect to the Grasshopper canvas and therefore cannot prove the required Parameter Viewer / Path Mapper GUI state.

## Current next gate

No more runtime execution should be attempted until an installer source and a legitimate Rhino 8 license path are explicitly authorized. See `execution_contract.json`.
