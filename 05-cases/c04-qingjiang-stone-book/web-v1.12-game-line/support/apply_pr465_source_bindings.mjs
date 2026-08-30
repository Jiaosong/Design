// One-shot compatibility repair helper for PR #465 effect layer. Delete after verified application.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const supportDir=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(supportDir);
const effectsJsPath=path.join(root,'effects.js');
const effectsCssPath=path.join(root,'effects.css');
let js=fs.readFileSync(effectsJsPath,'utf8');
let css=fs.readFileSync(effectsCssPath,'utf8');

const resetOld="    digitalQuote?.style.removeProperty('--digital-quote-alpha');";
const resetNew="    digitalQuote?.style.removeProperty('--digital-quote-opacity');\n    digitalQuote?.style.removeProperty('--digital-quote-x');";
if(js.includes(resetOld)) js=js.replace(resetOld,resetNew);

const stepOld="      thinkingSteps.forEach((step,index)=>step.classList.toggle('is-current',index===current&&thinkingProgress>.08&&thinkingProgress<.93));";
const stepNew="      const attentionActive=thinkingProgress>.08&&thinkingProgress<.93;\n      thinkingSteps.forEach((step,index)=>step.classList.toggle('is-current',index===current&&attentionActive));\n      thinking?.classList.toggle('effect-attention-active',attentionActive);";
if(js.includes(stepOld)) js=js.replace(stepOld,stepNew);

const quoteOld="      digitalQuote.style.setProperty('--digital-quote-alpha',quoteAlpha.toFixed(3));";
const quoteNew="      digitalQuote.style.setProperty('--digital-quote-opacity',(0.32+quoteAlpha*0.68).toFixed(3));\n      digitalQuote.style.setProperty('--digital-quote-x',`${((1-quoteAlpha)*18).toFixed(2)}px`);";
if(js.includes(quoteOld)) js=js.replace(quoteOld,quoteNew);

const hasOld='.motion-ready #thinking:has(.step-list li.is-current) .media-panel img{transform:scale(1);filter:saturate(.95) contrast(1.02)}';
const hasNew='.motion-ready #thinking.effect-attention-active .media-panel img{transform:scale(1);filter:saturate(.95) contrast(1.02)}';
if(css.includes(hasOld)) css=css.replace(hasOld,hasNew);

const quoteCssOld='.motion-ready #digital .large-quote{\n  opacity:calc(.32 + var(--digital-quote-alpha,0) * .68);\n  transform:translate3d(calc((1 - var(--digital-quote-alpha,0)) * 18px),0,0);\n  transition:opacity .2s linear;\n}';
const quoteCssNew='.motion-ready #digital .large-quote{\n  opacity:var(--digital-quote-opacity,.32);\n  transform:translate3d(var(--digital-quote-x,18px),0,0);\n  transition:opacity .2s linear;\n}';
if(css.includes(quoteCssOld)) css=css.replace(quoteCssOld,quoteCssNew);

if(js.includes('--digital-quote-alpha')) throw new Error('legacy digital quote alpha mapping remains');
if(css.includes(':has(')) throw new Error('CSS :has dependency remains');
if(css.includes('var(--digital-quote-alpha')) throw new Error('legacy CSS quote mapping remains');
if(!js.includes('effect-attention-active')) throw new Error('thinking attention class mapping missing');
if(!js.includes('--digital-quote-opacity')||!js.includes('--digital-quote-x')) throw new Error('direct digital quote mappings missing');
if(!css.includes('var(--digital-quote-opacity,.32)')||!css.includes('var(--digital-quote-x,18px)')) throw new Error('compatible digital quote CSS missing');

fs.writeFileSync(effectsJsPath,js);
fs.writeFileSync(effectsCssPath,css);
console.log(JSON.stringify({removed_has_dependency:true,removed_css_multiplication:true,direct_quote_mapping:true,syntax_check_by_workflow:true},null,2));
