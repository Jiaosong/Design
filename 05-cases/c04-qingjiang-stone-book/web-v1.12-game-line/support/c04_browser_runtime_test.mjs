import { chromium } from 'playwright';
import fs from 'node:fs';

const base = process.argv[2] || 'http://127.0.0.1:8765/';
const receiptPath = process.argv[3] || 'browser-runtime-receipt.json';
const out = {schema:'C04_BROWSER_RUNTIME_VALIDATION_v2', base, cases:[], verdict:'PASS_BOUNDED', browserCarrier:'Chromium headless + ANGLE/SwiftShader WebGL', holds:['Browser runtime PASS is not Design KEEP.','FPS/ms/memory not asserted.','Visual fidelity to upstream source remains Presentation/Design review.']};
const browser = await chromium.launch({headless:true,args:['--use-gl=angle','--use-angle=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});

async function runCase(name,width,height,{reducedMotion='no-preference',forceError=false}={}) {
  const ctx=await browser.newContext({viewport:{width,height},reducedMotion});
  const page=await ctx.newPage();
  const glb=[]; const consoleErrors=[]; const pageErrors=[];
  page.on('response',async r=>{if(r.url().endsWith('.glb')){let bytes=null;try{bytes=(await r.body()).length}catch{} glb.push({url:r.url(),status:r.status(),bytes})}});
  page.on('console',m=>{if(m.type()==='error')consoleErrors.push(m.text())});
  page.on('pageerror',e=>pageErrors.push(String(e)));
  await page.goto(base+(forceError?'?forceError=1':''),{waitUntil:'domcontentloaded'});
  try { await page.waitForFunction(()=>window.__C04_METRICS!==undefined,{timeout:10000}); }
  catch(e){ throw new Error(`${name}: harness boot failed; pageErrors=${JSON.stringify(pageErrors)} consoleErrors=${JSON.stringify(consoleErrors)}`); }
  const before=await page.evaluate(()=>window.__C04_METRICS);
  if(before.requestStarted) throw new Error(`${name}: model requested before user load action`);
  await page.click('#load');
  if(forceError){await page.waitForFunction(()=>document.querySelector('#status').textContent==='error'); await page.click('#retry');}
  try { await page.waitForFunction(()=>window.__C04_METRICS.modelLoaded===true,{timeout:30000}); }
  catch(e){ const m=await page.evaluate(()=>window.__C04_METRICS); throw new Error(`${name}: model load failed; metrics=${JSON.stringify(m)} pageErrors=${JSON.stringify(pageErrors)} consoleErrors=${JSON.stringify(consoleErrors)} glb=${JSON.stringify(glb)}`); }
  const canvas=page.locator('canvas'); const box=await canvas.boundingBox();
  await page.mouse.move(box.x+box.width*.45,box.y+box.height*.5); await page.mouse.down(); await page.mouse.move(box.x+box.width*.62,box.y+box.height*.55,{steps:5}); await page.mouse.up();
  await page.click('#hotspot');
  await page.waitForTimeout(250);
  const metrics=await page.evaluate(()=>window.__C04_METRICS);
  const shot=receiptPath.replace(/\.json$/,`-${name}.png`); await page.screenshot({path:shot});
  const expectedLOD=width<=500?'LOD2':width<=1500?'LOD1':'LOD0';
  const successful=glb.filter(x=>x.status===200);
  const pass=metrics.selectedLOD===expectedLOD && metrics.modelLoaded && metrics.interacted && metrics.hotspotSelected===true && successful.length===1 && pageErrors.length===0 && (!forceError || metrics.recovered===true) && (reducedMotion!=='reduce' || metrics.reducedMotion===true);
  out.cases.push({name,viewport:{width,height},reducedMotion,forceError,expectedLOD,metrics,glb,consoleErrors,pageErrors,screenshot:shot,pass});
  if(!pass) out.verdict='FAIL';
  await ctx.close();
}

await runCase('desktop1920',1920,1080);
await runCase('desktop1366',1366,768);
await runCase('mobile390',390,844);
await runCase('reduced390',390,844,{reducedMotion:'reduce'});
await runCase('recovery1366',1366,768,{forceError:true});
await browser.close();
fs.writeFileSync(receiptPath,JSON.stringify(out,null,2));
console.log('C04_BROWSER_RUNTIME_RECEIPT='+JSON.stringify(out));
if(out.verdict!=='PASS_BOUNDED') process.exit(5);
