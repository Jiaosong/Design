import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';

const baseURL = process.env.TIMER_V33_BASE_URL || 'http://127.0.0.1:4173/practice/timer-light-basin-v3/index.html';
const outDir = process.env.TIMER_V33_QA_OUT || 'test-results/timer-v33-integrated';
await mkdir(outDir, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  args: ['--use-angle=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist']
});

const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1 });
const pageErrors = [];
const consoleErrors = [];
const requestFailures = [];
const httpErrors = [];
const modelResponses = [];

page.on('pageerror', (error) => pageErrors.push(String(error?.stack || error)));
page.on('console', (message) => {
  if (message.type() === 'error') consoleErrors.push(message.text());
});
page.on('requestfailed', (request) => requestFailures.push({ url: request.url(), error: request.failure()?.errorText || 'unknown' }));
page.on('response', (response) => {
  const url = response.url();
  if (response.status() >= 400) httpErrors.push({ url, status: response.status() });
  if (/timer_(?:100|50|10)_pbr\.glb|timer_exploded_sequence_v32\.glb/.test(url)) {
    modelResponses.push({ url, status: response.status() });
  }
});

const result = {
  gate: 'Timer Light Basin v3.3 integrated browser',
  authorityBoundary: 'Runtime/integration QA only; photography render lock and engineering validation are unchanged.',
  url: baseURL,
  startedAt: new Date().toISOString(),
  checks: {},
  diagnostics: {}
};

let failed = false;
const fail = (name, detail) => {
  failed = true;
  result.checks[name] = { status: 'FAIL', detail };
};
const pass = (name, detail = '') => {
  result.checks[name] = { status: 'PASS', detail };
};

try {
  const response = await page.goto(baseURL, { waitUntil: 'domcontentloaded', timeout: 45_000 });
  if (!response || !response.ok()) fail('document_http', `HTTP ${response?.status() ?? 'NO_RESPONSE'}`);
  else pass('document_http', `HTTP ${response.status()}`);

  const title = await page.title();
  if (/Timer Light Basin v3\.3/.test(title)) pass('document_identity', title);
  else fail('document_identity', title || 'missing title');

  const webgl = await page.evaluate(() => {
    const canvas = document.createElement('canvas');
    const gl2 = canvas.getContext('webgl2');
    const gl = gl2 || canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) return { available: false };
    return {
      available: true,
      version: gl.getParameter(gl.VERSION),
      renderer: gl.getParameter(gl.RENDERER),
      vendor: gl.getParameter(gl.VENDOR)
    };
  });
  result.diagnostics.webgl = webgl;
  if (webgl.available) pass('webgl_context', `${webgl.version} / ${webgl.renderer}`);
  else fail('webgl_context', 'No WebGL/WebGL2 context');

  await page.waitForFunction(() => customElements.get('model-viewer'), null, { timeout: 30_000 });
  pass('model_viewer_registered');

  await page.waitForSelector('#heroStudio.is-loaded', { timeout: 45_000 });
  await page.waitForSelector('#materialStudio.is-loaded', { timeout: 45_000 });
  pass('photography_viewers_ready');

  const photoStatus = await page.locator('#heroStudio .viewer-status, #materialStudio .viewer-status').allTextContents();
  if (photoStatus.length === 2 && photoStatus.every((text) => /PHOTO PIPELINE READY/.test(text))) pass('photography_status', photoStatus.join(' | '));
  else fail('photography_status', photoStatus.join(' | '));

  const canvases = await page.locator('[data-photo-viewer] canvas').evaluateAll((nodes) => nodes.map((node) => ({ width: node.width, height: node.height })));
  if (canvases.length === 2 && canvases.every((item) => item.width > 0 && item.height > 0)) pass('photography_canvas', JSON.stringify(canvases));
  else fail('photography_canvas', JSON.stringify(canvases));

  await page.waitForFunction(() => document.querySelector('#stateModel')?.loaded === true, null, { timeout: 45_000 });
  await page.waitForFunction(() => document.querySelector('#explodedModel')?.loaded === true, null, { timeout: 45_000 });
  pass('model_viewer_initial_models_ready');

  for (const state of ['50', '10', '100']) {
    await page.locator(`.state-button[data-state="${state}"]`).click();
    await page.waitForFunction(() => document.querySelector('#stateModel')?.loaded === true, null, { timeout: 45_000 });
  }
  pass('state_model_switching', '100 → 50 → 10 → 100');

  for (const view of ['top', 'control', 'rear', 'body']) {
    await page.locator(`[data-material-view="${view}"]`).click();
    await page.waitForTimeout(120);
  }
  pass('cmf_focus_controls', 'top → control → rear → body');

  await page.locator('[data-explode-stage="4"]').click();
  await page.waitForTimeout(900);
  const explodePressed = await page.locator('[data-explode-stage="4"]').getAttribute('aria-pressed');
  if (explodePressed === 'true') pass('exploded_stage_controls');
  else fail('exploded_stage_controls', `aria-pressed=${explodePressed}`);

  await page.screenshot({ path: `${outDir}/full-page.png`, fullPage: true });
  await page.locator('#heroStudio').screenshot({ path: `${outDir}/hero.png` });
  await page.locator('#materialStudio').screenshot({ path: `${outDir}/cmf.png` });
} catch (error) {
  fail('uncaught_gate_error', String(error?.stack || error));
}

result.diagnostics.pageErrors = pageErrors;
result.diagnostics.consoleErrors = consoleErrors;
result.diagnostics.requestFailures = requestFailures;
result.diagnostics.httpErrors = httpErrors;
result.diagnostics.modelResponses = modelResponses;

const localFailures = requestFailures.filter((item) => item.url.startsWith('http://127.0.0.1:4173'));
const localHttpErrors = httpErrors.filter((item) => item.url.startsWith('http://127.0.0.1:4173'));
if (pageErrors.length === 0) pass('page_errors'); else fail('page_errors', pageErrors.join('\n'));
if (localFailures.length === 0) pass('local_request_failures'); else fail('local_request_failures', JSON.stringify(localFailures));
if (localHttpErrors.length === 0) pass('local_http_errors'); else fail('local_http_errors', JSON.stringify(localHttpErrors));

const requiredModelPatterns = [
  /timer_100_pbr\.glb$/,
  /timer_50_pbr\.glb$/,
  /timer_10_pbr\.glb$/,
  /timer_exploded_sequence_v32\.glb$/
];
const missingModelResponses = requiredModelPatterns.filter((pattern) => !modelResponses.some((item) => pattern.test(new URL(item.url).pathname) && item.status === 200));
if (missingModelResponses.length === 0) pass('canonical_model_http');
else fail('canonical_model_http', `${missingModelResponses.length} required model response(s) missing`);

result.finishedAt = new Date().toISOString();
result.status = failed ? 'FAIL' : 'PASS';
await writeFile(`${outDir}/result.json`, `${JSON.stringify(result, null, 2)}\n`);
console.log(JSON.stringify(result, null, 2));
await browser.close();
if (failed) process.exit(1);
