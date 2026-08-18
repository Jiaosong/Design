window.__C04_ERRORS__=[];window.addEventListener('error',e=>window.__C04_ERRORS__.push(String(e.message||e.error||'error')));window.addEventListener('unhandledrejection',e=>window.__C04_ERRORS__.push('unhandledrejection:'+String(e.reason)));
const app=document.getElementById('app');
const worldScroll=document.getElementById('worldScroll');
const behaviorReadout=document.getElementById('behaviorReadout');
const readingModeReadout=document.getElementById('readingModeReadout');
const realityReadout=document.getElementById('realityReadout');
const sheet=document.getElementById('contextSheet');
const sheetTitle=document.getElementById('sheetTitle');
const sheetSummary=document.getElementById('sheetSummary');
const revealPanel=document.getElementById('revealPanel');
const revealText=document.getElementById('revealText');
const sheetState=document.getElementById('sheetState');
const stateBoundary=document.getElementById('stateBoundary');
const revealBtn=document.getElementById('revealBtn');
const panCue=document.getElementById('panCue');
const serviceLayer=document.getElementById('serviceLayer');
const setupLayer=document.getElementById('setupLayer');
const systemPanel=document.getElementById('systemPanel');
const returnGuard=document.getElementById('returnGuard');
const systemNote=document.getElementById('systemNote');
const scopeToast=document.getElementById('scopeToast');

const modeData={
 A:{label:'A · 推荐',title:'水布垭 → 游客中心',focus:[.13,.5],meta:'同一 ROUTE-03 关系骨架；方向改变，不重画路线。'},
 B:{label:'B · 逆向',title:'游客中心 → 水布垭',focus:[.88,.5],meta:'逆向阅读相同来源关系，不生成第二套几何。'},
 C:{label:'C · 短线',title:'游客中心 ↔ 蝴蝶崖',focus:[.57,.5],meta:'短线折返来自 ROUTE-03 模式说明；实时运营状态仍由正式来源决定。'},
 D:{label:'D · 短线',title:'游船码头 ↔ 蝴蝶崖',focus:[.54,.5],meta:'以码头为端点的短线关系；距离、坡度与通行状态不由本图证明。'}
};
const anchorData={
 dam:{pos:[.0753,.2661],title:'水布垭大坝',summary:'ROUTE-03 的西端关系节点。当前 App 只使用锁定图中的相对关系，不把它解释为 GPS 定位。',reveal:'从这里进入长线阅读时，界面仅改变视口与上下文，不改变锁定路线形状。实际到达方式、开放与换乘需由正式运营或现场信息确认。'},
 cliff:{pos:[.2697,.3048],title:'蝴蝶崖',summary:'ROUTE-03 中的折返关键点，同时出现在 C / D 短线模式中。',reveal:'它承担“是否继续长线”的关系判断，但本原型不把折返写成强制任务。十三印内容仍是可选阅读，且与现场精确邻近关系保持 FIELD OPEN。'},
 dock:{pos:[.8422,.6807],title:'游船码头',summary:'ROUTE-03 的水陆转换节点。服务与回程优先于内容触发。',reveal:'在水陆转换与回程阶段，Return Guard 保持可立即中断当前阅读。若正式状态不可得，界面维持 UNKNOWN，而不是绘制为正常开放。'},
 center:{pos:[.8809,.8613],title:'游客中心',summary:'ROUTE-03 的服务 / 回程优先节点，也是恢复路径的稳定入口。',reveal:'App 可以把这里作为信息恢复的关系锚点，但不模拟实时排队、营业、索道或船班。Digital OFF 时，纸图、标识、人工与真实景观仍应承担连续性。'}
};
const readingModes={
 QUICK:{label:'QUICK',button:'看一眼关系'},
 DEEP:{label:'DEEP',button:'展开来源关系'},
 FAMILY:{label:'FAMILY',button:'一起看关系'}
};
const realityNotes={
 OPEN:'测试 OPEN：仅用于原型行为验证，不代表现场当前开放。',
 DEGRADED:'DEGRADED：路线关系仍可读；可选深读暂停，优先确认现场与回程。',
 CLOSED:'CLOSED：停止可选深读；Return / Service 提升为主动作。',
 UNKNOWN:'UNKNOWN：不把未知写成正常开放；Return / Service 提升优先级。'
};
const frameworkStorageKey='c04.currentization.v02.framework';
let frameworkState={readingMode:'QUICK',setupSeen:false,offlinePrepared:true,generated:false,readLater:[]};
try{
 const saved=JSON.parse(localStorage.getItem(frameworkStorageKey)||'null');
 if(saved)frameworkState={...frameworkState,...saved};
}catch(e){}
const saveFrameworkState=()=>{try{localStorage.setItem(frameworkStorageKey,JSON.stringify(frameworkState))}catch(e){}};
app.dataset.readingMode=readingModes[frameworkState.readingMode]?frameworkState.readingMode:'QUICK';

