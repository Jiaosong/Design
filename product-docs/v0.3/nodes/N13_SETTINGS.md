# N13｜SETTINGS

[← Node Graph](README.md)

| Field | Value |
|---|---|
| Node ID | N13 |
| Children | N13A, N13B, N13C — see [Atomic Children](#atomic-children) |
| Type | Supporting Product Surface |
| Product job | 提供少量真正需要用户控制的产品级偏好，而不把工作流复杂性转嫁给用户 |
| Inputs | explicit user preferences |
| Outputs | bounded interaction/configuration choices |
| Authority | Settings cannot override project/professional authority |
| Primary metric | setting usefulness / misconfiguration |
| Release priority | P2 |
| Doc state | OPEN |

## Candidate Settings

```mermaid
mindmap
  root((SETTINGS))
    Support_Mode
      AUTO
      COMPACT
      EXPLAIN
      OFF
    Notifications
    Data_Privacy
    Connector_Permissions
    Accessibility
    Cost_or_Model_Preferences
```

## Not a Setting

Do not expose as casual toggles:
- Design KEEP;
- Promotion;
- professional compliance;
- bypass Action Guard;
- “AI can do anything”;
- Project Current authority.

## Principle

> **If the product can infer safely from current context, do not make the user configure it permanently.**

Settings should remain small until real user evidence proves a persistent preference deserves a control.

## Atomic Children

```mermaid
flowchart TB
    P[N13 SETTINGS]
    P --> N13A[N13A DATA / PRIVACY SETTINGS]
    P --> N13B[N13B CONNECTOR PERMISSIONS]
    P --> N13C[N13C ACCESSIBILITY SETTINGS]
```

- [N13A｜DATA / PRIVACY SETTINGS](atomic/N13A_DATA_PRIVACY_SETTINGS.md)
- [N13B｜CONNECTOR PERMISSIONS](atomic/N13B_CONNECTOR_PERMISSIONS.md)
- [N13C｜ACCESSIBILITY SETTINGS](atomic/N13C_ACCESSIBILITY_SETTINGS.md)
