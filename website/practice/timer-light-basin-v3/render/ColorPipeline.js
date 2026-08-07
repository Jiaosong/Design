import * as THREE from 'three';

export const COLOR_PIPELINE = Object.freeze({
  workflow:'LINEAR HDR -> POST -> TONE MAP -> sRGB',
  outputColorSpace:'SRGBColorSpace',
  rendererToneMapping:'NoToneMapping',
  exposureHero:0.93,
  exposureMaterial:0.96,
  evidenceBoundary:'Visualization pipeline; not a measured colorimetry or material-color proof.'
});

export function configureColorPipeline(renderer, mode='hero'){
  renderer.outputColorSpace=THREE.SRGBColorSpace;
  renderer.toneMapping=THREE.NoToneMapping;
  renderer.toneMappingExposure=mode==='material'?COLOR_PIPELINE.exposureMaterial:COLOR_PIPELINE.exposureHero;
  renderer.shadowMap.enabled=true;
  renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  renderer.sortObjects=true;
  return COLOR_PIPELINE;
}
