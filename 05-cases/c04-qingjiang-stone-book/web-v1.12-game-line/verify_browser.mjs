import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright';
const root=path.dirname(fileURLToPath(import.meta.url));
const outDir=path.join(root,'browser-readback');
fs.rmSync(outDir,{recursive:true,force:true});fs.mkdirSync(outDir,{recursive:true});
const baseUrl=process.env.C04_BROWSER_URL||'http://127.0.0.1:4173/index.html';
const cases=[
 {name:'desktop-1920x1080',viewport:{width:1920,height:1080},anchors:['hero','assets','context','thinking','scenes','digital','physical','technical','final']},
 {name:'desktop-1366x768',viewport:{width:1366,height:768},anchors:['hero','journey','system','brandmemory','memory','final']},
 {name:'mobile-390x844',viewport:{width:390,height:844},anchors:['hero','assets','digital','physical','final']}
];
const report={schema:'C04_COMPLETE_SIMPLIFIED_BROWSER_READBACK_V1',generated_at:new Date().toISOString(),source_url:baseUrl,status:'RUNNING',cases:[],reduced_motion:null,failures:[]};
const fail=(message,details={})=>report.failures.push({message,...details});
async function settle(page){await page.waitForLoadState('domcontentloaded');await page.waitForTimeout(1400);await page.evaluate(async()=>{if(document.fonts?.ready)await document.fonts.ready;});await page.waitForTimeout(250);}
async function shot(page,dir,id){const el=page.locator(`#${id}`);if(await el.count()===0){fail(`Missing section #${id}`);return;}await el.scrollIntoViewIfNeeded();await page.waitForTimeout(160);await page.screenshot({path:path.join(dir,`${id}.png`),fullPage:false});}
const browser=await chromium.launch({headless:true});
try{
 for(const item of cases){
  const mobile=item.name.startsWith('mobile-');const context=await browser.newContext({viewport:item.viewport,deviceScaleFactor:1,hasTouch:mobile});const page=await context.newPage();const pageErrors=[];page.on('pageerror',e=>pageErrors.push(String(e?.message||e)));
  const response=await page.goto(baseUrl,{waitUntil:'domcontentloaded',timeout:30000});if(!response||response.status()>=400)fail('Page navigation failed',{case:item.name,status:response?.status?.()??null});await settle(page);
  const metrics=await page.evaluate(()=>({viewportWidth:innerWidth,documentWidth:document.documentElement.scrollWidth,bodyWidth:document.body.scrollWidth,sectionCount:document.querySelectorAll('.section').length,hero:!!document.querySelector('#hero h2'),topbar:getComputedStyle(document.querySelector('.topbar')).display!=='none',missingImages:[...document.images].filter(i=>!i.complete||i.naturalWidth===0).map(i=>i.src),heroLocalBound:document.querySelector('#heroImage')?.classList.contains('loaded')||false,r06LocalBound:document.querySelector('#r06Image')?.classList.contains('loaded')||false}));
  const overflow=Math.max(metrics.documentWidth,metrics.bodyWidth)-metrics.viewportWidth;if(overflow>2)fail('Horizontal overflow exceeds 2px',{case:item.name,overflow});if(metrics.sectionCount!==18)fail('Unexpected reading-section count',{case:item.name,count:metrics.sectionCount});if(!metrics.hero||!metrics.topbar)fail('Primary reading chrome missing',{case:item.name});if(metrics.missingImages.length)fail('Image failed to load',{case:item.name,missingImages:metrics.missingImages});if(!metrics.heroLocalBound||!metrics.r06LocalBound)fail('Local QJ-D raster binding did not complete',{case:item.name,hero:metrics.heroLocalBound,r06:metrics.r06LocalBound});
  const dir=path.join(outDir,item.name);fs.mkdirSync(dir,{recursive:true});for(const id of item.anchors)await shot(page,dir,id);
  await page.locator('#imprints').scrollIntoViewIfNeeded();const before=(await page.locator('#imprintCopy').textContent())?.trim();await page.locator('.imprint-wheel button').nth(1).click();const after=(await page.locator('#imprintCopy').textContent())?.trim();if(!before||!after||before===after)fail('Thirteen-imprint optional reading interaction failed',{case:item.name});
  await page.locator('#system').scrollIntoViewIfNeeded();const sb=page.locator('.state-buttons button[data-state="unknown"]');await sb.click();const stateText=(await page.locator('#stateResult').textContent())||'';if(!stateText.includes('未知即谨慎'))fail('UNKNOWN fail-closed design-state interaction failed',{case:item.name,stateText});
  const trigger=page.locator('#supplementTrigger');await trigger.click();await page.waitForTimeout(80);if(await page.locator('#supplementPanel').evaluate(el=>el.hidden))fail('Supplement did not open',{case:item.name});await page.keyboard.press('Escape');await page.waitForTimeout(80);if(!(await page.locator('#supplementPanel').evaluate(el=>el.hidden)))fail('Supplement did not close with Escape',{case:item.name});
  await page.locator('#hero').scrollIntoViewIfNeeded();const y0=await page.evaluate(()=>scrollY);if(mobile)await page.evaluate(()=>scrollBy(0,Math.min(innerHeight*.72,620)));else await page.keyboard.press('PageDown');await page.waitForTimeout(300);const y1=await page.evaluate(()=>scrollY);if(y1<=y0+20)fail('Reading sequence did not advance',{case:item.name,y0,y1});
  report.cases.push({name:item.name,viewport:item.viewport,metrics,horizontal_overflow_px:overflow,imprint_interaction:before!==after,unknown_state_fail_closed:stateText.includes('未知即谨慎'),screenshots:item.anchors.map(id=>`${item.name}/${id}.png`),page_errors:pageErrors});if(pageErrors.length)fail('Page runtime errors',{case:item.name,pageErrors});await context.close();
 }
 const ctx=await browser.newContext({viewport:{width:1366,height:768},reducedMotion:'reduce'});const page=await ctx.newPage();await page.goto(baseUrl,{waitUntil:'domcontentloaded'});await settle(page);const reduced=await page.evaluate(()=>({matches:matchMedia('(prefers-reduced-motion: reduce)').matches,scrollBehavior:getComputedStyle(document.documentElement).scrollBehavior,modeTransition:getComputedStyle(document.querySelector('.mode-card')).transitionDuration}));if(!reduced.matches)fail('Reduced-motion preference not applied',{reduced});if(reduced.modeTransition!=='0s')fail('Motion transition remains under reduced motion',{reduced});report.reduced_motion=reduced;await ctx.close();
}finally{await browser.close();}
report.status=report.failures.length?'FAIL':'PASS';fs.writeFileSync(path.join(outDir,'report.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report,null,2));if(report.failures.length)process.exit(1);
