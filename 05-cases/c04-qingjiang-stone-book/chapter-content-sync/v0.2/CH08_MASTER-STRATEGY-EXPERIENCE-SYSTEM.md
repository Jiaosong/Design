# CH08｜总体策略与体验系统

Project: `PRJ-C04-QINGJIANG-SHISHU`

Page grammar: `COMPONENTS → RELATIONS → USER FLOW → FALLBACK → LIMIT`.

Truth boundary: `FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION`.

## CH08-P01｜总体策略：让真实清江保持第一阅读

# 清江石书不是覆盖在景区上的第二套世界，而是一套会主动退场的阅读系统。

总体策略只有一个主次关系：

`REAL QINGJIANG / ROUTE / BODY > SERVICE / RETURN > OPTIONAL READING > DIGITAL / BRAND > MEMORY`。

它把已有系统重新组织为六个互相协作但不互相替代的层：
1. **LANDSCAPE / JOURNEY**｜真实清江、游船、索道、步行、停留、通过；
2. **READING / THIRTEEN IMPRINTS**｜R01–R13 可选内容库；
3. **DIGITAL COMPANION**｜TODAY / ROUTE / READ / MY BOOK / SERVICE / RETURN；
4. **PHYSICAL / BODY / SENSORY**｜休息、倚靠、局部感官与必要实体支持；
5. **BRAND / VISUAL IDENTITY**｜跨媒介识别，但按场景强度退场；
6. **MEMORY**｜清江旅记 × 我的石书，把旅行带出场地。

不是每一层都在每个场景出现。系统完整性来自**正确缺席**，不是同时出现。

---

## CH08-P02｜体验主线：同一条江，被看见三次

# 水上建立整体，空中建立关系，山中建立身体尺度。

核心体验链：

`ENTER → ORIENT → BOAT / ACCESS → CABLE → WALK / DISCOVER → STOP / RECOVER → PASS → RETURN → REMEMBER`

三种移动尺度分别承担不同认知任务：
- BOAT：连续整体 / 河谷内部；
- CABLE：跨江关系 / 移动视点；
- WALK：身体、细节、局部发现和选择。

因此内容不是沿路线平均分布，而应在游客已经获得必要空间前提后出现。

设计规则：
- 未建立整体尺度前，不急于解释局部；
- 移动视点发生时，屏幕退场；
- 需要比较关系时才 Reveal；
- 身体负担或路径风险上升时，内容权重下降；
- 接近 Return 时，服务权重继续上升。

---

## CH08-P03｜阅读系统：十三印是内容层，不是进度层

# PARTIAL IS COMPLETE。

R01–R13构成完整内容库，但用户不需要完成全部内容。系统允许：
- Quick Read：少量关键页；
- Deep Read：更多 Core + Companion + Evidence；
- Family Read：观察动作优先，不幼稚化；
- 无手机：纸图、导视、人工服务与真实景观仍能独立完成旅行。

页面深度由 `S0 / S1 / S2` 控制：
- S0：Landscape / Body；
- S1：Prompt；
- S2：Reveal / Evidence。

核心逻辑：`LOOK → OPTIONAL READ → OPTIONAL SAVE → CONTINUE / RETURN`。

禁止：13/13、遗漏惩罚、打卡进度、强制顺序、任务锁。

---

## CH08-P04｜注意力预算：数字与品牌强度必须随场景变化

# 注意力不是无限资源，设计必须知道什么时候安静。

把整条旅程理解为一个动态 Attention Budget：

### 高景观 / 高身体注意
索道移动、R13压缩通过等场景：
- Digital = OFF / minimal;
- Brand = TRACE / OFF;
- Content = S0;
- Return / Safety可覆盖其他层。

### 中等停留 / 可观察
步行发现、R05等：
- Digital = LIGHT;
- Brand = TRACE / LIGHT;
- Content = S1。

### 稳定停留 / 关系需要解释
R06：
- Landscape First；
- 可选 Relation Reveal；
- Digital 可短时 FULL，但必须完成 attention handoff，再退回 landscape；
- 技术 / Evidence 只做 near-read，不与景观争第一读。

### 离场 / 记忆
- Digital / Brand可重新增强；
- Memory可以成为主层；
- 仍不使用完成率制造压力。

注意：G3R 中的屏幕时间目标属于研究目标，不是现场测量值。

---

## CH08-P05｜异常与恢复：系统必须在“不顺利”时仍然成立

# 服务系统的专业度，不是在正常状态下有多少功能，而是在异常状态下是否仍知道该怎么办。

根据 OLEANDER Service Design 的 Failure & Recovery First，把系统状态作为总体策略，而不是 App 附属功能：

### NORMAL
正常路线、可选内容、完整体验。

### DEGRADED
部分内容 / 数字 / 设施能力下降；保留路线、Return、实体与人工服务。

### CLOSED
明确不可进入；视觉、地图、导视和数字都必须形成 hard stop，不以游戏化发现继续吸引。

### UNKNOWN
没有可靠信息时不假设开放；降低承诺，优先可靠路径、人工确认和 Return。

恢复链：
`DETECT → INFORM → REDUCE LOAD → OFFER SAFE ALTERNATIVE → RETURN / HUMAN HELP → RECORD OPEN ITEM`。

系统冗余：
`LANDSCAPE + SIGNAGE + PAPER + HUMAN + DIGITAL`。

任何单一技术失败，都不能让游客失去完成旅行和返回的能力。

---

## CH08-P06｜跨系统关系：每个系统只做它真正擅长的事

# 一个成熟系统的标志，是系统之间有边界，而不是所有系统都能做所有事情。

| System | Primary Role | Must Not Replace |
|---|---|---|
| Landscape / Journey | 空间、移动、身体、第一阅读 | Digital / Brand |
| Route / Service / Return | 决策、方向、异常恢复 | Thirteen Imprints |
| Thirteen Imprints | 可选观察与解释 | Route authority |
| Digital | 提示、Reveal、记录、服务辅助 | 现场定位真相 / 唯一Return |
| Physical / Sensory | 身体支持或必要局部体验 | 景观主角 |
| Brand | 跨媒介识别与语言一致性 | Operational state / Safety |
| Memory | 旅后记录与再认识 | 打卡完成率 |
| Technical Proof | 说明关系怎么成立 | Landscape / Experience Hero |

### 系统协同语法
`LANDSCAPE FIRST → ORIENT → CHOOSE → OBSERVE → OPTIONAL REVEAL → RECOVER / CONTINUE → RETURN → RECOGNIZE → RECORD`。

### 总体设计判断
**清江石书的“完整”，不是所有媒介同时工作，而是游客在任何状态下都能继续看清江、理解下一步、决定是否阅读，并随时安全地结束探索。**

### 本章来源边界
- C04 Canonical / G3R Experience Architecture / Current Authority v3.2。
- Notion Knowledge：`FW-SERVICE-DESIGN-001`、`MTH-RESEARCH-JOURNEY-001`、`FW-BRAND-STRATEGY-001`。
- OLEANDER reusable Skill lineage：route-state semantics、wayfinding decision priority、responsive recomposition、temporal handoff、brand-intensity modulation、exploration behavior grammar。
- DOES NOT PROVE：现场行走时间、疲劳曲线、真实关闭策略、实时运营接口、应急疏散、安全、无障碍、容量与管理SOP。