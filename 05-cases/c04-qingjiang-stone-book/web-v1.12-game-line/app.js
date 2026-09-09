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
  $$(".mode-card").forEach(btn=>btn.addEventListener("click",()=>{
    $$(".mode-card").forEach(x=>x.classList.toggle("active",x===btn));
    const d=modeData[btn.dataset.mode];
    if(!d)return;
    $("#modeKicker").textContent=d.k;
    $("#modeTitle").textContent=d.t;
    $("#modeBody").textContent=d.b;
  }));

  const audienceData=[
    {k:"FAMILY / EASY EXIT",t:"少读一点，也能完整经过。",b:"亲子场景优先短动作、低文字与清楚退出；不把深读变成同行压力。"},
    {k:"EXPLORER / CHOOSE",t:"把选择留给正在探索的人。",b:"青年与自主探索者可以比较路线、寻找关系并按兴趣进入更深内容。"},
    {k:"READER / DEEPEN",t:"需要证据时，再向下读。",b:"深读者可以进入证据、内容与对照层，但这些信息不占据所有人的第一视线。"},
    {k:"RECOVERY / RETURN",t:"体力下降时，服务先于内容。",b:"低体力与恢复状态优先休息、方向确认和回程；数字与阅读都可以暂时退场。"}
  ];
  const audienceTabs=$$(".audience-tab");
  const audienceList=$(".audience-list");
  let audienceReadout=null;
  if(audienceList&&audienceTabs.length){
    audienceReadout=document.createElement("div");
    audienceReadout.className="audience-readout";
    audienceReadout.setAttribute("aria-live","polite");
    audienceReadout.innerHTML='<p class="audience-kicker"></p><b class="audience-title"></b><span class="audience-body"></span>';
    audienceList.after(audienceReadout);
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
    setAudience(audienceTabs.find(x=>x.classList.contains("active"))||audienceTabs[0],Math.max(0,audienceTabs.findIndex(x=>x.classList.contains("active"))));
  }

  function syncPage(){
    const sections=$$(".section[id]");
    let active=sections[0]?.id||"hero";
    const y=window.scrollY+innerHeight*.32;
    for(const s of sections){if(s.offsetTop<=y)active=s.id;}
    const groups={
      journey:["journey"],
      context:["brief","context","audience"],
      thinking:["idea","thinking"],
      systems:["systems"],
      development:["development"],
      final:["final"]
    };
    $$(".layer-nav a").forEach(a=>{
      const target=a.getAttribute("href").slice(1);
      a.classList.toggle("active",(groups[target]||[]).includes(active));
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
    try{
      const text=(await Promise.all(parts.map(p=>fetch(p).then(r=>{
        if(!r.ok)throw new Error(p);
        return r.text();
      })))).join("").replace(/\s+/g,"");
      el.style.backgroundImage=`url("data:${mime};base64,${text}")`;
      el.classList.add("loaded");
    }catch(err){
      console.warn("C04 local image binding fallback:",err);
    }
  }
  bindLocalChunkImage($("#heroImage"),[
    "assets/qj_hero_keep_v11_b64_01.txt",
    "assets/qj_hero_keep_v11_b64_02a.txt"
  ]);

  if(!reduced.matches&&"IntersectionObserver" in window){
    const io=new IntersectionObserver(entries=>entries.forEach(e=>{
      if(e.isIntersecting)e.target.classList.add("in-view");
    }),{threshold:.08});
    $$(".section-head,.scope-grid,.analysis-grid,.asset-split").forEach(x=>io.observe(x));
  }
})();