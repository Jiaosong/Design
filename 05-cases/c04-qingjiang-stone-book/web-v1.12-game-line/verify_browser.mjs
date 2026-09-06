import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright';

const root = path.dirname(fileURLToPath(import.meta.url));
const outDir = path.join(root, 'browser-readback');
fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const baseUrl = process.env.C04_BROWSER_URL || 'http://127.0.0.1:4173/index.html';
const cases = [
  {
    name: 'desktop-1920x1080',
    viewport: { width: 1920, height: 1080 },
    anchors: ['hero', 'assets', 'thinking', 'scenes', 'digital', 'physical', 'final']
  },
  {
    name: 'desktop-1366x768',
    viewport: { width: 1366, height: 768 },
    anchors: ['hero', 'system', 'brandmemory', 'memory']
  },
  {
    name: 'mobile-390x844',
    viewport: { width: 390, height: 844 },
    anchors: ['hero', 'digital', 'physical', 'final']
  }
];

const report = {
  schema: 'C04_BROWSER_READBACK_V1',
  generated_at: new Date().toISOString(),
  source_url: baseUrl,
  status: 'RUNNING',
  cases: [],
  reduced_motion: null,
  failures: []
};

function fail(message, details = {}) {
  report.failures.push({ message, ...details });
}

async function settle(page) {
  await page.waitForLoadState('domcontentloaded');
  await page.waitForTimeout(1200);
  await page.evaluate(async () => {
    if (document.fonts?.ready) await document.fonts.ready;
  });
  await page.waitForTimeout(250);
}

async function snapshotSection(page, caseDir, id) {
  const section = page.locator(`#${id}`);
  if (await section.count() === 0) {
    fail(`Missing section #${id}`);
    return;
  }
  await section.scrollIntoViewIfNeeded();
  await page.waitForTimeout(260);
  await page.screenshot({ path: path.join(caseDir, `${id}.png`), fullPage: false });
}

