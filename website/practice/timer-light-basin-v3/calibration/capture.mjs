import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
const base=process.env.CALIBRATION_URL||'http://127.0.0.1:4173/';
await fs.mkdir('artifacts',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:1200,height:900},deviceScaleFactor:1});
page.on('console',m=>console.log(`[browser:${m.type()}] ${m.text()}`));
page.on('pageerror',e=>console.error('[pageerror]',e.stack||e.message));
page.on('requestfailed',r=>console.error('[requestfailed]',r.url(),r.failure()?.errorText||''));
const shots=['housing','diffuser','knob','shadow'];const manifest={shots:{},webgl:null};
for(const shot of shots){
  await page.goto(`${base}?shot=${shot}`,{waitUntil:'domcontentloaded'});
  try{
    await page.waitForFunction(()=>window.__CALIBRATION_READY===true,{timeout:45000});
  }catch(error){
    await page.screenshot({path:`artifacts/debug-${shot}.png`});
    console.error(`[ready-timeout:${shot}]`,error.message);
    console.error('[page-title]',await page.title());
    console.error('[body]',(await page.locator('body').innerText()).slice(0,2000));
    throw error;
  }
  const info=await page.evaluate(()=>window.__WEBGL_INFO);if(!manifest.webgl)manifest.webgl=info;
  const path=`artifacts/${shot}.png`;await page.screenshot({path});manifest.shots[shot]={path,info};
}
await fs.writeFile('artifacts/manifest.json',JSON.stringify(manifest,null,2));await browser.close();
