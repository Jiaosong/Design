# OLEANDER PRD Feature Specifications v0.2.0

[← Master PRD](../OLEANDER_DESIGN_COLLABORATION_PRD_v0.2.0.md)

本目录把 Master PRD 细化到**Product Area / Feature / Interaction / Acceptance Scenario / Failure Behaviour / Event** 层。

它不是软件详细设计，不规定数据库、API、Agent topology 或具体前端技术。

## Specification Set

| Spec | Scope |
|---|---|
| [HOME + FOCUS](PRD_HOME_FOCUS_v0.2.0.md) | Resume、Current Question、Problem / Value / Constraint / Reframe |
| [STUDIO + COMPARE](PRD_STUDIO_COMPARE_v0.2.0.md) | Explore / Develop / Synthesize、方案比较、Human decision |
| [MAP + ARTIFACTS](PRD_MAP_ARTIFACTS_v0.2.0.md) | Design Relation、Dependency、Change Impact、Native Artifact、Revision、Readback |
| [REVIEW + KNOWLEDGE + HISTORY](PRD_REVIEW_KNOWLEDGE_HISTORY_v0.2.0.md) | Critique、Verification、Validation、Evidence、Continuity、Handoff |
| [SESSION KERNEL + CONTINUITY](PRD_SESSION_KERNEL_CONTINUITY_v0.2.0.md) | Intent、Mutation、Human Steer、Human Stop、Guard、Multi-human、Plugin-off |

## 每个 Feature 的最小定义

每个 P0/P1 Feature 至少需要：

```text
FEATURE ID
PURPOSE
USER / CONTEXT
UPSTREAM NEED
TRIGGER
INPUT
SYSTEM BEHAVIOUR
VISIBLE RESULT
HUMAN / SYSTEM ALLOCATION
ACCEPTANCE SCENARIO
FAILURE / DEGRADED BEHAVIOUR
EVENTS
PRIORITY
```

## 阅读规则

Feature Spec 的“通过”只代表对应产品要求在该验证层成立。

```text
FEATURE ACCEPTANCE
≠
SYSTEM CURRENT
≠
DESIGN KEEP
≠
PROFESSIONAL PASS
≠
PROMOTION
```
