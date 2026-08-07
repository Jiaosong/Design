import * as THREE from 'three';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

RectAreaLightUniformsLib.init();

const PRESETS = {
  hero: {
    background: 0xe5ded3,
    cyclorama: 0xe3ddd3,
    cards: [
      { size:[6.8,1.05], pos:[0,4.8,1.8], color:0xfff8ed, energy:3.4 },
      { size:[3.3,4.6], pos:[-4.8,2.0,2.8], color:0xfff8ef, energy:2.9 },
      { size:[2.7,4.0], pos:[4.6,1.6,1.0], color:0xeaf1f5, energy:1.9 },
      { size:[1.0,4.5], pos:[-1.9,2.1,-5.2], color:0xffffff, energy:2.4 },
      { size:[0.7,2.7], pos:[3.1,0.9,2.8], color:0xffe6c8, energy:1.7 }
    ],
    direct: { key:5.0, fill:1.65, rim:2.25, hemi:0.55 }
  },
  material: {
    background: 0xeae5dd,
    cyclorama: 0xe9e4dc,
    cards: [
      { size:[7.4,1.15], pos:[0,5.0,1.2], color:0xffffff, energy:3.5 },
      { size:[3.8,4.6], pos:[-4.5,1.9,2.5], color:0xfff8ed, energy:3.1 },
      { size:[3.2,4.3], pos:[4.7,1.7,1.7], color:0xf0f5fa, energy:2.3 },
      { size:[0.85,3.8], pos:[0,1.7,-5.0], color:0xffffff, energy:2.65 }
    ],
    direct: { key:4.6, fill:1.8, rim:2.55, hemi:0.6 }
  }
};

function reflectionCard(scene, def) {
  const material = new THREE.MeshBasicMaterial({
    color: new THREE.Color(def.color).multiplyScalar(def.energy),
    side: THREE.DoubleSide,
    toneMapped: false
  });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(...def.size), material);
  mesh.position.set(...def.pos);
  mesh.lookAt(0, 0.32, 0);
  scene.add(mesh);
  return mesh;
}

export function buildStudioEnvironment(renderer, mode='hero') {
  const preset = PRESETS[mode] || PRESETS.hero;
  const capture = new THREE.Scene();
  capture.background = new THREE.Color(0x171511);
  preset.cards.forEach((def)=>reflectionCard(capture, def));
  reflectionCard(capture, {size:[2.2,5.6],pos:[5.7,2.3,-2.8],color:0x060606,energy:1});
  const pmrem = new THREE.PMREMGenerator(renderer);
  const target = pmrem.fromScene(capture, 0.03, 0.1, 100);
  const texture = target.texture;
  pmrem.dispose();
  capture.traverse((o)=>{ if(o.geometry) o.geometry.dispose?.(); if(o.material) o.material.dispose?.(); });
  return { texture, target, preset };
}

export function createCyclorama(mode='hero') {
  const preset = PRESETS[mode] || PRESETS.hero;
  const width=8.2, depth=8.2, segments=80;
  const geometry = new THREE.PlaneGeometry(width, depth, 1, segments);
  const p=geometry.attributes.position;
  for(let i=0;i<p.count;i++){
    const x=p.getX(i), t=p.getY(i);
    let y,z;
    if(t<1.25){ y=-0.012; z=t-1.35; }
    else {
      const radius=2.85;
      const angle=Math.min(Math.PI/2,(t-1.25)/radius);
      z=-0.10 + radius*Math.sin(angle);
      y=-0.012 + radius*(1-Math.cos(angle));
    }
    p.setXYZ(i,x,y,z);
  }
  p.needsUpdate=true;
  geometry.computeVertexNormals();
  const material=new THREE.MeshStandardMaterial({
    color:preset.cyclorama, roughness:0.98, metalness:0
  });
  const mesh=new THREE.Mesh(geometry,material);
  mesh.receiveShadow=true;
  mesh.name='PHOTOGRAPHY_CYCLORAMA';
  return mesh;
}

export function addStudioLights(scene, mode='hero') {
  const preset = PRESETS[mode] || PRESETS.hero;
  const {key,fill,rim,hemi}=preset.direct;
  const keyLight=new THREE.RectAreaLight(0xfff4e6,key,3.4,2.0);
  keyLight.position.set(-2.9,3.7,3.3); keyLight.lookAt(0,0.30,0); scene.add(keyLight);
  const fillLight=new THREE.RectAreaLight(0xeaf2f7,fill,2.8,2.9);
  fillLight.position.set(3.4,2.3,2.5); fillLight.lookAt(0,0.27,0); scene.add(fillLight);
  const rimLight=new THREE.RectAreaLight(0xffffff,rim,1.0,3.6);
  rimLight.position.set(-1.8,3.0,-3.5); rimLight.lookAt(0,0.30,0); scene.add(rimLight);
  const shadowKey=new THREE.DirectionalLight(0xfff7ee,1.05);
  shadowKey.position.set(-2.6,4.8,3.5); shadowKey.castShadow=true;
  shadowKey.shadow.mapSize.set(2048,2048);
  shadowKey.shadow.camera.left=-2; shadowKey.shadow.camera.right=2;
  shadowKey.shadow.camera.top=2; shadowKey.shadow.camera.bottom=-2;
  shadowKey.shadow.camera.near=0.1; shadowKey.shadow.camera.far=12;
  shadowKey.shadow.bias=-0.00015; scene.add(shadowKey);
  scene.add(new THREE.HemisphereLight(0xf8f1e8,0x625c54,hemi));
  return {keyLight,fillLight,rimLight,shadowKey};
}

export function applyStudioScene(scene, renderer, mode='hero') {
  const env=buildStudioEnvironment(renderer,mode);
  scene.environment=env.texture;
  scene.background=new THREE.Color(env.preset.background);
  const cyclorama=createCyclorama(mode); scene.add(cyclorama);
  const lights=addStudioLights(scene,mode);
  return { ...env, cyclorama, lights };
}
