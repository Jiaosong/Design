import * as THREE from 'three';
import { HorizontalBlurShader } from 'three/addons/shaders/HorizontalBlurShader.js';
import { VerticalBlurShader } from 'three/addons/shaders/VerticalBlurShader.js';

const VERTEX = `
  varying float vWorldY;
  void main(){
    vec4 world = modelMatrix * vec4(position, 1.0);
    vWorldY = world.y;
    gl_Position = projectionMatrix * viewMatrix * world;
  }
`;
const FRAGMENT = `
  uniform float groundY;
  uniform float heightRange;
  varying float vWorldY;
  void main(){
    float h = clamp((vWorldY-groundY)/max(heightRange,0.001),0.0,1.0);
    float contact = 1.0 - smoothstep(0.0,0.48,h);
    float alpha = 0.025 + 0.72 * contact * contact;
    gl_FragColor = vec4(0.0,0.0,0.0,alpha);
  }
`;

export class ContactShadow {
  constructor(renderer, scene, root, {resolution=1536, opacity=0.18, blur=4.8}={}){
    this.renderer=renderer; this.scene=scene; this.root=root;
    this.resolution=resolution; this.opacity=opacity; this.blurAmount=blur;
    this.targetA=new THREE.WebGLRenderTarget(resolution,resolution,{type:THREE.HalfFloatType,depthBuffer:true});
    this.targetB=new THREE.WebGLRenderTarget(resolution,resolution,{type:THREE.HalfFloatType,depthBuffer:false});
    this.camera=new THREE.OrthographicCamera(-1,1,1,-1,0.01,10);
    this.camera.layers.set(1);
    this.captureMaterial=new THREE.ShaderMaterial({
      uniforms:{groundY:{value:0},heightRange:{value:0.35}},
      vertexShader:VERTEX,fragmentShader:FRAGMENT,transparent:true,depthTest:true,depthWrite:true
    });
    this.blurScene=new THREE.Scene();
    this.blurCamera=new THREE.OrthographicCamera(-1,1,1,-1,0,1);
    this.blurPlane=new THREE.Mesh(new THREE.PlaneGeometry(2,2));
    this.blurScene.add(this.blurPlane);
    this.horizontal=new THREE.ShaderMaterial(HorizontalBlurShader);
    this.vertical=new THREE.ShaderMaterial(VerticalBlurShader);
    this.shadowMaterial=new THREE.MeshBasicMaterial({map:this.targetA.texture,transparent:true,opacity,depthWrite:false,toneMapped:false});
    this.shadowPlane=new THREE.Mesh(new THREE.PlaneGeometry(1,1),this.shadowMaterial);
    this.shadowPlane.rotation.x=-Math.PI/2; this.shadowPlane.position.y=0.002; this.shadowPlane.renderOrder=1;
    this.shadowPlane.name='PHOTOGRAPHY_CONTACT_SHADOW';
    scene.add(this.shadowPlane);
    this.updateBounds();
    this.render();
  }
  updateBounds(){
    const box=new THREE.Box3().setFromObject(this.root);
    const size=box.getSize(new THREE.Vector3());
    const center=box.getCenter(new THREE.Vector3());
    const span=Math.max(size.x,size.z)*1.48;
    const half=span/2;
    this.camera.left=-half; this.camera.right=half; this.camera.top=half; this.camera.bottom=-half;
    this.camera.near=0.01; this.camera.far=Math.max(2,size.y+1.2);
    this.camera.position.set(center.x,box.max.y+0.6,center.z);
    this.camera.up.set(0,0,-1); this.camera.lookAt(center.x,box.min.y,center.z); this.camera.updateProjectionMatrix();
    this.captureMaterial.uniforms.groundY.value=box.min.y;
    this.captureMaterial.uniforms.heightRange.value=Math.max(size.y,0.08);
    this.shadowPlane.position.x=center.x; this.shadowPlane.position.z=center.z;
    this.shadowPlane.position.y=box.min.y+0.002;
    this.shadowPlane.scale.set(span,span,1);
  }
  blur(targetIn,targetOut,amount,horizontal=true){
    const mat=horizontal?this.horizontal:this.vertical;
    mat.uniforms.tDiffuse.value=targetIn.texture;
    if(horizontal) mat.uniforms.h.value=amount/this.resolution;
    else mat.uniforms.v.value=amount/this.resolution;
    this.blurPlane.material=mat;
    this.renderer.setRenderTarget(targetOut);
    this.renderer.render(this.blurScene,this.blurCamera);
  }
  render(){
    const previousTarget=this.renderer.getRenderTarget();
    const previousOverride=this.scene.overrideMaterial;
    const previousBackground=this.scene.background;
    const previousAutoClear=this.renderer.autoClear;
    const previousColor=new THREE.Color(); this.renderer.getClearColor(previousColor);
    const previousAlpha=this.renderer.getClearAlpha();
    this.shadowPlane.visible=false;
    this.scene.overrideMaterial=this.captureMaterial;
    this.scene.background=null;
    this.renderer.autoClear=true;
    this.renderer.setClearColor(0xffffff,0);
    this.renderer.setRenderTarget(this.targetA);
    this.renderer.clear(true,true,true);
    this.renderer.render(this.scene,this.camera);
    this.scene.overrideMaterial=previousOverride;
    this.scene.background=previousBackground;
    this.blur(this.targetA,this.targetB,this.blurAmount,true);
    this.blur(this.targetB,this.targetA,this.blurAmount,false);
    this.blur(this.targetA,this.targetB,this.blurAmount*0.72,true);
    this.blur(this.targetB,this.targetA,this.blurAmount*0.64,false);
    this.renderer.setRenderTarget(previousTarget);
    this.renderer.setClearColor(previousColor,previousAlpha);
    this.renderer.autoClear=previousAutoClear;
    this.shadowPlane.visible=true;
    this.shadowMaterial.map=this.targetA.texture; this.shadowMaterial.needsUpdate=true;
  }
  setOpacity(value){this.opacity=value;this.shadowMaterial.opacity=value;}
  dispose(){
    this.targetA.dispose();this.targetB.dispose();this.captureMaterial.dispose();
    this.horizontal.dispose();this.vertical.dispose();this.shadowMaterial.dispose();
    this.shadowPlane.geometry.dispose();this.blurPlane.geometry.dispose();
  }
}
