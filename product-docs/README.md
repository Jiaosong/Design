# OLEANDER Product Docs

[← 返回 OLEANDER 首页](../README.md)

这里是 OLEANDER 的**产品经理文档层**。

它把产品定义从“系统架构说明”独立出来，按真实产品需求链组织：

```text
USER / CONTEXT
→ JOB
→ USER NEED
→ EXPERIENCE REQUIREMENT
→ PRODUCT REQUIREMENT
→ FEATURE / FLOW
→ INFORMATION / INTERFACE
→ ACCEPTANCE
→ VERIFICATION / VALIDATION
```

> **Product Docs ≠ OLEANDER Authority**

本目录是产品定义、沟通、评审和作品集阅读层，不创建新的 Project State、Current、Knowledge Authority、Artifact Registry、Checkpoint、Professional Process 或 Promotion 权限。

---

# Current Product Baseline

## [OLEANDER 设计协作系统 PRD v0.2.0](OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

这是当前公开产品定义主文档。

它恢复了之前 OLEANDER Product Discovery / Experience Requirements / Functional Architecture / Information Architecture / Human-System Allocation / Interface Architecture / System Requirements 的颗粒度，并把 Human–AI Co-Design Session Kernel 作为跨产品 interaction layer 合并回来。

主要覆盖：

- 用户 / 利益相关者
- Context / JTBD
- User Need baseline
- Experience Principles
- Product Structure
- HOME / FOCUS / STUDIO / COMPARE / MAP / ARTIFACTS / REVIEW / KNOWLEDGE / HISTORY
- Human–AI Session Kernel
- Human Steering / Human Stop
- Product Object Model
- Information Architecture
- Human / System Allocation
- Interfaces
- 14 条 Core User Flows
- Edge / Degraded Cases
- Metrics + Event Instrumentation
- NFR
- MVP Scope + Acceptance Gates
- Validation Plan
- Candidate Implementation Mapping
- Prioritization / Open Questions

## [Feature Specifications](features/README.md)

细化到 Product Area / Feature / Acceptance Scenario / Failure Behaviour / Event：

- [HOME + FOCUS](features/PRD_HOME_FOCUS_v0.2.0.md)
- [STUDIO + COMPARE](features/PRD_STUDIO_COMPARE_v0.2.0.md)
- [MAP + ARTIFACTS](features/PRD_MAP_ARTIFACTS_v0.2.0.md)
- [REVIEW + KNOWLEDGE + HISTORY](features/PRD_REVIEW_KNOWLEDGE_HISTORY_v0.2.0.md)
- [SESSION KERNEL + CONTINUITY](features/PRD_SESSION_KERNEL_CONTINUITY_v0.2.0.md)

## [PRD Traceability Matrix v0.2.0](OLEANDER_PRD_TRACEABILITY_MATRIX_v0.2.0.md)

将 Feature 反向追踪到：
- Product User Need
- Design Activity
- System Requirement Family
- Verification Class
- Priority

---

# Provenance

## [PRD v0.1](OLEANDER_DESIGN_COLLABORATION_PRD_v0.1.md)

保留为第一版 public PM framing 的 provenance。

v0.1 的价值在于快速建立：
- Product Vision
- Session Kernel
- MVP
- FR-01–20
- Metrics
- Rollout

但它的颗粒度不足以替代 v0.2.0 的 Feature / Flow / Acceptance / Trace 层。

---

# Historical Upstream Product Baselines

v0.2.0 不是从当前插件实现反推需求，而是重新吸收之前已形成的需求链：

- `OLEANDER_PRODUCT_DISCOVERY_USER_NEEDS_STORIES_UX_v0.1.0`
- `OLEANDER_DESIGN_PROCESS_USER_NEEDS_UX_v0.3.0`
- `OLEANDER_EXPERIENCE_REQUIREMENT_BASELINE_v0.4.0`
- `OLEANDER_PRODUCT_FUNCTION_INFORMATION_MAPS_v0.2.0`
- `OLEANDER_FUNCTIONAL_ARCHITECTURE_v1.3.0`
- `OLEANDER_INFORMATION_ARCHITECTURE_v1.4.0`
- `OLEANDER_HUMAN_SYSTEM_ALLOCATION_v1.5.0`
- `OLEANDER_INTERFACE_ARCHITECTURE_v1.6.0`
- `OLEANDER_SYSTEM_REQUIREMENTS_BASELINE_v1.7.0`

这些上游文档本身具有各自 authority boundary；PRD 不把它们压缩成第二套 Current Architecture。

---

# 推荐阅读

**产品经理 / 面试官**  
PRD v0.2.0 → Feature Specs → Cases → Evals

**AI / Agent 产品**  
Session Kernel Spec → Studio / Compare → Artifact / Readback → Trace Matrix → Evals

**设计 / 专业软件方向**  
Product Structure → Studio → Map → Artifacts → Review → Cases

**系统架构方向**  
PRD → Governance → Candidate implementation；不要把 PRD 当 Current Architecture。

---

# Candidate Implementation

当前 Human–AI Co-Design Candidate：

[查看 vNext Candidate](https://github.com/Jiaosong/Design/tree/candidate/oleander-human-ai-codesign-vnext-20260924/00-governance/runtime/candidates/human-ai-codesign-vnext)

它仍是 `CANDIDATE / NO PROMOTION`。

产品 PRD 描述产品需求；Candidate 证明部分实现。两者不能互相自证。
