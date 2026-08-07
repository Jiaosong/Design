# Timer Light Basin v3.0 Web

OLEANDER／织作 Practice 网页母版。

## 生产规则

- 完整页面由 HTML + CSS + SVG + structured data 构建。
- 图像生成不得生成完整网页、完整设计板或完整 PDF 页面。
- 独立效果图可以作为表现资源或对比参考，但不得替代结构、CAD、尺寸、BOM 或验证证据。
- 爆炸结构只来自同一套真实模型；不允许 AI 猜零件或改装配关系。
- 数据继续区分 `VERIFIED SOURCE / DESIGN INPUT / NOT RUN`。

## 第三方依赖

- `@google/model-viewer@4.1.0`
- `three@0.174.0 / r174`

版本、用途、许可证、升级门槛与 fallback 见 `DEPENDENCIES.json`。

## 四层架构

本 Practice 当前映射：

- `B02 Model & Offering` — PRIMARY
- `B04 Metrics & Governance` — SUPPORTING
- `IP02 Narrative & Content` — SUPPORTING
- `IP03 Visual & Verbal System` — SUPPORTING
- `IP04 Application & Licensing` — SUPPORTING
- `Culture` — N/A，当前无文化来源、权利或延续议题
- `Spatial` — N/A，当前为桌面产品，不涉及场地或空间系统

详见 `ARCHITECTURE_MAPPING.md`。

## 当前工程状态

`WEB MASTER GENERATED / REAL GLB PBR PROFILE / SOURCE EDITABLE / ENGINEERING VALIDATION PENDING`

网页正式源包与 GLB 二进制资产已归档到 OLEANDER Practice 文件库；本 GitHub 分支先登记依赖、架构与发布边界。二进制模型写入需要走仓库可用的二进制上传/本地 git 工作流后再补齐，不能用文本 Contents API 冒充完成。
