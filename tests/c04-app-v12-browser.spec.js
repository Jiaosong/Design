const { test, expect } = require('@playwright/test');

const TARGET = '/05-cases/c04-qingjiang-stone-book/digital-currentization/app-game-map-v1.2/C04_QINGJIANG_APP_GAME_MAP_v1_2_PORTABLE.html';

test.beforeEach(async ({ page }) => {
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(String(error)));
  await page.goto(TARGET);
  await page.waitForLoadState('load');
  await expect(page.locator('.view.active')).toHaveAttribute('data-view', 'today');
  expect(pageErrors).toEqual([]);
});

test('five views and return/service state execute in the actual browser runtime', async ({ page }) => {
  const navCases = [
    ['route', '#route'],
    ['read', '#read'],
    ['book', '#book']
  ];

  for (const [view, hash] of navCases) {
    await page.locator(`.nav [data-nav="${view}"]`).click();
    await expect(page.locator(`.view[data-view="${view}"]`)).toBeVisible();
    await expect(page).toHaveURL(new RegExp(`${hash.replace('#', '\\#')}$`));
  }

  await page.locator('.head [data-nav="service"]').click();
  await expect(page.locator('.view[data-view="service"]')).toBeVisible();
  await expect(page.locator('.status b')).toHaveText('UNKNOWN / 未确认');
  await expect(page.locator('.status em')).toHaveText('FAIL-CLOSED');
});

test('route mode and travel focus update the rendered map state', async ({ page }) => {
  await page.locator('.nav [data-nav="route"]').click();

  await page.locator('[data-rmode="return"]').click();
  await expect(page.locator('#map')).toHaveAttribute('data-mode', 'return');
  await expect(page.locator('#mk')).toHaveText('RETURN / 返回');
  await expect(page.locator('#mt')).toContainText('任何时候都能退出探索');

  await page.locator('[data-focus="walk"]').click();
  await expect(page.locator('#map')).toHaveAttribute('data-focus', 'walk');
  await expect(page.locator('[data-focus="walk"]')).toHaveClass(/active/);
});

test('imprint dialog can persist a page to My Book via localStorage', async ({ page }) => {
  await page.locator('.nav [data-nav="read"]').click();
  const first = page.locator('.imprint[data-imprint="R01"]');
  await expect(first).toBeVisible();
  await first.click();

  const dialog = page.locator('#dlg');
  await expect(dialog).toBeVisible();
  await expect(dialog.locator('h2')).toHaveText('红岩嘴');
  await dialog.locator('[data-save]').click();

  await expect(page.locator('.view[data-view="book"]')).toBeVisible();
  const stored = await page.evaluate(() => JSON.parse(localStorage.getItem('qj_memories') || '[]'));
  expect(stored.length).toBeGreaterThan(0);
  expect(stored[0].scene).toContain('R01 红岩嘴');
  expect(stored[0].action).toBe('READ / 读');
});

test('My Book form writes and clears local-only memory', async ({ page }) => {
  await page.locator('.nav [data-nav="book"]').click();
  await page.locator('#scene').selectOption({ label: 'R06 河谷观察' });
  await page.locator('#action').selectOption({ label: 'WRITE / 写' });
  await page.locator('#note').fill('浏览器运行时验证：本机记忆记录。');
  await page.locator('#revisit').check();
  await page.locator('#form .primary').click();

  const stored = await page.evaluate(() => JSON.parse(localStorage.getItem('qj_memories') || '[]'));
  expect(stored[0]).toMatchObject({
    scene: 'R06 河谷观察',
    action: 'WRITE / 写',
    note: '浏览器运行时验证：本机记忆记录。',
    revisit: true
  });
  await expect(page.locator('#mem article').first()).toContainText('浏览器运行时验证');

  await page.locator('#clear').click();
  expect(await page.evaluate(() => localStorage.getItem('qj_memories'))).toBeNull();
  await expect(page.locator('#mem article')).toHaveCount(4);
});

test('print fallback switches to route before invoking browser print', async ({ page }) => {
  await page.locator('.head [data-nav="service"]').click();
  await page.evaluate(() => {
    window.__c04PrintCalls = 0;
    window.print = () => { window.__c04PrintCalls += 1; };
  });

  await page.locator('#print').click();
  await expect(page.locator('.view[data-view="route"]')).toBeVisible();
  await expect.poll(() => page.evaluate(() => window.__c04PrintCalls)).toBe(1);
});

test('current runtime has no page-level horizontal overflow at the configured viewport', async ({ page }) => {
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  expect(overflow).toBeLessThanOrEqual(1);
});
