# OLEANDER Node Documentation Contract v0.3

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
