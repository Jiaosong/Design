const { test, expect } = require('@playwright/test');

test('portfolio separates presentation crops from complete boards', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  await page.goto('/');
  await expect(page.locator('html')).toHaveAttribute('data-oleander-ready', 'true');
  await expect(page.locator('html')).toHaveAttribute('data-portfolio-framework', 'ready');
  await expect(page.locator('html')).toHaveAttribute('data-portfolio-crops', 'ready');

  const boards = page.locator('.daylily-chapter figure img, .reno-chapter figure img');
  expect(await boards.count()).toBeGreaterThan(10);

  const boardMeasurements = await boards.evaluateAll((images) => images.map((img) => {
    const rect = img.getBoundingClientRect();
    return {
      src: img.getAttribute('src'),
      sourceRatio: img.naturalWidth / img.naturalHeight,
      renderedRatio: rect.width / rect.height,
      objectFit: getComputedStyle(img).objectFit,
      transform: getComputedStyle(img).transform
    };
  }));

  for (const item of boardMeasurements) {
    const relativeRatioDelta = Math.abs(item.sourceRatio - item.renderedRatio) / item.sourceRatio;
    expect(relativeRatioDelta, `${item.src} changed its source proportion`).toBeLessThan(0.02);
    expect(item.objectFit, `${item.src} must remain complete`).toBe('contain');
    expect(item.transform, `${item.src} must not be scale-softened`).toBe('none');
  }

  const crops = page.locator('.expression-encounter figure img, .daylily-opening__image img, .reno-opening__image img');
  await expect(crops).toHaveCount(4);
  const cropMeasurements = await crops.evaluateAll((images) => images.map((img) => {
    const rect = img.getBoundingClientRect();
    return {
      src: img.getAttribute('src'),
      objectFit: getComputedStyle(img).objectFit,
      transform: getComputedStyle(img).transform,
      width: rect.width,
      height: rect.height
    };
  }));

  for (const item of cropMeasurements) {
    expect(item.objectFit, `${item.src} should act as an editorial crop`).toBe('cover');
    expect(item.transform, `${item.src} crop must stay sharp`).toBe('none');
    expect(item.width).toBeGreaterThan(200);
    expect(item.height).toBeGreaterThan(160);
  }

  const firstCrop = crops.first();
  await firstCrop.scrollIntoViewIfNeeded();
  await firstCrop.click();
  await expect(page.locator('.work-viewer')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('.work-viewer')).toBeHidden();
  await expect(firstCrop).toBeFocused();

  const firstBoard = boards.first();
  await firstBoard.scrollIntoViewIfNeeded();
  await firstBoard.click();
  await expect(page.locator('.work-viewer')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('.work-viewer')).toBeHidden();
  await expect(firstBoard).toBeFocused();
});
