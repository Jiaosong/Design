#!/usr/bin/env node
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn, execFileSync } from 'node:child_process';

const buildDir = path.resolve(process.argv[2] ?? '');
const outDir = path.resolve(process.argv[3] ?? '');
if (!buildDir || !fs.existsSync(path.join(buildDir, 'index.html'))) throw new Error(`web build index.html missing: ${buildDir}`);
if (!outDir) throw new Error('capture output directory required');
fs.mkdirSync(outDir, { recursive: true });

const HTTP_PORT = Number(process.env.OLEANDER_CAPTURE_HTTP_PORT ?? 4173);
const DEBUG_PORT = Number(process.env.OLEANDER_CAPTURE_DEBUG_PORT ?? 9222);
const targetUrl = `http://127.0.0.1:${HTTP_PORT}/index.html`;

const mime = new Map([
  ['.html', 'text/html; charset=utf-8'], ['.js', 'text/javascript; charset=utf-8'], ['.mjs', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'], ['.json', 'application/json; charset=utf-8'], ['.wasm', 'application/wasm'],
  ['.bin', 'application/octet-stream'], ['.png', 'image/png'], ['.jpg', 'image/jpeg'], ['.jpeg', 'image/jpeg'],
  ['.webp', 'image/webp'], ['.svg', 'image/svg+xml'], ['.ico', 'image/x-icon'], ['.mp3', 'audio/mpeg'], ['.ogg', 'audio/ogg'],
]);

function safePath(urlPath) {
  const pathname = decodeURIComponent((urlPath ?? '/').split('?')[0]);
  const relative = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const full = path.resolve(buildDir, relative);
  if (full !== buildDir && !full.startsWith(`${buildDir}${path.sep}`)) return null;
  return full;
}

const server = http.createServer((req, res) => {
  const full = safePath(req.url);
  if (!full || !fs.existsSync(full) || fs.statSync(full).isDirectory()) {
    res.writeHead(404); res.end('Not found'); return;
  }
  res.setHeader('Content-Type', mime.get(path.extname(full).toLowerCase()) ?? 'application/octet-stream');
  res.setHeader('Cache-Control', 'no-store');
  fs.createReadStream(full).pipe(res);
});
await new Promise((resolve, reject) => server.listen(HTTP_PORT, '127.0.0.1', resolve).once('error', reject));

function which(names) {
  const explicit = process.env.CHROME_BIN;
  if (explicit && fs.existsSync(explicit)) return explicit;
  for (const name of names) {
    try { return execFileSync('which', [name], { encoding: 'utf8' }).trim(); } catch {}
  }
  return null;
}

const chrome = which(['google-chrome-stable', 'google-chrome', 'chromium', 'chromium-browser']);
if (!chrome) throw new Error('Chrome/Chromium executable not found on runner');
const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'oleander-ws07a-chrome-'));
const chromeLog = fs.openSync(path.join(outDir, 'chrome.log'), 'w');
const chromeProc = spawn(chrome, [
  '--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu', '--hide-scrollbars',
  '--remote-debugging-address=127.0.0.1', `--remote-debugging-port=${DEBUG_PORT}`, `--user-data-dir=${userDataDir}`, 'about:blank',
], { stdio: ['ignore', chromeLog, chromeLog] });

const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function jsonFetch(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${response.status} ${response.statusText}: ${url}`);
  return response.json();
}

let wsUrl;
for (let i = 0; i < 120; i += 1) {
  if (chromeProc.exitCode !== null) throw new Error(`Chrome exited before CDP became ready: ${chromeProc.exitCode}`);
  try {
    const pages = await jsonFetch(`http://127.0.0.1:${DEBUG_PORT}/json/list`);
    wsUrl = pages.find((item) => item.type === 'page')?.webSocketDebuggerUrl;
    if (wsUrl) break;
  } catch {}
  await delay(250);
}
if (!wsUrl) throw new Error('Timed out waiting for Chrome DevTools endpoint');

