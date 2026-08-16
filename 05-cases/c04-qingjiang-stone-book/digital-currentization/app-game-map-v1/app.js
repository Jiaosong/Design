const imprintData = [
{id:'R01',name:'红岩嘴',mode:'WISDOM',question:'移动中，你先看见江，还是先看见两岸？',adult:'先看跨江视点如何改变两岸、河面和峰林的整体关系。',family:'和孩子一起找：索道移动时，哪一边的山变化最快？',youth:'用移动视点判断远近变化，不要求在索道内完成阅读。',senior:'不增加任务；优先确认到达方向与回程。',action:'看一段，不用点开也成立。'},
{id:'R02',name:'华中第一藤',mode:'WISDOM',question:'一株藤怎样借树、坡地和光进入森林？',adult:'观察藤本与树木、光线和坡地的关系；物种、年龄与“第一”判据保持专家开放。',family:'找一找藤从哪里开始、向哪里爬，不做物种抢答。',youth:'先描述你看到的生长关系，再决定是否打开科学解释。',senior:'保持短阅读，可直接跳过。',action:'观察 → 描述 → 可选解释。'},
{id:'R03',name:'铁券天书',mode:'WISDOM',question:'石面上的裂隙与纹理，有哪些差异？',adult:'从颜色、裂隙和层面开始观察，不从外观直接宣布岩性与成因。',family:'像找线条一样找石面纹路。',youth:'比较两块石面的结构差异，留下问题。',senior:'只看最明显的一处变化即可。',action:'找差异，不急着得到结论。'},
{id:'R04',name:'母子相望',mode:'CULTURE / PLAY',question:'一个地方名字，怎样来自轮廓、故事和人的想象？',adult:'把地方命名与峰体轮廓并置阅读，不把名称当作科学事实。',family:'找一找“母”“子”可能分别对应哪里，说出自己的版本。',youth:'比较命名与实际轮廓之间的偏差。',senior:'听故事即可，不需要完成互动。',action:'看轮廓 → 听名字 → 保留不同解释。'},
{id:'R05',name:'红花石林',mode:'PLAY / WISDOM',question:'整片峰林里，你最先认出的是什么？',adult:'先看峰、谷、江与大气形成的整体景观，再选择一个问题深入。',family:'亲子一起找三种不同的峰形。',youth:'做轮廓匹配或摄影构图，不把峰林拆成任务点。',senior:'以完整观看和休息为主。',action:'看整体 → 找轮廓 → 可选记录。'},
{id:'R06',name:'河谷观察',mode:'WISDOM / WELLBEING',question:'江、两岸、坡面和步道，彼此在哪里？',adult:'先看完整河谷，再用简化剖面理解相对位置；精确几何仍待现场。',family:'一起找出江、两岸和不同高度的山体。',youth:'用剖面猜相对位置，再和实际观看对照。',senior:'先看休息和回程，再决定是否继续深入阅读。',action:'看见 → 比较 → 理解 → 休息。'},
{id:'R07',name:'仓禀峰／仓廪峰',mode:'CULTURE',question:'为什么同一座峰会出现不同写法？',adult:'保留现有来源中的名称冲突，把“如何确认地名”本身变成文化阅读。',family:'找相同的峰，不要求记住哪一个字“正确”。',youth:'比较不同来源写法，理解名称也需要证据。',senior:'显示双写，避免增加认知负担。',action:'保留冲突 → 等待现场牌示确认。'},
{id:'R08',name:'文山天书',mode:'CULTURE / WISDOM',question:'岩壁像“书页”的感觉，来自哪些线条和层次？',adult:'把“天书”作为地方阅读方式，科学解释保持证据边界。',family:'沿着岩壁找像“页边”的线。',youth:'比较层面、裂隙与光影，不把想象当地质事实。',senior:'短时观看即可。',action:'地方想象 + 观察，不替代地质结论。'},
{id:'R09',name:'盐水女神峰',mode:'CULTURE',question:'故事为什么会依附在山峰上？',adult:'听盐水女神相关地方叙事，同时保留故事与现代峰体地点之间的证据距离。',family:'听短故事，找故事里提到的形状与方向。',youth:'区分“文本传统”与“历史地点事实”。',senior:'以音频或短文为主。',action:'听故事，但不把故事当地理证明。'},
{id:'R10',name:'绝壁天书',mode:'WISDOM / PLAY',question:'近看岩壁时，你能找到几种不同的表面？',adult:'观察纹理、颜色、裂隙和风化差异。',family:'做“找不同”，不做危险靠近。',youth:'用手机只记录观察结果，不做 AR 追逐。',senior:'保持安全距离，内容可跳过。',action:'近看差异，保持安全边界。'},
{id:'R11',name:'金石为开',mode:'WISDOM',question:'身体通过狭窄空间时，尺度感为什么会改变？',adult:'把裂隙、身体和转折作为空间观察，不做力量或成因的伪科学解释。',family:'只在安全位置比较“宽/窄”。',youth:'观察身体尺度如何改变对岩壁的感受。',senior:'优先确认通过与返回条件。',action:'身体尺度优先。'},
{id:'R12',name:'廪君峰',mode:'CULTURE',question:'地方英雄的故事，怎样进入今天的景观阅读？',adult:'阅读廪君相关文本传统与地方文化，不把现代峰名等同为古代事件史址。',family:'用人物关系图听一个短故事。',youth:'比较故事文本与今天看到的景观。',senior:'音频/大字短文优先。',action:'故事进入景观，但不替地点作证。'},
{id:'R13',name:'一线天',mode:'WELLBEING / BODY',question:'当空间变窄，什么信息应该消失？',adult:'停止新增任务和长解释，只保留通过、观察、返回与必要安全信息。',family:'不设置追逐、计时、搜寻任务。',youth:'通过后再观察岩壁与光线，不在狭窄处抢注意力。',senior:'返回/绕行信息优先；实际条件仍待现场核验。',action:'PLAY OFF · BODY / RETURN ON。'}
];
let currentAudience='adult';
const views=[...document.querySelectorAll('.view')];
function openView(name){views.forEach(v=>v.classList.toggle('active',v.dataset.view===name));document.querySelectorAll('.nav-item').forEach(b=>b.classList.toggle('active',b.dataset.nav===name));window.scrollTo({top:0,behavior:'instant'});}
document.querySelectorAll('[data-nav]').forEach(b=>b.addEventListener('click',()=>openView(b.dataset.nav)));
document.querySelectorAll('[data-open="service"]').forEach(b=>b.addEventListener('click',()=>openView('service')));
document.querySelectorAll('.journey-mode').forEach(b=>b.addEventListener('click',()=>openView('route')));
function renderImprints(){const root=document.getElementById('imprintGrid');root.innerHTML=imprintData.map(d=>`<article class="imprint-card" data-id="${d.id}"><div><div class="top"><span class="num">${d.id}</span><span class="mode">${d.mode}</span></div><h3>${d.name}</h3><p>${d.question}</p></div><div class="gain">${d[currentAudience]}</div></article>`).join('');root.querySelectorAll('.imprint-card').forEach(c=>c.onclick=()=>openImprint(c.dataset.id));}
const dlg=document.getElementById('imprintDialog'),dc=document.getElementById('dialogContent');
function openImprint(id){const d=imprintData.find(x=>x.id===id);if(!d)return;dc.innerHTML=`<div class="dialog-inner"><div class="dialog-kicker">${d.id} · ${d.mode}</div><h2>${d.name}</h2><div class="question">${d.question}</div><div class="dialog-action"><b>这次可以怎么做</b><p>${d.action}</p></div><p>${d[currentAudience]}</p><div class="dialog-foot">可打开 / 可跳过 / 可错序。内容不拥有路线；现场条件、开放状态与安全仍以官方/现场信息为准。</div></div>`;dlg.showModal();}
document.querySelector('.close-dialog').onclick=()=>dlg.close();dlg.addEventListener('click',e=>{if(e.target===dlg)dlg.close();});
document.querySelectorAll('.aud').forEach(b=>b.onclick=()=>{currentAudience=b.dataset.audience;document.querySelectorAll('.aud').forEach(x=>x.classList.toggle('active',x===b));renderImprints();});
document.querySelectorAll('[data-open-imprint]').forEach(c=>c.onclick=()=>openImprint(c.dataset.openImprint));
document.querySelectorAll('.imprint-node').forEach(n=>n.addEventListener('click',()=>openImprint(n.dataset.id)));
document.querySelectorAll('.chip').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.chip').forEach(x=>x.classList.toggle('active',x===b));const key=b.dataset.layer;['journey','imprint','rest','service'].forEach(layer=>{document.querySelectorAll(`.${layer}-layer`).forEach(el=>el.classList.toggle('layer-hidden',key!=='all'&&key!==layer));});}));
renderImprints();
