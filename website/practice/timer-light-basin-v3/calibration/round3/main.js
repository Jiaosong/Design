import * as THREE from 'three';
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
import { ContactShadow } from '../../render/ContactShadow.js';
import { configureColorPipeline } from '../../render/ColorPipeline.js';
import { createPostProcessing } from '../../render/PostProcessing.js';

RectAreaLightUniformsLib.init();

const shot = new URLSearchParams(location.search).get('shot') || 'housing';
const mode = shot === 'diffuser' || shot === 'knob' ? 'material' : 'hero';
const VIEWS = {
  housing:  { fov: 27, cam: [1.72, 1.02, 1.88], target: [0, .155, 0] },
  diffuser: { fov: 29, cam: [.92, .92, .92], target: [0, .286, 0] },
  knob:     { fov: 31, cam: [.88, .39, 1.38], target: [.17, .13, .54] },
  shadow:   { fov: 31, cam: [1.58, .84, 1.84], target: [0, .055, 0] }
};

function reflectionCard(scene, { size, pos, color, energy = 1, target = [0, .2, 0] }) {
  const material = new THREE.MeshBasicMaterial({
    color: new THREE.Color(color).multiplyScalar(energy),
    side: THREE.DoubleSide,
    toneMapped: false
  });
  const mesh = new THREE.Mesh(new THREE.PlaneGeometry(...size), material);
  mesh.position.set(...pos);
  mesh.lookAt(...target);
  scene.add(mesh);
  return mesh;
}

function buildRound3Environment(renderer) {
  const capture = new THREE.Scene();
  capture.background = new THREE.Color(0x171513);
  const cards = mode === 'hero' ? [
    { size: [6.8, .85], pos: [-.4, 4.5, 1.8], color: 0xfffbf4, energy: 3.8 },
    { size: [2.4, 4.8], pos: [-4.2, 1.8, 2.8], color: 0xfff5e8, energy: 3.15 },
    { size: [.58, 4.4], pos: [2.65, 1.7, 3.05], color: 0xffffff, energy: 4.8 },
    { size: [2.8, 4.2], pos: [4.7, 1.7, -.6], color: 0xeaf2f7, energy: 2.15 },
    { size: [.72, 3.8], pos: [-1.6, 1.9, -4.8], color: 0xffffff, energy: 3.0 },
    { size: [1.8, 5.0], pos: [5.35, 2.1, 2.4], color: 0x030303, energy: 1.0 }
  ] : [
    { size: [7.2, .9], pos: [0, 4.8, 1.0], color: 0xffffff, energy: 4.1 },
    { size: [2.8, 4.8], pos: [-4.1, 1.9, 2.4], color: 0xfff7ec, energy: 3.3 },
    { size: [.52, 4.2], pos: [2.55, 1.55, 3.0], color: 0xffffff, energy: 5.4 },
    { size: [2.7, 4.5], pos: [4.4, 1.6, -.8], color: 0xeaf3f8, energy: 2.4 },
    { size: [.65, 3.5], pos: [-1.2, 1.7, -4.6], color: 0xffffff, energy: 3.3 },
    { size: [1.5, 5.0], pos: [5.1, 2.0, 2.2], color: 0x020202, energy: 1.0 }
  ];
  cards.forEach((c) => reflectionCard(capture, c));
  const pmrem = new THREE.PMREMGenerator(renderer);
  const target = pmrem.fromScene(capture, .025, .1, 100);
  pmrem.dispose();
  capture.traverse((o) => { o.geometry?.dispose?.(); o.material?.dispose?.(); });
  return target;
}

