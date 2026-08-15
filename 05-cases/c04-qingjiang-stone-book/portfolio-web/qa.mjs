import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';

const dir = path.dirname(new URL(import.meta.url).pathname);
const read = (name) => fs.readFileSync(path.join(dir, name), 'utf8');
const html = read('index.html');
const css = read('styles.css');
const drawingCss = read('drawing-gallery.css');
const offlineCss = read('offline-media.css');
const tokens = read('authority-tokens.css');
const app = read('app.js');
const dataSource = read('data.js');
const visibleTextSource = html.replace(/<br\s*\/?\s*>/gi, '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');

const failures = [];
const pass = (condition, message) => { if (!condition) failures.push(message); };

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(dataSource, sandbox);
const data = sandbox.window.C04_DATA;

pass(Boolean(data), 'C04_DATA missing');
pass(data?.meta?.fieldObserved === 0, 'FIELD OBSERVED must remain 0');
pass(data?.meta?.fieldMeasured === 0, 'FIELD MEASURED must remain 0');
pass(data?.meta?.g1f === 'HOLD', 'G1F must remain HOLD');
pass(data?.meta?.promotion === 'NO', 'Promotion must remain NO');

const routeIds = data.route.map(x => x.id);
pass(routeIds.join(',') === 'M0,M1,M2,M3,M4,M5,M6,M7', 'M0–M7 route contract incomplete or reordered');
pass(data.nodes.length === 13, 'Reading Library must expose 13 candidate pages');
pass(!html.includes('13/13'), 'No 13/13 completion logic allowed');
pass(visibleTextSource.includes('十三印不是十三站'), 'Non-linear reading-library proposition missing');
pass(html.includes('NOT GEOREFERENCED') || css.includes('NOT GEOREFERENCED') || offlineCss.includes('NOT GEOREFERENCED'), 'Map overlay must disclose non-georeferenced status');
pass(visibleTextSource.includes('非实测剖面'), 'Relational section must disclose non-measured status');
pass(visibleTextSource.includes('NOT FIELD VIDEO'), 'Motion study must disclose non-field-video status');
pass(visibleTextSource.includes('FIELD OBSERVED = 0') && visibleTextSource.includes('FIELD MEASURED = 0'), 'Visible field boundary missing');
pass(visibleTextSource.includes('G1F HOLD') && visibleTextSource.includes('NO PROMOTION'), 'Visible governance boundary missing');
pass(css.includes('@page{size:A3 landscape'), 'A3 landscape print rule missing');
pass(css.includes('@media(max-width:680px)'), 'Mobile responsive rule missing');
pass(app.includes("document.querySelectorAll('[data-route]')"), 'Plan/map linked-route interaction missing');
pass(app.includes('QJ-D-DUAL-QUALITY-GATE-2026-08-15'), 'Dual Quality Gate visual authority label is not loaded');
pass(app.includes('drawing-gallery.css'), 'Current QJ-C22 drawing gallery layer is not loaded');
pass(app.includes('offline-media.css'), 'Offline primary-media layer is not loaded');
pass(app.includes('IntersectionObserver'), 'Scroll narrative navigation missing');
pass(drawingCss.includes('.drawing-stage'), 'Drawing gallery responsive presentation contract missing');
pass(!/Paper\s*\/\s*Ink\s*\/\s*Line\s*\/\s*Seal/i.test(tokens), 'Superseded generic Seal visual language must not remain primary');
pass(tokens.includes('Relation Line') && tokens.includes('Evidence Trace'), 'Dual Gate relation/evidence visual language missing');

const drawingAssets = [
  'assets/drawings/00_Hero_Source-Grounded_Field.svg',
  'assets/drawings/01_Macro_Network_Masterplan.svg',
  'assets/drawings/05_Typical_Sections_A_B_C.svg'
];
for (const rel of drawingAssets) {
  const target = path.join(dir, rel);
  pass(fs.existsSync(target), `source-grounded drawing missing: ${rel}`);
}
for (const rel of drawingAssets.slice(1)) {
  const source = fs.readFileSync(path.join(dir, rel), 'utf8');
  pass(source.includes('FIELD OBSERVED=0') && source.includes('FIELD MEASURED=0'), `C22 source drawing field boundary missing: ${rel}`);
  pass(source.includes('G1F HOLD') && source.includes('NO_PROMOTION'), `C22 source drawing governance boundary missing: ${rel}`);
}
const heroSource = fs.readFileSync(path.join(dir, drawingAssets[0]), 'utf8');
pass(heroSource.includes('NOT SURVEY') && heroSource.includes('FIELD OBSERVED=0'), 'Hero source-grounded drawing boundary missing');
pass(offlineCss.includes("00_Hero_Source-Grounded_Field.svg"), 'Hero must use local source-grounded media');
pass(app.includes("01_Macro_Network_Masterplan.svg"), 'Atlas must switch to local C22 masterplan');

const requiredVisualTokens = {
  PAPER:'#F4F1E9', INK:'#17211F', QINGJIANG:'#3C8990', PEAK:'#566E5E', TRACE:'#6E7874', SIGNAL:'#B64936'
};
for (const [name, value] of Object.entries(requiredVisualTokens)) {
  pass(tokens.toUpperCase().includes(value), `QJ-D retained visual token missing: ${name} ${value}`);
}
pass(tokens.includes('Noto Serif CJK SC'), 'QJ-D display type token missing');
pass(tokens.includes('Noto Sans CJK SC'), 'QJ-D functional type token missing');

const forbiddenCurrentClaims = ['FIELD VALIDATED = YES','IMPLEMENTABLE = YES','FINAL PROMOTION = YES','Mucuna sempervirens is','2026票价','2026班次'];
for (const phrase of forbiddenCurrentClaims) {
  pass(!html.includes(phrase) && !dataSource.includes(phrase), `Forbidden promoted/current claim found: ${phrase}`);
}

for (const source of data.sources) {
  pass(/^https:\/\//.test(source.url), `Source URL invalid: ${source.title}`);
  pass(Boolean(source.use), `Source use boundary missing: ${source.title}`);
}

if (failures.length) {
  console.error('C04 PORTFOLIO WEB QA: FAIL');
  failures.forEach((f, i) => console.error(`${i + 1}. ${f}`));
  process.exit(1);
}

console.log('C04 PORTFOLIO WEB QA: PASS');
console.log(`route_segments=${data.route.length}`);
console.log(`reading_pages=${data.nodes.length}`);
console.log(`promotion_blockers=${data.blockers.length}`);
console.log(`sources=${data.sources.length}`);
console.log(`source_grounded_drawings=${drawingAssets.length}`);
console.log('professional_gate=DUAL_QUALITY_GATE_PREVIEW_REQUIRED');
console.log('visual_tokens=QJ-D-v1.0-retained / language-revised-by-dual-gate');
console.log('primary_media=LOCAL_SOURCE_GROUNDED');
console.log('field_observed=0 field_measured=0 g1f=HOLD promotion=NO');
