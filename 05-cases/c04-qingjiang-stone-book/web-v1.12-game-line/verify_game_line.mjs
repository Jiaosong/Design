import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.dirname(fileURLToPath(import.meta.url));
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const css=fs.readFileSync(path.join(root,"styles.css"),"utf8");
const js=fs.readFileSync(path.join(root,"app.js"),"utf8");

const sections=[...html.matchAll(/data-section="(\d{2})"/g)].map(match=>match[1]);
const expected=Array.from({length:18},(_,index)=>String(index+1).padStart(2,"0"));
const anchors=["hero","assets","brief","idea","thinking","workflow","system","digital","scenes","physical","brandmemory","technology","ai3d","technicalproof","innovation","difficulties","evolution","final"];
const assetRefs=[...html.matchAll(/src="(assets\/[^"]+)"/g)].map(match=>match[1]);
const forbiddenPublicPatterns=[/CH\d{2}-P\d+/i,/PR\s*#\d+/i,/blob\s+[0-9a-f]{7,}/i,/DESIGN REVIEW PENDING/i,/NO_PROMOTION/i,/FIELD OBSERVED/i];
const requiredPhrases=["原资产","设计创意","TASK FLOW / WORKFLOW","TECHNOLOGY APPLICATION ROUTE","AI + 3D CREATION PROCESS","INNOVATION POINTS","TECHNICAL DIFFICULTIES","DESIGN EVOLUTION / PROFESSIONAL JUDGMENT"];

const result={
  schema:"C04_WEB_PUBLIC_PORTFOLIO_STATIC_CHECK_V1_13",
  section_count:sections.length,
  unique_sections:new Set(sections).size,
  ordered_sections:JSON.stringify(sections)===JSON.stringify(expected),
  anchors_present:anchors.every(id=>html.includes(`id=\"${id}\"`)),
  required_content_present:requiredPhrases.every(text=>html.includes(text)),
  original_asset_reference_count:new Set(assetRefs).size,
  data_uri_images:(html.match(/src="data:/g)||[]).length,
  internal_production_tokens_visible:forbiddenPublicPatterns.filter(pattern=>pattern.test(html)).map(pattern=>pattern.source),
  live_svg_present:/<svg[\s>]/i.test(html),
  responsive_css:/@media\(max-width:/i.test(css),
  reduced_motion:/prefers-reduced-motion:reduce/i.test(css),
  interaction_script:/imprints/.test(js)&&/syncPage/.test(js),
  public_runtime_truth:"RESEARCH-GRADE DESIGN / FIELD AND ENGINEERING VALIDATION REMAIN OPEN"
};

result.pass=result.section_count===18&&result.unique_sections===18&&result.ordered_sections&&result.anchors_present&&result.required_content_present&&result.original_asset_reference_count>=10&&result.data_uri_images===0&&result.internal_production_tokens_visible.length===0&&result.live_svg_present&&result.responsive_css&&result.reduced_motion&&result.interaction_script;

fs.writeFileSync(path.join(root,"C04_WEB_v1_12_R2_STATIC_READBACK.json"),JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
if(!result.pass) process.exit(1);
