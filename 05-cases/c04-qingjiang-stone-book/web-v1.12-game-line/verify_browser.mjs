import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';

const root=path.dirname(fileURLToPath(import.meta.url));
const outDir=path.join(root,'browser-readback');
fs.rmSync(outDir,{recursive:true,force:true});
fs.mkdirSync(outDir,{recursive:true});

const baseUrl=process.env.C04_BROWSER_URL||'http://127.0.0.1:4173/index.html';
const expectedSections=['hero','assets','journey','brief','context','audience','idea','thinking','systems','brand-system','memory-system','development','r13','final'];
const cases=[
  {name:'desktop-1920x1080',viewport:{width:1920,height:1080},anchors:expectedSections},
  {name:'desktop-1366x768',viewport:{width:1366,height:768},anchors:['hero','journey','context','thinking','systems','brand-system','memory-system','development','r13','final']},
  {name:'mobile-390x844',viewport:{width:390,height:844},anchors:['hero','assets','journey','audience','systems','brand-system','memory-system','development','r13','final']}
];

const report={
  schema:'C04_CURRENTIZED_BROWSER_READBACK_V2',
  generated_at:new Date().toISOString(),
  source_url:baseUrl,
  status:'RUNNING',
  expected_sections:expectedSections,
  cases:[],
  reduced_motion:null,
  failures:[],
  design_review_open_items:[]
};
const fail=(message,details={})=>report.failures.push({message,...details});
const browser=await chromium.launch({headless:true});

async function settle(page){
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1200);
  await page.evaluate(async()=>{if(document.fonts?.ready)await document.fonts.ready;});
  await page.waitForTimeout(200);
}
async function shot(page,dir,id){
  const el=page.locator(`#${id}`);
  if(await el.count()===0){fail(`Missing section #${id}`);return false;}
  await page.evaluate(sectionId=>document.getElementById(sectionId)?.scrollIntoView({block:'start',behavior:'instant'}),id);
  await page.waitForTimeout(800);
  await page.screenshot({path:path.join(dir,`${id}.png`),fullPage:false});
  return true;
}

