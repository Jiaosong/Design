const { test, expect } = require('@playwright/test');

async function waitForXJ01(page) {
  await page.goto('/project.html?project=xj01');
  await expect(page.locator('html')).toHaveAttribute('data-project-display', 'ready');
  await expect(page.locator('html')).toHaveAttribute('data-pro04', 'ready');
}

async function capture(page, testInfo, name, selector) {
  const path = testInfo.outputPath(name);
  if (selector) {
    const target = page.locator(selector);
    await target.scrollIntoViewIfNeeded();
    const imgs = target.locator('img:visible');
    for (let i = 0; i < await imgs.count(); i += 1) {
      await expect.poll(() => imgs.nth(i).evaluate((img) => img.complete && img.naturalWidth > 0), { timeout: 5000 }).toBeTruthy();
    }
    await page.waitForTimeout(120);
  } else {
    await page.evaluate(() => window.scrollTo(0, 0));
  }
  await page.screenshot({ path, fullPage: false, animations: 'disabled' });
  await testInfo.attach(name, { path, contentType: 'image/png' });
}

test('XJ01 PRO-04.2 binds the editorial presentation spine instead of the old review-module stack', async ({ page }, testInfo) => {
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
  await expect(page.locator('#p04')).toContainText('Reflection Environment Adaptation');
  await expect(page.locator('#p05')).toContainText('Use → Wipe → Long-term Appearance');
  await expect(page.locator('#p06')).toContainText('What this digital CMF study proves');

  const primaryText = await page.locator('#p00, #p01, #p02, #p03, #p04, #p05').allTextContents();
  const joined = primaryText.join(' ');
  expect(joined).not.toContain('READY_NOT_EXECUTED');
  expect(joined).not.toContain('P1-P3 physical CMF samples');
  expect(joined).not.toContain('engineering-readable specification');

  const appendix = page.locator('.pro04-appendix-details');
  await expect(appendix).not.toHaveAttribute('open', '');
  const diagnostic = page.locator('.pro04-diagnostic');
  await expect(diagnostic).not.toHaveAttribute('open', '');
});

test('XJ01 PRO-04.2 viewport visual evidence — desktop, laptop and mobile', async ({ page }, testInfo) => {
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

  await page.setViewportSize({ width: 390, height: 844 });
  await capture(page, testInfo, 'xj01-390x844-p00-hero.png', '#p00');
  await capture(page, testInfo, 'xj01-390x844-p01-direction-dna.png', '#p01');
  await capture(page, testInfo, 'xj01-390x844-p03-interfaces.png', '#p03');
  await capture(page, testInfo, 'xj01-390x844-p05-lifecycle.png', '#p05');

  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
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