const ws = new WebSocket(wsUrl);
await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
let seq = 0;
const pending = new Map();
const consoleEvents = [];
const exceptions = [];
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.id) {
    const slot = pending.get(message.id);
    if (!slot) return;
    pending.delete(message.id);
    if (message.error) slot.reject(new Error(`${slot.method}: ${message.error.message}`)); else slot.resolve(message.result ?? {});
    return;
  }
  if (message.method === 'Runtime.consoleAPICalled') {
    consoleEvents.push({ type: message.params?.type, args: (message.params?.args ?? []).map((arg) => arg.value ?? arg.description ?? arg.type) });
  }
  if (message.method === 'Runtime.exceptionThrown') exceptions.push(message.params?.exceptionDetails ?? message.params);
};
function cdp(method, params = {}) {
  const id = ++seq;
  return new Promise((resolve, reject) => {
    pending.set(id, { resolve, reject, method });
    ws.send(JSON.stringify({ id, method, params }));
    setTimeout(() => {
      if (!pending.has(id)) return;
      pending.delete(id);
      reject(new Error(`CDP timeout: ${method}`));
    }, 30000).unref?.();
  });
}

await cdp('Page.enable');
await cdp('Runtime.enable');
await cdp('Log.enable');
await cdp('Page.navigate', { url: targetUrl });

async function evaluate(expression) {
  const result = await cdp('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) throw new Error(`Runtime.evaluate failed: ${result.exceptionDetails.text ?? 'unknown exception'}`);
  return result.result?.value;
}

async function waitReady(timeoutMs = 45000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    try {
      if (await evaluate('Boolean(globalThis.__OLEANDER_WS07A__ && globalThis.__OLEANDER_WS07A__.ready)')) return;
    } catch {}
    await delay(250);
  }
  throw new Error('WS-07A runtime bridge did not become ready');
}