let suppressScrollUntil=0;
let selectedAnchor=null;
let toastTimer=null;
let behaviorResetTimer=null;
let systemOpener=null;

const reducedMotion=()=>matchMedia('(prefers-reduced-motion: reduce)').matches;
const motionBehavior=()=>reducedMotion()?'auto':'smooth';
const reality=()=>app.dataset.reality||'UNKNOWN';
const digital=()=>app.dataset.digital||'FULL';
const readingMode=()=>app.dataset.readingMode||'QUICK';
const failClosed=()=>['CLOSED','UNKNOWN'].includes(reality());
const optionalRevealAllowed=()=>digital()!=='OFF' && reality()==='OPEN';

function showToast(text){
 scopeToast.textContent=text;scopeToast.classList.add('show');
 clearTimeout(toastTimer);toastTimer=setTimeout(()=>scopeToast.classList.remove('show'),2200);
}
function setBehavior(state){app.dataset.behavior=state;behaviorReadout.textContent=state.toUpperCase();}
function scrollWorldPct(xPct,yPct,announce=true){
 const maxX=Math.max(0,worldScroll.scrollWidth-worldScroll.clientWidth),maxY=Math.max(0,worldScroll.scrollHeight-worldScroll.clientHeight);
 const left=Math.max(0,Math.min(maxX,worldScroll.scrollWidth*xPct-worldScroll.clientWidth/2));
 const top=Math.max(0,Math.min(maxY,worldScroll.scrollHeight*yPct-worldScroll.clientHeight/2));
 suppressScrollUntil=performance.now()+480;
 worldScroll.scrollTo({left,top,behavior:motionBehavior()});
 if(announce)setBehavior('scout');
}
function syncGuard(){
 const st=reality();
 returnGuard.textContent=(st==='UNKNOWN'||st==='CLOSED')?`回程 · ${st}`:'回程';
 realityReadout.textContent=st==='OPEN'?'STATUS OPEN · TEST':`STATUS ${st}`;
 document.getElementById('serviceReality').textContent=st==='OPEN'?'OPEN · TEST ONLY / 非实时运营状态':`${st} · 不推断营业、排队或可通行状态`;
 systemNote.textContent=realityNotes[st];
 document.querySelectorAll('#realityControls button[data-reality]').forEach(b=>b.classList.toggle('active',b.dataset.reality===st));
}
function syncDigital(){
 const d=digital();
 document.getElementById('serviceDigital').textContent=d==='OFF'?'OFF · 数字解释退场；现场支持继续':d==='LIGHT'?'LIGHT · 轻量解释 / 路线优先':'FULL · 数字解释可用';
 document.querySelectorAll('#digitalControls button[data-digital]').forEach(b=>b.classList.toggle('active',b.dataset.digital===d));
}
function syncOptionalAccess(){
 const st=reality(),d=digital();
 const allowed=optionalRevealAllowed();
 revealBtn.disabled=!allowed;
 stateBoundary.hidden=allowed;
 if(allowed){
   stateBoundary.textContent='';
 }else if(d==='OFF'){
   stateBoundary.textContent='DIGITAL OFF：可选数字解释已退场；路线、回程与现场支持关系继续成立。';
 }else if(st==='DEGRADED'){
   stateBoundary.textContent='DEGRADED：保留路线关系，暂停可选深读；先确认现场与回程。';
 }else{
   stateBoundary.textContent=`${st}：不进入可选场景解释；先回程或确认正式现场信息。`;
 }
 if(!allowed){revealPanel.hidden=true;if(sheet.classList.contains('open'))sheetState.textContent=failClosed()?'HOLD':'COMMIT'}
 revealBtn.textContent=allowed?readingModes[readingMode()].button:'可选解释暂不可用';
}
function syncReadingMode(){
 const m=readingMode();readingModeReadout.textContent=m;
 document.querySelectorAll('.reading-options button[data-reading-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.readingMode===m)));
 syncOptionalAccess();
}
function setMode(mode){
 document.querySelectorAll('[data-mode]').forEach(b=>b.classList.toggle('active',b.dataset.mode===mode));
 const d=modeData[mode];document.getElementById('modeCode').textContent=d.label;document.getElementById('modeTitle').textContent=d.title;document.getElementById('modeMeta').textContent=d.meta;
 panCue.style.opacity='.35';scrollWorldPct(d.focus[0],d.focus[1],true);
}
function readingCopy(d){
 if(readingMode()==='QUICK')return d.reveal.split('。')[0]+'。';
 if(readingMode()==='FAMILY')return `一起先看“${d.title}”在路线里的位置，再决定要不要继续读。`+d.reveal.split('。')[0]+'。';
 return d.reveal;
}
function commitAnchor(id){
 selectedAnchor=id;
 document.querySelectorAll('.anchor').forEach(a=>a.classList.toggle('selected',a.dataset.anchor===id));
 const d=anchorData[id];setBehavior('commit');scrollWorldPct(d.pos[0],d.pos[1],false);
 sheetTitle.textContent=d.title;sheetSummary.textContent=d.summary;revealText.textContent=readingCopy(d);revealPanel.hidden=true;sheetState.textContent=failClosed()?'HOLD':'COMMIT';syncOptionalAccess();
 const open=()=>{sheet.classList.add('open');sheet.setAttribute('aria-hidden','false')};
 if(reducedMotion())open();else setTimeout(open,260);
}
function retreat(){
 selectedAnchor=null;sheet.classList.remove('open');sheet.setAttribute('aria-hidden','true');revealPanel.hidden=true;document.querySelectorAll('.anchor').forEach(a=>a.classList.remove('selected'));setBehavior('retreat');
 clearTimeout(behaviorResetTimer);behaviorResetTimer=setTimeout(()=>setBehavior('intent'),reducedMotion()?0:260);
}
function openReturn(){
 clearTimeout(behaviorResetTimer);
 serviceLayer.classList.add('open');serviceLayer.setAttribute('aria-hidden','false');sheet.classList.remove('open');sheet.setAttribute('aria-hidden','true');revealPanel.hidden=true;document.querySelectorAll('.anchor').forEach(a=>a.classList.remove('selected'));selectedAnchor=null;setBehavior('return');document.querySelectorAll('[data-nav]').forEach(b=>b.classList.toggle('active',b.dataset.nav==='service'));
}
function resume(){
 serviceLayer.classList.remove('open');serviceLayer.setAttribute('aria-hidden','true');setBehavior('intent');document.querySelectorAll('[data-nav]').forEach(b=>b.classList.toggle('active',b.dataset.nav==='route'));
}
function setReadingMode(mode){
 if(!readingModes[mode])mode='QUICK';app.dataset.readingMode=mode;frameworkState.readingMode=mode;saveFrameworkState();syncReadingMode();
 if(selectedAnchor)revealText.textContent=readingCopy(anchorData[selectedAnchor]);
}
function setDigitalMode(mode){
 if(!['FULL','LIGHT','OFF'].includes(mode))mode='LIGHT';
 app.dataset.digital=mode;syncDigital();syncOptionalAccess();
 if(mode==='OFF'){
   if(sheet.classList.contains('open')||selectedAnchor){
     sheet.classList.remove('open');sheet.setAttribute('aria-hidden','true');revealPanel.hidden=true;
     document.querySelectorAll('.anchor').forEach(a=>a.classList.remove('selected'));selectedAnchor=null;
     setBehavior('retreat');clearTimeout(behaviorResetTimer);behaviorResetTimer=setTimeout(()=>setBehavior('intent'),reducedMotion()?0:220);
   }
   showToast('Digital OFF：数字解释退场，路线与 Return 保留。');
 }
}
function setReality(state){
 if(!['OPEN','DEGRADED','CLOSED','UNKNOWN'].includes(state))state='UNKNOWN';app.dataset.reality=state;syncGuard();syncOptionalAccess();
 if(['CLOSED','UNKNOWN'].includes(state)&&!systemPanel.classList.contains('open')&&!setupLayer.classList.contains('open'))openReturn();
}
function openSetup(step='mode'){
 clearTimeout(behaviorResetTimer);setBehavior('intent');
 serviceLayer.classList.remove('open');serviceLayer.setAttribute('aria-hidden','true');
 setupLayer.classList.add('open');setupLayer.setAttribute('aria-hidden','false');
 document.querySelectorAll('[data-setup-step]').forEach(x=>x.classList.toggle('active',x.dataset.setupStep===step));
 syncReadingMode();setTimeout(()=>setupLayer.querySelector('.setup-step.active button')?.focus({preventScroll:true}),0);
}
function finishSetup(mode){setReadingMode(mode||readingMode());frameworkState.setupSeen=true;frameworkState.offlinePrepared=true;saveFrameworkState();setupLayer.classList.remove('open');setupLayer.setAttribute('aria-hidden','true');resume();worldScroll.focus({preventScroll:true});}
function resetSetup(){frameworkState.setupSeen=false;saveFrameworkState();openSetup('mode');}
function startJourney(){
 if(failClosed()){openReturn();return 'SERVICE_FAIL_CLOSED'}
 if(frameworkState.setupSeen){resume();return 'ROUTE'}
 openSetup('mode');return 'APP_INIT'
}
function openSystem(){systemOpener=document.activeElement;systemPanel.classList.add('open');systemPanel.setAttribute('aria-hidden','false');document.getElementById('systemClose').focus({preventScroll:true});}
function closeSystem(){systemPanel.classList.remove('open');systemPanel.setAttribute('aria-hidden','true');if(failClosed())openReturn();else if(systemOpener?.focus)systemOpener.focus({preventScroll:true});}

document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>setMode(b.dataset.mode)));
document.querySelectorAll('.anchor').forEach(a=>{
 a.addEventListener('pointerenter',()=>{if(!sheet.classList.contains('open')&&digital()!=='OFF')setBehavior('scout')});
 a.addEventListener('focus',()=>{if(!sheet.classList.contains('open')&&digital()!=='OFF')setBehavior('scout')});
 a.addEventListener('click',()=>commitAnchor(a.dataset.anchor));
});
document.querySelectorAll('.reading-options button[data-reading-mode]').forEach(b=>b.addEventListener('click',()=>setReadingMode(b.dataset.readingMode)));
document.querySelectorAll('#realityControls button[data-reality]').forEach(b=>b.addEventListener('click',()=>setReality(b.dataset.reality)));
document.querySelectorAll('#digitalControls button[data-digital]').forEach(b=>b.addEventListener('click',()=>setDigitalMode(b.dataset.digital)));
document.getElementById('setupNext').addEventListener('click',()=>openSetup('offline'));
document.getElementById('setupSkip').addEventListener('click',()=>openSetup('offline'));
document.getElementById('setupEnter').addEventListener('click',()=>finishSetup());
document.getElementById('systemTrigger').addEventListener('click',openSystem);
document.getElementById('systemClose').addEventListener('click',closeSystem);
document.getElementById('retreatBtn').addEventListener('click',retreat);
revealBtn.addEventListener('click',()=>{
 if(!optionalRevealAllowed()){showToast(stateBoundary.textContent||'可选解释当前不可用。');return}
 revealPanel.hidden=false;revealText.textContent=selectedAnchor?readingCopy(anchorData[selectedAnchor]):revealText.textContent;revealBtn.textContent='关系说明已展开';sheetState.textContent='REVEAL';setBehavior('reveal');
});
returnGuard.addEventListener('click',openReturn);
document.getElementById('serviceStatusBtn').addEventListener('click',openSystem);
document.getElementById('resumeRoute').addEventListener('click',startJourney);
document.querySelectorAll('[data-nav]').forEach(b=>b.addEventListener('click',()=>{
 const target=b.dataset.nav;
 if(target==='service')return openReturn();
 if(target==='route')return startJourney();
 showToast(target==='today'?'TODAY 继承 v1.27 主导航；本 bounded build 只验证 ROUTE。':'MY BOOK 继承 v1.27 主导航；本 bounded build 不伪造完整内容页。');
}));
worldScroll.addEventListener('scroll',()=>{panCue.style.opacity='.22';if(performance.now()<suppressScrollUntil)return;if(app.dataset.behavior==='intent')setBehavior('scout')},{passive:true});
worldScroll.addEventListener('keydown',e=>{
 if(e.key==='ArrowRight')worldScroll.scrollBy({left:120,behavior:motionBehavior()});
 if(e.key==='ArrowLeft')worldScroll.scrollBy({left:-120,behavior:motionBehavior()});
 if(e.key==='Escape'&&sheet.classList.contains('open'))retreat();
});
window.addEventListener('keydown',e=>{
 if(e.key!=='Escape')return;
 if(systemPanel.classList.contains('open'))return closeSystem();
 if(serviceLayer.classList.contains('open'))return resume();
 if(setupLayer.classList.contains('open'))return finishSetup('QUICK');
});

