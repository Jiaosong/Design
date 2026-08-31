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
