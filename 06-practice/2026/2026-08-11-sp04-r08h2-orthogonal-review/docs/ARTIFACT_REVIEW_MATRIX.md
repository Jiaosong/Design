# R08H.2｜Artifact Review Matrix

## Common Gate
AR-G01—AR-G10：**REVIEW PENDING** under v1.0.

## Triggered Specific Gates

| Artifact | Specific Gate | Current v1.0 status |
|---|---|---|
| Editable SVG / Outlined SVG / DXF / technical PNG | AR-S01 Drawing | REVIEW PENDING |
| JSON / QA data | AR-S03 Data | REVIEW PENDING |
| README / REVIEW / REVISION docs | AR-S07 Documentation | REVIEW PENDING |
| Folder / MANIFEST / ZIP / GitHub / Drive status | AR-S09 Release Package | REVIEW PENDING |

## Legacy review
旧 Post-Generation Review Gate 的 `POST-REVIEW PASS` 保留为 **LEGACY REVIEW RESULT**，不自动升级为 v1.0 PASS。

## Hard FAIL fields
- Occlusion / 遮挡
- Scale / Proportion / 比例
- Geometry ↔ Dimension
- View Appropriateness
- Cross-view Consistency
- Construction / Functional Logic
- Evidence / Claim integrity
- Open / file integrity

只有 Common PASS + 所有触发 Specific PASS + AR-S09 PASS 后，本包才能标记 `PACKAGE RELEASE PASS v1.0`。