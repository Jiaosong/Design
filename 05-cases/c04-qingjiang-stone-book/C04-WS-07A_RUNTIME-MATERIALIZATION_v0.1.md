# C04-WS-07A｜Runtime / Visual Reading System Materialization v0.1

Status: `RUNTIME SOURCE BUILD PASS / OFFICIAL SCENE MATERIALIZATION PASS / VISUALPROTOTYPE WEB-MOBILE BUILD PASS / RUNTIME CAPTURE ACTIVE / VISUAL AUDIT OPEN`

Date: 2026-08-11

## 1. Authority

This workstream materializes the already-approved research-prototype scope from `C04-WS-06｜Digital Product Architecture v1.0`, `C04-WS-07｜Visual Reading System v1.0`, and the OLEANDER shared COCOS4 toolchain.

It does not authorize field implementation, GPS/AR dependence, PHY-01, real-time operations claims, or 13/13 completion logic.

## 2. Runtime source materialized

A runtime-specific bundle is added under `assets/resources/c04/ws07a/` so COCOS can import the JSON as `JsonAsset` and load it from the built-in `resources` bundle.

The runtime contract fixes 8 Core + 5 replaceable Companion pages; S0/S1/S2 reading densities; first validation pages `R13 一线天`, `R01 红岩嘴`, `R06 多级阶地·不对称河谷`; Return/Service-first route priority; partial-is-complete My Book; static Return Guard; and S2 `FACT / LOCAL_NARRATIVE / DESIGN_READING` separation.

The pre-existing `assets/data/nodes.json` is retained as Legacy/framework history and is no longer the runtime authority for WS-07A.

## 3. Runtime code

Runtime modules under `assets/scripts/ws07a/`: `RuntimeTypes.ts`, `RuntimeCatalog.ts`, `RuntimeStore.ts`, `VisualPrototypeController.ts`, and `VisualAuditRules.ts`.

`VisualPrototypeController` resolves the stable scene naming contract at runtime rather than embedding generated Creator UUIDs. The current capture branch also exposes a bounded `globalThis.__OLEANDER_WS07A__` research/test bridge for deterministic browser-state capture and removes it when the component is destroyed.

## 4. Verified CI evidence

### 4.1 Runtime source/build — PASS

Initial authority commit: `12bdf2a4921e548db4ca6306aafb76de290d2767` on Draft PR #49.

GitHub Actions verified:
- WS-07A runtime contract validator — SUCCESS.
- shared COCOS4 bootstrap — SUCCESS.
- `oleander-cocos doctor` — SUCCESS.
- C04 materialization from authoritative source pack — SUCCESS.
- `web-mobile` build — SUCCESS.

Therefore `RUNTIME SOURCE BUILD PASS` is established.

### 4.2 Official VisualPrototype scene materialization — PASS

`OLEANDER COCOS4 Smoke #28` on PR #49 commit `2ac2c4368dbcf90c4ee220790228162078bbaa87` completed SUCCESS.

That run used the pinned official COCOS MCP asset API to:
- create/open `VisualPrototype.scene`;
- create the WS-07A node hierarchy;
- add/set COCOS UI components;
- mount `C04WS07AVisualPrototypeController`;
- save, reload and query the generated scene;
- remove the legacy `OleanderSmoke.scene` from build evidence;
- build the generated VisualPrototype as `web-mobile`.

Therefore `OFFICIAL SCENE MATERIALIZATION PASS` and `VISUALPROTOTYPE WEB-MOBILE BUILD PASS` are established. Generated Creator project metadata remains generated output, not authored source authority.

### 4.3 Browser runtime capture — ACTIVE

Current PR #49 head: `e56c1b561b7ccfd28a6a76087e4e9ee6893d8782`.

The active CI adds deterministic HTTP-served browser capture using Chrome DevTools Protocol without introducing Playwright/Puppeteer dependency drift. It targets:
- `1080×1920`;
- `390×844` narrow mobile;
- `844×390` wide/landscape mobile.

For each viewport it drives and captures:
1. S0 一线天;
2. S1 红岩嘴;
3. S1 record state;
4. S2 河谷;
5. S2 Reveal;
6. Route;
7. My Book.

Expected evidence is 18 screenshots plus `runtime-capture-report.json`, browser console/runtime exception records, scene proof and UITransform world-space AABB snapshots. Structural runtime failures are fail-closed; AABB overlap candidates are recorded for visual review rather than silently promoted to `VISUAL AUDIT PASS`.

## 5. Current gate boundary

Established:
- `RUNTIME SOURCE BUILD PASS`;
- `OFFICIAL SCENE MATERIALIZATION PASS`;
- `VISUALPROTOTYPE WEB-MOBILE BUILD PASS`.

Open:
- `RUNTIME CAPTURE` — current CI executing;
- `VISUAL AUDIT` — requires inspection of actual screenshots and geometry evidence;
- `LANDSCAPE FIRST FINAL VISUAL PASS` — cannot be claimed while `LandscapeSlot` is still placeholder media;
- `REPO RUNTIME PASS` — only after runtime capture + visual audit closure.

No runtime/build result in this workstream changes `G1F IMPLEMENTATION HOLD` for field installation or engineering claims.

## 6. Visual audit targets

- S0 landscape/negative space: 85–95%; S1: 60–75%; S2: 40–60%.
- S0 must not expose record/reveal chrome.
- S1 stays within one mark + one observation + one action.
- S2 exposes one relation and keeps three claim types structurally separate.
- Return/Service stays more reachable than Companion.
- Route and book remain usable without network/GPS/AR.
- 1080×1920 plus narrow/wide mobile ratios require explicit overflow/occlusion audit.
- A structural runtime capture pass is not equivalent to a visual-design pass.
