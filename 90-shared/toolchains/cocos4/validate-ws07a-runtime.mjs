#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo = process.cwd();
const root = path.join(repo, '05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source');
const manifestPath = path.join(root, 'assets/resources/c04/ws07a/runtime-manifest.json');
const tokensPath = path.join(root, 'assets/resources/c04/ws07a/ui-tokens.json');
const sceneContractPath = path.join(root, 'assets/resources/c04/ws07a/scene-contract.json');
const requiredScriptNames = [
  'RuntimeTypes.ts', 'RuntimeCatalog.ts', 'RuntimeStore.ts', 'VisualPrototypeController.ts',
  'ResponsiveVisualLayoutCorrection.ts', 'VisualAuditRules.ts',
];
const requiredScripts = requiredScriptNames.map((file) => path.join(root, 'assets/scripts/ws07a', file));
const toolchainFiles = [
  path.join(repo, '90-shared/toolchains/cocos4/materialize-ws07a-scene.mjs'),
  path.join(repo, '90-shared/toolchains/cocos4/materialize-ws07a-scene.sh'),
  path.join(repo, '90-shared/toolchains/cocos4/capture-ws07a-runtime.mjs'),
  path.join(repo, '90-shared/toolchains/cocos4/audit-ws07a-responsive-layout.mjs'),
];
function fail(message) { console.error(`ERROR: WS-07A runtime contract failed: ${message}`); process.exit(65); }
for (const file of [manifestPath, tokensPath, sceneContractPath, ...requiredScripts, ...toolchainFiles]) if (!fs.existsSync(file)) fail(`missing ${path.relative(repo, file)}`);
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
const tokens = JSON.parse(fs.readFileSync(tokensPath, 'utf8'));
const sceneContract = JSON.parse(fs.readFileSync(sceneContractPath, 'utf8'));
const pages = [...manifest.corePages, ...manifest.companionPages];
const ids = pages.map((page) => page.id);
if (manifest.corePages.length !== 8) fail(`expected 8 Core pages, got ${manifest.corePages.length}`);
if (manifest.companionPages.length !== 5) fail(`expected 5 Companion pages, got ${manifest.companionPages.length}`);
if (new Set(ids).size !== 13) fail('page ids must be unique and total 13');
if (manifest.prototypeScreens.length !== 5) fail('prototype must expose exactly S0 / S1 / S2 / Route / My Book');
if (!manifest.route.offlineFirst || manifest.route.autoGpsRequired) fail('route must be offline-first and must not require auto GPS');
if (manifest.myBook.requiresThirteenOfThirteen || manifest.myBook.completionReward) fail('My Book must support partial completion without reward economy');
const roleCounts = pages.reduce((acc, page) => { acc[page.role] = (acc[page.role] ?? 0) + 1; return acc; }, {});
if (roleCounts.CORE !== 8 || roleCounts.COMPANION !== 5) fail('role counts do not match Core/Companion architecture');
const modes = new Set(['S0','S1','S2']);
if (pages.some((page) => !modes.has(page.mode))) fail('unsupported page mode');
const screenExpectations = new Map([['S0_ONE_LINE_SKY','R13'],['S1_RED_ROCK_MOUTH','R01'],['S2_RIVER_VALLEY','R06']]);
for (const [screenId, pageId] of screenExpectations) { const screen = manifest.prototypeScreens.find((item) => item.id === screenId); if (!screen || screen.pageId !== pageId) fail(`${screenId} must bind ${pageId}`); }
const s0 = tokens.densityTargets?.S0; const s1 = tokens.densityTargets?.S1; const s2 = tokens.densityTargets?.S2;
if (!s0 || s0.landscapeMin < 0.85 || s0.landscapeMax > 0.95) fail('S0 density target drifted');
if (!s1 || s1.landscapeMin < 0.60 || s1.landscapeMax > 0.75) fail('S1 density target drifted');
if (!s2 || s2.landscapeMin < 0.40 || s2.landscapeMax > 0.60) fail('S2 density target drifted');

const controller = fs.readFileSync(path.join(root, 'assets/scripts/ws07a/VisualPrototypeController.ts'), 'utf8');
if (!controller.includes("showPageScreen('S0_ONE_LINE_SKY', 'R13')")) fail('controller S0 binding missing');
if (!controller.includes("showPageScreen('S1_RED_ROCK_MOUTH', 'R01')")) fail('controller S1 binding missing');
if (!controller.includes("showPageScreen('S2_RIVER_VALLEY', 'R06')")) fail('controller S2 binding missing');
if (!controller.includes("@ccclass('C04WS07AVisualPrototypeController')")) fail('controller class name drifted');
if (!controller.includes("const BRIDGE_KEY = '__OLEANDER_WS07A__'")) fail('runtime capture bridge missing');
if (!controller.includes('getAuditSnapshot')) fail('runtime audit snapshot contract missing');
if (!controller.includes('getBoundingBoxToWorld')) fail('runtime layout evidence contract missing');

