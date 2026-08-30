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
const angleDeg=(a,b)=>{const na=norm(a),nb=norm(b);const d=Math.max(-1,Math.min(1,na.reduce((s,x,i)=>s+x*nb[i],0)));return Math.acos(d)*180/Math.PI};
const maxAbsDelta=(a,b)=>Math.max(...a.map((x,i)=>Math.abs(x-b[i])));
const DIR_ANGLE_MAX_DEG=0.005;
const DIR_COMPONENT_MAX=5e-5;
const dirCheck=(a,b)=>{const angularErrorDeg=angleDeg(a,b),componentMaxAbsDelta=maxAbsDelta(a,b);return {angularErrorDeg,componentMaxAbsDelta,angleLimitDeg:DIR_ANGLE_MAX_DEG,componentLimit:DIR_COMPONENT_MAX,pass:angularErrorDeg<=DIR_ANGLE_MAX_DEG&&componentMaxAbsDelta<=DIR_COMPONENT_MAX}};
const expectedRGBA8=[...src.encoded_normal_rgb.map(x=>Math.round(x*255)),255];
const pixelCheck=rgba=>{const delta=rgba.map((x,i)=>Math.abs(x-expectedRGBA8[i]));return {expectedRGBA8,observedRGBA8:rgba,perChannelAbsDelta:delta,maxChannelAbsDelta:Math.max(...delta),pass:Math.max(...delta)<=1}};
const decodeNormal=rgba=>norm(rgba.slice(0,3).map(x=>x/255*2-1));

