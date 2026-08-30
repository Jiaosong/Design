import fs from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';

const out=path.resolve(process.env.OLEANDER_OUT||'out/TANGENT_BASIS_BROWSER');
const src=JSON.parse(fs.readFileSync(path.resolve(process.env.OLEANDER_SOURCE_RECEIPT||'out/TANGENT_BASIS_SOURCE/SOURCE_RECEIPT.json'),'utf8'));
fs.mkdirSync(out,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:720,height:720},deviceScaleFactor:1});
const logs=[]; page.on('console',m=>logs.push(`${m.type()}: ${m.text()}`)); page.on('pageerror',e=>logs.push(`pageerror: ${e.message}`));
await page.goto('http://127.0.0.1:4175/viewer.html',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.__OLEANDER_TANGENT_RUNTIME__?.ready||window.__OLEANDER_TANGENT_RUNTIME__?.error,{timeout:30000});
const rt=await page.evaluate(()=>window.__OLEANDER_TANGENT_RUNTIME__); if(rt.error) throw new Error(rt.error);
const checks={};
for(const name of ['UV_STANDARD','UV_MIRRORED']){
  const got=rt.objects[name]; const expected=src.objects[name];
  if(!got) throw new Error(`missing target object ${name}`);
  if(!got.tangentPresent||got.tangentCount<4) throw new Error(`missing TANGENT attribute ${name}: ${JSON.stringify(got)}`);
  const targetSigns=[]; if(got.tangentSignCounts.positive>0)targetSigns.push(1); if(got.tangentSignCounts.negative>0)targetSigns.push(-1); targetSigns.sort((a,b)=>a-b);
  const sourceSigns=[...expected.blender_tangent.unique_signs].sort((a,b)=>a-b);
  const signMatch=JSON.stringify(targetSigns)===JSON.stringify(sourceSigns);
  const normalMapped=got.materialReadback.some(m=>m.normalMap===true);
  checks[name]={sourceSigns,targetSigns,signMatch,normalMapped,target:got};
  if(!signMatch||!normalMapped) throw new Error(`target tangent/material mismatch ${name}: ${JSON.stringify(checks[name])}`);
}
if(checks.UV_STANDARD.targetSigns[0]===checks.UV_MIRRORED.targetSigns[0]) throw new Error('mirrored UV did not preserve opposite tangent handedness in target runtime');
await page.screenshot({path:path.join(out,'TANGENT_BASIS_BROWSER_720.png'),fullPage:true});
const receipt={
 schema:'oleander.3d.gltf-tangent-basis-target-runtime.v1',browser:'Chromium via Playwright 1.55.0',threeRevision:rt.threeRevision,
 sourceAsset:src.asset,sourceAssetBytes:src.asset_bytes,sourceAssetSha256:src.asset_sha256,
 sourceNormalTexture:src.normal_texture,sourceNormalTextureSha256:src.normal_texture_sha256,
 meshCount:rt.meshCount,normalMappedMaterialCount:rt.normalMappedMaterialCount,objectChecks:checks,
 tangentAttributePreserved:true,mirroredUvOppositeHandednessPreserved:true,normalTextureMaterialSemanticsPreserved:true,
 webgl:rt.webgl,screenshot:'TANGENT_BASIS_BROWSER_720.png',console:logs,
 evidenceClass:'TARGET_RUNTIME_TANGENT_BASIS_SEMANTIC_READBACK',
 promotionScope:['Blender loop bitangent-sign -> glTF TANGENT.w -> Three.js BufferAttribute sign preservation','mirrored-UV opposite tangent handedness preservation','glTF normalTexture -> Three.js normalMap material binding'],
 holds:['pixel-level Blender/Three shading parity','normal-map Y convention conversion across non-glTF pipelines','negative-scale tangent parity','UDIM/multi-material tangent parity','Design KEEP']
};
fs.writeFileSync(path.join(out,'TARGET_RUNTIME_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n'); console.log(JSON.stringify(receipt,null,2)); await browser.close();