function addRound3Lights(scene) {
  const key = new THREE.RectAreaLight(0xfff5e8, mode === 'hero' ? 4.3 : 4.7, 3.4, 2.2);
  key.position.set(-2.9, 3.5, 3.1); key.lookAt(0, .22, 0); scene.add(key);
  const edge = new THREE.RectAreaLight(0xffffff, mode === 'hero' ? 3.4 : 4.0, .55, 3.6);
  edge.position.set(2.55, 1.75, 3.1); edge.lookAt(0, .18, 0); scene.add(edge);
  const fill = new THREE.RectAreaLight(0xe9f1f6, 1.35, 2.6, 3.1);
  fill.position.set(3.6, 2.0, -.7); fill.lookAt(0, .2, 0); scene.add(fill);
  const rim = new THREE.RectAreaLight(0xffffff, 2.0, .8, 3.8);
  rim.position.set(-1.5, 2.8, -3.7); rim.lookAt(0, .2, 0); scene.add(rim);
  scene.add(new THREE.HemisphereLight(0xf8f2e9, 0x5a554f, .42));
  return { key, edge, fill, rim };
}

const view = VIEWS[shot];
const scene = new THREE.Scene();
scene.background = new THREE.Color(mode === 'hero' ? 0xe4ddd3 : 0xe9e4dc);
const camera = new THREE.PerspectiveCamera(view.fov, 4 / 3, .01, 20);
camera.position.set(...view.cam); camera.lookAt(...view.target);

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance', preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(1200, 900, false);
configureColorPipeline(renderer, mode);
document.querySelector('#app').appendChild(renderer.domElement);

const envTarget = buildRound3Environment(renderer);
scene.environment = envTarget.texture;
addRound3Lights(scene);

const ground = new THREE.Mesh(
  new THREE.PlaneGeometry(8, 8),
  new THREE.MeshStandardMaterial({ color: mode === 'hero' ? 0xe4ddd3 : 0xe9e4dc, roughness: .98, metalness: 0 })
);
ground.rotation.x = -Math.PI / 2;
ground.position.y = -.001;
ground.receiveShadow = true;
scene.add(ground);

const root = new THREE.Group();
root.name = 'MODEL_DERIVED_CALIBRATION_RIG_ROUND3';
scene.add(root);
const groundOffset = .014;

const housingProfile = [
  [.505,.245],[.505,.290],[.530,.290],[.580,.260],[.590,.245],[.590,.020],[.560,.000],
  [.540,.020],[.540,.225],[.515,.242],[.505,.245]
].map(([r,y]) => new THREE.Vector2(r, y + groundOffset));
const housing = new THREE.Mesh(new THREE.LatheGeometry(housingProfile, 192));
housing.name = '01_Upper_Housing';
housing.material = new THREE.MeshPhysicalMaterial({
  color: 0x756e66,
  metalness: 0,
  roughness: .43,
  clearcoat: .035,
  clearcoatRoughness: .58,
  ior: 1.46,
  specularIntensity: .52,
  envMapIntensity: 1.72
});
root.add(housing);

const R = [.001,.0313,.0625,.0938,.125,.1563,.1875,.2188,.250,.2813,.3125,.3438,.375,.4063,.4375,.4688,.500];
const top = [.27509,.27537,.27583,.27688,.27780,.27891,.28021,.28250,.28426,.28620,.28833,.29188,.29447,.29725,.30021,.30350,.30500];
const bottom = [.24500,.24521,.24558,.24613,.24688,.24833,.24954,.25093,.25250,.25521,.25725,.25947,.26315,.26583,.26870,.27176,.27176];
const diffuserProfile = [];
for (let i=0;i<R.length;i++) diffuserProfile.push(new THREE.Vector2(R[i], top[i] + groundOffset));
for (let i=R.length-1;i>=0;i--) diffuserProfile.push(new THREE.Vector2(R[i], bottom[i] + groundOffset));
const diffuser = new THREE.Mesh(new THREE.LatheGeometry(diffuserProfile, 224));
diffuser.name = '02_Formed_Diffuser';
diffuser.material = new THREE.MeshPhysicalMaterial({
  color: 0xf3efe8,
  metalness: 0,
  roughness: .31,
  transmission: .62,
  thickness: mode === 'material' ? .16 : .12,
  ior: 1.49,
  attenuationColor: new THREE.Color(0xffead0),
  attenuationDistance: .16,
  specularIntensity: .48,
  clearcoat: .015,
  clearcoatRoughness: .72,
  envMapIntensity: 1.38,
  side: THREE.FrontSide
});
root.add(diffuser);

