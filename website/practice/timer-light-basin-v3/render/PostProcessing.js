import * as THREE from 'three';
import {
  BloomEffect,
  EffectComposer,
  EffectPass,
  RenderPass,
  ToneMappingEffect,
  ToneMappingMode
} from 'postprocessing';

export const POST_PROFILE = Object.freeze({
  framebuffer:'HalfFloatType',
  bloom:{intensity:0.12,luminanceThreshold:1.15,luminanceSmoothing:0.18,mipmapBlur:true},
  toneMapping:'AGX',
  rule:'Bloom supports the luminous surface only; it must not hide geometry/material defects.'
});

export function createPostProcessing(renderer,scene,camera,mode='hero'){
  const composer=new EffectComposer(renderer,{frameBufferType:THREE.HalfFloatType});
  composer.addPass(new RenderPass(scene,camera));
  const bloom=new BloomEffect({
    intensity:mode==='hero'?0.12:0.08,
    luminanceThreshold:1.15,
    luminanceSmoothing:0.18,
    mipmapBlur:true
  });
  const toneMapping=new ToneMappingEffect({mode:ToneMappingMode.AGX});
  composer.addPass(new EffectPass(camera,bloom));
  composer.addPass(new EffectPass(camera,toneMapping));
  return {
    composer,bloom,toneMapping,
    setSize:(w,h)=>composer.setSize(w,h),
    render:(delta)=>composer.render(delta),
    dispose:()=>composer.dispose()
  };
}
