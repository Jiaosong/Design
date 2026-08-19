(()=>{
  const bar=document.querySelector('.v113-progress');
  const nav=[...document.querySelectorAll('.v113-nav a[href^="#"]')];
  const surfaces=[...document.querySelectorAll('.surface[id]')];
  const update=()=>{const max=document.documentElement.scrollHeight-innerHeight;if(bar)bar.style.width=`${max?scrollY/max*100:0}%`;};
  addEventListener('scroll',update,{passive:true});update();
  const obs=new IntersectionObserver(es=>es.forEach(e=>{if(!e.isIntersecting)return;nav.forEach(a=>a.dataset.active=(a.getAttribute('href')==='#'+e.target.dataset.chapter));}),{threshold:.18,rootMargin:'-18% 0px -60%'});
  surfaces.forEach(s=>obs.observe(s));
  nav.forEach(a=>a.addEventListener('click',e=>{const t=document.querySelector(a.getAttribute('href'));if(t){e.preventDefault();t.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});}}));
  document.querySelectorAll('.asset-shell img,.asset-shell object').forEach(el=>{
    const shell=el.closest('.asset-shell');
    const fail=()=>shell?.classList.add('missing');
    el.addEventListener('error',fail);
    if(el.tagName==='OBJECT')el.addEventListener('load',()=>{try{if(!el.contentDocument)fail()}catch(_){}});
  });
})();
