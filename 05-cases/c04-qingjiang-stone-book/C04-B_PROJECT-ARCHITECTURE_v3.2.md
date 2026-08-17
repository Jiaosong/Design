# C04｜清江石书｜完整项目架构 v3.2

- 项目：`PRJ-C04-QINGJIANG-SHISHU`
- 日期：`2026-08-17`
- 继承：`C04-B_PROJECT-ARCHITECTURE_v3.1`
- 角色：`CHAPTER-PAGE SEPARATION + INDEPENDENT BRAND CHAPTER`
- 变更性质：结构扩展，不删除、不压缩、不合并 v3.1 任何页面、设计对象或专业深度。

## 0｜继续生效的最高规则

> **CHAPTER ≠ PAGE。**
>
> **NO COMPRESSION / NO LOSS / RESTRUCTURE WITHOUT INFORMATION LOSS。**

固定层级：

`PROJECT → CHAPTER → PAGE → MODULE / FIGURE / ASSET`

现有 `C04-WEB-P001 ... C04-WEB-P052` 仍为受保护基线身份；未完成精确逐页映射前，默认 `PRESERVE / UNMAPPED`。新增专业页面使用 `C04-WEB-Nxxx`，但本轮 authoring sync 的章节内 `CHxx-Pxx` 仅用于保存内容身份，不等于最终 Web PAGE-ID。

## 1｜本次架构增量：品牌独立成章

用户明确已有独立品牌设计。品牌承担项目跨媒介识别系统，包括 Web、App、纸图、十三印、实体、展板、视频、文化产品等，不得压缩为 Memory/IP 章节中的一个 Logo 模块。

因此：

- 新增 `CH14｜品牌与视觉识别系统`；
- 原 `CH14｜记忆、IP与文化产品` 顺延为 `CH15`；
- 原 `CH15｜设计深化与细节` 顺延为 `CH16`；
- 原 `CH16｜技术、模型与工程证明` 顺延为 `CH17`；
- 原 `CH17｜方案演化与专业判断` 顺延为 `CH18`；
- 原 `CH18｜开放项、回程与结尾` 顺延为 `CH19`。

这不是删除、改名覆盖或页面合并；原章节内容身份全部保留，仅发生 `MOVE / RENUMBER`。

## 2｜Current Chapter Containers｜CH00–CH19

- CH00 项目定义
- CH01 项目问题与机会
- CH02 场地与山水分析
- CH03 地域文化与内容分析
- CH04 人群与使用状态分析
- CH05 游程与行为分析
- CH06 设计原理
- CH07 设计方法
- CH08 总体策略与体验系统
- CH09 路线、交通与服务设计
- CH10 十三印内容与互动系统
- CH11 数字陪伴系统
- CH12 关键场景设计
- CH13 实体、身体与感官设计
- **CH14 品牌与视觉识别系统**
- CH15 记忆、IP与文化产品
- CH16 设计深化与细节
- CH17 技术、模型与工程证明
- CH18 方案演化与专业判断
- CH19 开放项、回程与结尾

章节数现在是 **20 chapter containers**。它不等于页面总数。

## 3｜Brand Chapter Scope｜CH14

CH14 至少独立覆盖：

1. 品牌核心：为什么叫“清江石书”；
2. 品牌命题与语言系统；
3. 标志/字标系统；
4. 色彩系统；
5. 字体与版式系统；
6. 图形语言：线、印、页、路径/痕迹；
7. 图标、地图与信息图形语言；
8. 跨媒介品牌应用。

可继续新增：Brand Architecture、Naming System、Editorial System、Motion Identity、Photography Direction、Illustration/Diagram Direction、Material/Print 等页面。

Brand 的专业边界：

- `Brand = 整个项目如何被识别`；
- `Memory/IP = 游客离开以后，哪些东西继续被带走和传播`。

两者不得合并为同一章节。

## 4｜2026-08-17 Chapter Content Authoring Sync

本轮已把当前对话中实际逐页展开的章节内容写入：

`05-cases/c04-qingjiang-stone-book/chapter-content-sync/v0.1/`

已同步章节：

- CH00
- CH02
- CH03
- CH04
- CH05
- CH06
- CH07
- CH09
- CH10
- CH11
- CH12
- CH13
- CH14 Brand

本轮没有逐页重新生成 CH01 与 CH08，因此它们仍保留在架构中，但本次 sync **不补造正文**。

当前同步得到 **70 个 chapter-level authoring page units**。该数字只表示本轮逐页内容块数量，**不是当前正式 Web page_count，也不是 `52 + 70`**。原因：这些内容中有一部分是对既有52页概念的重写/展开，一部分才会成为新的 N-series 页面。最终数量必须经过：

`旧52逐页读取 → P001–P052映射 → authored units逐项比对 → KEEP/MOVE/REWRITE/EXPAND 或 NEW → 分配N-series → actual page_count`

在这个映射完成前，禁止用 70 推断新总页数。

## 5｜Page Authoring Identity Rule

本轮内容文件使用 `CHxx-Pxx` 作为 **authoring identity**，目的是避免聊天内容丢失，并保持“页面是页面”。

它们不是最终 Web PAGE-ID。

最终迁移时每个 authoring unit 必须单独判定：

- `MAP_TO_LEGACY C04-WEB-Pxxx`
- `EXPAND_FROM_LEGACY C04-WEB-Pxxx`
- `NEW C04-WEB-Nxxx`
- `PROCESS / SUPPORT`

不得因为标题类似就自动 MERGE。

## 6｜No-loss Locks Remain

本次结构扩展不改变：

- `ROUTE-03 = LOCKED CURRENT`；
- `JOURNEY-04 = PROVENANCE / NON-CURRENT`；
- R06 experience = `FINISHED / FROZEN / NO REOPEN`；
- R01–R13完整保留；
- App、Physical/Sensory、Memory/IP、Audience、C22/C23/Model、Motion 全部保留；
- P02 / step-light / Fluid Rest / Qingfengyin 保持其实际 KEEP/HOLD/competition 状态；
- `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION`。

## 7｜Next Migration Step

1. 逐页读取最后一套52 baseline surfaces；
2. 为 P001–P052 建立 exact page register；
3. 把本轮 70 authoring units 一对一与旧页比对；
4. 保留旧页身份，不默认合并；
5. 只对真正缺失页面分配 N-series；
6. 建立 CH00–CH19 的实际 PAGE sequence；
7. 浏览器/导出按 PAGE-ID 做 finished-pixel readback；
8. 独立 Design Crit 后才允许 MAIN / REVISE / REJECT / HOLD 判定。

**v3.2 的材料增量只有两项：保留本轮逐页内容正文，并把品牌正式提升为独立章节。其余设计权威与证据边界不被改写。**