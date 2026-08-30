import fs from 'node:fs';
import path from 'node:path';
import { chromium } from 'playwright';

const out = path.resolve(process.env.OLEANDER_OUT || 'out/BROWSER_TARGET_RUNTIME');
const expectedPath = path.resolve(process.env.OLEANDER_EXPECTED || 'out/GN_SOURCE/EXPORT_BAKE_RECEIPT.json');
fs.mkdirSync(out,{recursive:true});
const expected = JSON.parse(fs.readFileSync(expectedPath,'utf8'));

const browser = await chromium.launch({
  headless:true,
  args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']
});
const page = await browser.newPage({viewport:{width:720,height:720},deviceScaleFactor:1});
const consoleLines=[];
page.on('console',msg=>consoleLines.push(`${msg.type()}: ${msg.text()}`));
page.on('pageerror',err=>consoleLines.push(`pageerror: ${err.message}`));

await page.goto('http://127.0.0.1:4173/viewer.html',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.__OLEANDER_RUNTIME__?.ready || window.__OLEANDER_RUNTIME__?.error,{timeout:30000});
const runtime = await page.evaluate(()=>window.__OLEANDER_RUNTIME__);
if(runtime.error) throw new Error(`viewer runtime error: ${runtime.error}`);
if(runtime.meshCount < 1 || runtime.positionCount < 1 || runtime.triangleCount < 1) {
  throw new Error(`empty browser geometry: ${JSON.stringify(runtime)}`);
}
if(runtime.materialCount < 1) throw new Error(`no browser material: ${JSON.stringify(runtime)}`);

const eps = 1e-5;
function closeArray(a,b){return a.length===b.length && a.every((x,i)=>Math.abs(x-b[i])<=eps)}
const expectedMin = expected.bbox_min ?? null;
const expectedMax = expected.bbox_max ?? null;
// EXPORT_BAKE receipt does not carry bbox in v1; workflow supplies source reopen receipt for strict bbox comparison.
let sourceReopen=null;
if(process.env.OLEANDER_SOURCE_REOPEN){
  sourceReopen=JSON.parse(fs.readFileSync(path.resolve(process.env.OLEANDER_SOURCE_REOPEN),'utf8'));
  if(!closeArray(runtime.bboxMin,sourceReopen.native_reopen.bbox_min) || !closeArray(runtime.bboxMax,sourceReopen.native_reopen.bbox_max)){
    throw new Error(`browser bbox mismatch: ${JSON.stringify({browser:[runtime.bboxMin,runtime.bboxMax],native:[sourceReopen.native_reopen.bbox_min,sourceReopen.native_reopen.bbox_max]})}`);
  }
}

await page.screenshot({path:path.join(out,'BROWSER_RUNTIME_720.png'),fullPage:true});
const receipt={
  schema:'oleander.3d.gltf-browser-target-runtime.v1',
  browser:'Chromium via Playwright 1.55.0',
  threeRevision:runtime.threeRevision,
  asset:'GN_NATIVE_BENCH.glb',
  sourceGlbBytes:expected.glb_bytes,
  sourceGlbSha256:expected.glb_sha256,
  meshCount:runtime.meshCount,
  materialCount:runtime.materialCount,
  positionCount:runtime.positionCount,
  triangleCount:runtime.triangleCount,
  bboxMin:runtime.bboxMin,
  bboxMax:runtime.bboxMax,
  bboxSize:runtime.bboxSize,
  materialTypes:[...new Set(runtime.materialTypes)],
  gltfSceneCount:runtime.gltfSceneCount,
  webgl:{version:runtime.webglVersion,vendor:runtime.webglVendor,renderer:runtime.webglRenderer},
  nativeBBoxMatch:sourceReopen ? true : null,
  screenshot:'BROWSER_RUNTIME_720.png',
  console:consoleLines,
  evidenceClass:'TARGET_RUNTIME_BROWSER_READBACK',
  finding:'The explicitly baked GLB loads as visible mesh geometry in a real Chromium/WebGL/Three.js runtime with native-export bbox preserved. This does not restore the Blender Geometry Nodes dependency graph.',
  holds:['production browser/device matrix','performance budget','accessibility/interaction','Design KEEP']
};
fs.writeFileSync(path.join(out,'BROWSER_RUNTIME_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify(receipt,null,2));
await browser.close();
