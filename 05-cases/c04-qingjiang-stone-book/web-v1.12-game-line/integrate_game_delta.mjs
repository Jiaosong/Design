import fs from "node:fs";

const target = new URL("./index.html", import.meta.url);
let html = fs.readFileSync(target, "utf8");
if (html.includes('class="game-delta')) {
  console.log("v1.12 game delta already integrated; no duplicate write.");
  process.exit(0);
}

html = html
  .replace("清江石书｜v3.2 + Authoring v0.2｜112-page Web Carrier", "清江石书｜v1.12 游戏线整合｜20章 / 112页")
  .replace("清江石书 current Web carrier consuming v3.2 authority plus latest user authoring delta PR #230; 20 chapters / 112 carrier surfaces; official final project PAGE-ID count not claimed.", "清江石书 CH00–CH19 主 Web；在 v1.11 的 20 章 / 112 个载体页面中整合变形船、愿蝶、舟印、AR、佩戴物与营地兑换，不改变路线与回程主权。");

const inserts = [
  ["游客在任何状态下都能继续看清江、理解下一步、决定是否阅读，并随时结束探索。", `<div class="game-delta system-delta"><div class="delta-kicker">USER CURRENT DELTA / SYSTEM BINDING</div><div class="system-chain"><b>ROUTE-03</b><i>→</i><b>变形船钥匙</b><i>→</i><b>真实观察</b><i>→</i><b>愿蝶回应</b><i>→</i><b>个人舟印</b><i>→</i><b>RETURN / MEMORY</b></div><div class="delta-columns"><p><strong>路线与服务</strong>决定能否进入、继续或返回。</p><p><strong>变形船</strong>只把观察动作转译成可携带形态。</p><p><strong>愿蝶装置</strong>只作一次回应，不解锁真实路径。</p><p><strong>舟印</strong>进入个人石书，缺片仍然完整。</p></div></div>`],
  ["看到一个印，是一次邀请；跳过一个印，不是一次失败。", `<div class="game-delta"><div class="delta-kicker">CONTENT LIBRARY / NOT PHYSICAL CHECKPOINTS</div><p class="delta-lead">十三种舟形不是十三个必须安装的船，也不是十三处扫码闸门；它们是 R01–R13 内容对象在“观察完成以后”生成的可选形态。</p><div class="delta-columns"><p><strong>造型来源</strong>峰、谷、水、风、叶、星等已读关系。</p><p><strong>触发边界</strong>二维码 / NFC / 手动编号均可失败。</p><p><strong>跳过权</strong>未获得舟印不影响游程和回程。</p><p><strong>R13</strong>不扫描、不变形、不兑换，直接归航。</p></div></div>`],
  ["点击、滑动、打开只是载体操作；清江真正的互动是看、走、停、比较、等待、回望。", `<div class="game-delta morph-delta"><div class="delta-kicker">MORPHING BOAT / ONE CORE + THREE FOLDS</div><svg aria-label="船形从观看、解释、游戏、照护到归航的五种矢量状态" class="morph-sequence" role="img" viewBox="0 0 1100 250"><g transform="translate(30 22)"><path d="M20 90 Q95 135 170 90 L146 150 Q95 180 44 150Z"/><path class="wing" d="M26 83 L80 40 L77 110Z"/><path class="wing" d="M164 83 L110 40 L113 110Z"/><text x="95" y="210">观 / CULTURE</text></g><g transform="translate(245 22)"><path d="M20 90 Q95 135 170 90 L146 150 Q95 180 44 150Z"/><path class="wing" d="M22 82 L72 16 L82 112Z"/><path class="wing" d="M168 82 L118 16 L108 112Z"/><text x="95" y="210">解 / WISDOM</text></g><g transform="translate(460 22)"><path d="M20 90 Q95 135 170 90 L146 150 Q95 180 44 150Z"/><path class="wing" d="M18 92 L48 20 L82 112Z"/><path class="wing" d="M172 92 L142 20 L108 112Z"/><circle class="action" cx="95" cy="136" r="15"/><text x="95" y="210">变 / PLAY</text></g><g transform="translate(675 22)"><path d="M20 98 Q95 132 170 98 L150 145 Q95 168 40 145Z"/><path class="wing" d="M38 90 L76 61 L80 112Z"/><path class="wing" d="M152 90 L114 61 L110 112Z"/><text x="95" y="210">护 / CARE</text></g><g transform="translate(890 22)"><path d="M28 96 Q95 116 162 96 L145 136 Q95 153 45 136Z"/><path class="wing" d="M49 91 L82 76 L82 109Z"/><path class="wing" d="M141 91 L108 76 L108 109Z"/><text x="95" y="210">收 / RETURN</text></g></svg><p class="delta-lead">真实动作先发生：LOOK / COMPARE / LISTEN / WAIT / RECOVER；船形只是动作结果的可见反馈，不能反过来把现场变成操作屏。</p></div>`],
  ["游戏感来自未完全揭开的地图、路线选择和自己的轨迹，不来自任务点、积分或完成度。", `<div class="game-delta dark-delta"><div class="delta-kicker">QR / AR / ROUTE RELATION</div><div class="delta-columns"><p><strong>二维码识别</strong>只定位内容对象，不宣称实时 GPS。</p><p><strong>增强现实</strong>叠加植物、地形、文化来源或星空关系；正式文字保持网页矢量层。</p><p><strong>年龄深度</strong>儿童提问与 AI 宠物引导；青年比较与推理；成人来源化深读；长者先看休息与回程。</p><p><strong>失败路径</strong>离线预载、纸图、编号、标识与人工服务并列。</p></div><div class="delta-status">NORMAL × FULL · DEGRADED × LIGHT · CLOSED × OFF · UNKNOWN × OFF</div></div>`],
  ["我的石书由游客自己生成；数字记录与实体《清江旅记》互补，不互相复制。", `<div class="game-delta dark-delta"><div class="delta-kicker">IMPRINT AS PERSONAL MAP</div><p class="delta-lead">舟印组合不是标准答案：它可以形成个人的清江关系图、宝藏式线索图或抽象地图，但不能冒充测绘地图，也不要求拼齐。</p><div class="delta-columns"><p><strong>保存</strong>记录自己主动选择的观察。</p><p><strong>组合</strong>不同舟形以磁吸 / 卡扣 / 数字拼接形成关系。</p><p><strong>带走</strong>可转译为纸卡、徽章或佩戴识别件。</p><p><strong>空白</strong>未读内容保持空白，不显示缺失惩罚。</p></div></div>`],
  ["每提升一级重新判断 BODY VALUE / LANDSCAPE COST / SITE NECESSITY / MAINTENANCE / SAFETY / FIELD DEPENDENCY。", `<div class="game-delta"><div class="delta-kicker">WEARABLE / REST / AGE BINDING</div><div class="delta-columns"><p><strong>长者｜手链</strong>低操作、回程识别、休息提醒；不得作医疗监测承诺。</p><p><strong>青年｜手环</strong>承载可选舟印与夜间低照识别。</p><p><strong>儿童｜魔法棒</strong>用于指向、提问和亲子协作，不驱动追逐。</p><p><strong>颈枕 / 坐垫</strong>与 P02 栏杆倚靠、Fluid Rest 的靠 / 坐关系协同，不新增孤立产品。</p></div><div class="delta-status">防蚊、草药解暑、照明、承载与皮肤接触功效：PROVISIONAL / SAFETY + MATERIAL + OPERATION REVIEW REQUIRED</div></div>`],
  ["从风向、植物运动、温度、声音、雾、水面变化开始；禁止民族符号化、风铃景观化和巨大风动雕塑。", `<div class="game-delta"><div class="delta-kicker">QINGFENGYIN → WISH BUTTERFLY RESPONSE</div><div class="delta-columns"><p><strong>钥匙进入</strong>完成一次真实观察后，船核靠近装置。</p><p><strong>蝶翼回应</strong>暖光 / 轻响 / 局部摆动只出现一次，随后撤回。</p><p><strong>风的角色</strong>优先读取植物、水面与声音；微型发电只作待校核能源路径。</p><p><strong>夜间边界</strong>避免眩光、持续闪烁和大型景观化风铃。</p></div></div>`],
  ["清江一线 / 清江雾气 / 清风吟 / 红花峰崽等延展必须按真实成熟度分层。", `<div class="game-delta"><div class="delta-kicker">CARD → CAMP EXCHANGE / MEMORY CONTINUATION</div><div class="delta-columns"><p><strong>观察卡</strong>把舟印、来源与个人记录做成可交换纸卡。</p><p><strong>营地兑换</strong>只兑换已定义的服务或食物，不把路线安全与基础食物绑定到游戏完成。</p><p><strong>食物魔盒</strong>优先解决分格、密封、保温 / 保冷、过敏原提示、清洁与返还。</p><p><strong>露营设备</strong>沿用祝设计的现有系统，新增件必须证明接口和存储必要性。</p></div><div class="delta-status">兑换规则、食品安全、库存、回收清洁与运营责任：OPERATOR REVIEW OPEN</div></div>`],
  ["Open Register不是治理Dashboard；它要贴近具体图纸，告诉结构、景观、运营和施工专业下一步核什么。", `<div class="game-delta"><div class="delta-kicker">NEW OBJECT OPEN REGISTER</div><div class="delta-columns"><p><strong>船钥匙 / 舟印</strong>连接寿命、吞咽风险、锐边、磁体与可维修性。</p><p><strong>愿蝶装置</strong>结构、夹伤、耐候、眩光、噪声、维护与退出方式。</p><p><strong>佩戴物 / 草药</strong>皮肤接触、过敏、儿童误用、成分批次与功效合规。</p><p><strong>食物魔盒</strong>食品接触材料、温控、交叉污染、清洗消毒与运营闭环。</p></div></div>`]
];

for (const [anchor, block] of inserts) {
  const position = html.indexOf(anchor);
  if (position < 0) throw new Error(`Missing anchor: ${anchor}`);
  const note = html.lastIndexOf('<div class="authored-note-v32', position);
  if (note < 0) throw new Error(`Missing note container: ${anchor}`);
  html = html.slice(0, note) + block + html.slice(note);
}

fs.writeFileSync(target, html);
