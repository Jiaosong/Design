# OLEANDER Node Documentation Contract v0.3.2

[← Node Index](README.md)

## 1｜Hard Rule

> **ONE LOGICAL PRODUCT NODE → ONE PRIMARY NODE DOCUMENT**

允许存在：
- parent map；
- trace matrix；
- test/eval evidence；
- decision log；
- implementation reference。

不允许：
- 两份不同文档都自称同一节点的 Current product definition；
- 在 Master PRD、Feature Spec、Node Doc 中复制三套正文并各自漂移。

---

## 2｜Node ID

格式：

```text
N00
N01
N02
N03
N03A
...
```

Node ID 是**产品文档 locator**，不是 OLEANDER Project ID、runtime object ID 或 authority ID。

---

## 2A｜Node Levels

Node 粒度不是按文件数量机械拆分，而是按**独立产品责任**拆分：

| Level | Example | Meaning |
|---|---|---|
| Root | N00 | 整体产品边界 / graph root |
| Primary | N01 HOME / N06 ARTIFACTS / N10 SESSION KERNEL | first-class surface / kernel / control |
| Mode / Subsystem | N03A EXPLORE / N10A RESUME | 有独立 product job 的子系统 |
| Atomic | N01A Resume Snapshot / N06D Readback / N11B Scoped Rights | 可独立定义输入、输出、authority、failure、acceptance、metric 的最小产品能力 |

Feature 只有同时满足以下条件才提升为 Atomic Node：

1. 有独立的 product job；
2. 有明确 inputs / outputs；
3. 有独立 Human/System authority boundary；
4. 有自己的 failure / degraded behaviour；
5. 有独立 acceptance / metric / evaluation value；
6. 被多个 flow、surface 或 downstream object 引用，值得拥有稳定 identity。

否则继续保留为 Requirement，不为“一个功能点一个文件”而碎片化。

---

## 3｜Node Card

每个节点顶部必须给出：

| Field | Meaning |
|---|---|
| Node ID | 产品节点 ID |
| Parent | 父节点 |
| Children | 子节点 |
| Type | Surface / Mode / Kernel / Control / Integration |
| User | Primary user |
| Product job | 单一主要责任 |
| Inputs | 消费什么 |
| Outputs | 产生什么 |
| Authority | Human/System 边界 |
| Primary metric | 主要产品指标 |
| Release priority | P0/P1/P2 |
| Doc state | WORKING / OPEN / HOLD |

---

## 4｜Relationship First

节点正文优先用图表达关系。

推荐：

### Mindmap
适合：对象层级、模块拆分、问题空间。

### Flowchart
适合：用户流程、依赖、输入输出。

### State Diagram
适合：局部生命周期；必须注明不等于 Project State。

### Sequence Diagram
适合：Human / Kernel / Tool / Authority / Readback 交互。

### ER-like Flowchart
适合：对象关系。

---

## 5｜Mermaid Rule

优先用 GitHub 可直接渲染的 Mermaid，避免把重要逻辑只做成不可编辑图片。

一个节点至少应有：
- 1 张 node context graph；
- P0 节点至少再有 1 张核心 flow / state / sequence 图。

---

## 5A｜One Map One Document

产品图遵守：

> **ONE CORE MAP → ONE MAP DOCUMENT**

总览 README 只做地图索引。复杂关系分别维护为 Product Mindmap、Human–AI Loop、Autonomy × Control、Artifact Truth Chain、Decision Chain、Release Gates、Atomic Detail Maps 等独立 Mermaid 文档。

地图是关系视图，不是 authority。边类型必须遵守 [Node Relation Schema](NODE_RELATION_SCHEMA_v0.3.2.md)。

---

## 6｜No Duplication Rule

Parent doc：
- 只保留 summary；
- link child；
- 不复制 child acceptance criteria。

Child doc：
- 维护具体行为；
- parent 只引用。

Master PRD：
- 维护产品范围 / cutline / decision；
- 不作为所有节点的长篇正文容器。

---

## 7｜Trace Rule

每个 P0/P1 Node 至少连接：

```text
USER NEED
→ NODE
→ FEATURE / REQUIREMENT
→ ACCEPTANCE
→ EVENT / METRIC
→ EVAL / PILOT
```

Node 文档不是需求的终点。

---

## 7A｜Atomic Node Minimum Contract

每个 Atomic Node 至少必须具有：

```text
NODE CARD
CONTEXT GRAPH
PRODUCT CONTRACT
REQUIREMENT LINKS
ACCEPTANCE
FAILURE / DEGRADED BEHAVIOUR
EVENTS / METRICS
RELATIONS
```

Build-ready 之前再补齐真实 owner、依赖、test/eval evidence 和 release gate；不存在的 owner 或尚未执行的实验必须显式写 OPEN / UNASSIGNED / NOT_RUN。

---

## 8｜Authority Rule

Node docs 不允许：
- self-promote；
- 改变 Project Current；
- 伪造 professional authority；
- 通过 UI 节点重新定义 Governance。

如果产品要求与 Current architecture 冲突：

> **Architecture / owner-native Current wins; product doc becomes REVISE.**

---

## 9｜Change Rule

修改一个节点：
1. 修改本 Node Doc；
2. 检查父/子关系；
3. 检查 maps；
4. 检查 trace；
5. 检查 metrics / launch impact；
6. 如改变重要产品决策，更新 Product Decision Log。

不要在多个长文档中手工复制同一修改。

---

## 10｜Definition of Ready

节点进入 build-ready 前至少回答：
- user/context；
- product job；
- inputs/outputs；
- Human/System allocation；
- dependencies；
- happy path；
- failure path；
- acceptance；
- telemetry；
- owner；
- release priority。

## 11｜Definition of Done

节点实现完成不等于产品完成。

最低闭环：

```text
BUILD
→ ACTUAL RESULT
→ READBACK
→ ACCEPTANCE
→ METRIC / EVAL
→ RELEASE DECISION
```
