import fs from 'node:fs';
import path from 'node:path';
import {chromium} from 'playwright';

const out=path.resolve(process.env.OLEANDER_OUT||'out/TBN_BROWSER');
const src=JSON.parse(fs.readFileSync(path.resolve(process.env.OLEANDER_SOURCE_RECEIPT||'out/TBN_SOURCE/SOURCE_RECEIPT.json'),'utf8'));
fs.mkdirSync(out,{recursive:true});

const norm=v=>{const l=Math.hypot(...v);return v.map(x=>x/l)};
const avg=vs=>norm(vs.reduce((a,v)=>a.map((x,i)=>x+v[i]),[0,0,0]).map(x=>x/vs.length));
const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
const scale=(v,s)=>v.map(x=>x*s);
const add3=(a,b,c)=>a.map((x,i)=>x+b[i]+c[i]);
const close=(a,b,eps=2e-5)=>a.length===b.length&&a.every((x,i)=>Math.abs(x-b[i])<=eps);
const angleDeg=(a,b)=>{const na=norm(a),nb=norm(b);const d=Math.max(-1,Math.min(1,na.reduce((s,x,i)=>s+x*nb[i],0)));return Math.acos(d)*180/Math.PI};

const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:720,height:720},deviceScaleFactor:1});
const logs=[];page.on('console',m=>logs.push(`${m.type()}: ${m.text()}`));page.on('pageerror',e=>logs.push(`pageerror: ${e.message}`));
await page.goto('http://127.0.0.1:4176/viewer.html',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.__OLEANDER_TBN_RUNTIME__?.ready||window.__OLEANDER_TBN_RUNTIME__?.error,{timeout:30000});
const rt=await page.evaluate(()=>window.__OLEANDER_TBN_RUNTIME__);if(rt.error)throw new Error(rt.error);

const q=src.tangent_space_sample;
const checks={};
for(const name of ['TBN_STANDARD','TBN_MIRRORED']){
  const got=rt.objects[name], exp=src.objects[name].expected_target;
  if(!got||!got.normalPresent||!got.tangentPresent||!got.uvPresent)throw new Error(`missing TBN attributes ${name}: ${JSON.stringify(got)}`);
  const T=avg(got.worldTangents),N=avg(got.worldNormals);
  const signs=[...new Set(got.tangentW.map(v=>v<0?-1:1))];
  if(signs.length!==1)throw new Error(`mixed target tangent signs ${name}: ${JSON.stringify(signs)}`);
  const w=signs[0]; const B=norm(scale(cross(N,T),w));
  const P=norm(add3(scale(T,q[0]),scale(B,q[1]),scale(N,q[2])));
  const tangentMatch=close(T,exp.tangent),normalMatch=close(N,exp.normal),signMatch=w===exp.sign,bitangentMatch=close(B,exp.bitangent);
  const perturbedMatch=close(P,exp.perturbed_normal_mapped_source,4e-5);
  const mappedConstructionMatch=close(P,exp.perturbed_normal_from_mapped_tbn,4e-5);
  const normalMapped=got.material?.normalMap===true;
  checks[name]={expected:exp,observed:{T,N,B,w,perturbedNormal:P,vertexCount:got.vertexCount,matrixWorld:got.matrixWorld,material:got.material},tangentMatch,normalMatch,signMatch,bitangentMatch,perturbedMatch,mappedConstructionMatch,perturbedAngleErrorDeg:angleDeg(P,exp.perturbed_normal_mapped_source),normalMapped};
  if(!tangentMatch||!normalMatch||!signMatch||!bitangentMatch||!perturbedMatch||!mappedConstructionMatch||!normalMapped)throw new Error(`numeric TBN mismatch ${name}: ${JSON.stringify(checks[name])}`);
}
// Because q has non-zero B component, a wrong mirrored-UV handedness would change the reconstructed normal.
const separation=angleDeg(checks.TBN_STANDARD.observed.perturbedNormal,checks.TBN_MIRRORED.observed.perturbedNormal);
if(separation<5)throw new Error(`witness insufficiently discriminative: perturbed normal separation ${separation}`);
await page.screenshot({path:path.join(out,'TBN_NUMERIC_BROWSER_720.png'),fullPage:true});
const receipt={schema:'oleander.3d.gltf-tbn-reconstruction-target.v1',browser:'Chromium via Playwright 1.55.0',threeRevision:rt.threeRevision,sourceAsset:src.asset,sourceAssetSha256:src.asset_sha256,tangentSpaceSample:q,objectChecks:checks,standardVsMirroredPerturbedNormalSeparationDeg:separation,numericTangentVectorPreserved:true,numericNormalVectorPreserved:true,tangentHandednessPreserved:true,numericPerturbedNormalReconstructionPreserved:true,webgl:rt.webgl,screenshot:'TBN_NUMERIC_BROWSER_720.png',console:logs,evidenceClass:'TARGET_RUNTIME_NUMERIC_TBN_RECONSTRUCTION',promotionScope:['world-space tangent XYZ after glTF node transforms','world-space normal XYZ after glTF node transforms','TANGENT.w handedness','B = w * cross(N,T) reconstruction','non-trivial tangent-space sample reconstruction with non-zero T/B/N components'],holds:['actual embedded-texture pixel sampling','pixel shader output parity','negative-scale tangent frame','triangulation-change parity','skinning/animation tangent frame','Design KEEP']};
fs.writeFileSync(path.join(out,'TARGET_RUNTIME_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt,null,2));await browser.close();
