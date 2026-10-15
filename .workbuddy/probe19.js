const { chromium } = require('playwright');
(async () => {
  const file = 'file:///C:/Users/lenovo/Desktop/test2/.workbuddy/tmp-r19.html';
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto(file);
  await page.waitForTimeout(800);
  const boxes = await page.evaluate(() => {
    const b = sel => { const el = document.querySelector(sel); if (!el) return null; const r = el.getBoundingClientRect(); return { y: Math.round(r.y), h: Math.round(r.height) }; };
    return { progress: b('.progress'), panel: b('.panel'), hero: b('.hero') };
  });
  console.log('R19 baseline:', JSON.stringify(boxes));
  await browser.close();
})();
