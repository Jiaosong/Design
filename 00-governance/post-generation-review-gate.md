# OLEANDER／织作｜Post-Generation Review Gate

Status: ACTIVE
Date: 2026-08-11
Scope: All design / technical outputs, especially Practice and Spatial / SP04

## Mandatory rule

任何图纸、模型、分析图、参数表、脚本输出或交付包在“生成完成”后，必须再执行一次独立的 **Post-Generation Review｜成品审查**。自动 QA、脚本 PASS、bbox=0、文件成功导出或可复现运行，均不能替代成品审查。

## Review scope

1. 实际打开最终 SVG / PDF / PNG / 模型，检查版面、文字、尺寸、图形、索引、图签、线型、层级、拥挤、越框、遮挡与阅读顺序。
2. 几何—标注一致性：标注值必须与真实几何、比例和测量方向一致。
3. 图形边界：除文字 bbox 外，检查线、尺寸界线、气泡、表格、箭头、填充、图例、局部视图。
4. 尺度：声明 1:2 / 1:5 / 1:10 的视图必须真实按比例表达；示意图标 NTS。
5. 构造逻辑：水、气、热、受力、材料、锚固、排水、保温与收口不得相互冲突。
6. 证据状态：区分练习假设、外部核验事实、PENDING、厂家/结构输入、法规和项目数据。
7. 复现：确认修正真正进入最终交付文件。
8. 审查结果必须写入 README / REVIEW / REVISION / training record。

## Status gate

- 未执行：`REVIEW PENDING`
- 发现问题：`POST-REVIEW FAIL / NEEDS REVISION`
- 修正后重审通过：`POST-REVIEW PASS`
- **只有 `POST-REVIEW PASS` 才允许标记 DONE / PASS / Candidate。**

## Prohibited shortcuts

- 不得用自动 QA = 0 error 直接宣布合格；
- 不得生成完即交付而未打开最终成品；
- 不得发现问题后只改文档、不改源文件；
- 不得把未复核文件同步为正式候选版本。

## Trigger case: SP04 R08H.1

R08H.1-C-A04 在最终成品审查中判定为 `POST-REVIEW FAIL / NEEDS REVISION`：
- A1 标题与尺寸链净空不足；
- A2 构造标注与填充/线稿拥挤；
- A2 `60 [H]` 与实际 1:2 几何长度不一致；
- 证明自动边界 QA 不能替代成品审查。
