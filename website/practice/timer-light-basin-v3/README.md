# Timer Light Basin v3.3 Photography Web

OLEANDER／织作 Practice 网页母版。当前主目标不是增加页面装饰，而是把真实 GLB 的产品表现提升到可审查的工业设计摄影管线。

## 生产规则

- 完整页面由 HTML + CSS + SVG + structured data 构建。
- 图像生成不得生成完整网页、完整设计板或完整 PDF 页面。
- 独立效果图可以作为表现资源或对比参考，但不得替代结构、CAD、尺寸、BOM 或验证证据。
- 爆炸结构只来自同一套真实模型；不允许 AI 猜零件或改装配关系。
- 数据继续区分 `VERIFIED SOURCE / DESIGN INPUT / NOT RUN`。

## v3.3 viewer 分工

### Photography layer

Hero / CMF：

- `three@0.174.0`
- `postprocessing@6.39.4`
- modular pipeline：
  - `render/StudioEnvironment.js`
  - `render/DiffuserMaterial.js`
  - `render/ContactShadow.js`
  - `render/ColorPipeline.js`
  - `render/PostProcessing.js`
  - `render/PhotographyViewer.js`

组合原则：controlled reflection cards + physical material classes + opal transmission baseline + model-derived contact shadow + linear HDR + restrained bloom + final AGX tone mapping。

### Inspection layer

State / Exploded：`@google/model-viewer@4.1.0`

inspection viewer 用于检查状态、节点和结构，不承担正式 Hero photography render。

## GitHub 技术参考

见 `TECHNICAL_REFERENCES.md` 和 `PHOTOGRAPHY_PIPELINE_v3.3.md`。当前技术来源包括 Three.js 官方 car-material example、pmndrs dynamic envmaps / frosted glass / ground projection / bouncy watch、drei-vanilla transmission story 与 pmndrs/postprocessing。

只转译技术原理；第三方模型、品牌资产、截图、HDRI 和 LUT 不进入 OLEANDER 正式资产。

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

## 当前 QA

`SOURCE_QA_PASS / BROWSER_VISUAL_QA_BLOCKED / ENGINEERING_VALIDATION_PENDING`

当前执行容器无法初始化 Chromium EGL/WebGL，因此源码与资产检查通过不等于视觉通过。正式工业设计摄影级结果必须在可用 WebGL/GPU 浏览器环境中继续做 highlight、diffuser、metal、shadow 和 exposure 回归。

网页正式源包与 GLB 二进制资产归档到 OLEANDER Practice File Library；GitHub 当前分支保存可审计的文本源、依赖、参考和管线实现。二进制模型仍以 File Library 为权威交付，不能用文本 Contents API 冒充已同步。
