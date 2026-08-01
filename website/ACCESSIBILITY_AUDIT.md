# OLEANDER Website Accessibility Audit

Version anchor: `main@76a502d406212472ef6f152def64904e795c0062`
Audit branch: `agent/e2-web-audit`
Audit date: `2026-07-31`

## Evidence levels

| Level | Scope | Current status |
| --- | --- | --- |
| E1 / source review | HTML, CSS, JavaScript, ARIA references, anchors, image alternatives, reduced-motion declaration | Passed locally |
| E2 / automated browser tests | Playwright + axe in Chromium, Firefox, WebKit, desktop/mobile viewports, keyboard, reduced motion, 200% reflow equivalent | Configured; not executed in the current environment because browser downloads returned empty archives |
| E3 / human verification | Screen reader, real browser zoom, touch exploration, visual reading rhythm, real form delivery/privacy | Not completed |

Do not interpret E1 as proof that E2 or E3 passed.

## Implemented corrections

1. Added roving focus, arrow keys, Home / End, `aria-controls`, and `tabpanel` relationships to the three tab systems.
2. Added `aria-current="location"` updates to the primary navigation.
3. Added fixed-header offsets through `scroll-padding-top` and `scroll-margin-top`.
4. Associated form errors with their fields, exposed `aria-invalid`, and focused the first invalid control.
5. Expanded the home brand link’s accessible name to include OLEANDER and 刘旋 / LIU XUAN.
6. Added local-first `@font-face` declarations with system fallbacks and no remote font request.
7. Added Escape close and trigger-focus restoration to the mobile menu.
8. Added visible and assistive-technology-readable values to both range controls.

## Automated test contract

Install dependencies:

```sh
npm install
npx playwright install chromium firefox webkit
```

Run E1:

```sh
npm run test:e1
```

Run E2:

```sh
npm run test:e2
```

The Playwright configuration defines 36 test/project combinations across:

- Chromium desktop, 1440 × 1000
- Firefox desktop, 1440 × 1000
- WebKit desktop, 1440 × 1000
- Chromium mobile, Pixel 7 profile

The checks cover axe critical/serious findings, tab keyboard behavior, form error focus, range feedback, anchor offsets, 200% reflow equivalent, reduced motion, and mobile-menu focus restoration.

## E3 manual verification still required

- NVDA + Firefox or Chrome on Windows
- VoiceOver + Safari on macOS and iOS
- Actual browser zoom at 200%, including text clipping and fixed-header overlap
- Keyboard-only reading order through all dynamically inserted evidence layers
- Touch target and swipe-order review on a physical phone
- Contact backend, privacy notice, retention, and real-delivery verification
- Final visual QA for Chinese fallback fonts on target operating systems

## Evidence boundary

This audit changes interface behavior and test coverage only. It does not verify the project claims, prove public participation or implementation, replace cultural/professional review, or authorize public release.
