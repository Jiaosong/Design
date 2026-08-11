# OLEANDER Blender Runtime v1.0

Status: **ACTIVE RUNTIME INTERFACE / OLEANDER ALL PROJECTS**

This runtime interface makes Blender 5.2 LTS / Cycles available to the entire OLEANDER repository without coupling any individual case, Practice package, website module, CMF study, product study, spatial project, or rendering task to a Timer-specific absolute path.

## Current verified runtime

- Blender: `5.2.0 LTS`
- build: `fbe6228777e7`
- official Linux x64 release archive SHA-256: `96f6c181a30f4950607839dc84d42a354b250d8a0231b098b59b7bc69c351c48`
- current ChatGPT runtime home: `/mnt/data/runtime/blender-5.2.0-lts`
- global executable: `/usr/local/bin/blender`
- OLEANDER wrapper: `/usr/local/bin/oleander-blender`
- render engine baseline: `CYCLES`
- current container device: CPU path tracing; GPU acceleration is not available in this container.

The binary is an external runtime dependency. It is **not** vendored into this public repository.

## Project-wide resolution contract

All new OLEANDER tasks that need Blender must resolve it in this order:

1. `$OLEANDER_BLENDER_BIN` when explicitly supplied by the runtime;
2. `blender` found on `PATH`;
3. `/mnt/data/runtime/blender-5.2.0-lts/blender` only as the current ChatGPT-runtime fallback.

Project files must not hard-code a project-specific Blender path.

## Shared environment variables

```bash
OLEANDER_BLENDER_VERSION="5.2.0 LTS"
OLEANDER_BLENDER_BUILD="fbe6228777e7"
OLEANDER_BLENDER_HOME="<runtime-specific>"
OLEANDER_BLENDER_BIN="<runtime-specific>"
OLEANDER_RENDER_ENGINE="CYCLES"
```

Activate through:

```bash
source tools/oleander-runtime/activate-blender.sh
```

Run Blender through:

```bash
bash tools/oleander-runtime/blender.sh --version
bash tools/oleander-runtime/blender.sh --background scene.blend --python script.py
```

Direct `blender` invocation is also valid when the runtime has already placed Blender on `PATH`.

## Scope

This shared runtime may be used by, among others:

- product modeling and rendering;
- CMF and material visualization;
- architectural / spatial visualization;
- animation and motion studies;
- geometry inspection and conversion;
- Python `bpy` automation;
- Cycles path-traced verification;
- image/AOV generation for OLEANDER project QA.

It is not restricted to Timer Light Basin.

## Evidence boundary

`Blender available` or `Cycles render completed` proves only that the recorded runtime operation executed. It does not by itself establish:

- physical material truth;
- optical performance;
- structural or thermal validity;
- fabrication / DFM / DFA feasibility;
- compliance or safety;
- user-test results;
- release authorization.

Each project retains its own Evidence Gate and authority chain.

## Runtime persistence boundary

The absolute `/mnt/data/runtime/...` path is valid for the current managed ChatGPT execution environment. Future execution environments may rematerialize Blender at another location. That is why OLEANDER project code must use the resolver/environment contract instead of storing this absolute path inside individual projects.
