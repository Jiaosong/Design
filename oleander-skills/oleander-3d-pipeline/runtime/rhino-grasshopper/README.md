# OLEANDER Rhino + Grasshopper Runtime v0.1

Status: `BOOTSTRAP READY / HOST NOT YET CONNECTED / NOT PRACTICE-VALIDATED`

This runtime extends the existing `oleander-3d-pipeline`; it does **not** create a parallel OLEANDER method hierarchy.

## Goal

Provide a real Rhino 8 + Grasshopper execution node capable of producing evidence that an offline surrogate cannot provide:

- real `.gh` files;
- real Grasshopper solves;
- Data Tree path / branch / item inspection;
- Grasshopper canvas / Parameter Viewer screenshots;
- Rhino viewport screenshots;
- runtime logs and environment manifests;
- explicit OPEN/HOLD states when the host, plugin, definition, or evidence is unavailable.

## Architecture

```text
OLEANDER / ChatGPT / repository task
        |
        v
Runtime Contract
        |
        v
Windows Rhino Host
  Rhino 8.11+
  StartScriptServer
  rhinocode CLI
        |
        +--> Rhino Python/C# script
        |       |
        |       +--> Grasshopper SDK
        |       +--> GH_DocumentIO -> .gh
        |       +--> GH_Canvas -> canvas bitmap
        |       +--> RhinoView -> viewport bitmap
        |
        +--> runtime receipt / evidence manifest

Optional later layer:
Rhino.Compute -> headless Grasshopper solving / batch evaluation
```

## Why Desktop Runtime is primary

Rhino.Compute can solve Grasshopper definitions, but CP2 / CP4 training evidence also requires real Grasshopper GUI/canvas evidence and Rhino viewport comparison. Therefore:

1. **Desktop Rhino + `rhinocode` is the authoritative execution node for Practice evidence.**
2. **Rhino.Compute is an optional batch/headless solver**, not a replacement for GUI evidence.
3. `rhino3dm` or offline Python geometry is useful for surrogate checks only and must never be relabeled as Rhino/Grasshopper runtime evidence.

## Minimum host requirements

- Windows 10/11 x64.
- Rhino 8.11 or newer. `rhinocode` ships with Rhino >= 8.11.
- Valid local Rhino license or evaluation license.
- Grasshopper available in the Rhino installation.
- Rhino `StartScriptServer` command running.
- `%PROGRAMFILES%\Rhino 8\System` available on PATH, or use the full path to `rhinocode.exe`.

## Evidence boundary

Allowed runtime states:

- `HOST DETECTED`
- `RHINO RUNTIME PASS`
- `GRASSHOPPER SDK PASS`
- `DEFINITION SOLVED`
- `CANVAS CAPTURED`
- `VIEWPORT CAPTURED`
- `DESIGN-READY FOR FUTURE TEST`

Do **not** use `VERIFIED`, `TESTED`, `PASSED`, or equivalent project-approval language unless the exact real evidence required by the task was executed and preserved.

## Files

- `runtime_contract.schema.json` — stable execution / evidence contract.
- `windows/bootstrap_windows.ps1` — checks Rhino / rhinocode and starts a local Rhino execution instance if needed.
- `windows/healthcheck.ps1` — performs a real local runtime health check.
- `windows/run_job.ps1` — dispatches an allow-listed job to a running Rhino instance through `rhinocode`.
- `rhino/probe_runtime.py` — runs inside Rhino and writes the runtime manifest.
- `rhino/capture_evidence.py` — captures active Grasshopper canvas and active Rhino viewport.
- `jobs/cp2_cp4_data_tree.json` — locked job specification for the current Data Tree training.

## Current OPEN items

- The user's Windows Rhino host has not yet run this bootstrap package.
- No current ChatGPT tool is directly connected to the local Rhino script server.
- CP2 and CP4 remain OPEN until the host executes the Data Tree definition and returns real evidence.
- A custom remote connector / MCP bridge is intentionally deferred until the local runtime itself passes healthcheck and evidence capture.

## Security

Do not expose Rhino's local script server directly to the public internet. If a remote control layer is added later, use an authenticated, allow-listed bridge with explicit action receipts. The existing public `Jiaosong/Design` repository must not be given an unrestricted self-hosted runner that executes arbitrary fork / PR code.
