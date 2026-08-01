# OLEANDER Website — Brand System v0.7

本网站是刘旋的品牌、CMF、空间与文化体验设计作品集。当前生产基线为 **OLEANDER v0.7 / Visual Bible v1.0**。

## 品牌基准

- 核心：设计不是创造对象，而是重新组织关系。
- 文化与审美方向：中式极简；这是既定方向，不再重新选风格。
- 调性：以关系为骨，以气韵为势，以构造为证，以时间为尺度，以余地为伦理。
- 生成方法：关系、共边、位移、嵌合、层累、游观与修订。
- 识别成果：v0.7 字标、字体、色彩、版式、材料、影像及应用系统。

中式极简在这里不是水墨、书法、红印、茶、香、竹、仿古肌理或宋式配色的符号拼贴。它也不以西方极简的独立对象、几何纯化与均质网格为终点；在静、间、自然材料和无常之外，还强调历史层累、礼序与游观、共同体关系、文化来源与修订责任。

## 直接运行

打开 `index.html`。页面不请求外部字体或第三方 JavaScript；CSS 通过 `@font-face local()` 优先使用本机可用的思源 / Noto 中文字体，并保留系统字体回退。

## 视觉语言

- Field / Evidence / Material / Intervention / Residue 五层阅读结构
- PAPER、STONE、CHARCOAL、METAL、LINEN、MOSS、EARTH 的克制色彩系统
- 以无衬线字形、层级、间隔、共边和路径建立秩序
- 数字材料性来自响应、时间和行为，不依赖仿纸纹理
- 动效只服务 Scroll、Reveal、Return 三类关系变化

## 新增交互

- 首页关系织场：连接 / 松开、关系密度调节
- Relationship Reading：Original / Current / Intended 状态切换
- 关系张力调节：同步改变线型与节点距离
- 证据层抽屉：显示来源、限制与可信度
- Selected Evidence：逐项展开证据层
- Translation Logic：点击应用卡查看生成规则
- Experience Formation：切换用户角色与触点职责
- Project Index：关系 / 实践 / 档案模式
- Practice：六阶段方法切换并关联项目证据
- Contact：五步关系说明、验证、本地草稿及模拟提交

## 无障碍

- 主要交互均支持键盘 Enter / Space
- Tabs 支持方向键、Home / End，并具有完整 `tab` / `tabpanel` 关系
- 移动菜单支持 Escape 关闭与焦点恢复
- 表单错误与字段关联，并把焦点移动到首个错误字段
- Range 控件提供实时数值反馈
- 状态不只通过颜色表达
- 支持 `prefers-reduced-motion`
- 保留原生焦点、表单标签和状态说明

## 上线前需要替换

- 真实人物照片与项目图像
- 专业邮箱、LinkedIn 与 CV
- Contact 表单后端与隐私政策
- 项目真实证据来源和最终文案
