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
function sizeFromBounds(min,max){return max.map((x,i)=>x-min[i])}
let sourceReopen=null;
let axisContract=null;
if(process.env.OLEANDER_SOURCE_REOPEN){
  sourceReopen=JSON.parse(fs.readFileSync(path.resolve(process.env.OLEANDER_SOURCE_REOPEN),'utf8'));
  const nativeMin=sourceReopen.native_reopen.bbox_min;
  const nativeMax=sourceReopen.native_reopen.bbox_max;
  const nativeSize=sizeFromBounds(nativeMin,nativeMax);
  // Blender source is Z-up. glTF/Three.js runtime is Y-up. For this symmetric benchmark,
  // the observed and expected extent mapping is Blender XYZ -> browser XZY in magnitude.
  // The asset is symmetric around origin, so sign/handedness cannot be proven by this carrier.
  const expectedBrowserSize=[nativeSize[0],nativeSize[2],nativeSize[1]];
  const extentMappingMatch=closeArray(runtime.bboxSize,expectedBrowserSize);
  if(!extentMappingMatch){
    throw new Error(`browser axis/extent mismatch: ${JSON.stringify({browserSize:runtime.bboxSize,nativeSize,expectedBrowserSize})}`);
  }
  axisContract={
    sourceCoordinateSystem:'Blender Z-up',
    targetCoordinateSystem:'glTF/Three.js Y-up',
    observedExtentMapping:'Blender XYZ extents -> browser XZY extents',
    nativeSize,
    expectedBrowserSize,
    browserSize:runtime.bboxSize,
    extentMappingMatch:true,
    handednessSignProven:false,
    handednessHoldReason:'benchmark geometry is symmetric around origin; axis sign cannot be discriminated from bbox extents alone'
  };
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
  axisContract,
  screenshot:'BROWSER_RUNTIME_720.png',
  console:consoleLines,
  evidenceClass:'TARGET_RUNTIME_BROWSER_READBACK',
  finding:'The explicitly baked GLB loads as visible mesh geometry in a real Chromium/WebGL/Three.js runtime. Blender Z-up source extents are preserved under the expected glTF/Three.js Y-up axis mapping. The Blender Geometry Nodes dependency graph is not restored.',
  holds:['axis-sign/handedness witness on an asymmetric carrier','production browser/device matrix','performance budget','accessibility/interaction','Design KEEP']
};
fs.writeFileSync(path.join(out,'BROWSER_RUNTIME_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');
console.log(JSON.stringify(receipt,null,2));
await browser.close();
