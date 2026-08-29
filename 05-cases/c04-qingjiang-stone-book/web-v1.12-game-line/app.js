const sections=[...document.querySelectorAll('.section')];
const progress=document.querySelector('#progress');
const sectionNow=document.querySelector('#sectionNow');
const navLinks=[...document.querySelectorAll('.mainnav a')];

function syncPage(){
  const y=window.scrollY;
  const max=document.documentElement.scrollHeight-window.innerHeight;
  if(progress) progress.style.width=`${max?Math.min(100,(y/max)*100):0}%`;
  let best=sections[0];
  let distance=Infinity;
  for(const section of sections){
    const d=Math.abs(section.getBoundingClientRect().top-window.innerHeight*.24);
    if(d<distance){distance=d;best=section;}
  }
  if(!best) return;
  if(sectionNow) sectionNow.textContent=`${best.dataset.section} / ${String(sections.length).padStart(2,'0')}`;
  navLinks.forEach(link=>{
    const target=document.querySelector(link.getAttribute('href'));
    const active=target===best || (target && best.compareDocumentPosition(target)&Node.DOCUMENT_POSITION_PRECEDING && Math.abs(target.offsetTop-best.offsetTop)<window.innerHeight*1.6);
    link.classList.toggle('active',active);
  });
}

window.addEventListener('scroll',syncPage,{passive:true});
window.addEventListener('resize',syncPage);
syncPage();

document.addEventListener('keydown',event=>{
  if(!['PageDown','PageUp'].includes(event.key)) return;
  if(document.body.classList.contains('supplement-open')) return;
  event.preventDefault();
  const current=sections.reduce((best,section)=>Math.abs(section.getBoundingClientRect().top)<Math.abs(best.getBoundingClientRect().top)?section:best,sections[0]);
  const index=sections.indexOf(current);
  const next=event.key==='PageDown'?Math.min(sections.length-1,index+1):Math.max(0,index-1);
  sections[next]?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
});

const imprints=[...document.querySelectorAll('.imprint')];
const imprintStatus=document.querySelector('#imprintStatus');
function syncImprints(){
  const selected=imprints.filter(button=>button.classList.contains('active')).length;
  imprints.forEach(button=>button.setAttribute('aria-pressed',String(button.classList.contains('active'))));
  if(imprintStatus){
    imprintStatus.textContent=selected===0
      ?'没有选择任何内容也不会破坏游程；景观、路线与回程仍然完整。'
      :`当前留下 ${selected} 个阅读痕迹。它们组成这一次个人清江，不代表完成率。`;
  }
}
imprints.forEach(button=>button.addEventListener('click',()=>{button.classList.toggle('active');syncImprints();}));
syncImprints();

