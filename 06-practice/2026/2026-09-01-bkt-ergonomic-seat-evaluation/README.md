# PRJ-BKT01-ERGO-EVAL｜BKT 人体工学护腰坐姿椅｜人机工程学尺寸评价

Status: WIP / REVIEW PENDING  
Project Axis: P2 Project  
Parent Program: PG-30｜Cases & Practice  
Governance: `00-governance/README.md` — Governance v1.1.1 ACTIVE  
Practice Root: `06-practice/`  
Notion P2 Registry: https://app.notion.com/p/3ceb86be5c478116a9d4d0c11db3df13?pvs=204  
Runtime Tracker: https://github.com/Jiaosong/Design/issues/471  

## 1. Goal

完成一份可直接提交的人机工程学产品尺寸评价作业，并使结论能够区分：

- 已确认产品事实；
- 官方宣传主张；
- 人体尺寸证据；
- 本项目分析推论；
- 待验证问题；
- 已冻结结论。

最终输出应回答：**BKT 人体工学护腰坐姿椅的关键接触尺寸与成年用户坐姿人体尺寸之间是否形成可辩护的人机工程学匹配，其支撑逻辑、局限与优化方向是什么？**

## 2. Scope

本项目包含：

1. 产品身份、型号、使用场景与官方信息整理；
2. 产品关键尺寸：总宽 420 mm、总高 340 mm、总深 315 mm；
3. 产品尺寸标注图；
4. 人体坐姿分析图；
5. 产品功能分区图；
6. 人体尺寸数据库与数据来源核验；
7. 人体尺寸 ↔ 产品尺寸匹配评价；
8. 背部、腰椎、骨盆、臀部的支撑关系分析；
9. 问题识别与优化建议；
10. Word 最终报告整合与提交前审查。

## 3. Out of Scope

- 不把该产品当作完整办公椅进行全部座椅参数评价；
- 不把官方 AGR、专利、材料宣传自动等同于本项目独立验证；
- 不在缺少来源时冻结虚构的身高、体重或百分位覆盖范围；
- 不把 AI 生成分析图视为真实测量或实验数据；
- 不把“文件已生成”写成“人体工程学结论已验证”。

## 4. Evidence Baseline

### Confirmed / Working Facts

- 产品：BKT 人体工学护腰坐姿椅；
- 已知型号：加大款、超大款；
- 已提供尺寸：420 mm × 340 mm × 315 mm；
- 官网宣传包含：三角稳固一体承托、S 型贴合、高密度慢回弹、透气面料、多场景使用、AGR 人体工学相关认证宣传等。

### Existing Design Artifacts

- 产品尺寸标注图：已生成，需最终文字与尺寸审查；
- 人体坐姿分析图：已生成，需检查是否把外部座椅决定的角度误归因于产品；
- 产品功能分区图：已生成，需与最终正文术语统一；
- Word 报告草稿：已形成，需要按证据链重构。

### Open Evidence

- 成人关键人体测量项目的可靠来源、测量定义与 P5/P50/P95 数据；
- 420 mm 横向尺寸对应的实际有效承托宽度，而非仅外廓宽度；
- 315 mm 应定义为产品总深、有效承托深度还是其他几何量；
- 340 mm 对应的有效背腰支撑范围；
- 官方认证、专利与材料宣传的原始可核验文件。

## 5. Current Decision Question

**哪些人体尺寸与产品接触尺寸能够被可靠验证，并据此形成不夸大、不混淆完整座椅参数的人机工程学评价？**

## 6. OLEANDER Runtime

Current Loop: Exploration  
Design State: EXPLORE  
Current Gate: G1｜Evidence  

Working sequence:

`Read → Frame → Evidence Baseline → Define Measurement Objects → Compare → Reject unsupported claims → Candidate Evaluation → Report Integration → Post-Generation Review`

## 7. Workstreams

- WS-01｜Product Facts & Source Boundary
- WS-02｜Anthropometric Evidence Dataset
- WS-03｜Dimension Fit Evaluation
- WS-04｜Posture & Support Mechanics
- WS-05｜Issues / Optimization / Final Report

## 8. Gate Plan

- G0｜任务与评价对象：PASS
- G1｜人体与产品证据：CURRENT
- G2｜评价命题：PENDING
- G3｜图文分析结构：PARTIAL /已有初稿
- G4｜交叉比较与一致性检查：PENDING
- G6｜最终 Word 交付准备：PENDING
- G8｜提交前验收：PENDING

## 9. Review Contract

所有最终图、表、Word 内容均遵守：

`Generate → Automated/Logical QA → Open final artifact → Post-Generation Review → Fix → Re-review → Archive`

当前项目整体状态：**REVIEW PENDING**。

## 10. Immediate Next Step

先冻结 WS-01：产品身份、尺寸定义、官方主张与“本项目可独立验证事实”的边界；随后进入 WS-02 人体尺寸数据库核验。
