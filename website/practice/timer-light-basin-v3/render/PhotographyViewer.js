import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { applyStudioScene } from './StudioEnvironment.js';
import { tuneProductMaterials } from './DiffuserMaterial.js';
import { ContactShadow } from './ContactShadow.js';
import { configureColorPipeline } from './ColorPipeline.js';
import { createPostProcessing } from './PostProcessing.js';

const VIEWS={
  hero:{theta:-0.64,phi:1.02,distance:2.18,fov:27,focus:null},
  body:{theta:-0.62,phi:1.06,distance:2.05,fov:29,focus:null},
  top:{theta:0.02,phi:0.66,distance:1.80,fov:28,focus:/02_Formed_Diffuser|VISUALIZATION_State_Light/},
  control:{theta:-1.34,phi:1.14,distance:1.72,fov:30,focus:/17_Side_Knob|16_Encoder_Shaft|15_Bourns_PEC11R_Envelope/},
  rear:{theta:1.84,phi:1.14,distance:1.76,fov:30,focus:/12_USB_C_Shell|09_Controller_PCB|10_XIAO_RP2040/}
};

export class PhotographyViewer{
  constructor(root){
    this.root=root; this.wrap=root.querySelector('.studio-canvas');
    this.mode=root.dataset.view==='cmf'?'material':'hero';
    this.modelURL=root.dataset.modelSrc; this.meshes=[]; this.last=performance.now();
    this.scene=new THREE.Scene();
    this.camera=new THREE.PerspectiveCamera(28,1,0.01,50);
    this.renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance',alpha:false});
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));
    configureColorPipeline(this.renderer,this.mode);
    this.wrap.appendChild(this.renderer.domElement);
    this.studio=applyStudioScene(this.scene,this.renderer,this.mode);
    this.controls=new OrbitControls(this.camera,this.renderer.domElement);
    this.controls.enableDamping=true;this.controls.enablePan=false;
    this.controls.minPolarAngle=0.38;this.controls.maxPolarAngle=1.42;
    this.controls.minDistance=0.45;this.controls.maxDistance=5.0;
    this.group=new THREE.Group();this.scene.add(this.group);
    this.post=createPostProcessing(this.renderer,this.scene,this.camera,this.mode);
    this.load(); this.resize(); window.addEventListener('resize',()=>this.resize()); this.loop();
  }
  load(){
    new GLTFLoader().load(this.modelURL,(gltf)=>{
      this.object=gltf.scene;
      // Source geometry is Z-up; normalize once to Three.js Y-up before staging.
      this.object.rotation.x=-Math.PI/2;
      this.object.scale.setScalar(0.01);
      this.meshes=tuneProductMaterials(this.object,this.mode);
      this.group.add(this.object);
      this.normalizeToGround();
      this.contactShadow=new ContactShadow(this.renderer,this.scene,this.object,{
        resolution:this.mode==='hero'?1536:1024,
        opacity:this.mode==='hero'?0.30:0.25,
        blur:this.mode==='hero'?3.1:2.6
      });
      this.frame(this.mode==='hero'?VIEWS.hero:VIEWS.body);
      this.root.classList.add('is-loaded');
      const status=this.root.querySelector('.viewer-status');
      if(status) status.textContent='PHOTO PIPELINE READY';
    },undefined,(error)=>{
      console.error('PhotographyViewer GLB error',error);
      this.root.classList.add('is-error');
      const status=this.root.querySelector('.viewer-status');
      if(status) status.textContent='3D unavailable · HTML/SVG fallback remains';
    });
  }
  normalizeToGround(){
    this.object.updateMatrixWorld(true);
    let box=new THREE.Box3().setFromObject(this.object);
    const center=box.getCenter(new THREE.Vector3());
    this.object.position.x-=center.x;
    this.object.position.z-=center.z;
    this.object.position.y-=box.min.y;
    this.object.updateMatrixWorld(true);
  }
  selection(regex){
    if(!regex) return new THREE.Box3().setFromObject(this.object);
    const box=new THREE.Box3(); let hit=false;
    this.meshes.forEach((mesh)=>{if(regex.test(mesh.name)){box.expandByObject(mesh);hit=true;}});
    return hit?box:new THREE.Box3().setFromObject(this.object);
  }
  frame(preset){
    if(!this.object) return;
    const box=this.selection(preset.focus||null),size=box.getSize(new THREE.Vector3()),center=box.getCenter(new THREE.Vector3());
    const radius=Math.max(size.x,size.y,size.z)*preset.distance;
    this.camera.fov=preset.fov;
    this.camera.position.set(
      center.x+radius*Math.sin(preset.phi)*Math.sin(preset.theta),
      center.y+radius*Math.cos(preset.phi)+size.y*0.10,
      center.z+radius*Math.sin(preset.phi)*Math.cos(preset.theta)
    );
    this.controls.target.copy(center).add(new THREE.Vector3(0,size.y*0.04,0));
    this.camera.near=Math.max(0.01,radius/100);this.camera.far=radius*22;this.camera.updateProjectionMatrix();this.controls.update();
  }
  focus(key){
    const preset=VIEWS[key]||VIEWS.body;
    this.meshes.forEach((mesh)=>{
      mesh.visible=true;const material=mesh.material;if(!material)return;
      if(key==='body'){
        if(!/VISUALIZATION_State_Light/.test(mesh.name)){material.transparent=false;material.opacity=1;}
      }else if(!/02_Formed_Diffuser|VISUALIZATION_State_Light/.test(mesh.name)){
        const selected=!preset.focus||preset.focus.test(mesh.name);
        material.transparent=true;material.opacity=selected?1:0.11;
      }
      material.needsUpdate=true;
    });
    this.frame(preset);
  }
  resize(){
    const w=this.wrap.clientWidth||600,h=this.wrap.clientHeight||600;
    this.camera.aspect=w/h;this.camera.updateProjectionMatrix();this.renderer.setSize(w,h,false);this.post.setSize(w,h);
  }
  loop(){
    requestAnimationFrame(()=>this.loop());
    const now=performance.now(),delta=Math.min(0.05,(now-this.last)/1000);this.last=now;
    this.controls.update();this.post.render(delta);
  }
}
