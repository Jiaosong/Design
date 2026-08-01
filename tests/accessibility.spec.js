const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test.beforeEach(async ({ page }) => {
  await page.goto('/');
});

test('has no automatically detectable serious accessibility violations', async ({ page }) => {
  const results = await new AxeBuilder({ page }).analyze();
  const violations = results.violations.filter(({ impact }) => ['critical', 'serious'].includes(impact));
  expect(violations, JSON.stringify(violations, null, 2)).toEqual([]);
});

test('project tabs expose state and support arrow, Home, and End keys', async ({ page }) => {
  const tabs = page.getByRole('tablist', { name: '项目阅读模式' });
  const relation = tabs.getByRole('tab', { name: '按关系' });
  const practice = tabs.getByRole('tab', { name: '按实践' });
  const archive = tabs.getByRole('tab', { name: '开放档案' });

  await relation.focus();
  await page.keyboard.press('ArrowRight');
  await expect(practice).toBeFocused();
  await expect(practice).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#project-panel-practice')).toBeVisible();

  await page.keyboard.press('End');
  await expect(archive).toBeFocused();
  await expect(archive).toHaveAttribute('aria-selected', 'true');

  await page.keyboard.press('Home');
  await expect(relation).toBeFocused();
  await expect(relation).toHaveAttribute('aria-selected', 'true');
});

test('relationship and practice tabs keep the active tab linked to the panel', async ({ page }) => {
  const readingTabs = page.getByRole('tablist', { name: '关系命题状态' });
  const current = readingTabs.getByRole('tab', { name: 'CURRENT' });
  await current.focus();
  await page.keyboard.press('ArrowRight');
  await expect(readingTabs.getByRole('tab', { name: 'INTENDED' })).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#reading-panel')).toHaveAttribute('aria-labelledby', 'reading-tab-intended');

  const practiceTabs = page.getByRole('tablist', { name: 'Oleander 六阶段实践方法' });
  const read = practiceTabs.getByRole('tab', { name: /READ/ });
  await read.focus();
  await page.keyboard.press('End');
  await expect(practiceTabs.getByRole('tab', { name: /CONTINUE/ })).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#practice-panel')).toHaveAttribute('aria-labelledby', 'practice-tab-continue');
});

test('form errors are announced, associated, and focus the first invalid field', async ({ page }) => {
  await page.locator('#contact').scrollIntoViewIfNeeded();
  await page.locator('[data-form-step="1"] [data-next-step]').click();

  const firstPurpose = page.locator('input[name="purpose"]').first();
  await expect(firstPurpose).toBeFocused();
  await expect(firstPurpose).toHaveAttribute('aria-invalid', 'true');
  await expect(page.locator('#purpose-error')).toBeVisible();

  await firstPurpose.check();
  await expect(firstPurpose).not.toHaveAttribute('aria-invalid', 'true');
  await page.locator('[data-form-step="1"] [data-next-step]').click();
  await page.locator('[name="object"]').fill('太短');
  await page.locator('[data-form-step="2"] [data-next-step]').click();
  await expect(page.locator('[name="object"]')).toBeFocused();
  await expect(page.locator('#object-error')).toBeVisible();
});

test('range controls expose readable live values', async ({ page }) => {
  const density = page.locator('#weave-density');
  await density.fill('80');
  await expect(page.locator('#weave-density-value')).toHaveText('80%');
  await expect(density).toHaveAttribute('aria-valuetext', '关系织场密度 80%');

  const tension = page.locator('#reading-tension');
  await tension.fill('65');
  await expect(page.locator('#reading-tension-value')).toHaveText('65%');
  await expect(tension).toHaveAttribute('aria-valuetext', '关系张力 65%');
});

test('fixed-header anchors retain a visible offset', async ({ page }) => {
  await page.locator('a[href="#practice"]').first().click();
  await expect.poll(async () => page.locator('#practice').evaluate((node) => node.getBoundingClientRect().top)).toBeGreaterThanOrEqual(65);
});

test('200 percent reflow equivalent has no page-level horizontal overflow', async ({ page }) => {
  await page.setViewportSize({ width: 640, height: 720 });
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});

test.describe('reduced motion', () => {
  test.use({ reducedMotion: 'reduce' });

  test('reveals content without motion-dependent access', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('.reveal').first()).toHaveCSS('opacity', '1');
    const duration = await page.locator('.reveal').first().evaluate((node) => getComputedStyle(node).transitionDuration);
    expect(duration).toMatch(/0\.0*1m?s|0s/);
  });
});

test.describe('mobile menu', () => {
  test.use({ viewport: { width: 390, height: 844 }, isMobile: true });

  test('Escape closes the menu and restores focus to its trigger', async ({ page }) => {
    const toggle = page.getByRole('button', { name: '菜单' });
    await toggle.click();
    await expect(toggle).toHaveAttribute('aria-expanded', 'true');
    await expect(page.locator('#site-nav a').first()).toBeFocused();
    await page.keyboard.press('Escape');
    await expect(toggle).toHaveAttribute('aria-expanded', 'false');
    await expect(toggle).toBeFocused();
  });
});