// Bottom-right supplemental material drawer. This is a secondary reading layer only;
// the 18-section main work remains the primary project narrative.
const supplementStyle=document.createElement('style');
supplementStyle.textContent=`
  .supplement-trigger{position:fixed;right:24px;bottom:24px;z-index:1400;display:flex;align-items:center;gap:12px;min-width:152px;padding:12px 14px;border:1px solid rgba(18,29,27,.18);background:rgba(249,248,244,.94);color:#17201e;box-shadow:0 14px 42px rgba(18,28,26,.14);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);font:inherit;text-align:left;cursor:pointer;transition:transform .24s ease,box-shadow .24s ease,background .24s ease}
  .supplement-trigger:hover{transform:translateY(-2px);box-shadow:0 18px 48px rgba(18,28,26,.18);background:#fff}
  .supplement-trigger-mark{display:grid;place-items:center;width:32px;height:32px;border-radius:50%;background:#173c37;color:#eef4ef;font-size:17px;line-height:1}
  .supplement-trigger-copy{display:grid;gap:1px}.supplement-trigger-copy b{font-size:13px;font-weight:650;letter-spacing:.04em}.supplement-trigger-copy span{font-size:9px;letter-spacing:.13em;opacity:.56}
  .supplement-backdrop{position:fixed;inset:0;z-index:1390;background:rgba(7,14,13,.16);opacity:0;pointer-events:none;transition:opacity .25s ease}
  .supplement-panel{position:fixed;right:24px;bottom:82px;z-index:1395;width:min(590px,calc(100vw - 48px));height:min(78vh,790px);display:grid;grid-template-rows:auto auto minmax(0,1fr);overflow:hidden;border:1px solid rgba(18,29,27,.13);background:rgba(249,248,244,.985);box-shadow:0 30px 90px rgba(11,23,21,.24);transform:translateY(18px) scale(.985);transform-origin:100% 100%;opacity:0;pointer-events:none;transition:opacity .24s ease,transform .3s cubic-bezier(.2,.72,.2,1)}
  .supplement-open .supplement-backdrop{opacity:1;pointer-events:auto}.supplement-open .supplement-panel{opacity:1;transform:none;pointer-events:auto}.supplement-open .supplement-trigger{background:#173c37;color:#f4f6f0;border-color:#173c37}.supplement-open .supplement-trigger-mark{background:#f4f6f0;color:#173c37}
  .supplement-head{display:flex;justify-content:space-between;gap:20px;padding:22px 22px 16px;border-bottom:1px solid rgba(18,29,27,.08)}
  .supplement-head .eyebrow{margin:0 0 6px;font-size:9px;letter-spacing:.16em;opacity:.48}.supplement-head h3{margin:0;font-size:24px;line-height:1.08;font-weight:580;letter-spacing:-.02em}.supplement-head p{margin:7px 0 0;max-width:400px;font-size:12px;line-height:1.55;opacity:.62}
  .supplement-close{align-self:flex-start;width:34px;height:34px;border:1px solid rgba(18,29,27,.12);border-radius:50%;background:transparent;color:inherit;font:inherit;font-size:20px;line-height:1;cursor:pointer}
  .supplement-tabs{display:flex;gap:6px;padding:10px 12px;overflow-x:auto;border-bottom:1px solid rgba(18,29,27,.08);scrollbar-width:none}.supplement-tabs::-webkit-scrollbar{display:none}
  .supplement-tabs button{flex:0 0 auto;padding:7px 10px;border:0;border-radius:999px;background:transparent;color:inherit;font:inherit;font-size:11px;white-space:nowrap;cursor:pointer;opacity:.58}.supplement-tabs button.is-active{background:#173c37;color:#f4f6f0;opacity:1}
  .supplement-body{overflow:auto;padding:20px 22px 26px;overscroll-behavior:contain}.supplement-panel-section{display:none;animation:supplementFade .22s ease}.supplement-panel-section.is-active{display:block}@keyframes supplementFade{from{opacity:.25;transform:translateY(5px)}to{opacity:1;transform:none}}
  .supplement-section-head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:16px}.supplement-section-head p{margin:0;font-size:9px;letter-spacing:.15em;opacity:.46}.supplement-section-head h4{margin:3px 0 0;font-size:21px;line-height:1.16;font-weight:580}.supplement-jump{font-size:10px;color:inherit;text-decoration:none;border-bottom:1px solid rgba(18,29,27,.3);white-space:nowrap}
  .supplement-asset-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px}.supplement-asset{margin:0;min-width:0;border:1px solid rgba(18,29,27,.09);background:#fff}.supplement-asset img{display:block;width:100%;height:126px;object-fit:cover;background:#eef0eb}.supplement-asset img.contain{object-fit:contain;padding:10px}.supplement-asset figcaption{display:grid;gap:2px;padding:9px 10px 11px}.supplement-asset figcaption b{font-size:11px;font-weight:650}.supplement-asset figcaption span{font-size:10px;line-height:1.45;opacity:.58}
  .supplement-card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.supplement-card{min-height:142px;padding:15px;border:1px solid rgba(18,29,27,.1);background:#fff}.supplement-card em{display:block;margin-bottom:18px;font-size:9px;font-style:normal;letter-spacing:.15em;opacity:.42}.supplement-card b{display:block;margin-bottom:7px;font-size:16px;font-weight:580}.supplement-card p{margin:0;font-size:11px;line-height:1.6;opacity:.63}
  .supplement-principles{display:grid;gap:8px;counter-reset:sprinciple}.supplement-principle{display:grid;grid-template-columns:42px 1fr;gap:12px;padding:13px 14px;border-top:1px solid rgba(18,29,27,.12)}.supplement-principle:before{counter-increment:sprinciple;content:'0' counter(sprinciple);font-size:10px;letter-spacing:.12em;opacity:.4}.supplement-principle b{display:block;margin-bottom:3px;font-size:13px}.supplement-principle span{display:block;font-size:11px;line-height:1.55;opacity:.6}
  .supplement-route{display:grid;grid-template-columns:repeat(6,1fr);gap:5px;align-items:stretch}.supplement-route article{position:relative;min-width:0;padding:12px 8px 11px;border:1px solid rgba(18,29,27,.1);background:#fff}.supplement-route article:not(:last-child):after{content:'→';position:absolute;right:-7px;top:50%;z-index:2;transform:translateY(-50%);font-size:10px;opacity:.45}.supplement-route small{display:block;font-size:8px;letter-spacing:.1em;opacity:.4}.supplement-route b{display:block;margin:9px 0 5px;font-size:11px}.supplement-route span{display:block;font-size:9px;line-height:1.45;opacity:.58}
  .supplement-flow{display:grid;grid-template-columns:1fr 1fr;gap:7px}.supplement-flow article{display:grid;grid-template-columns:30px 1fr;gap:10px;padding:12px;border:1px solid rgba(18,29,27,.09);background:#fff}.supplement-flow article>span{font-size:9px;letter-spacing:.1em;opacity:.4}.supplement-flow b{display:block;margin-bottom:3px;font-size:12px}.supplement-flow p{margin:0;font-size:10px;line-height:1.5;opacity:.59}
  .supplement-split{display:grid;grid-template-columns:1fr 1fr;gap:10px}.supplement-split>article{padding:15px;border:1px solid rgba(18,29,27,.1);background:#fff}.supplement-split h5{margin:0 0 10px;font-size:15px}.supplement-split ul{margin:0;padding:0;list-style:none;display:grid;gap:8px}.supplement-split li{position:relative;padding-left:13px;font-size:10.5px;line-height:1.52;opacity:.7}.supplement-split li:before{content:'•';position:absolute;left:0}
  .supplement-ai3d{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.supplement-process-card{overflow:hidden;border:1px solid rgba(18,29,27,.1);background:#fff}.supplement-process-card img{display:block;width:100%;height:104px;object-fit:cover;background:#eef0eb}.supplement-process-card img.contain{object-fit:contain;padding:8px}.supplement-process-card div{padding:10px}.supplement-process-card small{font-size:8px;letter-spacing:.1em;opacity:.4}.supplement-process-card b{display:block;margin:5px 0 4px;font-size:11px}.supplement-process-card p{margin:0;font-size:9px;line-height:1.48;opacity:.58}.supplement-boundary{margin:12px 0 0;padding:12px 13px;border-left:2px solid #173c37;background:rgba(23,60,55,.045);font-size:10px;line-height:1.62;color:rgba(18,29,27,.7)}
  @media(max-width:760px){.supplement-trigger{right:14px;bottom:14px;min-width:0}.supplement-trigger-copy span{display:none}.supplement-panel{right:0;bottom:0;width:100%;height:min(84vh,780px);border-left:0;border-right:0;border-bottom:0;transform:translateY(22px);transform-origin:50% 100%}.supplement-head{padding:18px 16px 13px}.supplement-tabs{padding-inline:10px}.supplement-body{padding:16px}.supplement-card-grid{grid-template-columns:1fr}.supplement-route{grid-template-columns:1fr 1fr}.supplement-route article:not(:last-child):after{display:none}.supplement-ai3d{grid-template-columns:1fr 1fr}.supplement-asset img{height:110px}}
  @media(max-width:480px){.supplement-asset-grid,.supplement-flow,.supplement-split,.supplement-ai3d{grid-template-columns:1fr}.supplement-asset img,.supplement-process-card img{height:136px}}
  @media(prefers-reduced-motion:reduce){.supplement-trigger,.supplement-backdrop,.supplement-panel,.supplement-panel-section{transition:none!important;animation:none!important}}
`;
document.head.appendChild(supplementStyle);

