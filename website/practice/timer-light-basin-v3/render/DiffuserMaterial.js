import * as THREE from 'three';

export const DIFFUSER_VISUALIZATION_PROFILE = Object.freeze({
  status: 'VISUALIZATION ONLY / NOT MEASURED OPTICAL DATA',
  ior: 1.49,
  transmission: 0.34,
  roughness: 0.38,
  thicknessHero: 0.14,
  thicknessMaterial: 0.18,
  attenuationDistance: 0.11,
  attenuationColor: 0xffead2
});

export function createDiffuserMaterial(mode='hero') {
  const p=DIFFUSER_VISUALIZATION_PROFILE;
  return new THREE.MeshPhysicalMaterial({
    color:0xf2eee7,
    roughness:p.roughness,
    metalness:0,
    transmission:p.transmission,
    thickness:mode==='material'?p.thicknessMaterial:p.thicknessHero,
    ior:p.ior,
    attenuationColor:new THREE.Color(p.attenuationColor),
    attenuationDistance:p.attenuationDistance,
    specularIntensity:0.50,
    clearcoat:0.0,
    clearcoatRoughness:0.75,
    side:THREE.FrontSide
  });
}

export function createStateLightMaterial() {
  // Photography helper beneath the real formed diffuser. This is not physical LED/light-guide geometry.
  const hdr=new THREE.Color(0xffc58a).multiplyScalar(1.12);
  return new THREE.MeshBasicMaterial({
    color:hdr,
    side:THREE.DoubleSide,
    toneMapped:false,
    transparent:false,
    depthWrite:true
  });
}

export function tuneProductMaterials(root, mode='hero') {
  const meshes=[];
  root.traverse((obj)=>{
    if(!obj.isMesh) return;
    const n=obj.name||'';
    if(/01_Upper_Housing/.test(n)){
      obj.material=new THREE.MeshPhysicalMaterial({
        color:0x817a72, metalness:0, roughness:0.40,
        clearcoat:0.018, clearcoatRoughness:0.72,
        ior:1.46, specularIntensity:0.52,
        specularColor:new THREE.Color(0xf2ece4)
      });
      obj.material.envMapIntensity=1.70;
    } else if(/02_Formed_Diffuser/.test(n)){
      obj.material=createDiffuserMaterial(mode);
      obj.material.envMapIntensity=1.30;
    } else if(/VISUALIZATION_State_Light/.test(n)){
      obj.material=createStateLightMaterial();
    } else if(/17_Side_Knob/.test(n)){
      obj.material=new THREE.MeshPhysicalMaterial({
        color:0xc6c8c9, metalness:1, roughness:0.27,
        clearcoat:0.0, clearcoatRoughness:0.42,
        anisotropy:0.12
      });
      obj.material.envMapIntensity=2.35;
    } else if(/07_Aluminum_Heat_Spreader|12_USB_C_Shell|16_Encoder_Shaft|20_3x_ISO/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0xc3c6c7,metalness:1,roughness:0.28});
      obj.material.envMapIntensity=1.75;
    } else if(/18_Bottom_Cover/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0x4b4742,metalness:0,roughness:0.79});
    } else if(/19_Silicone_Foot_Ring/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0x181818,metalness:0,roughness:0.96});
    } else if(/04_LED_PCB|09_Controller_PCB|10_XIAO/.test(n)){
      obj.material=new THREE.MeshStandardMaterial({color:0x16463a,metalness:0,roughness:0.56});
    }
    if(obj.material){
      if('envMapIntensity' in obj.material && obj.material.envMapIntensity===1) obj.material.envMapIntensity=1.25;
      obj.material.needsUpdate=true;
    }
    obj.castShadow=true; obj.receiveShadow=true;
    obj.layers.enable(1);
    meshes.push(obj);
  });
  return meshes;
}
