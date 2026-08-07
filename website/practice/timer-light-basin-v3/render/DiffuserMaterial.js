import * as THREE from 'three';

export const DIFFUSER_VISUALIZATION_PROFILE = Object.freeze({
  status: 'VISUALIZATION ONLY / NOT MEASURED OPTICAL DATA',
  ior: 1.49,
  transmission: 0.9,
  roughness: 0.19,
  thicknessHero: 0.055,
  thicknessMaterial: 0.075,
  attenuationDistance: 0.32,
  attenuationColor: 0xffedd2
});

export function createDiffuserMaterial(mode='hero') {
  const p=DIFFUSER_VISUALIZATION_PROFILE;
  return new THREE.MeshPhysicalMaterial({
    color:0xf6f1e8,
    roughness:p.roughness,
    metalness:0,
    transmission:p.transmission,
    thickness:mode==='material'?p.thicknessMaterial:p.thicknessHero,
    ior:p.ior,
    attenuationColor:new THREE.Color(p.attenuationColor),
    attenuationDistance:p.attenuationDistance,
    specularIntensity:0.52,
    clearcoat:0.02,
    clearcoatRoughness:0.68,
    side:THREE.FrontSide
  });
}

export function createStateLightMaterial() {
  return new THREE.MeshStandardMaterial({
    color:0xffd5a0,
    emissive:0xff9638,
    emissiveIntensity:1.55,
    roughness:0.28,
    metalness:0,
    transparent:true,
    opacity:0.26,
    depthWrite:false
  });
}

export function tuneProductMaterials(root, mode='hero') {
  const meshes=[];
  root.traverse((obj)=>{
    if(!obj.isMesh) return;
    const n=obj.name||'';
    if(/01_Upper_Housing/.test(n)){
      obj.material=new THREE.MeshPhysicalMaterial({
        color:0x706b65, metalness:0, roughness:0.54,
        clearcoat:0.055, clearcoatRoughness:0.66,
        ior:1.46, specularIntensity:0.44
      });
    } else if(/02_Formed_Diffuser/.test(n)){
      obj.material=createDiffuserMaterial(mode);
    } else if(/VISUALIZATION_State_Light/.test(n)){
      obj.material=createStateLightMaterial();
    } else if(/17_Side_Knob/.test(n)){
      obj.material=new THREE.MeshPhysicalMaterial({
        color:0xb8b9b9, metalness:1, roughness:0.20,
        clearcoat:0.025, clearcoatRoughness:0.36
      });
    } else if(/07_Aluminum_Heat_Spreader|12_USB_C_Shell|16_Encoder_Shaft|20_3x_ISO/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0xbfc2c3,metalness:1,roughness:0.24});
    } else if(/18_Bottom_Cover/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0x45413d,metalness:0,roughness:0.77});
    } else if(/19_Silicone_Foot_Ring/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0x171717,metalness:0,roughness:0.95});
    } else if(/04_LED_PCB|09_Controller_PCB|10_XIAO/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0x16463a,metalness:0,roughness:0.56});
    }
    if(obj.material){
      if('envMapIntensity' in obj.material) obj.material.envMapIntensity=1.35;
      obj.material.needsUpdate=true;
    }
    obj.castShadow=true; obj.receiveShadow=true;
    obj.layers.enable(1);
    meshes.push(obj);
  });
  return meshes;
}
