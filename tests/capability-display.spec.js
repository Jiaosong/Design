const { test, expect } = require('@playwright/test');

async function waitForXJ01(page) {
  await page.goto('/project.html?project=xj01');
  await expect(page.locator('html')).toHaveAttribute('data-project-display', 'ready');
  await expect(page.locator('html')).toHaveAttribute('data-pro04', 'ready');
}

async function capture(page, testInfo, name, selector) {
  const path = testInfo.outputPath(name);
  const target = page.locator(selector);
  await page.evaluate(() => {
    document.documentElement.style.overflowAnchor = 'none';
    document.body.style.overflowAnchor = 'none';
  });
  const alignTop = async () => {
    const y = await target.evaluate((node) => node.getBoundingClientRect().top + window.scrollY);
    await page.evaluate((targetY) => window.scrollTo({ top: Math.max(0, targetY - 64), behavior: 'auto' }), y);
  };
  await alignTop();
  const imgs = target.locator('img:visible');
  for (let i = 0; i < await imgs.count(); i += 1) {
    await expect.poll(() => imgs.nth(i).evaluate((img) => img.complete && img.naturalWidth > 0), { timeout: 5000 }).toBeTruthy();
  }
  await alignTop();
  await page.waitForTimeout(150);
  await page.screenshot({ path, fullPage: false, animations: 'disabled' });
  await testInfo.attach(name, { path, contentType: 'image/png' });
}

async function desktopOverflowDiagnostics(page) {
  return page.evaluate(() => {
    const viewport = document.documentElement.clientWidth;
    const pageWidth = document.documentElement.scrollWidth;
    const offenders = [...document.querySelectorAll('body *')]
      .map((node) => {
        const rect = node.getBoundingClientRect();
        return {
          tag: node.tagName.toLowerCase(), id: node.id || '',
          className: typeof node.className === 'string' ? node.className : '',
          left: Math.round(rect.left * 10) / 10, right: Math.round(rect.right * 10) / 10,
          width: Math.round(rect.width * 10) / 10,
          overflowRight: Math.round(Math.max(0, rect.right - viewport) * 10) / 10,
          text: (node.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 90)
        };
      })
      .filter((item) => item.width > 0 && item.right > viewport + 1)
      .sort((a, b) => b.overflowRight - a.overflowRight)
      .slice(0, 20);
    return { viewport, pageWidth, overflow: pageWidth - viewport, offenders };
  });
}

test('XJ01 PRO-04.2 binds the editorial presentation spine and retained VE06 VE07 evidence', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  await waitForXJ01(page);

  const sections = page.locator('[data-pro04-section]');
  await expect(sections).toHaveCount(7);
  expect(await sections.evaluateAll((nodes) => nodes.map((node) => node.dataset.pro04Section)))
    .toEqual(['p00','p01','p02','p03','p04','p05','p06']);

  await expect(page.locator('#p00 h1')).toContainText('Continuous');
  await expect(page.locator('#p01')).toContainText('Direction DNA');
  await expect(page.locator('#p02')).toContainText('Colour × Material × Geometry');
  await expect(page.locator('#p03')).toContainText('Where materials meet');
  await expect(page.locator('#p04 img[src*="pro04-environment-d2-2x3.jpg"]')).toHaveCount(1);
  await expect(page.locator('#p05 img[src*="pro04-lifecycle-d2-2x3.jpg"]')).toHaveCount(1);
  await expect(page.locator('#p04')).not.toContainText('SUPPORT ONLY');
  await expect(page.locator('#p05')).not.toContainText('SUPPORT ONLY');
  await expect(page.locator('#p06')).toContainText('What this digital CMF study proves');

  const appendix = page.locator('.pro04-appendix-details');
  await expect(appendix).not.toHaveAttribute('open', '');
  const diagnostic = page.locator('.pro04-diagnostic');
  await expect(diagnostic).not.toHaveAttribute('open', '');
});

test('XJ01 PRO-04.2 desktop actual-preview evidence — 1920 and 1440 only', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');

  await page.setViewportSize({ width: 1920, height: 1080 });
  await waitForXJ01(page);
  await capture(page, testInfo, 'xj01-1920x1080-p00-hero.png', '#p00');
  await capture(page, testInfo, 'xj01-1920x1080-p02-cmf-system.png', '#p02');
  await capture(page, testInfo, 'xj01-1920x1080-p04-environment.png', '#p04');

  await page.setViewportSize({ width: 1440, height: 900 });
  await capture(page, testInfo, 'xj01-1440x900-p01-direction-dna.png', '#p01');
  await capture(page, testInfo, 'xj01-1440x900-p03-interfaces.png', '#p03');
  await capture(page, testInfo, 'xj01-1440x900-p05-lifecycle.png', '#p05');

  const diagnostics = await desktopOverflowDiagnostics(page);
  expect(diagnostics.overflow, JSON.stringify(diagnostics, null, 2)).toBeLessThanOrEqual(1);
});

test('project data remains capability-based and physical scope is not a presentation blocker', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  const response = await page.request.get('/data/projects/xj01.json');
  expect(response.ok()).toBeTruthy();
  const data = await response.json();

  expect(data.display.principle).toContain('not fixed page template');
  expect(data.status.interaction_06c_p1).toBe('OUT_OF_SCOPE');
  expect(data.status.physical_validation).toBe('OUT_OF_SCOPE');
  expect(data.status.promotion_blockers).not.toContain('P1-P3 physical CMF samples');
  expect(data.status.promotion_blockers).not.toContain('06C P1 physical interaction');
});
