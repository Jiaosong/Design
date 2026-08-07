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
    float alpha = 0.025 + 0.74 * contact * contact;
    gl_FragColor = vec4(0.0,0.0,0.0,alpha);
  }
`;

export class ContactShadow {
  constructor(renderer, scene, root, {resolution=1536, opacity=0.22, blur=5.2}={}){
    this.renderer=renderer; this.scene=scene; this.root=root;
    this.resolution=resolution; this.opacity=opacity; this.blurAmount=blur;
    this.captureTarget=new THREE.WebGLRenderTarget(resolution,resolution,{type:THREE.HalfFloatType,depthBuffer:true});
    this.workTarget=new THREE.WebGLRenderTarget(resolution,resolution,{type:THREE.HalfFloatType,depthBuffer:false});
    this.tightTarget=new THREE.WebGLRenderTarget(resolution,resolution,{type:THREE.HalfFloatType,depthBuffer:false});
    this.broadTarget=new THREE.WebGLRenderTarget(resolution,resolution,{type:THREE.HalfFloatType,depthBuffer:false});
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

    const planeGeometry=new THREE.PlaneGeometry(1,1);
    this.broadMaterial=new THREE.MeshBasicMaterial({map:this.broadTarget.texture,transparent:true,opacity:opacity*0.58,depthWrite:false,toneMapped:false});
    this.broadPlane=new THREE.Mesh(planeGeometry,this.broadMaterial);
    this.broadPlane.rotation.x=-Math.PI/2; this.broadPlane.renderOrder=1;
    this.broadPlane.name='PHOTOGRAPHY_CONTACT_SHADOW_BROAD';
    scene.add(this.broadPlane);

    this.tightMaterial=new THREE.MeshBasicMaterial({map:this.tightTarget.texture,transparent:true,opacity:opacity*0.88,depthWrite:false,toneMapped:false});
    this.tightPlane=new THREE.Mesh(planeGeometry.clone(),this.tightMaterial);
    this.tightPlane.rotation.x=-Math.PI/2; this.tightPlane.renderOrder=2;
    this.tightPlane.name='PHOTOGRAPHY_CONTACT_SHADOW_TIGHT';
    scene.add(this.tightPlane);

    this.updateBounds();
    this.render();
  }
  updateBounds(){
    const box=new THREE.Box3().setFromObject(this.root);
    const size=box.getSize(new THREE.Vector3());
    const center=box.getCenter(new THREE.Vector3());
    const span=Math.max(size.x,size.z)*1.58;
    const half=span/2;
    this.camera.left=-half; this.camera.right=half; this.camera.top=half; this.camera.bottom=-half;
    this.camera.near=0.01; this.camera.far=Math.max(2,size.y+1.2);
    this.camera.position.set(center.x,box.max.y+0.6,center.z);
    this.camera.up.set(0,0,-1); this.camera.lookAt(center.x,box.min.y,center.z); this.camera.updateProjectionMatrix();
    this.captureMaterial.uniforms.groundY.value=box.min.y;
    this.captureMaterial.uniforms.heightRange.value=Math.max(size.y,0.08);
    for(const plane of [this.broadPlane,this.tightPlane]){
      plane.position.x=center.x; plane.position.z=center.z;
      plane.position.y=box.min.y+0.002;
      plane.scale.set(span,span,1);
    }
    this.tightPlane.position.y=box.min.y+0.0025;
  }
  blur(targetIn,targetOut,amount,horizontal=true){
    const mat=horizontal?this.horizontal:this.vertical;
    mat.uniforms.tDiffuse.value=targetIn.texture;
    if(horizontal) mat.uniforms.h.value=amount/this.resolution;
    else mat.uniforms.v.value=amount/this.resolution;
    this.blurPlane.material=mat;
    this.renderer.setRenderTarget(targetOut);
    this.renderer.clear(true,true,true);
    this.renderer.render(this.blurScene,this.blurCamera);
  }
  render(){
    const previousTarget=this.renderer.getRenderTarget();
    const previousOverride=this.scene.overrideMaterial;
    const previousBackground=this.scene.background;
    const previousAutoClear=this.renderer.autoClear;
    const previousColor=new THREE.Color(); this.renderer.getClearColor(previousColor);
    const previousAlpha=this.renderer.getClearAlpha();
    this.broadPlane.visible=false; this.tightPlane.visible=false;
    this.scene.overrideMaterial=this.captureMaterial;
    this.scene.background=null;
    this.renderer.autoClear=true;
    this.renderer.setClearColor(0xffffff,0);
    this.renderer.setRenderTarget(this.captureTarget);
    this.renderer.clear(true,true,true);
    this.renderer.render(this.scene,this.camera);
    this.scene.overrideMaterial=previousOverride;
    this.scene.background=previousBackground;

    // Tight contact: retains foot-ring density while removing the aliased black-outline read.
    const tightBlur=Math.max(1.25,this.blurAmount*0.28);
    this.blur(this.captureTarget,this.workTarget,tightBlur,true);
    this.blur(this.workTarget,this.tightTarget,tightBlur*0.92,false);

    // Broad ambient penumbra: starts from the tight result and spreads gently beyond the footprint.
    const broadBlur=this.blurAmount*1.35;
    this.blur(this.tightTarget,this.workTarget,broadBlur,true);
    this.blur(this.workTarget,this.broadTarget,broadBlur*0.92,false);
    this.blur(this.broadTarget,this.workTarget,broadBlur*0.55,true);
    this.blur(this.workTarget,this.broadTarget,broadBlur*0.48,false);

    this.renderer.setRenderTarget(previousTarget);
    this.renderer.setClearColor(previousColor,previousAlpha);
    this.renderer.autoClear=previousAutoClear;
    this.broadPlane.visible=true; this.tightPlane.visible=true;
    this.tightMaterial.map=this.tightTarget.texture; this.tightMaterial.needsUpdate=true;
    this.broadMaterial.map=this.broadTarget.texture; this.broadMaterial.needsUpdate=true;
  }
  setOpacity(value){
    this.opacity=value;
    this.tightMaterial.opacity=value*0.88;
    this.broadMaterial.opacity=value*0.58;
  }
  dispose(){
    this.captureTarget.dispose();this.workTarget.dispose();this.tightTarget.dispose();this.broadTarget.dispose();this.captureMaterial.dispose();
    this.horizontal.dispose();this.vertical.dispose();this.tightMaterial.dispose();this.broadMaterial.dispose();
    this.tightPlane.geometry.dispose();this.broadPlane.geometry.dispose();this.blurPlane.geometry.dispose();
  }
}
