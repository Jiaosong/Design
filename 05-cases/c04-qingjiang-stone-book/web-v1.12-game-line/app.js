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
  $$(".mode-card").forEach(btn=>btn.addEventListener("click",()=>{$$(".mode-card").forEach(x=>x.classList.toggle("active",x===btn));const d=modeData[btn.dataset.mode];$("#modeKicker").textContent=d.k;$("#modeTitle").textContent=d.t;$("#modeBody").textContent=d.b;}));
  const stateData={normal:["正常阅读","完整游程可见；数字保持低干扰；回程入口始终可达。"],degraded:["降级阅读","减少非必要互动与解释，突出可走路线、休息与回程。"],closed:["关闭优先","停止引导进入受限段，不用内容奖励诱导继续；直接提供替代与回程。"],unknown:["未知即谨慎","不猜测可用性；隐藏不确定承诺，优先给出人工确认、保守路径与回程。"]};
  $$(".state-buttons button").forEach(btn=>btn.addEventListener("click",()=>{$$(".state-buttons button").forEach(x=>x.classList.toggle("active",x===btn));const d=stateData[btn.dataset.state];$("#stateResult").innerHTML=`<b>${d[0]}</b><span>${d[1]}</span>`;}));
  const imprints={"看":"先让景观完整出现；当你愿意继续时，再打开与此处真正相关的一页。","比":"把两处山形、水色或尺度放在一起看，发现关系，而不是寻找标准答案。","寻":"寻找一个真实存在的线索；找不到也不影响继续游程。","听":"降低屏幕与文字，让水、风、船与山谷的声音进入体验。","等":"允许停一会儿。等待光、雾、水面或人流变化本身就是阅读。","框":"用一个有限视域重新组织眼前景观，但不把框架变成主角。","望":"拉远距离，重新确认自己在整条清江中的位置。","辨":"辨认植物、岩层、地名或空间关系；证据不足时明确保持开放。","随":"跟随水、风、路径或视线移动，不强迫完成固定动作。","过":"通过是体验的一部分。狭窄、转折与退出必须先满足身体和安全。","记":"只保存真正愿意记住的内容，而不是自动收集所有页面。","回":"路线与服务优先，回程从进入项目的一刻就存在。","留":"带走一条线、一页石书或一个重新认识清江的方式。"};
  function setImprint(btn){$$(".imprint-wheel button").forEach(x=>x.classList.toggle("active",x===btn));$("#imprintAction").textContent=btn.dataset.imprint;$("#imprintCopy").textContent=imprints[btn.dataset.imprint];}
  $$(".imprint-wheel button").forEach(btn=>btn.addEventListener("click",()=>setImprint(btn)));setImprint($(".imprint-wheel button"));
  $$(".audience-tab").forEach(btn=>btn.addEventListener("click",()=>$$('.audience-tab').forEach(x=>x.classList.toggle('active',x===btn))));
  function syncPage(){const sections=$$(".section[id]");let active=sections[0]?.id||"hero";const y=window.scrollY+innerHeight*.32;for(const s of sections){if(s.offsetTop<=y)active=s.id;}const groups={journey:["journey"],context:["context","brief","audience"],thinking:["thinking","idea"],systems:["system","imprints","scenes","scene-r13","digital","physical","brandmemory","memory"],development:["technical"],final:["final"]};$$(".layer-nav a").forEach(a=>{const target=a.getAttribute("href").slice(1);a.classList.toggle("active",(groups[target]||[]).includes(active));});}
  addEventListener("scroll",syncPage,{passive:true});syncPage();
  const toggle=$(".nav-toggle"),mobile=$("#mobileNav");toggle?.addEventListener("click",()=>{const open=toggle.getAttribute("aria-expanded")==="true";toggle.setAttribute("aria-expanded",String(!open));mobile.hidden=open;});$$("#mobileNav a").forEach(a=>a.addEventListener("click",()=>{mobile.hidden=true;toggle?.setAttribute("aria-expanded","false");}));
  const trigger=$("#supplementTrigger"),panel=$("#supplementPanel"),close=$("#supplementClose"),scrim=$("#scrim");
  function setSupplement(open){panel.hidden=!open;scrim.hidden=!open;trigger.setAttribute("aria-expanded",String(open));document.body.style.overflow=open?"hidden":"";if(open)close.focus();else trigger.focus();}
  trigger.addEventListener("click",()=>setSupplement(panel.hidden));close.addEventListener("click",()=>setSupplement(false));scrim.addEventListener("click",()=>setSupplement(false));addEventListener("keydown",e=>{if(e.key==="Escape"&&!panel.hidden)setSupplement(false)});
  $$(".supplement-tabs button").forEach(btn=>btn.addEventListener("click",()=>{$$(".supplement-tabs button").forEach(x=>x.setAttribute("aria-selected",String(x===btn)));$$('[data-supplement]').forEach(x=>x.hidden=x.dataset.supplement!==btn.dataset.panel);}));
  async function bindLocalChunkImage(el,parts,mime="image/png"){if(!el)return;try{const text=(await Promise.all(parts.map(p=>fetch(p).then(r=>{if(!r.ok)throw new Error(p);return r.text();})))).join("").replace(/\s+/g,"");el.style.backgroundImage=`url("data:${mime};base64,${text}")`;el.classList.add("loaded");}catch(err){console.warn("C04 local image binding fallback:",err);}}
  bindLocalChunkImage($("#heroImage"),["assets/qj_hero_keep_v11_b64_01.txt","assets/qj_hero_keep_v11_b64_02a.txt"]);bindLocalChunkImage($("#r06Image"),["assets/qj_r06_landscape_keep_v11_b64_01.txt"]);
  $$(".app-tabs button").forEach(btn=>btn.addEventListener("click",()=>$$('.app-tabs button').forEach(x=>x.classList.toggle('active',x===btn))));
  if(!reduced.matches&&"IntersectionObserver" in window){const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add("in-view");}),{threshold:.08});$$('.section-head,.scope-grid,.analysis-grid,.asset-split,.technical-grid').forEach(x=>io.observe(x));}
})();
