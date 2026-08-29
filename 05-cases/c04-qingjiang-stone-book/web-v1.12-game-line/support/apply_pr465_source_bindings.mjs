import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const supportDir=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(supportDir);
const indexPath=path.join(root,'index.html');
const stylesPath=path.join(root,'styles.css');

let html=fs.readFileSync(indexPath,'utf8');
let css=fs.readFileSync(stylesPath,'utf8');

const source='assets/app_mybook.png';
const carrier='support/C04_APP_V1_6_MY_BOOK_SOURCE_CARRIER.html';
const imgRe=/<img\s+class="contain"\s+src="assets\/app_mybook\.png"\s+alt="我的石书数字界面"\s*\/?>|<img\s+src="assets\/app_mybook\.png"\s+alt="我的石书界面"\s*\/?>/g;
let replacements=0;
html=html.replace(imgRe,(match)=>{
  replacements+=1;
  const title=match.includes('数字界面')?'App v1.6 我的石书数字界面':'App v1.6 我的石书界面';
  return `<iframe class="app-mybook-carrier" src="${carrier}" title="${title}" loading="lazy"></iframe>`;
});
if(replacements!==2){
  throw new Error(`expected exactly 2 app_mybook replacements, got ${replacements}`);
}
if(html.includes(source)) throw new Error('obsolete app_mybook.png reference remains');

const phoneRule='.phone img{display:block;width:100%;border-radius:34px;object-fit:contain;background:#111}';
const replacementRule='.phone img{display:block;width:100%;border-radius:34px;object-fit:contain;background:#111}.phone .app-mybook-carrier{display:block;width:100%;height:min(760px,78vh);min-height:620px;border:0;border-radius:34px;background:#f2efe6}';
if(!css.includes(phoneRule) && !css.includes('.phone .app-mybook-carrier')) throw new Error('phone image rule not found');
if(!css.includes('.phone .app-mybook-carrier')) css=css.replace(phoneRule,replacementRule);

fs.writeFileSync(indexPath,html);
fs.writeFileSync(stylesPath,css);
console.log(JSON.stringify({replacements,carrier,styles_bound:true},null,2));
