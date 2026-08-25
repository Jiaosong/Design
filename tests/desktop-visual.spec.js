const { test, expect } = require('@playwright/test');

async function settle(page) {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.waitForLoadState('networkidle');
  await expect(page.locator('.expression-encounter')).toBeVisible();
  await expect(page.locator('html')).toHaveAttribute('data-portfolio-framework', 'ready');
  await expect(page.locator('html')).toHaveAttribute('data-portfolio-crops', 'ready');
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

  const order = await page.locator('#main > *').evaluateAll((nodes) => nodes.map((node) => node.id || (node.classList.contains('portfolio-research-divider') ? 'research-divider' : node.className)));
  const expected = ['home', 'selected-work', 'project-daylily', 'project-reno-cmf', 'project-weaving', 'projects', 'research-divider', 'question', 'relations', 'evidence', 'practice', 'about', 'contact'];
  expected.forEach((key, index) => expect(order.indexOf(key), `${key} should follow the portfolio-first spine`).toBe(index));

  await expect(page.locator('#site-nav a').first()).toHaveAttribute('href', '#selected-work');
  await expect(page.locator('.encounter-case-link')).toHaveCount(2);

  await captureViewport(page, testInfo, 'portfolio-1440-home.png');
  await captureViewport(page, testInfo, 'portfolio-1440-first-encounter.png', '#selected-work');
  await captureViewport(page, testInfo, 'portfolio-1440-project-index.png', '#projects');
  await captureViewport(page, testInfo, 'portfolio-1440-research-divider.png', '.portfolio-research-divider');

  await page.setViewportSize({ width: 1920, height: 1080 });
  await captureViewport(page, testInfo, 'portfolio-1920-daylily.png', '#project-daylily');
  await captureViewport(page, testInfo, 'portfolio-1920-reno.png', '#project-reno-cmf');
  await captureViewport(page, testInfo, 'portfolio-1920-about.png', '#about');
});