try{
  for(const item of cases){
    const mobile=item.name.startsWith('mobile-');
    const context=await browser.newContext({viewport:item.viewport,deviceScaleFactor:1,hasTouch:mobile});
    const page=await context.newPage();
    const pageErrors=[];
    page.on('pageerror',e=>pageErrors.push(String(e?.message||e)));
    const caseResult={name:item.name,viewport:item.viewport,screenshots:[],page_errors:pageErrors};

    try{
      const response=await page.goto(baseUrl,{waitUntil:'domcontentloaded',timeout:30000});
      if(!response||response.status()>=400)fail('Page navigation failed',{case:item.name,status:response?.status?.()??null});
      await settle(page);

      const metrics=await page.evaluate(()=>({
        viewportWidth:innerWidth,
        documentWidth:document.documentElement.scrollWidth,
        bodyWidth:document.body.scrollWidth,
        sectionIds:[...document.querySelectorAll('.section[id]')].map(x=>x.id),
        hero:!!document.querySelector('#hero h2'),
        topbar:!!document.querySelector('.topbar')&&getComputedStyle(document.querySelector('.topbar')).display!=='none',
        missingImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.getAttribute('src')||i.src),
        heroLocalBound:document.querySelector('#heroImage')?.classList.contains('loaded')||false,
        stateText:document.querySelector('#context')?.textContent||'',
        optionalReadingText:document.querySelector('#idea')?.textContent||'',
        fullScopeDetails:!!document.querySelector('details.professional'),
        r13Present:!!document.querySelector('#r13 .r13-figure img'),
        r13LocationText:document.querySelector('#r13 .r13-location')?.textContent||'',
        physicalCarrier:document.querySelector('.physical-transfer img')?.getAttribute('src')||'',
        stateScope:document.querySelector('.state-sim')?.dataset.scope||'',
        stateBoundary:document.querySelector('.state-boundary')?.textContent||''
        ,brandMainAsset:document.querySelector('#brand-system img')?.getAttribute('src')||''
        ,memoryMainAsset:document.querySelector('#memory-system img')?.getAttribute('src')||''
        ,brandText:document.querySelector('#brand-system')?.textContent||''
        ,memoryText:document.querySelector('#memory-system')?.textContent||''
      }));
      const overflow=Math.max(metrics.documentWidth,metrics.bodyWidth)-metrics.viewportWidth;
      if(overflow>2)fail('Horizontal overflow exceeds 2px',{case:item.name,overflow});
      if(JSON.stringify(metrics.sectionIds)!==JSON.stringify(expectedSections))fail('Current section spine mismatch',{case:item.name,sectionIds:metrics.sectionIds});
      if(!metrics.hero||!metrics.topbar)fail('Primary reading chrome missing',{case:item.name});
      if(metrics.missingImages.length)fail('Image failed to load',{case:item.name,missingImages:metrics.missingImages});
      if(!metrics.heroLocalBound)fail('Local Qingjiang hero binding did not complete',{case:item.name});
      if(!['UNKNOWN','FULL / LIGHT / OFF'].every(x=>metrics.stateText.includes(x)))fail('State/fallback truth content missing',{case:item.name});
      if(!metrics.optionalReadingText.includes('十三印可以不读完'))fail('Optional-reading boundary missing',{case:item.name});
      if(!metrics.r13Present||!['当前位置','R13','收束通过'].every(x=>metrics.r13LocationText.includes(x)))fail('R13 current-location relation missing',{case:item.name,r13LocationText:metrics.r13LocationText});
      if(metrics.physicalCarrier!=='assets/physical_body_support_hold.svg')fail('P01-B finished carrier is not bound in Development',{case:item.name,physicalCarrier:metrics.physicalCarrier});
      if(metrics.brandMainAsset!=='assets/brand_system_current.svg'||!metrics.brandText.includes('LINE / PAGE / SEAL / TRACE'))fail('Independent Brand MAIN surface is not bound to current editable carrier',{case:item.name,brandMainAsset:metrics.brandMainAsset});
      if(metrics.memoryMainAsset!=='assets/memory_journal_current.svg'||!metrics.memoryText.includes('MEMORY / IP / AFTER LEAVING'))fail('Independent Memory MAIN surface is not bound to current editable carrier',{case:item.name,memoryMainAsset:metrics.memoryMainAsset});
      if(metrics.stateScope!=='explanatory-simulation'||!metrics.stateBoundary.includes('不表示实时运营状态'))fail('Operational state boundary is not explicitly explanatory',{case:item.name,stateScope:metrics.stateScope,stateBoundary:metrics.stateBoundary});

      const dir=path.join(outDir,item.name);
      fs.mkdirSync(dir,{recursive:true});
      for(const id of item.anchors){if(await shot(page,dir,id))caseResult.screenshots.push(`${item.name}/${id}.png`);}

      await page.locator('#journey').scrollIntoViewIfNeeded();
      const modeBefore=(await page.locator('#modeTitle').textContent())?.trim()||'';
      await page.locator('.mode-card[data-mode="cable"]').click();
      const modeAfter=(await page.locator('#modeTitle').textContent())?.trim()||'';
      const activeMode=await page.locator('.mode-card[data-mode="cable"]').evaluate(el=>el.classList.contains('active'));
      if(!modeBefore||!modeAfter||modeBefore===modeAfter||!activeMode)fail('Journey scale interaction failed',{case:item.name,modeBefore,modeAfter,activeMode});

      await page.locator('#audience').scrollIntoViewIfNeeded();
      const audienceButtons=page.locator('.audience-tab');
      if(await audienceButtons.count()<2){
        fail('Audience depth controls missing',{case:item.name});
      }else{
        await audienceButtons.nth(1).click();
        const activeAudience=await audienceButtons.nth(1).evaluate(el=>el.classList.contains('active'));
        if(!activeAudience)fail('Audience depth interaction failed',{case:item.name});
      }

      const details=page.locator('details.professional');
      if(await details.count()===0){
        fail('Full-scope progressive disclosure missing',{case:item.name});
      }else{
        if(!(await details.evaluate(el=>el.open)))await details.locator('summary').click();
        if(!(await details.evaluate(el=>el.open)))fail('Full-scope progressive disclosure did not open',{case:item.name});
      }

      if(mobile){
        const toggle=page.locator('.nav-toggle');
        await toggle.click();
        const expanded=await toggle.getAttribute('aria-expanded');
        const hidden=await page.locator('#mobileNav').evaluate(el=>el.hidden);
        if(expanded!=='true'||hidden)fail('Mobile navigation did not open',{case:item.name,expanded,hidden});
        await page.locator('#mobileNav a[href="#systems"]').click();
        await page.waitForTimeout(120);
        if((await toggle.getAttribute('aria-expanded'))!=='false')fail('Mobile navigation did not close after selection',{case:item.name});
      }else{
        await page.locator('#systems').scrollIntoViewIfNeeded();
        await page.waitForTimeout(180);
        const activeHref=await page.locator('.layer-nav a.active').getAttribute('href').catch(()=>null);
        if(activeHref!=='#systems')fail('Current navigation state did not follow systems section',{case:item.name,activeHref});
      }

      await page.locator('#r13').scrollIntoViewIfNeeded();
      await page.waitForTimeout(180);
      const r13Nav=mobile
        ? await page.locator('#mobileNav a[href="#development"]').evaluate(el=>({active:el.classList.contains('active'),current:el.getAttribute('aria-current')}))
        : await page.locator('.layer-nav a[href="#development"]').evaluate(el=>({active:el.classList.contains('active'),current:el.getAttribute('aria-current'),cue:getComputedStyle(el,'::after').content}));
      if(!r13Nav.active||r13Nav.current!=='location')fail('R13 is not connected to current navigation location',{case:item.name,r13Nav});
      if(!mobile&&!String(r13Nav.cue).includes('当前'))fail('R13 navigation lacks a non-color current-location cue',{case:item.name,r13Nav});
      caseResult.r13_navigation=r13Nav;

      await page.locator('#hero').scrollIntoViewIfNeeded();
      const y0=await page.evaluate(()=>scrollY);
      if(mobile)await page.evaluate(()=>scrollBy(0,Math.min(innerHeight*.72,620)));
      else await page.keyboard.press('PageDown');
      await page.waitForTimeout(250);
      const y1=await page.evaluate(()=>scrollY);
      if(y1<=y0+20)fail('Reading sequence did not advance',{case:item.name,y0,y1});

      caseResult.metrics=metrics;
      caseResult.horizontal_overflow_px=overflow;
      caseResult.journey_mode_interaction=modeBefore!==modeAfter&&activeMode;
      caseResult.page_errors=pageErrors;
      if(pageErrors.length)fail('Page runtime errors',{case:item.name,pageErrors});
    }catch(err){
      fail('Unhandled browser case exception',{case:item.name,error:String(err?.stack||err)});
    }finally{
      report.cases.push(caseResult);
      await context.close();
    }
  }

  const ctx=await browser.newContext({viewport:{width:1366,height:768},reducedMotion:'reduce'});
  const page=await ctx.newPage();
  try{
    await page.goto(baseUrl,{waitUntil:'domcontentloaded'});
    await settle(page);
    const reduced=await page.evaluate(()=>({
      mediaQueryMatches:matchMedia('(prefers-reduced-motion: reduce)').matches,
      scrollBehavior:getComputedStyle(document.documentElement).scrollBehavior,
      modeTransition:getComputedStyle(document.querySelector('.mode-card')).transitionDuration
    }));
    if(!reduced.mediaQueryMatches)fail('Reduced-motion preference not applied',{reduced});
    if(reduced.modeTransition!=='0s')fail('Motion transition remains under reduced motion',{reduced});
    report.reduced_motion=reduced;
  }catch(err){
    fail('Reduced-motion readback exception',{error:String(err?.stack||err)});
  }finally{
    await ctx.close();
  }
}finally{
  await browser.close();
}

report.design_review_open_items=[
  'Brand/Memory independent MAIN surfaces now exist and are browser-covered; independent Design Crit still decides presentation KEEP/REVISE.',
  'P01-B remains a candidate/development carrier; browser coverage does not grant engineering or project FINAL_KEEP.'
];
report.status=report.failures.length?'FAIL':'PASS';
fs.writeFileSync(path.join(outDir,'report.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
if(report.failures.length)process.exit(1);
