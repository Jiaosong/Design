
const pages=[...document.querySelectorAll('.page')];
const progress=document.querySelector('#progress');const now=document.querySelector('#pageNow');
const rail=[...document.querySelectorAll('.rail a')];
function sync(){const y=scrollY, max=document.documentElement.scrollHeight-innerHeight;progress.style.width=(max?y/max*100:0)+'%';let best=pages[0],d=1e9;for(const p of pages){const r=p.getBoundingClientRect();const x=Math.abs(r.top-innerHeight*.22);if(x<d){d=x;best=p}}now.textContent=`${best.dataset.page} / 112`;rail.forEach(a=>a.classList.toggle('active',a.dataset.ch===best.dataset.chapter));}
addEventListener('scroll',sync,{passive:true});addEventListener('resize',sync);sync();
document.addEventListener('keydown',e=>{if(!['ArrowDown','ArrowUp','PageDown','PageUp'].includes(e.key))return;const current=pages.findIndex(p=>Math.abs(p.getBoundingClientRect().top)<innerHeight*.35);let n=current;if(e.key==='ArrowDown'||e.key==='PageDown')n=Math.min(pages.length-1,current+1);else n=Math.max(0,current-1);pages[n]?.scrollIntoView({behavior:'smooth'});});

const boatLabels={observe:'观 / LOOK',read:'解 / COMPARE',play:'变 / DISCOVER',care:'护 / RECOVER',return:'收 / RETURN'};
const boatStage=document.querySelector('[data-current-boat]');
document.querySelectorAll('[data-boat-state]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('[data-boat-state]').forEach(item=>item.classList.toggle('is-active',item===button));
  if(boatStage){boatStage.dataset.currentBoat=button.dataset.boatState;const label=boatStage.querySelector('.boat-state-label');if(label)label.textContent=boatLabels[button.dataset.boatState];}
}));

const ageCopy={
  child:{mode:'AI 宠物提问 / FAMILY READ',title:'先找出两岸最靠近的地方',body:'用指向与比较回答，不要求连续看屏幕；成人可关闭宠物提示。'},
  youth:{mode:'PUZZLE / RELATION READ',title:'哪一种地形关系让江面在这里收窄？',body:'比较峰体、谷向和水面线索，把判断放入个人舟印图；不设唯一答案。'},
  adult:{mode:'SOURCE-BOUND / DEEP READ',title:'从地形证据进入文化解释',body:'先显示来源与证据状态，再打开植物、地形和地方文化的分层解释。'},
  elder:{mode:'REST / RETURN FIRST',title:'先确认休息点与回程方向',body:'减少操作与动画；解释内容保持可选，纸图、标识和人工服务始终并列。'}
};
document.querySelectorAll('[data-age]').forEach(button=>button.addEventListener('click',()=>{
  document.querySelectorAll('[data-age]').forEach(item=>{const active=item===button;item.classList.toggle('is-active',active);item.setAttribute('aria-selected',String(active));});
  const copy=ageCopy[button.dataset.age];for(const [key,value] of Object.entries(copy)){const node=document.querySelector(`[data-ar-${key}]`);if(node)node.textContent=value;}
}));

const imprintButtons=[...document.querySelectorAll('[data-imprint]')];
function syncImprints(){const placed=imprintButtons.filter(button=>button.classList.contains('is-placed'));imprintButtons.forEach(button=>{const active=button.classList.contains('is-placed');button.setAttribute('aria-pressed',String(active));const state=button.querySelector('span');if(state)state.textContent=active?'已放入':'可选';document.querySelector(`.map-slot.slot-${button.dataset.imprint}`)?.classList.toggle('is-filled',active);});const copy=document.querySelector('[data-imprint-count]');if(copy)copy.textContent=`${placed.length} 枚舟印已形成一张完整的个人地图。`;}
imprintButtons.forEach(button=>button.addEventListener('click',()=>{button.classList.toggle('is-placed');syncImprints();}));syncImprints();

document.querySelectorAll('[data-flip-card]').forEach(card=>card.addEventListener('click',()=>{card.classList.toggle('is-flipped');card.setAttribute('aria-pressed',String(card.classList.contains('is-flipped')));}));
