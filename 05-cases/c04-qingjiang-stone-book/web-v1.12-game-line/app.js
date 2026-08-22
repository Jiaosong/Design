
const pages=[...document.querySelectorAll('.page')];
const progress=document.querySelector('#progress');const now=document.querySelector('#pageNow');
const rail=[...document.querySelectorAll('.rail a')];
function sync(){const y=scrollY, max=document.documentElement.scrollHeight-innerHeight;progress.style.width=(max?y/max*100:0)+'%';let best=pages[0],d=1e9;for(const p of pages){const r=p.getBoundingClientRect();const x=Math.abs(r.top-innerHeight*.22);if(x<d){d=x;best=p}}now.textContent=`${best.dataset.page} / 112`;rail.forEach(a=>a.classList.toggle('active',a.dataset.ch===best.dataset.chapter));}
addEventListener('scroll',sync,{passive:true});addEventListener('resize',sync);sync();
document.addEventListener('keydown',e=>{if(!['ArrowDown','ArrowUp','PageDown','PageUp'].includes(e.key))return;const current=pages.findIndex(p=>Math.abs(p.getBoundingClientRect().top)<innerHeight*.35);let n=current;if(e.key==='ArrowDown'||e.key==='PageDown')n=Math.min(pages.length-1,current+1);else n=Math.max(0,current-1);pages[n]?.scrollIntoView({behavior:'smooth'});});
