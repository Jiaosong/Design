#!/usr/bin/env node
import fs from 'node:fs';
import http from 'node:http';
import os from 'node:os';
import path from 'node:path';
import { spawn, execFileSync } from 'node:child_process';

const buildDir = path.resolve(process.argv[2] ?? '');
const outDir = path.resolve(process.argv[3] ?? '');
if (!buildDir || !fs.existsSync(path.join(buildDir, 'index.html'))) throw new Error(`web build index.html missing: ${buildDir}`);
if (!outDir) throw new Error('visual media capture output directory required');
fs.mkdirSync(outDir, { recursive: true });

const HTTP_PORT = Number(process.env.OLEANDER_MEDIA_CAPTURE_HTTP_PORT ?? 4174);
const DEBUG_PORT = Number(process.env.OLEANDER_MEDIA_CAPTURE_DEBUG_PORT ?? 9223);
const targetUrl = `http://127.0.0.1:${HTTP_PORT}/index.html`;
const expectedObservation = '收起手机，先看峰体的高低、疏密与层次。';
const mime = new Map([
  ['.html', 'text/html; charset=utf-8'], ['.js', 'text/javascript; charset=utf-8'], ['.mjs', 'text/javascript; charset=utf-8'],
  ['.css', 'text/css; charset=utf-8'], ['.json', 'application/json; charset=utf-8'], ['.wasm', 'application/wasm'],
  ['.bin', 'application/octet-stream'], ['.png', 'image/png'], ['.jpg', 'image/jpeg'], ['.jpeg', 'image/jpeg'],
  ['.webp', 'image/webp'], ['.svg', 'image/svg+xml'], ['.ico', 'image/x-icon'],
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
const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'oleander-c04-media-chrome-'));
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

async function evaluate(expression) {
  const result = await cdp('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (result.exceptionDetails) throw new Error(`Runtime.evaluate failed: ${result.exceptionDetails.text ?? 'unknown exception'}`);
  return result.result?.value;
}

async function waitReady(timeoutMs = 45000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    try {
      const ready = await evaluate('Boolean(globalThis.__OLEANDER_WS07A__?.ready && globalThis.__OLEANDER_C04_MEDIA__?.ready)');
      if (ready) return;
    } catch {}
    await delay(250);
  }
  throw new Error('C04 visual media/runtime bridges did not become ready');
}

async function setViewport(width, height) {
  await cdp('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: true, screenWidth: width, screenHeight: height });
  await cdp('Page.reload', { ignoreCache: true });
  await waitReady();
  await delay(350);
}

async function screenshot(folder, name) {
  const capture = await cdp('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false });
  const dir = path.join(outDir, folder);
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, `${name}.png`);
  fs.writeFileSync(file, Buffer.from(capture.data, 'base64'));
  return path.relative(outDir, file);
}

await cdp('Page.enable');
await cdp('Runtime.enable');
await cdp('Page.navigate', { url: targetUrl });
await waitReady();

const failures = [];
const viewports = [
  { id: '1080x1920', width: 1080, height: 1920 },
  { id: '390x844', width: 390, height: 844 },
  { id: '844x390', width: 844, height: 390 },
];
const report = {
  gate: 'WS-07A.2_RESEARCH_MEDIA_CAPTURE',
  experiment: 'A_PHOTO_DOMINANT_R05_READABILITY_A2',
  targetUrl,
  expectedObservation,
  viewports: [],
  failures,
  consoleEvents,
  exceptions,
  boundary: 'RESEARCH_PROTOTYPE_ONLY / NO_FINAL_VISUAL_PASS_INFERRED',
};

for (const viewport of viewports) {
  await setViewport(viewport.width, viewport.height);
  await evaluate('globalThis.__OLEANDER_C04_MEDIA__.showActiveExperiment()');
  await delay(300);
  const runtime = await evaluate('globalThis.__OLEANDER_WS07A__.snapshot()');
  const settledMedia = await evaluate('globalThis.__OLEANDER_C04_MEDIA__.snapshot()');

  if (runtime.currentScreen !== 'S0_ONE_LINE_SKY' || runtime.currentPageId !== 'R05') failures.push({ code: 'R05_BINDING', viewport: viewport.id, runtime });
  if (runtime.observation !== expectedObservation) failures.push({ code: 'R05_OBSERVATION_DRIFT', viewport: viewport.id, expectedObservation, actual: runtime.observation });
  if (!settledMedia.visible || settledMedia.assetId !== 'OW-20230616-2a923422a') failures.push({ code: 'R05_MEDIA_VISIBLE', viewport: viewport.id, media: settledMedia });
  if (settledMedia.usageGate !== 'RESEARCH_PROTOTYPE_ONLY') failures.push({ code: 'MEDIA_USAGE_GATE', viewport: viewport.id, media: settledMedia });
  if (settledMedia.techGate !== 'FAIL_LT2400_FINAL_HERO') failures.push({ code: 'TECH_BOUNDARY_DRIFT', viewport: viewport.id, media: settledMedia });
  if (settledMedia.renderedWidth < runtime.canvas.width || settledMedia.renderedHeight < runtime.canvas.height) failures.push({ code: 'COVER_LAYOUT', viewport: viewport.id, media: settledMedia, canvas: runtime.canvas });

  const protection = settledMedia.textProtection;
  if (!protection?.applied || !protection.titleShadow || !protection.observationShadow || !protection.returnGuardShadow) {
    failures.push({ code: 'A2_TEXT_PROTECTION_INACTIVE', viewport: viewport.id, textProtection: protection });
  }
  const guard = protection?.returnGuardColor;
  if (!Array.isArray(guard) || guard.length !== 4 || guard[0] < 250 || guard[1] < 250 || guard[2] < 250 || guard[3] < 220) {
    failures.push({ code: 'A2_RETURN_GUARD_CONTRAST_STATE', viewport: viewport.id, returnGuardColor: guard });
  }

  const capture = await screenshot(viewport.id, 'R05-A-photo-dominant-research');
  report.viewports.push({ ...viewport, capture, media: settledMedia, runtime: {
    currentScreen: runtime.currentScreen,
    currentPageId: runtime.currentPageId,
    pageTitle: runtime.pageTitle,
    observation: runtime.observation,
    canvas: runtime.canvas,
  }});
}

const errorConsole = consoleEvents.filter((item) => item.type === 'error');
if (errorConsole.length) failures.push({ code: 'CONSOLE_ERROR', events: errorConsole });
if (exceptions.length) failures.push({ code: 'RUNTIME_EXCEPTION', count: exceptions.length });

fs.writeFileSync(path.join(outDir, 'visual-media-capture-report.json'), `${JSON.stringify(report, null, 2)}\n`);
console.log(JSON.stringify(report, null, 2));

try { ws.close(); } catch {}
try { chromeProc.kill('SIGTERM'); } catch {}
await new Promise((resolve) => server.close(resolve));
try { fs.rmSync(userDataDir, { recursive: true, force: true }); } catch {}
fs.closeSync(chromeLog);

if (failures.length) process.exit(1);
console.log('PASS: C04 R05 A.2 photo-dominant research media + runtime text protection captured across 3 viewports');
