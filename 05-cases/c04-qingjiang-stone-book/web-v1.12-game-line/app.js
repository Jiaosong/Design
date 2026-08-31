const sections=[...document.querySelectorAll('.section')];
const progress=document.querySelector('#progress');
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

  navLinks.forEach(link=>{
    const target=document.querySelector(link.getAttribute('href'));
    if(!target){link.classList.remove('active');return;}
    const active=target===best || (best.offsetTop>=target.offsetTop && best.offsetTop-target.offsetTop<window.innerHeight*1.15);
    link.classList.toggle('active',active);
  });
}

window.addEventListener('scroll',syncPage,{passive:true});
window.addEventListener('resize',syncPage);
syncPage();

document.addEventListener('keydown',event=>{
  if(!['PageDown','PageUp'].includes(event.key)) return;
  if(document.body.classList.contains('supplement-open')) return;
  const current=sections.reduce((best,section)=>Math.abs(section.getBoundingClientRect().top)<Math.abs(best.getBoundingClientRect().top)?section:best,sections[0]);
  if(!current) return;
  event.preventDefault();
  const index=sections.indexOf(current);
  const next=event.key==='PageDown'?Math.min(sections.length-1,index+1):Math.max(0,index-1);
  sections[next]?.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
});

const imprints=[...document.querySelectorAll('.imprint')];
const imprintStatus=document.querySelector('#imprintStatus');
function syncImprints(){
  const selected=imprints.filter(button=>button.classList.contains('active')).length;
  imprints.forEach(button=>button.setAttribute('aria-pressed',String(button.classList.contains('active'))));
  if(!imprintStatus) return;
  imprintStatus.textContent=selected===0
    ?'没有选择任何内容也不会破坏游程；景观、路线与回程仍然完整。'
    :`当前留下 ${selected} 个阅读痕迹。它们组成这一次个人清江，不代表完成率。`;
}
imprints.forEach(button=>button.addEventListener('click',()=>{button.classList.toggle('active');syncImprints();}));
syncImprints();

