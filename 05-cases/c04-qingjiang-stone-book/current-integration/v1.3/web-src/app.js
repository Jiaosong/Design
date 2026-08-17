const $=(s,c=document)=>c.querySelector(s); const $$=(s,c=document)=>[...c.querySelectorAll(s)];

const progress=$('#progress');
const chapters=$$('.chapter[data-chapter]');
const dots=$$('.chapter-dot');
const navState=$('#navState');
function updateScroll(){
  const max=document.documentElement.scrollHeight-innerHeight;
  progress.style.width=`${max?scrollY/max*100:0}%`;
}
addEventListener('scroll',updateScroll,{passive:true}); updateScroll();

const chapterObs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{
    if(e.isIntersecting){
      const id=e.target.dataset.chapter;
      dots.forEach(d=>d.classList.toggle('active',d.dataset.target===id));
      if(navState) navState.textContent=id.toUpperCase();
    }
  })
},{threshold:.16,rootMargin:'-20% 0px -55% 0px'});
chapters.forEach(c=>chapterObs.observe(c));
dots.forEach(d=>d.addEventListener('click',()=>document.getElementById(d.dataset.target)?.scrollIntoView({behavior:'smooth'})));

const revealObs=new IntersectionObserver(entries=>entries.forEach(e=>{
  if(e.isIntersecting){e.target.classList.add('inview');}
}),{threshold:.15});
$$('.reveal,.route-card').forEach(el=>revealObs.observe(el));

const imprints=[
 {id:'R01',name:'红岩嘴',mode:'移动识别 / orientation',copy:'移动中看清江，不要求停下完成界面。索道与视域变化先于解释。',tags:['WISDOM','MOVING VIEW','NO FORCED UI']},
 {id:'R02',name:'华中第一藤',mode:'植物时间 / observation',copy:'先看生长与形态，再决定是否进入植物解释；物种与年龄结论保持专家开放。',tags:['LOOK','COMPARE','EVIDENCE OPEN']},
 {id:'R03',name:'铁券天书',mode:'岩面过程 / surface',copy:'从表面变化与崩塌痕迹提出问题，不把远程观察写成确定地质结论。',tags:['TRACE','PROCESS','SOURCE-BOUNDED']},
 {id:'R04',name:'母子相望 / 母子峰',mode:'形态与命名 / culture',copy:'比较形态与地方命名，让“像什么”成为对话，而不是把联想当事实。',tags:['COMPARE','CULTURE','PLAY LIGHT']},
 {id:'R05',name:'红花石林',mode:'峰林识别 / landscape',copy:'寻找与比较峰林轮廓。当前权威原图尚待绑定，因此不以通用清江或 AI 峰体替代。',tags:['LANDSCAPE','FIND','PIXEL OPEN']},
 {id:'R06',name:'多级阶地 · 不对称河谷',mode:'河谷空间 / science',copy:'清江先读；恢复体力后可选择短暂关系揭示，完成后界面退出。',tags:['LANDSCAPE FIRST','RECOVER','OPTIONAL REVEAL']},
 {id:'R07',name:'仓禀峰／仓廪峰',mode:'地名确认 / name reading',copy:'保留官方来源之间的名称冲突，不把一个版本伪装成现场最终结论。',tags:['CULTURE','NAME OPEN','VERIFY']},
 {id:'R08',name:'文山天书',mode:'层理与叙事 / surface',copy:'把纹理、层次和故事分开阅读；视觉观察不直接跳成岩性结论。',tags:['LOOK','TRACE','CULTURE']},
 {id:'R09',name:'盐水女神峰',mode:'地方故事 / listening',copy:'故事通过可选听读进入，不把传说等同于历史遗址证明。',tags:['LISTEN','CULTURE','OPTIONAL']},
 {id:'R10',name:'绝壁天书',mode:'近距离纹理 / close read',copy:'关注表面、裂隙和尺度，把解释留在需要时出现。',tags:['TRACE','FRAME','WISDOM']},
 {id:'R11',name:'金石为开',mode:'裂隙与身体 / transition',copy:'从身体经过与空间收窄感知力量关系，不制造伪科学机制。',tags:['BODY','WAIT','WISDOM']},
 {id:'R12',name:'廪君峰',mode:'地方历史 / culture',copy:'把文本传统与景观看法并置，故事与地点等同性保持来源边界。',tags:['CULTURE','REMEMBER','SOURCE-BOUNDED']},
 {id:'R13',name:'一线天',mode:'身体通过 / closure',copy:'收窄空间里 PLAY OFF，身体、安全与 Return 先于内容；记忆发生在通过之后。',tags:['BODY FIRST','PLAY OFF','RETURN ON']}
];

function mapPos(i){
  const xs=[12,18,27,33,42,49,55,64,72,78,84,88,93];
  const ys=[60,52,44,62,35,48,67,39,57,30,51,69,42];
  return [xs[i],ys[i]];
}
const field=$('#imprintField');
if(field){
  imprints.forEach((it,i)=>{
    const b=document.createElement('button');b.className='imprint-btn';b.textContent=it.id.slice(1);b.dataset.index=i;
    const [x,y]=mapPos(i);b.style.left=x+'%';b.style.top=y+'%';field.appendChild(b);
  });
  const no=$('#imprintNo'),title=$('#imprintTitle'),mode=$('#imprintMode'),copy=$('#imprintCopy'),tags=$('#imprintTags');
  function selectImprint(i){
    const it=imprints[i];
    $$('.imprint-btn',field).forEach((b,j)=>b.classList.toggle('active',j===i));
    no.textContent=it.id; title.textContent=it.name; mode.textContent=it.mode; copy.textContent=it.copy;
    tags.innerHTML=it.tags.map(t=>`<span class="tag">${t}</span>`).join('');
  }
  field.addEventListener('click',e=>{const b=e.target.closest('.imprint-btn');if(b)selectImprint(+b.dataset.index)});selectImprint(5);
}

const map=$('#gameMap');
if(map){
  imprints.forEach((it,i)=>{
    const b=document.createElement('button');b.className='map-marker';b.textContent=it.id.slice(1);b.dataset.index=i;
    const [x,y]=mapPos(i);b.style.left=(8+x*.88)+'%';b.style.top=(18+y*.72)+'%';map.appendChild(b);
  });
  const title=$('#mapInfoTitle'),copy=$('#mapInfoCopy'),tags=$('#mapInfoTags');
  function selectMap(i){
    const it=imprints[i];$$('.map-marker',map).forEach((b,j)=>b.classList.toggle('active',j===i));
    title.textContent=`${it.id} · ${it.name}`;copy.textContent=it.copy;tags.innerHTML=it.tags.map(t=>`<span class="tag">${t}</span>`).join('');
  }
  map.addEventListener('click',e=>{const b=e.target.closest('.map-marker');if(b)selectMap(+b.dataset.index)});selectMap(5);
}

const lb=$('#lightbox');
$$('[data-zoom]').forEach(el=>el.addEventListener('click',()=>{const src=el.dataset.zoom||el.src;$('#lightboxImg').src=src;lb.classList.add('open')}));
$('#closeLightbox')?.addEventListener('click',()=>lb.classList.remove('open'));
lb?.addEventListener('click',e=>{if(e.target===lb)lb.classList.remove('open')});
addEventListener('keydown',e=>{if(e.key==='Escape')lb?.classList.remove('open')});
