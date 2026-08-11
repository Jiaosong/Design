# SP04-R08H.2｜A04 正交视图重构

> **AR v1.0 CURRENT STATUS：REVIEW PENDING**  
> 原 `POST-REVIEW PASS` 保留为旧 Post-Generation Review Gate 的 **LEGACY REVIEW RESULT**。引入 `OLEANDER Artifact Review System v1.0` 后，必须重新执行 AR-G01—AR-G10 + AR-S01 Drawing + AR-S03 Data + AR-S07 Documentation + AR-S09 Release Package，才可升级为 `PACKAGE RELEASE PASS v1.0`。

## 目的
修正 R08H.1 中把“沿窗框周边锚固间距”“结构边距”“锚固深度”和“控制层冲突”混在同一视图的问题。

## 三个视图
- A1｜1:10 角部立面：150 首锚距、450/600 周边间距。
- A2｜1:2 锚固剖面：75 框、12 安装缝、45 锚固深度、30 保温回包、20 局部隔热垫、防水/气密桥接、结构基层。
- A3｜1:5 结构边缘定位：60 结构边距。

## 证据边界
以上数值均为**练习用假设参数**，不是规范、厂家或实际项目要求。
20 mm 局部隔热垫仅用于讨论热桥削弱路径；金属紧固件仍形成热桥，不能将本节点描述为“完全断桥”。

## OLEANDER Artifact Review System v1.0

本包审查改为两层：

- **A｜Common Review：AR-G01—AR-G10**
- **B｜Specific Review：AR-S01 / AR-S03 / AR-S07 / AR-S09**

AR-G10 必须独立审查：Visual hierarchy、Boundary、**Occlusion｜遮挡**、Clearance、Geometry ↔ Dimension、**Scale / Proportion｜技术比例 + 构造比例**、View Appropriateness、Cross-view Consistency、Construction / Functional Logic、Evidence / PENDING、Export / Reproduction。

硬 FAIL 不能通过总分平均抵消：关键遮挡、比例错误、几何—标注不一致、视图错误、多视图冲突、构造逻辑错误、虚假证据/同步声明、文件无法打开。

## Legacy Post-Generation Review Result

旧 Gate 下曾记录：`POST-REVIEW PASS`。

- Visual hierarchy：PASS
- Text + Graphic Boundary：PASS
- Geometry ↔ Dimension：PASS
- Scale：PASS
- Construction Logic：PASS WITH PENDING
- Evidence / PENDING：PASS
- Reproduction：PASS

**该结果不自动等于 AR v1.0 PASS。**