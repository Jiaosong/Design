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
    ['AI + 3D','模型与构造'],
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

  function bindDistinctDigitalView(){
    const finalView=document.querySelector('#digital .app-mybook-carrier');
    if(!finalView) return;
    finalView.src='support/C04_APP_V1_6_MY_BOOK_FINAL_VIEW.html';
    finalView.title='清江石书 我的石书最终展示界面';
    finalView.dataset.presentationRole='final-view';
  }

  applyPublicVoiceRepair();
  bindDistinctDigitalView();

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
