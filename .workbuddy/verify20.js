const { chromium } = require('playwright');
(async () => {
  const file = 'file:///C:/Users/lenovo/Desktop/test2/ai-daily-dashboard/index.html';
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto(file);
  await page.waitForTimeout(700);
  // 点击「精选」标签 -> 板块分布数字应联动，--bw 同步
  await page.click('.hero-tab[data-scope="featured"]');
  await page.waitForTimeout(500);
  const bw = await page.evaluate(() =>
    Array.from(document.querySelectorAll('.titem')).map(li => li.getAttribute('data-board') + ':' + li.style.getPropertyValue('--bw'))
  );
  console.log('--bw after featured filter:', bw.join(' | '));
  const dp = await page.evaluate(() => document.getElementById('densityBox').style.getPropertyValue('--dp'));
  console.log('--dp:', dp);
  await page.screenshot({ path: 'C:/Users/lenovo/Desktop/test2/.workbuddy/shots/r20-featured.png' });
  await browser.close();
})();
