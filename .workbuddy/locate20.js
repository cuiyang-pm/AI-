const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const file = 'file:///' + path.resolve('C:/Users/lenovo/Desktop/test2/ai-daily-dashboard/index.html').replace(/\\/g, '/');
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto(file);
  await page.waitForTimeout(800);
  await page.click('.news[data-card="2"] .done-btn');
  await page.waitForTimeout(700);
  const boxes = await page.evaluate(() => {
    const b = sel => { const el = document.querySelector(sel); if (!el) return null; const r = el.getBoundingClientRect(); return { x: r.x, y: r.y, w: r.width, h: r.height }; };
    return {
      card2: b('.news[data-card="2"]'),
      progress: b('.progress'),
      stampArea: b('.pinfo .pt'),
      panel: b('.panel'),
    };
  });
  console.log(JSON.stringify(boxes, null, 1));
  await browser.close();
})();
