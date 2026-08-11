# OLEANDER COCOS 4 Toolchain Policy v0.8

## Scope
COCOS 4 是共享执行工具，不属于 C04 私有方法。适用范围包括：文旅交互、品牌互动、产品 UI、空间导览、网站/实时可视化原型、Practice 技能训练。

## Governance
1. 项目层不得自行 pin COCOS 版本；版本由 `90-shared/toolchains/cocos4/toolchain.env` 管理。
2. 项目层只保存 source assets / logic / data；真实 CLI materialization 由共享脚本完成。
3. Store/第三方资源必须经过 Rights Gate：代码、视觉、音频、字体分别登记；“免费”不等于可公开或可商业化。
4. UI 类游戏化不允许自动滑向 RPG 视觉；机制可复用，最终视觉需服从各项目自身证据与品牌语法。
5. `cocos start-mcp-server` 仅在明确的项目目录运行，不把整个 OLEANDER 仓库作为无边界写入根目录。
6. Engine/CLI 当前均处于 4.0 alpha / CLI alpha 阶段，所有升级先在 smoke branch/CI 验证，再修改共享 pin。

## Evidence labels
- TOOLCHAIN_SOURCE_READY
- TOOLCHAIN_BOOTSTRAP_READY
- TOOLCHAIN_INSTALLED
- PROJECT_MATERIALIZED
- WEB_BUILD_SMOKE_PASS
- PLATFORM_BUILD_PASS

未实际运行不得越级标记。
