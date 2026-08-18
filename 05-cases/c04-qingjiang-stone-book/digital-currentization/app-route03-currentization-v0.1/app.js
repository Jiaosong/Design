const app=document.getElementById('app');
const worldScroll=document.getElementById('worldScroll');
const behaviorReadout=document.getElementById('behaviorReadout');
const sheet=document.getElementById('contextSheet');
const sheetTitle=document.getElementById('sheetTitle');
const sheetSummary=document.getElementById('sheetSummary');
const revealPanel=document.getElementById('revealPanel');
const revealText=document.getElementById('revealText');
const sheetState=document.getElementById('sheetState');
const panCue=document.getElementById('panCue');
const serviceLayer=document.getElementById('serviceLayer');

const modeData={
 A:{label:'A · 推荐',title:'水布垭 → 游客中心',focus:[.13,.5],meta:'同一 ROUTE-03 关系骨架；方向改变，不重画路线。'},
 B:{label:'B · 逆向',title:'游客中心 → 水布垭',focus:[.88,.5],meta:'逆向阅读相同来源关系，不生成第二套几何。'},
 C:{label:'C · 短线',title:'游客中心 ↔ 蝴蝶崖',focus:[.57,.5],meta:'短线折返来自 ROUTE-03 模式说明；实时运营状态仍 UNKNOWN。'},
 D:{label:'D · 短线',title:'游船码头 ↔ 蝴蝶崖',focus:[.54,.5],meta:'以码头为端点的短线关系；距离、坡度与通行状态不由本图证明。'}
};
const anchorData={
 dam:{pos:[.0753,.2661],title:'水布垭大坝',summary:'ROUTE-03 的西端关系节点。当前 App 只使用锁定图中的相对关系，不把它解释为 GPS 定位。',reveal:'从这里进入长线阅读时，界面仅改变视口与上下文，不改变锁定路线形状。实际到达方式、开放与换乘需由正式运营或现场信息确认。'},
 cliff:{pos:[.2697,.3048],title:'蝴蝶崖',summary:'ROUTE-03 中的折返关键点，同时出现在 C / D 短线模式中。',reveal:'它承担“是否继续长线”的关系判断，但本原型不把折返写成强制任务。十三印内容仍是可选阅读，且与现场精确邻近关系保持 FIELD OPEN。'},
 dock:{pos:[.8422,.6807],title:'游船码头',summary:'ROUTE-03 的水陆转换节点。服务与回程优先于内容触发。',reveal:'在水陆转换与回程阶段，Return Guard 保持可立即中断当前阅读。若正式状态不可得，界面维持 UNKNOWN，而不是绘制为正常开放。'},
 center:{pos:[.8809,.8613],title:'游客中心',summary:'ROUTE-03 的服务 / 回程优先节点，也是恢复路径的稳定入口。',reveal:'App 可以把这里作为信息恢复的关系锚点，但不模拟实时排队、营业、索道或船班。Digital OFF 时，纸图、标识、人工与真实景观仍应承担连续性。'}
};
let suppressScrollUntil=0;
function setBehavior(state){app.dataset.behavior=state;behaviorReadout.textContent=state.toUpperCase();}
function scrollWorldPct(xPct,yPct,announce=true){
 const maxX=Math.max(0,worldScroll.scrollWidth-worldScroll.clientWidth),maxY=Math.max(0,worldScroll.scrollHeight-worldScroll.clientHeight);
 const left=Math.max(0,Math.min(maxX,worldScroll.scrollWidth*xPct-worldScroll.clientWidth/2));
 const top=Math.max(0,Math.min(maxY,worldScroll.scrollHeight*yPct-worldScroll.clientHeight/2));
 suppressScrollUntil=performance.now()+480;
 worldScroll.scrollTo({left,top,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
 if(announce)setBehavior('scout');
}
function setMode(mode){
 document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
 const d=modeData[mode];document.getElementById('modeCode').textContent=d.label;document.getElementById('modeTitle').textContent=d.title;document.getElementById('modeMeta').textContent=d.meta;
 panCue.style.opacity='.35';scrollWorldPct(d.focus[0],d.focus[1],true);
}
function commitAnchor(id){
 document.querySelectorAll('.anchor').forEach(a=>a.classList.toggle('selected',a.dataset.anchor===id));
 const d=anchorData[id];setBehavior('commit');scrollWorldPct(d.pos[0],d.pos[1],false);
 sheetTitle.textContent=d.title;sheetSummary.textContent=d.summary;revealText.textContent=d.reveal;revealPanel.hidden=true;document.getElementById('revealBtn').textContent='展开关系说明';sheetState.textContent='COMMIT';
 const open=()=>{sheet.classList.add('open');sheet.setAttribute('aria-hidden','false')};
 if(matchMedia('(prefers-reduced-motion: reduce)').matches)open();else setTimeout(open,260);
}
function retreat(){sheet.classList.remove('open');sheet.setAttribute('aria-hidden','true');revealPanel.hidden=true;document.querySelectorAll('.anchor').forEach(a=>a.classList.remove('selected'));setBehavior('retreat');setTimeout(()=>setBehavior('intent'),260)}
function openReturn(){serviceLayer.classList.add('open');serviceLayer.setAttribute('aria-hidden','false');sheet.classList.remove('open');sheet.setAttribute('aria-hidden','true');revealPanel.hidden=true;document.querySelectorAll('.anchor').forEach(a=>a.classList.remove('selected'));setBehavior('return');document.querySelectorAll('[data-nav]').forEach(b=>b.classList.toggle('active',b.dataset.nav==='service'))}
function resume(){serviceLayer.classList.remove('open');serviceLayer.setAttribute('aria-hidden','true');setBehavior('intent');document.querySelectorAll('[data-nav]').forEach(b=>b.classList.toggle('active',b.dataset.nav==='route'))}

document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
document.querySelectorAll('.anchor').forEach(a=>{a.addEventListener('pointerenter',()=>{if(!sheet.classList.contains('open'))setBehavior('scout')});a.addEventListener('focus',()=>{if(!sheet.classList.contains('open'))setBehavior('scout')});a.addEventListener('click',()=>commitAnchor(a.dataset.anchor))});
document.getElementById('retreatBtn').addEventListener('click',retreat);
document.getElementById('revealBtn').addEventListener('click',()=>{revealPanel.hidden=false;document.getElementById('revealBtn').textContent='关系说明已展开';sheetState.textContent='REVEAL';setBehavior('reveal')});
document.getElementById('returnGuard').addEventListener('click',openReturn);
document.getElementById('resumeRoute').addEventListener('click',resume);
document.querySelectorAll('[data-nav]').forEach(b=>b.addEventListener('click',()=>{if(b.dataset.nav==='service')openReturn();else if(b.dataset.nav==='route')resume();}));
worldScroll.addEventListener('scroll',()=>{panCue.style.opacity='.22';if(performance.now()<suppressScrollUntil)return;if(app.dataset.behavior==='intent')setBehavior('scout')},{passive:true});
worldScroll.addEventListener('keydown',e=>{if(e.key==='ArrowRight')worldScroll.scrollBy({left:120,behavior:'smooth'});if(e.key==='ArrowLeft')worldScroll.scrollBy({left:-120,behavior:'smooth'});if(e.key==='Escape'&&sheet.classList.contains('open'))retreat()});
window.addEventListener('keydown',e=>{if(e.key==='Escape'&&serviceLayer.classList.contains('open'))resume()});
window.C04_ROUTE03={setMode,commitAnchor,retreat,openReturn,resume,state:()=>({behavior:app.dataset.behavior,reality:app.dataset.reality,digital:app.dataset.digital,scrollLeft:Math.round(worldScroll.scrollLeft),scrollTop:Math.round(worldScroll.scrollTop),sheetOpen:sheet.classList.contains('open'),serviceOpen:serviceLayer.classList.contains('open')})};
window.addEventListener('load',()=>{setTimeout(()=>{scrollWorldPct(.13,.5,false);setTimeout(()=>setBehavior('intent'),120)},20)});
