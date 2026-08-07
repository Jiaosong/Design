# OLEANDER／织作｜Timer Light Basin v3.3｜Photography Calibration Report

**Calibration status:** `FOUR-GATE PASS / HERO-CMF RENDER LOCK ACTIVE`  
**Engineering status:** `VALIDATION PENDING`  
**Calibration date:** 2026-08-07  
**Executable environment:** Chromium / WebGL 2.0 / ANGLE / Vulkan / SwiftShader.

## 01｜硬门槛

| Gate | Result | 视觉判断 |
|---|---|---|
| Housing highlight | **PASS** | 暖灰 PC+ABS 候选表面形成连续宽高光；曲率、上缘与暗部边界可读；没有硬白带，也没有金属化。 |
| Diffuser volume | **PASS** | 成形扩散面可读出浅凹体积、边缘厚度和中心—边缘过渡；乳白体量优先于暖色发光层，不再是平黄色圆盘。 |
| Metal knob reflection | **PASS** | 旋钮出现受控银灰明暗反射带，可读为 satin/anodized metal；没有棕黑塑料感，也没有镜面铬感。 |
| Contact shadow falloff | **PASS** | 双层接地阴影形成 tight contact + broad ambient penumbra；脚圈下密实、向外柔化，无矩形地台、环状伪影与漂浮缝。 |

**规则：四项全部 PASS 后才允许进入 Hero / CMF render lock。本轮满足该条件。**

## 02｜通过证据

Remote WebGL calibration run:
- GitHub Actions run ID: `31166364420`
- Artifact ID: `8989166344`
- Renderer: `ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)), SwiftShader driver)`
- API: `WebGL 2.0 (OpenGL ES 3.0 Chromium)`

Evidence frames:
- `calibration/round6/housing.png`
- `calibration/round6/diffuser.png`
- `calibration/round6/knob.png`
- `calibration/round6/shadow.png`
- `calibration/round6/manifest.json`

这些图是可执行 WebGL 的真实截图，不是图像生成结果，也不是完整页面生成图。

## 03｜Calibration Rig 边界

校准 rig 来自当前真实 GLB 的产品尺寸、外形包络和 diffuser 径向剖面，用于隔离四项摄影表现变量。它不是替代 CAD 的新模型，也不是新的工程权威。

正式网页仍读取当前真实 GLB；`PhotographyViewer.js` 使用同一组已锁定的 Studio / Material / Shadow / Color / Post 模块。

## 04｜Render Lock

从本报告起，以下内容进入 **LOCKED**：
- `render/StudioEnvironment.js`
- `render/DiffuserMaterial.js`
- `render/ContactShadow.js`
- `render/ColorPipeline.js`
- `render/PostProcessing.js`
- `render/PhotographyViewer.js`

除非出现以下情况，否则不得为了“更好看”继续任意调参：
1. 真实 GLB 出现明确视觉回归；
2. 产品几何发生批准后的结构变更；
3. 获得真实材料样片／光学数据，需要用证据替换 visualization hypothesis；
4. 浏览器/GPU/Three.js/postprocessing 版本变更导致可复现差异。

任何解锁都必须记录：`why → variable changed → same-condition comparison → result → keep/reject`。

## 05｜证据边界

本次 PASS 只证明 **摄影渲染行为** 达到当前 OLEANDER 门槛，不证明：
- PMMA 光学均匀性；
- PC+ABS 实物纹理、光泽或耐污；
- 金属真实阳极氧化表面；
- 色度／亮度／眩光；
- 热表现；
- DFM / DFA / 公差链；
- 电气集成；
- 实体触觉或用户识别。

以上仍为 `NOT RUN / TO VALIDATE`。