const supplementMarkup=`
  <div class="supplement-backdrop" data-supplement-close aria-hidden="true"></div>
  <button class="supplement-trigger" id="supplementTrigger" type="button" aria-expanded="false" aria-controls="supplementPanel">
    <span class="supplement-trigger-mark">＋</span>
    <span class="supplement-trigger-copy"><b>补充资料</b><span>SUPPLEMENT</span></span>
  </button>
  <aside class="supplement-panel" id="supplementPanel" aria-hidden="true" aria-label="清江石书补充资料">
    <header class="supplement-head">
      <div><p class="eyebrow">SUPPLEMENT / PROCESS & PROOF</p><h3>作品之外，再读一层。</h3><p>这里补充原资产、创意生成、技术路线和制作过程；不改变主页面的作品阅读顺序。</p></div>
      <button class="supplement-close" type="button" data-supplement-close aria-label="关闭补充资料">×</button>
    </header>
    <nav class="supplement-tabs" aria-label="补充资料分类">
      <button type="button" class="is-active" data-supplement-tab="assets">原资产</button>
      <button type="button" data-supplement-tab="idea">设计创意</button>
      <button type="button" data-supplement-tab="thinking">设计思路</button>
      <button type="button" data-supplement-tab="tech">技术路线</button>
      <button type="button" data-supplement-tab="workflow">任务流程</button>
      <button type="button" data-supplement-tab="innovation">创新 / 难点</button>
      <button type="button" data-supplement-tab="ai3d">AI + 3D</button>
    </nav>
    <div class="supplement-body">
      <section class="supplement-panel-section is-active" data-supplement-panel="assets">
        <div class="supplement-section-head"><div><p>01 / ORIGINAL MATERIAL</p><h4>先看原资产，再看设计如何发生。</h4></div><a class="supplement-jump" href="#assets" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-asset-grid">
          <figure class="supplement-asset"><img src="assets/hero_qingjiang.jpg" alt="清江景观原资产"><figcaption><b>真实清江</b><span>景观是第一阅读，不由模型或界面代替。</span></figcaption></figure>
          <figure class="supplement-asset"><img class="contain" src="assets/route03_locked_current.svg" alt="清江路线关系资产"><figcaption><b>路线关系</b><span>分支、回环、跨江与回程决定体验底板。</span></figcaption></figure>
          <figure class="supplement-asset"><img src="assets/r06_qingjiang.jpg" alt="河谷停留场景"><figcaption><b>停留场景</b><span>开阔河谷支持观察、比较与可选深读。</span></figcaption></figure>
          <figure class="supplement-asset"><img src="assets/r13_passage_sequence.png" alt="峡缝通过序列"><figcaption><b>通过场景</b><span>空间压缩时内容退场，身体与方向优先。</span></figcaption></figure>
          <figure class="supplement-asset"><img class="contain" src="assets/app_mybook.png" alt="数字记忆界面"><figcaption><b>数字资产</b><span>记录选择过的内容，而不是制造完成率。</span></figcaption></figure>
          <figure class="supplement-asset"><img class="contain" src="assets/r06_general_assembly_v11.svg" alt="技术装配资产"><figcaption><b>技术资产</b><span>装配与节点负责解释设计怎样成立。</span></figcaption></figure>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="idea">
        <div class="supplement-section-head"><div><p>02 / DESIGN IDEA</p><h4>创意不来自“再造景点”，而来自重新观看。</h4></div><a class="supplement-jump" href="#idea" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-card-grid">
          <article class="supplement-card"><em>WATER</em><b>水上看整体</b><p>沿江移动把峰林、两岸和河谷连续地读成一个整体。</p></article>
          <article class="supplement-card"><em>AIR</em><b>空中看关系</b><p>索道抬高视点，把江、岸、峰和跨江关系同时打开。</p></article>
          <article class="supplement-card"><em>BODY</em><b>山中看细节</b><p>步行降低速度，让身体、局部发现、停留和恢复成为设计尺度。</p></article>
        </div>
        <p class="supplement-boundary">核心创意：不是把清江包装成新的主题景区，而是让同一条真实清江在不同移动尺度中被重新认识。</p>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="thinking">
        <div class="supplement-section-head"><div><p>03 / DESIGN THINKING</p><h4>控制“什么时候出现”，比增加更多内容重要。</h4></div><a class="supplement-jump" href="#thinking" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-principles">
          <article class="supplement-principle"><div><b>景观先出现</b><span>第一眼先建立真实空间，不让说明覆盖现场。</span></div></article>
          <article class="supplement-principle"><div><b>路线拥有主权</b><span>内容可以跳过和改序，真实游程不能被十三个任务点重画。</span></div></article>
          <article class="supplement-principle"><div><b>场景决定信息密度</b><span>开阔处允许比较与深读，压缩处主动关闭玩法与解释。</span></div></article>
          <article class="supplement-principle"><div><b>Return 贯穿全程</b><span>方向、恢复、无手机和退出路径不是结尾功能，而是基础体验。</span></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="tech">
        <div class="supplement-section-head"><div><p>04 / TECHNOLOGY APPLICATION ROUTE</p><h4>不同技术承担不同证据角色。</h4></div><a class="supplement-jump" href="#technology" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-route">
          <article><small>01</small><b>Source</b><span>地图、影像、资料</span></article>
          <article><small>02</small><b>Relation</b><span>路线与空间关系</span></article>
          <article><small>03</small><b>Scene</b><span>观看与身体任务</span></article>
          <article><small>04</small><b>3D / Drawing</b><span>尺度与几何校核</span></article>
          <article><small>05</small><b>Prototype</b><span>交互与状态验证</span></article>
          <article><small>06</small><b>Web / Motion</b><span>统一体验表达</span></article>
        </div>
        <p class="supplement-boundary">技术路线不是“工具列表”。地图负责关系，AI负责探索，3D负责尺度与几何，图纸负责构造，原型负责行为，Web负责把这些角色重新编成一条可读的作品线。</p>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="workflow">
        <div class="supplement-section-head"><div><p>05 / TASK FLOW</p><h4>每一步都改变下一步设计判断。</h4></div><a class="supplement-jump" href="#workflow" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-flow">
          <article><span>01</span><div><b>读取原资产</b><p>场地、路线、文化和既有设计资料。</p></div></article>
          <article><span>02</span><div><b>提炼空间问题</b><p>分支、观看尺度、身体压力与回程。</p></div></article>
          <article><span>03</span><div><b>形成设计命题</b><p>把发现转成介入与内容深度判断。</p></div></article>
          <article><span>04</span><div><b>并行创意探索</b><p>路线、十三印、App、实体、品牌与记忆。</p></div></article>
          <article><span>05</span><div><b>放回真实场景</b><p>检查注意力、身体、服务和退出。</p></div></article>
          <article><span>06</span><div><b>原型与 3D</b><p>验证交互、人体尺度和空间关系。</p></div></article>
          <article><span>07</span><div><b>技术深化</b><p>连接、材料、排水、防滑和维护。</p></div></article>
          <article><span>08</span><div><b>作品整合</b><p>把成果组织成主阅读与补充阅读。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="innovation">
        <div class="supplement-section-head"><div><p>06 / INNOVATION & DIFFICULTIES</p><h4>创新成立的地方，也正是技术难点所在。</h4></div><a class="supplement-jump" href="#innovation" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-split">
          <article><h5>创新点</h5><ul>
            <li>把游船、索道、步行重新定义成三种观看尺度，而不是三段接驳。</li>
            <li>十三印采用可选阅读，不以 13/13 完成度组织体验。</li>
            <li>把“信息设计”进一步改写成“注意力设计”，让系统知道何时退场。</li>
            <li>数字、实体、品牌和记忆都服务于真实游程，而不是竞争主角位置。</li>
            <li>无手机、弱网和退出路径仍能保持完整旅行。</li>
          </ul></article>
          <article><h5>技术难点</h5><ul>
            <li>保持真实路线关系，同时让探索和游戏感成立。</li>
            <li>不同场景需要不同信息密度，不能套用同一 UI 或装置模板。</li>
            <li>地图、3D、剖面、轴测和网页必须共享同一空间事实。</li>
            <li>AI 概念探索容易生成不存在的地貌、平台、栏杆或构造，需要持续回读。</li>
            <li>户外实物还要面对湿热、排水、防滑、连接、维护与替换。</li>
          </ul></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="ai3d">
        <div class="supplement-section-head"><div><p>07 / AI + 3D CREATION PROCESS</p><h4>AI 用来探索，3D 与图纸把设计拉回可核验关系。</h4></div><a class="supplement-jump" href="#ai3d" data-supplement-jump>进入主章节 ↗</a></div>
        <div class="supplement-ai3d">
          <article class="supplement-process-card"><img src="assets/hero_qingjiang.jpg" alt="真实清江来源"><div><small>01 / SOURCE</small><b>真实来源与约束</b><p>从景观、路线和已有对象出发，不从空白画面开始。</p></div></article>
          <article class="supplement-process-card"><img src="assets/r06_qingjiang.jpg" alt="体验方向探索基础"><div><small>02 / AI EXPLORE</small><b>体验方向探索</b><p>AI 只承担氛围、构图、镜头和体验方向的候选探索。</p></div></article>
          <article class="supplement-process-card"><img class="contain" src="assets/technical_focus_v2.svg" alt="空间关系回读"><div><small>03 / READBACK</small><b>几何冲突回读</b><p>检查新增地形、平台、栏杆、路径和尺度错位。</p></div></article>
          <article class="supplement-process-card"><img class="contain" src="assets/fluid_v26_body_posture.png" alt="人体尺度校核"><div><small>04 / 3D</small><b>3D 与人体尺度</b><p>把空间关系、使用姿态和对象尺度重新落回几何。</p></div></article>
          <article class="supplement-process-card"><img class="contain" src="assets/r06_general_assembly_v11.svg" alt="总体装配图"><div><small>05 / DRAWING</small><b>平剖与装配</b><p>用平面、剖面和装配图解释“怎样成立”。</p></div></article>
          <article class="supplement-process-card"><img class="contain" src="assets/r06_detail_atlas_v11.svg" alt="技术节点详图"><div><small>06 / DETAIL</small><b>节点与维护</b><p>连接、材料、排水、防滑和替换继续深化。</p></div></article>
        </div>
        <p class="supplement-boundary">AI 图像不证明最终几何、现场事实、工程尺寸或结构安全。任何进入主展示的 AI / 3D 候选，都必须回到原资产和技术关系检查。</p>
      </section>
    </div>
  </aside>`;
