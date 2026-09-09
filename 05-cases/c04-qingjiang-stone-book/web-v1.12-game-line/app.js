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

  $$(".audience-tab").forEach(btn=>btn.addEventListener("click",()=>{
    $$(".audience-tab").forEach(x=>x.classList.toggle("active",x===btn));
  }));

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