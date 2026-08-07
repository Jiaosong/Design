import * as THREE from 'three';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

RectAreaLightUniformsLib.init();

const PRESETS = {
  hero: {
    background: 0xe7e1d8,
    cyclorama: 0xe5dfd6,
    cards: [
      { size:[6.8,1.10], pos:[0,4.8,1.5], color:0xfffbf3, energy:3.10 },
      { size:[3.8,4.2], pos:[3.8,2.2,4.0], color:0xfff6e9, energy:2.40 },
      { size:[3.1,4.6], pos:[-4.8,2.0,2.5], color:0xfff8ef, energy:2.20 },
      { size:[2.6,4.0], pos:[4.8,1.9,-1.8], color:0xeaf2f7, energy:1.80 },
      { size:[0.95,4.5], pos:[-1.8,2.1,-5.2], color:0xffffff, energy:2.50 },
      { size:[1.35,4.6], pos:[-2.7,2.0,4.6], color:0xfffbf3, energy:2.65 }
    ],
    direct: { key:3.70, fill:1.15, rim:1.70, hemi:0.38 }
  },
  material: {
    background: 0xe9e4dc,
    cyclorama: 0xe8e3db,
    cards: [
      { size:[7.2,1.15], pos:[0,5.0,1.2], color:0xffffff, energy:3.15 },
      { size:[4.0,4.2], pos:[3.9,2.0,3.7], color:0xfff7ec, energy:2.55 },
      { size:[3.4,4.5], pos:[-4.4,1.9,2.5], color:0xfff8ed, energy:2.25 },
      { size:[2.7,4.2], pos:[4.7,1.7,-2.0], color:0xecf3f8, energy:1.95 },
      { size:[0.90,4.0], pos:[-0.9,1.8,-5.0], color:0xffffff, energy:2.70 },
      { size:[1.10,4.2], pos:[-2.5,1.8,4.5], color:0xfffbf4, energy:2.45 }
    ],
    direct: { key:3.45, fill:1.25, rim:1.90, hemi:0.40 }
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
  mesh.lookAt(0, 0.22, 0);
  scene.add(mesh);
  return mesh;
}

export function buildStudioEnvironment(renderer, mode='hero') {
  const preset = PRESETS[mode] || PRESETS.hero;
  const capture = new THREE.Scene();
  capture.background = new THREE.Color(0x2b2824);
  preset.cards.forEach((def)=>reflectionCard(capture, def));
  reflectionCard(capture, {size:[0.62,4.8],pos:[5.5,2.0,-2.6],color:0x080808,energy:1});
  const pmrem = new THREE.PMREMGenerator(renderer);
  const target = pmrem.fromScene(capture, 0.025, 0.1, 100);
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
  const material=new THREE.MeshStandardMaterial({color:preset.cyclorama, roughness:0.98, metalness:0});
  const mesh=new THREE.Mesh(geometry,material);
  mesh.receiveShadow=true;
  mesh.name='PHOTOGRAPHY_CYCLORAMA';
  return mesh;
}

export function addStudioLights(scene, mode='hero') {
  const preset = PRESETS[mode] || PRESETS.hero;
  const {key,fill,rim,hemi}=preset.direct;
  const keyLight=new THREE.RectAreaLight(0xfff4e6,key,3.8,2.2);
  keyLight.position.set(-2.9,3.7,3.3); keyLight.lookAt(0,0.24,0); scene.add(keyLight);
  const fillLight=new THREE.RectAreaLight(0xeaf2f7,fill,3.2,3.0);
  fillLight.position.set(3.4,2.3,2.7); fillLight.lookAt(0,0.22,0); scene.add(fillLight);
  const rimLight=new THREE.RectAreaLight(0xffffff,rim,0.9,3.6);
  rimLight.position.set(-1.8,3.0,-3.5); rimLight.lookAt(0,0.24,0); scene.add(rimLight);
  const shadowKey=new THREE.DirectionalLight(0xfff7ee,0.30);
  shadowKey.position.set(-2.6,4.8,3.5); shadowKey.castShadow=false; scene.add(shadowKey);
  scene.add(new THREE.HemisphereLight(0xf8f1e8,0x625c54,hemi));
  return {keyLight,fillLight,rimLight,shadowKey};
}

export function applyFocusLighting(lights, focus='body') {
  if(!lights) return;
  const {keyLight,fillLight,rimLight}=lights;
  if(focus==='top' || focus==='diffuser'){
    // CAL-20260807-1721-SWIFTSHADER: grazing key exposes the real shallow basin without changing geometry.
    keyLight.intensity=2.35; keyLight.position.set(-3.1,0.75,2.45); keyLight.lookAt(0,0.24,0);
    fillLight.intensity=0.60; fillLight.position.set(3.0,1.15,2.0); fillLight.lookAt(0,0.23,0);
    rimLight.intensity=1.25; rimLight.position.set(-1.6,1.9,-3.0); rimLight.lookAt(0,0.24,0);
  } else if(focus==='control' || focus==='knob'){
    keyLight.intensity=4.0; keyLight.position.set(2.25,1.45,2.8); keyLight.lookAt(0.18,0.13,0.52);
    fillLight.intensity=1.0; fillLight.position.set(-2.0,1.2,2.4); fillLight.lookAt(0.18,0.13,0.52);
    rimLight.intensity=2.30; rimLight.position.set(1.0,1.8,-2.7); rimLight.lookAt(0.18,0.13,0.52);
  } else {
    keyLight.intensity=3.70; keyLight.position.set(-2.9,3.7,3.3); keyLight.lookAt(0,0.24,0);
    fillLight.intensity=1.15; fillLight.position.set(3.4,2.3,2.7); fillLight.lookAt(0,0.22,0);
    rimLight.intensity=1.70; rimLight.position.set(-1.8,3.0,-3.5); rimLight.lookAt(0,0.24,0);
  }
}

export function applyStudioScene(scene, renderer, mode='hero') {
  const env=buildStudioEnvironment(renderer,mode);
  scene.environment=env.texture;
  scene.background=new THREE.Color(env.preset.background);
  const cyclorama=createCyclorama(mode); scene.add(cyclorama);
  const lights=addStudioLights(scene,mode);
  return { ...env, cyclorama, lights };
}
