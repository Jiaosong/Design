const { test, expect } = require('@playwright/test');

test('capability-driven XJ01 project display preserves open evidence boundaries', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  await page.goto('/project.html?project=xj01');
  await expect(page.locator('html')).toHaveAttribute('data-project-display', 'ready');

  await expect(page.locator('[data-capability="identity"]')).toBeVisible();
  await expect(page.locator('[data-capability="directions"]')).toBeVisible();
  await expect(page.locator('[data-capability="materials"]')).toBeVisible();
  await expect(page.locator('[data-capability="evidence"]')).toBeVisible();

  const capabilityCount = await page.locator('[data-capability]').count();
  expect(capabilityCount).toBeGreaterThanOrEqual(10);

  await expect(page.getByText('VE06_OPEN', { exact: false })).toBeVisible();
  await expect(page.getByText('READY_NOT_EXECUTED', { exact: false })).toBeVisible();
  await expect(page.getByText('NOT_PUBLIC_RELEASE', { exact: true })).toBeVisible();

  const comparisonImages = page.locator('[data-artifact-id^="A1-WHOLE-"] img, [data-artifact-id^="A1-MID-"] img');
  expect(await comparisonImages.count()).toBeGreaterThanOrEqual(4);
  for (const fit of await comparisonImages.evaluateAll((imgs) => imgs.map((img) => getComputedStyle(img).objectFit))) {
    expect(fit).toBe('contain');
  }

  const diagnostic = page.locator('.project-diagnostic').first();
  if (await diagnostic.count()) {
    await expect(diagnostic).not.toHaveAttribute('open', '');
  }
});

test('project display ordering is driven by project plan instead of universal page numbering', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  const response = await page.request.get('/data/projects/xj01.json');
  expect(response.ok()).toBeTruthy();
  const data = await response.json();

  expect(data.display.principle).toContain('not fixed page template');
  expect(data.display.minimum_capabilities.length).toBeGreaterThanOrEqual(5);
  expect(data.display.plan.length).toBeGreaterThanOrEqual(8);
  expect(data.display.plan.every((item) => 'capability_id' in item)).toBeTruthy();
});
