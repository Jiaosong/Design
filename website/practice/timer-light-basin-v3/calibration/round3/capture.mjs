import { chromium } from 'playwright';
import fs from 'node:fs';
import path from 'node:path';

const out = path.resolve('artifacts');
fs.mkdirSync(out,{recursive:true});
const browser = await chromium.launch({
  headless:true,
  args:['--use-angle=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']
});
const context = await browser.newContext({viewport:{width:1200,height:900},deviceScaleFactor:1});
const shots = ['housing','diffuser','knob','shadow'];
const manifest = { round:3, shots:{}, webgl:null, decision:'HUMAN_REVIEW_REQUIRED / NO AUTOMATIC RENDER LOCK' };
for (const shot of shots) {
  const page = await context.newPage();
  page.on('console',m=>console.log(`[browser:${m.type()}]`,m.text()));
  await page.goto(`http://127.0.0.1:4174/?shot=${shot}`,{waitUntil:'networkidle',timeout:60000});
  await page.waitForFunction(()=>window.__CALIBRATION_READY===true,{timeout:60000});
  await page.waitForTimeout(400);
  const info = await page.evaluate(()=>window.__WEBGL_INFO);
  const r3 = await page.evaluate(()=>window.__ROUND3);
  const file = path.join(out,`${shot}.png`);
  await page.screenshot({path:file,fullPage:false});
  manifest.shots[shot] = {path:`artifacts/${shot}.png`,info,round3:r3};
  if(!manifest.webgl) manifest.webgl=info;
  await page.close();
}
fs.writeFileSync(path.join(out,'manifest.json'),JSON.stringify(manifest,null,2));
await browser.close();
console.log(JSON.stringify(manifest,null,2));
