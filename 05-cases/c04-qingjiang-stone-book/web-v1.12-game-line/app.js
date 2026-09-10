(() => {
  "use strict";
  const $=(q,root=document)=>root.querySelector(q);
  const $$=(q,root=document)=>[...root.querySelectorAll(q)];
  const reduced=window.matchMedia("(prefers-reduced-motion: reduce)");

  const modeData={
    boat:{k:"BOAT / OPEN",t:"先完整地看见清江。",b:"水面把峡谷、峰林、岸线和行进距离同时拉开。设计在这里降低解释密度，让真实景观成为第一信息层。"},
    cable:{k:"CABLE / RELATION",t:"从空中建立山、水、路的关系。",b:"索道改变观看高度与速度，使两岸、峰谷与路线联系变得可读。解释只揭示关系，不把视线从清江夺走。"},
    walk:{k:"WALK / DETAIL",t:"进入山中，才允许细读。",b:"步行把观察缩小到植物、岩壁、声音、身体与停留。十三印在这里按需出现，并始终允许跳过。"}
  };
  const modeCards=$$(".mode-card");
  const setMode=(btn)=>{
    modeCards.forEach(x=>{
      const active=x===btn;
      x.classList.toggle("active",active);
      x.setAttribute("aria-pressed",String(active));
      const label=$("small",x);
      if(label){
        if(!label.dataset.baseLabel)label.dataset.baseLabel=label.textContent.trim();
        label.textContent=active?`${label.dataset.baseLabel} · 当前`:label.dataset.baseLabel;
      }
    });
    const d=modeData[btn.dataset.mode];
    if(!d)return;
    $("#modeKicker").textContent=d.k;
    $("#modeTitle").textContent=d.t;
    $("#modeBody").textContent=d.b;
  };
  modeCards.forEach(btn=>btn.addEventListener("click",()=>setMode(btn)));
  const initialMode=modeCards.find(x=>x.classList.contains("active"))||modeCards[0];
  if(initialMode)setMode(initialMode);

  const audienceData=[
    {k:"FAMILY / EASY EXIT",t:"少读一点，也能完整经过。",b:"亲子场景优先短动作、低文字与清楚退出；不把深读变成同行压力。"},
    {k:"EXPLORER / CHOOSE",t:"把选择留给正在探索的人。",b:"青年与自主探索者可以比较路线、寻找关系并按兴趣进入更深内容。"},
    {k:"READER / DEEPEN",t:"需要证据时，再向下读。",b:"深读者可以进入证据、内容与对照层，但这些信息不占据所有人的第一视线。"},
    {k:"RECOVERY / RETURN",t:"体力下降时，服务先于内容。",b:"低体力与恢复状态优先休息、方向确认和回程；数字与阅读都可以暂时退场。"}
  ];
  const audienceTabs=$$(".audience-tab");
  const audienceReadout=$(".audience-readout");
  if(audienceReadout&&audienceTabs.length){
    const setAudience=(btn,index)=>{
      audienceTabs.forEach(x=>{
        const active=x===btn;
        x.classList.toggle("active",active);
        x.setAttribute("aria-pressed",String(active));
      });
      const d=audienceData[index];
      if(!d)return;
      $(".audience-kicker",audienceReadout).textContent=d.k;
      $(".audience-title",audienceReadout).textContent=d.t;
      $(".audience-body",audienceReadout).textContent=d.b;
    };
    audienceTabs.forEach((btn,index)=>btn.addEventListener("click",()=>setAudience(btn,index)));
    const initial=Math.max(0,audienceTabs.findIndex(x=>x.classList.contains("active")));
    setAudience(audienceTabs[initial],initial);
  }

  const stateData={
    normal:{k:"NORMAL / FULL",t:"路线、状态与可选深读都可用。",b:"路线保持第一层；十三印与数字内容按兴趣打开，不改变回程权威。"},
    degraded:{k:"DEGRADED / LIGHT",t:"减少内容，先保住方向与回程。",b:"降低阅读与互动密度；纸本、标识与人工确认继续承担方向和回退。"},
    closed:{k:"CLOSED / OFF",t:"停止继续进入，明确转向回程。",b:"关闭可选深读与前进承诺，只保留关闭信息、人工确认和返回路径。"},
    unknown:{k:"UNKNOWN / FAIL-CLOSED",t:"不确定时，不猜可用。",b:"不把未知状态显示成正常；先提示确认并保留最小回程路径，再决定是否继续。"}
  };
  const systems=$("#systems");
  if(systems){
    // SYSTEMS is a direct navigation destination and a browser-readback carrier.
    // Its claim and primary route visual must be readable immediately, even before
    // IntersectionObserver has a chance to resolve the decorative reveal transition.
    [$(".section-head",systems),$(".asset-split",systems)].filter(Boolean).forEach(x=>x.classList.add("in-view"));
  }
  if(systems&&!$(".state-sim",systems)){
    const host=document.createElement("div");
    host.className="state-sim";
    host.setAttribute("aria-label","路线状态与回程反馈");
    host.innerHTML=`<p class="micro">STATE FEEDBACK / ROUTE FIRST</p><div class="state-buttons" role="group" aria-label="路线状态"><button type="button" class="active" data-state="normal">NORMAL</button><button type="button" data-state="degraded">DEGRADED</button><button type="button" data-state="closed">CLOSED</button><button type="button" data-state="unknown">UNKNOWN</button></div><div class="state-result" aria-live="polite"><b>路线、状态与可选深读都可用。</b><span>路线保持第一层；十三印与数字内容按兴趣打开，不改变回程权威。</span></div>`;
    $(".asset-split",systems)?.insertAdjacentElement("afterend",host);
    const buttons=$$(".state-buttons button",host);
    const result=$(".state-result",host);
    const setState=(btn)=>{
      buttons.forEach(x=>{const active=x===btn;x.classList.toggle("active",active);x.setAttribute("aria-pressed",String(active));});
      const d=stateData[btn.dataset.state];
      if(!d||!result)return;
      $(".micro",host).textContent=`STATE FEEDBACK / ${d.k}`;
      $("b",result).textContent=d.t;
      $("span",result).textContent=d.b;
    };
    buttons.forEach(btn=>btn.addEventListener("click",()=>setState(btn)));
    setState(buttons[0]);
  }

  function syncPage(){
    const sections=$$(".section[id]");
    let active=sections[0]?.id||"hero";
    const y=window.scrollY+innerHeight*.32;
    for(const s of sections){if(s.offsetTop<=y)active=s.id;}
    const groups={journey:["journey"],context:["brief","context","audience"],thinking:["idea","thinking"],systems:["systems"],development:["development"],final:["final"]};
    $$(".layer-nav a").forEach(a=>{
      const target=a.getAttribute("href").slice(1);
      const current=(groups[target]||[]).includes(active);
      a.classList.toggle("active",current);
      if(current)a.setAttribute("aria-current","location");else a.removeAttribute("aria-current");
    });
    $$("#mobileNav a").forEach(a=>{
      const target=a.getAttribute("href").slice(1);
      const current=(groups[target]||[]).includes(active);
      a.classList.toggle("active",current);
      if(current){
        a.setAttribute("aria-current","location");
        a.style.background="rgba(120,197,196,.10)";
        a.style.color="#fff";
      }else{
        a.removeAttribute("aria-current");
        a.style.background="";
        a.style.color="";
      }
    });
  }
  addEventListener("scroll",syncPage,{passive:true});
  syncPage();

  const toggle=$(".nav-toggle"),mobile=$("#mobileNav");
  toggle?.addEventListener("click",()=>{
    const open=toggle.getAttribute("aria-expanded")==="true";
    toggle.setAttribute("aria-expanded",String(!open));
    if(mobile)mobile.hidden=open;
  });
  $$("#mobileNav a").forEach(a=>a.addEventListener("click",()=>{
    if(mobile)mobile.hidden=true;
    toggle?.setAttribute("aria-expanded","false");
  }));

  async function bindLocalChunkImage(el,parts,mime="image/png"){
    if(!el)return;
    el.dataset.state="loading";
    el.setAttribute("aria-busy","true");
    el.setAttribute("role","img");
    el.setAttribute("aria-label","清江峡谷主视觉正在载入");
    try{
      const text=(await Promise.all(parts.map(p=>fetch(p).then(r=>{if(!r.ok)throw new Error(p);return r.text();})))).join("").replace(/\s+/g,"");
      el.style.backgroundImage=`url("data:${mime};base64,${text}")`;
      el.classList.add("loaded");
      el.dataset.state="active";
      el.setAttribute("aria-busy","false");
      el.setAttribute("aria-label","清江峡谷主视觉");
    }catch(err){
      el.dataset.state="error";
      el.setAttribute("aria-busy","false");
      el.setAttribute("aria-label","清江主视觉暂未载入；可继续阅读游程与设计内容");
      el.style.backgroundImage="linear-gradient(135deg,#071318 0%,#123139 55%,#2e7f86 100%)";
      el.classList.add("loaded");
      console.warn("C04 local image binding fallback:",err);
    }
  }
  bindLocalChunkImage($("#heroImage"),["assets/qj_hero_keep_v11_b64_01.txt","assets/qj_hero_keep_v11_b64_02a.txt"]);

  if(!reduced.matches&&"IntersectionObserver" in window){
    const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add("in-view");}),{threshold:.08});
    $$(".section-head,.scope-grid,.analysis-grid,.asset-split").forEach(x=>io.observe(x));
  }
})();