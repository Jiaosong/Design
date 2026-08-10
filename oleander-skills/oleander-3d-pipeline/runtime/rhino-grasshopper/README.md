# OLEANDER Rhino + Grasshopper Real Runtime Adapter v0.2-draft

Status: `DRAFT / MULTI-RUNTIME ADAPTER / NOT PRACTICE-VALIDATED`

This runtime is a Resource Adapter under the existing `oleander-3d-pipeline`. It does not create a second OLEANDER method and it does not change the evidence rules defined in 01B.

## Current runtime priority

1. `FREE_PUBLIC_COMPUTE` — preferred no-cost, no-user-workstation path. **Implemented and attempted; currently blocked because the McNeel public service returns `This server has been turned off`. CP2 remains OPEN; CP4 remains OPEN.**
2. `PRIVATE_COMPUTE` — future authenticated/private headless runtime; may incur Core-Hour/server cost and therefore requires explicit authorization. Not enabled by the free mode.
3. `DESKTOP_RHINO` — optional local/debug runtime. It is no longer the default path because the user does not want their workstation to execute the training.
4. `SURROGATE_OFFLINE` — Python/DXF/SVG/rhino3dm precheck only; never runtime evidence.

## Evidence boundary

A real runtime adapter may create evidence only when its own receipt proves execution:

- repository code existence ≠ Rhino runtime evidence;
- GitHub Actions success ≠ Grasshopper solve success;
- offline Python/DXF/SVG/rhino3dm ≠ Rhino/Grasshopper runtime evidence;
- a network request reaching Compute but receiving service-disabled/auth/server errors ≠ Grasshopper runtime evidence;
- only a returned real runtime report may promote CP2;
- only desktop GUI evidence can close CP4 because CP4 requires Parameter Viewer / Path Mapper canvas evidence.

## FREE_PUBLIC_COMPUTE result｜2026-08-10

Actual GitHub-hosted probe:

```text
Run ID        31360491115
Artifact ID   9052171471
Mode          FREE_PUBLIC_COMPUTE
Cost policy   NO_PAID_RUNTIME
HTTP          404
Response      This server has been turned off
CP2           OPEN / PUBLIC_SERVICE_DISABLED
CP4           OPEN / HEADLESS_NO_GRASSHOPPER_GUI
Evidence      ATTEMPT_EVIDENCE_ONLY
```

The branch archives the exact response and receipt under `public_compute/attempts/`.

## Runtime Contract

The shared runtime contract supports:

- `DESKTOP_RHINO`
- `FREE_PUBLIC_COMPUTE`
- `PRIVATE_COMPUTE`
- `SURROGATE_OFFLINE`

Each run must record runtime mode, cost policy, input provenance, required outputs, evidence promotion rules, authority boundary and receipt.

## SP02 locked training target

Exercise assumptions only:

```text
zones = 4
items / zone = 6
DX = 2.4
DY = 3.6
```

CP2 target:

```text
BASE              4 × 6
GRAFT            24 × 1
FLATTEN            1 × 24
TRANSPOSE_BY_ITEM  6 × 4
```

CP2 may close only after a real Rhino/Grasshopper runtime returns these structures and versioned runtime metadata.

CP4 remains OPEN in every headless runtime. It requires real desktop Grasshopper Parameter Viewer / Path Mapper before/after evidence; no synthetic screenshot is acceptable.

## Directory

```text
rhino-grasshopper/
  README.md
  SECURITY.md
  runtime_contract.schema.json
  jobs/
  public_compute/
    README.md
    build_sp02_fixture.py
    run_sp02_public_compute.py
    attempts/
  windows/
  rhino/
```

The Windows/Desktop files remain for optional debug or a future controlled desktop node, but they are not required by the current no-user-workstation path.

## Security

- Public repository code must never contain Rhino billing tokens, cloud credentials or unrestricted machine-control credentials.
- `FREE_PUBLIC_COMPUTE` refuses `RHINO_TOKEN`, the Core-Hour billing token.
- A public-service shutdown cannot be bypassed by silently switching to a paid/private runtime.
- Any paid/private runtime requires a separate Human Authority gate.

## Current conclusion

`FREE_PUBLIC_COMPUTE` is now a real implemented execution mode with an auditable failed attempt. The failure is useful evidence: the no-cost public McNeel Compute endpoint is currently unavailable, so SP02 CP2 remains OPEN rather than being falsely promoted. CP4 remains OPEN by design.
