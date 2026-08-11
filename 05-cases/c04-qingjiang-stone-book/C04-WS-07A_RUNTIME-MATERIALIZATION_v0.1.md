# C04-WS-07A｜Runtime / Visual Reading System Materialization v0.1

Status: `RUNTIME SOURCE BUILD PASS / INTERACTIVE SCENE MOUNT PENDING`

Date: 2026-08-11

## 1. Authority

This workstream materializes the already-approved research-prototype scope from `C04-WS-06｜Digital Product Architecture v1.0`, `C04-WS-07｜Visual Reading System v1.0`, and the OLEANDER shared COCOS4 toolchain.

It does not authorize field implementation, GPS/AR dependence, PHY-01, real-time operations claims, or 13/13 completion logic.

## 2. Runtime source materialized

A runtime-specific bundle is added under `assets/resources/c04/ws07a/` so COCOS can import the JSON as `JsonAsset` and load it from the built-in `resources` bundle.

The runtime contract fixes 8 Core + 5 replaceable Companion pages; S0/S1/S2 reading densities; first validation pages `R13 一线天`, `R01 红岩嘴`, `R06 多级阶地·不对称河谷`; Return/Service-first route priority; partial-is-complete My Book; static Return Guard; and S2 `FACT / LOCAL_NARRATIVE / DESIGN_READING` separation.

The pre-existing `assets/data/nodes.json` is retained as Legacy/framework history and is no longer the runtime authority for WS-07A.

## 3. Runtime code

New `assets/scripts/ws07a/` modules: `RuntimeTypes.ts`, `RuntimeCatalog.ts`, `RuntimeStore.ts`, `VisualPrototypeController.ts`, and `VisualAuditRules.ts`.

The controller intentionally exposes Creator Inspector references instead of embedding scene UUIDs in source code.

## 4. CI evidence — PASS

Authority commit: `12bdf2a4921e548db4ca6306aafb76de290d2767` on Draft PR #49.

Validated on GitHub Actions:
- `AI Governance Evals #92` — SUCCESS.
- `OLEANDER COCOS4 Smoke #25` — SUCCESS.
- `Validate C04 WS-07A runtime source` — SUCCESS.
- shared COCOS4 bootstrap — SUCCESS.
- `oleander-cocos doctor` — SUCCESS.
- C04 materialization from authoritative source pack — SUCCESS.
- `web-mobile` build — SUCCESS.

Therefore the source/build gate advances to `RUNTIME SOURCE BUILD PASS`.

## 5. What this pass does not claim

The checked-in `OleanderSmoke.scene` remains a build-smoke asset, not the final visual prototype. COCOS scripting behavior becomes interactive only after the component is mounted to scene nodes. Therefore this pass is not yet `LOCAL RUN PASS`, `VISUAL AUDIT PASS`, or `REPO RUNTIME PASS`.

Next gate: `official VisualPrototype.scene creation/mount → S0/S1/S2 runtime capture → visual audit → Route/My Book audit → REPO RUNTIME PASS`.

The preferred route is the pinned official Creator/CLI/MCP asset API. If that pinned toolchain cannot create/save SceneAsset, Node, Component and serialized references, the gate remains pending; generated Creator metadata must not be hand-authored merely to force a pass.

## 6. Visual audit targets

- S0 landscape/negative space: 85–95%; S1: 60–75%; S2: 40–60%.
- S0 must not expose record/reveal chrome.
- S1 stays within one mark + one observation + one action.
- S2 exposes one relation and keeps three claim types structurally separate.
- Return/Service stays more reachable than Companion.
- Route and book remain usable without network/GPS/AR.
- 1080×1920 plus narrow/wide mobile ratios require explicit overflow/occlusion audit.
