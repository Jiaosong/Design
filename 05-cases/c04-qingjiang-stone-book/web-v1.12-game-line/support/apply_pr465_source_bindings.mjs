// One-shot bounded patch helper for PR #465 effect binding. Delete after verified application.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const supportDir=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(supportDir);
const indexPath=path.join(root,'index.html');
const appPath=path.join(root,'app.js');
const effectsPath=path.join(root,'effects.css');

let html=fs.readFileSync(indexPath,'utf8');
let app=fs.readFileSync(appPath,'utf8');
let effects=fs.readFileSync(effectsPath,'utf8');

const stylesLink='  <link rel="stylesheet" href="styles.css" />';
const effectsLink='  <link rel="stylesheet" href="effects.css" />';
if(!html.includes(effectsLink)){
  if(!html.includes(stylesLink)) throw new Error('styles.css binding point missing');
  html=html.replace(stylesLink,`${stylesLink}\n${effectsLink}`);
}

const appScript='  <script src="app.js"></script>';
const effectsScript='  <script src="effects.js"></script>';
if(!html.includes(effectsScript)){
  if(!html.includes(appScript)) throw new Error('app.js binding point missing');
  html=html.replace(appScript,`${appScript}\n${effectsScript}`);
}

const oldSupplement='<img class="contain" src="assets/app_mybook.png" alt="数字记忆界面">';
const newSupplement='<iframe class="supplement-app-carrier" src="support/C04_APP_V1_6_MY_BOOK_SOURCE_CARRIER.html" title="App v1.6 我的石书数字界面" loading="lazy"></iframe>';
const oldCount=app.split(oldSupplement).length-1;
if(oldCount>1) throw new Error(`expected at most one supplement MY BOOK source, got ${oldCount}`);
if(oldCount===1) app=app.replace(oldSupplement,newSupplement);
if(app.includes('assets/app_mybook.png')) throw new Error('obsolete supplement app_mybook.png reference remains');
if(!app.includes(newSupplement)) throw new Error('supplement MY BOOK current carrier missing');

const carrierRules='\n.asset-card .app-mybook-carrier{display:block;width:100%;height:100%;min-height:350px;border:0;background:#f2efe6}\n.supplement-asset .supplement-app-carrier{display:block;width:100%;height:126px;border:0;background:#f2efe6}\n@media(max-width:860px){.supplement-asset .supplement-app-carrier{height:110px}}\n@media(max-width:480px){.supplement-asset .supplement-app-carrier{height:136px}}\n';
if(!effects.includes('.asset-card .app-mybook-carrier')) effects+=carrierRules;

fs.writeFileSync(indexPath,html);
fs.writeFileSync(appPath,app);
fs.writeFileSync(effectsPath,effects);
console.log(JSON.stringify({effects_css_bound:true,effects_js_bound:true,supplement_mybook_currentized:true,carrier_fit_rules:true},null,2));
