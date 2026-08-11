# C04 cocos4-source

Authoritative source pack for `C04｜清江石书｜红花峰林十三印`.

This directory remains authored source rather than a checked-in generated COCOS project. `90-shared/toolchains/cocos4/materialize-c04.sh` invokes the pinned official COCOS CLI to create a real 2D project and overlays these assets; generated project metadata stays outside the authoritative source pack.

## Active layers

- `assets/data/` — legacy v0.8 production-framework data retained for traceability.
- `assets/resources/c04/ws07a/` — WS-07A runtime manifests loaded through COCOS `resources` / `JsonAsset`.
- `assets/scripts/core/` — existing C04 state/rule baseline.
- `assets/scripts/ws07a/` — WS-07A runtime source for S0 / S1 / S2 / Route / My Book.
- `assets/scenes/OleanderSmoke.scene` — minimal build-smoke scene only; it is not the final VisualPrototype scene.

## Current gate

`SOURCE_READY / SHARED_TOOLCHAIN_SMOKE_PASS / WS07A_RUNTIME_SOURCE_BUILD_PASS / VISUALPROTOTYPE_SCENE_MOUNT_PENDING`.

Evidence for `WS07A_RUNTIME_SOURCE_BUILD_PASS`: PR #49 commit `12bdf2a4921e548db4ca6306aafb76de290d2767`; `AI Governance Evals #92` and `OLEANDER COCOS4 Smoke #25` both succeeded, including WS-07A contract validation, shared bootstrap, `doctor`, C04 materialization, and `web-mobile` build.

`VisualPrototype.scene` must be created/mounted through the official Creator/CLI/MCP asset workflow before this can be called an interactive runtime pass. Do not hand-author project-wide generated metadata to bypass that gate.
