# CH09｜路线、交通与服务设计

- 章节角色：正式提出 `ROUTE + MOBILITY + SERVICE + RETURN` 设计。
- 当前路线权威：`ROUTE-03 = LOCKED CURRENT`；`JOURNEY-04 = PROVENANCE / NON-CURRENT`。
- 十三印不得重新取得路线主权。

## CH09-P01｜ROUTE-03｜一条允许选择的清江游程

# 路线不是把游客送到十三个点，而是让他始终知道自己还能怎么走。

路线图从POI Map改成Decision Map，回答：
- WHERE AM I｜我在哪里
- WHAT CAN I DO NEXT｜接下来有哪些选择
- WHAT WILL IT COST｜继续需要多少时间/体力/注意力
- HOW DO I RETURN｜怎样回来

### 四类关系
1. **ARRIVAL｜进入**：建立江、两岸、游船/索道/步行、服务、回程关系；重点ORIENTATION，不是十三印。
2. **PRIMARY MOVEMENT｜主移动**：游船、索道、步行是三种理解清江的移动方式，不是三关。
3. **BRANCH｜分支**：继续/转向/进入场景/跳过内容/回主路径/提前返回。
4. **RETURN｜回程**：从总图一开始可见，与探索路径并行。

视觉层级：真实路线/移动 > Return/Service > 场景/十三印 > 数字发现。

功能节点类别：ORIENT / MOVE / STAY / RETURN+SERVICE；十三印可在附近发生，但不定义路线节点。

结论：**路线设计目标不是让游客完成更多，而是让每一次继续、转向、停留和返回都更加确定。**

---

## CH09-P02｜游船｜从水上建立第一尺度

# 游船不是前往景点的交通工具，它是第一次从河谷内部认识清江。

设计任务：
- 建立整体尺度。
- 建立连续山水关系，不切碎成A/B/C点。
- 建立两岸认知，为后续索道、步行、R06提供空间记忆。

信息层级：
1. 景观：100%存在。
2. 方向：必要时出现。
3. 轻内容：名称/形态线索/短听觉。
4. 深读：留到步行/停留/旅后。

App状态：LIGHT / LOW-ATTENTION，核心是 `PHONE DOWN`。
主要行为：LOOK / COMPARE / LISTEN / FRAME，不是 READ / TASK / COLLECT。

结论：**水上设计的价值不是增加信息，而是建立以后可以反复调用的第一张清江空间记忆。**

---

## CH09-P03｜索道｜移动视点本身就是内容

# 当视点开始移动，不需要再制造第二套注意力任务。

索道价值：`VIEWPOINT TRANSFORMATION`，把游客从河谷内部抬升到同时理解江、两岸、峰林、站点关系的视点。

阶段：
- **BEFORE｜进入前**：ORIENT，告诉接下来发生什么空间转换。
- **DURING｜移动中**：LANDSCAPE FIRST；不强制App/点击/AR/长阅读/持续Relation Mark；R01只是可识别短提示。
- **AFTER｜抵达后**：允许轻关系Reveal，帮助重新理解刚刚跨过的两岸关系。

序列：`ORIENT → OBSERVE → RECOGNIZE`。
数字强度：Before LIGHT；During OFF/Optional Light；After Optional Reveal。

结论：**索道体验价值来自移动视点本身；不能增加空间理解的数字介入都应让位。**

---

## CH09-P04｜步行｜真正的探索从这里开始

# 山中步行不是把十三个点串起来，而是让游客拥有自己的探索顺序。

步行核心：`CHOICE + BODY + DISCOVERY`。

路径结构：
- **MAIN｜主路径**：确定；适合第一次、时间有限、需要稳定Return。
- **EXPLORE｜探索支路**：发现；进入R节点/景观/可选内容，但必须能回主网络。
- **RETURN / RECOVERY PATH**：回来；优先恢复服务、方向、出口。

现实路径不得由GAME PROGRESS锁定，不存在“完成R05才能去R06”“还差3个印”。

探索机制：未完全解释的线索→自己决定靠近→发现关系→决定继续读或走。
Game Map：真实路线骨架 + 可选发现层；避免全节点始终高亮，采用 PARTIAL REVEAL。

随步行：`STAMINA ↓ / RETURN PRIORITY ↑`，允许 Short Loop / Continue / Recover / Return。

结论：**真正的探索不是不知道怎么回来，而是在知道怎么回来的前提下，仍愿意偏离主路径去看看。**

---

## CH09-P05｜Return不是终点，而是整套路线的安全底层

# 好的探索需要自由，也需要随时结束探索的能力。

Return从到达开始与探索并行，至少形成多系统冗余：
1. **LANDSCAPE｜景观识别**：江、两岸、索道、关键峰林、已走过空间。
2. **SIGNAGE｜实体标识**：在真正决策点明确继续/返回/服务；不是高密度立牌。
3. **PAPER｜纸图**：无网络/电量/登录/定位也能独立工作。
4. **HUMAN SERVICE｜人工服务**：异常、不确定、身体不适、天气变化时求助。
5. **DIGITAL｜数字辅助**：Return、最近可回路径、服务、当前状态；不是唯一方式。

### 状态
- NORMAL：正常探索。
- DEGRADED：部分体验能力下降，但核心路线/Return仍成立。
- CLOSED：明确不可进入，不能用探索标记吸引继续。
- UNKNOWN：不能画成正常开放，必须降低承诺并引导确认/人工服务/可靠路径。

双系统图：上方EXPLORE（复杂/分支/可发现/可跳过），下方RETURN（简单/稳定/冗余/低认知负担），并行贯穿全程。

Route Design Grammar：`ORIENT → CHOOSE → OBSERVE → EXPLORE → STAY/RECOVER → CONTINUE/RETURN`；十三印只是 OPTIONAL CONTENT。

章节结束语：**探索的自由，不来自路线变得更不确定；而来自游客始终知道自己可以怎么回来。**