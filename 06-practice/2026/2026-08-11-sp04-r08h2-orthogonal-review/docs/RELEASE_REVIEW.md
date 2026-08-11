# R08H.2｜Release Review

> **AR v1.0 CURRENT STATUS：REVIEW PENDING**  
> 原 `POST-REVIEW PASS` 仅保留为 **LEGACY REVIEW RESULT**。R08H.2 必须重新执行 AR-G01—AR-G10 + AR-S01 Drawing + AR-S03 Data + AR-S07 Documentation + AR-S09 Release Package，才允许 `PACKAGE RELEASE PASS v1.0`。

## OLEANDER Artifact Review System v1.0

### A｜Common Review
AR-G01 Identity & Naming；AR-G02 Version & Status；AR-G03 Completeness；AR-G04 Internal Consistency；AR-G05 Cross-file Consistency；AR-G06 Evidence & Truth；AR-G07 Open & Integrity；AR-G08 Reproduction；AR-G09 Change Traceability；AR-G10 Final Artifact Review。

AR-G10 必须独立记录：Visual hierarchy、Boundary、**Occlusion｜遮挡**、Clearance、Geometry ↔ Dimension、**Scale / Proportion｜技术比例 + 构造比例**、View Appropriateness、Cross-view Consistency、Construction / Functional Logic、Evidence / PENDING、Export / Reproduction。

### B｜Specific Review｜本包触发
- **AR-S01 Drawing**：SVG / DXF / 技术 PNG
- **AR-S03 Data**：JSON / QA 数据
- **AR-S07 Documentation**：README / REVIEW / REVISION
- **AR-S09 Release Package**：目录 / MANIFEST / ZIP / GitHub / Drive 状态

硬 FAIL：关键遮挡、比例错误、几何—标注不一致、视图错误、多视图冲突、构造/功能逻辑错误、证据/同步声明失真、文件无法打开。硬 FAIL 不能用总分平均抵消。

## Legacy result｜旧 Gate 历史结果

旧 Post-Generation Review Gate 下曾记录：**POST-REVIEW PASS**。

- Visual hierarchy：PASS
- Text + Graphic Boundary：PASS
- Geometry ↔ Dimension：PASS
- Scale：PASS
- Construction Logic：PASS WITH PENDING
- Evidence / PENDING：PASS
- Reproduction：PASS

该结果证明旧 Gate 已执行，但**不自动等于 Artifact Review System v1.0 的 Common PASS / Specific PASS / PACKAGE RELEASE PASS**。

## Current gate rule

`REVIEW PENDING → NEEDS REVISION / FAIL → correction → rerun QA → reopen final artifact → POST-REVIEW PASS`

Package 还需全部触发 Gate + AR-S09 PASS 后才可标记 `PACKAGE RELEASE PASS v1.0`。