# OLEANDER Blender Runtime v1.0

Status: **ACTIVE RUNTIME INTERFACE / OLEANDER ALL PROJECTS**  
Implementation revision: **1.0.1**

This runtime interface makes Blender 5.2 LTS / Cycles available to the entire OLEANDER repository without coupling any individual case, Practice package, website module, CMF study, product study, spatial project, or rendering task to a project-specific absolute path or installation workflow.

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

All OLEANDER tasks that need Blender resolve the same shared runtime in this order:

1. `$OLEANDER_BLENDER_BIN` when explicitly supplied by the runtime;
2. `blender` found on `PATH`;
3. `/mnt/data/runtime/blender-5.2.0-lts/blender` as the managed ChatGPT-runtime fallback when materialized;
4. `90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh` to rematerialize the exact verified Blender 5.2 runtime;
5. `.github/workflows/oleander-shared-blender-runner.yml` when a shared GitHub runner is the available execution carrier.

Project files must not hard-code a project-specific Blender path, vendor a Blender binary, or duplicate Blender installation/download/bootstrap logic when the shared runtime can own the capability.

## Interface state is not job-local binary state

The shared OLEANDER runtime and a single execution job are different layers.

`ACTIVE_RUNTIME_INTERFACE` means the repository-wide capability and resolution contract are Current. A new container or GitHub job may still begin without a materialized binary. That state is **not** `BLENDER_ENVIRONMENT_MISSING`.

Use this distinction:

- `MATERIALIZED` — the current job can invoke the verified binary directly;
- `NEEDS_REMATERIALIZATION` — the shared interface is active but this job does not yet have the binary;
- `RUNNER_RESOLVED` — execution moved to the approved shared runner;
- `EXECUTION_FAILED` — the approved shared resolution paths were actually attempted and failed.

`UNAVAILABLE` may be reported only after the shared resolution order and allowed shared runner paths have genuinely failed. A missing `/mnt/data/runtime/...` path by itself is never evidence that the OLEANDER Blender environment does not exist.

## Shared rematerialization

The runtime-owned implementation is:

```bash
bash 90-shared/toolchains/blender-runtime/ensure-blender-5.2.sh
```

It uses the existing verified binary first, then approved cached archives, and downloads the official Blender 5.2 archive only when necessary. The archive must pass the canonical SHA-256 gate before activation.

This is **OLEANDER runtime logic**, not project logic. Current implementation lives under the canonical `90-shared/toolchains/` area; the frozen Legacy `tools/` root is not extended by new runtime work.

## Shared runner

The reusable GitHub execution carrier is:

```text
.github/workflows/oleander-shared-blender-runner.yml
```

It is a subordinate runtime adapter under the existing OLEANDER Universal Production Environment. It is not a new METHOD, Skill, framework, Gate or project architecture.

A project consumer declares only the bounded job-specific information required for its native output, such as:

- Blender producer script path;
- optional native reopen/validation script;
- expected `.blend` path when reopen is required;
- output directory;
- artifact name.

The shared runner owns Blender runtime libraries, verified Blender 5.2 resolution/rematerialization, Python failure propagation, native execution and baseline artifact hashing/upload. Project design authority, source authority, dimensions, geometry truth, visual review and final artifact ownership remain outside the runner.

## Shared environment variables

```bash
OLEANDER_BLENDER_VERSION="5.2.0 LTS"
OLEANDER_BLENDER_BUILD="fbe6228777e7"
OLEANDER_BLENDER_HOME="<runtime-specific>"
OLEANDER_BLENDER_BIN="<runtime-specific>"
OLEANDER_RENDER_ENGINE="CYCLES"
OLEANDER_JOB_OUTPUT_DIR="<shared-runner job output directory>"
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

It is not restricted to Timer Light Basin or any other individual project.

## Evidence boundary

`Blender available`, `runner PASS` or `Cycles render completed` proves only that the recorded runtime operation executed. It does not by itself establish:

- physical material truth;
- optical performance;
- structural or thermal validity;
- fabrication / DFM / DFA feasibility;
- compliance or safety;
- user-test results;
- release authorization;
- design quality or `MAIN KEEP`.

Each project retains its own Evidence Gate and authority chain.

## Runtime persistence boundary

The absolute `/mnt/data/runtime/...` path is valid only when materialized on that execution surface. Future execution environments may rematerialize Blender elsewhere. That is why all OLEANDER project code must use the resolver, rematerialization and shared-runner contract instead of storing an absolute path or project-specific installation workflow.
