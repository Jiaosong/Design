# OLEANDER／织作｜Post-Generation Review Gate

Status: ACTIVE
Date: 2026-08-11
Scope: All design / technical outputs, especially Practice and Spatial / SP04

## Mandatory rule

任何图纸、模型、分析图、参数表、脚本输出或交付包在“生成完成”后，必须再执行一次独立的 **Post-Generation Review｜成品审查**。自动 QA、脚本 PASS、bbox=0、文件成功导出或可复现运行，均不能替代成品审查。

## OLEANDER Artifact Review System v1.0

所有审查统一分为两层：

1. **A｜Common Review：AR-G01—AR-G10**，所有文件都必须执行。
2. **B｜Specific Review：AR-S01—AR-S09**，按文件/对象类型触发。

Canonical file: `00-governance/artifact-review-system-v1.0.md`.

一个文件只有 `Common PASS + 对应 Specific PASS` 才能标记 `POST-REVIEW PASS`；一个交付包只有全部触发 Gate 通过且 AR-S09 通过，才能标记 `PACKAGE RELEASE PASS`。历史审查未按 v1.0 重跑时，仅保留为 `LEGACY REVIEW RESULT`。

### Common Review

- AR-G01 Identity & Naming
- AR-G02 Version & Status
- AR-G03 Completeness
- AR-G04 Internal Consistency
- AR-G05 Cross-file Consistency
- AR-G06 Evidence & Truth
- AR-G07 Open & Integrity
- AR-G08 Reproduction
- AR-G09 Change Traceability
- AR-G10 Final Artifact Review

AR-G10 必须把以下内容作为独立检查项：Visual hierarchy、Boundary、**Occlusion｜遮挡**、Clearance、Geometry ↔ Dimension、**Scale / Proportion｜技术比例 + 构造比例**、View Appropriateness、Cross-view Consistency、Construction / Functional Logic、Evidence / PENDING、Export / Reproduction。

### Specific Review

- AR-S01 Drawing
- AR-S02 Model
- AR-S03 Data
- AR-S04 Code / Parametric
- AR-S05 GIS
- AR-S06 Visual / CMF
- AR-S07 Documentation
- AR-S08 Presentation
- AR-S09 Release Package

## Review scope

1. 实际打开最终 SVG / PDF / PNG / 模型，检查版面、文字、尺寸、图形、索引、图签、线型、层级、拥挤、越框、**遮挡**与阅读顺序。
2. 几何—标注一致性：标注值必须与真实几何、比例和测量方向一致。
3. 图形边界：除文字 bbox 外，检查线、尺寸界线、气泡、表格、箭头、填充、图例、局部视图。
4. 尺度与比例：声明 1:2 / 1:5 / 1:10 的视图必须真实按比例表达；示意图标 NTS；同时检查构件之间的比例关系是否误导。
5. 视图适配性：尺寸和构造关系必须放在正确的平/立/剖/详图方向表达；不同正交测量方向不得强行混画。
6. 多视图一致：同一对象在平、立、剖、详图中的位置、厚度、方向和控制层关系一致。
7. 构造逻辑：水、气、热、受力、材料、锚固、排水、保温、安装与收口不得相互冲突。
8. 证据状态：区分练习假设、外部核验事实、PENDING、厂家/结构输入、法规和项目数据。
9. 复现：确认修正真正进入最终交付文件。
10. 审查结果必须写入 README / REVIEW / REVISION / ARTIFACT_REVIEW_MATRIX / training record。

## Hard FAIL

以下问题不能通过总分平均抵消：关键遮挡、比例错误、几何—标注不一致、视图错误、多视图冲突、构造/功能逻辑错误、虚假证据/同步声明、文件无法打开。

## Status gate

- 未执行：`REVIEW PENDING`
- 发现问题：`POST-REVIEW FAIL / NEEDS REVISION`
- 修正后重审通过：`POST-REVIEW PASS`
- 所有触发 Gate + AR-S09 通过：`PACKAGE RELEASE PASS`

## Prohibited shortcuts

- 不得用自动 QA = 0 error 直接宣布合格；
- 不得生成完即交付而未打开最终成品；
- 不得发现问题后只改文档、不改源文件；
- 不得把未复核文件同步为正式候选版本；
- 不得把 Code PASS 当作 Generated Artifact PASS。

## Trigger case: SP04 R08H.1

R08H.1-C-A04 在最终成品审查中判定为 `POST-REVIEW FAIL / NEEDS REVISION`：
- A1 标题与尺寸链净空不足；
- A2 构造标注与填充/线稿拥挤；
- A2 `60 [H]` 与实际 1:2 几何长度不一致；
- 证明自动边界 QA 不能替代成品审查。
