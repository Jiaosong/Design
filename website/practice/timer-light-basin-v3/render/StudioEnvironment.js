import * as THREE from 'three';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';

RectAreaLightUniformsLib.init();

const BASE={
  background:0xe3ddd4,floor:0xe1dbd2,
  cards:[
    {size:[7.2,1.15],pos:[0,4.8,1.4],color:0xfffbf4,energy:2.5},
    {size:[3.8,4.7],pos:[-4.6,1.8,3.1],color:0xfff8ed,energy:3.3},
    {size:[2.8,4.2],pos:[4.7,1.6,1.8],color:0xeaf2f7,energy:1.8},
    {size:[0.85,4.8],pos:[-2.1,2.0,-5.0],color:0xffffff,energy:2.3}
  ],
  flags:[{size:[1.35,4.8],pos:[4.8,1.8,-2.9],color:0x050505,energy:1}],
  direct:{key:4.0,fill:1.35,rim:1.9,hemi:0.48}
};

const PRESETS={
  hero:BASE,
  material:{...BASE,background:0xe7e2da,floor:0xe5e0d8,direct:{key:3.7,fill:1.55,rim:2.15,hemi:0.52}},
  housing:{
    ...BASE,
    cards:[
      {size:[7.4,1.2],pos:[0,5.0,1.1],color:0xfffaf1,energy:2.1},
      {size:[4.8,5.6],pos:[-4.05,1.45,3.25],color:0xfff7ea,energy:5.0},
      {size:[1.9,4.3],pos:[4.25,1.2,2.05],color:0xe7eff5,energy:0.95},
      {size:[0.75,5.0],pos:[-2.3,1.9,-4.8],color:0xffffff,energy:2.0}
    ],
    flags:[{size:[1.35,5.2],pos:[3.7,1.5,-2.0],color:0x010101,energy:1}],
    direct:{key:2.8,fill:1.0,rim:1.55,hemi:0.42}
  },
  diffuser:{
    ...BASE,background:0xe7e2da,floor:0xe5dfd7,
    cards:[
      {size:[6.8,1.35],pos:[0,4.7,1.0],color:0xffffff,energy:2.4},
      {size:[4.2,4.8],pos:[-4.5,1.7,2.8],color:0xfff7ea,energy:2.7},
      {size:[2.6,4.0],pos:[4.4,1.3,2.2],color:0xeaf3f7,energy:1.3},
      {size:[0.65,4.5],pos:[1.8,1.9,-4.2],color:0xffffff,energy:2.8}
    ],
    flags:[{size:[1.0,4.2],pos:[-3.4,1.25,-2.1],color:0x080706,energy:1}],
    direct:{key:3.2,fill:1.45,rim:2.0,hemi:0.55}
  },
  knob:{
    ...BASE,background:0xded9d1,floor:0xdcd7cf,
    cards:[
      {size:[3.0,3.4],pos:[0.15,1.35,4.0],color:0xfffbf5,energy:3.7},
      {size:[0.75,4.4],pos:[-2.7,1.45,3.2],color:0xffffff,energy:2.8},
      {size:[0.65,4.2],pos:[2.8,1.35,3.1],color:0xe9f2f8,energy:2.1},
      {size:[5.8,0.9],pos:[0,4.4,1.5],color:0xfff7ea,energy:1.5}
    ],
    flags:[{size:[1.2,4.8],pos:[3.6,1.3,-1.8],color:0x020202,energy:1}],
    direct:{key:2.7,fill:1.85,rim:1.9,hemi:0.52}
  },
  shadow:{...BASE,background:0xe2ddd5,floor:0xe2ddd5,direct:{key:2.2,fill:1.45,rim:1.0,hemi:0.62}}
};

function reflectionCard(scene,def){
  const material=new THREE.MeshBasicMaterial({color:new THREE.Color(def.color).multiplyScalar(def.energy),side:THREE.DoubleSide,toneMapped:false});
  const mesh=new THREE.Mesh(new THREE.PlaneGeometry(...def.size),material);
  mesh.position.set(...def.pos);mesh.lookAt(0,0.25,0);scene.add(mesh);return mesh;
}

export function buildStudioEnvironment(renderer,mode='hero'){
  const preset=PRESETS[mode]||PRESETS.hero;
  const capture=new THREE.Scene();capture.background=new THREE.Color(0x11100e);
  preset.cards.forEach(d=>reflectionCard(capture,d));(preset.flags||[]).forEach(d=>reflectionCard(capture,d));
  const pmrem=new THREE.PMREMGenerator(renderer);const target=pmrem.fromScene(capture,0.025,0.1,100);const texture=target.texture;pmrem.dispose();
  capture.traverse(o=>{o.geometry?.dispose?.();o.material?.dispose?.();});
  return {texture,target,preset};
}

export function createCyclorama(mode='hero'){
  const preset=PRESETS[mode]||PRESETS.hero;const group=new THREE.Group();group.name='PHOTOGRAPHY_CYCLORAMA';
  const floor=new THREE.Mesh(new THREE.PlaneGeometry(14,14),new THREE.MeshStandardMaterial({color:preset.floor,roughness:0.98,metalness:0}));
  floor.rotation.x=-Math.PI/2;floor.position.set(0,-0.012,1.5);floor.receiveShadow=true;group.add(floor);
  const wall=new THREE.Mesh(new THREE.PlaneGeometry(14,9),new THREE.MeshBasicMaterial({color:preset.background,toneMapped:true}));wall.position.set(0,4.45,-4.7);group.add(wall);
  return group;
}

export function addStudioLights(scene,mode='hero'){
  const preset=PRESETS[mode]||PRESETS.hero;const {key,fill,rim,hemi}=preset.direct;
  const keyLight=new THREE.RectAreaLight(0xfff4e8,key,3.8,2.6);keyLight.position.set(-2.8,3.5,3.4);keyLight.lookAt(0,.22,0);scene.add(keyLight);
  const fillLight=new THREE.RectAreaLight(0xeaf2f7,fill,3.1,3.0);fillLight.position.set(3.3,2.2,2.6);fillLight.lookAt(0,.22,0);scene.add(fillLight);
  const rimLight=new THREE.RectAreaLight(0xffffff,rim,1.0,3.8);rimLight.position.set(-1.8,2.8,-3.6);rimLight.lookAt(0,.24,0);scene.add(rimLight);
  const shadowKey=new THREE.DirectionalLight(0xfff8ef,.72);shadowKey.position.set(-2.8,4.6,3.8);shadowKey.castShadow=true;shadowKey.shadow.mapSize.set(2048,2048);
  shadowKey.shadow.camera.left=-2;shadowKey.shadow.camera.right=2;shadowKey.shadow.camera.top=2;shadowKey.shadow.camera.bottom=-2;shadowKey.shadow.camera.near=.1;shadowKey.shadow.camera.far=12;shadowKey.shadow.bias=-.0001;scene.add(shadowKey);
  scene.add(new THREE.HemisphereLight(0xfaf3ea,0x665f56,hemi));return {keyLight,fillLight,rimLight,shadowKey};
}

export function applyStudioScene(scene,renderer,mode='hero'){
  const env=buildStudioEnvironment(renderer,mode);scene.environment=env.texture;scene.background=new THREE.Color(env.preset.background);
  const cyclorama=createCyclorama(mode);scene.add(cyclorama);const lights=addStudioLights(scene,mode);return {...env,cyclorama,lights};
}