const supplementStyle=document.createElement('style');
supplementStyle.textContent=`
  .supplement-trigger{position:fixed;right:24px;bottom:24px;z-index:1400;display:flex;align-items:center;gap:11px;padding:11px 14px;border:1px solid rgba(18,29,27,.16);background:rgba(249,248,244,.94);color:#17201e;box-shadow:0 14px 42px rgba(18,28,26,.14);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);font:inherit;cursor:pointer;transition:transform .24s ease,box-shadow .24s ease,background .24s ease}
  .supplement-trigger:hover{transform:translateY(-2px);box-shadow:0 18px 48px rgba(18,28,26,.18);background:#fff}
  .supplement-trigger-mark{display:grid;place-items:center;width:30px;height:30px;border-radius:50%;background:#173c37;color:#eef4ef;font-size:16px;line-height:1}
  .supplement-trigger-copy{display:grid;gap:1px;text-align:left}.supplement-trigger-copy b{font-size:12px;font-weight:650;letter-spacing:.04em}.supplement-trigger-copy span{font-size:8px;letter-spacing:.14em;opacity:.55}
  .supplement-backdrop{position:fixed;inset:0;z-index:1390;background:rgba(7,14,13,.18);opacity:0;pointer-events:none;transition:opacity .24s ease}
  .supplement-panel{position:fixed;right:24px;bottom:80px;z-index:1395;width:min(620px,calc(100vw - 48px));height:min(78vh,820px);display:grid;grid-template-rows:auto auto minmax(0,1fr);overflow:hidden;border:1px solid rgba(18,29,27,.12);background:rgba(249,248,244,.985);box-shadow:0 30px 90px rgba(11,23,21,.24);transform:translateY(18px) scale(.985);transform-origin:100% 100%;opacity:0;pointer-events:none;transition:opacity .24s ease,transform .3s cubic-bezier(.2,.72,.2,1)}
  .supplement-open .supplement-backdrop{opacity:1;pointer-events:auto}.supplement-open .supplement-panel{opacity:1;transform:none;pointer-events:auto}.supplement-open .supplement-trigger{background:#173c37;color:#f4f6f0;border-color:#173c37}.supplement-open .supplement-trigger-mark{background:#f4f6f0;color:#173c37}
  .supplement-head{display:flex;justify-content:space-between;gap:20px;padding:22px 22px 16px;border-bottom:1px solid rgba(18,29,27,.08)}
  .supplement-head .eyebrow{margin:0 0 6px;font-size:9px;letter-spacing:.16em;opacity:.48}.supplement-head h3{margin:0;font-size:24px;line-height:1.08;font-weight:580;letter-spacing:-.02em}.supplement-head p{margin:7px 0 0;max-width:430px;font-size:12px;line-height:1.55;opacity:.62}
  .supplement-close{align-self:flex-start;width:34px;height:34px;border:1px solid rgba(18,29,27,.12);border-radius:50%;background:transparent;color:inherit;font:inherit;font-size:20px;line-height:1;cursor:pointer}
  .supplement-tabs{display:flex;gap:5px;padding:10px 12px;overflow-x:auto;border-bottom:1px solid rgba(18,29,27,.08);scrollbar-width:none}.supplement-tabs::-webkit-scrollbar{display:none}
  .supplement-tabs button{flex:0 0 auto;padding:7px 10px;border:0;border-radius:999px;background:transparent;color:inherit;font:inherit;font-size:11px;white-space:nowrap;cursor:pointer;opacity:.56}.supplement-tabs button.is-active{background:#173c37;color:#f4f6f0;opacity:1}
  .supplement-body{overflow:auto;padding:20px 22px 26px;overscroll-behavior:contain}.supplement-panel-section{display:none}.supplement-panel-section.is-active{display:block}
  .supplement-section-head{display:flex;align-items:end;justify-content:space-between;gap:18px;margin-bottom:16px}.supplement-section-head p{margin:0;font-size:9px;letter-spacing:.15em;opacity:.46}.supplement-section-head h4{margin:3px 0 0;font-size:22px;line-height:1.16;font-weight:580}.supplement-jump{font-size:10px;color:inherit;text-decoration:none;border-bottom:1px solid rgba(18,29,27,.3);white-space:nowrap}
  .supplement-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.supplement-card{overflow:hidden;border:1px solid rgba(18,29,27,.09);background:#fff}.supplement-card img{display:block;width:100%;height:150px;object-fit:cover;background:#eef0eb}.supplement-card img.contain{object-fit:contain;padding:12px}.supplement-card div{padding:12px}.supplement-card small{display:block;margin-bottom:5px;font-size:8px;letter-spacing:.12em;opacity:.42}.supplement-card b{display:block;margin-bottom:5px;font-size:13px;font-weight:650}.supplement-card p{margin:0;font-size:10.5px;line-height:1.55;opacity:.62}
  .supplement-list{display:grid;gap:0;border-top:1px solid rgba(18,29,27,.1)}.supplement-list article{display:grid;grid-template-columns:34px 1fr;gap:12px;padding:13px 2px;border-bottom:1px solid rgba(18,29,27,.1)}.supplement-list span{font-size:9px;letter-spacing:.12em;opacity:.4}.supplement-list b{display:block;margin-bottom:3px;font-size:12px}.supplement-list p{margin:0;font-size:10.5px;line-height:1.55;opacity:.62}
  .supplement-boundary{margin:14px 0 0;padding:13px 14px;border-left:2px solid #173c37;background:rgba(23,60,55,.045);font-size:10.5px;line-height:1.65;color:rgba(18,29,27,.7)}
  @media(max-width:760px){.supplement-trigger{right:14px;bottom:14px}.supplement-trigger-copy span{display:none}.supplement-panel{right:0;bottom:0;width:100%;height:min(84vh,800px);border-left:0;border-right:0;border-bottom:0;transform:translateY(22px);transform-origin:50% 100%}.supplement-head{padding:18px 16px 13px}.supplement-tabs{padding-inline:10px}.supplement-body{padding:16px}.supplement-grid{grid-template-columns:1fr}}
  @media(prefers-reduced-motion: reduce){.supplement-trigger,.supplement-backdrop,.supplement-panel{transition:none!important}}
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
      <div><p class="eyebrow">SUPPLEMENT / SOURCE / PROCESS</p><h3>需要时，再往里读一层。</h3><p>主页面只保留清江、游程和设计对象。来源、过程、技术深化与未完成边界集中放在这里。</p></div>
      <button class="supplement-close" type="button" data-supplement-close aria-label="关闭补充资料">×</button>
    </header>
    <nav class="supplement-tabs" aria-label="补充资料分类">
      <button type="button" class="is-active" data-supplement-tab="source">原资产</button>
      <button type="button" data-supplement-tab="logic">设计逻辑</button>
      <button type="button" data-supplement-tab="technical">技术与任务</button>
      <button type="button" data-supplement-tab="digital">数字系统</button>
      <button type="button" data-supplement-tab="identity">品牌与记忆</button>
      <button type="button" data-supplement-tab="ai3d">AI + 3D</button>
      <button type="button" data-supplement-tab="boundary">演进与边界</button>
    </nav>
    <div class="supplement-body">
      <section class="supplement-panel-section is-active" data-supplement-panel="source">
        <div class="supplement-section-head"><div><p>01 / SOURCE</p><h4>先确认清江本身。</h4></div><a class="supplement-jump" href="#assets" data-supplement-jump>回到清江 ↗</a></div>
        <div class="supplement-grid">
          <article class="supplement-card"><img src="https://www.eslygroup.com/uploadfile/image/20230718/v0ii0wjlhe.jpg" alt="清江与跨江索道"><div><small>LANDSCAPE</small><b>真实清江</b><p>主视觉优先使用真实场地影像，模型和界面不替代景观证据。</p></div></article>
          <article class="supplement-card"><img class="contain" src="assets/route03_locked_current.svg" alt="清江路线关系"><div><small>ROUTE</small><b>路线与回程</b><p>分支、回环、跨江和回程共同构成体验骨架。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="logic">
        <div class="supplement-section-head"><div><p>02 / DESIGN LOGIC</p><h4>景观先行，解释后置。</h4></div><a class="supplement-jump" href="#thinking" data-supplement-jump>看场景逻辑 ↗</a></div>
        <div class="supplement-grid">
          <article class="supplement-card"><img class="contain" src="assets/r06_attention_sequence_current.svg" alt="R06 注意力序列"><div><small>R06</small><b>开阔时可以多读一点</b><p>完整景观先成立，再进入比较与关系揭示，最后主动退场。</p></div></article>
          <article class="supplement-card"><img class="contain" src="assets/r13_passage_sequence_current.svg" alt="R13 收束通过序列"><div><small>R13 / REMOTE CONCEPT</small><b>收束时让内容退后</b><p>接近、进入、通过、回看使用不同信息强度；该图只说明体验逻辑。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="technical">
        <div class="supplement-section-head"><div><p>03 / TECHNICAL</p><h4>从身体需求进入空间细节。</h4></div><a class="supplement-jump" href="#technical" data-supplement-jump>看空间与细节 ↗</a></div>
        <div class="supplement-grid">
          <article class="supplement-card"><img class="contain" src="assets/body_need_scenarios_current.svg" alt="身体需求场景"><div><small>BODY</small><b>先判断是否需要介入</b><p>不介入、身体支持、轻反馈、空间介入按真实需求逐级增加。</p></div></article>
          <article class="supplement-card"><img class="contain" src="assets/r06_technical_relation_current.svg" alt="R06 技术关系"><div><small>DETAIL</small><b>使用、排水、连接、维护</b><p>技术图只表达当前能够诚实说明的关系，不补写未知尺寸与结构规格。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="digital">
        <div class="supplement-section-head"><div><p>04 / DIGITAL</p><h4>数字只在需要时出现。</h4></div><a class="supplement-jump" href="#digital" data-supplement-jump>看数字陪伴 ↗</a></div>
        <div class="supplement-list">
          <article><span>01</span><div><b>定向</b><p>先回答怎么走、怎么回，而不是展示内容数量。</p></div></article>
          <article><span>02</span><div><b>可选阅读</b><p>提示、关系、深读都可以跳过，少读不影响游程成立。</p></div></article>
          <article><span>03</span><div><b>主动退场</b><p>景观或身体注意更强时，数字界面降低存在感。</p></div></article>
          <article><span>04</span><div><b>无手机仍成立</b><p>纸图、标识、人工服务和纸本记忆保留完整替代路径。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="identity">
        <div class="supplement-section-head"><div><p>05 / IDENTITY & MEMORY</p><h4>识别留下痕迹，记忆允许留白。</h4></div><a class="supplement-jump" href="#brandmemory" data-supplement-jump>看识别系统 ↗</a></div>
        <div class="supplement-grid">
          <article class="supplement-card"><img class="contain" src="assets/brand_system_current.svg" alt="清江品牌识别系统"><div><small>IDENTITY</small><b>线、印、页、痕迹</b><p>识别跟随路线与保存动作出现，不覆盖真实山水。</p></div></article>
          <article class="supplement-card"><img class="contain" src="assets/memory_journal_current.svg" alt="清江纸本记忆"><div><small>MEMORY</small><b>只保存真正发生的部分</b><p>路线、照片、一句话与空白共同组成个人版本的清江。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="ai3d">
        <div class="supplement-section-head"><div><p>06 / AI + 3D</p><h4>探索可以开放，事实必须收紧。</h4></div></div>
        <div class="supplement-list">
          <article><span>01</span><div><b>真实来源与限制</b><p>先确定场地、路线、已有资产和不能被改写的边界。</p></div></article>
          <article><span>02</span><div><b>概念探索</b><p>AI只用于氛围、构图和体验方向探索，不作为尺寸或结构依据。</p></div></article>
          <article><span>03</span><div><b>几何回读</b><p>把概念重新落回可检查的空间关系、截面和身体尺度。</p></div></article>
          <article><span>04</span><div><b>3D关系</b><p>模型用于看清空间层级、路径和身体关系，而不是替代清江主视觉。</p></div></article>
          <article><span>05</span><div><b>平面 / 剖面 / 组装</b><p>用图纸和节点解释如何成立，弱表达需要重画而不是靠渲染遮蔽。</p></div></article>
          <article><span>06</span><div><b>材料 / 维护</b><p>进入触面、排水、连接和维护动作，再决定下一轮专业验证内容。</p></div></article>
        </div>
      </section>

      <section class="supplement-panel-section" data-supplement-panel="boundary">
        <div class="supplement-section-head"><div><p>07 / EVOLUTION & BOUNDARY</p><h4>保留判断，不把过程变成主角。</h4></div></div>
        <div class="supplement-list">
          <article><span>A</span><div><b>真实景观优先于模型英雄图</b><p>模型承担空间证明；真实清江承担第一视觉阅读。</p></div></article>
          <article><span>B</span><div><b>十三印从“关卡”退回可选阅读</b><p>任何一印都可以跳过、改序或关闭，不形成完成率压力。</p></div></article>
          <article><span>C</span><div><b>技术内容回到具体对象旁边</b><p>不再把技术路线、创新点和难点作为等权主章节。</p></div></article>
        </div>
        <p class="supplement-boundary">远程研究不等同现场测量；R13 当前仍是远程空间概念。现场路线、尺寸、安全、结构、无障碍、容量与施工做法仍需后续实地与专业验证。</p>
      </section>
    </div>
  </aside>
`;
document.body.insertAdjacentHTML('beforeend',supplementMarkup);

