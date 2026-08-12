#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const repo = process.cwd();
const root = path.join(repo, '05-cases/c04-qingjiang-stone-book/game-ui/cocos4-source');
const manifestPath = path.join(root, 'assets/resources/c04/ws07a/runtime-manifest.json');
const tokensPath = path.join(root, 'assets/resources/c04/ws07a/ui-tokens.json');
const sceneContractPath = path.join(root, 'assets/resources/c04/ws07a/scene-contract.json');
const visualMediaManifestPath = path.join(root, 'assets/resources/c04/ws07a/visual-media-manifest.json');
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

const controllerPath = path.join(root, 'assets/scripts/ws07a/VisualPrototypeController.ts');
const controller = fs.readFileSync(controllerPath, 'utf8');
if (!controller.includes("showPageScreen('S0_ONE_LINE_SKY', 'R13')")) fail('controller S0 binding missing');
if (!controller.includes("showPageScreen('S1_RED_ROCK_MOUTH', 'R01')")) fail('controller S1 binding missing');
if (!controller.includes("showPageScreen('S2_RIVER_VALLEY', 'R06')")) fail('controller S2 binding missing');
if (!controller.includes("@ccclass('C04WS07AVisualPrototypeController')")) fail('controller class name drifted');
if (!controller.includes("const BRIDGE_KEY = '__OLEANDER_WS07A__'")) fail('runtime capture bridge missing');
if (!controller.includes('getAuditSnapshot')) fail('runtime audit snapshot contract missing');
if (!controller.includes('getBoundingBoxToWorld')) fail('runtime layout evidence contract missing');

const correctionPath = path.join(root, 'assets/scripts/ws07a/ResponsiveVisualLayoutCorrection.ts');
const correction = fs.readFileSync(correctionPath, 'utf8');
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
const responsiveCorrection = corrections.find((item) => item?.gate === 'WS-07A.1');
if (!responsiveCorrection) fail('responsive correction must remain declared as WS-07A.1');
if (responsiveCorrection.component !== 'db://assets/scripts/ws07a/ResponsiveVisualLayoutCorrection.ts') fail('responsive correction component URL drifted');
if (responsiveCorrection.className !== 'C04WS07AResponsiveVisualLayoutCorrection') fail('responsive correction class contract drifted');

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

