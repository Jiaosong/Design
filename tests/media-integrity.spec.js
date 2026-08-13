const { test, expect } = require('@playwright/test');

test('portfolio media keeps natural proportions and opens detail viewer', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  await page.goto('/');
  await expect(page.locator('html')).toHaveAttribute('data-oleander-ready', 'true');

  const boards = page.locator('.daylily-detail figure img, .reno-detail figure img, .expression-encounter figure img');
  expect(await boards.count()).toBeGreaterThan(10);

  const measurements = await boards.evaluateAll((images) => images.map((img) => {
    const rect = img.getBoundingClientRect();
    return {
      src: img.getAttribute('src'),
      sourceRatio: img.naturalWidth / img.naturalHeight,
      renderedRatio: rect.width / rect.height,
      objectFit: getComputedStyle(img).objectFit,
      transform: getComputedStyle(img).transform
    };
  }));

  for (const item of measurements) {
    const relativeRatioDelta = Math.abs(item.sourceRatio - item.renderedRatio) / item.sourceRatio;
    expect(relativeRatioDelta, `${item.src} changed its source proportion`).toBeLessThan(0.02);
    expect(item.objectFit, `${item.src} must remain complete`).toBe('contain');
    expect(item.transform, `${item.src} must not be scale-softened`).toBe('none');
  }

  const first = boards.first();
  await first.scrollIntoViewIfNeeded();
  await first.click();
  await expect(page.locator('.work-viewer')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('.work-viewer')).toBeHidden();
  await expect(first).toBeFocused();
});
