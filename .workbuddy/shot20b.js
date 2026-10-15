const { chromium } = require('playwright');
(async () => {
  const file = 'file:///C:/Users/lenovo/Desktop/test2/ai-daily-dashboard/index.html';
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto(file);
  await page.waitForTimeout(800);
  await page.evaluate(() => {
    document.querySelectorAll('.news .done-btn').forEach(b => b.click());
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(800);
  const box = await page.evaluate(() => {
    const r = document.querySelector('.news[data-card="2"]').getBoundingClientRect();
    const d = document.querySelector('.main::before') ? 1 : 1;
    return { x: r.x, y: r.y, w: r.width, h: r.height };
  });
  await page.screenshot({ path: 'C:/Users/lenovo/Desktop/test2/.workbuddy/shots/r20-done.png' });
  console.log('card2 box:', JSON.stringify(box));
  await browser.close();
})();
