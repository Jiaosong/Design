import fs from "node:fs";

const target = new URL("./index.html", import.meta.url);
let html = fs.readFileSync(target, "utf8");

if (html.includes('data-game-line-version="1.12-r2"')) {
  console.log("game-line v1.12-r2 already integrated");
  process.exit(0);
}
if (html.includes('class="game-delta')) {
  throw new Error("Refusing to stack r2 over an earlier game-line integration. Rebind from the v1.11 carrier first.");
}

html = html
  .replace("清江石书｜v3.2 + Authoring v0.2｜112-page Web Carrier", "清江石书｜v1.12-r2 游戏线细化｜20章 / 112载体页")
  .replace("<body>", '<body data-game-line-version="1.12-r2">')
  .replace("清江石书 current Web carrier consuming v3.2 authority plus latest user authoring delta PR #230; 20 chapters / 112 carrier surfaces; official final project PAGE-ID count not claimed.", "清江石书 CH00–CH19 主 Web；在 v1.11 的 20 章 / 112 个载体页面中细化变形船、愿蝶、舟印、AR、佩戴物与营地兑换。112 仅为当前 Web 载体页数，不作为最终 canonical PAGE count。");

const panels = [
  ["游客在任何状态下都能继续看清江、理解下一步、决定是否阅读，并随时结束探索。", `
  <section class="game-delta system-delta" aria-labelledby="game-system-title">
    <header class="delta-header"><div><span class="delta-kicker">041 / RELATION SYSTEM</span><h3 id="game-system-title">一枚舟印，必须从真实观察中来，也必须允许随时结束。</h3></div><span class="evidence-chip inferred">DESIGN INFERENCE</span></header>
    <ol class="relation-flow">
      <li><b>路线确认</b><span>先判断能否进入、继续或返回</span><em>ROUTE-03 / SERVICE</em></li>
      <li><b>完成观察</b><span>看、比较、听、等待或恢复</span><em>BODY / LANDSCAPE</em></li>
      <li><b>船核回应</b><span>把刚才的动作折成一种舟形</span><em>OPTIONAL OBJECT</em></li>
      <li><b>愿蝶一次响应</b><span>暖光或轻响后主动撤回</span><em>NO ROUTE UNLOCK</em></li>
      <li><b>保存舟印</b><span>进入个人石书，不计算完成率</span><em>PARTIAL IS COMPLETE</em></li>
      <li><b>继续或回程</b><span>游戏层退出，可靠路径保持可见</span><em>RETURN FIRST</em></li>
    </ol>
    <div class="state-strip" aria-label="运行和媒介状态"><b>NORMAL × FULL</b><b>DEGRADED × LIGHT</b><b>CLOSED × OFF</b><b>UNKNOWN × OFF</b></div>
  </section>`],

  ["看到一个印，是一次邀请；跳过一个印，不是一次失败。", `
  <section class="game-delta library-delta" aria-labelledby="boat-library-title">
    <header class="delta-header"><div><span class="delta-kicker">047 / THIRTEEN CONTENT OBJECTS</span><h3 id="boat-library-title">十三舟形是内容语法，不是十三处实体任务点。</h3></div><span class="evidence-chip material">CURRENT CONTENT LOGIC</span></header>
    <div class="boat-library" aria-label="十三个可选内容对象">
      ${Array.from({length:13},(_,i)=>`<article class="boat-token ${i===5?'is-known':''} ${i===12?'is-return':''}"><span>R${String(i+1).padStart(2,'0')}</span><svg viewBox="0 0 120 72" aria-hidden="true"><path d="M12 34 Q60 64 108 34 L91 58 Q60 70 29 58Z"/><path class="fold" d="M18 31 L${42+(i%4)*5} ${8+(i%3)*5} L50 42Z"/><path class="fold" d="M102 31 L${78-(i%4)*5} ${8+(i%3)*5} L70 42Z"/></svg><b>${i===5?'河谷观察':i===12?'归航 / 静默':'可选内容对象'}</b><small>${i===12?'PLAY OFF · RETURN ON':'SOURCE BINDING OPEN'}</small></article>`).join('')}
    </div>
    <footer class="delta-foot"><span>二维码 / NFC / 手动编号均可失败</span><span>不出现 13/13、连续签到或遗漏惩罚</span><span>R13 不扫描、不变形、不兑换</span></footer>
  </section>`],

  ["点击、滑动、打开只是载体操作；清江真正的互动是看、走、停、比较、等待、回望。", `
  <section class="game-delta morph-delta" aria-labelledby="morph-title">
    <header class="delta-header"><div><span class="delta-kicker">050 / MORPHING BOAT KEY</span><h3 id="morph-title">同一船核，用折叠表达五种行为结果。</h3></div><span class="evidence-chip inferred">EDITABLE VECTOR PROTOTYPE</span></header>
    <div class="morph-workbench">
      <div class="morph-controls" role="group" aria-label="选择船形状态">
        <button class="is-active" data-boat-state="observe" type="button"><b>观</b><span>LOOK / CULTURE</span></button>
        <button data-boat-state="read" type="button"><b>解</b><span>COMPARE / WISDOM</span></button>
        <button data-boat-state="play" type="button"><b>变</b><span>DISCOVER / PLAY</span></button>
        <button data-boat-state="care" type="button"><b>护</b><span>RECOVER / CARE</span></button>
        <button data-boat-state="return" type="button"><b>收</b><span>WITHDRAW / RETURN</span></button>
      </div>
      <figure class="boat-key-stage" data-current-boat="observe">
        <svg class="boat-key" role="img" aria-labelledby="boat-key-title boat-key-desc" viewBox="0 0 760 390">
          <title id="boat-key-title">可变形船钥匙矢量构型</title><desc id="boat-key-desc">固定中央船核与三条折线形成五种可逆状态；这是概念原型，不是制造图。</desc>
          <path class="guide" d="M86 302 H674M380 46 V337"/><path class="boat-core" d="M180 190 Q380 330 580 190 L510 310 Q380 366 250 310Z"/>
          <g class="boat-wings"><path class="wing wing-left" d="M190 180 L320 76 L332 232Z"/><path class="wing wing-right" d="M570 180 L440 76 L428 232Z"/></g>
          <circle class="boat-action" cx="380" cy="270" r="30"/><path class="fold-line" d="M190 180 L332 232M570 180 L428 232M250 310 L510 310"/>
          <text class="boat-state-label" x="380" y="35">观 / LOOK</text><text class="boat-note" x="380" y="382">ONE CORE · THREE FOLDS · REVERSIBLE STATES</text>
        </svg>
        <figcaption><b>固定：</b>船核、连接位、回程识别。<b>变化：</b>翼片角度、光点与信息深度。<span>CONCEPT / NTS / MANUFACTURING OPEN</span></figcaption>
      </figure>
    </div>
  </section>`],

  ["游戏感来自未完全揭开的地图、路线选择和自己的轨迹，不来自任务点、积分或完成度。", `
  <section class="game-delta ar-delta dark-delta" aria-labelledby="ar-title">
    <header class="delta-header"><div><span class="delta-kicker">054 / QR · AR · AGE DEPTH</span><h3 id="ar-title">识别同一个真实地点，不同年龄只改变解释深度。</h3></div><span class="evidence-chip unknown">GPS / LIVE DATA NOT CLAIMED</span></header>
    <div class="ar-layout">
      <figure class="ar-scene"><img alt="项目现有清江河谷观察图像" src="assets/r06_qingjiang.jpg"/><div class="ar-reticle" aria-hidden="true"><i></i><i></i><i></i><i></i></div><div class="ar-label" data-ar-copy><b>这片河谷为什么在这里收窄？</b><span>先比较两岸峰体，再选择是否打开解释。</span></div><figcaption>EXISTING PROJECT IMAGE + LIVE HTML/SVG OVERLAY</figcaption></figure>
      <div class="ar-interface">
        <div class="age-tabs" role="tablist" aria-label="解释深度"><button class="is-active" data-age="child" role="tab" aria-selected="true">儿童</button><button data-age="youth" role="tab" aria-selected="false">青年</button><button data-age="adult" role="tab" aria-selected="false">成人</button><button data-age="elder" role="tab" aria-selected="false">长者</button></div>
        <div class="ar-copy-panel"><span data-ar-mode>AI 宠物提问 / FAMILY READ</span><h4 data-ar-title>先找出两岸最靠近的地方</h4><p data-ar-body>用指向与比较回答，不要求连续看屏幕；成人可关闭宠物提示。</p></div>
        <dl class="fallback-list"><div><dt>识别成功</dt><dd>打开来源化矢量解释</dd></div><div><dt>弱网 / 离线</dt><dd>读取预载轻量内容</dd></div><div><dt>无法识别</dt><dd>输入编号或看纸图</dd></div><div><dt>CLOSED / UNKNOWN</dt><dd>AR OFF，路线与人工服务保留</dd></div></dl>
      </div>
    </div>
  </section>`],

  ["我的石书由游客自己生成；数字记录与实体《清江旅记》互补，不互相复制。", `
  <section class="game-delta imprint-delta dark-delta" aria-labelledby="imprint-title">
    <header class="delta-header"><div><span class="delta-kicker">058 / PERSONAL IMPRINT MAP</span><h3 id="imprint-title">拼图不还原一张标准地图，而是显出自己的观看关系。</h3></div><span class="evidence-chip inferred">ABSTRACT RELATION MAP</span></header>
    <div class="imprint-layout">
      <div class="imprint-pool" aria-label="可选择的舟印">${['水面','峰谷','风向','叶脉','河谷','星空'].map((n,i)=>`<button class="imprint-piece ${i<3?'is-placed':''}" data-imprint="${i}" type="button" aria-pressed="${i<3?'true':'false'}"><svg viewBox="0 0 120 84" aria-hidden="true"><path d="M10 38 Q60 78 110 38 L94 67 Q60 80 26 67Z"/><path class="fold" d="M16 34 L${44+i*3} ${9+i*2} L50 49Z"/><path class="fold" d="M104 34 L${76-i*3} ${9+i*2} L70 49Z"/></svg><b>${n}</b><span>${i<3?'已放入':'可选'}</span></button>`).join('')}</div>
      <div class="personal-map" aria-live="polite"><svg viewBox="0 0 620 430" role="img" aria-label="个人舟印关系图"><path class="map-thread" d="M92 284 C180 72 344 88 522 210 C408 374 222 382 92 284Z"/><path class="map-thread secondary" d="M126 170 C264 246 358 72 510 136"/><g class="map-slot slot-0 is-filled" transform="translate(42 236)"><circle r="46"/><text>水面</text></g><g class="map-slot slot-1 is-filled" transform="translate(212 86)"><circle r="46"/><text>峰谷</text></g><g class="map-slot slot-2 is-filled" transform="translate(426 116)"><circle r="46"/><text>风向</text></g><g class="map-slot slot-3" transform="translate(520 258)"><circle r="46"/><text>叶脉</text></g><g class="map-slot slot-4" transform="translate(330 348)"><circle r="46"/><text>河谷</text></g><g class="map-slot slot-5" transform="translate(146 354)"><circle r="46"/><text>星空</text></g></svg><p><b data-imprint-count>3 枚舟印已形成一张完整的个人地图。</b><span>空白不是缺失；可继续、保存或直接归航。</span></p></div>
    </div>
  </section>`],

  ["每提升一级重新判断 BODY VALUE / LANDSCAPE COST / SITE NECESSITY / MAINTENANCE / SAFETY / FIELD DEPENDENCY。", `
  <section class="game-delta wearable-delta" aria-labelledby="wearable-title">
    <header class="delta-header"><div><span class="delta-kicker">067 / BODY CARRIERS</span><h3 id="wearable-title">同一舟核进入不同身体载体，功能不能靠年龄标签替代。</h3></div><span class="evidence-chip unknown">ERGONOMICS / MATERIAL TEST OPEN</span></header>
    <div class="carrier-grid">
      <article><svg viewBox="0 0 220 150" aria-hidden="true"><path d="M48 82 C48 26 172 26 172 82 C172 132 48 132 48 82Z"/><rect x="90" y="54" width="40" height="56" rx="14"/></svg><h4>长者｜手链</h4><p>大触点、低操作、回程识别和休息提醒。</p><ul><li>不宣称医疗监测</li><li>闭合力与皮肤接触待测</li></ul></article>
      <article><svg viewBox="0 0 220 150" aria-hidden="true"><path d="M38 80 C38 30 182 30 182 80 C182 128 38 128 38 80Z"/><path class="accent" d="M84 55 H136 V105 H84Z"/></svg><h4>青年｜手环</h4><p>承载可选舟印、夜间低照识别和个人地图入口。</p><ul><li>不成为路线通行凭证</li><li>光照与续航待校核</li></ul></article>
      <article><svg viewBox="0 0 220 150" aria-hidden="true"><path d="M104 22 H116 V130 H104Z"/><path class="accent" d="M110 22 L70 58 L110 72 L150 58Z"/><circle cx="110" cy="132" r="10"/></svg><h4>儿童｜魔法棒</h4><p>用于指向、提问和亲子协作，不驱动奔跑追逐。</p><ul><li>小零件与锐边禁用</li><li>握持与误用测试待做</li></ul></article>
      <article><svg viewBox="0 0 220 150" aria-hidden="true"><path d="M35 100 Q110 30 185 100 Q166 134 110 128 Q54 134 35 100Z"/><path class="accent" d="M62 98 Q110 60 158 98"/></svg><h4>颈枕 / 坐垫</h4><p>与既有栏杆倚靠及 Fluid Rest 的靠 / 坐关系协同。</p><ul><li>不新增孤立景观家具</li><li>清洁、阻燃、耐候待核</li></ul></article>
    </div><div class="claim-boundary"><b>草药、防蚊、解暑、照明</b><span>均为待验证功能方向；必须经过成分、过敏、儿童使用、照度和运营审查后才能进入实物。</span></div>
  </section>`],

  ["从风向、植物运动、温度、声音、雾、水面变化开始；禁止民族符号化、风铃景观化和巨大风动雕塑。", `
  <section class="game-delta butterfly-delta" aria-labelledby="butterfly-title">
    <header class="delta-header"><div><span class="delta-kicker">073 / QINGFENGYIN · WISH BUTTERFLY</span><h3 id="butterfly-title">装置只回应一次，然后把注意力还给风与清江。</h3></div><span class="evidence-chip unknown">CONCEPT / NTS / FIELD OPEN</span></header>
    <div class="butterfly-sequence">
      <article><span>01</span><svg viewBox="0 0 180 120" aria-hidden="true"><path d="M20 78 Q62 18 90 62 Q118 18 160 78 Q122 100 90 78 Q58 100 20 78Z"/><circle cx="90" cy="70" r="9"/></svg><b>观察完成</b><p>船核记录一次真实观察，不记录路线完成率。</p></article>
      <article><span>02</span><svg viewBox="0 0 180 120" aria-hidden="true"><path d="M24 82 Q58 26 88 62 Q122 26 156 82 Q120 90 90 76 Q60 90 24 82Z"/><path class="signal" d="M90 25 V51"/></svg><b>近场识别</b><p>无机械插槽优先；识别失败不阻断体验。</p></article>
      <article><span>03</span><svg viewBox="0 0 180 120" aria-hidden="true"><path class="active" d="M16 72 Q58 6 90 58 Q122 6 164 72 Q122 108 90 78 Q58 108 16 72Z"/><circle class="signal" cx="90" cy="68" r="20"/></svg><b>一次回应</b><p>暖光、轻响或局部摆动，持续时间由现场审查决定。</p></article>
      <article><span>04</span><svg viewBox="0 0 180 120" aria-hidden="true"><path d="M36 82 Q68 42 90 66 Q112 42 144 82 Q116 91 90 80 Q64 91 36 82Z"/><path class="signal dashed" d="M38 28 Q90 12 142 28"/></svg><b>撤回 / 冷却</b><p>停止闪烁与声音；回到植物、水面和自然风。</p></article>
    </div><div class="mechanism-note"><b>安全边界</b><span>夹伤、锐边、眩光、噪声、耐候、鸟虫干扰、维护开启与紧急关闭均待专业校核。</span><b>能源边界</b><span>风与步道发电只保留为待测路径，不宣称景区自供能。</span></div>
  </section>`],

  ["清江一线 / 清江雾气 / 清风吟 / 红花峰崽等延展必须按真实成熟度分层。", `
  <section class="game-delta card-delta" aria-labelledby="card-title">
    <header class="delta-header"><div><span class="delta-kicker">086 / CARD · CAMP EXCHANGE</span><h3 id="card-title">卡牌把观察带到营地，不把食物和安全变成游戏奖励。</h3></div><span class="evidence-chip inferred">PRINT / OPERATION PROTOTYPE</span></header>
    <div class="card-system">
      <div class="card-deck" aria-label="观察卡原型">
        <button class="observation-card card-water" data-flip-card type="button" aria-pressed="false"><span class="card-face card-front"><small>R06 · OBSERVATION</small><svg viewBox="0 0 180 110" aria-hidden="true"><path d="M10 54 Q90 104 170 54 L146 94 Q90 112 34 94Z"/><path class="fold" d="M18 50 L70 12 L76 70Z"/><path class="fold" d="M162 50 L110 12 L104 70Z"/></svg><b>河谷观察</b><em>比较两岸峰体与江面收放</em><i>点击翻面</i></span><span class="card-face card-back"><small>MY QINGJIANG NOTE</small><b>我在哪里停下？</b><span class="write-lines"></span><span class="source-line">来源提示 / 编号 / 离线入口</span><i>不计完成率</i></span></button>
        <button class="observation-card card-wind" data-flip-card type="button" aria-pressed="false"><span class="card-face card-front"><small>WIND · LISTEN</small><svg viewBox="0 0 180 110" aria-hidden="true"><path d="M16 58 Q70 18 164 48M30 80 Q104 42 158 72"/><circle cx="50" cy="36" r="8"/></svg><b>清风吟</b><em>从叶片、水面和声音判断风</em><i>点击翻面</i></span><span class="card-face card-back"><small>ONE RESPONSE ONLY</small><b>我听见什么？</b><span class="write-lines"></span><span class="source-line">装置回应 / 撤回 / 继续</span><i>能源路径待测</i></span></button>
        <div class="card-spec"><b>纸卡建议原型</b><span>63 × 88 mm</span><span>圆角与纸张克重由印刷打样确认</span><span>正式二维码不得承载唯一服务入口</span></div>
      </div>
      <div class="camp-exchange"><h4>营地交换台 / SERVICE BOUNDARY</h4><ol><li><b>出示任意观察卡</b><span>用于开启谈话或内容交换，不验证路线完成。</span></li><li><b>选择已定义内容</b><span>地方食材介绍、饮水补给或可选餐食；基础饮水和必要食物不设门槛。</span></li><li><b>魔盒交付</b><span>分格、密封、温控标识、过敏原提示和返还编号同时可读。</span></li><li><b>清洁返还</b><span>运营方记录库存、清洗、消毒与报废，不把责任交给游客。</span></li></ol><div class="food-box-diagram" aria-label="食物魔盒功能分区"><span class="box-hot">保温 / 待测</span><span class="box-cold">保冷 / 待测</span><span class="box-info">过敏原<br/>时间<br/>返还编号</span><span class="box-seal">密封边界</span></div></div>
    </div>
  </section>`],

  ["Open Register不是治理Dashboard；它要贴近具体图纸，告诉结构、景观、运营和施工专业下一步核什么。", `
  <section class="game-delta register-delta" aria-labelledby="register-title">
    <header class="delta-header"><div><span class="delta-kicker">094 / OBJECT-SPECIFIC OPEN REGISTER</span><h3 id="register-title">每个新物件都要知道下一次由谁、对什么做验证。</h3></div><span class="evidence-chip unknown">NO CONSTRUCTION CLAIM</span></header>
    <div class="register-table" role="table" aria-label="游戏线新物件开放项"><div class="register-row register-head" role="row"><b role="columnheader">对象</b><b role="columnheader">当前设计作用</b><b role="columnheader">必须验证</b><b role="columnheader">责任专业</b><b role="columnheader">状态</b></div><div class="register-row" role="row"><strong>船钥匙 / 舟印</strong><span>可逆形态与个人记忆载体</span><span>连接寿命、锐边、小零件、磁体、维修</span><span>产品 / 儿童安全 / 运营</span><em>OPEN</em></div><div class="register-row" role="row"><strong>愿蝶装置</strong><span>一次低强度环境回应</span><span>结构、夹伤、耐候、眩光、噪声、生态干扰</span><span>结构 / 电气 / 景观 / 生态</span><em>OPEN</em></div><div class="register-row" role="row"><strong>佩戴物 / 草药</strong><span>低操作识别与可选照护</span><span>皮肤接触、过敏、误用、成分批次、功效合规</span><span>材料 / 医药合规 / 儿童安全</span><em>OPEN</em></div><div class="register-row" role="row"><strong>食物魔盒</strong><span>营地交换与可返还容器</span><span>食品接触、温控、交叉污染、清洗消毒</span><span>食品安全 / 工业设计 / 运营</span><em>OPEN</em></div></div>
    <footer class="delta-foot"><span>FIELD OBSERVED=0</span><span>FIELD MEASURED=0</span><span>G1F HOLD</span><span>NTS / NOT FOR CONSTRUCTION</span></footer>
  </section>`]
];

for (const [anchor, panel] of panels) {
  if (!html.includes(anchor)) throw new Error(`Missing integration anchor: ${anchor}`);
  html = html.replace(anchor, `${anchor}${panel}`);
}

fs.writeFileSync(target, html);
console.log(`integrated ${panels.length} refined panels into ${target.pathname}`);
