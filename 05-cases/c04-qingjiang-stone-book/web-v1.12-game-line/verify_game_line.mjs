import fs from "node:fs";
import path from "node:path";
import {fileURLToPath} from "node:url";

const root=path.dirname(fileURLToPath(import.meta.url));
const html=fs.readFileSync(path.join(root,"index.html"),"utf8");
const css=fs.readFileSync(path.join(root,"styles.css"),"utf8");
const pages=[...html.matchAll(/data-page="(\d{3})"/g)].map(match=>match[1]);
const chapters=new Set([...html.matchAll(/data-chapter="(CH\d{2})"/g)].map(match=>match[1]));
const refs=[...html.matchAll(/(?:src|href)="([^"#]+)"/g)].map(match=>match[1]).filter(ref=>!ref.startsWith("http")&&!ref.startsWith("mailto:")&&!ref.startsWith("data:"));
const missing=[...new Set(refs.filter(ref=>!fs.existsSync(path.join(root,ref))))];
const result={
  schema:"C04_WEB_V1_12_R2_STATIC_READBACK",
  carrier_surfaces:pages.length,
  unique_sequence_indexes:new Set(pages).size,
  first_sequence:pages[0],last_sequence:pages.at(-1),
  chapters:chapters.size,
  game_line_panels:(html.match(/class="game-delta/g)||[]).length,
  native_interaction_controls:(html.match(/<(?:button)[ >]/g)||[]).length,
  refined_components:{relation_flow:/class="relation-flow/.test(html),boat_library:/class="boat-library/.test(html),morph_workbench:/class="morph-workbench/.test(html),age_depth_ar:/class="age-tabs/.test(html),personal_imprint_map:/class="personal-map/.test(html),body_carriers:/class="carrier-grid/.test(html),butterfly_sequence:/class="butterfly-sequence/.test(html),card_camp_system:/class="card-system/.test(html),technical_register:/class="register-table/.test(html)},
  reduced_motion:/prefers-reduced-motion:reduce/.test(css),
  missing_local_runtime_refs:missing,
  truth_boundary:"FIELD OBSERVED=0 / FIELD MEASURED=0 / G1F HOLD / NO_PROMOTION / NTS / NOT FOR CONSTRUCTION"
};
const pass=result.carrier_surfaces===112&&result.unique_sequence_indexes===112&&result.first_sequence==="001"&&result.last_sequence==="112"&&result.chapters===20&&result.game_line_panels===9&&missing.length===0&&Object.values(result.refined_components).every(Boolean);
result.pass=pass;
fs.writeFileSync(path.join(root,"C04_WEB_v1_12_R2_STATIC_READBACK.json"),JSON.stringify(result,null,2)+"\n");
console.log(JSON.stringify(result,null,2));
if(!pass)process.exit(1);
