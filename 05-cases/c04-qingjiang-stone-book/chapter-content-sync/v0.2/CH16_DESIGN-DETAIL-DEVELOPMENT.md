# CH16｜设计深化与细节

Project: `PRJ-C04-QINGJIANG-SHISHU`

Page grammar: `USE → GEOMETRY / STATE → MATERIAL / INTERFACE → CONNECTION → MAINTENANCE / OPEN ITEM`.

All values that are not source-measured remain `DESIGNER ESTIMATE / RANGE / NTS / FIELD OPEN`.

## CH16-P01｜人体与使用尺度不是装饰性人形

深化必须从动作开始：MOVE / LEAN / PERCH / SIT / HALF-RECLINE / OBSERVE / MAINTAIN。人体图形必须与空间任务、视线、支撑点和维护行为绑定，而不是只证明“有一个1.7m的人”。

既有P02 / Fluid Rest尺度测试可作为概念接口，但不得自动升级为现场适配尺寸。

---

## CH16-P02｜平面与定位：先证明为什么需要落位

任何实体候选进入平面前，必须回答：
1. 这里发生什么身体 / 服务问题；
2. 现有设施是否已足够；
3. 不介入是否更好；
4. 介入是否阻挡视线、路径、维护或Return；
5. 位置证据属于 OBSERVED / SOURCE-GROUNDED / INFERRED / ASSUMPTION 哪一层。

R06体验已冻结；技术图只允许解释现有设计，不重新发明平台、栏杆或节点。

---

## CH16-P03｜剖面：把身体—路径—景观关系放在同一张图里

剖面第一阅读顺序：
`PRIMARY FORM / CUT → BODY / PATH → STRUCTURE / RELATION → EDGE / CONNECTION → DIMENSION / NOTE`。

需要表达：
- 行走与停留；
- 身体姿态；
- 观看方向；
- 恢复 / 维护界面；
- 与真实场地不确定性的边界。

模型 / 渲染不能替代剖面中的尺度和关系证据。

---

## CH16-P04｜材料 / CMF：材料角色先于颜色名称

材料选择按角色建立：
`CONTACT / SUPPORT / BUFFER / FASTENER / EXISTING BASE / WEATHER-EXPOSED SURFACE`。

每个材料至少说明：
- 接触和使用角色；
- 户外湿热 / 日晒 / 清洁 / 腐蚀敏感因素；
- 表面摩擦与触感要求；
- 维护、替换和老化方式；
- 当前证据是厂家资料 / 工程参考 / 概念选择 / FIELD待核。

“清江蓝 / 石灰 / 木色”不能替代真实材料性能。

---

## CH16-P05｜连接与可逆性：实体必须能被拆解地解释

连接图必须把 `COMPONENT IDENTITY → JOINT / REVEAL / SETBACK / TERMINATION → LINE HIERARCHY → NOTE` 画清楚。

优先关系：
`EXISTING BASE → BUFFER / ISOLATION → REVERSIBLE CLAMP / FASTENER → REPLACEABLE COMPONENT`。

若需要钻孔、基础、化学锚栓、焊接或结构改变，必须明确升级为 FIELD / ENGINEERING OPEN，不以概念图暗示已批准。

---

## CH16-P06｜排水、防滑、边缘与维护

户外细节不以“看起来完整”为结束。每个候选必须检查：
- 水从哪里来、往哪里走；
- 接触面是否积水 / 藏污；
- 湿态防滑如何验证；
- 边缘、缝隙和夹手点；
- 紧固件能否检查；
- 零件能否单独更换；
- 清洁 / 维修是否需要封路；
- 异常天气如何停用 / 收回。

没有现场与样机数据时给“敏感因素 + FIELD校核项”，不能给伪精确结论。

---

## CH16-P07｜Detail Open Register｜图纸必须告诉下一位专业人员还缺什么

每张深化图旁保留最小 Open Register：
- Source / Revision；
- Design intent；
- Recommended range；
- Sensitive factors；
- Engineering check；
- FIELD check；
- Maintenance check；
- Does-not-prove。

这不是治理Dashboard，而是让设计细节可被结构、景观、运营和施工专业继续校核的接口。

Sources: existing C04 P02 / Fluid Rest / C23 lineages; OLEANDER technical-drawing hierarchy, joint-legibility, dimension-to-object binding, human-scale-activity and material-identity knowledge. `NOT FOR CONSTRUCTION` remains mandatory.