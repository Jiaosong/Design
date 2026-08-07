import * as THREE from 'three';
import { applyStudioScene } from '../render/StudioEnvironment.js';
import { tuneProductMaterials } from '../render/DiffuserMaterial.js';
import { ContactShadow } from '../render/ContactShadow.js';
import { configureColorPipeline } from '../render/ColorPipeline.js';
import { createPostProcessing } from '../render/PostProcessing.js';

const shot=new URLSearchParams(location.search).get('shot')||'housing';
const materialMode=shot==='diffuser'||shot==='knob'?'material':'hero';
const VIEWS={
 housing:{fov:30,cam:[1.92,.78,2.20],target:[0,.16,0]},
 diffuser:{fov:32,cam:[.94,.54,1.08],target:[0,.286,0]},
 knob:{fov:34,cam:[.77,.34,1.24],target:[.18,.125,.58]},
 shadow:{fov:39,cam:[2.35,.52,2.72],target:[0,.045,0]}
};
const view=VIEWS[shot],scene=new THREE.Scene();
const camera=new THREE.PerspectiveCamera(view.fov,4/3,.01,30);camera.position.set(...view.cam);camera.lookAt(...view.target);
const renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance',preserveDrawingBuffer:true});
renderer.setPixelRatio(1);renderer.setSize(1200,900,false);configureColorPipeline(renderer,materialMode);document.querySelector('#app').appendChild(renderer.domElement);
const studio=applyStudioScene(scene,renderer,shot);

const root=new THREE.Group();root.name='MODEL_DERIVED_CALIBRATION_RIG';scene.add(root);const groundOffset=.014;
const housingProfile=[ [.505,.245],[.505,.290],[.530,.290],[.580,.260],[.590,.245],[.590,.020],[.560,.000],[.540,.020],[.540,.225],[.515,.242],[.505,.245] ].map(([r,y])=>new THREE.Vector2(r,y+groundOffset));
const housing=new THREE.Mesh(new THREE.LatheGeometry(housingProfile,192));housing.name='01_Upper_Housing';root.add(housing);
const R=[.001,.0313,.0625,.0938,.125,.1563,.1875,.2188,.250,.2813,.3125,.3438,.375,.4063,.4375,.4688,.500];
const top=[.27509,.27537,.27583,.27688,.27780,.27891,.28021,.28250,.28426,.28620,.28833,.29188,.29447,.29725,.30021,.30350,.30500];
const bottom=[.24500,.24521,.24558,.24613,.24688,.24833,.24954,.25093,.25250,.25521,.25725,.25947,.26315,.26583,.26870,.27176,.27176];
const diffuserProfile=[];for(let i=0;i<R.length;i++)diffuserProfile.push(new THREE.Vector2(R[i],top[i]+groundOffset));for(let i=R.length-1;i>=0;i--)diffuserProfile.push(new THREE.Vector2(R[i],bottom[i]+groundOffset));
const diffuser=new THREE.Mesh(new THREE.LatheGeometry(diffuserProfile,224));diffuser.name='02_Formed_Diffuser';root.add(diffuser);
const bottomCover=new THREE.Mesh(new THREE.CylinderGeometry(.56,.56,.025,192),new THREE.MeshStandardMaterial());bottomCover.name='18_Bottom_Cover';bottomCover.position.y=.0285;root.add(bottomCover);
const foot=new THREE.Mesh(new THREE.TorusGeometry(.5075,.0325,32,224),new THREE.MeshStandardMaterial());foot.name='19_Silicone_Foot_Ring';foot.rotation.x=Math.PI/2;foot.scale.z=.23;foot.position.y=.0075;root.add(foot);
const knob=new THREE.Mesh(new THREE.CylinderGeometry(.08,.08,.08,128),new THREE.MeshStandardMaterial());knob.name='17_Side_Knob';knob.rotation.x=Math.PI/2;knob.position.set(.18,.124,.602);root.add(knob);
const stateLight=new THREE.Mesh(new THREE.CylinderGeometry(.485,.485,.004,192),new THREE.MeshStandardMaterial());stateLight.name='VISUALIZATION_State_Light';stateLight.position.y=.284;root.add(stateLight);

tuneProductMaterials(root,materialMode);root.traverse(o=>{if(o.isMesh){o.layers.enable(1);o.castShadow=true;o.receiveShadow=true;}});
if(shot==='diffuser'){
  housing.material.transparent=true;housing.material.opacity=.08;bottomCover.visible=false;foot.visible=false;knob.visible=false;
  stateLight.material.emissiveIntensity=.72;stateLight.material.opacity=.13;
}
if(shot==='knob'){
  diffuser.material.transparent=true;diffuser.material.opacity=.08;stateLight.visible=false;
  housing.material.roughness=.48;housing.material.envMapIntensity=1.25;
}
if(shot==='shadow'){
  stateLight.visible=false;diffuser.visible=false;knob.visible=false;
  studio.cyclorama.children.forEach((c,i)=>{if(i===1)c.visible=false;});
  scene.background=new THREE.Color(0xe2ddd5);
}

const contactShadow=new ContactShadow(renderer,scene,root,{resolution:shot==='shadow'?1536:1024,opacity:shot==='shadow'?.46:.27,blur:shot==='shadow'?2.05:2.35});
const post=createPostProcessing(renderer,scene,camera,materialMode);post.setSize(1200,900);for(let i=0;i<12;i++)post.render(1/60);
const gl=renderer.getContext(),dbg=gl.getExtension('WEBGL_debug_renderer_info');
window.__WEBGL_INFO={renderer:dbg?gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL):gl.getParameter(gl.RENDERER),vendor:dbg?gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL):gl.getParameter(gl.VENDOR),version:gl.getParameter(gl.VERSION)};
window.__CALIBRATION_READY=true;document.querySelector('#label').textContent=`${shot.toUpperCase()} / ${window.__WEBGL_INFO.renderer}`;
