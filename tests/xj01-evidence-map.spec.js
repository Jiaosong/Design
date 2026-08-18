const { test, expect } = require('@playwright/test');

test('XJ01 desktop VE06 VE07 matrices expose direction and state mapping', async ({ page }, testInfo) => {
  test.skip(testInfo.project.name !== 'chromium-desktop');
  await page.goto('/project.html?project=xj01');
  await expect(page.locator('html')).toHaveAttribute('data-pro04', 'ready');

  const environment = page.locator('#p04 [data-evidence-map="environment"]');
  const lifecycle = page.locator('#p05 [data-evidence-map="lifecycle"]');
  await expect(environment).toContainText('D02 / TOP');
  await expect(environment).toContainText('D03 / BOTTOM');
  await expect(environment).toContainText('Neutral Studio');
  await expect(environment).toContainText('Soft Interior');
  await expect(environment).toContainText('Wet-zone');

  await expect(lifecycle).toContainText('D02 / TOP');
  await expect(lifecycle).toContainText('D03 / BOTTOM');
  await expect(lifecycle).toContainText('Day 0');
  await expect(lifecycle).toContainText('Dirty-wiped');
  await expect(lifecycle).toContainText('PU Aged');
});