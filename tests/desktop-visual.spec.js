const { test, expect } = require('@playwright/test');

async function settle(page) {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.waitForLoadState('networkidle');
  await expect(page.locator('.expression-encounter')).toBeVisible();
  await page.evaluate(async () => {
    await Promise.all([...document.images].map((img) => img.complete ? Promise.resolve() : new Promise((resolve) => {
      img.addEventListener('load', resolve, { once: true });
      img.addEventListener('error', resolve, { once: true });
    })));
  });
}

async function captureViewport(page, testInfo, name, selector) {
  if (selector) {
    await page.locator(selector).evaluate((node) => node.scrollIntoView({ block: 'start', behavior: 'auto' }));
    await page.waitForTimeout(120);
  } else {
    await page.evaluate(() => window.scrollTo(0, 0));
  }
  await page.screenshot({ path: testInfo.outputPath(name), fullPage: false, animations: 'disabled' });
}

test('portfolio desktop visual experiment', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop', 'Desktop visual evidence is captured once in Chromium.');

  await page.setViewportSize({ width: 1440, height: 900 });
  await page.goto('/');
  await settle(page);
  await captureViewport(page, testInfo, 'portfolio-1440-home.png');
  await captureViewport(page, testInfo, 'portfolio-1440-first-encounter.png', '.expression-encounter');
  await captureViewport(page, testInfo, 'portfolio-1440-question.png', '#question');

  await page.setViewportSize({ width: 1920, height: 1080 });
  await captureViewport(page, testInfo, 'portfolio-1920-daylily.png', '#project-daylily');
  await captureViewport(page, testInfo, 'portfolio-1920-reno.png', '#project-reno-cmf');
  await captureViewport(page, testInfo, 'portfolio-1920-about.png', '#about');

  throw new Error('VISUAL_EXPERIMENT_CAPTURE_COMPLETE');
});
