import fs from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';

const out=path.resolve(process.env.OLEANDER_OUT||'out/AXIS_WITNESS_BROWSER');
const source=JSON.parse(fs.readFileSync(path.resolve(process.env.OLEANDER_SOURCE_RECEIPT||'out/AXIS_WITNESS_SOURCE/SOURCE_RECEIPT.json'),'utf8'));
fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:720,height:720},deviceScaleFactor:1});
const consoleLines=[]; page.on('console',m=>consoleLines.push(`${m.type()}: ${m.text()}`)); page.on('pageerror',e=>consoleLines.push(`pageerror: ${e.message}`));
await page.goto('http://127.0.0.1:4174/viewer.html',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.__OLEANDER_AXIS_RUNTIME__?.ready||window.__OLEANDER_AXIS_RUNTIME__?.error,{timeout:30000});
const runtime=await page.evaluate(()=>window.__OLEANDER_AXIS_RUNTIME__);
if(runtime.error) throw new Error(runtime.error);
const eps=1e-5;
const close=(a,b)=>a.length===b.length&&a.every((v,i)=>Math.abs(v-b[i])<=eps);
const checks={};
for(const [name,expected] of Object.entries(source.expected_target_objects)){
  const got=runtime.objects[name];
  if(!got) throw new Error(`missing witness ${name}: ${JSON.stringify(runtime.objects)}`);
  const centerMatch=close(got.bboxCenter,expected.center);
  const positionMatch=close(got.worldPosition,expected.center);
  const sizeMatch=close(got.bboxSize,expected.size);
  checks[name]={expected,observed:got,centerMatch,positionMatch,sizeMatch};
  if(!centerMatch||!positionMatch||!sizeMatch) throw new Error(`signed transform mismatch ${name}: ${JSON.stringify(checks[name])}`);
}
if(source.transform_determinant!==1) throw new Error(`unexpected transform determinant ${source.transform_determinant}`);
await page.screenshot({path:path.join(out,'AXIS_HANDEDNESS_BROWSER_720.png'),fullPage:true});
const receipt={
  schema:'oleander.3d.gltf-axis-handedness-target-runtime.v1',
  browser:'Chromium via Playwright 1.55.0',
  threeRevision:runtime.threeRevision,
  sourceAsset:source.asset,
  sourceAssetBytes:source.asset_bytes,
  sourceAssetSha256:source.asset_sha256,
  declaredTransform:source.declared_transform,
  transformMatrixRows:source.transform_matrix_rows,
  transformDeterminant:source.transform_determinant,
  signedObjectChecks:checks,
  allSignedCentersMatch:true,
  allSizesMatch:true,
  handednessPreserved:true,
  handednessEvidence:'non-symmetric named witnesses with positive and negative Y coordinates validate (x,y,z)->(x,z,-y); declared matrix determinant is +1',
  meshCount:runtime.meshCount,
  webgl:runtime.webgl,
  screenshot:'AXIS_HANDEDNESS_BROWSER_720.png',
  console:consoleLines,
  evidenceClass:'TARGET_RUNTIME_SIGNED_AXIS_HANDEDNESS_READBACK',
  promotionScope:['signed coordinate conversion under Blender->glTF/Three.js exchange','right-handed transform preservation for declared exporter/runtime pair'],
  holds:['normal/tangent orientation','animation transform parity','negative-scale/mirror parity','production device/browser matrix','Design KEEP']
};
fs.writeFileSync(path.join(out,'TARGET_RUNTIME_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify(receipt,null,2));
await browser.close();
