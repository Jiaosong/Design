import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.dirname(fileURLToPath(import.meta.url));
const read=(name)=>fs.readFileSync(path.join(root,name),"utf8");
const html=read("index.html");
const css=read("styles.css");
const js=read("app.js");
const effectsCss=read("effects.css");
const effectsJs=read("effects.js");

function isRepoLocalRef(ref){
  if(!ref || ref.startsWith("#")) return false;
  return !/^(?:[a-z]+:)?\/\//i.test(ref) && !/^(?:data|mailto|tel|javascript):/i.test(ref);
}
function collectRawLocalRefs(text){
  const refs=[];
  for(const match of text.matchAll(/(?:src|href)=["']([^"']+)["']/g)) if(isRepoLocalRef(match[1])) refs.push(match[1]);
  for(const match of text.matchAll(/url\(\s*["']?([^)'"\s]+)["']?\s*\)/g)) if(isRepoLocalRef(match[1])) refs.push(match[1]);
  return refs;
}
function collectRuntimeAssetStrings(text){
  return [...text.matchAll(/["']((?:assets|support)\/[A-Za-z0-9_./-]+\.(?:svg|png|jpe?g|webp|html|json))["']/g)].map(m=>m[1]);
}
function normalizeRootRelative(file){return path.relative(root,file).split(path.sep).join("/");}
function resolveFrom(baseDir,ref){return path.resolve(baseDir,ref.split(/[?#]/,1)[0]);}

function collectRuntimeDependencyGraph(){
  const entryFiles=["index.html","styles.css","app.js","effects.css","effects.js"];
  const queue=[...entryFiles];
  const scanned=new Set();
  const refs=new Set(entryFiles);
  const textLike=new Set([".html",".htm",".css",".js",".mjs",".svg",".json"]);
  while(queue.length){
    const rel=queue.shift();
    if(scanned.has(rel)) continue;
    scanned.add(rel);
    const file=path.resolve(root,rel);
    if(!fs.existsSync(file) || !fs.statSync(file).isFile()) continue;
    if(!textLike.has(path.extname(file).toLowerCase())) continue;
    const text=fs.readFileSync(file,"utf8");
    const baseDir=path.dirname(file);
    const raw=[...collectRawLocalRefs(text),...collectRuntimeAssetStrings(text)];
    for(const rawRef of raw){
      const resolved=resolveFrom(baseDir,rawRef);
      const normalized=normalizeRootRelative(resolved);
      refs.add(normalized);
      if(textLike.has(path.extname(resolved).toLowerCase()) && !scanned.has(normalized)) queue.push(normalized);
    }
  }
  return [...refs].sort();
}

const sections=[...html.matchAll(/data-section="(\d{2})"/g)].map(m=>Number(m[1]));
const contiguousSections=sections.length>0 && sections.every((n,i)=>n===i+1);
const coreAnchors=["hero","assets","brief","idea","system","digital","scenes","physical","brandmemory","final"];
const referencedRepoLocalFiles=collectRuntimeDependencyGraph();
const missingRepoLocalFiles=referencedRepoLocalFiles.filter(ref=>!fs.existsSync(path.resolve(root,ref)));
const emptyRepoLocalFiles=referencedRepoLocalFiles.filter(ref=>{
  const file=path.resolve(root,ref);
  return fs.existsSync(file)&&fs.statSync(file).isFile()&&fs.statSync(file).size===0;
});
const referencedAssets=referencedRepoLocalFiles.filter(ref=>ref.startsWith("assets/"));

const qjdRuntimeTargets=["assets/hero_qingjiang.jpg","assets/r06_qingjiang.jpg","assets/r13_passage_sequence.png"];
const qjdMaterializationMissing=qjdRuntimeTargets.filter(ref=>!fs.existsSync(path.resolve(root,ref)));
const qjdManifest="support/C04_QJD_RUNTIME_MATERIALIZATION_20260830.json";
const currentVectorAssets=["assets/brand_system_current.svg","assets/memory_journal_current.svg","assets/body_need_scenarios_current.svg"];
const currentVectorAssetsPresent=currentVectorAssets.every(ref=>fs.existsSync(path.resolve(root,ref))&&fs.statSync(path.resolve(root,ref)).size>0);
const currentVectorBindingsPresent=currentVectorAssets.every(ref=>effectsJs.includes(ref));

const forbiddenPublicPatterns=[/CH\d{2}-P\d+/i,/PR\s*#\d+/i,/blob\s+[0-9a-f]{7,}/i,/DESIGN REVIEW PENDING/i,/NO_PROMOTION/i,/FIELD OBSERVED/i];
const forbiddenVisible=forbiddenPublicPatterns.filter(pattern=>pattern.test(html)).map(pattern=>pattern.source);
const staleForcedMainAssets=["assets/fluid_v26_body_posture.png","assets/fluid_rest_object.png","assets/r06_technical.png"];
const staleForcedMainPresent=staleForcedMainAssets.filter(ref=>html.includes(ref)||effectsJs.includes(ref));

const result={
  schema:"C04_WEB_PUBLIC_PORTFOLIO_STATIC_CHECK_V1_20",
  section_count:sections.length,
  section_numbers:sections,
  contiguous_section_numbering:contiguousSections,
  core_anchors_present:coreAnchors.every(id=>html.includes(`id=\"${id}\"`)),
  runtime_dependency_graph_entrypoints:["index.html","styles.css","app.js","effects.css","effects.js"],
  repo_local_reference_count:referencedRepoLocalFiles.length,
  runtime_asset_reference_count:referencedAssets.length,
  missing_repo_local_count:missingRepoLocalFiles.length,
  missing_repo_local_files:missingRepoLocalFiles,
  empty_repo_local_count:emptyRepoLocalFiles.length,
  empty_repo_local_files:emptyRepoLocalFiles,
  qjd_materialization_manifest_present:fs.existsSync(path.resolve(root,qjdManifest)),
  qjd_runtime_targets:qjdRuntimeTargets,
  qjd_runtime_materialization_missing:qjdMaterializationMissing,
  current_vector_assets:currentVectorAssets,
  current_vector_assets_present:currentVectorAssetsPresent,
  current_vector_bindings_present:currentVectorBindingsPresent,
  internal_production_tokens_visible:forbiddenVisible,
  stale_forced_main_assets_present:staleForcedMainPresent,
  live_svg_present:/<svg[\s>]/i.test(html),
  responsive_css:/@media\(max-width:/i.test(css+effectsCss),
  reduced_motion_source_rule_present:/prefers-reduced-motion\s*:\s*reduce/i.test(css+effectsCss)&&/prefers-reduced-motion\s*:\s*reduce/i.test(js+effectsJs),
  reduced_motion_runtime_preference_readback:"NOT_RUN",
  interaction_script:/imprints/.test(js)&&/syncPage/.test(js),
  supplement_trigger_present:js.includes('id="supplementTrigger"')&&js.includes('补充资料'),
  mybook_final_view_direct_bound:html.includes("support/C04_APP_V1_6_MY_BOOK_FINAL_VIEW.html")&&fs.existsSync(path.resolve(root,"support/C04_APP_V1_6_MY_BOOK_FINAL_VIEW.html")),
  r13_remote_concept_truth_boundary:html.includes("REMOTE CONCEPT / NOT SITE PHOTO")&&html.includes("非现场照片")&&html.includes("不作为现场照片或测量证据"),
  authority_keep_not_pixel_keep:true,
  hold_assets_not_required_for_public_pass:true,
  public_runtime_truth:"RESEARCH-GRADE DESIGN / FIELD AND ENGINEERING VALIDATION REMAIN OPEN"
};

result.structure_pass=result.section_count>=10&&result.contiguous_section_numbering&&result.core_anchors_present&&result.internal_production_tokens_visible.length===0&&result.responsive_css&&result.reduced_motion_source_rule_present&&result.interaction_script&&result.supplement_trigger_present&&result.mybook_final_view_direct_bound&&result.r13_remote_concept_truth_boundary&&result.current_vector_assets_present&&result.current_vector_bindings_present&&result.stale_forced_main_assets_present.length===0;
result.repo_local_runtime_pass=result.missing_repo_local_count===0&&result.empty_repo_local_count===0&&result.qjd_runtime_materialization_missing.length===0;
result.pass=result.structure_pass&&result.repo_local_runtime_pass;

fs.writeFileSync(path.join(root,"C04_WEB_v1_12_R2_STATIC_READBACK.json"),JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
if(!result.pass) process.exit(1);
