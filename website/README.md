# OLEANDER Website｜Portfolio & Research Interface

这是 OLEANDER／织作的个人设计作品与研究展示界面，用于呈现品牌、CMF、空间、文化体验、数字交互与设计方法相关成果。

网站首先是**作品集与研究界面**：让外部阅读者先感知项目，再逐步进入判断、方法、原型和证据边界。治理版本、历史映射与发布门槛继续保留，但只服务内容可信度与可追溯性，不作为页面第一阅读。

## 设计表达优先级

OLEANDER 网页现行表现规则：

**大图 > 小图 > 图表 > 表格 > 文字**

- 大图负责建立第一感知、尺度、气氛和项目判断。
- 小图负责补充局部、材料、触点和对照证据。
- 图表负责解释关系、过程、变化和因果。
- 表格只承担需要精确比较的内容，不作为主要视觉语言。
- 文字用于命名、判断、说明边界与证据状态，不与图像等权争夺第一阅读。
- 动态交互可以使用，但必须改变阅读理解，例如状态切换、滚动叙事、前后关系变化和证据展开；不为了展示交互能力增加控件。

当前案例阅读顺序优先采用真实视觉资产：**C02 Daylily → C03 The Light Collection → C01 一脉广渡（Research / Method）**。C01 当前缺少与 C02/C03 对等的真实项目图像资产，因此不伪造主视觉，不让图解冒充真实作品图。

## 设计基准

- 核心：设计不是创造对象，而是重新组织关系。
- 文化与审美方向：中式极简；这是当前持续研究和发展的设计方向。
- 调性：以关系为骨，以气韵为势，以构造为证，以时间为尺度，以余地为伦理。
- 生成方法：关系、共边、位移、嵌合、层累、游观与修订。

中式极简在这里不是水墨、书法、红印、茶、香、竹、仿古肌理或宋式配色的符号拼贴。它也不以西方极简的独立对象、几何纯化与均质网格为终点；在静、间、自然材料和无常之外，还强调历史层累、礼序与游观、共同体关系、文化来源与修订责任。

## Selected Works

- **C01｜一脉广渡**：`RESEARCH + PROPOSAL / EVIDENCE REVIEW`。当前以研究与设计提案为主；参与者结果仍为 `TEST PLANNED / NOT RUN`，不把风险假设写成已发生结果。
- **C02｜忘也 Daylily**：`INDEPENDENT PORTFOLIO / PROTOTYPED / TEST PLANNED / NOT RUN`。作为独立作品集项目展示，不主张医疗、心理或治疗效果。
- **C03｜The Light Collection**：Reno CMF 独立概念提案，`VISUALIZED / SAMPLE TEST PENDING`。不暗示 OPPO 委托、采用、量产或背书。

## 直接运行

打开 `index.html`。页面不请求外部字体或第三方 JavaScript；CSS 通过 `@font-face local()` 优先使用本机可用的思源 / Noto 中文字体，并保留系统字体回退。

## 视觉语言

- Field / Evidence / Material / Intervention / Residue 五层阅读结构
- PAPER、STONE、CHARCOAL、METAL、LINEN、MOSS、EARTH 的克制色彩系统
- 以无衬线字形、层级、间隔、共边和路径建立秩序
- 数字材料性来自响应、时间和行为，不依赖仿纸纹理
- 动效只服务 Scroll、Reveal、Return 以及明确的关系状态变化
- 工程网格只在阅读结构时出现，不作为全站装饰背景

## 交互与研究原型

- 首页关系织场：Context / Break / Reconnect 三态阅读
- Relationship Reading：Original / Current / Intended 状态切换
- 证据层抽屉：显示来源、限制与可信度
- Selected Evidence：逐项展开证据层
- Translation Logic：点击应用卡查看生成规则
- Experience Formation：切换用户角色与触点职责
- Project Index：关系 / 实践 / 档案模式
- Practice：六阶段方法切换并关联项目证据
- Contact：五步关系说明、验证、本地草稿及模拟提交

连续参数控制若只改变视觉效果而不改变内容理解，应从公共界面移除或降级。

## 外部开源工具

- [img2threejs/img2threejs](https://github.com/img2threejs/img2threejs)：单张参考图到程序化、可动画 Three.js 模型的质量门控工作流。
- 在 OLEANDER 中用于产品与器物体块验证、手机壳概念原型、展陈构件和网页三维展示。
- 它是独立开源项目，采用 Apache-2.0 许可证；不得表述为本项目的原创工具。
- 单图生成无法证明隐藏面和工程尺寸，输出必须经过 Rhino / Blender / 人工结构与版权复核。

## 无障碍

- 主要交互均支持键盘 Enter / Space
- Tabs 支持方向键、Home / End，并具有完整 `tab` / `tabpanel` 关系
- 移动菜单支持 Escape 关闭与焦点恢复
- 表单错误与字段关联，并把焦点移动到首个错误字段
- 状态不只通过颜色表达
- 支持 `prefers-reduced-motion`
- 保留原生焦点、表单标签和状态说明

## 证据与发布边界

当前内容治理基线为 **Governance v1.0.1 / ACTIVE / E2**。C01 / C02 / C03 是当前案例编号；旧 CASE/GD/DY/LC、Project 01–03、R4C-G2、v0.7 / v0.7-R1、Wordmark v0.8.1 仅作为 Legacy / Deprecated 历史映射。

- E1 / E2 自动化应在当前 head 保持通过。
- E3 人工验证仍需完成：屏幕阅读器、真实 200% zoom / reflow、实体设备触控、**浏览器中的真实视觉阅读节律**和目标平台字体 QA。
- 当前分支的设计表达审查已完成结构级检查，但在合并前仍应进行一次真实浏览器视觉 QA；不得把静态样式/结构检查表述为已完成的视觉验证。
- 28 项网站素材的来源、创作者、人物 / 场地产权、使用渠道与期限、修改 / AI 状态、撤回与发布记录仍需逐项闭环。
- Contact 仍为模拟提交；真实后端、已验证专业邮箱与隐私 / 数据路径未发布。
- 当前身份对象按各自证据等级保持开放状态；恢复或废弃的历史源文件不自动升级为当前权威。

## 上线前需要替换或闭环

- 未完成权利 / 来源核验的人物照片与项目图像
- 专业邮箱、LinkedIn 与 CV
- Contact 表单后端与隐私政策
- 项目真实证据来源和最终文案