const browser=await chromium.launch({headless:true,args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist','--disable-dev-shm-usage']});
const page=await browser.newPage({viewport:{width:720,height:720},deviceScaleFactor:1});
const logs=[];page.on('console',m=>logs.push(`${m.type()}: ${m.text()}`));page.on('pageerror',e=>logs.push(`pageerror: ${e.message}`));
await page.goto('http://127.0.0.1:4176/viewer.html',{waitUntil:'networkidle'});
await page.waitForFunction(()=>window.__OLEANDER_TBN_RUNTIME__?.ready||window.__OLEANDER_TBN_RUNTIME__?.error,{timeout:30000});
const rt=await page.evaluate(()=>window.__OLEANDER_TBN_RUNTIME__);if(rt.error)throw new Error(rt.error);

const q=src.tangent_space_sample;
const checks={};
for(const name of ['TBN_STANDARD','TBN_MIRRORED']){
  const got=rt.objects[name],exp=src.objects[name].expected_target;
  if(!got||!got.normalPresent||!got.tangentPresent||!got.uvPresent)throw new Error(`missing TBN attributes ${name}: ${JSON.stringify(got)}`);
  const px=got.material?.normalMapPixel;if(!px?.rgba8)throw new Error(`missing target normal-map pixel ${name}: ${JSON.stringify(got.material)}`);
  const T=avg(got.worldTangents),N=avg(got.worldNormals);
  const signs=[...new Set(got.tangentW.map(v=>v<0?-1:1))];if(signs.length!==1)throw new Error(`mixed target tangent signs ${name}: ${JSON.stringify(signs)}`);
  const w=signs[0],B=norm(scale(cross(N,T),w));
  const P=norm(add3(scale(T,q[0]),scale(B,q[1]),scale(N,q[2])));
  const tangentDirection=dirCheck(T,exp.tangent),normalDirection=dirCheck(N,exp.normal),bitangentDirection=dirCheck(B,exp.bitangent),perturbedDirection=dirCheck(P,exp.perturbed_normal_mapped_source),mappedConstructionDirection=dirCheck(P,exp.perturbed_normal_from_mapped_tbn);
  const sampledPixel=pixelCheck(px.rgba8),sampledQ=decodeNormal(px.rgba8);
  const sampledP=norm(add3(scale(T,sampledQ[0]),scale(B,sampledQ[1]),scale(N,sampledQ[2])));
  const sampledExpectedP=norm(add3(scale(exp.tangent,sampledQ[0]),scale(exp.bitangent,sampledQ[1]),scale(exp.normal,sampledQ[2])));
  const sampledPerturbedDirection=dirCheck(sampledP,sampledExpectedP);
  const tangentMatch=tangentDirection.pass,normalMatch=normalDirection.pass,signMatch=w===exp.sign,bitangentMatch=bitangentDirection.pass,perturbedMatch=perturbedDirection.pass,mappedConstructionMatch=mappedConstructionDirection.pass,normalMapped=got.material?.normalMap===true,embeddedPixelMatch=sampledPixel.pass,sampledPerturbedMatch=sampledPerturbedDirection.pass;
  checks[name]={expected:exp,observed:{T,N,B,w,perturbedNormal:P,vertexCount:got.vertexCount,matrixWorld:got.matrixWorld,material:got.material},numericError:{tangent:tangentDirection,normal:normalDirection,bitangent:bitangentDirection,perturbed:perturbedDirection,mappedConstruction:mappedConstructionDirection},embeddedNormalPixel:{...sampledPixel,decodedNormalizedTangentVector:sampledQ,textureMeta:{width:px.width,height:px.height,x:px.x,y:px.y,colorSpace:px.colorSpace,flipY:px.flipY,type:px.type},reconstructedTargetPerturbedNormal:sampledP,expectedPerturbedNormalFromSampledPixel:sampledExpectedP,directionError:sampledPerturbedDirection},tangentMatch,normalMatch,signMatch,bitangentMatch,perturbedMatch,mappedConstructionMatch,normalMapped,embeddedPixelMatch,sampledPerturbedMatch};
  if(!tangentMatch||!normalMatch||!signMatch||!bitangentMatch||!perturbedMatch||!mappedConstructionMatch||!normalMapped||!embeddedPixelMatch||!sampledPerturbedMatch)throw new Error(`numeric/pixel TBN mismatch ${name}: ${JSON.stringify(checks[name])}`);
}
const separation=angleDeg(checks.TBN_STANDARD.observed.perturbedNormal,checks.TBN_MIRRORED.observed.perturbedNormal);if(separation<5)throw new Error(`witness insufficiently discriminative: perturbed normal separation ${separation}`);
const sampledSeparation=angleDeg(checks.TBN_STANDARD.embeddedNormalPixel.reconstructedTargetPerturbedNormal,checks.TBN_MIRRORED.embeddedNormalPixel.reconstructedTargetPerturbedNormal);if(sampledSeparation<5)throw new Error(`sampled-pixel witness insufficiently discriminative: ${sampledSeparation}`);
await page.screenshot({path:path.join(out,'TBN_NUMERIC_BROWSER_720.png'),fullPage:true});
const receipt={schema:'oleander.3d.gltf-tbn-reconstruction-target.v3',browser:'Chromium via Playwright 1.55.0',threeRevision:rt.threeRevision,sourceAsset:src.asset,sourceAssetSha256:src.asset_sha256,tangentSpaceSample:q,sourceEncodedNormalRGB:src.encoded_normal_rgb,expectedEmbeddedRGBA8:expectedRGBA8,directionGate:{angleMaxDeg:DIR_ANGLE_MAX_DEG,componentMaxAbsDelta:DIR_COMPONENT_MAX,reason:'direction semantics are gated by angular and component error; embedded PNG bytes are separately gated at 8-bit channel precision'},objectChecks:checks,standardVsMirroredPerturbedNormalSeparationDeg:separation,standardVsMirroredSampledPixelPerturbedNormalSeparationDeg:sampledSeparation,numericTangentVectorPreserved:true,numericNormalVectorPreserved:true,tangentHandednessPreserved:true,numericPerturbedNormalReconstructionPreserved:true,embeddedNormalTexturePixelPreserved:true,sampledPixelDrivenPerturbedNormalReconstructionPreserved:true,webgl:rt.webgl,screenshot:'TBN_NUMERIC_BROWSER_720.png',console:logs,evidenceClass:'TARGET_RUNTIME_NUMERIC_TBN_PLUS_EMBEDDED_NORMAL_PIXEL',promotionScope:['world-space tangent XYZ after glTF node transforms','world-space normal XYZ after glTF node transforms','TANGENT.w handedness','B = w * cross(N,T) reconstruction','embedded normal-map image is actually readable from Three normalMap.image','embedded RGB bytes match the generated PNG within 8-bit quantization','the target-runtime sampled pixel is decoded to tangent space and drives the expected perturbed-normal direction'],holds:['actual GPU fragment-shader output parity','negative-scale tangent frame beyond dedicated witness','triangulation-change parity beyond dedicated witness','skinning/animation tangent frame','mip/filter/anisotropy sampling behavior','Design KEEP'],provenanceNote:'The original numeric witness and its first scalar-threshold failure remain in workflow history. v3 adds target texture sampling; it does not replace source q with an assumed constant.'};
fs.writeFileSync(path.join(out,'TARGET_RUNTIME_RECEIPT.json'),JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt,null,2));await browser.close();
