import { chromium } from '@playwright/test';
import fs from 'node:fs/promises';
const base=process.env.CALIBRATION_URL||'http://127.0.0.1:4173/';
await fs.mkdir('artifacts',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:1200,height:900},deviceScaleFactor:1});
page.on('console',m=>console.log(`[browser:${m.type()}] ${m.text()}`));
page.on('pageerror',e=>console.error('[pageerror]',e.stack||e.message));
page.on('requestfailed',r=>console.error('[requestfailed]',r.url(),r.failure()?.errorText||''));
const shots=['housing','diffuser','knob','shadow'];
const manifest={shots:{},webgl:null,capture:'canvas.toDataURL/png'};
for(const shot of shots){
  await page.goto(`${base}?shot=${shot}`,{waitUntil:'domcontentloaded'});
  await page.waitForFunction(()=>window.__CALIBRATION_READY===true,{timeout:45000});
  const payload=await page.evaluate(()=>{
    const canvas=document.querySelector('#app canvas');
    if(!canvas) throw new Error('WebGL canvas missing');
    return {info:window.__WEBGL_INFO,png:canvas.toDataURL('image/png')};
  });
  if(!manifest.webgl)manifest.webgl=payload.info;
  const path=`artifacts/${shot}.png`;
  await fs.writeFile(path,Buffer.from(payload.png.split(',')[1],'base64'));
  manifest.shots[shot]={path,info:payload.info};
  console.log(`[captured:${shot}] ${path}`);
}
await fs.writeFile('artifacts/manifest.json',JSON.stringify(manifest,null,2));
await browser.close();
