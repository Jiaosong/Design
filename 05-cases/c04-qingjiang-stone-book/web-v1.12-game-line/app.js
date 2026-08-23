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
