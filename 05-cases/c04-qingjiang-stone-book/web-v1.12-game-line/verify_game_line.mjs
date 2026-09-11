import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.dirname(fileURLToPath(import.meta.url));
const read=n=>fs.readFileSync(path.join(root,n),"utf8");
const html=read("index.html");
const css=read("styles.css");
const js=read("app.js");

const currentAnchors=["hero","assets","journey","brief","context","audience","idea","thinking","systems","development","r13","final"];
const expectedSectionLabels=["01","02","03","04","05","06","07","08","09","10","10B","11"];
const sections=[...html.matchAll(/data-section="([^"]+)"/g)].map(m=>m[1]);
const contiguous=JSON.stringify(sections)===JSON.stringify(expectedSectionLabels);
const anchorsPresent=currentAnchors.every(id=>html.includes(`id="${id}"`));

const requiredAssets=[
  "assets/body_need_scenarios_current.svg",
  "assets/route03_locked_current.svg",
  "assets/physical_body_support_hold.svg",
  "assets/r13_passage_sequence_current.svg",
  "assets/return_service_closure_current.svg",
  "assets/qj_hero_keep_v11_b64_01.txt",
  "assets/qj_hero_keep_v11_b64_02a.txt"
];
const missing=requiredAssets.filter(r=>!fs.existsSync(path.join(root,r))||fs.statSync(path.join(root,r)).size===0);
const directBindings=[
  "assets/body_need_scenarios_current.svg",
  "assets/route03_locked_current.svg",
  "assets/r13_passage_sequence_current.svg",
  "assets/return_service_closure_current.svg"
].every(r=>html.includes(r));
const physicalCarrierBound=js.includes('assets/physical_body_support_hold.svg')
  &&fs.existsSync(path.join(root,"assets/physical_body_support_hold.svg"));
const localHeroBinding=[
  "qj_hero_keep_v11_b64_01.txt",
  "qj_hero_keep_v11_b64_02a.txt"
].every(r=>js.includes(r));

const externalImageRuntime=/https?:\/\/[^"'`\s]+\.(?:jpg|jpeg|png|webp)/i.test(`${html}\n${js}`);
const forbidden=[/112\s*页/i,/三个产品[^。]*项目主体/i,/01\s*\/\s*18/i].filter(p=>p.test(html)).map(p=>p.source);
const semanticCoverage=["十三印","数字","身体","识别","记忆","回程"].every(x=>html.includes(x));
const optionalReadingBoundary=/十三印可以不读完/.test(html)&&/不是追求\s*13\/13\s*完成率/.test(html);
const stateAndFallback=["NORMAL","DEGRADED","CLOSED","UNKNOWN","FULL / LIGHT / OFF"].every(x=>html.includes(x))
  &&html.includes("状态变化时，先保住路线与回程");
const truthBoundary=["FIELD OBSERVED=0","FIELD MEASURED=0","G1F HOLD","NO_PROMOTION"].every(x=>html.includes(x))
  &&html.includes("不把远程研究写成现场事实");
const progressiveDisclosure=html.includes('<details class="professional">')
  &&["品牌与视觉识别","记忆/IP/文化产品","关键场景","技术/模型/工程证明"].every(x=>html.includes(x));
const currentNavigation=[
  'href="#journey"','href="#context"','href="#thinking"','href="#systems"','href="#development"','href="#final"'
].every(x=>html.includes(x))
  &&['systems:["systems"]','development:["development","r13"]'].every(x=>js.includes(x))
  &&html.includes('id="r13" data-section="10B" data-nav-parent="development"')
  &&css.includes('content:" · 当前"');
const stateSimulationBound=js.includes('host.dataset.scope="explanatory-simulation"')
  &&js.includes('不表示实时运营状态');
const interactiveReading=[".mode-card",".audience-tab","syncPage"].every(x=>js.includes(x));
const staleLegacyRuntimeSelectors=["imprint-wheel","supplementTrigger","stateResult","r06Image"].filter(x=>js.includes(x));
const responsiveCss=/@media\s*\(max-width:/i.test(css);
const reducedMotion=/prefers-reduced-motion\s*:\s*reduce/i.test(css)&&/prefers-reduced-motion:\s*reduce/i.test(js);

const designReviewOpenItems=[];
if(!html.includes("R13"))designReviewOpenItems.push("R13_SCENE_SPECIFICITY_NOT_EXPLICIT_IN_CURRENT_PUBLIC_SPINE");
if(!html.includes("品牌与视觉识别")||!html.includes("记忆/IP/文化产品"))designReviewOpenItems.push("BRAND_MEMORY_INDEPENDENT_MAIN_SURFACE_REVIEW_OPEN");

const result={
  schema:"C04_CURRENTIZED_STATIC_CHECK_V2",
  current_frontier:"PR465",
  section_count:sections.length,
  section_numbers:sections,
  contiguous_current_section_numbering:contiguous,
  current_semantic_anchors_present:anchorsPresent,
  semantic_system_coverage_present:semanticCoverage,
  optional_reading_non_completion_boundary_present:optionalReadingBoundary,
  state_and_return_fail_closed_content_present:stateAndFallback,
  truth_boundary_present:truthBoundary,
  progressive_full_scope_disclosure_present:progressiveDisclosure,
  current_navigation_binding_present:currentNavigation,
  local_hero_runtime_binding_present:localHeroBinding,
  external_raster_image_dependency_present:externalImageRuntime,
  required_asset_count:requiredAssets.length,
  missing_or_empty_assets:missing,
  current_direct_assets_bound:directBindings,
  p01_b_physical_carrier_bound:physicalCarrierBound,
  operational_state_scope_explicitly_explanatory:stateSimulationBound,
  interactive_current_reading_present:interactiveReading,
  stale_legacy_runtime_selectors:staleLegacyRuntimeSelectors,
  responsive_css:responsiveCss,
  reduced_motion_present:reducedMotion,
  forbidden_public_compression_tokens:forbidden,
  design_review_open_items:designReviewOpenItems
};

result.pass=
  result.contiguous_current_section_numbering
  &&result.current_semantic_anchors_present
  &&result.semantic_system_coverage_present
  &&result.optional_reading_non_completion_boundary_present
  &&result.state_and_return_fail_closed_content_present
  &&result.truth_boundary_present
  &&result.progressive_full_scope_disclosure_present
  &&result.current_navigation_binding_present
  &&result.local_hero_runtime_binding_present
  &&!result.external_raster_image_dependency_present
  &&result.missing_or_empty_assets.length===0
  &&result.current_direct_assets_bound
  &&result.p01_b_physical_carrier_bound
  &&result.operational_state_scope_explicitly_explanatory
  &&result.interactive_current_reading_present
  &&result.stale_legacy_runtime_selectors.length===0
  &&result.responsive_css
  &&result.reduced_motion_present
  &&result.forbidden_public_compression_tokens.length===0;

fs.writeFileSync(path.join(root,"C04_WEB_v1_12_R2_STATIC_READBACK.json"),JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
if(!result.pass)process.exit(1);
