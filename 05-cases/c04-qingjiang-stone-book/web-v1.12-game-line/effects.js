(()=>{
  const motionQuery=window.matchMedia('(prefers-reduced-motion: reduce)');
  const clamp=(value,min=0,max=1)=>Math.min(max,Math.max(min,value));
  const lerp=(a,b,t)=>a+(b-a)*t;
  const sectionProgress=element=>{
    if(!element) return 0;
    const rect=element.getBoundingClientRect();
    const viewport=window.innerHeight||1;
    return clamp((viewport-rect.top)/(viewport+rect.height));
  };

  const publicTextMap=new Map([
    ['原资产','清江与路线'],
    ['设计创意','水上 · 空中 · 山中'],
    ['设计系统','十三印'],
    ['技术路线','如何成立'],
    ['AI + 3D','AI 探索'],
    ['创新与难点','关键取舍'],
    ['ORIGINAL MATERIAL / EXISTING ASSETS','QINGJIANG / ROUTE / EXISTING WORK'],
    ['DESIGN QUESTION','ROUTE / ATTENTION / RETURN'],
    ['DESIGN IDEA / THREE SCALES','WATER / AIR / BODY'],
    ['DESIGN THINKING / ATTENTION','LANDSCAPE / ATTENTION'],
    ['TASK FLOW / WORKFLOW','SOURCE / ROUTE / SCENE / PROTOTYPE'],
    ['从原始证据到最终作品，\n每一步都有明确任务。','路线、场景、界面与构造，\n沿同一次清江游程接到一起。'],
    ['这里展示的是实际项目任务链，而不是通用设计方法模板。每一阶段都必须改变下一步设计判断，并能回到来源检查。','官方导览、路线和既有资产先确定空间关系；场景、界面、实体与模型随后进入同一游程，并在每个关键节点回到来源核对。']
  ]);

  function replaceExactText(element,next){
    if(!element||element.dataset.publicVoiceRepaired==='true') return;
    element.textContent=next;
    element.dataset.publicVoiceRepaired='true';
  }

  function applyPublicVoiceRepair(){
    document.title='清江石书｜一次从水上、空中到山中的清江游程';
    const meta=document.querySelector('meta[name="description"]');
    meta?.setAttribute('content','清江石书把游船、索道、步行、十三印、回程、数字与纸本记忆组织进同一次清江游程。');

    document.querySelectorAll('.mainnav a').forEach(link=>{
      const next=publicTextMap.get(link.textContent.trim());
      if(next) replaceExactText(link,next);
    });

    document.querySelectorAll('.kicker').forEach(kicker=>{
      const next=publicTextMap.get(kicker.textContent.trim());
      if(next) replaceExactText(kicker,next);
    });

    const workflow=document.querySelector('#workflow .section-head');
    if(workflow){
      const heading=workflow.querySelector('h2');
      const summary=workflow.querySelector(':scope > p');
      if(heading) replaceExactText(heading,'路线、场景、界面与构造，\n沿同一次清江游程接到一起。');
      if(summary) replaceExactText(summary,'官方导览、路线和既有资产先确定空间关系；场景、界面、实体与模型随后进入同一游程，并在每个关键节点回到来源核对。');
    }
  }

  function applyCurrentAssetBindings(){
    const bindings=[
      ['img[src$="hero_qingjiang.jpg"]','https://www.eslygroup.com/uploadfile/image/20230718/v0ii0wjlhe.jpg','跨清江索道与清江河谷官方摄影'],
      ['img[src$="r06_qingjiang.jpg"]','https://www.eslygroup.com/uploadfile/image/20240522/1cce70abb.jpg','云雾中的清江河谷与田地官方摄影'],
      ['img[src$="r13_passage_sequence.png"]','assets/r13_passage_sequence_current.svg','R13 接近、收束、通过、回看注意力序列'],
      ['img[src$="brand_journey_current.svg"]','assets/brand_system_current.svg','清江路线、印、页与痕迹的品牌应用系统'],
      ['img[src*="M01_qingjiang_journal_v1_2.svg"]','assets/memory_journal_current.svg','清江旅记纸本记忆使用态'],
      ['img[src$="physical_body_support_hold.svg"]','assets/body_need_scenarios_current.svg','走、停、倚、恢复的身体需求场景']
    ];
    bindings.forEach(([selector,src,alt])=>{
      document.querySelectorAll(selector).forEach(image=>{
        image.src=src;
        image.alt=alt;
        image.dataset.currentAssetBinding='true';
      });
    });
  }

  function injectTechnicalProof(){
    if(document.querySelector('#technical')) return;
    const memory=document.querySelector('#memory');
    if(!memory) return;

    const section=document.createElement('section');
    section.id='technical';
    section.className='section split dark';
    section.dataset.section='11';
    section.innerHTML='<div class="media-panel"><img class="contain" src="assets/technical_focus_v2.svg" alt="R06 技术证明关系：空间关系、人体尺度、构件顺序与维护接口" /></div><div class="copy-panel"><p class="kicker">TECHNICAL PROOF / R06</p><h2>技术层不是为了显得复杂，<br />而是回答它怎样成立。</h2><p>景观与体验先成立，技术证明随后检查空间关系、人体尺度、构件顺序与维护接口。当前公开层只呈现可以诚实说明的设计关系，不把尚未绑定的尺寸、锚固、基础或现场数据画成已确定事实。</p><ol class="step-list"><li><b>空间关系</b><span>路径、停留、视线与占用是否冲突。</span></li><li><b>人体尺度</b><span>倚靠、通过和短恢复是否自然。</span></li><li><b>构件顺序</b><span>结构、表面与连接是否能逐层核对。</span></li><li><b>维护接口</b><span>拆换、检查与后续进入是否被预留。</span></li></ol><p class="truth-note">研究级设计表达｜NTS｜现场尺寸、结构、安全与施工结论继续交后续专业验证</p></div>';
    memory.before(section);

    memory.dataset.section='12';
    const final=document.querySelector('#final');
    if(final) final.dataset.section='13';
    const counter=document.querySelector('#sectionNow');
    if(counter) counter.textContent='01 / 13';

    const nav=document.querySelector('.mainnav');
    if(nav&&!nav.querySelector('a[href="#technical"]')){
      const anchor=document.createElement('a');
      anchor.href='#technical';
      anchor.textContent='技术';
      const memoryLink=nav.querySelector('a[href="#memory"]');
      memoryLink?nav.insertBefore(anchor,memoryLink):nav.append(anchor);
    }
  }

  applyPublicVoiceRepair();
  applyCurrentAssetBindings();
  injectTechnicalProof();

  const root=document.documentElement;
  const hero=document.querySelector('#hero');
  const finalSection=document.querySelector('#final');
  const thinking=document.querySelector('#thinking');
  const digital=document.querySelector('#digital');
  const scenes=document.querySelector('#scenes');
  const thinkingSteps=[...document.querySelectorAll('#thinking .step-list li')];
  const digitalPhone=document.querySelector('#digital .phone');
  const digitalQuote=document.querySelector('#digital .large-quote');
  const sceneImages=[...document.querySelectorAll('#scenes .scene-pair img')];

  function resetMotionState(){
    root.classList.remove('motion-ready');
    hero?.style.removeProperty('--hero-media-y');
    hero?.style.removeProperty('--hero-media-scale');
    hero?.style.removeProperty('--hero-copy-y');
    hero?.style.removeProperty('--hero-copy-alpha');
    finalSection?.style.removeProperty('--return-media-y');
    finalSection?.style.removeProperty('--return-media-scale');
    finalSection?.style.removeProperty('--return-copy-y');
    digitalPhone?.style.removeProperty('--digital-y');
    digitalPhone?.style.removeProperty('--digital-scale');
    digitalPhone?.style.removeProperty('--digital-alpha');
    digitalQuote?.style.removeProperty('--digital-quote-opacity');
    digitalQuote?.style.removeProperty('--digital-quote-x');
    thinkingSteps.forEach(step=>step.classList.remove('is-current'));
    thinking?.classList.remove('effect-attention-active');
    sceneImages.forEach(image=>image.style.removeProperty('--scene-shift'));
  }

  function activateMotion(){
    if(motionQuery.matches){
      resetMotionState();
      return;
    }
    root.classList.add('motion-ready');
  }

  let ticking=false;
  function syncMotion(){
    ticking=false;
    if(motionQuery.matches) return;

    const viewport=window.innerHeight||1;
    const heroProgress=clamp(window.scrollY/(viewport*.92));
    if(hero){
      hero.style.setProperty('--hero-media-y',`${lerp(0,30,heroProgress).toFixed(2)}px`);
      hero.style.setProperty('--hero-media-scale',lerp(1.045,1.018,heroProgress).toFixed(4));
      hero.style.setProperty('--hero-copy-y',`${lerp(0,-20,heroProgress).toFixed(2)}px`);
      hero.style.setProperty('--hero-copy-alpha',lerp(1,.72,heroProgress).toFixed(3));
    }

    const thinkingProgress=sectionProgress(thinking);
    if(thinkingSteps.length){
      const local=clamp((thinkingProgress-.12)/.72);
      const current=Math.min(thinkingSteps.length-1,Math.floor(local*thinkingSteps.length));
      const attentionActive=thinkingProgress>.08&&thinkingProgress<.93;
      thinkingSteps.forEach((step,index)=>step.classList.toggle('is-current',index===current&&attentionActive));
      thinking?.classList.toggle('effect-attention-active',attentionActive);
    }

    const digitalProgress=sectionProgress(digital);
    if(digitalPhone){
      const enter=clamp((digitalProgress-.06)/.28);
      const retreat=clamp((digitalProgress-.62)/.24);
      digitalPhone.style.setProperty('--digital-y',`${lerp(24,-10,enter)+lerp(0,-18,retreat)}px`);
      digitalPhone.style.setProperty('--digital-scale',String(lerp(.975,1,enter)-retreat*.035));
      digitalPhone.style.setProperty('--digital-alpha',String(lerp(.82,1,enter)-retreat*.38));
    }
    if(digitalQuote){
      const quoteAlpha=clamp((digitalProgress-.56)/.2);
      digitalQuote.style.setProperty('--digital-quote-opacity',(0.32+quoteAlpha*0.68).toFixed(3));
      digitalQuote.style.setProperty('--digital-quote-x',`${((1-quoteAlpha)*18).toFixed(2)}px`);
    }

    const sceneProgress=sectionProgress(scenes);
    sceneImages.forEach((image,index)=>{
      const direction=index===0?-1:1;
      const shift=(sceneProgress-.5)*18*direction;
      image.style.setProperty('--scene-shift',`${shift.toFixed(2)}px`);
    });

    const finalProgress=sectionProgress(finalSection);
    if(finalSection){
      const local=clamp((finalProgress-.05)/.8);
      finalSection.style.setProperty('--return-media-y',`${lerp(-18,18,local).toFixed(2)}px`);
      finalSection.style.setProperty('--return-media-scale',lerp(1.045,1.018,local).toFixed(4));
      finalSection.style.setProperty('--return-copy-y',`${lerp(22,0,clamp((local-.08)/.55)).toFixed(2)}px`);
    }
  }

  function requestSync(){
    if(ticking) return;
    ticking=true;
    window.requestAnimationFrame(syncMotion);
  }

  activateMotion();
  requestSync();
  window.addEventListener('scroll',requestSync,{passive:true});
  window.addEventListener('resize',requestSync);
  motionQuery.addEventListener?.('change',()=>{activateMotion();requestSync();});
})();
