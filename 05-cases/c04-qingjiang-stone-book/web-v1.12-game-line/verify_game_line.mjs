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

function collectAssetRefs(text){
  const refs=[];
  for(const match of text.matchAll(/(?:src|href)=["'](assets\/[^"']+)["']/g)) refs.push(match[1]);
  for(const match of text.matchAll(/url\(\s*["']?(assets\/[^)"']+)["']?\s*\)/g)) refs.push(match[1]);
  return refs;
}

const referencedAssets=[...new Set([
  ...collectAssetRefs(html),
  ...collectAssetRefs(css),
  ...collectAssetRefs(js)
])].sort();
const missingAssets=referencedAssets.filter(ref=>!fs.existsSync(path.join(root,ref)));
const emptyAssets=referencedAssets.filter(ref=>{
  const file=path.join(root,ref);
  return fs.existsSync(file)&&fs.statSync(file).isFile()&&fs.statSync(file).size===0;
});
const forbiddenPublicPatterns=[/CH\d{2}-P\d+/i,/PR\s*#\d+/i,/blob\s+[0-9a-f]{7,}/i,/DESIGN REVIEW PENDING/i,/NO_PROMOTION/i,/FIELD OBSERVED/i];
const requiredPhrases=["原资产","设计创意","TASK FLOW / WORKFLOW","TECHNOLOGY APPLICATION ROUTE","AI + 3D CREATION PROCESS","INNOVATION POINTS","TECHNICAL DIFFICULTIES","DESIGN EVOLUTION / PROFESSIONAL JUDGMENT"];
const retiredFiles=[
  "C04_WEB_v1_11_V32_AUTHORING_V02_FRAMEWORK.json",
  "C04_WEB_v1_12_GAME_LINE_INTEGRATION_MAP.json",
  "C04_WEB_v1_12_PACKAGE_META_EXTERNAL.json",
  "integrate_game_delta.mjs"
];
const supplementTabs=["assets","idea","thinking","tech","workflow","innovation","ai3d"];
const supplementAssets=[
  "assets/hero_qingjiang.jpg",
  "assets/route03_locked_current.svg",
  "assets/r06_qingjiang.jpg",
  "assets/r13_passage_sequence.png",
  "assets/app_mybook.png",
  "assets/r06_general_assembly_v11.svg",
  "assets/r06_detail_atlas_v11.svg"
];

const result={
  schema:"C04_WEB_PUBLIC_PORTFOLIO_STATIC_CHECK_V1_16",
  section_count:sections.length,
  unique_sections:new Set(sections).size,
  ordered_sections:JSON.stringify(sections)===JSON.stringify(expected),
  anchors_present:anchors.every(id=>html.includes(`id=\"${id}\"`)),
  required_content_present:requiredPhrases.every(text=>html.includes(text)),
  runtime_asset_reference_count:referencedAssets.length,
  runtime_assets_referenced:referencedAssets,
  missing_asset_count:missingAssets.length,
  missing_assets:missingAssets,
  empty_asset_count:emptyAssets.length,
  empty_assets:emptyAssets,
  data_uri_images:(html.match(/src="data:/g)||[]).length,
  internal_production_tokens_visible:forbiddenPublicPatterns.filter(pattern=>pattern.test(html)).map(pattern=>pattern.source),
  retired_report_structure_absent:retiredFiles.every(file=>!fs.existsSync(path.join(root,file))),
  live_svg_present:/<svg[\s>]/i.test(html),
  responsive_css:/@media\(max-width:/i.test(css),
  reduced_motion_source_rule_present:/prefers-reduced-motion\s*:\s*reduce/i.test(css)&&/prefers-reduced-motion\s*:\s*reduce/i.test(js),
  reduced_motion_runtime_preference_readback:"NOT_RUN",
  interaction_script:/imprints/.test(js)&&/syncPage/.test(js),
  supplement_trigger_present:js.includes('id="supplementTrigger"')&&js.includes('补充资料'),
  supplement_tab_count:supplementTabs.filter(tab=>js.includes(`data-supplement-tab="${tab}"`)).length,
  supplement_panels_present:supplementTabs.every(tab=>js.includes(`data-supplement-panel="${tab}"`)),
  supplement_original_assets_present:supplementAssets.every(asset=>js.includes(asset)),
  supplement_ai3d_six_stage:js.includes('01 / SOURCE')&&js.includes('02 / AI EXPLORE')&&js.includes('03 / READBACK')&&js.includes('04 / 3D')&&js.includes('05 / DRAWING')&&js.includes('06 / DETAIL'),
  supplement_mobile_behavior:js.includes('@media(max-width:760px)')&&js.includes('@media(max-width:480px)'),
  supplement_escape_close:js.includes("event.key==='Escape'"),
  public_runtime_truth:"RESEARCH-GRADE DESIGN / FIELD AND ENGINEERING VALIDATION REMAIN OPEN"
};

result.pass=result.section_count===18&&result.unique_sections===18&&result.ordered_sections&&result.anchors_present&&result.required_content_present&&result.runtime_asset_reference_count>=10&&result.missing_asset_count===0&&result.empty_asset_count===0&&result.data_uri_images===0&&result.internal_production_tokens_visible.length===0&&result.retired_report_structure_absent&&result.live_svg_present&&result.responsive_css&&result.reduced_motion_source_rule_present&&result.interaction_script&&result.supplement_trigger_present&&result.supplement_tab_count===7&&result.supplement_panels_present&&result.supplement_original_assets_present&&result.supplement_ai3d_six_stage&&result.supplement_mobile_behavior&&result.supplement_escape_close;

fs.writeFileSync(path.join(root,"C04_WEB_v1_12_R2_STATIC_READBACK.json"),JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
if(!result.pass) process.exit(1);
