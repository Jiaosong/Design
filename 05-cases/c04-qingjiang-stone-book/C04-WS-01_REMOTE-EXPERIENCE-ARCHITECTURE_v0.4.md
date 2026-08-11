# C04 Remote Experience Architecture v0.4

**Project:** C04｜清江石书｜红花峰林十三印  
**Stage:** `G1-REMOTE CONDITIONAL PASS / PROVISIONAL G2-G3 DESIGN`  
**Basis:** Remote Site Reconstruction v0.3  
**Boundary:** 本版用于远程方案推进，不等同于现场实测。尺寸、安全、坡度、网络、施工与维护继续 `FIELD-NOT-VERIFIED`。

## 1｜Relation Statement Draft

把红花峰林既有地貌、地方命名与真实游览环线组织成一套“景观先读、文化后置、数字辅助、行走留痕”的低干预阅读系统；游客不是完成任务，而是在索道越江—步行—回程中逐页形成自己的《清江石书》。

## 2｜Master Experience Sequence

`OPEN-00 索道越江 → 01 红岩嘴 → 02 华中第一藤 → 03 铁券天书 → 04 母子相望 → 05 红花石林 → 06 多级阶地·不对称河谷 → 07 仓廪峰 → 08 文山天书 → 09 盐水女神峰 → 10 绝壁天书 → 11 金石为开 → 12 廪君峰 → 13 一线天 → FINALE-00 索道回程／我的清江石书`

## 3｜Four Chapters

1. **越江开卷**：OPEN-00 + 01–03。目标：从“看风景”进入“读山”。
2. **行于峰林**：04–07。目标：关系、景观、河谷与象形阅读，安排全程最大的屏幕退场段。
3. **石上有人**：08–10。目标：把层理事实与盐水女神等文化回声分层表达。
4. **裂隙归江**：11–13 + FINALE。目标：以裂隙、望山和一线天完成收束，手机在回程才重新成为主界面。

## 4｜Node Interaction Matrix

| ID | 节点 | 核心动作 | Phone | 负荷 | 印记 | 角色 |
|---|---|---|---|---|---|---|
| 01 | 红岩嘴 | LOOK / ORIENT | S1 | I0–1 | AUTO | 越江开卷 |
| 02 | 华中第一藤 | COMPARE TIME | S1 | I1 | LIGHT | 生长时间 |
| 03 | 铁券天书 | TRACE / REVEAL | S2 | I1–2 | REVEAL | 崩塌与石页 |
| 04 | 母子相望 | LOOK / RELATE | S1 | I1 | OBSERVATION | 关系阅读 |
| 05 | 红花石林 | REST / LOOK | S0 | I0 | AUTO | Landscape Hero |
| 06 | 多级阶地·不对称河谷 | ALIGN / READ RELATION | S2 | I2 | REVEAL | Science Hero |
| 07 | 仓廪峰 | COMPARE | S1 | I1 | OBSERVATION | 象形阅读 |
| 08 | 文山天书 | READ TIME | S2 | I2 | REVEAL | Narrative Hero |
| 09 | 盐水女神峰 | LOOK / LISTEN | S1 | I1 | LIGHT | 文化回声 |
| 10 | 绝壁天书 | TRACE | S1 | I1 | LIGHT | 纹理阅读 |
| 11 | 金石为开 | SWITCH：事实／故事 | S2 | I2 | REVEAL | 双阅读示范 |
| 12 | 廪君峰 | ALIGN / LISTEN | S1 | I1 | LIGHT | 文化投影 |
| 13 | 一线天 | PASS | S0 | I0 | AUTO | 归缝 |

## 5｜Phone State Rule

- `S0 LANDSCAPE`：屏幕退场；红花石林、一线天为强制候选。
- `S1 PROMPT`：只出现一句观察提示，完成后退屏。
- `S2 REVEAL`：只用于肉眼难理解的层理、河谷关系、崩塌或事实／故事切换。
- `S3 GENERATE`：不绑定具体节点，只保留给 `PHY-01 Route-Segment Hero Candidate`。

