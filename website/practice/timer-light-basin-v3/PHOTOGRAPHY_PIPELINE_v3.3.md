# OLEANDER／织作｜Timer Light Basin｜Photography Pipeline v3.3

**Status:** `DESIGN DEVELOPMENT / PHOTOGRAPHY PIPELINE PROTOTYPE / BROWSER VISUAL REGRESSION BLOCKED`

## Goal

把产品网页中的 Hero / CMF 表现从通用 3D inspection viewer 分离为可控的工业设计摄影管线，同时保留 state / exploded viewer 作为结构检查层。

## Combined pipeline

`Explicit normals → physical material classes → reflection-card studio environment → opal diffuser baseline → model-derived contact shadow → linear HDR composer → restrained bloom → AGX tone mapping → sRGB`

## Modules

### `render/StudioEnvironment.js`

- 采用 `building-dynamic-envmaps` 的 Lightformer 思路，但转译为原生 Three.js。
- 用 emissive reflection cards 先生成 PMREM 环境反射；再独立加入 RectArea key / fill / rim。
- 使用中性暖灰摄影棚，取消示例中的红色环形 key light。
- 使用无缝 cyclorama，而不是黑色矩形地面。

### `render/DiffuserMaterial.js`

- Housing / diffuser / aluminum / knob / silicone / PCB 按物理材质类别拆分。
- Diffuser 当前采用 MeshPhysicalMaterial transmission / thickness / IOR / attenuation baseline。
- 所有 diffuser 参数均为 `VISUALIZATION ONLY / NOT MEASURED OPTICAL DATA`。
- 如果实机浏览器结果仍显得“塑料片”，下一门槛是 reviewed front/back FBO MeshTransmissionMaterial，而不是继续增加 bloom。

### `render/ContactShadow.js`

- 从真实产品模型轮廓渲染到 HalfFloat target。
- 使用 height-aware alpha + horizontal / vertical separable blur。
- Hero 1536，Material 1024。
- 不使用固定 radial blob 或矩形 shadow plane 作为最终摄影阴影。

### `render/ColorPipeline.js`

`LINEAR HDR → POST → TONE MAP → sRGB`

- renderer 使用 `NoToneMapping`。
- Tone mapping 只在后期末端执行一次，避免 double tone mapping。

### `render/PostProcessing.js`

- `postprocessing@6.39.4`
- HalfFloat EffectComposer
- restrained Bloom：Hero 0.12 / Material 0.08
- 高 luminance threshold，只服务发光面
- final `AGX` ToneMappingEffect
- 不用强 SSR / vignette / noise 掩盖模型或材质缺陷。

### `render/PhotographyViewer.js`

- 固定小产品摄影机基线；Hero FOV 27°。
- CMF 提供 body / top / control / rear presets。
- orbit 被限制，最终构图不等同于任意 3D viewer 角度。
- model-viewer 继续承担 100/50/10 state 与 staged exploded inspection。

## Evidence boundary

摄影表现完成度不能升级为：

- optical PASS
- material sample approved
- measured colorimetry
- DFM / DFA validated
- thermal / electrical validated
- user test passed

## Source references

See `TECHNICAL_REFERENCES.md`.
