# OLEANDER PRD Feature Spec｜MAP + ARTIFACTS v0.2.0

[← Feature Specs](README.md) · [← Master PRD](../OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

**Scope:** Design Relation、Dependency、Change Impact、Artifact Identity、Revision、Native Source、Fidelity、Readback。  
**State:** WORKING PRODUCT SPEC / NON-AUTHORITY.

---

# 1｜MAP — Design Map

## 1.1 Product job

MAP 表达：

> **设计中什么关系重要、什么影响什么、变化会传播到哪里。**

它不是 BIM 模型、流程图、Task Graph 或组织结构图。

## 1.2 Layers

- Intent Layer
- Problem Layer
- Relation Layer
- Decision Layer
- Dependency Layer
- Artifact Layer
- Review Layer

---

# 2｜MAP Feature Requirements

## MAP-F01｜Relation Create

**Purpose**  
建立值得被持续判断、改变、保护或协同的 Design Relation。

**Minimal semantics**
- subject
- relation
- object
- significance
- linked Design Value
- linked realization
- scope
- owner if relevant

**Rule**
不是所有关系都应该 first-class。只有 materially affect judgment / change impact / integration / continuity / review 的关系才显式化。

**Acceptance**
创建 relation 时必须能解释“为什么值得单独维护”。

**Priority** P0

---

## MAP-F02｜Relation Link

支持：
- affects
- depends on
- carries value
- constrained by
- represented by
- verified by
- conflicts with
- coupled with

**Acceptance**
Link 不能只有 generic “related to”。

**Priority** P0

---

## MAP-F03｜Relation Importance

语义：
- CORE
- SUPPORTING
- LOCAL

这是设计理解语义，不是 Project State。

**Acceptance**
Importance 可以被 Human 修改；system recommendation 不自动 authoritative。

**Priority** P1

---

## MAP-F04｜Relation Stability

局部语义：
- STABLE
- PROVISIONAL
- OPEN

**Rule**
这些状态只描述当前 relation 的设计稳定度，不取代 Current/Candidate/Promotion state。

**Priority** P1

---

## MAP-F05｜Change Impact

**Trigger**
- Design Relation changed
- Constraint changed
- Artifact revision
- Professional input change
- Validation contradiction
- Question reframe

**Required output**
- directly affected relations
- downstream relations
- affected decisions
- affected artifacts
- affected domains
- affected verification / validation
- unaffected valid scope

**Acceptance**
不得默认全局 reopen。

**Events**
- `change_impact_requested`
- `change_impact_resolved`
- `revision_scope_created`

**Priority** P0

---

## MAP-F06｜Whole / Local Filter

用户可以：
- 看 whole design；
- 聚焦一个 subsystem / scene / component；
- 从 local 返回 whole；
- 保留 local change 对 whole 的影响提示。

**Acceptance**
Local view 不得让用户误以为未显示的 relation 不存在。

**Priority** P1

---

## MAP-F07｜Artifact Binding

每个关键 relation 可绑定：
- native artifact
- prototype
- simulation
- representation
- readback

**Acceptance**
必须显示 artifact role，避免 preview 冒充 source。

**Priority** P0

---

## MAP-F08｜Issue / Finding Binding

Finding 必须能定位到：
- Relation
- Artifact
- Decision
至少一个。

**Acceptance**
“整体感觉不好”可以先保存为 unstructured concern，但在形成 Finding 前需要进一步定位。

**Priority** P0

---

## MAP-F09｜Professional Binding

显示：
- which domains participate
- who owns professional claim
- shared variable
- interface conflict
- required response

**Rule**
Professional binding 不授予 whole-design authority。

**Priority** P1

---

## MAP-F10｜Dependency Traversal

支持从任何 critical object 查看：
- upstream basis
- downstream effect
- current consumers
- review / validation dependency

**Priority** P1

---

## MAP-F11｜Preserve Unaffected Scope

Revision Scope 生成时必须显式列出：
- AFFECTED
- PRESERVED
- UNKNOWN

**Acceptance**
未受影响的 valid work 不被默认重开。

**Priority** P0

---

# 3｜ARTIFACTS — Artifact & Reality

## 3.1 Product job

> **让真实 artifact 成为设计循环的一部分，并保持 artifact identity / role / revision / readback 可理解。**

## 3.2 Artifact roles

- Native Design Source
- Working Source
- Canonical Derivative
- Export
- Preview
- Prototype
- Simulation
- Reference
- AI Visual
- Snapshot

---

# 4｜ARTIFACT Feature Requirements

## ART-F01｜Artifact Register

**Purpose**
建立 logical artifact identity。

**Required fields**
- artifact_ref
- logical object
- role
- owner
- native/editor source if applicable
- current revision
- representations
- linked Question / Relation
- last readback

**Boundary**
Artifact registry semantics 不意味着 PRD 新建第二套 canonical artifact authority；正式 owner 仍由既有 architecture 决定。

**Priority** P0

---

## ART-F02｜Artifact Role

系统必须明确显示 artifact 是：
- source
- prototype
- evidence
- presentation
- derivative
- simulation
- snapshot

**Acceptance**
用户不能仅因“这个文件更新”就误把 presentation 当 source。

**Priority** P0

---

## ART-F03｜Native Source Link

**Purpose**
把 design reasoning 返回真实 editable source。

**Acceptance**
需要继续深化的生产级 artifact 必须能定位 native/editable carrier，或明确声明当前缺失。

**Failure**
Native 不可用时：
- 可以保留 bounded editable substitute；
- 必须 HOLD native completion claim。

**Priority** P0

---

## ART-F04｜Revision Identity

一次 meaningful design change 产生 revision identity。

**Meaningful change examples**
- relation changed
- geometry changed
- behaviour/state changed
- design decision implemented
- critical bug repaired

**Non-meaningful examples**
- metadata touch
- file timestamp only
- export regenerated with no material change

**Priority** P0

---

## ART-F05｜Design Relation Binding

Artifact 必须说明它表达/测试哪些 relation。

**Acceptance**
“这是最终图”而无 Question / Relation 关系不足以满足 design trace。

**Priority** P0

---

## ART-F06｜Design Question Binding

Artifact 可以明确：
- what question it helps answer
- key unknown
- fidelity
- does-not-prove

**Priority** P1

---

## ART-F07｜Readback Entry

每次 material making 后应产生 readback。

**Readback fields**
- artifact ref
- revision
- content identity / hash when available
- method
- observed result
- unexpected result
- verified invariants
- findings
- claim ceiling

**Acceptance**
producer assertion / tool log 不能替代 readback。

**Priority** P0

---

## ART-F08｜Cross-Version Compare

支持：
- predecessor / successor
- before / after
- Human steer before / after
- expected / observed

**Acceptance**
必须绑定具体 revisions。

**Priority** P1

---

## ART-F09｜Fidelity / Claim Ceiling

Artifact 必须说明当前 fidelity 能证明到什么程度。

示例：
- relation-level prototype
- non-metric spatial diagram
- visual concept only
- browser prototype
- physical mock-up
- tested sample
- field-measured drawing

**Rule**
低 fidelity 不阻止探索，但限制 claim。

**Priority** P0

---

## ART-F10｜Revision + Content Binding

Human-steered second round、critical review、high-impact handoff 应尽可能绑定：
- revision identity
- content hash / equivalent immutable identity
- lineage

**Acceptance**
同名文件 / 相同 revision string 不能单独证明内容一致。

**Priority** P0

---

## ART-F11｜Stale Artifact Warning

**Trigger**
- Current authority points to newer revision
- presentation derivative newer than native but not authoritative
- readback refers to older content
- downstream consumer uses stale artifact

**Required behaviour**
- warn affected operation
- block authority-sensitive mutation when necessary
- allow unrelated reversible exploration

**Priority** P0

---

## ART-F12｜Degraded Substitute

当 native surface 暂不可用时，可使用：
- editable SVG
- HTML/CSS/JS prototype
- simplified CAD-like geometry
- structured data
- other truthful carrier

前提：
- substitute 能回答当前 key unknown；
- 不声称 native completion；
- downstream claim ceiling 降低。

**Priority** P1

---

# 5｜Readback Levels

Readback 不使用一个总 PASS。

可以分别观察：

## Whole
整体关系、hierarchy、sequence、coherence。

## Region / Subsystem
局部与整体关系。

## Object / Component
具体 artifact / mechanism / geometry。

## Detail / State
尺寸、状态、interaction、material、behaviour。

## Use / Runtime
真实操作、浏览器、simulation、physical use。

---

# 6｜Artifact State Honesty

以下必须保持分离：

```text
FILE EXISTS
≠ ARTIFACT CURRENT
≠ ARTIFACT READ
≠ ARTIFACT VALID
≠ DESIGN KEEP
≠ PROFESSIONAL PASS
```

---

# 7｜MAP + ARTIFACT Core Flow

```text
DESIGN QUESTION
→ MAP identifies critical Relation
→ STUDIO changes Relation
→ ARTIFACT target selected
→ make/edit native or truthful substitute
→ new revision
→ actual READBACK
→ observed delta
→ MAP updates affected scope
→ REVIEW
→ preserve / revise / reopen
```

---

# 8｜Change Propagation Flow

```text
INPUT CHANGE
→ identify changed object
→ traverse explicit dependencies
→ classify affected / preserved / unknown
→ identify domains / artifacts / decisions
→ create Revision Scope
→ route only affected work
→ readback after repair
```

**Rule**
Missing explicit dependency may cause `UNKNOWN`, not false “unaffected”.

---

# 9｜Failure / Degraded Scenarios

## MA-E01｜Newest file is a PDF, native CAD older
Do not assume PDF is new authority. Show role mismatch and route change upstream unless authority explicitly changed.

## MA-E02｜Readback points to old revision
Readback cannot prove current revision. Mark unread current artifact.

## MA-E03｜Artifact exists but cannot open
No “DONE / VALIDATED” claim. Attempt truthful readback or mark inaccessible.

## MA-E04｜External tool unavailable
Use bounded substitute only if it answers current question.

## MA-E05｜Change impact incomplete
Show known affected + unknown rather than global certainty.

## MA-E06｜Artifact deleted
Preserve logical identity / history where owner-native rules allow; do not silently recreate a different object with same name.

## MA-E07｜AI visual looks finished
Role stays AI Visual / Preview unless explicitly adopted through valid owner workflow.

---

# 10｜Events

- `relation_created`
- `relation_linked`
- `relation_stability_changed`
- `change_impact_requested`
- `revision_scope_created`
- `artifact_registered`
- `artifact_role_changed`
- `artifact_revision_created`
- `native_source_opened`
- `readback_started`
- `readback_completed`
- `stale_artifact_detected`
- `degraded_substitute_used`

---

# 11｜Metrics

- Artifact Role Misclassification Rate
- Native Source Recovery Rate
- Readback Completion Rate
- Readback Revision Mismatch Rate
- Stale Artifact Prevention Rate
- Change Impact Precision
- Full-reset Avoidance Rate
- Preserved-valid-work Rate
- Percentage of important artifacts bound to Question / Relation
- Percentage of important revisions with actual readback

---

# 12｜Verification

必须至少覆盖：
- CAD / 3D / HTML / SVG 或等价多类 artifact；
- derivative newer than native；
- stale readback；
- partial tool outage；
- cross-domain dependency；
- local revision without global reset；
- one artifact with multiple representations；
- one Human-steered second-round delta。