## 6｜Route as Blank Pages

12段节点间路线不再全部塞信息，分为：

`TRANSITION / SILENCE / PREVIEW / RECOVERY / CONTEXT / CHAPTER SHIFT`

当前节律：

- 03→04：经过上部脊线普通景点与服务设施，作为 Chapter Shift。
- 04→05：Preview，逐渐把注意力交给峰林。
- 05：最大 Silence，不弹任务、不自动播放。
- 06→07：Recovery，允许纯步行和休息。
- 07→08：第二次 Chapter Shift，从景观关系转入“石上有人”。
- 12→13：强制低屏幕，准备身体穿越。
- 13→索道：Closure Walk，不再新增知识点。

## 7｜Hero Hierarchy

- `H-L01 红花石林`：Landscape Hero，原则 L0，不新增大型设施。
- `H-S01 多级阶地·不对称河谷`：Science Hero，只使用已安全关闭的河谷／阶地表述。
- `H-N01 文山天书`：Narrative Hero，以真实层理为“石书”核心物证。
- `PHY-01`：Physical Hero Candidate，属于路线段而非固定节点；机制仅锁“身体输入 → 低强度环境光反馈 → 自动留痕”，实施位置、发电技术与构造均不锁。

## 8｜Attention Budget

按当前项目资料的 2.5–3h 来源区间，手机主动前台阅读只作为约 20–30 分钟量级的设计上限；普通单次数字交互目标控制在 30–90 秒，Hero Reveal 原则上不超过约 2–3 分钟。其余时间归还给行走、景观、摄影、休息与服务行为。以上均为 `Design Target`，不是现场实测。

## 9｜My Qingjiang Stone Book

终点不显示“13/13通关”。记录结构：

- 已读页 / 未读页
- 四章轨迹
- AUTO 印记
- OBSERVATION 印
- REVEAL 印
- 可选照片 / 文字

回到索道后才生成“本次清江石书”，允许出现“这次读到了 9 页”等非满完成状态。未完成是下一次阅读入口，不是失败。

## 10｜Digital IA Implication

一级 IA 暂锁为：

`今日 / 路线 / 我的石书 / 服务`

十三印作为地图阅读层与“我的石书”目录，不再必须单独作为游戏式一级 Tab。

节点页统一三层：

1. 一句观察提示；
2. 一屏主要解释；
3. 用户主动展开的证据／文化／深读层。

## 11｜Fallback by Design

- AR 不可用：2D 对齐／剖面替代。
- GPS 不可用：二维码／NFC／手动到访作为候选降级，不提前承诺部署。
- 网络不可用：核心节点文本、缩略图与路线需支持离线包设计。
- PHY-01 不可实施：改为纯数字“行迹印”，不影响十三印主系统成立。

## 12｜Key Deletions from Legacy System

退出 Canonical：

- 三角色入口与角色授命；
- 30枚数量目标；
- 每节点强制扫码；
- 每节点 AR；
- 连续奖励／等级／通关表达；
- 为故事逻辑强迫真实路线改序；
- 将红花石林当成必须进入的实体装置节点；
- 将步步生光永久绑定母子峰。

## 13｜Gate Result

- `G2 Relation Statement = PROVISIONAL DRAFT READY FOR REVIEW`
- `G3 Experience Architecture = PROVISIONAL / REMOTE-GROUNDED`
- `G1 IMPLEMENTATION = NOT PASSED`

允许继续数字产品、视觉与展示深化；不允许把尺寸、安全、AR成功率、设备耐久、实际施工条件写成已验证。

**Next:** `C04 Remote Digital Product Architecture v0.5` —— 只做到 IA、状态机、Node Template、My Book Template 与 Fallback；不进入真实开发规格、AR性能承诺或工程实施。
