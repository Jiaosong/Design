# OLEANDER Shared COCOS 4 Toolchain v0.8

目标：把 COCOS 4 + COCOS CLI 从 C04 专项工具提升为 **OLEANDER 全仓共享数字交互工具链**，所有 Business / Culture / IP / Spatial / Cases / Practice 项目均通过同一入口调用。

## 固定版本
- Node.js: `22.17.0+`
- COCOS 4 Engine: `4.0.0-alpha.30`, SHA `ed0751652be521933d8e105fad29ff4ac356bf68`
- COCOS CLI: package `0.0.1-alpha.38`, pinned SHA `6f810d60d89f100b5a5d6f1b0cd3518b67b15e5c`

## 全局入口
安装后任何 OLEANDER 项目都只使用：

```bash
oleander-cocos doctor
oleander-cocos create ./path/to/project 2d
oleander-cocos import ./path/to/project
oleander-cocos build ./path/to/project web-mobile
oleander-cocos info ./path/to/project
oleander-cocos mcp ./path/to/project 9527
```

`oleander-cocos` 是 OLEANDER 层的稳定入口；上游 `cocos` CLI 的 alpha 变化不会直接污染各项目脚本。

## C04 升级原则
旧 `C04_GameUI_Framework_v0.7` 不伪装成 CLI 已创建项目，而重构为 `cocos4-source`：保存领域数据、13节点、四章节、TypeScript core 和视觉资源。上游 CLI 可用后，通过 `materialize-c04.sh` 调用官方 `cocos create --type 2d` 生成真实工程，再同步 source assets，避免伪造项目元数据。

## 当前沙箱说明
当前 ChatGPT Debian 环境无 GitHub/npm 外网 DNS，因此 **可以安装并暴露 OLEANDER gateway / doctor / bootstrap，但不能在本沙箱完成上游 COCOS CLI 的 clone + npm dependency install**。这不被记作“Cocos 已安装”。在有正常网络的 Linux/CI 上运行 `bootstrap-linux.sh` 才会完成真正安装。