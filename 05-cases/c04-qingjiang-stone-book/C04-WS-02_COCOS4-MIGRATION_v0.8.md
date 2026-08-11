# C04 COCOS 4 Migration v0.8

**From:** `C04_GameUI_Framework_v0.7` — Creator-ready skeleton.  
**To:** `COCOS 4 source pack + OLEANDER shared CLI materializer`.

## Source preserved
- `assets/data/chapters.json`
- `assets/data/nodes.json`
- `assets/data/ui-tokens.json`
- `assets/scripts/core/AppState.ts`
- `ExperienceRules.ts`
- `NodeRegistry.ts`

## New project rule
C04 不再自行维护一套私有 Cocos 安装。所有项目统一通过：

`90-shared/toolchains/cocos4/`

调用共享 `oleander-cocos` gateway。

## Materialization
```bash
oleander-cocos doctor
90-shared/toolchains/cocos4/materialize-c04.sh \
  05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source \
  05-cases/c04-qingjiang-stone-book/game-ui/cocos4-project
```

Then:
```bash
oleander-cocos build 05-cases/c04-qingjiang-stone-book/game-ui/cocos4-project web-mobile
```

## Gate
当前状态只允许标记：

`SOURCE_READY / TOOLCHAIN_BOOTSTRAP_READY / CLI_MATERIALIZATION_PENDING`

直到官方 `cocos create`、`cocos import`、`cocos info` 和 `web-mobile` smoke build 实际通过后，才可升级为 `PROJECT_MATERIALIZED / WEB_BUILD_SMOKE_PASS`。

## Current environment audit — 2026-08-11
当前 ChatGPT Debian 13 环境：Node `22.16.0`，低于 COCOS CLI 官方当前要求的 `22.17.0`；GitHub 与 npm registry 的外网 DNS 不可用，因此无法在本沙箱拉取上游 COCOS CLI 与依赖。OLEANDER gateway、doctor、bootstrap 已安装到共享位置，但这不等于上游 Cocos 已安装。
