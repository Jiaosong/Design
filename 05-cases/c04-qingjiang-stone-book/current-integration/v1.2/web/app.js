const imprintData=[
 ['R01','红岩嘴','CABLE · MOVING VIEW','索道段优先移动视野；不设置强制 UI、长解释或必做触发。',['OBSERVE','NO FORCED UI']],
 ['R02','华中第一藤','VEGETATION · FIELD OPEN','植物观察保持来源边界；现场物种、季相与精确位置继续 FIELD OPEN。',['PLANT','OBSERVE']],
 ['R03','铁券天书','READ · SCIENCE OPEN','作为可选阅读层进入；不把解释变成路线任务。',['READ','OPTIONAL']],
 ['R04','母子相望','NAMED VIEW · RELATION','景观关系先于故事说明，命名解释只在需要时出现。',['VIEW','RELATION']],
 ['R05','红花石林','SCENE · OFFICIAL PIXEL HOLD','场景逻辑保留；官方红花石林原始像素尚未 materialize 进 MAIN。',['SCENE','PIXEL HOLD']],
 ['R06','多级阶地 · 不对称河谷','OBSERVATION · RECOVER','先看河谷，再在需要时短暂 Reveal 关系。阅读完成后界面退出，注意力回到清江。',['LOOK','RECOVER','OPTIONAL REVEAL']],
 ['R07','仓禀峰／仓廪峰','NAME · FORM','官方来源存在名称冲突，当前双写并等待现场标牌校核。',['NAME','DUAL SOURCE']],
 ['R08','文山天书','CLIFF · READ','崖壁阅读保持科学解释 OPEN，不制造精确现场证据。',['CLIFF','READ']],
 ['R09','盐水女神峰','LOCAL STORY','地方故事可读，但不宣称故事与具体现场实体完全等同。',['STORY','SOURCE BOUNDARY']],
 ['R10','绝壁天书','SAFE-DISTANCE OBSERVE','以安全距离观察为前提，解释不鼓励越界接近。',['SAFETY','OBSERVE']],
 ['R11','金石为开','BODY · FISSURE','身体与裂隙关系优先，不把空间压成文本任务。',['BODY','RELATION']],
 ['R12','廪君峰','CULTURE · DISTANT VIEW','文化解释在远观层发生，保持来源与场景边界。',['CULTURE','DISTANT VIEW']],
 ['R13','一线天','BODY FIRST · RETURN','收紧注意：PLAY OFF，安全与 Return 提升，解释退场。',['BODY FIRST','SAFETY','RETURN']]
];
const coords=[[8,32],[16,43],[23,38],[31,47],[39,40],[47,54],[54,45],[61,59],[68,50],[75,61],[82,54],[88,66],[94,59]];
const map=document.getElementById('imprintMap');
function selectImprint(i){document.querySelectorAll('.imprintNode').forEach((n,j)=>n.classList.toggle('active',i===j));const d=imprintData[i];document.getElementById('imprintKicker').textContent=d[0]+' / '+d[2];document.getElementById('imprintTitle').textContent=d[1];document.getElementById('imprintCopy').textContent=d[3];document.getElementById('imprintTags').innerHTML=d[4].map(x=>'<span class="tag">'+x+'</span>').join('')}
if(map){imprintData.forEach((d,i)=>{const b=document.createElement('button');b.className='imprintNode'+(i===5?' active':'');b.style.left=coords[i][0]+'%';b.style.top=coords[i][1]+'%';b.textContent=String(i+1).padStart(2,'0');b.setAttribute('aria-label',d[0]+' '+d[1]);b.onclick=()=>selectImprint(i);map.appendChild(b)});selectImprint(5)}
const obs=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('inview')}),{threshold:.2});document.querySelectorAll('.observe').forEach(x=>obs.observe(x));
const sections=[...document.querySelectorAll('section')],navState=document.getElementById('navState'),progress=document.getElementById('progress');
const sectionObs=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting&&navState)navState.textContent=e.target.dataset.label}),{threshold:.45});sections.forEach(s=>sectionObs.observe(s));
addEventListener('scroll',()=>{const h=document.documentElement.scrollHeight-innerHeight;if(progress)progress.style.width=(h?scrollY/h*100:0)+'%'},{passive:true});
const lightbox=document.getElementById('lightbox'),tech=document.getElementById('techZoom'),close=document.getElementById('closeLightbox');
if(lightbox&&tech&&close){tech.onclick=()=>{lightbox.classList.add('open');lightbox.setAttribute('aria-hidden','false')};close.onclick=()=>{lightbox.classList.remove('open');lightbox.setAttribute('aria-hidden','true')};lightbox.addEventListener('click',e=>{if(e.target===lightbox)close.click()});addEventListener('keydown',e=>{if(e.key==='Escape')close.click()})}