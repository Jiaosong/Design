# C04 Remote Digital Product Migration v0.5

Project: C04｜清江石书｜红花峰林十三印  
Basis: Remote Experience Architecture v0.4 + existing `清江三十印` low-fi board  
Status: PROVISIONAL / REMOTE-GROUNDED

## 1. Migration principle

现有低保真不推翻重做；保留其已完成的页面骨架、地图、节点、AR、印记、个人记录和终章能力，删除角色/RPG/30枚任务制，把所有交互改写为“今日—路线—节点阅读—我的石书—服务”的低干预系统。

Public top-level IA: `今日 / 路线 / 我的石书 / 服务`

Non-tab states/components: `首次阅读方式 / 节点提示 / Reveal / 已记录Toast / PHY-01 / 本次石书生成 / 分享卡`.

## 2. Screen-by-screen migration

| Legacy screen | Action | New target |
|---|---|---|
| role-select 角色选择 | DELETE/MERGE | 首次使用“阅读方式”Bottom Sheet：轻读 / 深读 / 亲子；可跳过，不产生角色身份 |
| home 首页 | REWRITE | `今日`：当前章节、下一页、一个观察提示、路线继续、必要服务快捷入口 |
| map 路线地图 | KEEP/REBUILD | `路线`：真实景区底图 + 十三印阅读层 + 服务层；不使用幻想地图 |
| quest 行程任务 | DELETE AS PAGE | 拆到今日、节点、章节抽屉；不再有任务列表/完成率 |
| node 节点详情 | KEEP CORE | 三层Node Template：先看什么 → 一屏解释 → 深读证据/文化；保留下一页 |
| ar AR体验 | MERGE AS MODE | `Reveal`组件，仅S2节点调用；2D剖面/对齐为默认fallback |
| role 角色页 | DELETE | 迁为设置里的“阅读方式”，无角色头像、等级、技能 |
| my-book 我的行书 | PROMOTE | 一级Tab `我的石书`：四章、已读/未读、印记、照片/文字、分享 |
| check-in success 打卡成功 | MERGE | 非阻塞Toast：“这一页已记录”；不使用全屏成功页 |
| stamp collection 印章收集 | MERGE | 融入我的石书页格；章是阅读痕迹，不是稀有度奖励 |
| installation interaction 装置互动 | CONDITIONAL | `PHY-01`路线段Hero；仅实施时出现，默认“请收起手机继续前行” |
| AR互动场景 | MERGE | 节点Reveal的子模式：剖面/轮廓/声音/文化回声，不单独建页 |
| finale 终章仪式 | REWRITE | `本次石书生成`，放到索道回程/返回阶段；允许未完成 |
| result poster 结局海报 | KEEP OPTIONAL | `分享卡`，由本次已读页与照片生成；用户主动分享，不强制 |
| — | ADD | `服务`一级Tab：索道/游船入口、厕所、休息、餐饮、急救、返回、离线包；实时运营信息没有接入前不得伪装实时 |

## 3. State model

`APP_INIT → READING_MODE(optional) → TODAY → ROUTE → APPROACH_NODE → NODE_PROMPT → S0/S1/S2 → RECORDED → ROUTE_CONTINUE → ... → CLOSURE_WALK → BOOK_GENERATE → MY_BOOK`

Phone states:
- S0 LANDSCAPE: 红花石林、一线天等退屏。
- S1 PROMPT: 一句提示后退屏。
- S2 REVEAL: 河谷/层理/崩塌/事实-故事切换。
- S3 GENERATE: 只留给PHY-01，且不绑定具体节点。

## 4. Remote reconstructed node assignment

01 红岩嘴 S1 / AUTO  
02 华中第一藤 S1 / LIGHT  
03 铁券天书 S2 / REVEAL  
04 母子相望 S1 / OBSERVATION  
05 红花石林 S0 / AUTO  
06 多级阶地·不对称河谷 S2 / REVEAL  
07 仓廪峰 S1 / OBSERVATION  
08 文山天书 S2 / REVEAL  
09 盐水女神峰 S1 / LIGHT  
10 绝壁天书 S1 / LIGHT  
11 金石为开 S2 / REVEAL  
12 廪君峰 S1 / LIGHT  
13 一线天 S0 / AUTO

## 5. Page templates

### TODAY
- 当前章 + 页码状态（不用“任务进度”）
- 下一页名称
- 一句观察提示
- 主按钮：继续行走 / 打开路线
- 小型服务入口：返回、厕所、休息
- 无角色头像、经验值、奖励角标

### ROUTE
- 真实底图
- 当前路径与当前位置（未有真实定位时原型标为模拟）
- 十三印层开关
- 服务设施层开关
- 普通景点保持上下文但不全部任务化
- 用户界面不显示R1/R2证据等级；证据等级属于内部管理层

### NODE
1. `先看什么`（一句）
2. `看懂它`（一屏核心解释，必要时Reveal）
3. `再深一点`（事实 / 地方叙事 / 证据来源）
4. `这一页已记录`（自动或行为触发）
5. `下一页`

### MY BOOK
- 本次：读到X页（非13/13通关）
- 四章轨迹
- 13页网格：已读/未读/照片/文字
- 印记类型：AUTO / OBSERVATION / REVEAL / PHYSICAL
- 分享卡
- 未读页作为二刷入口

### SERVICE
- 索道/游船入口（仅展示已接入或官方链接信息）
- 厕所 / 休息 / 餐饮 / 急救 / 返回
- 离线包
- 紧急联系方式需在正式运营数据核验后填入

## 6. Fallback

- AR unavailable → 2D overlay / section.
- GPS unavailable → manual location / optional QR or NFC candidate.
- Network unavailable → cached route, node text and thumbnails.
- PHY-01 unavailable → digital `行迹印`.
- Node unavailable/closed → mark “本次未开放”，route reroutes without treating user as failed.

## 7. Legacy deletions

删除：角色授命、三角色分支、30枚目标、任务列表、全屏打卡成功、等级/奖励、每点AR、强制扫码、13/13通关、为故事改真实路线。

## 8. Design boundary

本版本可以用于低保真、展板和交互演示。以下仍为 FIELD-NOT-VERIFIED：真实GPS、路线时间、网络质量、AR成功率、设施实时状态、PHY-01工程条件、安全/维护/施工许可。