const browser = await chromium.launch({ headless: true });
try {
  for (const item of cases) {
    const isMobile = item.name.startsWith('mobile-');
    const context = await browser.newContext({ viewport: item.viewport, deviceScaleFactor: 1, hasTouch: isMobile });
    const page = await context.newPage();
    const consoleErrors = [];
    const pageErrors = [];
    page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });
    page.on('pageerror', err => pageErrors.push(String(err?.message || err)));

    const response = await page.goto(baseUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
    if (!response || response.status() >= 400) fail('Page navigation failed', { case: item.name, status: response?.status?.() ?? null });
    await settle(page);

    const metrics = await page.evaluate(() => ({
      viewportWidth: window.innerWidth,
      viewportHeight: window.innerHeight,
      documentWidth: document.documentElement.scrollWidth,
      documentHeight: document.documentElement.scrollHeight,
      bodyWidth: document.body.scrollWidth,
      topbarVisible: !!document.querySelector('.topbar') && getComputedStyle(document.querySelector('.topbar')).display !== 'none',
      heroVisible: !!document.querySelector('#hero h2'),
      missingImages: [...document.images].filter(img => !img.complete || img.naturalWidth === 0).map(img => img.currentSrc || img.src),
      sectionCount: document.querySelectorAll('.section').length
    }));

    const overflow = Math.max(metrics.documentWidth, metrics.bodyWidth) - metrics.viewportWidth;
    if (overflow > 2) fail('Horizontal overflow exceeds 2px', { case: item.name, overflow, metrics });
    if (!metrics.topbarVisible) fail('Topbar is not visible', { case: item.name });
    if (!metrics.heroVisible) fail('Hero heading is not present', { case: item.name });
    if (metrics.missingImages.length) fail('One or more images failed to load', { case: item.name, missingImages: metrics.missingImages });

    const caseDir = path.join(outDir, item.name);
    fs.mkdirSync(caseDir, { recursive: true });
    for (const id of item.anchors) await snapshotSection(page, caseDir, id);

    await page.locator('#system').scrollIntoViewIfNeeded();
    await page.waitForTimeout(150);
    const imprintStatus = page.locator('#imprintStatus');
    const beforeImprint = (await imprintStatus.textContent())?.trim();
    const firstImprint = page.locator('.imprint').first();
    await firstImprint.click();
    const afterImprint = (await imprintStatus.textContent())?.trim();
    if (!beforeImprint || !afterImprint || beforeImprint === afterImprint) fail('Imprint interaction did not update status copy', { case: item.name, beforeImprint, afterImprint });

    const trigger = page.locator('#supplementTrigger');
    await trigger.click();
    await page.waitForTimeout(120);
    const panel = page.locator('#supplementPanel');
    const openState = await panel.getAttribute('aria-hidden');
    if (openState !== 'false') fail('Supplement panel did not open', { case: item.name, openState });
    await page.keyboard.press('Escape');
    await page.waitForTimeout(120);
    const closedState = await panel.getAttribute('aria-hidden');
    if (closedState !== 'true') fail('Supplement panel did not close with Escape', { case: item.name, closedState });

    await page.locator('#digital').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    const iframe = page.locator('.app-mybook-carrier');
    const iframeVisible = await iframe.isVisible();
    const iframeUrl = await iframe.getAttribute('src');
    if (!iframeVisible || !iframeUrl?.includes('C04_APP_V1_6_MY_BOOK_FINAL_VIEW.html')) fail('My Book iframe binding is not visible/current', { case: item.name, iframeVisible, iframeUrl });

    await page.locator('#hero').scrollIntoViewIfNeeded();
    await page.waitForTimeout(120);
    const y0 = await page.evaluate(() => window.scrollY);
    let sequenceMethod = 'PageDown';
    if (isMobile) {
      sequenceMethod = 'mobile-scroll-range';
      await page.evaluate(() => window.scrollBy(0, Math.min(window.innerHeight * 0.72, 620)));
    } else {
      await page.keyboard.press('PageDown');
    }
    await page.waitForTimeout(650);
    const y1 = await page.evaluate(() => window.scrollY);
    const readingSequenceAdvanced = y1 > y0 + 20;
    if (!readingSequenceAdvanced) fail(`${sequenceMethod} did not advance the reading sequence`, { case: item.name, y0, y1 });

    const caseResult = {
      name: item.name,
      viewport: item.viewport,
      metrics,
      horizontal_overflow_px: overflow,
      imprint_interaction: beforeImprint !== afterImprint,
      supplement_open_close: openState === 'false' && closedState === 'true',
      mybook_iframe_visible: iframeVisible,
      reading_sequence_method: sequenceMethod,
      reading_sequence_advanced: readingSequenceAdvanced,
      console_errors: consoleErrors,
      page_errors: pageErrors,
      screenshots: item.anchors.map(id => `${item.name}/${id}.png`)
    };
    report.cases.push(caseResult);

    if (pageErrors.length) fail('Page runtime errors detected', { case: item.name, pageErrors });
    await context.close();
  }

  const rmContext = await browser.newContext({ viewport: { width: 1366, height: 768 }, reducedMotion: 'reduce', deviceScaleFactor: 1 });
  const rmPage = await rmContext.newPage();
  await rmPage.goto(baseUrl, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await settle(rmPage);
  await rmPage.locator('#system').scrollIntoViewIfNeeded();
  await rmPage.waitForTimeout(200);
  const reduced = await rmPage.evaluate(() => {
    const path = document.querySelector('#system .imprint.active svg path');
    const hero = document.querySelector('#hero .hero-media img');
    const pathStyle = path ? getComputedStyle(path) : null;
    const heroStyle = hero ? getComputedStyle(hero) : null;
    return {
      mediaQueryMatches: matchMedia('(prefers-reduced-motion: reduce)').matches,
      imprintAnimationName: pathStyle?.animationName ?? null,
      imprintAnimationDuration: pathStyle?.animationDuration ?? null,
      heroTransitionDuration: heroStyle?.transitionDuration ?? null
    };
  });
  if (!reduced.mediaQueryMatches) fail('Reduced-motion browser preference did not apply', { reduced });
  if (reduced.imprintAnimationName && reduced.imprintAnimationName !== 'none') fail('Imprint animation remains active under reduced motion', { reduced });
  const rmDir = path.join(outDir, 'reduced-motion');
  fs.mkdirSync(rmDir, { recursive: true });
  await rmPage.screenshot({ path: path.join(rmDir, 'system.png'), fullPage: false });
  report.reduced_motion = { ...reduced, screenshot: 'reduced-motion/system.png' };
  await rmContext.close();
} finally {
  await browser.close();
}

report.status = report.failures.length ? 'FAIL' : 'PASS';
fs.writeFileSync(path.join(outDir, 'report.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
if (report.failures.length) process.exit(1);
