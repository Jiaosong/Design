const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '.',
  testMatch: 'c04-app-v12-browser.spec.js',
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  reporter: [
    ['list'],
    ['html', { outputFolder: '../playwright-report/c04-app-v12', open: 'never' }]
  ],
  outputDir: '../test-results/c04-app-v12',
  use: {
    baseURL: 'http://127.0.0.1:4174',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  },
  projects: [
    {
      name: 'chromium-desktop-c04',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 1000 } }
    },
    {
      name: 'chromium-mobile-c04',
      use: { ...devices['Pixel 7'], viewport: { width: 390, height: 844 } }
    }
  ],
  webServer: {
    command: 'STATIC_ROOT=.. PORT=4174 node serve-static-root.mjs',
    url: 'http://127.0.0.1:4174/05-cases/c04-qingjiang-stone-book/digital-currentization/app-game-map-v1.2/C04_QINGJIANG_APP_GAME_MAP_v1_2_PORTABLE.html',
    reuseExistingServer: true,
    timeout: 30_000
  }
});