document.body.insertAdjacentHTML('beforeend',supplementMarkup);

const supplementTrigger=document.querySelector('#supplementTrigger');
const supplementPanel=document.querySelector('#supplementPanel');
const supplementTabs=[...document.querySelectorAll('[data-supplement-tab]')];
const supplementPanels=[...document.querySelectorAll('[data-supplement-panel]')];
const supplementClosers=[...document.querySelectorAll('[data-supplement-close]')];

function openSupplement(){
  document.body.classList.add('supplement-open');
  supplementTrigger?.setAttribute('aria-expanded','true');
  supplementPanel?.setAttribute('aria-hidden','false');
}
function closeSupplement(){
  document.body.classList.remove('supplement-open');
  supplementTrigger?.setAttribute('aria-expanded','false');
  supplementPanel?.setAttribute('aria-hidden','true');
}
function selectSupplementTab(name){
  supplementTabs.forEach(button=>button.classList.toggle('is-active',button.dataset.supplementTab===name));
  supplementPanels.forEach(panel=>panel.classList.toggle('is-active',panel.dataset.supplementPanel===name));
}

supplementTrigger?.addEventListener('click',()=>document.body.classList.contains('supplement-open')?closeSupplement():openSupplement());
supplementClosers.forEach(button=>button.addEventListener('click',closeSupplement));
supplementTabs.forEach(button=>button.addEventListener('click',()=>selectSupplementTab(button.dataset.supplementTab)));
document.querySelectorAll('[data-supplement-jump]').forEach(link=>link.addEventListener('click',closeSupplement));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&document.body.classList.contains('supplement-open')) closeSupplement();});