const correction = fs.readFileSync(path.join(root, 'assets/scripts/ws07a/ResponsiveVisualLayoutCorrection.ts'), 'utf8');
if (!correction.includes("@ccclass('C04WS07AResponsiveVisualLayoutCorrection')")) fail('WS-07A.1 correction class missing');
if (!correction.includes('@executionOrder(100)')) fail('WS-07A.1 correction must execute after base layout');
if (!correction.includes("m.profile === 'LANDSCAPE'")) fail('WS-07A.1 landscape reveal correction missing');
if (!correction.includes('s2Hint.active = !revealOpen')) fail('WS-07A.1 reveal must suppress placeholder hint');

if (sceneContract.scene?.baseName !== 'VisualPrototype' || sceneContract.scene?.templateType !== '2d') fail('scene contract must generate VisualPrototype as 2d');
if (sceneContract.scene?.dbURL !== 'db://assets/scenes') fail('VisualPrototype target directory drifted');
if (sceneContract.controller?.nodePath !== 'Canvas') fail('controller host must remain Canvas');
if (sceneContract.controller?.component !== 'db://assets/scripts/ws07a/VisualPrototypeController.ts') fail('controller component URL drifted');
if (sceneContract.controller?.className !== 'C04WS07AVisualPrototypeController') fail('controller class contract drifted');
const corrections = Array.isArray(sceneContract.corrections) ? sceneContract.corrections : [];
if (sceneContract.version !== '0.2') fail('WS-07A.1 scene contract must be v0.2');
if (corrections.length !== 1) fail('WS-07A.1 scene contract must declare exactly one responsive correction layer');
if (corrections[0]?.component !== 'db://assets/scripts/ws07a/ResponsiveVisualLayoutCorrection.ts') fail('responsive correction component URL drifted');
if (corrections[0]?.className !== 'C04WS07AResponsiveVisualLayoutCorrection') fail('responsive correction class contract drifted');
if (corrections[0]?.gate !== 'WS-07A.1') fail('responsive correction must remain scoped to WS-07A.1');

const scenePaths = sceneContract.nodes.map((node) => node.path);
if (new Set(scenePaths).size !== scenePaths.length) fail('scene contract node paths must be unique');
const requiredScenePaths = [
  'Canvas/PrototypeNav',
  'Canvas/S0_OneLineSky',
  'Canvas/S1_RedRockMouth',
  'Canvas/S2_RiverValley',
  'Canvas/S2_RiverValley/RevealRoot',
  'Canvas/ReadingOverlay',
  'Canvas/Route',
  'Canvas/MyBook',
  'Canvas/ReturnGuard',
];
for (const requiredPath of requiredScenePaths) if (!scenePaths.includes(requiredPath)) fail(`scene contract missing ${requiredPath}`);
const controllerPaths = ['S0_OneLineSky','S1_RedRockMouth','S2_RiverValley','S2_RiverValley/RevealRoot','ReadingOverlay','Route','MyBook','ReturnGuard/Label'];
for (const relativePath of controllerPaths) if (!controller.includes(`'${relativePath}'`)) fail(`controller does not resolve ${relativePath}`);

const materializer = fs.readFileSync(toolchainFiles[0], 'utf8');
if (!materializer.includes('componentContracts()')) fail('MCP materializer must mount declared correction components');
if (!materializer.includes('contract.corrections')) fail('MCP materializer correction contract missing');

const capture = fs.readFileSync(toolchainFiles[2], 'utf8');
for (const required of ['1080x1920', '390x844', '844x390', 'RUNTIME_CAPTURE_PASS', 'S0_MINIMAL_CHROME', 'S2_REVEAL_OPEN', 'BOOK_SUMMARY']) {
  if (!capture.includes(required)) fail(`capture contract missing ${required}`);
}
if (!capture.includes('Page.captureScreenshot')) fail('capture contract must persist browser screenshots');
if (!capture.includes('Runtime.exceptionThrown')) fail('capture contract must record browser runtime exceptions');

const responsiveAudit = fs.readFileSync(toolchainFiles[3], 'utf8');
for (const required of ['RESPONSIVE_INTERACTION_LAYOUT_PASS', 'INTERACTIVE_TOUCH_TARGET_LT_44PX', 'LANDSCAPE_REVEAL_READING_OVERLAY_VISIBLE']) {
  if (!responsiveAudit.includes(required)) fail(`responsive audit contract missing ${required}`);
}
if (!responsiveAudit.includes('MIN_TOUCH_PX = 44')) fail('responsive audit must preserve 44px minimum touch target');
if (!responsiveAudit.includes('Raw Label/UITransform AABB')) fail('responsive audit must preserve non-gating Label AABB diagnostic boundary');

console.log('PASS: WS-07A runtime + official scene + WS-07A.1 correction + browser capture + responsive interaction audit contract');
console.log(`  Core=${manifest.corePages.length} Companion=${manifest.companionPages.length} Screens=${manifest.prototypeScreens.length} SceneNodes=${scenePaths.length}`);
console.log('  Route=offline-first / MyBook=partial-is-complete / ResponsiveCorrection=declared+ordered / TouchTarget>=44px / RuntimeCapture=CDP');