window.C04_ROUTE03={
 setMode,commitAnchor,retreat,openReturn,resume,startJourney,openSetup,setReadingMode,setDigitalMode,setReality,finishSetup,resetSetup,openSystem,closeSystem,
 state:()=>({
   behavior:app.dataset.behavior,reality:reality(),digital:digital(),readingMode:readingMode(),
   scrollLeft:Math.round(worldScroll.scrollLeft),scrollTop:Math.round(worldScroll.scrollTop),
   sheetOpen:sheet.classList.contains('open'),revealOpen:!revealPanel.hidden,revealDisabled:revealBtn.disabled,
   serviceOpen:serviceLayer.classList.contains('open'),setupOpen:setupLayer.classList.contains('open'),systemOpen:systemPanel.classList.contains('open'),setupSeen:frameworkState.setupSeen
 })
};
window.__C04_FRAMEWORK_CURRENTIZED__={
 version:'v0.2',architectureAncestor:'v1.26',navigationSuccessor:'v1.27',
 getReadingMode:readingMode,setReadingMode,setDigitalMode,setReality,getState:()=>JSON.parse(JSON.stringify(frameworkState)),
 modeIsPersona:false,routeAuthority:'ROUTE-03 = LOCKED CURRENT'
};

window.addEventListener('load',()=>{
 setupLayer.classList.remove('open');setupLayer.setAttribute('aria-hidden','true');
 syncReadingMode();syncDigital();syncGuard();syncOptionalAccess();
 setTimeout(()=>{scrollWorldPct(.13,.5,false);setTimeout(()=>{setBehavior('intent');startJourney()},120)},20);
});