const bottomCover = new THREE.Mesh(
  new THREE.CylinderGeometry(.56,.56,.025,192),
  new THREE.MeshStandardMaterial({ color:0x46413c, roughness:.76, metalness:0, envMapIntensity:1.0 })
);
bottomCover.name = '18_Bottom_Cover';
bottomCover.position.y = .0285;
root.add(bottomCover);

const foot = new THREE.Mesh(
  new THREE.TorusGeometry(.5075,.0325,32,224),
  new THREE.MeshStandardMaterial({ color:0x181817, roughness:.94, metalness:0 })
);
foot.name = '19_Silicone_Foot_Ring';
foot.rotation.x = Math.PI/2;
foot.scale.z = .22;
foot.position.y = .0082;
root.add(foot);

const knob = new THREE.Mesh(
  new THREE.CylinderGeometry(.08,.08,.08,128),
  new THREE.MeshPhysicalMaterial({
    color:0xc3c4c2,
    metalness:1,
    roughness:.27,
    clearcoat:.018,
    clearcoatRoughness:.42,
    envMapIntensity:2.05
  })
);
knob.name = '17_Side_Knob';
knob.rotation.x = Math.PI/2;
knob.position.set(.18,.124,.602);
root.add(knob);

const stateLight = new THREE.Mesh(
  new THREE.CylinderGeometry(.435,.435,.004,192),
  new THREE.MeshStandardMaterial({
    color:0xffd4a5,
    emissive:0xff8c2f,
    emissiveIntensity: shot === 'diffuser' ? 1.12 : .82,
    roughness:.42,
    transparent:true,
    opacity: shot === 'diffuser' ? .20 : .13,
    depthWrite:false
  })
);
stateLight.name = 'VISUALIZATION_State_Light';
stateLight.position.y = .276;
root.add(stateLight);

if (shot === 'diffuser') {
  housing.material.transparent = true;
  housing.material.opacity = .16;
  bottomCover.visible = false;
  foot.visible = false;
  knob.visible = false;
  const innerGlow = new THREE.PointLight(0xffb66f, 1.55, 1.8, 2.0);
  innerGlow.position.set(0,.205,0);
  scene.add(innerGlow);
}
if (shot === 'knob') {
  diffuser.material.transparent = true;
  diffuser.material.opacity = .10;
  stateLight.visible = false;
}
if (shot === 'shadow') {
  stateLight.visible = false;
}

root.traverse((o) => {
  if (!o.isMesh) return;
  o.layers.enable(1);
  o.castShadow = true;
  o.receiveShadow = true;
});

const contactShadow = new ContactShadow(renderer, scene, root, {
  resolution: shot === 'shadow' ? 1536 : 1024,
  opacity: shot === 'shadow' ? .24 : .19,
  blur: shot === 'shadow' ? 4.1 : 3.0
});

const post = createPostProcessing(renderer, scene, camera, mode);
post.setSize(1200,900);
for (let i=0;i<12;i++) post.render(1/60);

const gl = renderer.getContext();
const dbg = gl.getExtension('WEBGL_debug_renderer_info');
window.__WEBGL_INFO = {
  renderer: dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER),
  vendor: dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR),
  version: gl.getParameter(gl.VERSION)
};
window.__ROUND3 = {
  shot,
  gates: ['Housing highlight','Diffuser volume','Metal knob reflection','Contact shadow falloff'],
  status: 'REVIEW_REQUIRED / NO AUTOMATIC VISUAL PASS'
};
window.__CALIBRATION_READY = true;
document.querySelector('#label').textContent = `ROUND 3 · ${shot.toUpperCase()} · ${window.__WEBGL_INFO.renderer}`;
