const { chromium } = require('playwright');
(async () => {
  const file = 'file:///C:/Users/lenovo/Desktop/test2/ai-daily-dashboard/index.html';
  const browser = await chromium.launch({ channel: 'msedge' });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto(file);
  await page.waitForTimeout(800);
  const data = await page.evaluate(() => {
    const panel = document.querySelector('.panel');
    const out = { sections: [], gap: getComputedStyle(panel).gap, pad: getComputedStyle(panel).padding };
    Array.from(panel.children).forEach(ch => {
      const r = ch.getBoundingClientRect();
      const cs = getComputedStyle(ch);
      out.sections.push({ cls: ch.className || ch.tagName, y: Math.round(r.y), h: Math.round(r.height), mb: cs.marginBottom });
    });
    const pr = panel.getBoundingClientRect();
    out.panel = { y: Math.round(pr.y), h: Math.round(pr.height) };
    const pg = document.querySelector('.progress').getBoundingClientRect();
    out.progressBottom = Math.round(pg.bottom);
    return out;
  });
  console.log(JSON.stringify(data, null, 1));
  await browser.close();
})();