async function setViewport(width, height) {
  await cdp('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: true, screenWidth: width, screenHeight: height });
  await cdp('Page.reload', { ignoreCache: true });
  await waitReady();
  await delay(400);
}

async function snapshot() { return evaluate('globalThis.__OLEANDER_WS07A__.snapshot()'); }

async function invoke(method) {
  await evaluate(`globalThis.__OLEANDER_WS07A__.${method}()`);
  await delay(220);
  return snapshot();
}

async function screenshot(folder, name) {
  const capture = await cdp('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false });
  const dir = path.join(outDir, folder); fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `${name}.png`); fs.writeFileSync(file, Buffer.from(capture.data, 'base64')); return path.relative(outDir, file);
}

function requireCheck(condition, code, detail, failures) { if (!condition) failures.push({ code, detail }); }
function checkExactlyOneActive(state, failures) { requireCheck(state.activeScreens?.length === 1, 'ACTIVE_SCREEN_COUNT', state.activeScreens, failures); }
function rectOverlap(a, b) {
  if (!a?.rect || !b?.rect || !a.active || !b.active) return false;
  const ar = a.rect; const br = b.rect;
  return ar.x < br.x + br.width && ar.x + ar.width > br.x && ar.y < br.y + br.height && ar.y + ar.height > br.y;
}
function layoutIssueScan(state) {
  const issues = [];
  const active = (state.layout ?? []).filter((item) => item.active && item.rect && item.rect.width > 0 && item.rect.height > 0);
  for (let i = 0; i < active.length; i += 1) {
    for (let j = i + 1; j < active.length; j += 1) {
      const a = active[i]; const b = active[j];
      if (a.path.startsWith(`${b.path}/`) || b.path.startsWith(`${a.path}/`)) continue;
      if (rectOverlap(a, b)) issues.push({ code: 'AABB_OVERLAP', a: a.path, b: b.path });
    }
  }
  return issues;
}

const criticalPairs = [
  ['PrototypeNav/NavS0', 'PrototypeNav/NavS1'], ['PrototypeNav/NavS1', 'PrototypeNav/NavS2'],
  ['PrototypeNav/NavS2', 'PrototypeNav/NavRoute'], ['PrototypeNav/NavRoute', 'PrototypeNav/NavBook'],
  ['PrototypeNav/NavS0', 'ReturnGuard/Label'], ['PrototypeNav/NavS1', 'ReturnGuard/Label'],
  ['PrototypeNav/NavS2', 'ReturnGuard/Label'], ['PrototypeNav/NavRoute', 'ReturnGuard/Label'], ['PrototypeNav/NavBook', 'ReturnGuard/Label'],
  ['ReadingOverlay/PageTitle', 'ReadingOverlay/Observation'],
  ['ReadingOverlay/RecordButton', 'ReadingOverlay/RevealButton'],
  ['ReadingOverlay/RecordButton', 'ReturnGuard/Label'], ['ReadingOverlay/RevealButton', 'ReturnGuard/Label'],
  ['Route/Title', 'Route/Priority'], ['MyBook/Title', 'MyBook/BookSummary'],
  ['S2_RiverValley/RevealRoot/EvidenceStatus', 'S2_RiverValley/RevealRoot/Fact'],
  ['S2_RiverValley/RevealRoot/EvidenceStatus', 'S2_RiverValley/RevealRoot/Narrative'],
  ['S2_RiverValley/RevealRoot/EvidenceStatus', 'S2_RiverValley/RevealRoot/DesignReading'],
  ['S2_RiverValley/RevealRoot/Fact', 'S2_RiverValley/RevealRoot/Narrative'],
  ['S2_RiverValley/RevealRoot/Narrative', 'S2_RiverValley/RevealRoot/DesignReading'],
  ['S2_RiverValley/RevealRoot/Fact', 'S2_RiverValley/RevealRoot/CloseReveal'],
  ['S2_RiverValley/RevealRoot/Narrative', 'S2_RiverValley/RevealRoot/CloseReveal'],
  ['S2_RiverValley/RevealRoot/DesignReading', 'S2_RiverValley/RevealRoot/CloseReveal'],
  ['S2_RiverValley/RevealRoot/CloseReveal', 'ReturnGuard/Label'],
];
function criticalLayoutScan(state) {
  const byPath = new Map((state.layout ?? []).map((item) => [item.path, item]));
  const issues = [];
  for (const [aPath, bPath] of criticalPairs) {
    const a = byPath.get(aPath); const b = byPath.get(bPath);
    if (rectOverlap(a, b)) issues.push({ code: 'CRITICAL_AABB_OVERLAP', a: aPath, b: bPath });
  }
  return issues;
}

const viewports = [
  { id: '1080x1920', width: 1080, height: 1920 },
  { id: '390x844', width: 390, height: 844 },
  { id: '844x390', width: 844, height: 390 },
];
const report = {
  gate: 'RUNTIME_CAPTURE',
  responsiveLayoutGate: 'RESPONSIVE_LAYOUT_AUDIT_OPEN',
  targetUrl,
  chrome,
  viewports: [],
  consoleEvents,
  exceptions,
  failures: [],
  visualIssues: [],
  responsiveLayoutIssues: [],
};

for (const viewport of viewports) {
  await setViewport(viewport.width, viewport.height);
  const record = { ...viewport, captures: [], states: {} };

  record.states.s0 = await invoke('showS0');
  checkExactlyOneActive(record.states.s0, report.failures);
  requireCheck(record.states.s0.currentScreen === 'S0_ONE_LINE_SKY' && record.states.s0.currentPageId === 'R13', 'S0_BINDING', record.states.s0, report.failures);
  requireCheck(!record.states.s0.recordButtonActive && !record.states.s0.revealButtonActive && !record.states.s0.revealRootActive, 'S0_MINIMAL_CHROME', record.states.s0, report.failures);
  record.captures.push(await screenshot(viewport.id, '01-s0-one-line-sky'));

  record.states.s1 = await invoke('showS1');
  checkExactlyOneActive(record.states.s1, report.failures);
  requireCheck(record.states.s1.currentScreen === 'S1_RED_ROCK_MOUTH' && record.states.s1.currentPageId === 'R01', 'S1_BINDING', record.states.s1, report.failures);
  requireCheck(record.states.s1.recordButtonActive && !record.states.s1.revealButtonActive, 'S1_ACTION_DENSITY', record.states.s1, report.failures);
  record.captures.push(await screenshot(viewport.id, '02-s1-red-rock-mouth'));

  record.states.s1Recorded = await invoke('recordCurrentPage');
  requireCheck(record.states.s1Recorded.recordedPageIds.includes('R01'), 'S1_RECORD', record.states.s1Recorded, report.failures);

  record.states.s2 = await invoke('showS2');
  checkExactlyOneActive(record.states.s2, report.failures);
  requireCheck(record.states.s2.currentScreen === 'S2_RIVER_VALLEY' && record.states.s2.currentPageId === 'R06', 'S2_BINDING', record.states.s2, report.failures);
  requireCheck(record.states.s2.recordButtonActive && record.states.s2.revealButtonActive && !record.states.s2.revealRootActive, 'S2_PRE_REVEAL', record.states.s2, report.failures);
  record.captures.push(await screenshot(viewport.id, '03-s2-river-valley'));

  record.states.s2Reveal = await invoke('openReveal');
  requireCheck(record.states.s2Reveal.revealOpen && record.states.s2Reveal.revealRootActive, 'S2_REVEAL_OPEN', record.states.s2Reveal, report.failures);
  for (const type of ['FACT', 'LOCAL_NARRATIVE', 'DESIGN_READING']) {
    requireCheck(record.states.s2Reveal.claims?.[type]?.active && Boolean(record.states.s2Reveal.claims?.[type]?.text), `S2_${type}_VISIBLE`, record.states.s2Reveal.claims?.[type], report.failures);
  }
  record.captures.push(await screenshot(viewport.id, '04-s2-reveal'));

  record.states.route = await invoke('showRoute');
  checkExactlyOneActive(record.states.route, report.failures);
  requireCheck(record.states.route.currentScreen === 'ROUTE' && !record.states.route.readingOverlayActive && record.states.route.returnGuardActive, 'ROUTE_RETURN_SERVICE', record.states.route, report.failures);
  record.captures.push(await screenshot(viewport.id, '05-route'));

  record.states.book = await invoke('showMyBook');
  checkExactlyOneActive(record.states.book, report.failures);
  requireCheck(record.states.book.currentScreen === 'MY_BOOK' && record.states.book.recordedPageIds.includes('R01'), 'BOOK_STATE', record.states.book, report.failures);
  requireCheck(record.states.book.bookSummary.includes('红岩嘴'), 'BOOK_SUMMARY', record.states.book.bookSummary, report.failures);
  record.captures.push(await screenshot(viewport.id, '06-my-book'));

  for (const [stateName, state] of Object.entries(record.states)) {
    for (const issue of layoutIssueScan(state)) report.visualIssues.push({ viewport: viewport.id, state: stateName, ...issue });
    for (const issue of criticalLayoutScan(state)) report.responsiveLayoutIssues.push({ viewport: viewport.id, state: stateName, ...issue });
  }
  report.viewports.push(record);
}

const errorConsole = consoleEvents.filter((item) => item.type === 'error');
if (exceptions.length) report.failures.push({ code: 'RUNTIME_EXCEPTIONS', count: exceptions.length, exceptions });
if (errorConsole.length) report.failures.push({ code: 'CONSOLE_ERRORS', count: errorConsole.length, errors: errorConsole });
report.finalSnapshot = await snapshot();
report.gate = report.failures.length === 0 ? 'RUNTIME_CAPTURE_PASS' : 'RUNTIME_CAPTURE_FAIL';
report.responsiveLayoutGate = report.responsiveLayoutIssues.length === 0 ? 'RESPONSIVE_LAYOUT_PASS' : 'RESPONSIVE_LAYOUT_AUDIT_OPEN';
fs.writeFileSync(path.join(outDir, 'runtime-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`);

console.log(`${report.gate}: ${report.viewports.length} viewports / ${report.viewports.reduce((sum, item) => sum + item.captures.length, 0)} screenshots`);
console.log(`${report.responsiveLayoutGate}: visualIssues=${report.visualIssues.length} critical=${report.responsiveLayoutIssues.length} consoleErrors=${errorConsole.length} exceptions=${exceptions.length}`);
if (report.failures.length) {
  console.error(JSON.stringify(report.failures, null, 2));
  process.exitCode = 65;
}

try { ws.close(); } catch {}
try { chromeProc.kill('SIGTERM'); } catch {}
await new Promise((resolve) => server.close(resolve));
try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch {}
