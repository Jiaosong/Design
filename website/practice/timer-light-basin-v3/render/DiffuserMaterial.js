import * as THREE from 'three';

export const DIFFUSER_VISUALIZATION_PROFILE=Object.freeze({
  status:'VISUALIZATION ONLY / NOT MEASURED OPTICAL DATA',ior:1.49,transmission:0.42,roughness:0.31,
  thicknessHero:0.070,thicknessMaterial:0.095,attenuationDistance:0.14,attenuationColor:0xffe8c7
});

export function createDiffuserMaterial(mode='hero'){
  const p=DIFFUSER_VISUALIZATION_PROFILE;
  return new THREE.MeshPhysicalMaterial({color:0xf2eee7,roughness:p.roughness,metalness:0,transmission:p.transmission,
    thickness:mode==='material'?p.thicknessMaterial:p.thicknessHero,ior:p.ior,attenuationColor:new THREE.Color(p.attenuationColor),
    attenuationDistance:p.attenuationDistance,specularIntensity:0.66,clearcoat:0.015,clearcoatRoughness:0.72,side:THREE.FrontSide});
}

export function createStateLightMaterial(){
  return new THREE.MeshStandardMaterial({color:0xffddb3,emissive:0xff9a45,emissiveIntensity:0.82,roughness:0.42,metalness:0,transparent:true,opacity:0.16,depthWrite:false});
}

export function tuneProductMaterials(root,mode='hero'){
  const meshes=[];root.traverse(obj=>{if(!obj.isMesh)return;const n=obj.name||'';
    if(/01_Upper_Housing/.test(n))obj.material=new THREE.MeshPhysicalMaterial({color:0x858079,metalness:0,roughness:0.40,clearcoat:0.025,clearcoatRoughness:0.70,ior:1.46,specularIntensity:0.58});
    else if(/02_Formed_Diffuser/.test(n))obj.material=createDiffuserMaterial(mode);
    else if(/VISUALIZATION_State_Light/.test(n))obj.material=createStateLightMaterial();
    else if(/17_Side_Knob/.test(n))obj.material=new THREE.MeshPhysicalMaterial({color:0xa6a9aa,metalness:0.92,roughness:0.27,clearcoat:0.01,clearcoatRoughness:0.48,anisotropy:0.32,anisotropyRotation:Math.PI/2});
    else if(/07_Aluminum_Heat_Spreader|12_USB_C_Shell|16_Encoder_Shaft|20_3x_ISO/.test(n))obj.material=new THREE.MeshStandardMaterial({color:0xbfc2c3,metalness:1,roughness:0.24});
    else if(/18_Bottom_Cover/.test(n))obj.material=new THREE.MeshStandardMaterial({color:0x4d4944,metalness:0,roughness:0.80});
    else if(/19_Silicone_Foot_Ring/.test(n))obj.material=new THREE.MeshStandardMaterial({color:0x161616,metalness:0,roughness:0.96});
    else if(/04_LED_PCB|09_Controller_PCB|10_XIAO/.test(n))obj.material=new THREE.MeshStandardMaterial({color:0x16463a,metalness:0,roughness:0.56});
    if(obj.material){if('envMapIntensity'in obj.material)obj.material.envMapIntensity=/17_Side_Knob/.test(n)?1.75:1.65;obj.material.needsUpdate=true;}
    obj.castShadow=true;obj.receiveShadow=true;obj.layers.enable(1);meshes.push(obj);
  });return meshes;
}
