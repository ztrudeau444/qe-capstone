/**
 * Week 3 — accessibility audit driven from Playwright.
 *
 * An automated audit covers roughly a third of WCAG success criteria (Deque
 * measured 57% of issue volume — a different metric). It cannot tell you
 * whether a focus order makes sense or whether an alt text is *useful*. Treat a
 * clean axe run as a floor, not a pass — Week 3 §5.4.
 *
 *   npm i -D @playwright/test @axe-core/playwright
 *   npx playwright test quality/accessibility/axe-audit.js
 */
const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const BASE = process.env.BASE_URL || 'http://localhost:8080';

const PAGES = [
  { name: 'home', path: '/' },
  { name: 'login', path: '/login' },
  { name: 'items', path: '/items' },
];

for (const page of PAGES) {
  test(`${page.name} has no critical or serious accessibility violations`, async ({ page: p }) => {
    await p.goto(`${BASE}${page.path}`);

    const results = await new AxeBuilder({ page: p })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();

    const blocking = results.violations.filter(
      (v) => v.impact === 'critical' || v.impact === 'serious'
    );

    // Print something a human can act on, not a wall of JSON.
    for (const v of blocking) {
      console.log(`[${v.impact}] ${v.id} — ${v.help}`);
      console.log(`   ${v.helpUrl}`);
      for (const node of v.nodes.slice(0, 3)) {
        console.log(`   at: ${node.target.join(' ')}`);
      }
    }

    expect(blocking, `${blocking.length} blocking violation(s) on ${page.name}`).toEqual([]);
  });
}
