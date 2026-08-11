#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo = process.cwd();
const root = path.join(repo, '05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source');
const manifestPath = path.join(root, 'assets/resources/c04/ws07a/runtime-manifest.json');
const tokensPath = path.join(root, 'assets/resources/c04/ws07a/ui-tokens.json');
const sceneContractPath = path.join(root, 'assets/resources/c04/ws07a/scene-contract.json');
const requiredScripts = ['RuntimeTypes.ts','RuntimeCatalog.ts','RuntimeStore.ts','VisualPrototypeController.ts','VisualAuditRules.ts'].map((file) => path.join(root, 'assets/scripts/ws07a', file));
const materializerFiles = [
  path.join(repo, '90-shared/toolchains/cocos4/materialize-ws07a-scene.mjs'),
  path.join(repo, '90-shared/toolchains/cocos4/materialize-ws07a-scene.sh'),
];
function fail(message) { console.error(`ERROR: WS-07A runtime contract failed: ${message}`); process.exit(65); }
for (const file of [manifestPath, tokensPath, sceneContractPath, ...requiredScripts, ...materializerFiles]) if (!fs.existsSync(file)) fail(`missing ${path.relative(repo, file)}`);
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
const controller = fs.readFileSync(requiredScripts[3], 'utf8');
if (!controller.includes("showPageScreen('S0_ONE_LINE_SKY', 'R13')")) fail('controller S0 binding missing');
if (!controller.includes("showPageScreen('S1_RED_ROCK_MOUTH', 'R01')")) fail('controller S1 binding missing');
if (!controller.includes("showPageScreen('S2_RIVER_VALLEY', 'R06')")) fail('controller S2 binding missing');
if (!controller.includes("@ccclass('C04WS07AVisualPrototypeController')")) fail('controller class name drifted');

if (sceneContract.scene?.baseName !== 'VisualPrototype' || sceneContract.scene?.templateType !== '2d') fail('scene contract must generate VisualPrototype as 2d');
if (sceneContract.scene?.dbURL !== 'db://assets/scenes') fail('VisualPrototype target directory drifted');
if (sceneContract.controller?.nodePath !== 'Canvas') fail('controller host must remain Canvas');
if (sceneContract.controller?.component !== 'db://assets/scripts/ws07a/VisualPrototypeController.ts') fail('controller component URL drifted');
if (sceneContract.controller?.className !== 'C04WS07AVisualPrototypeController') fail('controller class contract drifted');
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
const controllerPaths = ['S0_OneLineSky','S1_RedRockMouth','S2_RiverValley','S2_RiverValley/RevealRoot','ReadingOverlay','Route','MyBook','ReturnGuard'];
for (const relativePath of controllerPaths) if (!controller.includes(`'${relativePath}'`)) fail(`controller does not resolve ${relativePath}`);

console.log('PASS: WS-07A runtime + official scene materialization contract');
console.log(`  Core=${manifest.corePages.length} Companion=${manifest.companionPages.length} Screens=${manifest.prototypeScreens.length} SceneNodes=${scenePaths.length}`);
console.log('  Route=offline-first / MyBook=partial-is-complete / S0-S1-S2 density locked / VisualPrototype=MCP-generated');
