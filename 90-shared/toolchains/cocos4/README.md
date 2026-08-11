# OLEANDER Shared COCOS 4 Toolchain v0.8.2

目标：把 COCOS 4 + COCOS CLI 从 C04 专项工具提升为 **OLEANDER 全仓共享数字交互工具链**，所有 Business / Culture / IP / Spatial / Cases / Practice 项目均通过同一入口调用。

## 固定版本
- Node.js: `22.17.0+`
- COCOS 4 Engine: `4.0.0-alpha.30`, SHA `ed0751652be521933d8e105fad29ff4ac356bf68`
- COCOS CLI: package `0.0.1-alpha.38`, pinned SHA `6f810d60d89f100b5a5d6f1b0cd3518b67b15e5c`

## 全局入口
安装后 OLEANDER 项目通过共享 gateway 使用锁定 CLI：

```bash
oleander-cocos doctor
oleander-cocos create ./path/to/project 2d
oleander-cocos build ./path/to/project web-mobile
oleander-cocos mcp ./path/to/project 9527
```

`oleander-cocos` 是 OLEANDER 层的稳定入口；上游 `cocos` CLI 的 alpha 变化不会直接污染各项目脚本。

### Pinned CLI command boundary
当前锁定的 CLI commit 实际注册 `create`、`build`、`start-mcp-server` 等命令，但**没有注册 `import` 或 `info` 命令**。因此 OLEANDER gateway 不伪造这两个入口。项目 materialization 通过官方 `create --project ... --type 2d` 生成工程，再叠加治理后的 source assets，并以项目元数据／源文件 contract + 真正的 target build 作为验证。

## C04 升级原则
旧 `C04_GameUI_Framework_v0.7` 不伪装成 CLI 已创建项目，而重构为 `cocos4-source`：保存领域数据、13节点、四章节、TypeScript core 和视觉资源。上游 CLI 可用后，通过 `materialize-c04.sh` 调用官方 `cocos create --project ... --type 2d` 生成真实工程，再同步 source assets，避免伪造项目元数据。

`materialize-c04.sh` 必须把目标路径交给官方 create；由于锁定 CLI 会拒绝任何已存在的目标目录，脚本只允许删除空占位目录，非空目录一律 fail-closed。

## 当前执行状态
GitHub Actions 已具备正常 GitHub/npm 网络，可通过共享 bootstrap 安装锁定 runtime 并执行 C04 smoke。任何本地或沙箱环境若无法完成 clone、依赖安装和 target build，不得标记为 `TOOLCHAIN_INSTALLED` 或 `WEB_BUILD_SMOKE_PASS`。
