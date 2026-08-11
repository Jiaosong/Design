# C04 COCOS 4 Migration v0.8.2

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

## Pinned CLI correction
锁定的 COCOS CLI commit `6f810d60d89f100b5a5d6f1b0cd3518b67b15e5c` 的实际源码以 `create --project <path> --type <type>` 创建项目，并未注册 standalone `import` / `info` 命令。此前把上游文档中的漂移接口写入 Gate 属于工具链审计错误，现已修正：

1. 目标目录必须不存在；空占位目录由 materializer 安全移除，非空目录 fail-closed。
2. 官方 `create` 成功后验证 `package.json`、engine settings 与 2D/Cocos 4 元数据。
3. 叠加 C04 authoritative source assets，并验证关键 data/core 文件存在。
4. 最后执行真实 `web-mobile` build；只有 build 成功才允许标记 smoke pass。

## Gate
当前合并边界允许把 source pack、共享 toolchain 与 CI smoke 作为受治理基线进入 `main`，但不改变 C04 项目的现场/权利/科学证据 Gate。

工具链证据状态按实际运行升级：
- `SOURCE_READY`
- `TOOLCHAIN_BOOTSTRAP_READY`
- `PROJECT_MATERIALIZED`：官方 create + project/source contract 验证通过后成立。
- `WEB_BUILD_SMOKE_PASS`：真实 `web-mobile` build 成功后成立。

不得再以不存在的 `cocos import` / `cocos info` 作为通过条件，也不得把未运行的 target build 写成已通过。

## Environment audit — 2026-08-11
GitHub Actions 使用 Node `22.17.0` 和锁定的 CLI/Engine commit 执行真实 bootstrap、materialization 与 web-mobile smoke。单独的本地或 ChatGPT 沙箱若无法访问 GitHub/npm，仍不得据此声称本地 runtime 已安装或本地 build 已验证。
