# OLEANDER／织作｜v3.3 Photography Pipeline｜GitHub 技术参考

**状态：** TECHNIQUE REFERENCE / IMPLEMENTATION ADAPTED / THIRD-PARTY VISUAL ASSETS NOT INCLUDED

| Source | Commit / Version | 采用 | 不采用 / 边界 |
|---|---|---|---|
| mrdoob/three.js `webgl_materials_car.html` | `19567418fa4c798413d22c19b215171f3eaadb4c` | MeshPhysicalMaterial 分类、环境反射、产品阴影、tone-mapping 比较方法 | Ferrari 模型、AO 贴图与示例页面不进入 OLEANDER 资产 |
| pmndrs/examples `building-dynamic-envmaps` | `fb08c786c32655c40bc37152cc3e06500b153f5a` | Lightformer 式反射卡、controlled studio environment、ContactShadows 思路 | 不复制 Lamborghini、红色 ring key、示例 SSR/Bloom/LUT 参数 |
| pmndrs/examples `frosted-glass` | 同上 | transmission / thickness / roughness / environment 的半透明关系 | Nike 模型与交互不采用 |
| pmndrs/examples `envmap-ground-projection` | 同上 | 环境—地面连续性、接地阴影与 tone-mapping 比较 | Fisheye 不作为 Timer 正式产品相机 |
| pmndrs/examples `bouncy-watch` | 同上 | 小型产品低 FOV、受限相机、Environment + ContactShadows | 手表模型、annotation UI 不采用 |
| pmndrs/drei-vanilla `MeshTransmissionMaterial` story | `28978f680f9071e4f4794611781c19f46de48e35` | front/back FBO、thickness、attenuation、anisotropic blur 作为 diffuser 下一门槛 | v3.3 runtime 暂不直接引入；当前先用 Three MeshPhysicalMaterial baseline |
| pmndrs/postprocessing | `6.39.4` | HalfFloatType HDR composer、线性工作流、末端 ToneMappingEffect、克制 Bloom | 不用噪声、重 vignette、强 bloom 掩盖模型问题 |

## v3.3 转译

- `StudioEnvironment.js`：反射卡 → PMREM，并与真实 RectArea key/fill/rim 分离。
- `DiffuserMaterial.js`：opal diffuser visualization baseline；参数是视觉假设，不是材料检测。
- `ContactShadow.js`：真实模型轮廓 capture + separable blur，不再用矩形 shadow plane 或固定径向 blob。
- `ColorPipeline.js`：Linear HDR 保持至后期，renderer `NoToneMapping`，最终 sRGB。
- `PostProcessing.js`：HalfFloat composer + restrained bloom + AGX tone map。

## 权利边界

源码用于技术研究与实现判断。第三方模型、截图、HDRI、LUT、品牌资产不会因为代码许可证而自动获得 OLEANDER 的公开或商业再发布权。
