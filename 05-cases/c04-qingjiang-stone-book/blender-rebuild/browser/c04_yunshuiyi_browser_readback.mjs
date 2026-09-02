import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

const outDir=path.resolve(process.env.C04_REBUILD_OUT||'artifacts/c04-yunshuiyi');
const readbackDir=path.join(outDir,'browser-readback');
fs.mkdirSync(readbackDir,{recursive:true});
const port=4173;
const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1'],{stdio:['ignore','pipe','pipe']});
await new Promise(r=>setTimeout(r,700));
const base=`http://127.0.0.1:${port}/05-cases/c04-qingjiang-stone-book/blender-rebuild/browser/c04_yunshuiyi_web_runtime.html`;
const expected={
  LOD0:fs.statSync(path.join(outDir,'C04_YUNSHUIYI_REBUILD_v003_LOD0.glb')).size,
  LOD1:fs.statSync(path.join(outDir,'C04_YUNSHUIYI_REBUILD_v003_LOD1.glb')).size,
  LOD2:fs.statSync(path.join(outDir,'C04_YUNSHUIYI_REBUILD_v003_LOD2.glb')).size,
};
const results=[];
let browser;
try{
  browser=await chromium.launch({headless:true});
  async function caseRun(name,width,height,reduced=false,forceMissing=false){
    const page=await browser.newPage({viewport:{width,height}});
    if(reduced)await page.emulateMedia({reducedMotion:'reduce'});
    const pageErrors=[];const consoleErrors=[];const glbRequests=[];const glbResponses=[];
    page.on('pageerror',e=>pageErrors.push(String(e)));
    page.on('console',m=>{if(m.type()==='error'&&!String(m.text()).includes('__missing__.glb'))consoleErrors.push(m.text())});
    page.on('request',r=>{if(r.url().endsWith('.glb'))glbRequests.push(r.url())});
    page.on('response',r=>{if(r.url().endsWith('.glb'))glbResponses.push({url:r.url(),status:r.status()})});
    const url=base+(forceMissing?'?forceMissing=1':'');
    await page.goto(url,{waitUntil:'domcontentloaded'});
    await page.waitForTimeout(400);
    const before=glbRequests.length;
    await page.locator('#stage').scrollIntoViewIfNeeded();
    if(forceMissing){
      await page.waitForFunction(()=>window.__C04_STATE?.status==='error',{timeout:15000});
      await page.locator('#retry').click();
    }
    await page.waitForFunction(()=>window.__C04_STATE?.status==='ready',{timeout:20000});
    const state0=await page.evaluate(()=>structuredClone(window.__C04_STATE));
    const canvas=page.locator('canvas');const box=await canvas.boundingBox();
    if(!box)throw new Error(`${name}: canvas missing`);
    await page.mouse.move(box.x+box.width*0.5,box.y+box.height*0.5);
    await page.mouse.down();
    await page.mouse.move(box.x+box.width*0.62,box.y+box.height*0.44,{steps:8});
    await page.mouse.up();
    const afterDrag=await page.evaluate(()=>structuredClone(window.__C04_STATE));
    const beforeContact=afterDrag.contactVisible;
    await page.locator('#hotspot').click();
    const afterHotspot=await page.evaluate(()=>structuredClone(window.__C04_STATE));
    await page.screenshot({path:path.join(readbackDir,`${name}.png`),fullPage:false});
    const perf=await page.evaluate(()=>performance.getEntriesByType('resource').filter(e=>e.name.endsWith('.glb')).map(e=>({name:e.name,duration:e.duration,transferSize:e.transferSize,decodedBodySize:e.decodedBodySize})));
    const expectedLod=width>=1600?'LOD0':(width>=600?'LOD1':'LOD2');
    const pass=before===0 && state0.lod===expectedLod && state0.status==='ready' && afterDrag.dragCount>0 && beforeContact!==null && afterHotspot.contactVisible===!beforeContact && state0.reducedMotion===reduced && pageErrors.length===0 && consoleErrors.length===0 && glbResponses.some(x=>x.status===200);
    const rec={name,viewport:[width,height],reducedMotion:reduced,forceMissing,beforeScrollGlbRequests:before,expectedLod,selectedLod:state0.lod,assetBytes:expected[state0.lod],firstVisibleMsLocalCarrier:state0.firstVisibleMs,dragCount:afterDrag.dragCount,rotationAfterDrag:afterDrag.rotation,contactBefore:beforeContact,contactAfter:afterHotspot.contactVisible,requests:glbRequests,responses:glbResponses,resourceTiming:perf,pageErrors,consoleErrors,verdict:pass?'PASS_BOUNDED':'FAIL'};
    results.push(rec);await page.close();if(!pass)throw new Error(`${name} failed: ${JSON.stringify(rec)}`);
  }
  await caseRun('desktop-1920',1920,1080,false,false);
  await caseRun('desktop-1366-reduced',1366,768,true,false);
  await caseRun('mobile-390',390,844,false,false);
  await caseRun('error-recovery-1366',1366,768,false,true);
  const payload={schema:'oleander.c04.browser-readback.v1',browserVersion:browser.version(),carrier:'LOCAL_GITHUB_ACTIONS_CHROMIUM',timingBoundary:'timings are local runner observations only, not production-network performance claims',tests:results,holds:['FPS UNKNOWN','GPU memory UNKNOWN','production network latency UNKNOWN','Design KEEP','source-image fidelity approval'],verdict:'PASS_BOUNDED'};
  fs.writeFileSync(path.join(readbackDir,'C04_YUNSHUIYI_BROWSER_READBACK.json'),JSON.stringify(payload,null,2)+'\n');
  console.log(JSON.stringify(payload));
} finally {
  if(browser)await browser.close();
  server.kill('SIGTERM');
}
