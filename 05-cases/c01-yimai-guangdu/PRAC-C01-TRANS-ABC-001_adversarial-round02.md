# PRAC-C01-TRANS-ABC-001｜Adversarial Round 02｜版本身份盲法 × 提示污染

**状态：SIMULATED PROTOCOL STRESS TEST ONLY / NOT HUMAN TEST / NOT EFFECT VALIDATION**

## 1｜实验目的

本轮不问“旧版还是 v0.2 更好”，而问：

1. 回答中的关系、制度、治理、继续核验等概念，有多少可能是题目本身带进去的？
2. 当这些概念不出现在首读题目里时，它们是否仍然出现？
3. 研究者在不知道版本身份的情况下，能否稳定区分 prompt leakage 与 spontaneous relation emergence？

## 2｜盲法边界

这不是医学意义上的完全双盲。参与者能够看到题目语义，因此不可能对“提示内容”失明。

实际采用：
- 参与者版本身份盲法：只显示 X / Y / Z，不显示 OLD / v0.2 / N0；
- 研究者编码盲法：编码数据去除 condition、card ID 与版本名称；
- 协调者密钥：条件映射单独保存，在编码锁定后才解盲。

准确名称：`masked version identity + blinded coding`。

## 3｜为什么增加 N0

v0.2 已删除“解释权”和“谁必须遵守什么”，但仍提示：

`人 / 行为 / 制度 / 生活情境 / 继续问什么 / 问谁或查什么`

因此 v0.2 仍不能直接测“关系是否自发出现”。

N0 只问：

`第一眼注意到什么 → 哪些内容值得继续了解 → 还有什么想知道`

它不提示 actor / institution / governance / next verifier，作为 spontaneous relation emergence 的校准条件。

## 4｜确定性提示污染审计

| 条件 | 明示维度数 | 明示内容 | 可否直接测 SRE |
|---|---:|---|---|
| OLD | 4 | actor/regulation, interpretation governance, unresolved question, next verifier | NO |
| v0.2 | 4 | actor/relation, unresolved question, next verifier, uncertainty | NO |
| N0 | 1 | unresolved curiosity only | YES, for relation/governance dimensions |

**关键否决：把 v0.2 中由“人 / 行为 / 制度”提示后出现的回答记为 spontaneous relation emergence 是无效的。**

## 5｜Prompt Leakage Score / PLS

0–4：
- +1：复用显著提示词或近义概念；
- +1：出现被提示的关系/治理概念，但没有独立观察、来源或自生例子；
- +1：回答结构明显复制题目顺序；
- +1：问题/下一步只是改写或选择题目给出的路径。

PLS 是污染诊断指标，不是学习效果分数。

## 6｜Spontaneous Relation Emergence / SRE

0–3，且只编码未被该条件显式提示的维度：
- 0：只有对象/形式描述；
- 1：自发出现 actor/action/context 关系，但模糊；
- 2：关系 + 证据/未知边界；
- 3：关系 + 证据边界 + 自主问题 + 独立命名的继续核验来源。

若该维度已在题目中出现，必须标 `CONTAMINATED / NA`。

## 7｜模拟压力记录

12 种响应风格 × 3 条件 = 36 条协议压力记录。它们是为了攻击评分规则而预设的行为脚本，不是对真实游客/村民的预测。

内部协议自检：
- OLD：mean PLS 2.17；PLS≥3 为 6/12；SRE = CONTAMINATED / NA。
- v0.2：mean PLS 1.58；PLS≥3 为 2/12；SRE = CONTAMINATED / NA。
- N0：mean PLS 0.0；PLS≥3 为 0/12；模拟 SRE mean 1.17/3。

这些数值只证明协议能检测预先植入的污染模式，不能作为真实人群效应量。

## 8｜判决

- OLD：`REJECT / ARCHIVE AS CONTAMINATED CONTROL`。
- v0.2：`KEEP AS FACILITATED EXPLORATION / REJECT AS SRE MEASUREMENT CONDITION`。
- N0：`ADD AS REQUIRED FIRST-PASS CONTROL`。

## 9｜v0.3 实验结构

`N0 spontaneous → B1 evidence boundary → C1 facilitated relation probe`

### N0｜Neutral First Read
不出现关系型术语；用于测 first-reading unit 与 SRE。

### B1｜Evidence Boundary
N0 提交后才进入：
`我看到 / 来源说 / 我猜 / 我不知道 / 先验知识 / 来源冲突`

### C1｜Facilitated Relation Probe
前两层保存后才出现关系探针；用于观察提示后能否深化、修正或拒绝关系，不用于计算 spontaneous emergence。

## 10｜真人测试前 Gate

- coder 不得看到 condition key；
- coordinator 在 coder 完成第一轮编码后锁表；
- 至少一部分记录由第二编码者独立复核；
- PLS/SRE 分歧先记录，不通过讨论“平均掉”；
- 解盲后只比较污染与自发关系，不比较“谁写得更丰富”；
- 不使用模拟数据估算样本量或成功率。

**HUMAN TEST：NOT RUN。**
