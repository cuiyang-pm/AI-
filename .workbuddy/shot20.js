const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const file = 'file:///' + path.resolve('C:/Users/lenovo/Desktop/test2/ai-daily-dashboard/index.html').replace(/\\/g, '/');
  const browser = await chromium.launch({ channel: 'msedge' });
  const errors = [];

  // 桌面 1600x900
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
  await page.goto(file);
  await page.waitForTimeout(900);
  await page.screenshot({ path: 'C:/Users/lenovo/Desktop/test2/.workbuddy/shots/r20-desktop.png' });

  // 已读态：点 3 张卡片的标记按钮 → 底部进度条 scaleX(1) + 印章点亮
  await page.click('.news[data-card="1"] .done-btn');
  await page.click('.news[data-card="2"] .done-btn');
  await page.click('.news[data-card="3"] .done-btn');
  await page.waitForTimeout(800);
  await page.screenshot({ path: 'C:/Users/lenovo/Desktop/test2/.workbuddy/shots/r20-done.png' });

  // 溢出检查（桌面）
  const overflow = await page.evaluate(() => {
    const doc = document.documentElement;
    return { sw: doc.scrollWidth, cw: window.innerWidth };
  });
  console.log('desktop overflow check:', JSON.stringify(overflow));

  // 375px 移动端
  const m = await browser.newPage({ viewport: { width: 375, height: 812 } });
  m.on('pageerror', e => errors.push('m pageerror: ' + e.message));
  await m.goto(file);
  await m.waitForTimeout(900);
  const mOverflow = await m.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  console.log('375px horizontal overflow px:', mOverflow);
  await m.screenshot({ path: 'C:/Users/lenovo/Desktop/test2/.workbuddy/shots/r20-375.png', fullPage: false });

  // 375px 滚到面板区
  await m.evaluate(() => { const p = document.querySelector('.right'); if (p) p.scrollIntoView(); });
  await m.waitForTimeout(500);
  await m.screenshot({ path: 'C:/Users/lenovo/Desktop/test2/.workbuddy/shots/r20-375-panel.png' });

  console.log('errors:', errors.length ? errors : 'none');
  await browser.close();
})();
