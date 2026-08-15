window.C04_DATA = {
  meta: {
    project: "C04｜清江石书｜红花峰林十三印",
    projectId: "PRJ-C04-QINGJIANG-SHISHU",
    state: "REMOTE RESEARCH DESIGN / EXPLORE",
    fieldObserved: 0,
    fieldMeasured: 0,
    g1f: "HOLD",
    promotion: "NO",
    proposition: "山水为纸，岩层为字，行走成书。",
    boundary: "远程研究型概念展示。非现场测绘、非施工图、非实时运营系统。"
  },
  route: [
    { id:"M0", name:"PREP", zh:"出发准备", state:"LIGHT", reality:"OPERATION OPEN", responsibility:"服务 / 回程确定性 / 条件认知", note:"到达方式尚未锁定；不将游船设为必经。" },
    { id:"M1", name:"ARRIVAL", zh:"北岸抵达", state:"LIGHT", reality:"REMOTE SOURCE / FIELD OPEN", responsibility:"方向 / 回程 / 人工服务", note:"road | boat | unknown → 云坛口服务系统。" },
    { id:"M2", name:"CROSS-RIVER", zh:"索道越江", state:"MOVE · S0–LIGHT", reality:"REMOTE SOURCE / POV OPEN", responsibility:"安全 / 流动 / 交通 / 回程优先", note:"索道首先是交通基础设施，观看叙事退居其次。" },
    { id:"M3", name:"WALKING NETWORK", zh:"南岸峰林网络", state:"SILENCE ↔ LIGHT", reality:"NETWORK SOURCE / MICRO ORDER OPEN", responsibility:"路线连续 / 身体 / 景观", note:"多分支、随地形行走；十三印不拥有路线顺序。" },
    { id:"M4", name:"OBSERVE / READ / RECOVER", zh:"观察 · 阅读 · 恢复", state:"LIGHT → S1/S2 OPTIONAL", reality:"CONDITIONAL / G1F", responsibility:"观察 / 理解 / 休息", note:"只有真实视点、问题或疲劳状态触发；最低干预。" },
    { id:"M5", name:"NATURAL CLOSURE", zh:"自然收束", state:"WITHDRAW · S0/OFF", reality:"R13 FIELD OPEN", responsibility:"身体 / 景观 / 安全", note:"进入真实自然收束空间时，品牌、内容与数字主动退场。" },
    { id:"M6", name:"RETURN", zh:"安全回程", state:"RETURN · LIGHT", reality:"MACRO RETURN / OPERATION OPEN", responsibility:"回程 / 服务 / 方向 / 安全", note:"回程优先上升时关闭新深读入口。" },
    { id:"M7", name:"EXIT / MEMORY", zh:"离开 · 留痕", state:"LIGHT / POST-VISIT OPTIONAL", reality:"REAL EXIT SERVICE OPEN", responsibility:"退出确定性 / 记忆", note:"《我的清江石书》只能发生在不阻断退出之后。" }
  ],
  nodes: [
    {id:"R01", title:"红岩嘴", role:"移动观看 / 越江开卷", status:"SOURCE-GROUNDED · FIELD OPEN", evidence:"索道移动观看关系成立；连续 cabin POV 未取得。", level:"source", featured:true},
    {id:"R02", title:"华中第一藤", role:"生长阅读候选", status:"EXPERT REQUIRED", evidence:"公共节点使用有来源；物种、年龄与“第一”标准未闭合。", level:"hold", featured:false},
    {id:"R03", title:"铁券天书", role:"岩面阅读候选", status:"FIELD / GEOLOGY EXPERT", evidence:"区域地质背景不能替代具体节点岩性、时代与形成机制。", level:"hold", featured:false},
    {id:"R04", title:"母子相望 / 母子峰", role:"关系阅读候选", status:"FIELD NAME / VIEWPOINT OPEN", evidence:"名称与实际视点仍需现场标牌和观看关系核验。", level:"open", featured:false},
    {id:"R05", title:"红花石林", role:"Landscape Hero / 可选支线视域", status:"SOURCE-GROUNDED · SAME-VIEW WEATHER OPEN", evidence:"晴朗观景条件有第一方支持；不得伪造同机位晴雾 A/B。", level:"source", featured:true},
    {id:"R06", title:"多级阶地 · 不对称河谷", role:"Science Hero / 观景关系", status:"SOURCE PASS · FIELD GEOMETRY OPEN", evidence:"观景平台角色与河谷关系有运营方来源；精确平台、阶地计数、测量剖面均未验证。", level:"source", featured:true},
    {id:"R07", title:"仓禀峰", alt:"仓廪峰（Legacy / alternate provenance）", role:"象形阅读候选", status:"OPERATOR PUBLIC NAME · FIELD SIGN OPEN", evidence:"当前第一方公开材料优先“仓禀峰”；现场标牌仍待核验。", level:"source", featured:true},
    {id:"R08", title:"文山天书", role:"石书 / 层理阅读候选", status:"FIELD / GEOLOGY EXPERT", evidence:"可做观察型阅读；节点级科学形成机制不能由区域资料替代。", level:"hold", featured:false},
    {id:"R09", title:"盐水女神峰", role:"地方叙事回声", status:"TEXT TRADITION CLOSED · SITE EQUIVALENCE NO", evidence:"务相—廪君—盐水神女文本传统可引用；现代山峰不等于古代事件地点。", level:"source", featured:true},
    {id:"R10", title:"绝壁天书", role:"纹理阅读候选", status:"FIELD / GEOLOGY EXPERT", evidence:"具体岩性、时代与形成机制仍需现场或专家。", level:"hold", featured:false},
    {id:"R11", title:"金石为开", role:"事实 / 故事双读候选", status:"FIELD / SAFETY OPEN", evidence:"保留阅读机制，不把具体裂隙几何、安全或可达性写成已验证。", level:"open", featured:false},
    {id:"R12", title:"廪君峰", role:"望山 / 文本传统", status:"SOURCE-GROUNDED RELATION", evidence:"运营方报道给出其位于观景平台右侧的相对关系；不构成强制停留。", level:"source", featured:true},
    {id:"R13", title:"一线天", role:"Natural Closure / 归缝", status:"SOURCE-GROUNDED · SAFETY OPEN", evidence:"天然狭口框景关系有来源；尺寸、安全、无障碍与准确影像仍为现场项。", level:"source", featured:true}
  ],
  blockers: [
    {id:"A_G1F", title:"FIELD / PROFESSIONAL SURVEY", detail:"微路线、尺寸、可达性、容量、视点、安全与运营未现场闭合。"},
    {id:"R02_EXPERT_EVIDENCE", title:"BOTANY", detail:"R02 物种与生态判断需要合格植物证据。"},
    {id:"R06_EXACT_SCIENCE_HERO_AND_FIELD_GEOMETRY", title:"R06 SCIENCE HERO", detail:"观景平台眼高原像素与实测几何仍缺。"},
    {id:"R07_FIELD_NAME_AUTHORITY", title:"R07 FIELD NAME", detail:"“仓禀峰 / 仓廪峰”现场标牌权威未闭合。"},
    {id:"R13_IMAGE_ASSET_AND_FIELD_SAFETY", title:"R13 SAFETY + MEDIA", detail:"一线天准确影像、进出安全与无障碍未现场核验。"}
  ],
  sources: [
    {kind:"FIRST PARTY", title:"红花峰林景区手绘导览", date:"2025-08-05", url:"https://www.esdqj.cn/jdwf/87.html", direct:"https://www.esdqj.cn/upload/20250805/f8d50b8f0d5027.jpg", use:"宏观空间关系 / 多分支步行网络 / 跨江索道；非测绘。"},
    {kind:"FIRST PARTY", title:"2025年恩施大清江景区旅游攻略", date:"2025", url:"https://www.esdqj.cn/jdwf/85.html", use:"云坛口、索道往返与宏观进入链；2025票价/班次不作为2026实时事实。"},
    {kind:"OPERATOR / MEDIA", title:"在恩施红花峰林 遇见山高水长", date:"2024-05-22", url:"https://www.eslygroup.com/media_focus/3229.html", use:"R06观景平台角色、R12相对关系、R13天然框景关系。"},
    {kind:"OPERATOR CURRENT", title:"党建引领惠民生 跨江索道暖人心", date:"2026-02-10", url:"https://www.eslygroup.com/party_building/4357.html", use:"索道兼具两岸居民日常通行功能；否决tourist-only persona。"}
  ]
};