// Scene-contract v0.2 is the frozen WS-07A.1 baseline. v0.3 is accepted only
// when the complete WS-07A.2 research-media contract is present and preserves
// every v0.2 baseline binding above. This is an additive gate, not a relaxation.
if (sceneContract.version === '0.2') {
  if (corrections.length !== 1) fail('WS-07A.1 v0.2 scene contract must declare exactly one responsive correction layer');
} else if (sceneContract.version === '0.3') {
  if (corrections.length !== 2) fail('WS-07A.2 v0.3 scene contract must declare exactly responsive + research-media correction layers');
  const mediaCorrection = corrections.find((item) => item?.gate === 'WS-07A.2_RESEARCH_MEDIA');
  if (!mediaCorrection) fail('WS-07A.2 research-media correction layer missing');
  if (mediaCorrection.component !== 'db://assets/scripts/ws07a/LandscapeMediaController.ts') fail('WS-07A.2 media controller component URL drifted');
  if (mediaCorrection.className !== 'C04WS07ALandscapeMediaController') fail('WS-07A.2 media controller class contract drifted');

  const landscapeImage = sceneContract.nodes.find((node) => node.path === 'Canvas/S0_OneLineSky/LandscapeImage');
  if (!landscapeImage || landscapeImage.type !== 'Sprite') fail('WS-07A.2 must declare S0 LandscapeImage as Sprite');
  if (landscapeImage.active !== false) fail('WS-07A.2 LandscapeImage must default inactive to preserve baseline R13/S0');

  const mediaControllerPath = path.join(root, 'assets/scripts/ws07a/LandscapeMediaController.ts');
  const mediaCapturePath = path.join(repo, '90-shared/toolchains/cocos4/capture-c04-visual-media.mjs');
  for (const file of [visualMediaManifestPath, mediaControllerPath, mediaCapturePath]) {
    if (!fs.existsSync(file)) fail(`WS-07A.2 missing ${path.relative(repo, file)}`);
  }
  const mediaController = fs.readFileSync(mediaControllerPath, 'utf8');
  for (const required of [
    "@ccclass('C04WS07ALandscapeMediaController')",
    "const MEDIA_BRIDGE_KEY = '__OLEANDER_C04_MEDIA__'",
    'showActiveExperiment',
    "RuntimeStore.setScreen('S0_ONE_LINE_SKY')",
    'RuntimeStore.setCurrentPage(page.id)',
    'SpriteFrame.createWithImage',
  ]) {
    if (!mediaController.includes(required)) fail(`WS-07A.2 media controller contract missing ${required}`);
  }

  const mediaManifest = JSON.parse(fs.readFileSync(visualMediaManifestPath, 'utf8'));
  if (mediaManifest.version !== '0.1') fail('WS-07A.2 visual media manifest must be v0.1');
  if (mediaManifest.status !== 'RESEARCH_PROTOTYPE_MEDIA') fail('WS-07A.2 media manifest must remain research-only');
  if (!mediaManifest.policy?.offlineBundleRequired || !mediaManifest.policy?.verifyRemoteBytesBySha256) fail('WS-07A.2 media must be offline bundled and SHA-verified');
  if (mediaManifest.policy?.finalVisualPassInferred !== false) fail('WS-07A.2 media manifest must not infer final visual pass');
  const experiment = mediaManifest.activeExperiment;
  if (experiment?.id !== 'C04-WS04-A-R05-PHOTO-DOMINANT-v0.1') fail('WS-07A.2 active experiment id drifted');
  if (experiment?.pageId !== 'R05' || experiment?.screenId !== 'S0_ONE_LINE_SKY' || experiment?.variant !== 'A_PHOTO_DOMINANT') fail('WS-07A.2 active experiment must remain R05 / S0 / A_PHOTO_DOMINANT');
  const mediaAssets = Array.isArray(mediaManifest.assets) ? mediaManifest.assets : [];
  if (mediaAssets.length !== 1) fail('WS-07A.2 v0.1 must contain exactly one controlled research asset');
  const asset = mediaAssets[0];
  if (asset.assetId !== experiment.assetId || asset.pageId !== 'R05') fail('WS-07A.2 active media asset/page mismatch');
  if (asset.usageGate !== 'RESEARCH_PROTOTYPE_ONLY') fail('WS-07A.2 asset must remain research-only');
  if (asset.techGate !== 'FAIL_LT2400_FINAL_HERO') fail('WS-07A.2 must preserve failed Final Hero tech boundary');
  if (asset.rightsGate !== 'PASS_PROJECT_USE_APPROVED') fail('WS-07A.2 official media rights gate drifted');
  if (!/^https:\/\/(www\.)?eslygroup\.com\//.test(asset.sourceUrl ?? '')) fail('WS-07A.2 research asset must come from approved official host');
  if (!/^[a-f0-9]{64}$/.test(asset.sha256 ?? '')) fail('WS-07A.2 research asset SHA256 must be immutable 64-hex');
  if (!Number.isInteger(asset.expectedBytes) || asset.expectedBytes <= 0) fail('WS-07A.2 expected source byte count missing');
  if (!Number.isInteger(asset.sourceWidth) || !Number.isInteger(asset.sourceHeight) || asset.sourceWidth <= 0 || asset.sourceHeight <= 0) fail('WS-07A.2 source dimensions missing');
  if (!String(asset.materializedFile ?? '').startsWith('assets/resources/c04/ws07a/media/')) fail('WS-07A.2 media must materialize inside governed resources path');

  if (!materializer.includes("spec.type === 'Sprite'")) fail('MCP materializer must support governed Sprite contract nodes');
  const c04Materializer = fs.readFileSync(path.join(repo, '90-shared/toolchains/cocos4/materialize-c04.sh'), 'utf8');
  for (const required of ['visual-media-manifest.json', "createHash('sha256')", 'SHA256 mismatch', 'expectedBytes']) {
    if (!c04Materializer.includes(required)) fail(`C04 media materializer contract missing ${required}`);
  }

  const mediaCapture = fs.readFileSync(mediaCapturePath, 'utf8');
  for (const required of [
    '1080x1920', '390x844', '844x390',
    '__OLEANDER_C04_MEDIA__', 'showActiveExperiment',
    'RESEARCH_PROTOTYPE_ONLY', 'FAIL_LT2400_FINAL_HERO',
    'R05-A-photo-dominant-research', 'NO_FINAL_VISUAL_PASS_INFERRED',
  ]) {
    if (!mediaCapture.includes(required)) fail(`WS-07A.2 media capture contract missing ${required}`);
  }
} else {
  fail(`unsupported scene contract version ${sceneContract.version}; expected 0.2 baseline or governed 0.3 research-media extension`);
}

console.log('PASS: WS-07A runtime + official scene + WS-07A.1 correction + browser capture + responsive interaction audit contract');
console.log(`  Core=${manifest.corePages.length} Companion=${manifest.companionPages.length} Screens=${manifest.prototypeScreens.length} SceneNodes=${scenePaths.length} SceneContract=${sceneContract.version}`);
console.log('  Route=offline-first / MyBook=partial-is-complete / ResponsiveCorrection=declared+ordered / TouchTarget>=44px / RuntimeCapture=CDP');
if (sceneContract.version === '0.3') console.log('  WS-07A.2=research-media-only / OfficialAsset=SHA-pinned / FinalHeroTech=FAIL preserved / Baseline screen bindings unchanged');
