# OLEANDER Practice｜2026

**Design Research · Experiments · Prototypes · Validation Notes**

这里收录 2026 年 OLEANDER／织作中适合在 GitHub 公开阅读、复核或运行的设计研究与实践成果，包括方法实验、交互原型、评估框架与验证记录。

这些内容作为个人研究与方法积累的一部分展示。它们可能处于练习、原型、测试计划或阶段性验证状态，因此不会因为进入 GitHub 就被描述为真实项目结果、生产成果或已完成验证。

## Project Axis Registry｜2026-08-12

现行项目轴唯一使用：

`P0 Portfolio → P1 Program → P2 Project → P3 Workstream → P4 Validation`

四层节点 `B01–B04 / CU01–CU04 / IP01–IP04 / SP01–SP04` 只描述知识/设计归属，**不是项目编号**。日期、节点和历史版本组成的既有目录保留为 artifact lineage，不从文件夹名称反推项目层级。

当前年度 Practice 项目索引：
- Business：[`PRAC-BUSINESS-2026/`](PRAC-BUSINESS-2026/)
- Culture：[`PRAC-CULTURE-2026/`](PRAC-CULTURE-2026/) — 由 2026-08-12 CU01 Material Transformation 的真实来源转译问题触发，不是为了四层对称创建空壳项目。
- IP：[`PRAC-IP-2026/`](PRAC-IP-2026/)
- Spatial：[`PRAC-SPATIAL-2026/`](PRAC-SPATIAL-2026/)

跨项目共享系统不因为主要知识节点属于某层就塞入年度 Practice。例如 Blender Surface System 的项目身份是 `SYS-BLENDER-SURFACE`，归 `PG-10｜Knowledge & Governance`；`IP03` 只是知识归属。其当前共享工具链位于 [`../../90-shared/toolchains/blender-surface-system/`](../../90-shared/toolchains/blender-surface-system/)。

交付优先级与项目层级严格分离：优先级使用 `Priority-0 / Priority-1 / Priority-2 / Priority-3`，不得再用 `P0/P1/P2/P3` 表示优先级。旧 AI `P0/P1/P2` 名称只允许作为历史 provenance；当前 AI namespace 为 `AIG-01 / AIG-02 / AIG-03`。

## Mandatory Post-Generation Review｜2026 Practice Gate

2026 年所有 Practice 记录统一执行：

`Generate → Automated QA → Open final artifact → Post-Generation Review → Fix → Re-review → Archive`

- 自动 QA、bbox=0、脚本 PASS、文件导出成功或可复现运行都不能直接证明成品通过；
- 必须实际打开最终 SVG / PDF / PNG / 模型检查视觉、图文边界、比例、几何—标注一致性、构造逻辑和证据状态；
- 未审查：`REVIEW PENDING`；
- 发现问题：`POST-REVIEW FAIL / NEEDS REVISION`；
- 修正后重审通过：`POST-REVIEW PASS`；
- 只有 `POST-REVIEW PASS` 才允许 DONE / PASS / Candidate。

Canonical rule: [`../../00-governance/post-generation-review-gate.md`](../../00-governance/post-generation-review-gate.md)

## Included

| Practice | Scope / node | Repository artifact | Source |
| --- | --- | --- | --- |
| AI design evaluation | Business / B04 | Markdown standard | https://drive.google.com/file/d/1n6aqMpMgbQPRQMfUqtVf4U6m__5iwsd4 |
| Cross-media validation | Business / B04 | Markdown report | https://drive.google.com/file/d/11xXmm8Ph6qx8_E7sZ7BL9D5CzqhL_Phu |
| Dynamic relational field | IP / IP03 | Interactive HTML prototype | https://drive.google.com/file/d/1cnUK5wlN5EP8bnL8dyxgCTGj9KWWeuuR |
| Visual hierarchy test | IP / IP03 | Blocker report | https://drive.google.com/file/d/1k3AcITnfRwjiBqRZTRLF5DL0mLmktyG7 |

The `Scope / node` column is knowledge ownership only. It must not be read as a P2/P3 project identifier.

## Source & maintenance

Status: `PROTO / E2`  
Authority: Governance v1.0.1 / ACTIVE / E2 on `main`  
Source date: 2026-08-06 to 2026-08-07

部分文本与代码成果来自 Google Drive 中的可维护源文件，并在 GitHub 中保留为可追溯版本。GitHub 负责公开展示与版本记录，Drive 仍承载部分二进制、视觉刺激物和大型源文件。

## Excluded from GitHub

- ZIP、PDF、GIF、PNG、contact sheets 和 stimulus exports 保留在 Google Drive。
- 544 KB visual-hierarchy HTML 含内嵌 raster stimuli；在资产、参与者／隐私协议和权利复核分离完成前不镜像到 GitHub。
- 迁移登记中提到 evaluation schema、evaluation script 与 actual-results analysis script，但当前规范 Drive 文件夹中不存在这些独立源文件，因此不根据描述重建。
- Rhino `.3dm` 模型及其他二进制 practice packages 保留在 Drive。

## Evidence boundary

除非具体文件明确记录了计算或执行证据，否则尺寸、权重、评分、几何和阈值均应理解为练习用假设参数或设计判断。仓库中的实践成果不自动证明实施、公共认可、建造可行性、法规合规、工程性能、市场结果、参与者结果或 E4 发布权利。