const trigger=document.querySelector('#supplementTrigger');
const panel=document.querySelector('#supplementPanel');
const closeControls=[...document.querySelectorAll('[data-supplement-close]')];
const tabs=[...document.querySelectorAll('[data-supplement-tab]')];
const panels=[...document.querySelectorAll('[data-supplement-panel]')];
let lastFocus=null;

function setSupplement(open){
  document.body.classList.toggle('supplement-open',open);
  trigger?.setAttribute('aria-expanded',String(open));
  panel?.setAttribute('aria-hidden',String(!open));
  if(open){lastFocus=document.activeElement;document.querySelector('.supplement-close')?.focus();}
  else if(lastFocus instanceof HTMLElement){lastFocus.focus();}
}

trigger?.addEventListener('click',()=>setSupplement(!document.body.classList.contains('supplement-open')));
closeControls.forEach(control=>control.addEventListener('click',()=>setSupplement(false)));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&document.body.classList.contains('supplement-open')) setSupplement(false);});

tabs.forEach(tab=>tab.addEventListener('click',()=>{
  const key=tab.dataset.supplementTab;
  tabs.forEach(item=>item.classList.toggle('is-active',item===tab));
  panels.forEach(item=>item.classList.toggle('is-active',item.dataset.supplementPanel===key));
}));

document.querySelectorAll('[data-supplement-jump]').forEach(link=>link.addEventListener('click',()=>setSupplement(false)));
