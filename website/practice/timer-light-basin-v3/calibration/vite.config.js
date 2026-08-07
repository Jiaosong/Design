import { defineConfig } from 'vite';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const practiceRoot=path.resolve(here,'..');
const nm=path.resolve(here,'node_modules');

export default defineConfig({
  server:{
    host:'127.0.0.1',
    port:4173,
    strictPort:true,
    fs:{allow:[here,practiceRoot]}
  },
  resolve:{
    alias:[
      {find:/^three$/,replacement:path.resolve(nm,'three/build/three.module.js')},
      {find:/^three\/addons\/(.*)$/,replacement:path.resolve(nm,'three/examples/jsm/$1')},
      {find:/^postprocessing$/,replacement:path.resolve(nm,'postprocessing/build/index.js')}
    ]
  },
  optimizeDeps:{
    include:['three','postprocessing']
  }
});
